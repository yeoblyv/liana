# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Fake ``adsk.fusion``: designs, components, sketches and features.

Geometry is kept only as far as needed to verify sketch dimensions: every
dimension checks that its expression equals the distance it measures in the
drawn geometry and reports a mismatch in ``world().errors``.
"""

from __future__ import annotations

from typing import Any

from tests.fake_adsk import core
from tests.fake_adsk.world import mm, world

CM_PER_MM = 0.1


class FeatureOperations:
    """Feature operation enumeration."""

    NewBodyFeatureOperation = "NewBody"
    JoinFeatureOperation = "Join"
    CutFeatureOperation = "Cut"


class ExtentDirections:
    """Extent direction enumeration."""

    PositiveExtentDirection = "Positive"
    NegativeExtentDirection = "Negative"


class DimensionOrientations:
    """Dimension orientation enumeration."""

    HorizontalDimensionOrientation = "Horizontal"
    VerticalDimensionOrientation = "Vertical"
    AlignedDimensionOrientation = "Aligned"


class PointContainment:
    """Point containment enumeration."""

    PointInsidePointContainment = "IN"
    PointOutsidePointContainment = "OUT"


class DesignTypes:
    """Design type enumeration."""

    ParametricDesignType = "Parametric"


class DesignIntentTypes:
    """Design intent enumeration."""

    HybridDesignIntentType = "HY"
    PartDesignIntentType = "PART"
    AssemblyDesignIntentType = "ASM"


class DistanceExtentDefinition:
    """Distance extent of a one-sided extrude."""

    def __init__(self, distance: core.ValueInput) -> None:
        self.distance = distance

    @staticmethod
    def create(distance: core.ValueInput) -> DistanceExtentDefinition:
        """Create the extent."""
        return DistanceExtentDefinition(distance)


# ---------------------------------------------------------------- planes and axes
class Plane:
    """Plane with an origin and two in-plane unit directions (internal units)."""

    def __init__(self, origin: core.Point3D, xdir: core.Vector3D, ydir: core.Vector3D) -> None:
        self.origin = origin
        self.xdir = xdir
        self.ydir = ydir
        self.normal = xdir.crossProduct(ydir)

    def key(self) -> tuple[Any, ...]:
        """Rounded origin and normal for traces."""
        return (self.origin.key(), (self.normal.x, self.normal.y, self.normal.z))


class ConstructionPlane:
    """Construction plane."""

    def __init__(self, plane: Plane) -> None:
        self.geometry = plane
        self._light = True

    @property
    def isLightBulbOn(self) -> bool:
        """Visibility of the plane."""
        return self._light

    @isLightBulbOn.setter
    def isLightBulbOn(self, value: bool) -> None:
        self._light = value
        world().trace_event("constructionPlane.visible", value)


class ConstructionPlaneInput:
    """Definition of an offset construction plane."""

    def __init__(self) -> None:
        self.base: ConstructionPlane | None = None
        self.offset: core.ValueInput | None = None

    def setByOffset(self, base: ConstructionPlane, offset: core.ValueInput) -> bool:
        """Offset ``base`` along its normal."""
        self.base, self.offset = base, offset
        return True


class ConstructionPlanes:
    """Construction planes of a component."""

    def createInput(self) -> ConstructionPlaneInput:
        """Create an input."""
        return ConstructionPlaneInput()

    def add(self, definition: ConstructionPlaneInput) -> ConstructionPlane:
        """Create the plane."""
        assert definition.base is not None and definition.offset is not None
        base = definition.base.geometry
        expr = definition.offset.stringValue
        off = world().evaluate(expr) * CM_PER_MM
        n = base.normal
        origin = core.Point3D(
            base.origin.x + n.x * off, base.origin.y + n.y * off, base.origin.z + n.z * off
        )
        world().trace_event("constructionPlane.offset", base.key(), expr)
        return ConstructionPlane(Plane(origin, base.xdir, base.ydir))


class OriginPoint:
    """Origin construction point."""


class ConstructionAxis:
    """Construction axis through the origin."""

    def __init__(self, direction: tuple[float, float, float]) -> None:
        self.direction = direction


# ---------------------------------------------------------------- sketches
class SketchPoint:
    """Sketch point in sketch space (internal units)."""

    def __init__(self, sketch: Sketch, geometry: core.Point3D, reference: bool = False) -> None:
        self.sketch = sketch
        self.geometry = geometry
        self.reference = reference


class SketchLine:
    """Sketch line between two sketch points."""

    def __init__(
        self, sketch: Sketch, start: SketchPoint, end: SketchPoint, projected: bool = False
    ) -> None:
        self.sketch = sketch
        self.startSketchPoint = start
        self.endSketchPoint = end
        self.projected = projected
        self._construction = projected

    @property
    def isConstruction(self) -> bool:
        """Construction (non-profile) line flag."""
        return self._construction

    @isConstruction.setter
    def isConstruction(self, value: bool) -> None:
        self._construction = value
        if not self.projected:
            world().trace_event("line.construction", value)


class SketchCircle:
    """Sketch circle."""

    def __init__(self, center: SketchPoint, radius: float) -> None:
        self.centerSketchPoint = center
        self.radius = radius


class _Parameter:
    def __init__(self, dimension: SketchDimension) -> None:
        self._dimension = dimension

    @property
    def expression(self) -> str:
        return self._dimension.expression

    @expression.setter
    def expression(self, expr: str) -> None:
        self._dimension.set_expression(expr)


class SketchDimension:
    """Driving dimension; checks its expression against the geometry."""

    def __init__(self, kind: str, a: Any, b: Any, orientation: str | None) -> None:
        self.kind = kind
        self.a = a
        self.b = b
        self.orientation = orientation
        self.expression = ""
        self.parameter = _Parameter(self)

    def measured(self) -> float:
        """Current measured value in millimetres."""
        if self.kind == "diameter":
            return float(2.0 * self.a.radius / CM_PER_MM)
        if self.kind == "offset":
            p, a, b = (
                self.a.geometry,
                self.b.startSketchPoint.geometry,
                self.b.endSketchPoint.geometry,
            )
            dx, dy = b.x - a.x, b.y - a.y
            length = (dx * dx + dy * dy) ** 0.5
            return float(abs(dx * (p.y - a.y) - dy * (p.x - a.x)) / length / CM_PER_MM)
        ga, gb = self.a.geometry, self.b.geometry
        if self.orientation == DimensionOrientations.HorizontalDimensionOrientation:
            return float(abs(gb.x - ga.x) / CM_PER_MM)
        return float(abs(gb.y - ga.y) / CM_PER_MM)

    def set_expression(self, expr: str) -> None:
        """Apply an expression and verify it against the geometry."""
        self.expression = expr
        w = world()
        value = w.evaluate(expr)
        w.trace_event("dimension", self.kind, self.orientation, expr)
        actual = self.measured()
        if value <= 0 or abs(value - actual) > 1e-6:
            w.errors.append(
                "dimension %r = %.6f but geometry measures %.6f (%s)"
                % (expr, value, actual, self.kind)
            )


class SketchLines:
    """Lines of a sketch."""

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch

    def addByTwoPoints(
        self, a: core.Point3D | SketchPoint, b: core.Point3D | SketchPoint
    ) -> SketchLine:
        """Add a line; points may be new positions or existing sketch points."""
        sk = self._sketch
        pa, pb = sk.as_point(a), sk.as_point(b)
        line = SketchLine(sk, pa, pb)
        sk.lines.append(line)
        world().trace_event("line", sk.to_model(pa.geometry), sk.to_model(pb.geometry))
        return line


class SketchCircles:
    """Circles of a sketch."""

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch

    def addByCenterRadius(self, center: core.Point3D, radius: float) -> SketchCircle:
        """Add a circle."""
        sk = self._sketch
        if radius <= 0:
            world().errors.append("circle with radius <= 0")
        circle = SketchCircle(SketchPoint(sk, center), radius)
        sk.circles.append(circle)
        world().trace_event("circle", sk.to_model(center), mm(radius))
        return circle


class SketchPoints:
    """Free points of a sketch."""

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch

    def add(self, point: core.Point3D) -> SketchPoint:
        """Add a point."""
        sk = self._sketch
        world().trace_event("point", sk.to_model(point))
        return SketchPoint(sk, point)


class GeometricConstraints:
    """Geometric constraints; each checks that it holds for the geometry."""

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch

    @staticmethod
    def _check(ok: bool, what: str) -> None:
        if not ok:
            world().errors.append("constraint does not hold: " + what)

    def addHorizontal(self, line: SketchLine) -> object:
        """Keep a line horizontal."""
        self._check(
            abs(line.endSketchPoint.geometry.y - line.startSketchPoint.geometry.y) < 1e-9,
            "horizontal",
        )
        world().trace_event("constraint.horizontal")
        return object()

    def addVertical(self, line: SketchLine) -> object:
        """Keep a line vertical."""
        self._check(
            abs(line.endSketchPoint.geometry.x - line.startSketchPoint.geometry.x) < 1e-9,
            "vertical",
        )
        world().trace_event("constraint.vertical")
        return object()

    def addHorizontalPoints(self, a: SketchPoint, b: SketchPoint) -> object:
        """Keep two points at the same sketch y."""
        if not world().point_constraints:
            raise AttributeError("addHorizontalPoints")
        self._check(abs(a.geometry.y - b.geometry.y) < 1e-9, "horizontal points")
        world().trace_event("constraint.horizontalPoints")
        return object()

    def addVerticalPoints(self, a: SketchPoint, b: SketchPoint) -> object:
        """Keep two points at the same sketch x."""
        if not world().point_constraints:
            raise AttributeError("addVerticalPoints")
        self._check(abs(a.geometry.x - b.geometry.x) < 1e-9, "vertical points")
        world().trace_event("constraint.verticalPoints")
        return object()

    def addCoincident(self, point: SketchPoint, line: SketchLine) -> object:
        """Put a point on a line."""
        a, b, g = line.startSketchPoint.geometry, line.endSketchPoint.geometry, point.geometry
        cross = (b.x - a.x) * (g.y - a.y) - (b.y - a.y) * (g.x - a.x)
        self._check(abs(cross) < 1e-9, "coincident")
        world().trace_event("constraint.coincident")
        return object()


class SketchDimensions:
    """Dimensions of a sketch.

    Like Fusion, a second horizontal or vertical distance from the projected
    origin to a point that lies exactly on an already dimensioned coordinate
    is refused with ``VCS_SKETCH_OVER_CONSTRAINTS``.
    """

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch
        self._from_origin: set[tuple[str, float]] = set()

    def addDistanceDimension(
        self, a: SketchPoint, b: SketchPoint, orientation: str, text: core.Point3D
    ) -> SketchDimension:
        """Distance between two points along ``orientation``."""
        if a.reference and orientation != DimensionOrientations.AlignedDimensionOrientation:
            horizontal = orientation == DimensionOrientations.HorizontalDimensionOrientation
            coord = round(b.geometry.x if horizontal else b.geometry.y, 9)
            key = (orientation, coord)
            if key in self._from_origin:
                world().trace_event("dimension.refused", orientation)
                raise RuntimeError(
                    "3 : VCS_SKETCH_OVER_CONSTRAINTS - Sketch geometry is over constrained"
                )
            self._from_origin.add(key)
        return SketchDimension("distance", a, b, orientation)

    def addOffsetDimension(
        self, line: SketchLine, point: SketchPoint, text: core.Point3D
    ) -> SketchDimension:
        """Distance from a point to a line."""
        return SketchDimension("offset", point, line, None)

    def addDiameterDimension(self, circle: SketchCircle, text: core.Point3D) -> SketchDimension:
        """Diameter of a circle."""
        return SketchDimension("diameter", circle, None, None)


class Profile:
    """Closed profile of a sketch."""

    def __init__(self, sketch: Sketch, index: int) -> None:
        self.sketch = sketch
        self.index = index


class Profiles:
    """Profiles of a sketch: one per closed loop."""

    def __init__(self, sketch: Sketch) -> None:
        self._sketch = sketch

    @property
    def count(self) -> int:
        """Number of closed loops."""
        return self._sketch.loop_count()

    def item(self, index: int) -> Profile:
        """Profile at ``index``."""
        return Profile(self._sketch, index)


class SketchCurves:
    """Curves of a sketch."""

    def __init__(self, sketch: Sketch) -> None:
        self.sketchLines = SketchLines(sketch)
        self.sketchCircles = SketchCircles(sketch)


class Sketch:
    """Sketch on a plane."""

    def __init__(self, component: Component, plane: Plane) -> None:
        self.component = component
        self.plane = plane
        self._name = ""
        self._visible = True
        self.lines: list[SketchLine] = []
        self.circles: list[SketchCircle] = []
        self.xDirection = plane.xdir
        self.yDirection = plane.ydir
        self.sketchCurves = SketchCurves(self)
        self.sketchPoints = SketchPoints(self)
        self.geometricConstraints = GeometricConstraints(self)
        self.sketchDimensions = SketchDimensions(self)
        self.profiles = Profiles(self)

    @property
    def name(self) -> str:
        """Name shown in the browser."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        world().trace_event("sketch.name", value)

    @property
    def isVisible(self) -> bool:
        """Visibility."""
        return self._visible

    @isVisible.setter
    def isVisible(self, value: bool) -> None:
        self._visible = value
        world().trace_event("sketch.visible", self._name, value)

    def as_point(self, p: core.Point3D | SketchPoint) -> SketchPoint:
        """Wrap a position as a new sketch point, or keep an existing one."""
        return p if isinstance(p, SketchPoint) else SketchPoint(self, p)

    def to_model(self, p: core.Point3D) -> tuple[float, float, float]:
        """Model coordinates (mm, rounded) of a sketch-space point."""
        pl = self.plane
        return (
            mm(pl.origin.x + pl.xdir.x * p.x + pl.ydir.x * p.y),
            mm(pl.origin.y + pl.xdir.y * p.x + pl.ydir.y * p.y),
            mm(pl.origin.z + pl.xdir.z * p.x + pl.ydir.z * p.y),
        )

    def modelToSketchSpace(self, p: core.Point3D) -> core.Point3D:
        """Convert a model point to sketch space."""
        pl = self.plane
        d = core.Vector3D(p.x - pl.origin.x, p.y - pl.origin.y, p.z - pl.origin.z)
        return core.Point3D(
            d.x * pl.xdir.x + d.y * pl.xdir.y + d.z * pl.xdir.z,
            d.x * pl.ydir.x + d.y * pl.ydir.y + d.z * pl.ydir.z,
            d.x * pl.normal.x + d.y * pl.normal.y + d.z * pl.normal.z,
        )

    def project(self, entity: Any) -> core.ObjectCollection:
        """Project the origin point or an axis into the sketch."""
        result = core.ObjectCollection()
        o = self.modelToSketchSpace(core.Point3D(0.0, 0.0, 0.0))
        if isinstance(entity, OriginPoint):
            world().trace_event("sketch.project", "origin")
            result.add(SketchPoint(self, core.Point3D(o.x, o.y, 0.0), reference=True))
            return result
        assert isinstance(entity, ConstructionAxis)
        q = self.modelToSketchSpace(core.Point3D(*entity.direction))
        if abs(q.x - o.x) < 1e-9 and abs(q.y - o.y) < 1e-9:
            world().errors.append("axis projects to a point")
        world().trace_event("sketch.project", "axis", entity.direction)
        start = SketchPoint(self, core.Point3D(o.x, o.y, 0.0), reference=True)
        end = SketchPoint(self, core.Point3D(q.x, q.y, 0.0), reference=True)
        result.add(SketchLine(self, start, end, projected=True))
        return result

    def loop_count(self) -> int:
        """Closed loops formed by profile lines and circles."""
        parent: dict[int, int] = {}

        def find(i: int) -> int:
            while parent.setdefault(i, i) != i:
                i = parent[i]
            return i

        for line in self.lines:
            if line.isConstruction:
                continue
            parent[find(id(line.startSketchPoint))] = find(id(line.endSketchPoint))
        roots = {find(id(line.startSketchPoint)) for line in self.lines if not line.isConstruction}
        return len(roots) + len(self.circles)


