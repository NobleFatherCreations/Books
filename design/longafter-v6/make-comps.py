#!/usr/bin/env python3
"""The Long After v6: three design comps (A Notes on the table, B Margins, C Horizon cards).

Run:  python3 design/longafter-v6/make-comps.py
Reads built pages from library/longafter/ (never writes there) and writes
design/longafter-v6/comps/{a,b,c}/<page>.html. Each comp is the built page plus ONE extra <style> block and, on pages
with a decoder block, one small <script> (splits the decoder paragraph into its three voices without changing a word,
and adds a Copy button on the reply). No external requests, no storage, only the fonts already on the page.
Preview: python3 design/longafter-v6/serve-comps.py  ->  http://127.0.0.1:8766/design/longafter-v6/comps/a/index.html
"""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "library/longafter"
OUT = Path(__file__).resolve().parent / "comps"
PAGES = ["index", "the-trauma-bond", "family-court-honestly", "court-day-checklist",
         "abuse-or-a-hard-breakup"]  # the last one only to show a bridge block

# ------------------------------------------------------------------ icons (Lucide paths, tools/lucide-icons-lucide)
P = {
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
    "sunrise": '<path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m8 6 4-4 4 4"/><path d="M16 18a4 4 0 0 0-8 0"/>',
    "feather": '<path d="M14.086 18.412A2 2 0 0112.67 19H5v-7.672a2 2 0 01.586-1.414L11.75 3.75a6 6 0 118.49 8.49z"/><path d="M16 8 2 22"/><path d="M17.488 15H9"/>',
    "signpost": '<path d="M12 13v8"/><path d="M12 3v3"/><path d="M2.354 10.354a1.207 1.207 0 0 1 0-1.708l2.06-2.06A2 2 0 0 1 5.828 6h12.344a2 2 0 0 1 1.414.586l2.06 2.06a1.207 1.207 0 0 1 0 1.708l-2.06 2.06a2 2 0 0 1-1.414.586H5.828a2 2 0 0 1-1.414-.586z"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
}


def ico(name, stroke="black", w=1.75):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{stroke}' stroke-width='{w}' "
           f"stroke-linecap='round' stroke-linejoin='round'>{P[name].replace(chr(34), chr(39))}</svg>")
    return 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'


def mask(name):
    i = ico(name)
    return f"-webkit-mask:{i} center/contain no-repeat;mask:{i} center/contain no-repeat;"


WHERE = 'section[aria-labelledby="w-h"]>ul.where'
MORE = 'section[aria-labelledby="w-h"] details.more ul.where'
CHOICE_ICONS = {"i-left-in-the-last-few-days": "door", "they-keep-contacting-me": "msg", "we-have-children-together": "users",
                "theres-a-court-case": "scale", "i-dont-feel-safe": "shield", "i-cant-stop-thinking-about-them": "moon"}
CHOICE_VARS = "".join(f'{WHERE} a[href$="#{k}"]{{--ico:{ico(v)}}}' for k, v in CHOICE_ICONS.items())
ICO_MASK = "-webkit-mask:var(--ico) center/contain no-repeat;mask:var(--ico) center/contain no-repeat;"
SC = "font-variant-caps:all-small-caps;letter-spacing:.07em;font-weight:700;"  # small-caps label

