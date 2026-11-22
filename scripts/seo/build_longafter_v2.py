#!/usr/bin/env python3
"""The Long After, 2nd edition: build the book from content/longafter-v2 (plan.json + NN-*.md).

Run:  python3 scripts/seo/build_longafter_v2.py
Writes library/longafter/: index.html (cover, "Where are you right now?", contents), one page per chapter and tool,
contents.html, search.html (offline search, nothing sent anywhere), all.html (the whole book on one page, for offline
reading and print), redirect pages for retired addresses, sitemap.xml. Old #/c/N, #/help, #/card and #/limits links
are forwarded to their new pages. Design: "Dusk to first light" (DESIGN-STATE.md section 3.3 A): every part has its own
sky, from deep dusk in Part I to first light in Part XI; reading text sits on one quiet night page.
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
import importlib.util as _iu

ROOT = S.ROOT
SRC = ROOT / "content/longafter-v2"
OUT = ROOT / "library/longafter"
BASE = "/longafter"
URL = S.DOMAIN + BASE
PLAN = json.loads((SRC / "plan.json").read_text())
OLD = json.loads((SRC / "old_routes.json").read_text())
CH = {c["slug"]: c for c in PLAN["chapters"]}
ORDER = [c["slug"] for c in PLAN["chapters"]]
PARTS = {p["id"]: p for p in PLAN["parts"]}
ROMAN = {"i": "I", "ii": "II", "iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII", "viii": "VIII",
         "ix": "IX", "x": "X", "xi": "XI"}

spec = _iu.spec_from_file_location("nf_catalogue", ROOT / "scripts/nf-catalogue.py")
CAT = _iu.module_from_spec(spec); spec.loader.exec_module(CAT)

BOOK = {
    "slug": "longafter", "title": "The Long After", "version": "v5",
    "description": ("A free guide to life after leaving an abusive relationship: post-separation abuse, safety, contact, "
                    "courts, children, feelings and rebuilding."),
    "genre": ["Self-help", "Psychology", "Domestic abuse recovery"],
    "about": ["Post-separation abuse", "Leaving an abusive relationship", "Coercive control", "Hoovering",
              "Trauma bond", "Co-parenting with an abusive ex", "Litigation abuse", "Narcissistic abuse recovery"],
    "keywords": ["post-separation abuse", "after leaving an abusive relationship", "hoovering", "trauma bond",
                 "co-parenting with a narcissist", "grey rock", "litigation abuse", "free book"],
    "notice_short": ("Information, not legal, medical or therapeutic advice. If you are in danger, contact your local "
                     "emergency services."),
}

# Dusk to first light: [sky top, sky bottom, accent] per part
SKY = {
    "start": ("#1b1430", "#3a2346", "#e0957a"), "i": ("#1b1430", "#3a2346", "#e0957a"),
    "ii": ("#19142e", "#40274d", "#e39a7d"), "iii": ("#171630", "#3d2c57", "#e6a17f"),
    "iv": ("#151a33", "#35345e", "#e8a983"), "v": ("#141c36", "#2e3c64", "#eab089"),
    "vi": ("#13203a", "#2d4668", "#ecb68f"), "vii": ("#142540", "#365170", "#eebd96"),
    "viii": ("#162a45", "#495b75", "#efc39c"), "ix": ("#1a2e48", "#5e6479", "#f0c9a2"),
    "x": ("#20334c", "#66586e", "#f1cea7"), "xi": ("#283a52", "#7a5a64", "#f3d4ad"),
    "tools": ("#1d1a2a", "#36324a", "#e0b48e"),
}


def parse():
    out = {}
    for f in sorted(SRC.glob("[0-9][0-9]-*.md")):
        for block in re.split(r"^=== ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            slug, rest = block.split("\n", 1)
            head, _, body = rest.partition("\n---\n")
            out[slug.strip()] = {"meta": dict(re.findall(r"^(\w+):\s*(.+)$", head, re.M)), "body": body.strip()}
    return out


# ---------------------------------------------------------------- Markdown (the small subset the book uses)
def href(target):
    if target.startswith("ch:"):
        slug, _, frag = target[3:].partition("#")
        return f"{BASE}/{slug}" + (f"#{frag}" if frag else "")
    return target


def inline(t):
    t = html.escape(smart(t), quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(href(m.group(2)))}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def smart(t):
    t = re.sub(r'(^|[\s(\[>*_])"', "\\1\u201c", t)
    t = t.replace('"', "\u201d")
    t = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", t)
    t = re.sub(r"(^|[\s(\[>])'", "\\1\u2018", t)
    t = t.replace("'", "\u2019")
    return t


TEL_PAGES = {"if-youre-not-safe-right-now", "find-help", "the-card", "safety-plan-worksheet", "when-its-more-than-aftermath",
             "pocket-card-words-you-can-use"}
LONG_TEL = re.compile(r"(?<![\w-])(1-800-\d{3}-\d{4}|0\d{2,3}(?: \d{2,4}){2,3}|01 \d{3} \d{4}|1800 \d{3} \d{3}|13 11 14|116 123)(?![\w-])")
SHORT_TEL = re.compile(r"(?<![\w.,-])(911|999|000|112|988|211)(?![\w-])")
SMS = re.compile(r"text START to (88788)")


def telify(h):
    """Tap-to-call on the crisis pages: numbers in text (never inside a tag or an existing link) become tel:/sms: links."""
    out, in_a = [], 0
    for part in re.split(r"(<[^>]+>)", h):
        if part.startswith("<"):
            in_a += 1 if re.match(r"<a[\s>]", part) else (-1 if part.startswith("</a") else 0)
            out.append(part); continue
        if in_a:
            out.append(part); continue
        part = SMS.sub(lambda m: f'text START to <a class="tel" href="sms:{m.group(1)}?body=START">{m.group(1)}</a>', part)
        bits = re.split(r"(<a [^>]+>.*?</a>)", part)
        for i, b in enumerate(bits):
            if b.startswith("<a "):
                continue
            b = LONG_TEL.sub(lambda m: f'<a class="tel" href="tel:{re.sub(r"[^0-9]", "", m.group(1))}">{m.group(1)}</a>', b)
            segs = re.split(r"(<a [^>]+>.*?</a>)", b)
            bits[i] = "".join(x if x.startswith("<a ") else SHORT_TEL.sub(lambda m: f'<a class="tel" href="tel:{m.group(1)}">{m.group(1)}</a>', x) for x in segs)
        out.append("".join(bits))
    return "".join(out)


def md(body):
    lines = body.split("\n")
    out, i, used = [], 0, set()
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith("## "):
            text = ln[3:].strip()
            hid = S.slugify(text, 60)
            while hid in used:
                hid += "-2"
            used.add(hid)
            out.append(f'<h2 id="{hid}">{inline(text)}</h2>'); i += 1; continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:].strip())}</h3>"); i += 1; continue
        if ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].lstrip()); i += 1
            paras, cur = [], []
            for b in block:
                if b.strip():
                    cur.append(b)
                else:
                    if cur: paras.append(" ".join(cur)); cur = []
            if cur: paras.append(" ".join(cur))
            cls = "say" if any("**Say" in p for p in paras) else "pull"
            out.append(f'<blockquote class="{cls}">' + "".join(f"<p>{inline(p)}</p>" for p in paras) + "</blockquote>")
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body_rows = rows[0], [r for r in rows[1:] if not set("".join(r)) <= set("-: ")]
            t = '<div class="tbl"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body_rows)
            out.append(t + "</tbody></table></div>"); continue
        if re.match(r"^\s*- ", ln) or ln.startswith("☐"):
            items = []
            while i < len(lines) and (re.match(r"^\s*- ", lines[i]) or lines[i].startswith("☐")):
                items.append(lines[i]); i += 1
            lis = "".join(f'<li class="check">{inline(x)}</li>' if x.startswith("☐") else f"<li>{inline(re.sub(r'^\s*- ', '', x))}</li>" for x in items)
            out.append(f'<ul{" class=\"checks\"" if items[0].startswith("☐") else ""}>{lis}</ul>'); continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(## |### |>|\||\s*- |\d+\. |☐)", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def split_sources(body):
    main, _, src = body.partition("\n## Sources")
    return main.strip(), src.strip()


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


# ---------------------------------------------------------------- page frame
FONTS = (f"@font-face{{font-family:'BookDisplay';font-weight:400;font-style:normal;font-display:swap;src:url({BASE}/f/bookdisplay-400-normal.woff2) format('woff2')}}"
         f"@font-face{{font-family:'BookSerif';font-weight:400 700;font-style:normal;font-display:swap;src:url({BASE}/f/bookserif-400-700-normal.woff2) format('woff2')}}"
         f"@font-face{{font-family:'BookSerif';font-weight:400 700;font-style:italic;font-display:swap;src:url({BASE}/f/bookserif-400-700-italic.woff2) format('woff2')}}")

CSS = """
:root{color-scheme:dark;--night:#110e19;--panel:#1a1527;--panel2:#221c33;--fg:#efe9f4;--fg2:#bdb3cc;--line:#2f2842;
--disp:'BookDisplay','Iowan Old Style',Georgia,serif;--body:'BookSerif','Iowan Old Style',Georgia,serif;--sans:var(--body)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-padding-top:76px}
body{margin:0;background:var(--night);color:var(--fg);font:400 1.15rem/1.68 var(--body);text-rendering:optimizeLegibility}
a{color:var(--acc);text-underline-offset:.2em;text-decoration-thickness:1px}a:hover{color:#fff}
:focus-visible{outline:3px solid var(--acc);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:0;background:#fff;color:#000;padding:12px 16px;z-index:10000}.skip:focus{left:8px;top:8px}
.bar{position:sticky;top:0;z-index:9000;display:flex;align-items:center;gap:6px;padding:6px 88px 6px 12px;min-height:60px;
background:rgba(17,14,25,.94);backdrop-filter:saturate(1.2) blur(8px);border-bottom:1px solid var(--line);font-family:var(--sans)}
.bar .home{font:400 1.2rem/1 var(--disp);color:var(--fg);text-decoration:none;margin-right:auto;padding:12px 4px;white-space:nowrap}
.bar a.b,.bar button{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 12px;border-radius:10px;
border:1px solid var(--line);background:transparent;color:var(--fg);font:600 .95rem/1 var(--sans);text-decoration:none;cursor:pointer}
.bar .leave{background:#7a2730;border-color:#a33a45;color:#fff;min-width:84px}
.bar .leave:hover{background:#962f3a}
.nf-seal{top:8px!important;bottom:auto!important;right:10px!important;width:46px!important;height:46px!important;font-size:15px!important}
.sky{background:linear-gradient(180deg,var(--s1),var(--s2));position:relative;padding:28px 16px 64px;overflow:hidden}
.sky::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:linear-gradient(90deg,transparent,var(--acc),transparent);opacity:.7}
.sky::before{content:"";position:absolute;left:50%;bottom:-48px;width:calc(360px + var(--dawn) * 900px);max-width:180vw;height:96px;transform:translateX(-50%);
background:radial-gradient(closest-side,color-mix(in srgb,var(--acc) 45%,transparent),transparent);opacity:calc(.3 + var(--dawn) * .6);pointer-events:none}
.sky .in,.wrap{max-width:44rem;margin:0 auto;position:relative}
.loc{font:italic 400 .98rem/1.4 var(--sans);color:#f5ecef;margin:0 0 12px}
.loc a{color:inherit;display:inline-block;padding:13px 0;margin:-13px 0}
h1{font:400 clamp(2.1rem,1.5rem + 3vw,3.1rem)/1.1 var(--disp);margin:0 0 12px;color:#fff;text-wrap:balance}
.q{font-style:italic;color:#f1e9ee;margin:0;font-size:1.15rem;max-width:36rem}
main{padding:0 16px 64px}
.short{max-width:44rem;margin:-18px auto 32px;position:relative;background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--acc);
border-radius:12px;padding:16px 20px}
.short .lab{font:700 .78rem/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:0 0 8px}
.short p{margin:0;font-size:1.2rem;line-height:1.6}
article{max-width:44rem;margin:0 auto}
article h2{font:400 1.65rem/1.25 var(--disp);margin:2.2em 0 .5em;color:#fff;text-wrap:balance;scroll-margin-top:76px}
article h3{font:700 1.15rem/1.3 var(--body);margin:1.6em 0 .4em}
article p,article li{max-width:66ch}
article p{margin:0 0 1em}
article ul,article ol{padding-left:1.3em;margin:0 0 1.2em}article li{margin:.35em 0}
ul.checks{list-style:none;padding:0}ul.checks li{padding:.25em 0;border-bottom:1px solid var(--line)}
blockquote{margin:1.6em 0;padding:0}
blockquote.pull{border-left:3px solid var(--acc);padding:4px 0 4px 20px;font:italic 400 1.3rem/1.5 var(--body);color:#fff}
blockquote.pull p{margin:0 0 .5em}
blockquote.say{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:14px 18px}
blockquote.say p{margin:.3em 0}blockquote.say strong{color:var(--acc);font-family:var(--sans);font-size:.85rem;letter-spacing:.04em;text-transform:uppercase}
.tbl{overflow-x:auto;margin:1.4em 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:1rem;line-height:1.45}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
th{font:700 .85rem/1.3 var(--sans);letter-spacing:.03em;color:var(--fg2);background:var(--panel)}
details.sources{max-width:44rem;margin:2.5em auto 0;border-top:1px solid var(--line);padding-top:12px;font-size:1rem}
details.sources summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font:600 1rem/1 var(--sans);color:var(--fg2)}
details.sources ul{color:var(--fg2);padding-left:1.2em}details.sources li{margin:.4em 0}
.next{max-width:44rem;margin:40px auto 0}
.next h2{font:700 .8rem/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--fg2);margin:0 0 12px}
.next ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.next a{display:block;padding:14px 16px;border:1px solid var(--line);border-radius:12px;text-decoration:none;color:var(--fg);background:var(--panel)}
.next a small{display:block;color:var(--fg2);font:600 .78rem/1.3 var(--sans);letter-spacing:.05em;text-transform:uppercase;margin-bottom:4px}
.next a:hover{border-color:var(--acc)}
.byline{max-width:44rem;margin:32px auto 8px;font-size:.88rem;color:var(--fg2)}
.notice{max-width:44rem;margin:-16px auto 28px;font-size:.92rem;color:var(--fg2)}
footer{border-top:1px solid var(--line);padding:28px 16px 96px;font-size:.95rem;color:var(--fg2)}
footer .wrap p{margin:0 0 10px}footer nav{display:flex;flex-wrap:wrap;gap:4px 18px}footer nav a{display:inline-flex;min-height:44px;align-items:center}
/* home */
.cover{display:flex;flex-direction:column;align-items:center;text-align:center;padding:36px 16px 44px}
.cover img{width:min(44vw,200px);height:auto;border-radius:4px;box-shadow:0 22px 50px rgba(0,0,0,.45);margin:0 0 24px}
.cover .q{margin:0 auto}
.safe{position:relative;max-width:44rem;margin:-14px auto 28px;background:#2a1520;border:1px solid #6d2a36;border-radius:12px;padding:14px 18px;font-size:1.02rem}
.safe a{color:#ffd6c8;font-weight:700}
.sec{max-width:44rem;margin:0 auto 44px}
.sec>h2{font:400 1.8rem/1.2 var(--disp);color:#fff;margin:0 0 6px}
.sec>p.lede{color:var(--fg2);margin:0 0 18px}
.where{display:grid;grid-template-columns:1fr;gap:10px;list-style:none;margin:0;padding:0}
@media (min-width:620px){.where{grid-template-columns:1fr 1fr}}
.where a{display:flex;align-items:center;min-height:56px;padding:12px 16px;border-radius:12px;background:var(--panel);border:1px solid var(--line);
color:var(--fg);text-decoration:none;font:600 1.05rem/1.3 var(--sans)}
@media (hover:hover) and (pointer:fine){.where a:hover{border-color:var(--acc)}}
details.more{margin-top:10px}details.more summary{cursor:pointer;min-height:48px;display:flex;align-items:center;font-weight:600;color:var(--acc)}details.more summary::before{content:"▸";margin-right:10px;transition:transform .2s var(--ease-out)}details.more[open] summary::before{transform:rotate(90deg)}details.more .where{margin-top:8px}
form.find{display:flex;gap:8px}form.find input{flex:1;min-width:0;min-height:48px;padding:0 14px;border-radius:10px;border:1px solid var(--line);background:#0c0a13;color:var(--fg);font:1.05rem var(--sans)}
form.find button{min-height:48px;padding:0 18px;border-radius:10px;border:0;background:var(--acc);color:#1a1020;font:700 1rem var(--sans);cursor:pointer}
.path{list-style:none;margin:0;padding:0 0 0 26px;position:relative}
.path::before{content:"";position:absolute;left:8px;top:10px;bottom:10px;width:2px;background:linear-gradient(180deg,#3a2346,#a27d76)}
.path>li{position:relative;margin:0 0 26px}
.path>li::before{content:"";position:absolute;left:-24px;top:10px;width:14px;height:14px;border-radius:50%;background:var(--pa);box-shadow:0 0 0 4px var(--night)}
.path h3{font:400 1.4rem/1.25 var(--disp);margin:0 0 2px;color:#fff}.path h3 small{display:block;font:700 .75rem/1.4 var(--sans);letter-spacing:.08em;color:var(--pa)}
.path ol{list-style:none;margin:8px 0 0;padding:0}.path ol li{border-top:1px solid var(--line)}
.path ol a{display:block;padding:10px 0;text-decoration:none;color:var(--fg)}.path ol a span{color:var(--fg2);font-size:.95rem;display:block}
.path ol a b{font-weight:600}
.results{list-style:none;padding:0;margin:20px 0 0}.results li{border-top:1px solid var(--line)}.results a{display:block;padding:12px 0;text-decoration:none;color:var(--fg)}
.results a span{display:block;color:var(--fg2);font-size:.95rem}
@media (max-width:420px){body{font-size:1.1rem}.bar .home{font-size:1.05rem}.bar a.b{padding:0 9px}}
details.sources summary::before{content:"▸";display:inline-block;margin-right:10px;transition:transform .2s var(--ease-out)}details.sources[open] summary::before{transform:rotate(90deg)}
:root{--ease-out:cubic-bezier(.23,1,.32,1)}
a,.bar a.b,.bar button,.where a,.next a,.find button{transition:color .2s ease,background-color .2s ease,border-color .2s ease,transform .16s var(--ease-out)}
.bar a.b:active,.bar button:not(.leave):active,.where a:active,.next a:active,.find button:active{transform:scale(.97)}
.callnow{list-style:none;margin:16px 0 24px;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}.callnow a{display:flex;flex-direction:column;justify-content:center;min-height:64px;padding:10px 14px;border-radius:12px;background:#7a2730;border:1px solid #a33a45;color:#fff;text-decoration:none;font-size:.95rem;line-height:1.25}.callnow b{font-size:1.5rem}\na.tel{white-space:nowrap;font-weight:700;display:inline-block;padding:6px 2px;margin:-6px 0}
@media (prefers-reduced-motion:reduce){*{transition-property:color,background-color,border-color!important}}
@media print{.sky::before{display:none}.notice,.byline,th,td,.lede{color:#333!important}article a[href^="http"]::after{content:" (" attr(href) ")";font-size:.85em}.bar,.nf-seal,#nf-chrome,.next,footer nav,.skip{display:none!important}body{background:#fff;color:#000}.sky{background:none;color:#000}h1,.q,article h2,.loc{color:#000}a{color:#000}.short,blockquote.say{background:#fff;border-color:#999}}
"""

JS = f"""<script>
(function(){{var O={json.dumps(OLD['chapters'])},R={json.dumps(OLD['routes'])},h=location.hash,m;
if((m=h.match(/^#\\/c\\/(\\d+)/))&&O[m[1]])location.replace('{BASE}/'+O[m[1]]);
else if((m=h.match(/^#\\/(\\w+)/))&&R[m[1]])location.replace('{BASE}/'+R[m[1]]);
function leave(){{try{{document.title='New Tab';document.body.innerHTML='';}}catch(e){{}}location.replace('about:blank');}}
document.addEventListener('click',function(e){{var t=e.target.closest&&e.target.closest('[data-leave]');if(t){{e.preventDefault();leave();}}}});
addEventListener('beforeprint',function(){{document.querySelectorAll('details').forEach(function(d){{d.open=true}})}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&!document.querySelector('.nf-open,[data-nf-open]'))leave();}});
}})();
</script>"""


def house():
    src = S.read(ROOT / "library/silence/index.html")
    css, chrome, js = S.house_parts(CAT.retoc(src, "longafter"))
    return css, chrome, js, S.beacon(src)


HOUSE = None


def frame(*, title, desc, url, ld, body, part, robots=None, og_type="article"):
    s1, s2, acc = SKY.get(part, SKY["start"])
    order = list(SKY)
    dawn = round(max(0, order.index(part) - 1) / 11, 2) if part in order and part != "tools" else 0.1
    hc, hh, hj, beacon = HOUSE
    head = S.head_tags(BOOK, title, desc, url, f"{URL}/og.png", "The Long After by Shae Stovell, free to read", og_type)
    if robots:
        head = re.sub(r'<meta name="robots"[^>]*>', f'<meta name="robots" content="{robots}">', head)
    body = body.replace('<div class="sky"', '<div class="sky" role="region" aria-label="Title"', 1)
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + head +
            f'<meta name="theme-color" content="{s1}">\n'
            f'<link rel="preload" href="{BASE}/f/bookserif-400-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
            f"<style>{FONTS}{CSS}:root{{--s1:{s1};--s2:{s2};--acc:{acc};--dawn:{dawn}}}</style>\n{hc}\n"
            + (f'<script type="application/ld+json">{S.ld_json(ld)}</script>\n' if ld else "") + "</head>\n<body>\n"
            '<a class="skip" href="#text">Skip to the text</a>\n'
            f'<header class="bar"><a class="home" href="{BASE}">The Long After</a>'
            f'<a class="b" href="{BASE}/search">Search</a><a class="b" href="{BASE}/if-youre-not-safe-right-now">Help</a>'
            '<button class="leave" type="button" data-leave aria-label="Leave this page now">Leave</button></header>\n'
            + body +
            f'\n<footer><div class="wrap"><p>{S.LICENSE_LINE}</p><p>{BOOK["notice_short"]} '
            f'<a href="{BASE}/how-to-use-this-book">What this book is and isn\u2019t</a>.</p>'
            f'<nav aria-label="More"><a href="{BASE}">The Long After</a><a href="{BASE}/contents">Every chapter</a>'
            f'<a href="{BASE}/search">Search</a><a href="{BASE}/all">The whole book on one page</a><a href="/playbook">The Pattern Decoder</a>'
            '<a href="/topics">All topics</a><a href="/">Noble Father Creations</a></nav></div></footer>\n'
            + hh + "\n" + hj + "\n" + JS + "\n" + beacon + "\n</body>\n</html>\n")


def loc_line(c):
    if c["part"] == "start":
        return f'<a href="{BASE}">Start here</a>'
    if c["part"] == "tools":
        return f'<a href="{BASE}#toolbox">Toolbox</a>'
    p = PARTS[c["part"]]
    return f'<a href="{BASE}#part-{c["part"]}">Part {ROMAN[c["part"]]}: {html.escape(p["title"])}</a>, chapter {c["n"]} of {len(p["chapters"])}'


def crumbs(c, url):
    trail = [("Noble Father Creations", S.DOMAIN + "/"), ("The Long After", URL)]
    if c["part"] not in ("start", "tools"):
        trail.append((f"Part {ROMAN[c['part']]}: {PARTS[c['part']]['title']}", f"{URL}#part-{c['part']}"))
    trail.append((c["title"], url))
    return S.crumbs_ld(trail)


def faq_items(body):
    out = []
    for q, a in re.findall(r"^\*\*(.+?\?)\*\* (.+?) \[Read more\]", body, re.M):
        out.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(md(a))}})
    return out


def terms(body):
    return [{"@type": "DefinedTerm", "name": t.rstrip("."), "description": plain(md(d.split("[")[0])).strip()}
            for t, d in re.findall(r"^\*\*(.+?)\*\* (.+)$", body, re.M)]


def page(slug, ch, pos):
    c = CH[slug]
    m = ch["meta"]
    url = f"{URL}/{slug}"
    main, src = split_sources(ch["body"])
    body_html = md(main)
    if slug in TEL_PAGES:
        body_html = telify(body_html)
    if slug == "if-youre-not-safe-right-now":
        callnow = ('<ul class="callnow" aria-label="Emergency numbers">'
                     + "".join(f'<li><a href="tel:{n}"><b>{n}</b> {w}</a></li>' for n, w in
                               [("911", "US and Canada"), ("999", "UK"), ("000", "Australia"), ("112", "Ireland and Europe")])
                     + "</ul>")
    else:
        callnow = ""
    src_html = ""
    if src:
        src_html = '<details class="sources"><summary>Sources for this page</summary>' + md(src) + "</details>"
    # next, if this is you: the next page in reading order, then the first in-text chapter links
    links = []
    i = ORDER.index(slug)
    if i + 1 < len(ORDER):
        links.append(("Next", ORDER[i + 1]))
    for t in re.findall(r"\]\(ch:([a-z0-9-]+)", main):
        if t != slug and t not in [l[1] for l in links]:
            links.append(("Related", t))
        if len(links) >= 3:
            break
    nxt = ('<nav class="next" aria-labelledby="nx-h"><h2 id="nx-h">Next, if this is you</h2><ul>'
           + "".join(f'<li><a href="{BASE}/{t}"><small>{k}</small>{html.escape(CH[t]["title"])}</a></li>' for k, t in links)
           + "</ul></nav>")
    desc = S.clip(m["short"], 158)
    title = m["seo"]
    node = {"@type": "Chapter", "@id": url + "#chapter", "name": c["title"], "position": pos, "url": url,
            "isPartOf": {"@id": URL + "#book"}, "author": {"@id": S.PERSON["@id"]}, "inLanguage": "en",
            "isAccessibleForFree": True, "license": S.LICENSE_URL, "description": m["short"], "abstract": m["short"],
            "keywords": ", ".join([c["keyword"]] + c["keywords2"])}
    if c["keywords2"]:
        node["alternateName"] = c["keywords2"]
    cites = [re.sub(r"[*_]", "", l[2:]).strip() for l in src.splitlines() if l.startswith("- ")] if src else []
    if cites:
        node["citation"] = cites
    graph = [{"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
              "isPartOf": {"@id": URL + "#book"}, "breadcrumb": {"@id": url + "#crumbs"}, "datePublished": BOOK.get("published", "2026-11-22"), "dateModified": S.TODAY,
              "author": {"@id": S.PERSON["@id"]}, "isAccessibleForFree": True, "license": S.LICENSE_URL,
              "primaryImageOfPage": f"{URL}/og.png", "mainEntity": {"@id": url + "#chapter"}},
             node, dict(crumbs(c, url), **{"@id": url + "#crumbs"}), S.book_node(BOOK), S.PERSON, S.ORG]
    if slug == "questions-people-ask":
        graph[0]["@type"] = ["WebPage", "FAQPage"]
        graph[0]["mainEntity"] = faq_items(main)
    if slug == "a-to-z":
        graph.append({"@type": "DefinedTermSet", "@id": url + "#terms", "name": "Post-separation abuse terms", "hasDefinedTerm": terms(main)})
    body = (f'<div class="sky"><div class="in"><p class="loc">{loc_line(c)}</p>'
            f'<h1 id="top">{html.escape(smart(c["title"]))}</h1><p class="q">{html.escape(smart(m["question"]))}</p></div></div>\n'
            f'<main id="text">{callnow}<section class="short" aria-label="The short answer"><p class="lab">The short answer</p>'
            f'<p>{(inline(m["short"]))}</p></section>\n<p class="notice">{BOOK["notice_short"]} <a href="{BASE}/how-to-use-this-book">Full notice</a>.</p>\n<article>{body_html}</article><p class="byline">Written by Shae Stovell. Sources are listed below. Last reviewed <time datetime="{S.TODAY}">{S.TODAY_HUMAN}</time>.</p>{src_html}{nxt}</main>')
    return frame(title=title, desc=desc, url=url, ld={"@context": "https://schema.org", "@graph": graph}, body=body, part=c["part"])


def contents_list():
    out = ['<ol class="path">']
    for pid in [p["id"] for p in PLAN["parts"] if p["id"] not in ("start", "tools")]:
        p = PARTS[pid]
        out.append(f'<li id="part-{pid}" style="--pa:{SKY[pid][2]}"><h3 id="ph-{pid}"><small>PART {ROMAN[pid]}</small>{html.escape(p["title"])}</h3><ol>')
        for s in p["chapters"]:
            c = CH[s]
            out.append(f'<li><a href="{BASE}/{s}"><b>{html.escape(c["title"])}</b><span>{html.escape(smart(META[s]["question"]))}</span></a></li>')
        out.append("</ol></li>")
    out.append("</ol>")
    return "\n".join(out)


def tools_list():
    return ('<ul class="where" id="toolbox-list">' + "".join(
        f'<li><a href="{BASE}/{s}">{html.escape(CH[s]["title"])}</a></li>' for s in PARTS["tools"]["chapters"]) + "</ul>")


def where_items():
    body = META_BODY["where-are-you-right-now"]
    items = []
    for sec in re.split(r"^## ", body, flags=re.M)[1:]:
        head, _, rest = sec.partition("\n")
        items.append(head.strip())
    return items


def index_html():
    graph = [dict(S.book_node(BOOK, [CH[s] for s in ORDER]), **{"mainEntityOfPage": URL}),
             {"@type": "WebPage", "@id": URL, "url": URL, "name": "The Long After: Post-Separation Abuse After Leaving",
              "description": BOOK["description"], "inLanguage": "en", "about": {"@id": URL + "#book"},
              "dateModified": S.TODAY, "isAccessibleForFree": True, "license": S.LICENSE_URL}, S.PERSON, S.ORG]
    wl = [f'<li><a href="{BASE}/where-are-you-right-now#{S.slugify(h, 60)}">{html.escape(h)}</a></li>' for h in where_items()]
    where = '<ul class="where">' + "".join(wl[:6]) + "</ul>" + ('<details class="more"><summary>More situations</summary><ul class="where">' + "".join(wl[6:]) + "</ul></details>" if len(wl) > 6 else "")
    body = (f'<div class="sky" style="--s1:#120d22;--s2:#3d2448"><div class="cover">'
            f'<img src="{BASE}/cover.webp" width="720" height="1073" alt="The Long After by Shae Stovell, book cover" fetchpriority="high">'
            '<h1>The Long After</h1><p class="q">What happens once you\u2019ve left. A free guide to post-separation abuse, '
            'safety, courts, children, feelings and rebuilding.</p></div></div>\n<main id="text">'
            f'<p class="safe">Not safe right now? Call your emergency number. <a href="{BASE}/if-youre-not-safe-right-now">Where to get help today</a>. '
            'The <b>Leave</b> button at the top clears this page instantly.</p>'
            f'<section class="sec" aria-labelledby="w-h"><h2 id="w-h">Where are you right now?</h2>'
            '<p class="lede">Pick the line that sounds most like today. It opens the chapters that matter most.</p>'
            f'{where}</section>'
            f'<section class="sec" aria-labelledby="s-h"><h2 id="s-h">Search</h2><p class="lede">Type it the way you\u2019d say it. Nothing you type leaves this page.</p>'
            f'<form class="find" action="{BASE}/search" method="get" role="search"><label class="skip" for="q">Search the book</label>'
            '<input id="q" name="q" type="search" placeholder="he keeps texting my sister" autocomplete="off"><button type="submit">Search</button></form></section>'
            f'<section class="sec" id="contents" aria-labelledby="c-h"><h2 id="c-h">Contents</h2>'
            '<p class="lede">Eleven parts, from the first night to first light. Every chapter stands alone.</p>'
            f'<ul class="where" style="margin-bottom:24px"><li><a href="{BASE}/how-to-use-this-book">How to use this book</a></li>'
            f'<li><a href="{BASE}/if-youre-not-safe-right-now">If you\u2019re not safe right now</a></li></ul>{contents_list()}</section>'
            f'<section class="sec" id="toolbox" aria-labelledby="t-h"><h2 id="t-h">Toolbox</h2><p class="lede">Things to print, copy or keep. Keep them somewhere private.</p>{tools_list()}</section>'
            '<section class="sec" id="updates" aria-labelledby="u-h"><h2 id="u-h">Updates</h2>'
            '<p class="lede"><b>v5 \u00b7 November 2026.</b> Rewritten and greatly expanded: 83 chapters in eleven parts, a page for '
            'where you are right now, a toolbox, search, sources on every page, links to the matching patterns in the Pattern Decoder, and tap-to-call help numbers.</p>'
            '<p class="lede">v4 \u00b7 21 November 2026. Every chapter got its own page. v3 \u00b7 1 September 2026. Cover watermark updated. '
            'v2 \u00b7 1 September 2026. First published.</p></section></main>')
    return frame(title="The Long After: Post-Separation Abuse After Leaving", desc=BOOK["description"], url=URL,
                 ld={"@context": "https://schema.org", "@graph": graph}, body=body, part="start", og_type="book")


def simple(title, desc, url, inner, robots=None, part="start", ld=None):
    body = (f'<div class="sky"><div class="in"><p class="loc"><a href="{BASE}">The Long After</a></p><h1 id="top">{title}</h1></div></div>'
            f'<main id="text"><div class="wrap" style="padding-top:24px">{inner}</div></main>')
    return frame(title=f"{plain(title)} \u00b7 The Long After", desc=desc, url=url, ld=ld, body=body, part=part, robots=robots)


def search_html():
    idx = [{"s": s, "t": CH[s]["title"], "q": META[s]["question"],
            "k": " ".join([CH[s]["keyword"]] + CH[s]["keywords2"] + re.findall(r"^## (.+)$", META_BODY[s], re.M)),
            "a": META[s]["short"]} for s in ORDER]
    inner = (f'<form class="find" action="{BASE}/search" method="get" role="search" onsubmit="return false">'
             '<label class="skip" for="sq">Search the book</label><input id="sq" name="q" type="search" placeholder="Type it the way you\u2019d say it" autocomplete="off">'
             '<button type="button" id="sb">Search</button></form><p class="lede" style="color:var(--fg2)">Nothing you type is sent anywhere or saved.</p>'
             '<ul class="results" id="res" aria-live="polite"></ul>'
             f'<script>var I={json.dumps(idx)};'
             "function n(s){return s.toLowerCase().replace(/[\u2019']/g,'').replace(/[^a-z0-9 ]+/g,' ')}"
             "function go(){var q=n(document.getElementById('sq').value).split(' ').filter(function(w){return w.length>2});var r=document.getElementById('res');r.innerHTML='';if(!q.length)return;"
             "var sc=I.map(function(x){var t=n(x.t),k=n(x.k+' '+x.q),a=n(x.a),s=0;q.forEach(function(w){if(t.indexOf(w)>-1)s+=5;if(k.indexOf(w)>-1)s+=3;if(a.indexOf(w)>-1)s+=1;});return [s,x]}).filter(function(p){return p[0]>0}).sort(function(a,b){return b[0]-a[0]}).slice(0,12);"
             f"if(!sc.length){{r.innerHTML='<li>No match. Try other words, or see <a href=\"{BASE}/a-to-z\">A to Z</a>.</li>';return}}"
             f"sc.forEach(function(p){{var x=p[1],li=document.createElement('li'),a=document.createElement('a');a.href='{BASE}/'+x.s;a.textContent=x.t;var sp=document.createElement('span');sp.textContent=x.q;a.appendChild(sp);li.appendChild(a);r.appendChild(li)}})}}"
             "document.getElementById('sb').onclick=go;document.getElementById('sq').oninput=go;"
             "var u=new URLSearchParams(location.search).get('q');if(u){document.getElementById('sq').value=u;go()}</script>")
    return simple("Search", "Search The Long After. Nothing you type leaves this page.", f"{URL}/search", inner, robots="noindex, follow")


def all_html():
    parts = []
    for s in ORDER:
        c, mm = CH[s], META[s]
        main, _ = split_sources(META_BODY[s])
        parts.append(f'<section id="{s}"><h2 style="font:400 2rem/1.15 var(--disp);color:#fff;margin:2.4em 0 .2em">{html.escape(c["title"])}</h2>'
                     f'<p class="q" style="color:var(--fg2)">{html.escape(smart(mm["question"]))}</p>'
                     f'<div class="short" style="margin:16px 0"><p class="lab">The short answer</p><p>{(inline(mm["short"]))}</p></div>'
                     f'<article>{md(main)}</article></section>')
    toc = "<ol>" + "".join(f'<li><a href="#{s}">{html.escape(CH[s]["title"])}</a></li>' for s in ORDER) + "</ol>"
    inner = ('<p class="lede">The whole book on one page, for reading offline or printing. Save this page to keep it on your device. '
             f'Each chapter also has its own page with sources.</p><details><summary>Contents</summary>{toc}</details>' + "".join(parts))
    return simple("The whole book on one page", "The Long After, every chapter on one page.", f"{URL}/all", inner, robots="noindex, follow")


def contents_html():
    inner = f'<p class="lede">Every chapter of The Long After, by part. {len([s for s in ORDER if CH[s]["part"] not in ("start","tools")])} chapters, free to read.</p><h2 id="the-eleven-parts" style="font:400 1.6rem/1.2 var(--disp);color:#fff">The eleven parts</h2>{contents_list()}<h2 id="toolbox">Toolbox</h2>{tools_list()}<p class="notice" style="margin-top:28px">{BOOK["notice_short"]} <a href="{BASE}/how-to-use-this-book">Full notice</a>.</p>'
    graph = [{"@type": "CollectionPage", "@id": URL + "/contents", "url": URL + "/contents", "name": "The Long After: Every Chapter",
              "isPartOf": {"@id": URL + "#book"}, "inLanguage": "en", "dateModified": S.TODAY,
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(ORDER), "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": f"{URL}/{s}", "name": CH[s]["title"]} for i, s in enumerate(ORDER)]}},
             S.crumbs_ld([("Noble Father Creations", S.DOMAIN + "/"), ("The Long After", URL), ("Every chapter", URL + "/contents")]),
             S.book_node(BOOK), S.PERSON, S.ORG]
    return simple("Every chapter", "Every chapter of The Long After, a free guide to post-separation abuse, by part.",
                  URL + "/contents", inner, ld={"@context": "https://schema.org", "@graph": graph})


def redirect_html(to):
    u = f"{URL}/{to}"
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex, follow">'
            f'<link rel="canonical" href="{u}"><meta http-equiv="refresh" content="0; url={BASE}/{to}"></head>'
            f'<body><p>This page has moved: <a href="{BASE}/{to}">{BASE}/{to}</a></p></body></html>\n')


META, META_BODY = {}, {}


def main():
    global HOUSE
    chs = parse()
    missing = [s for s in ORDER if s not in chs]
    assert not missing, f"unwritten pages: {missing}"
    for s in ORDER:
        META[s] = chs[s]["meta"]; META_BODY[s] = chs[s]["body"]
    HOUSE = house()
    keep = {"index.html", "contents.html", "search.html", "all.html", "AUDIT.md", "BOOK-MAP.md", "BOOK-MAP-v2.md",
            "DESIGN-STATE.md", "qa.js"}
    for i, s in enumerate(ORDER, 1):
        S.write(OUT / f"{s}.html", page(s, chs[s], i))
        keep.add(f"{s}.html")
    for old, new in PLAN["old_redirects"].items():
        S.write(OUT / f"{old}.html", redirect_html(new)); keep.add(f"{old}.html")
    S.write(OUT / "index.html", index_html())
    S.write(OUT / "contents.html", contents_html())
    S.write(OUT / "search.html", search_html())
    S.write(OUT / "all.html", all_html())
    stale = [f.name for f in OUT.glob("*.html") if f.name not in keep]
    for n in stale:
        (OUT / n).unlink()
    urls = [URL, URL + "/contents"] + [f"{URL}/{s}" for s in ORDER]
    S.write(OUT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc><lastmod>{S.TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    print(f"longafter v5: {len(ORDER)} pages + index, contents, search, all; {len(stale)} stale pages removed; sitemap {len(urls)} URLs")


if __name__ == "__main__":
    main()
