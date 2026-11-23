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
from urllib.parse import quote
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

# Dusk to first light: [sky top, sky bottom, accent] per part. OKLCH steps: accent hue 32->88deg, lightness .72->.86 (coral to gold);
# sky top hue 298->255, bottom 318->35. Every step keeps link and sky text at AA (design/longafter-v6/check-v6.mjs).
SKY = {
    "start": ("#180b2c", "#3f1d49", "#e88572"), "i": ("#180b2c", "#3f1d49", "#e88572"),
    "ii": ("#180e2f", "#452047", "#eb8c6f"), "iii": ("#181232", "#4c2245", "#ee926c"),
    "iv": ("#181535", "#512543", "#f0996a"), "v": ("#181838", "#562740", "#f2a068"),
    "vi": ("#181c3a", "#5b2b3e", "#f3a768"), "vii": ("#191f3c", "#602e3c", "#f3af68"),
    "viii": ("#19223e", "#633239", "#f3b669"), "ix": ("#192640", "#673637", "#f3be6c"),
    "x": ("#192942", "#6a3b36", "#f2c570"), "xi": ("#1a2c44", "#6c4034", "#f0cd74"),
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


MANIFEST = json.loads((ROOT / "site_manifest.json").read_text())
CRISIS = {"if-youre-not-safe-right-now", "find-help", "when-its-more-than-aftermath"}   # byline only (06-ABOUT, rules)
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
    out, i, used, stack = [], 0, set(), []
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith(":::"):   # block fences (BOOK-PIPELINE-V2 section 3): "::: kind [arg]" opens, ":::" closes
            kind, _, arg = ln[3:].strip().partition(" ")
            if kind:
                extra = f' data-arg="{html.escape(arg)}"' if arg else ""
                out.append(f'<div class="blk blk-{html.escape(kind)}"{extra}>'); stack.append(kind)
            else:
                out.append("</div>"); stack and stack.pop()
            i += 1; continue
        if stack and stack[-1] == "decoder" and ln.startswith("**"):   # one element per voice; Copy on the reply
            voices = []
            while i < len(lines) and lines[i].startswith("**"):
                lab, _, rest = inline(lines[i].strip()).partition("</strong>")
                k = "say" if "They say" in lab else "why" if "What it" in lab else "reply"
                lab = lab.replace("<strong>", "<strong class=\"dv-l\">") + "</strong>"
                if k == "reply":   # Copy sits beside the label, so it shows as soon as the reply does (never under the dock)
                    lab = f'<span class="dv-h">{lab} <button class="dv-copy" type="button" data-js>Copy</button></span>'
                voices.append(f'<p class="dv dv-{k}">{lab} <span class="dv-t">{rest.strip()}</span></p>')
                i += 1
            out.append('<div class="dv-p">' + "".join(voices) + "</div>"); continue
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
            lis = "".join(f'<li class="check"><label><input type="checkbox"><span>{inline(x[1:].lstrip())}</span></label></li>' if x.startswith("☐") else f"<li>{inline(re.sub(r'^\s*- ', '', x))}</li>" for x in items)
            out.append(f'<ul{" class=\"checks\"" if items[0].startswith("☐") else ""}>{lis}</ul>'); continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(## |### |>|\||\s*- |\d+\. |☐|:::)", lines[i]):
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
--disp:'BookDisplay',serif;--body:'BookSerif',serif;--sans:var(--body)}
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
ul.checks{list-style:none;padding:0}ul.checks li{margin:0;border-bottom:1px solid var(--line)}
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

# ---------------------------------------------------------------- v6 design: A "Notes on the table" + C's cover tiles
# Lucide paths (tools/lucide-icons-lucide), drawn as CSS masks so they take the part's accent.
ICONS = {
    "lamp": '<path d="M12 12v6"/><path d="M4.077 10.615A1 1 0 0 0 5 12h14a1 1 0 0 0 .923-1.385l-3.077-7.384A2 2 0 0 0 15 2H9a2 2 0 0 0-1.846 1.23Z"/><path d="M8 20a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1z"/>',
    "door": '<path d="M11 20H2"/><path d="M11 4.562v16.157a1 1 0 0 0 1.242.97L19 20V5.562a2 2 0 0 0-1.515-1.94l-4-1A2 2 0 0 0 11 4.561z"/><path d="M11 4H8a2 2 0 0 0-2 2v14"/><path d="M14 12h.01"/><path d="M22 20h-3"/>',
    "msg": '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/>',
    "scale": '<path d="M12 3v18"/><path d="m19 8 3 8a5 5 0 0 1-6 0zV7"/><path d="M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1"/><path d="m5 8 3 8a5 5 0 0 1-6 0zV7"/><path d="M7 21h10"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
    "moon": '<path d="M18 5h4"/><path d="M20 3v4"/><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/>',
    "printer": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "signpost": '<path d="M12 13v8"/><path d="M12 3v3"/><path d="M2.354 10.354a1.207 1.207 0 0 1 0-1.708l2.06-2.06A2 2 0 0 1 5.828 6h12.344a2 2 0 0 1 1.414.586l2.06 2.06a1.207 1.207 0 0 1 0 1.708l-2.06 2.06a2 2 0 0 1-1.414.586H5.828a2 2 0 0 1-1.414-.586z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
}


def ico(name, stroke="black"):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{stroke}' stroke-width='1.75' "
           f"stroke-linecap='round' stroke-linejoin='round'>{ICONS[name].replace(chr(34), chr(39))}</svg>")
    return 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'


