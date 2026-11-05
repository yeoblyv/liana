# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Package the add-in in two archives, each with a SHA-256 checksum file.

- ``dist/Liana-<version>.zip`` holds one ``Liana`` folder, ready to add with
  Utilities > Add-Ins > Scripts and Add-Ins > +.
- ``dist/Liana-<version>.bundle.zip`` holds ``Liana.bundle``, the layout the
  Autodesk Marketplace installs into the ApplicationPlugins folder:
  ``PackageContents.xml`` next to a ``Contents`` folder with the add-in.

Only files tracked by git are packed.

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
import uuid
import zipfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from xml.sax.saxutils import quoteattr

from _project import (
    ADDIN,
    MANIFEST,
    ROOT,
    git,
    manifest_version,
    module_version,
    project_version,
)

DIST = ROOT / "dist"
"""Output folder."""

EXTRA_FILES = ("LICENSE", "NOTICE", "PRIVACY.md")
"""Repository files shipped inside the add-in folder."""

BUNDLE = "Liana.bundle"
"""Folder of the Marketplace bundle."""

PUBLISHER = {
    "Name": "Yehor Oblyvantsov",
    "Url": "https://github.com/yeoblyv/liana",
    "Email": "xineraman8@gmail.com",
}
"""Publisher details written into ``PackageContents.xml``."""

_OS_NAMES = {"windows": "Win64", "mac": "MacOS"}

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


def product_code(app_id: str, version: str) -> str:
    """Return the product code of one version: the same for every build of it.

    Installers tell versions apart by the product code and recognise an
    upgrade by the upgrade code, which is the add-in id and never changes.

    Args:
        app_id: The add-in id from the manifest.
        version: Version of the build.
    """
    return str(uuid.uuid5(uuid.UUID(app_id), version)).upper()


def package_contents(manifest: Mapping[str, Any], version: str) -> str:
    """Return the ``PackageContents.xml`` of the bundle.

    Args:
        manifest: The add-in manifest.
        version: Version of the build.

    Returns:
        The XML text; the component entry names the manifest in ``Contents``.
    """
    description = str(manifest.get("description", {}).get("", ""))
    systems = "|".join(
        _OS_NAMES[name] for name in str(manifest["supportedOS"]).split("|") if name in _OS_NAMES
    )
    attributes = [
        ("SchemaVersion", "1.0"),
        ("AutodeskProduct", "Fusion360"),
        ("ProductType", "Application"),
        ("Name", "Liana"),
        ("Description", description),
        ("AppVersion", version),
        ("Author", str(manifest["author"])),
        ("ProductCode", "{%s}" % product_code(str(manifest["id"]), version)),
        ("UpgradeCode", "{%s}" % str(manifest["id"]).upper()),
        ("HelpFile", "./Contents/resources/help.html"),
    ]
    company = " ".join("%s=%s" % (key, quoteattr(value)) for key, value in PUBLISHER.items())
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<ApplicationPackage"]
    lines += ["    %s=%s" % (key, quoteattr(value)) for key, value in attributes]
    lines[-1] += ">"
    lines += [
        "  <CompanyDetails %s />" % company,
        "  <Components>",
        '    <RuntimeRequirements OS=%s Platform="Fusion360" />' % quoteattr(systems),
        '    <ComponentEntry AppName="Liana" Version=%s ModuleName="./Contents/Liana.manifest" />'
        % quoteattr(version),
        "  </Components>",
        "</ApplicationPackage>",
    ]
    return "\n".join(lines) + "\n"


def _write_zip(path: Path, contents: list[tuple[str, bytes]], when: time.struct_time) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in sorted(contents):
            zf.writestr(_entry(name, when), data)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    checksum = path.with_name(path.name + ".sha256")
    checksum.write_text("%s  %s\n" % (digest, path.name), encoding="utf-8", newline="\n")


def build() -> list[Path]:
    """Write both archives and their checksum files.

    The archives are named after the version in ``pyproject.toml``; the
    manifest and ``_version.py`` must hold the same version.

    Returns:
        Paths of the folder archive and of the bundle archive.

    Raises:
        SystemExit: The version copies disagree.
    """
    version = project_version()
    if (manifest_version(), module_version()) != (version, version):
        raise SystemExit("version copies disagree: run python scripts/bump_version.py --check")
    DIST.mkdir(exist_ok=True)
    files = [(path.relative_to(ADDIN).as_posix(), path.read_bytes()) for path in addin_files()]
    files += [(name, (ROOT / name).read_bytes()) for name in EXTRA_FILES]
    when = build_time()
    archive = DIST / ("Liana-%s.zip" % version)
    _write_zip(archive, [("Liana/" + name, data) for name, data in files], when)
    bundle = DIST / ("Liana-%s.bundle.zip" % version)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    xml = package_contents(manifest, version).encode("utf-8")
    bundled = [(BUNDLE + "/Contents/" + name, data) for name, data in files]
    _write_zip(bundle, bundled + [(BUNDLE + "/PackageContents.xml", xml)], when)
    return [archive, bundle]


def archive_versions(archive: Path) -> set[str]:
    """Return every version an archive carries.

    That is the manifest, ``_version.py`` and, in a bundle, the application
    and component versions of ``PackageContents.xml``.
    """
    found = set()
    with zipfile.ZipFile(archive) as zf:
        for name in zf.namelist():
            if name.endswith("/Liana.manifest"):
                found.add(str(json.loads(zf.read(name).decode("utf-8"))["version"]))
            elif name.endswith("/_version.py") and "/core/" not in name:
                text = zf.read(name).decode("utf-8")
                found.update(re.findall(r'__version__ = "([^"]+)"', text))
            elif name.endswith("/PackageContents.xml"):
                text = zf.read(name).decode("utf-8")
                found.update(re.findall(r'\s(?:AppVersion|Version)="([^"]+)"', text))
    return found


def main(argv: list[str]) -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--expect-version", help="fail unless the archive carries this version")
    args = parser.parse_args(argv)
    for archive in build():
        print(archive.relative_to(ROOT).as_posix())
        print(archive.with_name(archive.name + ".sha256").read_text(encoding="utf-8").strip())
        if args.expect_version is not None:
            stamped = archive_versions(archive)
            if stamped != {args.expect_version}:
                print(
                    "%s carries %s, expected %s"
                    % (archive.name, sorted(stamped), args.expect_version)
                )
                return 1
            print("%s carries version %s" % (archive.name, args.expect_version))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
