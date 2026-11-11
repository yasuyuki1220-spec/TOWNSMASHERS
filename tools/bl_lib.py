# Shared Blender helpers. Geometry is written in game coordinates (x right, y up, z forward).
import bpy, bmesh, math, json, base64, struct
from mathutils import Vector, Matrix
PI = math.pi
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
def g2b(v): return Vector((v[0], -v[2], v[1]))
def b2g(v): return (v[0], v[2], -v[1])
RX = lambda a: Matrix.Rotation(a, 4, 'X'); RY = lambda a: Matrix.Rotation(a, 4, 'Y'); RZ = lambda a: Matrix.Rotation(a, 4, 'Z')

_M = {}
def M(hexc, kind='l', op=1.0):
    k = (hexc, kind, op)
    if k not in _M:
        m = bpy.data.materials.new('m%06x' % hexc); m['hex'] = hexc; m['kind'] = kind; m['op'] = op; _M[k] = m
    return _M[k]
def B(hexc, op=1.0): return M(hexc, 'b', op)

MODELS = {}; CUR = None
def begin(name):
    global CUR
    CUR = {'name': name, 'objs': [], 'piv': {}, 'att': {}, 'pos': {}, 'j': {}, 'a': {}}
def part(name, pivot=(0, 0, 0), att=(), pos=None):
    CUR['piv'][name] = tuple(pivot); CUR['att'][name] = list(att)
    if pos is not None: CUR['pos'][name] = [round(c, 4) for c in pos]
def add(pname, material, shape, bevel=None, sharp=None):
    if isinstance(material, int): material = M(material)
    verts, faces = shape
    me = bpy.data.meshes.new('m'); me.from_pydata([g2b(v) for v in verts], [], faces); me.update()
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    me.shade_smooth()
    if sharp: me.set_sharp_from_angle(angle=math.radians(sharp))
    me.materials.append(material)
    ob = bpy.data.objects.new(pname, me); scene.collection.objects.link(ob)
    if bevel:
        md = ob.modifiers.new('bev', 'BEVEL'); md.width = bevel; md.segments = 2
    CUR['objs'].append((ob, pname)); return ob

def frame(origin, direction=(0, 1, 0), rot=None):
    q = Vector((0, 1, 0)).rotation_difference(Vector(direction).normalized()).to_matrix().to_4x4()
    T = Matrix.Translation(Vector(origin)) @ q
    return T @ rot if rot else T
def lat(profile, seg=12, T=None, sx=1, sz=1, fn=None):
    verts = []; rings = []
    for h, r in profile:
        if r <= 1e-6: rings.append([len(verts)]); verts.append(Vector((0, h, 0)))
        else:
            rings.append(list(range(len(verts), len(verts) + seg)))
            for k in range(seg):
                a = 2 * PI * k / seg; verts.append(Vector((r * math.cos(a) * sx, h, r * math.sin(a) * sz)))
    faces = []
    for i in range(len(rings) - 1):
        A, Bq = rings[i], rings[i + 1]
        for k in range(seg):
            k2 = (k + 1) % seg
            if len(A) == 1 and len(Bq) == 1: continue
            if len(A) == 1: faces.append((A[0], Bq[k], Bq[k2]))
            elif len(Bq) == 1: faces.append((A[k], Bq[0], A[k2]))
            else: faces.append((A[k], Bq[k], Bq[k2], A[k2]))
    if fn: verts = [fn(v) for v in verts]
    if T: verts = [T @ v for v in verts]
    return [tuple(v) for v in verts], faces
def ell(c, r, seg=10, rings=6, rot=None, fn=None):
    if not isinstance(r, (tuple, list)): r = (r, r, r)
    prof = [(-r[1] * math.cos(PI * k / rings), math.sin(PI * k / rings)) for k in range(rings + 1)]
    prof[0] = (prof[0][0], 0); prof[-1] = (prof[-1][0], 0)
    return lat(prof, seg, frame(c, rot=rot), r[0], r[2], fn)
def cap(p0, p1, r0, r1=None, seg=10, n=2):
    if r1 is None: r1 = r0
    p0 = Vector(p0); p1 = Vector(p1); L = (p1 - p0).length
    prof = [(-r0 * math.cos(k * PI / 2 / n), r0 * math.sin(k * PI / 2 / n)) for k in range(n + 1)]
    prof += [(L + r1 * math.sin(k * PI / 2 / n), r1 * math.cos(k * PI / 2 / n)) for k in range(n + 1)]
    prof[0] = (prof[0][0], 0); prof[-1] = (prof[-1][0], 0)
    return lat(prof, seg, frame(p0, p1 - p0))
