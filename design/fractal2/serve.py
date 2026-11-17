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

    def send_head(self):                       # byte ranges, as Netlify serves them (the score is seeked by the audio element)
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        if not rng or not rng.startswith("bytes=") or not Path(path).is_file():
            return super().send_head()
        size = Path(path).stat().st_size; a, _, b = rng[6:].split(",")[0].partition("-")
        a = int(a) if a else max(0, size - int(b)); b = min(size - 1, int(b)) if (b and a is not None and rng[6:].split("-")[0]) else size - 1
        if a >= size:
            self.send_error(416); return None
        f = open(path, "rb"); f.seek(a); self._left = b - a + 1
        self.send_response(206); self.send_header("Content-Type", self.guess_type(path)); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (a, b, size)); self.send_header("Content-Length", str(self._left)); self.end_headers()
        return f

    def copyfile(self, src, dst):
        left = getattr(self, "_left", None)
        if left is None:
            return super().copyfile(src, dst)
        while left > 0:
            buf = src.read(min(65536, left))
            if not buf:
                break
            dst.write(buf); left -= len(buf)
        self._left = None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8802
    http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
