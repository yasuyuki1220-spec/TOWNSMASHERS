# Voxel models: fill boxes on a grid, greedy-mesh the visible faces and export in the models.js format.
import math, json, base64, struct, random

def shade(hexc, k):
    r, g, b = (hexc >> 16) & 255, (hexc >> 8) & 255, hexc & 255
    return (min(255, int(r * k)) << 16) | (min(255, int(g * k)) << 8) | min(255, int(b * k))

class Vox:
    def __init__(self, vs=0.1, seed=1):
        self.vs = vs; self.v = {}; self.rnd = random.Random(seed)
    def idx(self, x): return int(math.floor(x / self.vs + 1e-6))
    def rng(self, a, b):
        i0, i1 = int(round(a / self.vs)), int(round(b / self.vs))
        if i1 <= i0: i1 = i0 + 1
        return range(i0, i1)
    def box(self, x0, y0, z0, x1, y1, z1, col, kind='l', op=1.0, jit=0, erase=False):
        """Fill [x0,x1) x [y0,y1) x [z0,z1) metres. jit: pick from darker / base / lighter shades per voxel."""
        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0
        if z0 > z1: z0, z1 = z1, z0
        R = self.rnd
        for i in self.rng(x0, x1):
            for j in self.rng(y0, y1):
                for k in self.rng(z0, z1):
                    if erase: self.v.pop((i, j, k), None); continue
                    c = col
                    if jit: c = shade(col, R.choice((1 - jit, 1, 1, 1 + jit)))
                    self.v[(i, j, k)] = (c, kind, op)
    def cbox(self, cx, y0, cz, w, h, d, col, **k):   # centred footprint
        self.box(cx - w / 2, y0, cz - d / 2, cx + w / 2, y0 + h, cz + d / 2, col, **k)
    def cyl(self, cx, y0, cz, r, h, col, axis='y', **k):
        vs = self.vs
        if axis == 'y':
            for i in self.rng(cx - r, cx + r):
                for kk in self.rng(cz - r, cz + r):
                    if ((i + .5) * vs - cx) ** 2 + ((kk + .5) * vs - cz) ** 2 <= r * r + 1e-9:
                        self.box(i * vs, y0, kk * vs, (i + 1) * vs, y0 + h, (kk + 1) * vs, col, **k)
        elif axis == 'x':
            for j in self.rng(y0 - r, y0 + r):
                for kk in self.rng(cz - r, cz + r):
                    if ((j + .5) * vs - y0) ** 2 + ((kk + .5) * vs - cz) ** 2 <= r * r + 1e-9:
                        self.box(cx, j * vs, kk * vs, cx + h, (j + 1) * vs, (kk + 1) * vs, col, **k)
        else:
            for i in self.rng(cx - r, cx + r):
                for j in self.rng(y0 - r, y0 + r):
                    if ((i + .5) * vs - cx) ** 2 + ((j + .5) * vs - y0) ** 2 <= r * r + 1e-9:
                        self.box(i * vs, j * vs, cz, (i + 1) * vs, (j + 1) * vs, cz + h, col, **k)
    def sphere(self, cx, cy, cz, r, col, **k):
        vs = self.vs
        for i in self.rng(cx - r, cx + r):
            for j in self.rng(cy - r, cy + r):
                for kk in self.rng(cz - r, cz + r):
                    if ((i + .5) * vs - cx) ** 2 + ((j + .5) * vs - cy) ** 2 + ((kk + .5) * vs - cz) ** 2 <= r * r:
                        self.box(i * vs, j * vs, kk * vs, (i + 1) * vs, (j + 1) * vs, (kk + 1) * vs, col, **k)
    def voxel(self, x, y, z, col, **k): self.box(x, y, z, x + self.vs, y + self.vs, z + self.vs, col, **k)
    def text(self, x, y, z, s, col, axis='z', scale=1, **k):
        """Blocky 3x5 letters on a wall. axis='z': letters face +z, run along +x."""
        F = {'A': '010101111101101', 'B': '110101110101110', 'C': '011100100100011', 'D': '110101101101110', 'E': '111100110100111', 'F': '111100110100100',
             'G': '011100101101011', 'H': '101101111101101', 'I': '111010010010111', 'K': '101101110101101', 'L': '100100100100111', 'M': '101111111101101',
             'N': '110101101101101', 'O': '010101101101010', 'P': '110101110100100', 'R': '110101110101101', 'S': '011100010001110', 'T': '111010010010010',
             'U': '101101101101111', 'V': '101101101101010', 'W': '101101111111101', 'Y': '101101010010010', 'Z': '111001010100111', '!': '010010010000010',
             '0': '111101101101111', '1': '010110010010111', '2': '110001010100111', '3': '110001010001110', '4': '101101111001001', '5': '111100110001110',
             '6': '011100110101010', '7': '111001010010010', '8': '010101010101010', '9': '010101011001110', '$': '011110010011110', '.': '000000000000010',
             '%': '101001010100101', '-': '000000111000000', ' ': '000000000000000', 'J': '001001001101010', 'Q': '010101101110011', 'X': '101101010101101'}
        vs = self.vs * scale; cx = x
        for ch in s.upper():
            g = F.get(ch, F[' '])
            for r in range(5):
                for c in range(3):
                    if g[r * 3 + c] == '1':
                        if axis == 'z': self.box(cx + c * vs, y + (4 - r) * vs, z, cx + (c + 1) * vs, y + (5 - r) * vs, z + self.vs, col, **k)
                        elif axis == 'x': self.box(x, y + (4 - r) * vs, cx + c * vs, x + self.vs, y + (5 - r) * vs, cx + (c + 1) * vs, col, **k)
                        elif axis == '-x': self.box(x, y + (4 - r) * vs, cx - (c + 1) * vs, x + self.vs, y + (5 - r) * vs, cx - c * vs, col, **k)
            cx += 4 * vs * (1 if axis != '-x' else -1)
        return abs(cx - x)

    # ---------- meshing ----------
    def mesh(self):
        V = self.v; groups = {}
        def opaque(m): return m[2] >= 1 and m[1] != 'b' or m[1] == 'b' and m[2] >= 1
        for d in range(3):
            u, w = [a for a in range(3) if a != d]
            for sgn in (1, -1):
                slices = {}
                for key, m in V.items():
                    nb = list(key); nb[d] += sgn; nm = V.get(tuple(nb))
                    if nm is not None and (nm == m or (nm[2] >= 1 and m[2] >= 1) or (nm[2] >= 1 and m[2] < 1)): continue
                    slices.setdefault(key[d], {})[(key[u], key[w])] = m
                for s, mask in slices.items():
                    done = set()
                    for (a, b) in sorted(mask):
                        if (a, b) in done: continue
                        m = mask[(a, b)]; a1 = a + 1
                        while (a1, b) in mask and mask[(a1, b)] == m and (a1, b) not in done: a1 += 1
                        b1 = b + 1
                        while all((x, b1) in mask and mask[(x, b1)] == m and (x, b1) not in done for x in range(a, a1)): b1 += 1
                        for x in range(a, a1):
                            for y in range(b, b1): done.add((x, y))
                        plane = s + (1 if sgn > 0 else 0)
                        def P(aa, bb):
                            p = [0, 0, 0]; p[d] = plane; p[u] = aa; p[w] = bb; return [c * self.vs for c in p]
                        q = [P(a, b), P(a1, b), P(a1, b1), P(a, b1)]
                        n = [0, 0, 0]; n[d] = sgn
                        e1 = [q[1][i] - q[0][i] for i in range(3)]; e2 = [q[2][i] - q[0][i] for i in range(3)]
                        cr = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]
                        if sum(cr[i] * n[i] for i in range(3)) < 0: q = [q[0], q[3], q[2], q[1]]
                        groups.setdefault(m, []).append((q, n))
        return groups

