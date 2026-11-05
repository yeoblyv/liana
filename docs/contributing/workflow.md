---
id: contributing.workflow
title: Workflow
slug: /contributing/workflow
category: Contributing
since: 1.0.0
status: stable
---

[Docs](../README.md) / Contributing / Workflow

# Workflow

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)
![runtime](https://img.shields.io/badge/runtime-Python%20%3E%3D3.12-777bb4)

How to set up a working copy, try a change in Fusion, and pass the gates
every commit must pass.

## On this page

- [Set up](#set-up)
- [Try a change in Fusion](#try-a-change-in-fusion)
- [Gates](#gates)
- [Docstrings and API docs](#docstrings-and-api-docs)
- [Tests](#tests)
- [Commits and pull requests](#commits-and-pull-requests)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Set up

```bash
git clone https://github.com/yeoblyv/liana.git
cd liana
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

On Windows use `.venv\Scripts\python` instead of `.venv/bin/python`. The
tools need Python 3.12 or newer; Fusion ships its own Python.

## Try a change in Fusion

Add `src/Liana` with **Utilities > Add-Ins > Scripts and Add-Ins > + >
Script or add-in from device**. After an edit, switch the add-in's **Run**
off and on: stopping drops its modules from memory, so the edited code
loads.

## Gates

```bash
.venv/bin/python scripts/check.py
```

| Gate | Tool |
|---|---|
| Formatting | black, isort |
| Types | mypy in strict mode |
| Tests | pytest with coverage (at least 90 %) |
| API docs | `scripts/gen_api_docs.py --check` |
| Documentation pages | front matter, page registry, links and anchors |
| Version | `scripts/bump_version.py --check` |
| Text files | ASCII, LF line endings, SPDX header |
| Secrets | no keys or tokens in tracked files |

CI runs the same gates on Windows, macOS and Linux with Python 3.12 to
3.14, and audits the development dependencies. Commit only when every
gate passes.

## Docstrings and API docs

Every public module, class, function, method and constant has a
Google-style docstring [R1] with `Args`, `Returns` and `Raises` where they
apply. After changing one, regenerate and commit the reference:

```bash
.venv/bin/python scripts/gen_api_docs.py
```

New documentation pages start from [`_TEMPLATE.md`](../_TEMPLATE.md) and
are registered in [`reference-index.md`](../reference-index.md).

## Tests

Every behavior change comes with a test, and every fix with a regression
test. The golden traces and when to record them again are described in
[Testing](../architecture/testing.md#golden-traces).

## Commits and pull requests

- Commit messages follow Conventional Commits [R2], for example
  `fix(rail): keep the nut seat inside the end block`.
- User-visible changes get a line under `Unreleased` in `CHANGELOG.md`.
- A pull request says what changes for the user, how it was tested
  (including in Fusion, on which operating system) and which issue it
  addresses.

## See also

- [Releasing](releasing.md): versions, builds and tags.
- [Testing in Fusion](fusion-test-checklist.md): the manual checks.

## References

- [R1]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings "Google Python Style Guide - Comments and Docstrings"
- [R2]: https://www.conventionalcommits.org/en/v1.0.0/ "Conventional Commits 1.0.0"

## Changelog

- 1.0.0: page added.
