#!/usr/bin/env python3
"""Composite Artlist cover art into each book's cover-mark slot:
crop to the 640:280 slot ratio, add 'Shae Stovell' author credit,
and a subtle watermark of the user's actual logo."""
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COVERS = Path(__file__).resolve().parent / "_work"
FONTS = Path(__file__).resolve().parents[2] / "tools/fonts"
LOGO = Path(__file__).resolve().parents[2] / "design/brand/logo-noble-father.png"

TARGET_W, TARGET_H = 1600, 700  # 640:280 ratio, high-res for retina @560px display width

# per-book display font (matches each book's own established typeface) + accent color
BOOKS = {
    "longafter": dict(font=FONTS/"instrumentserif/InstrumentSerif-Regular.ttf", accent=(232,164,138)),   # coral
    "silence":   dict(font=FONTS/"youngserif/YoungSerif-Regular.ttf",           accent=(214,224,230)),   # steel/mist
    "atwill":    dict(font=FONTS/"bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf", accent=(200,222,255)), # blue
    "repair":    dict(font=FONTS/"anton/Anton-Regular.ttf",                     accent=(214,196,150)),   # wax/brass
    "slowtake":  dict(font=FONTS/"outfit/Outfit[wght].ttf",                     accent=(226,214,164)),   # gold
}

def crop_to_ratio(img, ratio):
    w, h = img.size
    target_w = h * ratio
    if target_w <= w:
        new_w = int(round(target_w))
        x0 = (w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, h))
    else:
        target_h = w / ratio
        new_h = int(round(target_h))
        y0 = (h - new_h) // 2
        img = img.crop((0, y0, w, y0 + new_h))
    return img


def add_bottom_vignette(img):
    w, h = img.size
    grad = Image.new("L", (1, h), 0)
    band = int(h * 0.42)
    for y in range(h):
        if y < h - band:
            grad.putpixel((0, y), 0)
        else:
            t = (y - (h - band)) / band
            grad.putpixel((0, y), int(150 * (t ** 1.4)))
    grad = grad.resize((w, h))
    dark = Image.new("RGB", (w, h), (10, 8, 10))
    img = Image.composite(dark, img, grad)
    return img


def paste_logo(img, height, margin, opacity=0.8):
    """The user's actual logo, scaled small and set semi-transparent,
    bottom-left -- opposite the author credit, so the two never collide."""
    logo = Image.open(LOGO).convert("RGBA")
    w = int(height * logo.width / logo.height)
    logo = logo.resize((w, height), Image.LANCZOS)
    if opacity < 1:
        r, g, b, a = logo.split()
        a = a.point(lambda v: int(v * opacity))
        logo = Image.merge("RGBA", (r, g, b, a))
    img.paste(logo, (margin, img.size[1] - height - margin), logo)
    return img


def compose(name, cfg):
    src = Image.open(COVERS/f"{name}.png").convert("RGB")
    src = crop_to_ratio(src, TARGET_W/TARGET_H)
    src = src.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    src = add_bottom_vignette(src)

    draw = ImageDraw.Draw(src)
    accent = cfg["accent"]
    size = int(TARGET_H * 0.075)
    try:
        f = ImageFont.truetype(str(cfg["font"]), size)
    except Exception:
        f = ImageFont.load_default()

    label = "SHAE STOVELL"
    bbox = draw.textbbox((0,0), label, font=f)
    tw = bbox[2]-bbox[0]
    x = TARGET_W - tw - 56
    y = TARGET_H - (bbox[3]-bbox[1]) - 44 - bbox[1]
    # soft shadow for legibility over art
    draw.text((x+2, y+2), label, font=f, fill=(0,0,0,140))
    draw.text((x, y), label, font=f, fill=accent)

    # small rule above the name
    draw.line([(x, y-14), (x+tw, y-14)], fill=accent, width=1)

    src = paste_logo(src, height=int(TARGET_H*0.155), margin=int(TARGET_H*0.055))

    out = COVERS/f"{name}-final.jpg"
    src.save(out, "JPEG", quality=86, optimize=True)
    b64 = base64.b64encode(out.read_bytes()).decode("ascii")
    (COVERS/f"{name}-final.b64").write_text(b64)
    print(name, "->", out, out.stat().st_size, "bytes,", len(b64), "b64 chars")


if __name__ == "__main__":
    for name, cfg in BOOKS.items():
        compose(name, cfg)
