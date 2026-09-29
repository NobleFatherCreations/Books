#!/usr/bin/env python3
"""The Sacred Divide — one-page-scroll redesign (undeployed).

Generates, from the same content/sacred-divide/religions/*.md the PDFs use:

  index.html      The family home: the ten families as numbered cards, each listing its traditions
                  with the question that tradition's page could not answer.
  <id>.html       One continuous scroll page per religion, all 27 sections, each opened by a short
                  "Before you read" note and closed by a "Why this matters to you" caption
                  (scripts/sacred_divide_narration.py — the same text the expanded PDFs carry).
                  A section jump menu (a rail on wide screens, a sheet on phones); a persistent
                  family bar whose arrows go to the previous/next tradition in the same family AND
                  land on the section you are reading; the PDF download (one edition: the full record with this narration) at the top.

House rules honoured: every page is self-contained (fonts subset and inlined as base64, CSS and JS
inline, no external requests, no storage); dark theme; one accent (the brass shared with the
site-wide Catalogue); two type families (Newsreader for reading, Codex Display for headings);
NO reading-progress bar (BOOKS.md: this book refuses one, as part of its anti-tracking stance); ~66ch measure; 8px spacing grid; scroll-triggered fades that switch
off under prefers-reduced-motion; THE HOUSE / Catalogue drawer from scripts/nf-install-chrome.py,
so it is the same component the other books carry rather than a hand-pasted copy.

Links. Pages are served under a clean path (e.g. /faith/judaism), and a relative link resolves
differently at /faith/judaism and /faith/judaism/ (see CLAUDE.md). So every internal link and PDF
link is built from BASE. The default ('' + relative PDF paths) is for local preview from this
folder; for a deploy pass --base /faith/ --pdf-base /faith/pdf/ so every link is absolute.

Usage:  python3 scripts/sacred-divide-site.py [--base /faith/] [--pdf-base /faith/pdf/] [--ext .html|'']
Output: library/_undeployed/sacred-divide-redesign/
"""
import base64
import html as H
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'library/_undeployed/sacred-divide-redesign')
FONTS = os.path.join(ROOT, 'tools/pdf/fonts')
PDFDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-pdf')


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


exp = load('sdexp', 'sacred-divide-pdf-expanded.py')      # build_sections(): the narrated page body
exporter = load('sdexport', 'sacred-divide-export-md.py')   # FAMILIES
chrome = load('nfchrome', 'nf-install-chrome.py')           # THE HOUSE / Catalogue component
narr = exp.narr
sdp = exp.sdp
FAMILIES = exporter.FAMILIES


def arg(flag, default):
    a = sys.argv[1:]
    return a[a.index(flag) + 1] if flag in a else default


BASE = arg('--base', '')                                   # '' = relative (local preview)
PDF_BASE = arg('--pdf-base', '../sacred-divide-pdf/expanded/')
# One PDF edition only: the full record with the reader narration. The live build publishes each as
# pdf/<id>.pdf (--pdf-flat); the local preview links the build output, <id>-expanded.pdf.
PDF_FLAT = '--pdf-flat' in sys.argv[1:]


def pdf_href(rid):
    return f'{PDF_BASE}{rid}.pdf' if PDF_FLAT else f'{PDF_BASE}{rid}-expanded.pdf'
EXT = arg('--ext', '.html')
OUT = arg('--out', OUT)
LIVE = '--live' in sys.argv[1:]
# The owner's standing decision for the live site (sites.json, 2026-09-27): keep Cloudflare's
# anonymous visit counter and state it plainly. Added to the live build only, never to previews.
BEACON = ('<script defer type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
          'data-cf-beacon=\'{"token": "c8d1aea530814aea8c7a92baa2accef3"}\'></script>')
VERSION, RELEASED = 'v4', '2026-09-29'
# the earlier single-page codex, published alongside as the reference edition (live: <base>codex)
CODEX_HREF = f'{BASE}codex{EXT}' if LIVE else '../sacred-divide-v4-factchecked.html'


def e(t):
    return H.escape(str(t), quote=True)


def href(rid, anchor=''):
    return f'{BASE}{rid}{EXT}' + (f'#{anchor}' if anchor else '')


def home():
    return f'{BASE}index{EXT}' if EXT else (BASE or './')


# ---------------------------------------------------------------- fonts: subset to the characters used, inline
def font_css(text):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    chars = set(text) | set(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:!?\'"()[]-–—…‘’“”·/&%$#@*+=<>|')
    unicodes = sorted(ord(c) for c in chars if ord(c) > 31)
    try:
        import brotli  # noqa: F401
        flavor, mime = 'woff2', 'font/woff2'
    except ImportError:
        flavor, mime = 'woff', 'font/woff'
    out = []
    for fam, file, style in [('Newsreader', 'Newsreader[opsz,wght].ttf', 'normal'),
                             ('Newsreader', 'Newsreader-Italic[opsz,wght].ttf', 'italic'),
                             ('Codex Display', 'codex-display.woff', 'normal')]:
        f = TTFont(os.path.join(FONTS, file))
        opts = subset.Options()
        opts.flavor = flavor
        opts.layout_features = ['kern', 'liga', 'onum', 'lnum', 'smcp', 'c2sc']
        opts.notdef_outline = True
        s = subset.Subsetter(opts)
        s.populate(unicodes=unicodes)
        s.subset(f)
        buf = io.BytesIO()
        f.flavor = flavor
        f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        weight = '200 800' if fam == 'Newsreader' else '400'
        out.append(f"@font-face{{font-family:'{fam}';src:url(data:{mime};base64,{b64}) format('{flavor}');"
                   f"font-weight:{weight};font-style:{style};font-display:swap}}")
    return '\n'.join(out)


