# The 15 fighters. Each one is a set of rigid parts hung on the game's joints.
from bl_lib import *

DEF = dict(hipx=.115, thigh=.33, shin=.33, foot=.14, shx=.25, shy=1.27, uarm=.23, farm=.27, heady=1.4, hunch=.1, hs=1.0,
           tw=1.0, td=.86, belly=1.0, ra=.062, rl=.078, hc=(0, .25, .02), hr=(.29, .27, .27), handr=.07,
           skin=0xf1c9a5, top=0x8a8a94, sleeve=None, fore=None, hand=None, hips=None, leg=0x3a3f4a, shinc=None, shoe=0x2a2018, sole=None,
           headc=None, shoes='shoe', hands='mitt', legs=True, neck=True, torso=True, head=True)

def kit(name, **o):
    S = dict(DEF); S.update(o); begin(name)
    for k, d in (('sleeve', 'top'), ('fore', 'sleeve'), ('hand', 'skin'), ('shinc', 'leg'), ('headc', 'skin'), ('sole', 'shoe')):
        if S[k] is None: S[k] = S[d]
    S['hip'] = S['thigh'] + S['shin'] + S['foot']; hip = S['hip']; hy = S['heady']
    part('torso', (0, 0, 0), ['upper']); part('head', (0, hy, 0), ['head'])
    part('armU', (-S['shx'], S['shy'], 0), ['arm0', 'arm1']); part('armF', (-S['shx'], S['shy'] - S['uarm'], 0), ['elb0', 'elb1'])
    part('ext0', (-S['shx'], S['shy'] - S['uarm'], 0), ['elb0']); part('ext1', (S['shx'], S['shy'] - S['uarm'], 0), ['elb1'])
    part('legU', (-S['hipx'], hip, 0), ['leg0', 'leg1'] if S['legs'] else []); part('legF', (-S['hipx'], hip - S['thigh'], 0), ['knee0', 'knee1'] if S['legs'] else [])
    S['H'] = lambda p: (p[0], hy + p[1], p[2])
    S['E0'] = lambda p: (-S['shx'] + p[0], S['shy'] - S['uarm'] + p[1], p[2]); S['E1'] = lambda p: (S['shx'] + p[0], S['shy'] - S['uarm'] + p[1], p[2])
    S['handy'] = -(S['farm'] + .04)
    tw, td = S['tw'], S['td']; y0 = hip - .05; y1 = S['shy'] + .1
    def tr(y):   # torso radius (x) at height y
        t = (y - y0) / (y1 - y0); return (.2 + .06 * S['belly'] * math.sin(PI * min(1, t * 1.25)) - .09 * t * t) * tw
    S['tr'] = tr; S['tz'] = lambda y, a=0: tr(y) * td * math.cos(a)
    if S['torso']:
        ys = [y0 + (y1 - y0) * k / 8 for k in range(9)]
        add('torso', S['top'], lat([(y0 - .01, 0)] + [(y, tr(y)) for y in ys] + [(y1 + .03, .1 * tw), (y1 + .04, 0)], 16, sz=td))
        if S['hips'] is not None:
            add('torso', S['hips'], lat([(y0 - .05, 0), (y0 - .04, .1 * tw)] + [(y, tr(y) + .012) for y in ys[:3]] + [(ys[2] + .02, tr(ys[2]) - .02), (ys[2] + .025, 0)], 16, sz=td))
    if S['neck']: add('torso', S['skin'], cap((0, y1, 0), (0, hy + .04, 0), .07, .065, 8, 1))
    if S['head']:
        c = S['hc']; add('head', S['headc'], ell((0, hy + c[1], c[2]), S['hr'], 20, 12))
    def limb(s):
        if s > 0: return
        U = lambda p: (-S['shx'] + p[0], S['shy'] + p[1], p[2]); F = S['E0']; ra = S['ra']
        if S['uarm'] > 0:
            add('armU', S['sleeve'], ell(U((0, 0, 0)), ra * 1.25, 10, 6)); add('armU', S['sleeve'], cap(U((0, -.02, 0)), U((0, -S['uarm'] + .02, 0)), ra, ra * .92))
            add('armF', S['fore'], cap(F((0, 0, 0)), F((0, -S['farm'] + .01, 0)), ra * .9, ra * .98))
        if S['hands'] == 'mitt':
            add('armF', S['hand'], ell(F((0, S['handy'], 0)), S['handr'], 10, 6)); add('armF', S['hand'], ell(F((0, S['handy'] - .01, S['handr'] * .8)), (.025, .035, .025), 6, 4, RX(-.6)))
        if S['legs']:
            L = lambda p: (-S['hipx'] + p[0], hip + p[1], p[2]); K = lambda p: (-S['hipx'] + p[0], hip - S['thigh'] + p[1], p[2]); rl = S['rl']; sh = S['shin']
            add('legU', S['leg'], cap(L((0, -.02, 0)), L((0, -S['thigh'] + .02, 0)), rl, rl * .88))
            add('legF', S['shinc'], cap(K((0, 0, 0)), K((0, -sh, 0)), rl * .84, rl * .76))
            if S['shoes'] == 'shoe':
                add('legF', S['shoe'], ell(K((0, -sh - .07, .05)), (rl * 1.25, .068, .155), 12, 6)); add('legF', S['sole'], ell(K((0, -sh - .115, .05)), (rl * 1.32, .025, .163), 12, 4))
            elif S['shoes'] == 'paw':
                add('legF', S['shoe'], ell(K((0, -sh - .075, .05)), (rl * 1.3, .065, .16), 12, 6))
            elif S['shoes'] == 'heel':
                add('legF', S['shoe'], ell(K((0, -sh - .075, .06)), (rl * 1.05, .055, .15), 12, 6)); add('legF', S['shoe'], cap(K((0, -sh - .05, -.05)), K((0, -sh - .125, -.05)), .022, .016, 6, 1))
    limb(-1); return S

def onhead(S, x, y, k=1.0):
    c = S['hc']; r = S['hr']; dx = x / r[0]; dy = (y - c[1]) / r[1]; dz = math.sqrt(max(0.0, 1 - dx * dx - dy * dy))
    return (x * k, S['heady'] + c[1] + (y - c[1]) * k, c[2] + r[2] * dz * k), RY(math.atan2(dx / r[0], max(1e-3, dz) / r[2]))
