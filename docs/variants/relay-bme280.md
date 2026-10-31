# Variant: relay + BME280 (rev2, built)

**Status:** built and routed — `hardware/esp32-c3-sensor-board-rev2.*`
**Board:** 46 × 89 mm, R3, 2-layer

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
- J5 breakout 1×14 holes: 3V3, 5V, GND, GPIO0, GPIO1, GPIO2, GPIO5, GPIO6, GPIO7, GPIO10, SDA, SCL, RX, TX
- JP1/JP2/JP3 jumper headers, defaults 1–2 (I²C, 0x76, 0x23)

## Firmware
`doorbell.yml`: I²C on GPIO8/9, UART on GPIO20/21, relay on GPIO4 (active-high, off at boot),
button on GPIO3 with internal pull-up.

## Layout notes
- Radar patch area and ESP32 antenna end are copper-free (both layers).
- BME280 sits away from the ESP32/radar/relay heat; keep the enclosure louvred above it.
- Relay module must be clear of the BME280 in plan (relay can ≈ 15 mm tall).