# ---------------------------------------------------------------- shared CSS / JS
CSS = r"""
:root{
  --bg:#141010; --bg2:#1C1716; --surface:#221C1A; --surface2:#2A2320; --ink:#ECE4D6; --ink2:#BCB1A0; --ink3:#8A8071;
  --line:rgba(201,163,91,.18); --line2:rgba(236,228,214,.10);
  --acc:#C9A35B; --acc-bright:#E8C879; --acc-soft:rgba(201,163,91,.10);
  --paper:#F3EDE1; --paper-ink:#241E17;
  --gY:#2F6B3A; --gP:#8A6A1F; --gN:#8E2B26; --gQ:#4A4440;
  --serif:'Newsreader',Georgia,'Times New Roman',serif; --display:'Codex Display','Newsreader',Georgia,serif;
  --mono:ui-monospace,'SFMono-Regular',Menlo,monospace;
  --measure:66ch; --ease:cubic-bezier(.2,.7,.2,1);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font:400 19px/1.62 var(--serif);font-optical-sizing:auto;
  font-variant-numeric:oldstyle-nums proportional-nums;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--acc-bright);text-decoration:underline;text-decoration-color:rgba(232,200,121,.35);text-underline-offset:3px;
  transition:color .2s var(--ease),text-decoration-color .2s var(--ease)}
a:hover{text-decoration-color:var(--acc-bright)}
a:focus-visible,button:focus-visible{outline:2px solid var(--acc-bright);outline-offset:3px;border-radius:4px}
strong{font-weight:650;color:#fff}
p{margin:0 0 16px}
ul,ol{margin:0 0 16px;padding-left:24px}
li{margin:0 0 8px}
li::marker{color:var(--acc)}
h3{font:400 28px/1.2 var(--display);margin:48px 0 16px;color:var(--ink);letter-spacing:.005em}
h4{font:600 14px/1.4 var(--serif);letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin:32px 0 8px}
.skip{position:absolute;left:-9999px;top:8px;background:var(--acc);color:#141010;padding:8px 16px;z-index:10000}
.skip:focus{left:8px}

/* top bar. No reading-progress bar: BOOKS.md records that this book refuses one (anti-tracking stance). */
.bar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:16px;height:56px;padding:0 24px;
  background:rgba(20,16,16,.88);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line2)}
.bar .home{font:400 18px/1 var(--display);color:var(--ink);text-decoration:none;white-space:nowrap}
.bar .where{flex:1;min-width:0;font-size:14px;color:var(--ink3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:.04em}
.bar .where b{color:var(--ink2);font-weight:500}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:8px 16px;border-radius:999px;border:1px solid var(--line);
  background:transparent;color:var(--ink);font:500 15px/1 var(--serif);cursor:pointer;text-decoration:none;
  transition:background .2s var(--ease),border-color .2s var(--ease),transform .2s var(--ease)}
.btn:hover{background:var(--acc-soft);border-color:var(--acc)}
.btn:active{transform:translateY(1px)}
.btn svg{width:16px;height:16px;flex:none}
.btn.solid{background:var(--acc);color:#141010;border-color:var(--acc);font-weight:600}
.btn.solid:hover{background:var(--acc-bright);border-color:var(--acc-bright)}

/* layout: rail + reading column */
.wrap{display:grid;grid-template-columns:1fr;max-width:1240px;margin:0 auto;padding:0 24px}
@media (min-width:1100px){.wrap{grid-template-columns:248px minmax(0,1fr);gap:64px}}
.rail{display:none}
@media (min-width:1100px){.rail{display:block;position:sticky;top:80px;align-self:start;max-height:calc(100vh - 96px);overflow:auto;padding:24px 0 96px;scrollbar-width:thin}}
.toc{list-style:none;margin:0;padding:0;counter-reset:none}
.toc li{margin:0}
.toc a{display:grid;grid-template-columns:32px 1fr;gap:8px;padding:6px 8px;border-radius:8px;text-decoration:none;color:var(--ink3);
  font-size:15px;line-height:1.3;transition:color .2s var(--ease),background .2s var(--ease)}
.toc a .n{font-variant-numeric:lining-nums tabular-nums;color:var(--ink3);font-size:13px;padding-top:2px}
.toc a:hover{color:var(--ink);background:var(--acc-soft)}
.toc a[aria-current="true"]{color:var(--ink);background:var(--acc-soft)}
.toc a[aria-current="true"] .n{color:var(--acc)}
.rail h2{font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px 8px}
main{min-width:0;padding-bottom:160px}
.col{max-width:var(--measure)}

/* hero */
.hero{padding:88px 0 56px;border-bottom:1px solid var(--line2);margin-bottom:24px}
.eyebrow{font:600 13px/1.4 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--acc)}
.hero h1{font:400 clamp(48px,9vw,104px)/.95 var(--display);margin:16px 0 24px;letter-spacing:-.01em;color:#F6EFE4;text-wrap:balance}
.hero .blurb{font:italic 400 clamp(20px,2.4vw,24px)/1.5 var(--serif);color:var(--ink2);max-width:40ch;margin:0 0 32px}
.hero .dl{display:flex;flex-wrap:wrap;gap:16px;margin:0 0 24px}
.hero .meta{font-size:14px;color:var(--ink3);letter-spacing:.03em}
.hero .fam{margin-top:32px;font-size:15px;color:var(--ink3)}
.hero .fam a{color:var(--ink2)}
.hero .fam a[aria-current="page"]{color:var(--acc-bright);text-decoration:none;font-weight:600}

/* sections */
section.sec{padding:80px 0 24px;border-bottom:1px solid var(--line2)}
.sec-head{margin:0 0 32px}
.sec-head .num{display:block;font:600 13px/1 var(--serif);letter-spacing:.24em;text-transform:uppercase;color:var(--acc);margin:0 0 16px;
  font-variant-numeric:lining-nums tabular-nums}
.sec-head h2{font:400 clamp(36px,5.4vw,56px)/1.05 var(--display);margin:0;color:#F6EFE4;text-wrap:balance}
.reveal{transition:opacity .6s var(--ease),transform .6s var(--ease)}
.js .reveal.pending{opacity:0;transform:translateY(16px)}
@media (prefers-reduced-motion:reduce){.js .reveal.pending{opacity:1;transform:none}.reveal{transition:none}}

/* narration */
.box.intro{background:transparent;border:0;border-left:2px solid var(--line);padding:0 0 0 24px;margin:0 0 40px;max-width:var(--measure)}
.box .lbl{display:block;font:600 12px/1.4 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--ink3);margin:0 0 8px}
.box.intro p{font-size:17px;line-height:1.6;color:var(--ink2);margin:0}
.box.foryou{position:relative;max-width:var(--measure);margin:56px 0 24px;padding:32px 32px 24px;background:linear-gradient(180deg,var(--surface2),var(--surface));
  border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:4px 16px 16px 4px}
.box.foryou .lbl{color:var(--acc);font-size:13px}
.box.foryou p{font-size:20px;line-height:1.6;color:var(--ink)}
.box.foryou p:last-child{margin:0}
.box.foryou em{color:var(--acc-bright)}

/* content boxes from the markdown */
.body > p,.body > ul,.body > ol,.body > h3,.body > h4,.body > .box.card,.body > .box.case,.body > .box.tell,.body > .box.lede,
.body > .box.question,.body > .box.stage,.body > .box.cites,.body > figure{max-width:var(--measure)}
.box{margin:0 0 24px}
.box.lede p{font:italic 400 23px/1.55 var(--serif);color:var(--ink)}
.box.question{padding:24px 0 24px 24px;border-left:3px solid var(--acc)}
.box.question p{font:400 clamp(24px,3vw,30px)/1.35 var(--display);color:#F6EFE4;margin:0}
.box.tell{padding:16px 24px;background:var(--acc-soft);border-radius:8px;font-style:italic;color:var(--ink)}
.box.cites{font-size:14px;color:var(--ink3)}
.box.card,.box.case,.box.tactic{background:var(--surface);border:1px solid var(--line2);border-radius:12px;padding:24px 24px 8px;margin:0 0 24px}
.box.card h3,.box.case h3{font-size:24px;margin:0 0 16px}
.box.case li strong:first-child,.box.card li strong:first-child{color:var(--acc);font-weight:600;font-size:14px;letter-spacing:.08em;text-transform:uppercase}
.box.case ul,.box.card ul{list-style:none;padding:0}
.box.stage{border-top:1px solid var(--line);padding-top:16px;margin-top:48px;color:var(--ink2)}
.box.stage strong{color:var(--acc-bright)}
.box.tactic h4{font:400 24px/1.25 var(--display);text-transform:none;letter-spacing:0;color:#F6EFE4;margin:0 0 8px}
.box.tactic{scroll-margin-top:80px}
.box.hardq{background:var(--surface);border:1px solid var(--line2);border-top:3px solid var(--acc);border-radius:4px 4px 12px 12px;padding:32px;margin:0 0 32px;max-width:var(--measure)}
.hardq .qn{font:600 12px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px}
.hardq .qtext{font:400 clamp(24px,3vw,30px)/1.35 var(--display);color:#F6EFE4;margin:0 0 24px}
.hardq h4{margin:24px 0 8px}
.hardq h4.ex{color:var(--ink2)}
.hardq p{font-size:18px}

/* tables scroll inside their own box, never the page */
.tw{overflow-x:auto;margin:0 0 32px;border:1px solid var(--line2);border-radius:12px;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:16px;line-height:1.5;min-width:520px}
.glance table,.score-wrap table{min-width:0}
th{font:600 12px/1.3 var(--serif);letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);text-align:left;padding:16px;border-bottom:1px solid var(--line)}
td{padding:16px;vertical-align:top;border-bottom:1px solid var(--line2)}
tr:last-child td{border-bottom:0}
.glance table thead{display:none}
.glance td:first-child{width:30%;font:600 13px/1.4 var(--serif);letter-spacing:.12em;text-transform:uppercase;color:var(--acc)}
table.score td{text-align:center;font:600 20px/1 var(--serif);color:#fff}
td.sY{background:var(--gY)} td.sP{background:var(--gP)} td.sN{background:var(--gN)} td.sQ{background:var(--gQ)}

/* chips, receipts, cites */
.chip{display:inline-block;font:600 11px/1.6 var(--serif);letter-spacing:.12em;text-transform:uppercase;padding:0 8px;border:1px solid;border-radius:6px;margin-right:4px;white-space:nowrap;vertical-align:2px}
.g-codified{background:#7E1F2B;border-color:#7E1F2B;color:#fff}.g-documented{background:#3B4A6B;border-color:#3B4A6B;color:#fff}
.g-taught{color:#E1C47F;border-color:#96772F}.g-cultural{color:#CBBFAE;border-color:#8A8071}.g-contested{color:#C7A9E6;border-color:#6B4A8A}
.g-reformed{color:#8FCB98;border-color:#2F6B3A}.g-ungraded{color:#9A938A;border-color:#5A544D;border-style:dashed}
.rcpt{font:600 11px/1.6 var(--serif);letter-spacing:.1em;color:var(--acc);border:1px solid var(--line);border-radius:6px;padding:0 6px}
.rcpt i{font:italic 400 13px var(--serif);letter-spacing:0;color:var(--ink2)}
a.cite{font-size:12px;vertical-align:super;line-height:0;padding:0 2px;text-decoration:none;font-variant-numeric:lining-nums}
a.ext{word-break:break-word}
a.tlink{font-size:15px}

/* graphics: charts are drawn for paper, so they sit on a paper plate */
figure.fig{background:var(--paper);color:var(--paper-ink);border-radius:12px;padding:24px;margin:0 0 32px;max-width:var(--measure)}
figure.fig .ftitle{font:400 20px/1.3 var(--display);margin:0 0 8px}
figure.fig figcaption{font-size:13px;color:#6C6154;margin-top:8px}
figure.fig svg{max-width:100%;height:auto}
.tl{list-style:none;padding:0 0 0 24px;margin:0 0 32px;border-left:2px solid var(--line);max-width:var(--measure)}
.tl li{position:relative;padding:0 0 24px 16px}
.tl li::before{content:attr(data-n);position:absolute;left:-37px;top:2px;width:24px;height:24px;border-radius:50%;background:var(--acc);color:#141010;
  font:600 12px/24px var(--serif);text-align:center;font-variant-numeric:lining-nums}
.tl .d{display:block;font:600 13px/1.4 var(--serif);letter-spacing:.14em;text-transform:uppercase;color:var(--acc)}
.tl .e{display:block;font:400 21px/1.35 var(--display);color:#F6EFE4}
.tl .r{display:block;font:italic 16px/1.5 var(--serif);color:var(--ink2)}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px 24px;margin:0 0 40px}
.tgrid a{display:flex;gap:8px;align-items:baseline;font-size:15px;padding:8px 0;border-bottom:1px solid var(--line2);text-decoration:none;color:var(--ink2)}
.tgrid a:hover{color:var(--ink)}
.tgrid .n{color:var(--acc);width:24px;font-variant-numeric:lining-nums}
.tgrid .nm{flex:1}
#sources ol li{font-size:15px;color:var(--ink2);scroll-margin-top:80px}
#sources ol li:target{color:var(--ink);background:var(--acc-soft);border-radius:6px}

/* family bar: previous / next tradition in the same family, landing on the same section */
.famnav{position:fixed;left:16px;right:88px;bottom:16px;z-index:40;display:flex;justify-content:center;pointer-events:none}
.famnav .inner{pointer-events:auto;display:flex;align-items:center;gap:4px;max-width:100%;padding:4px;border-radius:999px;
  background:rgba(34,28,26,.94);border:1px solid var(--line);box-shadow:0 8px 32px rgba(0,0,0,.45);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.famnav a{display:flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px;border-radius:999px;text-decoration:none;color:var(--ink);
  font-size:15px;white-space:nowrap;min-width:0;transition:background .2s var(--ease)}
.famnav a:hover{background:var(--acc-soft)}
.famnav a span{overflow:hidden;text-overflow:ellipsis}
.famnav svg{width:18px;height:18px;flex:none;color:var(--acc)}
.famnav .mid{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);padding:0 8px;white-space:nowrap}
.famnav .sheet-btn{border:0;background:transparent;color:var(--ink);min-height:44px;padding:8px 16px;border-radius:999px;cursor:pointer;font:500 15px var(--serif);display:flex;gap:8px;align-items:center}
.famnav .sheet-btn:hover{background:var(--acc-soft)}
@media (min-width:1100px){.famnav .sheet-btn{display:none}}
@media (max-width:640px){.famnav .mid{display:none}.famnav a{padding:8px 12px}.famnav a .lab{display:none}}

/* section sheet (phones and tablets) */
.sheet{position:fixed;inset:0;z-index:9000;display:none}
.sheet.open{display:block}
.sheet .scrim{position:absolute;inset:0;background:rgba(0,0,0,.6)}
.sheet .panel{position:absolute;left:0;right:0;bottom:0;max-height:80vh;overflow:auto;background:var(--bg2);border-top:1px solid var(--line);
  border-radius:16px 16px 0 0;padding:24px 16px 32px;transform:translateY(0);animation:sheetin .3s var(--ease)}
@keyframes sheetin{from{transform:translateY(24px);opacity:0}to{transform:none;opacity:1}}
@media (prefers-reduced-motion:reduce){.sheet .panel{animation:none}}
.sheet .panel h2{font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px 8px}
.sheet .close{position:absolute;right:16px;top:16px}

/* home */
.home-hero{max-width:1240px;margin:0 auto;padding:120px 24px 64px}
.home-hero h1{font:400 clamp(56px,11vw,136px)/.92 var(--display);margin:24px 0 32px;color:#F6EFE4;letter-spacing:-.015em}
.home-hero .lead{font:italic 400 clamp(21px,2.6vw,26px)/1.5 var(--serif);color:var(--ink2);max-width:44ch;margin:0 0 32px}
.home-hero .how{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:24px;max-width:960px;margin:48px 0 0;padding:0;list-style:none}
.home-hero .how li{border-top:1px solid var(--line);padding:16px 0 0;color:var(--ink2);font-size:17px}
.home-hero .how b{display:block;color:var(--ink);font-weight:600;margin-bottom:4px}
.families{max-width:1240px;margin:0 auto;padding:0 24px 160px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}
@media (max-width:420px){.families{grid-template-columns:1fr}}
.family{background:var(--surface);border:1px solid var(--line2);border-radius:16px;padding:32px 24px 16px;transition:border-color .2s var(--ease),transform .2s var(--ease)}
.family:hover{border-color:var(--line)}
.family .fnum{font:600 13px/1 var(--serif);letter-spacing:.24em;text-transform:uppercase;color:var(--acc);font-variant-numeric:lining-nums}
.family h2{font:400 32px/1.1 var(--display);margin:16px 0 24px;color:#F6EFE4}
.family ol{list-style:none;margin:0;padding:0}
.family li{margin:0;border-top:1px solid var(--line2)}
.family li a{display:block;padding:16px 8px;margin:0 -8px;border-radius:8px;text-decoration:none;transition:background .2s var(--ease)}
.family li a:hover{background:var(--acc-soft)}
.family li .nm{display:block;font:400 22px/1.2 var(--display);color:var(--ink)}
.family li .uq{display:block;font-size:15px;line-height:1.5;color:var(--ink3);margin-top:4px}
footer.colophon{max-width:1240px;margin:0 auto;padding:48px 24px 120px;color:var(--ink3);font-size:15px;border-top:1px solid var(--line2)}
footer.colophon h2{font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px}
.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:2px 12px;color:var(--acc);font-size:13px;letter-spacing:.06em}
@media (max-width:640px){body{font-size:18px}.bar{padding:0 16px;gap:8px}.bar .where{display:none}.wrap{padding:0 16px}
  .hero{padding:56px 0 40px}.box.foryou{padding:24px 20px 16px}.box.foryou p{font-size:18px}.box.hardq{padding:24px 20px}
  .box.card,.box.case,.box.tactic{padding:20px 16px 4px}.home-hero{padding:72px 16px 40px}.families{padding:0 16px 120px}}
"""

