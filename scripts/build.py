# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Package the add-in as ``dist/Liana-<version>.zip`` with a SHA-256 checksum.

The archive holds one ``Liana`` folder, ready to add with Utilities >
Add-Ins > Scripts and Add-Ins > +. Only files tracked by git are packed.

Entries are sorted and dated with the commit time: one commit built with
the same Python gives the same bytes, and every new commit gets new file
times. The new times matter because Python reuses cached bytecode in
``__pycache__`` when a source file keeps its size and time, so an update
unpacked over an older build would otherwise keep running the old code.

The version is the plain semantic version from ``pyproject.toml``.

Usage:
    python scripts/build.py
    python scripts/build.py --expect-version 1.0.0   # fail unless the build carries it
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import time
import zipfile
from pathlib import Path

from _project import ADDIN, ROOT, git, manifest_version, module_version, project_version

DIST = ROOT / "dist"
"""Output folder."""

EXTRA_FILES = ("LICENSE", "NOTICE", "PRIVACY.md")
"""Repository files shipped inside the add-in folder."""

_ZIP_EPOCH = 315532800  # 1980-01-01, the earliest time a zip entry can hold


def addin_files() -> list[Path]:
    """Return the files of the add-in folder that git tracks.

    Files the add-in writes while it runs from the source folder, editor
    settings and caches are not tracked, so they never reach a build.
    """
    listed = git("ls-files", "-z", "--", ADDIN.relative_to(ROOT).as_posix())
    if listed is None:
        raise SystemExit("build.py needs git and a clone of the repository")
    return sorted(ROOT / name for name in listed.split("\0") if name)


def build_time() -> time.struct_time:
    """Return the time to date the entries with, in UTC.

    The commit time for a clean tree; the current time when there are
    uncommitted changes, so that every test build gets new file times.
    """
    dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    stamp = None if dirty else git("log", "-1", "--format=%ct")
    seconds = int(stamp) if stamp else int(time.time())
    return time.gmtime(max(seconds, _ZIP_EPOCH))


def _entry(name: str, when: time.struct_time) -> zipfile.ZipInfo:
    stamp = (when.tm_year, when.tm_mon, when.tm_mday, when.tm_hour, when.tm_min, when.tm_sec)
    info = zipfile.ZipInfo(name, stamp)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3  # Unix, on every platform, so the bytes do not depend on it
    info.external_attr = (stat.S_IFREG | 0o644) << 16  # a regular file, rw-r--r--
    return info


def build() -> Path:
    """Write the archive and its checksum file.

    The archive is named after the version in ``pyproject.toml``; the
    manifest and ``_version.py`` must hold the same version.

    Returns:
        Path of the archive.

    Raises:
        SystemExit: The version copies disagree.
    """
    version = project_version()
    if (manifest_version(), module_version()) != (version, version):
        raise SystemExit("version copies disagree: run python scripts/bump_version.py --check")
    DIST.mkdir(exist_ok=True)
    archive = DIST / ("Liana-%s.zip" % version)
    contents = [
        ("Liana/" + path.relative_to(ADDIN).as_posix(), path.read_bytes())
        for path in addin_files()
    ]
    for name in EXTRA_FILES:
        contents.append(("Liana/" + name, (ROOT / name).read_bytes()))
    when = build_time()
    with zipfile.ZipFile(archive, "w") as zf:
        for name, data in sorted(contents):
            zf.writestr(_entry(name, when), data)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_name(archive.name + ".sha256")
    checksum.write_text("%s  %s\n" % (digest, archive.name), encoding="utf-8", newline="\n")
    return archive


def archive_versions(archive: Path) -> tuple[str, str]:
    """Return the versions inside an archive: manifest and ``_version.py``."""
    with zipfile.ZipFile(archive) as zf:
        manifest = json.loads(zf.read("Liana/Liana.manifest").decode("utf-8"))["version"]
        module = re.search(
            r'__version__ = "([^"]+)"', zf.read("Liana/_version.py").decode("utf-8")
        )
    return str(manifest), module.group(1) if module else ""


def main(argv: list[str]) -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expect-version", help="fail unless the archive carries this version")
    args = parser.parse_args(argv)
    archive = build()
    print(archive.relative_to(ROOT).as_posix())
    print(archive.with_name(archive.name + ".sha256").read_text(encoding="utf-8").strip())
    if args.expect_version is not None:
        stamped = archive_versions(archive)
        if stamped != (args.expect_version, args.expect_version):
            print("archive carries %s, expected %s" % (stamped, args.expect_version))
            return 1
        print("archive carries version %s" % args.expect_version)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
