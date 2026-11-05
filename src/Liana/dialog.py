# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""The Liana dialog: inputs, their mapping to settings and the live summary."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Literal, NamedTuple, cast

import adsk.core

from ._version import __version__
from .cad.api import API_ERRORS, MM
from .core.layout import fit_report
from .core.report import summary_html
from .core.settings import DEFAULTS, LIMITS, MOUNTS, Mount, Settings, from_mapping, problems
from .privacy import POLICY_TITLE, POLICY_URL, policy_html

FieldKind = Literal["int", "mm", "bool", "mount"]
"""How a setting is shown: spinner, length, check box or the mount list."""

RESET_ID = "reset"
"""Input id of the reset button."""

PRIVACY_ID = "privacy"
"""Input id of the button that opens the online privacy policy."""

PRIVACY_GROUP_ID = "g_privacy"
"""Input id of the collapsed group with the privacy policy text."""

POLICY_TEXT_ID = "policy_text"
"""Input id of the text box with the privacy policy."""

SUMMARY_ID = "summary"
"""Input id of the summary text box."""

DIALOG_SIZE = (430, 820)
"""Initial dialog width and height in pixels."""


class Field(NamedTuple):
    """One dialog input.

    Attributes:
        key: Settings key, also the input id.
        label: Label shown left of the input.
        kind: Input type.
        tooltip: Tooltip, empty for none.
    """

    key: str
    label: str
    kind: FieldKind
    tooltip: str = ""


class Group(NamedTuple):
    """A collapsible group of inputs.

    Attributes:
        id: Input id of the group.
        label: Group title.
        expanded: Whether the group starts expanded.
        fields: Inputs of the group.
    """

    id: str
    label: str
    expanded: bool
    fields: tuple[Field, ...]


GROUPS: tuple[Group, ...] = (
    Group(
        "g_cables",
        "Cables",
        True,
        (
            Field(
                "cradles",
                "Cradles per holder",
                "int",
                "Number of cable cradles in one holder (1-15).",
            ),
            Field(
                "cable_d",
                "Cable diameter",
                "mm",
                "Cradle diameter. The pitch is cable diameter + tooth width.",
            ),
            Field("tooth_w", "Tooth width", "mm", "Width of the teeth between the cradles."),
            Field(
                "raised_teeth",
                "Raised teeth (U-cradles)",
                "bool",
                "Teeth reach the top of the cable so cables cannot wander into the next cradle.",
            ),
            Field(
                "center_pin",
                "Center T-pin (4+ cradles)",
                "bool",
                "Supports the middle of the comb against sagging."
                " Side screws are added when there is room.",
            ),
        ),
    ),
    Group(
        "g_parts",
        "Parts",
        True,
        (
            Field("make_holder", "Holder (rail + comb)", "bool"),
            Field(
                "make_frame",
                "X-frame",
                "bool",
                "One frame for straight runs, turns, branches and crossings:"
                " screw holders to the sides you need.",
            ),
            Field(
                "make_tie", "Tie mount", "bool", "Small pad with two zip-tie tunnels, one screw."
            ),
            Field(
                "mount",
                "Show holders on the frame",
                "mount",
                "Only for the preview in the design: which frame sides get a holder.",
            ),
            Field(
                "new_design",
                "Build in a new design",
                "bool",
                "Leave the current design untouched and build in a new one.",
            ),
        ),
    ),
    Group(
        "g_holder",
        "Holder",
        False,
        (
            Field("depth", "Depth (along the cable)", "mm"),
            Field(
                "screw_d",
                "Wood screw hole",
                "mm",
                "Clearance hole for the wood screw (4.2 for 3.5 mm screws).",
            ),
            Field(
                "screw_csk",
                "Wood screw countersink",
                "mm",
                "Countersink diameter at the surface (8.4 for a 7 mm head).",
            ),
            Field(
                "screw_len",
                "Wood screw length",
                "mm",
                "Only used for the summary: how deep the screw bites into the table.",
            ),
            Field("m3_d", "M3 hole", "mm"),
            Field(
                "nut_af",
                "M3 nut seat (across flats)",
                "mm",
                "Hex seat for the M3 nut: 5.5 mm nut + ~0.5 mm, so it slides in by hand.",
            ),
            Field(
                "clr",
                "Pin / slot clearance",
                "mm",
                "Side clearance of the T-pin in the slot, per side.",
            ),
        ),
    ),
    Group(
        "g_frame",
        "X-frame",
        False,
        (Field("frame_t", "Thickness", "mm"), Field("beam_w", "Beam width", "mm")),
    ),
    Group(
        "g_tie",
        "Tie mount",
        False,
        (
            Field("tm_l", "Length", "mm"),
            Field("tm_w", "Width", "mm"),
            Field("tm_h", "Height", "mm"),
            Field(
                "tie_w", "Tie tunnel width", "mm", "Fits zip ties up to this width minus ~0.4 mm."
            ),
        ),
    ),
    Group(
        "g_bed",
        "Printer bed",
        True,
        (
            Field("bed_x", "Bed X", "mm"),
            Field("bed_y", "Bed Y", "mm"),
            Field("margin", "Margin from the edge", "mm"),
        ),
    ),
)
"""Dialog layout, top to bottom."""

