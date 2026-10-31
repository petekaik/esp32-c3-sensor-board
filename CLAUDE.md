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
| I2C SDA (BME280 + BH1750) | GPIO8 | BME280 @ 0x76 (SDO→GND), BH1750 @ 0x23 (ADDR→GND) |
| I2C SCL (BME280 + BH1750) | GPIO9 | shared bus; modules usually carry pull-ups — fit board-side 4.7k to 3V3 only if they don't |
| LD2410C UART TX (ESP→module RX) | GPIO21 | 256000 baud, 8N1 |
| LD2410C UART RX (ESP←module TX) | GPIO20 | cross TX/RX on the connector |

Constraints to respect:

- GPIO18/19 are native USB D-/D+ — reserved; do not use for peripherals.
- GPIO2/8/9 are strapping pins; avoid designs that hold them low at boot. GPIO9 is the onboard BOOT button and GPIO8 the onboard LED on most Super Mini variants — verify against the actual board. Rev2 deliberately uses GPIO8/GPIO9 for I²C (the reference pinout's SDA/SCL); the module pull-ups hold both high at reset.
- GPIO4/5/6/7 are the C3 JTAG pins. This pinout gives up JTAG debugging; acceptable, but don't add a conflicting debug header.
- GPIO20/21 are the UART0 defaults. The ESPHome logger is configured for `USB_SERIAL_JTAG`, so keep the USB-C connector accessible for logs and flashing.
- **Verify the Super Mini header footprint and pinout against the physical board before schematic capture.** Variants differ. Rev2 uses the reference order: pad 1 = 5V at the USB end, pad 8 = GPIO0, pad 9 = GPIO5, pad 16 = GPIO21; the U1 footprint was corrected to that order.

Every HW-dependent default (polarity, pull-ups, addresses, baud) is fixed by `doorbell.yml` and must stay documented here so the YAML never needs board knowledge.

## Connectors

- I2C: one socket per module on the shared bus.
  - **BME280 (6-pin module, ~15.2×12 mm, 2.54 mm pitch):** 1x06 socket — 3V3, GND, SCL, SDA, CSB, SDO. CSB→3V3 (I2C mode) and SDO→GND (0x76) through 3-pad solder jumpers, default bridged; SDO alternate to 3V3 = 0x77. Verify silkscreen pin order — some clones swap CSB/SDO.
  - **BH1750 (GY-302 5-pin module, 13.9×18.5 mm, 2.54 mm pitch):** 1x05 socket — VCC (3V3), GND, SCL, SDA, ADDR. The module already pulls ADDR low (0x23), so JP3 is optional; alternate 3V3 = 0x5C.
- Female headers: 2× 1×8 (U1), 1× 1×5 (U2), 1× 1×6 (J1), 1× 1×5 (J2), 1× 1×14 (J5 breakout). U1/U2 and J1/J2 have socket 3D models and J1/J2 use the detailed baked module models; J3/J4 terminal 3D uses Phoenix MKDS 5.00 stand-ins for the MX126 5.0 footprints.
- UART: 4-pin header for LD2410C — 5V, GND, ESP TX (GPIO21) → module RX, ESP RX (GPIO20) ← module TX
- Relay: 3-pin screw terminal in module pin order — **5V, GND, RELAY (GPIO4)**. External active-high module (10 A contacts); switched load is low voltage (<50 V), so no mains isolation on the carrier.
- Button: 2-pin wire terminal — GPIO3, GND; internal pull-up, button shorts to GND

## Enclosure and mechanical

PCB and case are co-designed: footprint positions, module heights and connector orientations determine every opening. Freeze placement before modelling. Treat one face as the **front** (radar + light + air); put wiring and USB elsewhere.

- **LD2410C (24 GHz radar)**
  - The twin patch antennas are on the module's component side, centred on the board — that face looks at the case front through a thin RF-transparent wall (≤2–3 mm ABS/PETG/PLA). No metal, no carbon- or metal-filled filament, no conductive mesh, no foil tape in front of it.
  - Copper/screw keep-out under and around the patch area; keep relay, screw terminals and the Super Mini's shielded can out of the forward beam.
  - Module is 22×16 mm; leave ~8–10 mm stack height for the socket/header. It runs warm (~0.4 W) — vent its pocket and keep it away from the BME280.
- **BH1750 (GY-302 lux module, 13.9×18.5 mm on a 2.54 mm socket)**
  - Clear or translucent window directly in front of the sensor, on the front face. No opaque or tinted plastic, no case shadow, no long/attenuating light pipe.
  - At the board edge so the window stays small; leave clearance for the ~8–10 mm module stack height.
- **BME280 (temp/humidity/pressure)**
  - Module is ~15.2×12 mm on a 2.54 mm socket (~8–10 mm stack height); louvre the case above the sensor can and leave clearance for the module.
  - Needs ambient airflow: louvred vents, not a sealed pocket; no direct sunlight; not in the exhaust path of the ESP32, relay or LD2410.
  - Furthest from heat sources; thermal-relief the PCB under it (slot/cutout) so board heat doesn't bias the reading.
  - Do not share its vent path with the radar's heat exhaust.
- **Relay module (25.6×33.5 mm, external):** mount on the wiring side with wire-entry knockouts on bottom/back and access to its screw terminals; keep its coil/LED heat away from the sensors. The carrier only brings out 5V, GND and the GPIO4 signal on J3.
- **USB-C:** opening aligned with the Super Mini's connector — needed for flashing and `USB_SERIAL_JTAG` logs.
- **Wall mount:** mounting holes/bracket, cable entry, and header service clearance.
- **Filament:** PLA/PETG fine; never carbon-fibre or metal-filled anywhere in front of radar or light sensor.

## PCB layout

**Current design is rev2:** `hardware/esp32-c3-sensor-board-rev2.*` — 40 × 70 mm portrait, R3, USB-C on the top short edge, relay on a right-angle 1×3 socket at the bottom edge. Rev2 is routed with 0.25 mm traces, 0.20 mm clearance, **0.8/0.3 mm vias (0.25 mm annular ring, untented, 0.9 mm mask openings)**, 50 µm mask expansion and 0.15 mm silkscreen, so it passes AISLER's 2L 1.6 mm 35 µm process checks (no tented vias, no silk on pads). Details in `HANDOFF.md`. The rev1 numbers below are kept for reference.

Board 80×60 mm, 3 mm corner radius, origin top-left, +Y toward the wiring edge.

- Top half: U2 LD2410C (20.5, 16, 180°), J2 BH1750 socket (36, 21.9, 90°) in the middle, J1 BME280 socket (55, 20, 90°) far right — the BME280 is deliberately away from the LD2410C, ESP32 and relay heat. Module bodies: BH1750 x 34–48, BME280 x 53.7–69; keep the radar patch area and Super Mini antenna end free of carrier copper.
- Connector/mounting 3D: U1 two 1×8 female headers, U2 one 1×5, J1 1×6, J2 1×5; U1/U2 socket models are attached, J1/J2 are standard socket footprints with their 3D models. J3/J4 use Phoenix MKDS 5.00 terminal 3D models as visual stand-ins for the MX126 5.0 footprints.
- BME280/BH1750 use the **baked models** attached to J1/J2: `bme280-good-baked.step` (vendor, re-coloured) and `bh1750-good-baked.step` (rebuilt in Fusion from the vendor's measured geometry: PCB, pads, chip passives and ICs as separate bodies, since the vendor file was one merged solid). Frame: pin row +Y at x=0, body −X, PCB bottom Z=0; rotation 0. Final offsets, aligned manually in the KiCad 3D preview and saved in the board file: BME280 `(0, −12.7, 11)`; BH1750 `(−0.04, −10.2, 11)`. Vendor originals remain in `lib/models/`.
- J1/J2 also have 1×6/1×5 male pin-header 3D models (`PinHeader_1x06/1x05`, rotation X=180, offsets (0, −12.7, 11) and (0, −10.16, 11)): long pins down into the female sockets, short pins through the module edges.
- Socket stacking: female header 8.5 mm + male header plastic 2.5 mm → module PCB at Z≈11 mm. U1 model at 11.0, U2 at 11.5 (LD2410C model has 3 mm below-PCB geometry), BME/BH at 11.0.
- U1 has two 1×8 male pin-header 3D models (`PinHeader_1x08`, rotation X=180, offset x=±7.62, y=−8.89, z=11): long pins point down into the female sockets, short pins protrude through the module edges.
- Bottom half: U1 Super Mini socket (19, 45.26, 0°) with USB at the bottom edge; J3 relay terminal (56, 51, 180°) and J4 button terminal (37, 51, 180°), wire entry toward the bottom edge.
- H1–H4 M3 holes at (5,5), (76,5), (5,55), (76,55).
- Routing: 2-layer; signals/power on F.Cu, GND pour on B.Cu with two holes — LD2410C patch area (x 10–31, y 8–21) and Super Mini antenna (x 14–24, y 34–37). Autorouted (Freerouting), then zone-filled; min trace 0.20 mm, min clearance 0.15 mm, vias 0.6/0.3 mm.
- Verified: 0 courtyard overlaps at 0.3 mm margin, 0 boundary violations, 0 DRC errors (2 warnings: cosmetic U2 pin-1 silk and a JP2 library-mismatch note).

## Workflow

Design is automated with Claude Code + the KiCad MCP server (KiCad 10).

- Project: `hardware/esp32-c3-sensor-board.kicad_pro`. Libraries: `sensor-board` (symbols + footprints) and `ld2410c` (symbol), both `${KIPRJMOD}`-relative. Super Mini socket is `sensor-board:ESP32-C3-SuperMini_Socket` — 2x8, 2.54 mm pitch, 15.24 mm rows, 22.52x18 mm outline, pin 1 = 5V top-left, USB end at +Y. Its symbol is `sensor-board:ESP32-C3-SuperMini`.

- Drive KiCad through the MCP server; do not hand-edit `.kicad_sch` / `.kicad_pcb` text.
- Run ERC and DRC before declaring a design done, and report the actual output.
- Prefer standard KiCad library footprints; add custom ones only for module-specific connectors.
- Export BOM and gerbers when the board is ready to order (JLCPCB).

Reference: https://jlcpcb.com/blog/kicad-mcp-how-to-design-a-pcb-with-claude-code

## Open decisions

- Count and placement of spare GPIO breakout headers
- Final module placement / board outline (module sizes: BME280 15.2×12, BH1750 13.9×18.5, LD2410C 22×16 mm)

## Confirmed

- Relay module is external, active-high, 5 V / 10 A; switched load is low voltage (<50 V) — no mains isolation required on the carrier
- LD2410C is powered from 5V (3.3V logic)
- BME280 modules are 6-pin (~15.2×12 mm); BH1750 is the GY-302 5-pin (13.9×18.5 mm, ADDR low = 0x23)
- LD2410C silkscreen is **TX RX OUT GND VCC**, matching the PartReel footprint/symbol; 22×16 mm, 5 V / ~79 mA, 256000 baud 8N1
- LD2410C is socketed, not soldered down: fit a 1×05 female header on U2, solder pins out the module's back, and plug it in. The 3D model is the official Hi-Link STEP (vendor file had the PCB and parts at different origins; translated the board by −162.535, −37.165 mm to assemble it) with an 8.5 mm socket offset. Right-angle pins would need a different socket orientation and a U2 re-layout.
