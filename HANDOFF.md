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
