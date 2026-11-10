#!/usr/bin/env python3
"""Local preview of everything under /fractal2, with the same addresses as production.
  python3 design/fractal2/serve.py [port=8802]
/fractal2            -> library/fractal2/site/fractal2.html
/fractal2/<path>     -> library/fractal2/site/fractal2/<path>(.html)
/fractal/..., /playbook/..., / -> the published books and Decoder from this repo (so cross-links can be checked)
Extensionless pages are served the way Netlify serves them. Unknown paths return 404 (never a silent index)."""
import http.server, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "library/fractal2/site"
MAP = {"playbook": ROOT / "instruments/playbook/site"}


class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0].strip("/")
        parts = p.split("/")
        if parts[0] == "fractal2":
            f = SITE / p
            if f.is_file():
                return str(f)
            return str(SITE / (p + ".html"))
        if p == "":
            return str(ROOT / "hub/catalogue-redesign.html")
        base = MAP.get(parts[0], ROOT / "library" / parts[0])
        rest = "/".join(parts[1:])
        if not rest:
            return str(base / "index.html")
        f = base / rest
        return str(f if f.is_file() else base / (rest + ".html"))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8802
    http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