def export(vx, name, models):
    groups = vx.mesh(); mx = 1.0
    for qs in groups.values():
        for q, n in qs:
            for p in q: mx = max(mx, max(abs(c) for c in p))
    S = math.ceil(mx * 1.05 * 2) / 2; out = {'s': S, 'parts': {'m': []}, 'att': {}, 'pos': {}, 'j': {}, 'a': {}}
    b64 = lambda fmt, arr: base64.b64encode(struct.pack('<%d%s' % (len(arr), fmt), *arr)).decode()
    nv = 0
    for (hexc, kind, op), qs in groups.items():
        for k0 in range(0, len(qs), 16000):
            P, N, I = [], [], []
            for q, n in qs[k0:k0 + 16000]:
                b = len(P) // 3
                for p in q: P += [max(-32767, min(32767, round(c / S * 32767))) for c in p]; N += [c * 127 for c in n]
                I += [b, b + 1, b + 2, b, b + 2, b + 3]
            nv += len(P) // 3
            out['parts']['m'].append({'c': hexc, 'k': kind, 'o': op, 'p': b64('h', P), 'n': b64('b', N), 'i': b64('H', I)})
    models[name] = out
    print('%-16s %6d verts %5d KB' % (name, nv, len(json.dumps(out)) // 1024))
    return out
