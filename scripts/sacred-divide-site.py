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
                  land on the section you are reading; PDF downloads (standard + expanded) at the top.

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
PDF_BASE = arg('--pdf-base', '../sacred-divide-pdf/')
EXT = arg('--ext', '.html')


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


# ---------------------------------------------------------------- page pieces
def page(title, desc, body, slug, fonts):
    css_chrome, js_chrome = chrome.component_css(), chrome.component_js()
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141010">
<style>{fonts}</style>
<style>{CSS}</style>
<style id="nf-chrome-css">{css_chrome}</style>
</head><body>
<a class="skip" href="#main">Skip to the reading</a>
{body}
{chrome.component_html('faith')}
<script>{JS}</script>
<script id="nf-chrome-js">{js_chrome}</script>
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
    secs = []
    for num, t, slug, h, _subs in sections:
        h = wrap_tables(h)
        # the intro box leads, the for-you box closes; both are kept out of .body's measure rules by class
        secs.append(f'<section class="sec" id="{slug}" data-title="{e(t)}" aria-labelledby="h-{slug}">'
                    f'<header class="sec-head reveal"><span class="num">Section {int(num):02d}</span><h2 id="h-{slug}">{e(t)}</h2></header>'
                    f'<div class="body">{h}</div></section>')
    lede = re.search(r'<div class="box lede"[^>]*>\s*<p>(.*?)</p>', ''.join(s[3] for s in sections[:4]), re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else unanswered(rid)
    if len(blurb) > 240:  # end on a sentence where one fits, so the hero never stops mid-thought
        cut = max(blurb.rfind('. ', 0, 240), blurb.rfind('? ', 0, 240))
        blurb = blurb[:cut + 1] if cut > 80 else blurb[:237].rsplit(' ', 1)[0] + '…'
    std, ex = man_std.get(rid, {}), man_exp.get(rid, {})
    dl = (f'<a class="btn solid" href="{PDF_BASE}{rid}.pdf" download>{ICON["down"]}Download the full record'
          f'{" · " + str(std.get("pages")) + " pp" if std.get("pages") else ""}</a>'
          f'<a class="btn" href="{PDF_BASE}expanded/{rid}-expanded.pdf" download>{ICON["down"]}Expanded edition'
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
    body = f'''<header class="bar"><a class="home" href="{home()}">The Sacred Divide</a>
<span class="where">{e(name)} · <b>At a glance</b></span>
<a class="btn" href="{PDF_BASE}{rid}.pdf" download aria-label="Download the {e(name)} PDF">{ICON["down"]}<span>PDF</span></a></header>
<div class="wrap">
<aside class="rail" aria-label="Sections on this page"><h2>On this page</h2><ol class="toc">{toc}</ol></aside>
<main id="main">
<div class="hero col"><div class="eyebrow">Family {fnum:02d} · {e(fam_name)}</div><h1>{e(name)}</h1>
<p class="blurb">{e(blurb)}</p><div class="dl">{dl}</div>
<div class="meta">{e(meta.get("version", ""))} · checked {e(meta.get("checked", ""))} · 27 sections · every claim numbered to a source</div>
<div class="fam">In this family: {fam_links}</div></div>
{"".join(secs)}
</main></div>
{famnav}
<div class="sheet" role="dialog" aria-modal="true" aria-label="Sections on this page"><div class="scrim"></div><div class="panel">
<h2>On this page</h2><button class="btn close" type="button" aria-label="Close">{ICON["x"]}</button><ol class="toc">{toc}</ol></div></div>'''
    return page(f'{name} — The Sacred Divide', f'The full record for {name}: 27 sections, sourced, with a note on why each one matters to you.', body, rid, '{FONTS}')


def index_page():
    cards = []
    for n, (fid, fname, members) in enumerate(FAMILIES, 1):
        items = ''.join(f'<li><a href="{href(m)}"><span class="nm">{e(narr.facts(m)["title"])}</span>'
                        f'<span class="uq">{e(unanswered(m))}</span></a></li>' for m in members)
        cards.append(f'<article class="family reveal" id="{fid}"><div class="fnum">Family {n:02d} · {len(members)} tradition{"s" if len(members) != 1 else ""}</div>'
                     f'<h2>{e(fname)}</h2><ol>{items}</ol></article>')
    total = sum(len(m) for _, _, m in FAMILIES)
    body = f'''<main id="main">
<div class="home-hero"><div class="eyebrow">Noble Father Creations</div><h1>The Sacred Divide</h1>
<p class="lead">Honor the faith. Name the machinery. {total} traditions in {len(FAMILIES)} families, each held to the same 27-section standard and the same rule: nothing goes in that can't be traced to a source.</p>
<ul class="how">
<li><b>One page per tradition</b>Read it top to bottom, or jump straight to a section. Every page has the same 27 sections in the same order.</li>
<li><b>Why it matters to you</b>Each section closes with a short note on where the finding touches an ordinary reader, and a question worth asking.</li>
<li><b>Move across a family</b>The arrows at the bottom of each page take you to the next tradition in the same family, landing on the section you were reading.</li>
</ul></div>
<div class="families">{"".join(cards)}</div>
<footer class="colophon" id="updates"><h2>About this edition</h2>
<p><span class="badge">Redesign preview</span> Built from the v4 fact-checked record. Every page is self-contained: no trackers, no external requests, and it works offline. Each page offers the standard PDF and an expanded PDF with the same narration.</p></footer>
</main>'''
    return page('The Sacred Divide — Noble Father Creations', 'How institutional power works inside 34 religious traditions: one sourced page each, with a note on why each finding matters to you.', body, 'index', '{FONTS}')


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
