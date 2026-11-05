# `Liana.cad.design`

Design-level helpers: documents, components, attributes and parameters.

## Constants

### `ATTR_GROUP`

Attribute group of everything Liana stores in a design.

## Functions

### `tag(occ: Occurrence, place: str) -> None`

```text
Mark an occurrence with its role, e.g. ``"seat:S"``.
```

### `new_comp(parent: Component, name: str, place: str | None=None) -> Occurrence`

```text
Add a new component at identity under ``parent``.

Args:
    parent: Parent component.
    name: Component name.
    place: Optional role tag (see :func:`tag`).

Returns:
    The new occurrence.
```

### `find_system(design: Design | None) -> Occurrence | None`

```text
Return the Liana system occurrence of a design, if there is one.
```

### `load_design_settings(design: Design) -> Settings | None`

```text
Return the settings stored in a design, or None if there are none.

The stored JSON is untrusted: the design may come from anyone.
```

### `save_design_settings(design: Design, s: Settings) -> None`

```text
Store the settings in the design, so running Liana again edits it.
```

### `upsert_params(design: Design, s: Settings) -> int`

```text
Create missing User Parameters and update the ones that differ.

Changed parameters are set in one call, so the design recomputes once.

Args:
    design: Design to update.
    s: Settings.

Returns:
    Number of parameters whose expression changed.
```

### `is_hybrid(design: Design) -> bool`

```text
Return whether a design can hold several components (hybrid intent).
```

### `is_empty(design: Design) -> bool`

```text
Return whether the root component has no occurrences, bodies or sketches.
```

### `new_design(app: Application) -> Design`

```text
Open a new hybrid design document and return its design.
```
