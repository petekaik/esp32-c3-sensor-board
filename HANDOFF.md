# Handoff — 3D models

## Done

- Detailed BME280/BH1750 vendor models are baked and attached to J1/J2:
  - `bme280-good-baked.step` — flattened from the Fusion assembly
    (TemporaryBRepManager per body, global occurrence matrices + frame transform).
  - `bh1750-good-baked.step` — baked with a Fusion Move feature.
  - Frame: pin row +Y at x=0, body −X, PCB bottom Z=0.
- Colours/detail restored in Fusion and re-exported into the same STEPs:
  - BME280: 47 bodies re-appeared (green PCB, gold pins, steel can, black SMD,
    white silk). Was one grey `Steel - Satin` default. Then the 6 chip passives
    were detailed in place (bodies belong to one base feature, so they cannot be
    deleted individually): 4 resistors got nickel end caps, 2 capacitors got a
    white body shell plus nickel end caps (61 bodies now). Pre-detail copy:
    /tmp/bme280-good-baked.pre-smd.step.
  - BH1750: vendor model rebuilt in Fusion from its measured geometry because
    it was one merged solid. Now 47 bodies: PCB (18.7×14×1.6, 5 × Ø0.9 pin holes,
    2 × Ø3.0 mounting holes), 10 brass pad rings (1.9 mm OD / 0.92 mm ID,
    both faces), 8 chip passives (ceramic/black body + nickel end caps),
    SOT-23 with 3 gull-wing leads, BH1750 sensor with 3+3 leads and a
    translucent window. Same coordinate frame, so the J2 3D offsets still hold.
    Pre-rebuild originals: /tmp/bh1750-good-baked.pre-pads.step (vendor),
    /tmp/bh1750-good-baked.pads-only.step (vendor + pads).
- BME280/BH1750 baked vendor models attached to J1/J2, rotation 0.
  Final offsets aligned manually in KiCad and saved in the board file:
  `(0, −12.7, 11)` (BME280) and `(−0.04, −10.2, 11)` (BH1750).
  Male pin headers: `(0, −12.7, 11)` / `(0, −10.16, 11)`, rotation X 180.
  - J1 BME280 is at (55, 20), far right; deliberately away from the LD2410C,
    ESP32 and relay heat.
  - J2 BH1750 is at (36, 21.9), middle.
- Jumpers moved with them: JP1 (62,28), JP2 (70,28), JP3 (44,28).
- Board re-routed with Freerouting (Java 25 Docker image) and the GND zone
  refilled.
- J1/J2 have 1×6/1×5 male pin-header 3D models: long pins down into the
  female sockets, short pins through the module edges.
- Stacking: 8.5 mm female header + 2.5 mm male plastic ≈ 11 mm module PCB.
  U1 = 11.0 mm, U2 = 11.5 mm (LD2410C has 3 mm below-PCB geometry), J1/J2 = 11.0.
- U1 has two 1×8 male pin-header 3D models: long pins down into the female
  sockets, short pins through the module edges.
- Female sockets (U1/U2/J1/J2) and J3/J4 terminal 3D are in place.
- DRC: 0 errors, 2 warnings (cosmetic U2 pin-1 silk; JP2 library mismatch). ERC: 0.

Vendor originals remain in `lib/models/` for reference. Placeholder and
dummy-carrier experiments were removed.

## Rev2 (draft, separate files)

- `hardware/esp32-c3-sensor-board-rev2.{kicad_pro,kicad_sch,kicad_pcb}` —
  rev1 untouched. Same `${KIPRJMOD}` libs.
- **40 × 70 mm**, R3. USB-C out the top short edge (U1 at 22, 11.2, 180;
  connector overhangs ~0.4 mm). LD2410C (20, 31, 0). BME280 (3.5, 42.6, 90).
  BH1750 (23, 42.2, 90) — 1.6 mm clear of the radar body. Relay
  `PinSocket_1x03_P2.54mm_Horizontal` tucked under the BH1750 footprint
  (25, 58.5, 90), module out the bottom edge. Button terminal beside the
  ESP32 on the left (6.5, 14.5, -90, user-rotated). Jumpers (5/10/15, 55.5). Holes (3,3),
  (37,3), (3,67), (37,67) with hidden refs.
- 3D levels: module STEPs use different Z datums. PCB bottoms aligned at
  11.0 mm by offsetting the ESP32 model to z 11.55 (PCB bottom −0.55) and the
  LD2410C model to z 11.99 (PCB bottom −0.99); BME/BH stay at 11.0.
- ESP32-C3 model is the vendor STEP unchanged: it already carries its own
  soldered pads, and adding rings on top duplicated them out of alignment.
  Backups: /tmp/esp32c3.pre-rings.step (identical to the vendor file).
- LD2410C model rebuilt from /tmp/ld2410c.pre-rings.step: PCB recoloured navy
  blue, 10 brass pin rings (r 0.45, both faces), brass antenna pour that stops
  at y 4.35 (below the pad rings), two silver patch antennas (y 1.9-4.15) and
  copper feed stubs. The vendor STEP's component layout differs from current
  modules (no QFN in the middle), so only antenna/pour/pin detail was added.
