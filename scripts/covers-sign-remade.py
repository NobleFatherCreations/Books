# Signature into the empty bottom band of the three Artlist remakes (Fractal, Fracture, Sacred Divide).
# Run from the repo root: python3 scripts/covers-sign-remade.py
import cv2, numpy as np
SIG = 'tools/brand/signature-shae-stovell.png'
PICKS = {'07-fractal': ('fractal-b.png', (95, 175, 222)),    # BGR warm gold, like the title
         '08-fracture': ('fracture-a.png', (235, 235, 240)), # silver-white, like the title
         '09-faith': ('faith-b.png', (95, 175, 222))}
sig = cv2.imread(SIG, cv2.IMREAD_GRAYSCALE); a = 255 - sig
ys, xs = np.where(a > 40); a = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
for out, (src, color) in PICKS.items():
    im = cv2.imread('content/covers/remade/' + src); h, w = im.shape[:2]
    sw = int(w * 0.46); sh = int(sw * a.shape[0] / a.shape[1])
    aa = cv2.resize(a, (sw, sh), interpolation=cv2.INTER_AREA)
    aa = cv2.dilate(aa, np.ones((2, 2), np.uint8)).astype(np.float32) / 255
    aa = np.clip(aa * 1.35, 0, 1)
    ox = (w - sw) // 2; oy = h - sh - int(h * 0.022)
    roi = im[oy:oy+sh, ox:ox+sw].astype(np.float32)
    halo = cv2.GaussianBlur(aa, (0, 0), sw / 120)[..., None] * 0.45
    roi = roi * (1 - halo)
    roi = roi * (1 - aa[..., None]) + np.array(color, np.float32)[None, None, :] * aa[..., None]
    im[oy:oy+sh, ox:ox+sw] = np.clip(roi, 0, 255).astype(np.uint8)
    cv2.imwrite(f'content/covers/signed/{out}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 93])
    print(out, 'from', src)
