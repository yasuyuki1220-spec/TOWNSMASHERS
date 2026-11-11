# Builds the Alien fighter in Blender and exports it for the game.
#   python3 tools/alien_blender.py <out.json> [preview.png]
# Geometry is written in game coordinates (x right, y up, z forward) and converted to Blender (Z up).
import bpy, math, json, base64, struct, sys
from mathutils import Vector, Matrix
OUT = sys.argv[1]; PNG = sys.argv[2] if len(sys.argv) > 2 else None
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
PI = math.pi

def g2b(v): return Vector((v[0], -v[2], v[1]))
def b2g(v): return (v[0], v[2], -v[1])

def lin(c): return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
def mat(name, hexc, kind='l', op=1.0, rough=.55):
    m = bpy.data.materials.new(name)
    try: m.use_nodes = True
    except Exception: pass
    rgb = [lin(((hexc >> s) & 255) / 255) for s in (16, 8, 0)]
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
    if kind == 'b':
        b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = 1.6
    if op < 1:
        b.inputs['Alpha'].default_value = op * 1.3; b.inputs['Roughness'].default_value = .05
    m['hex'] = hexc; m['kind'] = kind; m['op'] = op
    return m

SUIT = mat('suit', 0xeef1f6); SLATE = mat('slate', 0x4d5a73); ORANGE = mat('orange', 0xff8a4a); SKIN = mat('skin', 0xa9bccb)
METAL = mat('metal', 0xb9c2d0, rough=.3); GLOW = mat('glow', 0x7affea, 'b'); EYE = mat('eye', 0x0c0e18, rough=.08)
WHITE = mat('white', 0xffffff, 'b'); CHEEK = mat('cheek', 0xc9b0d8); MOUTH = mat('mouth', 0x5b4a70)
GLASS = mat('glass', 0xcfeaff, 'l', .2); SHINE = mat('shine', 0xffffff, 'b', .7); RED = mat('red', 0xff5a4a, 'b')

OBJS = []   # (object, part or None)
def add(part, material, verts, faces, bevel=None, sharp=None):
    me = bpy.data.meshes.new('m'); me.from_pydata([g2b(v) for v in verts], [], faces); me.update()
    import bmesh
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    me.shade_smooth()
    if sharp: me.set_sharp_from_angle(angle=math.radians(sharp))
    me.materials.append(material)
    ob = bpy.data.objects.new(part or 'x', me); scene.collection.objects.link(ob)
    if bevel:
        md = ob.modifiers.new('bev', 'BEVEL'); md.width = bevel; md.segments = 2
    OBJS.append((ob, part)); return ob

def frame(origin, direction=(0, 1, 0), rot=None):
    q = Vector((0, 1, 0)).rotation_difference(Vector(direction).normalized()).to_matrix().to_4x4()
    T = Matrix.Translation(Vector(origin)) @ q
    return T @ rot if rot else T

def lathe(profile, seg, T=None, sx=1, sz=1, fn=None):
    """profile: [(h, r)] along +y. r == 0 at an end makes a pole."""
    verts = []; rings = []
    for h, r in profile:
        if r <= 1e-6: rings.append([len(verts)]); verts.append(Vector((0, h, 0)))
        else:
            rings.append(list(range(len(verts), len(verts) + seg)))
            for k in range(seg):
                a = 2 * PI * k / seg; verts.append(Vector((r * math.cos(a) * sx, h, r * math.sin(a) * sz)))
    faces = []
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        for k in range(seg):
            k2 = (k + 1) % seg
            if len(A) == 1 and len(B) == 1: continue
            if len(A) == 1: faces.append((A[0], B[k], B[k2]))
            elif len(B) == 1: faces.append((A[k], B[0], A[k2]))
            else: faces.append((A[k], B[k], B[k2], A[k2]))
    if fn: verts = [fn(v) for v in verts]
    if T: verts = [T @ v for v in verts]
    return [tuple(v) for v in verts], faces

