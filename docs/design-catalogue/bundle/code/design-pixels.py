#!/usr/bin/env python3
"""Pixel-level design metrics for one profile folder written by design-gates.mjs.

Reads NNN.jpg + NNN.json (text rectangles, colours, sizes) and measures what DOM tests cannot:
  - contrast of every text block measured against the pixels actually rendered behind it
  - dominant hue count (palette discipline), dead-space fraction, focal dominance (hierarchy proxy)
  - scroll determinism (same scroll position looks the same after scrolling away and back)
  - optional perceptual diff against an approved baseline folder
  - a contact sheet (contact.jpg) so a human can read the whole scroll at a glance
Usage: design-pixels.py <profile_dir> <dsf> [baseline_dir]    Prints one JSON object on stdout.
"""
import sys, os, json, glob, math, colorsys
import numpy as np
from PIL import Image

d, dsf = sys.argv[1], float(sys.argv[2])
base = sys.argv[3] if len(sys.argv) > 3 else None
out = {"contrast_fail": {}, "hues": [], "empty": [], "focal": [], "sizes": set(), "diff": None, "sync": []}

def lum(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]

def ratio(a, b):
    hi, lo = np.maximum(a, b), np.minimum(a, b)
    return (hi + 0.05) / (lo + 0.05)

steps = sorted(f for f in glob.glob(os.path.join(d, "[0-9][0-9][0-9].jpg")))
for jp in steps:
    meta_p = jp[:-4] + ".json"
    if not os.path.exists(meta_p):
        continue
    meta = json.load(open(meta_p))
    im = Image.open(jp).convert("RGB")
    W, H = im.size
    arr = np.asarray(im).astype(np.float32)
    # ---- contrast behind text
    for t in meta.get("texts", []):
        x0, y0 = int(max(0, t["x"] * dsf)), int(max(0, t["y"] * dsf))
        x1, y1 = int(min(W, (t["x"] + t["w"]) * dsf)), int(min(H, (t["y"] + t["h"]) * dsf))
        if x1 - x0 < 8 or y1 - y0 < 6:
            continue
        crop = arr[y0:y1, x0:x1].reshape(-1, 3)
        tc = np.array(t["color"], dtype=np.float32)
        dist = np.sqrt(((crop - tc) ** 2).sum(axis=1))
        bg = crop[dist > 90]
        if len(bg) < max(20, 0.25 * len(crop)):
            bg = crop  # text colour nearly equals background: judge everything
        bl = lum(bg)
        lt = float(lum(tc))
        # p15/p85 (not p5/p95): anti-aliased glyph edges are blends of text and background and must not count as background
        worst = float(min(ratio(lt, np.percentile(bl, 15)), ratio(lt, np.percentile(bl, 85))))
        large = t["fs"] >= 24 or (t["fs"] >= 18.66 and t["fw"] >= 700)
        need = 3.0 if large else 4.5
        if worst < need:
            k = t["label"]
            prev = out["contrast_fail"].get(k)
            if prev is None or worst < prev[0]:
                out["contrast_fail"][k] = [round(worst, 2), need]
        out["sizes"].add(round(t["fs"]))
    # ---- palette: dominant saturated hues
    small = np.asarray(im.resize((96, 160))).astype(np.float32) / 255.0
    flat = small.reshape(-1, 3)
    mx, mn = flat.max(axis=1), flat.min(axis=1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    mask = (sat > 0.28) & (mx > 0.25)
    if mask.sum() > 40:
        hs = np.array([colorsys.rgb_to_hsv(*p)[0] for p in flat[mask]])
        hist, _ = np.histogram(hs, bins=12, range=(0, 1))
        out["hues"].append(int((hist / hist.sum() > 0.08).sum()))
    else:
        out["hues"].append(0)
    # ---- dead space and focal dominance
    g = lum(arr)
    gh, gw = 28, 16
    bh, bw = H // gh, W // gw
    energy = np.zeros((gh, gw))
    covered = np.zeros((gh, gw), bool)
    for r in range(gh):
        for c in range(gw):
            blk = g[r * bh:(r + 1) * bh, c * bw:(c + 1) * bw]
            energy[r, c] = float(blk.std())
    for t in meta.get("texts", []):
        c0, c1 = int(t["x"] * dsf // bw), int(min(W - 1, (t["x"] + t["w"]) * dsf) // bw)
        r0, r1 = int(t["y"] * dsf // bh), int(min(H - 1, (t["y"] + t["h"]) * dsf) // bh)
        covered[max(0, r0):min(gh, r1 + 1), max(0, c0):min(gw, c1 + 1)] = True
    quiet = (energy < 0.012) & ~covered
    out["empty"].append(round(float(quiet.mean()), 2))
    e = np.sort(energy.ravel())[::-1]
    tot = e.sum()
    out["focal"].append(round(float(e[: max(1, len(e) // 10)].sum() / tot), 2) if tot > 0 else 0)

# ---- scroll determinism
for a in sorted(glob.glob(os.path.join(d, "sync-A-*.jpg"))):
    b = a.replace("sync-A-", "sync-B-")
    if os.path.exists(b):
        A = np.asarray(Image.open(a).convert("L")).astype(np.int16)
        B = np.asarray(Image.open(b).convert("L")).astype(np.int16)
        if A.shape == B.shape:
            out["sync"].append(round(float((np.abs(A - B) > 14).mean()), 3))

# ---- baseline diff
if base and os.path.isdir(base):
    ds = []
    for jp in steps[:40]:
        bp = os.path.join(base, os.path.basename(jp))
        if os.path.exists(bp):
            A = np.asarray(Image.open(jp).convert("L").resize((120, 200))).astype(np.float32)
            B = np.asarray(Image.open(bp).convert("L").resize((120, 200))).astype(np.float32)
            ds.append(float(np.abs(A - B).mean() / 255))
    if ds:
        out["diff"] = {"mean": round(float(np.mean(ds)), 3), "max": round(float(np.max(ds)), 3), "n": len(ds)}

# ---- contact sheet: up to 32 evenly spaced steps
if steps:
    pick = [steps[int(i * (len(steps) - 1) / max(1, min(32, len(steps)) - 1))] for i in range(min(32, len(steps)))]
    th = []
    for p in pick:
        im = Image.open(p).convert("RGB")
        w = 150
        th.append(im.resize((w, int(im.size[1] * w / im.size[0]))))
    cols = 8
    rows = math.ceil(len(th) / cols)
    cell_h = max(t.size[1] for t in th)
    sheet = Image.new("RGB", (cols * 154, rows * (cell_h + 4)), (24, 24, 24))
    for i, t in enumerate(th):
        sheet.paste(t, ((i % cols) * 154 + 2, (i // cols) * (cell_h + 4) + 2))
    sheet.save(os.path.join(d, "contact.jpg"), quality=80)
    out["contact"] = os.path.join(d, "contact.jpg")

out["sizes"] = sorted(out["sizes"])
print(json.dumps(out))