class Sketches:
    """Sketches of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component
        self.items: list[Sketch] = []

    @property
    def count(self) -> int:
        """Number of sketches."""
        return len(self.items)

    def add(self, plane: ConstructionPlane) -> Sketch:
        """Create a sketch on a plane."""
        sketch = Sketch(self._component, plane.geometry)
        self.items.append(sketch)
        world().trace_event("sketch.add", self._component.name, plane.geometry.key())
        return sketch


# ---------------------------------------------------------------- bodies and features
class BRepBody:
    """Solid body; containment answers come from the last feature outcome."""

    def __init__(self, component: Component) -> None:
        self.component = component
        self.edges = core.ObjectCollection()
        self._appearance: Appearance | None = None

    def pointContainment(self, point: core.Point3D) -> str:
        """Whether ``point`` is inside the body."""
        w = world()
        if w.containment_queue:
            return w.containment_queue.pop(0)
        return w.containment

    @property
    def appearance(self) -> Appearance | None:
        """Appearance override."""
        return self._appearance

    @appearance.setter
    def appearance(self, value: Appearance) -> None:
        self._appearance = value
        world().trace_event("body.appearance", self.component.name, value.name)


class BRepBodies:
    """Bodies of a component."""

    def __init__(self) -> None:
        self.items: list[BRepBody] = []

    @property
    def count(self) -> int:
        """Number of bodies."""
        return len(self.items)

    def item(self, index: int) -> BRepBody:
        """Body at ``index``."""
        return self.items[index]


class Feature:
    """Timeline feature."""

    def __init__(
        self, component: Component, kind: str, bodies: list[BRepBody] | None = None
    ) -> None:
        self.component = component
        self.kind = kind
        self.bodies = core.ObjectCollection()
        for b in bodies or []:
            self.bodies.add(b)

    def deleteMe(self) -> bool:
        """Remove the feature and the bodies it created."""
        for b in self.bodies.items:
            if b in self.component.bRepBodies.items:
                self.component.bRepBodies.items.remove(b)
        world().trace_event("feature.delete", self.kind)
        return True


def _outcome(op: str, key: tuple[Any, ...], one_sided: bool, taper: str | None = None) -> None:
    """Decide what probe points report after a feature."""
    w = world()
    ok = True
    if one_sided and w.fail_first_direction:
        w.attempts[key] = w.attempts.get(key, 0) + 1
        ok = w.attempts[key] % 2 == 0
    good = (
        PointContainment.PointOutsidePointContainment
        if op == FeatureOperations.CutFeatureOperation
        else "IN"
    )
    bad = "IN" if good == "OUT" else "OUT"
    w.containment = good if ok else bad
    w.containment_queue = []
    if taper is not None:
        right_sign = taper.startswith("-(")
        w.containment_queue = [good if ok else bad, "IN" if right_sign else "OUT"]


class ExtrudeInput:
    """Definition of an extrude."""

    def __init__(self, profiles: core.ObjectCollection, operation: str) -> None:
        self.profiles = profiles
        self.operation = operation
        self.kind = ""
        self.distance = ""
        self.direction = ""
        self.taper: str | None = None

    def setSymmetricExtent(self, distance: core.ValueInput, is_full_length: bool) -> bool:
        """Extrude symmetrically about the sketch plane."""
        self.kind = "symmetric" if is_full_length else "symmetric-half"
        self.distance = distance.stringValue
        world().evaluate(self.distance)
        return True

    def setOneSideExtent(
        self,
        extent: DistanceExtentDefinition,
        direction: str,
        taper: core.ValueInput | None = None,
    ) -> bool:
        """Extrude to one side."""
        self.kind = "one-side"
        self.distance = extent.distance.stringValue
        self.direction = direction
        self.taper = taper.stringValue if taper is not None else None
        world().evaluate(self.distance)
        if self.taper is not None:
            world().evaluate(self.taper)
        return True


class ExtrudeFeatures:
    """Extrude features of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component

    def createInput(self, profiles: core.ObjectCollection, operation: str) -> ExtrudeInput:
        """Create an input."""
        if profiles.count == 0:
            world().errors.append("extrude without profiles")
        return ExtrudeInput(profiles, operation)

    def add(self, definition: ExtrudeInput) -> Feature:
        """Create the extrude."""
        c = self._component
        if not definition.kind:
            world().errors.append("extrude without extent")
        sketch_name = definition.profiles.item(0).sketch.name if definition.profiles.count else ""
        bodies: list[BRepBody] = []
        if definition.operation == FeatureOperations.NewBodyFeatureOperation:
            bodies = [BRepBody(c) for _ in range(max(1, definition.profiles.count))]
            c.bRepBodies.items.extend(bodies)
        elif not c.bRepBodies.items:
            world().errors.append("join or cut with no body in " + c.name)
        world().trace_event(
            "extrude",
            c.name,
            sketch_name,
            definition.operation,
            definition.kind,
            definition.distance,
            definition.direction,
            definition.taper,
            definition.profiles.count,
        )
        _outcome(
            definition.operation,
            (c.name, sketch_name, definition.taper),
            definition.kind == "one-side",
            definition.taper,
        )
        return Feature(c, "extrude", bodies)


