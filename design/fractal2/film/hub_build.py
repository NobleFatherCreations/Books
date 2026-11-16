#!/usr/bin/env python3
"""Fractal² hub: the page the film's last button leads to. python3 design/fractal2/film/hub_build.py
Thirty sectors in the owner's 1 to 30 order (tables.json), the owner's map at the centre, an idle WebGL light, and the thirty touchable technique pairs.
Writes library/fractal2/site/fractal2/hub.html (served at /fractal2/hub)."""
import os, json, html, math, base64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
OUT = os.path.join(ROOT, 'library/fractal2/site/fractal2/hub.html')
A = '/fractal2/_a/'
TB = json.load(open(os.path.join(HERE, 'tables.json')))
imp, pairs = TB['impulses'], TB['pairs']
# the owner's 1 to 30 numbering: tables.json lists impulses and pairs in that order; sectors are sorted to match
sectors = sorted(json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors'], key=lambda s: s['n'])
assert [s['n'] for s in sectors] == list(range(1, 31)) and len(imp) == 30 and len(pairs) == 30
def b64(path, mime):
    # the page is proxied at a clean path, so every font and image travels inside it
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())
SITE = os.path.join(ROOT, 'library/fractal2/site/fractal2/_a')
VOICE = b64(os.path.join(SITE, 'v9/instrument.ttf'), 'font/ttf')
SERIF = b64(os.path.join(SITE, 'v8/fonts/sourceserif4.woff2'), 'font/woff2')
MAP = b64(os.path.join(HERE, 'hub-assets/map.webp'), 'image/webp')
STILL_P = os.path.join(HERE, 'hub-assets/still.webp')
STILL = b64(STILL_P, 'image/webp') if os.path.exists(STILL_P) else ''
FAVICON = b64(os.path.join(SITE, 'v8/favicon.ico'), 'image/x-icon')
OPEN = {12: ('/fractal2/entertainment', 'Entertainment & Music')}     # built and live
NEXT = {10}                                                            # written, site not built yet
e = lambda s: html.escape(s, quote=True)

def status(n):
    return 'open' if n in OPEN else 'next' if n in NEXT else 'soon'


nodes, items, data, pr = [], [], [], []
for s in sectors:
    n = s['n']; st = status(n); name = OPEN[n][1] if n in OPEN else s['name']
    a = (n - 1) / 30 * 2 * math.pi; x = 500 + 410 * math.sin(a); y = 500 - 410 * math.cos(a)
    lx = 500 + 486 * math.sin(a); ly = 500 - 486 * math.cos(a) + 14
    nodes.append(f'<g class="nd {st}" data-i="{n - 1}"><circle class="hit" cx="{x:.1f}" cy="{y:.1f}" r="36"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="{18 if st == "open" else 14}"/><text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle">{n:02d}</text></g>')
    label = {'open': 'Open', 'next': 'Next', 'soon': 'In production'}[st]
    link = f'<a class="go" href="{OPEN[n][0]}">Enter {e(name)}</a>' if st == 'open' else f'<span class="st">{label}</span>'
    items.append(f'<li class="{st}" id="s{n}"><span class="n">{n:02d}</span><div><h3>{e(name)}</h3><p class="rel">Your relationship with {e(s["relationship"])}</p><p class="imp">Here first: {e(imp[n - 1][0].lower() + imp[n - 1][1:])}</p>{link}</div></li>')
    data.append({'n': n, 'name': name, 'rel': s['relationship'], 'imp': imp[n - 1], 'st': st, 'url': OPEN[n][0] if n in OPEN else ''})
for i, (g, x) in enumerate(pairs):
    pr.append(f'<li><button type="button" class="pr" aria-expanded="false"><span class="pn">{i + 1:02d}</span><span class="k2">Technique</span><span class="w g">{e(g)}</span><span class="rv"><span class="in"><span class="k2">Inversion</span><span class="w x">{e(x)}</span></span></span></button></li>')

