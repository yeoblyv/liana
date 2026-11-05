# Security policy

## Supported versions

Only the latest release receives fixes.

| Version | Supported |
|---------|-----------|
| 1.0.x   | yes       |

## What Liana does

Liana runs inside Autodesk Fusion with the rights of the Fusion user. It
makes no network connections and loads no code from outside its own folder.
It reads three kinds of input:

- the values typed into its dialog;
- its own settings file in the user data folder;
- the settings stored in a design, which may come from someone else.

The last two are parsed as JSON and every value is checked against the type
of its default before use; unknown keys are dropped.

## Reporting a vulnerability

Please report security problems privately, not in a public issue:

- through GitHub: **Security > Report a vulnerability** on
  https://github.com/yeoblyv/liana, or
- by email to xineraman8@gmail.com.

Include the Liana version (shown in the dialog), the Fusion version, your
operating system and the steps to reproduce. Please allow time for a fix
before disclosing the problem publicly.
