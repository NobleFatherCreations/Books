#!/usr/bin/env node
// Frame walk: scrolls a scroll-story the way a thumb does and writes contact sheets you can READ in one look.
//   node scripts/frame-walk.mjs <url> <outdir> [--n=48] [--vp=390x844] [--click=#begin] [--from=0] [--to=1] [--cols=8] [--settle=900] [--rm]
// Each tile is labelled with its scroll % and the caption visible at that moment (largest visible text with opacity > .5).
// Also prints: console errors, sideways overflow, and a motion table (camera scale change per screen of scroll) when the page exposes window.__cam().
import { createRequire } from 'module'; import fs from 'fs'; import { execFileSync } from 'child_process';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const [, , url, out, ...rest] = process.argv; const o = Object.fromEntries(rest.map((a) => { const m = a.match(/^--([a-z]+)(?:=(.*))?$/); return [m[1], m[2] ?? '1']; }));
const n = +(o.n || 48), [vw, vh] = (o.vp || '390x844').split('x').map(Number), cols = +(o.cols || 8), from = +(o.from || 0), to = +(o.to || 1), settle = +(o.settle || 900);
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const mob = vw < 700; const ctx = await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1, isMobile: mob, hasTouch: mob, reducedMotion: o.rm ? 'reduce' : 'no-preference' });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
const bad = []; p.on('requestfailed', (r) => bad.push(r.url())); p.on('response', (r) => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
await p.goto(url, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' }); await p.waitForTimeout(1200);
const meta = []; const shot = async (name) => { await p.screenshot({ path: `${out}/${name}.jpg`, type: 'jpeg', quality: 70 }); };
if (o.click) { await shot('f-pre'); meta.push({ f: 'f-pre', pct: 'pre', cap: '(before ' + o.click + ')' }); await p.click(o.click); await p.waitForTimeout(2500); }
const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
for (let i = 0; i < n; i++) {
  const y = Math.round(H * (from + (to - from) * i / (n - 1))); await p.evaluate((v) => scrollTo(0, v), y); await p.waitForTimeout(settle);
  const info = await p.evaluate(() => { let best = '', bs = 0; for (const e of document.querySelectorAll('main p, main h1, main h2, main h3, main li, main a, main button, [data-cap]')) { const r = e.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight || !r.width) continue; let op = 1, x = e; while (x && x !== document.body) { op *= +getComputedStyle(x).opacity; x = x.parentElement; } const ws = e.querySelectorAll('.w'); let vis = e.innerText.trim(); if (ws.length) vis = [...ws].filter((w) => +getComputedStyle(w).opacity > .5).map((w) => w.textContent).join(' '); if (op < .5 || !vis) continue; const fs = parseFloat(getComputedStyle(e).fontSize); if (fs > bs) { bs = fs; best = vis; } } return { cap: best.slice(0, 90), cam: window.__cam ? window.__cam() : null, over: document.documentElement.scrollWidth > innerWidth + 1 }; });
  const f = 'f-' + String(i).padStart(3, '0'); await shot(f); meta.push({ f, y, pct: (100 * y / H).toFixed(1), ...info });
}
await b.close(); fs.writeFileSync(`${out}/walk.json`, JSON.stringify({ url, vw, vh, H, meta, errs, bad }, null, 1));
execFileSync('python3', [new URL('./frame-sheet.py', import.meta.url).pathname, out, String(cols)], { stdio: 'inherit' });
console.log(`screens of scroll: ${(H / vh).toFixed(1)} | console errors: ${errs.length} | failed requests: ${bad.length} | sideways overflow: ${meta.some((m) => m.over)}`);
errs.slice(0, 5).forEach((e) => console.log('  ERR', e)); bad.slice(0, 5).forEach((e) => console.log('  REQ', e));
const cm = meta.filter((m) => m.cam); if (cm.length > 2) { let worst = 0, at = ''; for (let i = 1; i < cm.length; i++) { const dz = Math.abs(Math.log(cm[i].cam.z / cm[i - 1].cam.z)) / ((cm[i].y - cm[i - 1].y) / vh || 1); if (dz > worst) { worst = dz; at = cm[i].pct; } } console.log(`fastest camera move: ${worst.toFixed(2)} log-scale per screen of scroll, at ${at}%`); }
