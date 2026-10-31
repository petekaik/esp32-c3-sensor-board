# Faceplate stone texture

The compact faceplate relief is sampled from **Rustic Stone Wall 02** by
Poly Haven. Poly Haven assets are **CC0 1.0 Universal** (public domain).

- Asset page: https://polyhaven.com/a/rustic_stone_wall_02
- Displacement 2K (used for geometry): `rustic_stone_wall_02_disp_2k.jpg`
  — https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/rustic_stone_wall_02/rustic_stone_wall_02_disp_2k.jpg
- Diffuse 1K (used for the preview render): `rustic_stone_wall_02_diff_1k.jpg`
  — https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/rustic_stone_wall_02/rustic_stone_wall_02_diff_1k.jpg
- Downloaded 2026-10-31.

Used by [`tools/blender/make_compact_faceplate.py`](../../tools/blender/make_compact_faceplate.py).
The faceplate maps a 300 mm tile of the stone texture onto the 39.5 × 82.5 mm
plaque (`TILE` in the script), which turns the slate courses into ~3–6 mm
relief at print scale.

A wood alternative was also checked: Poly Haven **Bark Brown 02**
(https://polyhaven.com/a/bark_brown_02, also CC0). Swap the two paths and the
`TILE` value if you want a bark/wood plaque instead of stone.
