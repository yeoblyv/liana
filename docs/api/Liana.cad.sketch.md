# `Liana.cad.sketch`

Sketches whose every coordinate is driven by a parameter expression.

## Classes

### `ParamSketch`

```text
A sketch on a plane, drawn in model coordinates given as expressions.

Geometry is placed at the current parameter values and then dimensioned
with the same expressions, so the sketch follows any later parameter
change.

Attributes:
    ctx: Build context.
    comp: Component that owns the sketch.
    iu: Model axis (0 = X, 1 = Y, 2 = Z) of the first in-plane coordinate.
    iv: Model axis of the second in-plane coordinate.
    sk: The Fusion sketch.
```

#### `ParamSketch.__init__(self, ctx: BuildContext, comp: Component, plane: ConstructionPlane, name: str, iu: int, iv: int) -> None`

```text
Create the sketch.

Args:
    ctx: Build context.
    comp: Component that receives the sketch.
    plane: Sketch plane.
    name: Sketch name shown in the browser.
    iu: Model axis of the first in-plane coordinate.
    iv: Model axis of the second in-plane coordinate.
```

#### `ParamSketch.name(self) -> str`

```text
Sketch name.
```

#### `ParamSketch.dim_coord(self, pt: SketchPoint, axis: int, expr: str) -> None`

```text
Drive one model coordinate of a sketch point by an expression.

Fusion refuses a second origin dimension for a point that sits on the
same coordinate as a point already dimensioned (an over-constraint
error) without tying the two points together. Such a point would stay
behind when the parameter changes, so it is aligned to the first point
with an explicit constraint instead.

Args:
    pt: Sketch point.
    axis: Model axis of the coordinate.
    expr: Expression of the coordinate.
```

#### `ParamSketch.dim_between(self, a: SketchPoint, b: SketchPoint, axis: int, expr: str) -> None`

```text
Drive the distance between two points along a model axis.
```

#### `ParamSketch.rect(self, u0: str, v0: str, u1: str, v1: str) -> None`

```text
Draw an axis-aligned rectangle between two opposite corners.
```

#### `ParamSketch.right_triangle(self, uc: str, vc: str, ue: str, ve: str) -> None`

```text
Draw a right triangle with the corner at ``(uc, vc)``.

The legs end at ``(ue, vc)`` and ``(uc, ve)``.
```

#### `ParamSketch.circle(self, uc: str, vc: str, dia: str) -> SketchCircle`

```text
Draw a circle with a driven center and diameter.
```

#### `ParamSketch.polygon(self, pts: Outline) -> list[SketchLine]`

```text
Draw a closed polygon; every vertex is dimensioned.
```

#### `ParamSketch.point(self, u: str, v: str) -> SketchPoint`

```text
Add a driven sketch point.
```

#### `ParamSketch.profiles(self) -> Any`

```text
Return every profile of the sketch as an ``ObjectCollection``.
```

#### `ParamSketch.normal(self) -> Any`

```text
Return the sketch normal as a ``Vector3D``.
```

## Functions

### `plane_y(ctx: BuildContext, comp: Component, y_expr: str) -> ConstructionPlane`

```text
Return a plane parallel to XZ at ``Y = y_expr``.

The XZ plane itself is returned for a zero offset; any other plane is a
hidden offset construction plane driven by the expression.
```

### `plane_z(comp: Component, z_expr: str) -> ConstructionPlane`

```text
Return a hidden plane parallel to XY at ``Z = z_expr``.
```
