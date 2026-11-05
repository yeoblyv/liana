# `Liana.cad.tie_mount`

Tie mount: a small pad with two zip-tie tunnels and one screw.

The tie mount is modelled around ``(0, 0, TIE_Z)`` in its own component with
the occurrence at identity, so its tunnels can never cut the holder or the
frame.

## Functions

### `build_tie(ctx: BuildContext, comp: Component, s: Settings) -> None`

```text
Model the tie mount in ``comp``.

Args:
    ctx: Build context; the parameters already exist.
    comp: Empty component that receives the tie mount.
    s: Settings (the sizes come from the parameters).
```
