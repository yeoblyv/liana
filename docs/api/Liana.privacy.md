---
id: api.liana.privacy
title: Liana.privacy
slug: /api/Liana.privacy
category: API
since: 1.0.0
status: stable
---

[Docs](../README.md) / [API](README.md) / `Liana.privacy`

# `Liana.privacy`

![status](https://img.shields.io/badge/status-stable-2ea44f)
![since](https://img.shields.io/badge/since-1.0.0-5b4fe0)

The privacy policy, shipped inside the add-in and shown from the dialog.

Autodesk asks for the policy text inside the app, not only a link to it.
`POLICY_MARKDOWN` is a copy of `PRIVACY.md` at the repository root;
a test keeps the two identical.

## On this page

- [Constants](#constants)
  - [`POLICY_URL`](#liana-privacy-const-policy-url)
  - [`POLICY_TITLE`](#liana-privacy-const-policy-title)
  - [`POLICY_MARKDOWN`](#liana-privacy-const-policy-markdown)
- [Functions](#functions)
  - [`policy_text`](#liana-privacy-policy-text)
  - [`policy_html`](#liana-privacy-policy-html)
- [See also](#see-also)
- [Changelog](#changelog)

## Constants

### `POLICY_URL` {#liana-privacy-const-policy-url}

Online version of the policy.

**Since** 1.0.0

### `POLICY_TITLE` {#liana-privacy-const-policy-title}

Title of the dialog group that shows the policy.

**Since** 1.0.0

### `POLICY_MARKDOWN` {#liana-privacy-const-policy-markdown}

The policy as written in `PRIVACY.md`.

**Since** 1.0.0

## Functions

### `policy_text() -> str` {#liana-privacy-policy-text}

Return the policy as plain text.

**Returns** `str`  
**Since** 1.0.0

### `policy_html() -> str` {#liana-privacy-policy-html}

Return the policy as text-box HTML, with the headings in bold.

**Returns** `str`  
**Since** 1.0.0

## See also

- [Architecture](../architecture/overview.md): how the modules work together.

## Changelog

- 1.0.0: first release.
