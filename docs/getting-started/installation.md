---
id: getting-started.installation
title: Installation
slug: /getting-started/installation
category: Getting started
since: 1.0.0
status: stable
---

[Docs](../README.md) / Getting started / Installation

# Installation

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)
![runtime](https://img.shields.io/badge/runtime-Autodesk%20Fusion-777bb4)

How to install Liana in Fusion on Windows or macOS, check the download,
update to a new release and remove the add-in.

## On this page

- [Install](#install)
- [Check the download](#check-the-download)
- [Update](#update)
- [Remove](#remove)
- [Files Liana keeps](#files-liana-keeps)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Install

1. Download `Liana-<version>.zip` from the
   [releases page](https://github.com/yeoblyv/liana/releases).
2. Unpack it. Inside is a folder named `Liana`; on Windows, **Extract All**
   puts it in a folder named after the archive. Use the inner folder and
   keep its name: Fusion expects the folder, `Liana.py` and
   `Liana.manifest` to share one name [R1].
3. Move the folder somewhere permanent, for example
   `Documents\Fusion add-ins\Liana`. Fusion loads the add-in from wherever
   you add it.
4. In Fusion, open **Utilities > Add-Ins > Scripts and Add-Ins**, click
   **+** and choose **Script or add-in from device**, then select the
   `Liana` folder.
5. Select **Liana**, switch **Run** on and tick **Run on Startup**.

The command now appears as **Solid > Create > Liana**.

## Check the download

`Liana-<version>.zip.sha256` next to the archive holds its SHA-256
checksum. Compare it with:

```powershell
Get-FileHash .\Liana-1.0.0.zip -Algorithm SHA256
```

```bash
shasum -a 256 Liana-1.0.0.zip
```

## Update

1. In **Scripts and Add-Ins**, switch Liana's **Run** off.
2. Replace the contents of your `Liana` folder with the new release.
3. Switch **Run** on again. Stopping the add-in drops its modules from
   memory, so the new code loads; restarting Fusion works as well.

The last dialog settings live in the add-in folder, so after an update the
dialog starts from the defaults. Systems in designs keep their own
settings.

## Remove

1. In **Scripts and Add-Ins**, select **Liana**, switch **Run** off and
   untick **Run on Startup**.
2. Delete the `Liana` add-in folder. The settings and the log go with it.

Designs built with Liana keep working without the add-in; they are
ordinary parametric Fusion designs.

## Files Liana keeps

| File | Contents |
|---|---|
| `last_settings.json` | The last values of the dialog. |
| `build_log.txt` | Report of the last build. |

They are in the add-in folder, next to `Liana.py`; when the folder is
read-only, nothing is stored. The [privacy policy](../../PRIVACY.md)
describes them in full.

## See also

- [Quickstart](quickstart.md): build a first system.
- [Editing a system](../guides/editing-a-system.md): change a design after the first build.

## References

- [R1]: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PythonTemplate_UM.htm "Autodesk - Introduction to the Python Add-In Template"

## Changelog

- 1.0.0: page added.
