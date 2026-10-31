"""Generate the organic faceplate for the ESP32-C3 sensor case.

Run inside Blender:  exec(open('/Users/petekaik/projects/esphome-sensor-board/tools/blender/make_faceplate.py').read())

Builds a heightfield lid that occupies the cover's top-plate volume
(x -6.5..50.25, y -91.25..4.3, z 22..24.5 mm), with:
  - a flat 3 mm border rim at z 24.5
  - a 1 mm recessed deck carrying an organic vein/root field
  - the five BME louvres and three radar vents cut clean through the deck
  - a BH1750 funnel: an organic lobe at the surface narrowing to the exact
    11 x 11 mm sensor opening at the bottom face

Everything is a heightfield plus loft, so there are no undercuts: it prints
flat on the bed without supports.
"""

import bpy
import bmesh
import math
from mathutils import Vector, noise

# ---- envelope (mm) -------------------------------------------------------
X0, X1, Y0, Y1 = -6.5, 50.25, -91.25, 4.3
DECK, RIM, BOTTOM = 23.5, 24.5, 22.0
NX, NY = 114, 191                      # ~0.5 mm pitch, ends on the rectangle
CX, CY = 27.5, -55.5                   # BH1750 opening centre
STL_PATH = "/Users/petekaik/projects/esphome-sensor-board/case/faceplate_organic.stl"

# ---- mandatory openings (sensor geometry, must stay exact at the bottom) --
OPEN_VENTS = [(18.0, 20.6, -40.0, -26.0), (24.0, 26.6, -40.0, -26.0), (30.0, 32.6, -40.0, -26.0)]
OPEN_LOUVRES = [(3.0, 4.6, -56.0, -46.5), (6.0, 7.6, -56.0, -46.5), (9.0, 10.6, -56.0, -46.5),
                (12.0, 13.6, -56.0, -46.5), (15.0, 16.6, -56.0, -46.5)]

# ---- relief tuning -------------------------------------------------------
GRAIN_SCALE = (0.085, 0.016)           # x, y noise scale: strongly stretched along the length
GRAIN_CUT = 0.058                      # contour half-width -> narrower = thinner veins
BRANCH_SCALE = (0.050, 0.030)
BRANCH_CUT = 0.042
AMP_MAIN, AMP_BRANCH, AMP_FINE = 1.55, 0.80, 0.15
AMP_MAX = 1.85


def fbm(x, y, seed=0.0):
    v = a = s = 0.0
    a = 1.0
    f = 1.0
    v = s = 0.0
    for _ in range(3):
        v += a * noise.noise(Vector((x * f, y * f, seed)))
        s += a
        a *= 0.5
        f *= 2.0
    return v / s


def smoothstep(e0, e1, t):
    t = max(0.0, min(1.0, (t - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def rect_gap(x, y, r):
    return math.hypot(max(r[0] - x, 0, x - r[1]), max(r[2] - y, 0, y - r[3]))


def mask(x, y):
    """1 where roots may grow, 0 over the mandatory openings and the BH mouth."""
    m = 1.0
    for r in OPEN_VENTS + OPEN_LOUVRES:
        m = min(m, smoothstep(0.25, 1.5, rect_gap(x, y, r)))
    return min(m, smoothstep(6.6, 8.4, math.hypot(x - CX, y - CY)))


def ztop(x, y):
    d = min(x - X0, X1 - x, y - Y0, Y1 - y)
    rim = 1.0 - smoothstep(3.0, 4.8, d)          # 1 at the border, 0 in the field
    f = fbm(x * GRAIN_SCALE[0], y * GRAIN_SCALE[1])
    f2 = fbm(x * BRANCH_SCALE[0] + 11.0, y * BRANCH_SCALE[1] - 7.0, 3.0)
    vein = (max(0.0, 1.0 - abs(f) / GRAIN_CUT) ** 1.6
            + AMP_BRANCH * max(0.0, 1.0 - abs(f2) / BRANCH_CUT) ** 1.8)
    g = noise.noise(Vector((x * 0.22, y * 0.11, 5.0)))
    h = min(AMP_MAX, AMP_MAIN * vein + AMP_FINE * g * vein) * mask(x, y)
    return DECK + (RIM - DECK) * rim + h * (1.0 - rim)


def build():
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o.name != 'sensorbox_case':
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
    me = bpy.data.meshes.new("faceplate")
    bm.to_mesh(me)
    bm.free()
    fp = bpy.data.objects.new("faceplate", me)
    bpy.context.collection.objects.link(fp)
    bpy.context.view_layer.objects.active = fp
    return fp


def funnel():
    """Exact 11 x 11 at z 22, organic lobe at the surface."""
    n_ring = 96

    def ring(z, ax, ay, n, mod=None):
        pts = []
        for k in range(n_ring):
            th = 2 * math.pi * k / n_ring
            c, s = math.cos(th), math.sin(th)
            r = (abs(c) ** n + abs(s) ** n) ** (-1.0 / n)
            m = 1.0 if mod is None else mod(th)
            pts.append((CX + ax * r * c * m, CY + ay * r * s * m, z))
        return pts

    rings = [ring(21.0, 5.5, 5.5, 12.0), ring(22.0, 5.5, 5.5, 12.0),
             ring(23.2, 6.4, 6.4, 4.0),
             ring(25.9, 9.0, 8.6, 2.0,
                  lambda th: 1.0 + 0.14 * math.sin(3 * th + 0.7) + 0.07 * math.sin(5 * th + 2.1))]
    bm = bmesh.new()
    vr = [[bm.verts.new(p) for p in r] for r in rings]
    for a, b in zip(vr, vr[1:]):
        for k in range(n_ring):
            k2 = (k + 1) % n_ring
            bm.faces.new((a[k], a[k2], b[k2], b[k]))
    bm.faces.new(list(reversed(vr[0])))
    bm.faces.new(vr[-1])
    me = bpy.data.meshes.new("funnel")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("funnel", me)
    bpy.context.collection.objects.link(o)
    return o


def cube(x0, x1, y0, y1, z0, z1):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.object
    o.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o


def main():
    fp = build()
    cutters = [funnel()] + [cube(x0, x1, y0, y1, 20.0, 30.0)
                            for (x0, x1, y0, y1) in OPEN_VENTS + OPEN_LOUVRES]
    bpy.context.view_layer.objects.active = fp
    for i, c in enumerate(cutters):
        m = fp.modifiers.new(f"b{i}", 'BOOLEAN')
        m.operation = 'DIFFERENCE'
        m.solver = 'EXACT'
        m.object = c
        bpy.ops.object.modifier_apply(modifier=m.name)
        c.hide_set(True)
        c.hide_render = True

    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))

    bpy.ops.object.select_all(action='DESELECT')
    fp.select_set(True)
    bpy.context.view_layer.objects.active = fp
    bpy.ops.wm.stl_export(filepath=STL_PATH, export_selected_objects=True, global_scale=1.0)

    zs = [v.co.z for v in fp.data.vertices]
    print("faces", len(fp.data.polygons),
          "z", round(min(zs), 2), "..", round(max(zs), 2),
          "bbox", tuple(round(d, 2) for d in fp.dimensions),
          "->", STL_PATH)


main()
