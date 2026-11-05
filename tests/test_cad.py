# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Sketch, feature, appearance, design and system helpers against the fake API.

The golden traces cover the normal build paths; these tests cover the
fallbacks that only run when Fusion refuses something.
"""

from __future__ import annotations

import json
from typing import Any, cast

import pytest

import tests.fake_adsk as fake
from Liana.cad import appearance, design, features, system
from Liana.cad.api import CUT, JOIN, NEW_BODY, collection
from Liana.cad.context import BuildContext
from Liana.cad.sketch import ParamSketch, plane_y
from Liana.core.report import BuildLog
from Liana.core.settings import defaults, from_mapping
from tests.fake_adsk import core, fusion


def new_context() -> tuple[BuildContext, Any]:
    """Return a build context on a fresh design with parameters, and a component."""
    app = core.Application.get()
    d = fusion.Design()
    design.upsert_params(d, defaults())
    comp = fusion.Component(d, "Part")
    return BuildContext(app, d, BuildLog()), comp


def events(w: fake.World, name: str) -> list[tuple[Any, ...]]:
    return [e for e in w.trace if e[0] == name]


# ---------------------------------------------------------------- context


def test_soft_logs_the_first_line_of_any_error(world: fake.World) -> None:
    ctx, _ = new_context()

    def fail() -> None:
        raise ValueError("bad\nmore")

    assert ctx.soft("Step", fail) is None
    assert ctx.soft("Ok", lambda: 3) == 3
    assert ctx.log.soft == ["Step: bad"]


def test_mag_turns_negative_expressions_positive(world: fake.World) -> None:
    ctx, _ = new_context()
    expr, value = ctx.mag("-PLATE_T")
    assert expr == "-(-PLATE_T)" and value == pytest.approx(3.0)
    expr, value = ctx.mag("PLATE_T")
    assert expr == "PLATE_T" and value == pytest.approx(3.0)


# ---------------------------------------------------------------- sketch


def test_point_on_an_axis_is_made_coincident(world: fake.World) -> None:
    ctx, comp = new_context()
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("0 mm", "PLATE_T")
    assert len(events(world, "constraint.coincident")) == 1
    assert ctx.log.dims == []


def test_same_coordinate_is_aligned_not_dimensioned_twice(world: fake.World) -> None:
    ctx, comp = new_context()
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("PLATE_T", "PAD_T")
    sk.point("PLATE_T", "END_W")
    assert ctx.log.aligned == ["S | axis 0 = PLATE_T"]
    assert world.errors == []


def test_without_point_constraints_a_construction_line_aligns(world: fake.World) -> None:
    world.point_constraints = False
    ctx, comp = new_context()
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("PLATE_T", "PAD_T")
    sk.point("PLATE_T", "END_W")
    assert events(world, "constraint.vertical") == [("constraint.vertical",)]
    assert ctx.log.aligned and not ctx.log.dims


def test_coincident_points_fall_back_to_an_offset_dimension(world: fake.World) -> None:
    world.point_constraints = False
    ctx, comp = new_context()
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("PLATE_T", "PAD_T")
    sk.point("PLATE_T", "PAD_T")
    assert len(events(world, "dimension.refused")) == 2
    assert ctx.log.dims == [] and world.errors == []


def test_refused_dimensions_are_logged(world: fake.World, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx, comp = new_context()

    def refuse(*args: Any) -> None:
        raise RuntimeError("refused\nby fake")

    monkeypatch.setattr(fusion.SketchDimensions, "addDistanceDimension", refuse)
    monkeypatch.setattr(fusion.SketchDimensions, "addOffsetDimension", refuse)
    monkeypatch.setattr(fusion.SketchDimensions, "addDiameterDimension", refuse)
    monkeypatch.setattr(fusion.GeometricConstraints, "addCoincident", refuse)
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.circle("0 mm", "PLATE_T", "WS_D")
    sk.rect("PLATE_T", "PAD_T", "END_W", "DEPTH")
    assert ctx.log.dims[:2] == [
        "S | diameter = WS_D | refused",
        "S | coincident to axis = 0 mm | refused",
    ]
    assert "S | coord axis 1 = PLATE_T | origin: refused / axis line: refused" in ctx.log.dims
    assert any(d.startswith("S | between axis 0") for d in ctx.log.dims)


def test_alignment_failure_dimensions_instead(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    world.point_constraints = False
    ctx, comp = new_context()

    def refuse(*args: Any) -> None:
        raise RuntimeError("no lines")

    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("PLATE_T", "PAD_T")
    monkeypatch.setattr(fusion.SketchLines, "addByTwoPoints", refuse)
    sk.point("PLATE_T", "END_W")
    assert ctx.log.aligned == []
    assert events(world, "dimension.refused")


def test_construction_flag_failure_is_tolerated(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx, comp = new_context()

    def refuse(self: Any, value: bool) -> None:
        raise RuntimeError("read-only")

    monkeypatch.setattr(fusion.SketchLine, "isConstruction", property(lambda self: False, refuse))
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "S", 0, 1)
    sk.point("0 mm", "PLATE_T")
    assert ctx.log.dims == []


def test_plane_y_reuses_the_base_plane_at_zero_and_hides_others(world: fake.World) -> None:
    ctx, comp = new_context()
    assert plane_y(ctx, comp, "0 mm") is comp.xZConstructionPlane
    plane_y(ctx, comp, "-PLATE_T")
    assert ("constructionPlane.visible", False) in world.trace


# ---------------------------------------------------------------- features


def sketch_with_rect(ctx: BuildContext, comp: Any) -> ParamSketch:
    sk = ParamSketch(ctx, comp, comp.xYConstructionPlane, "R", 0, 1)
    sk.rect("-EAR_X", "-PLATE_T", "EAR_X", "0 mm")
    return sk


def test_ext_one_deletes_wrong_results_and_raises(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    ctx, comp = new_context()
    features.ext_sym(comp, sketch_with_rect(ctx, comp), NEW_BODY, "DEPTH")
    monkeypatch.setattr(features, "inside", lambda c, p: True)
    with pytest.raises(RuntimeError, match="R: extrude did not work in either direction"):
        features.ext_one(ctx, comp, sketch_with_rect(ctx, comp), CUT, "1 mm", 1, (0, 0, 0))
    assert len(events(world, "feature.delete")) == 2


def test_ext_one_reports_the_api_error(world: fake.World, monkeypatch: pytest.MonkeyPatch) -> None:
    ctx, comp = new_context()

    def refuse(*args: Any) -> None:
        raise RuntimeError("no profile")

    monkeypatch.setattr(fusion.ExtrudeFeatures, "add", refuse)
    with pytest.raises(RuntimeError, match=r"\(no profile\)"):
        features.ext_one(ctx, comp, sketch_with_rect(ctx, comp), JOIN, "1 mm", -1, (0, 0, 0))


def test_ext_one_checks_the_taper_sign(world: fake.World) -> None:
    ctx, comp = new_context()
    features.ext_sym(comp, sketch_with_rect(ctx, comp), NEW_BODY, "DEPTH")
    with pytest.raises(RuntimeError):
        features.ext_one(
            ctx,
            comp,
            sketch_with_rect(ctx, comp),
            CUT,
            "1 mm",
            1,
            (0, 0, 0),
            "(90 deg) / 2",
            (1, 1, 1),
        )


def test_combine_needs_two_bodies(world: fake.World) -> None:
    ctx, comp = new_context()
    assert features.combine(comp, (0, 0, 0)) is None


class Vertex:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.geometry = core.Point3D(x / 10, y / 10, z / 10)


class Box:
    def __init__(self, lo: Vertex, hi: Vertex) -> None:
        self.minPoint, self.maxPoint = lo.geometry, hi.geometry


class Geometry:
    def __init__(self, kind: str) -> None:
        self.objectType = kind


class Edge:
    """Edge between two points in mm; ``curved`` edges are arcs."""

    def __init__(
        self, a: tuple[float, float, float], b: tuple[float, float, float], curved: bool = False
    ) -> None:
        self.startVertex, self.endVertex = Vertex(*a), Vertex(*b)
        self.geometry = Geometry("arc" if curved else core.Line3D.classType())
        lo = tuple(min(p, q) for p, q in zip(a, b))
        hi = tuple(max(p, q) for p, q in zip(a, b))
        self.boundingBox = Box(Vertex(*lo), Vertex(*hi))


class ClosedEdge:
    """A full circle: Fusion gives it no vertices."""

    geometry = Geometry("circle")

    @property
    def startVertex(self) -> Any:
        raise RuntimeError("no vertex")


class Body:
    def __init__(self, edges: list[Any]) -> None:
        self.edges = collection(edges)


def test_edge_finders() -> None:
    along_z = Edge((5, -3, -6), (5, -3, 6))
    along_y = Edge((5, 0, 6), (5, -3, 6))
    arc = Edge((1, -4, 0), (2, -4, 1), curved=True)
    flat = Edge((0, -4, 0), (3, -4, 0))
    body = Body([along_z, along_y, arc, flat, ClosedEdge()])
    assert features.z_edges([body], [(5, -3)]) == [along_z]
    assert features.z_edges([body], [(5, -2)]) == []
    assert features.y_edges([body], [(5, 6)]) == [along_y]
    assert features.face_edges_at_y([body], -4.0) == [arc, flat]
    assert [e for e, _, _ in features.line_edges([body])] == [along_z, along_y, flat]
    assert features.sym(2, 3) == [(2, 3), (-2, 3)]
    assert features.corners(1, 2) == [(1, 2), (-1, 2), (1, -2), (-1, -2)]


def test_end_face_edges_finds_the_slot_mouth() -> None:
    mouth = Edge((-2, -10, 6), (2, -10, 6))
    back = Edge((-2, -10, -6), (2, -10, -6))
    too_wide = Edge((-5, -10, 6), (5, -10, 6))
    too_low = Edge((-2, -14, 6), (2, -14, 6))
    along_z = Edge((1, -10, -6), (1, -10, 6))
    inner = Edge((-2, -10, 3), (2, -10, 3))
    body = Body([mouth, back, too_wide, too_low, along_z, inner])
    assert features.end_face_edges([body], 6.0, 0.0, 3.0, -12.0, -8.0) == [mouth, back]


def test_fillet_and_chamfer(world: fake.World) -> None:
    ctx, comp = new_context()
    edge = Edge((0, 0, 0), (0, 0, 1))
    with pytest.raises(RuntimeError, match="edges not found"):
        features.fillet(comp, [], "1 mm")
    with pytest.raises(RuntimeError, match="edges not found"):
        features.chamfer(comp, [], "1 mm")
    features.fillet(comp, [edge], "END_R")
    features.chamfer(comp, [edge, edge], "LIP_CH")
    assert events(world, "fillet") == [("fillet", "Part", [(1, "END_R")])]
    assert events(world, "chamfer") == [("chamfer", "Part", [(2, "LIP_CH")])]


class OldFilletInput:
    def __init__(self) -> None:
        self.sets: list[str] = []

    def addConstantRadiusEdgeSet(self, edges: Any, radius: Any, tangent: bool) -> None:
        self.sets.append(radius.stringValue)


class OldChamferInput:
    def __init__(self, edges: Any, tangent: bool) -> None:
        self.distance = ""

    def setToEqualDistance(self, distance: Any) -> None:
        self.distance = distance.stringValue


class OldFeatures:
    """Fillet and chamfer collections of a Fusion release before edge sets."""

    def __init__(self) -> None:
        self.added: list[Any] = []

    def createInput(self, *args: Any) -> Any:
        return OldChamferInput(*args) if args else OldFilletInput()

    def add(self, definition: Any) -> Any:
        self.added.append(definition)
        return definition


class OldComponent:
    def __init__(self) -> None:
        self.features = type(
            "F", (), {"filletFeatures": OldFeatures(), "chamferFeatures": OldFeatures()}
        )()


def test_fillet_and_chamfer_on_older_fusion() -> None:
    comp = OldComponent()
    fil = features.fillet(comp, [object()], "1 mm")
    cha = features.chamfer(comp, [object()], "0.5 mm")
    assert fil.sets == ["1 mm"]
    assert cha.distance == "0.5 mm"


def test_countersink_fallback_tries_both_taper_signs(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    world.hole_feature_broken = True
    ctx, comp = new_context()
    features.ext_sym(comp, sketch_with_rect(ctx, comp), NEW_BODY, "DEPTH")
    real = features.ext_one
    tapers: list[str | None] = []

    def ext_one(*args: Any, taper: str | None = None, **kwargs: Any) -> Any:
        tapers.append(taper)
        if taper is not None:
            raise RuntimeError("taper refused")
        return real(*args, **kwargs)

    monkeypatch.setattr(features, "ext_one", ext_one)
    with pytest.raises(RuntimeError, match=r"Holes: countersink failed \(taper refused\)"):
        features.csk_holes(
            ctx,
            comp,
            "-PAD_T",
            [("EAR_X", "0 mm")],
            "WS_D",
            "WS_CSK",
            "CSK_ANGLE",
            "PAD_T",
            "Holes",
        )
    assert tapers == [None, "-(CSK_ANGLE) / 2", "(CSK_ANGLE) / 2"]
    assert ctx.log.soft == ["Holes: Hole feature did not work, built as extrude cut"]


def test_hole_in_the_wrong_direction_is_redone(world: fake.World) -> None:
    world.fail_first_direction = True
    ctx, comp = new_context()
    features.ext_sym(comp, sketch_with_rect(ctx, comp), NEW_BODY, "DEPTH")
    features.csk_holes(
        ctx, comp, "-PAD_T", [("EAR_X", "0 mm")], "WS_D", "WS_CSK", "CSK_ANGLE", "PAD_T", "Holes"
    )
    holes = events(world, "hole")
    assert [h[6] for h in holes] == [False, True]
    assert ("sketch.visible", "Holes", False) in world.trace


# ---------------------------------------------------------------- appearance


def test_appearances_are_created_once(world: fake.World) -> None:
    app = core.Application.get()
    d = fusion.Design()
    first = appearance.part_appearance(app, d, "Liana Red", (220, 45, 45))
    again = appearance.part_appearance(app, d, "Liana Red", (220, 45, 45))
    assert first is again
    assert events(world, "appearance.copy") == [
        ("appearance.copy", "Plastic - Matte (Yellow)", "Liana Red")
    ]
    assert events(world, "appearance.color") == [
        ("appearance.color", "opaque_albedo", (220, 45, 45, 0))
    ]


def test_library_is_found_by_name_and_any_plastic_will_do(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    app = core.Application.get()

    def refuse(self: Any, lib_id: str) -> None:
        raise RuntimeError("unknown id")

    monkeypatch.setattr(fusion.MaterialLibraries, "itemById", refuse)
    lib = app.materialLibraries.items[1]
    lib.appearances.items[0].name = "Plastic - Satin (Blue)"
    appearance.part_appearance(app, fusion.Design(), "Liana Blue", (1, 2, 3))
    assert events(world, "appearance.copy") == [
        ("appearance.copy", "Plastic - Satin (Blue)", "Liana Blue")
    ]


def test_appearance_without_color_property_fails(world: fake.World) -> None:
    app = core.Application.get()
    base = app.materialLibraries.items[1].appearances.items[0]
    gloss = type("Property", (), {"id": "surface_gloss", "name": "Gloss"})()
    base.appearanceProperties.items = [gloss]
    with pytest.raises(RuntimeError, match="no color property"):
        appearance.part_appearance(app, fusion.Design(), "Liana Red", (1, 2, 3))


def test_failing_library_lookup_by_name_is_skipped(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    app = core.Application.get()

    def refuse(self: Any, name: str) -> None:
        raise RuntimeError("lookup failed")

    monkeypatch.setattr(fusion.Appearances, "itemByName", refuse)
    lib = app.materialLibraries.items[1]
    assert appearance._base_appearance(lib) is lib.appearances.items[0]


# ---------------------------------------------------------------- design


def test_design_settings_round_trip_and_bad_data(world: fake.World) -> None:
    d = fusion.Design()
    assert design.load_design_settings(d) is None
    s = from_mapping({"cradles": 4})
    design.save_design_settings(d, s)
    assert design.load_design_settings(d) == s
    d.attributes.add("Liana", "settings", "{not json")
    assert design.load_design_settings(d) is None
    d.attributes.add("Liana", "settings", json.dumps([1, 2]))
    assert design.load_design_settings(d) is None


def test_save_design_settings_tolerates_refusal(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    def refuse(*args: Any) -> None:
        raise RuntimeError("read-only design")

    monkeypatch.setattr(fusion.Attributes, "add", refuse)
    design.save_design_settings(fusion.Design(), defaults())


def test_upsert_params_updates_in_one_call_or_one_by_one(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    d = fusion.Design()
    assert design.upsert_params(d, defaults()) == 0
    assert design.upsert_params(d, defaults()) == 0
    assert design.upsert_params(d, from_mapping({"cable_d": 11.0})) == 1

    def refuse(*args: Any) -> None:
        raise RuntimeError("no batch")

    monkeypatch.setattr(fusion.Design, "modifyParameters", refuse)
    monkeypatch.setattr(fusion.UserParameter, "comment", property(lambda self: "", refuse))
    assert design.upsert_params(d, from_mapping({"cable_d": 12.0, "tm_l": 40.0})) == 2
    assert world.expressions["CABLE_D"] == "12 mm" and world.expressions["TM_L"] == "40 mm"


def test_design_intent_helpers(world: fake.World, monkeypatch: pytest.MonkeyPatch) -> None:
    d = fusion.Design()
    assert design.is_hybrid(d) and design.is_empty(d)
    d.designIntent = "PART"
    assert not design.is_hybrid(d)

    class OldDesign:
        @property
        def designIntent(self) -> str:
            raise AttributeError("designIntent")

    assert design.is_hybrid(OldDesign())

    real = cast(property, vars(fusion.Design)["designIntent"])

    def refuse_hybrid(self: Any, value: str) -> None:
        if value == "HY":
            raise RuntimeError("no hybrid designs")
        assert real.fset is not None
        real.fset(self, value)

    world.new_design_intent = "PART"
    monkeypatch.setattr(fusion.Design, "designIntent", property(real.fget, refuse_hybrid))
    assert design.new_design(core.Application.get()).designIntent == "PART"


def test_find_system(world: fake.World) -> None:
    assert design.find_system(None) is None
    d = fusion.Design()
    assert design.find_system(d) is None
    occ = design.new_comp(d.rootComponent, "Liana")
    occ.attributes.add("Liana", "system", "1")
    assert design.find_system(d) is occ


# ---------------------------------------------------------------- system


def test_progress_without_ui_or_dialog(world: fake.World, monkeypatch: pytest.MonkeyPatch) -> None:
    quiet = system.Progress(None)
    quiet.start(3)
    quiet.step("x")
    quiet.close()

    def refuse(self: Any) -> None:
        raise RuntimeError("no dialogs")

    monkeypatch.setattr(core.UserInterface, "createProgressDialog", refuse)
    broken = system.Progress(core.Application.get().userInterface)
    broken.start(2)
    broken.step("y")
    broken.close()
    assert not [e for e in world.trace if e[0].startswith("progress")]


def test_progress_survives_dialog_errors(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    progress = system.Progress(core.Application.get().userInterface)
    progress.start(2)

    def refuse(*args: Any) -> None:
        raise RuntimeError("dialog gone")

    monkeypatch.setattr(core.ProgressDialog, "message", property(lambda self: "", refuse))
    monkeypatch.setattr(core.ProgressDialog, "hide", refuse)
    progress.step("x")
    progress.close()
    progress.close()


def test_a_broken_part_does_not_stop_the_others(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*args: Any) -> None:
        raise RuntimeError("rail exploded")

    monkeypatch.setattr(system, "build_rail", broken)

    def no_compute(self: Any) -> None:
        raise RuntimeError("compute failed")

    monkeypatch.setattr(fusion.Design, "computeAll", no_compute)
    world.active_product = fusion.Design()
    mode, log = system.generate(core.Application.get(), defaults(), system.Progress(None))
    assert mode == "built in this design"
    assert len(log.hard) == 1 and log.hard[0].startswith("Rail:\nTraceback")
    assert "RuntimeError: rail exploded" in log.hard[0]
    assert ("component.name", "Tie Mount") in world.trace


def test_failed_rebuild_falls_back_to_a_new_design(
    world: fake.World, monkeypatch: pytest.MonkeyPatch
) -> None:
    app = core.Application.get()
    world.active_product = fusion.Design()
    system.generate(app, defaults(), system.Progress(None))
    real = system.build_system
    calls = []

    def flaky(ctx: BuildContext, s: Any, progress: Any) -> Any:
        calls.append(ctx.design)
        if len(calls) == 1:
            raise RuntimeError("in-place rebuild failed")
        return real(ctx, s, progress)

    monkeypatch.setattr(system, "build_system", flaky)
    mode, log = system.generate(app, from_mapping({"cradles": 6}), system.Progress(None))
    assert mode == "built in a new design"
    assert log.hard[0].startswith("in-place rebuild failed, built in a new design:\n")
    assert calls[0] is not calls[1]


def test_no_active_design_builds_a_new_one(world: fake.World) -> None:
    world.active_product = None
    mode, _ = system.generate(core.Application.get(), defaults(), system.Progress(None))
    assert mode == "built in a new design"


def test_stored_settings_that_cannot_be_read_force_a_rebuild(world: fake.World) -> None:
    app = core.Application.get()
    d = fusion.Design()
    world.active_product = d
    system.generate(app, defaults(), system.Progress(None))
    d.attributes.add("Liana", "settings", "{broken")
    mode, _ = system.generate(app, defaults(), system.Progress(None))
    assert mode == "rebuilt in this design"


def test_one_parameter_changed_is_singular(world: fake.World) -> None:
    app = core.Application.get()
    world.active_product = fusion.Design()
    system.generate(app, defaults(), system.Progress(None))
    mode, _ = system.generate(app, from_mapping({"tm_l": 40.0}), system.Progress(None))
    assert mode == "updated in place (1 parameter changed)"
