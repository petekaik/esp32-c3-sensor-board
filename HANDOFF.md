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
- Routed with Freerouting (Java 25 image): 225 tracks / 6 vias, 0 unrouted;
  0.25 mm traces, 0.20 mm clearance, 0.8/0.3 mm vias (0.25 mm annular),
  untented (0.9 mm mask openings), 50 µm mask expansion and 0.15 mm silk for
  AISLER's 35 µm rules. U2 pin-1 silk moved off pad 1 (silk-on-pad is not
  supported by AISLER).
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


## Session resume (2026-10-30)

### Where things are
- Repo: `github.com/petekaik/esp32-c3-sensor-board` (public). Pages live at
  `http://gitpages.morgeweb.com/esp32-c3-sensor-board/` (served from `main` / `docs`,
  custom account domain). Landing page is `docs/index.html`; variant pages are
  generated HTML next to their .md sources.
- KiCad project: `hardware/esp32-c3-sensor-board-rev2.kicad_pro` (46 x 89 mm rev2).
  DRC 0 errors / 0 unconnected / 2 known warnings; ERC 0.
- Fabrication: `fabrication/esp32-c3-sensor-board-rev2-gerbers.zip` (8 files),
  `bom-jlc.csv`, `cpl-jlc.csv`, `QUOTE.md`.
- Docs: `README.md`, `docs/pinout.md`, `docs/pricing.md`, `docs/BOM.csv`,
  `docs/variants/*.md|html`, `tools/aisler_quote.py`, `tools/kicad-plugin/`.
- Case: Fusion document `Sensorbox v4` (cloud, saved). Bodies: TRAY_FLOOR,
  TRAY_WALLS (with rails), MOUNT_BOSS, STANDOFF_1..4, COVER_SLIDE + the imported
  board assembly.

### Environment facts
- KiCad MCP moved out of iCloud: `~/mcp/KiCAD-MCP-Server`, config in
  `~/.claude.json` (backup `.bak-mcp-move`). Tools only register at session start;
  if missing, restart Claude Code (server must be running).
- `kicad-cli` at `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.
- Fusion MCP: `http://127.0.0.1:27182/mcp` (Fusion must be running).
- FreeRouting: `docker run --rm -v /tmp:/work -v ~/.kicad-mcp:/data
  eclipse-temurin:25-jre java -jar /data/freerouting.jar -de in.dsn -do out.ses`.

