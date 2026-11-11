#!/usr/bin/env node
// Visual-quality gates v2 for any page or scroll experience (necessary, NOT sufficient: a human must still read the screenshots).
//
//   node scripts/design-gates.mjs <url> <outdir> [options]
//     --profiles a,b      phone-light, phone-dark, phone-reduced, desktop-light, desktop-dark   (default: all five)
//     --max N --step 0.7  number of scroll steps (default 60) and step size in viewport heights
//     --stage "css"       selector for figure/stage elements (default: canvas, figure, svg, video, img)
//     --engine chromium   chromium | webkit | firefox (only chromium is installed in the cloud container; webkit gives real-Safari-like checks where available)
//     --baseline DIR      compare against an approved run's screenshots (perceptual diff)
//     --click "css"       press this first (e.g. "#begin") for pages whose scroll is locked until a button is pressed
//     --no-motion         skip the CPU-throttled frame-time pass     --no-pixels  skip pixel analysis
//     --dark-js "js"      run once after load in *-dark profiles for sites with their own theme toggle, e.g. --dark-js "document.querySelector('#darkbtn').click()"
//
// DOM checks:   figure/text overlap, text over text, translucent header, tiny text, small tap targets, errors, external requests,
//               overflow, fonts, simultaneous animations, reduced-motion violations, token sprawl (radii, shadows, families, colours).
// Motion pass:  scrolls the whole page at constant speed under 4x CPU throttle; reports frame-time p95/max, dropped frames, long tasks.
// Pixel checks: (design-pixels.py) contrast against the rendered pixels behind text, hue count, dead space, focal dominance,
//               scroll determinism (same position looks the same after scrolling away and back), baseline diff, contact sheet.
// Output: <outdir>/<profile>/NNN.jpg (+ .json), contact.jpg (read it first), report.json.  Exit 1 if any FAIL.
// Playwright and Chromium are preinstalled; never run `playwright install`.
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
const require = createRequire(import.meta.url);
const pw = require('playwright');

const args = process.argv.slice(2);
const url = args[0], out = args[1];
if (!url || !out) { console.error('usage: design-gates.mjs <url> <outdir> [options]  (see header)'); process.exit(2); }
const opt = (k, d) => { const i = args.indexOf('--' + k); return i > -1 ? args[i + 1] : d; };
const flag = (k) => args.includes('--' + k);
const MAX = +opt('max', 60), STEP = +opt('step', 0.7);
const STAGE = opt('stage', 'canvas, figure, [data-figure], svg[viewBox], video, img');
const ENGINE = opt('engine', 'chromium');
const BASE = opt('baseline', '');
const DARKJS = opt('dark-js', '');
const PROFILES = (opt('profiles', 'phone-light,phone-dark,phone-reduced,desktop-light,desktop-dark')).split(',');
const SPEC = {
  'phone-light':   { viewport: { width: 390, height: 844 }, dsf: 2, mobile: true,  scheme: 'light', reduce: 'no-preference' },
  'phone-dark':    { viewport: { width: 390, height: 844 }, dsf: 2, mobile: true,  scheme: 'dark',  reduce: 'no-preference' },
  'phone-reduced': { viewport: { width: 390, height: 844 }, dsf: 2, mobile: true,  scheme: 'light', reduce: 'reduce' },
  'desktop-light': { viewport: { width: 1440, height: 900 }, dsf: 1, mobile: false, scheme: 'light', reduce: 'no-preference' },
  'desktop-dark':  { viewport: { width: 1440, height: 900 }, dsf: 1, mobile: false, scheme: 'dark',  reduce: 'no-preference' },
};
fs.mkdirSync(out, { recursive: true });
const origin = new URL(url).origin;

