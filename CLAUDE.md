# ESP32-C3 Super Mini Sensor Board

Hardware-only repo: a wall-mountable add-in/carrier board for the **ESP32-C3 Super Mini** that exposes GPIO, power and comms for plug-in sensor and peripheral modules.

**Not in this repo:** ESPHome YAML configs live in a separate project. This repo owns the schematic, PCB, enclosure and the pin-map documentation the YAML must match.

## Deliverables

- KiCad 10 schematic + PCB for the carrier board
- 3D-printed wall-mount enclosure
- Pin map / HW config doc (pin assignments, active-high/low defaults, connector pinouts) so ESPHome YAML can be written without reverse-engineering the board

## Board requirements

Carrier board — the Super Mini plugs into headers; it is not soldered down. Must provide:

- Access to spare GPIO, 3V3, 5V and GND
- One I2C bus shared by **BME280** (temp/humidity/pressure) and **BH1750** (lux)
- UART to **HLK-LD2410C** presence sensor
- **Relay module** via wire terminals — GPIO4
- **Button** via wire terminals — GPIO3
- 3D-printable, wall-mountable enclosure

## Pin map

Authoritative source: `doorbell.yml`. The PCB must match it, not the other way round.

| Function | Pin | Notes |
|---|---|---|
| Relay control | GPIO4 | active-high; off at boot (`ALWAYS_OFF`) |
| Button input | GPIO3 | button to GND, internal pull-up, active-low physically |
| I2C SDA (BME280 + BH1750) | GPIO6 | BME280 @ 0x76 (SDO→GND), BH1750 @ 0x23 (ADDR→GND) |
| I2C SCL (BME280 + BH1750) | GPIO7 | shared bus; modules usually carry pull-ups — fit board-side 4.7k to 3V3 only if they don't |
| LD2410C UART TX (ESP→module RX) | GPIO21 | 256000 baud, 8N1 |
| LD2410C UART RX (ESP←module TX) | GPIO20 | cross TX/RX on the connector |

Constraints to respect:

- GPIO18/19 are native USB D-/D+ — reserved; do not use for peripherals.
- GPIO2/8/9 are strapping pins; avoid designs that hold them low at boot. GPIO9 is the onboard BOOT button and GPIO8 the onboard LED on most Super Mini variants — verify against the actual board.
- GPIO4/5/6/7 are the C3 JTAG pins. This pinout gives up JTAG debugging; acceptable, but don't add a conflicting debug header.
- GPIO20/21 are the UART0 defaults. The ESPHome logger is configured for `USB_SERIAL_JTAG`, so keep the USB-C connector accessible for logs and flashing.
- **Verify the Super Mini header footprint and pinout against the physical board before schematic capture.** Variants differ.

Every HW-dependent default (polarity, pull-ups, addresses, baud) is fixed by `doorbell.yml` and must stay documented here so the YAML never needs board knowledge.

## Connectors

- I2C: 4-pin header(s) — 3V3, GND, SDA, SCL; BME280 and BH1750 share the bus
- UART: 4-pin header for LD2410C — 5V, GND, ESP TX (GPIO21) → module RX, ESP RX (GPIO20) ← module TX
- Relay: wire terminal — GPIO4 control, 5V, GND; **module must be active-high** to match `doorbell.yml`
- Button: 2-pin wire terminal — GPIO3, GND; internal pull-up, button shorts to GND

## Enclosure and mechanical

PCB and case are co-designed: footprint positions, module heights and connector orientations determine every opening. Freeze placement before modelling. Treat one face as the **front** (radar + light + air); put wiring and USB elsewhere.

- **LD2410C (24 GHz radar)**
  - Antenna end faces front through a thin RF-transparent wall (≤2–3 mm ABS/PETG/PLA). No metal, no carbon- or metal-filled filament, no conductive mesh, no foil tape in front of it.
  - Copper/screw keep-out under and around the antenna end; hang the antenna at the board edge facing out.
  - Keep relay, screw terminals and the Super Mini's shielded can out of the forward beam.
  - It runs warm (a few hundred mW) — vent its pocket and keep it away from the BME280.
- **BH1750 (lux)**
  - Clear or translucent window directly in front, on the front face. No opaque or tinted plastic, no case shadow, no long/attenuating light pipe.
  - At the board edge so the window stays small.
- **BME280 (temp/humidity/pressure)**
  - Needs ambient airflow: louvred vents, not a sealed pocket; no direct sunlight; not in the exhaust path of the ESP32, relay or LD2410.
  - Furthest from heat sources; thermal-relief the PCB under it (slot/cutout) so board heat doesn't bias the reading.
  - Do not share its vent path with the radar's heat exhaust.
- **Relay + wire terminals:** wire-entry knockouts on bottom/back, reachable without removing the board; relay coil heat away from the sensors.
- **USB-C:** opening aligned with the Super Mini's connector — needed for flashing and `USB_SERIAL_JTAG` logs.
- **Wall mount:** mounting holes/bracket, cable entry, and header service clearance.
- **Filament:** PLA/PETG fine; never carbon-fibre or metal-filled anywhere in front of radar or light sensor.

## Workflow

Design is automated with Claude Code + the KiCad MCP server (KiCad 10).

- Drive KiCad through the MCP server; do not hand-edit `.kicad_sch` / `.kicad_pcb` text.
- Run ERC and DRC before declaring a design done, and report the actual output.
- Prefer standard KiCad library footprints; add custom ones only for module-specific connectors.
- Export BOM and gerbers when the board is ready to order (JLCPCB).

Reference: https://jlcpcb.com/blog/kicad-mcp-how-to-design-a-pcb-with-claude-code

## Open decisions

- Exact breakout-module dimensions and mounting-hole positions for BME280, BH1750 and LD2410C — drives case alignment
- Count and placement of spare GPIO breakout headers

## Confirmed

- Relay module is active-high (matches `doorbell.yml`)
- LD2410C is powered from 5V (3.3V logic)
