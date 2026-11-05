# Contributing to Liana

Thank you for helping. This page covers the workflow; the code is described
in [docs/architecture.md](docs/architecture.md).

## Set up

```sh
git clone https://github.com/yeoblyv/liana.git
cd liana
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt   # Windows: .venv\Scripts\python
```

Python 3.12 or newer is needed for the tools; Fusion itself ships its own
Python.

To try a change in Fusion, add the `src/Liana` folder with
**Utilities > Add-Ins > Scripts and Add-Ins > + > Script or add-in from
device**. Python keeps imported modules in memory, so restart Fusion after
an edit to be sure the new code runs.

## Before every commit

```sh
.venv/bin/python scripts/check.py
```

It runs black, isort, mypy in strict mode, the tests with coverage, the API
docs check, the version check and a check that every text file is ASCII
with LF line endings. Commit only when it passes.

- **Docstrings.** Every public module, class, function, method and constant
  has a Google-style docstring. After changing one, run
  `python scripts/gen_api_docs.py` and commit `docs/api` with the change.
- **Tests.** Every behavior change comes with a test. The golden tests
  (`tests/test_golden.py`) compare every call Liana makes to the Fusion API
  with the traces in `tests/golden`. When a change to the model is
  intended, check it in Fusion, then record new traces with
  `python scripts/update_golden.py` and describe the difference in the
  commit message.
- **Commit messages** follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/),
  for example `fix(rail): keep the nut seat inside the end block`.
- **Changelog.** User-visible changes get a line under `Unreleased` in
  [CHANGELOG.md](CHANGELOG.md).

## Pull requests

Describe what changes for the user, how it was tested (including in Fusion,
on which operating system), and link the issue it addresses. CI runs the
same gates on Windows, macOS and Linux with Python 3.12 to 3.14.

## License

Contributions are accepted under the [Apache License 2.0](LICENSE).