def cone(p0, p1, r, seg=8, r1=0.0):
    p0 = Vector(p0); p1 = Vector(p1); L = (p1 - p0).length
    return lat([(0, 0), (0, r), (L, r1)] + ([(L, 0)] if r1 > 0 else []), seg, frame(p0, p1 - p0))
def tor(c, R, r, axis=(0, 1, 0), seg=16, tseg=6, sx=1, sz=1, arc=1.0):
    verts = []; faces = []; T = frame(c, axis); n = seg if arc >= 1 else seg + 1
    for i in range(n):
        a = 2 * PI * arc * i / seg
        for j in range(tseg):
            b = 2 * PI * j / tseg; rr = R + r * math.cos(b)
            verts.append(tuple(T @ Vector((rr * math.cos(a) * sx, r * math.sin(b), rr * math.sin(a) * sz))))
    for i in range(seg):
        i2 = (i + 1) % n
        for j in range(tseg):
            j2 = (j + 1) % tseg; faces.append((i * tseg + j, i * tseg + j2, i2 * tseg + j2, i2 * tseg + j))
    if arc < 1: faces.append(tuple(range(tseg))); faces.append(tuple(seg * tseg + j for j in range(tseg)))
    return verts, faces
def box(c, size, rot=None):
    T = frame(c, rot=rot); h = [s / 2 for s in size]
    v = [tuple(T @ Vector((x * h[0], y * h[1], z * h[2]))) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    return v, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
def chain(pname, col, pts, r0, r1, seg=8):
    n = len(pts) - 1
    for i in range(n):
        a = r0 + (r1 - r0) * i / n; b = r0 + (r1 - r0) * (i + 1) / n; add(pname, col, cap(pts[i], pts[i + 1], a, b, seg, 2))

def end(j=None, a=None, scale=None):
    m = CUR
    if scale is None:
        mx = max([abs(c) for ob, _ in m['objs'] for v in ob.data.vertices for c in v.co] + [1.0]); scale = math.ceil(mx * 1.3 * 2) / 2
    dg = bpy.context.evaluated_depsgraph_get(); parts = {}; nv = 0
    for ob, pname in m['objs']:
        me = ob.evaluated_get(dg).to_mesh(); me.calc_loop_triangles(); mt = ob.data.materials[0]; piv = m['piv'][pname]
        d = parts.setdefault(pname, {}).setdefault((mt['hex'], mt['kind'], round(mt['op'], 2)), {'map': {}, 'p': [], 'n': [], 'i': []})
        cn = me.corner_normals
        for t in me.loop_triangles:
            for li in t.loops:
                p = b2g(me.vertices[me.loops[li].vertex_index].co); n = b2g(cn[li].vector)
                p = tuple(round(p[x] - piv[x], 4) for x in range(3)); k = (p, tuple(round(c, 1) for c in n)); ix = d['map'].get(k)
                if ix is None:
                    ix = len(d['p']) // 3; d['map'][k] = ix
                    d['p'] += [max(-32767, min(32767, round(c / scale * 32767))) for c in p]; d['n'] += [round(max(-1, min(1, c)) * 127) for c in n]
                d['i'].append(ix)
    b64 = lambda fmt, arr: base64.b64encode(struct.pack('<%d%s' % (len(arr), fmt), *arr)).decode()
    out = {'s': scale, 'parts': {}, 'att': m['att'], 'pos': m['pos'], 'j': j or m['j'], 'a': {k: [round(c, 4) for c in v] for k, v in (a or m['a']).items()}}
    for pname, groups in parts.items():
        out['parts'][pname] = []
        for (hx, kind, op), d in groups.items():
            assert len(d['p']) // 3 < 65536
            nv += len(d['p']) // 3
            out['parts'][pname].append({'c': hx, 'k': kind, 'o': op, 'p': b64('h', d['p']), 'n': b64('b', d['n']), 'i': b64('H', d['i'])})
    for ob, _ in m['objs']: bpy.data.objects.remove(ob)
    MODELS[m['name']] = out; print('%-10s %5d verts %4d KB' % (m['name'], nv, len(json.dumps(out)) // 1024)); return out
def write(path):
    open(path, 'w').write('var MDL=' + json.dumps(MODELS, separators=(',', ':')) + ';\n')
    import os; print('wrote', path, os.path.getsize(path) // 1024, 'KB')