- Silk: BME280 outline (1.9,40.9)–(17.8,52.6); BH1750 outline
  (21.15,40.64)–(35.15,59.34) with the bottom edge split around J3 pads;
  labels `ESP32-C3`, `LD2410C`, `BH1750`, `BME280`, `RELAY`, `BUTTON`,
  `USB-C`, `REV2`.
- Copper: GND pours B.Cu + F.Cu (0.5 mm inset, solid pad connection); holes at
  radar (9,26)–(31,39) and ESP32 antenna (14,17)–(30,22); both-layer rule area
  x9–31 y27–39.
- Pin labels: J1 (3V3 GND SCL SDA CSB SDO) and J2 (3V3 GND SCL SDA ADR) on
  F.SilkS above their pad rows; J4 legend (BUTTON / GPIO3 / GND) below the
  terminal; U1 2x8, U2 (TX RX OUT GND 5V) and J3 (5V GND RLY) on B.SilkS
  (mirrored) because the modules cover those pads from above. Hole and U2
  reference fields are hidden.
- Routed with Freerouting (Java 25 image): 75 tracks / 4 vias, 0 unrouted.
- DRC: 0 errors, 0 unconnected, 3 warnings — JP2 library mismatch, U2 pin-1
  silk, U1 silk clipped by the top edge (USB overhang).
- Schematic (rev2 copy): J3 footprint changed to
  `Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Horizontal`; project
  instance names rewritten to `esp32-c3-sensor-board-rev2`; ERC 0 violations.

## Jumpers -> pin headers + BME SPI (done)

- Jumpers moved under the BME280 module: JP1 (3.5, 48.2), JP2 (7.1, 48.2),
  JP3 (10.7, 48.2), pin1 at the bottom of the module; refs hidden. Clearance
  under the module is ~11 mm, header + shunt ~4.5 mm -> ~6 mm spare.
- Relay is now a vertical `PinSocket_1x03_Vertical` at (11, 58.5), rot 90,
  nets 5V/GND/RELAY, for a KY-019 style module with male pins.
- The relay module (25.6 x 33.5 mm, ~15 mm tall relay can) cannot overlap the
  BME/BH/ESP32 (11-13.6 mm) - the body must extend over the freed bottom strip
  and past the bottom edge (~22 mm overhang) into the case. Case depth on the
  wiring side must allow it; if it must sit fully on the board, the PCB has to
  grow or the relay move to a taller mount.
- Schematic matches (ERC 0). Board: 0 errors, 0 unconnected, 2 warnings
  (U1 USB silk past top edge, U2 pin-1 silk).
- Relay socket now `PinSocket_1x03_Vertical` at (32, 55), pin row along the
  long board axis, module facing the BME280; it sits under the BH1750 module.
- JP1/JP2/JP3 labels are silkscreen text at y 55.4 (visible below the BME
  module, refs remain hidden).
- Fit check, KY-019 (25.6 x 33.5 mm, ~15 mm relay can) in the old jumper strip
  next to the BME280: the free rectangle is only 21.15 x 15.5 mm, so it cannot
  sit fully on the board - it needs 10-18 mm of overhang past the bottom edge
  depending on orientation. Do not grow the board (decision 2026-10-29).

- KY-019 3D model added: `lib/models/ky019.step` (built in Fusion from
  25.6 x 33.5 mm board, 19 x 15.5 x 15 mm relay can, 3-pin header, screw
  terminal), attached to J3 with offset (0, 0, 8.5). Simplified representation,
  no vendor STEP. The render shows the relay can rising to ~25 mm and cutting
  through the BME280/BH1750 module space - the fit conflict in 3D.

## KY-019 right-angle mount + resize (done)

- Board enlarged to **46 x 94 mm**, R3 (width for 33.5 module + 8.6 socket
  body; length for the 25.6 mm module depth below the sensors).
- J3 back to `PinSocket_1x03_P2.54mm_Horizontal` at (44, 76.56), rot 0:
  socket body x 33.9-42.5, opening faces the module (left), pads at x 44.
- KY-019 occupies x 1-34.5, y 66.3-91.9: clears BME280 (ends y 54.5) and
  BH1750 (ends 61.6). Mounting holes at (3,3), (43,3), (3,91.5), (43,91.5).
- `lib/models/ky019.step` rebuilt: right-angle pins, PCB, relay can, screw
  terminal, header, and SMDs with end caps / SOT-23 leads; attached to J3 at
  offset (-10.1, 0, 2.0). Silk label `KY-019` at (40.5, 85).
- Re-routed and zones refilled: 0 errors, 0 unconnected, 2 warnings
  (U1 USB silk past top edge, U2 pin-1 silk).
- Schematic already points J3 at the horizontal socket footprint - unchanged.

## Notes

- Fusion MCP: `http://127.0.0.1:27182/mcp`.
- KiCad MCP moved to `~/mcp/KiCAD-MCP-Server` (was under iCloud `~/Documents`,
  where `import kipy` took 91 s and blew the 30 s startup timeout; now 2.4 s).
  `~/.claude.json` updated; venv rebuilt with `kicad-python` (import name kipy).
- KiCad 3D viewer: File → Revert + Reload 3D cache.
- Plug-and-play: male pin rows on ESP32-C3, LD2410C, BME280, BH1750; female
  sockets on the carrier; relay/button remain screw terminals.
