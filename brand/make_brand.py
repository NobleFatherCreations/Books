#!/usr/bin/env python3
"""Brand kit builder: the Noble Father Creations character holding the Fractal as a wax seal.
Keeps the original header untouched everywhere except the seal medallion, where the Fractal disc is set inside the gold wax rim.
   python3 brand/make_brand.py        -> brand/out/*"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source'); OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)

header = Image.open(os.path.join(SRC, 'nfc-header-original.png')).convert('RGB')          # 5504 x 3072
W, H = header.size
# seal medallion measured on the 5504-wide original (see build notes)
CX, CY, R = 4096, 1351, 232

def fractal_disc(path, r, centre=(1024, 996), crop_r=905, feather=0.035):
    """Circular crop of the Fractal artwork (outer gold ring included) with a soft edge, as an RGBA disc of radius r."""
    im = Image.open(path).convert('RGB')
    cx, cy = centre
    sq = im.crop((cx - crop_r, cy - crop_r, cx + crop_r, cy + crop_r)).resize((2 * r, 2 * r), Image.LANCZOS)
    mask = Image.new('L', (2 * r, 2 * r), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(1, int(r * feather))))
    out = sq.convert('RGBA'); out.putalpha(mask)
    return out

def relief(img):
    """Give the flat dial the wax's lighting: top-left highlight on the raised rim, bottom-right shade, inner shadow, a wax-gold tint."""
    r = R
    box = (CX - r, CY - r, CX + r, CY + r)
    base = img.crop(box).convert('RGB')
    S = 2 * r
    yy, xx = np.mgrid[0:S, 0:S]
    dx = (xx - r) / r; dy = (yy - r) / r; d = np.sqrt(dx * dx + dy * dy)
    ndl = (-dx * 0.55 - dy * 0.65)
    edge = np.clip((d - 0.50) / 0.50, 0, 1)
    hi = np.clip(ndl, 0, 1) * edge
    sh = np.clip(-ndl, 0, 1) * edge
    arr = np.asarray(base).astype(float)
    arr = arr * 0.94 + np.array([205, 150, 62]) * 0.06                       # wax-gold tint: the dial is pressed into gold, not printed
    arr = arr * (1 - 0.50 * sh[..., None]) + 255 * 0.20 * hi[..., None] * np.array([1.0, 0.92, 0.62])
    spec = np.exp(-(((dx + 0.42) / 0.30) ** 2 + ((dy + 0.46) / 0.16) ** 2)) * 0.10   # soft specular streak
    arr = arr + 255 * spec[..., None] * np.array([1.0, 0.95, 0.75])
    ring = np.clip((d - 0.88) / 0.12, 0, 1)
    arr = arr * (1 - 0.60 * ring[..., None])                                   # inner shadow where the dial meets the wax rim
    out = Image.fromarray(np.clip(arr, 0, 255).astype('uint8'), 'RGB')
    m = Image.fromarray((np.clip(1.0 - (d - 0.985) / 0.03, 0, 1) * 255).astype('uint8'), 'L')
    img = img.copy(); img.paste(out, box[:2], m)
    return img

def set_seal(base, disc_path, name):
    img = base.copy().convert('RGBA')
    r = R
    disc = fractal_disc(disc_path, r)
    # dark inner shadow ring so the disc sits INSIDE the wax rim, then the disc, then a warm rim light
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    ds.ellipse((CX - r - 14, CY - r - 14, CX + r + 14, CY + r + 14), fill=(40, 18, 6, 235))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, shadow)
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0)); layer.paste(disc, (CX - r, CY - r), disc)
    img = Image.alpha_composite(img, layer)
    img = relief(img.convert('RGB')).convert('RGBA')
    rim = Image.new('RGBA', img.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(rim)
    dr.ellipse((CX - r, CY - r, CX + r, CY + r), outline=(255, 214, 120, 150), width=6)
    rim = rim.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, rim)
    # soft golden bloom around the seal (screen blend) so it reads as the light source
    bloom = Image.new('RGB', img.size, (0, 0, 0)); db = ImageDraw.Draw(bloom)
    db.ellipse((CX - r - 40, CY - r - 40, CX + r + 40, CY + r + 40), fill=(120, 80, 20))
    bloom = bloom.filter(ImageFilter.GaussianBlur(70))
    hole = Image.new('L', img.size, 255); ImageDraw.Draw(hole).ellipse((CX - r + 4, CY - r + 4, CX + r - 4, CY + r - 4), fill=0)
    bloom = ImageChops.multiply(bloom, Image.merge('RGB', [hole.filter(ImageFilter.GaussianBlur(5))] * 3))
    out = ImageChops.screen(img.convert('RGB'), bloom)
    out.save(os.path.join(OUT, name + '-full.png'))
    return out

variants = {
    'fractal-seal-clean': os.path.join(SRC, 'fractal-rings-only.png'),
    'fractal-seal-30': os.path.join(SRC, 'fractal-30-techniques.jpg'),
}
for name, p in variants.items():
    full = set_seal(header, p, name)
    w = 3000; h = round(H * w / W)
    full.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, name + '-3000.jpg'), quality=90)
    full.resize((2000, round(H * 2000 / W)), Image.LANCZOS).save(os.path.join(OUT, name + '-2000.jpg'), quality=88)
print(sorted(os.listdir(OUT)))

# ---------------------------------------------------------------- kit derived from the primary
primary = Image.open(os.path.join(OUT, 'fractal-seal-30-full.png')).convert('RGB')
# primary header
primary.resize((2000, round(H * 2000 / W)), Image.LANCZOS).save(os.path.join(OUT, 'header-primary-2000.jpg'), quality=90)
# social card 1200x630 (crop the 2000-wide header to the 1.905 ratio)
p2 = primary.resize((2000, round(H * 2000 / W)), Image.LANCZOS)
ch = round(2000 / 1.905); y0 = (p2.size[1] - ch) // 2
p2.crop((0, y0, 2000, y0 + ch)).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, 'og-card-1200x630.jpg'), quality=90)
# square avatar: the character holding the seal (no wordmark fragments)
sq = primary.crop((3220, 330, 4840, 1950)).resize((1080, 1080), Image.LANCZOS)
sq.save(os.path.join(OUT, 'avatar-character-seal-1080.jpg'), quality=90)
# emblem: clean ring artwork as a transparent circle for small sizes
emb = fractal_disc(os.path.join(SRC, 'fractal-rings-only.png'), 512, feather=0.012)
emb.save(os.path.join(OUT, 'emblem-512.png'))
for s in (256, 192, 128, 64, 32):
    emb.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, f'emblem-{s}.png'))
emb.resize((64, 64), Image.LANCZOS).save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
# the 30-technique dial as a transparent circle (large uses: intro, covers, wax seal product)
dial = fractal_disc(os.path.join(SRC, 'fractal-30-techniques.jpg'), 900, feather=0.012)
dial.save(os.path.join(OUT, 'dial-30-900.png'))
print('kit:', sorted(os.listdir(OUT)))
