---
id: architecture.overview
title: Architecture overview
slug: /architecture/overview
category: Architecture
since: 1.0.0
status: stable
---

[Docs](../README.md) / Architecture / Architecture overview

# Architecture overview

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)
![runtime](https://img.shields.io/badge/runtime-Python%20%3E%3D3.12-777bb4)

How the code of the add-in is organized, how a build runs from the dialog
to the finished design, and how errors and state are handled. Testing is
on its own page [R1].

## On this page

- [Repository layout](#repository-layout)
- [How a build runs](#how-a-build-runs)
- [Keeping sketches parametric](#keeping-sketches-parametric)
- [Errors](#errors)
- [Untrusted settings](#untrusted-settings)
- [State](#state)
- [API links](#api-links)
- [See also](#see-also)
- [References](#references)
- [Changelog](#changelog)

## Repository layout

| Path | Contents |
|---|---|
| `src/Liana/` | The add-in folder exactly as Fusion loads it. |
| `src/Liana/Liana.py` | Entry points `run` and `stop` that Fusion calls. |
| `src/Liana/addin.py` | `LianaAddIn`: registers the command and the build event, opens the dialog, runs builds. |
| `src/Liana/dialog.py` | Dialog layout, mapping between inputs and settings, live summary. |
| `src/Liana/handlers.py` | Fusion event handler classes that forward to callables and report errors. |
| `src/Liana/storage.py` | Last settings and build log in the add-in folder, written atomically. |
| `src/Liana/privacy.py` | The privacy policy text shown in the dialog; a test keeps it identical to `PRIVACY.md`. |
| `src/Liana/resources/` | Toolbar icons [R2]. |
| `src/Liana/core/` | Pure Python, no Fusion imports: settings, layout arithmetic, User Parameters, expression builders, texts. |
| `src/Liana/cad/` | Modelling with the Fusion API: sketches, features, the four parts, colors and the system. |
| `tests/` | Tests and an in-memory stand-in for the Fusion API (`tests/fake_adsk`). |
| `scripts/` | Quality gates, build, version bump, API docs, golden traces. |
| `assets/brand/` | Icon masters and the Marketplace icon. |

Fusion imports the add-in folder as a package, so modules import each
other with relative imports [R3].

## How a build runs

<!-- FIGURE: replace with docs/assets/build-flow.svg -->
```text
run() -> LianaAddIn.start() -> Solid > Create > Liana
  commandCreated -> SettingsDialog (settings from the design or the last run)
  inputChanged   -> summary;  validateInputs -> Generate on/off
  execute        -> save settings -> fire "lianaBuild"
  lianaBuild     -> generate(): update in place | rebuild | build new
                 -> write log -> message
```

1. Fusion calls `run`, which creates a `LianaAddIn` and calls `start`. The
   command is added to **Solid > Create** and a custom event `lianaBuild`
   is registered.
2. **Solid > Create > Liana** fires `commandCreated`. The dialog is filled
   from the settings stored in the active design, with the sizes its User
   Parameters hold now, or else from the last settings in the add-in
   folder. The dialog's help button opens `resources/help.html`.
3. Every input change refreshes the summary; `validateInputs` keeps
   **Generate** off while `core.settings.problems` reports anything.
4. **Generate** saves the settings and fires `lianaBuild` with them as
   JSON. The build runs from that event, after the command has closed,
   because it may open a new document.
5. `cad.system.generate` picks one of three paths:
   - the design holds a Liana system with the same topology
     (`core.layout.topology`): update the User Parameters in place and
     re-place the holder copies on the frame;
   - it holds a system with another topology: delete it and rebuild;
   - otherwise: build into the active design if it is an empty hybrid
     design, or into a new design.
6. `build_system` creates the User Parameters, one component per part, and
   calls the part builders. A failure in one part is logged and the other
   parts are still built; a failed fillet or chamfer is logged as skipped.
7. The log is written to the add-in folder and a message reports the
   result.

## Keeping sketches parametric

Every coordinate is an expression of User Parameters (`core.params`), such
as `END_X1 - END_R - 1 mm`. `cad.sketch.ParamSketch` draws each entity at
the current value of its expressions and then adds driving dimensions with
the same expressions, so the model follows a later change in **Change
Parameters**.

Fusion refuses a second distance dimension from the origin to a point that
sits on an already dimensioned coordinate, without tying the two points
together; such a point would stay behind when the parameter changes.
`ParamSketch` remembers the first point dimensioned with each expression
and aligns later points to it with a horizontal or vertical point
constraint, or a construction line on older Fusion releases.

One-sided extrudes and holes check their direction with probe points:
after a cut the probe must be empty, after a join it must be filled. A
wrong result is deleted and the other direction is tried.

## Errors

Calls that Fusion may refuse are wrapped in `except cad.api.API_ERRORS`
(RuntimeError, AttributeError, NotImplementedError, TypeError,
ValueError). A broad `except Exception` appears only where any failure
must be contained: optional finishing steps, one part of a build, the
rebuild fallback, `LianaAddIn.start` and `stop`, and the event handlers,
because Fusion drops exceptions raised in a handler without telling the
user.

## Untrusted settings

Settings read back from a file, a design or the build event may come from
anyone. `core.settings.from_mapping(..., within_limits=True)` keeps only
known keys with the type of their default and finite values inside the
dialog limits; everything else falls back to the default.

## State

The only module-level state is the running `LianaAddIn` in `Liana.py`,
because Fusion's entry points are module functions. Everything else is
passed explicitly: the add-in owns its handlers and the progress dialog,
and a `BuildContext` carries the design and the build log through one
build. `stop` also drops the add-in's modules from the import cache, so
that Run after an update loads the new code.

## API links

- [`Liana.addin`](../api/Liana.addin.md)
- [`Liana.cad.system`](../api/Liana.cad.system.md)
- [`Liana.cad.sketch`](../api/Liana.cad.sketch.md)
- [`Liana.core.settings`](../api/Liana.core.settings.md)

## See also

- [Testing](testing.md): how the code is tested without Fusion.
- [Workflow](../contributing/workflow.md): the gates every change passes.

## References

- [R1]: testing.md#testing-without-fusion "Testing - Testing without Fusion"
- [R2]: ../contributing/brand-and-icons.md#toolbar-icons "Brand and icons - Toolbar icons"
- [R3]: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PythonTemplate_UM.htm "Autodesk - Introduction to the Python Add-In Template"

## Changelog

- 1.0.0: page added.
