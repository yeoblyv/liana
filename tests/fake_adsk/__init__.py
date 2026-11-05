# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""In-memory stand-in for the parts of the Autodesk Fusion API that Liana uses.

The fake keeps just enough geometry to check that every sketch dimension Liana
sets agrees with the geometry it drew, and it records every call that changes
the design in the trace of the current :class:`World`. Tests compare that trace
with golden files, so a refactor that changes what Liana asks Fusion to do is
caught without running Fusion.

Fusion exposes one application object per process; the fake mirrors that with
one :class:`World` that :func:`reset` replaces between tests.
"""

from __future__ import annotations

from tests.fake_adsk.world import World, reset, world

__all__ = ["World", "doEvents", "reset", "world"]


def doEvents() -> None:
    """Let Fusion process pending UI events (no-op in the fake)."""
    world().trace_event("doEvents")
