#!/usr/bin/env python3
"""The Weighing, v5: build the book from content/scale-v2 (plan.json + NN-*.md) on the shared shell (scripts/book/shell.py).

Run:  python3 scripts/seo/build_scale_v2.py [--og]
Writes library/scale/: index.html (cover, contents, toolbox, updates), one page per chapter and tool, contents.html,
search.html (offline, nothing sent anywhere), all.html (whole book on one page), sitemap.xml. Old #/c/N, #/card and
#/limits links are forwarded to their new pages. Skin: interim (the v4 brass on dark); the v5 look comes from the design phase.
"""
import html
import json
from urllib.parse import quote
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "book"))
import shell as SH
from shell import smart, inline, telify, md, split_sources, plain, ico, mask, ICONS  # noqa: F401
import importlib.util as _iu

ROOT = S.ROOT
SRC = ROOT / "content/scale-v2"
OUT = ROOT / "library/scale"
BASE = "/scale"
URL = S.DOMAIN + BASE
PLAN = json.loads((SRC / "plan.json").read_text())
OLD = json.loads((SRC / "old_routes.json").read_text())
CH = {c["slug"]: c for c in PLAN["chapters"]}
ORDER = [c["slug"] for c in PLAN["chapters"]]
PARTS = {p["id"]: p for p in PLAN["parts"]}
SH.BASE = BASE
ROMAN = {"i": "I", "ii": "II", "iii": "III", "iv": "IV", "v": "V", "vi": "VI"}
NOT_MOVEMENTS = ("start", "tools", "appendix")
TOOLS = next((p["id"] for p in PLAN["parts"] if p["id"] in ("tools", "appendix")), None)

spec = _iu.spec_from_file_location("nf_catalogue", ROOT / "scripts/nf-catalogue.py")
CAT = _iu.module_from_spec(spec); spec.loader.exec_module(CAT)

BOOK = {
    "slug": "scale", "title": "The Weighing", "version": "v4",
    "description": ("A free book on how to be right about people: telling manipulation from ordinary conflict, "
                    "weighing evidence, checking your own read, and trusting again."),
    "genre": ["Psychology", "Critical thinking", "Self-help"],
    "about": ["Discernment", "Manipulation", "Cognitive bias", "Evidence", "Healthy conflict", "Coercive control",
              "Recognising abuse", "Trust"],
    "keywords": ["is it manipulation", "am I being manipulated", "am I overreacting", "red flag or normal",
                 "gut feeling or anxiety", "healthy conflict vs abuse", "free book"],
    "notice_short": ("A thinking tool, not a diagnosis, legal or therapeutic advice. If you are in danger, contact your local "
                     "emergency services."),
}

# Interim skin: the v4 brass on dark, one accent per movement. Replaced in the design phase (DESIGN-STATE.md).
SKY = {
    "start": ("#1a1712", "#3a3122", "#d8b46a"), "i": ("#1a1712", "#3a3122", "#d8b46a"),
    "ii": ("#19170f", "#3b3320", "#dcb66c"), "iii": ("#181710", "#3c3420", "#d9bb72"),
    "iv": ("#17170f", "#3b3521", "#d6bf78"), "v": ("#171710", "#3a3624", "#d2c27e"),
    "vi": ("#161711", "#383826", "#cfc585"), "tools": ("#1b1914", "#36302a", "#d0b894"),
    "appendix": ("#1b1914", "#36302a", "#d0b894"),
}


def parse():
    return SH.parse(SRC)


MANIFEST = json.loads((ROOT / "site_manifest.json").read_text())
CRISIS = {"when-weighing-stops", "before-you-test-is-testing-safe", "this-book-in-the-wrong-hands"}   # byline only (06-ABOUT, rules)
TEL_PAGES = {"when-weighing-stops"}


# ---------------------------------------------------------------- page frame
FONTS = "".join(f"@font-face{{font-family:'Fraunces';font-weight:{w};font-style:{st};font-display:swap;src:url({BASE}/f/fraunces-{w}-{st}.woff2) format('woff2')}}"
                for w, st in (("400", "normal"), ("400", "italic"), ("600", "normal"), ("700", "normal")))

