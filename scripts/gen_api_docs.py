# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Generate ``docs/api`` from the docstrings, and fail on a missing docstring.

One page per module, one entry per public constant, class, function and
method. The Google-style ``Args``, ``Returns``, ``Raises`` and ``Attributes``
sections become tables and labelled lines. A line ``Since: x.y.z`` in a
docstring sets the version the symbol appeared in; the default is
:data:`FIRST_RELEASE`.

The sources are parsed, not imported, so this runs without Fusion.

Usage:
    python scripts/gen_api_docs.py          # write docs/api
    python scripts/gen_api_docs.py --check  # fail if docs/api is out of date
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from _project import ADDIN, ROOT

API_DIR = ROOT / "docs" / "api"
"""Output folder."""

FIRST_RELEASE = "1.0.0"
"""Version of every symbol whose docstring names no other."""

_SECTIONS = ("Args", "Returns", "Raises", "Attributes", "Yields")
_SINCE = re.compile(r"^Since:\s*(\S+)\s*$", re.MULTILINE)
_ROLE = re.compile(r":(?:mod|data|func|class|meth|attr|exc):`~?\.?([^`]+)`")
Node = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


@dataclass
class Docstring:
    """A docstring split into its parts.

    Attributes:
        summary: First line.
        body: Paragraphs between the summary and the first section.
        sections: Google-style sections by name, as ``(name, text)`` items.
        since: Version the symbol appeared in.
    """

    summary: str
    body: str
    sections: dict[str, list[tuple[str, str]]]
    since: str


@dataclass
class Entry:
    """One documented symbol.

    Attributes:
        anchor: Stable heading anchor.
        heading: Heading text without the anchor.
        level: Markdown heading level.
        doc: Parsed docstring.
        params: Parameter names and annotations for the table.
        returns: Return annotation, empty when there is none.
    """

    anchor: str
    heading: str
    level: int
    doc: Docstring
    params: list[tuple[str, str]] = field(default_factory=list)
    returns: str = ""


@dataclass
class Module:
    """Documentation of one module.

    Attributes:
        name: Dotted module name.
        path: Source file.
        text: Generated Markdown.
        missing: Public symbols without a docstring.
    """

    name: str
    path: Path
    text: str = ""
    missing: list[str] = field(default_factory=list)


def _public(name: str) -> bool:
    return not name.startswith("_")


def _clean(doc: str) -> str:
    lines = doc.strip("\n").splitlines()
    indent = min((len(x) - len(x.lstrip()) for x in lines[1:] if x.strip()), default=0)
    return "\n".join([lines[0].strip()] + [x[indent:] for x in lines[1:]]).strip()


