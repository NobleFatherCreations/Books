#!/usr/bin/env python3
"""Comparison sheets: comps/sheets/<page>.png, one row per region, A | B | C side by side (shots from shoot-comps.mjs)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
D = Path(__file__).resolve().parent / "comps"
ROWS = {"index": ["top", "choices"], "the-trauma-bond": ["top", "scene", "honest", "action"],
        "family-court-honestly": ["decoder", "honest"], "court-day-checklist": ["top", "sheet"],
        "abuse-or-a-hard-breakup": ["bridge"]}
NAMES = {"a": "A  Notes on the table", "b": "B  Margins", "c": "C  Horizon cards"}
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
big, small = ImageFont.truetype(F, 26), ImageFont.truetype(F, 20)
W, H, G, TOP, LAB = 375, 812, 24, 70, 34   # each shot at half its 2x size
(D / "sheets").mkdir(exist_ok=True)
for page, rows in ROWS.items():
    img = Image.new("RGB", (G + 3 * (W + G), TOP + len(rows) * (LAB + H + G)), "#e9e6ee")
    d = ImageDraw.Draw(img)
    d.text((G, 20), f"The Long After v6 comps: {page}", font=big, fill="#1a1527")
    for r, region in enumerate(rows):
        y = TOP + r * (LAB + H + G)
        for c, v in enumerate("abc"):
            x = G + c * (W + G)
            d.text((x, y + 6), f"{NAMES[v]}  ·  {region}", font=small, fill="#3a3346")
            shot = Image.open(D / "shots" / f"{v}-{page}-{region}.png").convert("RGB").resize((W, H), Image.LANCZOS)
            img.paste(shot, (x, y + LAB))
    img.save(D / "sheets" / f"{page}.png", optimize=True)
    print("sheet", page, img.size)
