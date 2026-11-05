# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Check the documentation pages and keep ``docs/reference-index.md`` current.

Every page under ``docs/`` needs front matter with a unique ``id``; every
relative link must reach an existing file and, when it names one, an
existing anchor; every ``[Rn]`` cited in a page must be listed in its
References section and the other way round. The Markdown files at the
repository root are link-checked too.

Usage:
    python scripts/check_docs.py          # check
    python scripts/check_docs.py --write  # also rewrite docs/reference-index.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _project import ROOT

DOCS = ROOT / "docs"
"""Documentation folder."""

INDEX = DOCS / "reference-index.md"
"""Registry of page ids."""

FRONT_MATTER_KEYS = ("id", "title", "slug", "category", "since", "status")
"""Keys every page declares, in this order."""

STATUSES = ("draft", "stable", "deprecated")
"""Allowed page statuses."""

_FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_HEADING = re.compile(r"^#{1,6} (.+?)(?: \{#([^}]+)\})?\s*$", re.MULTILINE)
_CITE = re.compile(r"\[(R\d+)\](?!:)")
_REFERENCE = re.compile(r'^- \[(R\d+)\]: (\S+) "([^"]+)"$', re.MULTILINE)


def github_slug(heading: str) -> str:
    """Return the anchor GitHub generates for a heading."""
    text = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return text.replace(" ", "-")


def front_matter(text: str) -> dict[str, str] | None:
    """Return the front matter of a page, or None when it has none."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.split("#")[0].strip()
    return fields


def anchors(text: str) -> set[str]:
    """Return every anchor a page defines."""
    found = set()
    for heading, explicit in _HEADING.findall(_FENCE.sub("", text)):
        found.add(explicit or github_slug(heading))
        if explicit:
            found.add(github_slug(heading))
    return found


def page_problems(path: Path, text: str, ids: dict[str, Path]) -> list[str]:
    """Return the front matter and citation problems of one docs page."""
    rel = path.relative_to(ROOT).as_posix()
    if path.name == "_TEMPLATE.md":
        return []
    meta = front_matter(text)
    if meta is None:
        return ["%s: missing front matter" % rel]
    problems = []
    if tuple(meta) != FRONT_MATTER_KEYS:
        problems.append("%s: front matter keys must be %s" % (rel, ", ".join(FRONT_MATTER_KEYS)))
    if meta.get("status") not in STATUSES:
        problems.append("%s: status must be one of %s" % (rel, ", ".join(STATUSES)))
    page_id = meta.get("id", "")
    if page_id in ids:
        problems.append("%s: id %s is also used by %s" % (rel, page_id, ids[page_id]))
    ids[page_id] = path
    body = _FENCE.sub("", text)
    cited = set(_CITE.findall(body))
    listed = {ref for ref, _, _ in _REFERENCE.findall(body)}
    for ref in sorted(cited - listed):
        problems.append("%s: [%s] is cited but not in References" % (rel, ref))
    for ref in sorted(listed - cited):
        problems.append("%s: [%s] is in References but never cited" % (rel, ref))
    return problems


def link_problems(path: Path, text: str) -> list[str]:
    """Return the broken relative links of one Markdown file."""
    rel = path.relative_to(ROOT).as_posix()
    body = _FENCE.sub("", text)
    targets = _LINK.findall(body) + [target for _, target, _ in _REFERENCE.findall(body)]
    problems = []
    for target in targets:
        if re.match(r"^[a-z]+:", target):
            continue
        file_part, _, anchor = target.partition("#")
        dest = (path.parent / file_part).resolve() if file_part else path
        if not dest.exists():
            problems.append("%s: link to missing %s" % (rel, file_part))
            continue
        if (
            anchor
            and dest.suffix == ".md"
            and anchor not in anchors(dest.read_text(encoding="utf-8"))
        ):
            problems.append(
                "%s: no anchor #%s in %s" % (rel, anchor, dest.relative_to(ROOT).as_posix())
            )
    return problems


def index_text(ids: dict[str, Path]) -> str:
    """Return the registry page that maps every id to its file."""
    lines = [
        "---",
        "id: docs.reference-index",
        "title: Reference index",
        "slug: /reference-index",
        "category: Index",
        "since: 1.0.0",
        "status: stable",
        "---",
        "",
        "[Docs](README.md) / Reference index",
        "",
        "# Reference index",
        "",
        "![status](https://img.shields.io/badge/status-stable-2ea44f)",
        "![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)",
        "",
        "Every documentation page by its permanent `id`. A page may move; its `id` does not."
        " Generated by `scripts/check_docs.py --write`.",
        "",
        "## On this page",
        "",
        "- [Pages](#pages)",
        "- [Changelog](#changelog)",
        "",
        "## Pages",
        "",
        "| id | Page |",
        "|---|---|",
    ]
    for page_id, path in sorted(ids.items()):
        if page_id == "docs.reference-index":
            continue
        rel = path.relative_to(DOCS).as_posix()
        lines.append("| `%s` | [%s](%s) |" % (page_id, rel, rel))
    lines += ["", "## Changelog", "", "- 1.0.0: index added."]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="rewrite docs/reference-index.md")
    args = parser.parse_args(argv)
    ids: dict[str, Path] = {}
    problems: list[str] = []
    pages = sorted(DOCS.rglob("*.md"))
    for path in pages:
        text = path.read_text(encoding="utf-8")
        problems += page_problems(path, text, ids)
    expected = index_text(ids)
    if args.write:
        INDEX.write_text(expected, encoding="utf-8", newline="\n")
    elif not INDEX.exists() or INDEX.read_text(encoding="utf-8") != expected:
        problems.append(
            "docs/reference-index.md is out of date: run python scripts/check_docs.py --write"
        )
    for path in pages + sorted(ROOT.glob("*.md")):
        if path.name != "_TEMPLATE.md":  # its links are written for a page in a category
            problems += link_problems(path, path.read_text(encoding="utf-8"))
    if problems:
        print("\n".join(problems))
        return 1
    print("docs: %d pages, links and anchors resolve" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
