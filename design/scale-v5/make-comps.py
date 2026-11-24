#!/usr/bin/env python3
"""The Weighing v5.1: three design comps (A The Instrument, B Plain Speech, C The Ledger) on the v5.1 pilot chapters.

Run:  python3 scripts/seo/build_scale_v2.py && python3 design/scale-v5/make-comps.py
Reads built pages from library/scale/ (never writes there); writes design/scale-v5/comps/{a,b,c}/<page>.html.
Each comp = the built page + one <style> + one small <script> (movement cards on the contents, recall quizzes in batches
of four). No words change, no external requests, no storage. Fonts are the repo's own (tools/fonts).
Preview: python3 design/scale-v5/serve-comps.py  ->  http://127.0.0.1:8766/design/scale-v5/comps/a/index.html
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC, OUT = ROOT / "library/scale", Path(__file__).resolve().parent / "comps"
PAGES = ["index", "the-gradient", "a-boundary-or-a-rule", "field-card", "when-weighing-stops"]


def face(fam, file, style="normal", wght="100 900"):
    return f"@font-face{{font-family:'{fam}';src:url(/tools/fonts/{file}) format('truetype');font-style:{style};font-weight:{wght};font-display:swap}}"


# shared by all three: behaviour fixes from R1 (layout only; each comp skins them)
SHARED = """
html{scroll-padding-top:72px;scroll-padding-bottom:96px}
.sky .cover img{width:min(78vw,340px);height:auto;display:block;margin:0 auto 24px}
article .blk-gradient ul{list-style:none;margin:24px 0;padding:0;display:grid;gap:0}
article .blk-gradient li{position:relative;margin:0}
.blk-tool .when,.blk-ask .ask,.blk-tool .ask{display:block}
.path>li>details>summary{cursor:pointer;list-style:none}
.path>li>details>summary::-webkit-details-marker{display:none}
.sort li.batch-hidden{display:none}
ul.sort{list-style:none;padding-left:0}
.sort-more{border-radius:0}
.sort-more{margin:8px 0 0;min-height:44px;padding:0 16px;font:inherit;cursor:pointer}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = """<script>(function(){
document.querySelectorAll('ol.path>li[id^="part-"]').forEach(function(li){
  var h=li.querySelector('h3'), ol=li.querySelector('ol'); if(!h||!ol) return;
  var d=document.createElement('details'), s=document.createElement('summary');
  s.innerHTML=h.innerHTML+'<span class="cnt">'+ol.children.length+' chapters</span>';
  d.appendChild(s); d.appendChild(ol); h.replaceWith(d);
});
document.querySelectorAll('ul.sort').forEach(function(ul){
  var items=[].slice.call(ul.children); if(items.length<=5) return;
  items.forEach(function(li,i){ if(i>=4) li.classList.add('batch-hidden'); });
  var b=document.createElement('button'); b.type='button'; b.className='sort-more';
  function label(){ var left=ul.querySelectorAll('.batch-hidden').length; b.textContent=left?('Show '+Math.min(4,left)+' more'+(left>4?(' ('+left+' left)'):'')):''; b.hidden=!left; }
  b.addEventListener('click',function(){ [].slice.call(ul.querySelectorAll('.batch-hidden'),0,4).forEach(function(li){li.classList.remove('batch-hidden');}); label(); });
  ul.after(b); label();
});
})();</script>"""

