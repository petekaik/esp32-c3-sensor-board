# Fabrication quote sheet — ESP32-C3 sensor carrier, rev2

Upload `esp32-c3-sensor-board-rev2-gerbers.zip` (8 files: 2 copper, 2 mask, 2 silk,
Edge.Cuts, drill). Bare PCB, **5 pieces**, ship to Finland.

## Board parameters (tick these at every vendor)

| Parameter | Value |
|---|---|
| Size | 46 × 89 mm (+2 mm mouse-bites if panelised) |
| Layers | **2** |
| Material / thickness | FR4, **1.6 mm** |
| Copper weight | 1 oz (35 µm) |
| Minimum trace / clearance | **0.15 mm / 0.2 mm** |
| Minimum drill | 0.3 mm (vias 0.7/0.3) |
| Surface finish | **ENIG** preferred (HASL lead-free acceptable) |
| Solder mask | green, both sides |
| Silkscreen | white, both sides |
| Castellations / slots | none |
| Impedance control | not required |
| Panelisation | none — single boards are fine at 5 pcs |

Not needed for bare PCB: paste layers (excluded), assembly, test fixtures.

## What to compare (5 pcs, delivered)

Ask each vendor for the **delivered** total, not the board price:
- board + setup + tooling
- shipping to Finland (post vs courier)
- VAT / import handling
- lead time (working days)

## Vendor quick list

| Vendor | Quote route | Notes |
|---|---|---|
| Aisler (EU) | https://aisler.net — instant quote on upload; **API available** for scripted pricing | EU shipping, no customs surprises |
| Eurocircuits | https://www.eurocircuits.com — online price calculator; API for account holders | EU, more options |
| JLCPCB | https://cart.jlcpcb.com/quote — upload zip, pick 5 pcs | Cheapest board, shipping+VAT usually dominate |
| PCBWay | https://www.pcbway.com/orderonline.aspx | Similar to JLC, better for mixed orders |
| OSHPark | https://oshpark.com — upload zip | US, purple boards, price per area |

## Notes for the order form

- The module sockets, the 1×14 J5 breakout socket, the relay socket and the jumper
  headers are **through-hole**; no paste layers are needed.
- No controlled impedance, no blind/buried vias, no edge plating.
- Mounting holes are plain 3.2 mm NPTH — do not tent them.
- Silkscreen includes small 0.8 mm text; if a vendor flags legibility, allow 0.8 mm minimum.

## Assembly BOM / CPL

Per-provider assembly files are in `fabrication/assembly/` (JLCPCB, PCBWay,
Aisler/generic). They list only the **soldered connectors**; the ESP32-C3
Super Mini, LD2410C, BME280, BH1750 and relay are plug-in modules and are not
assembled. U1 is fitted as **two 1×8 sockets** (`U1A`/`U1B`); U2 is a 1×5
socket. The JLCPCB files are also at `fabrication/bom-jlc.csv` and
`fabrication/cpl-jlc.csv`.

**J3 is excluded** from the assembly files and hand-soldered: the relay socket
has to be raised to meet the KY-019 module's header, which a flush automated
THT placement cannot do. See `fabrication/assembly/hand-solder-j3.md` for the
height, part and procedure.

## After the boards arrive

1. **Bare board:** fit sockets (2× 1×8, 1×6, 1×5, 1×14), terminals, jumper headers. **Assembled order:** the provider fits them, except J3 — skip to step 2.
2. Hand-solder J3 (relay socket) at the height that mates with the relay module; see `fabrication/assembly/hand-solder-j3.md`.
3. Insert the ESP32-C3 Super Mini and modules, flash via USB-C.
4. Set jumpers: JP1 1–2 (I²C), JP2 1–2 (0x76), JP3 1–2 (0x23).
