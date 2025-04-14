"""Package information."""

from __future__ import annotations

import contextlib
import dataclasses
import functools
import importlib
import io
import os
import re
import subprocess
import tarfile
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

import pydantic
from wheel import wheelfile

from pup517 import fetch

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

    from pup517.build_system import base


def serialize_wheel_metadata(metadata: Mapping[str, str | list[str]]) -> str:
    values: list[tuple[str, str]] = []
    for key, value in metadata.items():
        if isinstance(value, str):
            value = [value]
        values.extend((key, v) for v in value)
    return "".join(f"{k}: {v.replace('\n', '\n       |')}\n" for k, v in values)


class Hooks(pydantic.BaseModel):
    prepare: list[str] = ["default"]
    configure: list[str] = ["default"]
    compile: list[str] = ["default"]
    install: list[str] = ["default"]


class BuildSystemConfig(pydantic.BaseModel):
    backend: str = "pup517.build_system.base"


class LauncherConfig(pydantic.BaseModel):
    name: str
    path: str


class PupConfig(pydantic.BaseModel):
    build_system: BuildSystemConfig = pydantic.Field(default_factory=BuildSystemConfig, alias="build-system")
    hooks: Hooks = Hooks()
    launchers: list[LauncherConfig] = pydantic.Field(default_factory=list)


@dataclasses.dataclass
class PkgBuilder:
    pkg: Pkg
    build_dir: Path

    @property
    def src_dir(self):
        return self.build_dir / "src"

    @property
    def work_dir(self):
        return self.build_dir / "work"

    @property
    def install_dir(self):
        return self.build_dir / "install"

    @property
    def data_dir(self):
        return self.install_dir / f"{self.pkg.distribution}-{self.pkg.version}.data"

    @property
    def bin_dir(self):
        return self.data_dir / "scripts"

    @property
    def env(self) -> dict[str, str]:
        """Default environment variables exposed by this project."""
        return {
            "PUP_NAME": self.pkg.name,
            "PUP_VERSION": self.pkg.version,
            "PUP_WORKDIR": str(self.work_dir),
        }

    @contextlib.contextmanager
    def _run_hooks(self, hooks_list: list[str], cwd: Path, extra_env: dict[str, str] | None = None) -> Iterator[None]:
        env = os.environ.copy()
        env.update(self.env)
        if extra_env:
            env.update(extra_env)
        for hook in hooks_list:
            if hook == "default":
                yield
            else:
                subprocess.run(hook, shell=True, check=True, cwd=cwd, env=env)  # noqa: S602

    def phase_fetch(self) -> None:
        """Fetch all sources."""
        self.src_dir.mkdir(exist_ok=True, parents=True)
        for fetcher in self.pkg.fetchers:
            fetcher.fetch(self.src_dir)

    def phase_prepare(self) -> None:
        """Patch sources as required."""
        self.work_dir.mkdir(exist_ok=True, parents=True)
        with self._run_hooks(self.pkg.pup_config.hooks.prepare, cwd=self.src_dir):
            pass

    def phase_configure(self) -> None:
        """Configure sources to build."""
        with self._run_hooks(self.pkg.pup_config.hooks.configure, cwd=self.src_dir):
            self.pkg.build_system.configure(self.src_dir, self.work_dir)

    def phase_compile(self) -> None:
        """Compile sources to build."""
        with self._run_hooks(self.pkg.pup_config.hooks.compile, cwd=self.src_dir):
            self.pkg.build_system.compile(self.src_dir, self.work_dir)

    def phase_install(self) -> None:
        """Install binaries."""
        self.bin_dir.mkdir(exist_ok=True, parents=True)
        (self.data_dir / "data").mkdir(exist_ok=True, parents=True)

        with self._run_hooks(
            self.pkg.pup_config.hooks.install,
            cwd=self.src_dir,
            extra_env={
                "PUP_BINDIR": str(self.bin_dir),
                "PUP_DATADIR": str(self.data_dir / "data"),
            },
        ):
            self.pkg.build_system.install(self.src_dir, self.work_dir, self.bin_dir)

        # Generate launchers.
        for launcher in self.pkg.pup_config.launchers:
            launcher_path = self.bin_dir / launcher.name
            launcher_path.write_text(
                "#!/bin/sh\n"
                'if [ -z "${VIRTUAL_ENV}" ]; then\n'
                '  source "$(dirname "$0")/activate"\n'
                "fi\n"
                f'exec "{launcher.path.replace('"', r'\"')}" "$@"\n'
            )
            os.chmod(launcher_path, 0o755)  # noqa: S103

    def export_wheel_metadata(self) -> None:
        dist_info_dir = self.install_dir / f"{self.pkg.distribution}-{self.pkg.version}.dist-info"
        dist_info_dir.mkdir(exist_ok=True, parents=True)

        wheel_metadata = {
            "Wheel-Version": "1.0",
            "Generator": "pup517",
            "Root-Is-Purelib": "false",
            "Tag": "py3-none-manylinux1_x86_64",
        }
        (dist_info_dir / "WHEEL").write_text(serialize_wheel_metadata(wheel_metadata), encoding="utf-8")
        (dist_info_dir / "METADATA").write_text(serialize_wheel_metadata(self.pkg.metadata), encoding="utf-8")

    def build(self):
        """Execute all build phases."""
        self.phase_fetch()
        self.phase_prepare()
        self.phase_configure()
        self.phase_compile()
        self.phase_install()
        self.export_wheel_metadata()

    def export_wheel(self, wheel_dir: Path) -> Path:
        output_file = wheel_dir / f"{self.pkg.distribution}-{self.pkg.version}-py3-none-manylinux1_x86_64.whl"
        with wheelfile.WheelFile(output_file, "w") as wheel:
            for path in self.install_dir.rglob("*"):
                path = path.resolve(strict=True)
                if path.is_file():
                    wheel.write(str(path), arcname=str(path.relative_to(self.install_dir)))
        return output_file


