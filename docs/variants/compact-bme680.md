# Variant: compact, no relay, BME680 (rev3, planned)

**Status:** planned — rev3 layout
**Board:** 46 × 68 mm, R3, 2-layer

Combines the two changes:
1. **Compact / no relay / no button terminal** — J3, the relay area and J4 removed;
   GPIO3 and GPIO4 freed (see [compact-bme280](compact-bme280.md)).
2. **BME680** instead of BME280 on the same 1×6 socket (see [relay-bme680](relay-bme680.md)).
   Note the CJMCU-680 SDO/CS pin-order caveat.

## Breakout row (J5, 1×16)
`3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO3 · GPIO4 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`

## Jumper defaults
JP1 1–2 (I²C), JP2 1–2 (0x76), JP3 1–2 (0x23) — same as every other variant.

## Firmware
Compact base configuration plus the BME680 component:
- I²C on GPIO8/9, UART on GPIO20/21
- BME680 via `bme680_bsec` (or `bme680_i2c` if BSEC is not wanted)
- No relay switch and no J4 button; GPIO3 and GPIO4 are free on J5 pins 7/8

## BOM
[`../BOM.csv`](../BOM.csv) minus the J3 socket, J4 terminal and relay module;
J5 becomes the 1×16 socket (LCSC C7499334); BME280 replaced by BME680.

## Risks to check before layout
- BSEC needs ~2 kB more RAM and a slower I²C bus; verify timing on the C3.
- VOC accuracy is affected by the enclosure airflow — keep the louvres above the sensor.
