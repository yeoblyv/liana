---
id: api.index
title: API reference
slug: /api
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / API

# API reference

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

Every public constant, class, function and method of the add-in, generated from the docstrings by `scripts/gen_api_docs.py`. Do not edit these pages by hand.

## On this page

- [Modules](#modules)
- [See also](#see-also)
- [Changelog](#changelog)

## Modules

| Module | Summary |
|---|---|
| [`Liana.Liana`](Liana.Liana.md) | Liana for Autodesk Fusion: parametric under-desk cable holders. |
| [`Liana._version`](Liana._version.md) | Version of the add-in; written by `scripts/bump_version.py`. |
| [`Liana.addin`](Liana.addin.md) | The add-in: registers the Liana command and runs builds. |
| [`Liana.cad`](Liana.cad.md) | Modelling with the Fusion API: sketches, features, parts and the system. |
| [`Liana.cad.api`](Liana.cad.api.md) | Thin helpers over the Fusion API used by every builder. |
| [`Liana.cad.appearance`](Liana.cad.appearance.md) | Part colors, so the rail, comb, frame and tie mount stay apart visually. |
| [`Liana.cad.comb`](Liana.cad.comb.md) | Comb: the lower half of the holder with the cable cradles. |
| [`Liana.cad.context`](Liana.cad.context.md) | State shared by the builders during one build. |
| [`Liana.cad.design`](Liana.cad.design.md) | Design-level helpers: documents, components, attributes and parameters. |
| [`Liana.cad.features`](Liana.cad.features.md) | Extrudes, combines, rounds and countersunk holes with checked directions. |
| [`Liana.cad.frame`](Liana.cad.frame.md) | X-frame: a square frame that carries holders on up to four sides. |
| [`Liana.cad.rail`](Liana.cad.rail.md) | Rail: the upper half of the holder, screwed to the table. |
| [`Liana.cad.sketch`](Liana.cad.sketch.md) | Sketches whose every coordinate is driven by a parameter expression. |
| [`Liana.cad.system`](Liana.cad.system.md) | Build, update or rebuild a whole Liana system in a design. |
| [`Liana.cad.tie_mount`](Liana.cad.tie_mount.md) | Tie mount: a small pad with two zip-tie tunnels and one screw. |
| [`Liana.core`](Liana.core.md) | Pure Python part of Liana: settings, layout arithmetic, parameters and texts. |
| [`Liana.core.expr`](Liana.core.expr.md) | Builders for Fusion parameter expressions and the outlines drawn with them. |
| [`Liana.core.layout`](Liana.core.layout.md) | Layout arithmetic shared by the dialog and the builders; no Fusion calls. |
| [`Liana.core.params`](Liana.core.params.md) | User Parameters that drive every sketch dimension of a Liana system. |
| [`Liana.core.report`](Liana.core.report.md) | Texts shown to the user: dialog summary, build log and result message. |
| [`Liana.core.settings`](Liana.core.settings.md) | Dialog settings: defaults, limits, validation and loading from untrusted JSON. |
| [`Liana.dialog`](Liana.dialog.md) | The Liana dialog: inputs, their mapping to settings and the live summary. |
| [`Liana.handlers`](Liana.handlers.md) | Fusion event handler classes that forward to plain callables. |
| [`Liana.privacy`](Liana.privacy.md) | The privacy policy, shipped inside the add-in and shown from the dialog. |
| [`Liana.storage`](Liana.storage.md) | Files Liana keeps between sessions: the last dialog settings and the build log. |

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
