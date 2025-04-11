"""PEP-517 Build Backend."""

import tempfile
from pathlib import Path
from typing import Any

from pup517 import pkg


def build_sdist(sdist_directory: str, config_settings: dict[str, Any] | None = None) -> str:
    """Build the source distribution.

    Args:
        sdist_directory: The directory in which to write the source distribution
            tarball.
        config_settings: Command line settings for build.

    Returns:
        The basename of the source tarball written to sdist_directory.
    """
    del config_settings
    package = pkg.Pkg.from_cwd()
    return package.export_sdist(Path(sdist_directory)).name


def build_wheel(
    wheel_directory: str,
    config_settings: dict[str, Any] | None = None,
    metadata_directory: str | None = None,
) -> str:
    """Build a wheel.

    Args:
        sdist_directory: The directory in which to write the source distribution
            tarball.
        config_settings: Command line settings for build.
        metadata_directory: Per PEP-517, we can ignore unless we implement
            prepare_metadata_for_build_wheel.

    Returns:
        The basename of the wheel written to wheel_directory.
    """
    del config_settings
    del metadata_directory
    package = pkg.Pkg.from_cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        builder = pkg.PkgBuilder(package, Path(tmpdir))
        builder.build()
        return builder.export_wheel(Path(wheel_directory)).name


def get_requires_for_build_wheel(config_settings: dict[str, Any] | None = None):
    """Get the list of requirements to run build_wheel.

    Args:
        config_settings: Command line settings for build.

    Returns:
        A list of PEP-508 dependencies we need to build the wheel.
    """
    del config_settings
    package = pkg.Pkg.from_cwd()
    return package.get_build_requirements()