A = face("Newsreader", "newsreader/Newsreader[opsz,wght].ttf") + face("Newsreader", "newsreader/Newsreader-Italic[opsz,wght].ttf", "italic") + \
    face("Plex Mono", "ibmplexmono/IBMPlexMono-Regular.ttf", wght="400") + face("Plex Mono", "ibmplexmono/IBMPlexMono-SemiBold.ttf", wght="600") + """
/* A  The Instrument: data-sheet precision, single hue, ticks and callouts (S-34 + S-53) */
:root{--bg:#0d1013;--ink:#e4e7ea;--dim:#9aa3ab;--line:#2a3138;--acc:#7fd1c7}
body{background:var(--bg)!important;color:var(--ink)!important;font-family:'Newsreader',Georgia,serif!important;font-size:1.12rem}
h1,h2,h3{font-family:'Newsreader',serif!important;font-weight:500!important;letter-spacing:-.01em}
.sky{background:linear-gradient(var(--bg),var(--bg))!important;border-bottom:1px solid var(--line)}
.loc,.blk-k,.lab,.by,.bar a,.bar button,.path small,.cnt,.sort-more,.dock a,.dock button{font-family:'Plex Mono',monospace!important;letter-spacing:.04em}
.loc,.lab,.blk-k,.path small{text-transform:uppercase;font-size:.72rem!important;color:var(--acc)!important}
a{color:var(--acc)}
.short{border:1px solid var(--line)!important;background:none!important;border-radius:0!important;position:relative}
.short::before,.short::after{content:"";position:absolute;width:10px;height:10px;border:1px solid var(--acc)}
.short::before{top:-1px;left:-1px;border-right:0;border-bottom:0}.short::after{bottom:-1px;right:-1px;border-left:0;border-top:0}
article .blk-gradient ul{grid-template-columns:repeat(7,1fr);border-top:1px solid var(--ink);padding-top:0}
article .blk-gradient li{font:600 .66rem/1.2 'Plex Mono',monospace;text-transform:uppercase;padding:18px 2px 0;text-align:center;color:var(--dim)}
article .blk-gradient li::before{content:"";position:absolute;top:0;left:50%;width:1px;height:12px;background:var(--ink)}
article .blk-gradient li::after{counter-increment:g;content:counter(g);position:absolute;top:-22px;left:0;right:0;font-size:.62rem;color:var(--acc)}
article .blk-gradient ul{counter-reset:g;margin-top:40px}
@media (max-width:520px){article .blk-gradient ul{grid-template-columns:1fr;border-top:0;border-left:1px solid var(--ink);margin-left:24px}
 article .blk-gradient li{text-align:left;padding:10px 0 10px 18px;font-size:.78rem}
 article .blk-gradient li::before{top:50%;left:0;width:12px;height:1px}
 article .blk-gradient li::after{top:50%;left:-26px;right:auto;transform:translateY(-50%)}}
article .blk-tool{border:1px solid var(--acc)!important;background:none!important;border-radius:0!important;padding:20px 22px!important}
.blk-tool .blk-k{font-size:1.05rem!important;letter-spacing:.12em;color:var(--ink)!important}
.blk-tool .when{color:var(--dim);font-style:italic}.blk-tool .ask,.blk-ask .ask{font-weight:600}
article .blk-ask{border-left:2px solid var(--acc)!important;background:none!important;padding:8px 0 8px 18px!important;border-radius:0!important}
article .blk-scene{background:#12171b!important;border:1px solid var(--line)!important;border-radius:0!important}
.path>li>details{border-top:1px solid var(--line);padding:16px 0}
.path>li>details>summary{display:grid;grid-template-columns:1fr auto;align-items:baseline;font:500 1.35rem/1.25 'Newsreader',serif}
.path>li>details>summary small{grid-column:1/-1}
.cnt{font-size:.7rem;color:var(--dim)}
.sort-more{background:none;border:1px solid var(--acc);color:var(--acc)}
.sky .cover img{width:min(56vw,250px)!important;border:1px solid var(--line);padding:8px}
.sky .cover::after{content:"59 chapters  ·  6 movements  ·  free, nothing stored";display:block;text-align:center;margin-top:16px;font:500 .7rem 'Plex Mono',monospace;letter-spacing:.08em;color:var(--acc);text-transform:uppercase}
"""

