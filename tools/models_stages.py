# Voxel stages, US style. Every prop's origin is the centre of its collision footprint on the floor.
import math, random
from vox import Vox, export, shade
OUT = {}
def V(vs=.1, seed=1): return Vox(vs, seed)
def E(v, name): export(v, 'pr_' + name, OUT)
GLASS = dict(kind='l', op=.28)
def glow(c): return dict(kind='b')
WOOD = 0xa8743f; METAL = 0xb8c0c8; DARK = 0x3a3f48; WHITE = 0xf4f4f0

# =============================== walls ===============================
def walls(st, col, band, top, deco=None, h=2.8, sh=.9):
    for side in ('n', 's', 'w', 'e'):
        v = V(.2, 7)
        hh = sh if side == 's' else h
        if side in 'ns': v.cbox(0, 0, 0, 42, hh, 1, col); v.cbox(0, 0, 0, 42.2, .4, 1.1, band); v.cbox(0, hh - .2, 0, 42.2, .2, 1.1, top)
        else: v.cbox(0, 0, 0, 1, hh, 32, col); v.cbox(0, 0, 0, 1.1, .4, 32.2, band); v.cbox(0, hh - .2, 0, 1.1, .2, 32.2, top)
        if deco: deco(v, side, hh)
        E(v, 'wall_%s_%s' % (st, side))

def super_deco(v, side, h):
    if side == 'n':   # inner face is z=+0.5
        for x0, x1, c, t in ((-19, -8, 0x2f8a4a, 'PRODUCE'), (-7, 5, 0x3a6ad0, 'DAIRY'), (6, 19, 0xc8372d, 'SEAFOOD')):
            v.box(x0, 1.6, .5, x1, 2.6, .7, c); w = len(t) * .64 - .16; v.text((x0 + x1) / 2 - w / 2, 1.72, .7, t, WHITE, scale=.8)
    if side == 'w':
        v.box(.5, 1.6, -8, .7, 2.6, 4, 0xd9a521); v.text(.7, 1.72, -2 - 1.2, 'DELI', 0x2a1d14, axis='x', scale=.8)
    if side == 'e':
        v.box(-.7, 1.6, 4, -.5, 2.6, 15, 0xc8372d); v.text(-.7, 1.72, 9.5 + 2.5, 'CHECKOUT', WHITE, axis='-x', scale=.8)
def school_deco(v, side, h):
    if side == 'n':
        v.box(-7.2, .8, .5, 7.2, 2.4, .6, 0x8a6a3a); v.box(-7, .9, .6, 7, 2.3, .7, 0x2f4a3a)
        v.text(-2.5, 1.2, .7, 'BE NICE!', 0xf4f4f0)
        for i in range(13): v.box(-12.8 + i * .4, 2.42, .5, -12.4 + i * .4, 2.62, .7, (0xc8372d, 0xf4f4f0)[i % 2])
        for i, c in enumerate((0xc8372d, 0xf4f4f0) * 3): v.box(-15.4, 1.4 + i * .2, .5, -13.6, 1.6 + i * .2, .7, c)
        v.box(-15.4, 2.0, .5, -14.6, 2.6, .72, 0x2a3a8a)
        for (x, y) in ((-15.2, 2.4), (-14.8, 2.4), (-15.0, 2.2), (-15.2, 2.0), (-14.8, 2.0)): v.box(x, y, .72, x + .2, y + .2, .76, WHITE)
        v.box(8.4, 1.8, .5, 9.6, 2.8, .7, WHITE); v.box(8.6, 2.0, .7, 9.4, 2.6, .74, 0xf4f4f0); v.box(8.9, 2.2, .74, 9.1, 2.6, .78, DARK); v.box(9.0, 2.2, .74, 9.4, 2.4, .78, DARK)
        v.box(11, 1.4, .5, 17, 2.6, .7, 0x1d3a8a); v.text(11.3, 1.62, .7, 'GO EAGLES', 0xffd23a, scale=.8)
    if side == 'e':
        v.box(-.7, 1.0, -14, -.5, 2.4, -10, 0x8a6a3a); v.box(-.75, 1.1, -13.8, -.6, 2.3, -10.2, 0xcfe8ff, kind='l', op=.35)
        for z in (-13.4, -12.4, -11.2): v.box(-.6, 1.2, z, -.4, 1.8, z + .4, 0xffd23a)
def park_deco(v, side, h):
    for k in range(-80, 81):
        x = k * .2 if side in 'ns' else 0; z = 0 if side in 'ns' else k * .2
        if abs(x) > 21 or abs(z) > 16: continue
        if k % 6 == 0: v.box(x - .1, 0, z - .1, x + .1, h + .2, z + .1, 0x2f5a2a)
def arcade_deco(v, side, h):
    neon = (0xff4ad0, 0x3ad8ff, 0xffd23a, 0x5aff7a)
    if side == 'n':
        v.box(-21, 2.2, .5, 21, 2.4, .7, 0x3ad8ff, kind='b')
        v.text(-8.0, .8, .7, 'ARCADE', 0xff4ad0, scale=1.2, kind='b'); v.text(3.0, .8, .7, 'PLAY!', 0xffd23a, scale=1.2, kind='b')
    elif side in 'we':
        x = .5 if side == 'w' else -.7
        v.box(x, 2.2, -16, x + .2, 2.4, 16, 0xff4ad0, kind='b')
        if side == 'w': v.text(.7, 1.0, 3.6, 'TOKENS', 0xffd23a, axis='x', kind='b')
        else: v.text(-.7, 1.0, 14.6, 'PRIZES', 0x5aff7a, axis='-x', kind='b')

# =============================== supermarket ===============================
def produce(name, crate_fill):
    v = V(.1, len(name)); R = random.Random(len(name))
    w, d, h = 5, 1.8, .85
    v.cbox(0, 0, 0, w, .15, d, DARK); v.cbox(0, .15, 0, w, .55, d, 0x7a5a34, jit=.05)
    for i in range(5):
        x = -2 + i
        v.cbox(x, .7, 0, .9, .1, 1.7, WOOD, jit=.06); v.cbox(x, .8, -.8, .9, .3, .1, WOOD); v.cbox(x, .8, .8, .9, .3, .1, WOOD)
        c = crate_fill[i % len(crate_fill)]
        for xx in range(-4, 4):
            for zz in range(-7, 7):
                hh = .1 + .1 * (R.random() < .55) + .1 * (abs(zz) < 4 and R.random() < .5)
                v.box(x + xx * .1, .8, zz * .1, x + xx * .1 + .1, .8 + hh, zz * .1 + .1, shade(c, R.choice((.9, 1, 1.1))))
    v.cbox(0, .85, -1.0, w, .9, .1, 0x5a4024); v.cbox(-1.5, 1.4, -1.0, 1.6, .5, .12, 0xfff4d0); v.cbox(1.5, 1.4, -1.0, 1.6, .5, .12, 0xfff4d0)
    v.text(-2.1, 1.45, -.94, '99', 0xc8372d); v.text(.9, 1.45, -.94, '1.49', 0xc8372d)
    E(v, name)
