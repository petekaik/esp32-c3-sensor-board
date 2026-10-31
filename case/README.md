# Cases

## Compact — 34 × 76 mm board

Print files:

- `compact_tray.stl` — floor, walls, standoffs, USB-C opening, J5 side slot,
  ESP32 side vents and two wall-mount keyholes.
- `compact_cover.stl` — press-fit lid with the radar vents, BH1750 window,
  BME280 louvres and the internal heat-separation walls.

Fusion master: document **Sensorbox Compact v1** in the `Modules` project.
Bodies `TRAY_COMPACT` and `COVER_COMPACT`; `COVER_SCREW_TEST` is a hidden
archive of a screw-hole trial and is not used.

| | |
|---|---|
| Case envelope | 41 × 84 × 24 mm (x −3.5…37.5, y −80…4, z −3.5…20.5) |
| Tray | 2 mm floor at z −3.5…−1.5, 2 mm walls to z 18.5 |
| PCB | z 0…1.52, on four 1.5 mm standoffs with Ø2.5 mm M3 pilots |
| Cover | 2 mm plate z 18.5…20.5, 1.5 mm press-fit lip; outer R1.5 |
| Outer corners | R3 tray |
| Openings | USB-C 9.2 × 3.4 at x 17, z 13.6; J5 1×16 side slot 42 × 8.5 on the right wall; 3 radar vents 3 × 10; BH1750 11 × 11 window; 5 BME280 louvres 1.6 × 9.5; 3 ESP32 side vents |
| Heat separation | Cover walls at y −42.6 and −24.4 keep the radar pocket away from the BH window and BME louvres |
| Wall mount | Two keyhole slots through the floor at x 10 / 24, y −45 |

Board fixing: four M3 self-tapping screws from the top through the PCB into
the standoffs, with the cover off; the Ø2.5 pilots are 3.5 mm deep, so an
M3 × 6–8 mm screw is right. Trim the J5 socket pins flush on the underside
before fitting the board — the 3D socket model shows them 1.5 mm below the PCB
and the floor is 1.5 mm below the board.

The cover is a friction/press fit; sand the lip if it is too tight, tape or add
screws if it is too loose.

Printer notes: PLA or PETG, 0.2 mm layers, 3 perimeters. Print the tray
floor-down and the cover outer-face-down; no supports. Never use carbon- or
metal-filled filament in front of the radar or the BH1750 window.

The compact case has **no wiring channel**; the 3.5 mm perimeter margin is all
the space around the board. The J5 breakout exits through the right-hand slot.

### Decorative faceplate

Optional stone plaque that sits on the cover top (z 20.5):

- `faceplate_compact.stl` — 39.5 × 82.5 × 3.9 mm, bottom z 20.5. It is inset
  0.75 mm from the 41 × 84 cover, leaving a fine shadow gap; fix with
  double-sided tape or a few drops of glue.
- The field is a heightfield sampled from the CC0 **Rustic Stone Wall 02**
  displacement map (Poly Haven), with a flat 3 mm rim, a carved border groove,
  a raised ring and 16 short rays around the BH1750 opening, and the exact
  radar/BME/BH openings of the cover.
- `compact_faceplate.blend` — Blender 5.2 scene with the compact case,
  faceplate, stone material, camera and lights.
- `renders/faceplate_compact.png`, `renders/faceplate_compact_top.png`,
  `renders/compact_case_faceplate.png` — previews.
- Source texture and license: [`textures/README.md`](textures/README.md);
  generator: [`../tools/blender/make_compact_faceplate.py`](../tools/blender/make_compact_faceplate.py).
- Print bottom-face-down, no supports. Use plain PLA/PETG (or a mineral
  “stone” PLA); do **not** use carbon- or metal-filled filament in front of the
  radar or the BH1750 window.

## rev2 — 46 × 89 mm board (previous)

- `tray.stl`, `cover_open.stl`, `faceplate_organic.stl`
- Fusion document **Sensorbox v8** (Modules project); the old faceplate
  experiments are in `renders/` and the hidden archive bodies.