def mask(name):
    return f"-webkit-mask:{ico(name)} center/contain no-repeat;mask:{ico(name)} center/contain no-repeat;"


SC = "font-variant-caps:all-small-caps;letter-spacing:.07em;font-weight:700;"
CSS += f"""
/* v6: the hour on every page (sky band, horizon rules, accent edges) */
.bar{{border-bottom-color:transparent}}
.bar::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;height:3px;pointer-events:none;background:linear-gradient(90deg,var(--s1),var(--s2) 22%,var(--acc) 50%,var(--s2) 78%,var(--s1))}}
.sky{{background:linear-gradient(180deg,var(--s1) 0%,var(--s2) 78%,color-mix(in srgb,var(--s2) 78%,var(--acc)) 100%)}}
article>h2::before,.blk-sheet>h2::before{{content:"";display:block;height:1px;margin:0 0 1.1em;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--acc) 80%,transparent) 50%,transparent)}}
.blk-sheet>h2:first-of-type::before{{display:none}}
article .blk{{margin:2.5rem 0;position:relative}}
article .blk h2{{font:400 1.45rem/1.25 var(--disp);color:#fff;margin:0 0 .5em;scroll-margin-top:76px}}
article .blk>:last-child{{margin-bottom:0}}
.blk-action::before,.blk-scene::before,.blk-sheet::before{{display:block;font-family:var(--sans);font-size:1rem;line-height:1.2;{SC}margin:0 0 10px}}
/* action: an index card with a hand-drawn circle */
article .blk-action{{background-color:#2a2232;border-top:3px solid var(--acc);border-radius:4px 4px 12px 12px;padding:18px 20px 20px;
box-shadow:0 18px 32px -18px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.04)}}
.blk-action::before{{content:"One small step";color:var(--acc)}}
article .blk-action h2{{position:relative;padding-left:42px}}
article .blk-action h2::before{{content:"";position:absolute;left:2px;top:.1em;width:26px;height:26px;border:2px solid var(--acc);
border-radius:54% 44% 57% 43% / 46% 56% 44% 54%;transform:rotate(-9deg);box-shadow:1px 1px 0 0 color-mix(in srgb,var(--acc) 35%,transparent)}}
article .blk-action p{{color:#f3edf6;background:linear-gradient(180deg,transparent calc(1lh - 5px),rgba(239,233,244,.11) calc(1lh - 5px),rgba(239,233,244,.11) calc(1lh - 4px),transparent calc(1lh - 4px)) 0 0/100% 1lh repeat-y}}
/* decoder: two voices as chat bubbles, Copy on the reply */
article .blk-decoder{{background:#1c1727;border:1px solid color-mix(in srgb,var(--acc) 30%,#2c2539);border-radius:20px;padding:16px 14px}}
.dv-p{{display:flex;flex-direction:column;gap:12px}}
article .dv{{margin:0;max-width:none}}
.dv-l,.dv-t{{display:block}}
.dv-say{{align-self:flex-start;max-width:90%;background:#2e2839;border-radius:20px 20px 20px 6px;padding:12px 16px}}
.dv-why{{align-self:stretch;color:var(--fg2);font-style:italic;padding:0 10px 0 14px;border-left:2px solid #3b3349;margin:2px 8px!important}}
.dv-why a{{color:var(--acc)}}
.dv-reply{{align-self:flex-end;max-width:90%;display:flex;flex-direction:column;background:var(--acc);color:#1c1322;border-radius:20px 20px 6px 20px;padding:12px 16px 10px}}
.dv-l{{font-family:var(--sans);font-size:1rem;line-height:1.3;{SC}color:var(--fg2);margin:0 0 2px}}
.dv-reply .dv-l{{color:#4a2733}}
.dv-h{{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 0 4px}}.dv-h .dv-l{{margin:0}}
.dv-copy{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;min-width:44px;cursor:pointer;font:600 1rem/1 var(--sans);
flex:none;padding:0 16px;border-radius:999px;border:1px solid rgba(28,19,34,.45);background:rgba(28,19,34,.07);color:#1c1322}}
.dv-copy::before{{content:"";width:16px;height:16px;background:currentColor;{mask('copy')}}}
.dv-copy:hover{{background:rgba(28,19,34,.16)}}
.dv-copy:focus-visible{{outline-color:#1c1322}}
/* honest: recessed, private, a small lamp */
article .blk-honest{{background:radial-gradient(110% 70% at 100% 0%,color-mix(in srgb,var(--acc) 15%,transparent),transparent 62%),#0b0911;
border-radius:20px;padding:22px 20px;box-shadow:inset 0 4px 14px rgba(0,0,0,.75),inset 0 0 0 1px rgba(255,255,255,.035)}}
.blk-honest::before{{content:"";position:absolute;right:18px;top:20px;width:26px;height:26px;background:var(--acc);{mask('lamp')}}}
article .blk-honest h2{{padding-right:40px}}
article .blk-honest p:first-of-type{{color:var(--fg2)}}
/* scene: a softer paper tone, in italics */
article .blk-scene{{background:#251f2e;border:1px solid #362e43;border-left:3px solid color-mix(in srgb,var(--acc) 55%,#362e43);border-radius:4px 16px 16px 16px;padding:18px 20px 20px}}
.blk-scene::before{{content:"A made-up story";color:#d8cde4}}
article .blk-scene p{{font-style:italic;color:#e9e2f0}}
article .blk-scene p:first-of-type{{color:var(--fg2)}}
/* bridge: a signpost */
article .blk-bridge{{border-top:1px dashed #3d3550;border-bottom:1px dashed #3d3550;padding:16px 0 16px 46px}}
.blk-bridge::before{{content:"";position:absolute;left:4px;top:18px;width:28px;height:28px;background:var(--acc);{mask('signpost')}}}
article .blk-bridge a{{font-size:1.12em;{SC}white-space:nowrap}}
article .blk-bridge a::after{{content:"";display:inline-block;width:18px;height:18px;margin-left:6px;vertical-align:-3px;background:currentColor;{mask('arrow')}}}
/* sheet: cut along the dashes */
article .blk-sheet{{border:2px dashed color-mix(in srgb,var(--fg2) 55%,transparent);border-radius:10px;padding:18px 18px 12px;background:#16121e}}
.blk-sheet::before{{content:"Printable sheet";color:var(--fg2);padding-left:30px;min-height:22px;background:{ico('printer', '#bdb3cc')} left center/22px no-repeat}}
.blk-sheet::after{{content:"";position:absolute;right:28px;top:-14px;width:28px;height:26px;background:var(--night) {ico('scissors', '#bdb3cc')} center/22px no-repeat}}
article .blk-sheet h2{{font-size:1.3rem;margin:1.3em 0 .3em}}
article .blk-sheet h2:first-of-type{{margin-top:.2em}}
article .blk-sheet ul.checks li{{border-bottom-color:#2d2639}}
/* checklists: real checkboxes, ticks live in memory only (nothing stored, reset on reload) */
ul.checks label{{display:flex;align-items:flex-start;gap:12px;min-height:44px;padding:10px 0;cursor:pointer}}
ul.checks input{{appearance:none;-webkit-appearance:none;flex:none;width:22px;height:22px;margin:.2em 0 0;border:2px solid var(--acc);border-radius:5px;background:transparent;cursor:pointer;display:grid;place-content:center}}
ul.checks input:checked{{background:var(--acc) {ico('check', '#1c1322')} center/16px no-repeat}}
/* shell */
[hidden]{{display:none!important}}
html:not(.js) [data-js]{{display:none!important}}
button{{font-family:var(--sans)}}
details:not([open])>:not(summary){{display:none}}
/* compact chapter header: byline on one line where it fits, then one row of controls (44px tall) */
.by{{font-size:.9rem;line-height:1.45;color:#f1e9ee;margin:10px 0 0}}
.sky:has(.hrow){{padding-bottom:44px}}
.hrow{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0 0}}.hrow .tools,.hrow .otp{{margin:0}}.otp[open]{{flex-basis:100%;order:2}}.by a{{color:#fff;display:inline-block;padding:10px 0;margin:-10px 0}}
.tools{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:12px 0 0}}
.mode{{display:inline-flex;padding:3px;border-radius:999px;background:rgba(10,8,16,.55);border:1px solid rgba(255,255,255,.14)}}
.mode button,.disc{{min-height:44px;padding:0 14px;border-radius:999px;border:0;background:none;color:#f1e9ee;font:600 1rem/1 var(--sans);cursor:pointer}}
.mode button[aria-pressed=true]{{background:var(--acc);color:#1c1322}}
.disc{{border:1px solid rgba(255,255,255,.22);background:rgba(10,8,16,.4)}}.disc[aria-pressed=true]{{background:#f1e9ee;color:#1c1322}}
.otp{{margin:12px 0 0;background:rgba(10,8,16,.55);border:1px solid rgba(255,255,255,.14);border-radius:12px;font-size:1rem}}
.otp summary{{cursor:pointer;min-height:44px;display:flex;align-items:center;padding:0 14px;font-weight:600;color:#fff}}
.otp summary::before{{content:"▸";margin-right:10px;transition:transform .2s var(--ease-out)}}.otp[open] summary::before{{transform:rotate(90deg)}}
.otp ol{{margin:0;padding:0 14px 8px;list-style:none}}.otp a{{display:block;padding:10px 0;color:#f1e9ee;border-top:1px solid rgba(255,255,255,.1);text-decoration:none}}
.prog{{position:fixed;top:0;left:0;right:0;height:3px;z-index:9600;pointer-events:none}}.prog i{{display:block;height:100%;background:var(--acc);transform:scaleX(0);transform-origin:0 50%}}
.end{{max-width:44rem;margin:40px auto 0;padding-top:20px;border-top:1px solid var(--line);font-size:1rem;color:var(--fg2)}}
.end p{{margin:0 0 8px}}.end a{{display:inline-block;padding:10px 0;margin:-10px 0}}
.share button{{min-height:44px;padding:0 4px;border:0;background:none;color:var(--acc);font:600 1rem/1 var(--sans);text-decoration:underline;text-underline-offset:.2em;cursor:pointer}}
footer .disc{{color:var(--fg2);margin-top:8px}}
.rail,.dock .leave{{font-family:var(--sans)}}
.rail{{display:none}}
.dock{{position:fixed;left:0;right:0;bottom:0;z-index:8999;display:grid;grid-template-columns:auto auto 1fr;align-items:end;gap:8px;padding:8px 12px calc(8px + env(safe-area-inset-bottom));
background:var(--night);border-top:1px solid var(--line)}}
.dock a,.dock button{{display:flex;align-items:center;justify-content:center;min-height:48px;padding:0 12px;border-radius:12px;border:1px solid var(--line);background:var(--panel);
color:var(--fg);font:600 .95rem/1.1 var(--sans);white-space:nowrap;text-decoration:none;text-align:center;cursor:pointer}}
.dock button[aria-pressed=true]{{background:var(--acc);color:#1c1322;border-color:var(--acc)}}
.dock [data-mode-toggle]{{min-width:8.4em}}.dock .leave{{min-height:56px;background:#7a2730;border-color:#a33a45;color:#fff;font-size:1.1rem}}
body:has(.dock) footer{{padding-bottom:120px}}
@media (max-width:1099px){{.tools .mode{{display:none}}}}
@media (min-width:1100px){{.dock{{display:none}}.otp{{display:none}}
.rail{{display:flex;flex-direction:column;gap:6px;position:fixed;z-index:50;top:84px;right:calc(50% + 22rem + 24px);width:min(240px,calc(50vw - 22rem - 40px));max-height:calc(100vh - 100px);overflow:auto;
padding:14px;background:rgba(17,14,25,.94);border:1px solid var(--line);border-radius:14px;font-size:.95rem;line-height:1.35}}
.rail p{{margin:0}}.rail .r-loc a{{color:var(--acc);display:inline;padding:0;margin:0}}.rail .r-t{{font:400 1.2rem/1.2 var(--disp);color:#fff;margin:4px 0 6px}}
.rail ol{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}.rail ol a{{display:block;padding:9px 0;color:var(--fg2);text-decoration:none;border-bottom:1px solid var(--line)}}
.rail ol a:hover{{color:#fff}}
.rail .leave{{position:sticky;bottom:0;flex:none;box-shadow:0 -12px 12px rgba(17,14,25,.94);margin-top:10px;min-height:52px;border-radius:12px;background:#7a2730;border:1px solid #a33a45;color:#fff;font:600 1.1rem/1 var(--sans);cursor:pointer}}}}
/* Just the steps: keep the short answer, the step, the decoder, safety links, lists and tables */
.steps article>:not(.blk-action):not(.blk-decoder):not(ul):not(ol):not(.tbl):not(h2:has(+ul,+ol,+.tbl)):not(p:has(a.tel,a[href$="/if-youre-not-safe-right-now"],a[href$="/find-help"],a[href$="/when-its-more-than-aftermath"])),
.steps details.sources{{display:none}}
@media print{{@page{{margin:14mm}}html{{background:#fff;color-scheme:light}}.sky{{background:none!important;padding-bottom:16px}}.sky .loc,.sky .q,.by{{color:#000!important}}footer,.end,.end a{{color:#333!important}}.short{{margin-top:8px}}.prog,.rail,.dock,.tools,.otp,.share,.dv-copy,.bar::after,footer .disc{{display:none!important}}
article>h2::before{{background:#999}}article .blk-sheet{{border-color:#000;background:none;break-before:page;break-after:page}}.blk-sheet::after{{background-color:#fff}}
.blk-sheet::before{{color:#000}}article .blk-sheet ul.checks li{{border-bottom-color:#999;break-inside:avoid}}
ul.checks input{{background:none!important;border-color:#000!important}}
article .blk-action,article .blk-scene,article .blk-honest,article .blk-decoder{{background:none;box-shadow:none;border:1px solid #999;break-inside:avoid}}
.dv-say,.dv-reply{{background:#eee;color:#000}}.dv-l,.dv-why,article .blk p,article .blk h2,.by,.by a{{color:#000!important}}}}
"""

