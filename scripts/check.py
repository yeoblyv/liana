# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Run every quality gate; the same command runs locally and in CI.

Gates: formatting (black, isort), types (mypy --strict), tests with
coverage, API docs up to date, version copies in agreement, ASCII-only
sources with an SPDX header.

Usage:
    python scripts/check.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _project import ROOT

SOURCE_DIRS = ("src", "tests", "scripts")
"""Folders with Python sources."""

TEXT_SUFFIXES = {".py", ".manifest", ".md", ".toml", ".yml", ".yaml", ".txt", ".cfg"}
"""Files that must be plain ASCII, by suffix."""

TEXT_NAMES = {"LICENSE", "NOTICE", ".gitignore", ".gitattributes", ".editorconfig"}
"""Files that must be plain ASCII, by name."""

SPDX = "# SPDX-License-Identifier: Apache-2.0"
"""First line of every Python source."""

_SKIP_PARTS = {".git", ".venv", "dist", "__pycache__", "golden"}


def _files() -> list[Path]:
    out = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if path.is_file() and not _SKIP_PARTS.intersection(rel.parts):
            out.append(path)
    return out


def text_problems() -> list[str]:
    """Return files with non-ASCII text or a missing SPDX header."""
    problems = []
    for path in _files():
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        data = path.read_bytes()
        try:
            data.decode("ascii")
        except UnicodeDecodeError as e:
            line = data[: e.start].count(b"\n") + 1
            problems.append("%s:%d: non-ASCII character" % (rel, line))
        if b"\r\n" in data:
            problems.append("%s: CRLF line endings" % rel)
        if path.suffix == ".py" and rel.split("/")[0] in SOURCE_DIRS:
            if not data.decode("utf-8", "replace").startswith(SPDX):
                problems.append("%s: missing SPDX header" % rel)
    return problems


def main() -> int:
    """Run the gates in order and stop at the first failure."""
    py = sys.executable
    steps = [
        ("black", [py, "-m", "black", "--check", "--quiet", *SOURCE_DIRS]),
        ("isort", [py, "-m", "isort", "--check-only", "--quiet", *SOURCE_DIRS]),
        ("mypy", [py, "-m", "mypy"]),
        ("pytest", [py, "-m", "pytest", "-q", "--cov", "--cov-report=term-missing"]),
        ("api docs", [py, "scripts/gen_api_docs.py", "--check"]),
        ("version", [py, "scripts/bump_version.py", "--check"]),
    ]
    for name, cmd in steps:
        print("== %s" % name, flush=True)
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            print("FAILED: %s" % name)
            return 1
    print("== text files")
    problems = text_problems()
    if problems:
        print("\n".join(problems))
        print("FAILED: text files")
        return 1
    print("all gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
