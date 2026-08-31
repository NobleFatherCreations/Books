#!/usr/bin/env python3
"""Self-host a book's typefaces as subset, base64 @font-face rules.

House rule: no external requests, ever. The four new books shipped with
system font stacks ('Iowan Old Style', Palatino, Georgia, serif), so the
typography the author sees on a Mac is not what most readers get -- on
Windows and Android it falls through to whatever the default serif is.
Self-hosting is the only way the design is the same for everyone.

Two things keep the cost honest:

  * Variable fonts are instanced before subsetting -- optical size pinned,
    weight kept as a range. On Newsreader that is 76 KB -> 21 KB for the
    same glyphs, because the unused variation machinery dominates a small
    subset. Each family is then declared once with `font-weight: <range>`.
    MEMORY.md records a page that inlined one family three times at
    discrete weights with byte-identical blobs; a range cannot do that.
  * The subset is the characters the book actually renders, read out of
    its own chapter bodies, plus what the interface adds.

Usage:
  embed-fonts.py <book.html> <spec> [<spec> ...]
  spec = family:role:path[:italic][:opsz=N][:wght=A-B]
  role = serif | mono | display
"""
import base64, io, re, sys, pathlib
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

book = pathlib.Path(sys.argv[1])
html = book.read_text(encoding="utf-8")

js = html.split('<script id="book-js">')[1].split("</script>")[0]
text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), js)
text = re.sub(r"&(#\d+|[a-z]+);", " ", text)
chars = set(text) | set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    " .,;:!?'\"()[]{}/\\|-_=+*&%#@") | set("‘’“”—–…·→←°§")
unicodes = sorted(ord(c) for c in chars if 31 < ord(c) < 0x3000)

def build(spec):
    parts = spec.split(":")
    role, path = parts[0], parts[1]
    italic = "italic" in parts
    opsz = next((float(p.split("=")[1]) for p in parts if p.startswith("opsz=")), None)
    wght = next((p.split("=")[1] for p in parts if p.startswith("wght=")), "400-700")
    lo, hi = (int(x) for x in wght.split("-"))

    f = TTFont(path)
    is_var = "fvar" in f
    if is_var:
        axes = {}
        if opsz is not None:
            axes["opsz"] = opsz
        axes["wght"] = (lo, hi) if lo != hi else lo
        f = instantiateVariableFont(f, axes, updateFontNames=False)
    if is_var:
        # a lazily-loaded gvar can raise KeyError mid-subset on some fonts
        # (HankenGrotesk: 'space'). Round-tripping materialises it.
        tmp = io.BytesIO(); f.save(tmp); tmp.seek(0)
        f = TTFont(tmp, lazy=False)
    o = subset.Options()
    o.flavor = "woff2"
    o.layout_features = ["kern", "liga", "clig", "calt"]
    # notdef_outline conflicts with gvar subsetting on instanced variable fonts
    s = subset.Subsetter(options=o)
    s.populate(unicodes=unicodes)
    s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    raw = buf.getvalue()
    name = {"serif":"BookSerif","mono":"BookMono","display":"BookDisplay"}[role]
    weight = f"{lo} {hi}" if (is_var and lo != hi) else str(lo)
    rule = (f"@font-face{{font-family:'{name}';font-style:{'italic' if italic else 'normal'};"
            f"font-weight:{weight};font-display:swap;"
            f"src:url(data:font/woff2;base64,{base64.b64encode(raw).decode()}) format('woff2')}}")
    print(f"    {pathlib.Path(path).name:42} {len(raw)/1024:6.1f} KB  "
          f"{'variable ' + weight if is_var and lo != hi else 'static ' + weight}")
    return rule, len(raw)

rules, total = [], 0
for spec in sys.argv[2:]:
    r, n = build(spec); rules.append(r); total += n

block = ('<style id="embedded-fonts">/* Self-hosted, subset to this book’s own '
         'character set. Zero requests, works offline. */\n' + "\n".join(rules) + "\n</style>")
if 'id="embedded-fonts"' in html:
    html = re.sub(r'<style id="embedded-fonts">[\s\S]*?</style>', block, html, count=1)
else:
    html = html.replace("</head>", block + "\n</head>", 1)
book.write_text(html, encoding="utf-8")
print(f"    -> {total/1024:.1f} KB of font, {len(unicodes)} glyphs, page {len(html)/1024:.0f} KB")