COVER_CSS = "".join(f'.where.tiles a[href$="#{k}"]{{--ico:{ico(v)}}}' for k, v in {
    "i-left-in-the-last-few-days": "door", "they-keep-contacting-me": "msg", "we-have-children-together": "users",
    "theres-a-court-case": "scale", "i-dont-feel-safe": "shield", "i-cant-stop-thinking-about-them": "moon"}.items()) + f"""
/* C's cover tiles: each choice a different hour of the night */
.where.tiles li,.more .where li{{display:flex}}.where.tiles a,.more .where a{{flex:1}}
.where.tiles{{grid-template-columns:1fr 1fr;gap:10px}}
.where.tiles a{{flex-direction:column;align-items:flex-start;justify-content:space-between;gap:14px;min-height:120px;padding:14px;
border:1px solid rgba(255,255,255,.1);border-radius:18px;color:#fff;font-size:1.1rem;line-height:1.28;background:linear-gradient(165deg,var(--t2),var(--t1))}}
.where.tiles a::before{{content:"";width:28px;height:28px;background:#fff;opacity:.92;-webkit-mask:var(--ico) center/contain no-repeat;mask:var(--ico) center/contain no-repeat}}
.where.tiles li:nth-child(1) a{{--t1:#1b1430;--t2:#3a2346}}.where.tiles li:nth-child(2) a{{--t1:#171630;--t2:#3d2c57}}
.where.tiles li:nth-child(3) a{{--t1:#141c36;--t2:#2e3c64}}.where.tiles li:nth-child(4) a{{--t1:#13203a;--t2:#2d4668}}
.where.tiles li:nth-child(5) a{{--t1:#2a1520;--t2:#5a2633}}.where.tiles li:nth-child(6) a{{--t1:#1a2e48;--t2:#4b5068}}
@media (hover:hover) and (pointer:fine){{.where.tiles a:hover{{border-color:var(--acc)}}}}
.more .where{{grid-template-columns:1fr 1fr}}
.more .where a{{min-height:64px;padding:10px 12px;font-size:1.1rem;line-height:1.28;border-radius:14px;background:linear-gradient(165deg,#2a2440,#1a1527)}}
"""

