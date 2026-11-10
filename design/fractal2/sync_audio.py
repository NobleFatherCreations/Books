#!/usr/bin/env python3
"""Turn the owner's recorded takes into the page's narration.   python3 design/fractal2/sync_audio.py <folder-with-takes>

In:  take-00.wav ... take-11.wav (or .m4a/.mp3), named as in content/fractal2/RECORDING-GUIDE.md
     and, beside each, a transcript with word times: take-NN.words.json = [{"w": "word", "t": seconds}, ...]
     (from any speech-to-text that returns word timestamps; nothing is sent anywhere by this script).
Out: library/fractal2/site/fractal2/_a/au/intro.mp3              one file, loudness-normalised, 64 kbps mono
     library/fractal2/site/fractal2/_a/au/intro.sync.json        when each line of the page starts
     library/fractal2/site/fractal2/_a/au/intro.vtt              captions taken from the page text (not from the transcript)
     library/fractal2/site/fractal2/_a/au/intro.sync.recorded.json   marker so the builder stops writing the placeholder

How lines are found: the narration script is the source of truth. For every script line, the transcript words are
searched for its first few words with a fuzzy match, in order, never going backwards. A line that cannot be found
is placed evenly between its neighbours and listed in the report, so a missed line never breaks the page.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AU = ROOT / "library/fractal2/site/fractal2/_a/au"
SCRIPT = ROOT / "content/fractal2/narration-script.md"


def norm(s):
    return re.sub(r"[^a-z0-9 ]+", "", s.lower().replace("’", "'")).split()


def script_takes():
    takes, cur = [], None
    for line in SCRIPT.read_text().split("\n"):
        m = re.match(r"## Take (\d+)", line)
        if m:
            cur = {"take": int(m.group(1)), "lines": []}
            takes.append(cur)
            continue
        m = re.match(r"`(\d+)` (.*)", line)
        if m and cur is not None:
            text = re.sub(r"\[(?:breath|pause [\d.]+)\]", "", m.group(2)).replace("**", "").strip()
            cur["lines"].append({"n": int(m.group(1)), "text": text})
    return takes


def align(lines, words):
    """-> [(n, start_seconds or None)]"""
    toks = [norm(w["w"]) for w in words]
    toks = [t[0] if t else "" for t in toks]
    pos, out = 0, []
    for ln in lines:
        key = norm(ln["text"])[:6]
        best, best_i = 0.0, None
        for i in range(pos, min(len(toks), pos + 400)):
            r = difflib.SequenceMatcher(None, key, toks[i:i + len(key)]).ratio()
            if r > best:
                best, best_i = r, i
            if r > 0.92:
                break
        if best_i is not None and best >= 0.6:
            out.append((ln["n"], words[best_i]["t"]))
            pos = best_i + max(1, len(key) // 2)
        else:
            out.append((ln["n"], None))
    return out


def fill(times, total):
    """Place unfound lines evenly between found neighbours."""
    t = [x for _, x in times]
    i = 0
    while i < len(t):
        if t[i] is None:
            j = i
            while j < len(t) and t[j] is None:
                j += 1
            a = t[i - 1] if i else 0.0
            b = t[j] if j < len(t) else total
            for k in range(i, j):
                t[k] = a + (b - a) * (k - i + 1) / (j - i + 1)
            i = j
        else:
            i += 1
    return [(n, round(x, 2)) for (n, _), x in zip(times, t)]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def vtt_time(x):
    return "%02d:%02d:%06.3f" % (x // 3600, x % 3600 // 60, x % 60)


def main(folder):
    folder = Path(folder)
    takes = script_takes()
    offset, units, missing, parts = 0.0, [], [], []
    for tk in takes:
        audio = next((p for ext in ("wav", "m4a", "mp3", "flac") for p in [folder / ("take-%02d.%s" % (tk["take"], ext))] if p.exists()), None)
        if audio is None:
            sys.exit("missing audio for take %02d" % tk["take"])
        wj = folder / ("take-%02d.words.json" % tk["take"])
        if not wj.exists():
            sys.exit("missing word timings %s" % wj.name)
        d = dur(audio)
        al = align(tk["lines"], json.loads(wj.read_text()))
        missing += [n for n, x in al if x is None]
        for n, x in fill(al, d):
            units.append({"n": n, "t": round(offset + x, 2)})
        parts.append(audio)
        offset += d + 1.2          # 1.2 s of room tone between parts
    AU.mkdir(parents=True, exist_ok=True)
    lst = folder / "_concat.txt"
    gap = folder / "_gap.wav"
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "1.2", str(gap)])
    tmp = []
    for i, p in enumerate(parts):
        w = folder / ("_n%02d.wav" % i)
        subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-i", str(p), "-ac", "1", "-ar", "44100", "-af", "highpass=f=70,loudnorm=I=-18:TP=-2:LRA=9", str(w)])
        tmp += [w, gap]
    lst.write_text("".join("file '%s'\n" % t.resolve() for t in tmp[:-1]))
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-b:a", "64k", str(AU / "intro.mp3")])
    total = dur(AU / "intro.mp3")
    (AU / "intro.sync.json").write_text(json.dumps({"placeholder": False, "duration": round(total, 1), "units": units}, separators=(",", ":")))
    (AU / "intro.sync.recorded.json").write_text(json.dumps({"takes": len(parts), "missing": missing}))
    text = {l["n"]: l["text"] for tk in takes for l in tk["lines"]}
    cues = ["WEBVTT", ""]
    for i, u in enumerate(units):
        end = units[i + 1]["t"] if i + 1 < len(units) else total
        cues += ["%s --> %s" % (vtt_time(u["t"]), vtt_time(max(u["t"] + 0.5, end - 0.05))), text[u["n"]], ""]
    (AU / "intro.vtt").write_text("\n".join(cues))
    for t in tmp[:-1:2] + [gap, lst]:
        Path(t).unlink(missing_ok=True)
    print("narration: %d lines, %.0f s, %d lines placed by estimate %s" % (len(units), total, len(missing), missing[:12]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))
