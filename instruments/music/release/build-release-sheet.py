#!/usr/bin/env python3
"""Generate MASTER-RELEASE-SHEET.csv from instruments/music/MANIFEST.json.

Pre-fills what the manifest already knows (file, duration, Suno id/date,
shelf) and proposes a store-safe commercial title + flags. Columns a human
must decide (keeper, release slot, ISRC, dates) are left blank on purpose.
"""
import csv, json, re, collections, pathlib

HERE = pathlib.Path(__file__).parent
M = json.load(open(HERE.parent / "MANIFEST.json"))

GENRE = {  # proposal only; DistroKid wants one primary + optional secondary
    "reckoning": ("Hip-Hop/Rap", "Alternative"),
    "descent": ("Alternative", "Electronic"),
    "frequency": ("Electronic", "Christian & Gospel"),
    "dragons": ("Soundtrack", "Electronic"),
    "festival": ("Hip-Hop/Rap", "Dance"),
    "tender": ("Singer/Songwriter", "Pop"),
}
EMOJI = re.compile("[\U0001F000-\U0001FFFF☀-➿‍️]")
VARIANT = re.compile(r"\s*(·\s*Version\s*\d+|\((?:Remastered[^)]*)\))", re.I)
EXPLICIT = re.compile(r"fuck|bitch|ass\b|dick|orgy|horny|whippit|contact high|puff pass|high freak|goose juice", re.I)
TRADEMARK = re.compile(r"jedi|hufflepuff|potter|chuck(?:e|ee)? ?chees", re.I)

def commercial(title):
    t = EMOJI.sub("", title)
    t = VARIANT.sub("", t)
    t = re.sub(r"\^", "i", t)          # Sw^ng -> Swing; stores reject stylised glyphs
    t = re.sub(r"\s+\)", ")", t)
    return re.sub(r"\s{2,}", " ", t).strip(" ·")

def base(title):
    return re.sub(r"\s*\(.*\)$", "", commercial(title)).lower()

groups = collections.Counter(base(t["title"]) for t in M["tracks"])
gid = {b: f"G{i:03d}" for i, b in enumerate(sorted(b for b, n in groups.items() if n > 1), 1)}

cols = ["System File Name", "Drive ID", "Library Title (as-is)", "Commercial Track Title",
        "Version Field", "Duplicate Group", "Keeper (Y/N)", "Shelf", "Proposed Release",
        "Release Format (Single/EP/LP)", "Track #", "Primary Genre", "Secondary Genre",
        "Explicit (Y/N)", "Flags", "Duration (m:ss)", "Suno Created", "Suno ID",
        "Suno Plan At Creation (verify)", "WAV Re-download", "Mixea Master Status",
        "Integrated LUFS", "True Peak dBTP", "Lyricist", "AI Disclosure",
        "ISRC", "UPC", "Distribution Date", "Release Date", "DistroKid Status", "Notes"]

rows = []
for t in sorted(M["tracks"], key=lambda t: (t["shelf"], t["title"].lower())):
    title, flags = t["title"], []
    ct = commercial(title)
    m = re.search(r"Version\s*(\d+)", title) or re.search(r"\((Remastered[^)]*)\)", title)
    if EMOJI.search(title): flags.append("emoji-in-title")
    if "Remastered" in title: flags.append("'Remastered' not allowed unless prior release")
    if re.search(r"Version\s*\d", title): flags.append("version-suffix")
    if TRADEMARK.search(title): flags.append("trademark/IP risk - retitle")
    if t["duration"] > 480: flags.append(">8 min")
    if base(title) in gid: flags.append("multiple takes - choose one")
    s = round(t["duration"])
    rows.append({
        "System File Name": t["file"], "Drive ID": t["driveId"],
        "Library Title (as-is)": title, "Commercial Track Title": ct,
        "Version Field": "", "Duplicate Group": gid.get(base(title), ""),
        "Keeper (Y/N)": "" if base(title) in gid else "Y",
        "Shelf": t["shelfName"], "Proposed Release": t["shelfName"],
        "Primary Genre": GENRE[t["shelf"]][0], "Secondary Genre": GENRE[t["shelf"]][1],
        "Explicit (Y/N)": "Y?" if EXPLICIT.search(title) else "listen",
        "Flags": "; ".join(flags), "Duration (m:ss)": f"{s//60}:{s%60:02d}",
        "Suno Created": t.get("created", ""), "Suno ID": t.get("sunoId", ""),
        "WAV Re-download": "TODO", "Mixea Master Status": "Not started",
        "AI Disclosure": "Music generated with Suno; lyrics by artist (confirm)",
        "DistroKid Status": "Not uploaded",
    })

# Tracks in Drive that post-date the manifest (2026-08-12 build).
rows.append({c: "" for c in cols} | {
    "System File Name": "the-fourth-position.mp3", "Drive ID": "1lmvDeUgmMzF-3Mup6IWJT8RGKIjO6ptK",
    "Library Title (as-is)": "The Fourth Position", "Commercial Track Title": "The Fourth Position",
    "Keeper (Y/N)": "Y", "Shelf": "(unshelved - added 2026-09-17)", "Explicit (Y/N)": "listen",
    "WAV Re-download": "TODO", "Mixea Master Status": "Not started", "DistroKid Status": "Not uploaded",
    "Notes": "Not in the Listening Room manifest yet"})

out = HERE / "MASTER-RELEASE-SHEET.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, "") for c in cols})
print(f"{len(rows)} rows, {len(gid)} duplicate groups, "
      f"{sum(1 for r in rows if r['Keeper (Y/N)'] == 'Y')} unambiguous keepers -> {out}")