JS = f"""<script>
(function(){{var O={json.dumps(OLD['chapters'])},R={json.dumps(OLD['routes'])},h=location.hash,m;
if((m=h.match(/^#\\/c\\/(\\d+)/))&&O[m[1]])location.replace('{BASE}/'+O[m[1]]);
else if((m=h.match(/^#\\/(\\w+)/))&&R[m[1]])location.replace('{BASE}/'+R[m[1]]);
var D=document,H=D.documentElement,$$=function(q){{return D.querySelectorAll(q)}};
function leave(){{try{{document.title='New Tab';document.body.innerHTML='';}}catch(e){{}}location.replace('about:blank');}}
D.addEventListener('click',function(e){{var t=e.target.closest&&e.target.closest('[data-leave]');if(t){{e.preventDefault();leave();}}}});
addEventListener('beforeprint',function(){{$$('details').forEach(function(d){{d.open=true}})}});
var esc=0;D.addEventListener('keydown',function(e){{if(e.key!=='Escape'||D.querySelector('.nf-open,[data-nf-open]'))return;
var n=Date.now();if(n-esc<1500)leave();else esc=n;}});
/* nothing below stores anything: every setting lives in memory and resets on reload */
function steps(on){{H.classList.toggle('steps',on);$$('[data-mode]').forEach(function(b){{b.setAttribute('aria-pressed',String((b.dataset.mode==='steps')===on))}});
$$('[data-mode-toggle]').forEach(function(b){{b.setAttribute('aria-pressed',String(on));b.textContent=on?'Full read':'Just the steps'}});}}
$$('[data-mode]').forEach(function(b){{b.onclick=function(){{steps(b.dataset.mode==='steps')}}}});
$$('[data-mode-toggle]').forEach(function(b){{b.onclick=function(){{steps(!H.classList.contains('steps'))}}}});
var title0=D.title,disc=false,fav=null;$$('[data-discreet]').forEach(function(b){{b.onclick=function(){{disc=!disc;D.title=disc?'Reading':title0;
if(disc){{fav=D.createElement('link');fav.rel='icon';fav.href='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 rx=%223%22 fill=%22%23888%22/%3E%3C/svg%3E';D.head.appendChild(fav)}}
else if(fav){{D.head.removeChild(fav);fav=null}}$$('[data-discreet]').forEach(function(x){{x.setAttribute('aria-pressed',String(disc))}});}}}});
function flash(b,t,t0){{b.textContent=t;clearTimeout(b._t);b._t=setTimeout(function(){{b.textContent=t0}},2000)}}
$$('.dv-copy').forEach(function(b){{if(!navigator.clipboard){{b.hidden=true;return}}b.onclick=function(){{
var x=b.closest('.dv').querySelector('.dv-t').textContent.trim(),q=x.match(/\\u201c[^\\u201d]+\\u201d/g);if(q)x=q.map(function(s){{return s.slice(1,-1)}}).join(' ');
navigator.clipboard.writeText(x).then(function(){{flash(b,'Copied','Copy')}})}}}});
$$('[data-share]').forEach(function(b){{b.onclick=function(){{var u=location.href.split('#')[0];
if(navigator.share)navigator.share({{title:D.title,url:u}}).catch(function(){{}});
else if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){{flash(b,'Link copied','Share this page')}});}}}});
var bar=D.querySelector('.prog i');if(bar){{var f=0;addEventListener('scroll',function(){{if(f)return;f=requestAnimationFrame(function(){{f=0;
var d=H.scrollHeight-innerHeight;bar.style.transform='scaleX('+(d>0?Math.min(1,scrollY/d):0)+')'}})}},{{passive:true}});}}
}})();
</script>"""


