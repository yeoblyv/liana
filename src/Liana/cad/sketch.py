# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Sketches whose every coordinate is driven by a parameter expression."""

from __future__ import annotations

from typing import Any

import adsk.core
import adsk.fusion

from ..core.expr import Outline, diff, neg
from .api import (
    API_ERRORS,
    MM,
    Component,
    ConstructionPlane,
    Point,
    SketchCircle,
    SketchLine,
    SketchPoint,
    collection,
    first_line,
    point,
    value,
)
from .context import BuildContext

_HORIZONTAL = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
_VERTICAL = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation

_TEXT_OFFSET = 0.4
"""Distance of a dimension text from its point, in cm."""


class ParamSketch:
    """A sketch on a plane, drawn in model coordinates given as expressions.

    Geometry is placed at the current parameter values and then dimensioned
    with the same expressions, so the sketch follows any later parameter
    change.

    Attributes:
        ctx: Build context.
        comp: Component that owns the sketch.
        iu: Model axis (0 = X, 1 = Y, 2 = Z) of the first in-plane coordinate.
        iv: Model axis of the second in-plane coordinate.
        sk: The Fusion sketch.
    """

    def __init__(
        self,
        ctx: BuildContext,
        comp: Component,
        plane: ConstructionPlane,
        name: str,
        iu: int,
        iv: int,
    ) -> None:
        """Create the sketch.

        Args:
            ctx: Build context.
            comp: Component that receives the sketch.
            plane: Sketch plane.
            name: Sketch name shown in the browser.
            iu: Model axis of the first in-plane coordinate.
            iv: Model axis of the second in-plane coordinate.
        """
        self.ctx = ctx
        self.comp = comp
        self.iu, self.iv = iu, iv
        self.sk = comp.sketches.add(plane)
        self.sk.name = name
        self._origin = self.sk.project(comp.originConstructionPoint).item(0)
        self._axes: dict[int, SketchLine] = {}
        self._lines = self.sk.sketchCurves.sketchLines
        self._constraints = self.sk.geometricConstraints
        self._dims = self.sk.sketchDimensions
        # (model axis, expression) -> first point dimensioned with that expression
        self._refs: dict[tuple[int, str], SketchPoint] = {}

    @property
    def name(self) -> str:
        """Sketch name."""
        return str(self.sk.name)

    # ------------------------------------------------------------ geometry helpers

    def _axis_line(self, axis: int) -> SketchLine:
        """Return the projected model axis, projected once per sketch."""
        if axis not in self._axes:
            model_axis = (
                self.comp.xConstructionAxis,
                self.comp.yConstructionAxis,
                self.comp.zConstructionAxis,
            )[axis]
            line = self.sk.project(model_axis).item(0)
            try:
                line.isConstruction = True
            except API_ERRORS:
                pass  # a solid projected axis still works as a reference
            self._axes[axis] = line
        return self._axes[axis]

    def _sketch_point(self, u: str, v: str) -> Point:
        """Return the sketch-space point for model coordinates ``(u, v)``."""
        xyz = [0.0, 0.0, 0.0]
        xyz[self.iu] = self.ctx.ev(u)
        xyz[self.iv] = self.ctx.ev(v)
        p = self.sk.modelToSketchSpace(point(xyz[0], xyz[1], xyz[2]))
        return adsk.core.Point3D.create(p.x, p.y, 0)

    def _orientation(self, axis: int) -> Any:
        """Return the sketch dimension orientation that measures a model axis."""
        o = self.sk.modelToSketchSpace(adsk.core.Point3D.create(0, 0, 0))
        u = [0.0, 0.0, 0.0]
        u[axis] = 1.0
        q = self.sk.modelToSketchSpace(adsk.core.Point3D.create(u[0], u[1], u[2]))
        if abs(q.x - o.x) > abs(q.y - o.y):
            return _HORIZONTAL
        return _VERTICAL

    @staticmethod
    def _text_between(a: SketchPoint, b: SketchPoint) -> Point:
        """Return a text position next to the middle of two points."""
        g1, g2 = a.geometry, b.geometry
        return adsk.core.Point3D.create((g1.x + g2.x) / 2 + 0.15, (g1.y + g2.y) / 2 + 0.15, 0)

    def _text_beside(self, pt: SketchPoint, axis: int) -> Point:
        """Return a text position offset across the measured direction."""
        g = pt.geometry
        if self._orientation(axis) == _HORIZONTAL:
            dy = _TEXT_OFFSET if g.y >= 0 else -_TEXT_OFFSET
            return adsk.core.Point3D.create(g.x / 2, g.y + dy, 0)
        dx = _TEXT_OFFSET if g.x >= 0 else -_TEXT_OFFSET
        return adsk.core.Point3D.create(g.x + dx, g.y / 2, 0)

    def _log_dim(self, what: str, expr: str, err: object) -> None:
        self.ctx.log.dims.append(
            "%s | %s = %s | %s" % (self.name, what, expr, str(err).strip().split("\n")[0])
        )

    def _align(self, ref: SketchPoint, pt: SketchPoint, axis: int) -> bool:
        """Constrain ``pt`` to share the coordinate of ``ref`` along a model axis.

        Returns:
            Whether a constraint was added.
        """
        along_sketch_x = self._orientation(axis) == _HORIZONTAL
        try:
            if along_sketch_x:
                self._constraints.addVerticalPoints(ref, pt)
            else:
                self._constraints.addHorizontalPoints(ref, pt)
            return True
        except API_ERRORS:
            pass  # older Fusion: no point-to-point constraints
        try:
            # older Fusion: a construction line kept vertical or horizontal ties
            # the points instead; coincident points cannot carry a line
            g0, g1 = ref.geometry, pt.geometry
            if abs(g0.x - g1.x) + abs(g0.y - g1.y) < 1e-6:
                return False
            line = self._lines.addByTwoPoints(ref, pt)
            line.isConstruction = True
            if along_sketch_x:
                self._constraints.addVertical(line)
            else:
                self._constraints.addHorizontal(line)
            return True
        except API_ERRORS:
            return False

    # ------------------------------------------------------------ dimensions

    def dim_coord(self, pt: SketchPoint, axis: int, expr: str) -> None:
        """Drive one model coordinate of a sketch point by an expression.

        Fusion refuses a second origin dimension for a point that sits on the
        same coordinate as a point already dimensioned (an over-constraint
        error) without tying the two points together. Such a point would stay
        behind when the parameter changes, so it is aligned to the first point
        with an explicit constraint instead.

        Args:
            pt: Sketch point.
            axis: Model axis of the coordinate.
            expr: Expression of the coordinate.
        """
        magnitude, v = self.ctx.mag(expr)
        other = self.iv if axis == self.iu else self.iu
        if v < 1e-4:  # zero coordinate: the point lies on the other in-plane axis
            try:
                self._constraints.addCoincident(pt, self._axis_line(other))
            except API_ERRORS as e:
                self._log_dim("coincident to axis", expr, e)
            return
        key = (axis, expr.replace(" ", ""))
        ref = self._refs.get(key)
        if ref is not None and self._align(ref, pt, axis):
            self.ctx.log.aligned.append("%s | axis %d = %s" % (self.name, axis, expr))
            return
        errs = []
        # the origin dimension reads naturally in the sketch; the offset from
        # the projected axis is the fallback when Fusion refuses it
        try:
            d = self._dims.addDistanceDimension(
                self._origin, pt, self._orientation(axis), self._text_beside(pt, axis)
            )
            d.parameter.expression = magnitude
            self._refs.setdefault(key, pt)
            return
        except API_ERRORS as e:
            errs.append("origin: %s" % first_line(e))
        try:
            d = self._dims.addOffsetDimension(
                self._axis_line(other), pt, self._text_beside(pt, axis)
            )
            d.parameter.expression = magnitude
            self._refs.setdefault(key, pt)
            return
        except API_ERRORS as e:
            errs.append("axis line: %s" % first_line(e))
        self._log_dim("coord axis %d" % axis, expr, " / ".join(errs))

    def dim_between(self, a: SketchPoint, b: SketchPoint, axis: int, expr: str) -> None:
        """Drive the distance between two points along a model axis."""
        magnitude, _ = self.ctx.mag(expr)
        try:
            d = self._dims.addDistanceDimension(
                a, b, self._orientation(axis), self._text_between(a, b)
            )
            d.parameter.expression = magnitude
        except API_ERRORS as e:
            self._log_dim("between axis %d" % axis, expr, e)

    def _horizontal_or_vertical(self, line: SketchLine) -> None:
        g0, g1 = line.startSketchPoint.geometry, line.endSketchPoint.geometry
        if abs(g1.x - g0.x) >= abs(g1.y - g0.y):
            self._constraints.addHorizontal(line)
        else:
            self._constraints.addVertical(line)

    # ------------------------------------------------------------ shapes

    def rect(self, u0: str, v0: str, u1: str, v1: str) -> None:
        """Draw an axis-aligned rectangle between two opposite corners."""
        a, b, c, d = (
            self._sketch_point(u0, v0),
            self._sketch_point(u1, v0),
            self._sketch_point(u1, v1),
            self._sketch_point(u0, v1),
        )
        l1 = self._lines.addByTwoPoints(a, b)
        l2 = self._lines.addByTwoPoints(l1.endSketchPoint, c)
        l3 = self._lines.addByTwoPoints(l2.endSketchPoint, d)
        l4 = self._lines.addByTwoPoints(l3.endSketchPoint, l1.startSketchPoint)
        for line in (l1, l2, l3, l4):
            self._horizontal_or_vertical(line)
        corner = l1.startSketchPoint
        self.dim_coord(corner, self.iu, u0)
        self.dim_coord(corner, self.iv, v0)
        self.dim_between(corner, l1.endSketchPoint, self.iu, diff(u1, u0))
        self.dim_between(corner, l3.endSketchPoint, self.iv, diff(v1, v0))

    def right_triangle(self, uc: str, vc: str, ue: str, ve: str) -> None:
        """Draw a right triangle with the corner at ``(uc, vc)``.

        The legs end at ``(ue, vc)`` and ``(uc, ve)``.
        """
        a, b, c = (
            self._sketch_point(uc, vc),
            self._sketch_point(ue, vc),
            self._sketch_point(uc, ve),
        )
        l1 = self._lines.addByTwoPoints(a, b)
        l2 = self._lines.addByTwoPoints(l1.endSketchPoint, c)
        l3 = self._lines.addByTwoPoints(l2.endSketchPoint, l1.startSketchPoint)
        self._horizontal_or_vertical(l1)
        self._horizontal_or_vertical(l3)
        corner = l1.startSketchPoint
        self.dim_coord(corner, self.iu, uc)
        self.dim_coord(corner, self.iv, vc)
        self.dim_between(corner, l1.endSketchPoint, self.iu, diff(ue, uc))
        self.dim_between(corner, l2.endSketchPoint, self.iv, diff(ve, vc))

    def circle(self, uc: str, vc: str, dia: str) -> SketchCircle:
        """Draw a circle with a driven center and diameter."""
        c = self.sk.sketchCurves.sketchCircles.addByCenterRadius(
            self._sketch_point(uc, vc), self.ctx.ev(dia) / 2 * MM
        )
        g = c.centerSketchPoint.geometry
        try:
            d = self._dims.addDiameterDimension(
                c, adsk.core.Point3D.create(g.x + 0.3, g.y + 0.3, 0)
            )
            d.parameter.expression = dia
        except API_ERRORS as e:
            self._log_dim("diameter", dia, e)
        self.dim_coord(c.centerSketchPoint, self.iu, uc)
        self.dim_coord(c.centerSketchPoint, self.iv, vc)
        return c

    def polygon(self, pts: Outline) -> list[SketchLine]:
        """Draw a closed polygon; every vertex is dimensioned."""
        sketch_pts = [self._sketch_point(u, v) for u, v in pts]
        lines: list[SketchLine] = []
        for i in range(len(sketch_pts)):
            a = lines[-1].endSketchPoint if lines else sketch_pts[0]
            b = lines[0].startSketchPoint if i == len(sketch_pts) - 1 else sketch_pts[i + 1]
            lines.append(self._lines.addByTwoPoints(a, b))
        for (u, v), line in zip(pts, lines):
            self.dim_coord(line.startSketchPoint, self.iu, u)
            self.dim_coord(line.startSketchPoint, self.iv, v)
        return lines

    def point(self, u: str, v: str) -> SketchPoint:
        """Add a driven sketch point."""
        p = self.sk.sketchPoints.add(self._sketch_point(u, v))
        self.dim_coord(p, self.iu, u)
        self.dim_coord(p, self.iv, v)
        return p

    # ------------------------------------------------------------ queries

    def profiles(self) -> Any:
        """Return every profile of the sketch as an ``ObjectCollection``."""
        return collection([self.sk.profiles.item(i) for i in range(self.sk.profiles.count)])

    def normal(self) -> Any:
        """Return the sketch normal as a ``Vector3D``."""
        return self.sk.xDirection.crossProduct(self.sk.yDirection)


