# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Paths and version helpers shared by the scripts."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
"""Repository root."""

ADDIN = ROOT / "src" / "Liana"
"""The add-in folder as Fusion loads it."""

PYPROJECT = ROOT / "pyproject.toml"
"""Holds the version that every other place copies."""

MANIFEST = ADDIN / "Liana.manifest"
"""Fusion add-in manifest."""

VERSION_PY = ADDIN / "_version.py"
"""Version module of the add-in."""

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
"""Semantic version without build metadata."""

_PROJECT_VERSION = re.compile(r'^version = "([^"]+)"$', re.MULTILINE)
_MODULE_VERSION = re.compile(r'^__version__ = "([^"]+)"$', re.MULTILINE)


def project_version() -> str:
    """Return the version in ``pyproject.toml``."""
    match = _PROJECT_VERSION.search(PYPROJECT.read_text(encoding="utf-8"))
    if match is None:
        raise SystemExit("no version in pyproject.toml")
    return match.group(1)


def manifest_version() -> str:
    """Return the version in the add-in manifest."""
    return str(json.loads(MANIFEST.read_text(encoding="utf-8"))["version"])


def module_version() -> str:
    """Return the version in ``_version.py``."""
    match = _MODULE_VERSION.search(VERSION_PY.read_text(encoding="utf-8"))
    if match is None:
        raise SystemExit("no __version__ in _version.py")
    return match.group(1)


def replace_module_version(text: str, version: str) -> str:
    """Return ``_version.py`` text with a new version."""
    return _MODULE_VERSION.sub('__version__ = "%s"' % version, text, count=1)


def replace_project_version(text: str, version: str) -> str:
    """Return ``pyproject.toml`` text with a new version."""
    return _PROJECT_VERSION.sub('version = "%s"' % version, text, count=1)


def replace_manifest_version(text: str, version: str) -> str:
    """Return manifest text with a new version, keeping its formatting."""
    new, count = re.subn(r'("version":\s*)"[^"]*"', r'\g<1>"%s"' % version, text, count=1)
    if count != 1:
        raise SystemExit("no version in Liana.manifest")
    return new


def git(*args: str) -> str | None:
    """Run git in the repository; None when git or the repository is missing."""
    try:
        done = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return done.stdout.strip()