def house():
    src = S.read(ROOT / "library/silence/index.html")
    css, chrome, js = S.house_parts(CAT.retoc(src, "longafter"))
    return css, chrome, js, S.beacon(src)


HOUSE = None


def frame(*, title, desc, url, ld, body, part, robots=None, og_type="article", extra_css=""):
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
            f'<link rel="preload" href="{BASE}/f/bookdisplay-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="preload" href="{BASE}/f/bookserif-400-700-italic.woff2" as="font" type="font/woff2" crossorigin>\n'
            "<script>document.documentElement.className+=' js'</script>\n"
            f"<style>{FONTS}{CSS}{extra_css}:root{{--s1:{s1};--s2:{s2};--acc:{acc};--dawn:{dawn}}}</style>\n{hc}\n"
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
            '<a href="/topics">All topics</a><a href="/">Noble Father Creations</a></nav>'
            '<button class="disc" type="button" data-discreet aria-pressed="false" data-js>Discreet mode</button></div></footer>\n'
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
    h2s = [(i, plain(t)) for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)]
    mins = max(1, round(len(plain(body_html + " " + m["short"]).split()) / 220))
    jump = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in h2s)
    otp = f'<details class="otp"><summary>On this page</summary><ol>{jump}</ol></details>' if len(h2s) >= 5 else ""
    title_h = html.escape(smart(c["title"]))
    end = (f'<aside class="end" aria-label="Who made this"><p>{html.escape(MANIFEST["who_made_this"])} '
           f'<a href="{MANIFEST["about_url"]}">Who made this \u2192</a></p>'
           '<p class="share" data-js>Know someone this would help? <button type="button" data-share>Share this page</button></p></aside>'
           if slug not in CRISIS else "")
    chrome = ('<div class="prog" aria-hidden="true"><i></i></div>'
              f'<nav class="rail" aria-label="This chapter"><p class="r-loc">{loc_line(c)}</p><p class="r-t">{title_h}</p>'
              + (f'<ol>{jump}</ol>' if h2s else "") +
              '<button class="leave" type="button" data-leave>Leave</button></nav>'
              '<nav class="dock" aria-label="Quick actions"><button type="button" data-mode-toggle aria-pressed="false" data-js>Just the steps</button>'
              f'<a href="{BASE}/contents">Contents</a><button class="leave" type="button" data-leave>Leave</button></nav>\n')
    body = (f'{chrome}<div class="sky"><div class="in"><p class="loc">{loc_line(c)}</p>'
            f'<h1 id="top">{title_h}</h1><p class="q">{html.escape(smart(m["question"]))}</p>'
            f'<p class="by">By <a href="{MANIFEST["about_url"]}">{MANIFEST["author"]}</a> \u00b7 Last reviewed <time datetime="{S.TODAY}">{S.TODAY_HUMAN}</time> \u00b7 <span style="white-space:nowrap">{mins} min read</span></p>'
            '<div class="hrow"><div class="tools" data-js><div class="mode" role="group" aria-label="How much to show">'
            '<button type="button" data-mode="full" aria-pressed="true">Full read</button><button type="button" data-mode="steps" aria-pressed="false">Just the steps</button></div>'
            f'<button class="disc" type="button" data-discreet aria-pressed="false">Discreet mode</button></div>{otp}</div></div></div>\n'
            f'<main id="text">{callnow}<section class="short" aria-label="The short answer"><p class="lab">The short answer</p>'
            f'<p>{(inline(m["short"]))}</p></section>\n<p class="notice">{BOOK["notice_short"]} <a href="{BASE}/how-to-use-this-book">Full notice</a>.</p>\n<article>{body_html}</article>{src_html}{nxt}{end}</main>')
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
        if not head.startswith("If you only have"):
            items.append(head.strip())
    return items


