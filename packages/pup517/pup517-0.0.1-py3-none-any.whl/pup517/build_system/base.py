from pathlib import Path
from typing import Any


class BuildSystem:
    """Base class for all build systems.

    Build systems must conform to this API.
    """

    def __init__(self, pyproject_config: dict[str, Any]):
        """Create the build system.  Loaded config is provided."""
        del pyproject_config

    def get_requirements(self) -> list[str]:
        """List the Python packages needed to build the source."""
        return []

    def configure(self, srcdir: Path, workdir: Path) -> None:
        """Configure the source (e.g., run ./configure or cmake, etc.).

        Fundamentally, configure is not much different from compile, but we split the
        two phases into separate functions to make inheritance patterns easier.  For
        example, this enables a base "Makefile" build system, and a CMake build system
        can extend it by running CMake to generate the Makefile during configure.

        Args:
            srcdir: The directory which the sources were dowloaded to.
            workdir: A temporary directory the build system can use to store
                intermediate artifacts.
        """

    def compile(self, srcdir: Path, workdir: Path) -> None:
        """Compile the source (e.g., run "make" or "ninja", etc.).

        Args:
            srcdir: The directory which the sources were dowloaded to.
            workdir: A temporary directory the build system can use to store
                intermediate artifacts.
        """

    def install(self, srcdir: Path, workdir: Path, bindir: Path) -> None:
        """Install the built programs.

        Args:
            srcdir: The directory which the sources were dowloaded to.
            workdir: A temporary directory the build system can use to store
                intermediate artifacts.
            bindir: A directory in which binaries should be installed.
        """
