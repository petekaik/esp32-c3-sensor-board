# Cases

## Compact — 34 × 76 mm board

Print files:

- `compact_tray.stl` — floor, walls, standoffs, USB-C stadium notch, the same
  Ø1.6 vent holes on both long walls and the single keyhole mounting pod.
- `compact_cover.stl` — press-fit lid with the radar and BME hole meshes, the
  Ø5 BH1750 sight hole, the full-height module partitions and the underside
  relief over the ESP32 USB shell.

Fusion master: document **Sensorbox Compact v11** in the `Modules` project.
The current bodies `TRAY_COMPACT` and `COVER_COMPACT` live in component
`CASE_V2`; the older `CASE_COMPACT` component is kept hidden for reference.
The reference board is modelled at the real stack height: 8.5 mm female
sockets + 2.5 mm male-header plastic, so the ESP32-C3 PCB sits 11 mm above the
carrier, with a 1×8 male pin row on each socket.

| | |
|---|---|
| Case envelope | 41 × 84 × 22.5 mm (x −3.5…37.5, y −80…4, z −3.5…19.0) |
| Tray | 2 mm floor at z −3.5…−1.5; cavity x −0.5…34.5, y −76.5…0, z −1.5…17.0 — 0.5 mm clearance on the left, right and bottom, USB edge flush with the top inner wall |
| PCB | z 0…1.5, on four 1.5 mm standoffs with Ø3.2 clearance holes and Ø6.6 × 1.7 mm countersinks in the bottom |
| Cover | 2 mm plate z 17.0…19.0, 1.5 mm press-fit lip with a stadium notch cut back to y −1.7 around the USB-C port so the lip clears the connector; the outer edge has a 9.4 × 2 mm stadium groove continuing the port opening; outer R1.5; 0.8 mm underside relief over the ESP32 USB shell; four poles at the PCB holes with modelled **M3×0.5 blind threads, 8 mm deep**; the lid top is solid |
| Outer corners | R3 tray |
| Openings | USB-C stadium 9.4 × 3.85 at x 17, z 13.35…17.0, cut through the 4 mm top wall from y −0.2 and open at the top under the cover, with a 1.2 mm chamfered mouth — the PCB edge sits on the inner wall and the connector sits in the notch; radar 22 × Ø1.6 holes (3.0 pitch, staggered); BH1750 Ø5 sight hole at (14.65, −50.1) with a Ø7 underside counterbore; BME280 18 × Ø1.2 holes (2.2 pitch, staggered); the same 36 × Ø1.6 side vents in two rows on both long walls |
| Partitions | full-height walls at y −24.4…−23.4, −42.85…−42.25 and −58.6…−57.8, z 2.0…17.0 (0.5 mm above the PCB), x −0.5…28.5 to clear the J5 socket — ESP32, radar, BH1750 and BME280 each in their own segment |
| Wall mount | One keyhole in a Ø28 × 5 mm pod on the back at (17, −45); the screw head sits in the pod cavity outside the sealed case, so it cannot reach the PCB. The case stands 5 mm off the wall on the pod. |

Board fixing: **four M3×12 countersunk screws from the bottom**. Each goes up
through a Ø6.6 × 1.7 mm countersink and Ø3.2 clearance hole in the floor and
standoff, through the PCB, and into a threaded pole on the lid; the PCB is
clamped between the standoff and the pole. The screw heads sit flush/recessed
in the bottom face. Run an M3×0.5 tap through the printed pole threads if they
come out tight. Remove the case from the wall to reach the screws. Trim the J5
socket pins flush on the underside before fitting the board — the 3D socket
model shows them 1.5 mm below the PCB and the floor is 1.5 mm below the board.

The cover is a press-fit lip plus **four M3×12 screws from the bottom** into threaded poles on the lid. The lid top is solid, so the faceplate sits flush and no screw holes show. The wall mount is a single keyhole in a back pod; the wall screw stays in the pod cavity, outside the sealed case. The lid and base are separate components `LID` and `BASE` in Fusion.

Printer notes: PLA or PETG, 0.2 mm layers, 3 perimeters. Print the tray
floor-down and the cover outer-face-down; no supports. Never use carbon- or
metal-filled filament in front of the radar or the BH1750 window.

The compact case has **no wiring channel**; the 3.5 mm perimeter margin is all
the space around the board. The J5 breakout is fully enclosed — both long
walls carry the same 36-hole vent pattern, with no side slot.

### Decorative faceplate

Optional stone plaque that sits on the cover top (z 19.0):

- `faceplate_compact.stl` — 39.5 × 82.5 × 3.85 mm, bottom z 19.0, top
  22.85. It is inset 0.75 mm from the 41 × 84 cover, leaving a fine shadow
  gap; fix with double-sided tape or a few drops of glue.
- The field is a heightfield sampled from the CC0 **Rustic Stone Wall 02**
  displacement map (Poly Haven), with a flat 3 mm rim, a carved border groove,
  a raised ring and 16 short rays around the BH1750 opening. It carries the
  same 22 × Ø1.6 radar holes and 18 × Ø1.2 BME holes as the cover, plus the
  funnel centred on the BH1750 sensor at (14.65, −50.1).
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
