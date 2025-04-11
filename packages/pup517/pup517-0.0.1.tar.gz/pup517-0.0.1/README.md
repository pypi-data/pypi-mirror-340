# pup517

[![PyPI - Version](https://img.shields.io/pypi/v/pup517.svg)](https://pypi.org/project/pup517)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pup517.svg)](https://pypi.org/project/pup517)

-----

pup517 is a PEP-517 backend for shipping non-Python tools as wheels in a venv.
Imagine a Gentoo ebuild but in `pyproject.toml`.

Each tool is a Python package (that is, a directory with a `pyproject.toml`)
which specifies how to build the tool.  In general, the tool uses a common build
system (defined in `src/pup517/build_system`) instead of implementing it's own
build actions as shell commands, but arbitrary shell commands are supported.

This project is still experiemental, and the API is subject to change.

See examples inside `pups`.

## License

`pup517` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