def fe(S, col, x, y, r, tilt=0, k=1.0, pn='head', seg=8, rings=5):
    p, R = onhead(S, x, y, k); add(pn, col, ell(p, r, seg, rings, R @ RZ(tilt)))
def eyes(S, x=.1, y=.27, r=(.043, .06, .022), tilt=0, col=0x15151c, hl=True, k=1.0, hlc=0xffffff):
    for s, pn in ((-1, 'eyeL'), (1, 'eyeR')):
        p, R = onhead(S, s * x, y, k); R = R @ RZ(-s * tilt); part(pn, p, ['head'], (p[0], p[1] - S['heady'], p[2]))
        add(pn, col, ell(p, r, 12, 8, R))
        if hl:
            q = lambda v: tuple(Vector(p) + (R @ Vector(v)))
            add(pn, B(hlc), ell(q((-r[0] * .3, r[1] * .38, r[2] * .85)), (r[0] * .34, r[0] * .36, .008), 6, 4, R))
            add(pn, B(hlc), ell(q((r[0] * .32, -r[1] * .36, r[2] * .9)), (r[0] * .15, r[0] * .15, .005), 5, 3, R))
def hair(S, col, k=1.06, cut=lambda z: .3, pn='head', kz=None, seg=18, rings=10):
    c = S['hc']; r = S['hr']
    add(pn, col, ell((0, S['heady'] + c[1], c[2]), (r[0] * k, r[1] * k, r[2] * (kz or k)), seg, rings, None, lambda v: Vector((v.x, max(v.y, cut(v.z) - c[1]), v.z))))
def done(S, **extra):
    j = {k: S[k] for k in ('hipx', 'hip', 'thigh', 'heady', 'shx', 'shy', 'uarm', 'handy', 'hunch', 'hs', 'skin')}
    j['hand'] = round(S['handy'] + .03, 3); j.update(extra); return end(j)
def cheeks(S, col=0xf3a9a0, x=.19, y=.17):
    for s in (-1, 1): fe(S, col, s * x, y, (.04, .025, .01))
def mouth(S, col=0x8a3a34, y=.12, r=(.03, .012, .01), x=0): fe(S, col, x, y, r)
def chestz(S, y): return S['tz'](y)
H2 = lambda S: S['H']

# ============================== humans ==============================
def jiji():
    S = kit('jiji', skin=0xeebf98, top=0x8a7a5a, hips=0x6a5a48, leg=0x6a5a48, shoe=0x3a2a1a, hunch=.3); H = S['H']
    hair(S, 0xf2f2ee, 1.04, lambda z: .1 if z < .08 else .5)
    add('head', 0x6a5238, ell(H((0, .47, 0)), (.3, .09, .31), 16, 6)); add('head', 0x6a5238, ell(H((0, .44, .2)), (.2, .03, .16), 12, 4)); add('head', 0x5a4430, ell(H((0, .55, 0)), .03, 6, 4))
    eyes(S, .1, .27, (.03, .04, .018))
    for s in (-1, 1):
        fe(S, 0xf7f7f2, s * .1, .345, (.07, .024, .022), -s * .25); fe(S, 0xf7f7f2, s * .055, .14, (.065, .03, .03), s * .35)
        add('head', S['skin'], ell(H((s * .285, .25, .02)), (.03, .055, .04), 6, 4))
    fe(S, 0xe2ad88, 0, .2, (.04, .04, .045)); cheeks(S, 0xe9a48e, .2, .2)
    for y in (1.2, 1.08, .96): add('torso', 0x3a2a1a, ell((0, y, chestz(S, y) + .005), .022, 6, 4))
    add('torso', 0xf2efe6, tor((0, S['shy'] + .1, 0), .1, .035, seg=12))
    add('ext0', 0x6b4a2a, cap(S['E0']((0, S['handy'] + .1, .05)), S['E0']((0, S['handy'] - .72, .05)), .022, .02, 8, 1))
    add('ext0', 0x6b4a2a, tor(S['E0']((0, S['handy'] + .1, .0)), .05, .022, (1, 0, 0), 8, 6, arc=.5))
    done(S)
def baba():
    S = kit('baba', skin=0xf1c9a5, top=0x2f3f6a, hips=0x39455f, leg=0x39455f, shoe=0x2a2018, hunch=.24); H = S['H']
    hair(S, 0xdadde2, 1.04, lambda z: .2 if z < .1 else .43)
    hair(S, 0xf2efe6, 1.09, lambda z: .34 if z < .12 else .45); add('head', 0x2f5fb0, tor(H((0, .4, .02)), .262, .022, (0, 1, .12), 18, 6))
    add('head', 0xdadde2, ell(H((0, .3, -.3)), (.1, .1, .09), 8, 6)); add('head', 0xf2efe6, ell(H((0, .58, -.02)), (.07, .05, .07), 8, 4))
    eyes(S, .105, .27, (.03, .036, .018))
    for s in (-1, 1):
        p, R = onhead(S, s * .105, .27, 1.04); add('head', 0x3a2a2a, tor(p, .062, .01, tuple(R @ Vector((0, 0, 1))), 14, 5))
        add('head', S['skin'], ell(H((s * .285, .25, .02)), (.03, .055, .04), 6, 4))
    add('head', 0x3a2a2a, cap(H((-.045, .275, .29)), H((.045, .275, .29)), .009, .009, 5, 1))
    cheeks(S, 0xf09a90, .2, .18); fe(S, 0xe6b592, 0, .21, (.03, .03, .03)); mouth(S, 0xb04a44, .13, (.035, .012, .01))
    for x, y in ((-.1, 1.2), (.09, 1.25), (0, 1.08), (-.12, .98), (.13, 1.02), (.02, .9)):
        a = math.asin(max(-1, min(1, x / S['tr'](y)))); add('torso', 0xf2efe6, ell((x, y, S['tz'](y, a) + .003), .018, 6, 4))
    add('torso', 0xc8372d, tor((0, .86, 0), S['tr'](.86) + .012, .03, sz=S['td'], seg=18))
    add('torso', 0x2f8a4a, ell((0, 1.14, -.3), (.22, .18, .16), 14, 8)); add('torso', 0xe8f0d8, tor((0, 1.14, -.455), .07, .012, (0, 0, 1), 12, 5)); add('torso', 0xe8f0d8, ell((0, 1.14, -.46), .02, 6, 4))
    add('torso', 0x2f8a4a, tor((0, 1.2, -.02), .25, .035, (.3, 1, .15), 18, 6, sz=.95))
    add('torso', 0x2f8a4a, ell((-.05, 1.33, .19), (.05, .035, .04), 6, 4, RZ(.5))); add('torso', 0x2f8a4a, ell((.05, 1.31, .19), (.05, .035, .04), 6, 4, RZ(-.5)))
    done(S)
