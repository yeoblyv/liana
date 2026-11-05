# `Liana.cad.appearance`

Part colours, so the rail, comb, frame and tie mount stay apart visually.

## Constants

### `APPEARANCE_LIBRARY_ID`

Id of the Fusion Appearance Library.

### `BASE_APPEARANCES`

Library appearances to copy, in order of preference.

### `PART_COLORS`

Component name to appearance name and RGB colour.

## Functions

### `part_appearance(app: Application, design: Design, name: str, rgb: tuple[int, int, int]) -> Any`

```text
Return the named appearance of the design, creating it on first use.

A plastic appearance from the Fusion library is copied into the design and
its colour property is set.

Args:
    app: Fusion application.
    design: Design that owns the appearance.
    name: Appearance name.
    rgb: Colour.

Returns:
    The appearance.

Raises:
    RuntimeError: The copied appearance has no colour property.
```

### `paint_parts(app: Application, design: Design) -> None`

```text
Colour every Liana part of the design: rail red, comb green, frame blue.
```