class _EdgeSets:
    def __init__(self) -> None:
        self.sets: list[tuple[int, str]] = []

    def addConstantRadiusEdgeSet(
        self, edges: core.ObjectCollection, radius: core.ValueInput, tangent: bool
    ) -> bool:
        world().evaluate(radius.stringValue)
        self.sets.append((edges.count, radius.stringValue))
        return True

    def addEqualDistanceChamferEdgeSet(
        self, edges: core.ObjectCollection, distance: core.ValueInput, tangent: bool
    ) -> bool:
        world().evaluate(distance.stringValue)
        self.sets.append((edges.count, distance.stringValue))
        return True


class FilletInput:
    """Definition of a fillet."""

    def __init__(self) -> None:
        self.edgeSetInputs = _EdgeSets()


class FilletFeatures:
    """Fillet features of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component

    def createInput(self) -> FilletInput:
        """Create an input."""
        return FilletInput()

    def add(self, definition: FilletInput) -> Feature:
        """Create the fillet."""
        world().trace_event("fillet", self._component.name, definition.edgeSetInputs.sets)
        return Feature(self._component, "fillet")


class ChamferInput:
    """Definition of a chamfer."""

    def __init__(self) -> None:
        self.chamferEdgeSets = _EdgeSets()


class ChamferFeatures:
    """Chamfer features of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component

    def createInput2(self) -> ChamferInput:
        """Create an input."""
        return ChamferInput()

    def add(self, definition: ChamferInput) -> Feature:
        """Create the chamfer."""
        world().trace_event("chamfer", self._component.name, definition.chamferEdgeSets.sets)
        return Feature(self._component, "chamfer")


