#!/usr/bin/env python3
"""Put the one canonical catalogue (scripts/nf-catalogue.py, 21 entries) into EVERY file that carries the seal menu,
outputs and sources alike, so no page is missing a book. Idempotent. Run after adding anything to the catalogue,
then redeploy the sites whose files changed.   python3 scripts/nf-catalogue-sweep.py [--dry]"""
import importlib.util, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cat", R / "scripts/nf-catalogue.py"); CAT = importlib.util.module_from_spec(spec); spec.loader.exec_module(CAT)
HERE = {"library": None, "playbook": "playbook", "shadowroot": "shadowroot", "music": "music", "nfcguide": "nfc/",
        "seals": "press", "portals": "portals", "casting": "resin", "fractal2": "fractal"}
FILES = [p for root in ("library", "instruments", "workshop", "other", "design/decoder-v10") for p in (R / root).rglob("*.html")]
changed = {}
for f in FILES:
    rel = f.relative_to(R).as_posix()
    if "_undeployed" in rel or "node_modules" in rel or "/qa" in rel:
        continue
    h = f.read_text(encoding="utf-8", errors="surrogateescape")
    if 'class="nf-toc"' not in h:
        continue
    parts = rel.split("/")
    site = parts[1] if parts[0] in ("library", "instruments", "workshop") else ("playbook" if parts[0] == "design" else None)
    here = HERE.get(site, site if parts[0] == "library" else None)
    out = CAT.retoc(h, here)
    if out != h:
        changed.setdefault(site or parts[0], 0)
        changed[site or parts[0]] += 1
        if "--dry" not in sys.argv:
            f.write_text(out, encoding="utf-8", errors="surrogateescape")
for k, v in sorted(changed.items()):
    print(f"{k:12} {v} files updated")