def gondola(name, length=8, tag='3'):
    v = V(.1, 11); R = random.Random(11); w, h = 1.2, 2.0
    v.cbox(0, 0, 0, w, .15, length, DARK); v.cbox(0, 0, 0, .12, h, length, 0xd8d0c0); v.cbox(0, h - .1, 0, w, .1, length, 0xe8e0d0)
    pal = (0xc8372d, 0xffd23a, 0x2f8a4a, 0x3a6ad0, 0xf4f1e8, 0x8a5ab0, 0xff8a3a, 0x5ab0f0, 0xd9a521, 0x7a3a2a)
    for y in (.15, .6, 1.05, 1.5):
        for s in (-1, 1):
            v.box(s * .06, y, -length / 2, s * .6, y + .05, length / 2, 0xf0e8d8); v.box(s * .6 - (.03 if s > 0 else 0), y, -length / 2, s * .6 + (.03 if s < 0 else 0), y + .1, length / 2, 0xc8372d if y > 1 else 0x3a6ad0)
            z = -length / 2 + .05
            while z < length / 2 - .2:
                bw = R.choice((.2, .2, .3, .4)); bh = R.choice((.2, .3, .3, .4)); c = R.choice(pal); dep = R.choice((.3, .4, .5))
                x0 = s * .1; x1 = s * (.1 + dep)
                v.box(x0, y + .05, z, x1, y + .05 + bh, z + bw - .02, c)
                if bh >= .3: v.box(x0, y + .05 + bh * .4, z, x1 + s * .01, y + .05 + bh * .7, z + bw - .02, shade(c, 1.3) if c != 0xf4f1e8 else 0xc8372d)
                z += bw
    for s in (-1, 1):
        v.box(-.6, 0, s * length / 2 - (.3 if s > 0 else 0), .6, 1.4, s * length / 2 + (0 if s > 0 else .3), 0xffd23a)
        v.box(-.4, .2, s * length / 2 + (.0 if s > 0 else -.02), .4, .6, s * length / 2 + (.02 if s > 0 else 0), 0xc8372d)
    v.cbox(0, h, 0, .1, .8, .1, METAL); v.cbox(0, h + .8, 0, 1.6, .6, .12, 0x1d5fa8)
    v.text(-.5, h + .9, .06, 'AISLE', WHITE, scale=.5); v.text(-.1, h + .9, -.18, tag, 0xffd23a)
    E(v, name)
def dairy():
    v = V(.1, 3); w, d, h = 9, .8, 2.3
    v.cbox(0, 0, 0, w, h, d, 0xe8eef4); v.cbox(0, 0, 0, w, .3, d + .02, DARK); v.cbox(0, h - .3, 0, w + .02, .3, d + .02, 0x3a6ad0)
    v.text(-1.0, h - .27, d / 2 + .01, 'MILK', WHITE, scale=.6)
    R = random.Random(4)
    for k in range(6):
        x = -4.5 + k * 1.5
        v.box(x + .05, .35, -.3, x + 1.45, h - .35, d / 2 - .1, 0x10161e)
        for y in (.4, .9, 1.4):
            v.box(x + .05, y, -.3, x + 1.45, y + .04, .2, METAL)
            for j in range(7): c = R.choice((WHITE, WHITE, 0x3a6ad0, 0xc8372d, 0xffd23a)); v.box(x + .1 + j * .19, y + .04, -.2, x + .25 + j * .19, y + .34, .1, c)
        v.box(x + .05, .35, d / 2 - .1, x + 1.45, h - .35, d / 2, **dict(col=0xcfe8ff, **GLASS)); v.box(x, .35, d / 2 - .1, x + .05, h - .35, d / 2 + .02, METAL); v.box(x + 1.2, 1.0, d / 2, x + 1.25, 1.6, d / 2 + .08, METAL)
    E(v, 'dairy')
def seafood():
    v = V(.1, 5); w, d, h = 8, 1.6, 1.0; R = random.Random(5)
    v.cbox(0, 0, 0, w, .9, d, 0xf0f4f8); v.cbox(0, 0, 0, w, .2, d + .02, 0x1d5fa8); v.cbox(0, .9, 0, w, .1, d, METAL)
    for i in range(-38, 38):
        for k in range(-6, 7): v.box(i * .1, 1.0, k * .1, i * .1 + .1, 1.0 + .1 * (R.random() < .5), k * .1 + .1, shade(0xf4faff, R.choice((.95, 1))))
    for x, c in ((-3.2, 0xe8a060), (-2, 0x8aa0c0), (-.6, 0xf08a7a), (.8, 0x8aa0c0), (2.4, 0xe8a060), (3.4, 0xf08a7a)):
        v.box(x - .2, 1.1, -.3, x + .3, 1.25, .1, c); v.box(x + .3, 1.12, -.25, x + .45, 1.23, .05, shade(c, .8)); v.voxel(x - .15, 1.2, .1, 0x15151a)
    v.box(-w / 2, 1.0, d / 2 - .1, w / 2, 1.7, d / 2, **dict(col=0xcfe8ff, **GLASS)); v.box(-w / 2, 1.7, -.1, w / 2, 1.8, d / 2, METAL)
    for x in (-2.5, 0, 2.5): v.cbox(x, .45, d / 2, .5, .3, .04, 0xfff4d0)
    E(v, 'seafood')
def coffin():
    v = V(.1, 6); w, d, h = 9, 1.2, 1.0
    v.cbox(0, 0, 0, w, .15, d, DARK); v.cbox(0, .15, 0, w, .75, d, 0xf0f4f8, jit=.02); v.cbox(0, .55, 0, w + .02, .15, d + .02, 0x1d5fa8)
    v.box(-w / 2, .9, -d / 2, w / 2, 1.0, -d / 2 + .1, WHITE); v.box(-w / 2, .9, d / 2 - .1, w / 2, 1.0, d / 2, WHITE); v.box(-w / 2, .9, -d / 2, -w / 2 + .1, 1.0, d / 2, WHITE); v.box(w / 2 - .1, .9, -d / 2, w / 2, 1.0, d / 2, WHITE)
    v.box(-w / 2 + .1, .85, -d / 2 + .1, w / 2 - .1, .9, d / 2 - .1, 0xbfe4f8)
    for x in (-3, 0, 3): v.cbox(x, .3, d / 2, .6, .2, .04, 0xffd23a)
    E(v, 'coffin')
