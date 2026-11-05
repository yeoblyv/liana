# `Liana.cad.context`

State shared by the builders during one build.

## Classes

### `BuildContext`

```text
The design being built, the application and the log of the build.

Attributes:
    app: Fusion application.
    design: Design that receives the system.
    log: Problems recorded so far.
```

#### `BuildContext.ev(self, expr: str) -> float`

```text
Evaluate an expression against the design parameters, in mm.
```

#### `BuildContext.mag(self, expr: str) -> tuple[str, float]`

```text
Return an expression for the magnitude of ``expr`` and its value in mm.

Sketch dimensions are always positive, so a negative coordinate is
driven by its negation.
```

#### `BuildContext.soft(self, name: str, fn: Callable[[], _T]) -> _T | None`

```text
Run an optional finishing step; a failure is logged, not raised.

Fillets, chamfers and colours only refine a part, so the part stays
usable without them. Fusion can fail them in ways the API does not
document (edge topology, tangency), hence the broad catch.

Args:
    name: Label for the log, e.g. ``"Rail: end rounding"``.
    fn: The step.

Returns:
    What ``fn`` returned, or None if it failed.
```