ICON = {
    'down': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg>',
    'left': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    'right': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    'list': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/></svg>',
    'x': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
}

JS = r"""
(function(){
  var d=document, root=d.documentElement;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('js');
  /* fades: only elements below the fold start hidden. A scroll check (not an IntersectionObserver)
     reveals everything at or above the bottom of the screen, so a fast fling that jumps an element
     from below the screen to above it between two frames can never leave it invisible. */
  if(!reduce){
    var pend=[].slice.call(d.querySelectorAll('.reveal')).filter(function(el){ return el.getBoundingClientRect().top>innerHeight; });
    pend.forEach(function(el){ el.classList.add('pending'); });
    var ticking=false;
    function reveal(){ ticking=false;
      /* at the very bottom nothing can scroll further up, so everything left is shown */
      var lim=(scrollY+innerHeight>=root.scrollHeight-2)?Infinity:innerHeight*0.94;
      pend=pend.filter(function(el){ if(el.getBoundingClientRect().top<lim){ el.classList.remove('pending'); return false; } return true; }); }
    addEventListener('scroll',function(){ if(!ticking&&pend.length){ ticking=true; requestAnimationFrame(reveal); } },{passive:true});
    addEventListener('resize',reveal);
  }
  /* current section: highlights the menu, names it in the bar, and re-aims the family arrows */
  var secs=[].slice.call(d.querySelectorAll('section.sec')), links=[].slice.call(d.querySelectorAll('.toc a')),
      where=d.querySelector('.bar .where b'), fam=[].slice.call(d.querySelectorAll('.famnav a[data-rid]'));
  function setCur(id){
    links.forEach(function(a){ a.setAttribute('aria-current', a.getAttribute('href').slice(a.getAttribute('href').indexOf('#')+1)===id ? 'true':'false'); });
    fam.forEach(function(a){ a.href=a.getAttribute('data-href')+'#'+id; });
    var s=d.getElementById(id); if(where&&s) where.textContent=s.getAttribute('data-title');
  }
  if('IntersectionObserver' in window && secs.length){
    var so=new IntersectionObserver(function(es){ es.forEach(function(x){ if(x.isIntersecting) setCur(x.target.id); }); },{rootMargin:'-35% 0px -60% 0px'});
    secs.forEach(function(s){so.observe(s);});
  }
  if(location.hash && d.getElementById(location.hash.slice(1))){ var t=d.getElementById(location.hash.slice(1)).closest('section.sec'); if(t) setCur(t.id); }
  /* section sheet */
  var sheet=d.querySelector('.sheet'), opener=null;
  function openSheet(){ if(!sheet) return; opener=d.activeElement; sheet.classList.add('open'); var c=sheet.querySelector('[aria-current="true"]')||sheet.querySelector('a'); if(c) c.focus(); }
  function closeSheet(){ if(!sheet) return; sheet.classList.remove('open'); if(opener) opener.focus(); }
  d.querySelectorAll('[data-open-sheet]').forEach(function(b){ b.addEventListener('click',openSheet); });
  if(sheet){ sheet.querySelector('.scrim').addEventListener('click',closeSheet); sheet.querySelector('.close').addEventListener('click',closeSheet);
    sheet.querySelectorAll('a').forEach(function(a){ a.addEventListener('click',function(){ sheet.classList.remove('open'); }); });
    d.addEventListener('keydown',function(ev){ if(ev.key==='Escape'&&sheet.classList.contains('open')) closeSheet(); }); }
})();
"""