def wagon():
    v = V(.1, 8); R = random.Random(8); w, d = 1.6, 1.0
    for x in (-.7, .7):
        for z in (-.4, .4): v.cbox(x, 0, z, .1, .3, .1, METAL)
    v.cbox(0, .3, 0, w, .1, d, METAL)
    for k in range(17): v.box(-.8 + k * .1, .4, -.5, -.75 + k * .1, .9, -.45, METAL); v.box(-.8 + k * .1, .4, .45, -.75 + k * .1, .9, .5, METAL)
    for k in range(11): v.box(-.8, .4, -.5 + k * .1, -.75, .9, -.45 + k * .1, METAL); v.box(.75, .4, -.5 + k * .1, .8, .9, -.45 + k * .1, METAL)
    v.box(-.8, .85, -.5, .8, .9, .5, METAL, erase=False)
    for i in range(-7, 7):
        for k in range(-4, 4): v.box(i * .1, .4, k * .1, i * .1 + .1, .4 + .1 * R.choice((2, 3, 3, 4)), k * .1 + .1, R.choice((0xc8372d, 0xffd23a, 0x3a6ad0, 0x2f8a4a, 0xff8a3a)))
    v.cbox(0, .9, 0, .1, .6, .1, METAL); v.cbox(0, 1.5, 0, 1.2, .5, .1, 0xc8372d); v.text(-.5, 1.55, .05, 'SALE', 0xffd23a, scale=.6)
    E(v, 'wagon')
def checkout():
    v = V(.1, 9); w, d, h = 3.6, 1.1, 1.0
    v.cbox(0, 0, 0, w, .9, d, 0x3a4a5a); v.cbox(0, .9, 0, w + .04, .1, d + .04, 0xd8d8d0); v.box(-1.7, 1.0, -.4, .6, 1.03, .2, 0x15151a, jit=.08)
    v.cbox(1.1, 1.0, -.1, .5, .3, .4, 0x2a2a30); v.cbox(1.1, 1.3, -.25, .5, .35, .08, 0x2a2a30); v.cbox(1.1, 1.35, -.2, .4, .25, .04, 0x5ad06a, kind='b')
    v.cbox(1.5, 1.0, .35, .2, .25, .15, DARK); v.cbox(1.5, 1.25, .35, .18, .05, .1, 0x5ad06a, kind='b')
    v.cbox(1.7, 1.0, -.45, .1, 1.3, .1, METAL); v.cbox(1.7, 2.3, -.45, .5, .5, .3, 0xffd23a, kind='b'); v.text(1.6, 2.32, -.29, '1', 0x2a2a30, scale=1)
    R = random.Random(9)
    for y in (.1, .4, .7):
        for k in range(10): v.box(-1.7 + k * .18, y, d / 2, -1.55 + k * .18, y + .2, d / 2 + .12, R.choice((0xc8372d, 0xffd23a, 0x3a6ad0, 0x8a5ab0, 0x2f8a4a)))
    E(v, 'checkout')
def corral():
    v = V(.1, 10); w, d = 3.2, 1.6
    v.cbox(0, 0, 0, w, .05, d, 0x8a9098)
    for s in (-1, 1):
        v.box(-1.6, 0, s * .8 - .05, 1.6, 1.0, s * .8 + .05, 0xc8372d, erase=False)
        v.box(-1.5, .1, s * .8 - .05, 1.5, .9, s * .8 + .05, 0, erase=True)
    for k in range(4):
        x = -1.3 + k * .55
        v.cbox(x, .15, 0, .5, .05, 1.2, METAL); v.cbox(x, .2, -.6, .5, .55, .05, METAL); v.cbox(x, .2, .6, .5, .55, .05, METAL); v.cbox(x - .22, .2, 0, .05, .55, 1.2, METAL); v.cbox(x, .75, 0, .5, .05, 1.2, METAL)
        v.cbox(x + .2, .75, -.65, .1, .3, .1, 0xc8372d); v.cbox(x, 0, -.5, .1, .1, .1, DARK); v.cbox(x, 0, .5, .1, .1, .1, DARK)
    v.cbox(-1.6, 0, -.8, .1, 1.8, .1, METAL); v.cbox(-1.6, 1.6, -.4, .1, .4, .9, 0x1d5fa8); v.text(-1.54, 1.65, -.65, 'CARTS', WHITE, axis='x', scale=.5)
    E(v, 'corral')
def sample():
    v = V(.1, 12); w, d = 2, 2
    v.cbox(0, 0, 0, 1.8, .9, 1.8, WHITE); v.cbox(0, .9, 0, 2, .1, 2, 0xc8372d)
    for k in range(-9, 10): v.box(k * .1, .2, .9, k * .1 + .1, .7, .92, (0xc8372d, WHITE)[k % 2])
    v.cbox(-.5, 1.0, -.4, .7, .4, .5, DARK); v.cbox(-.5, 1.05, -.13, .5, .25, .04, 0xff8a3a, kind='b')
    v.cbox(.5, 1.0, .3, .6, .05, .6, 0xf4f4f0); v.cbox(-.1, 1.0, -.9, .1, 1.2, .1, METAL); v.cbox(-.1, 2.1, -.9, .9, .4, .1, 0xffd23a); v.text(-.5, 2.15, -.84, 'FREE', 0xc8372d, scale=.5)
    E(v, 'sample')
def gumball():
    v = V(.1, 13); R = random.Random(13)
    for x in (-.25, .25):
        v.cyl(x, 0, 0, .1, .9, 0xc8372d); v.cbox(x, .9, 0, .4, .3, .4, 0xc8372d); v.sphere(x, 1.45, 0, .25, 0xcfe8ff, **GLASS)
        for k in range(20): v.voxel(x + R.uniform(-.15, .1), R.uniform(1.25, 1.55), R.uniform(-.15, .1), R.choice((0xff3a6a, 0x3ad8ff, 0xffd23a, 0x5aff7a)))
        v.cbox(x, 1.7, 0, .2, .1, .2, 0xc8372d); v.cbox(x, 1.0, .2, .1, .1, .05, METAL)
    E(v, 'gumball')
def wetfloor():
    v = V(.05, 14)
    for s in (-1, 1): v.box(-.2, 0, s * .05 - .03, .2, .65, s * .05 + .03, 0xffd23a)
    v.text(-.15, .38, .09, 'WET', 0x2a2a30, scale=.6); v.box(-.05, .15, .08, .05, .3, .1, 0x2a2a30)
    E(v, 'wetfloor')

