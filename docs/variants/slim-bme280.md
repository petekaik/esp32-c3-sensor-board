# Variant: slim, no relay, BME280 (routed)

**Status:** routed — `hardware/esp32-c3-sensor-board-slim.*`
**Board:** 42 × 84 mm, R3, 2-layer. Wider and taller than the compact, but the
module deck height drops from ~16.6 mm to ~7.5 mm above the carrier.

## Concept

All four modules — ESP32-C3 Super Mini, LD2410C, BH1750 and BME280 — mount on
**right-angle (horizontal) 2.54 mm female sockets** soldered flat to the
carrier. Each module carries a **90° bent male pin row soldered to its solder
(non-component) side**. The stack is three layers:

```
module PCB + sensors        top ≈ 7.5 mm
module PCB 1.6 mm          z ≈ 2.5 mm
male body / female socket  z 0–2.5 mm
carrier PCB                z 0
```

The module lies flat over the carrier, components facing up, extending
sideways from its socket. No vertical 8.5 mm socket standoffs are used.

**Pin run:** the sockets are placed so the socket opening sits at the module
edge, i.e. the bent male pins have a horizontal run of ~1.4 mm. This requires
bare pins or right-angle headers with the plastic body removed/trimmed. An
untouched 6 mm right-angle male header pushes the sockets ~5 mm further out
and the board to ~56 mm wide.

## Layout

| Item | Placement (mm, origin top-left) |
|---|---|
| Board outline | 42 × 84, R3 |
| ESP32-C3 module body | x 12–30, y 1.0–23.5; USB-C at the top edge, centred x 21 |
| U1A (right 1×8) | `sensor-board:PinSocket_1x08_P2.54mm_Horizontal_MirrorX` at (17.14, 3.36), rot 0 |
| U1B (left 1×8) | `sensor-board:PinSocket_1x08_P2.54mm_Horizontal_MirrorX` at (1.9, 3.36), rot 0 |
| LD2410C body | MOD2 outline at (21.0, 32.5), rot 90 |
| U2 (radar 1×5) | `sensor-board:PinSocket_1x05_P2.54mm_Horizontal_Rev` at (15.9, 25.1), rot 90 |
| BH1750 body | MOD3 outline at (21.0, 49.5), rot 180 |
| J2 (BH 1×5) | `sensor-board:PinSocket_1x05_P2.54mm_Horizontal_Rev` at (16.6, 54.6), rot 180 |
| BME280 body | MOD4 outline at (21.0, 66), rot 0 |
| J1 (BME 1×6) | `sensor-board:PinSocket_1x06_P2.54mm_Horizontal_MirrorX_Rev` at (13.6, 60.125), rot 0 |
| J5 (GPIO 1×16) | `PinSocket_1x16_P2.54mm_Vertical` at (3.5, 26.95), **unpopulated (DNP)** |
| Mounting holes | none |

Both ESP32 sockets are mirrored-X and open toward **+X**, so the module
**slides in from the right**. U1A sits under the module's right half; U1B is
just outside the left edge. Both rows use pad 1 at the top, keeping the
existing pin map. The mirrored footprints keep the pad order (+Y from pad 1)
while putting the socket body on the opposite side; a plain 180° rotation
would reverse the pad order.

### Pin order (underside-folded rows)

The LD2410C, BH1750 and BME280 male rows are soldered to the module's solder
side and fold under its PCB, so the pin order along each row is reversed
relative to a socket numbered 1..N from the original end. Those three sockets
use reversed-pad variants:

- `sensor-board:PinSocket_1x05_P2.54mm_Horizontal_Rev` — U2 and J2, pad 1 at
  the far end of the row.
- `sensor-board:PinSocket_1x06_P2.54mm_Horizontal_MirrorX_Rev` — J1, pad 1 at
  the far end, body on the +X side.

The schematic pin numbers and net names are unchanged; pad 1 now lands at the
end the module's pin 1 reaches. U1A/U1B keep the original mirrored-X
footprints (pad order +Y).

F.SilkS carries open-sided placement outlines and names for all four modules
(`MOD1`–`MOD4`), a `USB` mark at the top, and a `GPIO 1x16 (DNP)` note beside
J5. The outlines are open on the socket side so they do not cross the socket
silkscreen.

### Centring and slim-down

The sensor modules are centred on **x = 21**, the ESP32/USB centreline. Assuming
each sensor sits at its module centre, the USB-C, radar array, BH1750 light
sensor and BME280 sensor then share that line. Sockets and modules were moved as
pairs, so the pin rows keep their alignment.

