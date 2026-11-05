---
id: contributing.fusion-test-checklist
title: Testing in Fusion
slug: /contributing/fusion-test-checklist
category: Contributing
since: 1.0.0
status: stable
---

[Docs](../README.md) / Contributing / Testing in Fusion

# Testing in Fusion

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)
![runtime](https://img.shields.io/badge/runtime-Autodesk%20Fusion-777bb4)

The checks to run in Fusion itself, on Windows and on macOS, with the
archive from `python scripts/build.py`, before a release. Note the Fusion
version and the operating system with the results.

## On this page

- [Install and start](#install-and-start)
- [Dialog](#dialog)
- [Builds](#builds)
- [Editing](#editing)
- [Files](#files)
- [Stop and run](#stop-and-run)
- [See also](#see-also)
- [Changelog](#changelog)

## Install and start

1. Unpack `dist/Liana-<version>.zip` into a new, empty folder and add the
   inner `Liana` folder with **Utilities > Add-Ins > Scripts and Add-Ins >
   + > Script or add-in from device**.
2. Switch **Run** on. No error message appears.
3. **Solid > Create** shows the Liana command with its icon, in the Light
   Gray and the Dark Blue theme.
4. Restart Fusion with **Run on Startup** ticked: the command is there
   again.
5. Bundle: with Fusion closed, unpack `dist/Liana-<version>.bundle.zip`
   into the ApplicationPlugins folder (`%APPDATA%\Autodesk\ApplicationPlugins`
   on Windows, `~/Library/Application Support/Autodesk/ApplicationPlugins`
   on macOS) and start Fusion: Liana runs without being added by hand.
   Remove any other copy of Liana from **Scripts and Add-Ins** first.

## Dialog

1. Open the dialog in an empty design. The summary starts with
   "10 cradles", every group is present, and the version next to **Open
   online version** in the **Privacy policy** group matches the build.
2. Set cradles to 3: **Center T-pin** is grayed out.
3. Untick **X-frame**: **Show holders on the frame** is grayed out.
4. Set the bed to 100 x 100: the summary marks parts that do not fit and
   **Generate** is off. Restore the bed size.
5. Type an invalid length such as `abc`, then clear the field: in both
   cases **Generate** is off and nothing fails.
6. Click **Reset to defaults**: every value returns to its default. A box
   that held letters stays red until you type a number into it.
7. Expand **Privacy policy**: the full policy, sections 1 to 4, scrolls in
   the text box. **Open online version** opens the policy page in the
   default browser.
8. The help button at the bottom left of the dialog, and F1, open the help
   page in the default browser.

## Builds

Build each row into a new design (tick **Build in a new design** after the
first one) and check the result.

| Settings | Check |
|---|---|
| Defaults | Rail, comb, frame with 4 holder copies, tie mount; colors red, green, blue, green; the message reports no skipped features. |
| Cradles 1, cable 6 mm | Builds; the summary says "no T-pin". |
| Cradles 5 | T-pin half a pitch off center. |
| Cradles 15, cable 3 mm | Builds; the nut seats open to the face the cables pass through. |
| Cable 25 mm, cradles 2 | Builds; the nut seats open to the end faces of the rail. |
| Mount T | The browser shows 3 holder copies besides the holder. |
| Holder only, frame only, tie mount only | Only that part is built. |

For the default build also check:

1. A real nut or a nut model fits its seat and sits on the screw axis.
2. **Inspect > Interference** between rail and comb reports nothing.
3. **Modify > Change Parameters**: change `CABLE_D` from 10 to 12 mm. The
   cradles, teeth, end blocks and frame holes follow, and the timeline
   shows no warnings.

## Editing

1. Run Liana on the default design, set the cable diameter to 11 mm and
   the depth to 14 mm, click **Generate**: "updated in place (3 parameters
   changed)".
2. Change a size in **Change Parameters**, then open Liana: the dialog
   shows the changed size.
3. Run it again with 6 cradles: "rebuilt in this design", and the browser
   still shows one Liana system.
4. Run it again with **Build in a new design** ticked: a new document
   opens; the first design is unchanged.

## Files

1. After a build, the add-in folder holds `last_settings.json` and
   `build_log.txt`.
2. Restart Fusion and open the dialog in a new design: it starts from the
   last settings.

## Stop and run

1. Switch **Run** off in **Scripts and Add-Ins**: the command disappears
   from **Solid > Create**, with no error message.
2. Replace the add-in files with a newer build and switch **Run** on: the
   dialog shows the newer version.

## See also

- [Testing](../architecture/testing.md): the automated tests.
- [Releasing](releasing.md): where these checks fit in a release.

## Changelog

- 1.0.0: page added.