CSS = r"""
@font-face{font-family:"Voice";src:url(%%VOICE%%) format("truetype");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:"Source Serif";src:url(%%SERIF%%) format("woff2");font-weight:300 700;font-style:normal;font-display:swap}
:root{--bg:#05070d;--ink:#F3ECD9;--ink2:#CFC8B6;--gold:#E9C27A;--grey:#BFC4D2;--line:#2A3350;color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Source Serif",Georgia,serif;font-size:1rem;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:72rem;margin:0 auto;padding:0 24px}
@media (max-width:600px){.wrap{padding:0 16px}}
header{padding:56px 0 8px;text-align:center}
h1{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(3rem,13vw,6.5rem);line-height:.98;margin:0;letter-spacing:-.01em}
header p{margin:16px auto 0;max-width:30em;color:var(--ink2)}
.stage{display:grid;grid-template-columns:1fr;gap:8px;align-items:center;max-width:36rem;margin:24px auto 0}
@media (min-width:900px){.stage{grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:56px;max-width:66rem}.card{text-align:left}}
.fig{position:relative;width:100%;aspect-ratio:1/1}
.fig svg{position:absolute;inset:0;display:block;width:100%;height:100%;overflow:visible}
.fx{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}
#fx{opacity:0;transition:opacity .3s ease-out}
.fig.gl #fx{opacity:1}
.fig.gl #fxs{opacity:0}
#fxs{transition:opacity .3s ease-out}
.orbit{fill:none;stroke:rgba(233,194,122,.34);stroke-width:1.2}
.orbit.b{stroke:rgba(243,236,217,.12);stroke-width:1}
.nd{cursor:pointer}
.nd .hit{fill:transparent}
.nd .dot{fill:#111728;stroke:rgba(243,236,217,.4);stroke-width:1.5;transition:fill .25s,stroke .25s}
.nd.next .dot{stroke:var(--gold)}
.nd.open .dot{fill:var(--gold);stroke:var(--gold)}
.nd text{font:400 40px/1 "Source Serif",Georgia,serif;fill:var(--ink2);letter-spacing:.04em;pointer-events:none;transition:fill .25s}
.nd.on .dot{fill:var(--ink);stroke:var(--ink)}
.nd.on text{fill:var(--ink)}
.nd.open.on .dot{fill:var(--gold);stroke:var(--ink);stroke-width:3}
@keyframes turn{to{transform:rotate(360deg)}}
.ticks{transform-origin:500px 500px;animation:turn 240s linear infinite}
@media (prefers-reduced-motion:reduce){.ticks{animation:none}#fx,#fxs,.nd .dot,.nd text{transition:none}}
@media (max-width:700px),(pointer:coarse){.nd{pointer-events:none}}
.card{text-align:center;min-height:16rem;padding:8px 0 0}
.card .k{font-size:.75rem;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);margin:0}
.card h2{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(2.4rem,9vw,4rem);line-height:1.02;margin:8px 0 16px}
.card p{margin:0;color:var(--ink2);font-size:1.125rem;line-height:1.45}
.card p.imp{margin-top:8px;color:var(--ink)}
.card .go,.card .st{margin-top:16px}
.go,.st{display:inline-flex;align-items:center;justify-content:center;min-height:48px}
.go{font-size:1rem;letter-spacing:.16em;text-align:center;text-transform:uppercase;text-decoration:none;color:#0b0d14;background:var(--gold);padding:8px 24px;border-radius:40px;transition:transform .25s}
@media (hover:hover){.go:hover{transform:translateY(-2px)}}
.st{font-size:.75rem;letter-spacing:.24em;text-transform:uppercase;color:var(--ink2);border:1px solid var(--line);padding:0 16px;border-radius:40px;min-height:48px}
.go:focus-visible,.nd:focus-visible .dot,a:focus-visible,.pr:focus-visible{outline:2px solid var(--gold);outline-offset:4px}
.nd:focus{outline:none}
.nd:focus-visible .dot{stroke:var(--gold);stroke-width:3}
h2.sec{font-family:"Voice",Georgia,serif;font-weight:400;font-size:clamp(2rem,6vw,3rem);line-height:1.1;margin:72px 0 8px;text-align:center}
.lead{text-align:center;color:var(--ink2);margin:0 auto 32px;max-width:32em}
ul.pairs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;align-items:start}
@media (min-width:700px){ul.pairs{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
@media (min-width:1100px){ul.pairs{grid-template-columns:repeat(5,minmax(0,1fr))}}
.pr{display:block;width:100%;min-height:96px;text-align:left;font:inherit;color:inherit;background:transparent;border:1px solid var(--line);border-radius:16px;padding:16px;cursor:pointer;position:relative;transition:border-color .25s,background-color .25s}
@media (hover:hover){.pr:hover{border-color:rgba(233,194,122,.5)}}
.pr[aria-expanded=true]{border-color:rgba(233,194,122,.6);background:rgba(233,194,122,.04)}
.pn{position:absolute;right:16px;top:16px;font-size:.75rem;letter-spacing:.12em;color:var(--ink2)}
.k2{display:block;font-size:.75rem;letter-spacing:.24em;text-transform:uppercase;color:var(--ink2);margin:0 0 4px}
.w{display:block;font-family:"Voice",Georgia,serif;font-size:1.5rem;line-height:1.12;overflow-wrap:anywhere}
.w.g{color:var(--gold)}
.w.x{color:var(--grey)}
.rv{display:grid;grid-template-rows:0fr;opacity:0;visibility:hidden;transition:grid-template-rows .3s ease-out,opacity .3s ease-out,visibility 0s .3s}
.rv .in{overflow:hidden;min-height:0}
.rv .in:before{content:"";display:block;height:1px;background:var(--line);margin:16px 0}
.pr[aria-expanded=true] .rv{grid-template-rows:1fr;opacity:1;visibility:visible;transition-delay:0s}
@media (prefers-reduced-motion:reduce){.rv,.pr,.go{transition:none}}
ol.all{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr;gap:0}
@media (min-width:760px){ol.all{grid-template-columns:1fr 1fr;column-gap:48px}}
ol.all li{display:flex;gap:16px;padding:24px 0;border-top:1px solid var(--line)}
ol.all .n{font-family:"Voice",Georgia,serif;font-size:1.5rem;color:var(--ink2);min-width:2ch}
ol.all li.open .n{color:var(--gold)}
ol.all h3{font-family:"Voice",Georgia,serif;font-weight:400;font-size:1.5rem;line-height:1.1;margin:0 0 4px}
ol.all p{margin:0;color:var(--ink2)}
ol.all p.imp{color:var(--ink);margin-top:4px}
ol.all .go,ol.all .st{margin-top:16px}
footer{margin:72px 0 0;padding:32px 0 56px;border-top:1px solid var(--line);text-align:center;color:var(--ink2);font-size:1rem}
footer a{margin:0 8px;text-underline-offset:4px;display:inline-flex;align-items:center;min-height:48px;padding:0 8px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
"""