# ================================================================ refinement pass (2026-09-28)
# Owner's brief: keep the information the focal point, but make its display feel refined — small,
# deliberate luxury details rather than decoration. Everything below either clarifies a piece of
# evidence (the dossier, the seals, the docket, the contact cards, source pop-ups) or is a quiet
# material detail (hairline gilt rules, paper grain, outlined numerals, pull-questions).
REFINE_CSS = r"""
::selection{background:rgba(232,200,121,.28);color:#fff}
p,li,dd{text-wrap:pretty} h1,h2,h3,.qtext{text-wrap:balance}
html{hanging-punctuation:first}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.05;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 .95 0 0 0 0 .85 0 0 0 .55 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
/* the grain sits at z-index 1; reading layers sit above it without losing their own positioning */
main{position:relative;z-index:2} .rail{z-index:2} .bar{z-index:50}
.pop{position:absolute}
td,th,.tl .d,.dossier dd{font-variant-numeric:lining-nums proportional-nums}
table td{font-variant-numeric:lining-nums tabular-nums}
tbody tr{transition:background .2s var(--ease)} tbody tr:hover{background:rgba(236,228,214,.03)}

/* No content-visibility here on purpose: its estimated heights made section jumps (menu, family
   arrows, compare) land one section early on phones. Correct navigation beats the paint saving. */

/* section openers: outlined numeral, kicker, title, compare */
section.sec{border-bottom:0;padding-top:96px}
section.sec::before{content:"";display:block;height:16px;margin:0 0 64px;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16'%3E%3Cpath d='M8 1 15 8 8 15 1 8z' fill='none' stroke='%23C9A35B' stroke-width='1'/%3E%3C/svg%3E") center/16px no-repeat,
  linear-gradient(90deg,transparent,rgba(201,163,91,.35) 30%,rgba(201,163,91,.35) 70%,transparent) center/100% 1px no-repeat}
section.sec:first-of-type::before{display:none}
.sec-head{display:grid;grid-template-columns:auto 1fr;align-items:end;column-gap:24px;row-gap:8px;margin:0 0 40px}
.sec-head .numeral{font:400 clamp(72px,11vw,128px)/.8 var(--display);color:transparent;-webkit-text-stroke:1px rgba(201,163,91,.55);
  font-variant-numeric:lining-nums;letter-spacing:-.02em;user-select:none}
@supports not (-webkit-text-stroke:1px black){.sec-head .numeral{color:rgba(201,163,91,.35)}}
.sec-head .st{min-width:0;padding-bottom:4px}
.sec-head .num{margin:0 0 8px;font-size:12px}
.sec-head{grid-template-columns:auto 1fr auto}
.sec-head .tools{display:flex;gap:8px;align-self:end;padding-bottom:10px}
@media (max-width:760px){.sec-head{grid-template-columns:auto 1fr}.sec-head .tools{grid-column:1/-1;padding-bottom:0}}
.cmp-btn{display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);
  background:transparent;color:var(--ink2);font:500 14px/1 var(--serif);letter-spacing:.02em;cursor:pointer;
  transition:color .2s var(--ease),border-color .2s var(--ease),background .2s var(--ease)}
.cmp-btn:hover{color:var(--ink);border-color:var(--acc);background:var(--acc-soft)}
.cmp-btn svg{width:16px;height:16px;color:var(--acc)}

/* buttons: a little material */
.btn.solid{background:linear-gradient(180deg,#D9B66E,#B8924A);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 1px 0 rgba(0,0,0,.4)}
.btn.solid:hover{background:linear-gradient(180deg,#E8C879,#C9A35B)}

/* hero: the evidence stamp */
.hero{position:relative}
.stamp{position:absolute;right:0;top:72px;width:136px;height:136px;color:var(--acc);opacity:.85;transition:transform .6s var(--ease)}
.stamp:hover{transform:rotate(-12deg)}
@media (max-width:760px){.stamp{display:none}}
@media (prefers-reduced-motion:reduce){.stamp{transition:none}.stamp:hover{transform:none}}

/* 01 · the dossier */
.dossier{margin:0 0 40px;border-top:3px double var(--line);border-bottom:1px solid var(--line);max-width:var(--measure)}
.dossier .dr{display:grid;grid-template-columns:176px 1fr;gap:24px;padding:16px 0;border-top:1px solid var(--line2)}
.dossier .dr:first-child{border-top:0}
.dossier dt{font:600 12px/1.6 var(--serif);letter-spacing:.18em;text-transform:uppercase;color:var(--acc);padding-top:4px}
.dossier dd{margin:0;font-size:19px;line-height:1.5;color:var(--ink)}
@media (max-width:640px){.dossier .dr{grid-template-columns:1fr;gap:4px}}
.uq-pull{margin:0 0 48px;padding:32px 0 32px 40px;position:relative;max-width:var(--measure);border-left:1px solid var(--line)}
.uq-pull::before{content:"\201C";position:absolute;left:-12px;top:-8px;font:400 96px/1 var(--display);color:var(--acc);opacity:.6;background:var(--bg);padding:0 4px}
.uq-pull .lbl{display:block;font:600 12px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px}
.uq-pull p{font:italic 400 clamp(24px,3vw,32px)/1.35 var(--serif);color:#F6EFE4;margin:0}

/* the scorecard as six stamped seals */
.seals{list-style:none;display:grid;grid-template-columns:repeat(6,1fr);gap:16px;padding:0;margin:0 0 24px;max-width:880px}
@media (max-width:760px){.seals{grid-template-columns:repeat(3,1fr);gap:24px 8px}}
.seals li{margin:0;text-align:center}
.seal{width:72px;height:72px;margin:0 auto 12px;border-radius:50%;display:grid;place-items:center;position:relative;
  font:400 30px/1 var(--display);border:1px solid currentColor;box-shadow:inset 0 0 0 4px var(--bg),inset 0 0 0 5px currentColor}
.seal::after{content:"";position:absolute;inset:-6px;border-radius:50%;border:1px dashed currentColor;opacity:.35}
.s-Y .seal{color:#8FCB98;background:rgba(47,107,58,.18)} .s-P .seal{color:#E1C47F;background:rgba(138,106,31,.18)}
.s-N .seal{color:#E3877D;background:rgba(142,43,38,.2)} .s-Q .seal{color:#9A938A;background:rgba(74,68,64,.25)}
.seals b{display:block;font:600 12px/1.35 var(--serif);letter-spacing:.14em;text-transform:uppercase;color:var(--ink2)}
.seals .v{display:block;font-size:15px;color:var(--ink3);margin-top:2px}
.seals .note{display:block;font-size:13px;color:var(--ink3);margin-top:4px;line-height:1.35}

/* 02 · a day inside opens like a book */
.dropcap::first-letter{float:left;font:400 5.2em/.8 var(--display);margin:.06em .1em 0 0;color:var(--acc-bright)}

/* 19 · cases as dockets */
.box.case{border-left:3px solid var(--acc);border-radius:4px 12px 12px 4px}
.box.case h3 .dk{display:block;font:600 12px/1.4 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--acc);margin:0 0 8px}
.box.case li,.box.card li{position:relative;padding-left:112px;margin:0 0 12px}
.box.case li strong:first-child,.box.card li strong:first-child{position:absolute;left:0;top:.35em;width:100px;font-size:12px;line-height:1.3}
@media (max-width:640px){.box.case li,.box.card li{padding-left:0}.box.case li strong:first-child,.box.card li strong:first-child{position:static;display:block;width:auto;margin-bottom:2px}}

/* 25 · where to get help: contact cards */
.contacts{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin:0 0 32px}
.contact{background:var(--surface);border:1px solid var(--line2);border-radius:12px;padding:24px;display:flex;flex-direction:column;gap:8px}
.contact h4{font:400 24px/1.2 var(--display);text-transform:none;letter-spacing:0;color:#F6EFE4;margin:0}
.contact .for{color:var(--ink2);font-size:16px;line-height:1.45}
.contact .where{font:600 12px/1.4 var(--serif);letter-spacing:.16em;text-transform:uppercase;color:var(--ink3)}
.contact .how{margin-top:auto;padding-top:8px;font-size:17px}
.contact a.tel{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px;border-radius:999px;border:1px solid var(--acc);
  color:var(--acc-bright);text-decoration:none;font-weight:600;font-variant-numeric:lining-nums tabular-nums}
.contact a.tel:hover{background:var(--acc-soft)}
.contact a.tel svg{width:16px;height:16px}

/* captions: the closing question as a pull-question */
.box.foryou .pq{display:block;margin-top:16px;padding-top:16px;border-top:1px solid var(--line);font:italic 400 clamp(21px,2.4vw,24px)/1.45 var(--serif);color:var(--acc-bright)}
.box.foryou .pq-tail{display:block;margin-top:8px;font-size:17px;color:var(--ink2)}
.box.foryou .lbl::before{content:"";display:inline-block;width:8px;height:8px;margin-right:10px;transform:rotate(45deg) translateY(-2px);border:1px solid var(--acc)}

/* take-away questions */
.takeaway{max-width:var(--measure);margin:96px 0 0;padding:40px 32px;border:1px solid var(--line);border-radius:16px;background:var(--surface)}
.takeaway h2{font:400 clamp(32px,4vw,44px)/1.1 var(--display);margin:8px 0 16px;color:#F6EFE4}
.takeaway ol{padding-left:0;list-style:none;counter-reset:q}
.takeaway li{counter-increment:q;position:relative;padding:12px 0 12px 48px;border-top:1px solid var(--line2);font-size:17px}
.takeaway li::before{content:counter(q,decimal-leading-zero);position:absolute;left:0;top:14px;font:600 13px/1 var(--serif);color:var(--acc);font-variant-numeric:lining-nums tabular-nums}
.takeaway li a{color:var(--ink3);font-size:13px;letter-spacing:.06em;text-decoration:none;margin-left:6px}
@media print{body *{visibility:hidden} .takeaway,.takeaway *{visibility:visible} .takeaway{position:absolute;left:0;top:0;border:0;background:#fff;color:#000}
  .takeaway h2,.takeaway li{color:#000} .takeaway button{display:none} body::before{display:none}}

/* quick exit */
.qx{display:inline-flex;align-items:center;min-height:36px;padding:6px 14px;border-radius:999px;border:1px solid rgba(227,135,125,.5);color:#F0B3AB;
  font:600 13px/1 var(--serif);letter-spacing:.06em;text-decoration:none;white-space:nowrap}
.qx:hover{background:rgba(142,43,38,.25)}

/* source pop-up */
.pop{z-index:9500;width:min(440px,calc(100vw - 32px));background:#241D1B;border:1px solid var(--line);border-radius:12px;padding:20px 20px 16px;
  box-shadow:0 24px 64px rgba(0,0,0,.55);font-size:15px;line-height:1.55;color:var(--ink2);animation:popin .2s var(--ease)}
@keyframes popin{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.pop{animation:none}}
.pop .lbl{display:block;font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--acc);margin:0 0 8px}
.pop .go{display:inline-block;margin-top:8px;font-size:14px}
.pop a.ext{word-break:break-all}

/* the compare layer: a horizontal axis over the vertical page */
:root{--cmpw:min(46vw,760px)}
.cmp{position:fixed;top:56px;right:0;bottom:0;width:var(--cmpw);z-index:45;display:flex;flex-direction:column;background:rgba(24,19,18,.97);
  border-left:1px solid var(--line);box-shadow:-24px 0 64px rgba(0,0,0,.4);transform:translateX(0);transition:transform .35s var(--ease)}
.cmp[hidden]{display:flex;transform:translateX(105%);visibility:hidden;transition:transform .35s var(--ease),visibility 0s .35s}
@media (prefers-reduced-motion:reduce){.cmp,.cmp[hidden]{transition:none}}
body.comparing .wrap{margin-right:var(--cmpw);grid-template-columns:minmax(0,1fr)}
body.comparing .rail{display:none}
body.comparing .famnav{right:calc(var(--cmpw) + 16px)}
.cmp-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:16px 20px;border-bottom:1px solid var(--line2)}
.cmp-head .ttl{flex:1;min-width:0}
.cmp-head .ttl .lbl{display:block;font:600 11px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--ink3);margin-bottom:4px}
.cmp-head .ttl b{font:400 22px/1.2 var(--display);color:#F6EFE4;font-weight:400}
.cmp-head select{min-height:40px;max-width:220px;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:6px 12px;font:500 14px var(--serif)}
.icon-btn{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;transition:background .2s var(--ease)}
.icon-btn:hover{background:var(--acc-soft)} .icon-btn svg{width:18px;height:18px}
.cmp-track{flex:1;display:flex;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none}
.cmp-track::-webkit-scrollbar{display:none}
.cmp-card{flex:0 0 100%;scroll-snap-align:start;overflow-y:auto;padding:24px 24px 120px;overscroll-behavior:contain}
.cmp-card > header{margin:0 0 24px;padding:0 0 16px;border-bottom:1px solid var(--line2)}
.cmp-card > header .fam{font:600 11px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--acc)}
.cmp-card > header h3{margin:8px 0 8px;font-size:32px}
.cmp-card > header a{font-size:14px}
.cmp-card .body > *{max-width:none}
.cmp-card .box.intro{display:none}
.cmp-dots{display:flex;justify-content:center;gap:6px;padding:10px 0 14px;border-top:1px solid var(--line2)}
.cmp-dots button{width:8px;height:8px;border-radius:50%;border:0;padding:0;background:var(--line);cursor:pointer;transition:background .2s var(--ease),transform .2s var(--ease)}
.cmp-dots button[aria-current="true"]{background:var(--acc);transform:scale(1.4)}
.cmp-empty{padding:40px 24px;color:var(--ink3)}
@media (max-width:1099px){
  :root{--cmpw:100vw}
  .cmp{top:auto;left:0;height:88vh;width:100%;border-left:0;border-top:1px solid var(--line);border-radius:20px 20px 0 0;box-shadow:0 -24px 64px rgba(0,0,0,.5)}
  .cmp[hidden]{transform:translateY(105%)}
  body.comparing .wrap{margin-right:0} body.comparing .famnav{display:none}
  .cmp{background:#181312}
  .cmp::before{content:"";display:block;width:40px;height:4px;border-radius:2px;background:var(--line);margin:10px auto 0}
  .cmp-card{padding:20px 16px 96px}
  .cmp-head{display:grid;grid-template-columns:1fr auto auto;gap:8px 8px;padding:12px 16px}
  .cmp-head .ttl{grid-column:1/3}
  .cmp-head .cmp-close{grid-column:3;grid-row:1}
  .cmp-head select{grid-column:1;grid-row:2;max-width:none;width:100%}
  .cmp-head .cmp-prev{grid-column:2;grid-row:2} .cmp-head .cmp-next{grid-column:3;grid-row:2}
}

/* home: the disclosure ledger */
.ledger{max-width:1240px;margin:0 auto;padding:0 24px 120px}
.ledger h2{font:400 clamp(36px,5vw,56px)/1.05 var(--display);margin:8px 0 16px;color:#F6EFE4}
.ledger .intro{max-width:60ch;color:var(--ink2);margin:0 0 32px}
.ledger table{min-width:0;font-size:15px}
.ledger th{padding:12px 8px;text-align:center}
.ledger th:first-child{text-align:left} .ledger th .sh{display:none}
@media (max-width:640px){.ledger th .lg{display:none}.ledger th .sh{display:inline}}
.ledger td{padding:10px 8px;text-align:center;vertical-align:middle}
.ledger td:first-child{text-align:left}
.ledger td:first-child a{color:var(--ink);text-decoration:none;font:400 18px/1.25 var(--display)}
.ledger td:first-child a:hover{color:var(--acc-bright)}
.ledger tr.fam td{padding-top:24px;font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--acc);text-align:left;border-bottom:1px solid var(--line)}
.dot{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;border:1px solid currentColor;font:600 12px/1 var(--serif)}
.dot.s-Y{color:#8FCB98} .dot.s-P{color:#E1C47F} .dot.s-N{color:#E3877D} .dot.s-Q,.dot.s-X{color:#6F6860}
@media (max-width:640px){.ledger{padding:0 16px 96px}.ledger th{font-size:9px;letter-spacing:.06em;padding:8px 2px}.ledger td{padding:8px 2px}.dot{width:24px;height:24px;font-size:11px}
  .ledger td:first-child a{font-size:15px}}
@media (max-width:640px){.sec-head{column-gap:16px}.qx{padding:6px 10px}.bar .btn span{display:none}}
"""

