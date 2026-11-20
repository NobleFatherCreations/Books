#!/usr/bin/env python3
"""Site-wide page tags (owner decisions 2026-11-20).

1. EVERY page carries the Cloudflare Web Analytics beacon (the one sanctioned
   external script). Pages that lack it get it just before </body>.
2. ONLY the homepage (hub/catalogue-redesign.html) carries the small visit
   counter. It reads /api/visits (hub/netlify/functions/visits.mjs, the
   Cloudflare total). No cookies, no storage, and hidden if the number can't
   be fetched. Any counter found on another page is removed.

Idempotent. Run it after ANY build that rewrites a page, so live keeps
matching the repo:

    python3 scripts/visit-counter.py --all            # every deployable page
    python3 scripts/visit-counter.py PATH [PATH...]   # files or folders
    python3 scripts/visit-counter.py --all --dry-run  # report only
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOMEPAGE = (ROOT / "hub/catalogue-redesign.html").resolve()

BEACON = ("<script defer type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
          "data-cf-beacon='{\"token\": \"c8d1aea530814aea8c7a92baa2accef3\"}'></script>")

START, END = "<!-- nf-visits -->", "<!-- /nf-visits -->"
COUNTER_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
COUNTER = START + (
    '<p id="nf-visits" hidden style="all:initial;display:block;box-sizing:border-box;'
    'width:100%;margin:0;padding:24px 16px 112px;text-align:center;'
    'font:500 12px/1.5 system-ui,-apple-system,sans-serif;letter-spacing:.08em;'
    'color:inherit;opacity:.8;font-variant-numeric:tabular-nums"></p>'
    '<script>(function(){var e=document.getElementById("nf-visits");'
    'if(!e||!/(^|\\.)noblefathercreations\\.com$/.test(location.hostname))return;'
    'e.style.color=getComputedStyle(document.body).color;'
    'fetch("/api/visits").then(function(r){return r.ok?r.json():null})'
    '.then(function(d){if(d&&d.visits>0){e.textContent=d.visits.toLocaleString("en-US")'
    '+" visits to Noble Father Creations";e.hidden=false}}).catch(function(){})})();</script>'
) + END + "\n"

SKIP_PARTS = {"_undeployed", "og-src"}  # og-src = social-card render sources, not served pages


def deployable_paths():
    """Every page source the live site serves, from the sites.json registry."""
    d = json.loads((ROOT / "sites.json").read_text())
    paths = [HOMEPAGE, ROOT / "hub/topics.html"]
    projects = d["projects"]
    entries = list(projects.values()) if isinstance(projects, dict) else list(projects)
    entries += [e for e in d.get("craftBusiness", []) if isinstance(e, dict)]
    paths += [ROOT / e["repoPath"] for e in entries if e.get("repoPath")]
    return paths


def html_files(paths):
    for p in paths:
        if p.is_dir():
            yield from sorted(f for f in p.rglob("*.html") if not SKIP_PARTS & set(f.parts))
        elif p.suffix == ".html" and p.exists():
            yield p


def insert_before_body(text, block):
    i = text.lower().rfind("</body>")
    return text[:i] + block + text[i:] if i != -1 else text + "\n" + block


def apply(text, is_home):
    text = COUNTER_RE.sub("", text)
    if "cloudflareinsights.com/beacon" not in text:
        text = insert_before_body(text, BEACON + "\n")
    if is_home:
        text = insert_before_body(text, COUNTER)
    return text


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    paths = deployable_paths() if "--all" in argv else [Path(a).resolve() for a in args]
    changed = []
    total = 0
    for f in html_files(paths):
        raw = f.read_bytes()
        if b"<html" not in raw[:5000].lower() and b"</body>" not in raw.lower():
            continue  # a fragment, not a page
        total += 1
        old = raw.decode("utf-8")
        new = apply(old, f.resolve() == HOMEPAGE)
        if new != old:
            changed.append(f.relative_to(ROOT))
            if not dry:
                f.write_bytes(new.encode("utf-8"))
    print(f"{total} pages scanned, {len(changed)} {'would change' if dry else 'changed'}")
    for c in changed:
        print("  ", c)


if __name__ == "__main__":
    main(sys.argv[1:])