class HoleInput:
    """Definition of a countersunk hole."""

    def __init__(
        self, diameter: core.ValueInput, csk: core.ValueInput, angle: core.ValueInput
    ) -> None:
        self.values = (diameter.stringValue, csk.stringValue, angle.stringValue)
        for v in self.values:
            world().evaluate(v)
        self.points = 0
        self.depth = ""
        self.isDefaultDirection = True

    def setPositionBySketchPoints(self, points: core.ObjectCollection) -> bool:
        """Place holes at sketch points."""
        if points.count == 0:
            world().errors.append("hole without points")
        self.points = points.count
        return True

    def setDistanceExtent(self, distance: core.ValueInput) -> bool:
        """Hole depth."""
        self.depth = distance.stringValue
        world().evaluate(self.depth)
        return True


class HoleFeatures:
    """Hole features of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component

    def createCountersinkInput(
        self, diameter: core.ValueInput, csk: core.ValueInput, angle: core.ValueInput
    ) -> HoleInput:
        """Create an input."""
        return HoleInput(diameter, csk, angle)

    def add(self, definition: HoleInput) -> Feature:
        """Create the holes."""
        c = self._component
        if world().hole_feature_broken:
            world().trace_event("hole.failed", c.name)
            raise RuntimeError("hole feature failed (simulated)")
        world().trace_event(
            "hole",
            c.name,
            *definition.values,
            definition.depth,
            definition.isDefaultDirection,
            definition.points,
        )
        _outcome(FeatureOperations.CutFeatureOperation, ("hole", c.name, definition.values), True)
        return Feature(c, "hole")


class CombineInput:
    """Definition of a combine."""

    def __init__(self, target: BRepBody, tools: core.ObjectCollection) -> None:
        self.target = target
        self.tools = tools
        self.operation = FeatureOperations.JoinFeatureOperation


class CombineFeatures:
    """Combine features of a component."""

    def __init__(self, component: Component) -> None:
        self._component = component

    def createInput(self, target: BRepBody, tools: core.ObjectCollection) -> CombineInput:
        """Create an input."""
        return CombineInput(target, tools)

    def add(self, definition: CombineInput) -> Feature:
        """Join the tool bodies into the target."""
        c = self._component
        for b in definition.tools.items:
            c.bRepBodies.items.remove(b)
        index = c.bRepBodies.items.index(definition.target)
        world().trace_event("combine", c.name, index, definition.tools.count, definition.operation)
        return Feature(c, "combine")


class Features:
    """Feature collections of a component."""

    def __init__(self, component: Component) -> None:
        self.extrudeFeatures = ExtrudeFeatures(component)
        self.filletFeatures = FilletFeatures(component)
        self.chamferFeatures = ChamferFeatures(component)
        self.holeFeatures = HoleFeatures(component)
        self.combineFeatures = CombineFeatures(component)


# ---------------------------------------------------------------- attributes and components
class Attribute:
    """Named string value attached to an object."""

    def __init__(self, value: str) -> None:
        self.value = value


class Attributes:
    """Attributes of an object."""

    def __init__(self, owner: str) -> None:
        self._owner = owner
        self.items: dict[tuple[str, str], Attribute] = {}

    def add(self, group: str, name: str, value: str) -> Attribute:
        """Add or replace an attribute."""
        attr = Attribute(value)
        self.items[(group, name)] = attr
        world().trace_event("attribute.add", self._owner, group, name, value)
        return attr

    def itemByName(self, group: str, name: str) -> Attribute | None:
        """Attribute or None."""
        return self.items.get((group, name))


class Occurrence:
    """Occurrence of a component in a parent component."""

    def __init__(
        self, parent: Occurrences, component: Component, transform: core.Matrix3D
    ) -> None:
        self._parent = parent
        self.component = component
        self.transform2 = transform
        self.attributes = Attributes("occurrence")

    def deleteMe(self) -> bool:
        """Remove the occurrence."""
        self._parent.items.remove(self)
        world().trace_event("occurrence.delete", self.component.name)
        return True


class Occurrences:
    """Occurrences inside a component."""

    def __init__(self, owner: Component) -> None:
        self._owner = owner
        self.items: list[Occurrence] = []

    @property
    def count(self) -> int:
        """Number of occurrences."""
        return len(self.items)

    def item(self, index: int) -> Occurrence:
        """Occurrence at ``index``."""
        return self.items[index]

    def addNewComponent(self, transform: core.Matrix3D) -> Occurrence:
        """Create a new component and an occurrence of it."""
        component = Component(self._owner.design)
        occurrence = Occurrence(self, component, transform)
        self.items.append(occurrence)
        world().trace_event("occurrence.new", self._owner.name, transform.key())
        return occurrence

    def addExistingComponent(self, component: Component, transform: core.Matrix3D) -> Occurrence:
        """Add another occurrence of an existing component."""
        occurrence = Occurrence(self, component, transform)
        self.items.append(occurrence)
        world().trace_event(
            "occurrence.existing", self._owner.name, component.name, transform.key()
        )
        return occurrence


class Component:
    """Component with its own sketches, features and bodies."""

    def __init__(self, design: Design, name: str = "") -> None:
        self.design = design
        design.components.append(self)
        self._name = name
        o = core.Point3D(0.0, 0.0, 0.0)
        x, y, z = (
            core.Vector3D(1.0, 0.0, 0.0),
            core.Vector3D(0.0, 1.0, 0.0),
            core.Vector3D(0.0, 0.0, 1.0),
        )
        self.xYConstructionPlane = ConstructionPlane(Plane(o, x, y))
        # Fusion's XZ plane: sketch x along +X, sketch y along -Z, normal +Y
        self.xZConstructionPlane = ConstructionPlane(Plane(o, x, core.Vector3D(0.0, 0.0, -1.0)))
        self.originConstructionPoint = OriginPoint()
        self.xConstructionAxis = ConstructionAxis((1.0, 0.0, 0.0))
        self.yConstructionAxis = ConstructionAxis((0.0, 1.0, 0.0))
        self.zConstructionAxis = ConstructionAxis((0.0, 0.0, 1.0))
        self.constructionPlanes = ConstructionPlanes()
        self.sketches = Sketches(self)
        self.features = Features(self)
        self.bRepBodies = BRepBodies()
        self.occurrences = Occurrences(self)

    @property
    def name(self) -> str:
        """Component name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        world().trace_event("component.name", value)


