#!/usr/bin/env python3
"""Fractal² hub: the page the film's last button leads to. python3 design/fractal2/film/hub_build.py
Thirty sectors in the author's own order, each with what it governs and what was here first.
Writes library/fractal2/site/fractal2/hub.html (served at /fractal2/hub)."""
import os, json, html, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
OUT = os.path.join(ROOT, 'library/fractal2/site/fractal2/hub.html')
A = '/fractal2/_a/'
sectors = json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']
imp = json.load(open(os.path.join(HERE, 'tables.json')))['impulses']
OPEN = {12: ('/fractal2/entertainment', 'Entertainment & Music')}     # built and live
NEXT = {10}                                                            # written, site not built yet
e = lambda s: html.escape(s, quote=True)

def status(n):
    return 'open' if n in OPEN else 'next' if n in NEXT else 'soon'

nodes, items, data = [], [], []
for s in sectors:
    n = s['n']; st = status(n); name = OPEN[n][1] if n in OPEN else s['name']
    a = (n - 1) / 30 * 2 * math.pi; x = 500 + 410 * math.sin(a); y = 500 - 410 * math.cos(a)
    lx = 500 + 484 * math.sin(a); ly = 500 - 484 * math.cos(a) + 7
    nodes.append(f'<g class="nd {st}" data-i="{n - 1}"><circle class="hit" cx="{x:.1f}" cy="{y:.1f}" r="36"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{17 if st == "open" else 13}"/><text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle">{n:02d}</text></g>')
    label = {'open': 'Open', 'next': 'Next', 'soon': 'In production'}[st]
    link = f'<a class="go" href="{OPEN[n][0]}">Enter {e(name)}</a>' if st == 'open' else f'<span class="st">{label}</span>'
    items.append(f'<li class="{st}" id="s{n}"><span class="n">{n:02d}</span><div><h3>{e(name)}</h3><p class="rel">Your relationship with {e(s["relationship"])}</p><p class="imp">Here first: {e(imp[n - 1][0].lower() + imp[n - 1][1:])}</p>{link}</div></li>')
    data.append({'n': n, 'name': name, 'rel': s['relationship'], 'imp': imp[n - 1], 'st': st, 'url': OPEN[n][0] if n in OPEN else ''})

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Fractal² · The map</title>
<meta name="description" content="Thirty sectors of human life, one cycle. Choose a sector to enter the map.">
<meta name="theme-color" content="#05070d">
<link rel="icon" href="{A}v8/favicon.ico">
<style>
@font-face{{font-family:"Voice";src:url({A}v9/instrument.ttf) format("truetype");font-weight:400;font-style:normal;font-display:swap}}
@font-face{{font-family:"Source Serif";src:url({A}v8/fonts/sourceserif4.woff2) format("woff2");font-weight:300 700;font-style:normal;font-display:swap}}
:root{{--bg:#05070d;--ink:#F3ECD9;--ink2:#CFC8B6;--gold:#E9C27A;--line:#2A3350;color-scheme:dark}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Source Serif",Georgia,serif;font-size:1.0625rem;line-height:1.55;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.wrap{{max-width:72rem;margin:0 auto;padding:0 20px}}
header{{padding:56px 0 8px;text-align:center}}
h1{{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(3rem,13vw,6.5rem);line-height:.98;margin:0;letter-spacing:-.01em}}
header p{{margin:16px auto 0;max-width:30em;color:var(--ink2);font-size:1.0625rem}}
.stage{{display:grid;grid-template-columns:1fr;gap:8px;align-items:center;max-width:34rem;margin:24px auto 0}}
@media (max-width:600px){{.wrap{{padding:0 12px}}}}
@media (min-width:900px){{.stage{{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:56px;max-width:66rem}}.card{{text-align:left}}}}
.stage svg{{display:block;width:100%;height:auto;overflow:visible}}
.orbit{{fill:none;stroke:rgba(233,194,122,.28);stroke-width:1.2}}
.orbit.b{{stroke:rgba(243,236,217,.08);stroke-width:1}}
.nd{{cursor:pointer}}
.nd .hit{{fill:transparent}}
.nd .dot{{fill:#111728;stroke:rgba(243,236,217,.34);stroke-width:1.5;transition:fill .25s,stroke .25s}}
.nd.next .dot{{stroke:var(--gold)}}
.nd.open .dot{{fill:var(--gold);stroke:var(--gold)}}
.nd text{{font:400 26px/1 "Source Serif",Georgia,serif;fill:var(--ink2);letter-spacing:.06em;pointer-events:none}}
.nd.on .dot{{fill:var(--ink);stroke:var(--ink)}}
.nd.on text{{fill:var(--ink)}}
.light{{fill:url(#lg)}}
@keyframes breathe{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}
@keyframes turn{{to{{transform:rotate(360deg)}}}}
.light{{animation:breathe 5.2s ease-in-out infinite;transform-origin:500px 500px}}
.ticks{{transform-origin:500px 500px;animation:turn 240s linear infinite}}
@media (prefers-reduced-motion:reduce){{.light,.ticks{{animation:none}}}}
.card{{text-align:center;min-height:15rem;padding:8px 4px 0}}
.card .k{{font-size:.75rem;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);margin:0}}
.card h2{{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(2.4rem,9vw,4rem);line-height:1.02;margin:10px 0 12px}}
.card p{{margin:0;color:var(--ink2);font-size:1.125rem;line-height:1.45}}
.card p.imp{{margin-top:8px;color:var(--ink)}}
.card .go,.card .st{{display:inline-block;margin-top:14px}}
.go{{font-size:.8125rem;letter-spacing:.24em;text-transform:uppercase;text-decoration:none;color:#0b0d14;background:var(--gold);padding:13px 20px;border-radius:40px}}
.st{{font-size:.75rem;letter-spacing:.24em;text-transform:uppercase;color:var(--ink2);border:1px solid var(--line);padding:9px 14px;border-radius:40px}}
.go:focus-visible,.nd:focus-visible .dot,a:focus-visible{{outline:2px solid var(--gold);outline-offset:4px}}
.nd:focus{{outline:none}}
.nd:focus-visible .dot{{stroke:var(--gold);stroke-width:3}}
h2.sec{{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(2rem,6vw,3rem);margin:72px 0 8px;text-align:center}}
.lead{{text-align:center;color:var(--ink2);margin:0 auto 32px;max-width:32em}}
ol.all{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr;gap:0}}
@media (min-width:760px){{ol.all{{grid-template-columns:1fr 1fr;column-gap:48px}}}}
ol.all li{{display:flex;gap:16px;padding:20px 0;border-top:1px solid var(--line)}}
ol.all .n{{font-family:"Voice",Georgia,serif;font-size:1.5rem;color:var(--ink2);min-width:2ch}}
ol.all li.open .n{{color:var(--gold)}}
ol.all h3{{font-family:"Voice",Georgia,serif;font-weight:400;font-size:1.6rem;line-height:1.1;margin:0 0 4px}}
ol.all p{{margin:0;color:var(--ink2)}}
ol.all p.imp{{color:var(--ink);margin-top:2px}}
ol.all .go,ol.all .st{{display:inline-block;margin-top:12px}}
footer{{margin:72px 0 0;padding:32px 0 56px;border-top:1px solid var(--line);text-align:center;color:var(--ink2);font-size:.9375rem}}
footer a{{margin:0 12px;text-underline-offset:4px;display:inline-block;padding:10px 0}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>The map</h1>
<p>Thirty sectors of human life. One cycle. One sector is open so far, Entertainment &amp; Music, and the rest are being mapped one at a time.</p>
</header>
<div class="stage">
<svg viewBox="-28 -28 1056 1056" role="group" aria-label="Thirty sectors arranged in a ring. Choose one to read what it governs and what was here first.">
<defs><radialGradient id="lg"><stop offset="0" stop-color="#FFF6E2"/><stop offset=".16" stop-color="#FFE0A6" stop-opacity=".75"/><stop offset=".5" stop-color="#E9C27A" stop-opacity=".12"/><stop offset="1" stop-color="#E9C27A" stop-opacity="0"/></radialGradient></defs>
<circle class="orbit" cx="500" cy="500" r="410"/><circle class="orbit b" cx="500" cy="500" r="330"/><circle class="orbit b" cx="500" cy="500" r="300"/>
<g class="ticks">{''.join(f'<line x1="500" y1="172" x2="500" y2="{184 if i % 5 else 194}" stroke="rgba(243,236,217,.22)" stroke-width="1" transform="rotate({i * 3} 500 500)"/>' for i in range(120))}</g>
<circle class="light" cx="500" cy="500" r="290"/>
{''.join(nodes)}
</svg>
<div class="card" id="card" aria-live="polite"></div>
</div>
<h2 class="sec">All thirty</h2>
<p class="lead">Each sector governs one of your relationships. Under each one is what was here first.</p>
<ol class="all">
{''.join(items)}
</ol>
<footer><a href="/fractal2">Watch the film again</a><a href="/fractal">The Fractal</a><a href="/playbook">Pattern Decoder</a></footer>
</div>
<script>
(function(){{var S={json.dumps(data, ensure_ascii=False, separators=(',', ':'))},card=document.getElementById('card'),nd=[].slice.call(document.querySelectorAll('.nd')),cur=-1;
function esc(s){{return s.replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
function show(i){{if(i===cur)return;cur=i;var s=S[i];nd.forEach(function(g,k){{g.classList.toggle('on',k===i);g.setAttribute('aria-pressed',k===i?'true':'false')}});
card.innerHTML='<p class="k">'+('0'+s.n).slice(-2)+' of 30</p><h2>'+esc(s.name)+'</h2><p>Your relationship with '+esc(s.rel)+'</p><p class="imp">Here first: '+esc(s.imp.charAt(0).toLowerCase()+s.imp.slice(1))+'</p>'+(s.st==='open'?'<a class="go" href="'+s.url+'">Enter</a>':'<span class="st">'+(s.st==='next'?'Next':'In production')+'</span>')}}
nd.forEach(function(g,i){{var s=S[i];g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-label',s.n+'. '+s.name+'. '+(s.st==='open'?'Open':s.st==='next'?'Next':'In production'));
g.addEventListener('click',function(){{show(i)}});g.addEventListener('mouseenter',function(){{show(i)}});g.addEventListener('focus',function(){{show(i)}});
g.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();show(i);if(s.url)location.href=s.url}}else if(e.key==='ArrowRight'||e.key==='ArrowDown'){{e.preventDefault();nd[(i+1)%30].focus()}}else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){{e.preventDefault();nd[(i+29)%30].focus()}}}})}});
show(11)}})();
</script>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote hub.html', len(page) // 1024, 'KB')
