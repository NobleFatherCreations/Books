#!/usr/bin/env python3
"""The shelf jacket for the NFC guide's card on the hub.

Every other card on that page carries real cover art in a 1:1.42 portrait
face, so a typographic placeholder would read as the one unfinished thing on
the shelf. The guide already ships its own artwork -- the Dapper Dad figure
with the near-field waves, in assets/og-image.jpg -- but that is a 1200x630
share card whose left two-thirds is the wordmark. Cropped to a portrait face
it would keep the wordmark and lose the figure.

So this crops to the figure, fades it into the house ground, and sets the
title underneath in Fraunces, matching compose-jackets.py's layout language
(art field, scrim, title, rule, credit, seal) rather than inventing a second
one. Unlike the books, the credit line reads "NFC DIGITAL EXPERIENCES" -- this
is a manual, not a book Shae wrote as an author.

Writes _work/nfcguide-jacket.jpg and .b64; embed-guide-jacket.py puts the
payload into the hub card.
"""
import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = HERE / "_work"
FONTS = ROOT / "tools/fonts"
LOGO = ROOT / "design/brand/logo-noble-father.png"
SRC = ROOT / "workshop/nfcguide/assets/og-image.jpg"

W, H = 800, 1136              # 1:1.42, the shelf's own ratio
GROUND = (20, 16, 25)         # --ink, the house ground
CREAM = (236, 228, 214)       # --bone
BRASS = (201, 163, 91)        # --brass

# The figure sits in the right third of the share card. Cropped any wider than
# this and the wordmark's last letters bleed in behind the title as ghost
# serifs -- so the left edge starts past the "S" of CREATIONS, and the box is
# already the jacket's own 1.136 art-field ratio so nothing is re-cropped.
CROP = (690, 20, 1190, 460)


def art_field():
    img = Image.open(SRC).convert("RGB").crop(CROP)
    target = (W, int(H * 0.62))
    r = max(target[0] / img.width, target[1] / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - target[0]) // 2
    return img.crop((x, 0, x + target[0], target[1]))


def scrim(img):
    """Fade the art's lower edge into the ground so the type sits clean."""
    w, h = img.size
    grad = Image.new("L", (1, h), 0)
    start = int(h * 0.45)
    for y in range(h):
        grad.putpixel((0, y), 0 if y < start
                      else int(255 * (((y - start) / (h - start)) ** 1.6)))
    return Image.composite(Image.new("RGB", (w, h), GROUND), img,
                           grad.resize((w, h)))


def logo_mark(height, opacity=0.82):
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((int(height * logo.width / logo.height), height),
                       Image.LANCZOS)
    r, g, b, a = logo.split()
    return Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * opacity))))


def fitted(draw, text, font_path, start, room, **kw):
    size = start
    while size > 24:
        f = ImageFont.truetype(str(font_path), size)
        if draw.textlength(text, font=f) <= room:
            return f, size
        size -= 2
    return ImageFont.truetype(str(font_path), size), size


def build():
    display = FONTS / "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf"
    mono = FONTS / "spacemono/SpaceMono-Bold.ttf"

    jacket = Image.new("RGB", (W, H), GROUND)
    jacket.paste(scrim(art_field()), (0, 0))
    d = ImageDraw.Draw(jacket)

    y = int(H * 0.565)
    for line in ("How to", "Program", "NFC Tags"):
        f, size = fitted(d, line, display, 92, W - 112)
        d.text((56, y), line, font=f, fill=CREAM)
        y += int(size * 1.04)

    y += 22
    d.line([(56, y), (W - 56, y)], fill=BRASS, width=2)
    y += 26
    f, _ = fitted(d, "NFC DIGITAL EXPERIENCES", mono, 30, W - 260)
    d.text((56, y), "NFC DIGITAL EXPERIENCES", font=f, fill=BRASS)

    mark = logo_mark(150)
    jacket.paste(mark, (W - mark.width - 40, H - mark.height - 36), mark)

    WORK.mkdir(exist_ok=True)
    out = WORK / "nfcguide-jacket.jpg"
    jacket.save(out, "JPEG", quality=86, optimize=True)
    (WORK / "nfcguide-jacket.b64").write_text(
        base64.b64encode(out.read_bytes()).decode("ascii"))
    print(f"nfcguide jacket: {out.stat().st_size:,} bytes -> {out}")


if __name__ == "__main__":
    build()
