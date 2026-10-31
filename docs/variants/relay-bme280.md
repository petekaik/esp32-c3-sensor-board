# Variant: relay + BME280 (rev2 built, rev3 routed)

**Status:** rev2 built/ordered; rev3 routed — `hardware/esp32-c3-sensor-board-rev3.*`
**Board:** 46 × 89 mm, R3, 2-layer

## rev3 — 1×16 breakout
Rev3 keeps the relay and button terminals but expands J5 from 1×14 to **1×16**,
so every header pin is also available on the breakout:
`3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO3 · GPIO4 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`.
GPIO3/GPIO4 are the button and relay nets; they appear on J4/J3 and on J5.
J3/J4 and all other placements are unchanged. The board was re-routed with
FreeRouting at 0.25 mm traces / 0.20 mm clearance; ERC is 0 and DRC is
**0 violations, 0 unconnected**. J5 and U2 use project-local footprint copies
with the side/top silk moved to the fab layer, so the silkscreen no longer
clashes with the breakout labels or the nearby vias.

Rev2 remains the ordered baseline and still has the 1×14 row.

## Bill of materials
See [`../BOM.csv`](../BOM.csv). Modules: BME280, BH1750, LD2410C, KY-019 relay, 2-pin button
terminal.

## Differences from base
This is the base design. All other variants are derived from it.

| Feature | This variant |
|---|---|
| Relay | J3 right-angle socket, KY-019 class, pins GND / 5V / RELAY |
| Temperature sensor | BME280, 1×6 socket, address 0x76 |
| GPIO4 | relay signal (J3) |
| Board length | 89 mm (relay module overhangs the sensor area in plan) |

## Connectors
- U1 ESP32-C3 Super Mini socket (2×8)
- U2 LD2410C (1×5) — UART 256000 8N1
- J1 BME280 (1×6) — I²C 0x76
- J2 BH1750 (1×5) — I²C 0x23
- J3 relay (1×3 horizontal socket)
- J4 button (2-pin terminal)
- J5 breakout **1×16** female socket (rev3): 3V3, 5V, GND, GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO10, SDA, SCL, RX, TX; rev2 is the older 1×14 row without GPIO3/GPIO4
- JP1/JP2/JP3 jumper headers, defaults 1–2 (I²C, 0x76, 0x23)

## Firmware
`doorbell.yml`: I²C on GPIO8/9, UART on GPIO20/21, relay on GPIO4 (active-high, off at boot),
button on GPIO3 with internal pull-up.

## Layout notes
- Radar patch area and ESP32 antenna end are copper-free (both layers).
- BME280 sits away from the ESP32/radar/relay heat; keep the enclosure louvred above it.
- Relay module must be clear of the BME280 in plan (relay can ≈ 15 mm tall).