def ellipsoid(c, r, seg=12, rings=8, rot=None, fn=None):
    prof = [(-r[1] * math.cos(PI * k / rings), math.sin(PI * k / rings)) for k in range(rings + 1)]
    prof[0] = (prof[0][0], 0); prof[-1] = (prof[-1][0], 0)
    return lathe(prof, seg, frame(c, rot=rot), r[0], r[2], fn)

def capsule(p0, p1, r0, r1, seg=12, n=3):
    p0 = Vector(p0); p1 = Vector(p1); L = (p1 - p0).length
    prof = [(-r0 * math.cos(k * PI / 2 / n), r0 * math.sin(k * PI / 2 / n)) for k in range(n + 1)]
    prof += [(L + r1 * math.sin(k * PI / 2 / n), r1 * math.cos(k * PI / 2 / n)) for k in range(n + 1)]
    prof[0] = (prof[0][0], 0); prof[-1] = (prof[-1][0], 0)
    return lathe(prof, seg, frame(p0, p1 - p0))

def torus(c, R, r, axis=(0, 1, 0), seg=20, tseg=6, sx=1, sz=1):
    verts = []; faces = []; T = frame(c, axis)
    for i in range(seg):
        a = 2 * PI * i / seg
        for j in range(tseg):
            b = 2 * PI * j / tseg; rr = R + r * math.cos(b)
            verts.append(tuple(T @ Vector((rr * math.cos(a) * sx, r * math.sin(b), rr * math.sin(a) * sz))))
    for i in range(seg):
        for j in range(tseg):
            i2 = (i + 1) % seg; j2 = (j + 1) % tseg
            faces.append((i * tseg + j, i * tseg + j2, i2 * tseg + j2, i2 * tseg + j))
    return verts, faces

def box(c, size, rot=None):
    T = frame(c, rot=rot); h = [s / 2 for s in size]
    v = [tuple(T @ Vector((x * h[0], y * h[1], z * h[2]))) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    return v, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]

def off(vf, d): return [(v[0] + d[0], v[1] + d[1], v[2] + d[2]) for v in vf[0]], vf[1]
RY = lambda a: Matrix.Rotation(a, 4, 'Y'); RZ = lambda a: Matrix.Rotation(a, 4, 'Z'); RX = lambda a: Matrix.Rotation(a, 4, 'X')

# ---------------- skeleton (rest pose) ----------------
THIGH = .28; FOOT = .484; HIP = THIGH + FOOT; HIPX = .105
HEADY = 1.33; SHX = .215; SHY = 1.2; UARM = .2; HANDY = -.40; GZ = .065
PIV = {'torso': (0, 0, 0), 'head': (0, HEADY, 0), 'helmet': (0, HEADY, 0), 'beacon': (0, HEADY, 0),
       'legU': (-HIPX, HIP, 0), 'legF': (-HIPX, HIP - THIGH, 0), 'armU': (-SHX, SHY, 0), 'armF': (-SHX, SHY - UARM, 0),
       'gun': (SHX, SHY - UARM, 0)}
EYE_C = {'eyeL': (-.088, .195, .198), 'eyeR': (.088, .195, .198)}
for k, c in EYE_C.items(): PIV[k] = (c[0], HEADY + c[1], c[2])

