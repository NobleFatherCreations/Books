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
  // ---- exact frames
  await p.mouse.move(2, 2);
  await p.goto(url + '?capture'); await p.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 }); await p.evaluate(() => document.fonts.ready);
  const st0 = await p.evaluate(() => FILM.state()); ok(N + 'WebGL2 pipeline up', st0.gl, 'tier ' + st0.tier + ', hdr ' + st0.hdr);
  const shot = async (t, name, hideCaps) => { await p.evaluate(([t, h]) => { FILM.seek(t); document.querySelectorAll('.cap').forEach(e => e.style.visibility = h ? 'hidden' : ''); }, [t, hideCaps]); await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(r, 30))))); const f = `${out}/${pr.name}-${name}.png`; await p.screenshot({ path: f }); return f; };
  const hash = f => crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex');
  // same time, same frame
  const times = [-20, 1.2, 30, 86.5, 125, 141, 160].filter(t => t < upto);
  let same = true, which = '';
  for (const t of times) { const fa = await shot(t, 'det-a'); await p.evaluate(() => FILM.seek(55)); await p.waitForTimeout(30); const fb = await shot(t, 'det-b');
    if (hash(fa) !== hash(fb)) { const dmax = Number(py(`
import sys
from PIL import Image
import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); b=np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(int); print(int(np.abs(a-b).max()))`, [fa, fb])); if (dmax > 1) { same = false; which += t + '(' + dmax + ') '; } } }
  ok(N + 'same time gives the same frame', same, which ? 'differs at ' + which : times.length + ' times, seeked out of order (tolerance: one brightness level, for the browser\'s own gradient rounding)');
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
  // banding in the darkest smooth scene
  if (upto > 31) { const f = await shot(30, 'band', true); const r = py(lum + `
im=np.asarray(Image.open(sys.argv[1]).convert('L')).astype(int); h,w=im.shape; row=im[int(h*.4)]
best=0; run=1
for i in range(1,w):
    if row[i]==row[i-1] and 8<row[i]<200: run+=1; best=max(best,run)
    else: run=1
print(best/w)`, [f]); ok(N + 'no banding in the light falloff', Number(r) < .05, 'longest flat run ' + (Number(r) * 100).toFixed(1) + '% of the width'); }
  // every tier draws the same scene
  if (pr.name === 'phone' && upto > 134) { const res = []; for (const tr of [0, 1, 2]) { const q = await ctx.newPage(); await q.goto(url + '?capture&tier=' + tr); await q.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 90000 }); await q.evaluate(() => { FILM.seek(133); }); await q.waitForTimeout(60); const f = `${out}/tier-${tr}.png`; await q.screenshot({ path: f }); res.push(f); await q.close(); }
    const r = py(`
import sys
from PIL import Image
import numpy as np
a=[np.asarray(Image.open(f).convert('L').resize((195,422))).astype(float) for f in sys.argv[1:]]
def c(x,y): return float(np.corrcoef(x.ravel(),y.ravel())[0,1])
print(min(c(a[0],a[1]),c(a[0],a[2])))`, res); ok(N + 'tiers show the same picture', Number(r) > .9, 'lowest correlation with full tier ' + Number(r).toFixed(3)); }
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
