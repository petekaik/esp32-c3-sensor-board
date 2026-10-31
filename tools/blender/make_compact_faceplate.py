"""Compact stone faceplate for the 34 x 76 mm sensor case.

Run inside Blender:
    exec(open('/Users/petekaik/projects/esphome-sensor-board/tools/blender/make_compact_faceplate.py').read())

Builds a 39.5 x 82.5 mm plaque that sits on the 41 x 84 mm compact cover
(cover top z 20.5).  The field is a heightfield sampled from the CC0 Poly
Haven "Rustic Stone Wall 02" displacement map, with:

  - a flat 3 mm rim and a carved border groove,
  - a raised ring and 16 short rays around the BH1750 opening ("eye"),
  - the exact radar vents, BME280 louvres and an 11 x 11 mm BH1750 funnel
    at the bottom face, matching the case cover,
  - the stone diffuse map on a UV-mapped material for the preview render.

All geometry is a heightfield plus a loft, so it prints flat on the bed with
no supports and no undercuts.
"""

import bpy
import bmesh
import math
import os
import numpy as np
from mathutils import Vector

BASE = "/Users/petekaik/projects/esphome-sensor-board"
DISP = os.path.join(BASE, "case/textures/rustic_stone_wall_02_disp_2k.jpg")
DIFF = os.path.join(BASE, "case/textures/rustic_stone_wall_02_diff_1k.jpg")
STL = os.path.join(BASE, "case/faceplate_compact.stl")
PNG = os.path.join(BASE, "case/renders/faceplate_compact.png")

# envelope: 0.75 mm inset from the 41 x 84 cover, bottom on z 20.5
X0, X1, Y0, Y1 = -2.75, 36.75, -79.25, 3.25
BOTTOM, DECK, RIM = 20.5, 22.5, 23.5
NX, NY = 114, 238
CX, CY = 17.0, -50.0
TILE = 300.0              # mm of stone map per tile on the plaque
OFF_U, OFF_V = 0.23, 0.41
STONE_AMP = 2.2

OPEN_VENTS = [(8.5, 11.5, -38.0, -28.0), (15.5, 18.5, -38.0, -28.0),
              (22.5, 25.5, -38.0, -28.0)]
OPEN_LOUVRES = [(15.7, 17.3, -71.75, -62.25), (18.2, 19.8, -71.75, -62.25),
                (20.7, 22.3, -71.75, -62.25), (23.2, 24.8, -71.75, -62.25),
                (25.7, 27.3, -71.75, -62.25)]

# ---- stone displacement map ------------------------------------------------
_img = bpy.data.images.load(DISP, check_existing=True)
_w, _h = _img.size
_buf = np.empty(_w * _h * 4, dtype=np.float32)
_img.pixels.foreach_get(_buf)
_arr = _buf.reshape(_h, _w, 4)[:, :, 0]


def stone(x, y):
    u = ((x - X0) / TILE + OFF_U) % 1.0
    v = ((y - Y0) / TILE + OFF_V) % 1.0
    fx, fy = u * _w - 0.5, v * _h - 0.5
    x0, y0 = int(math.floor(fx)), int(math.floor(fy))
    tx, ty = fx - x0, fy - y0
    x0 %= _w
    x1 = (x0 + 1) % _w
    y0 %= _h
    y1 = (y0 + 1) % _h
    a = _arr[y0, x0] * (1 - tx) + _arr[y0, x1] * tx
    b = _arr[y1, x0] * (1 - tx) + _arr[y1, x1] * tx
    return a * (1 - ty) + b * ty


