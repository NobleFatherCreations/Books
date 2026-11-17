#!/usr/bin/env python3
"""Fractal² film gate helper: is each of the owner's plates actually visible as itself in the rendered frame?
python3 -I scripts/film2-plates.py jobs.json out.json   (called by scripts/film2-check.mjs)

Each job: a frame (PNG at CSS scale, captions hidden), the engine's geometry for that frame (FILM.heroGeo()), the plate(s)
expected, and a role. For every frame the expected plate is warped to its footprint (centre, size, angle), unlit, and the
frame is compared with it inside the footprint: SSIM and the normalized cross-correlation of Sobel edge magnitude, both
on grayscale downsampled to 256 px on the long side (AUDIT-2026-11-17.md section 5)."""
import sys, json, os, math
import numpy as np
from PIL import Image
from scipy import ndimage as nd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')); PL = os.path.join(ROOT, 'library/fractal2/site/fractal2/_a/film/plates')
CACHE = {}
def plate(k):
    k = k.replace('p:', '')
    if k not in CACHE: CACHE[k] = np.asarray(Image.open(os.path.join(PL, k + '-m.webp')).convert('L')).astype(np.float32) / 255
    return CACHE[k]

def sample(img, u, v):
    h, w = img.shape; x = np.clip(u * (w - 1), 0, w - 1); y = np.clip((1 - v) * (h - 1), 0, h - 1)
    return nd.map_coordinates(img, [y, x], order=1)

def warp(k, g, X, Y, twin=None):
    """plate k drawn at g (CSS px: x, y, r, ang, asp, disc) onto the pixel grid X, Y (CSS px). Returns (image, mask)."""
    fx, fy = X - g['x'], g['y'] - Y; c, s = math.cos(g['ang']), math.sin(g['ang'])
    dx, dy = (c * fx - s * fy) / g['r'], (s * fx + c * fy) / g['r']
    off = .026 if g.get('disc', 0) > 1.5 else 0.
    u, v = (dx / g.get('asp', 1)) * .5 + .5, (dy - off) * .5 + .5
    rr = np.hypot(dx, dy)
    m = (rr < .88) if g.get('disc', 0) > .5 else ((np.abs(dx) < g.get('asp', 1) * .985) & (np.abs(dy) < .985))
    if g.get('rev', 9) < 1.5: m &= rr < g['rev'] - .03
    return sample(plate(k), u, v), m

def ssim_map(a, b):
    C1, C2 = .01 ** 2, .03 ** 2; f = lambda z: nd.gaussian_filter(z, 1.5)
    ma, mb = f(a), f(b); va, vb, cv = f(a * a) - ma * ma, f(b * b) - mb * mb, f(a * b) - ma * mb
    return ((2 * ma * mb + C1) * (2 * cv + C2)) / ((ma * ma + mb * mb + C1) * (va + vb + C2))

def edges(a): a = nd.gaussian_filter(a, 1.0); return np.hypot(nd.sobel(a, 0), nd.sobel(a, 1))      # 1 px blur first: sub-pixel registration must not decide the score
def ncc(a, b, m):
    a, b = a[m], b[m]
    if a.size < 50: return 0.
    a = a - a.mean(); b = b - b.mean(); d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 1e-9 else 0.

def L(rgb):
    a = rgb / 255.; a = np.where(a <= .03928, a / 12.92, ((a + .055) / 1.055) ** 2.4); return .2126 * a[..., 0] + .7152 * a[..., 1] + .0722 * a[..., 2]

