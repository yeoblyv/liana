# `Liana.cad.system`

Build, update or rebuild a whole Liana system in a design.

## Constants

### `SYSTEM_NAME`

Name of the top component of a system.

### `TITLE`

Title of the progress dialog.

### `PartBuilder`

Function that models one part into an empty component.

## Classes

### `Progress`

```text
Progress dialog for builds.

One dialog is kept for the whole session: Fusion does not destroy a
dialog it created, so a new one per build would pile up hidden windows.
```

#### `Progress.__init__(self, ui: UserInterface | None) -> None`

```text
Create the reporter; the dialog itself is created on first use.

Args:
    ui: Fusion user interface, or None to report nothing.
```

#### `Progress.start(self, total: int) -> None`

```text
Show the dialog for a build of ``total`` steps.
```

#### `Progress.step(self, message: str) -> None`

```text
Advance by one step and show what is being built.
```

#### `Progress.close(self) -> None`

```text
Hide the dialog.
```

## Functions

### `seat_matrix(ctx: BuildContext, side: Side) -> object`

```text
Return the transform that puts a holder under one side of the frame.
```

### `seat_holders(ctx: BuildContext, system: Component, holder: Component, s: Settings) -> None`

```text
Show the holder on the frame sides chosen in the settings.

Each copy is inserted straight at its final position; moving occurrences
afterwards would rely on position snapshots that do not survive recompute.
```

### `reseat_holders(ctx: BuildContext, system_occ: Occurrence, s: Settings) -> None`

```text
Replace the holder copies on the frame after a size change.
```

### `build_system(ctx: BuildContext, s: Settings, progress: Progress) -> Occurrence`

```text
Build every enabled part into the design of ``ctx``.

Args:
    ctx: Build context.
    s: Settings.
    progress: Progress reporter.

Returns:
    The system occurrence.
```

### `generate(app: Application, s: Settings, progress: Progress) -> tuple[str, BuildLog]`

```text
Apply the dialog settings to the active design.

- A design that already holds a system with the same layout gets its
  parameters updated in place.
- A different layout is rebuilt in the same design.
- Otherwise the system is built into the active design when it is an
  empty hybrid design, or into a new design.

Args:
    app: Fusion application.
    s: Settings.
    progress: Progress reporter.

Returns:
    How the system was built, and the problems recorded.
```