# ------------------------------------------------------------------ shared by all three comps
SHARED = f"""
/* v6 comp: shared */
article>h2::before{{content:"";display:block;height:1px;margin:0 0 1.1em;
background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--acc) 80%,transparent) 50%,transparent)}}
article .blk{{margin:2.5rem 0;position:relative}}
article .blk h2{{margin-top:0;scroll-margin-top:76px}}
article .blk>:last-child{{margin-bottom:0}}
.bar::after{{content:"";position:absolute;left:0;right:0;bottom:-1px;pointer-events:none}}
.dv-p{{display:flex;flex-direction:column;max-width:none!important;margin:0!important}}
.dv,.dv-l,.dv-t{{display:block}}
.dv-copy{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;min-width:44px;cursor:pointer;font:600 1rem/1 var(--sans)}}
.dv-copy::before{{content:"";width:16px;height:16px;background:currentColor;{mask('copy')}}}
{CHOICE_VARS}
{WHERE}{{grid-template-columns:1fr 1fr}}
{WHERE}>li,{MORE}>li{{display:flex}}{WHERE} a,{MORE} a{{flex:1}}
article .blk-sheet ul.checks li{{padding-left:1.25em;text-indent:-1.25em}}
{MORE}{{grid-template-columns:1fr 1fr}}
@media print{{.dv-copy,.bar::after{{display:none!important}}article>h2::before{{background:#999}}}}
"""

# ------------------------------------------------------------------ A: Notes on the table
A = f"""
/* v6 comp A: Notes on the table */
.bar{{border-bottom-color:transparent}}
.bar::after{{height:3px;background:linear-gradient(90deg,var(--s1),var(--s2) 22%,var(--acc) 50%,var(--s2) 78%,var(--s1))}}
.sky{{background:linear-gradient(180deg,var(--s1) 0%,var(--s2) 74%,color-mix(in srgb,var(--s2) 62%,var(--acc)) 100%)}}
article .blk h2{{font:400 1.45rem/1.25 var(--disp);color:#fff;margin-bottom:.5em}}
.blk-action::before,.blk-scene::before,.blk-sheet::before{{display:block;font-family:var(--sans);font-size:1rem;line-height:1.2;{SC}margin:0 0 10px}}
/* action: an index card with a hand-drawn circle */
article .blk-action{{background-color:#2a2232;background-image:repeating-linear-gradient(180deg,transparent 0 30px,rgba(239,233,244,.05) 30px 31px);
background-position:0 66px;border-top:3px solid var(--acc);border-radius:4px 4px 12px 12px;padding:18px 20px 20px;
box-shadow:0 18px 32px -18px rgba(0,0,0,.75),inset 0 1px 0 rgba(255,255,255,.04)}}
.blk-action::before{{content:"One small step";color:var(--acc)}}
article .blk-action h2{{position:relative;padding-left:42px}}
article .blk-action h2::before{{content:"";position:absolute;left:2px;top:.1em;width:26px;height:26px;border:2px solid var(--acc);
border-radius:54% 44% 57% 43% / 46% 56% 44% 54%;transform:rotate(-9deg);box-shadow:1px 1px 0 0 color-mix(in srgb,var(--acc) 35%,transparent)}}
article .blk-action p{{color:#f3edf6}}
/* decoder: two voices as chat bubbles */
article .blk-decoder{{background:#1c1727;border:1px solid #2c2539;border-radius:20px;padding:16px 14px}}
.dv-p{{gap:12px}}
.dv-say{{align-self:flex-start;max-width:90%;background:#2e2839;border-radius:20px 20px 20px 6px;padding:12px 16px}}
.dv-why{{align-self:stretch;color:var(--fg2);font-style:italic;padding:0 10px 0 14px;border-left:2px solid #3b3349;margin:2px 8px}}
.dv-reply{{align-self:flex-end;max-width:90%;display:flex;flex-direction:column;background:var(--acc);color:#1c1322;border-radius:20px 20px 6px 20px;padding:12px 16px 10px}}
.dv-l{{font-family:var(--sans);font-size:1rem;line-height:1.3;{SC}color:var(--fg2);margin:0 0 2px}}
.dv-reply .dv-l{{color:#4a2733}}
.dv-reply .dv-copy{{align-self:flex-end;margin-top:8px;padding:0 16px;border-radius:999px;border:1px solid rgba(28,19,34,.45);background:rgba(28,19,34,.07);color:#1c1322}}
.dv-reply .dv-copy:hover{{background:rgba(28,19,34,.16)}}
/* honest: recessed, private, a small lamp */
article .blk-honest{{background:radial-gradient(110% 70% at 100% 0%,color-mix(in srgb,var(--acc) 15%,transparent),transparent 62%),#0b0911;
border-radius:20px;padding:22px 20px;box-shadow:inset 0 4px 14px rgba(0,0,0,.75),inset 0 0 0 1px rgba(255,255,255,.035)}}
.blk-honest::before{{content:"";position:absolute;right:18px;top:20px;width:26px;height:26px;background:var(--acc);{mask('lamp')}}}
article .blk-honest h2{{padding-right:40px}}
article .blk-honest p:first-of-type{{color:var(--fg2)}}
/* scene: a softer paper tone, in italics */
article .blk-scene{{background:#251f2e;border:1px solid #362e43;border-radius:4px 16px 16px 16px;padding:18px 20px 20px}}
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
.blk-sheet::before{{content:"Printable sheet";color:var(--fg2);padding-left:30px;min-height:22px;
background:{ico('printer', '#bdb3cc')} left center/22px no-repeat}}
.blk-sheet::after{{content:"";position:absolute;right:28px;top:-14px;width:28px;height:26px;background:var(--night) {ico('scissors', '#bdb3cc')} center/22px no-repeat}}
article .blk-sheet h2{{font-size:1.3rem;margin:1.3em 0 .3em}}
article .blk-sheet h2:first-of-type{{margin-top:.2em}}
article .blk-sheet ul.checks li{{padding:.5em 0;border-bottom-color:#2d2639}}
/* cover choices */
{WHERE}{{gap:10px}}
{WHERE} a{{flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:12px;min-height:116px;padding:14px 14px 16px;
background:#231c2e;border-color:#362c45;border-radius:16px 16px 16px 5px;font-size:1.1rem;line-height:1.28}}
{WHERE} a::before{{content:"";flex:none;width:28px;height:28px;background:var(--acc);{ICO_MASK}}}
{WHERE} a[href$="#i-dont-feel-safe"]{{background:#2a1722;border-color:#5a2633}}
{WHERE} a[href$="#i-dont-feel-safe"]::before{{background:#ffb4a6}}
{MORE} a{{min-height:64px;padding:10px 12px;font-size:1.1rem;line-height:1.28;border-radius:12px}}
@media print{{article .blk-sheet{{border-color:#000;background:none}}.blk-sheet::after{{background-color:#fff}}article .blk-action,article .blk-scene,article .blk-honest,article .blk-decoder{{background:none;box-shadow:none;border:1px solid #999}}.dv-reply{{background:#eee}}}}
"""

