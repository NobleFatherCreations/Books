#!/usr/bin/env python3
"""Record the 2026-09-01 launch round in sites.json.

Run with --deployed only once the deploys have actually succeeded, so the
ledger never claims something is live before it is.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = ROOT / "sites.json"
DATE = "2026-09-01"

NEW = {
    "longafter": ("noble-the-long-after", "6061de1c-d0fb-4410-8168-33f487da80fa"),
    "silence":   ("noble-the-silence",    "e01cef5e-2c2c-4361-8c35-28605049513f"),
    "atwill":    ("noble-at-will",        "42391fff-a788-4132-bc6a-222a9e8c965a"),
    "repair":    ("noble-the-repair",     "e91359be-0cf1-4390-8ce6-9660252b28cb"),
    "slowtake":  ("noble-the-slow-take",  "2ab4e8f6-f7da-41bc-a5dc-d6856b6f913f"),
}

LAUNCH = ("Published. Bespoke cover art with Shae Stovell as author and the NF "
          "seal, and THE HOUSE catalogue added so this book reaches every other "
          "one on the site.")

# every page that carries the catalogue drawer and therefore changed this round
RETOC = ["wook", "children", "feminine", "fracture", "fractal", "press",
         "portals", "music", "shadowroot"]
RETOC_NOTE = ("The Catalogue now lists all twenty volumes, including the five "
              "new books. It had drifted to different lengths on different "
              "pages.")


def bump(p, summary):
    cur = p.get("version") or "v0"
    n = int(str(cur).lstrip("v") or 0) + 1
    p["version"] = f"v{n}"
    p.setdefault("changelog", []).insert(
        0, {"date": DATE, "version": f"v{n}", "summary": summary})


def main():
    deployed = "--deployed" in sys.argv        # the 5 books + the hub are live
    retoc_done = "--retoc-done" in sys.argv    # the older sites got the new nav
    d = json.loads(SITES.read_text())

    for p in d["projects"]:
        slug = p.get("slug")

        if slug in NEW:
            name, sid = NEW[slug]
            p["netlifySite"] = name
            p["netlifySiteId"] = sid
            p["deploySource"] = "cli (via @netlify/mcp deploy-site)"
            p["url"] = f"https://noblefathercreations.com/{slug}"
            p["netlifyUrl"] = f"https://{name}.netlify.app/"
            p["houseTabLeak"] = {"found": False, "checkedAt": DATE,
                                 "note": "Shared catalogue drawer installed."}
            if deployed:
                p["status"] = "live"
                bump(p, LAUNCH)
            else:
                p["status"] = ("Netlify site created, deploy pending. Repo copy "
                               "is finished and verified.")

        elif slug in RETOC and retoc_done:
            bump(p, RETOC_NOTE)

    if deployed:
        hub = d["hub"]
        cur = int(str(hub.get("version", "v0")).lstrip("v") or 0) + 1
        hub["version"] = f"v{cur}"
        hub.setdefault("changelog", []).insert(0, {
            "date": DATE, "version": f"v{cur}",
            "summary": ("Added five new books to the Library -- The Long After, "
                        "The Silence, At Will, The Repair and The Slow Take -- "
                        "each with its own cover art, and corrected the book "
                        "count in the header and the intro tour. The Catalogue "
                        "now lists all twenty volumes on every page.")})

    d["updated"] = DATE
    SITES.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print("sites.json updated;", f"deployed={deployed} retoc_done={retoc_done}")


if __name__ == "__main__":
    main()
