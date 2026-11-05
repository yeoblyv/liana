---
id: contributing.releasing
title: Releasing
slug: /contributing/releasing
category: Contributing
since: 1.0.0
status: stable
---

[Docs](../README.md) / Contributing / Releasing

# Releasing

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

How versions are numbered and stamped into builds, how a release is cut,
and what the Autodesk Marketplace needs before a submission.

## On this page

- [Versions](#versions)
- [Builds](#builds)
- [Cutting a release](#cutting-a-release)
- [After the release](#after-the-release)
- [Autodesk Marketplace requirements](#autodesk-marketplace-requirements)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Versions

Liana uses Semantic Versioning [R1]. The owner decides the next version
before a release. `pyproject.toml` holds it; `src/Liana/Liana.manifest`
(shown by Fusion) and `src/Liana/_version.py` (shown in the dialog) are
copies, changed only by the bump script:

```bash
python scripts/bump_version.py 1.1.0
python scripts/bump_version.py --check
```

## Builds

```bash
python scripts/build.py
```

writes `dist/Liana-<version>.zip` with one `Liana` folder inside, and
`dist/Liana-<version>.zip.sha256`. Only files tracked by git are packed.

- The archive, the manifest and the dialog carry the plain semantic
  version from `pyproject.toml`; the build stops if the copies disagree.
- Entries are dated with the commit time: one commit built with the same
  Python gives the same bytes, and a new commit gives new file times, so
  Python does not reuse bytecode cached for an older build.

## Cutting a release

1. Move the entries under `Unreleased` in `CHANGELOG.md` to a section for
   the new version and date [R2].
2. Bump the version, run `python scripts/check.py` and commit:
   `chore(release): 1.1.0`.
3. Build and run the [manual checks in Fusion](fusion-test-checklist.md)
   on Windows and macOS.
4. Tag and push:

   ```bash
   git tag -s v1.1.0 -m "Liana 1.1.0"
   git push origin main v1.1.0
   ```

5. The release workflow runs the gates, checks that the tag, the manifest
   and the version inside the built archive are identical, and publishes
   the archive with its checksum and the changelog section as notes.

## After the release

Move the version to the next planned one with a `-dev` suffix, so a build
from main is never numbered like a release:

```bash
python scripts/bump_version.py 1.2.0-dev
```

## Autodesk Marketplace requirements

The publisher agreement asks every app to carry its privacy policy in
three places. Check them before each submission:

1. **Description page.** The listing links to
   https://github.com/yeoblyv/liana/blob/main/PRIVACY.md, and the
   repository is public so the link opens.
2. **Link inside the app.** **Open online version** in the **Privacy
   policy** group of the dialog opens the same page.
3. **Text inside the app.** The same group shows the full text, from
   `src/Liana/privacy.py`. When `PRIVACY.md` changes, copy it into
   `POLICY_MARKDOWN`; the tests fail until the two match.

The policy keeps four sections: what data is collected and how it is used,
third parties, retention and deletion, and how users revoke consent or ask
for deletion. The listing icon is described in
[Brand and icons](brand-and-icons.md#marketplace-icon).

## See also

- [Workflow](workflow.md): the gates.
- [Testing in Fusion](fusion-test-checklist.md): manual checks before a release.

## References

- [R1]: https://semver.org/spec/v2.0.0.html "Semantic Versioning 2.0.0"
- [R2]: https://keepachangelog.com/en/1.1.0/ "Keep a Changelog 1.1.0"

## Changelog

- 1.0.0: page added.
