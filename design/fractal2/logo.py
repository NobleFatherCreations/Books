#!/usr/bin/env python3
"""The Fractal² series logo: the whole map as one image.   python3 design/fractal2/logo.py [--size 4096]

A gold core named Fractal², then eight rings, one for each stage of the cycle, in the colours of the original
Fractal artwork (gold, amber, burnt orange, crimson, wine, steel, blue, navy). Each stage is named once, at the top of
its ring. Every tactic of the standard list (335) is set in its stage's ring, evenly spaced, upright in both halves.

Drawn from data, so every word is spelled as it is in the source:
  content/fractal/ent/build/sector.json   stage order and the standard tactic names (the same 335 in every sector)
Writes
  design/fractal2/art/fractal2-logo.svg                   the source drawing (fonts embedded)
  design/fractal2/art/fractal2-logo.json                  where every name sits (angle, radius) for interactive use
  library/fractal2/review/fractal2-logo-<size>.png        rendered by design/fractal2/logo_render.mjs
Typeface: Cormorant Garamond (SIL Open Font License), from tools/fonts/.
"""
import base64
import io
import json
import math
import random
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "design/fractal2/art"
TAU = 2 * math.pi

STAGES = ["Idealize", "Hook", "Devalue", "Confuse", "Isolate", "Extract", "Discard", "Replace"]
# ring colours, inside to outside: (inner edge, outer edge) of each band, sampled from the original artwork's rings
BAND = [("#8a5f22", "#4a3215"), ("#b8741f", "#6f4012"), ("#a9521c", "#6a2a12"), ("#8a2327", "#531219"),
        ("#641a2e", "#3a0f1f"), ("#4a5672", "#2c354d"), ("#263a66", "#17254a"), ("#152248", "#0b1330")]
LINE = ["#f6d98f", "#f6d98f", "#f3c781", "#f0b08a", "#e7a6ae", "#c5d3ee", "#a9c0ea", "#9fb6e4", "#f6d98f"]   # ring lines, core outward
CREAM, GOLD = "#f6ecd6", "#f6d98f"


# ---------- type ----------
def static_font(italic, wght, text):
    src = ROOT / "tools/fonts/cormorantgaramond" / ("CormorantGaramond-Italic[wght].ttf" if italic else "CormorantGaramond[wght].ttf")
    f = instancer.instantiateVariableFont(TTFont(src), {"wght": wght})
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    o = subset.Options(); o.layout_features = ["kern", "liga"]; o.notdef_outline = True; o.drop_tables += ["DSIG"]
    f2 = subset.load_font(buf, o)
    s = subset.Subsetter(o); s.populate(text=text + " "); s.subset(f2)
    out = io.BytesIO(); f2.save(out)
    f2 = TTFont(io.BytesIO(out.getvalue()))
    return f2, base64.b64encode(out.getvalue()).decode()


class Metrics:
    def __init__(self, font):
        self.cmap, self.hmtx, self.upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm

    def width(self, text, size, track=0.0):
        w = sum(self.hmtx[self.cmap.get(ord(ch), ".notdef")][0] if ord(ch) in self.cmap else self.upm * 0.5 for ch in text)
        return w / self.upm * size + track * size * len(text)


# ---------- layout ----------
RC = 182.0                           # core radius, in units where the disc radius is 1000
TRACK, TTRACK = 0.015, 0.14


def spread(names, widths, radii, caps, k, tw, s):
    """Share one stage's names between its k rows (the last row holds the title) and space them with equal gaps.
    -> (rows, smallest gap). Keeps the author's order, filling from the title row inward."""
    mingap = s * 1.7
    need = sum(widths) + mingap * len(names)
    rows, i, acc_cap, acc_w, worst = [], 0, 0.0, 0.0, 1e9
    order = list(range(k - 1, -1, -1))
    for idx, j in enumerate(order):
        acc_cap += caps[j]
        target = need * acc_cap / sum(caps)
        row = []
        while i < len(names) and (acc_w + (widths[i] + mingap) / 2 <= target or idx == len(order) - 1):
            row.append(i); acc_w += widths[i] + mingap; i += 1
        rr, is_title = radii[j], j == k - 1
        wsum = sum(widths[x] for x in row)
        gap = (caps[j] - wsum) / max(1, len(row) + (1 if is_title else 0))
        if row:
            worst = min(worst, gap)
        # angle 0 is the top, clockwise. A title row starts just right of the title; the others are staggered.
        a = (tw / 2 + gap) / rr if is_title else ((gap / 2) / rr if j % 2 else -(widths[row[0]] / 2) / rr if row else 0)
        items = []
        for x in row:
            items.append({"t": names[x], "a": (a + widths[x] / 2 / rr) % TAU, "w": widths[x]})
            a += (widths[x] + gap) / rr
        rows.append({"r": rr, "items": items, "gap": gap, "title": is_title, "f": s})
    return rows, worst


