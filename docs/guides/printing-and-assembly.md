---
id: guides.printing-and-assembly
title: Printing and assembly
slug: /guides/printing-and-assembly
category: Guides
since: 1.0.0
status: stable
---

[Docs](../README.md) / Guides / Printing and assembly

# Printing and assembly

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

How to export the parts, print them, and mount a holder under a table,
with the hardware the default sizes need.

## On this page

- [Export](#export)
- [Print](#print)
- [Hardware](#hardware)
- [Assembly](#assembly)
- [Before you mount](#before-you-mount)
- [See also](#see-also)
- [Changelog](#changelog)

## Export

Right-click each component (Rail, Comb, X-Frame, Tie Mount) in the browser
and choose **Save As Mesh**.

## Print

- Use PLA or PETG.
- Print one holder first and check the fit of the comb, the nut seats and
  the screws before printing a batch.
- The parts are designed to print with their table side on the bed: the
  rail, the frame and the tie mount lie on the face that touches the
  table, and the comb lies on its bottom face. This orientation has not
  yet been confirmed on test prints of every size.
- If your printer prints holes tight, raise the hole, nut seat or
  clearance values in the dialog.

## Hardware

| Part | Hardware (default sizes) |
|---|---|
| Holder | 2 countersunk wood screws 3.5 mm (4 when the summary says "4 table screws"), 2 M3 countersunk screws DIN 965 and 2 M3 nuts. The summary shows the M3 length. |
| X-frame | 4 countersunk wood screws 3.5 mm at the corners. Holder screws pass through the holder and the frame, so use longer ones there; the summary shows the engagement. |
| Tie mount | 1 countersunk wood screw 3.5 mm and a zip tie up to 4.8 mm wide. |

## Assembly

1. Push an M3 nut into each nut seat of the rail.
2. Screw the rail under the table, through the frame if you use one.
3. Lay the cables into the comb and slide the comb into the rail from the
   side.
4. Insert the M3 screws from the bottom of the comb and tighten them until
   the comb holds the cables.

## Before you mount

> **Warning.** Liana gives you the geometry; how well it holds depends on
> your printer, filament and screws. Check that a test holder and the
> screws suit your table and the weight of your cables, and do not hang
> anything heavy on it. Liana is provided as is: you print and mount the
> parts at your own risk.

## See also

- [Dialog settings](dialog-settings.md): hole sizes and clearances.

## Changelog

- 1.0.0: page added.