# =============================== school ===============================
def board_cab(name, w):
    v = V(.1, int(w)); v.cbox(0, 0, 0, w, .9, .8, 0x8a6a3a, jit=.05); v.cbox(0, .9, 0, w + .06, .06, .86, 0xb08a58)
    for i in range(int(w)): x = -w / 2 + .5 + i; v.cbox(x, .15, .4, .8, .6, .04, 0x9a7a4a); v.cbox(x + .3, .4, .43, .06, .1, .04, 0xe8c55a)
    E(v, name)
def tdesk():
    v = V(.1, 15); w, d = 3.4, 1.3
    v.cbox(0, 0, 0, w, .9, d, 0x7a5a34, jit=.05); v.cbox(0, .9, 0, w + .1, .1, d + .1, 0xa8845a)
    v.cbox(-1.2, 1.0, -.2, .3, .1, .3, DARK); v.cbox(-1.2, 1.1, -.2, .05, .2, .05, METAL); v.sphere(-1.2, 1.45, -.2, .17, 0x3a8ad0); v.box(-1.3, 1.45, -.12, -1.1, 1.6, -.0, 0x5ab04a); v.box(-1.35, 1.35, -.3, -1.2, 1.45, -.2, 0x5ab04a)
    v.sphere(1.2, 1.1, .1, .1, 0xd83a2a); v.voxel(1.2, 1.2, .1, 0x5a4024); v.voxel(1.25, 1.22, .1, 0x5ab04a)
    for i, c in enumerate((0xc8372d, 0x3a6ad0, 0xffd23a)): v.cbox(.4, 1.0 + i * .06, -.2, .5, .06, .35, c)
    v.cbox(-.2, 1.0, .2, .6, .02, .4, WHITE)
    E(v, 'tdesk')
def combo_desk():
    v = V(.05, 16); Y = 0xd8c098; M = 0x6a7480; B_ = 0x3a6ad0
    v.cbox(0, .7, -.05, 1.0, .05, .6, Y, jit=.04)
    for x in (-.4, .4): v.cbox(x, 0, -.25, .05, .7, .05, M)
    v.cbox(0, .4, .5, .6, .05, .5, B_); v.cbox(0, .45, .72, .6, .5, .05, B_); v.cbox(.35, 0, .5, .05, .7, .05, M); v.cbox(.35, .7, .1, .05, .05, .8, M); v.cbox(-.25, 0, .5, .05, .4, .05, M)
    v.cbox(0, .55, -.05, .9, .1, .5, 0x4a5058)
    E(v, 'combo')
def janitor():
    v = V(.1, 17); v.cbox(0, 0, 0, 1.0, .1, 2.2, DARK); v.cbox(0, .1, -.4, .9, .9, 1.2, 0xffd23a); v.cbox(0, 1.0, -.4, .95, .1, 1.25, 0xd9a521)
    v.cbox(0, .1, .6, .9, .6, .8, 0x6a7480); v.cbox(0, .5, .6, .8, .2, .7, 0x5a9ae8)
    for x in (-.3, .3): v.cbox(x, .5, .6, .06, 1.5, .06, 0x9a7a4a)
    v.cbox(.3, .5, .6, .3, .1, .3, 0xf4f1e8); v.cbox(0, 1.1, -.4, .7, .1, .1, 0x3a3f48); v.cbox(-.5, .2, -.8, .05, .1, .1, DARK)
    for z in (-.9, .9):
        for x in (-.4, .4): v.cbox(x, 0, z, .12, .12, .12, 0x15151a)
    E(v, 'janitor')
def mopbucket():
    v = V(.1, 18); v.cbox(0, 0, 0, 1.2, .55, 1.0, 0xffd23a); v.cbox(0, .45, 0, 1.0, .1, .8, 0x6ab0e0); v.cbox(.3, .55, 0, .4, .3, .7, 0xd9a521)
    v.cbox(-.3, .4, 0, .06, 1.4, .06, 0x9a7a4a); v.cbox(-.3, 1.75, 0, .2, .1, .2, 0x3a3f48)
    for x in (-.5, .5):
        for z in (-.4, .4): v.cbox(x, 0, z, .1, .1, .1, 0x15151a)
    v.cbox(.2, 0, .6, .4, .7, .06, 0xffd23a); v.text(.05, .3, .63, '!', 0x2a2a30, scale=1)
    E(v, 'mopbucket')
def lockers(name, length, h=1.9):
    v = V(.1, 19); cols = (0x3a6ad0, 0x2a5ab0)
    v.cbox(0, 0, 0, 1.2, .1, length, DARK); v.cbox(0, .1, 0, 1.2, h - .1, length, 0x6a7480)
    n = int(length / .5)
    for i in range(n):
        z = -length / 2 + i * .5
        v.box(-.62, .15, z + .03, -.6, h - .05, z + .47, cols[i % 2]); v.box(-.64, .9, z + .35, -.62, 1.1, z + .42, 0xc0c8d0)
        for k in range(3): v.box(-.64, h - .35 - k * .08, z + .1, -.62, h - .32 - k * .08, z + .4, 0x1a2a4a)
    v.cbox(0, h, 0, 1.2, .1, length, 0x5a6470)
    E(v, name)
def musiccart():
    v = V(.1, 20); v.cbox(0, 0, 0, 1.2, .1, 3, DARK); v.cbox(0, .1, 0, 1.1, 1.0, 2.9, 0x8a6a45, jit=.05)
    for z in (-1.0, 0, 1.0): v.cbox(-.56, .5, z, .04, .4, .7, 0x6a4a2a)
    v.cbox(0, .55, 0, 1.0, .05, 2.8, 0xb08a58); v.cyl(.1, 1.1, -.9, .25, .25, 0xc8372d); v.cyl(.1, 1.35, -.9, .26, .03, 0xf4f1e8)
    for k in range(5): v.cbox(-.2 + k * .1, 1.1, .8, .06, .5 - k * .08, .06, (0xffd23a, 0x3ad8ff, 0xff7ab8, 0x5aff7a, 0xff8a3a)[k])
    E(v, 'musiccart')
def milkcooler():
    v = V(.1, 21); v.cbox(0, 0, 0, 2, .9, 1.2, 0xf4f4f0); v.cbox(0, .1, 0, 2.02, .2, 1.22, 0x3a6ad0); v.cbox(0, .9, 0, 2, .05, 1.2, 0xbfe4f8)
    v.text(-.6, .45, .6, 'MILK', 0x3a6ad0, scale=.8); E(v, 'milkcooler')
