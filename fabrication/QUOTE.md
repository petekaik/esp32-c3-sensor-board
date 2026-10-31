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

- The relay socket and jumper headers are **through-hole**; no paste layers are needed.
- No controlled impedance, no blind/buried vias, no edge plating.
- Mounting holes are plain 3.2 mm NPTH — do not tent them.
- Silkscreen includes small 0.8 mm text; if a vendor flags legibility, allow 0.8 mm minimum.

## After the boards arrive

1. Fit sockets (2× 1×8, 1×6, 2× 1×5, 1×3 horizontal), terminals, jumper headers.
2. Insert the ESP32-C3 Super Mini and modules, flash via USB-C.
3. Set jumpers: JP1 1–2 (I²C), JP2 1–2 (0x76), JP3 1–2 (0x23).