TOOLS_JS = r"""
(function(){
  var d=document, root=d.documentElement;
  /* ---- quick exit: the button, or Escape twice with nothing open. replace() keeps this page out of Back. */
  var qx=d.querySelector('[data-quick-exit]'), lastEsc=0;
  function leave(){ try{ location.replace(qx.getAttribute('href')); }catch(e){ location.href=qx.getAttribute('href'); } }
  if(qx){ qx.addEventListener('click',function(ev){ ev.preventDefault(); leave(); });
    d.addEventListener('keydown',function(ev){ if(ev.key!=='Escape') return;
      if(d.querySelector('.sheet.open,.pop,body.comparing,.nf-chrome.nf-open')) return;
      var t=Date.now(); if(t-lastEsc<700) leave(); lastEsc=t; }); }

  /* ---- source pop-ups: a citation opens its source in place instead of jumping to the bottom */
  var pop=null, popFor=null;
  function closePop(){ if(pop){ pop.remove(); pop=null; if(popFor){ popFor.setAttribute('aria-expanded','false'); popFor.focus({preventScroll:true}); } popFor=null; } }
  d.addEventListener('click',function(ev){
    var a=ev.target.closest&&ev.target.closest('a.cite');
    if(pop && !ev.target.closest('.pop') && a!==popFor){ closePop(); }
    if(!a||a.closest('.cmp')) return;
    var id=a.getAttribute('href').slice(1), li=d.getElementById(id); if(!li) return;
    ev.preventDefault(); if(popFor===a){ closePop(); return; }
    closePop();
    pop=d.createElement('div'); pop.className='pop'; pop.setAttribute('role','dialog'); pop.setAttribute('aria-label','Source '+a.textContent);
    pop.innerHTML='<span class="lbl">Source '+a.textContent+'</span><div class="src"></div><a class="go" href="#'+id+'">Go to the source list</a>';
    pop.querySelector('.src').innerHTML=li.innerHTML;
    d.body.appendChild(pop);
    var r=a.getBoundingClientRect(), w=pop.offsetWidth, left=Math.max(16,Math.min(r.left+scrollX-w/2, scrollX+innerWidth-w-16));
    var top=r.bottom+scrollY+10; if(r.bottom+pop.offsetHeight+24>innerHeight && r.top>pop.offsetHeight+80) top=r.top+scrollY-pop.offsetHeight-10;
    pop.style.left=left+'px'; pop.style.top=top+'px';
    a.setAttribute('aria-expanded','true'); popFor=a;
    pop.querySelector('.go').addEventListener('click',function(){ closePop(); });
  });
  d.addEventListener('keydown',function(ev){ if(ev.key==='Escape'&&pop){ ev.stopPropagation(); closePop(); } },true);

  /* ---- print the take-away questions */
  var pr=d.querySelector('[data-print-questions]'); if(pr) pr.addEventListener('click',function(){ print(); });

  /* ---- compare: the same section, across traditions, on a horizontal axis ---- */
  var dataEl=d.getElementById('sd-data'); if(!dataEl) return;
  var D=JSON.parse(dataEl.textContent), panel=d.querySelector('.cmp'); if(!panel) return;
  var track=panel.querySelector('.cmp-track'), dots=panel.querySelector('.cmp-dots'), ttl=panel.querySelector('.ttl b'),
      pick=panel.querySelector('select'), cache={}, slug=null, order=[], opener=null;
  var byId={}; D.all.forEach(function(x){ byId[x.id]=x; });
  function titleOf(s){ var el=d.getElementById(s); return el?el.getAttribute('data-title'):s; }
  function loadDoc(rid){
    if(cache[rid]) return cache[rid];
    cache[rid]=fetch(byId[rid].href.split('#')[0]).then(function(r){ if(!r.ok) throw 0; return r.text(); })
      .then(function(t){ return new DOMParser().parseFromString(t,'text/html'); });
    return cache[rid];
  }
  function fill(card){
    var rid=card.getAttribute('data-rid'), body=card.querySelector('.cmp-body'), want=slug, base=byId[rid].href.split('#')[0];
    card.querySelector('header a').href=base+'#'+want;
    card.querySelector('header a').textContent='Open '+byId[rid].t+' at '+titleOf(want)+' →';
    if(card.getAttribute('data-slug')===want) return;
    card.setAttribute('data-slug',want); body.innerHTML='<p class="cmp-empty">Loading…</p>';
    loadDoc(rid).then(function(doc){
      if(card.getAttribute('data-slug')!==want) return;
      var sec=doc.getElementById(want), b=sec&&sec.querySelector('.body');
      if(!b){ body.innerHTML='<p class="cmp-empty">This section is not on that page.</p>'; return; }
      var c=b.cloneNode(true);
      /* ids would collide with this page's, and local anchors belong to the other page */
      c.querySelectorAll('[id]').forEach(function(n){ n.removeAttribute('id'); });
      c.querySelectorAll('a[href^="#"]').forEach(function(n){ n.href=base+n.getAttribute('href'); });
      body.innerHTML=''; body.appendChild(c);
    }).catch(function(){
      body.innerHTML='<p class="cmp-empty">This preview could not load here (opened from a file). <a href="'+base+'#'+want+'">Open '+byId[rid].t+' at this section</a>.</p>';
    });
  }
  function build(first){
    var sib=D.fam.filter(function(x){ return x!==D.me; });
    order=[]; if(first) order.push(first); sib.forEach(function(x){ if(order.indexOf(x)<0) order.push(x); });
    extras.forEach(function(x){ if(order.indexOf(x)<0) order.push(x); });
    track.innerHTML=''; dots.innerHTML=''; track.scrollLeft=0; cur=0;
    if(!order.length){ track.innerHTML='<p class="cmp-empty">This tradition is the only one in its family. Choose another tradition above to set it beside this one.</p>'; return; }
    order.forEach(function(rid,i){
      var c=d.createElement('article'); c.className='cmp-card'; c.setAttribute('data-rid',rid); c.setAttribute('aria-label',byId[rid].t);
      c.innerHTML='<header><span class="fam">'+byId[rid].f+'</span><h3>'+byId[rid].t+'</h3><a href="#"></a></header><div class="cmp-body"></div>';
      track.appendChild(c);
      var b=d.createElement('button'); b.type='button'; b.setAttribute('aria-label','Show '+byId[rid].t);
      b.addEventListener('click',function(){ go(i); }); dots.appendChild(b);
    });
    if(io){ track.querySelectorAll('.cmp-card').forEach(function(c){ io.observe(c); }); }
  }
  var extras=[], cur=0;
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){ es.forEach(function(x){
      if(x.isIntersecting){ fill(x.target);
        if(x.intersectionRatio>0.6){ cur=[].indexOf.call(track.children,x.target); mark(); } } }); },{root:track,threshold:[0.01,0.6]}):null;
  function mark(){
    [].forEach.call(dots.children,function(b,i){ b.setAttribute('aria-current',i===cur?'true':'false'); });
    var rid=order[cur]; if(rid) history.replaceState(null,'',location.pathname+'?vs='+rid+'#'+slug);
    var n=track.children[cur+1]; if(n&&n.classList&&n.classList.contains('cmp-card')) fill(n);
  }
  function go(i){ i=Math.max(0,Math.min(order.length-1,i)); var c=track.children[i]; if(c) track.scrollTo({left:c.offsetLeft,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}); }
  function open(s,first){
    slug=s; ttl.textContent=titleOf(s); opener=d.activeElement;
    build(first||null); panel.hidden=false; d.body.classList.add('comparing'); cur=0;
    if(!io) [].forEach.call(track.children,function(c){ if(c.classList.contains('cmp-card')) fill(c); });
    mark(); var sec=d.getElementById(s); if(sec) sec.scrollIntoView({block:'start'});
    panel.querySelector('.cmp-close').focus({preventScroll:true});
  }
  function close(){ panel.hidden=true; d.body.classList.remove('comparing'); history.replaceState(null,'',location.pathname+'#'+(slug||'')); if(opener) opener.focus({preventScroll:true}); }
  d.querySelectorAll('.cmp-btn').forEach(function(b){ b.addEventListener('click',function(){ open(b.getAttribute('data-compare')); }); });
  panel.querySelector('.cmp-close').addEventListener('click',close);
  panel.querySelector('.cmp-prev').addEventListener('click',function(){ go(cur-1); });
  panel.querySelector('.cmp-next').addEventListener('click',function(){ go(cur+1); });
  pick.addEventListener('change',function(){ var v=pick.value; pick.value=''; if(!v) return;
    if(extras.indexOf(v)<0) extras.unshift(v); open(slug,v); });
  d.addEventListener('keydown',function(ev){
    if(panel.hidden) return;
    if(ev.key==='Escape'){ ev.preventDefault(); close(); return; }
    if(ev.target&&(ev.target.tagName==='SELECT'||ev.target.tagName==='INPUT')) return;
    if(ev.key==='ArrowRight'){ ev.preventDefault(); go(cur+1); } else if(ev.key==='ArrowLeft'){ ev.preventDefault(); go(cur-1); } });
  /* the vertical axis drives the horizontal one: scrolling the page to a new section re-aims every card */
  if('IntersectionObserver' in window){
    var so=new IntersectionObserver(function(es){ es.forEach(function(x){ if(x.isIntersecting&&!panel.hidden&&x.target.id!==slug){
      slug=x.target.id; ttl.textContent=titleOf(slug);
      track.querySelectorAll('.cmp-card').forEach(function(c){ var r=c.getBoundingClientRect(), tr=track.getBoundingClientRect();
        if(r.right>tr.left-10&&r.left<tr.right+10) fill(c); else c.removeAttribute('data-slug'); });
      mark(); } }); },{rootMargin:'-35% 0px -60% 0px'});
    d.querySelectorAll('section.sec').forEach(function(s){ so.observe(s); });
  }
  var q=new URLSearchParams(location.search).get('vs');
  if(q&&byId[q]){ var h=location.hash.slice(1)||'at-a-glance'; if(d.getElementById(h)) open(h,q); }
})();
"""

