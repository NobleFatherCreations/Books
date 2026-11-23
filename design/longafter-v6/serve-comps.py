#!/usr/bin/env python3
"""Preview server for the v6 comps (port 8766). /design/... is served from the repo root; everything else
(/longafter/f/..., /longafter/cover.webp, links between pages) uses scripts/seo/serve.py's live-site mapping."""
import http.server, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0].strip("/")
        if p.startswith("design/"):
            return str(ROOT / p)
        parts = p.split("/")
        base = ROOT / "library" / parts[0]
        rest = "/".join(parts[1:])
        if not rest: return str(base / "index.html")
        f = base / rest
        return str(f if f.is_file() else base / (rest + ".html"))
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8766), H).serve_forever()
