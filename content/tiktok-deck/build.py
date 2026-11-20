#!/usr/bin/env python3
"""Build the TikTok book deck: slides (PNG) -> full MP4 + one MP4 per book.

    python3 content/tiktok-deck/build.py            # everything
    python3 content/tiktok-deck/build.py --no-video # slides only

Content lives in books.py. Covers in covers/ (new, Artlist) and
covers-existing/ (from the catalogue PDF). Output in build/ (git-ignored).
"""
import json, math, os, shutil, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
sys.path.insert(0, HERE)
from books import BOOKS, INTRO, OUTRO, DONATE  # noqa: E402

FPS = 30
COVER_SECS = 4.0
FADE = 0.4


def prep_images():
    img = os.path.join(BUILD, "img")
    os.makedirs(img, exist_ok=True)
    out = []
    for b in BOOKS:
        src = os.path.join(HERE, b["cover"])
        im = Image.open(src).convert("RGB")
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        elif im.width < 1080:  # upscale low-res PDF covers once, cleanly
            im = im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS)
        dst = os.path.join(img, b["slug"] + ".jpg")
        im.save(dst, quality=92)
        out.append({**b, "coverUrl": "file://" + dst, "coverW": im.width, "coverH": im.height})
    brand = os.path.join(img, "brand.jpg")
    Image.open(os.path.join(HERE, "covers-existing/brand-mark.jpg")).convert("RGB").save(brand, quality=90)
    return {"books": out, "brandUrl": "file://" + brand, "intro": INTRO, "outro": OUTRO, "donate": DONATE}


def secs(m):
    if m["kind"] == "cover":
        return COVER_SECS
    if m["kind"] == "title":
        return 4.5
    if m["kind"] == "card":
        return round(min(10.0, max(4.5, m["words"] / 2.7 + 1.5)), 2)
    return round(min(18.0, max(5.0, m["words"] / 2.7 + 2.0)), 2)


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def segment(png, dur, dst, fade_in, fade_out):
    vf = ["format=yuv420p"]
    if fade_in:
        vf.insert(0, f"fade=t=in:st=0:d={FADE}")
    if fade_out:
        vf.insert(0, f"fade=t=out:st={dur - FADE:.2f}:d={FADE}")
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur}", "-i", png,
         "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "veryfast", "-threads", "2", "-crf", "18",
         "-tune", "stillimage", "-r", str(FPS), "-pix_fmt", "yuv420p", dst])


def concat(parts, dst):
    lst = dst + ".txt"
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    # silent AAC track: TikTok and some players reject video-only files
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", dst])
    os.remove(lst)


def main():
    shutil.rmtree(BUILD, ignore_errors=True)
    os.makedirs(BUILD)
    with open(os.path.join(BUILD, "books.json"), "w") as f:
        json.dump(prep_images(), f)
    subprocess.run(["node", os.path.join(HERE, "render.mjs"), HERE], check=True)
    if "--no-video" in sys.argv:
        return
    man = json.load(open(os.path.join(BUILD, "manifest.json")))
    segdir = os.path.join(BUILD, "seg")
    os.makedirs(segdir)
    segs, total = [], 0.0
    for i, m in enumerate(man):
        d = secs(m)
        nxt = man[i + 1] if i + 1 < len(man) else None
        fade_in = m["kind"] == "cover" or i == 0
        fade_out = nxt is None or nxt["kind"] == "cover"
        dst = os.path.join(segdir, m["file"].replace(".png", ".mp4"))
        segment(os.path.join(BUILD, "slides", m["file"]), d, dst, fade_in, fade_out)
        m["secs"] = d
        total += d
        segs.append(dst)
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    concat(segs, os.path.join(out, "noble-father-books-full.mp4"))
    # one video per book (cover through its last info slide)
    order = [b["slug"] for b in BOOKS]
    for n, slug in enumerate(order, 1):
        parts = [s for s, m in zip(segs, man) if m["slug"] == slug]
        concat(parts, os.path.join(out, f"{n:02d}-{slug}.mp4"))
    json.dump(man, open(os.path.join(BUILD, "manifest.json"), "w"), indent=1)
    print(f"slides {len(man)}  total {total/60:.1f} min")


if __name__ == "__main__":
    main()
