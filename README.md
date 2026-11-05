# Liana

Liana is an add-in for Autodesk Fusion that generates 3D-printable
under-desk cable holders, an X-frame for turns and branches, and a zip-tie
mount. Every size is a User Parameter, so the design stays editable.

## Quickstart

```bash
git clone https://github.com/yeoblyv/liana.git
cd liana
python scripts/build.py
```

Then, in Fusion:

1. Unpack `dist/Liana-<version>.zip` (or a release archive from the
   [releases page](https://github.com/yeoblyv/liana/releases)).
2. Open **Utilities > Add-Ins > Scripts and Add-Ins**, click **+**, choose
   **Script or add-in from device** and select the `Liana` folder inside
   the archive.
3. Switch **Run** on and tick **Run on Startup**.
4. In an empty design choose **Solid > Create > Liana**, set the cables
   and your printer bed, and click **Generate**.

[Installation](docs/getting-started/installation.md) covers checking the
download, updating and removing the add-in.

## What it builds

- **Holder.** A rail screwed under the table and a comb with one cradle per
  cable. The comb slides into the rail from the side and is pulled tight
  with two M3 screws. 1 to 15 cradles, cables 3 to 25 mm in diameter.
- **X-frame.** One square frame for straight runs, L-turns, T-branches and
  crossings: screw a holder to each side you need.
- **Tie mount.** A small pad with two zip-tie tunnels and one screw.

The dialog checks every part against your printer bed and keeps
**Generate** off until everything fits. Running Liana again on the same
design edits the system: size changes update the parameters in place,
changes to the layout rebuild it.

| Topic | Page |
|---|---|
| Every setting | [Dialog settings](docs/guides/dialog-settings.md) |
| Changing a design | [Editing a system](docs/guides/editing-a-system.md) |
| From the design to the desk | [Printing and assembly](docs/guides/printing-and-assembly.md) |
| All documentation | [docs/](docs/README.md) |

## Hardware

With the default sizes:

| Part | Hardware |
|---|---|
| Holder | 2 countersunk wood screws 3.5 mm (4 when side screws are shown), 2 M3 countersunk screws DIN 965 and 2 M3 nuts; the dialog shows the M3 length |
| X-frame | 4 countersunk wood screws 3.5 mm at the corners; holder screws pass through the frame, so use longer ones there |
| Tie mount | 1 countersunk wood screw 3.5 mm, zip ties up to 4.8 mm wide |

Print one holder first and check that it suits your table, screws and
cables. Liana is provided as is, under the Apache License 2.0: you print
and mount the parts at your own risk.

## Privacy

Liana collects no data and makes no network connections. It keeps your
last dialog settings and the log of the last build in its own add-in
folder, so uninstalling removes them, and the settings of a system inside
the design. Details are in the
[privacy policy](PRIVACY.md); the same text is in the **Privacy policy**
group of the Liana dialog.

## Support

Questions and bug reports: [GitHub issues](https://github.com/yeoblyv/liana/issues)
or support@oblyvantsov.net. Security problems: see [SECURITY.md](SECURITY.md).

## Development

The tests run against an in-memory stand-in for the Fusion API, on any
computer with Python 3.12 or newer:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check.py
```

On Windows use `.venv\Scripts\python`. The
[workflow](docs/contributing/workflow.md) lists the gates, and the
[architecture overview](docs/architecture/overview.md) describes the code.

## License

Copyright 2026 Yehor Oblyvantsov. Licensed under the
[Apache License, Version 2.0](LICENSE).
