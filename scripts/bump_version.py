# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Set the version everywhere, or check that every copy agrees.

The version lives in ``pyproject.toml``; the manifest and ``_version.py``
are copies.

Usage:
    python scripts/bump_version.py 1.1.0
    python scripts/bump_version.py --check
"""

from __future__ import annotations

import argparse
import sys

from _project import (
    MANIFEST,
    PYPROJECT,
    SEMVER,
    VERSION_PY,
    manifest_version,
    module_version,
    project_version,
    replace_manifest_version,
    replace_module_version,
    replace_project_version,
)


def check() -> int:
    """Return 0 when all copies agree, 1 otherwise."""
    versions = {
        "pyproject.toml": project_version(),
        "Liana.manifest": manifest_version(),
        "_version.py": module_version(),
    }
    if len(set(versions.values())) != 1 or not SEMVER.match(versions["pyproject.toml"]):
        print("version mismatch: %s" % versions)
        return 1
    print("version %s" % versions["pyproject.toml"])
    return 0


def bump(version: str) -> int:
    """Write ``version`` to every copy."""
    if not SEMVER.match(version):
        print("not a semantic version: %s" % version)
        return 2
    for path, replace in (
        (PYPROJECT, replace_project_version),
        (MANIFEST, replace_manifest_version),
        (VERSION_PY, replace_module_version),
    ):
        text = path.read_text(encoding="utf-8")
        path.write_text(replace(text, version), encoding="utf-8", newline="\n")
    return check()


def main(argv: list[str]) -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("version", nargs="?", help="new version, e.g. 1.1.0")
    group.add_argument("--check", action="store_true", help="only check that the copies agree")
    args = parser.parse_args(argv)
    return check() if args.check else bump(args.version)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
