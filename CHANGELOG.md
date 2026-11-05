# Changelog

All notable changes to Liana are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-05

First public release.

### Added

- Command **Solid > Create > Liana** with one dialog for cables, parts,
  holder, frame, tie mount and printer bed settings.
- Holder with 1 to 15 cradles for cables of 3 to 25 mm: a rail screwed to
  the table and a comb that slides into it, pulled tight with two M3 screws
  whose nuts sit in hex seats.
- Optional raised teeth between the cradles and a center T-pin for combs
  with 4 or more cradles, with side screws when there is room.
- X-frame for straight runs, L-turns, T-branches and crossings, with
  locating ribs and through holes for the holder screws.
- Zip-tie mount with two tunnels and one screw.
- Printer bed check with the largest cradle count that fits; Generate stays
  off until every part fits.
- Parametric result: User Parameters, sketches dimensioned with
  expressions, full timeline. Running Liana on the same design updates the
  parameters in place, or rebuilds the system when the layout changes.
- Part colors: rail red, comb green, frame blue, tie mount green.
- Toolbar icon in SVG for the Light Gray and Dark Blue themes.
- Editing a system starts from the sizes in its User Parameters, so
  changes made in Change Parameters are kept.
- Privacy policy group in the dialog with the full policy text and a
  button that opens its online version; the version number is shown
  next to it.
- Settings and build log stored in the user data folder, so they survive
  add-in updates.

[Unreleased]: https://github.com/yeoblyv/liana/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yeoblyv/liana/releases/tag/v1.0.0