# ------------------------------------------------------------------ B: Margins
B = f"""
/* v6 comp B: Margins */
.bar{{border-bottom-color:transparent}}
.bar::after{{height:1px;background:linear-gradient(90deg,transparent,var(--acc) 50%,transparent)}}
.sky{{background:linear-gradient(180deg,var(--s1) 0%,var(--s2) 82%,color-mix(in srgb,var(--s2) 72%,var(--acc)) 100%)}}
.short{{background:none;border:0;border-top:3px solid var(--acc);border-radius:0;padding:14px 0 0;margin-top:28px}}
article .blk h2{{font:400 1.5rem/1.25 var(--disp);color:#fff;margin-bottom:.45em}}
.blk-action::before,.blk-scene::before,.blk-sheet::before{{display:block;font-family:var(--sans);font-size:1rem;line-height:1.2;{SC}margin:0 0 8px}}
/* action: a thick accent rule and a label */
article .blk-action{{border-top:6px solid var(--acc);padding-top:14px}}
.blk-action::before{{content:"One small step";color:var(--acc)}}
/* decoder: a two-column script */
.dv-p{{gap:0}}
.dv{{display:grid;grid-template-columns:6.5rem minmax(0,1fr);gap:0 16px;padding:14px 0;border-top:1px solid var(--line)}}
.dv:last-child{{border-bottom:1px solid var(--line)}}
.dv-l{{font-family:var(--sans);font-size:1rem;line-height:1.3;{SC}color:var(--fg2);padding-top:.25em}}
.dv-say .dv-t{{font-style:italic}}
.dv-why .dv-t{{color:var(--fg2)}}
.dv-reply .dv-l{{color:var(--acc)}}
.dv-reply .dv-t{{color:#fff;border-left:2px solid var(--acc);padding-left:14px}}
.dv-reply .dv-copy{{grid-column:2;justify-self:start;margin:6px 0 -8px 2px;padding:0 4px;border:0;background:none;color:var(--acc);text-decoration:underline;text-underline-offset:.2em}}
/* honest: a full-bleed tinted band */
article .blk-honest{{--band:color-mix(in srgb,var(--acc) 9%,#110e19);background:var(--band);box-shadow:0 0 0 100vmax var(--band);clip-path:inset(0 -100vmax);padding:30px 0 28px;margin:3rem 0}}
article .blk-honest p:first-of-type{{color:var(--fg2)}}
/* scene: indented italic with a hairline */
article .blk-scene{{margin-left:4px;padding-left:20px;border-left:1px solid color-mix(in srgb,var(--fg2) 45%,transparent)}}
.blk-scene::before{{content:"A made-up story";color:var(--fg2)}}
article .blk-scene p{{font-style:italic}}
article .blk-scene p:first-of-type{{color:var(--fg2)}}
/* bridge: an em-rule and small caps */
article .blk-bridge::before{{content:"";display:block;width:2.4em;height:1px;background:var(--acc);margin:0 0 12px}}
article .blk-bridge a{{font-size:1.12em;{SC}}}
/* sheet: a framed print area */
article .blk-sheet{{border:1px solid color-mix(in srgb,var(--fg2) 60%,transparent);outline:1px solid var(--line);outline-offset:5px;padding:26px 20px 14px;margin:3rem 6px}}
.blk-sheet::before{{content:"For print";position:absolute;top:-.75em;left:14px;padding:0 8px;background:var(--night);color:var(--fg2);margin:0}}
article .blk-sheet h2{{font-size:1.3rem;margin:1.3em 0 .3em}}
article .blk-sheet h2:first-of-type{{margin-top:0}}
/* cover choices: a ruled list, no boxes */
{WHERE}{{gap:0 18px}}
{WHERE} a{{position:relative;align-items:flex-start;min-height:72px;padding:14px 0 14px 34px;background:none;border:0;border-top:1px solid var(--line);border-radius:0;font-size:1.1rem;line-height:1.3}}
{WHERE} a::before{{content:"";position:absolute;left:0;top:16px;width:22px;height:22px;background:var(--acc);{ICO_MASK}}}
{MORE}{{gap:0 18px}}
{MORE} a{{min-height:60px;padding:12px 0;background:none;border:0;border-top:1px solid var(--line);border-radius:0;font-size:1.1rem;line-height:1.3;align-items:flex-start}}
@media (hover:hover) and (pointer:fine){{{WHERE} a:hover,{MORE} a:hover{{color:var(--acc)}}}}
@media print{{article .blk-honest{{box-shadow:none;background:none;clip-path:none;border-top:1px solid #999;border-bottom:1px solid #999}}.blk-sheet::before{{background:#fff}}}}
"""

