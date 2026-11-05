---
id: contributing.brand-and-icons
title: Brand and icons
slug: /contributing/brand-and-icons
category: Contributing
since: 1.0.0
status: stable
---

[Docs](../README.md) / Contributing / Brand and icons

# Brand and icons

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

The Liana mark, its colors and type, and which icon file goes where. The
mark is one U-cradle of the holder comb with the cable in signal red; the
source files are in `assets/brand/`.

## On this page

- [Toolbar icons](#toolbar-icons)
- [Marketplace icon](#marketplace-icon)
- [Masters](#masters)
- [Colors and type](#colors-and-type)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Toolbar icons

`src/Liana/resources/` holds the command icons as SVG, the format Fusion
prefers; Fusion renders SVG at the resolution a high-density display needs,
so no `@2x` files are needed [R1].

| File | Theme |
|---|---|
| `16x16.svg`, `32x32.svg` | Light Gray: graphite mark |
| `16x16-dark_blue.svg`, `32x32-dark_blue.svg` | Dark Blue: light mark |

Fusion picks the `-dark_blue` file in the Dark Blue theme and the file
without a token otherwise [R1]. The 16 px icon is drawn on its own 16-pixel
grid so it stays sharp; the 32 px icon on a 32-pixel grid.

`assets/brand/fusion-png/` holds the same icons as PNG (16, 32 and 64 px,
with `@2x` versions) as a fallback if the SVGs ever render wrong. Use one
set at a time: do not mix SVG and PNG files in the resource folder.

## Marketplace icon

Upload `assets/brand/marketplace/liana-marketplace-icon-120.png` to the
Autodesk Marketplace listing (120 x 120 px, framed). The 240, 512 and
1024 px files are the same icon for high-density screens, the website and
social posts; `-dark` files show it on a graphite tile. The `.svg` files
are the editable masters.

## Masters

| File | Use |
|---|---|
| `assets/brand/master/liana-icon.svg` | Full hatched mark on a transparent background, 64 px and up. |
| `liana-icon-simple.svg`, `liana-icon-simple-16px.svg` | Solid versions for 32 px and below. |
| `-dark` versions | Dark backgrounds. |
| `-1024.png` | Renders. |

## Colors and type

| Name | Hex | Use |
|---|---|---|
| Graphite | `#141619` | ink, outlines, hatching |
| Paper | `#F3F3F1` | light background |
| Signal red | `#D7362B` | the cable, the only accent |
| Light ink | `#E6E8EB` | ink on dark backgrounds |

Wordmark: Barlow SemiBold, capitals, tracked. Secondary text: IBM Plex
Mono. Both fonts are under the SIL Open Font License.

## See also

- [Releasing](releasing.md#autodesk-marketplace-requirements): what a Marketplace submission needs.

## References

- [R1]: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserInterface_UM.htm "Autodesk - User Interface Customization with Fusion's API"

## Changelog

- 1.0.0: page added.
