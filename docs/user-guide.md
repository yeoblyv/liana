---
title: User guide
summary: Every setting of the Liana dialog, what Liana builds, printing, hardware and assembly.
audience: users
updated: 2026-11-05
---

# User guide

This page explains the Liana dialog setting by setting, then how to print
and mount the parts. Installation is in [Getting started](getting-started.md).

## The parts

| Part      | What it is |
|-----------|------------|
| Rail      | Screwed under the table. Ears at both ends carry the wood screws; end blocks reach down to the cable axis and hold the M3 nuts. |
| Comb      | One cradle per cable. It slides into the rail from the side and is pulled up against the rail by two M3 screws, so the cables are held between comb and rail. |
| X-frame   | A square frame with a holder position on each side, for straight runs, L-turns, T-branches and crossings. Ribs on its underside locate the holders; the holder screws pass through the frame into the table. |
| Tie mount | A pad with two tunnels for a zip tie and one screw, for single cables and bundles along the route. |

In the design, the rail is red, the comb and tie mount green and the frame
blue. Each part is its own component, modelled in its own region of the
design, so a cut in one part never reaches another.

## Dialog settings

Lengths are in millimeters. The summary at the bottom of the dialog updates
as you type: cradle count and pitch, part sizes against the printer bed,
the largest cradle count that fits, the hardware and the screw engagement.
**Generate** stays off while a problem is listed there.

### Cables

| Setting | Meaning |
|---------|---------|
| Cradles per holder | 1 to 15. |
| Cable diameter | Cradle diameter, 3 to 25 mm. The pitch is cable diameter plus tooth width. |
| Tooth width | Width of the teeth between cradles. The summary suggests at least 15 % of the cable diameter. |
| Raised teeth (U-cradles) | Teeth reach the top of the cables, so a cable cannot wander into the next cradle. |
| Center T-pin (4+ cradles) | A pin on the comb hooks into a slot in the rail and stops a long comb from sagging. When there is room, two extra table screws are added next to it. |

### Parts

| Setting | Meaning |
|---------|---------|
| Holder (rail + comb) | Build the holder. |
| X-frame | Build the frame. |
| Tie mount | Build the tie mount. |
| Show holders on the frame | Which frame sides show a copy of the holder in the design: none, straight run, L-turn, T-branch or X-cross. This is a preview only; you print one holder per side you use. |
| Build in a new design | Leave the active design untouched and build in a new one. |

### Holder

| Setting | Default | Meaning |
|---------|---------|---------|
| Depth (along the cable) | 12 | Holder depth. A frame beam widens to depth + 4.5 mm to make room for the locating ribs. |
| Wood screw hole | 4.2 | Clearance hole for a 3.5 mm wood screw. |
| Wood screw countersink | 8.4 | Countersink diameter at the surface, for a 7 mm head. |
| Wood screw length | 20 | Used for the summary only: how deep the screw bites into the table. Below 10 mm the summary asks for longer screws. |
| M3 hole | 3.4 | Clearance hole for the M3 screws. |
| M3 nut seat (across flats) | 6.0 | Hex seat for the M3 nut (5.5 mm across flats plus clearance), so the nut slides in by hand. |
| Pin / slot clearance | 0.2 | Side clearance of the T-pin in its slot, per side. |

### X-frame

| Setting | Default | Meaning |
|---------|---------|---------|
| Thickness | 4 | Frame plate thickness. |
| Beam width | 18 | Beam width; widened automatically for deep holders. |

### Tie mount

| Setting | Default | Meaning |
|---------|---------|---------|
| Length, Width, Height | 36, 14, 6.5 | Outer size of the pad. |
| Tie tunnel width | 5.2 | Fits zip ties up to this width minus about 0.4 mm. |

### Printer bed

| Setting | Default | Meaning |
|---------|---------|---------|
| Bed X, Bed Y | 256, 256 | Printable area. |
| Margin from the edge | 5 | Kept free on every side. |

A rail longer than the bed may still fit diagonally; the summary says so.
The frame must fit the shorter side of the bed.

**Privacy policy**, a collapsed group above the summary, holds the full
privacy policy; its **Open online version** button opens the policy page in
your browser, and the version of Liana is shown next to it. **Reset to
defaults** restores every value.

## Editing a system

Run Liana on a design it built and the dialog opens with that design's
settings ("Editing the system in this design"), including sizes you changed
in **Change Parameters** since. Then:

- If only sizes change, the User Parameters are updated in place and the
  model recomputes.
- If the layout changes, the system is rebuilt in the same design. Edits
  you made to the generated parts by hand are lost. The layout is: the
  cradle count, the T-pin and its side screws, raised teeth, the set of
  parts, the frame preview, and the face the nut seats open to, which
  depends on the cable diameter (small cables get seats that open to the
  face the cables pass through).

Liana finds its system through markers it stores on the components.
Renaming components is fine; after deleting them the next run builds a new
system.

Every size is also a User Parameter, so you can change it in **Modify >
Change Parameters** without the dialog. Parameters marked "(derived)" are
expressions of the others; change the plain values instead.

## Printing

1. Right-click each component (Rail, Comb, X-Frame, Tie Mount) and choose
   **Save As Mesh** to export it.
2. Use PLA or PETG.
3. Print one holder first and check the fit of the comb, the nut seats and
   the screws before printing a batch.

The parts are designed to print with their table side on the bed: the
rail, the frame and the tie mount lie on the face that touches the table,
and the comb lies on its bottom face. This orientation has not yet been
confirmed on test prints of every size.

If your printer prints holes tight, raise the hole, nut seat or clearance
values in the dialog.

## Hardware and assembly

With the default sizes:

| Part      | Hardware |
|-----------|----------|
| Holder    | 2 countersunk wood screws 3.5 mm (4 when the summary says "4 table screws"), 2 M3 countersunk screws DIN 965 and 2 M3 nuts. The summary shows the M3 length. |
| X-frame   | 4 countersunk wood screws 3.5 mm at the corners. Holder screws pass through the holder and the frame, so use longer ones there; the summary shows the engagement. |
| Tie mount | 1 countersunk wood screw 3.5 mm and a zip tie up to 4.8 mm wide. |

1. Push an M3 nut into each nut seat of the rail.
2. Screw the rail under the table (through the frame, if you use one).
3. Lay the cables into the comb and slide the comb into the rail from the
   side.
4. Insert the M3 screws from the bottom of the comb and tighten them until
   the comb holds the cables.

## Before you mount

Liana gives you the geometry; how well it holds depends on your printer,
filament and screws. Check that a test holder and the screws suit your
table and the weight of your cables, and do not hang anything heavy on it.
Liana is provided as is: you print and mount the parts at your own risk.