# ------------------------------------------------------------------ C: Horizon cards
PANEL = "linear-gradient(168deg,color-mix(in srgb,var(--s2) 72%,#0b0912) 0%,var(--s1) 100%)"
C = f"""
/* v6 comp C: Horizon cards */
.bar{{border-bottom-color:transparent}}
.bar::after{{height:4px;background:linear-gradient(90deg,var(--s1),var(--s2) 25%,var(--acc) 50%,var(--s2) 75%,var(--s1))}}
.sky{{background:linear-gradient(180deg,var(--s1) 0%,var(--s2) 70%,color-mix(in srgb,var(--s2) 50%,var(--acc)) 100%)}}
.sky::after{{height:2px;opacity:1}}
article .blk{{border-radius:22px;padding:62px 20px 22px;background:{PANEL};color:#fff;border:1px solid color-mix(in srgb,var(--s2) 70%,#fff 12%)}}
article .blk::before{{content:"";position:absolute;left:18px;top:16px;width:36px;height:36px;border-radius:50%;
background:color-mix(in srgb,var(--acc) 22%,transparent) var(--ico) center/20px no-repeat;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--acc) 45%,transparent)}}
article .blk::after{{position:absolute;left:64px;top:24px;font:700 1rem/1.2 var(--sans);{SC}color:var(--acc)}}
article .blk h2{{font:400 1.5rem/1.25 var(--disp);color:#fff;margin-bottom:.5em}}
article .blk p,article .blk li{{color:#f6f1f8}}
article .blk a{{color:var(--acc)}}
.blk-action{{--ico:{ico('sunrise', '#fff')}}}.blk-action::after{{content:"One small step"}}
.blk-decoder{{--ico:{ico('msg', '#fff')}}}.blk-decoder::after{{content:"Two voices"}}
.blk-honest{{--ico:{ico('lamp', '#fff')}}}.blk-honest::after{{content:"Just for you"}}
.blk-scene{{--ico:{ico('feather', '#fff')}}}.blk-scene::after{{content:"A made-up story"}}
.blk-bridge{{--ico:{ico('signpost', '#fff')}}}
.blk-sheet{{--ico:{ico('printer', '#fff')}}}.blk-sheet::after{{content:"Print this sheet"}}
/* action: the warmest panel, first light along its bottom edge */
article .blk-action{{background:radial-gradient(120% 60% at 50% 115%,color-mix(in srgb,var(--acc) 30%,transparent),transparent 70%),{PANEL};
border-color:color-mix(in srgb,var(--acc) 55%,transparent)}}
/* honest: the darkest panel, lamp glow in one corner */
article .blk-honest{{background:radial-gradient(90% 60% at 0% 0%,color-mix(in srgb,var(--acc) 18%,transparent),transparent 70%),linear-gradient(180deg,var(--s1),#0d0b15)}}
article .blk-honest p:first-of-type{{color:#d9cfe3}}
/* scene */
article .blk-scene p{{font-style:italic}}
article .blk-scene p:first-of-type{{color:#d9cfe3}}
/* decoder */
.dv-p{{gap:12px}}
.dv-say{{align-self:flex-start;max-width:92%;background:rgba(6,4,12,.42);border-radius:18px 18px 18px 6px;padding:12px 16px}}
.dv-why{{color:#e3dbea;padding:0 4px}}
.dv-reply{{align-self:flex-end;max-width:92%;display:flex;flex-direction:column;background:var(--acc);color:#1c1322;border-radius:18px 18px 6px 18px;padding:12px 16px 10px}}
.dv-l{{font-family:var(--sans);font-size:1rem;line-height:1.3;{SC}color:#d9cfe3;margin:0 0 2px}}
.dv-reply .dv-l{{color:#4a2733}}
.dv-reply .dv-copy{{align-self:flex-end;margin-top:8px;padding:0 16px;border-radius:999px;border:0;background:#1c1322;color:var(--acc)}}
/* bridge: a slim panel */
article .blk-bridge{{padding:16px 20px 16px 68px;border-radius:18px}}
article .blk-bridge::before{{top:50%;margin-top:-18px}}
article .blk-bridge a{{{SC}font-size:1.12em}}
/* sheet */
article .blk-sheet h2{{font-size:1.3rem;margin:1.3em 0 .3em}}
article .blk-sheet h2:first-of-type{{margin-top:0}}
article .blk-sheet ul.checks li{{border-bottom-color:rgba(255,255,255,.14);padding:.45em 0}}
/* cover choices: each tile a different hour of the night */
{WHERE}{{gap:10px}}
{WHERE} a{{flex-direction:column;align-items:flex-start;justify-content:space-between;gap:14px;min-height:120px;padding:14px;
border:1px solid rgba(255,255,255,.1);border-radius:18px;color:#fff;font-size:1.1rem;line-height:1.28;background:linear-gradient(165deg,var(--t2),var(--t1))}}
{WHERE} a::before{{content:"";width:28px;height:28px;background:#fff;opacity:.92;{ICO_MASK}}}
{WHERE} li:nth-child(1) a{{--t1:#1b1430;--t2:#3a2346}}{WHERE} li:nth-child(2) a{{--t1:#171630;--t2:#3d2c57}}
{WHERE} li:nth-child(3) a{{--t1:#141c36;--t2:#2e3c64}}{WHERE} li:nth-child(4) a{{--t1:#13203a;--t2:#2d4668}}
{WHERE} li:nth-child(5) a{{--t1:#2a1520;--t2:#5a2633}}{WHERE} li:nth-child(6) a{{--t1:#1a2e48;--t2:#4b5068}}
{MORE} a{{min-height:64px;padding:10px 12px;font-size:1.1rem;line-height:1.28;border-radius:14px;background:linear-gradient(165deg,#2a2440,#1a1527)}}
@media print{{article .blk{{background:none!important;color:#000;border:1px solid #999}}article .blk p,article .blk li,article .blk h2{{color:#000}}}}
"""