# ---------------- torso ----------------
add('torso', SUIT, *lathe([(.74, 0), (.75, .15), (.79, .215), (.87, .238), (.98, .225), (1.1, .19), (1.2, .155), (1.27, .125), (1.3, .08), (1.31, 0)], 20, sz=.9))
add('torso', SLATE, *lathe([(.63, 0), (.645, .1), (.69, .185), (.75, .225), (.81, .236), (.83, .2), (.84, 0)], 20, sz=.9))
add('torso', SLATE, *torus((0, .82, 0), .236, .028, sz=.9, seg=24))
add('torso', ORANGE, *torus((0, .862, 0), .238, .011, sz=.9, seg=24))
add('torso', ORANGE, *box((0, .82, .222), (.085, .06, .035)), bevel=.012)
add('torso', GLOW, *ellipsoid((0, .82, .243), (.018, .018, .008), 10, 6))
add('torso', METAL, *torus((0, 1.3, 0), .15, .043, seg=24, tseg=8))
add('torso', GLOW, *torus((0, 1.338, 0), .168, .011, seg=24))
# chest emblem
add('torso', SLATE, *lathe([(0, 0), (0, .062), (.02, .066), (.03, .05), (.032, 0)], 16, frame((0, 1.07, .158), (0, .12, 1))))
add('torso', GLOW, *torus((0, 1.074, .192), .036, .011, (0, .12, 1), 16, 6))
add('torso', WHITE, *ellipsoid((0, 1.074, .193), (.014, .014, .008), 8, 5))
# oxygen tank + backplate
add('torso', SLATE, *box((0, 1.0, -.195), (.21, .3, .08)), bevel=.025)
add('torso', ORANGE, *capsule((0, .9, -.285), (0, 1.07, -.285), .082, .082, 14, 4))
add('torso', METAL, *torus((0, .92, -.285), .084, .013, seg=16))
add('torso', METAL, *torus((0, 1.05, -.285), .084, .013, seg=16))
add('torso', METAL, *lathe([(1.13, 0), (1.13, .032), (1.19, .028), (1.19, 0)], 10, frame((0, 0, -.285))), sharp=40)
add('torso', SLATE, *ellipsoid((0, 1.205, -.285), (.04, .022, .04), 10, 6))
PORT = (0, 1.21, -.285)

# ---------------- head ----------------
def headshape(v):
    ux, uy, uz = v
    x = ux * .222; y = uy * .2; z = uz * .2
    if uz < 0:
        t = -uz
        z = -(.2 * t + .19 * t * t); y = y * (1 - .12 * t) + .12 * t * t; x *= 1 - .3 * t * t
    if uy < 0: x *= 1 - .2 * (-uy) ** 1.6
    return Vector((x, y, z))
hv, hf = lathe([(-math.cos(PI * k / 16), math.sin(PI * k / 16) if 0 < k < 16 else 0) for k in range(17)], 28, None, 1, 1, headshape)
add('head', SKIN, *off((hv, hf), (0, HEADY + .215, .03)))
add('head', SKIN, *capsule((0, HEADY - .06, 0), (0, HEADY + .05, .01), .06, .07, 10, 2))
for s in (-1, 1):
    add('head', CHEEK, *ellipsoid((s * .15, HEADY + .125, .158), (.036, .022, .012), 10, 5, RY(s * .75)))
add('head', MOUTH, *ellipsoid((0, HEADY + .108, .222), (.02, .011, .01), 8, 5))
for k, c in EYE_C.items():
    s = 1 if c[0] > 0 else -1; R = RY(s * .4) @ RZ(-s * .2)
    P = lambda p: tuple(Vector((c[0], HEADY + c[1], c[2])) + (R @ Vector(p)))
    add(k, EYE, *ellipsoid(P((0, 0, 0)), (.06, .08, .03), 16, 10, R))
    add(k, WHITE, *ellipsoid(P((-.02, .032, .026)), (.02, .022, .01), 8, 5, R))
    add(k, WHITE, *ellipsoid(P((.02, -.03, .027)), (.009, .009, .005), 6, 4, R))
# bubble helmet
HC = (0, HEADY + .25, -.07); HR = (.4, .4, .44)
add('helmet', GLASS, *ellipsoid(HC, HR, 24, 14))
def onhel(d, k=.985):
    d = Vector(d).normalized(); return (HC[0] + HR[0] * d.x * k, HC[1] + HR[1] * d.y * k, HC[2] + HR[2] * d.z * k), d
for d, r, roll in (((-.5, .5, .7), (.1, .03, .012), .7), ((-.2, .72, .66), (.03, .022, .01), 0)):
    p, n = onhel(d); Q = Vector((0, 0, 1)).rotation_difference(n).to_matrix().to_4x4() @ RZ(roll)
    add('helmet', SHINE, *ellipsoid(p, r, 10, 5, Q))
add('helmet', METAL, *capsule((0, HC[1] + .39, HC[2]), (0, HC[1] + .46, HC[2]), .012, .01, 6, 1))
add('beacon', RED, *ellipsoid((0, HC[1] + .485, HC[2]), (.03, .03, .03), 10, 6))