def layout(names_by_stage, M, MT, R=1000.0, grow=2.2):
    """All eight rings inside radius R. Each stage takes the fewest rows that hold it, then its letters are enlarged
    until those rows are full, so no ring is left with empty space. Returns rows with every name placed."""

    def stage(g, names, r_in, f, s, k):
        lh, tsize = s * 1.5, f * 2.55
        tlh = max(tsize * 1.22, lh)
        widths = [M.width(n, s, TRACK) for n in names]
        tw = MT.width(STAGES[g].upper(), tsize, TTRACK) + f * 7.0             # title plus its ornaments and air
        radii = [r_in + f * 0.55 + j * lh + lh / 2 for j in range(k - 1)]
        r_title = r_in + f * 0.55 + (k - 1) * lh + tlh / 2
        radii.append(r_title)
        caps = [TAU * x for x in radii[:-1]] + [TAU * r_title - tw]
        if min(caps) <= 0 or sum(caps) < sum(widths) + s * 1.7 * len(names):
            return None
        rows, worst = spread(names, widths, radii, caps, k, tw, s)
        if worst < s * 1.2:
            return None
        return rows, r_title, tsize, tlh, tw

    def build(f, extra):
        rows, bands, r = [], [], RC + f * 1.0
        for g, names in enumerate(names_by_stage):
            r_in, k = r, 1
            while stage(g, names, r_in, f, f, k) is None:                        # fewest rows that hold the stage
                k += 1
            k += extra[g]
            lo, hi = f, f * grow                                                 # then the largest letters those rows hold
            for _ in range(22):
                mid = (lo + hi) / 2
                if stage(g, names, r_in, f, mid, k) is None:
                    hi = mid
                else:
                    lo = mid
            srows, r_title, tsize, tlh, tw = stage(g, names, r_in, f, lo, k)
            for row in srows:
                row["g"] = g
            rows += srows
            r = r_title + tlh / 2 + f * 0.5
            bands.append({"g": g, "r0": r_in - f * 1.0 if g == 0 else r_in, "r1": r, "r_title": r_title, "tsize": tsize, "tw": tw, "f": lo})
        return {"f": f, "rows": rows, "bands": bands, "R": r, "RC": RC, "track": TRACK, "ttrack": TTRACK}

    def solve(extra):
        lo, hi = 4.0, 40.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if build(mid, extra)["R"] > R:
                hi = mid
            else:
                lo = mid
        return build(lo, extra)

    # give the ring with the smallest letters one more row for as long as that makes the smallest letters larger
    extra = [0] * len(names_by_stage)
    best = solve(extra)
    for _ in range(6):
        small = min(best["bands"], key=lambda b: b["f"])
        trial = extra[:]; trial[small["g"]] += 1
        cand = solve(trial)
        if min(b["f"] for b in cand["bands"]) <= small["f"] * 1.02:
            break
        extra, best = trial, cand
    return best