CSS = """
:root{color-scheme:dark;--night:#110e19;--panel:#1a1527;--panel2:#221c33;--fg:#efe9f4;--fg2:#bdb3cc;--line:#2f2842;
--disp:'Fraunces',Georgia,serif;--body:'Fraunces',Georgia,serif;--sans:var(--body)}
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
""" + SH.SHELL_CSS + f"""/* Just the steps: keep the short answer, the step, the decoder, safety links, lists and tables */
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

# The Weighing's own fixes on top of the inherited skin: long sister-book titles and printable blank lines must wrap on phones
CSS += "article .blk-bridge a{white-space:normal}article .blk-sheet p,article .blk-sheet li{overflow-wrap:anywhere}"

JS = SH.js(OLD['chapters'], OLD['routes'], BASE)


def house():
    return SH.house("scale")


_jb = _iu.spec_from_file_location("build_jsbook", ROOT / "scripts/seo/build_jsbook.py")
JB = _iu.module_from_spec(_jb); _jb.loader.exec_module(JB)


def labels(h):
    """Box labels are reader text in this book ("The exercise", "Rule one"): print them as the box's first line."""
    def one(m):
        kind, arg = m.group(1), html.unescape(m.group(2))
        danger = arg.startswith("danger")
        arg = arg[6:].strip() if danger else arg
        cls = f"blk blk-{kind}" + (" blk-danger" if danger else "")
        if kind == "bridge":   # "book:slug" is link data, not reader text (R1 2026-11-24: it was printing as a label)
            return f'<div class="{cls}" data-to="{html.escape(arg)}">'
        return f'<div class="{cls}"><p class="blk-k">{html.escape(arg, quote=False)}</p>' if arg else f'<div class="{cls}">'
    h = re.sub(r'<div class="blk blk-(\w+)" data-arg="([^"]*)">', one, h)
    used = set(re.findall(r' id="([^"]+)"', h))

    def h3(m):   # sub-headings get an anchor too, so every heading can be linked to and cited
        hid = S.slugify(plain(m.group(1)), 60)
        while hid in used:
            hid += "-2"
        used.add(hid)
        return f'<h3 id="{hid}">{m.group(1)}</h3>'
    return re.sub(r"<h3>(.*?)</h3>", h3, h)


HOUSE = None


def a11y(body):
    """Weighing-only accessibility fixes (axe 2026-11-24), kept out of shell.py so The Long After stays byte-identical:
    scrollable tables reachable by keyboard, no empty header cells, and FAQ "Read more" links named after their question."""
    n = iter(range(1, 99))
    body = re.sub(r'<div class="tbl"><table>', lambda m: f'<div class="tbl" tabindex="0" role="region" aria-label="Table {next(n)}, scrolls sideways"><table>', body)
    body = body.replace("<thead><tr><th></th>", "<thead><tr><td></td>")
    # tool cards: "When ..." and "Ask yourself: ..." are two lines (v5.1 retention card)
    body = re.sub(r'(<div class="blk blk-tool"><p class="blk-k">[^<]*</p>\s*<p>)(When [^<]*?)\s+(Ask yourself:)',
                  r'\1<span class="when">\2</span></p><p class="ask">\3', body)
    body = body.replace('<div class="blk blk-ask">\n<p>Ask yourself:', '<div class="blk blk-ask">\n<p class="ask">Ask yourself:')
    return re.sub(r'(<strong>([^<]+\?)</strong>[^<]*)<a href="([^"]+)">Read more</a>',
                  lambda m: f'{m.group(1)}<a href="{m.group(3)}" aria-label="Read more: {m.group(2)}">Read more</a>', body)


def whole_sentences(text, n=158):
    """Meta description from the short answer: whole sentences up to n chars; if that is under 110 chars, cut at a word."""
    t = plain(text)
    out = ""
    for sent in re.split(r"(?<=[.?!])\s+", t):
        if len(out) + len(sent) + 1 > n:
            break
        out = (out + " " + sent).strip()
    return out if len(out) >= 110 else S.clip(t, n)


