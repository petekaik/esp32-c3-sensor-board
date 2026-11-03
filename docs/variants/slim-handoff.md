# Slim PCB — session handoff (2026-11-03)

**Branch:** `worktree-slim-pcb` (pushed; design at commit `90108ce`, this
handoff added after it; clean tree when written)
**Project:** `hardware/esp32-c3-sensor-board-slim.kicad_pro`
**Board:** 42.1 × 84.1 mm, 2-layer, no relay/button.

The slim variant mounts all four modules — ESP32-C3 Super Mini, LD2410C,
BH1750, BME280 — on **flat right-angle 2.54 mm female sockets**, with a 90°
bent male row soldered to each module's solder side. Stack: carrier /
horizontal pins / module PCB. Module bodies face up and are centred on
x = 21 (the USB-C centreline).

## Current layout

| Ref | Part | Position (mm) | Rot | Notes |
|---|---|---|---|---|
| U1A | 1×8 horizontal, mirrored-X | 17.14, 3.36 | 0 | ESP32 right row, mouth +X |
| U1B | 1×8 horizontal, mirrored-X | 1.9, 3.36 | 0 | ESP32 left row, mouth +X |
| U2 | 1×5 horizontal `_Rev` | 15.9, 25.1 | 90 | LD2410C; pad 1 at far end |
| J2 | 1×5 horizontal `_Rev` | 16.6, 54.6 | 180 | BH1750; pad 1 at far end |
| J1 | 1×6 horizontal mirrored-X `_Rev` | 13.6, 60.125 | 0 | BME280; pad 1 at far end |
| J5 | 1×16 vertical, unpopulated | 3.5, 26.95 | 0 | bare holes |
| MOD1 | ESP32 outline + 3D | 21.0, 12.25 | 0 | 18 × 22.5 body |
| MOD2 | LD2410C outline + 3D | 21.0, 32.5 | 90 | 22 × 16 body |
| MOD3 | BH1750 outline + 3D | 21.0, 49.5 | 180 | 18.5 × 13.9 body |
| MOD4 | BME280 outline + 3D | 21.0, 66.0 | 0 | 12 × 15.2 body |

No mounting holes. BME280 CSB→3V3, SDO→GND (0x76); BH1750 ADDR→GND (0x23);
JP1–JP3 removed; ERC 0.

**Reversed pads:** because the LD/BH/BME pin rows are soldered on the
underside and fold under the PCB, U2/J2/J1 use the `_Rev` footprints (pad 1 at
the far end). The schematic pin numbers/net names are unchanged. Footprints:
`sensor-board:PinSocket_1x05_P2.54mm_Horizontal_Rev`,
`sensor-board:PinSocket_1x06_P2.54mm_Horizontal_MirrorX_Rev`.

## 3D assembly

| Ref | Models |
|---|---|
| MOD1 | `esp32c3-supermini.step` offset (0, 0, 5.7); two `PinHeader_1x08_P2.54mm_Horizontal` at (−8.9, −8.3, 1.0) rot (−180, 90, 0) and (6.4, −8.3, 1.0) rot (0, 90, −180) |
| MOD2 | `ld2410c-nopins.step` offset (0, 0, 5.0) rot Z 270; `PinHeader_1x05` at (5.46, −5.08, 2.54) rot Z 180 |
| MOD3 | `bh1750-good-baked.step` offset (−7.75, 4.95, 5.0) rot Z 180; `PinHeader_1x05` at (−7.75, 4.95, 2.54) rot 0 |
| MOD4 | `bme280-good-baked.step` offset (4.4, −6.35, 5.0) rot 0; `PinHeader_1x06` at (4.4, −6.35, 2.54) rot Z 180 |

`ld2410c-nopins.step` is the vendor STEP with the five `HDR2.54-1P` straight-pin
assemblies removed (the product geometry remains but is unreferenced).
The mirror-X socket models use scale 1 + Z 180 (not a negative X scale).
Standard 6 mm headers still overlap the ~1.4 mm trimmed-pin sockets in 3D —
expected.

