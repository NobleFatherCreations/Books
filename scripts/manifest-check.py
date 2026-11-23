#!/usr/bin/env python3
"""Check that pages agree with site_manifest.json.  python3 scripts/manifest-check.py [--book longafter]

  decoder count   the manifest's decoder_tactics == the single tactics in content/decoder-v20/playbook_singles.json
                  == the count in the catalogue tagline (nf-catalogue.py) == every "N tactics" in the book's source and
                  built pages
  titles          the manifest's book title == the catalogue's title for that slug
  chapter counts  "N chapters" on the book's cover page == the chapters in its plan (reading chapters, Start and
                  Toolbox excluded)
Exit 1 on any disagreement. Read-only.
"""
import argparse, html, importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = json.loads((ROOT / "site_manifest.json").read_text())


def count_singles():
    d = json.loads((ROOT / "content/decoder-v20/playbook_singles.json").read_text())
    return sum(len(v) for v in d.values())


def catalogue():
    spec = importlib.util.spec_from_file_location("nf_catalogue", ROOT / "scripts/nf-catalogue.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {s: (html.unescape(t), html.unescape(g)) for s, t, g, _ in mod.CATALOGUE}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", action="append", help="limit to these books (default: every book in the manifest)")
    a = ap.parse_args()
    bad = []
    n = M["decoder_tactics"]
    singles = count_singles()
    if singles != n:
        bad.append(f"decoder: manifest says {n}, the Decoder data holds {singles}")
    cat = catalogue()
    m = re.search(r"(\d+) tactics", cat.get("playbook", ("", ""))[1])
    if not m or int(m.group(1)) != n:
        bad.append(f"catalogue tagline for the Decoder says {cat.get('playbook')}, manifest {n}")
    for slug, b in M["books"].items():
        if a.book and slug not in a.book:
            continue
        if cat.get(slug, ("",))[0] != b["title"]:
            bad.append(f"{slug}: catalogue title {cat.get(slug, ('missing',))[0]!r} != manifest {b['title']!r}")
        files = list((ROOT / b["source"]).glob("[0-9][0-9]-*.md")) + list((ROOT / b["built"]).glob("*.html"))
        for f in files:
            for k in set(re.findall(r"\b(\d+) (?:single )?tactics\b", f.read_text(encoding="utf-8", errors="ignore"))):
                if int(k) != n:
                    bad.append(f"{slug}: {f.relative_to(ROOT)} says {k} tactics, manifest {n}")
        plan = json.loads((ROOT / b["source"] / "plan.json").read_text())
        reading = sum(len(p["chapters"]) for p in plan["parts"] if p["id"] not in ("start", "tools"))
        cover = ROOT / b["built"] / "index.html"
        if cover.exists():
            for k in set(re.findall(r"\b(\d+) chapters\b", cover.read_text(encoding="utf-8"))):
                if int(k) != reading:
                    bad.append(f"{slug}: cover says {k} chapters, plan has {reading} reading chapters")
    for b in bad:
        print("DISAGREE", b)
    print(f"manifest check: {len(bad)} disagreement(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