def salary():
    S = kit('salary', skin=0xf1c9a5, top=0x24304a, hips=0x3a3f4a, leg=0x3a3f4a, shoe=0x151515, hunch=.06); H = S['H']
    hair(S, 0x1a1612, 1.05, lambda z: .26 if z < .1 else .42); add('head', 0x1a1612, ell(H((.09, .49, .17)), (.16, .06, .1), 8, 5, RZ(-.25)))
    eyes(S, .1, .27, (.03, .04, .018))
    for s in (-1, 1):
        p, R = onhead(S, s * .1, .27, 1.04); add('head', 0x22252e, tor(p, .06, .01, tuple(R @ Vector((0, 0, 1))), 4, 4, sx=1.25))
        add('head', S['skin'], ell(H((s * .285, .25, .02)), (.03, .055, .04), 6, 4)); fe(S, 0x1a1612, s * .1, .36, (.05, .012, .012), -s * .1)
    add('head', 0x22252e, cap(H((-.035, .275, .29)), H((.035, .275, .29)), .009, .009, 5, 1))
    fe(S, 0xe6b592, 0, .21, (.028, .03, .03)); mouth(S, 0x9a4a40, .13, (.03, .01, .01))
    z = lambda y: chestz(S, y)
    add('torso', 0xf4f4f0, ell((0, 1.2, z(1.2) - .03), (.1, .16, .05), 8, 6)); add('torso', 0xc8372d, ell((0, 1.14, z(1.14) + .012), (.032, .14, .02), 6, 5)); add('torso', 0xc8372d, ell((0, 1.3, z(1.3) + .005), .035, 6, 4))
    for s in (-1, 1): add('torso', 0x1c2740, ell((s * .1, 1.2, z(1.2) - .01), (.05, .17, .04), 6, 5, RZ(s * .28)))
    e = S['E0']; hy = S['handy']
    add('ext0', 0x5a3a1c, box(e((0, hy - .2, .02)), (.1, .26, .36)), bevel=.025); add('ext0', 0xe8c55a, box(e((-.055, hy - .12, .02)), (.02, .05, .09)), bevel=.006)
    add('ext0', 0x3a2414, tor(e((0, hy - .07, .02)), .06, .014, (1, 0, 0), 10, 5, arc=.5))
    done(S)
def career():
    S = kit('career', skin=0xf5d3b3, top=0x8a8a94, hips=0x2a2a34, leg=0xe2b898, shoe=0xc02a2a, shoes='heel', hunch=.04, tw=.9, rl=.066, ra=.055); H = S['H']
    hair(S, 0x4a2c1a, 1.07, lambda z: .08 if z < .08 else .4, kz=1.08); add('head', 0x4a2c1a, ell(H((-.06, .47, .2)), (.19, .07, .1), 8, 5, RZ(.3)))
    for s in (-1, 1):
        add('head', 0x4a2c1a, ell(H((s * .25, .16, -.02)), (.09, .16, .15), 8, 6)); add('head', 0xe8c55a, ell(H((s * .3, .12, .06)), .025, 6, 4))
        fe(S, 0x3a2418, s * .1, .355, (.045, .01, .01), -s * .15)
    eyes(S, .1, .27, (.034, .048, .018), .08); cheeks(S, 0xf5a0a0, .19, .18); fe(S, 0xe8bc9c, 0, .21, (.022, .026, .026)); mouth(S, 0xd0303a, .13, (.03, .014, .01))
    z = lambda y: chestz(S, y); hip = S['hip']
    add('torso', 0xffffff, ell((0, 1.22, z(1.22) - .03), (.08, .14, .05), 8, 6)); add('torso', 0xe8c55a, tor((0, 1.33, .03), .1, .009, (0, 1, .5), 14, 4))
    for s in (-1, 1): add('torso', 0x7c7c88, ell((s * .09, 1.2, z(1.2) - .012), (.045, .17, .04), 6, 5, RZ(s * .3)))
    add('torso', 0x2a2a34, lat([(hip - .32, 0), (hip - .32, .3), (hip - .1, .25), (hip + .06, .215), (hip + .07, 0)], 16, sz=.85))
    done(S)
def kid():
    S = kit('kid', skin=0xf8d0b0, top=0x5ab0f0, hips=0x2a4a8a, leg=0xf8d0b0, shoe=0xffffff, sole=0xdddddd, hunch=0, hs=1.2, hr=(.33, .3, .31), hc=(0, .28, .02), heady=1.36, shy=1.22, thigh=.3, shin=.3); H = S['H']
    hair(S, 0x3a2a1a, 1.04, lambda z: .22 if z < .1 else .42)
    hair(S, 0xffd23a, 1.1, lambda z: .4); add('head', 0xffd23a, lat([(0, 0), (0, .47), (.03, .46), (.035, 0)], 20, frame(H((0, .385, .01)), (0, 1, .06)))); add('head', 0xff7a3a, ell(H((0, .62, .02)), .035, 6, 4))
    eyes(S, .12, .28, (.045, .062, .02)); cheeks(S, 0xf79a94, .22, .17); mouth(S, 0xb0403a, .12, (.035, .02, .01)); fe(S, 0xeebf9c, 0, .2, (.02, .02, .022))
    z = lambda y: chestz(S, y); hip = S['hip']
    add('torso', 0x5ab0f0, lat([(hip - .14, 0), (hip - .14, .31), (hip + .1, .25), (hip + .11, 0)], 16, sz=.86)); add('torso', 0xffffff, tor((0, S['shy'] + .1, 0), .11, .035, seg=12))
    add('torso', 0xff7ab8, ell((.1, 1.12, z(1.12) + .01), (.045, .045, .014), 8, 4)); add('torso', 0xffffff, ell((.1, 1.12, z(1.12) + .02), (.02, .02, .008), 6, 3))
    add('torso', 0xffd23a, ell((-.26, .86, .02), (.07, .09, .1), 8, 5)); add('torso', 0xc8372d, tor((0, 1.08, 0), .255, .014, (.75, 1, 0), 18, 4, sz=.86))
    done(S)
