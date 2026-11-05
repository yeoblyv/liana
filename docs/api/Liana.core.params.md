# `Liana.core.params`

User Parameters that drive every sketch dimension of a Liana system.

## Constants

### `ANGLE_PARAMS`

Parameters measured in degrees; all others are lengths in mm.

## Classes

### `ParamSpec(NamedTuple)`

```text
One User Parameter.

Attributes:
    name: Parameter name.
    expression: Fusion expression, with units.
    comment: Comment shown in Change Parameters.
```

## Functions

### `fmt(value: float) -> str`

```text
Format a length in mm as a Fusion expression, e.g. ``"4.2 mm"``.
```

### `make_params(s: Settings) -> list[ParamSpec]`

```text
Return the User Parameters for the settings, in dependency order.

Values the dialog sets become plain lengths; everything else is an
expression of other parameters, so a size changed later in Change
Parameters propagates through the whole design.

Args:
    s: Settings.

Returns:
    Parameters; each one refers only to parameters listed before it.
```
