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
Everything the dialog sets; lengths in millimetres.
```

## Functions

### `defaults() -> Settings`

```text
Return a fresh copy of the default settings.
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

### `from_mapping(raw: object) -> Settings`

```text
Build settings from untrusted data, keeping only well-typed known keys.

Values come from JSON files, design attributes or event payloads, so
unknown keys are dropped and every value is checked against the type of
its default. Range limits are enforced separately by
:func:`problems`, which keeps an out-of-range value visible in the
dialog instead of silently replacing it.

Args:
    raw: Parsed JSON; anything that is not an object yields the defaults.

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
