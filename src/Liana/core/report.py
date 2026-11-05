# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""Texts shown to the user: dialog summary, build log and result message."""

from __future__ import annotations

from dataclasses import dataclass, field

from .layout import fit_report, layout
from .settings import Settings

SHORT_BITE_MM = 10.0
"""Wood screw engagement below which the summary suggests longer screws."""


@dataclass
class BuildLog:
    """What went wrong during one build, grouped by severity.

    Attributes:
        hard: Parts that could not be finished, with a short traceback.
        soft: Finishing features (fillets, chamfers, colors) that were skipped.
        dims: Sketch dimensions Fusion refused.
        aligned: Coordinates tied to an earlier point with the same expression.
    """

    hard: list[str] = field(default_factory=list)
    soft: list[str] = field(default_factory=list)
    dims: list[str] = field(default_factory=list)
    aligned: list[str] = field(default_factory=list)

    def clear(self) -> None:
        """Forget everything recorded so far."""
        self.hard.clear()
        self.soft.clear()
        self.dims.clear()
        self.aligned.clear()

    @property
    def has_problems(self) -> bool:
        """Whether anything was skipped or failed."""
        return bool(self.hard or self.soft or self.dims)


def summary_html(s: Settings, problems: list[str], editing: bool) -> str:
    """Return the dialog summary as Fusion text-box HTML.

    Args:
        s: Settings shown in the dialog.
        problems: Output of :func:`.settings.problems`.
        editing: Whether the dialog edits a system already in the design.

    Returns:
        Lines joined with ``<br>``.
    """
    lay = layout(s)
    fit = fit_report(s)
    lines = []
    if editing and not s["new_design"]:
        lines.append("<b>Editing the system in this design.</b>")
    lines.append(
        "<b>%d cradle%s</b> for %.1f mm cables, pitch %.1f mm"
        % (lay.n, "" if lay.n == 1 else "s", s["cable_d"], lay.p)
    )
    if lay.pin:
        pin = "T-pin at the %s" % ("center" if lay.pin_x == 0 else "tooth next to the center")
    else:
        pin = "no T-pin"
    lines.append(", ".join([pin, "4 table screws" if lay.side else "2 table screws"]))
    lines.extend(fit.lines)
    lines.append("Max cradles for this bed: <b>%d</b>" % fit.max_cradles)
    bom = []
    if s["make_holder"]:
        bom.append(
            "holder: %d x wood screw %gx%g, 2 x M3x%s DIN 965 + 2 nuts"
            % (
                4 if lay.side else 2,
                s["screw_d"] - 0.7,
                s["screw_len"],
                lay.m3_len if lay.m3_len else "?",
            )
        )
    if s["make_frame"]:
        bom.append("frame: 4 corner screws")
    if s["make_tie"]:
        bom.append("tie mount: 1 screw")
    if bom:
        lines.append("Hardware - " + "; ".join(bom))
    if s["make_holder"]:
        bite = "Screw in the wood: %.1f mm (holder)" % lay.bite_holder
        shortest = lay.bite_holder
        if s["make_frame"]:
            bite += ", %.1f mm (holder on frame)" % lay.bite_frame
            shortest = min(shortest, lay.bite_frame)
        if shortest < SHORT_BITE_MM:
            bite += " - use longer screws"
        lines.append(bite)
    if s["raised_teeth"] and s["tooth_w"] < 0.15 * s["cable_d"]:
        lines.append(
            "Note: teeth are thin for %.0f mm cables - consider %.1f mm or more"
            % (s["cable_d"], 0.15 * s["cable_d"])
        )
    for p in problems:
        lines.append("<b>! %s</b>" % p)
    return "<br>".join(lines)


def log_text(mode: str, s: Settings, log: BuildLog) -> str:
    """Return the build log written after every build.

    Args:
        mode: How the system was built, e.g. ``"built in this design"``.
        s: Settings of the build.
        log: Problems recorded during the build.

    Returns:
        Plain text ending with a newline.
    """
    lay = layout(s)
    report = [
        "Liana build log",
        "mode: %s" % mode,
        "cradles=%d cable=%.1f pitch=%.1f pin=%s side_screws=%s"
        % (lay.n, s["cable_d"], lay.p, lay.pin, lay.side),
        "",
        "ERRORS (part not finished): %d" % len(log.hard),
        *log.hard,
        "",
        "Skipped features (fillets / chamfers etc.): %d" % len(log.soft),
        *log.soft,
        "",
        "Skipped sketch dimensions: %d" % len(log.dims),
        *log.dims,
        "",
        "Coordinates aligned to a point with the same expression (explicit constraint): %d"
        % len(log.aligned),
        *log.aligned,
    ]
    return "\n".join(report) + "\n"


def result_message(mode: str, log: BuildLog, log_path: str) -> str:
    """Return the message shown when a build finishes.

    Args:
        mode: How the system was built.
        log: Problems recorded during the build.
        log_path: Where the full build log was written, or ``""`` if it could
            not be written.

    Returns:
        Plain text for a message box.
    """
    msg = "Liana: system %s." % mode
    if log.has_problems:
        msg += (
            "\n\nParts not finished: %d\nSkipped features: %d\nSkipped sketch dimensions: %d"
            % (
                len(log.hard),
                len(log.soft),
                len(log.dims),
            )
        )
        if log.hard:
            msg += "\n\n" + log.hard[0].strip().split("\n")[-1]
        if log_path:
            msg += "\n\nLog: " + log_path
    msg += (
        "\n\nSizes stay editable in Modify > Change Parameters;"
        " run Liana again to change the cradle count or layout."
    )
    return msg
