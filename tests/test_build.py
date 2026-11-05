# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""The Marketplace bundle description written by ``scripts/build.py``."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build  # noqa: E402
from _project import ADDIN, MANIFEST  # noqa: E402

from Liana.addin import HELP_FILE  # noqa: E402


def test_package_contents_describes_the_bundle() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    root = ET.fromstring(build.package_contents(manifest, "1.2.3"))
    assert root.tag == "ApplicationPackage"
    assert root.get("AutodeskProduct") == "Fusion360"
    assert root.get("AppVersion") == "1.2.3"
    assert root.get("ProductCode") == "{%s}" % manifest["id"].upper()
    help_file = root.get("HelpFile", "")
    assert help_file == "./Contents/" + HELP_FILE.relative_to(ADDIN).as_posix()
    company = root.find("CompanyDetails")
    assert company is not None and company.get("Email") == "support@oblyvantsov.net"
    requirements = root.find("Components/RuntimeRequirements")
    assert requirements is not None and requirements.get("OS") == "Win64|MacOS"
    entry = root.find("Components/ComponentEntry")
    assert entry is not None
    assert entry.get("ModuleName") == "./Contents/Liana.manifest"
    assert entry.get("Version") == "1.2.3"


def test_package_contents_escapes_text() -> None:
    manifest = {
        "id": "x",
        "author": 'A & "B"',
        "description": {"": "<tags>"},
        "supportedOS": "windows",
    }
    root = ET.fromstring(build.package_contents(manifest, "1.0.0"))
    assert root.get("Author") == 'A & "B"' and root.get("Description") == "<tags>"
    requirements = root.find("Components/RuntimeRequirements")
    assert requirements is not None and requirements.get("OS") == "Win64"
