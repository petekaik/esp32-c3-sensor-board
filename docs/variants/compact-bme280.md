# Variant: compact, no relay, BME280 (planned)

**Status:** planned
**Board:** 46 × 68 mm, R3, 2-layer (≈21 mm shorter than rev2)

## What changes
- **J3 and the relay module area removed** — no relay socket, no relay footprint.
- Board shortened to 46 × 68 mm; the sensor strip, ESP32, LD2410C and breakout keep their
  positions.
- **GPIO4 freed** and added to the breakout row → **J5 becomes 1×15**:
  `3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO4 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`
- Buttons stay on J4; jumpers JP1/JP2/JP3 unchanged with defaults 1–2 (I²C, 0x76, 0x23).

## BOM
[`../BOM.csv`](../BOM.csv) minus the J3 socket and the KY-019 relay module.

## Layout
| Item | Position (mm, origin top-left) |
|---|---|
| ESP32-C3 socket | (22, 11.2), USB out the top short edge |
| LD2410C | (20, 33) |
| BME280 | (3.5, 47.5) |
| BH1750 | (23, 47.5) |
| Jumper headers | (3.5 / 7.1 / 10.7, 51.2) |
| Breakout row J5 | x 40, y 25 … 60.6 (15 holes) |
| Button terminal | (6.5, 14.5) |

## Firmware
Same as [relay-bme280](relay-bme280.md) but **remove the `switch: chime` block** and the button's
`on_press` action; GPIO4 is now a free I/O on the breakout row.

## Open questions
- Does the enclosure still need the wiring-side depth, or can it become a slimmer wall box?
- Keep the 2-pin button terminal, or move the button onto the breakout row?