def job(j):
    im = np.asarray(Image.open(j['f']).convert('RGB')).astype(np.float32); H, W = im.shape[:2]
    k = 256 / max(W, H); w2, h2 = max(8, round(W * k)), max(8, round(H * k))
    Y, X = np.mgrid[0:h2, 0:w2].astype(np.float32); X = (X + .5) / k; Y = (Y + .5) / k
    fr = np.asarray(Image.fromarray(im.astype(np.uint8)).convert('L').resize((w2, h2), Image.BILINEAR)).astype(np.float32) / 255
    lum = L(im); out = {'t': j['t'], 'hero': j['hero']}
    out['white90'] = float((lum >= .90).mean())
    g = j['geo']; role = j['role']
    if role == 'stone':
        w = g['win']
        if not w: out.update(ok=False, why='no window'); return out
        th = max(W, H) / 2; ref = sample(plate('basalt'), (X - W / 2) / (2 * th) + .5, 1 - ((Y - H / 2) / (2 * th) + .5))
        ox, oy = X - w['x'], w['y'] - Y; tp = w['hh'] - w['hw']
        so = np.where(oy > tp, np.hypot(ox, oy - tp) - w['hw'], np.maximum(np.abs(ox) - w['hw'], -w['hh'] - oy))
        m = so > 6
        for b in j.get('caps', []): m &= ~((X >= b[0]) & (X <= b[2]) & (Y >= b[1]) & (Y <= b[3]))
        Yf, Xf = np.mgrid[0:H, 0:W].astype(np.float32) + .5      # stone grain is fine: measured at full CSS resolution
        reff = sample(plate('basalt'), (Xf - W / 2) / (2 * th) + .5, 1 - ((Yf - H / 2) / (2 * th) + .5)); ox, oy = Xf - w['x'], w['y'] - Yf
        so = np.where(oy > tp, np.hypot(ox, oy - tp) - w['hw'], np.maximum(np.abs(ox) - w['hw'], -w['hh'] - oy)); mf = so > 6
        for b in j.get('caps', []): mf &= ~((Xf >= b[0]) & (Xf <= b[2]) & (Yf >= b[1]) & (Yf <= b[3]))
        e = ncc(edges(lum.astype(np.float32) ** (1 / 2.2)), edges(reff), mf); out.update(ncc=e, ok=e >= .30, frac=float(mf.mean())); return out
    refs = []
    if role == 'split':
        pl = g['pl']; a, ma = warp(pl['pa'], pl, X, Y); b, mb = warp(pl['pb'], pl, X, Y); right = X >= pl['seam']; ref = np.where(right, b, a); m = ma
        refs.append((ref, m, pl))
    elif role == 'texture':
        pl = g['pl']
        if not pl or not pl.get('pa'): out.update(ok=False, why='no plate'); return out
        ref, m = warp(pl['pa'], pl, X, Y); refs.append((ref, m, pl))
    else:
        hs = [h for h in g['hero'] if h and h['a'] > 0]
        for p in j['plates']:
            h = next((h for h in hs if h['k'] == 'p:' + p), None)
            if h is None: out.update(ok=False, why='plate %s not drawn' % p); return out
            ref, m = warp(h['k'], h, X, Y); refs.append((ref, m, h))
    res = []
    if role != 'texture':                                    # measure at 256 px across the plate's footprint (not across the whole screen, where a small plate would be a few dozen pixels)
        refs2 = []
        for ref, m, gg in refs:
            ex = gg['r'] * (gg.get('asp', 1) if gg.get('disc', 0) < .5 else 1) * 1.02; ey = gg['r'] * 1.02
            x0, x1, y0, y1 = max(0, gg['x'] - ex), min(W, gg['x'] + ex), max(0, gg['y'] - ey), min(H, gg['y'] + ey)
            if x1 - x0 < 8 or y1 - y0 < 8: continue
            kk = 256 / max(x1 - x0, y1 - y0); ww, hh = max(8, round((x1 - x0) * kk)), max(8, round((y1 - y0) * kk))
            Yc, Xc = np.mgrid[0:hh, 0:ww].astype(np.float32); Xc = x0 + (Xc + .5) / kk; Yc = y0 + (Yc + .5) / kk
            crop = np.asarray(Image.fromarray(im.astype(np.uint8)).convert('L').crop((int(x0), int(y0), int(math.ceil(x1)), int(math.ceil(y1)))).resize((ww, hh), Image.BILINEAR)).astype(np.float32) / 255
            if gg is refs[0][2] and role == 'split':
                pl = gg; a, ma = warp(pl['pa'], pl, Xc, Yc); b, _ = warp(pl['pb'], pl, Xc, Yc); r2, m2 = np.where(Xc >= pl['seam'], b, a), ma
            else: r2, m2 = warp(gg.get('k') or gg['pa'], gg, Xc, Yc)
            refs2.append((r2, m2, gg, crop))
        refs = refs2
    else: refs = [(r, m, g_, fr) for r, m, g_ in refs]
    for ref, m, gg, fr in refs:
        if m.sum() < 50: out.update(ok=False, why='footprint off screen'); return out
        ss = float(ssim_map(fr, ref)[m].mean()); ee = ncc(edges(fr), edges(ref), m)
        # how much of the plate's own image is inside the viewport (sampled over its full disc or rectangle)
        n = 64; uu, vv = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n)); disc = gg.get('disc', 0) > .5; asp = gg.get('asp', 1)
        sel = (np.hypot(uu, vv) <= .905) if disc else np.ones_like(uu, bool); px_, py_ = uu * (1 if disc else asp), vv
        c, s = math.cos(gg['ang']), math.sin(gg['ang']); sx = gg['x'] + (c * px_ + s * py_) * gg['r']; sy = gg['y'] - (-s * px_ + c * py_) * gg['r']
        inv = float(((sx >= 0) & (sx <= W) & (sy >= 0) & (sy <= H))[sel].mean())
        g2 = dict(gg); mm = warp(gg.get('k') or gg['pa'], g2, *np.mgrid[0:H, 0:W].astype(np.float32)[::-1] + .5)[1]
        burn = float((lum[mm] >= .95).mean()) if mm.any() else 0.
        thr = (.20, None) if role == 'texture' else (.45, .50)
        ok = ee >= thr[0] and (thr[1] is None or ss >= thr[1])
        res.append({'ssim': round(ss, 3), 'ncc': round(ee, 3), 'inview': round(inv, 3), 'burn95': round(burn, 4), 'ok': ok, 'x': gg['x'], 'y': gg['y'], 'r': gg['r'], 'k': gg.get('k') or gg.get('pa')})
    out['plates'] = res; out['ok'] = all(r['ok'] for r in res); return out

def strength(j):
    """effective strength at mid-hold: the change the plate makes, projected on the change the bare plate would make"""
    A = np.asarray(Image.open(j['f']).convert('L')).astype(np.float32) / 255; B = np.asarray(Image.open(j['f0']).convert('L')).astype(np.float32) / 255
    H, W = A.shape; Y, X = np.mgrid[0:H, 0:W].astype(np.float32) + .5; out = []
    for h in [h for h in j['geo']['hero'] if h and h['a'] > 0 and h['k'] in ['p:' + p for p in j['plates']]]:
        P, m = warp(h['k'], h, X, Y)
        if m.sum() < 50: continue
        d = (P - B)[m]; num = float(((A - B)[m] * d).sum()); den = float((d * d).sum()) + 1e-9
        out.append({'k': h['k'], 's': round(min(1.5, max(0., num / den)), 3)})
    return out

if __name__ == '__main__':
    J = json.load(open(sys.argv[1])); R = {'frames': [job(j) for j in J['frames']], 'strength': [{'hero': j['hero'], 'res': strength(j)} for j in J.get('strength', [])]}
    json.dump(R, open(sys.argv[2], 'w'))
