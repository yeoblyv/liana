---
title: Brand and icons
summary: The Liana mark, its colors, and which icon file goes where.
audience: contributors
updated: 2026-11-05
---

# Brand and icons

The Liana mark is one U-cradle of the holder comb with the cable in signal
red. The source files are in `assets/brand/`.

## Toolbar icons

`src/Liana/resources/` holds the command icons as SVG, the format Fusion
prefers; Fusion renders SVG at the resolution a high-density display needs,
so no `@2x` files are needed [R8].

| File | Use |
|------|-----|
| `16x16.svg`, `32x32.svg` | Light Gray theme: graphite mark |
| `16x16-dark_blue.svg`, `32x32-dark_blue.svg` | Dark Blue theme: light mark |

Fusion picks the `-dark_blue` file in the Dark Blue theme and the file
without a token otherwise [R8]. The 16 px icon is drawn on its own 16-pixel
grid so it stays sharp; the 32 px icon on a 32-pixel grid.

`assets/brand/fusion-png/` holds the same icons as PNG (16, 32 and 64 px
with `@2x` versions), as a fallback if the SVGs ever render wrong. Use one
set at a time: do not mix SVG and PNG files in the resource folder.

## Marketplace icon

Upload `assets/brand/marketplace/liana-marketplace-icon-120.png` to the
Autodesk Marketplace listing (120 x 120 px, framed). The 240, 512 and
1024 px files are the same icon for high-density screens, the website and
social posts; `-dark` files show it on a graphite tile. The `.svg` files are
the editable masters.

## Masters

- `assets/brand/master/liana-icon.svg`: the full hatched mark on a
  transparent background, for 64 px and up.
- `liana-icon-simple.svg` and `liana-icon-simple-16px.svg`: solid versions
  for 32 px and below.
- `-dark` versions for dark backgrounds; `-1024.png` are renders.

## Colors and type

| Name | Hex | Use |
|------|-----|-----|
| Graphite | `#141619` | ink, outlines, hatching |
| Paper | `#F3F3F1` | light background |
| Signal red | `#D7362B` | the cable, the only accent |
| Light ink | `#E6E8EB` | ink on dark backgrounds |

Wordmark: Barlow SemiBold, capitals, tracked. Secondary text: IBM Plex
Mono. Both fonts are under the SIL Open Font License.

## References

- [R8] Autodesk, "User Interface Customization with Fusion's API",
  https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserInterface_UM.htm