def zombie():
    Z = 0x8aa870
    S = kit('zombie', skin=Z, top=0x7a7868, sleeve=Z, hips=0x3a4a6a, leg=0x3a4a6a, shoe=0x3a3530, hunch=.28); H = S['H']
    for p, r in (((-.1, .5, .05), (.1, .05, .09)), ((.09, .51, -.03), (.09, .05, .1)), ((0, .47, -.17), (.12, .06, .09)), ((.17, .43, .1), (.07, .04, .06)), ((-.18, .42, -.1), (.07, .05, .08))):
        add('head', 0x2a2a1a, ell(H(p), r, 8, 5))
    eyes(S, .1, .28, (.06, .06, .022), 0, 0xf4f0d8, False)
    for s, pn, pr in ((-1, 'eyeL', .028), (1, 'eyeR', .014)):
        p, R = onhead(S, s * .1, .28, 1.07); add(pn, 0x2a1a10, ell((p[0] + s * .01, p[1] - .005, p[2] + .004), (pr, pr, .008), 6, 4, R)); fe(S, 0x5a6a50, s * .1, .27, (.085, .08, .012))
    fe(S, 0x3a2a2a, 0, .12, (.06, .035, .012)); fe(S, 0xf4f0d8, -.025, .135, (.014, .016, .012), 0, 1.03); fe(S, 0xf4f0d8, .03, .105, (.012, .014, .012), 0, 1.03)
    for dx in (-.03, 0, .03): fe(S, 0x3a4a30, .12 + dx, .41, (.006, .028, .008), .2, 1.01)
    fe(S, 0x3a4a30, .12, .41, (.06, .006, .008), .2, 1.01); fe(S, 0x6f8a5a, -.17, .16, (.05, .035, .01))
    z = lambda y: chestz(S, y)
    add('torso', 0x4a4a3a, ell((.09, 1.02, z(1.02) - .005), (.06, .07, .02), 6, 4)); add('torso', 0x6a2a20, ell((-.1, 1.18, z(1.18) - .005), (.05, .045, .02), 6, 4)); add('torso', 0x5f5d50, ell((-.02, .9, z(.9) - .005), (.08, .035, .02), 6, 4, RZ(.4)))
    add('ext1', 0xf4f0e0, cap(S['E1']((0, -.1, .0)), S['E1']((.09, -.14, .03)), .022, .022, 6, 1)); add('ext1', 0xf4f0e0, ell(S['E1']((.1, -.145, .03)), (.03, .03, .03), 6, 4))
    add('ext1', 0x6a2a20, ell(S['E1']((.03, -.115, .01)), (.04, .035, .04), 6, 4))
    done(S)
def sumo():
    Sk = 0xf0c09a; P = 0x3a2a6a
    S = kit('sumo', skin=Sk, top=Sk, hips=P, leg=Sk, shoe=Sk, shoes='paw', hunch=.08, tw=1.4, belly=1.5, rl=.115, ra=.085, shx=.36, hipx=.17, handr=.085, hr=(.3, .27, .28)); H = S['H']
    hair(S, 0x15151a, 1.04, lambda z: .25 if z < .12 else .44); add('head', 0x15151a, cap(H((0, .55, -.08)), H((0, .58, .1)), .04, .05, 8, 2)); add('head', 0x15151a, ell(H((0, .53, -.12)), (.07, .05, .07), 8, 4))
    eyes(S, .1, .29, (.028, .034, .016))
    for s in (-1, 1): fe(S, 0x15151a, s * .1, .36, (.055, .016, .012), -s * .3); add('head', Sk, ell(H((s * .295, .25, .02)), (.03, .055, .04), 6, 4))
    cheeks(S, 0xf0a090, .2, .19); fe(S, 0xe2ad88, 0, .22, (.035, .03, .03)); mouth(S, 0x8a3a34, .135, (.03, .01, .01))
    hip = S['hip']
    add('torso', Sk, ell((0, 1.02, .07), (.37, .3, .33), 16, 10)); add('torso', P, tor((0, hip + .06, .02), .37, .07, seg=20, tseg=8, sz=.86))
    for s in (-1, 1): add('torso', 0xe0a888, ell((s * .16, 1.21, .3), .022, 6, 4))
    add('torso', P, box((0, hip - .08, .33), (.3, .26, .04)), bevel=.015)
    for k in range(-2, 3): add('torso', 0xe8c55a, cap((k * .06, hip - .12, .36), (k * .06, hip - .3, .37), .012, .012, 5, 1))
    add('torso', P, ell((0, hip + .08, -.3), (.1, .08, .06), 8, 5))
    done(S)

# ============================== animals & others ==============================
def monkey():
    F = 0x8a5a32; T = 0xe0b080; D = 0x5a3a20
    S = kit('monkey', skin=F, top=F, leg=F, hand=D, shoe=D, shoes='paw', hunch=.42, tw=.9, uarm=.27, farm=.35, hr=(.27, .25, .25)); H = S['H']
    add('head', T, ell(H((-.085, .3, .15)), (.11, .1, .1), 10, 6)); add('head', T, ell(H((.085, .3, .15)), (.11, .1, .1), 10, 6)); add('head', T, ell(H((0, .16, .17)), (.15, .11, .13), 12, 6))
    for s in (-1, 1):
        add('head', F, ell(H((s * .29, .27, 0)), (.05, .1, .1), 8, 6)); add('head', T, ell(H((s * .305, .27, .01)), (.04, .075, .075), 8, 5))
        add('head', 0x3a2414, ell(H((s * .025, .2, .295)), .01, 5, 3))
    S['hc'] = (0, .27, .1); S['hr'] = (.2, .2, .17)
    eyes(S, .085, .31, (.034, .046, .018)); fe(S, 0x6a3a2a, 0, .12, (.05, .012, .012), 0, 1.04); add('head', F, ell(H((0, .53, .02)), (.05, .06, .05), 6, 4))
    add('torso', T, ell((0, 1.05, chestz(S, 1.05) - .05), (.15, .2, .08), 10, 6))
    pts = [(0, .86, -.17), (0, .8, -.34), (0, .86, -.5), (0, 1.02, -.58), (0, 1.17, -.54), (0, 1.24, -.43), (0, 1.2, -.34)]; chain('torso', F, pts, .034, .026)
    done(S)