def cafetable():
    v = V(.1, 22); v.cbox(0, .7, 0, 4, .08, 1.0, 0xe8e0d0); v.cbox(0, .0, 0, .1, .7, .8, 0x6a7480)
    for s in (-1, 1):
        v.cbox(0, .4, s * .75, 4, .06, .3, 0x3a6ad0); v.cbox(-1.6, 0, s * .75, .06, .4, .06, 0x6a7480); v.cbox(1.6, 0, s * .75, .06, .4, .06, 0x6a7480)
    for x, c in ((-1.4, 0xffd23a), (-.2, 0xc8372d), (1.1, 0x5ab04a)): v.cbox(x, .78, -.2, .4, .04, .3, 0xd8d8d8); v.cbox(x, .82, -.2, .14, .14, .14, c)
    E(v, 'cafetable')

# =============================== park ===============================
def vtree(name='vtree', seed=30, r=1.4):
    v = V(.2, seed); R = random.Random(seed)
    v.cbox(0, 0, 0, .4, 1.8, .4, 0x6b4a2a, jit=.08)
    for (cx, cy, cz, rr) in ((0, 2.4, 0, r), (.6, 2.0, .3, r * .7), (-.6, 2.1, -.2, r * .75), (0, 3.1, 0, r * .7), (.1, 2.5, .7, r * .5)):
        for i in v.rng(cx - rr, cx + rr):
            for j in v.rng(cy - rr, cy + rr):
                for k in v.rng(cz - rr, cz + rr):
                    p = ((i + .5) * .2 - cx, (j + .5) * .2 - cy, (k + .5) * .2 - cz)
                    if p[0] ** 2 + p[1] ** 2 * 1.3 + p[2] ** 2 <= rr * rr and R.random() < .93:
                        v.voxel(i * .2, j * .2, k * .2, R.choice((0x3f8a3a, 0x4a9a42, 0x357a33, 0x52a84a)))
    E(v, name)
def tubeslide():
    v = V(.1, 31); RR = 0xc8372d; Y = 0xffd23a; B_ = 0x3a6ad0
    for x in (-.5, .5):
        for z in (-1.9, -1.1): v.cbox(x, 0, z, .12, 1.7, .12, B_)
    v.cbox(0, 1.5, -1.5, 1.2, .1, 1.0, Y); v.cbox(0, 1.6, -2.0, 1.2, .5, .08, RR); v.cbox(-.6, 1.6, -1.5, .08, .5, 1.0, RR); v.cbox(.6, 1.6, -1.5, .08, .5, 1.0, RR)
    for k in range(5): v.cbox(0, .3 * k, -2.05 - .05, 1.0, .06, .1, B_)
    for k in range(30):
        t = k / 29; y = 1.5 - 1.4 * t; z = -1.0 + 3.0 * t
        v.cbox(0, y, z, .9, .08, .14, Y); v.cbox(-.45, y, z, .08, .3, .14, Y); v.cbox(.45, y, z, .08, .3, .14, Y)
    v.cbox(0, 2.1, -1.5, .1, .7, .1, B_); v.cbox(0, 2.8, -1.5, 1.4, .1, 1.2, RR)
    E(v, 'tubeslide')
def dome():
    v = V(.1, 32); R_ = 1.6
    for a in range(16):
        for b in range(1, 9):
            th = a / 16 * 2 * math.pi; ph = b / 9 * math.pi / 2
            p = (R_ * math.cos(ph) * math.cos(th), R_ * math.sin(ph) * 1.2, R_ * math.cos(ph) * math.sin(th))
            v.cbox(p[0], p[1], p[2], .1, .1, .1, (0xd04a3a, 0x3a6ad0, 0xffd23a)[b % 3])
    for a in range(48):
        th = a / 48 * 2 * math.pi
        for b in range(30):
            ph = b / 30 * math.pi / 2
            if a % 6 == 0 or b % 8 == 0: v.cbox(R_ * math.cos(ph) * math.cos(th), R_ * math.sin(ph) * 1.2, R_ * math.cos(ph) * math.sin(th), .08, .08, .08, 0x9aa4ac)
    E(v, 'dome')
def drinkfountain():
    v = V(.1, 33); v.cbox(0, 0, 0, 2.4, .1, 1.6, 0x8a9098)
    for x in (-.7, .7): v.cbox(x, .1, 0, .3, .7, .3, 0x5a8a5a); v.cbox(x, .8, 0, .6, .15, .5, 0x6a9a6a); v.cbox(x, .95, 0, .4, .02, .3, 0x6ac4f0); v.cbox(x, .95, -.15, .05, .12, .05, METAL)
    v.cbox(0, .1, -.6, .2, 1.4, .2, 0x5a6470); v.cbox(0, 1.5, -.6, .9, .4, .1, 0x1d5fa8); v.text(-.35, 1.55, -.54, 'H2O', WHITE, scale=.5)
    E(v, 'drinkfountain')
def ballcart():
    v = V(.1, 34); v.cbox(0, 0, 0, 1.4, .1, 1.4, DARK)
    for x in (-.6, .6):
        for z in (-.6, .6): v.cbox(x, .1, z, .08, .6, .08, METAL)
    v.cbox(0, .3, 0, 1.4, .05, 1.4, METAL)
    for (x, z) in ((-.35, -.35), (.35, -.35), (-.35, .35), (.35, .35), (0, 0)): v.sphere(x, .55, z, .22, 0xe07a2a)
    E(v, 'ballcart')
def hoop():
    v = V(.1, 35); v.cbox(0, 0, 0, .2, 3.0, .2, 0x5a6470); v.cbox(0, 2.6, .35, .1, .1, .6, 0x5a6470); v.cbox(0, 2.6, .7, 1.8, 1.1, .1, WHITE); v.cbox(0, 2.75, .76, .6, .5, .02, 0xc8372d)
    v.cbox(0, 2.75, .76, .4, .3, .03, WHITE)
    for a in range(12): th = a / 12 * 2 * math.pi; v.cbox(.25 * math.cos(th), 2.95, 1.05 + .25 * math.sin(th), .06, .06, .06, 0xff6a2a)
    for a in range(8): th = a / 8 * 2 * math.pi; v.cbox(.2 * math.cos(th), 2.65, 1.05 + .2 * math.sin(th), .03, .3, .03, WHITE)
    E(v, 'hoop')
def quarterpipe():
    v = V(.1, 36); w, d = 3, 1.2
    for i in range(30):
        x = -1.5 + i * .1; t = abs(x) / 1.5; hgt = .6 * (t ** 2) if abs(x) > .3 else .0
        v.box(x, 0, -.6, x + .1, max(.1, hgt + .1), .6, 0x6a6a72)
    v.box(-.3, 0, -.6, .3, .6, .6, 0x5a5a62); v.box(-1.5, .6, -.6, -1.4, .7, .6, METAL); v.box(1.4, .6, -.6, 1.5, .7, .6, METAL)
    v.box(-.25, .6, -.4, .25, .61, .4, 0xc8372d); E(v, 'quarterpipe')
