# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Generate ``docs/api`` from the docstrings, and fail on a missing docstring.

The sources are parsed, not imported, so this runs without Fusion.

Usage:
    python scripts/gen_api_docs.py          # write docs/api
    python scripts/gen_api_docs.py --check  # fail if docs/api is out of date
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path

from _project import ADDIN, ROOT

API_DIR = ROOT / "docs" / "api"
"""Output folder."""


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


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = ast.unparse(node.args)
    returns = " -> %s" % ast.unparse(node.returns) if node.returns else ""
    return "%s(%s)%s" % (node.name, args, returns)


def _assigned_names(node: ast.stmt) -> list[str]:
    if isinstance(node, ast.Assign):
        return [t.id for t in node.targets if isinstance(t, ast.Name)]
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def _string(node: ast.stmt | None) -> str | None:
    if (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ):
        return node.value.value
    return None


def _clean(doc: str) -> str:
    lines = doc.strip("\n").splitlines()
    indent = min((len(x) - len(x.lstrip()) for x in lines[1:] if x.strip()), default=0)
    return "\n".join([lines[0].strip()] + [x[indent:] for x in lines[1:]]).strip()


def _block(doc: str) -> list[str]:
    return ["```text", _clean(doc), "```", ""]


def document(path: Path) -> Module:
    """Return the documentation of one source file."""
    rel = path.relative_to(ADDIN.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    mod = Module(".".join(parts), path)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = ["# `%s`" % mod.name, ""]
    doc = ast.get_docstring(tree)
    if doc is None:
        mod.missing.append(mod.name)
    else:
        out += [_clean(doc), ""]
    constants: list[str] = []
    for i, node in enumerate(tree.body):
        for name in filter(_public, _assigned_names(node)):
            text = _string(tree.body[i + 1] if i + 1 < len(tree.body) else None)
            if text is None:
                mod.missing.append("%s.%s" % (mod.name, name))
                continue
            constants += ["### `%s`" % name, "", _clean(text), ""]
    if constants:
        out += ["## Constants", ""] + constants
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef) and _public(n.name)]
    if classes:
        out += ["## Classes", ""]
    for cls in classes:
        out += _class(mod, cls)
    functions = [
        n
        for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and _public(n.name)
    ]
    if functions:
        out += ["## Functions", ""]
    for fn in functions:
        out += ["### `%s`" % _signature(fn), ""]
        fdoc = ast.get_docstring(fn)
        if fdoc is None:
            mod.missing.append("%s.%s" % (mod.name, fn.name))
        else:
            out += _block(fdoc)
    mod.text = "\n".join(out).rstrip() + "\n"
    return mod


def _class(mod: Module, cls: ast.ClassDef) -> list[str]:
    bases = ", ".join(ast.unparse(b) for b in cls.bases)
    out = ["### `%s%s`" % (cls.name, "(%s)" % bases if bases else ""), ""]
    doc = ast.get_docstring(cls)
    if doc is None:
        mod.missing.append("%s.%s" % (mod.name, cls.name))
    else:
        out += _block(doc)
    for node in cls.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not (_public(node.name) or node.name == "__init__"):
            continue
        out += ["#### `%s.%s`" % (cls.name, _signature(node)), ""]
        mdoc = ast.get_docstring(node)
        if mdoc is None:
            mod.missing.append("%s.%s.%s" % (mod.name, cls.name, node.name))
        else:
            out += _block(mdoc)
    return out


def modules() -> list[Module]:
    """Return the documentation of every add-in module, sorted by name."""
    return sorted((document(p) for p in ADDIN.rglob("*.py")), key=lambda m: m.name)


def index(mods: list[Module]) -> str:
    """Return ``docs/api/README.md``."""
    lines = [
        "# API reference",
        "",
        "Generated from the docstrings by `scripts/gen_api_docs.py`; do not edit by hand.",
        "",
    ]
    for m in mods:
        summary = m.text.split("\n")[2] if m.text.count("\n") > 2 else ""
        lines.append("- [`%s`](%s.md): %s" % (m.name, m.name, summary))
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
