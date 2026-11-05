# Liana

Liana is an add-in for Autodesk Fusion that generates 3D-printable
under-desk cable holders, an X-frame for turns and branches, and a zip-tie
mount. Every size is a User Parameter, so the design stays editable.

## Quick start

1. Download `Liana-<version>.zip` from the
   [releases page](https://github.com/yeoblyv/liana/releases) and unpack it.
   Inside is a folder named `Liana` (Windows' **Extract All** puts it in a
   folder named after the archive).
2. In Fusion, open **Utilities > Add-Ins > Scripts and Add-Ins**, click
   **+** and choose **Script or add-in from device**, then select the
   `Liana` folder.
3. Select Liana in the list and click **Run**. Tick **Run on Startup** to
   load it every time Fusion starts.
4. Open an empty design and choose **Solid > Create > Liana**. Set the
   number of cables and their diameter, enter your printer bed size and
   click **Generate**.

The [getting started guide](docs/getting-started.md) covers updating and
removing the add-in.

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
changes to the layout rebuild it. See the [user guide](docs/user-guide.md) for
every setting, printing and assembly.

## Hardware

With the default sizes:

| Part      | Hardware                                                              |
|-----------|-----------------------------------------------------------------------|
| Holder    | 2 countersunk wood screws 3.5 mm (4 when side screws are shown), 2 M3 countersunk screws DIN 965 and 2 M3 nuts; the dialog shows the M3 length |
| X-frame   | 4 countersunk wood screws 3.5 mm at the corners; holder screws pass through the frame, so use longer ones there |
| Tie mount | 1 countersunk wood screw 3.5 mm, zip ties up to 4.8 mm wide           |

Print one holder first and check that it suits your table, screws and
cables. Liana is provided as is, under the Apache License 2.0: you print
and mount the parts at your own risk.

## Privacy

Liana collects no data and makes no network connections. It keeps your
last dialog settings and the log of the last build in your user data
folder, and the settings of a system inside the design. Details are in the
[privacy policy](PRIVACY.md); the same text is in the **Privacy policy**
group of the Liana dialog.

## Support

Questions and bug reports: [GitHub issues](https://github.com/yeoblyv/liana/issues)
or support@oblyvantsov.net. Security problems: see [SECURITY.md](SECURITY.md).

## Development

Liana needs only the Python that ships with Fusion. The tests run against an
in-memory stand-in for the Fusion API, on any computer:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt   # Windows: .venv\Scripts\python
.venv/bin/python scripts/check.py                         # every quality gate
.venv/bin/python scripts/build.py                         # dist/Liana-<version>.zip
```

[CONTRIBUTING.md](CONTRIBUTING.md) describes the workflow and
[docs/architecture.md](docs/architecture.md) the code.

## License

Copyright 2026 Yehor Oblyvantsov. Licensed under the
[Apache License, Version 2.0](LICENSE).
