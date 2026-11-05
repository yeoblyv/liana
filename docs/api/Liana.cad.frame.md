# `Liana.cad.frame`

X-frame: a square frame that carries holders on up to four sides.

The frame is modelled around ``(0, 0, FRAME_Z)`` in its own component with
the occurrence at identity, so no frame feature can reach the holder or the
tie mount, at build time or on any later recompute.

## Functions

### `build_frame(ctx: BuildContext, comp: Component, s: Settings) -> None`

```text
Model the frame in ``comp``.

Args:
    ctx: Build context; the parameters already exist.
    comp: Empty component that receives the frame.
    s: Settings.
```