def picnic():
    v = V(.1, 37); v.cbox(0, .7, 0, 2.6, .08, .9, WOOD, jit=.06)
    for s in (-1, 1): v.cbox(0, .4, s * .7, 2.6, .06, .3, WOOD, jit=.06); v.cbox(s * 1.0, 0, 0, .1, .7, 1.6, 0x7a5a34)
    v.cbox(-.6, .78, 0, .5, .02, .4, 0xc8372d); v.cbox(.5, .78, .1, .3, .2, .3, 0x2f6aa0)
    E(v, 'picnic')
def feedsign():
    v = V(.1, 38); v.cbox(0, 0, 0, .2, 1.0, .2, 0x5a4024); v.cbox(0, .5, 0, 1.0, .5, .8, 0xc9a45a, jit=.04); v.cbox(0, 1.0, 0, 1.2, .06, 1.0, 0x8a5a2a)
    v.cbox(0, 1.06, 0, .6, .1, .3, 0x8a8f9a); v.cbox(.25, 1.12, 0, .15, .15, .15, 0x8a8f9a); v.voxel(.33, 1.16, 0, 0xff8a2a)
    E(v, 'feedsign')
def lemonade():
    v = V(.1, 39); v.cbox(0, 0, 0, 2, .9, 1.4, 0xf4e8c8, jit=.04); v.cbox(0, .9, 0, 2.1, .1, 1.5, 0xffd23a)
    v.cbox(-.95, 1.0, -.65, .1, 1.2, .1, WOOD); v.cbox(.95, 1.0, -.65, .1, 1.2, .1, WOOD); v.cbox(0, 2.1, -.65, 2.1, .5, .1, 0xffd23a); v.text(-.9, 2.15, -.59, 'LEMONADE', 0xc8372d, scale=.5)
    v.cyl(-.6, 1.0, 0, .2, .5, 0xffe86a, **dict(kind='l', op=.6)); v.text(-.4, .3, .7, '25C', 0xc8372d, scale=.8)
    E(v, 'lemonade')
def icetruck():
    v = V(.1, 40); W_ = 0xf8f8f4; P = 0xff8ab8
    v.cbox(0, .3, 0, 2, 1.9, 4, W_); v.cbox(0, .3, 1.5, 2, 1.2, 1.0, W_); v.cbox(0, .3, 0, 2.02, .3, 4.02, P)
    v.box(-1.01, 1.5, 1.2, 1.01, 2.2, 2.0, 0, erase=True); v.box(-1.0, 1.0, 1.4, 1.0, 1.4, 2.0, 0xcfe8ff, **GLASS)
    v.box(.99, .9, -1.4, 1.02, 1.8, .6, 0x2a2a30); v.box(1.0, .85, -1.5, 1.3, .9, .7, W_); v.text(1.02, 2.0, -1.6 + 3.0, 'ICE CREAM', P, axis='-x', scale=.6)
    for z in (-1.3, 1.3):
        for x in (-1, 1): v.cyl(x * .95, .3, z, .3, .15 * x if x > 0 else .15, 0x15151a, axis='x') if False else v.cbox(x * .95, 0, z, .2, .6, .6, 0x15151a)
    for i, (y, r) in enumerate(((2.3, .35), (2.55, .27), (2.75, .18))): v.cyl(0, y, -1.0, r, .25, 0xfffaf0)
    v.cyl(0, 2.0, -1.0, .18, .3, 0xd9a050); v.sphere(0, 3.0, -1.0, .1, 0xff3a4a)
    E(v, 'icetruck')
def bbq():
    v = V(.1, 41); v.cbox(0, 0, 0, .1, .7, .1, DARK); v.cbox(0, .7, 0, .8, .3, .6, 0x2a2a30); v.cbox(0, 1.0, 0, .8, .04, .6, METAL)
    for x in (-.25, 0, .25): v.cbox(x, 1.04, 0, .15, .06, .3, 0x8a3a20)
    E(v, 'bbq')
def trashcan():
    v = V(.1, 42); v.cyl(0, 0, 0, .3, .9, 0x2f6a3a); v.cyl(0, .9, 0, .32, .1, 0x255a30); v.cyl(0, .4, 0, .31, .1, 0x255a30); E(v, 'trashcan')
def hydrant():
    v = V(.05, 43); v.cyl(0, 0, 0, .16, .1, 0xc8372d); v.cyl(0, .1, 0, .12, .45, 0xc8372d); v.cyl(0, .55, 0, .14, .06, 0xa82a20); v.sphere(0, .65, 0, .12, 0xc8372d)
    v.cbox(0, .35, 0, .38, .1, .1, 0xc8372d); v.cbox(0, .72, 0, .06, .08, .06, 0xffd23a); E(v, 'hydrant')
def sandframe():
    v = V(.1, 44)
    for (cx, cz, w, d) in ((0, -2.6, 7.2, .2), (0, 2.6, 7.2, .2), (-3.6, 0, .2, 5.4), (3.6, 0, .2, 5.4)): v.cbox(cx, 0, cz, w, .3, d, WOOD)
    v.cbox(-2.6, .02, -1.6, .8, .3, .6, 0xe8d090); v.cbox(1.8, .02, 1.0, .6, .2, .5, 0xe8d090)
    E(v, 'sandframe')
def bucket2():
    v = V(.05, 45); v.cyl(0, 0, 0, .3, .4, 0xff5a3a); v.cyl(0, .35, 0, .26, .05, 0xd8b878); v.cbox(0, .4, 0, .6, .04, .04, 0xffd23a); E(v, 'bucket2')
def lamppost():
    v = V(.1, 46); v.cyl(0, 0, 0, .15, .2, 0x2a2a30); v.cbox(0, .2, 0, .1, 3.0, .1, 0x2a2a30); v.cbox(0, 3.2, 0, .4, .4, .4, 0xfff4c0, kind='b'); v.cbox(0, 3.6, 0, .5, .1, .5, 0x2a2a30); E(v, 'lamppost')