def frame(*, title, desc, url, ld, body, part, robots=None, og_type="article", extra_css=""):
    s1, s2, acc = SKY.get(part, SKY["start"])
    order = list(SKY)
    dawn = round(max(0, order.index(part) - 1) / 6, 2) if part in order and part not in ("tools", "appendix") else 0.1
    hc, hh, hj, beacon = HOUSE
    head = S.head_tags(BOOK, title, desc, url, f"{URL}/og.png", "The Weighing by Shae Stovell, free to read", og_type)
    if robots:
        head = re.sub(r'<meta name="robots"[^>]*>', f'<meta name="robots" content="{robots}">', head)
    body = body.replace('<div class="sky"', '<div class="sky" role="region" aria-label="Title"', 1)
    body = a11y(body)
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + head +
            f'<meta name="theme-color" content="{s1}">\n'
            f'<link rel="preload" href="{BASE}/f/fraunces-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
            "<script>document.documentElement.className+=' js'</script>\n"
            f"<style>{FONTS}{CSS}{extra_css}:root{{--s1:{s1};--s2:{s2};--acc:{acc};--dawn:{dawn}}}</style>\n{hc}\n"
            + (f'<script type="application/ld+json">{S.ld_json(ld)}</script>\n' if ld else "") + "</head>\n<body>\n"
            '<a class="skip" href="#text">Skip to the text</a>\n'
            f'<header class="bar"><a class="home" href="{BASE}">The Weighing</a>'
            f'<a class="b" href="{BASE}/search">Search</a><a class="b" href="{BASE}/when-weighing-stops">Help</a>'
            '<button class="leave" type="button" data-leave aria-label="Leave this page now">Leave</button></header>\n'
            + body +
            f'\n<footer><div class="wrap"><p>{S.LICENSE_LINE}</p><p>{BOOK["notice_short"]} '
            f'<a href="{BASE}/limits">What this book can\u2019t do</a>.</p>'
            f'<nav aria-label="More"><a href="{BASE}">The Weighing</a><a href="{BASE}/contents">Every chapter</a>'
            f'<a href="{BASE}/search">Search</a><a href="{BASE}/all">The whole book on one page</a><a href="/playbook">The Pattern Decoder</a>'
            f'<a href="/topics">All topics</a><a href="{MANIFEST["about_url"]}">Who made this</a><a href="/">Noble Father Creations</a></nav>'
            '<button class="disc" type="button" data-discreet aria-pressed="false" data-js>Discreet mode</button></div></footer>\n'
            + hh + "\n" + hj + "\n" + JS + "\n" + beacon + "\n</body>\n</html>\n")


def loc_line(c):
    if c["part"] == "start":
        return f'<a href="{BASE}">Start here</a>'
    if c["part"] in ("tools", "appendix"):
        return f'<a href="{BASE}#toolbox">Toolbox</a>'
    p = PARTS[c["part"]]
    n = p["chapters"].index(c["slug"]) + 1
    return f'<a href="{BASE}#part-{c["part"]}">Movement {ROMAN[c["part"]]}: {html.escape(p["title"])}</a>, chapter {n} of {len(p["chapters"])}'


def crumbs(c, url):
    trail = [("Noble Father Creations", S.DOMAIN + "/"), ("The Weighing", URL)]
    if c["part"] not in NOT_MOVEMENTS:
        trail.append((f"Movement {ROMAN[c['part']]}: {PARTS[c['part']]['title']}", f"{URL}#part-{c['part']}"))
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
    m = dict(ch["meta"])
    m.setdefault("question", "")
    m.setdefault("seo", f'{c["title"]}: The Weighing')
    url = f"{URL}/{slug}"
    main, src = split_sources(ch["body"])
    body_html = labels(md(main))
    dec_html, _ = JB.decoder_block(c["title"], body_html)
    body_html += dec_html
    if slug in TEL_PAGES:
        body_html = telify(body_html)
    if False:
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
    desc = m.get("desc") or whole_sentences(m["short"], 158)
    title = m["seo"]
    node = {"@type": "Chapter", "@id": url + "#chapter", "name": c["title"], "position": pos, "url": url,
            "isPartOf": {"@id": URL + "#book"}, "author": {"@id": S.PERSON["@id"]}, "inLanguage": "en",
            "isAccessibleForFree": True, "license": S.LICENSE_URL, "description": m["short"], "abstract": m["short"],
            "keywords": ", ".join([k for k in [c["keyword"]] + c["keywords2"] if k])}
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
        graph.append({"@type": "DefinedTermSet", "@id": url + "#terms", "name": "The Weighing: terms", "hasDefinedTerm": terms(main)})
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
            f'<h1 id="top">{title_h}</h1>' + (f'<p class="q">{html.escape(smart(m["question"]))}</p>' if m["question"] else "") +
            f'<p class="by">By <a href="{MANIFEST["about_url"]}">{MANIFEST["author"]}</a> \u00b7 Last reviewed <time datetime="{S.TODAY}">{S.TODAY_HUMAN}</time> \u00b7 <span style="white-space:nowrap">{mins} min read</span></p>'
            '<div class="hrow"><div class="tools" data-js><div class="mode" role="group" aria-label="How much to show">'
            '<button type="button" data-mode="full" aria-pressed="true">Full read</button><button type="button" data-mode="steps" aria-pressed="false">Just the steps</button></div>'
            f'<button class="disc" type="button" data-discreet aria-pressed="false">Discreet mode</button></div>{otp}</div></div></div>\n'
            f'<main id="text">{callnow}<section class="short" aria-label="The short answer"><p class="lab">The short answer</p>'
            f'<p>{(inline(m["short"]))}</p></section>\n<p class="notice">{BOOK["notice_short"]} <a href="{BASE}/how-to-use-this-book">Full notice</a>.</p>\n<article>{body_html}</article>{src_html}{nxt}{end}</main>')
    return frame(title=title, desc=desc, url=url, ld={"@context": "https://schema.org", "@graph": graph}, body=body, part=c["part"])