Silk: module outlines/names (open on the socket side); front `USB-C`,
`SLIM R1`; back legends for LD2410C, BH1750, BME280 and `GPIO 1x16 (DNP)`.

## Verification (last run)

- ERC: **0 violations**.
- DRC: **0 violations**, 36 warnings (2 silk-edge, 34 silk-overlap) and
  **2 same-net GND-zone island notices** on B.Cu. No pad, signal track or via
  is unconnected.
- Routing: Freerouting best-of-3, **156 segments / 2 vias**; default 0.25 mm,
  thin traces 0.125–0.187 mm (`min_track_width` 0.12 mm), 0.2 mm clearance.
  GND pour on B.Cu only; the F.Cu pour was dropped because the routing split it
  into isolated islands.

## Measured extents / slimming

| Feature | x | y |
|---|---|---|
| Sockets | 0.12–27.88 | 1.58–74.65 |
| Module bodies | 9.93–32.08 | 0.93–74.65 |

- **Width:** a USB-centred board (centreline x = 21) floors at **≈41.8 mm** —
  the current 42 mm is already the limit. With the USB-C off-centre the board
  could be **≈28.5 mm** (USB ~7 mm off centre).
- **Length:** the module column ends at y ≈ 74.7; the board can shrink
  **84 → ≈76 mm**.

## Open work (next session)

1. **Socket ↔ module pin-row alignment is still rough.** The sockets are a few
   mm off the module pin rows (especially U2/MOD2). Move each socket so its
   mouth sits exactly at the module's pin row, then nudge the angled 3D rows in
   the 3D viewer. Re-route afterwards.
2. **Pin length:** the 3D rows are standard 6 mm headers. Decide trimmed/bare
   pins (~1.4 mm run) or widen the board to ~56 mm for untouched headers.
3. **Resize:** apply length 84 → 76 mm only, or also the off-centre ≈28.5 mm
   width. Both need a new outline + zone + re-route.
4. **Case:** not rebuilt. USB-C opening drops to ≈z 4–6 mm; all front openings
   move to the centred module column. The compact case will not fit.
5. **Copper keep-outs:** the radar-patch and ESP32-antenna carrier-copper
   keep-outs were not re-created.

## Pitfalls

- The MCP flips between the live KiCad GUI (IPC) and the on-disk file (SWIG).
  After MCP/file edits the GUI can hold a stale board and overwrite the file on
  close/save. **Close the project without saving, then reopen** after edits;
  while the GUI holds the board, do not script-edit the `.kicad_pcb`.
- The autorouter produces some 0.125–0.187 mm traces; widening them to 0.25 mm
  creates 0.17 mm clearance misses, hence `min_track_width` 0.12 mm.
- GND-zone island notices are same-net copper fragments (the compact had the
  same); they are not pad/signal disconnects.

## Files touched

- `hardware/esp32-c3-sensor-board-slim.{kicad_pro,kicad_sch,kicad_pcb}`
- `hardware/lib/sensor-board.pretty/PinSocket_1x0{5,6}_P2.54mm_Horizontal_Rev.kicad_mod`
- `hardware/lib/sensor-board.pretty/PinSocket_1x0{6,8}_P2.54mm_Horizontal_MirrorX.kicad_mod`
- `hardware/lib/sensor-board.pretty/module_outline_{esp32c3,ld2410c,bh1750,bme280}.kicad_mod`
- `hardware/lib/models/ld2410c-nopins.step`
- `docs/variants/slim-bme280.md`, `HANDOFF.md`, `CLAUDE.md`, `README.md`

## Open it

```sh
open -a KiCad "/Users/petekaik/projects/esphome-sensor-board/.claude/worktrees/slim-pcb/hardware/esp32-c3-sensor-board-slim.kicad_pro"
```

If you want the slim variant in the main checkout, fast-forward:
`git merge --ff-only worktree-slim-pcb` from `~/projects/esphome-sensor-board`.
