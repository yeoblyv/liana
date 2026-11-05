# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Extrudes, combines, rounds and countersunk holes with checked directions."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

import adsk.core
import adsk.fusion

from .api import (
    API_ERRORS,
    CUT,
    JOIN,
    MM,
    BRepBody,
    BRepEdge,
    Component,
    Feature,
    Point,
    bodies,
    collection,
    inside,
    is_inside,
    value,
)
from .context import BuildContext
from .sketch import ParamSketch, plane_y

Vec3 = tuple[float, float, float]
"""Model point in millimeters."""

Pt2 = tuple[float, float]
"""Pair of model coordinates in millimeters."""

_POSITIVE = adsk.fusion.ExtentDirections.PositiveExtentDirection
_NEGATIVE = adsk.fusion.ExtentDirections.NegativeExtentDirection


def ext_sym(comp: Component, sketch: ParamSketch, op: object, dist: str) -> Feature:
    """Extrude every profile of a sketch symmetrically, ``dist`` in total.

    Cuts use a bounded distance rather than "All", so they stay inside the
    part's own bodies.

    Args:
        comp: Component of the sketch.
        sketch: Sketch with the profiles.
        op: Feature operation (new body, join or cut).
        dist: Total distance expression.
    """
    extrudes = comp.features.extrudeFeatures
    ext_input = extrudes.createInput(sketch.profiles(), op)
    ext_input.setSymmetricExtent(value(dist), True)
    return extrudes.add(ext_input)


def ext_one(
    ctx: BuildContext,
    comp: Component,
    sketch: ParamSketch,
    op: object,
    dist: str,
    want_y: int,
    probe: Vec3,
    taper: str | None = None,
    wrong_probe: Vec3 | None = None,
) -> Feature:
    """Extrude one-sided toward +Y or -Y, checking the result with probe points.

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
    """
    extrudes = comp.features.extrudeFeatures
    first = _POSITIVE if sketch.normal().y * want_y > 0 else _NEGATIVE
    second = _NEGATIVE if first == _POSITIVE else _POSITIVE
    expect_inside = op != CUT
    last: Exception | None = None
    for direction in (first, second):
        feature = None
        try:
            ext_input = extrudes.createInput(sketch.profiles(), op)
            extent = adsk.fusion.DistanceExtentDefinition.create(value(dist))
            if taper:
                ext_input.setOneSideExtent(extent, direction, value(taper))
            else:
                ext_input.setOneSideExtent(extent, direction)
            feature = extrudes.add(ext_input)
        except API_ERRORS as e:
            last = e
        if feature is not None:
            good = inside(comp, probe) == expect_inside
            if good and wrong_probe is not None:
                good = inside(comp, wrong_probe)
            if good:
                return feature
            feature.deleteMe()
    raise RuntimeError("%s: extrude did not work in either direction (%s)" % (sketch.name, last))


def combine(comp: Component, probe: Vec3) -> Feature | None:
    """Join every body of a component into the one that contains ``probe``.

    Args:
        comp: Component with the bodies.
        probe: Point in mm inside the body that receives the others.

    Returns:
        The combine feature, or None when there is only one body.
    """
    bs = bodies(comp)
    if len(bs) < 2:
        return None
    target = next((i for i, b in enumerate(bs) if is_inside(b, probe)), 0)
    combines = comp.features.combineFeatures
    comb_input = combines.createInput(
        bs[target], collection([b for i, b in enumerate(bs) if i != target])
    )
    comb_input.operation = JOIN
    return combines.add(comb_input)


# ---------------------------------------------------------------- edge finders


def line_edges(bs: Sequence[BRepBody]) -> Iterator[tuple[BRepEdge, Point, Point]]:
    """Yield the straight edges of some bodies with their end points.

    Args:
        bs: Bodies to search.
    """
    line_type = adsk.core.Line3D.classType()
    for b in bs:
        for i in range(b.edges.count):
            e = b.edges.item(i)
            try:
                if e.geometry.objectType != line_type:
                    continue
                yield e, e.startVertex.geometry, e.endVertex.geometry
            except API_ERRORS:
                continue  # an edge without vertices (closed curve) is never a match