def contents_list():
    out = ['<ol class="path">']
    for pid in [p["id"] for p in PLAN["parts"] if p["id"] not in NOT_MOVEMENTS]:
        p = PARTS[pid]
        out.append(f'<li id="part-{pid}" style="--pa:{SKY[pid][2]}"><h3 id="ph-{pid}"><small>MOVEMENT {ROMAN[pid]}</small>{html.escape(p["title"])}</h3><ol>')
        for s in p["chapters"]:
            c = CH[s]
            out.append(f'<li><a href="{BASE}/{s}"><b>{html.escape(c["title"])}</b><span>{html.escape(smart(META[s].get("question") or META[s]["short"]))}</span></a></li>')
        out.append("</ol></li>")
    out.append("</ol>")
    return "\n".join(out)


def tools_list():
    return ('<ul class="where" id="toolbox-list">' + "".join(
        f'<li><a href="{BASE}/{s}">{html.escape(CH[s]["title"])}</a></li>' for s in (PARTS[TOOLS]["chapters"] if TOOLS else [])) + "</ul>")


def index_html():
    graph = [dict(S.book_node(BOOK, [CH[s] for s in ORDER]), **{"mainEntityOfPage": URL}),
             {"@type": "WebPage", "@id": URL, "url": URL, "name": "The Weighing: Is It Manipulation or Ordinary Conflict?",
              "description": BOOK["description"], "inLanguage": "en", "about": {"@id": URL + "#book"},
              "dateModified": S.TODAY, "isAccessibleForFree": True, "license": S.LICENSE_URL}, S.PERSON, S.ORG]
    start = "".join(f'<li><a href="{BASE}/{s}">{html.escape(CH[s]["title"])}</a></li>' for s in (PARTS["start"]["chapters"] if "start" in PARTS else []))
    body = (f'<div class="sky"><div class="cover">'
            f'<img src="{BASE}/cover.webp" width="720" height="1073" alt="The Weighing by Shae Stovell, book cover" fetchpriority="high">'
            '<h1>The Weighing</h1><p class="q">How to be right about people. A free book on telling manipulation from ordinary conflict, '
            'weighing the evidence, checking your own read, and trusting again.</p></div></div>\n<main id="text">'
            f'<p class="safe">In danger right now? Stop weighing and get safe. <a href="{BASE}/when-weighing-stops">When weighing stops</a>. '
            'The <b>Leave</b> button at the top clears this page instantly.</p>'
            + (f'<section class="sec" aria-labelledby="w-h"><h2 id="w-h">Start here</h2><ul class="where">{start}</ul></section>' if start else "") +
            f'<section class="sec" aria-labelledby="s-h"><h2 id="s-h">Search</h2><p class="lede">Type it the way you\u2019d say it. Nothing you type leaves this page.</p>'
            f'<form class="find" action="{BASE}/search" method="get" role="search"><label class="skip" for="q">Search the book</label>'
            '<input id="q" name="q" type="search" placeholder="am i overreacting" autocomplete="off"><button type="submit">Search</button></form></section>'
            f'<section class="sec" id="contents" aria-labelledby="c-h"><h2 id="c-h">Contents</h2>'
            '<p class="lede">Six movements, from why to weigh at all to trusting people again. Every chapter stands alone.</p>'
            f'{contents_list()}</section>'
            f'<section class="sec" id="toolbox" aria-labelledby="t-h"><h2 id="t-h">Toolbox</h2><p class="lede">Things to keep, print or screenshot.</p>{tools_list()}</section>'
            f'<section class="sec" id="who" aria-labelledby="who-h"><h2 id="who-h">Who made this</h2><p class="lede">{html.escape(MANIFEST["who_made_this"])} '
            f'<a href="{MANIFEST["about_url"]}">Read why \u2192</a></p></section>'
            '<section class="sec" id="updates" aria-labelledby="u-h"><h2 id="u-h">Updates</h2>'
            '<p class="lede">v4 \u00b7 21 November 2026. Every chapter got its own page, a contents page, links to the matching patterns in the '
            'Pattern Decoder, and new cover art. v3 \u00b7 1 September 2026. The list of other books was brought up to date. '
            'v2 \u00b7 5 August 2026. A leftover build note was removed.</p></section></main>')
    return frame(title="The Weighing: Is It Manipulation or Ordinary Conflict?", desc=BOOK["description"], url=URL,
                 ld={"@context": "https://schema.org", "@graph": graph}, body=body, part="start", og_type="book")


