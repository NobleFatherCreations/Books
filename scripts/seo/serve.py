#!/usr/bin/env python3
"""Local preview that mirrors noblefathercreations.com's paths: /<book>/<page> -> library/<book>/<page>.html,
/<book> -> library/<book>/index.html, /playbook/... -> instruments/playbook/site/..., / -> hub. Port 8765."""
import http.server, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MAP = {"playbook": ROOT / "instruments/playbook/site", "shadowroot": ROOT / "instruments/shadowroot", "music": ROOT / "instruments/music"}
class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0].strip("/")
        if p == "": return str(ROOT / "hub/catalogue-redesign.html")
        if p in ("robots.txt", "sitemap.xml", "llms.txt"): return str(ROOT / "hub" / p)
        if "/" not in p and (ROOT / "hub" / (p + ".html")).exists(): return str(ROOT / "hub" / (p + ".html"))
        if "/" not in p and (ROOT / "hub" / p).is_file(): return str(ROOT / "hub" / p)
        if p.split("/")[0] in ("media", "f") and (ROOT / "hub" / p).is_file(): return str(ROOT / "hub" / p)
        parts = p.split("/")
        base = MAP.get(parts[0], ROOT / "library" / parts[0])
        rest = "/".join(parts[1:])
        if not rest: return str(base / "index.html")
        f = base / rest
        if f.is_file(): return str(f)
        return str(base / (rest + ".html"))
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8765), H).serve_forever()
