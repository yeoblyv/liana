---
title: Getting started
summary: Install Liana in Fusion, build a first system, update and remove the add-in.
audience: users
updated: 2026-11-05
---

# Getting started

This page takes you from the download to a first cable holder in Fusion, on
Windows or macOS.

## Install

1. Download `Liana-<version>.zip` from the
   [releases page](https://github.com/yeoblyv/liana/releases). The file
   `Liana-<version>.zip.sha256` next to it holds its SHA-256 checksum.
2. Unpack the archive. Keep the folder named `Liana`; Fusion expects the
   folder, the `Liana.py` file and the `Liana.manifest` file to share one
   name [R2].
3. Move the folder somewhere permanent, for example `Documents\Fusion
   add-ins\Liana`. Fusion loads the add-in from wherever you add it.
4. In Fusion, open **Utilities > Add-Ins > Scripts and Add-Ins**.
5. Click **+** and choose **Script or add-in from device**, then select the
   `Liana` folder.
6. Select **Liana** in the list, click **Run**, and tick **Run on
   Startup** so it loads with Fusion.

The command now appears as **Solid > Create > Liana**.

To check the download on Windows, run this in PowerShell and compare the
result with the `.sha256` file:

```powershell
Get-FileHash .\Liana-1.0.0.zip -Algorithm SHA256
```

On macOS: `shasum -a 256 Liana-1.0.0.zip`.

## Build a first system

1. Open a new, empty design.
2. Choose **Solid > Create > Liana**.
3. In **Cables**, set the number of cradles and the cable diameter.
4. In **Printer bed**, enter your bed size. The summary at the bottom shows
   each part's size and the largest cradle count that fits.
5. Click **Generate**.

Liana builds into the active design when it is empty, and into a new design
otherwise. A message tells you what was built. If a finishing feature such
as a fillet could not be made, the message names the log file with the
details; the parts are still usable.

## Change a system

- **Sizes:** **Modify > Change Parameters** lists every Liana size as a
  User Parameter. Change one and the model follows.
- **Layout:** run **Solid > Create > Liana** on the same design. The dialog
  opens with the settings of that design. If only sizes change, the
  parameters are updated in place; a new cradle count, pin or set of parts
  rebuilds the system in the same design.

## Update

Download the new release, replace the contents of your `Liana` folder with
the new one, and restart Fusion. Your last dialog settings are kept in your
user data folder, not in the add-in folder, so they survive the update.

## Remove

1. In **Utilities > Add-Ins > Scripts and Add-Ins**, select **Liana**,
   click **Stop** and untick **Run on Startup**.
2. Delete the `Liana` add-in folder.
3. Optionally delete Liana's settings folder: `%APPDATA%\Liana` on Windows,
   `~/Library/Application Support/Liana` on macOS.

Designs you built keep working without the add-in; they are ordinary
parametric Fusion designs.

## References

- [R2] Autodesk, "Introduction to the Python Add-In Template",
  https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PythonTemplate_UM.htm
