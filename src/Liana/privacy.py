# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yehor Oblyvantsov
"""The privacy policy, shipped inside the add-in and shown from the dialog.

Autodesk asks for the policy text inside the app, not only a link to it.
:data:`POLICY_MARKDOWN` is a copy of ``PRIVACY.md`` at the repository root;
a test keeps the two identical.
"""

from __future__ import annotations

import html

POLICY_URL = "https://github.com/yeoblyv/liana/blob/main/PRIVACY.md"
"""Online version of the policy."""

POLICY_TITLE = "Privacy policy"
"""Title of the dialog group that shows the policy."""

POLICY_MARKDOWN = r"""# Liana privacy policy

Last updated: 5 November 2026.

Liana is an add-in for Autodesk Fusion published by Yehor Oblyvantsov,
Groningen, the Netherlands. Contact: support@oblyvantsov.net.

The same text is in Liana itself: open the Liana dialog and expand
Privacy policy.

## 1. What data Liana collects and how it is used

Liana does not collect personal data. It contains no analytics, tracking or
advertising, makes no network connections, and sends nothing to the
publisher or to anyone else.

To work, Liana stores three things on your own computer and in your own
designs:

- Last dialog settings. Written when you click Generate, to the file
  last_settings.json in your user data folder. They hold only the numbers
  and switches of the dialog and are used to open the dialog with your last
  values.
- Build log. Written after every build, to the file build_log.txt in the
  same folder. It is used for troubleshooting and lists the features that
  were skipped and, if a part failed, the error message. Error messages can
  contain folder names on your computer, such as your user name in a path.
  The log stays on your computer unless you choose to send it to someone.
- System settings in the design. When Liana builds a system, the dialog
  values are saved inside that Fusion design, so that running Liana again
  can edit the system. They travel with the design wherever you save or
  share it; how Autodesk stores designs is covered by Autodesk's own terms
  and privacy statement.

The user data folder is %APPDATA%\Liana on Windows and
~/Library/Application Support/Liana on macOS.

## 2. Third parties

Liana shares no data with any third party: no analytics tools, advertising
networks, third-party SDKs, or companies related to the publisher. It
contains no third-party code.

If this ever changes, this policy will be updated before the change is
released, and any third party that receives data will be required to
protect it at least as well as this policy does.

## 3. Retention and deletion

The publisher holds no data from Liana, so there is nothing to retain or
delete on the publisher's side.

On your computer, each Generate replaces the previous settings file and
each build replaces the previous log. Both files stay until you delete
them; uninstalling Liana does not remove them. The values saved in a design
stay part of that design until you delete it.

## 4. Revoking consent and deleting your data

All data stays under your control:

- To stop Liana from storing anything, stop using it and uninstall it.
- To delete the stored files, delete the folder Liana in your user data
  folder (see section 1). Liana works normally afterwards and starts from
  its default settings.
- To delete the values saved in a design, delete the design.

If you write to support@oblyvantsov.net, your message and address are used
only to answer you. They are deleted on request; write to the same address
to ask for that. Issues opened on GitHub are public and are covered by
GitHub's privacy statement.

## Online version

This policy is published at
https://github.com/yeoblyv/liana/blob/main/PRIVACY.md. The Open online
version button under Privacy policy in the Liana dialog opens that page in
your web browser; GitHub's privacy statement applies to that visit.

## Changes

A new version of this policy appears at the address above with a new date,
and in the next release of Liana.
"""
"""The policy as written in ``PRIVACY.md``."""


def _blocks() -> list[tuple[bool, str]]:
    """Split the policy into ``(is_heading, text)`` blocks.

    Heading marks are removed and the lines of each paragraph or list item
    are joined, so the text wraps to the width of wherever it is shown.
    """
    blocks: list[tuple[bool, str]] = []
    for block in POLICY_MARKDOWN.strip().split("\n\n"):
        lines = [line.strip() for line in block.splitlines()]
        if lines[0].startswith("#"):
            blocks.append((True, " ".join(lines).lstrip("#").strip()))
            continue
        items: list[str] = []
        for line in lines:
            if line.startswith("- ") or not items:
                items.append(line)
            else:
                items[-1] += " " + line
        blocks.append((False, "\n".join(items)))
    return blocks


def policy_text() -> str:
    """Return the policy as plain text."""
    return "\n\n".join(text for _, text in _blocks())


def policy_html() -> str:
    """Return the policy as text-box HTML, with the headings in bold."""
    parts = []
    for heading, text in _blocks():
        escaped = html.escape(text, quote=False).replace("\n", "<br>")
        parts.append("<b>%s</b>" % escaped if heading else escaped)
    return "<br><br>".join(parts)
