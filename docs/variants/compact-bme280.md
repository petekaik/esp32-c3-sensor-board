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
- Fusion document **Sensorbox Compact v18** (Modules project); print files
  `case/compact_tray.stl` and `case/compact_cover.stl`.
- **41 × 84 × 22.5 mm** envelope (roof lowered 1.5 mm to z 19.0; the ESP32
  USB shell at 16.6 mm is the limiting part). The interior is sized to the
  PCB: 0.5 mm clearance left/right/bottom and the USB edge flush with the top
  inner wall, with the USB notch cut through the 4 mm wall. J5 is fully
  enclosed (no side slot) and both long walls carry the same 36-hole vent
  pattern. No wiring channel.
- Openings: USB-C stadium at x 17 centred on the connector with a chamfered
  mouth; 22 × Ø1.6 radar holes; Ø5 BH1750 sight hole with an
  underside counterbore; 18 × Ø1.2 BME280 holes; the same 36 × Ø1.6 side vents on both
  long walls. Full-height cover walls at y −24.4, −42.85 and −58.6 split the ESP32,
  radar, BH1750 and BME280 into separate segments (0.5 mm above the PCB,
  stopping at x 28.5 to clear the J5 socket).
- One wall-mount keyhole in a separate Ø28 × 5 mm `MOUNT` pod glued to the
  base back; the base floor seals the screw cavity from the PCB. Four
  **M3×0.5 threaded poles** on
  the lid. The USB-C cutout is built from the actual port: 9.6 × 4.0 mm,
  9.6 mm wide with r0.5 bottom corners and full width at the top, centred at
  (x 17, z 15.05), continuing through the lid lip. The 10.8 × 4.6 mm
  r1.2 outer recess is completed by the lid at the seam, so the assembled
  case shows one continuous opening. Four M3×12 countersunk screws from the bottom clamp the PCB and
  lid; the heads sit in Ø6.6 countersinks and do not protrude. The lid top is
  solid and the faceplate sits flush. The lid and base are separate `LID` and
  `BASE` components. See [`case/README.md`](../../case/README.md).
- Optional decorative stone faceplate **`case/faceplate_compact.stl`** —
  39.5 × 82.5 × 3.85 mm, bottom z 19.0, with matching radar/BME hole fields
  and a funnel over the BH1750 sensor. The stone surface is sampled from the
  CC0 Poly Haven *Rustic Stone Wall 02* displacement map; previews are in
  `case/renders/`. The Blender scene is `case/compact_faceplate.blend` and the
  generator is [`tools/blender/make_compact_faceplate.py`](../../tools/blender/make_compact_faceplate.py).

## Open questions
- Optional decorative faceplate overlay in Blender; the base cover is already
  printable without it.
- Does the enclosure still need the wiring-side depth, or can it become a slimmer wall box?