# =============================== arcade ===============================
def cabinet(name, col):
    v = V(.05, 50); D = 0x15151e
    v.cbox(0, 0, 0, 1.0, 1.8, .9, col); v.box(-.5, .9, .1, .5, 1.75, .46, 0, erase=True); v.box(-.45, 1.0, .2, .45, 1.65, .25, D)
    v.box(-.5, .85, .2, .5, .95, .6, D); v.box(-.5, 1.6, -.45, .5, 1.85, .5, col); v.box(-.45, 1.65, .45, .45, 1.8, .5, 0xffd23a, kind='b')
    v.cbox(-.25, .95, .4, .05, .12, .05, METAL); v.cbox(-.25, 1.07, .4, .1, .1, .1, 0xff3a3a)
    for i, c in enumerate((0xff3a3a, 0x3a8aff, 0xffd23a)): v.cbox(.05 + i * .13, .95, .42, .08, .04, .08, c, kind='b')
    v.box(-.2, .3, .45, .2, .5, .47, 0x30303c); v.box(-.1, .38, .47, -.05, .45, .48, 0xffd23a, kind='b'); v.box(.05, .38, .47, .1, .45, .48, 0xffd23a, kind='b')
    v.box(-.51, .1, -.4, -.49, 1.5, .4, (0xff4ad0, 0x3ad8ff, 0x5aff7a)[hash(name) % 3], kind='b'); v.box(.49, .1, -.4, .51, 1.5, .4, (0xff4ad0, 0x3ad8ff, 0x5aff7a)[hash(name) % 3], kind='b')
    E(v, name)
def pinball():
    v = V(.05, 51); D = 0x15151e
    for x in (-.35, .35):
        for z in (-.4, .4): v.cbox(x, 0, z, .06, .8, .06, DARK)
    for k in range(20): z = -.45 + k * .05; y = .8 + .15 * (.45 - z) / .9; v.box(-.4, y, z, .4, y + .15, z + .05, 0x8a2a8a)
    for k in range(20): z = -.45 + k * .05; y = .95 + .15 * (.45 - z) / .9; v.box(-.35, y, z, .35, y + .01, z + .05, 0x1a3a8a)
    for (x, z, c) in ((-.15, -.2, 0xff3a3a), (.15, -.25, 0xffd23a), (0, 0, 0x3ad8ff)): v.cbox(x, 1.05 - z * .15, z, .08, .06, .08, c, kind='b')
    v.cbox(0, .95, -.48, .8, .9, .1, 0x8a2a8a); v.cbox(0, 1.15, -.42, .7, .6, .02, 0xff4ad0, kind='b')
    E(v, 'pinball')
def clawpair():
    v = V(.1, 52); w, d = 5, 2.4
    for x in (-1.25, 1.25):
        v.cbox(x, 0, 0, 2.3, 1.0, 2.3, 0xff7ab8); v.cbox(x, .9, 0, 2.3, .1, 2.3, WHITE)
        for xx in (-1.1, 1.1):
            for zz in (-1.1, 1.1): v.cbox(x + xx, 1.0, zz, .1, 1.3, .1, 0xff4ad0)
        v.box(x - 1.1, 1.0, 1.1, x + 1.1, 2.3, 1.15, **dict(col=0xcfe8ff, **GLASS)); v.box(x - 1.15, 1.0, -1.1, x - 1.1, 2.3, 1.1, **dict(col=0xcfe8ff, **GLASS)); v.box(x + 1.1, 1.0, -1.1, x + 1.15, 2.3, 1.1, **dict(col=0xcfe8ff, **GLASS))
        v.cbox(x, 2.3, 0, 2.4, .4, 2.4, 0xff7ab8); v.box(x - 1.2, 2.4, 1.2, x + 1.2, 2.6, 1.22, 0xffd23a, kind='b')
        v.cbox(x + .3, 2.1, 0, .2, .2, .2, METAL); v.cbox(x + .3, 1.8, 0, .04, .3, .04, METAL)
        for a in (-1, 1): v.cbox(x + .3 + a * .1, 1.65, 0, .04, .15, .04, 0xc0c0c8)
        v.cbox(x - .6, .7, 1.2, .5, .2, .3, 0x30203a); v.cbox(x - .6, .9, 1.25, .05, .15, .05, METAL); v.cbox(x - .6, 1.05, 1.25, .1, .1, .1, 0xff3a3a)
    E(v, 'clawpair')
def vending():
    v = V(.1, 53); R = random.Random(53)
    for x in (-1.7, 0, 1.7):
        v.cbox(x, 0, 0, 1.5, 2.3, 1.6, (0xc8372d, 0x1d5fa8, 0x2f8a4a)[int(x + 2) % 3]); v.box(x - .65, 1.0, .75, x + .35, 2.1, .82, 0x10161e)
        for y in (1.05, 1.35, 1.65, 1.9):
            for k in range(5): v.box(x - .6 + k * .19, y, .7, x - .45 + k * .19, y + .2, .78, R.choice((0xffd23a, 0xc8372d, 0xff8a3a, 0x8a5ab0, 0x5ab0f0)))
        v.box(x - .65, 1.0, .82, x + .35, 2.1, .84, **dict(col=0xcfe8ff, **GLASS)); v.box(x + .4, 1.4, .8, x + .65, 1.9, .84, 0x30303a); v.box(x - .5, .3, .8, x + .3, .55, .84, 0x15151a)
        v.box(x - .65, 2.15, .8, x + .65, 2.28, .84, 0xffffff, kind='b')
    E(v, 'vending')
def capsules():
    v = V(.1, 54); R = random.Random(54)
    for z in (-1.8, -.6, .6, 1.8):
        v.cbox(0, 0, z, 1.2, .9, 1.0, 0xc8372d); v.cbox(0, .9, z, 1.1, .5, .9, **dict(col=0xcfe8ff, **GLASS)); v.cbox(0, 1.4, z, 1.2, .2, 1.0, 0xc8372d); v.cbox(0, 1.6, z, 1.0, .3, .9, 0xffd23a, kind='b')
        for k in range(12): v.cbox(R.uniform(-.4, .4), .95 + R.uniform(0, .25), z + R.uniform(-.35, .35), .15, .15, .15, R.choice((0xff3a6a, 0x3ad8ff, 0xffd23a, 0x5aff7a, 0x8a5ab0)))
        v.cbox(-.6, .5, z, .05, .15, .15, METAL)
    E(v, 'capsules')
def coinpusher():
    v = V(.1, 55); v.cbox(0, 0, 0, 3, 1.0, 3, 0xd9a521); v.cbox(0, 1.0, 0, 2.6, .05, 2.6, 0xffe88a)
    for k in range(40): a = k * 2.4; r = .2 + (k % 9) * .12; v.cbox(r * math.cos(a), 1.05 + (k % 3) * .04, r * math.sin(a), .12, .04, .12, (0xe8c55a, 0xf4d870)[k % 2])
    v.box(-1.5, 1.0, -1.5, 1.5, 2.0, -1.45, **dict(col=0xcfe8ff, **GLASS)); v.box(-1.5, 1.0, 1.45, 1.5, 2.0, 1.5, **dict(col=0xcfe8ff, **GLASS))
    v.box(-1.5, 1.0, -1.5, -1.45, 2.0, 1.5, **dict(col=0xcfe8ff, **GLASS)); v.box(1.45, 1.0, -1.5, 1.5, 2.0, 1.5, **dict(col=0xcfe8ff, **GLASS))
    v.cbox(0, 2.0, 0, 3.1, .3, 3.1, 0xd9a521); v.box(-1.55, 2.3, -1.55, 1.55, 2.4, 1.55, 0xff4ad0, kind='b'); E(v, 'coinpusher')
