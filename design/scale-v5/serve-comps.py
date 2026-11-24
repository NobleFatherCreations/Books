#!/usr/bin/env python3
"""Serve The Weighing comps: /scale/* -> library/scale/*, /tools/*, /design/* from the repo. http://127.0.0.1:8766/design/scale-v5/comps/a/index.html"""
import http.server, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0]
        if p.startswith("/scale"):
            rest = p[len("/scale"):].lstrip("/") or "index.html"
            f = ROOT / "library/scale" / rest
            if not f.suffix and (f.with_suffix(".html")).exists(): f = f.with_suffix(".html")
            return str(f)
        return str(ROOT / p.lstrip("/"))
    def log_message(self, *a): pass
os.chdir(ROOT); http.server.ThreadingHTTPServer(("127.0.0.1", 8766), H).serve_forever()