B = face("Public Sans", "public-sans/PublicSans[wght].ttf") + face("Public Sans", "public-sans/PublicSans-Italic[wght].ttf", "italic") + \
    face("Bricolage", "bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf") + """
/* B  Plain Speech: gov-grade clarity + oversized blunt headings (S-44 + S-46) */
:root{--bg:#111214;--ink:#f4f4f2;--dim:#b8b8b2;--line:#34363a;--acc:#ffd23f}
body{background:var(--bg)!important;color:var(--ink)!important;font-family:'Public Sans',system-ui,sans-serif!important;font-size:1.14rem;line-height:1.6}
h1,h2,h3,.blk-k,.path summary{font-family:'Bricolage',sans-serif!important;font-weight:800!important;letter-spacing:-.025em}
h1{font-size:clamp(2.6rem,9vw,5rem)!important;line-height:.98!important}
h2{font-size:clamp(1.6rem,5vw,2.3rem)!important;line-height:1.05}
.sky{background:var(--bg)!important}
a{color:var(--ink);text-decoration-color:var(--acc);text-decoration-thickness:2px;text-underline-offset:3px}
.loc,.lab,.path small{color:var(--acc)!important;font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:.78rem!important}
.short{background:#1b1c1f!important;border:0!important;border-left:6px solid var(--acc)!important;border-radius:0!important;font-size:1.2rem}
article .blk-gradient ul{grid-template-columns:repeat(7,1fr);gap:3px}
article .blk-gradient li{padding:44px 2px 0;font:700 .66rem/1.2 'Public Sans',sans-serif;text-align:center}
article .blk-gradient li::before{content:"";position:absolute;top:0;left:0;right:0;height:34px;background:var(--acc);opacity:calc(.18 + var(--i,0)*.13)}
article .blk-gradient li:nth-child(1){--i:0}article .blk-gradient li:nth-child(2){--i:1}article .blk-gradient li:nth-child(3){--i:2}article .blk-gradient li:nth-child(4){--i:3}article .blk-gradient li:nth-child(5){--i:4}article .blk-gradient li:nth-child(6){--i:5}article .blk-gradient li:nth-child(7){--i:6}
@media (max-width:520px){article .blk-gradient ul{grid-template-columns:1fr;gap:3px}
 article .blk-gradient li{padding:12px 14px 12px 64px;text-align:left;font-size:.95rem}
 article .blk-gradient li::before{right:auto;width:48px;height:100%}}
article .blk-tool{background:var(--acc)!important;color:#111!important;border:0!important;border-radius:0!important;padding:22px!important}
.blk-tool .blk-k{color:#111!important;font-size:1.6rem!important;margin:0 0 8px}
.blk-tool .when{font-weight:500}.blk-tool .ask{font-weight:800;font-size:1.15rem;margin-top:8px}
article .blk-ask{background:none!important;border:2px solid var(--ink)!important;border-radius:0!important;padding:14px 18px!important}
.blk-ask .ask{font-weight:800}
article .blk-scene{background:#1b1c1f!important;border:0!important;border-radius:0!important}
.path>li>details{border-top:3px solid var(--ink);padding:18px 0}
.path>li>details>summary{display:grid;grid-template-columns:1fr auto;gap:6px;font-size:1.6rem;line-height:1.05}
.path>li>details>summary small{grid-column:1/-1}
.cnt{font:600 .8rem 'Public Sans',sans-serif;color:var(--dim);letter-spacing:0;align-self:end}
.sort-more{background:var(--acc);color:#111;border:0;font-weight:800}
.bar,.bar a,.bar button,.dock a,.dock button{font-family:'Public Sans',sans-serif!important;font-weight:700}
.sky .cover{display:flex;flex-direction:column;align-items:flex-start;text-align:left}
.sky .cover h1{order:-2;margin:8px 0 12px!important;text-align:left}
.sky .cover .q{order:-1;text-align:left;font-style:normal!important;font-size:1.15rem;margin:0 0 24px}
.sky .cover img{width:min(48vw,220px)!important;align-self:flex-end;margin:0!important;border-left:6px solid var(--acc)}
"""

