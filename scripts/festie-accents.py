#!/usr/bin/env python3
"""Give every guide a distinct accent color, placed by hue gap.

Each guide's cards, chips, bullets and labels are tinted by a --acc custom
property keyed off its acronymClass. A new guide with no rule silently falls
back to the page default and looks unfinished, so this assigns one: convert
the existing accents to HSL, find the widest unused arc on the hue wheel,
and place the new guide at its midpoint using the family's mean saturation
and lightness so it belongs to the same palette.

Idempotent -- a guide that already has a rule is left alone.
"""
import colorsys
import json
import re
import sys

DATA = "content/festie-bible-data.json"
PAGE = "library/festival/index.html"


def hexof(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    rgb = tuple(int(round(c * 255)) for c in (r, g, b))
    return "#" + "".join(f"{c:02X}" for c in rgb), rgb


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    s = open(PAGE, encoding="utf-8").read()
    before = s

    have = dict(re.findall(r"\.(fb-g-[a-z]+)\{ --acc:(#[0-9A-Fa-f]{6});", s))
    need = [g for g in d["guides"] if g["acronymClass"] not in have]
    if not need:
        print("every guide already has an accent")
        return 0

    for g in need:
        pts = []
        for hx in have.values():
            r, gg, b = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            h, l, sat = colorsys.rgb_to_hls(r, gg, b)
            pts.append((h * 360, sat, l))
        hues = sorted(p[0] for p in pts)
        gaps = [(((hues[(i + 1) % len(hues)] - hues[i]) % 360), hues[i])
                for i in range(len(hues))]
        gap, at = max(gaps)
        mid = (at + gap / 2) % 360
        mean_s = sum(p[1] for p in pts) / len(pts)
        mean_l = sum(p[2] for p in pts) / len(pts)
        hx, rgb = hexof(mid, mean_s, mean_l)

        # insert next to the other guide rules so the block stays together
        anchor = re.search(r"\.fb-g-[a-z]+\{ --acc:#[0-9A-Fa-f]{6}; --acc-dim:[^}]*\}", s)
        rule = f"\n.{g['acronymClass']}{{ --acc:{hx}; --acc-dim:rgba({rgb[0]},{rgb[1]},{rgb[2]},.14); }}"
        s = s[:anchor.end()] + rule + s[anchor.end():]
        have[g["acronymClass"]] = hx
        print(f"  {g['acronym']:14} {hx}  (hue {mid:.0f}°, widest gap was {gap:.0f}°)")

    if s != before:
        open(PAGE, "w", encoding="utf-8").write(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
