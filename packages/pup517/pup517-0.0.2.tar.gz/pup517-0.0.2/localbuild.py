#!/usr/bin/env -S uv run --group localbuild

"""Helper script for in-repo builds.

This script exists to resolve the dependency graph of packages defined in this
repo, and execute local builds in the correct order with a local pypi server for
dependencies.
"""

import asyncio
import random
import sys
from pathlib import Path
from typing import Annotated, Optional

import aiohttp
import async_typer
import rich.console
import typer

from pup517 import pkg

console = rich.console.Console()
app = async_typer.AsyncTyper()
HERE = Path(__file__).resolve().parent


def _pop_buildable_pkg(
    pkg_dirs: dict[str, Path],
    pkg_deps: dict[str, set[str]],
) -> tuple[str, Path]:
    """Select a package that can be built and pop it.

    Args:
        pkg_dirs: A mapping of package names to their directories.
        pkg_deps: A mapping of package names to their dependencies.

    Returns:
        The name and directory of a package that can be built.
    """
    for pkg_name, deps in pkg_deps.items():
        if not deps:
            pkg_deps.pop(pkg_name)
            return pkg_name, pkg_dirs.pop(pkg_name)

    msg = "No buildable packages found."
    raise RuntimeError(msg)


async def _buildall(
    pkg_dirs: dict[str, Path],
    pkg_deps: dict[str, set[str]],
    wheel_dir: Path,
    pypi_server_url: str,
) -> None:
    """Build all packages in the correct order.

    Args:
        pkg_dirs: A mapping of package names to their directories.
        pkg_deps: A mapping of package names to their dependencies.
        wheel_dir: The directory to store built wheels.
        pypi_server_url: The URL of the local pypi server.
    """
    while pkg_dirs:
        pkg_name, pkg_dir = _pop_buildable_pkg(pkg_dirs, pkg_deps)

        console.print(f"Building {pkg_name}...")
        proc = await asyncio.create_subprocess_exec(
            "uv",
            "build",
            "--out-dir",
            str(wheel_dir),
            "--extra-index-url",
            pypi_server_url,
            cwd=pkg_dir,
        )
        await proc.wait()
        if proc.returncode != 0:
            msg = f"Failed to build {pkg_name}."
            raise RuntimeError(msg)

        for dep in pkg_deps.values():
            dep.discard(pkg_name)


@app.async_command()
async def main(
    packages: Annotated[list[Path], typer.Argument(help="The packages to build.")],
    wheel_dir: Annotated[Path, typer.Option("--dist-dir", "-d", help="Directory to store built wheels.")] = HERE
    / "dist",
    port: Annotated[Optional[int], typer.Option("--port", "-p", help="Port for the local pypi server.")] = None,  # noqa: UP007
) -> None:
    """Build the specified packages."""
    pkg_dirs: dict[str, Path] = {}
    pkg_deps: dict[str, set[str]] = {}

    for package_dir in packages:
        if package_dir.resolve() == HERE:
            pkg_dirs["pup517"] = HERE
            pkg_deps["pup517"] = set()
            continue

        pup = pkg.Pkg(pkg_dir=package_dir)
        pkg_dirs[pup.name] = package_dir
        pkg_deps[pup.name] = {"pup517", *pup.get_build_requirements()}

    # Reduce dependencies to only what is requested to build.
    for deps in pkg_deps.values():
        deps.intersection_update(pkg_dirs.keys())

    # pypiserver requires the wheel dir to exist.
    wheel_dir.mkdir(parents=True, exist_ok=True)

    if not port:
        port = random.randrange(10000, 65535)  # noqa: S311

    pypiserver_proc = await asyncio.create_subprocess_exec(
        "pypi-server",
        "run",
        "-p",
        str(port),
        str(wheel_dir),
    )

    pypi_server_base_url = f"http://localhost:{port}"

    for _ in range(10):
        console.print("Waiting for pypi-server to start...")
        await asyncio.sleep(0.1)

        if pypiserver_proc.returncode is not None:
            console.print("pypi-server exited unexpectedly.")
            sys.exit(1)

        try:
            async with aiohttp.ClientSession() as session, session.get(f"{pypi_server_base_url}/health") as response:
                if response.ok:
                    break
                console.print(f"pypi-server response: {response.status}")
        except aiohttp.ClientError:
            console.print("pypi-server may not be ready yet.")
    else:
        console.print("pypi-server failed to start.")
        pypiserver_proc.kill()
        await pypiserver_proc.wait()
        sys.exit(1)

    try:
        await _buildall(pkg_dirs, pkg_deps, wheel_dir, pypi_server_base_url)
    finally:
        pypiserver_proc.kill()
        await pypiserver_proc.wait()


if __name__ == "__main__":
    app()