JS = r"""<script>
/* v6 comp: split each decoder paragraph into its three voices (no words change) and add Copy to the reply. */
(function(){
document.querySelectorAll('.blk-decoder > p').forEach(function(p){
  var segs=[],cur=null;
  [].slice.call(p.childNodes).forEach(function(n){
    if(n.nodeType===1&&n.tagName==='STRONG'){var t=n.textContent;
      cur={k:/^They say/.test(t)?'say':/^What it/.test(t)?'why':/reply/i.test(t)?'reply':'other',l:n,b:[]};segs.push(cur);}
    else if(cur)cur.b.push(n);
  });
  if(segs.length<2)return;
  p.classList.add('dv-p');
  segs.forEach(function(s){
    var w=document.createElement('span'),t=document.createElement('span');
    w.className='dv dv-'+s.k;t.className='dv-t';s.l.classList.add('dv-l');
    p.insertBefore(w,s.l);w.appendChild(s.l);s.b.forEach(function(n){t.appendChild(n)});w.appendChild(t);
    if(s.k==='reply'&&navigator.clipboard){
      var b=document.createElement('button');b.type='button';b.className='dv-copy';b.textContent='Copy';b.setAttribute('aria-live','polite');
      b.addEventListener('click',function(){
        var x=t.textContent.trim(),q=x.match(/\u201c[^\u201d]+\u201d/g);
        if(q)x=q.map(function(s){return s.slice(1,-1)}).join(' ');
        navigator.clipboard.writeText(x).then(function(){b.textContent='Copied';clearTimeout(b._t);b._t=setTimeout(function(){b.textContent='Copy'},2000)});
      });
      w.appendChild(b);
    }
  });
});
})();
</script>"""

VARIANTS = {"a": A, "b": B, "c": C}


def main():
    for v, css in VARIANTS.items():
        d = OUT / v
        d.mkdir(parents=True, exist_ok=True)
        for name in PAGES:
            src = (SRC / f"{name}.html").read_text(encoding="utf-8")
            assert src.count("</head>") == 1 and src.count("</body>") == 1, name
            out = src.replace("</head>", f'<style id="v6-comp-{v}">{SHARED}{css}</style>\n</head>', 1)
            if 'class="blk blk-decoder"' in src:
                out = out.replace("</body>", JS + "\n</body>", 1)
            (d / f"{name}.html").write_text(out, encoding="utf-8")
    print(f"wrote {len(VARIANTS) * len(PAGES)} pages to {OUT.relative_to(ROOT)}/{{a,b,c}}/")


if __name__ == "__main__":
    main()