KINDS: dict[str, FieldKind] = {f.key: f.kind for g in GROUPS for f in g.fields}
"""Input type of every settings key shown in the dialog."""


def mount_label(key: Mount) -> str:
    """Return the dialog label of a mount option.

    Args:
        key: Mount option.
    """
    return next(label for k, label, _ in MOUNTS if k == key)


def mount_key(label: str | None) -> Mount:
    """Return the mount option for a dialog label (``"none"`` if unknown).

    Args:
        label: Dialog label, or None when nothing is selected.
    """
    return next((k for k, lbl, _ in MOUNTS if label is not None and lbl == label), "none")


class SettingsDialog:
    """The inputs of one open dialog.

    Attributes:
        editing: Whether the dialog edits a system already in the design.
    """

    def __init__(self, editing: bool, open_url: Callable[[str], None]) -> None:
        """Prepare a dialog; inputs are created by :meth:`build`.

        Args:
            editing: Whether the dialog edits a system already in the design.
            open_url: Opens a web page in the browser.
        """
        self.editing = editing
        self._open_url = open_url
        self._inputs: dict[str, Any] = {}
        self._summary: Any = None

    def build(self, inputs: Any, s: Settings) -> None:
        """Create every input of the dialog, filled from the settings.

        Args:
            inputs: ``CommandInputs`` of the command.
            s: Initial values.
        """
        self._inputs.clear()
        for group in GROUPS:
            g = inputs.addGroupCommandInput(group.id, group.label)
            g.isExpanded = group.expanded
            children = g.children
            for f in group.fields:
                self._inputs[f.key] = self._add_field(children, f, s)
        # the policy text sits in the dialog itself, collapsed above the
        # summary so its header is visible without scrolling
        group = inputs.addGroupCommandInput(PRIVACY_GROUP_ID, POLICY_TITLE)
        group.isExpanded = False
        policy = group.children.addTextBoxCommandInput(POLICY_TEXT_ID, "", policy_html(), 12, True)
        _full_width(policy)
        online = group.children.addBoolValueInput(
            PRIVACY_ID, "Liana " + __version__, False, "", False
        )
        _set_text(online, "Open online version")
        reset = inputs.addBoolValueInput(RESET_ID, "Reset to defaults", False, "", False)
        _set_text(reset, "Reset to defaults")
        self._summary = inputs.addTextBoxCommandInput(SUMMARY_ID, "", "", 14, True)
        _full_width(self._summary)

    @staticmethod
    def _add_field(children: Any, f: Field, s: Settings) -> Any:
        current = cast(Mapping[str, Any], s)[f.key]
        if f.kind == "int":
            lo, hi = LIMITS[f.key]
            inp = children.addIntegerSpinnerCommandInput(
                f.key, f.label, int(lo), int(hi), 1, int(current)
            )
        elif f.kind == "mm":
            inp = children.addValueInput(
                f.key, f.label, "mm", adsk.core.ValueInput.createByReal(float(current) * MM)
            )
        elif f.kind == "bool":
            inp = children.addBoolValueInput(f.key, f.label, True, "", bool(current))
        else:
            inp = children.addDropDownCommandInput(
                f.key, f.label, adsk.core.DropDownStyles.TextListDropDownStyle
            )
            for key, label, _ in MOUNTS:
                inp.listItems.add(label, key == current, "")
        if f.tooltip:
            try:
                inp.tooltip = f.tooltip
            except API_ERRORS:
                pass  # tooltips are cosmetic
        return inp

    def read(self) -> Settings:
        """Return the settings currently shown in the dialog."""
        values: dict[str, object] = {}
        for key, kind in KINDS.items():
            inp = self._inputs.get(key)
            if inp is None:
                continue
            if kind == "int":
                values[key] = int(inp.value)
            elif kind == "mm":
                values[key] = round(inp.value / MM, 4)
            elif kind == "bool":
                values[key] = bool(inp.value)
            else:
                selected = inp.selectedItem
                values[key] = mount_key(selected.name if selected is not None else None)
        return from_mapping(values)

    def write(self, s: Settings) -> None:
        """Show the given settings in the dialog.

        Args:
            s: Settings to show.
        """
        values = cast(Mapping[str, Any], s)
        for key, kind in KINDS.items():
            inp = self._inputs.get(key)
            if inp is None:
                continue
            # A box the user typed letters into keeps its text: Fusion keeps
            # such a box invalid until the user edits it, so overwriting the
            # text would show a valid number while Generate stays off.
            if kind == "int":
                inp.value = int(values[key])
            elif kind == "mm":
                inp.value = float(values[key]) * MM
            elif kind == "bool":
                inp.value = bool(values[key])
            else:
                wanted = mount_label(s["mount"])
                for i in range(inp.listItems.count):
                    item = inp.listItems.item(i)
                    item.isSelected = item.name == wanted

    def problems(self, s: Settings) -> list[str]:
        """Return what prevents building the settings.

        Args:
            s: Settings to check.
        """
        return problems(s, fit_report(s).ok)

    def refresh(self, s: Settings | None = None) -> bool:
        """Update enabled inputs and the summary.

        Args:
            s: Settings to show; read from the inputs when omitted.

        Returns:
            Whether the settings can be built.
        """
        if s is None:
            s = self.read()
        found = self.problems(s)
        try:
            self._inputs["center_pin"].isEnabled = s["cradles"] >= 4
            self._inputs["mount"].isEnabled = s["make_frame"] and s["make_holder"]
        except API_ERRORS:
            pass  # enabling is a hint only; the build ignores disabled options
        self._summary.formattedText = summary_html(s, found, self.editing)
        return not found

    def inputs_valid(self) -> bool:
        """Return whether every length is a valid expression and the settings build."""
        for key, kind in KINDS.items():
            if kind == "mm" and not self._inputs[key].isValidExpression:
                return False
        return not self.problems(self.read())

    def input_changed(self, input_id: str) -> None:
        """React to a changed input: buttons act, then the summary is refreshed.

        Args:
            input_id: Id of the input that changed.
        """
        if input_id == RESET_ID:
            self.write(DEFAULTS)
        elif input_id == PRIVACY_ID:
            self._open_url(POLICY_URL)
        self.refresh()


def _full_width(text_box: Any) -> None:
    try:
        text_box.isFullWidth = True
    except API_ERRORS:
        pass  # older Fusion: the text keeps a label column


def _set_text(button: Any, text: str) -> None:
    try:
        button.text = text
    except API_ERRORS:
        pass  # older Fusion shows the label only
