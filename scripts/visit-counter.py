#!/usr/bin/env python3
"""Put the small whole-site visit counter on every page (owner request 2026-11-20).

The counter is one self-contained block placed just before </body>. It asks
the homepage's own endpoint /api/visits (hub/netlify/functions/visits.mjs)
for the number. That endpoint reads the Cloudflare Web Analytics total. No
cookies and no storage. It only shows on noblefathercreations.com (the
endpoint lives there) and stays hidden if the number can't be fetched.

Idempotent: re-running replaces the block. Run it after ANY build that
rewrites a page, so live keeps matching the repo:

    python3 scripts/visit-counter.py --all            # every deployable page
    python3 scripts/visit-counter.py PATH [PATH...]   # files or folders
    python3 scripts/visit-counter.py --all --dry-run  # count only
    python3 scripts/visit-counter.py --all --remove   # take it off again
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- nf-visits -->", "<!-- /nf-visits -->"
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)

BLOCK = START + (
    '<p id="nf-visits" hidden style="all:initial;display:block;box-sizing:border-box;'
    'width:100%;margin:0;padding:24px 16px 32px;text-align:center;'
    'font:500 12px/1.5 system-ui,-apple-system,sans-serif;letter-spacing:.08em;'
    'color:inherit;opacity:.8;font-variant-numeric:tabular-nums"></p>'
    '<script>(function(){var e=document.getElementById("nf-visits");'
    'if(!e||!/(^|\\.)noblefathercreations\\.com$/.test(location.hostname))return;'
    'e.style.color=getComputedStyle(document.body).color;'
    'fetch("/api/visits").then(function(r){return r.ok?r.json():null})'
    '.then(function(d){if(d&&d.visits>0){e.textContent=d.visits.toLocaleString("en-US")'
    '+" visits to Noble Father Creations";e.hidden=false}}).catch(function(){})})();</script>'
) + END + "\n"


def deployable_paths():
    """Every page source the live site serves, from the sites.json registry."""
    d = json.loads((ROOT / "sites.json").read_text())
    paths = [ROOT / "hub/catalogue-redesign.html", ROOT / "hub/topics.html"]
    projects = d["projects"]
    entries = list(projects.values()) if isinstance(projects, dict) else list(projects)
    entries += [e for e in d.get("craftBusiness", []) if isinstance(e, dict)]
    for e in entries:
        if e.get("repoPath"):
            paths.append(ROOT / e["repoPath"])
    return paths


def html_files(paths):
    for p in paths:
        if p.is_dir():
            yield from sorted(f for f in p.rglob("*.html") if "_undeployed" not in f.parts)
        elif p.suffix == ".html" and p.exists():
            yield p


def apply(text, remove=False):
    text = BLOCK_RE.sub("", text)
    if remove:
        return text
    i = text.lower().rfind("</body>")
    return text[:i] + BLOCK + text[i:] if i != -1 else text + "\n" + BLOCK


def main(argv):
    dry, remove = "--dry-run" in argv, "--remove" in argv
    args = [a for a in argv if not a.startswith("--")]
    paths = deployable_paths() if "--all" in argv else [Path(a).resolve() for a in args]
    changed = total = 0
    for f in html_files(paths):
        raw = f.read_bytes()
        if b"<html" not in raw[:5000].lower() and b"</body>" not in raw.lower():
            continue  # a fragment, not a page
        total += 1
        old = raw.decode("utf-8")
        new = apply(old, remove)
        if new != old:
            changed += 1
            if not dry:
                f.write_bytes(new.encode("utf-8"))
    verb = "would change" if dry else "changed"
    print(f"{total} pages scanned, {changed} {verb}")


if __name__ == "__main__":
    main(sys.argv[1:])
