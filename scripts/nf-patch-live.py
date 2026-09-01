#!/usr/bin/env python3
"""Patch the canonical catalogue into the LIVE copy of each existing site.

Why not just deploy the repo copy: the live sites have moved ahead of this
repo. Eight of them carry Cloudflare Web Analytics added 2026-08-15, the
Listening Room is live at v4 against v2 here, the Portals carry CSS fixes
this repo never received, and the reaction map's live file is a different
build entirely. Deploying the repo copies would silently strip all of that.

So instead: fetch what is actually live, swap only the catalogue and its
volume count, and send that back. Nothing else about the live page changes.

Usage:  nf-patch-live.py fetch     -- download live -> staging, patch, report
        nf-patch-live.py verify    -- re-fetch and confirm the catalogue landed
"""
import re
import subprocess
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
cat = importlib.import_module("nf-catalogue")

STAGE = Path("/tmp/claude-0/-home-user/a0ec5e44-ffe5-5bba-b9bd-3cb1a2115366/scratchpad/live")

# netlify site name, the catalogue slug this page IS (None = not in the list)
SITES = [
    ("wook-in-sheeps-clothing", "wook",       "460c07e8-463e-4213-8e14-9711cb430741"),
    ("playgroundprotector",     "children",   "90b0a06d-1e11-4302-9292-f2e2780b195a"),
    ("sovereign-woman",         "feminine",   "7683f8ed-03f4-4829-8fd4-f6affea18a16"),
    ("fractures",               "fracture",   "8939c138-e34a-433c-8c01-9af5ebbd75b2"),
    ("thefractal",              "fractal",    "e94ed486-0392-4045-86c8-b9c3a26b911a"),
    ("noblenfcseals",           "press",      None),
    ("nfcportals",              "portals",    None),
    ("noblemusic",              "music",      "05683d2c-cb07-43cb-8e2c-d8cd380c0287"),
    ("nobleshadows",            "shadowroot", "b5ff07f1-2ee6-4c6a-9591-a1e6ef7baa91"),
    ("noblereactionmap",        None,         "d38d9339-7bc1-448c-a17c-c1183798cfab"),
]


def fetch(site, dest, tries=5):
    """Some of these files are multi-megabyte and the egress proxy drops the
    odd transfer, so retry rather than half-patching the set."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    for n in range(1, tries + 1):
        r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "300",
                            "-o", str(dest), f"https://{site}.netlify.app/"])
        if r.returncode == 0 and dest.exists() and dest.stat().st_size > 1000:
            return dest.read_text(errors="surrogateescape")
        print(f"  {site}: fetch attempt {n} failed (rc={r.returncode}), retrying")
        time.sleep(2 ** n)
    raise SystemExit(f"{site}: could not fetch after {tries} attempts")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    for site, here, _sid in SITES:
        out = STAGE / site / "index.html"
        html = fetch(site, out)

        if mode == "verify":
            rows = len(re.findall(r'class="nf-row', html))
            foot = re.search(r'<div class="nf-panel-foot">([^<]*)</div>', html)
            newb = len(re.findall(r'noblefathercreations\.com/(?:longafter|silence|'
                                  r'atwill|repair|slowtake)', html))
            keep = "cloudflareinsights" in html
            print(f"{site:26s} rows={rows:2d} new-links={newb} "
                  f"analytics-intact={keep} foot={foot.group(1)[:42] if foot else 'NONE'!r}")
            continue

        before = len(html)
        had_analytics = "cloudflareinsights" in html
        patched = cat.retoc(html, here)
        # the swap must not disturb anything else on the page
        assert ("cloudflareinsights" in patched) == had_analytics, \
            f"{site}: analytics state changed"
        out.write_text(patched, errors="surrogateescape")
        rows = len(re.findall(r'class="nf-row', patched))
        print(f"{site:26s} {before:>9} -> {len(patched):>9}  rows={rows} "
              f"here={here} analytics={had_analytics}")


if __name__ == "__main__":
    main()