def dog():
    F = 0xd98a3a; W = 0xf4ece0
    S = kit('dog', skin=F, top=F, leg=F, hand=W, shoe=W, shoes='paw', hunch=.18, hr=(.27, .25, .25)); H = S['H']
    add('head', W, ell(H((0, .17, .21)), (.14, .11, .16), 12, 6)); add('head', 0x1a1a1a, ell(H((0, .22, .365)), (.04, .03, .03), 8, 5)); add('head', 0xf07a8a, ell(H((0, .085, .3)), (.035, .02, .05), 6, 4))
    add('head', 0x3a2414, cap(H((0, .19, .368)), H((0, .14, .355)), .007, .007, 4, 1))
    for s in (-1, 1):
        add('head', F, cone(H((s * .15, .43, 0)), H((s * .2, .66, .02)), .085, 6)); add('head', 0xf0b890, cone(H((s * .155, .45, .03)), H((s * .195, .6, .04)), .045, 5))
        add('head', W, ell(H((s * .15, .15, .13)), (.09, .08, .1), 8, 5)); fe(S, W, s * .1, .37, (.03, .02, .012))
    eyes(S, .11, .3, (.034, .046, .018))
    add('torso', W, ell((0, 1.08, chestz(S, 1.08) - .05), (.15, .22, .08), 10, 6))
    add('torso', 0xc8372d, tor((0, S['shy'] + .12, 0), .1, .028, seg=14)); add('torso', 0xe8c55a, ell((0, S['shy'] + .08, .11), .032, 8, 5))
    add('torso', F, tor((0, .98, -.28), .09, .04, (1, 0, 0), 12, 6, arc=.8)); add('torso', W, ell((0, 1.07, -.3), .042, 6, 4))
    done(S)
def panda():
    W = 0xf4f4ee; K = 0x1a1a1e
    S = kit('panda', skin=W, top=W, sleeve=K, leg=K, hand=K, shoe=K, shoes='paw', hunch=.15, tw=1.25, belly=1.3, rl=.105, ra=.08, shx=.31, hipx=.14, handr=.08, hr=(.31, .27, .28)); H = S['H']
    for s in (-1, 1):
        add('head', K, ell(H((s * .22, .5, 0)), (.095, .095, .06), 10, 6)); fe(S, K, s * .115, .275, (.075, .09, .012), s * .5)
    eyes(S, .11, .285, (.03, .036, .016), 0, 0x000000, True, 1.045)
    add('head', W, ell(H((0, .17, .25)), (.1, .07, .08), 10, 5)); add('head', K, ell(H((0, .2, .325)), (.035, .024, .02), 8, 4)); add('head', K, cap(H((0, .185, .328)), H((0, .15, .322)), .006, .006, 4, 1))
    cheeks(S, 0xf7c0c0, .21, .16)
    y = S['shy'] + .02; add('torso', K, tor((0, y, 0), S['tr'](y) - .02, .1, seg=18, tseg=8, sz=.86)); add('torso', W, ell((0, .82, -.3), .075, 8, 5))
    done(S)
def dino():
    G = 0x5aa04a; D = 0x3a7a32; Bl = 0xc8d890
    S = kit('dino', skin=G, top=G, leg=G, hand=D, shoe=D, shoes='paw', hunch=.38, hs=1.25, tw=1.15, rl=.125, ra=.06, uarm=.13, farm=.15, hipx=.15, handr=.055, hr=(.27, .25, .27), hc=(0, .27, 0)); H = S['H']
    add('head', G, ell(H((0, .24, .3)), (.19, .12, .25), 12, 6)); add('head', G, ell(H((0, .11, .27)), (.16, .055, .21), 12, 5)); add('head', 0xb03a4a, ell(H((0, .15, .29)), (.165, .03, .215), 10, 4))
    for s in (-1, 1):
        for k in range(4): add('head', 0xffffff, cone(H((s * (.15 - k * .012), .175, .2 + k * .075)), H((s * (.15 - k * .012), .115, .2 + k * .075)), .02, 4))
        add('head', D, ell(H((s * .07, .31, .5)), .018, 5, 3)); add('head', D, ell(H((s * .15, .43, .15)), (.07, .04, .08), 8, 4, RZ(-s * .3)))
    S['hc'] = (0, .3, .08); S['hr'] = (.23, .2, .2); eyes(S, .15, .36, (.034, .042, .018), .1, 0x1a1a10, True, 1.02, 0xffe27a)
    add('torso', Bl, ell((0, 1.02, chestz(S, 1.02) - .06), (.19, .25, .1), 10, 6))
    for k in range(5): y = 1.36 - k * .15; add('torso', 0x2a6a2a, cone((0, y, -S['tz'](y) + .03), (0, y + .06, -S['tz'](y) - .13), .06, 4))
    chain('torso', G, [(0, .84, -.15), (0, .72, -.42), (0, .56, -.68), (0, .42, -.92), (0, .34, -1.14), (0, .32, -1.32)], .15, .03, 10)
    for dx in (-.03, 0, .03): add('armF', 0xffffff, cone(S['E0']((dx, S['handy'] - .03, .03)), S['E0']((dx, S['handy'] - .09, .05)), .014, 4))
    K = lambda p: (-S['hipx'] + p[0], S['hip'] - S['thigh'] + p[1], p[2])
    for dx in (-.06, 0, .06): add('legF', 0xffffff, cone(K((dx, -S['shin'] - .09, .19)), K((dx, -S['shin'] - .11, .26)), .022, 4))
    done(S)
