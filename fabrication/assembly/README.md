# Assembly BOM / CPL

The carrier board is **through-hole only**: the provider fits the sockets, headers and terminals, except **J3** (the raised relay socket), which is hand-soldered. The ESP32-C3 Super Mini, LD2410C, BME280, BH1750 and relay are **plug-in modules** and are *not* part of the assembly — insert them after the board arrives.

## What is assembled

| Designator | Part | Qty | LCSC |
|---|---|---|---|
| U1A, U1B | 2.54 mm 1×8 female header | 2 | C27438 |
| U2, J2 | 2.54 mm 1×5 female header | 2 | C50950 |
| J1 | 2.54 mm 1×6 female header | 1 | C40877 |
| J4 | 5.0 mm 2P screw terminal (MX126-5.0-02P) | 1 | C5188434 |
| J5 | 2.54 mm 1×14 female header | 1 | C41417326 |
| JP1, JP2 | 2.54 mm 1×3 male pin header | 2 | C49257 |
| JP3 | 2.54 mm 1×2 male pin header | 1 | C32713268 |
| H1–H4 | 3.2 mm NPTH mounting holes | — | no part |

**J3 is hand-soldered, not assembled.** The relay socket must be raised to meet the KY-019 module's header; automated THT assembly places parts flush. J3 is therefore excluded from every provider BOM/CPL — see [hand-solder-j3.md](hand-solder-j3.md).

**U1 is two 1×8 sockets**, not a 2×8 header: the Super Mini's two pin rows are 15.24 mm apart, so they are fitted as `U1A` and `U1B`. **U2 is a 1×5 socket** for the LD2410C; the module itself is not assembled.

## Provider files

- `jlcpcb/bom-jlcpcb.csv`, `cpl-jlcpcb.csv` — JLCPCB format:
  `Comment,Designator,Footprint,LCSC Part #` and
  `Designator,Mid X,Mid Y,Layer,Rotation`.
  The same JLCPCB files are also at the top level as
  `fabrication/bom-jlc.csv` and `fabrication/cpl-jlc.csv`.
- `pcbway/bom-pcbway.csv`, `cpl-pcbway.csv` — PCBWay format:
  `Designator,Qty,Value,Footprint,MPN,LCSC` and the same CPL columns.
- `aisler/bom-aisler.csv`, `cpl-aisler.csv` — generic / Aisler format:
  `Designator,Qty,Value,Footprint,MPN` and the same CPL columns. Aisler may
  ask for their own template; the part data is the same.

## Notes

- Positions are in mm with the origin at the board's bottom-left corner and Y
  measured up (KiCad position-file convention). The board is 46 × 89 mm.
- U1A/U1B and U2 are placed from the **pad-1 origins** of the standard 1×8 /
  1×5 sockets, not from the custom module footprints. Check the provider's
  placement preview. U2 (90°) and J4 (−90°) may need a provider-specific
  rotation offset; JLCPCB applies its own corrections for some parts.
- The LCSC parts are JLCPCB **extended** parts, so an assembly setup fee may
  apply. Stock was checked on 2026-10-31; re-check at order time.
- The modules are not in JLCPCB's assembly library. Source them separately and
  plug them into the sockets after assembly.
