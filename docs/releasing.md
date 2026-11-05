---
title: Releasing
summary: How versions are numbered, how a build is made and how a release is published.
audience: contributors
updated: 2026-11-05
---

# Releasing

Liana uses Semantic Versioning [R4]: a fix raises the patch number, a new
setting or part the minor number, and a change that breaks existing designs
or settings files the major number.

## Where the version lives

`pyproject.toml` holds the version. `src/Liana/Liana.manifest` (shown by
Fusion) and `src/Liana/_version.py` (shown in the dialog) are copies.
Change all three with:

```sh
python scripts/bump_version.py 1.1.0
```

`python scripts/bump_version.py --check` fails when the copies disagree; it
is one of the gates.

## Builds

```sh
python scripts/build.py
```

writes `dist/Liana-<version>.zip` with a `Liana` folder inside, and
`dist/Liana-<version>.zip.sha256`. The archive is reproducible: the same
sources give the same bytes.

A build of a commit that is not tagged `v<version>` gets the version
`<version>+g<commit>`, with `.dirty` appended when the working tree has
uncommitted changes. That version is stamped into the manifest and the
dialog, so a test build is never mistaken for a release.

## Publishing a release

1. Move the entries under `Unreleased` in `CHANGELOG.md` to a new section
   with the version and date [R3].
2. Bump the version, run `python scripts/check.py`, and commit:
   `chore(release): 1.1.0`.
3. Build and run the [manual checks in Fusion](fusion-test-checklist.md) on
   Windows and macOS.
4. Tag and push:

   ```sh
   git tag -a v1.1.0 -m "Liana 1.1.0"
   git push origin main v1.1.0
   ```

5. The release workflow runs the gates again, checks that the tag matches
   the version, builds the archive and publishes a GitHub release with the
   archive, its checksum and the changelog section as notes.

## References

- [R3] Olivier Lacan and contributors, "Keep a Changelog 1.1.0",
  https://keepachangelog.com/en/1.1.0/
- [R4] Tom Preston-Werner, "Semantic Versioning 2.0.0",
  https://semver.org/spec/v2.0.0.html