def penguin():
    K = 0x1a1f2a; W = 0xf4f4f0; O = 0xffa020
    S = kit('penguin', skin=K, top=K, leg=O, shoe=O, shoes=None, hands=None, hunch=.05, tw=1.3, belly=1.5, thigh=.1, shin=.1, foot=.07, hipx=.12, shx=.3, shy=.98, uarm=0, farm=.3, heady=1.12, neck=False, rl=.05, hr=(.28, .25, .26)); H = S['H']
    add('torso', W, ell((0, .68, .1), (.25, .34, .2), 14, 8))
    for s in (-1, 1): add('head', W, ell(H((s * .1, .28, .17)), (.125, .14, .15), 10, 6))
    add('head', W, ell(H((0, .17, .18)), (.16, .1, .14), 10, 5)); add('head', O, cone(H((0, .2, .28)), H((0, .17, .47)), .065, 8)); 
    for s in (-1, 1): add('head', 0xf7a8a8, ell(H((s * .17, .17, .27)), (.035, .022, .02), 6, 4))
    S['hc'] = (0, .28, .17); S['hr'] = (.21, .14, .15); eyes(S, .1, .3, (.036, .048, .018))
    U = lambda p: (-S['shx'] + p[0], S['shy'] + p[1], p[2])
    add('armU', K, ell(U((0, 0, 0)), .07, 8, 5)); add('armF', K, ell(S['E0']((-.03, -.17, 0)), (.04, .21, .11), 10, 6, RZ(-.25)))
    Kn = lambda p: (-S['hipx'] + p[0], S['hip'] - S['thigh'] + p[1], p[2])
    add('legF', O, ell(Kn((0, -.13, .08)), (.1, .035, .16), 10, 5)); 
    for dx in (-.07, 0, .07): add('legF', O, ell(Kn((dx, -.14, .2)), (.035, .025, .06), 6, 4))
    done(S)
def robot():
    Mt = 0xa8b0bc; D = 0x5a6270
    S = kit('robot', skin=Mt, top=Mt, sleeve=D, hand=Mt, hips=None, leg=D, shoe=D, shoes=None, hunch=0, tw=1.05, torso=False, head=False, neck=False, ra=.055, rl=.07, handr=.075); H = S['H']
    add('head', Mt, box(H((0, .26, 0)), (.56, .46, .46)), bevel=.07); add('head', 0x232a3a, box(H((0, .27, .215)), (.42, .2, .06)), bevel=.03)
    add('head', D, cap(H((0, .49, 0)), H((0, .64, 0)), .014, .012, 6, 1)); add('head', B(0xff3a3a), ell(H((0, .67, 0)), .04, 8, 5))
    for s in (-1, 1): add('head', D, lat([(0, 0), (0, .07), (.05, .06), (.05, 0)], 10, frame(H((s * .27, .26, 0)), (s, 0, 0))))
    for k in range(-2, 3): add('head', D, box(H((k * .05, .1, .228)), (.022, .06, .02)))
    for s, pn in ((-1, 'eyeL'), (1, 'eyeR')):
        p = H((s * .1, .275, .25)); part(pn, p, ['head'], (p[0], p[1] - S['heady'], p[2])); add(pn, B(0x7affea), ell(p, (.05, .055, .014), 10, 5))
    add('torso', Mt, box((0, 1.12, 0), (.54, .5, .38)), bevel=.07); add('torso', D, lat([(.72, 0), (.72, .17), (.9, .19), (.9, 0)], 12)); add('torso', D, cap((0, 1.36, 0), (0, 1.42, 0), .08, .08, 8, 1))
    add('torso', 0x2a3a5a, box((0, 1.15, .19), (.3, .2, .03)), bevel=.012)
    for i, c in enumerate((0xff4a3a, 0xffd23a, 0x5aff7a)): add('torso', B(c), ell((-.08 + i * .08, 1.18, .208), (.026, .026, .008), 8, 3))
    add('torso', B(0x7affea), box((0, 1.1, .207), (.2, .025, .008)))
    for s in (-1, 1): add('torso', D, ell((s * .16, 1.24, -.2), (.05, .05, .03), 8, 4))
    for pn, f in (('armF', S['E0']),): add(pn, Mt, ell(f((0, 0, 0)), .068, 8, 5)); add(pn, D, tor(f((0, S['handy'] + .075, 0)), .06, .016, seg=10, tseg=5))
    K = lambda p: (-S['hipx'] + p[0], S['hip'] - S['thigh'] + p[1], p[2])
    add('legF', Mt, ell(K((0, 0, 0)), .075, 8, 5)); add('legF', Mt, box(K((0, -S['shin'] - .075, .045)), (.19, .13, .3)), bevel=.04)
    done(S)
def ghost():
    W = 0xf2f4ff
    S = kit('ghost', skin=W, top=W, legs=False, torso=False, neck=False, hunch=.1, tw=1.1, uarm=.16, farm=.2, shy=1.2, shx=.36, ra=.075, handr=.085, hr=(.3, .28, .28)); H = S['H']
    def hem(v):
        if v.y < .3:
            a = math.atan2(v.z, v.x); return Vector((v.x, v.y + .07 * math.sin(a * 6), v.z))
        return v
    add('torso', W, lat([(1.5, 0), (1.5, .12), (1.38, .26), (1.15, .33), (.8, .39), (.45, .46), (.2, .52), (.14, .47), (.14, 0)], 24, None, 1, .9, hem))
    add('head', W, cone(H((0, .5, 0)), H((.06, .7, -.04)), .07, 8)); add('head', W, ell(H((.07, .7, -.05)), .03, 6, 4))
    eyes(S, .11, .3, (.06, .085, .02), .12); fe(S, 0x2a2a40, 0, .13, (.06, .05, .012)); fe(S, 0xf07a9a, 0, .1, (.03, .03, .014), 0, 1.02); cheeks(S, 0xc8cdf7, .2, .17)
    done(S)

