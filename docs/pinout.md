# Pin map and connectors

Authoritative electrical reference for the carrier board. Rev2 hardware is frozen: I²C is on
GPIO8 (SDA) / GPIO9 (SCL), UART on GPIO20/21, relay GPIO4, button GPIO3. `doorbell.yml` still
lists GPIO6/7 for I²C and must be updated to `sda: GPIO8` / `scl: GPIO9` to match.

## ESP32-C3 Super Mini socket (U1, 2×8)

| Pad | Net | Pad | Net |
|---|---|---|---|
| 1 | 5V | 9 | GPIO5 → SPI_MISO (JP2 pin 3, J5) |
| 2 | GND | 10 | GPIO6 (J5) |
| 3 | 3V3 | 11 | GPIO7 → SPI_CS (JP1 pin 3, J5) |
| 4 | RELAY (GPIO4) | 12 | I2C_SDA (GPIO8) |
| 5 | BUTTON (GPIO3) | 13 | I2C_SCL (GPIO9) |
| 6 | GPIO2 (J5) | 14 | GPIO10 (J5) |
| 7 | GPIO1 (J5) | 15 | UART_RX (GPIO20) |
| 8 | GPIO0 (J5) | 16 | UART_TX (GPIO21) |

## Connectors

### U2 — LD2410C (1×5 socket)
`1 TX · 2 RX · 3 OUT · 4 GND · 5 VCC (5 V)`
Module silkscreen order is TX RX OUT GND VCC; nets are crossed on purpose (module TX → UART_RX).

### J1 — BME280 / BME680 (1×6 socket)
`1 3V3 · 2 GND · 3 SCL · 4 SDA · 5 CSB · 6 SDO`
CSB is pulled to 3V3 through JP1 (I²C mode); SDO selects the address through JP2.

### J2 — BH1750 GY-302 (1×5 socket)
`1 3V3 · 2 GND · 3 SCL · 4 SDA · 5 ADDR`
ADDR to GND through JP3 → 0x23.

### J3 — relay (1×3 right-angle socket, KY-019 class)
`1 GND · 2 5V · 3 RELAY (GPIO4)` — module pin order GND, Vcc+, Signal.
Not fitted on the compact variants.

### J4 — button (2-pin screw terminal)
`1 BUTTON (GPIO3) · 2 GND` — internal pull-up, button shorts to GND.

### J5 — breakout row (1×14 female socket)
`3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO5 · GPIO6 · GPIO7 · GPIO10 · SDA · SCL · RX · TX`

Fitted with a standard 2.54 mm 1×14 female socket
(`Connector_PinSocket_2.54mm:PinSocket_1x14_P2.54mm_Vertical`).

Compact variants add **GPIO4** as hole 15.

## Jumper defaults

| Ref | Default | Meaning |
|---|---|---|
| JP1 | 1–2 | CSB tied to 3V3 → I²C mode (2–3 = CSB to GPIO7, SPI mode) |
| JP2 | 1–2 | SDO tied to GND → address 0x76 (2–3 = SDO to GPIO5, SPI MISO) |
| JP3 | 1–2 | ADDR tied to GND → 0x23 (open = 0x5C) |

All three are 2.54 mm pin headers; fit a shunt on the marked pair. The default pairs are boxed on
the bottom silkscreen.

## Bus settings

| Bus | Pins | Settings |
|---|---|---|
| I²C | GPIO8 / GPIO9 | 100 kHz default, pull-ups on the modules |
| UART | GPIO20 / GPIO21 | 256000 baud, 8N1 |
| SPI (optional, BME280 only) | SCK GPIO9, MOSI GPIO8, MISO GPIO5, CS GPIO7 | reuses SCL/SDA as SCK/MOSI |