def index_html():
    graph = [dict(S.book_node(BOOK, [CH[s] for s in ORDER]), **{"mainEntityOfPage": URL}),
             {"@type": "WebPage", "@id": URL, "url": URL, "name": "The Long After: Post-Separation Abuse After Leaving",
              "description": BOOK["description"], "inLanguage": "en", "about": {"@id": URL + "#book"},
              "dateModified": S.TODAY, "isAccessibleForFree": True, "license": S.LICENSE_URL}, S.PERSON, S.ORG]
    wl = [f'<li><a href="{BASE}/where-are-you-right-now#{S.slugify(h, 60)}">{html.escape(h)}</a></li>' for h in where_items()]
    where = '<ul class="where tiles">' + "".join(wl[:6]) + "</ul>" + ('<details class="more"><summary>More situations</summary><ul class="where">' + "".join(wl[6:]) + "</ul></details>" if len(wl) > 6 else "")
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
                 ld={"@context": "https://schema.org", "@graph": graph}, body=body, part="start", og_type="book", extra_css=COVER_CSS)


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


def share_card():
    """1200x630 share card in the book's own Dusk colours and fonts, with the author's logo and name (scripts/seo/seo_common.make_og)."""
    n = sum(1 for c in PLAN["chapters"] if c["part"] not in ("start", "tools"))
    card = {"slug": "longafter", "title": "The Long After", "fonts": ["bookdisplay", "bookserif"],
            "theme": {"bg": "#1b1430", "fg": "#F4EEE6", "fg2": "#CBBFB6", "panel": "#241a3a", "glow": "#3a2346", "acc": "#e0957a",
                      "disp": "'bookdisplay',Georgia,serif", "body": "'bookserif',Georgia,serif"}}
    S.make_og(card, OUT, f"Free to read \u00b7 second edition \u00b7 {n} chapters", "What happens once you've left.")


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
    if "--og" in sys.argv:
        share_card()
    print(f"longafter v5: {len(ORDER)} pages + index, contents, search, all; {len(stale)} stale pages removed; sitemap {len(urls)} URLs")


if __name__ == "__main__":
    main()