def alien():
    begin('alien')
    SUIT = M(0xeef1f6); SLATE = M(0x4d5a73); ORANGE = M(0xff8a4a); SKIN = M(0xa9bccb); METAL = M(0xb9c2d0); GLOW = B(0x7affea); EYE = M(0x0c0e18)
    WHITE = B(0xffffff); CHEEK = M(0xc9b0d8); MOUTH = M(0x5b4a70); GLASS = M(0xcfeaff, 'l', .2); SHINE = B(0xffffff, .7); RED = B(0xff5a4a)
    def off(vf, d): return [(v[0] + d[0], v[1] + d[1], v[2] + d[2]) for v in vf[0]], vf[1]
    # ---------------- skeleton (rest pose) ----------------
    THIGH = .28; FOOT = .484; HIP = THIGH + FOOT; HIPX = .105
    HEADY = 1.33; SHX = .215; SHY = 1.2; UARM = .2; HANDY = -.40; GZ = .065
    PIV0 = {'torso': (0, 0, 0), 'head': (0, HEADY, 0), 'helmet': (0, HEADY, 0), 'beacon': (0, HEADY, 0),
           'legU': (-HIPX, HIP, 0), 'legF': (-HIPX, HIP - THIGH, 0), 'armU': (-SHX, SHY, 0), 'armF': (-SHX, SHY - UARM, 0),
           'gun': (SHX, SHY - UARM, 0)}
    EYE_C = {'eyeL': (-.088, .195, .198), 'eyeR': (.088, .195, .198)}


    # ---------------- torso ----------------
    add('torso', SUIT, lat([(.74, 0), (.75, .15), (.79, .215), (.87, .238), (.98, .225), (1.1, .19), (1.2, .155), (1.27, .125), (1.3, .08), (1.31, 0)], 20, sz=.9))
    add('torso', SLATE, lat([(.63, 0), (.645, .1), (.69, .185), (.75, .225), (.81, .236), (.83, .2), (.84, 0)], 20, sz=.9))
    add('torso', SLATE, tor((0, .82, 0), .236, .028, sz=.9, seg=24))
    add('torso', ORANGE, tor((0, .862, 0), .238, .011, sz=.9, seg=24))
    add('torso', ORANGE, box((0, .82, .222), (.085, .06, .035)), bevel=.012)
    add('torso', GLOW, ell((0, .82, .243), (.018, .018, .008), 10, 6))
    add('torso', METAL, tor((0, 1.3, 0), .15, .043, seg=24, tseg=8))
    add('torso', GLOW, tor((0, 1.338, 0), .168, .011, seg=24))
    # chest emblem
    add('torso', SLATE, lat([(0, 0), (0, .062), (.02, .066), (.03, .05), (.032, 0)], 16, frame((0, 1.07, .158), (0, .12, 1))))
    add('torso', GLOW, tor((0, 1.074, .192), .036, .011, (0, .12, 1), 16, 6))
    add('torso', WHITE, ell((0, 1.074, .193), (.014, .014, .008), 8, 5))
    # oxygen tank + backplate
    add('torso', SLATE, box((0, 1.0, -.195), (.21, .3, .08)), bevel=.025)
    add('torso', ORANGE, cap((0, .9, -.285), (0, 1.07, -.285), .082, .082, 14, 4))
    add('torso', METAL, tor((0, .92, -.285), .084, .013, seg=16))
    add('torso', METAL, tor((0, 1.05, -.285), .084, .013, seg=16))
    add('torso', METAL, lat([(1.13, 0), (1.13, .032), (1.19, .028), (1.19, 0)], 10, frame((0, 0, -.285))), sharp=40)
    add('torso', SLATE, ell((0, 1.205, -.285), (.04, .022, .04), 10, 6))
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
    hv, hf = lat([(-math.cos(PI * k / 14), math.sin(PI * k / 14) if 0 < k < 14 else 0) for k in range(15)], 22, None, 1, 1, headshape)
    add('head', SKIN, off((hv, hf), (0, HEADY + .215, .03)))
    add('head', SKIN, cap((0, HEADY - .06, 0), (0, HEADY + .05, .01), .06, .07, 10, 2))
    for s in (-1, 1):
        add('head', CHEEK, ell((s * .15, HEADY + .125, .158), (.036, .022, .012), 10, 5, RY(s * .75)))
    add('head', MOUTH, ell((0, HEADY + .108, .222), (.02, .011, .01), 8, 5))
    for k, c in EYE_C.items():
        s = 1 if c[0] > 0 else -1; R = RY(s * .4) @ RZ(-s * .2)
        P = lambda p: tuple(Vector((c[0], HEADY + c[1], c[2])) + (R @ Vector(p)))
        add(k, EYE, ell(P((0, 0, 0)), (.06, .08, .03), 16, 10, R))
        add(k, WHITE, ell(P((-.02, .032, .026)), (.02, .022, .01), 8, 5, R))
        add(k, WHITE, ell(P((.02, -.03, .027)), (.009, .009, .005), 6, 4, R))
    # bubble helmet
    HC = (0, HEADY + .25, -.07); HR = (.4, .4, .44)
    add('helmet', GLASS, ell(HC, HR, 24, 14))
    def onhel(d, k=.985):
        d = Vector(d).normalized(); return (HC[0] + HR[0] * d.x * k, HC[1] + HR[1] * d.y * k, HC[2] + HR[2] * d.z * k), d
    for d, r, roll in (((-.5, .5, .7), (.1, .03, .012), .7), ((-.2, .72, .66), (.03, .022, .01), 0)):
        p, n = onhel(d); Q = Vector((0, 0, 1)).rotation_difference(n).to_matrix().to_4x4() @ RZ(roll)
        add('helmet', SHINE, ell(p, r, 10, 5, Q))
    add('helmet', METAL, cap((0, HC[1] + .39, HC[2]), (0, HC[1] + .46, HC[2]), .012, .01, 6, 1))
    add('beacon', RED, ell((0, HC[1] + .485, HC[2]), (.03, .03, .03), 10, 6))

    # ---------------- limbs (left side is exported, right side is the same mesh) ----------------
    def arm(s, ex):
        U = lambda p: (s * SHX + p[0], SHY + p[1], p[2]); F = lambda p: (s * SHX + p[0], SHY - UARM + p[1], p[2])
        pu = 'armU'; pf = 'armF'
        if not ex: return
        add(pu, SUIT, ell(U((0, 0, 0)), (.074, .074, .074), 12, 8))
        add(pu, SUIT, cap(U((0, -.02, 0)), U((0, -UARM + .02, 0)), .058, .05, 12, 2))
        add(pf, SLATE, ell(F((0, 0, 0)), (.054, .054, .054), 12, 8))
        add(pf, SUIT, lat([(-.02, 0), (-.02, .046), (-.2, .054), (-.3, .07), (-.34, .078), (-.345, 0)], 12, frame(F((0, 0, 0)))))
        add(pf, ORANGE, tor(F((0, -.325, 0)), .074, .014, seg=14))
        add(pf, SLATE, ell(F((0, HANDY, 0)), (.064, .062, .064), 12, 8))
        for dx, dy, dz in ((-.038, -.058, .004), (0, -.072, .012), (.038, -.058, .004)):
            add(pf, SLATE, ell(F((dx, HANDY + dy, dz)), (.022, .04, .022), 8, 5))
        add(pf, SLATE, ell(F((0, HANDY - .02, .06)), (.021, .034, .021), 8, 5, RX(-.7)))
    def leg(s, ex):
        U = lambda p: (s * HIPX + p[0], HIP + p[1], p[2]); F = lambda p: (s * HIPX + p[0], HIP - THIGH + p[1], p[2])
        pu = 'legU'; pf = 'legF'
        if not ex: return
        add(pu, SUIT, cap(U((0, -.02, 0)), U((0, -THIGH + .02, 0)), .07, .06, 12, 2))
        add(pf, SLATE, ell(F((0, 0, 0)), (.06, .06, .06), 12, 8))
        add(pf, SUIT, lat([(-.02, 0), (-.02, .05), (-.24, .06), (-.34, .08), (-.385, .09), (-.39, 0)], 12, frame(F((0, 0, 0)))))
        add(pf, ORANGE, tor(F((0, -.37, 0)), .085, .014, seg=14))
        add(pf, SUIT, ell(F((0, -.425, .04)), (.09, .06, .138), 14, 8))
        add(pf, SLATE, ell(F((0, -.46, .04)), (.097, .024, .146), 14, 6))
    for s in (-1, 1): arm(s, s < 0); leg(s, s < 0)

    # ---------------- ray gun (right forearm) ----------------
    G = lambda p: (SHX + p[0], SHY - UARM + p[1], p[2])
    add('gun', ORANGE, ell(G((0, -.365, GZ)), (.04, .045, .04), 10, 6))
    add('gun', SUIT, lat([(0, 0), (.006, .04), (.05, .064), (.11, .06), (.165, .04), (.2, .03), (.235, .028), (.24, 0)], 14, frame(G((0, -.36, GZ)), (0, -1, 0))))
    for h, r, m in ((.265, .052, ORANGE), (.305, .043, SUIT), (.345, .035, ORANGE)):
        add('gun', m, ell(G((0, -.36 - h, GZ)), (r, .013, r), 14, 4))
    add('gun', METAL, cap(G((0, -.59, GZ)), G((0, -.74, GZ)), .015, .013, 8, 1))
    add('gun', GLOW, ell(G((0, -.765, GZ)), (.032, .032, .032), 10, 6))
    add('gun', SLATE, box(G((0, -.41, .02)), (.046, .11, .075)), bevel=.012)
    add('gun', ORANGE, box(G((0, -.455, GZ + .075)), (.016, .14, .06), RX(.25)), bevel=.006)
    add('gun', SLATE, lat([(0, 0), (0, .022), (.03, .022), (.03, 0)], 8, frame(G((0, -.335, GZ)), (0, 1, 0))), sharp=40)
    ANCH = {'port': PORT, 'gp': (0, -.3, GZ), 'muzzle': (0, -.765, GZ)}


    for k, (pv, at) in {'torso': ((0, 0, 0), ['upper']), 'head': ((0, HEADY, 0), ['head']), 'helmet': ((0, HEADY, 0), ['head']), 'beacon': ((0, HEADY, 0), ['head']),
                        'legU': (PIV0['legU'], ['leg0', 'leg1']), 'legF': (PIV0['legF'], ['knee0', 'knee1']), 'armU': (PIV0['armU'], ['arm0', 'arm1']), 'armF': (PIV0['armF'], ['elb0', 'elb1']), 'gun': (PIV0['gun'], ['elb1'])}.items(): part(k, pv, at)
    for k, c in EYE_C.items(): part(k, (c[0], HEADY + c[1], c[2]), ['head'], c)
    end({'hipx': HIPX, 'hip': round(HIP, 4), 'thigh': THIGH, 'heady': HEADY, 'shx': SHX, 'shy': SHY, 'uarm': UARM, 'handy': HANDY, 'hand': HANDY, 'hunch': .22, 'hs': 1.3, 'skin': 0xa9bccb}, ANCH)