Measured extents after centring:

| Feature | x | y |
|---|---|---|
| Socket copper/courtyards | 0.12–27.88 | 1.58–74.65 |
| Module bodies | 9.93–32.08 | 0.93–74.65 |

- **Width:** a board centred on the USB (x = 21) must reach the left socket
  (x = 0.12) symmetrically, i.e. ≈41.8 mm — the present 42 mm is already the
  floor. If the USB-C may sit off-centre, the board can shrink to ≈28.5 mm
  (just over the socket span), with the USB about 7 mm off the board centre.
  The slide-in ESP32 arrangement (both sockets opening +X) is what makes the
  left side wider than the right.
- **Length:** the module column ends at y ≈ 74.7; the board can shrink from 84
  to ≈76 mm (≈8 mm) without moving any module.

## 3D assembly

MOD1 (the ESP32 placement outline, at 21, 12.25) carries the ESP32-C3 Super
Mini STEP and two `PinHeader_1x08_P2.54mm_Horizontal` models, aligned manually
in the 3D viewer. The module PCB is lifted clear of the 2.54 mm socket bodies;
the exact model offsets/rotations are in the board file.

The sensor module bodies are attached to MOD2/3/4 (`ld2410c-nopins.step`,
`bh1750-good-baked.step`, `bme280-good-baked.step`) with body-centred offsets
and Z ≈ 5 mm, plus one angled right-angle row per module at the module's pin
row, Z = 2.54 mm so the arms land at the socket mouths. The LD2410C body uses a
pin-less copy of the vendor STEP (`ld2410c-nopins.step`, the five
`HDR2.54-1P` assemblies removed) so only the angled row is visible. Nudge the
rows in the 3D viewer once the sockets sit exactly at the module pin rows.

The header model is the standard 6 mm right-angle part. The sockets are placed
for a ~1.4 mm trimmed-pin run, so the standard header's plastic body and long
arms overlap the socket in the 3D view — that is the visual confirmation that
the pins must be trimmed (or bare pins used). An untrimmed header needs the
~56 mm-wide board variant.

The mirror-X socket footprints (U1A/U1B/J1) use scale 1 and a 180° Z model
rotation instead of a negative X scale. The negative scale rendered the
sockets half-transparent; the rotation is visually identical to the standard
sockets used on U2/J2.

## Electrical

- Pin map unchanged from the compact / `doorbell.yml`.
- BME280 CSB hard-wired to 3V3 and SDO to GND (0x76); BH1750 ADDR to GND
  (0x23). JP1/JP2/JP3 jumpers removed — I²C-only, addresses fixed in hardware
  and matched by the ESPHome YAML.
- J5 pin row is present as bare holes; the socket need not be fitted.

## Verification

- ERC: **0 violations**.
- DRC: **0 violations**, 36 warnings — 2 silkscreen-edge and 34 silkscreen-overlap
  notices from the module outlines and labels laid over the sockets. KiCad also
  reports **2 GND-zone island notices** on the B.Cu pour (same-net copper
  fragments); no pad, signal track or via is unconnected.
- Routing: Freerouting best-of-3, 156 segments / 2 signal vias; all 16 nets
  connected. Default track 0.25 mm, autorouter thin traces 0.125–0.187 mm
  (`min_track_width` 0.12 mm), vias 0.8/0.3 mm, clearance 0.2 mm.
- GND pour on B.Cu (solid pad connection). The F.Cu pour was dropped because
  the routing fragmented it into isolated islands; the B.Cu plane carries the
  ground and all GND pads are through-hole.

## Build notes

- Solder the right-angle female sockets flat on the carrier.
- Solder a bent male row to each module's solder side. Trim the horizontal run
  so the pin enters the socket with the module edge at the opening (~1.4 mm).
- **ESP32 insertion:** both U1A and U1B open toward +X. Place the module with
  both bent rows aligned to the socket mouths and slide it in from the right
  edge. Do not fit U1A backwards — the two rows must face the same way.
- Populate the PCB before fitting it into the enclosure; no in-place module
  access is required.
- The enclosure must be rebuilt for the 42 × 84 board and the lower deck.
  The USB-C opening drops to roughly z 4–6 mm, and the radar / BH1750 / BME280
  openings move to the module positions above.

## Open

- Case rebuild.
- Radar-patch and ESP32-antenna carrier-copper keep-outs were not re-created
  on this revision (the old compact keep-out did not match the new module
  positions). Refine in KiCad if RF range/pattern needs it.
