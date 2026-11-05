# `Liana.privacy`

The privacy policy, shipped inside the add-in and shown from the dialog.

Autodesk asks for the policy text inside the app, not only a link to it.
:data:`POLICY_MARKDOWN` is a copy of ``PRIVACY.md`` at the repository root;
a test keeps the two identical.

## Constants

### `POLICY_URL`

Online version of the policy.

### `POLICY_TITLE`

Title of the dialog group that shows the policy.

### `POLICY_MARKDOWN`

The policy as written in ``PRIVACY.md``.

## Functions

### `policy_text() -> str`

```text
Return the policy as plain text.
```

### `policy_html() -> str`

```text
Return the policy as text-box HTML, with the headings in bold.
```