JS = r"""
(function(){var S=%%DATA%%,card=document.getElementById('card'),svg=document.getElementById('ring'),nd=[].slice.call(document.querySelectorAll('.nd')),cur=-1,
dec=matchMedia('(max-width:700px),(pointer:coarse)');
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function show(i){if(i===cur)return;cur=i;var s=S[i];nd.forEach(function(g,k){g.classList.toggle('on',k===i);if(!dec.matches)g.setAttribute('aria-pressed',k===i?'true':'false')});
card.innerHTML='<p class="k">'+('0'+s.n).slice(-2)+' of 30</p><h2>'+esc(s.name)+'</h2><p>Your relationship with '+esc(s.rel)+'</p><p class="imp">Here first: '+esc(s.imp.charAt(0).toLowerCase()+s.imp.slice(1))+'</p>'+(s.st==='open'?'<a class="go" href="'+s.url+'">Enter</a>':'<span class="st">'+(s.st==='next'?'Next':'In production')+'</span>')}
/* on phones and touch screens the ring is a picture and the list below is the route: nothing in it is tappable */
function mode(){var d=dec.matches;svg.setAttribute('aria-hidden',d?'true':'false');if(d)svg.removeAttribute('role');else svg.setAttribute('role','group');
nd.forEach(function(g,i){var s=S[i];if(d){g.removeAttribute('tabindex');g.removeAttribute('role');g.removeAttribute('aria-label');g.removeAttribute('aria-pressed')}else{g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-pressed',i===cur?'true':'false');g.setAttribute('aria-label',s.n+'. '+s.name+'. '+(s.st==='open'?'Open':s.st==='next'?'Next':'In production'))}});if(d)show(11)}
nd.forEach(function(g,i){var s=S[i];
g.addEventListener('click',function(){if(!dec.matches)show(i)});g.addEventListener('mouseenter',function(){if(!dec.matches)show(i)});g.addEventListener('focus',function(){show(i)});
g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();show(i);if(s.url)location.href=s.url}else if(e.key==='ArrowRight'||e.key==='ArrowDown'){e.preventDefault();nd[(i+1)%30].focus()}else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();nd[(i+29)%30].focus()}})});
show(11);mode();if(dec.addEventListener)dec.addEventListener('change',mode);
/* the thirty pairs: tap or focus a technique to see its inversion */
[].slice.call(document.querySelectorAll('.pr')).forEach(function(b){
b.addEventListener('click',function(){b.setAttribute('aria-expanded',b.getAttribute('aria-expanded')==='true'?'false':'true')});
b.addEventListener('focus',function(){try{if(b.matches(':focus-visible'))b.setAttribute('aria-expanded','true')}catch(x){}})});
/* idle light: a slow breath behind the ring. Pixel ratio capped, 30 fps, paused when the tab is hidden or the ring is off screen,
   a still picture when WebGL is missing, the context is lost, or the visitor asks for reduced motion */
(function(){var fig=document.getElementById('fig'),cv=document.getElementById('fx'),mq=matchMedia('(prefers-reduced-motion:reduce)'),gl=null,U={},raf=0,t0=0,last=0,seen=true,dead=false,drawn=false,START=2;
var VS='attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
var FS='precision mediump float;uniform vec2 R;uniform float T;'+
'float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}'+
'void main(){vec2 p=gl_FragCoord.xy/R*2.-1.;float r=length(p),a=atan(p.y,p.x),br=.5+.5*sin(T*.45);'+
'float core=exp(-r*r*5.)*(.1+.09*br);'+
'float halo=exp(-pow((r-.777)*9.,2.))*(.1+.07*sin(T*.3+1.));'+
'float rays=pow(.5+.5*cos(a*30.+T*.1),8.)*exp(-pow((r-.62)*3.2,2.))*(.045+.035*br);'+
'float rip=exp(-pow((fract(r*1.4-T*.035)-.5)*7.,2.))*.035*smoothstep(1.,.35,r);'+
'vec3 bg=vec3(.0196,.0275,.051),gold=vec3(.914,.761,.478);'+
'vec3 c=bg+gold*(core+halo+rays+rip)*smoothstep(1.,.8,r)+vec3((h(gl_FragCoord.xy)-.5)/255.);gl_FragColor=vec4(c,1.);}';
function sh(t,s){var o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw 0;return o}
function init(){if(gl)return true;if(dead)return false;try{gl=cv.getContext('webgl',{alpha:false,antialias:false,depth:false,stencil:false,powerPreference:'low-power'});if(!gl)throw 0;
var p=gl.createProgram();gl.attachShader(p,sh(gl.VERTEX_SHADER,VS));gl.attachShader(p,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw 0;gl.useProgram(p);
var b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);var l=gl.getAttribLocation(p,'a');gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0);
U.R=gl.getUniformLocation(p,'R');U.T=gl.getUniformLocation(p,'T');return true}catch(e){gl=null;dead=true;return false}}
function size(){var d=Math.min(window.devicePixelRatio||1,1.5),w=Math.max(2,Math.round(cv.clientWidth*d));if(cv.width!==w||cv.height!==w){cv.width=cv.height=w}gl.viewport(0,0,w,w);gl.uniform2f(U.R,w,w)}
function draw(t){size();gl.uniform1f(U.T,t);gl.drawArrays(gl.TRIANGLES,0,3);if(!drawn){drawn=true;fig.classList.add('gl')}}
function run(){return !dead&&!mq.matches&&!document.hidden&&seen}
function loop(now){raf=0;if(!run())return;if(now-last>=33){last=now;draw(START+(now-t0)/1000)}raf=requestAnimationFrame(loop)}
function kick(){if(!run()||raf)return;if(!init())return;t0=performance.now();last=0;raf=requestAnimationFrame(loop)}
function stop(){if(raf){cancelAnimationFrame(raf);raf=0}}
function still(){stop();fig.classList.remove('gl');drawn=false}
document.addEventListener('visibilitychange',function(){if(document.hidden)stop();else kick()});
if('IntersectionObserver' in window)new IntersectionObserver(function(es){seen=es[es.length-1].isIntersecting;if(seen)kick();else stop()}).observe(fig);
cv.addEventListener('webglcontextlost',function(e){e.preventDefault();dead=true;still()});
var chg=function(){if(mq.matches)still();else kick()};if(mq.addEventListener)mq.addEventListener('change',chg);
kick()})();
})();
"""

