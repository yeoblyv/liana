# `Liana.core.expr`

Builders for Fusion parameter expressions and the outlines drawn with them.

Every sketch coordinate is an expression of User Parameters rather than a
number, so the design follows a parameter change without running Liana again.

## Constants

### `Outline`

Closed polygon as ``(u, v)`` expression pairs.

## Functions

### `neg(e: str) -> str`

```text
Return the negated expression.
```

### `sgn(sign: int, e: str) -> str`

```text
Return ``e`` for a positive sign and its negation otherwise.
```

### `diff(a: str, b: str) -> str`

```text
Return the expression ``a - b``.
```

### `pitch_expr(t: float) -> str`

```text
Return ``t`` cradle pitches from the center as an expression.

Args:
    t: Offset in pitches; may be fractional.

Returns:
    ``"0 mm"`` for zero, otherwise ``"<t> * NOTCH_PITCH"``.
```

### `nut_seat(sx: int, side: bool) -> Outline`

```text
Return the outline of one M3 nut seat at ``x = sx * M3_X``.

The seat is an entry slot with a flared mouth that ends in a half hexagon
centered on the screw, so the nut slides in by hand, stops on the screw
axis and cannot turn.

Args:
    sx: ``1`` for the seat at +X, ``-1`` for the one at -X.
    side: The slot opens to the -Z face (low end blocks) when true,
        otherwise to the end face at +-X.

Returns:
    Vertices with ``u`` along X and ``v`` along Z.
```

### `member_coords(side: Side, width: str, half_len: str) -> tuple[str, str, str, str]`

```text
Return the rectangle of one frame beam as ``(u0, v0, u1, v1)``.

Args:
    side: Frame side; S and N beams run along X, E and W along Z.
    width: Beam width expression.
    half_len: Half of the beam length.

Returns:
    Opposite corners with ``u`` along X and ``v`` along Z, relative to
    the frame center.
```

### `holder_hole_exprs(side_screws: bool, ev: Callable[[str], float]) -> list[str]`

```text
Return the holder screw positions along the holder axis.

The frame gets a hole under every holder screw for both orientations of
the holder, so the side screws are mirrored; mirrored positions that
coincide with an existing hole are dropped.

Args:
    side_screws: Whether the holder has side screws next to the pin.
    ev: Evaluates an expression to millimeters.

Returns:
    X expressions of the holes.
```
