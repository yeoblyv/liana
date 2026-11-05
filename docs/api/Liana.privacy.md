# `Liana.privacy`

The privacy policy, shipped inside the add-in and shown from the dialog.

Autodesk asks for the policy text inside the app, not only a link to it.
:data:`POLICY_MARKDOWN` is a copy of ``PRIVACY.md`` at the repository root;
a test keeps the two identical.

## Constants

### `POLICY_URL`

Online version of the policy.

### `POLICY_TITLE`

Title of the policy window.

### `POLICY_MARKDOWN`

The policy as written in ``PRIVACY.md``.

## Functions

### `policy_text() -> str`

```text
Return the policy as plain text for a message box.

Heading marks are removed and the lines of each paragraph or list item
are joined, so the window wraps the text to its own width.
```