C = face("Source Serif", "source-serif-4/SourceSerif4[opsz,wght].ttf") + face("Source Serif", "source-serif-4/SourceSerif4-Italic[opsz,wght].ttf", "italic") + \
    face("DM Mono", "dmmono/DMMono-Regular.ttf", wght="400") + face("DM Mono", "dmmono/DMMono-Medium.ttf", wght="500") + """
/* C  The Ledger: receipts, tags and tickets on warm dark (S-49 + S-45) */
:root{--bg:#191614;--ink:#ece6dc;--dim:#a99f92;--paper:#f2ece1;--pink:#1d1a17;--line:#3a332d;--acc:#e0805a}
body{background:var(--bg)!important;color:var(--ink)!important;font-family:'Source Serif',Georgia,serif!important;font-size:1.13rem}
h1,h2,h3{font-family:'Source Serif',serif!important;font-weight:600!important}
.sky{background:var(--bg)!important}
a{color:var(--acc)}
.loc,.lab,.blk-k,.path small,.cnt,.by,.sort-more{font-family:'DM Mono',monospace!important;text-transform:uppercase;letter-spacing:.08em;font-size:.72rem!important}
.loc,.path small{color:var(--acc)!important}
.short{background:var(--paper)!important;color:var(--pink)!important;border:0!important;border-radius:2px!important;
 mask:radial-gradient(circle 6px at 50% 0,#0000 98%,#000) top/16px 51% repeat-x,radial-gradient(circle 6px at 50% 100%,#0000 98%,#000) bottom/16px 51% repeat-x}
.short .lab{color:#8a5b3c!important}
article .blk-gradient ul{border:1px dashed var(--line);padding:6px 16px}
article .blk-gradient li{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px dotted var(--line);font:500 .9rem 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.06em}
article .blk-gradient li:last-child{border-bottom:0}
article .blk-gradient li::after{content:"";width:calc(var(--i,1)*14px);height:8px;align-self:center;background:var(--acc);opacity:.85}
article .blk-gradient li:nth-child(1){--i:1}article .blk-gradient li:nth-child(2){--i:2}article .blk-gradient li:nth-child(3){--i:3}article .blk-gradient li:nth-child(4){--i:4}article .blk-gradient li:nth-child(5){--i:5}article .blk-gradient li:nth-child(6){--i:6}article .blk-gradient li:nth-child(7){--i:7}
article .blk-tool{background:var(--paper)!important;color:var(--pink)!important;border:0!important;border-radius:4px 4px 4px 22px!important;padding:22px 22px 22px 26px!important;position:relative}
article .blk-tool::before{content:"";position:absolute;top:16px;right:16px;width:12px;height:12px;border-radius:50%;background:var(--bg)}
.blk-tool .blk-k{color:#8a5b3c!important;font-size:.9rem!important}
.blk-tool .ask{font-weight:600}
article .blk-ask{background:none!important;border:1px dashed var(--acc)!important;border-radius:2px!important;padding:12px 16px!important}
article .blk-scene{background:var(--paper)!important;color:var(--pink)!important;border:0!important;border-radius:2px!important}
article .blk-scene a{color:#8a3f1f}
article .blk-scene p,article .blk-scene em,.short p{color:var(--pink)!important}
article .blk-scene::before,article .blk-scene .blk-k{color:#8a5b3c!important}
.path>li>details{border-bottom:1px dashed var(--line);padding:14px 0}
.path>li>details>summary{display:grid;grid-template-columns:1fr auto;font-size:1.3rem}
.path>li>details>summary small{grid-column:1/-1}
.cnt{color:var(--dim)}
.sort-more{background:none;border:1px dashed var(--acc);color:var(--acc)}
.bar,.bar a,.bar button,.dock a,.dock button{font-family:'DM Mono',monospace!important;text-transform:uppercase;letter-spacing:.05em;font-size:.8rem!important}
.sky .cover img{width:min(64vw,270px)!important;background:var(--paper);padding:12px 12px 36px;border-radius:2px;box-shadow:0 18px 40px rgba(0,0,0,.45);transform:rotate(-1.5deg)}
.sky .cover::after{content:"59 CHAPTERS  ·  FREE  ·  NOTHING STORED";display:block;margin:20px auto 0;width:max-content;padding:6px 12px;border:1px dashed var(--acc);font:500 .68rem 'DM Mono',monospace;letter-spacing:.1em;color:var(--acc)}
"""

for name, css in (("a", A), ("b", B), ("c", C)):
    d = OUT / name; d.mkdir(parents=True, exist_ok=True)
    for p in PAGES:
        h = (SRC / f"{p}.html").read_text()
        h = h.replace("</head>", f"<style>{SHARED}{css}</style>\n</head>", 1).replace("</body>", JS + "\n</body>", 1)
        (d / f"{p}.html").write_text(h)
print("comps written:", [f"{n}/{p}.html" for n in "abc" for p in PAGES][:3], "...")