page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Fractal² · The map</title>
<meta name="description" content="Thirty sectors of human life, one cycle. Choose a sector to enter the map.">
<meta name="theme-color" content="#05070d">
<link rel="icon" href="%%FAVICON%%">
<style>%%CSS%%</style>
</head>
<body>
<div class="wrap">
<header>
<h1>The map</h1>
<p>Thirty sectors of human life. One cycle. One sector is open so far, Entertainment &amp; Music, and the rest are being mapped one at a time.</p>
</header>
<div class="stage">
<div class="fig" id="fig">
<img class="fx" id="fxs" src="%%STILL%%" alt="" width="640" height="640" decoding="async">
<canvas class="fx" id="fx" aria-hidden="true"></canvas>
<svg id="ring" viewBox="-40 -40 1080 1080" role="group" aria-label="Thirty sectors arranged in a ring around the map. Choose one to read what it governs and what was here first.">
<circle class="orbit" cx="500" cy="500" r="410"/><circle class="orbit b" cx="500" cy="500" r="336"/>
<g class="ticks">%%TICKS%%</g>
<image href="%%MAP%%" x="200" y="200" width="600" height="600" preserveAspectRatio="xMidYMid meet" aria-hidden="true"/>
%%NODES%%
</svg>
</div>
<div class="card" id="card" aria-live="polite"></div>
</div>
<h2 class="sec">Thirty techniques and their inversions</h2>
<p class="lead">Tap a technique to see its inversion.</p>
<ul class="pairs">
%%PAIRS%%
</ul>
<h2 class="sec">All thirty</h2>
<p class="lead">Each sector governs one of your relationships. Under each one is what was here first.</p>
<ol class="all">
%%ITEMS%%
</ol>
<footer><a href="/fractal2">Watch the film again</a><a href="/fractal">The Fractal</a><a href="/playbook">Pattern Decoder</a></footer>
</div>
<script>%%JS%%</script>
</body>
</html>
"""
ticks = ''.join(f'<line x1="500" y1="172" x2="500" y2="{184 if i % 5 else 194}" stroke="rgba(243,236,217,.26)" stroke-width="1" transform="rotate({i * 3} 500 500)"/>' for i in range(120))
js = JS.replace('%%DATA%%', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
css = CSS.replace('%%VOICE%%', VOICE).replace('%%SERIF%%', SERIF)
for k, v in (('%%CSS%%', css), ('%%JS%%', js), ('%%FAVICON%%', FAVICON), ('%%STILL%%', STILL), ('%%MAP%%', MAP), ('%%TICKS%%', ticks), ('%%NODES%%', ''.join(nodes)), ('%%PAIRS%%', '\n'.join(pr)), ('%%ITEMS%%', ''.join(items))):
    page = page.replace(k, v)
open(OUT, 'w', encoding='utf-8').write(page)
print('wrote hub.html', len(page) // 1024, 'KB')
