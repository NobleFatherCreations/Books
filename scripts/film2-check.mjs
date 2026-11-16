#!/usr/bin/env node
// Fractal² film gate (clock-driven). node scripts/film2-check.mjs <url> [--upto=seconds] [--out=dir]
// Runs on phone, phone reduced-motion and desktop. Every frame is a function of time, so every check is exact.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs'; import crypto from 'crypto'; import { execFileSync } from 'child_process';
const url = process.argv[2]; const arg = k => (process.argv.find(a => a.startsWith('--' + k + '=')) || '').split('=')[1];
const out = arg('out') || '/tmp/film2-check'; fs.mkdirSync(out, { recursive: true });
const cues = JSON.parse(fs.readFileSync(new URL('../design/fractal2/film/cues.json', import.meta.url)));
const upto = Number(arg('upto') || cues.dur);
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const PROFILES = [
  { name: 'phone', vp: { width: 390, height: 844 }, dpr: 2, rm: false },
  { name: 'phone-rm', vp: { width: 390, height: 844 }, dpr: 2, rm: true },
  { name: 'desktop', vp: { width: 1440, height: 900 }, dpr: 1, rm: false }
];
let fail = 0; const rows = [];
function ok(name, pass, note) { rows.push([pass ? 'PASS' : 'FAIL', name, note || '']); if (!pass) fail++; }
const py = (code, args) => execFileSync('python3', ['-I', '-c', code, ...args], { encoding: 'utf8' }).trim();
const lum = `
import sys,json
from PIL import Image
import numpy as np
def L(a):
    a=a/255.0; a=np.where(a<=0.03928,a/12.92,((a+0.055)/1.055)**2.4); return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
`;
const b = await chromium.launch({ args: GL });
for (const pr of PROFILES) {
  const ctx = await b.newContext({ viewport: pr.vp, deviceScaleFactor: pr.dpr, reducedMotion: pr.rm ? 'reduce' : 'no-preference' });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const N = pr.name + ': ';
  // ---- real playback first (no capture flag): Begin, time advances, pause holds, no layout shift
  await p.goto(url); await p.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 });
  await p.evaluate(() => { window.__cls = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); });
  await p.click('#begin'); await p.waitForTimeout(7000);
  let s = await p.evaluate(() => FILM.state());
  ok(N + 'begin starts the film', s.mode === 'film' && s.playing && s.t > .25, 't=' + s.t + (pr.rm ? ' (reduced motion still plays)' : ''));
  await p.keyboard.press('Space'); await p.waitForTimeout(300); const a = await p.evaluate(() => FILM.state().t); await p.waitForTimeout(700); const c = await p.evaluate(() => FILM.state());
  ok(N + 'pause holds the clock', !c.playing && Math.abs(c.t - a) < .02, a + ' -> ' + c.t);
  const cls = await p.evaluate(() => window.__cls); ok(N + 'zero layout shift', cls === 0, 'cls=' + cls);
  const budget = await p.evaluate(() => ({ wc: [...document.querySelectorAll('*')].filter(e => getComputedStyle(e).willChange !== 'auto').length, nodes: document.querySelectorAll('#stage *').length, cv: [...document.querySelectorAll('canvas')].map(c => [c.width, c.height]), st: FILM.state() }));
  ok(N + 'layer budget', budget.wc === 0 && budget.nodes < 120 && budget.cv.length === 1 && budget.cv[0][0] <= pr.vp.width * 2 && budget.st.peakMB < (pr.name === 'desktop' ? 260 : 170), `will-change ${budget.wc}, nodes ${budget.nodes}, canvas ${budget.cv[0]}, gpu ${budget.st.peakMB} MB`);
  if (upto >= cues.dur) {
    await p.evaluate(() => { FILM.seek(FILM.dur - 1.5); FILM.play(); }); await p.waitForFunction(() => !FILM.state().playing, null, { timeout: 30000 }).catch(() => {});   // software GL draws slowly: wait for the clock, not the wall
    const e = await p.evaluate(() => { const a = document.querySelector('#end .door'), r = a.getBoundingClientRect(), s = FILM.state(); return { t: s.t, playing: s.playing, dur: FILM.dur, op: +getComputedStyle(a).opacity, vis: getComputedStyle(document.getElementById('end')).display !== 'none', r: [r.left, r.top, r.right, r.bottom], href: a.getAttribute('href'), W: innerWidth, H: innerHeight }; });
    ok(N + 'playing to the end shows "Enter the map"', !e.playing && e.t >= e.dur - .01 && e.vis && e.op > .98 && e.r[0] >= 0 && e.r[2] <= e.W && e.r[3] <= e.H && e.href === '/fractal2/hub', `t ${e.t}/${e.dur}, opacity ${e.op}, box ${e.r.map(Math.round)}, href ${e.href}`);
    await p.click('#end .door', { noWaitAfter: true }); await p.waitForURL(/\/fractal2\/hub/, { waitUntil: 'commit', timeout: 90000 }).catch(() => {});
    await p.waitForLoadState('domcontentloaded', { timeout: 30000 }).catch(() => {}); const there = new URL(p.url()).pathname, ttl = await p.title().catch(() => '');
    ok(N + '"Enter the map" opens the hub', /\/fractal2\/hub\/?$/.test(there) && /map/i.test(ttl), there + ' "' + ttl + '"');
  }
  // ---- exact frames
  await p.mouse.move(2, 2);
  await p.goto(url + '?capture'); await p.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 }); await p.evaluate(() => document.fonts.ready);
  const st0 = await p.evaluate(() => FILM.state()); ok(N + 'WebGL2 pipeline up', st0.gl, 'tier ' + st0.tier + ', hdr ' + st0.hdr);
  const shot = async (t, name, hideCaps) => { await p.evaluate(([t, h]) => { FILM.seek(t); document.querySelectorAll('.cap').forEach(e => e.style.visibility = h ? 'hidden' : ''); }, [t, hideCaps]); await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 30))))); const f = `${out}/${pr.name}-${name}.png`; await p.screenshot({ path: f }); return f; };
  const hash = f => crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex');
  // same time, same frame
  const times = [-20, 1.2, 30, 86.5, 125, 141, 160, 192, 207, 226, 242.5, 268, 316, 336, 352, 357, 388, 415, 427, 446, 460, 482, 500, 526, 548, 606, 694, 740, 758, 815, 900, 1000, 1088, 1098, 1112].filter(t => t < upto);
  let same = true, which = '';
  for (const t of times) { const fa = await shot(t, 'det-a'); await p.evaluate(() => FILM.seek(55)); await p.waitForTimeout(30); const fb = await shot(t, 'det-b');
    if (hash(fa) !== hash(fb)) { const dmax = Number(py(`
import sys
from PIL import Image
import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); b=np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(int); print(int(np.abs(a-b).max()))`, [fa, fb])); if (dmax > 1) { same = false; which += t + '(' + dmax + ') '; } } }
  ok(N + 'same time gives the same frame', same, which ? 'differs at ' + which : times.length + ' times, seeked out of order (tolerance: one brightness level, for the browser\'s own gradient rounding)');
  // the end: seek to the last moments; the button is there, on screen, under the last line, leading to the hub
  if (upto >= cues.dur) { let eb = [];
    for (const t of [cues.dur - 8, cues.dur - .5, cues.dur]) { const e = await p.evaluate(t => { FILM.seek(t); const a = document.querySelector('#end .door'), r = a.getBoundingClientRect(), c = [...document.querySelectorAll('.cap')].find(e => +e.style.opacity > .5), g = c ? [...c.querySelectorAll('.g')].map(x => x.getBoundingClientRect()) : []; return { op: +getComputedStyle(a).opacity, on: getComputedStyle(document.getElementById('end')).display !== 'none', r: [r.left, r.top, r.right, r.bottom], c: g.length ? [Math.min(...g.map(r => r.left)), Math.min(...g.map(r => r.top)), Math.max(...g.map(r => r.right)), Math.max(...g.map(r => r.bottom))] : null, href: a.getAttribute('href') }; }, t);
      if (!(e.on && e.op > .98)) eb.push(t + ': not shown (' + e.op + ')'); else { if (e.r[0] < 0 || e.r[2] > pr.vp.width || e.r[3] > pr.vp.height - 4) eb.push(t + ': off screen'); if (!e.c) eb.push(t + ': last line not on screen'); else if (e.r[1] < e.c[3] + 8) eb.push(t + ': on the last line'); if (e.href !== '/fractal2/hub') eb.push('href ' + e.href); } }
    ok(N + '"Enter the map" is there at the end (by seek), under the last line', eb.length === 0, eb.join('; ') || 'last 8 s'); }
  // round picture
  if (upto > 152) { const f = await shot(151, 'round', true); const dm = await p.evaluate(() => FILM.dims()); const r = py(lum + `
im=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); m=L(im)>0.012
d=float(sys.argv[2]); cx=int(float(sys.argv[3])*d); cy=int(float(sys.argv[4])*d)
def ext(v,c):
    out=[]
    for step in (-1,1):
        i=c; gap=0; last=c
        while 0<=i<len(v) and gap<70:
            if v[i]: last=i; gap=0
            else: gap+=1
            i+=step
        out.append(last)
    return out[1]-out[0]
print(json.dumps([int(ext(m[cy],cx)),int(ext(m[:,cx],cy))]))`, [f, String(pr.dpr), String(dm.W * dm.CXF), String(dm.H * dm.CYF)]); const [w, h] = JSON.parse(r); ok(N + 'round picture', w > 200 && Math.abs(w - h) / w < .012, `${w} x ${h} px`); }
  // captions: on-screen time (from the cue table) and contrast (from pixels)
  const caps = cues.caps.filter(c => c.t0 < upto - 1);
  const shortc = caps.filter(c => c.t1 - c.t0 < c.need && c.text.split(' ').length > 1);
  ok(N + 'caption time on screen (0.35 s a word + 1.2 s)', shortc.length === 0, shortc.length ? shortc.map(c => c.slug).join(', ') : caps.length + ' captions');
  const over = cues.caps.filter((c, i) => i + 1 < cues.caps.length && c.t1 + (c.text.split(' ').length > 1 ? .6 : .22) > cues.caps[i + 1].t0 + .001);
  ok(N + 'one caption at a time (the last has left before the next arrives)', over.length === 0, over.length ? over.length + ' overlap, first: ' + over[0].slug : cues.caps.length + ' captions');
  { let bad = [];
    for (const c of caps) for (const dt of [.02, .12, .25]) {
      const r = await p.evaluate(t => { FILM.seek(t); const g = [...document.querySelectorAll('.cap')].filter(e => +e.style.opacity > .02).flatMap(e => [...e.querySelectorAll('.g')].map(x => +x.style.opacity * +e.style.opacity)); const k = FILM.S.poolk == null ? 1 : FILM.S.poolk; return [Math.max(0, ...g), +document.getElementById('pool').style.opacity, k]; }, c.t0 + dt);
      if (r[0] > .05 && r[1] < .97 * r[2] - .005) bad.push(`${c.slug}+${dt}: words ${r[0].toFixed(2)}, ground ${r[1].toFixed(2)}`); }
    ok(N + 'the dark ground is in place before any word shows', bad.length === 0, bad.length ? bad.length + ' moments, first: ' + bad[0] : caps.length + ' captions x 3 moments'); }
  let worst = 99, worstAt = '', inView = true;
  for (const c of caps) {
    const t = Math.min(c.t0 + 1.6, (c.t0 + c.t1) / 2 + .4);
    await p.evaluate(t => FILM.seek(t), t); await p.waitForTimeout(25);
    const r = await p.evaluate(() => { const e = [...document.querySelectorAll('.cap')].find(e => +e.style.opacity > .5); if (!e) return null; const g = [...e.querySelectorAll('.g')].map(x => x.getBoundingClientRect()); const x0 = Math.min(...g.map(r => r.left)), x1 = Math.max(...g.map(r => r.right)), y0 = Math.min(...g.map(r => r.top)), y1 = Math.max(...g.map(r => r.bottom)); return [x0, y0, x1, y1, innerWidth, innerHeight]; });
    if (!r) { ok(N + 'caption shown: ' + c.slug, false, 'not visible at ' + t.toFixed(1)); continue; }
    if (r[0] < 4 || r[2] > r[4] - 4 || r[3] > r[5] - 8 || r[1] < 0) inView = false;
    const f = await shot(t, 'cc', true);
    const v = Number(py(lum + `
x0,y0,x1,y1,d=[float(v) for v in sys.argv[2:7]]
im=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)[int(y0*d):int(y1*d),int(x0*d):int(x1*d)]
bg=np.percentile(L(im),99); tx=L(np.array([[[243,236,217]]],dtype=float))[0,0]
print((tx+0.05)/(bg+0.05))`, [f, ...r.slice(0, 4).map(String), String(pr.dpr)]));
    if (v < worst) { worst = v; worstAt = c.slug + ' @' + t.toFixed(1); }
  }
  ok(N + 'caption contrast (brightest pixel behind the words)', worst >= 4.5, worst.toFixed(1) + ':1 at ' + worstAt);
  ok(N + 'captions inside the screen', inView, '');
  // ---- GPU labels (map text drawn by the engine): readable size, inside the screen, never on top of each other or of a marker
  const capAt = (slug, f, n = 0) => { const c = cues.caps.filter(x => x.slug === slug)[n]; return c ? c.t0 + (c.t1 - c.t0) * f : null; };
  const labelTimes = [capAt('election-becomes-idealize-covenant', .5), capAt('i-will-never-leave', .6), capAt('and-the-one-who', .6), capAt('a-pattern-observed-traced', .9), capAt('it-only-needs-your', .5),
    capAt('i-did-not-rise', .5), capAt('the-sun-did-not', .5), capAt('like-the-debt-prison', .2), capAt('like-the-debt-prison', .5),
    capAt('the-muslim-speaks-of', .8), capAt('the-jew-speaks-of', .5), capAt('if-none-of-those', .6), capAt('which-means-something-real', 1) + 4, capAt('which-means-something-real', 1) + 10].filter(t => t != null && t < upto);
  let lbBad = [], lbMin = 99;
  for (const t of labelTimes) {
    await p.evaluate(t => FILM.seek(t), t);
    const L = await p.evaluate(() => (FILM.rec || []).filter(r => r.a > .35 && r.soft < .5));
    const cb = await p.evaluate(() => { const e = [...document.querySelectorAll('.cap')].find(e => +e.style.opacity > .3); if (!e) return null; const g = [...e.querySelectorAll('.g')].map(x => x.getBoundingClientRect()); return [Math.min(...g.map(r => r.left)), Math.min(...g.map(r => r.top)), Math.max(...g.map(r => r.right)), Math.max(...g.map(r => r.bottom))]; });
    const box = r => { const x0 = r.al === 0 ? r.x - r.w / 2 : r.al < 0 ? r.x : r.x - r.w; return r.dot ? [r.x - 7, r.y - 7, r.x + 7, r.y + 7] : [x0, r.y - r.size * .72, x0 + r.w, r.y + r.size * .2]; };
    const B = L.map(r => [box(r), r]);
    for (const [b, r] of B) { if (r.dot) continue; lbMin = Math.min(lbMin, r.size); if (r.size < 12) lbBad.push(`${t.toFixed(1)} "${r.s}" ${r.size.toFixed(1)}px`);
      if (cb && (pr.name === 'desktop' ? b[2] > cb[0] - 8 : b[0] < cb[2] + 8 && b[2] > cb[0] - 8 && b[1] < cb[3] + 8 && b[3] > cb[1] - 8)) lbBad.push(`${t.toFixed(1)} "${r.s || 'marker'}" in the caption's place`);
      if (r.mapTop != null && b[3] > r.mapTop - 4) lbBad.push(`${t.toFixed(1)} "${r.s}" on the map's outer words`);
      if (b[0] < 2 || b[2] > pr.vp.width - 2 || b[1] < 0 || b[3] > pr.vp.height) lbBad.push(`${t.toFixed(1)} "${r.s}" off screen`); }
    for (let i = 0; i < B.length; i++) for (let j = i + 1; j < B.length; j++) { const [a, ra] = B[i], [c, rc] = B[j]; if (ra.dot && rc.dot) continue;
      const ov = Math.min(a[2], c[2]) - Math.max(a[0], c[0]), oh = Math.min(a[3], c[3]) - Math.max(a[1], c[1]); if (ov > 2 && oh > 2) lbBad.push(`${t.toFixed(1)} "${ra.s || 'marker'}" over "${rc.s || 'marker'}"`); }
  }
  ok(N + 'GPU labels: 12 px or more, on screen, not overlapping, clear of the caption and the map rim', lbBad.length === 0, lbBad.length ? lbBad.slice(0, 4).join('; ') : labelTimes.length + ' frames, smallest ' + lbMin.toFixed(1) + ' px');
  // ---- GPU label contrast, from pixels: the same frame with and without the engine's text
  { let worstL = 99, at = '';
    for (const t of labelTimes) {
      const f1 = await shot(t, 'lb-a', true); await p.evaluate(() => { FILM.opt.notext = 1; }); const f0 = await shot(t, 'lb-b', true); await p.evaluate(() => { FILM.opt.notext = 0; });
      const L = await p.evaluate(() => (FILM.rec || []).filter(r => r.a > .35 && r.soft < .5 && !r.dot && r.s.trim()));
      const bx = L.map(r => { const x0 = r.al === 0 ? r.x - r.w / 2 : r.al < 0 ? r.x : r.x - r.w; return [x0, r.y - r.size * .72, x0 + r.w, r.y + r.size * .2, r.size]; });
      if (!bx.length) continue;
      const v = JSON.parse(py(lum + `
a=L(np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)); b=L(np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float)); d=float(sys.argv[3]); out=[]
for x0,y0,x1,y1,sz in json.loads(sys.argv[4]):
    X0,Y0,X1,Y1=max(0,int(x0*d)),max(0,int(y0*d)),int(x1*d),int(y1*d)
    A=a[Y0:Y1,X0:X1]; Bk=b[Y0:Y1,X0:X1]
    if A.size<20: continue
    m=(A-Bk)>0.03
    if m.sum()<6: out.append([0,sz]); continue
    tx=np.percentile(A[m],98); bg=np.percentile(Bk,95)
    out.append([(max(tx,bg)+0.05)/(min(tx,bg)+0.05),sz])
print(json.dumps(out))`, [f1, f0, String(pr.dpr), JSON.stringify(bx)]));
      for (const [c, sz] of v) { const need = sz >= 24 ? 3 : 4.5; if (c / need < worstL) { worstL = c / need; at = `${t.toFixed(1)} ${c.toFixed(1)}:1 at ${sz.toFixed(0)} px`; } }
    }
    ok(N + 'GPU label contrast (4.5:1 under 24 px, 3:1 above)', worstL >= 1, at); }
  // ---- the glass: real refraction inside the lens, nothing changed outside it
  { const tg = capAt('every-technique-is-a', .78); if (tg && tg < upto) {
      const fa = await shot(tg, 'glass-a', true); await p.evaluate(() => { FILM.opt.norefr = 1; }); const fb = await shot(tg, 'glass-b', true); await p.evaluate(() => { FILM.opt.norefr = 0; });
      const st = await p.evaluate(() => { const d = FILM.dims(), S = FILM.S; return [d.H * d.CYF - S.lineh * d.U, S.glw * d.U, S.glass]; });
      const r = JSON.parse(py(`
import sys,json
from PIL import Image
import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); b=np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(int); d=float(sys.argv[3]); y=float(sys.argv[4])*d; w=float(sys.argv[5])*d
D=np.abs(a-b).max(2); Y0,Y1=int(y-w)-2,int(y+w)+2
print(json.dumps([float(D[Y0:Y1].mean()), int(np.delete(D,range(max(0,Y0),Y1),0).max())]))`, [fa, fb, String(pr.dpr), String(st[0]), String(st[1])]));
      ok(N + 'glass refracts inside the lens only', st[2] > .5 && r[0] > 2 && r[1] <= 1, `inside mean change ${r[0].toFixed(1)}, outside max ${r[1]} (glass ${st[2].toFixed(2)})`);
  } }
  // ---- the window: the light must read as whole; no dark pool may cut it off at the caption gutter (desktop: words on the right)
  if (pr.name === 'desktop') { const tw = ['the-sun-did-not', 'one-block-at-a', 'pulsing-quietly-and-waiting'].map(s => capAt(s, .5)).filter(t => t && t < upto); let worstW = 9, atW = '';
    for (const t of tw) { const f = await shot(t, 'win', true); const lx = await p.evaluate(() => { const d = FILM.dims(); return [d.W * FILM.S.cxf + FILM.S.lx * d.U, d.H * d.CYF - FILM.S.ly * d.U]; });
      const r = Number(py(lum + `
im=L(np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)); y=int(float(sys.argv[2])); W=im.shape[1]
band=np.convolve(im[y-40:y+40].mean(0),np.ones(15)/15,'same'); print(band[int(W*.625)]/max(band[int(W*.486)],1e-4))`, [f, String(lx[1])]));
      if (r < worstW) { worstW = r; atW = t.toFixed(1); } }
    if (tw.length) ok(N + 'window light reaches the caption column (no cut)', worstW >= .1, `lowest gutter ratio ${worstW.toFixed(2)} at ${atW} (a dark pool gives under 0.08)`); }
  // banding in the darkest smooth scene
  if (upto > 31) { const f = await shot(30, 'band', true); const r = py(lum + `
im=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(int); h,w=im.shape; row=im[int(h*.4)]
best=0; run=1
for i in range(1,w):
    if row[i]==row[i-1] and 8<row[i]<200: run+=1; best=max(best,run)
    else: run=1
print(best/w)`, [f]); ok(N + 'no banding in the light falloff', Number(r) < .05, 'longest flat run ' + (Number(r) * 100).toFixed(1) + '% of the width'); }
  // every tier draws the same scene
  for (const tt of [133, 412.6]) if (pr.name === 'phone' && upto > tt + 1) { const res = []; for (const tr of [0, 1, 2]) { const q = await ctx.newPage(); await q.goto(url + '?capture&tier=' + tr); await q.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 }); await q.evaluate(tt => { FILM.seek(tt); }, tt); await q.waitForTimeout(60); const f = `${out}/tier-${tr}-${tt}.png`; await q.screenshot({ path: f }); res.push(f); await q.close(); }
    const r = py(`
import sys
from PIL import Image
import numpy as np
a=[np.asarray(Image.open(f).convert('L').resize((195,422))).astype(float) for f in sys.argv[1:]]
def c(x,y): return float(np.corrcoef(x.ravel(),y.ravel())[0,1])
print(min(c(a[0],a[1]),c(a[0],a[2])))`, res); ok(N + 'tiers show the same picture at ' + tt + ' s', Number(r) > .9, 'lowest correlation with full tier ' + Number(r).toFixed(3)); }
  { const q = await ctx.newPage(); await q.goto(url + '?capture&nogl'); await q.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 }); await q.evaluate(() => FILM.seek(30)); await q.waitForTimeout(60); const f = `${out}/${pr.name}-nogl.png`; await q.screenshot({ path: f });
    const r = py(lum + `im=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); print(float(L(im).max()))`, [f]); ok(N + 'no-WebGL fallback draws', Number(r) > .3, 'max luminance ' + Number(r).toFixed(2)); await q.close(); }
  ok(N + 'no errors', errs.length === 0, errs.slice(0, 3).join(' | '));
  await ctx.close();
}
await b.close();
const w = Math.max(...rows.map(r => r[1].length));
for (const r of rows) console.log(r[0], r[1].padEnd(w), r[2]);
console.log(fail ? `FILM2 CHECK FAIL (${fail})` : 'FILM2 CHECK PASS');
process.exit(fail ? 1 : 0);
