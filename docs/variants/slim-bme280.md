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
| ESP32-C3 module body | x 12–30, y 0.8–23.3; USB-C at the top edge, centred x 21 |
| U1A (right 1×8) | `PinSocket_1x08_P2.54mm_Horizontal` at (40.1, 3.36), rot 0 |
| U1B (left 1×8) | `sensor-board:PinSocket_1x08_P2.54mm_Horizontal_MirrorX` at (1.9, 3.36), rot 0 |
| LD2410C body | x 15.16–31.16, y 24.58–46.58 |
| U2 (radar 1×5) | `PinSocket_1x05_P2.54mm_Horizontal` at (40.1, 30.5), rot 0 |
| BH1750 body | x 11.48–30.53, y 47.84–62.07 |
| J2 (BH 1×5) | `PinSocket_1x05_P2.54mm_Horizontal` at (40.1, 50), rot 0 |
| BME280 body | x 12.36–24.30, y 65.73–81.22 |
| J1 (BME 1×6) | `sensor-board:PinSocket_1x06_P2.54mm_Horizontal_MirrorX` at (1.9, 68), rot 0 |
| J5 (GPIO 1×16) | `PinSocket_1x16_P2.54mm_Vertical` at (4, 26), **unpopulated (DNP)** |
| Mounting holes | none |

Both ESP32 rows use pad 1 at the top, keeping the existing pin map. The
mirrored footprints keep the pad order (+Y from pad 1) while putting the
socket body on the opposite side; a plain 180° rotation would reverse the
pad order.

F.SilkS carries open-sided placement outlines and names for all four modules
(`MOD1`–`MOD4`), a `USB` mark at the top, and a `GPIO 1x16 (DNP)` note beside
J5. The outlines are open on the socket side so they do not cross the socket
silkscreen.

## Electrical

- Pin map unchanged from the compact / `doorbell.yml`.
- BME280 CSB hard-wired to 3V3 and SDO to GND (0x76); BH1750 ADDR to GND
  (0x23). JP1/JP2/JP3 jumpers removed — I²C-only, addresses fixed in hardware
  and matched by the ESPHome YAML.
- J5 pin row is present as bare holes; the socket need not be fitted.

## Verification

- ERC: **0 violations**.
- DRC: **0 errors, 0 unconnected, 4 warnings** — 2 silkscreen-edge and 2
  silkscreen-overlap notices from the placement outlines and the mirrored
  socket reference text. No copper, clearance, width or unconnected-item
  errors.
- Routing: Freerouting best-of-3, 141 segments / 8 vias (4 signal + 4 GND
  stitching); all 16 nets connected. All tracks normalised to 0.25 mm; vias
  0.8/0.3 mm; clearance 0.2 mm.
- GND pours on F.Cu and B.Cu (0.5 mm inset, solid pad connection).

## Build notes

- Solder the right-angle female sockets flat on the carrier.
- Solder a bent male row to each module's solder side. Trim the horizontal run
  so the pin enters the socket with the module edge at the opening (~1.4 mm).
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