def molegame():
    v = V(.1, 56); v.cbox(0, 0, 0, 4, .9, 1.6, 0x3a8ad0); v.cbox(0, .9, 0, 4, .05, 1.6, 0xffd23a)
    for i, x in enumerate((-1.5, -.5, .5, 1.5)):
        for j, z in enumerate((-.4, .4)):
            v.cyl(x, .9, z, .2, .06, 0x2a1a14)
            if (i + j) % 2 == 0: v.cyl(x, .95, z, .15, .25, 0x8a5a32); v.voxel(x - .1, 1.1, z + .1, 0x15151a); v.voxel(x + .05, 1.1, z + .1, 0x15151a); v.voxel(x - .05, 1.0, z + .14, 0xff7a8a)
    v.cbox(0, .9, -.75, 4, 1.0, .1, 0xc8372d); v.text(-1.1, 1.3, -.7, 'WHACK!', 0xffd23a, scale=.8, kind='b')
    E(v, 'molegame')
def prizecounter():
    v = V(.1, 57); R = random.Random(57); v.cbox(0, 0, 0, 3, .9, 1.2, 0x8a5ab0); v.cbox(0, .9, 0, 3.05, .1, 1.25, 0xff7ab8)
    v.box(-1.45, .2, .55, 1.45, .8, .6, **dict(col=0xcfe8ff, **GLASS))
    for k in range(12): v.cbox(-1.3 + k * .23, .25, .3, .15, .2 + .1 * (k % 3), .15, R.choice((0xffd23a, 0xff3a6a, 0x3ad8ff, 0x5aff7a)))
    v.cbox(0, 1.0, -.55, 3, 1.3, .1, 0x2a1a3a); v.text(-1.2, 1.7, -.49, 'PRIZES', 0x5aff7a, scale=.8, kind='b')
    for k in range(5): v.cbox(-1.2 + k * .6, 1.1, -.48, .4, .4, .04, R.choice((0xff7ab8, 0xffd23a, 0x3ad8ff)))
    E(v, 'prizecounter')
def airhockey():
    v = V(.1, 58); v.cbox(0, 0, 0, 2.2, .7, 1.2, 0x1d5fa8)
    for x in (-1, 1):
        for z in (-.5, .5): v.cbox(x, 0, z, .1, .7, .1, DARK)
    v.cbox(0, .7, 0, 2.2, .08, 1.2, 0xf4f4f0); v.cbox(0, .78, 0, 2.2, .06, .1, 0x1d5fa8); v.cbox(0, .78, -.6, 2.2, .06, .1, 0x1d5fa8); v.cbox(-1.1, .78, 0, .1, .06, 1.2, 0x1d5fa8); v.cbox(1.1, .78, 0, .1, .06, 1.2, 0x1d5fa8)
    v.cbox(0, .78, .55, 2.2, .06, .1, 0x1d5fa8); v.cbox(0, .78, 0, .04, .01, 1.0, 0xc8372d); v.cbox(-.7, .78, 0, .12, .05, .12, 0xc8372d); v.cbox(.7, .78, .1, .12, .05, .12, 0x2f8a4a); v.cbox(.1, .78, -.1, .08, .02, .08, 0x15151a)
    v.box(-1.2, .5, -.62, 1.2, .55, .62, 0x3ad8ff, kind='b'); E(v, 'airhockey')
def skeeball():
    v = V(.1, 59)
    for x in (-.7, .7):
        v.cbox(x, 0, 0, 1.2, .5, 2.8, 0x6a2a4a)
        for k in range(18): z = 1.3 - k * .1; v.cbox(x, .5 + max(0, (.4 - z) * .3), z, 1.0, .05, .1, WOOD)
        v.cbox(x, .5, -1.2, 1.2, 1.4, .4, 0x6a2a4a); v.cyl(x, 1.0, -1.0, .35, .02, 0x15151a, axis='z'); v.cyl(x, 1.0, -.99, .2, .02, 0xffd23a, axis='z')
        v.cbox(x, 1.9, -1.2, 1.2, .5, .4, 0x15151a); v.cbox(x, 1.95, -1.0, 1.0, .35, .02, 0xff3a3a, kind='b'); v.cbox(x - .3, .55, 1.2, .25, .25, .25, 0xc8372d)
    E(v, 'skeeball')

ALL = [lambda: walls('super', 0xf2ecd8, 0x2f8a4a, 0xd8d0b8, super_deco), lambda: walls('school', 0xf0e6cc, 0x6a7a8a, 0xd8ccb0, school_deco),
       lambda: walls('park', 0x3f7a3a, 0x2f5a2a, 0x4f8a46, park_deco, 1.4, .9), lambda: walls('arcade', 0x2a1a3a, 0x15101f, 0x3ad8ff, arcade_deco),
       lambda: produce('produce_a', (0xd83a2a, 0x6ab04a, 0xff8a2a, 0xe8e0c0, 0x8ac04a)), lambda: produce('produce_b', (0x6ab04a, 0x3f8a3a, 0xc8d878, 0x6ab04a, 0x2f7a3a)), lambda: produce('produce_c', (0xffd23a, 0xff8a2a, 0xd83a2a, 0xffd23a, 0x8ac04a)),
       lambda: gondola('gondola_a', 8, '3'), lambda: gondola('gondola_b', 8, '4'), lambda: gondola('gondola_c', 8, '5'), dairy, seafood, coffin, wagon, checkout, corral, sample, gumball, wetfloor,
       lambda: board_cab('boardcab5', 5), lambda: board_cab('boardcab4', 4), tdesk, combo_desk, janitor, mopbucket, lambda: lockers('lockers5', 5), musiccart, milkcooler, cafetable,
       vtree, lambda: vtree('vtree2', 31, 1.2), tubeslide, dome, drinkfountain, ballcart, hoop, quarterpipe, picnic, feedsign, lemonade, icetruck, bbq, trashcan, hydrant, sandframe, bucket2, lamppost,
       lambda: cabinet('cab_a', 0x3a2a6a), lambda: cabinet('cab_b', 0x6a2a4a), lambda: cabinet('cab_c', 0x2a4a6a), pinball, clawpair, vending, capsules, coinpusher, molegame, prizecounter, airhockey, skeeball]