def simple(title, desc, url, inner, robots=None, part="start", ld=None):
    body = (f'<div class="sky"><div class="in"><p class="loc"><a href="{BASE}">The Weighing</a></p><h1 id="top">{title}</h1></div></div>'
            f'<main id="text"><div class="wrap" style="padding-top:24px">{inner}</div></main>')
    return frame(title=f"{plain(title)} \u00b7 The Weighing", desc=desc, url=url, ld=ld, body=body, part=part, robots=robots)


def search_html():
    idx = [{"s": s, "t": CH[s]["title"], "q": META[s].get("question") or META[s]["short"],
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
             f"if(!sc.length){{r.innerHTML='<li>No match. Try other words, or see <a href=\"{BASE}/contents\">every chapter</a>.</li>';return}}"
             f"sc.forEach(function(p){{var x=p[1],li=document.createElement('li'),a=document.createElement('a');a.href='{BASE}/'+x.s;a.textContent=x.t;var sp=document.createElement('span');sp.textContent=x.q;a.appendChild(sp);li.appendChild(a);r.appendChild(li)}})}}"
             "document.getElementById('sb').onclick=go;document.getElementById('sq').oninput=go;"
             "var u=new URLSearchParams(location.search).get('q');if(u){document.getElementById('sq').value=u;go()}</script>")
    return simple("Search", "Search The Weighing. Nothing you type leaves this page.", f"{URL}/search", inner, robots="noindex, follow")


def all_html():
    parts = []
    for s in ORDER:
        c, mm = CH[s], META[s]
        main, _ = split_sources(META_BODY[s])
        parts.append(f'<section id="{s}"><h2 style="font:400 2rem/1.15 var(--disp);color:#fff;margin:2.4em 0 .2em">{html.escape(c["title"])}</h2>' +
                     (f'<p class="q" style="color:var(--fg2)">{html.escape(smart(mm["question"]))}</p>' if mm.get("question") else "") +
                     f'<div class="short" style="margin:16px 0"><p class="lab">The short answer</p><p>{(inline(mm["short"]))}</p></div>'
                     f'<article>{md(main)}</article></section>')
    toc = "<ol>" + "".join(f'<li><a href="#{s}">{html.escape(CH[s]["title"])}</a></li>' for s in ORDER) + "</ol>"
    inner = ('<p class="lede">The whole book on one page, for reading offline or printing. Save this page to keep it on your device. '
             f'Each chapter also has its own page with sources.</p><details><summary>Contents</summary>{toc}</details>' + "".join(parts))
    return simple("The whole book on one page", "The Weighing, every chapter on one page.", f"{URL}/all", inner, robots="noindex, follow")


def contents_html():
    n = len([s for s in ORDER if CH[s]["part"] not in NOT_MOVEMENTS])
    inner = (f'<p class="lede">Every chapter of The Weighing, by movement. {n} chapters, free to read.</p>'
             f'<h2 id="the-six-movements" style="font:400 1.6rem/1.2 var(--disp);color:#fff">The six movements</h2>{contents_list()}'
             f'<h2 id="toolbox">Toolbox</h2>{tools_list()}<p class="notice" style="margin-top:28px">{BOOK["notice_short"]} <a href="{BASE}/how-to-use-this-book">Full notice</a>. <a href="{BASE}/limits">What this book can\u2019t do</a>.</p>')
    graph = [{"@type": "CollectionPage", "@id": URL + "/contents", "url": URL + "/contents", "name": "The Weighing: Every Chapter",
              "isPartOf": {"@id": URL + "#book"}, "inLanguage": "en", "dateModified": S.TODAY,
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(ORDER), "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": f"{URL}/{s}", "name": CH[s]["title"]} for i, s in enumerate(ORDER)]}},
             S.crumbs_ld([("Noble Father Creations", S.DOMAIN + "/"), ("The Weighing", URL), ("Every chapter", URL + "/contents")]),
             S.book_node(BOOK), S.PERSON, S.ORG]
    return simple("Every chapter, by movement", "Every chapter of The Weighing, a free book on how to be right about people, by movement.",
                  URL + "/contents", inner, ld={"@context": "https://schema.org", "@graph": graph})


