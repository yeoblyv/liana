# `Liana.cad.api`

Thin helpers over the Fusion API used by every builder.

The ``adsk`` package ships without type information, so its objects are typed
as :data:`typing.Any` through the aliases below; the aliases document which
Fusion class a value is expected to be.

## Constants

### `Application`

``adsk.core.Application``.

### `UserInterface`

``adsk.core.UserInterface``.

### `Design`

``adsk.fusion.Design``.

### `Component`

``adsk.fusion.Component``.

### `Occurrence`

``adsk.fusion.Occurrence``.

### `ConstructionPlane`

``adsk.fusion.ConstructionPlane``.

### `Sketch`

``adsk.fusion.Sketch``.

### `SketchPoint`

``adsk.fusion.SketchPoint``.

### `SketchLine`

``adsk.fusion.SketchLine``.

### `SketchCircle`

``adsk.fusion.SketchCircle``.

### `Feature`

Any timeline feature, e.g. ``adsk.fusion.ExtrudeFeature``.

### `BRepBody`

``adsk.fusion.BRepBody``.

### `BRepEdge`

``adsk.fusion.BRepEdge``.

### `Point`

``adsk.core.Point3D``.

### `MM`

One millimetre in Fusion internal units (centimetres).

### `API_ERRORS`

Exceptions that mean "Fusion refused this call".

Fusion raises RuntimeError for a refused operation, AttributeError when a
method or property is missing in an older release, and its bindings raise
NotImplementedError when no overload matches the arguments.

### `NEW_BODY`

Feature operation that creates a new body.

### `JOIN`

Feature operation that adds to the existing body.

### `CUT`

Feature operation that removes material.

## Functions

### `value(expr: str) -> Any`

```text
Return a ``ValueInput`` for an expression.
```

### `point(x: float, y: float, z: float) -> Point`

```text
Return a ``Point3D`` from millimetre coordinates.
```

### `collection(items: Iterable[Any]) -> Any`

```text
Return an ``ObjectCollection`` holding ``items`` in order.
```

### `bodies(comp: Component) -> list[BRepBody]`

```text
Return the bodies of a component.
```

### `is_inside(body: BRepBody, p: tuple[float, float, float]) -> bool`

```text
Return whether a point in millimetres lies inside a body.
```

### `inside(comp: Component, p: tuple[float, float, float]) -> bool`

```text
Return whether a point in millimetres lies inside any body of a component.
```

### `first_line(error: BaseException) -> str`

```text
Return the first line of an exception message, for logs.
```