STAMP = ('<svg class="stamp" viewBox="0 0 136 136" aria-hidden="true"><defs><path id="stp" d="M68 68 m-52 0 a52 52 0 1 1 104 0 a52 52 0 1 1 -104 0"/></defs>'
         '<circle cx="68" cy="68" r="66" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="68" cy="68" r="61" fill="none" stroke="currentColor" stroke-width=".6" stroke-dasharray="2 3"/>'
         '<circle cx="68" cy="68" r="38" fill="none" stroke="currentColor" stroke-width=".8"/>'
         '<text font-family="Newsreader,serif" font-size="10.5" letter-spacing="3.1" fill="currentColor"><textPath href="#stp">{ring}</textPath></text>'
         '<text x="68" y="64" text-anchor="middle" font-family="Codex Display,serif" font-size="22" fill="currentColor">{big}</text>'
         '<text x="68" y="82" text-anchor="middle" font-family="Newsreader,serif" font-size="8.5" letter-spacing="2" fill="currentColor">{small}</text></svg>')

ICON2 = {
    'compare': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></svg>',
    'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    'print': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v8H6z"/></svg>',
}

SEAL_LABEL = [('Accounts', 'Accounts published'), ('Pay', "Leaders' pay"), ('Safeguarding', 'Safeguarding policy'),
              ('External first', 'Police first'), ('Removal', 'Removal procedure'), ('Reply', 'Replies on record')]
SEAL_WORD = {'Y': 'Yes', 'P': 'Partial', 'N': 'No', '?': 'Not assessable'}


def dossier(h):
    m = re.search(r'<div class="box glance">\s*<div class="tw"><table>.*?<tbody>(.*?)</tbody>\s*</table></div>\s*</div>', h, re.S)
    if not m:
        return h
    items, uq = [], ''
    for k, v in re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>', m.group(1), re.S):
        k = k.strip()
        if k in ('Family', 'Last checked'):
            continue
        if k == 'The unanswered question':
            uq = v
            continue
        if k == 'Chosen by / removable by' and ' / ' in v:
            a, b = v.split(' / ', 1)
            items += [('Chosen by', a), ('Removable by', b)]
            continue
        items.append((k, v))
    out = '<dl class="dossier">' + ''.join(f'<div class="dr"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items) + '</dl>'
    if uq:
        out += f'<blockquote class="uq-pull"><span class="lbl">The unanswered question</span><p>{uq}</p></blockquote>'
    return h[:m.start()] + out + h[m.end():]


def seals(h):
    m = re.search(r'<div class="tw(?: score-wrap)?"><table(?: class="score")?>\s*<thead>\s*<tr>\s*<th>Accounts</th>.*?<tbody>(.*?)</tbody>\s*</table></div>', h, re.S)
    if not m:
        return h
    cells = re.findall(r'<td[^>]*>(.*?)</td>', m.group(1), re.S)
    lis = []
    for (key, label), c in zip(SEAL_LABEL, cells):
        txt = re.sub(r'<[^>]+>', '', c).strip()
        v = txt[:1] if txt[:1] in 'YPN?' else '?'
        note = c.strip()[1:].strip()
        cls = 'Q' if v == '?' else v
        lis.append(f'<li class="s-{cls}"><div class="seal" aria-hidden="true">{v}</div><b>{label}</b><span class="v">{SEAL_WORD[v]}</span>'
                   + (f'<span class="note">{note}</span>' if note else '') + '</li>')
    return h[:m.start()] + '<ul class="seals" aria-label="Disclosure scorecard">' + ''.join(lis) + '</ul>' + h[m.end():]


KEYPAD = {c: str(n) for n, cs in {2: 'ABC', 3: 'DEF', 4: 'GHI', 5: 'JKL', 6: 'MNO', 7: 'PQRS', 8: 'TUV', 9: 'WXYZ'}.items() for c in cs}


def tel_link(cell):
    def rep(mm):
        raw = mm.group(1)
        if not re.fullmatch(r'\+?[\dA-Z][\dA-Z \-()]{5,}', raw) or sum(ch.isdigit() for ch in raw) < 3:
            return mm.group(0)
        num = ''.join(KEYPAD.get(ch, ch) for ch in raw if ch.isalnum() or ch == '+')
        return f'<a class="tel" href="tel:{num}">{ICON2["phone"]}{raw}</a>'
    return re.sub(r'<strong>([^<]+)</strong>', rep, cell)


def contacts(h):
    m = re.search(r'<div class="tw"><table>\s*<thead>\s*<tr>\s*<th>Organization</th>.*?<tbody>(.*?)</tbody>\s*</table></div>', h, re.S)
    if not m:
        return h
    cards = []
    for row in re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S):
        c = re.findall(r'<td>(.*?)</td>', row, re.S)
        if len(c) < 4:
            continue
        name = re.sub(r'</?strong>', '', c[0])
        cards.append(f'<article class="contact"><h4>{name}</h4><div class="for">{c[1]}</div><div class="where">{c[2]}</div>'
                     f'<div class="how">{tel_link(c[3])}</div></article>')
    return h[:m.start()] + '<div class="contacts">' + ''.join(cards) + '</div>' + h[m.end():]


def dockets(h):
    # the title may not cross its own </h3>: a case without "(Place, year)" keeps its plain title
    return re.sub(r'(<div class="box case">\s*<h3 id="[^"]+">)([^<]*?) \(([^()<]*\d{4}[^()<]*)\)(</h3>)',
                  lambda mm: f'{mm.group(1)}<span class="dk">{mm.group(3).replace(", ", " · ")}</span>{mm.group(2)}{mm.group(4)}', h)


def dropcap(h):
    for mm in re.finditer(r'<p>(.*?)</p>', h, re.S):
        inner = mm.group(1).strip()
        if inner.startswith('<em>') or len(re.sub(r'<[^>]+>', '', inner)) < 120 or 'class="lbl"' in h[max(0, mm.start() - 80):mm.start()]:
            continue
        if not re.match(r'[A-Za-z“"]', re.sub(r'<[^>]+>', '', inner)):
            continue
        return h[:mm.start()] + '<p class="dropcap">' + h[mm.start() + 3:]
    return h


def pullq(h):
    """Set the closing question of the 'why this matters' caption as a pull-question; return it too."""
    m = re.search(r'(<aside class="box foryou">.*?)(<p>)((?:(?!<p>).)*?)(</p>)(</aside>)', h, re.S)
    if not m:
        return h, ''
    text = m.group(3)
    # the last question in the caption, wherever it falls; any sentence after it follows the pull-question
    qs = list(re.finditer(r'(?:^|(?<=[.!?”"]\s))([^.?!<>]*(?:<(?:strong|em)>[^<]*</(?:strong|em)>[^.?!<>]*)*\?)(?=\s|$)', text))
    q = qs[-1] if qs else None
    if not q or len(q.group(1)) < 12:
        return h, ''
    tail = text[q.end(1):].strip()
    new_p = text[:q.start(1)] + f'<span class="pq">{q.group(1).strip()}</span>' + (f'<span class="pq-tail">{tail}</span>' if tail else '')
    return h[:m.start(3)] + new_p + h[m.end(3):], re.sub(r'<[^>]+>', '', q.group(1)).strip()


GRADE_WORDS = ('Codified', 'Documented', 'Taught', 'Cultural', 'Contested', 'Reformed', 'Ungraded')


def grade_chips(h):
    def cell(mm):
        g = mm.group(1)
        return f'<td><span class="chip g-{g.lower()}">{g}</span>{mm.group(2)}</td>'
    return re.sub(r'<td>(' + '|'.join(GRADE_WORDS) + r')((?:\s*\([^)<]*\))?)</td>', cell, h)


def polish(slug, h):
    if slug == 'techniques':
        h = grade_chips(h)
    if slug == 'at-a-glance':
        h = seals(dossier(h))
    if slug == 'a-day-inside':
        h = dropcap(h)
    if slug == 'cases':
        h = dockets(h)
    if slug == 'help':
        h = contacts(h)
    return pullq(h)