def parse_docstring(raw: str) -> Docstring:
    """Split a Google-style docstring into summary, body and sections."""
    text = _ROLE.sub(r"`\1`", _clean(raw)).replace("``", "`")
    since_match = _SINCE.search(text)
    since = since_match.group(1) if since_match else FIRST_RELEASE
    text = _SINCE.sub("", text).strip()
    lines = text.splitlines()
    summary = lines[0].strip()
    body: list[str] = []
    sections: dict[str, list[tuple[str, str]]] = {}
    current: str | None = None
    for line in lines[1:]:
        header = line.strip().rstrip(":")
        if line.strip().endswith(":") and header in _SECTIONS and not line.startswith(" "):
            current = header
            sections[current] = []
            continue
        if current is None:
            body.append(line)
            continue
        if line.startswith("    ") and not line.startswith("        ") and line.strip():
            item = line.strip()
            name, sep, desc = item.partition(":")
            if current in ("Returns", "Yields") or not sep:
                sections[current].append(("", item))
            else:
                sections[current].append((name.strip(), desc.strip()))
        elif line.strip() and sections[current]:
            name, desc = sections[current][-1]
            sections[current][-1] = (name, (desc + " " + line.strip()).strip())
    return Docstring(summary, "\n".join(body).strip(), sections, since)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _params(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[tuple[str, str]]:
    args = node.args
    out = []
    for arg in [*args.posonlyargs, *args.args, *args.kwonlyargs]:
        if arg.arg in ("self", "cls"):
            continue
        out.append((arg.arg, ast.unparse(arg.annotation) if arg.annotation else ""))
    return out


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    returns = " -> %s" % ast.unparse(node.returns) if node.returns else ""
    return "%s(%s)%s" % (node.name, ast.unparse(node.args), returns)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render(entry: Entry) -> list[str]:
    """Return the Markdown lines of one entry."""
    doc = entry.doc
    out = ["%s `%s` {#%s}" % ("#" * entry.level, entry.heading, entry.anchor), "", doc.summary, ""]
    if doc.body:
        out += [doc.body, ""]
    described = dict(doc.sections.get("Args", []))
    if entry.params:
        out += ["| Parameter | Type | Description |", "|---|---|---|"]
        for name, annotation in entry.params:
            out.append(
                "| `%s` | %s | %s |"
                % (
                    name,
                    "`%s`" % _cell(annotation) if annotation else "",
                    _cell(described.get(name, "")),
                )
            )
        out.append("")
    attributes = doc.sections.get("Attributes", [])
    if attributes:
        out += ["| Attribute | Description |", "|---|---|"]
        out += ["| `%s` | %s |" % (name, _cell(desc)) for name, desc in attributes]
        out.append("")
    labelled = []
    if entry.returns and entry.returns != "None":
        returned = " ".join(desc for _, desc in doc.sections.get("Returns", []))
        labelled.append(
            "**Returns** `%s`%s" % (entry.returns, " - " + returned if returned else "")
        )
    for name, desc in doc.sections.get("Raises", []):
        labelled.append("**Raises** `%s` - %s" % (name, desc))
    labelled.append("**Since** %s" % doc.since)
    out += ["  \n".join(labelled), ""]
    return out


def _package_pages() -> set[str]:
    """Return the dotted names of the packages that have an ``__init__.py``."""
    return {".".join(p.parent.relative_to(ADDIN.parent).parts) for p in ADDIN.rglob("__init__.py")}


def document(path: Path) -> Module:
    """Return the documentation page of one source file."""
    rel = path.relative_to(ADDIN.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    mod = Module(".".join(parts), path)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    raw = ast.get_docstring(tree, clean=False)
    if raw is None:
        mod.missing.append(mod.name)
        raw = mod.name
    module_doc = parse_docstring(raw)
    prefix = _slug(mod.name)
    entries: list[tuple[str, list[Entry]]] = []

    constants = []
    for i, node in enumerate(tree.body):
        names = []
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names = [node.target.id]
        for name in filter(_public, names):
            follower = tree.body[i + 1] if i + 1 < len(tree.body) else None
            if not (
                isinstance(follower, ast.Expr)
                and isinstance(follower.value, ast.Constant)
                and isinstance(follower.value.value, str)
            ):
                mod.missing.append("%s.%s" % (mod.name, name))
                continue
            doc = parse_docstring(follower.value.value)
            constants.append(Entry("%s-const-%s" % (prefix, _slug(name)), name, 3, doc))
    if constants:
        entries.append(("Constants", constants))

    classes = []
    for cls in (n for n in tree.body if isinstance(n, ast.ClassDef) and _public(n.name)):
        classes += _class_entries(mod, prefix, cls)
    if classes:
        entries.append(("Classes", classes))

    functions = []
    for fn in tree.body:
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) and _public(fn.name):
            fdoc = ast.get_docstring(fn, clean=False)
            if fdoc is None:
                mod.missing.append("%s.%s" % (mod.name, fn.name))
                continue
            functions.append(
                Entry(
                    "%s-%s" % (prefix, _slug(fn.name)),
                    _signature(fn),
                    3,
                    parse_docstring(fdoc),
                    _params(fn),
                    ast.unparse(fn.returns) if fn.returns else "",
                )
            )
    if functions:
        entries.append(("Functions", functions))
    mod.text = _page(mod, module_doc, entries)
    return mod


def _class_entries(mod: Module, prefix: str, cls: ast.ClassDef) -> list[Entry]:
    raw = ast.get_docstring(cls, clean=False)
    if raw is None:
        mod.missing.append("%s.%s" % (mod.name, cls.name))
        raw = cls.name
    bases = ", ".join(ast.unparse(b) for b in cls.bases)
    heading = "%s(%s)" % (cls.name, bases) if bases else cls.name
    out = [Entry("%s-class-%s" % (prefix, _slug(cls.name)), heading, 3, parse_docstring(raw))]
    for node in cls.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not (_public(node.name) or node.name == "__init__"):
            continue
        mdoc = ast.get_docstring(node, clean=False)
        if mdoc is None:
            mod.missing.append("%s.%s.%s" % (mod.name, cls.name, node.name))
            continue
        out.append(
            Entry(
                "%s-class-%s-%s" % (prefix, _slug(cls.name), _slug(node.name).strip("-")),
                "%s.%s" % (cls.name, _signature(node)),
                4,
                parse_docstring(mdoc),
                _params(node),
                ast.unparse(node.returns) if node.returns else "",
            )
        )
    return out


def _page(mod: Module, module_doc: Docstring, entries: list[tuple[str, list[Entry]]]) -> str:
    package = mod.name.rpartition(".")[0]
    out = [
        "---",
        "id: api.%s" % mod.name.lower(),
        "title: %s" % mod.name,
        "slug: /api/%s" % mod.name,
        "category: API",
        "since: %s" % FIRST_RELEASE,
        "status: stable",
        "---",
        "",
        "[Docs](../README.md) / [API](README.md) / `%s`" % mod.name,
        "",
        "# `%s`" % mod.name,
        "",
        "![status](https://img.shields.io/badge/status-stable-2ea44f)",
        "![since](https://img.shields.io/badge/since-%s-5b4fe0)" % FIRST_RELEASE,
        "",
        module_doc.summary,
        "",
    ]
    if module_doc.body:
        out += [module_doc.body, ""]
    out += ["## On this page", ""]
    for title, items in entries:
        out.append("- [%s](#%s)" % (title, _slug(title)))
        for e in items:
            indent = "  " if e.level == 3 else "    "
            out.append("%s- [`%s`](#%s)" % (indent, e.heading.split("(")[0], e.anchor))
    out += ["- [See also](#see-also)", "- [Changelog](#changelog)", ""]
    for title, items in entries:
        out += ["## %s" % title, ""]
        for e in items:
            out += render(e)
    out += ["## See also", ""]
    if package in _package_pages():
        out.append("- [`%s`](%s.md): the package this module belongs to." % (package, package))
    out += [
        "- [Architecture](../architecture/overview.md): how the modules work together.",
        "",
        "## Changelog",
        "",
        "- %s: first release." % FIRST_RELEASE,
    ]
    return "\n".join(out).rstrip() + "\n"


def modules() -> list[Module]:
    """Return the documentation of every add-in module, sorted by name."""
    return sorted((document(p) for p in ADDIN.rglob("*.py")), key=lambda m: m.name)


def index(mods: list[Module]) -> str:
    """Return ``docs/api/README.md``, the list of module pages."""
    lines = [
        "---",
        "id: api.index",
        "title: API reference",
        "slug: /api",
        "category: API",
        "since: %s" % FIRST_RELEASE,
        "status: stable",
        "---",
        "",
        "[Docs](../README.md) / API",
        "",
        "# API reference",
        "",
        "![status](https://img.shields.io/badge/status-stable-2ea44f)",
        "![since](https://img.shields.io/badge/since-%s-5b4fe0)" % FIRST_RELEASE,
        "",
        "Every public constant, class, function and method of the add-in, generated from the"
        " docstrings by `scripts/gen_api_docs.py`. Do not edit these pages by hand.",
        "",
        "## On this page",
        "",
        "- [Modules](#modules)",
        "- [See also](#see-also)",
        "- [Changelog](#changelog)",
        "",
        "## Modules",
        "",
        "| Module | Summary |",
        "|---|---|",
    ]
    for m in mods:
        summary = m.text.split("\n")[16] if m.text.count("\n") > 16 else ""
        lines.append("| [`%s`](%s.md) | %s |" % (m.name, m.name, _cell(summary)))
    lines += [
        "",
        "## See also",
        "",
        "- [Architecture](../architecture/overview.md): how the modules work together.",
        "",
        "## Changelog",
        "",
        "- %s: first release." % FIRST_RELEASE,
    ]
    return "\n".join(lines) + "\n"


def expected_files() -> tuple[dict[Path, str], list[str]]:
    """Return the files docs/api should hold and the symbols that lack docs."""
    mods = modules()
    files = {API_DIR / (m.name + ".md"): m.text for m in mods}
    files[API_DIR / "README.md"] = index(mods)
    missing = [name for m in mods for name in m.missing]
    return files, missing


def main(argv: list[str]) -> int:
    """Command line entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if docs/api is out of date")
    args = parser.parse_args(argv)
    files, missing = expected_files()
    if missing:
        print("missing docstrings:\n  " + "\n  ".join(missing))
        return 1
    if args.check:
        current = {p: p.read_text(encoding="utf-8") for p in API_DIR.glob("*.md")}
        if current != files:
            print("docs/api is out of date: run python scripts/gen_api_docs.py")
            return 1
        print("docs/api is up to date (%d files)" % len(files))
        return 0
    API_DIR.mkdir(parents=True, exist_ok=True)
    for stale in set(API_DIR.glob("*.md")) - set(files):
        stale.unlink()
    for path, text in files.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    print("wrote %d files to %s" % (len(files), API_DIR.relative_to(ROOT).as_posix()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
