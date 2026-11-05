---
id: getting-started.quickstart
title: Quickstart
slug: /getting-started/quickstart
category: Getting started
since: 1.0.0
status: stable
---

[Docs](../README.md) / Getting started / Quickstart

# Quickstart

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)
![runtime](https://img.shields.io/badge/runtime-Autodesk%20Fusion-777bb4)

```bash
git clone https://github.com/yeoblyv/liana.git
cd liana
python scripts/build.py
```

The build needs only Python 3.12 or newer and git; it writes
`dist/Liana-<version>.zip`. Unpack it and add the `Liana` folder inside to
Fusion, as below, or download the same archive from the
[releases page](https://github.com/yeoblyv/liana/releases) instead of
building it.

## On this page

- [Run Liana in Fusion](#run-liana-in-fusion)
- [Build a first system](#build-a-first-system)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Run Liana in Fusion

1. In Fusion, open **Utilities > Add-Ins > Scripts and Add-Ins**.
2. Click **+**, choose **Script or add-in from device** and select the
   `Liana` folder.
3. Select **Liana** in the list and switch **Run** on. Tick **Run on
   Startup** to load it with Fusion.

The command appears as **Solid > Create > Liana**. Installation details,
updates and removal are in [Installation](installation.md) [R1].

## Build a first system

1. Open an empty design and choose **Solid > Create > Liana**.
2. In **Cables**, set the number of cradles and the cable diameter.
3. In **Printer bed**, enter your bed size. The summary at the bottom of
   the dialog shows each part's size and the largest cradle count that
   fits.
4. Click **Generate**.

Liana builds into the active design when it is an empty hybrid design, and
into a new design otherwise. A message reports what was built; when a
finishing feature such as a fillet could not be made, it names the log
file with the details, and the parts are still usable.

## See also

- [Dialog settings](../guides/dialog-settings.md): every setting of the dialog.
- [Printing and assembly](../guides/printing-and-assembly.md): from the design to the desk.

## References

- [R1]: installation.md#install "Installation - Install"

## Changelog

- 1.0.0: page added.