def z_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float = 0.02) -> list[BRepEdge]:
    """Return the straight edges parallel to Z that pass through given ``(x, y)``.

    Args:
        bs: Bodies to search.
        pts: ``(x, y)`` in mm.
        tol: Match tolerance in mm.
    """
    out = []
    for e, p, q in line_edges(bs):
        if abs(p.x - q.x) > 1e-5 or abs(p.y - q.y) > 1e-5:
            continue
        x, y = p.x / MM, p.y / MM
        if any(abs(x - a) < tol and abs(y - b) < tol for a, b in pts):
            out.append(e)
    return out


def y_edges(bs: Sequence[BRepBody], pts: Sequence[Pt2], tol: float = 0.02) -> list[BRepEdge]:
    """Return the straight edges parallel to Y that pass through given ``(x, z)``.

    Args:
        bs: Bodies to search.
        pts: ``(x, z)`` in mm.
        tol: Match tolerance in mm.
    """
    out = []
    for e, p, q in line_edges(bs):
        if abs(p.x - q.x) > 1e-5 or abs(p.z - q.z) > 1e-5:
            continue
        x, z = p.x / MM, p.z / MM
        if any(abs(x - a) < tol and abs(z - b) < tol for a, b in pts):
            out.append(e)
    return out


def face_edges_at_y(bs: Sequence[BRepBody], y: float, tol: float = 0.01) -> list[BRepEdge]:
    """Return every edge, straight or curved, that lies in the plane ``Y = y`` (mm).

    Args:
        bs: Bodies to search.
        y: Height of the plane in mm.
        tol: Match tolerance in mm.
    """
    out = []
    for b in bs:
        for i in range(b.edges.count):
            e = b.edges.item(i)
            try:
                p, q = e.startVertex.geometry, e.endVertex.geometry
            except API_ERRORS:
                continue  # closed curve without vertices
            if abs(p.y / MM - y) < tol and abs(q.y / MM - y) < tol:
                bb = e.boundingBox
                if abs(bb.minPoint.y / MM - y) < tol and abs(bb.maxPoint.y / MM - y) < tol:
                    out.append(e)
    return out


def end_face_edges(
    bs: Sequence[BRepBody], dz: float, x: float, half_width: float, y0: float, y1: float
) -> list[BRepEdge]:
    """Return the straight edges on the end faces ``Z = +-dz`` inside a window.

    Args:
        bs: Bodies to search.
        dz: Distance of the end faces from Z = 0, in mm.
        x: Center of the window along X, in mm.
        half_width: Half-width of the window along X, in mm.
        y0: Bottom of the window, in mm.
        y1: Top of the window, in mm.
    """
    out = []
    for e, p, q in line_edges(bs):
        if not (abs(abs(p.z / MM) - dz) < 1e-3 and abs(q.z - p.z) < 1e-6):
            continue
        if all(
            abs(g.x / MM - x) <= half_width and y0 - 0.01 <= g.y / MM <= y1 + 0.01 for g in (p, q)
        ):
            out.append(e)
    return out


def sym(x: float, y: float) -> list[Pt2]:
    """Return a point and its mirror image across X = 0.

    Args:
        x: X in mm.
        y: Second coordinate in mm.
    """
    return [(x, y), (-x, y)]


def corners(x: float, z: float) -> list[Pt2]:
    """Return the four corners of a rectangle centered on the origin.

    Args:
        x: Half-width in mm.
        z: Half-depth in mm.
    """
    return [(x, z), (-x, z), (x, -z), (-x, -z)]


# ---------------------------------------------------------------- finishing


def fillet(comp: Component, edges: Sequence[BRepEdge], radius: str) -> Feature:
    """Round edges with a constant radius.

    Args:
        comp: Component of the edges.
        edges: Edges to round.
        radius: Radius expression.

    Raises:
        RuntimeError: No edges were given.
    """
    if not edges:
        raise RuntimeError("edges not found")
    fillets = comp.features.filletFeatures
    fillet_input = fillets.createInput()
    oc = collection(edges)
    try:
        fillet_input.edgeSetInputs.addConstantRadiusEdgeSet(oc, value(radius), True)
    except AttributeError:  # Fusion before edge-set inputs
        fillet_input.addConstantRadiusEdgeSet(oc, value(radius), True)
    return fillets.add(fillet_input)


