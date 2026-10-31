# Variant: compact, no relay, BME280 (rev3, planned)

**Status:** planned — rev3 layout
**Board:** 46 × 68 mm, R3, 2-layer (≈21 mm shorter than rev2)

## What changes
- **J3, the relay module area and J4 (button terminal) removed.**
- Board shortened to 46 × 68 mm; the sensor strip, ESP32, LD2410C and breakout keep their
  positions.
- **GPIO3 and GPIO4 freed** and added to the breakout row → **J5 becomes 1×16**:
  `3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO3 · GPIO4 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`
- Jumpers JP1/JP2/JP3 unchanged with defaults 1–2 (I²C, 0x76, 0x23).

## BOM
[`../BOM.csv`](../BOM.csv) minus the J3 socket, the J4 terminal and the KY-019 relay module;
J5 becomes the 1×16 socket (LCSC C7499334).

## Layout
| Item | Position (mm, origin top-left) |
|---|---|
| ESP32-C3 socket | (22, 11.2), USB out the top short edge |
| LD2410C | (20, 33) |
| BME280 | (3.5, 47.5) |
| BH1750 | (23, 47.5) |
| Jumper headers | (3.5 / 7.1 / 10.7, 51.2) |
| Breakout row J5 | x 40, y 25 … 63.1 (16 socket positions) |
| Button terminal | removed (GPIO3 on J5 pin 7) |

## Firmware
Same as [relay-bme280](relay-bme280.md) but **remove the `switch: chime` block** and the
J4 button configuration; GPIO3 and GPIO4 are now free I/O on the breakout row (pins 7 and 8).

## Open questions
- Does the enclosure still need the wiring-side depth, or can it become a slimmer wall box?
- J5 now reaches y = 63.1 mm; the bottom mounting holes must move (or the board grow
  to ~70 mm) to keep clearance from the 1×16 socket.
