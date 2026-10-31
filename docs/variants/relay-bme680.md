# Variant: relay + BME680 (rev3, planned)

**Status:** planned — rev3 PCB, BME680 module fitted instead of BME280.
**Board:** 46 × 89 mm, R3, 2-layer

## Difference from relay-bme280
The sensor module and the firmware change; rev3 also uses the 1×16 breakout row.
The 1×6 BME socket, JP1/JP2 jumpers and the I²C bus are pin-compatible with a
BME280 module, **but the common CJMCU-680 BME680 is not**: its header is
`VCC, GND, SCL, SDA, SDO, CS`, so pins 5/6 are swapped versus J1’s
`3V3, GND, SCL, SDA, CSB, SDO`. Use a 6-pin crossover adapter, or a clone
silkscreened `…, CS, SDO`. Do not plug a standard CJMCU-680 straight in: JP2
would pull CS low (SPI) and JP1 would pull SDO high (0x77).

| Item | BME280 variant | BME680 variant |
|---|---|---|
| Sensor | BME280 | BME680 (same 6-pin socket) |
| I²C address | 0x76 | 0x76 (JP2 1–2) |
| ESPHome component | `bme280_i2c` | `bme680_bsec` or `bme680_i2c` |
| Measurements | T, RH, P | T, RH, P, VOC/IAQ |

## Firmware notes
- BME680 modules with the **BSEC** library need a longer I²C timeout and are happier at 100 kHz.
- If the module's SDO is tied high on the PCB itself, the address is 0x77 — check the module and
  set JP2 accordingly.
- VOC output needs a burn-in period; expose it as a separate sensor with `state_class:
  measurement`.

## Everything else
Identical to [relay-bme280](relay-bme280.md): relay on J3, button on J4, LD2410C on U2, BH1750 on
J2, 1×16 breakout female socket (GPIO3/GPIO4 included), jumper defaults 1–2.
