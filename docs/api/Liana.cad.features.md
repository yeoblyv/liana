# `Liana.cad.features`

Extrudes, combines, rounds and countersunk holes with checked directions.

## Constants

### `Vec3`

Model point in millimetres.

### `Pt2`

Pair of model coordinates in millimetres.

## Functions

### `ext_sym(comp: Component, sketch: ParamSketch, op: object, dist: str) -> Feature`

```text
Extrude every profile of a sketch symmetrically, ``dist`` in total.

Cuts use a bounded distance rather than "All", so they stay inside the
part's own bodies.
```

### `ext_one(ctx: BuildContext, comp: Component, sketch: ParamSketch, op: object, dist: str, want_y: int, probe: Vec3, taper: str | None=None, wrong_probe: Vec3 | None=None) -> Feature`

```text
Extrude one-sided toward +Y or -Y, checking the result with probe points.

Which extent direction points toward the wanted side depends on the plane
normal Fusion picked, so the likely direction is tried first and the
result is checked: after a cut the probe must be empty, after a join or
new body it must be filled. A wrong result is deleted and the other
direction is tried.

Args:
    ctx: Build context.
    comp: Component of the sketch.
    sketch: Sketch with the profiles.
    op: Feature operation.
    dist: Distance expression.
    want_y: ``1`` to extrude toward +Y, ``-1`` toward -Y.
    probe: Point that tells whether the extrude went the right way.
    taper: Optional taper angle expression.
    wrong_probe: Optional point that must stay filled; it catches a taper
        with the wrong sign.

Returns:
    The feature.

Raises:
    RuntimeError: Neither direction gave the expected result.
```

### `combine(comp: Component, probe: Vec3) -> Feature | None`

```text
Join every body of a component into the one that contains ``probe``.

Returns:
    The combine feature, or None when there is only one body.
```

### `line_edges(bs: Sequence[BRepBody]) -> Iterator[tuple[BRepEdge, Point, Point]]`

```text
Yield the straight edges of some bodies with their end points.
```

### `z_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float=0.02) -> list[BRepEdge]`

```text
Return the straight edges parallel to Z that pass through given ``(x, y)``.

Args:
    bs: Bodies to search.
    pts: ``(x, y)`` in mm.
    tol: Match tolerance in mm.
```

### `y_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float=0.02) -> list[BRepEdge]`

```text
Return the straight edges parallel to Y that pass through given ``(x, z)``.

Args:
    bs: Bodies to search.
    pts: ``(x, z)`` in mm.
    tol: Match tolerance in mm.
```

### `face_edges_at_y(bs: Sequence[BRepBody], y: float, tol: float=0.01) -> list[BRepEdge]`

```text
Return every edge, straight or curved, that lies in the plane ``Y = y`` (mm).
```

### `end_face_edges(bs: Sequence[BRepBody], dz: float, x: float, half_width: float, y0: float, y1: float) -> list[BRepEdge]`

```text
Return the straight edges on the end faces ``Z = +-dz`` inside a window.

Args:
    bs: Bodies to search.
    dz: Distance of the end faces from Z = 0, in mm.
    x: Centre of the window along X, in mm.
    half_width: Half-width of the window along X, in mm.
    y0: Bottom of the window, in mm.
    y1: Top of the window, in mm.
```

### `sym(x: float, y: float) -> list[Pt2]`

```text
Return a point and its mirror image across X = 0.
```

### `corners(x: float, z: float) -> list[Pt2]`

```text
Return the four corners of a rectangle centred on the origin.
```

### `fillet(comp: Component, edges: Sequence[BRepEdge], radius: str) -> Feature`

```text
Round edges with a constant radius.

Raises:
    RuntimeError: No edges were given.
```

### `chamfer(comp: Component, edges: Sequence[BRepEdge], dist: str) -> Feature`

```text
Chamfer edges with an equal distance.

Raises:
    RuntimeError: No edges were given.
```

### `csk_holes(ctx: BuildContext, comp: Component, y_expr: str, pts: Sequence[tuple[str, str]], dia: str, csk: str, angle: str, depth: str, name: str, want_y: int=1) -> Feature`

```text
Drill countersunk holes from the plane ``Y = y_expr`` toward ``want_y``.

The Hole feature is used when it works. Otherwise each hole is built as
two extrude cuts: the bore and a tapered countersink.

Args:
    ctx: Build context.
    comp: Component to drill.
    y_expr: Y of the surface the holes start from.
    pts: Hole centres as ``(x, z)`` expressions.
    dia: Bore diameter.
    csk: Countersink diameter at the surface.
    angle: Countersink angle.
    depth: Bore depth.
    name: Sketch name.
    want_y: ``1`` to drill toward +Y, ``-1`` toward -Y.

Returns:
    The last feature created.

Raises:
    RuntimeError: The countersink could not be cut in either taper sign.
```