@dataclasses.dataclass
class Pkg:
    pkg_dir: Path

    @classmethod
    def from_cwd(cls) -> Self:
        return cls(pkg_dir=Path.cwd())

    @functools.cached_property
    def pyproject_config(self) -> dict[str, Any]:
        with (self.pkg_dir / "pyproject.toml").open("rb") as f:
            return tomllib.load(f)

    @functools.cached_property
    def pup_config(self) -> PupConfig:
        return PupConfig.model_validate(self.pyproject_config.get("pup517", {}))

    @functools.cached_property
    def fetchers(self) -> list[fetch.BaseSrc]:
        return fetch.get_fetchers_from_config(self.pyproject_config)

    @property
    def name(self) -> str:
        return self.pyproject_config["project"]["name"]

    @property
    def distribution(self) -> str:
        """A version of the package name escaped for wheels."""
        return re.sub("[-_.]+", "_", self.name)

    @property
    def version(self) -> str:
        return self.pyproject_config["project"]["version"]

    @property
    def metadata(self) -> dict[str, str | list[str]]:
        """https://packaging.python.org/en/latest/specifications/core-metadata"""
        project_config = self.pyproject_config.get("project", {})
        return {
            "Metadata-Version": "2.4",
            "Name": self.name,
            "Version": self.version,
            "Requires-Dist": project_config.get("dependencies", []),
            "Classifier": project_config.get("classifiers", []),
            "Keywords": project_config.get("keywords", []),
        }

    @functools.cached_property
    def build_system(self) -> base.BuildSystem:
        module_name, _, member_name = self.pup_config.build_system.backend.partition(":")
        if not member_name:
            member_name = "BuildSystem"
        module = importlib.import_module(module_name)
        build_system_cls = getattr(module, member_name)
        return build_system_cls(pyproject_config=self.pyproject_config)

    def get_build_requirements(self) -> list[str]:
        result = []
        for fetcher in self.fetchers:
            result.extend(fetcher.get_requirements())
        result.extend(self.build_system.get_requirements())
        return result

    def export_sdist(self, sdist_dir: Path) -> Path:
        base_dir_name = f"{self.distribution}-{self.version}"
        sdist_path = sdist_dir / f"{base_dir_name}.tar.gz"
        core_metadata = serialize_wheel_metadata(self.metadata).encode("utf-8")

        with tarfile.open(sdist_path, "w:gz", format=tarfile.PAX_FORMAT) as sdist:
            sdist.add(self.pkg_dir / "pyproject.toml", f"{base_dir_name}/pyproject.toml")

            tar_info = tarfile.TarInfo(f"{base_dir_name}/PKG-INFO")
            tar_info.size = len(core_metadata)
            sdist.addfile(tar_info, io.BytesIO(core_metadata))

        return sdist_path