def _hide(plane: ConstructionPlane) -> None:
    try:
        plane.isLightBulbOn = False
    except API_ERRORS:
        pass  # a visible helper plane is cosmetic


def plane_y(ctx: BuildContext, comp: Component, y_expr: str) -> ConstructionPlane:
    """Return a plane parallel to XZ at ``Y = y_expr``.

    The XZ plane itself is returned for a zero offset; any other plane is a
    hidden offset construction plane driven by the expression.
    """
    base = comp.xZConstructionPlane
    if abs(ctx.ev(y_expr)) < 1e-6:
        return base
    n = base.geometry.normal
    offset = y_expr if n.y > 0 else neg(y_expr)
    plane_input = comp.constructionPlanes.createInput()
    plane_input.setByOffset(base, value(offset))
    plane = comp.constructionPlanes.add(plane_input)
    _hide(plane)
    return plane


def plane_z(comp: Component, z_expr: str) -> ConstructionPlane:
    """Return a hidden plane parallel to XY at ``Z = z_expr``."""
    base = comp.xYConstructionPlane
    n = base.geometry.normal
    plane_input = comp.constructionPlanes.createInput()
    plane_input.setByOffset(base, value(z_expr if n.z > 0 else neg(z_expr)))
    plane = comp.constructionPlanes.add(plane_input)
    _hide(plane)
    return plane