### Pending work, highest first
1. Case fixes in Fusion (rebuild tray+cover in one pass, after deleting the
   existing TRAY_*/COVER_* bodies):
   - trim the slide rails so they stop at the USB clearance line (`rail y1 = iy1`);
     currently they run to `oy1` and appear as strips floating in the open USB end;
   - `wallTop = tallest component + 3 mm` (relay top is 18.1 mm; ceiling at 19.1 is
     only 1 mm clear and the cover's inward lips sit in the same band);
   - move the rail lips/grooves to mid-wall (z ~15) rather than at the top;
   - rebuild as ONE base feature, then verify the body list has no `(1)` duplicates.
2. Relay 3D in the case: `kicad-cli pcb export step` ignores J3's 3D-model transform,
   so the relay lands at raw coordinates (x ~ -43). J3 currently carries only the
   socket model; drop `lib/models/ky019.step` into the Fusion assembly manually at
   board x 0.5-33.9, y -62.55..-88.45, z 1.0-18.1.
3. Optional: add the fab/quote outputs and new docs to git (they are committed up to
   the earlier documentation commit; fabrication/, tools/, docs/pricing.md are new).
4. Nice-to-have: corner fillets on the case, lid fit check, snap-bump tuning.

### Known quirks
- `FusionDocument.saveAs` needs a DataFolder argument through the MCP bridge, so the
  document could not be renamed to plain "Sensorbox"; it is `Sensorbox v2...v4` in the
  data panel - rename there if wanted.
- Aisler has no public REST pricing API; `tools/aisler_quote.py` uses their published
  formula (EUR12 job fee + 0.067 EUR/cm2 x qty). Live quotes need an access key + MCP.
- JLCPCB asks for BOM/CPL only for assembly; our board is THT + modules, so order
  bare PCB and hand-solder.


## Session resume (2026-10-31) - case candidates in Fusion + Blender

### State
- Fusion document **Sensorbox v6** (cloud, saved 2026-10-31).
- The v4/v5 candidates (TRAY_SHARED, TRAY_SHARED_WALLS, CAND_A/B/C, Move1..3) were
  **never saved** and were lost when the app closed. The saved document had only the
  old case: TRAY_FLOOR, TRAY_WALLS, MOUNT_BOSS, COVER_SLIDE, STANDOFF_1..4.
- Candidates rebuilt by script on 2026-10-31 from the surviving `COVER_SLIDE`
  (which already carries the USB-C opening, grommet, BH window, 5 BME louvres and
  slide rails). Everything is a TemporaryBRepManager boolean, one body per
  base feature — adding three bodies in one base-feature edit keeps only the last.
  Build recipe (all mm, case frame x -6.5..50.25, y -91.25..4.3, R14 corners):
  - `base` = COVER_SLIDE ∩ rounded prism; + internal wall x -5.5..49.25,
    y -45.5..-44, z 14..22.5 (separates radar vents from BME louvres).
  - openings cut **last**, through any added top: 5 louvres x 3/6/9/12/15 +1.6,
    y -56..-46.5; BH window x 22..33, y -61..-50; 3 radar vents x 18/24/30 +2.6,
    y -40..-26; all from z 21 to 28.
  - A stepped: + box x 1.5..42.25, y -83.25..-5.7, z 24.4..26.5.
  - B wavy: three crests — cylinders r 89.6, axis along X at y -84/-44/-4,
    top z 25.6, clipped to y ±14 and to the prism.
  - C ribbed: + three ribs 3 mm wide at x 12/22/32, y -83.25..-5.7, z 24.4..26.7.
  - Every top is re-clipped to the prism so nothing overhangs the rounded outline.
- Renders: `case/renders/cand_{a_stepped,b_wavy,c_ribbed}_iso.png` (+ b side view).
- Blender: addon `blender_mcp.py` installed for 5.2, MCP server `uvx mcp-for-blender`
  (user scope), tools available. /tmp/sensorbox_case.stl (old case, all bodies merged)
  was imported once; scene units set to mm.
- Shared case parameters: board 46x89 mm, PCB z 0..1.51; clrL 2.5 (wire channel),
  others 0.25, USB side 0.3; wall 2; floor 2 mm at z -3.5..-1.5; standoffs 1.5 mm;
  wallTop 22; cover top 24.5. Openings: rounded USB-C 9.2x3.4 R1.6 at x22,z13.6;
  grommet D8 at x36,z4; BH window 11x11; 5 BME louvres 1.6x9.5; 3 radar vents.

### Next steps (in order)
1. Pick a candidate with the user.
2. Export the chosen cover + the tray as STL (CASE_EXPORT component pattern:
   copy bodies into a new component, then exportManager.createSTLExportOptions(comp, path)).
3. Blender artistic pass, then return a STEP/STL; keep Fusion as dimensional master.
4. Constraints to preserve: smallest envelope, USB-C flush (0.3 mm wall engagement),
   radar kept in its own pocket with an internal wall, BME louvres not shared with
   radar exhaust, BH clear window, printable flat without supports.
5. Nice-to-have: corner fillets on the tray, lid fit check, snap-bump tuning.

### Environment
- Fusion MCP http://127.0.0.1:27182/mcp; Blender MCP `uvx mcp-for-blender`;
  KiCad MCP `~/mcp/KiCAD-MCP-Server` (reconnect at session start).
- kicad-cli: /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
- Fusion MCP quirks: long script calls and screenshots over ~700 px often exceed the
  idle timeout even though the work completes — verify with a cheap read-only script
  afterwards. `body.deleteMe()` inside a base-feature edit can take other bodies with it.
- Committed as `cc315db`: case/, fabrication/, tools/, docs/pricing.md, ky019.step,
  board, HANDOFF/README. Later this session: `case/renders/`.

## Faceplate route (organic, 2026-10-31)

The three rounded-corner covers were rejected: rounding the lid exposed the square
tray underneath. New route — a flat faceplate taken from the cover's top rectangle,
with the mandatory openings, sculpted in Blender.

- **Generator:** `tools/blender/make_faceplate.py`, run in Blender with
  `exec(open('.../make_faceplate.py').read())`. It rebuilds, sculpts and exports the
  STL in one go; tune the constants at the top rather than editing the mesh.
- **Part:** `case/faceplate_organic.stl` — 56.75 x 95.55 mm, z 22..25.35, occupying
  the `COVER_SLIDE` top-plate volume. Manifold (0 non-manifold edges), 41.6k tris.
- **Shape:** heightfield top — flat 3 mm border rim at z 24.5, deck recessed to 23.5,
  vein field of stretched fbm contours (grain along the length) rising to ~25.3.
  0.5 mm grid. Heightfield → no undercuts, prints flat without supports.
- **BH1750:** lofted funnel, exact 11 x 11 at the bottom face z 22, flaring through
  6.4 to an organic lobe (~18 mm) at the surface. Monotonic, so no undercut.
- **Openings:** five louvres and three radar vents cut clean through the deck; roots
  are masked 0.4–2.4 mm clear of each so nothing is blocked. Verified: 0 bottom
  faces inside any opening.
- **Not yet in Fusion:** the faceplate is still a standalone STL. To finish the case,
  remove `COVER_SLIDE`'s top plate, add a seating lip, and fit the faceplate.
- Blender 5.2 scene keeps `faceplate` plus the hidden `sensorbox_case` reference.

### Faceplate integrated (2026-10-31)

Fusion **Sensorbox v6** now holds the assembled case:
- `TRAY_UNION` — the seven tray bodies unioned into one solid (57 faces).
- `COVER_OPEN` — `COVER_SLIDE` with everything above z 22 removed (open top) plus a
  2 mm seating ledge at z 21..22 inset from the cavity (x -3.5..47.25, y -89.25..0.3).
- `FACEPLATE` — mesh body from `case/faceplate_organic.stl`, seated at z 22..25.35.
- Hidden archive (do not delete again, see below): `COVER_SLIDE`, `CAND_A/B/C`,
  the original `TRAY_FLOOR/WALLS/MOUNT_BOSS/STANDOFF_*`.

Print-ready STLs: `case/tray.stl`, `case/cover_open.stl`, `case/faceplate_organic.stl`.

**Fusion gotchas found the hard way**
- `BRepBody.deleteMe()` inside/after a base-feature edit can remove sibling bodies —
  it cost the tray bodies twice. Never delete when a rename + hide will do. Recover
  by closing without saving and reopening the last saved version.
- `MeshBodies.addByTriangleMeshData(coords, coordIdx, normals, normalIdx)`. STL
  triangles must be wound so Fusion does not backface-cull them — the first import
  rendered see-through until the winding and normals were flipped.
- A new body's `name` set inside the same base-feature edit often does not stick;
  rename it in a later call (`Body103` -> `TRAY_UNION`).
- Export right after adding a body in the same script can silently write nothing;
  re-run the export in a fresh call.

## Session 2026-10-31 — vendor-assignable BOM + three-vendor pricing

### Schematic
- `U1` replaced by `U1A`/`U1B` (`Connector_Generic:Conn_01x08`, at
  92.71/99.06 and 118.11/99.06), footprints
  `Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical`.
  Existing global labels re-used in place; no wires.
- `U2` replaced by `Conn_01x05` at 193.04/100.33, footprint kept as
  `sensor-board:ld2410c`. `J1`/`J2` values renamed to connector part names.
- ERC: **0 violations**.
- KiCad quirk: the BOM exporter prints `U1A?`/`U1B?` because single-unit
  symbols with a unit-letter suffix are treated as unannotated. The netlist and
  PCB use `U1A`/`U1B` correctly; do not run "annotate" (it would rename them).

### PCB
- U1's custom 2x8 footprint removed; two standard 1x8 sockets at
  `U1A (29.62, 2.31)` and `U1B (14.38, 2.31)`, 0°. `U1A` carries the ESP32-C3
  module STEP (`offset -7.62,-8.89,8.5`, rot 0).
- IO6 track rerouted at the U1B pad-1 corner (pad 1 is square in the standard
  footprint; the old route clipped it).
- U2 pad 3 carries `unconnected-(U2-Pin_3-Pad3)` for schematic parity.
- DRC: **0 errors, 0 unconnected**, 24 warnings (21 silk overlap, 3 silk edge;
  baseline was 28). Schematic parity: only the 4 pre-existing H1–H4
  "exclude from BOM" notices.
- Gerbers, drill and the zip were regenerated.

### Aisler
- Project `BEAGDVXB` (`esp32-c3-sensor-board-rev2`), new revision imported.
  10 assembled lines assigned; J3 excluded (hand-solder). Modules are plug-in
  and have no PCB BOM line.
- Live BOM (MCP): €7.28 at MOQ for one board; ~€10.3 of parts for 5 boards.
- J5 uses Samtec `SSW-114-01-T-S` because LCSC `C41417326` is not in Aisler's
  catalogue; shunts (`C5305`) are hand-fit and have no CAD line.

### Files
- `fabrication/assembly/vendor-neutral-bom.csv` — LCSC + Aisler MPN filled.
- `fabrication/assembly/jlcpcb/` — `bom-jlcpcb.csv`, `cpl-jlcpcb.csv`,
  `gerbers-jlcpcb.zip`, `netlist-jlcpcb.ipc`, `designators-jlcpcb.csv`,
  generated by Fabrication Toolkit 5.3.1. J3 is filtered from BOM/CPL.
  Mirrored at `fabrication/bom-jlc.csv` / `fabrication/cpl-jlc.csv`.
- `fabrication/assembly/pcbway/cpl-pcbway.csv` — part-centre positions,
  bottom-left/Y-up, generated from the toolkit CPL.
- `docs/pricing.md` — three-vendor comparison.

### Fabrication Toolkit (JLCPCB) — installed 2026-10-31
- Installed from release 5.3.1 into
  `~/Documents/KiCad/10.0/3rdparty/plugins/com.github.bennymeg.JLC-Plugin-for-KiCad`.
  KiCad must be restarted to show the toolbar button; the CLI works headlessly.
- The board footprints now carry a hidden `LCSC` field (and the schematic
  symbols a matching `LCSC` property). `U2` also has `FT Rotation Offset = 90`
  because the custom `ld2410c` footprint has no standard-socket equivalent.
- Regenerate:
  ```
  cd ~/Documents/KiCad/10.0/3rdparty/plugins/com.github.bennymeg.JLC-Plugin-for-KiCad
  PYTHONPATH=. /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
    -m plugins.cli -p /Users/petekaik/projects/esphome-sensor-board/hardware/esp32-c3-sensor-board-rev2.kicad_pcb \
    -nI -t -f -e
  ```
  Output lands in `hardware/production/` (`bom.csv`, `positions.csv`,
  `netlist.ipc`, `<board>.zip`). Filter the `J3` rows out of the BOM/CPL before
  copying to `fabrication/assembly/jlcpcb/`.
- The toolkit's CPL is part-centre and uses a negative-Y origin; keep it paired
  with the toolkit's gerber zip. Do not mix it with the generic
  `fabrication/*-gerbers.zip`.
- `hardware/production/` is a build artifact (gitignored).

## Session 2026-10-31 — rev3 1×16 breakout

- New project `hardware/esp32-c3-sensor-board-rev3.*`, copied from rev2; project
  instance names/sheet path rewritten to rev3. Rev2 is unchanged and remains the
  ordered baseline.
- **J5: 1×14 → 1×16**, standard `PinSocket_1x16_P2.54mm_Vertical` at (40, 25),
  numeric order after GPIO2:
  `3V3 · 5V · GND · GPIO0 · GPIO1 · GPIO2 · GPIO3 · GPIO4 · GPIO5 · GPIO6 ·
  GPIO7 · GPIO10 · SDA · SCL · RX · TX`.
  J3 (relay) and J4 (button) stay; GPIO3/GPIO4 are duplicated on J5. J5 has
  LCSC C7499334 (Megastar 16P female header).
- Schematic J5 rebuilt as `Connector_Generic:Conn_01x16` at (199.39, 62.23),
  16 global labels snapped to the pins; ERC 0.
- PCB: old routing cleared (228 tracks/vias), DSN exported, FreeRouting
  (Java 25 image) completed with 0 unrouted / 0 violations, SES imported.
  Freerouting left 44 tracks at 0.187 mm; all were set to 0.25 mm and DRC
  showed no clearance errors.
- DRC after silk cleanup: **0 violations, 0 unconnected**; ERC 0. Schematic
  parity: only the 4 pre-existing H1–H4 BOM-attribute notices.
- J5 breakout silkscreen labels replaced with the 16 new names; `REV2` silk
  changed to `REV3`.
- Rev3 gerbers/drill/zip generated under `fabrication/esp32-c3-sensor-board-rev3-*`.
- Variant docs updated: relay rev3 keeps J3/J4 with the 1×16 row; compact
  variants drop **J3 and J4** and use the same 1×16 row (all header pins on J5).
- BME680 variants: standard CJMCU-680 has `SDO, CS` order, opposite to J1's
  `CSB, SDO`; require a 6-pin crossover adapter or a CS-before-SDO clone.

### Compact board (2026-10-31)
- `hardware/esp32-c3-sensor-board-compact.*` — **34 × 76 mm** R3, no J3/J4.
  Stacked column: U1 at the top (U1A 24.62,2.31; U1B 9.38,2.31), LD2410C at
  (17,33), BH1750 J2 at (24.79,44.92) rot 0 (body landscape, aligned with the
  radar), BME280 J1 at (25,60.55) rot 0 (body portrait), J5 1×16 at (31,24),
  JP1/JP2/JP3 at (5/8.6/12.2,60), holes at (3,3), (31,3), (3,73), (31,73).
  BH1750 and BME280 are rotated 90° from the old compact layout.
- The 34 mm width leaves no room for 16 on-board J5 pin labels; the breakout
  pinout stays in `docs/pinout.md`. The J5/U2 local footprints and schematic
  fields are unchanged.
- Routing: FreeRouting (0 unrouted), all tracks normalised to 0.25 mm,
  zones refilled. Added left-edge GND stitching vias at (1.5,30/45/55) and
  bottom GND tracks at y75.
- DRC: **0 violations, 0 errors**; ERC 0; parity only the 4 pre-existing
  H1–H4 notices. KiCad reports **3 GND-zone connectivity notices** between
  pour islands; no pads or signal tracks are unconnected (GND is continuous
  through the through-hole pads and stitching vias).
- Gerbers/drill/zip: `fabrication/esp32-c3-sensor-board-compact-*`.
- The enclosure front must move the radar, BH window and BME louvres to the
  new stacked positions; the current case is for the old layout.
- Rev3 and rev2 are unchanged; rev2 remains the ordered baseline.

### Compact case (2026-10-31)
- Fusion document **Sensorbox Compact v2** in the `Modules` project. Imported
  the compact board STEP (`kicad-cli pcb export step --output /tmp/compact-board.step
  hardware/esp32-c3-sensor-board-compact.kicad_pcb`) and built the case around
  it. Bodies: `TRAY_COMPACT`, `COVER_COMPACT`; hidden `COVER_SCREW_TEST`.
- Envelope **41 × 84 × 24 mm** (x −3.5…37.5, y −80…4, z −3.5…20.5).
  2 mm floor at z −3.5…−1.5, 2 mm walls to z 18.5, 1.5 mm standoffs with Ø2.5
  M3 pilots, 2 mm cover plate z 18.5…20.5 with a 1.5 mm press-fit lip. Tray
  outer corners R3, cover R1.5. No wiring channel.
- Openings: USB-C 9.2 × 3.4 at x 17, z 13.6; J5 1×16 side slot 42 × 8.5 on the
  right wall; 3 radar vents 3 × 10; BH1750 11 × 11 window; 5 BME280 louvres
  1.6 × 9.5; 3 ESP32 side vents. Cover walls at y −42.6 and −24.4 separate the
  radar pocket from the BH/BME side. Two wall-mount keyholes through the floor
  at x 10/24, y −45.
- Print files `case/compact_tray.stl` (1780 tris) and `case/compact_cover.stl`
  (384 tris); both manifold, 0 boundary/non-manifold edges. See
  `case/README.md` for print notes.
- The cover is a friction/press fit; the PCB is fixed with four M3
  self-tapping screws from the top into the standoffs with the cover off.
- The base cover is printable without the decorative faceplate.

### Compact decorative faceplate (2026-10-31)
- Blender 5.2 scene `case/compact_faceplate.blend`; generator
  `tools/blender/make_compact_faceplate.py`.
- `case/faceplate_compact.stl` — 39.5 × 82.5 × 3.88 mm, bottom z 20.5. It sits
  on the cover top, inset 0.75 mm from the 41 × 84 cover for a shadow gap;
  tape/glue it in place. Its openings match the cover: 3 radar vents, 5 BME
  louvres, and an 11 × 11 BH funnel flaring to a raised “eye” with 16 short
  rays and a ring.
- The stone field is a heightfield sampled from the CC0 Poly Haven **Rustic
  Stone Wall 02** 2K displacement map, mapped at 300 mm per tile; the diffuse
  1K map drives the preview material. Sources/licence in
  `case/textures/README.md`. A CC0 wood alternative is **Bark Brown 02**.
- STL: 102,028 tris, 0 boundary / 0 non-manifold edges. Renders:
  `case/renders/faceplate_compact.png`, `faceplate_compact_top.png`,
  `compact_case_faceplate.png`.
- Print bottom-face-down, no supports; plain PLA/PETG or a mineral stone PLA,
  never carbon- or metal-filled in front of the radar or BH1750.

### Compact case: ESP32 stack fix (2026-11-01)
- The imported board STEP modelled the Super Mini PCB at 8.5 mm, directly on
  the female sockets, and had no male pin rows. Physically the stack is
  8.5 mm socket + 2.5 mm male-header plastic = **11 mm** to the module PCB.
- In Fusion, imported two `PinHeader_1x08_P2.54mm_Vertical` STEP rows
  (`/Applications/KiCad/…/Connector_PinHeader_2.54mm.3dshapes/`) at the two
  socket origins (0.938, −0.231) and (2.462, −0.231) cm, z **1.2595 cm**,
  rotated 180° about local Y so the long pins point down into the sockets and
  the 2.5 mm plastic lands on the socket tops.
- The ESP32 STEP origin is the **PCB mid-plane** (PCB 0.9 mm thick), not its
  bottom; the module occurrence was then set to z **1.3045 cm** so the PCB
  bottom rests on the header plastic at 12.595 mm (11 mm above the carrier).
- The USB-C connector now lines up with the case opening; the pin tops clear
  the cover underside. Document versions: **Sensorbox Compact v2** after this
  fix, **v5** after the case redesign below.
- The KiCad board's 3D preview still places the module at z 8.5 with no male
  headers; this is cosmetic (3D only) and would need an IPC session with the
  compact board open in pcbnew to add the two models.

### Compact case v5 (2026-11-01)
- New component `CASE_V2` in **Sensorbox Compact v6** (Modules project);
  bodies `TRAY_COMPACT` and `COVER_COMPACT` rebuilt there, old `CASE_COMPACT`
  hidden. Roof lowered 1.5 mm: envelope **41 × 84 × 22.5 mm** (z −3.5…19.0),
  tray walls to 17.0, cover plate 17.0…19.0.
- 5 mm lower is not physically possible: the tallest parts are the ESP32
  USB-C shell at 16.6 mm, the 1×8 pin tops at 15.6, BH1750/BME280 at 15.2 and
  the radar at 14.4. A 5 mm drop would put the roof at 13.5 and cut through
  the sensors. The cover has a 0.8 mm underside relief over the USB shell
  (clearance 1.2 mm); the rest has 1.8–2.6 mm.
- USB-C: stadium notch 9.4 × 3.85 at x 17, z 13.35…17.0, open at the top
  under the cover, with a 1.2 mm chamfered mouth; it follows the connector
  shell (13.5…16.6 mm).
- BH1750: single Ø5 sight hole at (14.65, −50.1) with a Ø7 × 0.8 mm
  counterbore on the underside, replacing the 11 × 11 window.
- Radar: 22 × Ø1.6 holes (3.0 mm pitch, staggered) replace the three slots.
  BME280: 18 × Ø1.2 holes (2.2 mm pitch) replace the five louvres.
  Side walls: 36 × Ø1.6 holes in two rows (z 13.2 / 15.4) on each long wall,
  identical on both sides.
- Full-height partition walls at y −24.4…−23.4, −42.85…−42.25 and
  −58.6…−57.8, z 2.0…17.0 (0.5 mm above the PCB), x −1.3…28.5 so they clear
  the J5 socket; the top 14.2…17.0 section stays full width. This gives the
  ESP32, radar, BH1750 and BME280 their own segments. The radar wall was
  centred in the 1.1 mm gap after the first version clipped the radar PCB.
- Print files: `compact_tray.stl` 8796 tris / 440 KB and
  `compact_cover.stl` 4562 tris / 228 KB, both manifold. Exported from the
  CASE_V2 bodies.
- Faceplate regenerated for the z 19.0 roof: 39.5 × 82.5 × 3.85 mm (bottom
  19.0, top 22.85), with the same radar/BME hole fields and a funnel at the
  new BH sensor position (14.65, −50.1). Generator and blend updated.


### Compact case: J5 side slot filled (2026-11-01)
- The 42 × 8.5 mm GPIO-breakout slot in the right wall is not needed. It was
  filled flush and the wall was recut with the same 36-hole vent pattern as
  the left wall (6/4/4/4 groups, z 13.2 / 15.4). J5 is now fully enclosed.
- `compact_tray.stl` regenerated: 8796 tris, manifold; both long walls are
  identical. Docs updated to drop the side-slot reference.

- The two `PinHeader_1x08` occurrences were found back at the origin and the
  ESP32 at z 10.1 in the v5 document (the stack-fix transforms had been lost,
  most likely by the undo operations during the case edit). Restored them to
  (0.938, −0.231, 1.2595) and (2.462, −0.231, 1.2595) cm with the 180° Y
  rotation, module at 1.3045 cm, and saved **Sensorbox Compact v6** with the
  J5 slot filled.
