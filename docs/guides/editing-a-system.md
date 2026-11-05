---
id: guides.editing-a-system
title: Editing a system
slug: /guides/editing-a-system
category: Guides
since: 1.0.0
status: stable
---

[Docs](../README.md) / Guides / Editing a system

# Editing a system

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

How to change a design Liana built: sizes in **Change Parameters**, or any
setting by running Liana again on the same design, and which changes keep
the timeline and which rebuild the system.

## On this page

- [Change Parameters](#change-parameters)
- [Running Liana again](#running-liana-again)
- [What counts as layout](#what-counts-as-layout)
- [Markers in the design](#markers-in-the-design)
- [API links](#api-links)
- [See also](#see-also)
- [Changelog](#changelog)

## Change Parameters

Every size is a User Parameter: **Modify > Change Parameters** lists them
with a comment each. Sketches are dimensioned with these parameters, so
the model follows a change. Parameters marked "(derived)" are expressions
of the others; change the plain values instead.

## Running Liana again

Run **Solid > Create > Liana** on a design it built and the dialog opens
with that design's settings ("Editing the system in this design"),
including sizes changed in **Change Parameters** since. Then:

- If only sizes change, the User Parameters are updated in place and the
  model recomputes. The message says how many parameters changed.
- If the layout changes, the system is rebuilt in the same design. Edits
  made to the generated parts by hand are lost.

Tick **Build in a new design** to leave the design as it is.

## What counts as layout

| Setting | Why it rebuilds |
|---|---|
| Cradle count | Adds or removes cradles, teeth and screws. |
| T-pin and its side screws | Adds or removes the pin, slot and screws. |
| Raised teeth | Adds or removes the teeth. |
| Parts | Adds or removes components. |
| Frame preview | Adds or removes holder copies. |
| Nut seat face | Depends on the cable diameter: small cables get seats that open to the face the cables pass through, larger ones seats that open to the end faces. |

## Markers in the design

Liana finds its system through markers it stores on the components and
the dialog values it stores in the design. Renaming components is fine;
after deleting them the next run builds a new system.

## API links

- [`Liana.cad.system`](../api/Liana.cad.system.md): update, rebuild or build.
- [`Liana.core.layout`](../api/Liana.core.layout.md): `topology`, the layout comparison.
- [`Liana.cad.design`](../api/Liana.cad.design.md): parameters and stored settings.

## See also

- [Dialog settings](dialog-settings.md): every setting.
- [Architecture overview](../architecture/overview.md): how a build runs.

## Changelog

- 1.0.0: page added.