def teacher():
    S = kit('teacher', skin=0xf1c9a5, top=0xf4f1e8, hips=0x4a5a7a, leg=0x4a5a7a, shoe=0x8a5a3a, hunch=.1); H = S['H']
    hair(S, 0x3a2a1a, 1.06, lambda z: .14 if z < .08 else .42)
    for p in ((-.2, .5, .05), (.2, .5, .05), (0, .54, -.1), (-.26, .3, -.1), (.26, .3, -.1), (0, .3, -.28)): add('head', 0x3a2a1a, ell(H(p), (.12, .1, .12), 8, 5))
    hair(S, 0x3a6ad0, 1.1, lambda z: .44); add('head', 0x3a6ad0, ell(H((0, .3, -.33)), (.08, .06, .05), 6, 4))
    eyes(S, .105, .27, (.03, .038, .018))
    for s in (-1, 1):
        p, R = onhead(S, s * .105, .27, 1.04); add('head', 0xc8372d, tor(p, .062, .01, tuple(R @ Vector((0, 0, 1))), 14, 5)); fe(S, 0x3a2a1a, s * .1, .37, (.05, .012, .012), s * .3)
    add('head', 0xc8372d, cap(H((-.045, .275, .29)), H((.045, .275, .29)), .009, .009, 5, 1)); cheeks(S, 0xf09a90, .2, .18); mouth(S, 0xb04a44, .13, (.03, .016, .01))
    z = lambda y: chestz(S, y)
    add('torso', 0xffffff, lat([(S['hip'] - .2, 0), (S['hip'] - .2, .29), (S['hip'] + .1, .26), (S['hip'] + .11, 0)], 16, sz=.86)); add('torso', 0x3a6ad0, tor((0, .9, 0), S['tr'](.9) + .01, .025, sz=S['td'], seg=18))
    add('torso', 0xffd23a, ell((.1, 1.15, z(1.15) + .005), (.035, .035, .012), 8, 4))
    e = S['E1']; hy = S['handy']
    add('ext1', 0x30303a, cap(e((0, hy + .02, .02)), e((0, hy - .2, .02)), .035, .035, 8, 1)); add('ext1', 0xb0b8c0, cone(e((0, hy - .3, .02)), e((0, hy - .18, .02)), .07, 10, .035)); add('ext1', B(0xfff4a0), ell(e((0, hy - .3, .02)), (.06, .01, .06), 10, 3))
    done(S)

ALL = [teacher, jiji, baba, salary, career, monkey, dog, alien, zombie, dino, panda, sumo, penguin, robot, ghost, kid]
