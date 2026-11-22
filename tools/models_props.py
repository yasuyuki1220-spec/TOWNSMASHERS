# Stage props and gimmicks. Origin = centre of the footprint on the ground; sizes match the collision boxes in index.html.
from bl_lib import *
import random
def P(name): begin(name if name.startswith('gm_') else 'pr_' + name); part('m')
def A(col, shape, **k): return add('m', col, shape, **k)
def bx(col, c, size, bev=None, rot=None): return A(col, box(c, size, rot), bevel=bev)
def tube(col, p0, p1, r, seg=5): return A(col, cap(p0, p1, r, r, seg, 1))
def cy(col, c, r, h, seg=12, r1=None, sx=1, sz=1): return A(col, lat([(0, 0), (0, r), (h, r if r1 is None else r1), (h, 0)], seg, frame(c), sx, sz), sharp=40)
def ball(col, c, r, seg=8, rings=5): return A(col, ell(c, r, seg, rings))
def counter(w, h, d, body, top, band=None, kick=0x3a3a44, tt=.07, bev=.04):
    bx(kick, (0, .06, 0), (w - .12, .12, d - .12)); bx(body, (0, .12 + (h - .12 - tt) / 2, 0), (w, h - .12 - tt, d), bev); bx(top, (0, h - tt / 2, 0), (w + .08, tt, d + .08), .025)
    if band is not None: bx(band, (0, h * .5, 0), (w + .02, .14, d + .02), .01)