def redirect_html(to):
    u = f"{URL}/{to}"
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex, follow">'
            f'<link rel="canonical" href="{u}"><meta http-equiv="refresh" content="0; url={BASE}/{to}"></head>'
            f'<body><p>This page has moved: <a href="{BASE}/{to}">{BASE}/{to}</a></p></body></html>\n')


META, META_BODY = {}, {}


def share_card():
    n = sum(1 for c in PLAN["chapters"] if c["part"] not in NOT_MOVEMENTS)
    card = {"slug": "scale", "title": "The Weighing", "fonts": ["fraunces"],
            "theme": {"bg": "#16140F", "fg": "#E7DFCE", "fg2": "#A09683", "panel": "#1D1A14", "glow": "#3A342A", "acc": "#C29A52",
                      "disp": "'fraunces',Georgia,serif", "body": "'fraunces',Georgia,serif"}}
    S.make_og(card, OUT, f"Free to read \u00b7 {n} chapters", "How to be right about people.")


def llms_txt():
    """A plain map of the book for AI assistants (llmstxt.org format): every page with its one-line answer."""
    out = [f"# {BOOK['title']}", "", f"> {BOOK['description']} By {MANIFEST['author']} ({S.DOMAIN}{MANIFEST['about_url']}). "
           "Free to read, no account, nothing stored. A thinking tool, not a diagnosis, legal or therapeutic advice.", "",
           f"The whole book on one page: {URL}/all", f"Every chapter: {URL}/contents", ""]
    for p in PLAN["parts"]:
        name = p["title"] if p["id"] in NOT_MOVEMENTS else f"Movement {ROMAN[p['id']]}: {p['title']}"
        out.append(f"## {name}")
        out += [f"- [{CH[s]['title']}]({URL}/{s}): {plain(inline(META[s]['short']))}" for s in p["chapters"]]
        out.append("")
    out += ["## Related", f"- [The Pattern Decoder]({S.DOMAIN}/playbook): the named tactics this book links to",
            f"- [The Long After]({S.DOMAIN}/longafter): life after leaving an abusive relationship",
            f"- [All books]({S.DOMAIN}/llms.txt)", ""]
    return "\n".join(out)


def main():
    global HOUSE
    chs = parse()
    missing = [s for s in ORDER if s not in chs]
    assert not missing, f"unwritten pages: {missing}"
    for s in ORDER:
        META[s] = chs[s]["meta"]; META_BODY[s] = chs[s]["body"]
    HOUSE = house()
    keep = {"index.html", "contents.html", "search.html", "all.html"}
    for i, s in enumerate(ORDER, 1):
        S.write(OUT / f"{s}.html", page(s, chs[s], i))
        keep.add(f"{s}.html")
    for old, new in PLAN.get("old_redirects", {}).items():
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
    S.write(OUT / "llms.txt", llms_txt())
    if "--og" in sys.argv:
        share_card()
    print(f"scale {BOOK['version']}: {len(ORDER)} pages + index, contents, search, all; {len(stale)} stale pages removed; sitemap {len(urls)} URLs")


if __name__ == "__main__":
    main()