# ---------------------------------------------------------------- page pieces
def page(title, desc, body, slug, fonts):
    css_chrome, js_chrome = chrome.component_css(), chrome.component_js()
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141010">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%23141010%27/%3E%3Cpath d=%27M16 5 27 16 16 27 5 16z%27 fill=%27none%27 stroke=%27%23C9A35B%27 stroke-width=%272%27/%3E%3Ccircle cx=%2716%27 cy=%2716%27 r=%273%27 fill=%27%23C9A35B%27/%3E%3C/svg%3E">
<style>{fonts}</style>
<style>{CSS}</style>
<style>{REFINE_CSS}</style>
<style>{TREE_CSS if slug == 'index' else ''}</style>
<style id="nf-chrome-css">{css_chrome}</style>
</head><body>
<a class="skip" href="#main">Skip to the reading</a>
{body}
{chrome.component_html('faith')}
<script>{JS}</script>
<script>{TOOLS_JS}</script>
<script id="nf-chrome-js">{js_chrome}</script>
{BEACON if LIVE else ''}
</body></html>'''


def wrap_tables(h):
    h = re.sub(r'(<table class="score">.*?</table>)', r'<div class="tw score-wrap">\1</div>', h, flags=re.S)
    return re.sub(r'(?<!score-wrap">)(<table>.*?</table>)', r'<div class="tw">\1</div>', h, flags=re.S)


def unanswered(rid):
    f = narr.facts(rid)
    uq = f['glance'].get('The unanswered question')
    if uq:
        return uq
    raw = open(os.path.join(sdp.SRC, f'{rid}.md'), encoding='utf-8').read()
    m = re.search(r'^::: question\s*\n(.*?)\n:::', raw, re.S | re.M)
    if m:
        return narr._clean(m.group(1))
    q = re.search(r'^## 23\. [^\n]*\n\s*1\.\s+([^\n]+)', raw, re.M)
    return narr._clean(q.group(1)) if q else ''


def manifest(path):
    p = os.path.join(PDFDIR, path)
    return json.load(open(p)) if os.path.exists(p) else {}


def mb(n):
    return f'{n / 1048576:.1f} MB' if n else ''


def religion_page(rid, fam_name, members, fnum, man_std, man_exp):
    sections, meta = exp.build_sections(rid)
    name = meta.get('title', rid)
    i = members.index(rid)
    prev_id, next_id = (members[i - 1], members[(i + 1) % len(members)]) if len(members) > 1 else (None, None)
    title_of = {m: narr.facts(m)['title'] for m in members}

    toc = ''.join(f'<li><a href="#{slug}"><span class="n">{int(num):02d}</span><span>{e(t)}</span></a></li>' for num, t, slug, _h, _s in sections)
    secs, takeaway = [], []
    for num, t, slug, h, _subs in sections:
        h, q = polish(slug, wrap_tables(h))
        if q:
            takeaway.append((slug, t, q))
        # the intro box leads, the for-you box closes; both are kept out of .body's measure rules by class
        secs.append(f'<section class="sec" id="{slug}" data-title="{e(t)}" aria-labelledby="h-{slug}">'
                    f'<header class="sec-head reveal"><span class="numeral" aria-hidden="true">{int(num):02d}</span>'
                    f'<div class="st"><span class="num">Section {int(num):02d} of 27</span><h2 id="h-{slug}">{e(t)}</h2></div>'
                    f'<div class="tools"><button class="cmp-btn" type="button" data-compare="{slug}" aria-label="Compare {e(t)} with other traditions">'
                    f'{ICON2["compare"]}Compare</button></div></header>'
                    f'<div class="body">{h}</div></section>')
    if takeaway:
        items = ''.join(f'<li>{e(q)} <a href="#{sl}">§ {e(tt)}</a></li>' for sl, tt, q in takeaway)
        aside = (f'<aside class="takeaway" id="take-away" aria-labelledby="h-take"><div class="eyebrow">Questions to take with you</div>'
                 f'<h2 id="h-take">One question from every section</h2><p class="lede-s">The closing question of each section\'s note, gathered in one place. '
                 f'Nothing is saved; print it if you want to keep it.</p><ol>{items}</ol>'
                 f'<button class="btn" type="button" data-print-questions>{ICON2["print"]}Print this list</button></aside>')
        at = next((k for k, x in enumerate(secs) if 'id="leaving"' in x), len(secs))
        secs.insert(at, aside)
    lede = re.search(r'<div class="box lede"[^>]*>\s*<p>(.*?)</p>', ''.join(s[3] for s in sections[:4]), re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else unanswered(rid)
    if len(blurb) > 240:  # end on a sentence where one fits, so the hero never stops mid-thought
        cut = max(blurb.rfind('. ', 0, 240), blurb.rfind('? ', 0, 240))
        blurb = blurb[:cut + 1] if cut > 80 else blurb[:237].rsplit(' ', 1)[0] + '…'
    std, ex = man_std.get(rid, {}), man_exp.get(rid, {})
    dl = (f'<a class="btn solid" href="{pdf_href(rid)}" download>{ICON["down"]}Download the full record (PDF)'
          f'{" · " + str(ex.get("pages")) + " pp" if ex.get("pages") else ""}</a>')
    fam_links = ' · '.join((f'<a href="{href(m)}" aria-current="page">{e(title_of[m])}</a>' if m == rid else f'<a href="{href(m)}">{e(title_of[m])}</a>') for m in members)
    famnav = ''
    if prev_id and prev_id == next_id:   # a two-tradition family: one arrow, not the same name twice
        famnav = (f'<nav class="famnav" aria-label="The other tradition in the {e(fam_name)} family"><div class="inner">'
                  f'<span class="mid">{e(fam_name)} · {i + 1} of {len(members)}</span>'
                  f'<button class="sheet-btn" type="button" data-open-sheet aria-label="Jump to a section">{ICON["list"]}Sections</button>'
                  f'<a data-rid="{next_id}" data-href="{href(next_id)}" href="{href(next_id)}" rel="next" aria-label="Other tradition in this family: {e(title_of[next_id])}"><span class="lab">{e(title_of[next_id])}</span>{ICON["right"]}</a>'
                  f'</div></nav>')
    elif prev_id:
        famnav = (f'<nav class="famnav" aria-label="Other traditions in the {e(fam_name)} family"><div class="inner">'
                  f'<a data-rid="{prev_id}" data-href="{href(prev_id)}" href="{href(prev_id)}" rel="prev" aria-label="Previous in family: {e(title_of[prev_id])}">{ICON["left"]}<span class="lab">{e(title_of[prev_id])}</span></a>'
                  f'<span class="mid">{e(fam_name)} · {i + 1} of {len(members)}</span>'
                  f'<button class="sheet-btn" type="button" data-open-sheet aria-label="Jump to a section">{ICON["list"]}Sections</button>'
                  f'<a data-rid="{next_id}" data-href="{href(next_id)}" href="{href(next_id)}" rel="next" aria-label="Next in family: {e(title_of[next_id])}"><span class="lab">{e(title_of[next_id])}</span>{ICON["right"]}</a>'
                  f'</div></nav>')
    else:
        famnav = (f'<nav class="famnav" aria-label="Sections"><div class="inner"><span class="mid">{e(fam_name)} · the only tradition in this family</span>'
                  f'<button class="sheet-btn" type="button" data-open-sheet aria-label="Jump to a section">{ICON["list"]}Sections</button></div></nav>')
    checked = meta.get('checked', '')
    stamp = STAMP.format(ring='SOURCED · NUMBERED · CHECKED · ' + e(checked) + ' · ', big=e(meta.get('version', 'v4')), small='27 SECTIONS')
    opts = ''.join(f'<optgroup label="{e(fn)}">' + ''.join(f'<option value="{m}">{e(narr.facts(m)["title"])}</option>' for m in mem if m != rid) + '</optgroup>'
                   for _fid, fn, mem in FAMILIES)
    cmp_panel = (f'<div class="cmp" role="dialog" aria-label="Compare this section across traditions" hidden><div class="cmp-head">'
                 f'<div class="ttl"><span class="lbl">Comparing</span><b>—</b></div>'
                 f'<select aria-label="Add a tradition to compare"><option value="">Add a tradition…</option>{opts}</select>'
                 f'<button class="icon-btn cmp-prev" type="button" aria-label="Previous tradition">{ICON["left"]}</button>'
                 f'<button class="icon-btn cmp-next" type="button" aria-label="Next tradition">{ICON["right"]}</button>'
                 f'<button class="icon-btn cmp-close" type="button" aria-label="Close compare">{ICON["x"]}</button></div>'
                 f'<div class="cmp-track" tabindex="0" aria-label="Traditions, side by side — swipe or use the arrow keys"></div><div class="cmp-dots"></div></div>')
    data_json = json.dumps({'me': rid, 'fam': members,
                            'all': [{'id': m, 't': narr.facts(m)['title'], 'f': fn, 'href': href(m)} for _fid, fn, mem in FAMILIES for m in mem]},
                           ensure_ascii=False).replace('</', '<\\/')
    body = f'''<header class="bar"><a class="home" href="{home()}">The Sacred Divide</a>
