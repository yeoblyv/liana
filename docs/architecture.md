---
title: Architecture
summary: How the Liana code is organised, how a build runs and how it is tested without Fusion.
audience: contributors
updated: 2026-11-05
---

# Architecture

Liana is a Fusion add-in written in Python with no third-party
dependencies. This page describes the modules, the flow of a build, the way
sketches stay parametric, and the test strategy.

## Layout of the repository

| Path | Contents |
|------|----------|
| `src/Liana/` | The add-in folder exactly as Fusion loads it. |
| `src/Liana/Liana.py` | Entry points `run` and `stop` that Fusion calls [R2]. |
| `src/Liana/addin.py` | `LianaAddIn`: registers the command and the build event, opens the dialog, runs builds. |
| `src/Liana/dialog.py` | Dialog layout, mapping between inputs and settings, live summary. |
| `src/Liana/handlers.py` | Fusion event handler classes that forward to callables and report errors. |
| `src/Liana/storage.py` | Last settings and build log in the user data folder, written atomically. |
| `src/Liana/core/` | Pure Python, no Fusion imports: settings, layout arithmetic, User Parameters, expression builders, texts. |
| `src/Liana/cad/` | Modelling with the Fusion API: sketches, features, the four parts, colours and the system. |
| `tests/` | Tests, including an in-memory stand-in for the Fusion API (`tests/fake_adsk`). |
| `scripts/` | Quality gates, build, version bump, API docs, golden traces. |

Fusion imports the add-in folder as a package, so modules import each other
with relative imports [R2].

## How a build runs

1. Fusion calls `run`, which creates a `LianaAddIn` and calls `start`. The
   command is added to **Solid > Create** and a custom event `lianaBuild`
   is registered.
2. **Solid > Create > Liana** fires `commandCreated`. The dialog is filled
   from the settings stored in the active design, or else from the last
   settings in the user data folder.
3. Every input change refreshes the summary; `validateInputs` keeps
   **Generate** off while `core.settings.problems` reports anything.
4. **Generate** saves the settings and fires `lianaBuild` with them as
   JSON. The build runs from that event, after the command has closed,
   because it may open a new document.
5. `cad.system.generate` decides between three paths:
   - the design holds a Liana system with the same topology
     (`core.layout.topology`): update the User Parameters in place and
     re-place the holder copies on the frame;
   - it holds a system with another topology: delete it and rebuild;
   - otherwise: build into the active design if it is an empty hybrid
     design, or into a new design.
6. `build_system` creates the User Parameters, one component per part, and
   calls the part builders. A failure in one part is logged and the other
   parts are still built; a failed fillet or chamfer is logged as skipped.
7. The log is written to the user data folder and a message reports the
   result.

## Keeping sketches parametric

Every coordinate is an expression of User Parameters (`core.params`), such
as `END_X1 - END_R - 1 mm`. `cad.sketch.ParamSketch` draws each entity at
the current value of its expressions and then adds driving dimensions with
the same expressions, so the model follows a later change in **Change
Parameters**.

Fusion refuses a second distance dimension from the origin to a point that
sits on an already dimensioned coordinate, without tying the two points
together. Such a point would stay behind when the parameter changes.
`ParamSketch` therefore remembers the first point dimensioned with each
expression and aligns later points to it with a horizontal or vertical
point constraint (or a construction line on older Fusion releases).

One-sided extrudes and holes check their direction with probe points:
after a cut the probe must be empty, after a join it must be filled. A
wrong result is deleted and the other direction is tried.

## Errors

Calls that Fusion may refuse are wrapped in `except cad.api.API_ERRORS`
(RuntimeError, AttributeError, NotImplementedError). A broad
`except Exception` appears only at boundaries where any failure must be
contained: optional finishing steps, one part of a build, the rebuild
fallback, and the event handlers, because Fusion drops exceptions raised
in a handler without telling the user.

## State

The only module-level state is the running `LianaAddIn` in `Liana.py`,
because Fusion's entry points are module functions. Everything else is
passed explicitly: the add-in owns its handlers and the progress dialog,
and a `BuildContext` carries the design and the build log through one
build.

## Testing without Fusion

Fusion cannot run in CI, so `tests/fake_adsk` implements the part of the
API that Liana uses. It keeps enough geometry to check that every
dimension agrees with the drawn geometry and every constraint holds, and
it records each call that changes the design.

`tests/test_golden.py` runs 42 scenarios (cradle counts, cable sizes, part
combinations, updates, rebuilds, failure fallbacks) and compares the trace
with `tests/golden`, recorded from the release checked in Fusion. A
refactor that changes any sketch, dimension or feature, or their order,
fails there. Unit tests cover the fallbacks, the dialog, storage and the
add-in lifecycle. What the fake cannot show (real geometry, fillets, the
look of the dialog) is covered by the [manual checks in
Fusion](fusion-test-checklist.md).

## References

- [R2] Autodesk, "Introduction to the Python Add-In Template",
  https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PythonTemplate_UM.htm