# ---------------- limbs (left side is exported, right side is the same mesh) ----------------
def arm(s, ex):
    U = lambda p: (s * SHX + p[0], SHY + p[1], p[2]); F = lambda p: (s * SHX + p[0], SHY - UARM + p[1], p[2])
    pu = 'armU' if ex else None; pf = 'armF' if ex else None
    add(pu, SUIT, *ellipsoid(U((0, 0, 0)), (.074, .074, .074), 12, 8))
    add(pu, SUIT, *capsule(U((0, -.02, 0)), U((0, -UARM + .02, 0)), .058, .05, 12, 2))
    add(pf, SLATE, *ellipsoid(F((0, 0, 0)), (.054, .054, .054), 12, 8))
    add(pf, SUIT, *lathe([(-.02, 0), (-.02, .046), (-.2, .054), (-.3, .07), (-.34, .078), (-.345, 0)], 12, frame(F((0, 0, 0)))))
    add(pf, ORANGE, *torus(F((0, -.325, 0)), .074, .014, seg=14))
    add(pf, SLATE, *ellipsoid(F((0, HANDY, 0)), (.064, .062, .064), 12, 8))
    for dx, dy, dz in ((-.038, -.058, .004), (0, -.072, .012), (.038, -.058, .004)):
        add(pf, SLATE, *ellipsoid(F((dx, HANDY + dy, dz)), (.022, .04, .022), 8, 5))
    add(pf, SLATE, *ellipsoid(F((0, HANDY - .02, .06)), (.021, .034, .021), 8, 5, RX(-.7)))
def leg(s, ex):
    U = lambda p: (s * HIPX + p[0], HIP + p[1], p[2]); F = lambda p: (s * HIPX + p[0], HIP - THIGH + p[1], p[2])
    pu = 'legU' if ex else None; pf = 'legF' if ex else None
    add(pu, SUIT, *capsule(U((0, -.02, 0)), U((0, -THIGH + .02, 0)), .07, .06, 12, 2))
    add(pf, SLATE, *ellipsoid(F((0, 0, 0)), (.06, .06, .06), 12, 8))
    add(pf, SUIT, *lathe([(-.02, 0), (-.02, .05), (-.24, .06), (-.34, .08), (-.385, .09), (-.39, 0)], 12, frame(F((0, 0, 0)))))
    add(pf, ORANGE, *torus(F((0, -.37, 0)), .085, .014, seg=14))
    add(pf, SUIT, *ellipsoid(F((0, -.425, .04)), (.09, .06, .138), 14, 8))
    add(pf, SLATE, *ellipsoid(F((0, -.46, .04)), (.097, .024, .146), 14, 6))
for s in (-1, 1): arm(s, s < 0); leg(s, s < 0)

# ---------------- ray gun (right forearm) ----------------
G = lambda p: (SHX + p[0], SHY - UARM + p[1], p[2])
add('gun', ORANGE, *ellipsoid(G((0, -.365, GZ)), (.04, .045, .04), 10, 6))
add('gun', SUIT, *lathe([(0, 0), (.006, .04), (.05, .064), (.11, .06), (.165, .04), (.2, .03), (.235, .028), (.24, 0)], 14, frame(G((0, -.36, GZ)), (0, -1, 0))))
for h, r, m in ((.265, .052, ORANGE), (.305, .043, SUIT), (.345, .035, ORANGE)):
    add('gun', m, *ellipsoid(G((0, -.36 - h, GZ)), (r, .013, r), 14, 4))
add('gun', METAL, *capsule(G((0, -.59, GZ)), G((0, -.74, GZ)), .015, .013, 8, 1))
add('gun', GLOW, *ellipsoid(G((0, -.765, GZ)), (.032, .032, .032), 10, 6))
add('gun', SLATE, *box(G((0, -.41, .02)), (.046, .11, .075)), bevel=.012)
add('gun', ORANGE, *box(G((0, -.455, GZ + .075)), (.016, .14, .06), RX(.25)), bevel=.006)
add('gun', SLATE, *lathe([(0, 0), (0, .022), (.03, .022), (.03, 0)], 8, frame(G((0, -.335, GZ)), (0, 1, 0))), sharp=40)
ANCH = {'port': PORT, 'gp': (0, -.3, GZ), 'muzzle': (0, -.765, GZ)}