class Components:
    """All components of a design."""

    def __init__(self, items: list[Component]) -> None:
        self._items = items

    @property
    def count(self) -> int:
        """Number of components."""
        return len(self._items)

    def item(self, index: int) -> Component:
        """Component at ``index``."""
        return self._items[index]


# ---------------------------------------------------------------- appearances
class Appearance:
    """Appearance with colour properties."""

    def __init__(self, name: str, properties: list[core.ColorProperty]) -> None:
        self.name = name
        self.appearanceProperties = core.ObjectCollection()
        for p in properties:
            self.appearanceProperties.add(p)


class Appearances:
    """Appearances of a library or a design."""

    def __init__(self, items: list[Appearance] | None = None) -> None:
        self.items = items or []

    @property
    def count(self) -> int:
        """Number of appearances."""
        return len(self.items)

    def item(self, index: int) -> Appearance:
        """Appearance at ``index``."""
        return self.items[index]

    def itemByName(self, name: str) -> Appearance | None:
        """Appearance or None."""
        return next((a for a in self.items if a.name == name), None)

    def addByCopy(self, base: Appearance, name: str) -> Appearance:
        """Copy a library appearance into the design."""
        copy = Appearance(
            name, [core.ColorProperty(p.id, p.name) for p in base.appearanceProperties.items]
        )
        self.items.append(copy)
        world().trace_event("appearance.copy", base.name, name)
        return copy


