# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Thin helpers over the Fusion API used by every builder.

The ``adsk`` package ships without type information, so its objects are typed
as :data:`typing.Any` through the aliases below; the aliases document which
Fusion class a value is expected to be.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import adsk.core
import adsk.fusion

Application = Any
"""``adsk.core.Application``."""

UserInterface = Any
"""``adsk.core.UserInterface``."""

Design = Any
"""``adsk.fusion.Design``."""

Component = Any
"""``adsk.fusion.Component``."""

Occurrence = Any
"""``adsk.fusion.Occurrence``."""

ConstructionPlane = Any
"""``adsk.fusion.ConstructionPlane``."""

Sketch = Any
"""``adsk.fusion.Sketch``."""

SketchPoint = Any
"""``adsk.fusion.SketchPoint``."""

SketchLine = Any
"""``adsk.fusion.SketchLine``."""

SketchCircle = Any
"""``adsk.fusion.SketchCircle``."""

Feature = Any
"""Any timeline feature, e.g. ``adsk.fusion.ExtrudeFeature``."""

BRepBody = Any
"""``adsk.fusion.BRepBody``."""

BRepEdge = Any
"""``adsk.fusion.BRepEdge``."""

Point = Any
"""``adsk.core.Point3D``."""

MM = 0.1
"""One millimeter in Fusion internal units (centimetres)."""

API_ERRORS: tuple[type[Exception], ...] = (
    RuntimeError,
    AttributeError,
    NotImplementedError,
    TypeError,
    ValueError,
)
"""Exceptions that mean "Fusion refused this call".

Fusion raises RuntimeError for a refused operation and AttributeError when a
method or property is missing in an older release. Its bindings raise
NotImplementedError when no overload matches the arguments, and TypeError or
ValueError when an argument cannot be converted.
"""

NEW_BODY = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
"""Feature operation that creates a new body."""

JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation
"""Feature operation that adds to the existing body."""

CUT = adsk.fusion.FeatureOperations.CutFeatureOperation
"""Feature operation that removes material."""


def value(expr: str) -> Any:
    """Return a ``ValueInput`` for an expression."""
    return adsk.core.ValueInput.createByString(expr)


def point(x: float, y: float, z: float) -> Point:
    """Return a ``Point3D`` from millimeter coordinates."""
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def collection(items: Iterable[Any]) -> Any:
    """Return an ``ObjectCollection`` holding ``items`` in order."""
    oc = adsk.core.ObjectCollection.create()
    for item in items:
        oc.add(item)
    return oc


def bodies(comp: Component) -> list[BRepBody]:
    """Return the bodies of a component."""
    return [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]


def is_inside(body: BRepBody, p: tuple[float, float, float]) -> bool:
    """Return whether a point in millimeters lies inside a body."""
    return bool(
        body.pointContainment(point(*p))
        == adsk.fusion.PointContainment.PointInsidePointContainment
    )


def inside(comp: Component, p: tuple[float, float, float]) -> bool:
    """Return whether a point in millimeters lies inside any body of a component."""
    return any(is_inside(b, p) for b in bodies(comp))


def first_line(error: BaseException) -> str:
    """Return the first line of an exception message, for logs."""
    return str(error).strip().split("\n")[0]
