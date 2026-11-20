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
from books import BOOKS, INTRO, OUTRO, DONATE, ABOUT  # noqa: E402

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
    return {"books": out, "brandUrl": "file://" + brand, "intro": INTRO, "outro": OUTRO, "donate": DONATE, "about": ABOUT}


BPM = 96
BAR = 4 * 60 / BPM          # 2.5 s: every slide lasts a whole number of bars
TARGET_BARS = 180           # 7:30 total, to sit under the Suno song
CLIP_BARS = {"opener": 2, "end": 5, "signature": 3}


def plan_bars(man):
    """Give every slide a whole number of bars so book changes land on bar lines.
    Fixed: card 2 (about 3), cover 1, title 1. Info slides share what is left,
    2 bars each, with the shortest ones dropped to 1 bar until the total fits."""
    for m in man:
        m["bars"] = {"cover": 1, "title": 1, "card": 3 if m["slug"] == "about" else 2}.get(m["kind"], 2)
    budget = TARGET_BARS - sum(CLIP_BARS.values())
    over = sum(m["bars"] for m in man) - budget
    for m in sorted([m for m in man if m["kind"] == "info"], key=lambda m: m["words"]):
        if over <= 0:
            break
        m["bars"] = 1
        over -= 1
    assert over == 0, f"bar plan off by {over}"


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


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-threads", "2", "-crf", "18", "-r", str(FPS),
       "-pix_fmt", "yuv420p", "-video_track_timescale", "15360",
       "-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "128k"]
ASSETS = os.path.join(HERE, "assets")


def segment(png, dur, dst, fade_in, fade_out):
    vf = ["format=yuv420p"]
    if fade_in:
        vf.insert(0, f"fade=t=in:st=0:d={FADE}")
    if fade_out:
        vf.insert(0, f"fade=t=out:st={dur - FADE:.2f}:d={FADE}")
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur}", "-i", png,
         "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=44100:cl=stereo",
         "-vf", ",".join(vf), "-tune", "stillimage", *ENC, "-shortest", dst])


def clip(src, dst, fade_in=True, fade_out=True, keep_audio=True, length=None):
    """Normalise an owner video to 1080x1920/30fps with an audio track."""
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", src]).strip())
    pad = 0.0
    if length:
        pad = max(0.0, length - dur)
        dur = length
    vf = "scale=1080:1920:force_original_aspect_ratio=decrease:flags=lanczos,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30"
    if pad:
        vf += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
    if fade_in:
        vf += f",fade=t=in:st=0:d={FADE}"
    if fade_out:
        vf += f",fade=t=out:st={dur - FADE - 0.05:.2f}:d={FADE}"
    if keep_audio:
        run(["ffmpeg", "-y", "-i", src, "-vf", vf, "-af", f"aresample=44100,apad", *ENC, "-t", f"{dur:.3f}", dst])
    else:
        run(["ffmpeg", "-y", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
             "-map", "0:v", "-map", "1:a", "-vf", vf, *ENC, "-shortest", dst])
    return dur


def signature(bg_png, dst):
    """Owner's signature video, 3x speed, white paper removed, drawn in gold over the end card."""
    src = os.path.join(ASSETS, "signature-draw.mp4")
    fc = ("[1:v]setpts=PTS/3,scale=960:-2,format=gray,negate,format=gray[a];"
          "color=c=0xF4D58A:s=960x540:r=30[g];[g][a]alphamerge[s];"
          "[0:v][s]overlay=x=60:y=380:shortest=1,tpad=stop_mode=clone:stop_duration=2.5,"
          f"fade=t=in:st=0:d={FADE},fade=t=out:st=6.9:d=0.6,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", bg_png, "-i", src,
         "-f", "lavfi", "-t", "7.5", "-i", "anullsrc=r=44100:cl=stereo",
         "-filter_complex", fc, "-map", "[v]", "-map", "2:a", *ENC, "-t", "7.5", dst])
    return 7.5


def concat(parts, dst):
    lst = dst + ".txt"
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", dst])
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
    sigbg = [m for m in man if m["kind"] == "sigbg"]
    poster = [m for m in man if m["kind"] == "poster"]
    man = [m for m in man if m["kind"] not in ("sigbg", "poster")]
    plan_bars(man)
    for i, m in enumerate(man):
        d = m["bars"] * BAR
        nxt = man[i + 1] if i + 1 < len(man) else None
        fade_in = m["kind"] == "cover" or i == 0
        fade_out = nxt is None or nxt["kind"] == "cover"
        dst = os.path.join(segdir, m["file"].replace(".png", ".mp4"))
        segment(os.path.join(BUILD, "slides", m["file"]), d, dst, fade_in, fade_out)
        m["secs"] = d
        total += d
        segs.append(dst)
    # owner videos: angel opens, the 12 s film and the signature close
    opener = os.path.join(segdir, "000-angel.mp4")
    total += clip(os.path.join(ASSETS, "angel-6s.mov"), opener, length=CLIP_BARS["opener"] * BAR)
    ender = os.path.join(segdir, "998-end.mp4")
    total += clip(os.path.join(ASSETS, "end-12s.mp4"), ender, length=CLIP_BARS["end"] * BAR)
    sig = os.path.join(segdir, "999-signature.mp4")
    total += signature(os.path.join(BUILD, "slides", sigbg[0]["file"]), sig)
    full = [opener] + segs + [ender, sig]
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    if poster:
        shutil.copy(os.path.join(BUILD, "slides", poster[0]["file"]), os.path.join(out, "tiktok-cover-photo.png"))
    concat(full, os.path.join(out, "noble-father-books-full.mp4"))
    # one video per book (cover through its last info slide)
    order = [b["slug"] for b in BOOKS]
    for n, slug in enumerate(order, 1):
        parts = [s for s, m in zip(segs, man) if m["slug"] == slug]
        concat(parts, os.path.join(out, f"{n:02d}-{slug}.mp4"))
    json.dump(man, open(os.path.join(BUILD, "manifest.json"), "w"), indent=1)
    print(f"slides {len(man)}  total {total/60:.1f} min")


if __name__ == "__main__":
    main()