class MaterialLibrary:
    """Material or appearance library."""

    def __init__(self, lib_id: str, name: str, appearances: list[Appearance]) -> None:
        self.id = lib_id
        self.name = name
        self.appearances = Appearances(appearances)


class MaterialLibraries:
    """Libraries known to the application."""

    APPEARANCE_LIBRARY_ID = "BA5EE55E-9982-449B-9D66-9F036540E140"

    def __init__(self) -> None:
        plastic = Appearance(
            "Plastic - Matte (Yellow)", [core.ColorProperty("opaque_albedo", "Color")]
        )
        self.items = [
            MaterialLibrary("C1EEA57C-3F56-45FC-B8CB-A9EC46A9994C", "Fusion Material Library", []),
            MaterialLibrary(self.APPEARANCE_LIBRARY_ID, "Fusion Appearance Library", [plastic]),
        ]

    @property
    def count(self) -> int:
        """Number of libraries."""
        return len(self.items)

    def item(self, index: int) -> MaterialLibrary:
        """Library at ``index``."""
        return self.items[index]

    def itemById(self, lib_id: str) -> MaterialLibrary | None:
        """Library or None."""
        return next((lib for lib in self.items if lib.id == lib_id), None)


# ---------------------------------------------------------------- parameters and design
class UserParameter:
    """User parameter."""

    def __init__(self, name: str, comment: str) -> None:
        self.name = name
        self._comment = comment

    @property
    def expression(self) -> str:
        """Expression."""
        return world().expressions[self.name]

    @expression.setter
    def expression(self, expr: str) -> None:
        w = world()
        w.expressions[self.name] = expr
        w.recompute()
        w.trace_event("parameter.expression", self.name, expr)

    @property
    def comment(self) -> str:
        """Comment."""
        return self._comment

    @comment.setter
    def comment(self, text: str) -> None:
        self._comment = text
        world().trace_event("parameter.comment", self.name, text)


