import enum
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pydantic

from pup517.build_system import base


class Lang(str, enum.Enum):
    C = "c"
    CXX = "c++"


class Target(pydantic.BaseModel):
    lang: Lang
    bin: Path
    srcs: list[Path]


class BuildSystem(base.BuildSystem):
    """A simple build system which just takes a list of C/C++ sources.

    Some tools just have a few C/C++ sources to compile, and don't even need a
    a Makefile or other things.  This build system allows you to define targets
    which just take a list of sources.  For example:

    [[pup517.simple-cc.targets]]
    lang = "c"
    bin = "toolname"
    srcs = [ "toolname.c", "lib.c" ]
    """

    def __init__(self, pyproject_config: dict[str, Any]):
        config = pyproject_config.get("pup517", {}).get("simple-cc", {})
        self.targets = [Target.model_validate(x) for x in config.get("targets", [])]

    def get_requirements(self) -> list[str]:
        return ["pup-zig-bin", *super().get_requirements()]

    def compile(self, srcdir: Path, workdir: Path) -> None:
        for target in self.targets:
            sources = [srcdir / x for x in target.srcs]
            subprocess.run(
                [
                    "zig",
                    "cc",
                    "-target",
                    "x86_64-linux-musl",
                    *sources,
                    "-o",
                    workdir / target.bin,
                ],
                check=True,
            )

    def install(self, srcdir: Path, workdir: Path, bindir: Path) -> None:
        del srcdir
        for target in self.targets:
            shutil.copy2(workdir / target.bin, bindir / target.bin)