def smoothstep(e0, e1, t):
    t = max(0.0, min(1.0, (t - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def rect_gap(x, y, r):
    return math.hypot(max(r[0] - x, 0, x - r[1]), max(r[2] - y, 0, y - r[3]))


def mask_openings(x, y):
    m = 1.0
    for r in OPEN_VENTS + OPEN_LOUVRES:
        m = min(m, smoothstep(0.35, 1.5, rect_gap(x, y, r)))
    return m


def rays(x, y):
    """Raised eye/sun rays around the BH1750 opening."""
    r = math.hypot(x - CX, y - CY)
    if r < 10.6 or r > 14.8:
        return 0.0
    ang = math.atan2(y - CY, x - CX)
    n = 16
    a = abs(((ang + math.pi / n) % (2 * math.pi / n)) - math.pi / n)
    d = r * math.sin(a)
    return 1.1 * math.exp(-(d / 0.5) ** 2) * \
        smoothstep(10.6, 11.4, r) * (1 - smoothstep(13.8, 14.8, r))


def ztop(x, y):
    d = min(x - X0, X1 - x, y - Y0, Y1 - y)
    rim = 1.0 - smoothstep(3.0, 4.2, d)
    edge = 1.0 - smoothstep(0.0, 0.9, d)
    groove = -0.45 * math.exp(-((d - 4.6) / 0.55) ** 2)
    r = math.hypot(x - CX, y - CY)
    ring = 0.9 * math.exp(-((r - 9.6) / 1.0) ** 2)
    hgt = (stone(x, y) - 0.5) * STONE_AMP
    z = DECK + (RIM - DECK) * rim + hgt * mask_openings(x, y) * \
        smoothstep(9.6, 10.8, r) * (1 - rim)
    z += ring * smoothstep(8.6, 9.1, r) * (1 - smoothstep(11.5, 12.5, r)) * (1 - rim)
    z += rays(x, y) * mask_openings(x, y) * (1 - rim)
    z += groove * (1 - rim)
    z -= 0.8 * edge
    return z


# ---- mesh ------------------------------------------------------------------
old = bpy.data.objects.get('faceplate')
if old:
    old.hide_set(True)
    old.hide_render = True
for name in ('faceplate_compact',):
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

xs = [X0 + i * (X1 - X0) / (NX - 1) for i in range(NX)]
ys = [Y0 + j * (Y1 - Y0) / (NY - 1) for j in range(NY)]
bm = bmesh.new()
top = [[bm.verts.new((xs[i], ys[j], ztop(xs[i], ys[j]))) for j in range(NY)] for i in range(NX)]
bot = [[bm.verts.new((xs[i], ys[j], BOTTOM)) for j in range(NY)] for i in range(NX)]
for i in range(NX - 1):
    for j in range(NY - 1):
        bm.faces.new((top[i][j], top[i + 1][j], top[i + 1][j + 1], top[i][j + 1]))
        bm.faces.new((bot[i][j], bot[i][j + 1], bot[i + 1][j + 1], bot[i + 1][j]))
for i in range(NX - 1):
    bm.faces.new((top[i][0], bot[i][0], bot[i + 1][0], top[i + 1][0]))
    bm.faces.new((top[i][NY - 1], top[i + 1][NY - 1], bot[i + 1][NY - 1], bot[i][NY - 1]))
for j in range(NY - 1):
    bm.faces.new((top[0][j], top[0][j + 1], bot[0][j + 1], bot[0][j]))
    bm.faces.new((top[NX - 1][j], bot[NX - 1][j], bot[NX - 1][j + 1], top[NX - 1][j + 1]))
me = bpy.data.meshes.new('faceplate_compact')
bm.to_mesh(me)
bm.free()
fp = bpy.data.objects.new('faceplate_compact', me)
bpy.context.collection.objects.link(fp)
bpy.context.view_layer.objects.active = fp

uv = me.uv_layers.new(name='UVMap')
for poly in me.polygons:
    for li in poly.loop_indices:
        co = me.vertices[me.loops[li].vertex_index].co
        uv.data[li].uv = ((co.x - X0) / TILE + OFF_U, (co.y - Y0) / TILE + OFF_V)


# ---- funnel + opening cutters ----------------------------------------------
def ring(z, ax, ay, n, mod=None):
    pts = []
    nr = 96
    for k in range(nr):
        th = 2 * math.pi * k / nr
        c, s = math.cos(th), math.sin(th)
        rr = (abs(c) ** n + abs(s) ** n) ** (-1.0 / n)
        m = 1.0 if mod is None else mod(th)
        pts.append((CX + ax * rr * c * m, CY + ay * rr * s * m, z))
    return pts


def funnel():
    rings = [ring(19.5, 5.5, 5.5, 12.0), ring(20.5, 5.5, 5.5, 12.0),
             ring(21.8, 6.6, 6.6, 4.0),
             ring(23.6, 9.0, 8.6, 2.0,
                  lambda th: 1.0 + 0.12 * math.sin(3 * th + 0.7) +
                  0.06 * math.sin(5 * th + 2.1))]
    bm2 = bmesh.new()
    vr = [[bm2.verts.new(p) for p in r] for r in rings]
    nr = len(rings[0])
    for a, b in zip(vr, vr[1:]):
        for k in range(nr):
            k2 = (k + 1) % nr
            bm2.faces.new((a[k], a[k2], b[k2], b[k]))
    bm2.faces.new(list(reversed(vr[0])))
    bm2.faces.new(vr[-1])
    m2 = bpy.data.meshes.new('funnel_compact')
    bm2.to_mesh(m2)
    bm2.free()
    o = bpy.data.objects.new('funnel_compact', m2)
    bpy.context.collection.objects.link(o)
    return o


def cube(x0, x1, y0, y1, z0, z1):
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


cutters = [funnel()] + [cube(x0, x1, y0, y1, 19.0, 25.0)
                        for (x0, x1, y0, y1) in OPEN_VENTS + OPEN_LOUVRES]
bpy.context.view_layer.objects.active = fp
for i, c in enumerate(cutters):
    m = fp.modifiers.new(f'b{i}', 'BOOLEAN')
    m.operation = 'DIFFERENCE'
    m.solver = 'EXACT'
    m.object = c
    bpy.ops.object.modifier_apply(modifier=m.name)
    c.hide_set(True)
    c.hide_render = True

bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))

# ---- stone material --------------------------------------------------------
mat = bpy.data.materials.get('CompactStone') or bpy.data.materials.new('CompactStone')
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
out = nt.nodes.new('ShaderNodeOutputMaterial')
bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = bpy.data.images.load(DIFF, check_existing=True)
tex.interpolation = 'Linear'
tex.extension = 'REPEAT'
nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.82
nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
fp.data.materials.clear()
fp.data.materials.append(mat)

# ---- export STL ------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
fp.select_set(True)
bpy.context.view_layer.objects.active = fp
bpy.ops.wm.stl_export(filepath=STL, export_selected_objects=True, global_scale=1.0)

# ---- preview render --------------------------------------------------------
scene = bpy.context.scene
for name in ('CameraFP', 'KeyFP', 'FillFP', 'RimFP', 'GroundFP'):
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

cam_data = bpy.data.cameras.new('CameraFP')
cam = bpy.data.objects.new('CameraFP', cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 100.0
cam.location = (55, -135, 95)
target = Vector((17.0, -38.0, 22.0))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()


def add_light(name, loc, energy, size, color):
    d = bpy.data.lights.new(name, 'AREA')
    d.energy = energy
    d.size = size
    d.color = color
    o = bpy.data.objects.new(name, d)
    scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o


add_light('KeyFP', (10, -80, 140), 3500, 140, (1.0, 0.93, 0.82))
add_light('FillFP', (-50, 20, 70), 1200, 120, (0.75, 0.84, 1.0))
add_light('RimFP', (80, -10, 60), 900, 80, (1.0, 1.0, 1.0))

world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World')
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.10, 0.11, 0.13, 1)
    bg.inputs['Strength'].default_value = 1.0

bpy.ops.mesh.primitive_plane_add(size=400, location=(17, -38, 20.4))
g = bpy.context.object
g.name = 'GroundFP'
gm = bpy.data.materials.new('GroundFP')
gm.use_nodes = True
gb = gm.node_tree.nodes.get('Principled BSDF')
gb.inputs['Base Color'].default_value = (0.22, 0.22, 0.24, 1)
gb.inputs['Roughness'].default_value = 0.65
g.data.materials.append(gm)

try:
    scene.view_settings.view_transform = 'AgX'
except Exception:
    pass
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
scene.view_settings.exposure = 1.4
scene.render.filepath = PNG
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 1400
scene.render.resolution_y = 1000
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    try:
        scene.render.engine = 'BLENDER_EEVEE'
    except Exception:
        pass
try:
    scene.eevee.taa_render_samples = 64
except Exception:
    pass
bpy.ops.render.render(write_still=True)

zs = [v.co.z for v in fp.data.vertices]
print('FACEPLATE', len(fp.data.polygons), 'faces', 'z',
      round(min(zs), 2), '..', round(max(zs), 2),
      'bbox', tuple(round(d, 2) for d in fp.dimensions))
print('STL', STL)
print('PNG', PNG)
