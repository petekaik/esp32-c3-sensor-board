# Variant: compact, no relay, BME280 (routed)

**Status:** routed — `hardware/esp32-c3-sensor-board-compact.*`
**Board:** 34 × 76 mm, R3, 2-layer (12 mm narrower, 13 mm shorter than rev2)

## What changes
- **J3, the relay module area and J4 (button terminal) removed.**
- Board is a **34 × 76 mm** stacked column: radar, BH1750 and BME280 one below
  the other, with J5 on the right. It is 12 mm narrower than rev2.
- **GPIO3 and GPIO4 freed** and added to the breakout row → **J5 is 1×16**:
  `3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO3 · GPIO4 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`
- Jumpers JP1/JP2/JP3 unchanged with defaults 1–2 (I²C, 0x76, 0x23).

## BOM
[`../BOM.csv`](../BOM.csv) minus the J3 socket, the J4 terminal and the KY-019 relay module;
J5 becomes the 1×16 socket (LCSC C7499334).

## Layout
| Item | Position (mm, origin top-left) |
|---|---|
| ESP32-C3 socket | U1A (24.62, 2.31), U1B (9.38, 2.31), USB out the top short edge |
| LD2410C | (17, 33), landscape |
| BH1750 | J2 at (24.79, 44.92), rot 0 — body landscape, socket row vertical |
| BME280 | J1 at (25, 60.55), rot 0 — body portrait, socket row vertical |
| Jumper headers | (5 / 8.6 / 12.2, 60) |
| Breakout row J5 | x 31, y 24 … 64.64 (16 socket positions) |
| Button terminal | removed (GPIO3 on J5 pin 7) |
| Mounting holes | H1–H4 at (3,3), (31,3), (3,73), (31,73) |

BH1750 and BME280 are rotated 90° from the old compact layout: the BH module
body is landscape and aligned with the radar, and the BME module is portrait
below it. J5 sits in the right-hand strip. The 34 mm width leaves no room for
16 on-board pin labels; the breakout pinout is in
[`../pinout.md`](../pinout.md) and the J5 reference is on the silkscreen.

## Firmware
Same as [relay-bme280](relay-bme280.md) but **remove the `switch: chime` block** and the
J4 button configuration; GPIO3 and GPIO4 are now free I/O on the breakout row (pins 7 and 8).

## Verification
- ERC: 0 violations.
- DRC: **0 violations, 0 errors**. KiCad reports 3 GND-zone connectivity notices
  between pour islands; no pads or signal tracks are unconnected, and the GND
  net is continuous through the through-hole pads and stitching vias.
- Schematic parity: only the 4 pre-existing H1–H4 BOM-attribute notices.
- Gerbers/drill/zip: `fabrication/esp32-c3-sensor-board-compact-gerbers.zip`.

## Case
- Fusion document **Sensorbox Compact v1** (Modules project); print files
  `case/compact_tray.stl` and `case/compact_cover.stl`.
- 41 × 84 × 24 mm envelope with a 3.5 mm perimeter margin and **no wiring
  channel**; the J5 breakout exits through the right-hand slot.
- Openings: USB-C, J5 side slot, 3 radar vents, BH1750 11 × 11 window, 5 BME280
  louvres and 3 ESP32 side vents. Internal cover walls at y −42.6 and −24.4
  keep the radar pocket separate from the BH/BME side.
- Two wall-mount keyholes in the back; four M3 standoffs for the PCB; the cover
  is a press-fit lid. See [`case/README.md`](../../case/README.md).
- Optional decorative stone faceplate **`case/faceplate_compact.stl`** —
  39.5 × 82.5 × 3.9 mm, sitting on the cover top (z 20.5), with the same
  openings and a raised BH1750 “eye”. The stone surface is sampled from the
  CC0 Poly Haven *Rustic Stone Wall 02* displacement map; previews are in
  `case/renders/`. The Blender scene is `case/compact_faceplate.blend` and the
  generator is [`tools/blender/make_compact_faceplate.py`](../../tools/blender/make_compact_faceplate.py).

## Open questions
- Optional decorative faceplate overlay in Blender; the base cover is already
  printable without it.
- Does the enclosure still need the wiring-side depth, or can it become a slimmer wall box?