<span class="where">{e(name)} · <b>At a glance</b></span>
<a class="qx" href="https://www.google.com/search?q=weather" rel="noreferrer" data-quick-exit title="Leaves this page at once (or press Escape twice)">Quick exit</a>
<a class="btn" href="{pdf_href(rid)}" download aria-label="Download the {e(name)} PDF">{ICON["down"]}<span>PDF</span></a></header>
<div class="wrap">
<aside class="rail" aria-label="Sections on this page"><h2>On this page</h2><ol class="toc">{toc}</ol></aside>
<main id="main">
<div class="hero col">{stamp}<div class="eyebrow">Family {fnum:02d} · {e(fam_name)}</div><h1>{e(name)}</h1>
<p class="blurb">{e(blurb)}</p><div class="dl">{dl}</div>
<div class="meta">{e(meta.get("version", ""))} · checked {e(meta.get("checked", ""))} · 27 sections · every claim numbered to a source</div>
<div class="fam">In this family: {fam_links}</div></div>
{"".join(secs)}
</main></div>
{famnav}
{cmp_panel}
<script type="application/json" id="sd-data">{data_json}</script>
<div class="sheet" role="dialog" aria-modal="true" aria-label="Sections on this page"><div class="scrim"></div><div class="panel">
<h2>On this page</h2><button class="btn close" type="button" aria-label="Close">{ICON["x"]}</button><ol class="toc">{toc}</ol></div></div>'''
    return page(f'{name} — The Sacred Divide', f'The full record for {name}: 27 sections, sourced, with a note on why each one matters to you.', body, rid, '{FONTS}')


def ledger():
    short = {'Accounts': 'Acc.', 'Pay': 'Pay', 'Safeguarding': 'Safe.', 'External first': 'Police', 'Removal': 'Remove', 'Reply': 'Reply'}
    heads = ''.join(f'<th scope="col"><span class="lg">{e(lab)}</span><span class="sh" aria-hidden="true">{short[k]}</span></th>' for k, lab in SEAL_LABEL)
    rows = []
    for _fid, fname, members in FAMILIES:
        rows.append(f'<tr class="fam"><td colspan="7">{e(fname)}</td></tr>')
        for m in members:
            sc = narr.facts(m)['score']
            cells = ''.join((f'<td><span class="dot s-{"Q" if sc[k] == "?" else sc[k]}" title="{SEAL_WORD[sc[k]]}">{sc[k]}</span></td>' if k in sc
                             else '<td><span class="dot s-X" title="Not yet scored">–</span></td>') for k, _l in SEAL_LABEL)
            rows.append(f'<tr><td><a href="{href(m, "at-a-glance")}">{e(narr.facts(m)["title"])}</a></td>{cells}</tr>')
    return (f'<section class="ledger reveal" id="ledger" aria-labelledby="h-ledger"><div class="eyebrow">Side by side</div>'
            f'<h2 id="h-ledger">The disclosure ledger</h2><p class="intro">Six questions any charity or public company would be expected to answer, '
            f'asked of every tradition in this book. <b>Y</b> established from a public source · <b>P</b> partly, or only in some places · '
            f'<b>N</b> not established from any public source · <b>?</b> no single office exists to ask · – not yet scored.</p>'
            f'<div class="tw"><table><thead><tr><th scope="col">Tradition</th>{heads}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')


def tree():
    total = sum(len(m) for _, _, m in FAMILIES)
    branches = []
    for n, (fid, fname, members) in enumerate(FAMILIES, 1):
        leaves = ''.join(f'<li><a href="{href(m)}">{e(narr.facts(m)["title"])}</a></li>' for m in members)
        branches.append(f'<li class="branch reveal" id="{fid}"><div class="node"><span class="fnum">Family {n:02d}</span>'
                        f'<h3>{e(fname)}</h3><ol class="leaves">{leaves}</ol></div></li>')
    return (f'<section class="tree" id="families" aria-labelledby="h-tree"><div class="root"><span class="seal-sm" aria-hidden="true"></span>'
            f'<h2 id="h-tree">The family tree</h2><p>{total} traditions · {len(FAMILIES)} families</p></div>'
            f'<ol class="branches">{"".join(branches)}</ol></section>')


TREE_CSS = r"""
.home-bar{display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:1240px;margin:0 auto;padding:16px 24px}
.home-bar .brand{font:400 18px/1 var(--display);color:var(--ink);text-decoration:none}
.entrance{max-width:1240px;margin:0 auto;padding:clamp(64px,12vh,136px) 24px 72px;text-align:center}
.entrance .eyebrow{display:block}
.entrance h1{font:400 clamp(52px,9vw,120px)/1.02 var(--display);margin:24px auto 40px;color:#F6EFE4;letter-spacing:-.015em;text-wrap:balance}
.entrance .statement{font:400 clamp(21px,2.5vw,27px)/1.55 var(--serif);color:var(--ink);max-width:36ch;margin:0 auto 24px;text-wrap:pretty}
.entrance .statement em{color:var(--acc-bright)}
.entrance .standard{font:italic 400 clamp(18px,2vw,21px)/1.5 var(--serif);color:var(--ink2);max-width:40ch;margin:0 auto 48px}
.entrance .down{display:inline-flex;flex-direction:column;align-items:center;gap:12px;color:var(--ink3);text-decoration:none;font:600 12px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase}
.entrance .down::after{content:"";width:1px;height:64px;background:linear-gradient(var(--acc),transparent)}
.entrance .down:hover{color:var(--acc-bright)}
.tree{position:relative;max-width:1120px;margin:0 auto;padding:0 24px 120px}
.tree .root{position:relative;text-align:center;margin:0 auto 56px;padding:24px 0 0}
.tree .root h2{font:400 clamp(32px,4vw,44px)/1.1 var(--display);margin:16px 0 8px;color:#F6EFE4}
.tree .root p{margin:0;font:600 12px/1 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--acc)}
.seal-sm{display:inline-block;width:18px;height:18px;transform:rotate(45deg);border:1px solid var(--acc);box-shadow:0 0 0 4px var(--bg),0 0 0 5px rgba(201,163,91,.4)}
.branches{list-style:none;margin:0;padding:0;position:relative}
.branches::before{content:"";position:absolute;left:50%;top:-40px;bottom:0;width:1px;
  background:linear-gradient(rgba(201,163,91,.7),rgba(201,163,91,.35) 85%,transparent)}
.branch{position:relative;width:calc(50% - 48px);margin:0 0 40px}
.branch:nth-child(odd){margin-right:auto} .branch:nth-child(even){margin-left:auto}
.branch::before{content:"";position:absolute;top:44px;width:48px;height:1px;background:rgba(201,163,91,.5)}
.branch:nth-child(odd)::before{right:-48px} .branch:nth-child(even)::before{left:-48px}
.branch::after{content:"";position:absolute;top:39px;width:10px;height:10px;transform:rotate(45deg);background:var(--bg);border:1px solid var(--acc)}
.branch:nth-child(odd)::after{right:-54px} .branch:nth-child(even)::after{left:-54px}
.node{background:var(--surface);border:1px solid var(--line2);border-radius:16px;padding:28px 28px 20px;transition:border-color .25s var(--ease),transform .25s var(--ease)}
.node:hover{border-color:var(--line);transform:translateY(-2px)}
@media (prefers-reduced-motion:reduce){.node,.node:hover{transition:none;transform:none}}
.node .fnum{font:600 12px/1 var(--serif);letter-spacing:.24em;text-transform:uppercase;color:var(--acc);font-variant-numeric:lining-nums}
.node h3{font:400 clamp(26px,2.6vw,32px)/1.15 var(--display);margin:12px 0 16px;color:#F6EFE4}
.leaves{list-style:none;margin:0;padding:0 0 0 16px;border-left:1px solid var(--line)}
.leaves li{position:relative;margin:0}
.leaves li::before{content:"";position:absolute;left:-16px;top:50%;width:10px;height:1px;background:var(--line)}
.leaves a{display:block;padding:8px 8px;margin:0 -8px 0 0;border-radius:8px;text-decoration:none;color:var(--ink);font:400 20px/1.3 var(--display);
  transition:background .2s var(--ease),color .2s var(--ease)}
.leaves a:hover{background:var(--acc-soft);color:var(--acc-bright)}
@media (max-width:760px){
  .branches::before{left:0;top:-24px}
  .branch,.branch:nth-child(odd),.branch:nth-child(even){width:calc(100% - 32px);margin:0 0 24px 32px}
  .branch:nth-child(odd)::before,.branch:nth-child(even)::before{left:-32px;right:auto;width:32px}
  .branch:nth-child(odd)::after,.branch:nth-child(even)::after{left:-5px;right:auto;margin-left:-32px}
  .tree .root{text-align:left;margin-bottom:40px}
  .node{padding:24px 20px 16px}
}
.refband{max-width:760px;margin:0 auto 96px;padding:24px 28px;border:1px solid var(--line);border-radius:16px;text-align:center;color:var(--ink2);font-size:17px}
.refband p{margin:0}
@media (max-width:760px){.refband{margin:0 16px 72px}}
.updates{max-width:1240px;margin:0 auto;padding:48px 24px 120px;border-top:1px solid var(--line2);color:var(--ink2)}
.updates h2{font:600 12px/1 var(--serif);letter-spacing:.2em;text-transform:uppercase;color:var(--ink3);margin:0 0 16px}
.updates .ver{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 14px;color:var(--acc);font-size:14px;letter-spacing:.06em;margin:0 0 16px}
.updates ul{max-width:70ch;padding-left:20px;font-size:16px} .updates li{margin:0 0 8px}
.updates .privacy{max-width:70ch;font-size:15px;color:var(--ink3)}
"""

UPDATES = [
    "A new edition: one page for each of 34 traditions, grouped into 10 families, every page built on the same 27 sections.",
    "Every section now opens with a short note on what it shows, and closes with a note on why it matters to you.",
    "Compare any section side by side with the same section from other traditions.",
    "Tap a citation to read its source in place. Every page has a quick-exit button.",
    "Each tradition can be downloaded as a PDF: the full record, with the same notes and captions as the page.",
    "Fact-check corrections are applied throughout; each page lists its own in \"What changed on this page\".",
    "The earlier single-page codex stays available as the reference edition, with its volumes, instruments and methodology.",
]


def index_page():
    total = sum(len(m) for _, _, m in FAMILIES)
    updates = ''.join(f'<li>{e(u)}</li>' for u in UPDATES)
    privacy = ('This site keeps an anonymous visit count (Cloudflare Web Analytics, which sets no cookies). '
               'Nothing you read, compare or print is stored, and no page asks who you are.') if LIVE else \
              'Preview build: no visit counter. The live build adds only an anonymous visit count.'
    body = f'''<header class="home-bar"><a class="brand" href="{home()}">The Sacred Divide</a>
<a class="qx" href="https://www.google.com/search?q=weather" rel="noreferrer" data-quick-exit title="Leaves this page at once (or press Escape twice)">Quick exit</a></header>
<main id="main">
<section class="entrance" aria-labelledby="h-entrance"><span class="eyebrow">Noble Father Creations</span>
<h1 id="h-entrance">The Sacred Divide</h1>
<p class="statement">Faith is honored here. What is examined is the institution built around it: <em>who holds power, where the money goes, what leaving costs, and who is protected when something goes wrong.</em></p>
<p class="standard">{total} traditions, one standard, and nothing that can't be traced to a source.</p>
<a class="down" href="#families">Begin with the family tree</a></section>
{tree()}
<aside class="refband"><p>Looking for the volumes, the instruments, the glossary or the methodology? They are in the
<a href="{CODEX_HREF}">reference edition</a>: the earlier single-page codex, fact-checked and kept whole while its material moves into these pages.</p></aside>
{ledger()}
<footer class="updates" id="updates" aria-labelledby="h-updates"><h2 id="h-updates">Updates</h2>
<span class="ver">{VERSION} — {RELEASED}</span><ul>{updates}</ul><p class="privacy">{privacy}</p></footer>
</main>'''
    return page('The Sacred Divide — Noble Father Creations', 'How institutional power works inside 34 religious traditions, each held to one standard and every claim sourced.', body, 'index', '{FONTS}')


def main():
    os.makedirs(OUT, exist_ok=True)
    man_std, man_exp = manifest('manifest.json'), manifest('expanded/manifest.json')
    pages = {'index': index_page()}
    for n, (fid, fname, members) in enumerate(FAMILIES, 1):
        for rid in members:
            pages[rid] = religion_page(rid, fname, members, n, man_std, man_exp)
    # one shared subset covering every character any page uses, so the pages stay consistent
    text = re.sub(r'<[^>]+>', ' ', ''.join(pages.values()))
    fonts = font_css(H.unescape(text))
    total = 0
    for slug, doc in pages.items():
        doc = doc.replace('{FONTS}', fonts, 1)
        path = os.path.join(OUT, f'{slug}.html')
        open(path, 'w', encoding='utf-8').write(doc)
        total += len(doc.encode())
    print(f'{len(pages)} pages → {OUT} ({total / 1048576:.1f} MB total; fonts {len(fonts) / 1024:.0f} KB per page)')


if __name__ == '__main__':
    main()