# ------------------------------ supermarket ------------------------------
def veg(name, top, pile):
    P(name); w, h, d = 5, .85, 1.8
    bx(0x6a4a2a, (0, .06, 0), (w - .1, .12, d - .1)); bx(0x9a7448, (0, .44, 0), (w, .64, d), .03); bx(top, (0, h - .04, 0), (w + .06, .08, d + .06), .03)
    for y in (.26, .46, .66):
        for s in (-1, 1): bx(0x7a5a34, (0, y, s * (d / 2 + .004)), (w - .08, .025, .01))
    random.seed(len(name) * 7)
    for s in (-1, 1):
        bx(0xb08a58, (s * 2.2, h + .08, 0), (.5, .16, 1.3), .02)
        for k in range(9): ball(random.choice(pile), (s * 2.2 + random.uniform(-.14, .14), h + .2 + (k // 5) * .1, -.5 + (k % 5) * .25 + random.uniform(-.04, .04)), random.uniform(.085, .12), 8, 5)
        bx(0xfff4d0, (s * 1.85, h + .2, .78), (.26, .2, .02), .01); bx(0xc8372d, (s * 1.85, h + .22, .792), (.18, .05, .006)); tube(0x8a6a3a, (s * 1.85, h, .78), (s * 1.85, h + .12, .78), .012, 4)
    end()
def fish():
    P('fish'); w, h, d = 8, 1.0, 1.6; counter(w, h, d, 0xf0f4f8, 0x9ad4f0, 0x1d5fa8)
    random.seed(3)
    for k in range(26): ball(0xf4faff, (random.uniform(-3.8, 3.8), h + .01, random.uniform(-.65, .65)), (random.uniform(.12, .22), .035, random.uniform(.1, .18)), 6, 3)
    for x, c in ((-3.5, 0xf08a7a), (-3.1, 0xe8a060), (3.2, 0xf08a7a), (3.6, 0x8aa0c0)):
        A(c, ell((x, h + .07, -.35), (.08, .05, .22), 8, 5)); A(c, cone((x, h + .07, -.55), (x, h + .07, -.68), .07, 4)); ball(0x15151a, (x + .04, h + .09, -.2), .012, 4, 3)
    add('m', M(0xcfe8ff, 'l', .3), box((0, h + .28, -d / 2 + .04), (w - .2, .5, .03))); bx(0x1d5fa8, (0, h + .55, -d / 2 + .04), (w - .1, .05, .06), .01)
    for x in (-2.5, 0, 2.5): bx(0xfff4d0, (x, h + .1, d / 2 - .06), (.3, .16, .02), .008)
    end()
def gondola():
    P('gondola'); w, h, d = 9, 1.9, 1.2; random.seed(11)
    bx(0x4a4a54, (0, .06, 0), (w, .12, d)); bx(0xe4dccc, (0, h / 2 + .05, 0), (w, h - .14, .08)); bx(0xece4d4, (0, h - .035, 0), (w + .06, .07, d + .06), .02)
    for s in (-1, 1): bx(0xd8d0c0, (s * (w / 2 - .03), h / 2, 0), (.06, h - .04, d), .012)
    pal = (0xc8372d, 0xffd23a, 0x2f8a4a, 0x3a6ad0, 0xf4f1e8, 0x8a5ab0, 0xff8a3a, 0x5ab0f0, 0xd9a521)
    for y in (.14, .56, .98, 1.4):
        bx(0xf0e8d8, (0, y, 0), (w - .1, .035, d - .04))
        for s in (-1, 1):
            bx(0xc8372d if y > 1 else 0x3a6ad0, (0, y, s * (d / 2 - .01)), (w - .1, .05, .012)); x = -w / 2 + .3
            while x < w / 2 - .3:
                c = random.choice(pal); t = random.random(); z = s * .34; hh = random.uniform(.2, .33)
                if t < .45: bx(c, (x, y + .02 + hh / 2, z), (random.uniform(.2, .3), hh, .26)); x += .36
                elif t < .8: cy(c, (x, y + .02, z), .09, hh, 7); cy(0xf4f1e8, (x, y + .02 + hh, z), .04, .05, 6); x += .28
                else: cy(c, (x, y + .02, z), .11, hh * .7, 8); x += .32
    end()
def chiller():
    P('chiller'); w, h, d = 9, 1.0, 1.2; counter(w, h, d, 0xf0f4f8, 0xbfe4f8, 0x1d5fa8)
    for s in (-1, 1): bx(0xf8fbff, (0, h + .03, s * (d / 2 - .03)), (w + .08, .07, .1), .02); bx(0xf8fbff, (s * (w / 2), h + .03, 0), (.1, .07, d + .08), .02)
    for x in (-3, 0, 3): bx(0xfff4d0, (x, h + .12, d / 2), (.3, .16, .02), .008); bx(0x3a6ad0, (x, h + .14, d / 2 + .012), (.2, .04, .006))
    end()
def corral():
    P('corral'); w, h, d = 3.2, .5, 1.6; bx(0x7a848c, (0, .05, 0), (w, .1, d), .02); bx(0x9aa4ac, (0, h - .03, 0), (w - .3, .06, d - .3), .02)
    for x in (-1.2, 0, 1.2):
        for s in (-1, 1): tube(0x9aa4ac, (x, .1, s * .55), (x, h - .06, s * .55), .03, 6)
    for s in (-1, 1): tube(0xc8372d, (s * (w / 2 - .05), .1, -.75), (s * (w / 2 - .05), .9, -.75), .035, 6); tube(0xc8372d, (s * (w / 2 - .05), .9, -.75), (s * (w / 2 - .05), .9, .75), .035, 6); tube(0xc8372d, (s * (w / 2 - .05), .9, .75), (s * (w / 2 - .05), .1, .75), .035, 6)
    end()
def register():
    P('register'); w, h, d = 3.6, 1.0, 1.1; counter(w, h, d, 0x3a4a5a, 0xd8d8d0); bx(0x1a1a20, (-.5, h + .005, 0), (2.2, .02, .6), .008)
    bx(0x2a2a30, (1.0, h + .18, 0), (.52, .34, .42), .04); bx(B(0x5ad06a), (1.0, h + .45, -.14), (.4, .26, .04)); bx(0x2a2a30, (1.0, h + .45, -.11), (.46, .32, .05), .02); bx(0xd8d8d0, (1.0, h + .37, .08), (.34, .02, .2))
    tube(0x9aa4ac, (1.6, h, .4), (1.6, h + 1.0, .4), .025, 6); bx(B(0xffd23a), (1.6, h + 1.1, .4), (.34, .24, .08), .03); bx(0xc8372d, (-1.55, h + .1, 0), (.3, .2, .5), .03)
    end()
def sample():
    P('sample'); w, h, d = 2, 1.0, 2; bx(0xf4f1e8, (0, h / 2 - .04, 0), (w - .1, h - .1, d - .1), .04); bx(0xc8372d, (0, h - .04, 0), (w + .06, .08, d + .06), .03)
    for k in range(-3, 4):
        for s in (-1, 1): bx(0xffffff if k % 2 else 0xc8372d, (k * .29, h - .2, s * (d / 2 + .034)), (.29, .26, .012)); bx(0xffffff if k % 2 else 0xc8372d, (s * (w / 2 + .034), h - .2, k * .29), (.012, .26, .29))
    cy(0x2a2a30, (-.6, h, -.6), .28, .05, 14); cy(0xb0b8c0, (-.6, h + .05, -.6), .24, .03, 14); cy(0xf4f1e8, (.65, h, -.65), .08, .14, 8)
    for k in range(5): tube(0xe8d8b0, (.65, h + .1, -.65), (.65 + math.cos(k) * .05, h + .26, -.65 + math.sin(k) * .05), .005, 3)
    end()
def pillar():
    P('pillar'); w, h, d = 1.2, 2.4, 1.2; bx(0xc8c0a8, (0, .12, 0), (w, .24, d), .03); bx(0xe4dcc4, (0, h / 2, 0), (w - .14, h - .1, d - .14), .05); bx(0xc8c0a8, (0, h - .1, 0), (w, .2, d), .03); bx(0x2f8a4a, (0, 1.05, 0), (w - .12, .12, d - .12), .012)
    bx(0xfff4d0, (0, 1.6, d / 2 - .06), (.6, .7, .02), .01); bx(0xc8372d, (0, 1.78, d / 2 - .048), (.46, .16, .01)); bx(0xffd23a, (0, 1.5, d / 2 - .048), (.3, .22, .01))
    end()
# ------------------------------ school ------------------------------
def cab(name, w):
    P(name); h, d = .95, .8; bx(0x5a4024, (0, .05, 0), (w - .1, .1, d - .1)); bx(0x8a6a3a, (0, .1 + (h - .16) / 2, 0), (w, h - .16, d), .03); bx(0xb08a58, (0, h - .03, 0), (w + .06, .06, d + .06), .02)
    n = int(w); 
    for i in range(n): x = -w / 2 + (i + .5) * w / n; bx(0xa07c4a, (x, .5, d / 2 + .004), (w / n - .08, .62, .02), .012); ball(0xe8c55a, (x + (w / n / 2 - .12) * (1 if i % 2 else -1), .52, d / 2 + .03), .028, 6, 4)
    end()
def tdesk():
    P('tdesk'); w, h, d = 3.4, 1.0, 1.3; bx(0x5a4024, (0, .05, 0), (w - .1, .1, d - .1)); bx(0x8a6a45, (0, .1 + (h - .17) / 2, 0), (w, h - .17, d), .03); bx(0xa8845a, (0, h - .035, 0), (w + .06, .07, d + .06), .02); bx(0x6a8a6a, (0, h + .005, 0), (w - .5, .012, d - .4))
    bx(0x7a5a34, (0, .55, d / 2 + .004), (w - .3, .6, .02), .01)
    cy(0x5a4024, (-1.25, h, -.2), .1, .03, 10); tube(0x9aa4ac, (-1.25, h, -.2), (-1.25, h + .2, -.2), .015, 5); A(0x3a8ad0, ell((-1.25, h + .34, -.2), .16, 12, 8)); A(0x5ab04a, ell((-1.19, h + .38, -.08), (.07, .09, .05), 6, 4)); A(0x5ab04a, ell((-1.34, h + .3, -.1), (.05, .06, .05), 6, 4))
    for i, c in enumerate((0xc8372d, 0x3a6ad0, 0xffd23a)): bx(c, (1.2, h + .035 + i * .065, 0), (.42 - i * .04, .06, .3), .01, RY(i * .2))
    ball(0xd83a2a, (1.2, h + .28, 0), .07, 8, 5); tube(0x5a4024, (1.2, h + .34, 0), (1.21, h + .38, 0), .008, 3)
    end()
def desk():
    P('desk'); bx(0xd8c098, (0, .72, 0), (1.1, .06, .8), .02); bx(0x9a7a4a, (0, .6, 0), (.96, .16, .68), .015)
    for x in (-1, 1):
        for z in (-1, 1): tube(0x8a9098, (x * .48, 0, z * .33), (x * .48, .7, z * .33), .022, 5)
        tube(0x8a9098, (x * .48, .12, -.33), (x * .48, .12, .33), .018, 4)
    bx(0xb08a58, (0, .45, .75), (.6, .05, .5), .02); bx(0xb08a58, (0, .78, .98), (.6, .26, .04), .02)
    for x in (-1, 1):
        tube(0x8a9098, (x * .26, 0, .55), (x * .26, .44, .55), .02, 5); tube(0x8a9098, (x * .26, 0, .98), (x * .26, .9, .98), .02, 5)
    end()
def locker():
    P('locker'); w, h, d = 1.2, 2.0, 2.4; bx(0x4a5560, (0, .05, 0), (w - .06, .1, d - .06)); bx(0x7a8a9a, (0, h / 2 + .04, 0), (w, h - .1, d), .03); bx(0x8a9aa8, (0, h - .02, 0), (w + .04, .05, d + .04), .015)
    for i in range(3):
        z = -d / 2 + (i + .5) * d / 3; bx(0x8e9eac, (w / 2 + .004, h / 2 + .04, z), (.02, h - .3, d / 3 - .08), .012); bx(0x3a444e, (w / 2 + .02, 1.1, z + .25), (.02, .16, .04), .008)
        for k in range(4): bx(0x4a5560, (w / 2 + .018, 1.7 - k * .06, z), (.008, .02, .4))
    end()
def sink():
    P('sink'); w, h, d = 1.4, .7, 2; bx(0x2a5aa0, (0, .05, 0), (w - .1, .1, d - .1)); bx(0x3a7ad0, (0, h / 2, 0), (w, h - .1, d), .04); bx(0xdfe8f0, (0, h - .03, 0), (w + .04, .06, d + .04), .02); bx(0xa8b8c8, (.08, h + .003, 0), (w - .5, .01, d - .3))
    bx(0x3a7ad0, (-w / 2 + .1, h + .2, 0), (.14, .4, d), .03)
    for z in (-.6, 0, .6): tube(0xc0c8d0, (-w / 2 + .17, h + .25, z), (-w / 2 + .42, h + .25, z), .025, 6); tube(0xc0c8d0, (-w / 2 + .42, h + .25, z), (-w / 2 + .42, h + .15, z), .022, 6); ball(0x3a8ad0 if z else 0xc8372d, (-w / 2 + .2, h + .32, z), .04, 6, 4)
    end()
def cubby(name, h, d):
    P(name); w = 1.2; bx(0x5a4024, (0, .05, 0), (w - .06, .1, d - .06)); bx(0x8a6a45, (w / 2 - .04, h / 2, 0), (.08, h - .06, d)); bx(0xa8845a, (0, h - .03, 0), (w + .04, .06, d + .04), .02); bx(0x8a6a45, (0, .13, 0), (w, .06, d))
    n = int(d)
    for i in range(n + 1): bx(0x8a6a45, (0, h / 2, -d / 2 + i * d / n + (.03 if i == 0 else -.03 if i == n else 0)), (w, h - .06, .06))
    bx(0x9a7a50, (0, h * .55, 0), (w, .05, d)); random.seed(int(d * 10))
    for i in range(n):
        z = -d / 2 + (i + .5) * d / n
        if random.random() < .7: bx(random.choice((0xc8372d, 0x2a2a34, 0x3a6ad0, 0xff7ab8)), (0, .32, z), (.5, .32, d / n * .5), .05)
        if random.random() < .6: bx(random.choice((0xffd23a, 0x5ab0f0, 0xf4f1e8)), (.05, h * .55 + .1, z), (.4, .14, d / n * .4), .03)
    end()
def crate():
    P('crate'); w, h, d = 2, .6, 1.2; bx(0x3a7ad0, (0, h / 2 - .02, 0), (w, h - .04, d), .04); bx(0x2a5aa0, (0, h - .03, 0), (w - .1, .03, d - .1))
    for s in (-1, 1): bx(0x2a5aa0, (0, .3, s * (d / 2 + .004)), (w - .3, .12, .01)); bx(0x5a9ae8, (s * (w / 2 + .004), .42, 0), (.01, .1, .5), .004)
    for s in (-1, 1): tube(0x5a9ae8, (s * (w / 2 - .02), h - .02, -d / 2 + .02), (s * (w / 2 - .02), h - .02, d / 2 - .02), .03, 6)
    end()
# ------------------------------ park ------------------------------
def bucket():
    P('bucket'); A(0xd8b878, ell((0, .03, 0), (.52, .1, .5), 12, 4)); A(0xff5a3a, lat([(0, 0), (0, .26), (.43, .36), (.45, .38), (.43, .3), (.04, .22), (.04, 0)], 14)); A(0xffd23a, tor((0, .44, 0), .37, .02, (1, 0, 0), 12, 4, arc=.5)); A(0xd8b878, ell((0, .4, 0), (.3, .05, .3), 10, 3))
    end()
def tree():
    P('tree'); A(0x6b4a2a, lat([(0, 0), (0, .42), (.2, .3), (.9, .24), (1.7, .2), (1.75, 0)], 10))
    for a in range(4): A(0x6b4a2a, cone((math.cos(a * 1.57 + .4) * .2, .12, math.sin(a * 1.57 + .4) * .2), (math.cos(a * 1.57 + .4) * .62, 0, math.sin(a * 1.57 + .4) * .62), .13, 5))
    random.seed(5)
    def lump(v): n = v.normalized() if v.length > 0 else v; return v + n * (.07 * math.sin(v.x * 9) * math.cos(v.z * 8 + v.y * 6))
    for p, r, c in (((0, 2.3, 0), 1.2, 0x3f8a3a), ((.6, 2.0, .3), .85, 0x4a9a42), ((-.55, 2.1, -.2), .9, 0x357a33), ((0, 2.95, 0), .85, 0x4fa348), ((.1, 2.4, .75), .6, 0x4a9a42)):
        A(c, ell(p, r, 12, 8, None, lump))
    for p in ((.7, 2.2, .95), (-.5, 2.6, .85), (.2, 3.2, .7), (-.9, 2.0, .5)): ball(0xff5a3a, p, .07, 6, 4)
    end()
def slide():
    P('slide'); 
    for s in (-1, 1):
        tube(0x3a6ad0, (s * .5, 0, -1.9), (s * .5, 2.1, -1.2), .04, 6); tube(0x3a6ad0, (s * .5, 0, -.9), (s * .5, 1.6, -.9), .04, 6); tube(0x3a6ad0, (s * .5, 2.1, -1.2), (s * .5, 2.1, -.9), .04, 6); tube(0x3a6ad0, (s * .5, 2.1, -.9), (s * .5, 1.6, -.9), .035, 6)
        A(0xff8a3a, box((s * .52, .93, .65), (.07, .32, 3.5), RX(math.atan2(1.5, 3.1))), bevel=.02)
    for k in range(6): t = (k + 1) / 7; tube(0xffd23a, (-.5, 2.1 * t * .8, -1.9 + .7 * t * .8), (.5, 2.1 * t * .8, -1.9 + .7 * t * .8), .03, 5)
    bx(0xffd23a, (0, 1.6, -1.05), (1.05, .06, .4), .02); A(0xffd23a, box((0, .82, .65), (1.0, .05, 3.5), RX(math.atan2(1.5, 3.1))), bevel=.02); bx(0xffd23a, (0, .1, 2.0), (1.0, .05, .5), .02)
    end()
def jungle():
    P('jungle')
    for i in range(4):
        for j in range(4): tube(0xd04a3a, (-1.5 + i, 0, -1.5 + j), (-1.5 + i, 2.0, -1.5 + j), .04, 6); ball(0xffd23a, (-1.5 + i, 2.02, -1.5 + j), .06, 6, 4)
    for y in (.65, 1.3, 1.95):
        for k in range(4): tube(0x3a6ad0, (-1.5, y, -1.5 + k), (1.5, y, -1.5 + k), .03, 5); tube(0x3a6ad0, (-1.5 + k, y, -1.5), (-1.5 + k, y, 1.5), .03, 5)
    end()
def fountain():
    P('fountain'); w, h, d = 2.4, .9, 1.6; bx(0x8a9098, (0, .08, 0), (w, .16, d), .04); bx(0xa8b0b8, (0, h / 2 + .04, 0), (w - .3, h - .16, d - .3), .08); bx(0xc4ccd4, (0, h - .04, 0), (w, .08, d), .04)
    for x in (-.85, .85): cy(0x8a9098, (x, h, -.5), .12, .03, 10); tube(0xd0d8e0, (x, h, -.5), (x, h + .22, -.5), .03, 6); tube(0xd0d8e0, (x, h + .22, -.5), (x, h + .2, -.32), .025, 6); ball(0x3a6ad0, (x, h + .27, -.5), .045, 6, 4)
    add('m', M(0x6ac4f0, 'l', .7), ell((0, h + .01, -.5), (.4, .02, .18), 10, 3))
    end()
def bin_():
    P('bin'); A(0x3a6ad0, lat([(0, 0), (0, .62), (.64, .76), (.7, .78), (.7, .7), (.66, .68), (.66, 0)], 16)); A(0x2a4a9a, tor((0, .35, 0), .7, .03, (0, 1, 0), 16, 4))
    for a, c in ((0, 0xe03a2a), (2.1, 0xffd23a), (4.2, 0x5ab04a)): ball(c, (math.cos(a) * .38, .58, math.sin(a) * .38), .22, 10, 6)
    end()
def ramp():
    P('ramp'); w, h, d = 3, .6, 1.2; v = [(-1.5, 0, -.6), (-1.5, 0, .6), (1.5, 0, .6), (1.5, 0, -.6), (-1.0, h, -.6), (-1.0, h, .6), (1.0, h, .6), (1.0, h, -.6)]
    add('m', 0x6a6a72, (v, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (0, 4, 7, 3)]), sharp=30)
    for s in (-1, 1): tube(0xd0d8e0, (s * 1.0, h, -.6), (s * 1.0, h, .6), .035, 6); bx(0xffd23a, (s * 1.27, .3, 0), (.5, .012, .2), None, RZ(-s * math.atan2(.6, .5)))
    bx(0xc8372d, (0, h + .004, 0), (1.4, .01, .14))
    end()
def bench():
    P('bench'); 
    for k in range(4): bx(0xa8743f if k % 2 else 0x9a6836, (0, .47, -.28 + k * .19), (2.6, .05, .17), .015)
    for k in range(2): bx(0xa8743f, (0, .74 + k * .2, -.4), (2.6, .16, .05), .015, RX(-.12))
    for s in (-1, 1):
        bx(0x3a3a44, (s * 1.1, .22, 0), (.08, .44, .7), .02); bx(0x3a3a44, (s * 1.1, .7, -.4), (.07, .56, .07), .015, RX(-.12)); bx(0x3a3a44, (s * 1.1, .03, 0), (.12, .06, .78), .015)
    end()
def feedbox():
    P('feedbox'); w, h, d = 1.2, 1.0, 1.2; tube(0x8a6a3a, (0, 0, 0), (0, .5, 0), .12, 8); bx(0xc9a45a, (0, .72, 0), (w - .1, .5, d - .1), .04); bx(0x8a5a2a, (0, h - .03, 0), (w + .06, .06, d + .06), .02)
    bx(0xf4ecd8, (0, .72, d / 2 - .045), (.5, .34, .02), .01); A(0x8a8f9a, ell((-.02, .72, d / 2 - .03), (.1, .075, .02), 8, 4)); ball(0x8a8f9a, (.08, .79, d / 2 - .03), .05, 6, 4); A(0xff8a2a, cone((.12, .79, d / 2 - .03), (.18, .78, d / 2 - .03), .018, 4))
    bx(0x3a3a44, (.38, .8, d / 2 - .04), (.12, .03, .02))
    end()
def kiosk():
    P('kiosk'); w, h, d = 2, 1.0, 1.4; bx(0xff8ab8, (0, h / 2 - .04, 0), (w - .06, h - .1, d - .06), .04); bx(0xffffff, (0, h - .04, 0), (w + .08, .08, d + .08), .03)
    for k in range(-4, 5):
        for s in (-1, 1): A(0xffffff if k % 2 else 0xffc0d8, ell((k * .23, h - .1, s * (d / 2)), (.12, .1, .02), 8, 4))
    for p, r in (((-.8, h + .35, -.5), .13), ((.85, h + .5, -.45), .1), ((-.95, h + .65, -.3), .07), ((.7, h + .8, -.55), .06)): add('m', M(0xcfeaff, 'l', .4), ell(p, r, 10, 6))
    end()
def icestand():
    P('icestand'); w, h, d = 2, 1.7, 4; bx(0xd8d0c0, (0, .06, 0), (w - .1, .12, d - .1)); bx(0xf8f4ec, (0, h / 2 + .03, 0), (w, h - .14, d), .04); bx(0xff7ab8, (0, .5, 0), (w + .02, .22, d + .02), .01); bx(0xffffff, (0, h - .03, 0), (w + .06, .06, d + .06), .02)
    bx(0x6a5a50, (w / 2 + .004, 1.15, -.4), (.02, .6, 2.2), .01); bx(0xffffff, (w / 2 + .1, .84, -.4), (.24, .05, 2.4), .02)
    for k in range(8): A(0xff7ab8 if k % 2 else 0xffffff, box((w / 2 + .28, 1.55, -1.45 + k * .3), (.62, .04, .3), RZ(-.35)))
    A(0xd9a050, lat([(0, 0), (0, .01), (.7, .3), (.72, .3), (.72, 0)], 12, frame((0, h, 1.3)))); 
    for i, (y, r) in enumerate(((.82, .34), (1.05, .27), (1.25, .2), (1.4, .12))): A(0xfffaf0, ell((0, h + y, 1.3), (r, .15, r), 12, 5))
    A(0xfffaf0, cone((0, h + 1.45, 1.3), (.06, h + 1.7, 1.3), .07, 6)); ball(0xff3a4a, (.1, h + 1.38, 1.42), .07, 6, 4)
    end()
# ------------------------------ arcade ------------------------------
def arcab(name, col):
    P(name); D = 0x1a1a2a
    for s in (-1, 1):
        v = [(s * .55, 0, -.5), (s * .55, 0, .5), (s * .55, .85, .5), (s * .55, .98, .72), (s * .55, 1.06, .72), (s * .55, 1.0, .5), (s * .55, 1.62, .5), (s * .55, 1.72, .62), (s * .55, 1.8, .62), (s * .55, 1.8, -.5)]
        v2 = [(p[0] - s * .06, p[1], p[2]) for p in v]; n = len(v)
        add('m', col, (v + v2, [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]), sharp=30)
    bx(col, (0, .9, -.46), (1.0, 1.8, .06)); bx(D, (0, .45, .47), (1.0, .9, .04)); bx(D, (0, 1.3, .485), (1.0, .64, .02)); bx(col, (0, 1.79, .05), (1.0, .03, 1.1))
    A(D, box((0, .99, .6), (1.0, .05, .27), RX(.5))); bx(B(0xffd23a), (0, 1.71, .6), (.98, .14, .04), .01); bx(B(0xff4ad0), (0, 1.71, .625), (.6, .06, .01))
    tube(0x9aa4ac, (-.25, 1.0, .6), (-.25, 1.1, .62), .012, 4); ball(0xff3a3a, (-.25, 1.12, .625), .04, 6, 4)
    for i, c in enumerate((0xff3a3a, 0x3a8aff, 0xffd23a)): cy(B(c), (.08 + i * .13, 1.0, .64 - i * .01), .035, .03, 8)
    bx(0x30303c, (0, .4, .495), (.4, .3, .01)); bx(B(0xffd23a), (-.08, .46, .503), (.03, .08, .004)); bx(B(0xffd23a), (.08, .46, .503), (.03, .08, .004)); bx(0x0c0c14, (0, .08, .495), (1.0, .14, .01))
    end()
def crane():
    P('crane'); w, h, d = 5, 1.0, 2.4; counter(w, h, d, 0xff7ab8, 0xffffff, 0xff4ad0)
    for x in (-1, 1):
        for z in (-1, 1): bx(0xff4ad0, (x * (w / 2 - .06), h + .8, z * (d / 2 - .06)), (.12, 1.6, .12), .02)
    bx(0xff7ab8, (0, h + 1.7, 0), (w + .1, .22, d + .1), .04); tube(0xb0b8c0, (-w / 2 + .1, h + 1.5, 0), (w / 2 - .1, h + 1.5, 0), .03, 5)
    bx(0x8a9098, (1.2, h + 1.42, 0), (.3, .14, .3), .02); tube(0x8a9098, (1.2, h + 1.4, 0), (1.2, h + 1.0, 0), .012, 4)
    for a in range(3): tube(0xc0c0c8, (1.2, h + 1.0, 0), (1.2 + math.cos(a * 2.09) * .16, h + .78, math.sin(a * 2.09) * .16), .018, 4)
    bx(0x30203a, (-1.4, h * .55, d / 2 + .1), (1.2, .3, .24), .03); tube(0x9aa4ac, (-1.6, h * .55 + .15, d / 2 + .12), (-1.6, h * .55 + .3, d / 2 + .12), .014, 4); ball(0xff3a3a, (-1.6, h * .55 + .32, d / 2 + .12), .05, 6, 4)
    for i, c in enumerate((0x3ad8ff, 0xffd23a)): cy(B(c), (-1.25 + i * .22, h * .55 + .15, d / 2 + .12), .05, .03, 8)
    bx(0x1a1020, (1.5, .35, d / 2 + .01), (.8, .4, .02), .02)
    end()
def snackcase():
    P('snackcase'); w, h, d = 5, 1.0, 1.8; counter(w, h, d, 0xffd23a, 0xffffff, 0xc8372d)
    for x in (-1, 1):
        for z in (-1, 1): bx(0xc8372d, (x * (w / 2 - .06), h + .7, z * (d / 2 - .06)), (.1, 1.4, .1), .02)
    bx(0xffd23a, (0, h + 1.5, 0), (w + .1, .2, d + .1), .04)
    for k in range(10): A(0xc8372d if k % 2 else 0xffffff, box((-2.25 + k * .5, h + 1.34, d / 2 + .22), (.5, .04, .5), RX(.45)))
    end()
def gachas():
    P('gachas'); w, h, d = 1.6, 1.2, 5; counter(w, h, d, 0xc8372d, 0xf4f1e8); random.seed(9)
    for z in (-1.6, 0, 1.6):
        bx(0xf4f1e8, (.4, h + .22, z), (.72, .44, .9), .05); bx(0xc8372d, (.4, h + .47, z), (.78, .08, .96), .03)
        add('m', M(0xcfe8ff, 'l', .35), lat([(0, .43), (.2, .44), (.42, .36), (.56, .2), (.62, 0)], 14, frame((.4, h + .5, z))))
        for k in range(9): ball(random.choice((0xff3a6a, 0x3ad8ff, 0xffd23a, 0x5aff7a, 0x8a5ab0)), (.4 + random.uniform(-.24, .24), h + .6 + random.uniform(0, .22), z + random.uniform(-.24, .24)), .09, 7, 4)
        cy(0x9aa4ac, (.0, h + .22, z), .09, .05, 10); bx(0x30303a, (-.38, .75, z), (.02, .22, .34), .02); bx(B(0xffd23a), (-.385, 1.0, z), (.01, .1, .5))
    end()
def medalgame():
    P('medalgame'); A(0x9a7418, lat([(0, 0), (0, 1.42), (.12, 1.42), (.12, 0)], 8)); A(0xd9a521, lat([(.12, 1.48), (.9, 1.5), (1.02, 1.44), (1.03, 0)], 8), sharp=30); A(0xffe88a, lat([(1.03, 1.52), (1.1, 1.52), (1.1, 0)], 8), sharp=30)
    for k in range(8): a = (k + .5) * PI / 4; ball(B(0xff4ad0 if k % 2 else 0x3ad8ff), (math.cos(a) * 1.42, .75, math.sin(a) * 1.42), .07, 6, 4)
    for k in range(8): a = k * PI / 4; A((0xc8372d, 0xf4f1e8)[k % 2], box((math.cos(a) * 1.25, 1.104, math.sin(a) * 1.25), (.36, .01, .5), RY(-a)))
    end()
def mole():
    P('mole'); w, h, d = 4, .9, 1.6; counter(w, h, d, 0x3a8ad0, 0xffd23a, 0xffffff)
    for i, x in enumerate((-1.5, -.5, .5, 1.5)):
        for j, z in enumerate((-.5, .5)):
            cy(0x2a1a14, (x, h + .001, z), .19, .012, 12)
            if (i + j) % 2 == 0:
                A(0x8a5a32, ell((x, h + .08, z), (.16, .2, .16), 10, 6)); ball(0xf4d8b0, (x, h + .1, z + .13), .06, 6, 4); ball(0xff7a8a, (x, h + .12, z + .185), .025, 5, 3)
                for s in (-1, 1): ball(0x15151a, (x + s * .06, h + .2, z + .12), .022, 5, 3)
    bx(0xc8372d, (0, h + .25, -d / 2 + .05), (w - .2, .5, .08), .03)
    for k in range(7): ball(B((0xff4ad0, 0x3ad8ff, 0x5aff7a)[k % 3]), (-1.5 + k * .5, h + .4, -d / 2 + .1), .05, 6, 4)
    end()
def candystand():
    P('candystand'); w, h, d = 3, 1.0, 1.2; counter(w, h, d, 0x8a5ab0, 0xff7ab8, 0xffffff)
    for s in (-1, 1):
        for k in range(6): cy(0xff4a9a if k % 2 else 0xffffff, (s * 1.3, h + k * .13, -.4), .04, .13, 8)
        A(0xfff4f8, lat([(-.03, 0), (-.03, .2), (.03, .2), (.03, 0)], 16, frame((s * 1.3, h + .98, -.4), (0, 0, 1)))); A((0xff4a9a, 0x3ad8ff)[s > 0], tor((s * 1.3, h + .98, -.4), .2, .02, (0, 0, 1), 16, 4)); A((0xff4a9a, 0x3ad8ff)[s > 0], tor((s * 1.3, h + .98, -.365), .1, .018, (0, 0, 1), 12, 4))
    end()
# ------------------------------ gimmicks ------------------------------
def gm_roomba():
    P('gm_roomba'); A(0x3a3a44, lat([(0, 0), (.02, .43), (.1, .46), (.14, .44), (.165, .3), (.165, 0)], 22)); A(0x55555f, lat([(.166, 0), (.166, .26), (.17, .24), (.172, 0)], 18)); A(0x25252c, tor((0, .07, 0), .455, .03, (0, 1, 0), 22, 5))
    bx(0x25252c, (0, .15, .38), (.3, .04, .08), .015); 
    for s in (-1, 1): ball(B(0xffffff), (s * .12, .13, .43), .03, 6, 4)
    end()
def gm_sprinkler():
    P('gm_sprinkler'); cy(0x5a5a5a, (0, 0, 0), .16, .06, 10); tube(0x7a7a80, (0, .05, 0), (0, .26, 0), .05, 8); A(0xd0a030, lat([(0, 0), (0, .09), (.06, .1), (.1, .05), (.11, 0)], 10, frame((0, .26, 0))))
    for a in range(3): tube(0xd0a030, (0, .32, 0), (math.cos(a * 2.09) * .16, .36, math.sin(a * 2.09) * .16), .018, 5)
    end()
def gm_clawhub():
    P('gm_clawhub'); A(0xd8d8d8, lat([(-.2, 0), (-.2, .3), (-.1, .36), (.12, .34), (.2, .2), (.22, 0)], 14)); A(0xff3a2a, tor((0, -.02, 0), .34, .04, (0, 1, 0), 14, 5)); ball(B(0xffd23a), (0, -.2, 0), .08, 8, 5)
    end()
def gm_prong():
    P('gm_prong'); tube(0xc0c0c8, (0, 0, 0), (.16, -.42, 0), .045, 6); tube(0xc0c0c8, (.16, -.42, 0), (0, -.9, 0), .04, 6); ball(0x8a9098, (0, 0, 0), .07, 6, 4); ball(0xff3a2a, (0, -.9, 0), .06, 6, 4)
    end()
def gm_stone():
    P('gm_stone'); 
    def rough(v): return v * (1 + .05 * math.sin(v.x * 3.1 + 1) * math.cos(v.z * 2.7) + .04 * math.sin(v.y * 5))
    A(0x8a8478, ell((0, 0, 0), (1.7, 1.22, 1.7), 18, 12, None, rough)); A(0xd8c090, tor((0, .25, 0), 1.62, .13, (0, 1, 0), 24, 6)); A(0xd8c090, tor((0, .25, 0), 1.25, .13, (1, 0, 0), 20, 6, sz=1.02)); 
    for p in ((.9, .7, .9), (-1.0, .5, .6), (.3, -.2, -1.5)): A(0x767064, ell(p, (.3, .2, .3), 6, 4))
    A(0xf4f1e8, box((0, .62, 1.58), (.5, .7, .03), RX(-.38))); A(0xc8372d, box((0, .68, 1.6), (.3, .3, .02), RX(-.38)))
    end(scale=4.0)
ALL = [lambda: veg('veg', 0x5a8a3a, (0x6ab04a, 0xd83a2a, 0xff8a2a, 0x8ac04a)), lambda: veg('vegy', 0xd9a521, (0xffd23a, 0xff8a2a, 0xd83a2a, 0x8ac04a)), fish, gondola, chiller, corral, register, sample, pillar,
       lambda: cab('cab5', 5), lambda: cab('cab4', 4), tdesk, desk, locker, sink, lambda: cubby('cubby5', 1.3, 5), lambda: cubby('cubby3', 1.1, 3), crate,
       bucket, tree, slide, jungle, fountain, bin_, ramp, bench, feedbox, kiosk, icestand,
       lambda: arcab('arcab0', 0x3a2a6a), lambda: arcab('arcab1', 0x6a2a4a), lambda: arcab('arcab2', 0x2a4a6a), crane, snackcase, gachas, medalgame, mole, candystand,
       gm_roomba, gm_sprinkler, gm_clawhub, gm_prong, gm_stone]