def chamfer(comp: Component, edges: Sequence[BRepEdge], dist: str) -> Feature:
    """Chamfer edges with an equal distance.

    Args:
        comp: Component of the edges.
        edges: Edges to chamfer.
        dist: Distance expression.

    Raises:
        RuntimeError: No edges were given.
    """
    if not edges:
        raise RuntimeError("edges not found")
    chamfers = comp.features.chamferFeatures
    oc = collection(edges)
    try:
        chamfer_input = chamfers.createInput2()
        chamfer_input.chamferEdgeSets.addEqualDistanceChamferEdgeSet(oc, value(dist), False)
    except AttributeError:  # Fusion before createInput2
        chamfer_input = chamfers.createInput(oc, False)
        chamfer_input.setToEqualDistance(value(dist))
    return chamfers.add(chamfer_input)


# ---------------------------------------------------------------- holes


def csk_holes(
    ctx: BuildContext,
    comp: Component,
    y_expr: str,
    pts: Sequence[tuple[str, str]],
    dia: str,
    csk: str,
    angle: str,
    depth: str,
    name: str,
    want_y: int = 1,
) -> Feature:
    """Drill countersunk holes from the plane ``Y = y_expr`` toward ``want_y``.

    The Hole feature is used when it works. Otherwise each hole is built as
    two extrude cuts: the bore and a tapered countersink.

    Args:
        ctx: Build context.
        comp: Component to drill.
        y_expr: Y of the surface the holes start from.
        pts: Hole centers as ``(x, z)`` expressions.
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
    """
    plane = plane_y(ctx, comp, y_expr)
    sketch = ParamSketch(ctx, comp, plane, name, 0, 2)
    sketch_pts = [sketch.point(u, v) for (u, v) in pts]
    y0 = ctx.ev(y_expr)
    u0, v0 = ctx.ev(pts[0][0]), ctx.ev(pts[0][1])
    probe = (u0, y0 + want_y * 0.3, v0)
    holes = comp.features.holeFeatures
    default_ok = (-sketch.normal().y) * want_y > 0
    for use_default in (default_ok, not default_ok):
        feature = None
        try:
            hole_input = holes.createCountersinkInput(value(dia), value(csk), value(angle))
            hole_input.setPositionBySketchPoints(collection(sketch_pts))
            hole_input.setDistanceExtent(value(depth))
            hole_input.isDefaultDirection = use_default
            feature = holes.add(hole_input)
        except API_ERRORS:
            feature = None
        if feature is not None:
            if not inside(comp, probe):
                try:
                    sketch.sk.isVisible = False
                except API_ERRORS:
                    pass  # a visible sketch is cosmetic
                return feature
            feature.deleteMe()
    ctx.log.soft.append("%s: Hole feature did not work, built as extrude cut" % name)
    bore = ParamSketch(ctx, comp, plane, name + " bore", 0, 2)
    for u, v in pts:
        bore.circle(u, v, dia)
    ext_one(ctx, comp, bore, CUT, depth, want_y, (u0, y0 + want_y * 0.5, v0))
    sink = ParamSketch(ctx, comp, plane, name + " csk", 0, 2)
    for u, v in pts:
        sink.circle(u, v, csk)
    height = "((%s) - (%s)) / 2" % (csk, dia)
    radius, t = ctx.ev(csk) / 2, ctx.ev(height) * 0.8
    sx = -1 if u0 > 0 else 1  # probe toward the part center
    rim = (u0 + sx * (radius - 0.3), y0 + want_y * 0.1, v0)
    wrong = (u0 + sx * (radius + 0.5 * t), y0 + want_y * t, v0)
    last: Exception | None = None
    for taper in ("-(%s) / 2" % angle, "(%s) / 2" % angle):
        try:
            return ext_one(
                ctx, comp, sink, CUT, height, want_y, rim, taper=taper, wrong_probe=wrong
            )
        except API_ERRORS as e:
            last = e
    raise RuntimeError("%s: countersink failed (%s)" % (name, last))
