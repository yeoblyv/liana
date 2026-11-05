# Contributing to Liana

Thank you for helping. In short:

1. Set up a working copy and the tools as described in
   [Workflow](docs/contributing/workflow.md#set-up).
2. Make the change with a test, and update the docstrings, `docs/` and
   `CHANGELOG.md` where it changes what users or contributors see.
3. Run `python scripts/check.py` and commit only when every gate passes.
   Commit messages follow Conventional Commits, for example
   `fix(rail): keep the nut seat inside the end block`.
4. Open a pull request that says what changes for the user, how it was
   tested (including in Fusion, on which operating system), and which issue
   it addresses.

How the code works: [Architecture overview](docs/architecture/overview.md).
Manual checks before a release: [Testing in Fusion](docs/contributing/fusion-test-checklist.md).
Security problems are reported privately, see [SECURITY.md](SECURITY.md).

Contributions are accepted under the [Apache License 2.0](LICENSE).
