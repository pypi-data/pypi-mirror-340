"""Fetch the sources."""

import abc
import hashlib
import io
import subprocess
import tarfile
import urllib.request
from pathlib import Path
from typing import Any

import pydantic


class FetchError(Exception):
    """Raised for an issue fetching the archive."""


class BaseSrc(abc.ABC, pydantic.BaseModel):
    type: str
    destdir: Path = Path(".")

    def get_requirements(self) -> list[str]:
        """List the Python packages needed to download and extract the source."""
        return []

    @abc.abstractmethod
    def fetch(self, base_dir: Path) -> None:
        """Download the sources.

        Args:
            base_dir: The base directory in which destdir resides.
        """
        raise NotImplementedError


class GitSrc(BaseSrc):
    repo: str
    commit: str

    def fetch(self, base_dir: Path) -> None:
        destdir = base_dir / self.destdir
        destdir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "-c", "init.defaultBranch=main", "init"],
            check=True,
            cwd=destdir,
        )
        subprocess.run(
            ["git", "fetch", self.repo, self.commit],
            check=True,
            cwd=destdir,
        )
        subprocess.run(
            ["git", "-c", "advice.detachedHead=false", "checkout", self.commit],
            check=True,
            cwd=destdir,
        )


class HttpArchiveSrc(BaseSrc):
    url: str
    sha256: str
    strip_components: int = 0

    def fetch(self, base_dir: Path) -> None:
        with urllib.request.urlopen(self.url) as f:  # noqa: S310
            body = f.read()

        sha256 = hashlib.sha256(body).hexdigest()
        if sha256 != self.sha256:
            msg = f"While fetching {self.url}, got {sha256=}, expected {self.sha256}."
            raise FetchError(msg)

        with tarfile.open(fileobj=io.BytesIO(body)) as tar:
            while member := tar.next():
                path = Path(member.name)
                if path.is_absolute():
                    msg = f"Tarball {self.url} has members with absolute paths.  Do better."
                    raise FetchError(msg)
                dest_path = base_dir.joinpath(*path.parts[self.strip_components :]).resolve()
                if not dest_path.is_relative_to(base_dir):
                    continue
                if dest_path == base_dir:
                    continue
                member.name = dest_path.name
                tar.extract(member, dest_path.parent)


SRC_TYPES: dict[str, type[BaseSrc]] = {
    "git": GitSrc,
    "http_archive": HttpArchiveSrc,
}


def get_fetchers_from_config(pyproject_config: dict[str, Any]) -> list[BaseSrc]:
    """Construct fetcher objects from the pyproject.toml.

    Args:
        pyproject_config: The loaded config.

    Returns:
        A list of fetcher objects.
    """
    result = []
    srcuris = pyproject_config.get("pup517", {}).get("srcuris", [])

    for srcuri in srcuris:
        fetcher_cls = SRC_TYPES[srcuri["type"]]
        result.append(fetcher_cls.model_validate(srcuri, strict=True))

    return result
