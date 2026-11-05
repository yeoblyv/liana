---
id: guides.dialog-settings
title: Dialog settings
slug: /guides/dialog-settings
category: Guides
since: 1.0.0
status: stable
---

[Docs](../README.md) / Guides / Dialog settings

# Dialog settings

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

What Liana builds and what every setting of its dialog does. Lengths are
in millimetres. The summary at the bottom of the dialog updates as you
type: cradle count and pitch, part sizes against the printer bed, the
largest cradle count that fits, the hardware and the screw engagement.
**Generate** stays off while the summary lists a problem.

## On this page

- [The parts](#the-parts)
- [Cables](#cables)
- [Parts](#parts)
- [Holder](#holder)
- [X-frame](#x-frame)
- [Tie mount](#tie-mount)
- [Printer bed](#printer-bed)
- [Privacy policy](#privacy-policy)
- [Help](#help)
- [API links](#api-links)
- [See also](#see-also)
- [Changelog](#changelog)

## The parts

| Part | What it is |
|---|---|
| Rail | Screwed under the table. Ears at both ends carry the wood screws; end blocks reach down to the cable axis and hold the M3 nuts. |
| Comb | One cradle per cable. It slides into the rail from the side and is pulled up against the rail by two M3 screws, so the cables are held between comb and rail. |
| X-frame | A square frame with a holder position on each side, for straight runs, L-turns, T-branches and crossings. Ribs on its underside locate the holders; the holder screws pass through the frame into the table. |
| Tie mount | A pad with two tunnels for a zip tie and one screw, for single cables and bundles along the route. |

In the design the rail is red, the comb and the tie mount green and the
frame blue. Each part is its own component, modelled in its own region of
the design, so a cut in one part never reaches another.

## Cables

| Setting | Meaning |
|---|---|
| Cradles per holder | 1 to 15. |
| Cable diameter | Cradle diameter, 3 to 25 mm. The pitch is cable diameter plus tooth width. |
| Tooth width | Width of the teeth between cradles. The summary suggests at least 15 % of the cable diameter. |
| Raised teeth (U-cradles) | Teeth reach the top of the cables, so a cable cannot wander into the next cradle. |
| Center T-pin (4+ cradles) | A pin on the comb hooks into a slot in the rail and stops a long comb from sagging. When there is room, two extra table screws are added next to it. |

## Parts

| Setting | Meaning |
|---|---|
| Holder (rail + comb) | Build the holder. |
| X-frame | Build the frame. |
| Tie mount | Build the tie mount. |
| Show holders on the frame | Which frame sides show a copy of the holder: none, straight run, L-turn, T-branch or X-cross. A preview only; print one holder per side you use. |
| Build in a new design | Leave the active design untouched and build in a new one. |

## Holder

| Setting | Default | Meaning |
|---|---|---|
| Depth (along the cable) | 12 | Holder depth. A frame beam widens to depth + 4.5 mm to make room for the locating ribs. |
| Wood screw hole | 4.2 | Clearance hole for a 3.5 mm wood screw. |
| Wood screw countersink | 8.4 | Countersink diameter at the surface, for a 7 mm head. |
| Wood screw length | 20 | Used for the summary only: how deep the screw bites into the table. Below 10 mm the summary asks for longer screws. |
| M3 hole | 3.4 | Clearance hole for the M3 screws. |
| M3 nut seat (across flats) | 6.0 | Hex seat for the M3 nut (5.5 mm across flats plus clearance), so the nut slides in by hand. |
| Pin / slot clearance | 0.2 | Side clearance of the T-pin in its slot, per side. |

## X-frame

| Setting | Default | Meaning |
|---|---|---|
| Thickness | 4 | Frame plate thickness. |
| Beam width | 18 | Beam width; widened automatically for deep holders. |

## Tie mount

| Setting | Default | Meaning |
|---|---|---|
| Length, Width, Height | 36, 14, 6.5 | Outer size of the pad. |
| Tie tunnel width | 5.2 | Fits zip ties up to this width minus about 0.4 mm. |

## Printer bed

| Setting | Default | Meaning |
|---|---|---|
| Bed X, Bed Y | 256, 256 | Printable area. |
| Margin from the edge | 5 | Kept free on every side. |

A rail longer than the bed may still fit diagonally; the summary says so.
The frame must fit the shorter side of the bed. **Reset to defaults**
restores every value.

## Privacy policy

A collapsed group above the summary holds the full privacy policy. Its
**Open online version** button opens the policy page in your browser; the
version of Liana is shown next to it.

## Help

The help button at the bottom left of the dialog opens a help page that
ships with the add-in, in your default browser. It works offline and links
to this documentation.

## API links

- [`Liana.dialog`](../api/Liana.dialog.md): the dialog layout and its mapping to settings.
- [`Liana.core.settings`](../api/Liana.core.settings.md): defaults and limits.
- [`Liana.core.layout`](../api/Liana.core.layout.md): sizes and the printer bed check.

## See also

- [Editing a system](editing-a-system.md): what happens when you run Liana again.
- [Printing and assembly](printing-and-assembly.md): hardware for these settings.

## Changelog

- 1.0.0: page added.