class UserParameters:
    """User parameters of a design."""

    def __init__(self) -> None:
        self.items: dict[str, UserParameter] = {}

    @property
    def count(self) -> int:
        """Number of parameters."""
        return len(self.items)

    def itemByName(self, name: str) -> UserParameter | None:
        """Parameter or None."""
        return self.items.get(name)

    def add(self, name: str, value: core.ValueInput, units: str, comment: str) -> UserParameter:
        """Create a parameter."""
        if name in self.items:
            raise RuntimeError("parameter already exists: " + name)
        w = world()
        w.order.append(name)
        w.expressions[name] = value.stringValue
        w.values[name] = w.evaluate(value.stringValue)
        param = UserParameter(name, comment)
        self.items[name] = param
        w.trace_event("parameter.add", name, value.stringValue, units, comment)
        return param


class UnitsManager:
    """Units manager of a design."""

    def evaluateExpression(self, expr: str, units: str) -> float:
        """Evaluate in internal units (centimetres)."""
        return world().evaluate(expr) * CM_PER_MM


class Design:
    """Fusion design."""

    def __init__(self) -> None:
        self.components: list[Component] = []
        self.unitsManager = UnitsManager()
        self.userParameters = UserParameters()
        self.attributes = Attributes("design")
        self.appearances = Appearances()
        self._design_type = ""
        self._intent = "HY"
        self.rootComponent = Component(self, "(Unsaved)")

    @staticmethod
    def cast(obj: Any) -> Design | None:
        """Return ``obj`` if it is a design, else None."""
        return obj if isinstance(obj, Design) else None

    @property
    def allComponents(self) -> Components:
        """All components of the design."""
        return Components(self.components)

    @property
    def designType(self) -> str:
        """Parametric or direct."""
        return self._design_type

    @designType.setter
    def designType(self, value: str) -> None:
        self._design_type = value
        world().trace_event("design.type", value)

    @property
    def designIntent(self) -> str:
        """Hybrid, part or assembly."""
        return self._intent

    @designIntent.setter
    def designIntent(self, value: str) -> None:
        self._intent = value
        world().trace_event("design.intent", value)

    def modifyParameters(self, params: list[UserParameter], values: list[core.ValueInput]) -> bool:
        """Change several parameters with one recompute."""
        w = world()
        for p, v in zip(params, values):
            w.expressions[p.name] = v.stringValue
        w.recompute()
        w.trace_event(
            "parameters.modify", [(p.name, v.stringValue) for p, v in zip(params, values)]
        )
        return True

    def computeAll(self) -> bool:
        """Recompute the timeline."""
        world().trace_event("design.computeAll")
        return True