# ---------------- export ----------------
dg = bpy.context.evaluated_depsgraph_get(); S = 2.0; parts = {}; nv = 0
for ob, part in OBJS:
    if not part: continue
    me = ob.evaluated_get(dg).to_mesh(); me.calc_loop_triangles(); m = ob.data.materials[0]; piv = PIV[part]
    key = (m['hex'], m['kind'], round(m['op'], 2))
    d = parts.setdefault(part, {}).setdefault(key, {'map': {}, 'p': [], 'n': [], 'i': []})
    cn = me.corner_normals
    for t in me.loop_triangles:
        for li in t.loops:
            p = b2g(me.vertices[me.loops[li].vertex_index].co); n = b2g(cn[li].vector)
            p = tuple(round(p[a] - piv[a], 4) for a in range(3)); k = (p, tuple(round(c, 1) for c in n))
            ix = d['map'].get(k)
            if ix is None:
                ix = len(d['p']) // 3; d['map'][k] = ix
                d['p'] += [max(-32767, min(32767, round(c / S * 32767))) for c in p]; d['n'] += [round(max(-1, min(1, c)) * 127) for c in n]
            d['i'].append(ix)
out = {'s': S, 'parts': {}, 'a': {k: [round(c, 4) for c in v] for k, v in ANCH.items()},
       'j': {'hipx': HIPX, 'hip': round(HIP, 4), 'thigh': THIGH, 'head': HEADY, 'shx': SHX, 'shy': SHY, 'uarm': UARM, 'hand': HANDY,
             'eyeL': list(EYE_C['eyeL']), 'eyeR': list(EYE_C['eyeR'])}}
b64 = lambda fmt, a: base64.b64encode(struct.pack('<%d%s' % (len(a), fmt), *a)).decode()
for part, groups in parts.items():
    out['parts'][part] = []
    for (hx, kind, op), d in groups.items():
        nv += len(d['p']) // 3
        out['parts'][part].append({'c': hx, 'k': kind, 'o': op, 'p': b64('h', d['p']), 'n': b64('b', d['n']), 'i': b64('H', d['i'])})
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
print('exported', nv, 'verts,', len(json.dumps(out)) // 1024, 'KB')

# ---------------- preview render ----------------
if PNG:
    gv, gf = box((0, -.05, 0), (12, .1, 12)); add(None, mat('floor', 0xd9b98a, rough=.9), gv, gf)
    w = bpy.data.worlds.new('w'); scene.world = w
    try: w.use_nodes = True
    except Exception: pass
    w.node_tree.nodes['Background'].inputs[0].default_value = (.55, .7, .9, 1); w.node_tree.nodes['Background'].inputs[1].default_value = .9
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); sun.data.energy = 3.2; sun.data.angle = .25
    sun.rotation_euler = (math.radians(50), 0, math.radians(35)); scene.collection.objects.link(sun)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); scene.collection.objects.link(cam); scene.camera = cam
    cam.data.lens = 70
    def look(pos, tgt):
        cam.location = g2b(pos); d = g2b(tgt) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    scene.render.engine = 'CYCLES'; scene.cycles.samples = 40; scene.cycles.device = 'CPU'
    try: scene.cycles.use_denoising = True
    except Exception: pass
    scene.render.resolution_x = 700; scene.render.resolution_y = 900; scene.render.image_settings.file_format = 'PNG'
    for i, (pos, tgt) in enumerate((((2.6, 1.7, 5.6), (0, 1.0, 0)), ((-5.6, 1.5, -2.2), (0, 1.0, 0)))):
        look(pos, tgt); scene.render.filepath = PNG.replace('.png', '_%d.png' % i); bpy.ops.render.render(write_still=True)