// ---- runs inside the page for what is currently in the viewport
const probe = ({ stage, phone }) => {
  const vw = innerWidth, vh = innerHeight;
  const vis = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return null;
    let p = el.parentElement; while (p) { const c = getComputedStyle(p); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity < 0.05) return null; p = p.parentElement; }
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2 || r.bottom < 0 || r.top > vh || r.right < 0 || r.left > vw) return null;
    return r;
  };
  const label = (el) => (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + ' "' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 28) + '"');
  const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  const isLeaf = (el) => [...el.children].every((c) => getComputedStyle(c).display.startsWith('inline') || c.tagName === 'BR');
  const texts = [...document.querySelectorAll('p,h1,h2,h3,h4,h5,li,blockquote,figcaption,span,a,button,label,div,td,th')]
    .filter((el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 2) && isLeaf(el))
    .map((el) => ({ el, r: vis(el) })).filter((x) => x.r)
    .map((x) => { // real text line boxes (a stretched card link has a huge element box but small text)
      const lines = []; for (const n of x.el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { const rg = document.createRange(); rg.selectNodeContents(n); for (const q of rg.getClientRects()) if (q.width > 1 && q.height > 1 && q.bottom > 0 && q.top < vh) lines.push(q); }
      return { ...x, lines }; }).filter((x) => x.lines.length);
  const figs = [...document.querySelectorAll(stage)].map((el) => ({ el, r: vis(el) }))
    .filter((x) => x.r && x.r.width > 120 && x.r.height > 120 && !x.el.closest('header,nav,footer,button,a'));
  const isBar = (el) => { let p = el; while (p && p !== document.body) { const c = getComputedStyle(p); if (c.position === 'fixed' || c.position === 'sticky') {
      const m = c.backgroundColor.match(/[\d.]+/g) || []; const a = m.length === 4 ? +m[3] : (c.backgroundColor === 'transparent' ? 0 : 1);
      if (a >= 0.9 || /blur/.test(c.backdropFilter || c.webkitBackdropFilter || '')) return true; } p = p.parentElement; } return false; };
  const f = { figText: [], svgLabel: [], bleed: [], textText: [], hidden: [], header: null, tiny: [], taps: [], anims: 0, texts: [] };
  for (const t of texts) {
    const area = t.r.width * t.r.height;
    for (const g of figs) {
      if (g.el.contains(t.el) || t.el.contains(g.el)) continue;
      if (isBar(t.el)) continue;
      if (isBar(g.el) && !isBar(t.el)) continue;   // text scrolling UNDER an opaque sticky stage is hidden, not colliding
      const i = inter(t.r, g.r);
      if (i / area > 0.12) {
        const full = g.r.width * g.r.height > vw * vh * 0.8;
        (full ? f.bleed : f.figText).push(label(t.el) + '  OVER  ' + label(g.el)); break;
      }
    }
  }
  for (let a = 0; a < texts.length; a++) for (let b = a + 1; b < texts.length; b++) {
    const A = texts[a], B = texts[b];
    if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
    if (isBar(A.el) || isBar(B.el)) continue;   // content scrolling under an opaque bar is not a collision
    let hit = false;
    for (const la of A.lines) { for (const lb of B.lines) { const i = inter(la, lb), m = Math.min(la.width * la.height, lb.width * lb.height); if (m > 0 && i / m > 0.25) { hit = true; break; } } if (hit) break; }
    if (hit) f.textText.push(label(A.el) + '  OVER  ' + label(B.el));
  }
  // labels INSIDE a figure (SVG text) that cross the figure's own shapes: element-box tests cannot see these
  for (const el of document.querySelectorAll('svg text')) {
    const r = vis(el); if (!r || r.width < 10) continue;
    let hits = 0; const nx = 6, ny = 3;
    for (let ix = 0; ix < nx; ix++) for (let iy = 0; iy < ny; iy++) {
      const x = r.left + (ix + 0.5) * r.width / nx, y = r.top + (iy + 0.5) * r.height / ny;
      if (document.elementsFromPoint(x, y).some((e) => e !== el && e.ownerSVGElement && /^(path|line|circle|rect|polygon|polyline|ellipse)$/i.test(e.tagName) && !e.classList.contains('guide') && !e.classList.contains('cross') && !e.classList.contains('minor') && +getComputedStyle(e).opacity > 0.12)) hits++;
    }
    if (hits >= 3) f.svgLabel.push(label(el) + ' crosses figure shapes (' + hits + '/' + nx * ny + ' sample points)');
  }
  const hdr = [...document.querySelectorAll('header,nav,[class*=header],[class*=topbar]')].map((el) => ({ el, cs: getComputedStyle(el), r: el.getBoundingClientRect() }))
    .find((x) => (x.cs.position === 'fixed' || x.cs.position === 'sticky') && x.r.top <= 8 && x.r.height < 160 && x.r.width > vw * 0.5);
  if (hdr) {
    const m = hdr.cs.backgroundColor.match(/[\d.]+/g) || [];
    const alpha = m.length === 4 ? +m[3] : (hdr.cs.backgroundColor === 'transparent' ? 0 : 1);
    const blur = /blur/.test(hdr.cs.backdropFilter || hdr.cs.webkitBackdropFilter || '');
    f.header = { alpha: +alpha.toFixed(2), blur, h: Math.round(hdr.r.height) };
    f.headerOver = texts.filter((t) => !hdr.el.contains(t.el) && inter(t.r, hdr.r) / (t.r.width * t.r.height) > 0.3).length;
  }
  for (const el of document.querySelectorAll('p,h1,h2,h3,li,blockquote')) {
    if ((el.textContent || '').trim().length < 20) continue;
    const r = el.getBoundingClientRect(); const cy = r.top + r.height / 2;
    if (cy > vh * 0.25 && cy < vh * 0.75 && r.width > 40) {
      let o = 1, p = el; while (p) { o *= +getComputedStyle(p).opacity; if (getComputedStyle(p).display === 'none' || getComputedStyle(p).visibility === 'hidden') { o = 1; break; } p = p.parentElement; }
      if (o < 0.15 && !el.closest('[hidden],[aria-hidden=true],details:not([open])')) f.hidden.push(label(el));
    }
  }
  const covers = [...document.querySelectorAll('body *')].filter((e) => { const c = getComputedStyle(e); if (c.position !== 'fixed' && c.position !== 'sticky') return false; const m = c.backgroundColor.match(/[\d.]+/g) || []; const al = m.length === 4 ? +m[3] : (c.backgroundColor === 'transparent' ? 0 : 1); return (al >= 0.9 || /blur/.test(c.backdropFilter || c.webkitBackdropFilter || '')) && e.getBoundingClientRect().height > 20; }).map((e) => ({ e, r: e.getBoundingClientRect() }));
  for (const t of texts) {
    const cs = getComputedStyle(t.el); const fs = parseFloat(cs.fontSize);
    if (fs < (phone ? 12 : 11)) f.tiny.push(label(t.el) + ' ' + fs + 'px');
    const m = cs.color.match(/[\d.]+/g) || [0, 0, 0];
    const cx = t.r.left + t.r.width / 2, cy = t.r.top + t.r.height / 2;
    const underBar = covers.some((c) => !c.e.contains(t.el) && cy > c.r.top && cy < c.r.bottom && cx > c.r.left && cx < c.r.right);   // text hidden under an opaque pinned element (bar, sticky stage)
    let top = t.r.top, bot = t.r.bottom;   // measure only the visible part when an opaque pinned element covers some of the text
    for (const c of covers) if (!c.e.contains(t.el) && cx > c.r.left && cx < c.r.right) { if (c.r.bottom > top && c.r.bottom < bot) top = c.r.bottom; if (c.r.top < bot && c.r.top > top) bot = c.r.top; }
    if (!underBar && bot - top > 6 && f.texts.length < 90 && t.r.width > 16) f.texts.push({ x: t.r.left, y: top, w: t.r.width, h: bot - top, color: [+m[0], +m[1], +m[2]], fs, fw: +cs.fontWeight || 400, label: label(t.el) });
  }
  if (phone) for (const el of document.querySelectorAll('a,button,input,select,summary,[role=button]')) {
    const r = vis(el); if (r && (r.width < 40 || r.height < 40) && (el.textContent || '').trim().length) f.taps.push(label(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  }
  f.anims = document.getAnimations().filter((a) => a.playState === 'running').length;
  return f;
};

// token sprawl across the whole page
const tokens = () => {
  const radii = new Set(), shadows = new Set(), fams = new Set(), cols = new Set();
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none') continue;
    if (cs.borderTopLeftRadius !== '0px') radii.add(cs.borderTopLeftRadius);
    if (cs.boxShadow !== 'none') shadows.add(cs.boxShadow.replace(/rgba?\([^)]*\)/g, 'C'));
    if ((el.textContent || '').trim().length > 2 && el.children.length === 0) { fams.add(cs.fontFamily.split(',')[0].replace(/["']/g, '').trim()); cols.add(cs.color); }
  }
  return { radii: radii.size, shadows: shadows.size, families: [...fams], colors: cols.size };
};

const report = { url, at: new Date().toISOString(), engine: ENGINE, profiles: {} };
let fails = 0;
const launcher = pw[ENGINE];
if (!launcher) { console.error('unknown engine ' + ENGINE); process.exit(2); }
let browser;
try {
  browser = await launcher.launch(ENGINE === 'chromium' ? { executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--no-sandbox'] } : {});
} catch (e) {
  console.error(`Could not launch ${ENGINE}: ${String(e).split('\n')[0]}\n(The cloud container only has Chromium. For real iPhone behaviour use a private preview link and scripts/../docs PHONE-CHECK.)`);
  process.exit(2);
}
const here = path.dirname(new URL(import.meta.url).pathname);
for (const name of PROFILES) {
  const S = SPEC[name]; if (!S) continue;
  const ctx = await browser.newContext({ viewport: S.viewport, deviceScaleFactor: S.dsf, isMobile: S.mobile && ENGINE !== 'firefox', hasTouch: S.mobile, colorScheme: S.scheme, reducedMotion: S.reduce });
  const page = await ctx.newPage();
  const errors = [], external = new Set();
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 160)));
  page.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights|ERR_FAILED|Failed to load resource/.test(m.text())) errors.push('console: ' + m.text().slice(0, 160)); });
  page.on('response', (r) => { if (r.status() >= 400 && !/cloudflareinsights/.test(r.url())) errors.push(r.status() + ' ' + r.url().slice(0, 100)); });
  page.on('request', (rq) => { const u = rq.url(); if (!u.startsWith(origin) && !u.startsWith('data:') && !u.startsWith('blob:') && !/cloudflareinsights/.test(u)) external.add(u.slice(0, 100)); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.addStyleTag({ content: 'html{scroll-behavior:auto !important}' }).catch(() => {});   // measure positions and pixels at the same instant
  await page.waitForTimeout(1200);
  if (opt('click')) { await page.click(opt('click')).catch(() => {}); await page.waitForTimeout(2000); }   // pages with a locked opening (a Begin button): press it, or the gates only ever see the first screen
  if (DARKJS && name.includes('dark')) { await page.evaluate(DARKJS).catch(() => {}); await page.waitForTimeout(600); }
  const dir = path.join(out, name); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const R = { steps: 0, svgLabel: {}, bleed: {}, hidden: {}, figText: {}, textText: {}, headerThin: 0, headerOver: 0, tiny: {}, taps: {}, maxAnims: 0 };
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  const vh = S.viewport.height; const n = Math.min(MAX, Math.ceil(total / (vh * STEP)));
  for (let i = 0; i < n; i++) {
    await page.evaluate((y) => scrollTo(0, y), Math.round(i * vh * STEP));
    await page.waitForTimeout(450);
    const f = await page.evaluate(probe, { stage: STAGE, phone: S.mobile });
    R.steps++;
    f.figText.forEach((k) => (R.figText[k] = (R.figText[k] || 0) + 1));
    f.textText.forEach((k) => (R.textText[k] = (R.textText[k] || 0) + 1));
    f.bleed.forEach((k) => (R.bleed[k] = (R.bleed[k] || 0) + 1)); f.hidden.forEach((k) => (R.hidden[k] = (R.hidden[k] || 0) + 1));
    f.svgLabel.forEach((k) => (R.svgLabel[k] = (R.svgLabel[k] || 0) + 1));
    f.tiny.forEach((k) => (R.tiny[k] = 1)); f.taps.forEach((k) => (R.taps[k] = 1));
    if (f.header && f.header.alpha < 0.8 && !f.header.blur && f.headerOver) R.headerThin++;
    R.headerOver += f.headerOver || 0; R.maxAnims = Math.max(R.maxAnims, f.anims);
    const id = String(i).padStart(3, '0');
    await page.screenshot({ path: path.join(dir, id + '.jpg'), type: 'jpeg', quality: 88 });
    fs.writeFileSync(path.join(dir, id + '.json'), JSON.stringify({ texts: f.texts }));
  }
  // scroll determinism: same position, before and after scrolling away
  if (!flag('no-pixels')) for (const frac of [0.25, 0.5, 0.75]) {
    const y = Math.round(Math.max(0, (total - vh) * frac));
    await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(dir, `sync-A-${frac}.jpg`), type: 'jpeg', quality: 80 });
    await page.evaluate((v) => scrollTo(0, v), Math.min(total, y + vh * 2.5)); await page.waitForTimeout(500);
    await page.evaluate((v) => scrollTo(0, v), y); await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(dir, `sync-B-${frac}.jpg`), type: 'jpeg', quality: 80 });
  }
  const end = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth > innerWidth + 1,
    fonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '')).filter((v, i, a) => a.indexOf(v) === i),
    bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0].replace(/["']/g, '').trim(),
    h1Font: (document.querySelector('h1') ? getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0].replace(/["']/g, '').trim() : null),
  }));
  const tok = await page.evaluate(tokens);

  // motion pass under CPU throttle (Chromium only)
  let motion = null;
  if (!flag('no-motion') && ENGINE === 'chromium' && name !== 'phone-reduced') {
    try {
      const cdp = await ctx.newCDPSession(page);
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      motion = await page.evaluate(async ({ speed }) => {
        const total = document.documentElement.scrollHeight - innerHeight;
        const frames = []; let long = 0, longMs = 0;
        const po = new PerformanceObserver((l) => { for (const e of l.getEntries()) { long++; longMs += e.duration; } });
        try { po.observe({ entryTypes: ['longtask'] }); } catch (e) {}
        return await new Promise((res) => {
          let last = performance.now(), y = 0; const start = last; scrollTo(0, 0);
          const f = (t) => { frames.push(t - last); const dt = t - last; last = t; y += speed * (dt / 1000); scrollTo(0, y);
            if (y < total && t - start < 14000) requestAnimationFrame(f); else { po.disconnect(); res({ frames, long, longMs, reached: Math.round(Math.min(1, y / total) * 100) }); } };
          requestAnimationFrame(f);
        });
      }, { speed: vh * 1.2 });
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
      const fr = motion.frames.slice(5).sort((a, b) => a - b);
      motion = { frames: fr.length, p50: +fr[Math.floor(fr.length * 0.5)].toFixed(1), p95: +fr[Math.floor(fr.length * 0.95)].toFixed(1), max: +fr[fr.length - 1].toFixed(1),
        over33: +(fr.filter((x) => x > 33.4).length / fr.length * 100).toFixed(1), over50: +(fr.filter((x) => x > 50).length / fr.length * 100).toFixed(1), longTasks: motion.long, longTaskMs: Math.round(motion.longMs), reached: motion.reached };
    } catch (e) { motion = { error: String(e).slice(0, 100) }; }
  }
  await ctx.close();

  // pixel analysis
  let px = null;
  if (!flag('no-pixels')) {
    const base = BASE ? path.join(BASE, name) : '';
    const r = spawnSync('python3', [path.join(here, 'design-pixels.py'), dir, String(S.dsf)].concat(base ? [base] : []), { encoding: 'utf8', maxBuffer: 1 << 26 });
    try { px = JSON.parse(r.stdout); } catch (e) { px = { error: (r.stderr || '').slice(0, 200) }; }
  }

  const problems = [];
  const nFT = Object.keys(R.figText).length, nTT = Object.keys(R.textText).length;
  if (nFT) problems.push(['FAIL', `figure/text overlap in ${nFT} place(s)`, Object.keys(R.figText).slice(0, 6)]);
  if (nTT) problems.push(['FAIL', `text over text in ${nTT} place(s)`, Object.keys(R.textText).slice(0, 6)]);
  const nSL = Object.keys(R.svgLabel).length;
  if (nSL) problems.push(['FAIL', `${nSL} label(s) inside a figure cross the figure's own shapes`, Object.keys(R.svgLabel).slice(0, 4)]);
  if (end.overflow) problems.push(['FAIL', 'horizontal overflow']);
  if (errors.length) problems.push(['FAIL', 'page/console errors', errors.slice(0, 4)]);
  if (external.size) problems.push(['FAIL', 'external requests', [...external].slice(0, 4)]);
  const nH = Object.keys(R.hidden).length;
  if (nH) problems.push(['WARN', `${nH} text block(s) near-invisible while in the middle of the screen`, Object.keys(R.hidden).slice(0, 5)]);
  const nB = Object.keys(R.bleed).length;
  if (nB) problems.push(['WARN', `${nB} text block(s) sit over a full-screen background figure: confirm legibility in contact.jpg / screenshots`, Object.keys(R.bleed).slice(0, 3)]);
  if (R.headerThin) problems.push(['WARN', `translucent header with no blur over content at ${R.headerThin} step(s)`]);
  if (Object.keys(R.tiny).length) problems.push(['WARN', 'tiny text', Object.keys(R.tiny).slice(0, 4)]);
  if (S.mobile && Object.keys(R.taps).length) problems.push(['WARN', 'tap targets under 40px', Object.keys(R.taps).slice(0, 4)]);
  if (name !== 'phone-reduced' && R.maxAnims > 14) problems.push(['WARN', `up to ${R.maxAnims} animations running at once (visual burn-out risk)`]);
  if (name === 'phone-reduced' && R.maxAnims > 3) problems.push(['FAIL', `reduced motion still runs ${R.maxAnims} animations`]);
  const first = (end.h1Font || end.bodyFont || '');
  if (first && /^(system-ui|-apple-system|blinkmacsystemfont|sans-serif|serif|georgia|times|arial|helvetica|segoe ui|roboto)/i.test(first) && !end.fonts.some((f) => f.toLowerCase() === first.toLowerCase())) problems.push(['WARN', `headline/body use system font "${first}" (no custom type loaded?)`]);
  if (tok.radii > 6) problems.push(['WARN', `${tok.radii} different corner radii (token sprawl; aim <= 4)`]);
  if (tok.shadows > 5) problems.push(['WARN', `${tok.shadows} different shadows (aim <= 3)`]);
  if (tok.families.length > 3) problems.push(['WARN', `${tok.families.length} font families in use: ${tok.families.join(', ')} (rule: max 2)`]);
  if (tok.colors > 10) problems.push(['WARN', `${tok.colors} distinct text colours (aim <= 6)`]);
  if (motion && !motion.error) {
    if (motion.p95 > 50 || motion.over33 > 20) problems.push(['WARN', `motion under 4x CPU throttle: p95 ${motion.p95}ms, ${motion.over33}% of frames over 33ms, ${motion.longTasks} long tasks (software-rendered headless run: treat as relative, compare before/after)`]);
    if (motion.reached < 90) problems.push(['WARN', `scroll pass only reached ${motion.reached}% of the page in 14 s (heavy frames)`]);
  }
  if (px && !px.error) {
    const cf = Object.entries(px.contrast_fail || {});
    if (cf.length) problems.push([cf.some(([, v]) => v[0] < 2.5) ? 'FAIL' : 'WARN', `contrast below target on the rendered pixels for ${cf.length} text block(s) (ratio vs needed)`, cf.slice(0, 6).map(([k, v]) => `${v[0]} < ${v[1]}  ${k}`)]);
    const mean = (a) => a.length ? a.reduce((x, y) => x + y, 0) / a.length : 0;
    if (mean(px.hues) > 4.5) problems.push(['WARN', `about ${mean(px.hues).toFixed(1)} dominant hues per screen (palette discipline; aim <= 3 plus neutrals)`]);
    if (px.sizes.length > 9) problems.push(['WARN', `${px.sizes.length} distinct font sizes (${px.sizes.join(', ')}); define a scale`]);
    const emptyHigh = px.empty.filter((x) => x > 0.7).length;
    if (emptyHigh > 3) problems.push(['WARN', `${emptyHigh} screens are > 70% empty (dead-space risk; intentional silence or unfinished?)`]);
    if (mean(px.focal) < 0.28) problems.push(['WARN', `low focal dominance (${mean(px.focal).toFixed(2)}): screens may lack one clear focal point`]);
    if (px.sync.some((v) => v > 0.06)) problems.push(['WARN', `scroll state not deterministic: the same position looks different after scrolling away and back (${px.sync.join(', ')}); check scrubbed animations`]);
    if (px.diff) problems.push([px.diff.max > 0.12 ? 'WARN' : 'INFO', `baseline diff: mean ${px.diff.mean}, max ${px.diff.max} over ${px.diff.n} screens`]);
  } else if (px && px.error) problems.push(['WARN', 'pixel analysis failed: ' + px.error]);
  report.profiles[name] = { steps: R.steps, fonts: end.fonts, tokens: tok, motion, pixels: px && !px.error ? { hues: px.hues, empty: px.empty, focal: px.focal, sizes: px.sizes, sync: px.sync, contact: px.contact } : null, problems };
  fails += problems.filter((p) => p[0] === 'FAIL').length;
  console.log(`\n== ${name}: ${R.steps} screens, fonts loaded: ${end.fonts.join(', ') || 'none'}${px && px.contact ? '\n   contact sheet: ' + px.contact : ''}`);
  if (!problems.length) console.log('   clean');
  for (const p of problems) console.log(`   ${p[0]}  ${p[1]}` + (p[2] ? '\n        ' + p[2].join('\n        ') : ''));
}
await browser.close();
fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
console.log(`\n${fails ? 'FAILED' : 'PASSED'}: ${fails} failing check(s). Read <profile>/contact.jpg first, then the individual screenshots. These gates are necessary, not sufficient.`);
process.exit(fails ? 1 : 0);
