# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Package the add-in as ``dist/Liana-<version>.zip`` with a SHA-256 checksum.

The archive holds one ``Liana`` folder, ready to unpack into Fusion's add-in
folder or to add with Utilities > Add-Ins > Scripts and Add-Ins > +. Entries
are sorted and dated 1980-01-01, so the same sources give the same bytes.

Usage:
    python scripts/build.py
"""

from __future__ import annotations

import hashlib
import sys
import zipfile
from pathlib import Path

from _project import (
    ADDIN,
    ROOT,
    build_version,
    project_version,
    replace_manifest_version,
    replace_module_version,
)

DIST = ROOT / "dist"
"""Output folder."""

EXTRA_FILES = ("LICENSE", "NOTICE", "PRIVACY.md")
"""Repository files shipped inside the add-in folder."""

_EPOCH = (1980, 1, 1, 0, 0, 0)
_SKIP_DIRS = {"__pycache__"}


def addin_files() -> list[Path]:
    """Return every file of the add-in folder that belongs in a build."""
    files = []
    for path in sorted(ADDIN.rglob("*")):
        rel = path.relative_to(ADDIN)
        if path.is_file() and not _SKIP_DIRS.intersection(rel.parts) and path.suffix != ".pyc":
            files.append(path)
    return files


def _entry(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, _EPOCH)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    return info


def build(version: str) -> Path:
    """Write the archive and its checksum file.

    Args:
        version: Version stamped into the manifest and ``_version.py``.

    Returns:
        Path of the archive.
    """
    DIST.mkdir(exist_ok=True)
    archive = DIST / ("Liana-%s.zip" % version)
    contents: list[tuple[str, bytes]] = []
    for path in addin_files():
        data = path.read_bytes()
        if path.name == "Liana.manifest":
            data = replace_manifest_version(data.decode("utf-8"), version).encode("utf-8")
        elif path.name == "_version.py":
            data = replace_module_version(data.decode("utf-8"), version).encode("utf-8")
        contents.append(("Liana/" + path.relative_to(ADDIN).as_posix(), data))
    for name in EXTRA_FILES:
        contents.append(("Liana/" + name, (ROOT / name).read_bytes()))
    with zipfile.ZipFile(archive, "w") as zf:
        for name, data in sorted(contents):
            zf.writestr(_entry(name), data)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_name(archive.name + ".sha256")
    checksum.write_text("%s  %s\n" % (digest, archive.name), encoding="utf-8", newline="\n")
    return archive


def main() -> int:
    """Command line entry point."""
    archive = build(build_version(project_version()))
    print(archive.relative_to(ROOT).as_posix())
    print(archive.with_name(archive.name + ".sha256").read_text(encoding="utf-8").strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
