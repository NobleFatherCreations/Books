#!/usr/bin/env python3
"""Portrait book jackets for the hub's Library shelf.

The shelf renders each cover in a 1:1.42 portrait face with object-fit:cover.
Dropping the 21:9 banners in there would crop to the middle third and throw
away both the author credit and the seal, so the art is re-laid out as an
actual jacket: art as the field, scrim, title, author, seal.
"""
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = Path(__file__).resolve().parent / "_work"
FONTS = Path(__file__).resolve().parents[2] / "tools/fonts"
LOGO = Path(__file__).resolve().parents[2] / "design/brand/logo-noble-father.png"

W, H = 800, 1136          # 1:1.42, the shelf's own ratio
CREAM = (242, 230, 210)

BOOKS = {
    "longafter": dict(
        font=FONTS / "instrumentserif/InstrumentSerif-Regular.ttf",
        title=["The", "Long", "After"], accent=(232, 164, 138),
        ground=(30, 22, 38), upper=True),
    "silence": dict(
        font=FONTS / "youngserif/YoungSerif-Regular.ttf",
        title=["The", "Silence"], accent=(214, 224, 230),
        ground=(26, 30, 34), upper=False),
    "atwill": dict(
        font=FONTS / "bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf",
        title=["At", "Will"], accent=(200, 222, 255),
        ground=(18, 24, 32), upper=False),
    "repair": dict(
        font=FONTS / "anton/Anton-Regular.ttf",
        title=["The", "Repair"], accent=(214, 196, 150),
        ground=(24, 23, 21), upper=True),
    "slowtake": dict(
        font=FONTS / "outfit/Outfit[wght].ttf",
        title=["The", "Slow", "Take"], accent=(226, 214, 164),
        ground=(24, 21, 14), upper=False),
}


def fit_art(name):
    """Cover-crop the source art to the jacket's upper field."""
    img = Image.open(S / f"{name}.png").convert("RGB")
    target = (W, int(H * 0.62))
    r = max(target[0] / img.width, target[1] / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - target[0]) // 2
    y = (img.height - target[1]) // 2
    return img.crop((x, y, x + target[0], y + target[1]))


def scrim(img, ground):
    """Fade the art's lower edge into the jacket ground so type sits clean."""
    w, h = img.size
    grad = Image.new("L", (1, h), 0)
    start = int(h * 0.45)
    for y in range(h):
        if y < start:
            grad.putpixel((0, y), 0)
        else:
            t = (y - start) / (h - start)
            grad.putpixel((0, y), int(255 * (t ** 1.6)))
    grad = grad.resize((w, h))
    return Image.composite(Image.new("RGB", (w, h), ground), img, grad)


def logo_mark(height, opacity=0.82):
    """The user's actual logo, scaled small and set semi-transparent."""
    logo = Image.open(LOGO).convert("RGBA")
    w = int(height * logo.width / logo.height)
    logo = logo.resize((w, height), Image.LANCZOS)
    r, g, b, a = logo.split()
    a = a.point(lambda v: int(v * opacity))
    return Image.merge("RGBA", (r, g, b, a))


def build(name, cfg):
    jacket = Image.new("RGB", (W, H), cfg["ground"])
    art = scrim(fit_art(name), cfg["ground"])
    jacket.paste(art, (0, 0))
    d = ImageDraw.Draw(jacket)

    # title, set to fill the width, line by line
    lines = [l.upper() for l in cfg["title"]] if cfg["upper"] else cfg["title"]
    y = int(H * 0.575)
    for line in lines:
        size = 96
        while size > 24:
            f = ImageFont.truetype(str(cfg["font"]), size)
            if d.textlength(line, font=f) <= W - 112:
                break
            size -= 2
        f = ImageFont.truetype(str(cfg["font"]), size)
        d.text((56, y), line, font=f, fill=CREAM)
        y += int(size * 1.02)

    # rule + author
    y += 22
    d.line([(56, y), (W - 56, y)], fill=cfg["accent"], width=2)
    y += 24
    fa = ImageFont.truetype(str(cfg["font"]), 40)
    d.text((56, y), "SHAE STOVELL", font=fa, fill=cfg["accent"])

    mark = logo_mark(150)
    jacket.paste(mark, (W - mark.width - 40, H - mark.height - 36), mark)

    out = S / f"{name}-jacket.jpg"
    jacket.save(out, "JPEG", quality=86, optimize=True)
    (S / f"{name}-jacket.b64").write_text(
        base64.b64encode(out.read_bytes()).decode("ascii"))
    print(f"{name}: {out.stat().st_size} bytes")


if __name__ == "__main__":
    for n, c in BOOKS.items():
        build(n, c)