def layout_original(names_by_stage, M, MT, R=1000.0, caps=True, fill=0.80, biggest=1.12, outer=1.24):
    """The original Fractal: eight rings, one line of lettering in each. The stage name sits at the top of its ring and
    its techniques follow it round with the same gap between every two neighbours.

    To keep the rings full: every ring's letters are as large as its circumference allows (up to `biggest` times the
    middle ring's size), each ring is as tall as its letters need, and where a ring holds few words its letters are
    spaced out until the lettering covers about `fill` of the way round."""
    if caps:
        names_by_stage = [[n.upper() for n in st] for st in names_by_stage]
    t_min, t_max = (0.05, 0.62) if caps else (0.02, 0.12)
    H = R - RC - 10.0
    TS = 1.16                                                                 # stage name size, in name sizes

    def need(g, names, s, t):
        """length of the title, the names and the smallest gaps for one ring at name size s and letter-spacing t"""
        tw = MT.width(STAGES[g].upper(), s * TS, TTRACK) + s * 0.5 * 7.0
        return tw + sum(M.width(n, s, t) for n in names) + (len(names) + 1) * 1.5 * s

    heights = [H / 8] * 8
    for _ in range(40):                                                       # ring heights and letter sizes depend on each other
        radii, r = [], RC + 10.0
        for h in heights:
            radii.append(r + h / 2); r += h
        fit = []
        for g, names in enumerate(names_by_stage):
            lo, hi = 8.0, 200.0
            for _ in range(30):
                mid = (lo + hi) / 2
                if need(g, names, mid, t_min) > TAU * radii[g] * 0.94:
                    hi = mid
                else:
                    lo = mid
            fit.append(lo)
        cap = sorted(fit)[len(fit) // 2 - 1] * biggest                        # no ring's letters dwarf the others
        sizes = [min(x, cap * (outer if g >= 6 else 1.0)) for g, x in enumerate(fit)]   # the two outermost rings hold two names each on the longest circles
        want = [x * H / sum(sizes) for x in sizes]
        heights = [(a + b) / 2 for a, b in zip(heights, want)]

    rows, bands, r0 = [], [], RC + 10.0
    for g, names in enumerate(names_by_stage):
        s, r, C = sizes[g], radii[g], TAU * radii[g]
        lo, hi = t_min, t_max                                                 # space the letters out until the ring is covered
        for _ in range(30):
            mid = (lo + hi) / 2
            if need(g, names, s, mid) > C * fill:
                hi = mid
            else:
                lo = mid
        t = lo
        ts, u = s * TS, s * 0.5
        widths = [M.width(n, s, t) for n in names]
        tw = MT.width(STAGES[g].upper(), ts, TTRACK) + u * 7.0
        gap = (C - tw - sum(widths)) / (len(names) + 1)
        a, items = (tw / 2 + gap) / r, []
        for n, w in zip(names, widths):
            items.append({"t": n, "a": (a + w / 2 / r) % TAU, "w": w})
            a += (w + gap) / r
        rows.append({"g": g, "r": r, "items": items, "gap": gap, "title": True, "f": s, "track": t, "u": u})
        bands.append({"g": g, "r0": RC if g == 0 else r0, "r1": r0 + heights[g], "r_title": r, "tsize": ts, "tw": tw, "f": s, "u": u})
        r0 += heights[g]
    return {"f": sorted(sizes)[3] * 0.5, "rows": rows, "bands": bands, "R": R, "RC": RC, "track": t_min, "ttrack": TTRACK, "leaders": True}


# ---------- drawing ----------
def P(cx, cy, r, ang):
    """angle 0 = top, clockwise."""
    return cx + r * math.sin(ang), cy - r * math.cos(ang)


def arc_paths(pid, cx, cy, r):
    """Two full-circle paths: clockwise from the bottom (text upright in the top half) and counter-clockwise from the top (bottom half)."""
    cw = f'<path id="{pid}a" d="M{cx:.2f} {cy + r:.2f}A{r:.2f} {r:.2f} 0 1 1 {cx + 0.05:.2f} {cy + r:.2f}"/>'
    ccw = f'<path id="{pid}b" d="M{cx:.2f} {cy - r:.2f}A{r:.2f} {r:.2f} 0 1 0 {cx + 0.05:.2f} {cy - r:.2f}"/>'
    return cw + ccw


def on_arc(pid, r, ang, lift):
    """-> (href, startOffset). Top half reads clockwise on the baseline r - lift; bottom half reads counter-clockwise on r + lift."""
    top = ang < math.pi / 2 or ang > 3 * math.pi / 2
    if top:
        return pid + "a", (r - lift) * ((ang + math.pi) % TAU)
    return pid + "b", (r + lift) * ((TAU - ang) % TAU)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def draw(L, fonts, size=4096, caption=True, seed=7, names=True, core="Fractal2", cap=None):
    S = size
    cx, cy = S / 2, S * 0.487
    k = S * 0.437 / 1000.0                       # map units -> pixels (disc radius is 1000 units)
    f, RC = L["f"] * k, L["RC"] * k
    rnd = random.Random(seed)
    o = []
    A = o.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {S} {S}" width="{S}" height="{S}">')
    A("<defs><style>")
    for fam, b64, wt, st in fonts:
        A(f'@font-face{{font-family:"{fam}";src:url(data:font/ttf;base64,{b64}) format("truetype");font-weight:{wt};font-style:{st}}}')
    A(f'.n{{font-family:"FL";font-weight:700;letter-spacing:{L["track"]}em;fill:{CREAM};paint-order:stroke;stroke:#140b08;stroke-opacity:.55;stroke-linejoin:round}}')
    A(f'.nb{{font-family:"FL";font-weight:700;letter-spacing:{L["track"]}em;fill:#fbf3df;stroke:#fbf3df;stroke-linejoin:round}}')
    A(f'.t{{font-family:"FL";font-weight:700;letter-spacing:{L["ttrack"]}em;fill:#fdf1cf;paint-order:stroke;stroke:#140b08;stroke-opacity:.45;stroke-width:{f * .16:.2f}px;stroke-linejoin:round}}')
    A(f'.c{{font-family:"FL";font-weight:600;fill:#fdf3d8}}.cap{{font-family:"FL";font-style:italic;font-weight:500;fill:#ead9ae}}')
    A("</style>")
    A('<radialGradient id="sky" cx="50%" cy="48.7%" r="72%"><stop offset="0" stop-color="#131a3a"/><stop offset=".55" stop-color="#0a0f26"/><stop offset="1" stop-color="#04050d"/></radialGradient>')
    A('<radialGradient id="coreglow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffe9a8" stop-opacity=".95"/><stop offset=".35" stop-color="#f1b952" stop-opacity=".55"/><stop offset=".7" stop-color="#c76a22" stop-opacity=".18"/><stop offset="1" stop-color="#c76a22" stop-opacity="0"/></radialGradient>')
    A('<radialGradient id="corefill" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#16101a"/><stop offset=".6" stop-color="#120d16"/><stop offset="1" stop-color="#2c1b0f"/></radialGradient>')
    A('<linearGradient id="ringgold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff3c4"/><stop offset=".45" stop-color="#f0c35f"/><stop offset="1" stop-color="#b9792a"/></linearGradient>')
    for g, b in enumerate(L["bands"]):
        r0, r1 = b["r0"] * k, b["r1"] * k
        c0, c1 = BAND[g]
        A(f'<radialGradient id="b{g}" gradientUnits="userSpaceOnUse" cx="{cx:.1f}" cy="{cy:.1f}" r="{r1:.2f}"><stop offset="{r0 / r1:.4f}" stop-color="{c0}"/><stop offset="{(r0 + (r1 - r0) * .5) / r1:.4f}" stop-color="{c1}"/><stop offset="1" stop-color="{c1}"/></radialGradient>')
    A(f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{S * .0022:.2f}"/></filter>')
    A(f'<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{S * .006:.2f}"/></filter>')
    A(f'<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{S * .03:.2f}"/></filter>')
    A(f'<filter id="neb" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{3.2 / S:.6f}" numOctaves="5" seed="11"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .8  1.5 0 0 0 -.62"/><feGaussianBlur stdDeviation="{S * .006:.2f}"/></filter>')
    A(f'<filter id="neb2" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{2.1 / S:.6f}" numOctaves="4" seed="29"/><feColorMatrix values="0 0 0 0 .95  0 0 0 0 .66  0 0 0 0 .34  0 1.6 0 0 -.74"/><feGaussianBlur stdDeviation="{S * .008:.2f}"/></filter>')
    A(f'<radialGradient id="ray" gradientUnits="userSpaceOnUse" cx="{cx:.1f}" cy="{cy:.1f}" r="{S * .7:.1f}"><stop offset="0" stop-color="#ffe7a6" stop-opacity=".0"/><stop offset=".3" stop-color="#ffe7a6" stop-opacity=".22"/><stop offset="1" stop-color="#9fb6ff" stop-opacity="0"/></radialGradient>')
    A(f'<radialGradient id="vig" cx="50%" cy="48.7%" r="75%"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".62"/></radialGradient>')
    A(f'<clipPath id="disc"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{L["R"] * k:.2f}"/></clipPath>')
    # text paths
    for i, row in enumerate(L["rows"]):
        lift = row["f"] * k * 0.30
        r = row["r"] * k
        A(f'<path id="r{i}a" d="M{cx:.2f} {cy + r - lift:.2f}A{r - lift:.2f} {r - lift:.2f} 0 1 1 {cx + .05:.2f} {cy + r - lift:.2f}"/>')
        A(f'<path id="r{i}b" d="M{cx:.2f} {cy - r - lift:.2f}A{r + lift:.2f} {r + lift:.2f} 0 1 0 {cx + .05:.2f} {cy - r - lift:.2f}"/>')
    for g, b in enumerate(L["bands"]):
        r = b["r_title"] * k
        lift = b["tsize"] * k * 0.33
        A(f'<path id="t{g}" d="M{cx:.2f} {cy + r - lift:.2f}A{r - lift:.2f} {r - lift:.2f} 0 1 1 {cx + .05:.2f} {cy + r - lift:.2f}"/>')
    A("</defs>")

    # ---- the sky ----
    A(f'<rect width="{S}" height="{S}" fill="url(#sky)"/>')
    A(f'<rect width="{S}" height="{S}" filter="url(#neb)" opacity=".5"/>')
    A(f'<rect width="{S}" height="{S}" filter="url(#neb2)" opacity=".34"/>')
    Rpx = L["R"] * k
    for i in range(24):                                   # light rays from the core, out past the rings
        a = TAU * i / 24 + (0.06 if i % 2 else 0)
        wdt = (0.011 if i % 3 == 0 else 0.005) * (1.6 if i % 6 == 0 else 1)
        ln = S * (0.70 if i % 6 == 0 else 0.6 if i % 3 == 0 else 0.5)
        x1, y1 = P(cx, cy, ln, a - wdt); x2, y2 = P(cx, cy, ln, a + wdt)
        A(f'<path d="M{cx:.1f} {cy:.1f}L{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}Z" fill="url(#ray)" opacity="{.9 if i % 6 == 0 else .55}"/>')
    stars = []
    for _ in range(2600):
        x, y = rnd.uniform(0, S), rnd.uniform(0, S)
        d = math.hypot(x - cx, y - cy)
        if d < Rpx * 1.005:
            continue
        rr = S * rnd.choice([.00022, .00026, .0003, .00036, .00044, .0006, .0009])
        stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.2f}" fill="{rnd.choice(["#fff", "#fff", "#ffe9c2", "#cfe0ff"])}" opacity="{rnd.uniform(.35, .95):.2f}"/>')
    A("".join(stars))
    for _ in range(13):                                   # a few bright four-point stars
        while True:
            x, y = rnd.uniform(S * .03, S * .97), rnd.uniform(S * .03, S * .97)
            if math.hypot(x - cx, y - cy) > Rpx * 1.03:
                break
        ln = S * rnd.uniform(.004, .011); col = rnd.choice(["#fff6d8", "#ffffff", "#dbe7ff"])
        A(f'<g opacity="{rnd.uniform(.6, 1):.2f}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{ln * .9:.1f}" fill="{col}" opacity=".16" filter="url(#glow2)"/>'
          f'<path d="M{x - ln:.1f} {y:.1f}Q{x:.1f} {y:.1f} {x:.1f} {y - ln * 1.25:.1f}Q{x:.1f} {y:.1f} {x + ln:.1f} {y:.1f}Q{x:.1f} {y:.1f} {x:.1f} {y + ln * 1.25:.1f}Q{x:.1f} {y:.1f} {x - ln:.1f} {y:.1f}Z" fill="{col}" opacity=".9"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{ln * .12:.2f}" fill="#fff"/></g>')

    # ---- the disc: an outer halo, then the eight bands ----
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{Rpx * 1.012:.1f}" fill="none" stroke="#f1c66a" stroke-width="{S * .012:.1f}" opacity=".5" filter="url(#soft)"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{Rpx:.2f}" fill="#0b1330"/>')
    for g in range(7, -1, -1):
        b = L["bands"][g]
        A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{b["r1"] * k:.2f}" fill="url(#b{g})"/>')
    # warmth spilling out of the core, and a little cloud inside the rings, as in the painting
    A(f'<g clip-path="url(#disc)"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{Rpx * .56:.1f}" fill="url(#coreglow)" opacity=".36"/>'
      f'<rect width="{S}" height="{S}" filter="url(#neb2)" opacity=".22"/><rect width="{S}" height="{S}" filter="url(#neb)" opacity=".16"/></g>')
    # faint spokes behind the words: the eight directions of the original
    for i in range(8):
        a = TAU * i / 8
        x1, y1 = P(cx, cy, RC, a); x2, y2 = P(cx, cy, Rpx, a)
        A(f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="#ffe6a8" stroke-width="{S * .0005:.2f}" opacity="{.0 if i in (0, 4) else .13}"/>')
    # ring lines with their glow, and the small lights where the eight directions cross them
    radii = [L["bands"][0]["r0"] * k] + [b["r1"] * k for b in L["bands"]]
    for i, r in enumerate(radii):
        col = LINE[i]
        wline = S * (.0011 if i not in (0, 8) else .0018)
        A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{wline * 3.2:.2f}" opacity=".5" filter="url(#glow)"/>')
        A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{wline:.2f}" opacity=".95"/>')
        for j in range(8):
            if i < 8 and j in (0,) and False:
                continue
            x, y = P(cx, cy, r, TAU * j / 8)
            dr = S * (.0019 if j % 2 == 0 else .0015)
            A(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{dr * 2.6:.2f}" fill="{col}" opacity=".45" filter="url(#glow)"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{dr:.2f}" fill="#fffbe9"/>')

    # ---- the words ----
    place = []
    for i, row in enumerate(L["rows"] if names else []):
        r = row["r"] * k
        fs = row["f"] * k
        n = len(row["items"])
        for j, it in enumerate(row["items"]):
            top = it["a"] < math.pi / 2 or it["a"] > 3 * math.pi / 2
            href = f"r{i}a" if top else f"r{i}b"
            lift = fs * 0.30
            off = (r - lift) * ((it["a"] + math.pi) % TAU) if top else (r + lift) * ((TAU - it["a"]) % TAU)
            tp = f'<textPath href="#{href}" xlink:href="#{href}" startOffset="{off:.2f}">{esc(it["t"])}</textPath></text>'
            ls = f' letter-spacing="{row["track"]:.3f}em"' if "track" in row else ""
            A(f'<text class="n"{ls} font-size="{fs:.2f}px" stroke-width="{fs * .16:.2f}" text-anchor="middle">{tp}')      # soft dark edge
            A(f'<text class="nb"{ls} font-size="{fs:.2f}px" stroke-width="{fs * .034:.2f}" text-anchor="middle">{tp}')    # the letter, a touch heavier than the bold cut
            place.append({"t": it["t"], "g": row["g"], "a": round(it["a"], 5), "r": round(row["r"], 2), "f": round(row["f"], 2)})
            if L.get("leaders"):
                continue
            # a small gold point in the middle of the space before the next name
            nxt = row["items"][(j + 1) % n]
            if n > 1 or row["title"]:
                if row["title"] and j == n - 1:
                    continue
                span = (nxt["a"] - it["a"]) % TAU
                mid = (it["a"] + (it["w"] / 2 / row["r"] + (span - it["w"] / 2 / row["r"] - nxt["w"] / 2 / row["r"]) / 2)) % TAU
                x, y = P(cx, cy, r, mid)
                A(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{fs * .075:.2f}" fill="{GOLD}" opacity=".85"/>')
        if L.get("leaders"):
            # the original: a fine gold line and a light in every space, so each ring reads as one unbroken circle
            b = L["bands"][row["g"]]
            uu = row.get("u", L["f"])
            half = (b["tw"] - uu * 7.0) / 2 / row["r"] + uu * 3.6 / row["r"]                  # title and its side ornaments
            spans = [(-half, half)] + [(it["a"] - it["w"] / 2 / row["r"], it["a"] + it["w"] / 2 / row["r"]) for it in row["items"]]
            m = row["f"] * 0.85 / row["r"]
            for q in range(len(spans)):
                a0 = spans[q][1] + m
                a1 = (spans[(q + 1) % len(spans)][0] - m) if q + 1 < len(spans) else (TAU - half - m)
                if a1 - a0 <= 0:
                    continue
                mid = (a0 + a1) / 2
                if (a1 - a0) * row["r"] > row["f"] * 2.4:
                    for (p0, p1) in ((a0, mid - row["f"] * 0.55 / row["r"]), (mid + row["f"] * 0.55 / row["r"], a1)):
                        x0, y0 = P(cx, cy, r, p0); x1, y1 = P(cx, cy, r, p1)
                        A(f'<path d="M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 {1 if p1 - p0 > math.pi else 0} 1 {x1:.2f} {y1:.2f}" stroke="{GOLD}" stroke-width="{fs * .035:.2f}" fill="none" opacity=".55"/>')
                x, y = P(cx, cy, r, mid)
                A(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{fs * .28:.2f}" fill="{GOLD}" opacity=".45" filter="url(#glow)"/><circle cx="{x:.2f}" cy="{y:.2f}" r="{fs * .1:.2f}" fill="#fff6d6"/>')
    for g, b in enumerate(L["bands"]):
        r, ts = b["r_title"] * k, b["tsize"] * k
        lift = ts * 0.33
        off = (r - lift) * math.pi
        A(f'<text class="t" font-size="{ts:.2f}px" text-anchor="middle" filter="url(#glow2)" opacity=".55" style="fill:#ffd98a"><textPath href="#t{g}" xlink:href="#t{g}" startOffset="{off:.2f}">{STAGES[g].upper()}</textPath></text>')
        A(f'<text class="t" font-size="{ts:.2f}px" text-anchor="middle"><textPath href="#t{g}" xlink:href="#t{g}" startOffset="{off:.2f}">{STAGES[g].upper()}</textPath></text>')
        fo = b.get("u", L["f"]) * k                                     # ornament unit: the ring's own, if it has one
        half = (b["tw"] * k - fo * 7.0 + ts * L["ttrack"]) / 2 / r     # half the title's angle
        for sgn in (-1, 1):                                             # the line and light on each side of the name
            a0 = sgn * (half + fo * 0.9 / r); a1 = sgn * (half + fo * 2.9 / r)
            x0, y0 = P(cx, cy, r, a0); x1, y1 = P(cx, cy, r, a1)
            A(f'<path d="M{x0:.2f} {y0:.2f}A{r:.2f} {r:.2f} 0 0 {1 if sgn > 0 else 0} {x1:.2f} {y1:.2f}" stroke="{GOLD}" stroke-width="{fo * .07:.2f}" fill="none" opacity=".9"/>')
            A(f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="{fo * .2:.2f}" fill="#fff6d6"/><circle cx="{x0:.2f}" cy="{y0:.2f}" r="{fo * .55:.2f}" fill="{GOLD}" opacity=".5" filter="url(#glow)"/>')

    # ---- the core ----
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * 2.1:.1f}" fill="url(#coreglow)" opacity=".85"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC:.2f}" fill="url(#corefill)"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * .93:.2f}" fill="none" stroke="#ffcf73" stroke-width="{RC * .26:.2f}" opacity=".6" filter="url(#glow2)"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * .93:.2f}" fill="none" stroke="url(#ringgold)" stroke-width="{RC * .115:.2f}"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * .985:.2f}" fill="none" stroke="#fff6d2" stroke-width="{RC * .012:.2f}" opacity=".9"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * .868:.2f}" fill="none" stroke="#fff6d2" stroke-width="{RC * .010:.2f}" opacity=".75"/>')
    A(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RC * .80:.2f}" fill="none" stroke="#f0c35f" stroke-width="{RC * .006:.2f}" opacity=".5"/>')
    if core == "Fractal2":
        cs = RC * 0.40
        title = f'<text class="c" x="{cx - cs * .06:.1f}" y="{cy + cs * .30:.1f}" font-size="{cs:.1f}px" text-anchor="middle" letter-spacing=".01em">Fractal<tspan font-size="{cs * .58:.1f}px" dy="{-cs * .40:.1f}" dx="{cs * .03:.1f}" fill="{GOLD}">2</tspan></text>'
    else:                                                                     # two lines: a small first word over the name
        w1, w2 = core.split(" ", 1)
        cs = RC * 0.40
        title = (f'<text class="c" x="{cx:.1f}" y="{cy - cs * .42:.1f}" font-size="{cs * .46:.1f}px" text-anchor="middle" letter-spacing=".22em" fill="{GOLD}" style="fill:{GOLD}">{esc(w1.upper())}</text>'
                 f'<text class="c" x="{cx:.1f}" y="{cy + cs * .52:.1f}" font-size="{cs:.1f}px" text-anchor="middle" letter-spacing=".01em">{esc(w2)}</text>')
    A(title.replace('class="c"', 'class="c" filter="url(#glow2)" opacity=".5"'))
    A(title)
    if caption:
        n_tac = sum(len(r["items"]) for r in L["rows"])
        A(f'<text class="cap" x="{cx:.1f}" y="{S * .962:.1f}" font-size="{S * .0165:.1f}px" text-anchor="middle" letter-spacing=".04em">{cap or ("8 Stages. %d Tactics. One Cycle." % n_tac if names else "8 Stages. One Cycle.")}</text>')
    A(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    A("</svg>")
    return "".join(o), place


def original_names():
    """The thirty techniques of The Fractal, by stage, read from the published chapter (so every word matches the book)."""
    import html as H, re
    h = (ROOT / "library/fractal/the-pattern.html").read_text(encoding="utf-8")
    h = re.sub(r"(?s)<(script|style|svg)\b.*?</\1>", "", h)
    text = H.unescape(re.sub(r"<[^>]+>", "\n", h))
    out, cur = [[] for _ in STAGES], None
    for line in (x.strip() for x in text.split("\n")):
        m = re.match(r"Stage:\s*(\w+)\s*[—-]", line)
        if m and m.group(1) in STAGES:
            cur = STAGES.index(m.group(1)); continue
        m = re.match(r"(\d\d)\s*·\s*(.+)$", line)
        if m and cur is not None and m.group(2) not in out[cur] and sum(map(len, out)) < 30:
            out[cur].append(m.group(2).strip())
    assert [len(x) for x in out] == [2, 2, 4, 5, 6, 7, 2, 2], [len(x) for x in out]
    return out


def main():
    size = int(sys.argv[sys.argv.index("--size") + 1]) if "--size" in sys.argv else 4096
    sec = json.loads((ROOT / "content/fractal/ent/build/sector.json").read_text())
    names = [[t["name"] for t in sec["tactics"] if t["stage"] == s] for s in sec["stages"]]
    orig = original_names()
    alltext = "".join(n + n.upper() for st in names + orig for n in st) + "".join(s.upper() for s in STAGES) + "Fractal2 THE The 8 Stages. 0123456789 Tactics. Techniques. One Cycle."
    f600, b600 = static_font(False, 600, alltext)
    f700, b700 = static_font(False, 700, alltext)
    fi, bi = static_font(True, 500, alltext)
    fonts = [("FL", b600, 600, "normal"), ("FL", b700, 700, "normal"), ("FL", bi, 500, "italic")]
    M7 = Metrics(f700)

    # the series logo: all 335 tactics
    L = layout(names, M7, M7)
    svg, place = draw(L, fonts, size)
    (ART / "fractal2-logo.svg").write_text(svg)
    emblem, _ = draw(L, fonts, size, names=False)
    (ART / "fractal2-emblem.svg").write_text(emblem)        # the same rings without the small names, for small sizes
    (ART / "fractal2-logo.json").write_text(json.dumps({"R": 1000, "core": L["RC"],
        "bands": [{"stage": STAGES[b["g"]], "r0": round(b["r0"], 2), "r1": round(b["r1"], 2), "letter": round(b["f"], 2)} for b in L["bands"]], "names": place}, ensure_ascii=False, separators=(",", ":")))
    print("logo: base letter %.2f units; rows %d; names placed %d; rings end at %.1f" % (L["f"], len(L["rows"]), len(place), L["R"]))
    print("  rows per stage:", [sum(1 for r in L["rows"] if r["g"] == g) for g in range(8)], "names per stage:", [sum(len(r["items"]) for r in L["rows"] if r["g"] == g) for g in range(8)])
    print("  letter size per stage (units, px at %d):" % size, [(round(b["f"], 1), round(b["f"] * size * 0.437 / 1000, 1)) for b in L["bands"]])

    # the original: eight stages, thirty techniques, in the same colours, so one can open into the other
    LO = layout_original(orig, M7, M7)
    for core, cap, out in (("The Fractal", "8 Stages. 30 Techniques. One Cycle.", "fractal-original.svg"),
                           ("Fractal2", "8 Stages. 30 Techniques. One Cycle.", "fractal-original-f2.svg")):
        svg, place = draw(LO, fonts, size, core=core, cap=cap)
        (ART / out).write_text(svg)
    print("original: names placed %d; per ring (letter px at %d, spacing em, share of ring covered):" % (len(place), size),
          [(round(r["f"] * size * 0.437 / 1000), round(r["track"], 2), round(1 - (len(r["items"]) + 1) * r["gap"] / (TAU * r["r"]), 2)) for r in LO["rows"]])


if __name__ == "__main__":
    main()
