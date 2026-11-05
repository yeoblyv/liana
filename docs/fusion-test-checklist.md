---
title: Testing in Fusion
summary: Manual checks in Fusion on Windows and macOS before a release.
audience: contributors
updated: 2026-11-05
---

# Testing in Fusion

The automated tests run against a stand-in for the Fusion API. Before a
release, run these checks in Fusion itself, on Windows and on macOS, with
the archive from `python scripts/build.py`. Note the Fusion version and
the operating system with the results.

## Install and start

1. Unpack `dist/Liana-<version>.zip` and add the `Liana` folder with
   **Utilities > Add-Ins > Scripts and Add-Ins > + > Script or add-in from
   device**.
2. Click **Run**. No error message appears.
3. **Solid > Create** shows the Liana command with its icon, in light and
   dark theme.
4. Restart Fusion with **Run on Startup** ticked: the command is there
   again.

## Dialog

1. Open the dialog in an empty design. The summary starts with
   "10 cradles", all groups are present, and the version next to
   **Privacy policy** matches the release.
2. Set cradles to 3: **Center T-pin** is greyed out.
3. Untick **X-frame**: **Show holders on the frame** is greyed out.
4. Set the bed to 100 x 100: the summary marks parts that do not fit and
   **Generate** is off. Restore the bed size.
5. Type an invalid length such as `abc`: **Generate** is off.
6. Click **Reset to defaults**: every value returns to its default.
7. Click **Privacy policy**: the policy opens in the default browser.

## Builds

For each row, build into a new empty design and check the result.

| Settings | Check |
|----------|-------|
| Defaults | Rail, comb, frame with 4 holder copies, tie mount; colours red, green, blue, green; the message reports no skipped features. |
| Cradles 1, cable 6 mm | Builds; summary says "no T-pin". |
| Cradles 5 | T-pin half a pitch off centre; 4 table screws if the summary says so. |
| Cradles 15, cable 3 mm | Builds; the nut seats open to the face the cables pass through. |
| Cable 25 mm, cradles 2 | Builds; the nut seats open to the end faces of the rail. |
| Mount T | Frame shows 3 holder copies. |
| Holder only, frame only, tie mount only | Only that part is built. |

For the default build also check:

1. An M3 nut model or a real printed part: the nut fits its seat and sits
   on the screw axis.
2. **Inspect > Interference** between rail and comb reports nothing.
3. **Modify > Change Parameters**: change `CABLE_D` from 10 to 12 mm. The
   cradles, teeth, end blocks and frame holes all follow, and the timeline
   shows no errors.

## Editing

1. Run Liana on the default design, change the cable diameter to 11 mm and
   the depth to 14 mm, click **Generate**. The message says "updated in
   place (3 parameters changed)".
2. Run it again and set cradles to 6. The message says "rebuilt in this
   design" and there is still exactly one Liana system.
3. Run it again with **Build in a new design** ticked: a new document opens
   with the system; the first design is unchanged.

## Files

1. After a build, the settings folder exists: `%APPDATA%\Liana` on Windows,
   `~/Library/Application Support/Liana` on macOS, with
   `last_settings.json` and `build_log.txt`.
2. Reopen the dialog in a new design: it starts from the last settings.
3. Check with a Windows user name that contains non-ASCII letters, if one
   is available.

## Stop

1. Click **Stop** in **Scripts and Add-Ins**: the command disappears from
   **Solid > Create** and no error message appears.
