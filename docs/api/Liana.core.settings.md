# `Liana.core.settings`

Dialog settings: defaults, limits, validation and loading from untrusted JSON.

## Constants

### `Mount`

Which frame sides show a holder in the design preview.

### `Side`

Frame side: south, east, north, west.

### `SETTINGS_VERSION`

Version written with saved settings; older files are migrated on load.

### `NUT_H`

M3 nut slot height in mm: a 2.4 mm nut plus room for a sagging bridge.

### `SIDES`

Frame sides in build order.

### `MOUNTS`

Mount options: key, dialog label, frame sides that get a holder.

### `MOUNT_SIDES`

Frame sides for each mount option.

### `DEFAULTS`

Settings of a fresh install.

### `LIMITS`

Allowed range (inclusive) of every numeric setting.

### `MAX_CRADLES`

Largest cradle count the dialog offers.

## Classes

### `Settings(TypedDict)`

```text
Everything the dialog sets; lengths in millimeters.
```

## Functions

### `defaults() -> Settings`

```text
Return a fresh copy of the default settings.
```

### `finite_number(value: object) -> float | None`

```text
Return ``value`` as a finite float, or None.

Booleans, strings, NaN, infinities and integers too large for a float
are rejected, so untrusted JSON cannot smuggle them into the arithmetic.
```

### `migrate(raw: dict[str, Any]) -> dict[str, Any]`

```text
Upgrade settings saved by an older version, in place.

Version 1 used a 5.8 mm nut slot that is too tight for printed parts; a
stored value equal to that old default is raised to the current one.

Args:
    raw: Settings as read from JSON.

Returns:
    The same dictionary, tagged with :data:`SETTINGS_VERSION`.
```

### `from_mapping(raw: object, within_limits: bool=False) -> Settings`

```text
Build settings from data of unknown quality, keeping well-typed known keys.

Unknown keys are dropped and every value is checked against the type of
its default; numbers must be finite.

Values read back from files, designs or events pass ``within_limits``,
so an out-of-range value (a cradle count of a billion, say) is replaced
by the default before any arithmetic runs on it. The dialog leaves it
off: there an out-of-range value must stay visible and be reported by
:func:`problems`.

Args:
    raw: Parsed JSON; anything that is not an object yields the defaults.
    within_limits: Also drop numbers outside :data:`LIMITS`.

Returns:
    Complete settings.
```

### `problems(s: Settings, fits_bed: bool) -> list[str]`

```text
List what is wrong with the settings, in dialog wording.

Args:
    s: Settings to check.
    fits_bed: Whether every part fits on the printer bed.

Returns:
    Problems; empty when the settings can be built.
```
