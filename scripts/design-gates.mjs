#!/usr/bin/env node
// Visual-quality gates for any page or scroll experience. Catches what "no console errors" misses:
// figures over text, text over text, translucent header over content, tiny tap targets, tiny text,
// fonts that never loaded, too many things moving at once, text stuck invisible, external requests.
// Also saves screenshots at every scroll step so a human (or Claude) can READ them.
//
//   node scripts/design-gates.mjs <url> <outdir> [--max 60] [--step 0.7] [--stage "css"] [--profiles phone-light,desktop-dark,...]
//
// Profiles: phone-light, phone-dark, phone-reduced, desktop-light, desktop-dark  (default: all five)
// Exit code 1 if any FAIL. Playwright and its Chromium are preinstalled; do not run `playwright install`.
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const url = args[0], out = args[1];
if (!url || !out) { console.error('usage: design-gates.mjs <url> <outdir> [--max N] [--step 0.7] [--stage css] [--profiles a,b]'); process.exit(2); }
const opt = (k, d) => { const i = args.indexOf('--' + k); return i > -1 ? args[i + 1] : d; };
const MAX = +opt('max', 60), STEP = +opt('step', 0.7);
const STAGE = opt('stage', 'canvas, figure, [data-figure], svg[viewBox], video, img');
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

// Runs inside the page. Returns findings for what is currently in the viewport.
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
  // text leaves: elements with their own text and no block children
  const isLeaf = (el) => [...el.children].every((c) => getComputedStyle(c).display.startsWith('inline') || c.tagName === 'BR');
  const texts = [...document.querySelectorAll('p,h1,h2,h3,h4,h5,li,blockquote,figcaption,span,a,button,label,div,td,th')]
    .filter((el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 2) && isLeaf(el))
    .map((el) => ({ el, r: vis(el) })).filter((x) => x.r);
  const figs = [...document.querySelectorAll(stage)].map((el) => ({ el, r: vis(el) }))
    .filter((x) => x.r && x.r.width > 120 && x.r.height > 120 && !x.el.closest('header,nav,footer,button,a'));
  const f = { figText: [], bleed: [], textText: [], hidden: [], header: null, tiny: [], taps: [], anims: 0 };
  for (const t of texts) {
    const area = t.r.width * t.r.height;
    for (const g of figs) {
      if (g.el.contains(t.el) || t.el.contains(g.el)) continue;
      const i = inter(t.r, g.r);
      if (i / area > 0.12) {
        const full = g.r.width * g.r.height > vw * vh * 0.8;           // full-viewport background stage: cannot tell from boxes alone
        (full ? f.bleed : f.figText).push(label(t.el) + '  OVER  ' + label(g.el)); break;
      }
    }
  }
  for (let a = 0; a < texts.length; a++) for (let b = a + 1; b < texts.length; b++) {
    const A = texts[a], B = texts[b];
    if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
    const i = inter(A.r, B.r), m = Math.min(A.r.width * A.r.height, B.r.width * B.r.height);
    if (m > 0 && i / m > 0.25) f.textText.push(label(A.el) + '  OVER  ' + label(B.el));
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
  for (const t of texts) { const fs = parseFloat(getComputedStyle(t.el).fontSize); if (fs < (phone ? 12 : 11)) f.tiny.push(label(t.el) + ' ' + fs + 'px'); }
  if (phone) for (const el of document.querySelectorAll('a,button,input,select,summary,[role=button]')) {
    const r = vis(el); if (r && (r.width < 40 || r.height < 40) && (el.textContent || '').trim().length) f.taps.push(label(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  }
  f.anims = document.getAnimations().filter((a) => a.playState === 'running').length;
  return f;
};

const report = { url, at: new Date().toISOString(), profiles: {} };
let fails = 0;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
for (const name of PROFILES) {
  const S = SPEC[name]; if (!S) continue;
  const ctx = await browser.newContext({ viewport: S.viewport, deviceScaleFactor: S.dsf, isMobile: S.mobile, hasTouch: S.mobile, colorScheme: S.scheme, reducedMotion: S.reduce });
  const page = await ctx.newPage();
  const errors = [], external = new Set();
  page.on('pageerror', (e) => errors.push(String(e).slice(0, 160)));
  page.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights|ERR_FAILED|Failed to load resource/.test(m.text())) errors.push('console: ' + m.text().slice(0, 160)); });
  page.on('response', (r) => { if (r.status() >= 400 && !/cloudflareinsights/.test(r.url())) errors.push(r.status() + ' ' + r.url().slice(0, 100)); });
  page.on('request', (rq) => { const u = rq.url(); if (!u.startsWith(origin) && !u.startsWith('data:') && !u.startsWith('blob:') && !/cloudflareinsights/.test(u)) external.add(u.slice(0, 100)); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(1200);
  const dir = path.join(out, name); fs.mkdirSync(dir, { recursive: true });
  const R = { steps: 0, bleed: {}, hidden: {}, figText: {}, textText: {}, headerThin: 0, headerOver: 0, tiny: {}, taps: {}, maxAnims: 0 };
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  const vh = S.viewport.height; const n = Math.min(MAX, Math.ceil(total / (vh * STEP)));
  const keepAll = name === 'phone-light' || name === 'desktop-light';
  for (let i = 0; i < n; i++) {
    await page.evaluate((y) => scrollTo(0, y), Math.round(i * vh * STEP));
    await page.waitForTimeout(450);
    const f = await page.evaluate(probe, { stage: STAGE, phone: S.mobile });
    R.steps++;
    f.figText.forEach((k) => (R.figText[k] = (R.figText[k] || 0) + 1));
    f.textText.forEach((k) => (R.textText[k] = (R.textText[k] || 0) + 1));
    f.bleed.forEach((k) => (R.bleed[k] = (R.bleed[k] || 0) + 1)); f.hidden.forEach((k) => (R.hidden[k] = (R.hidden[k] || 0) + 1));
    f.tiny.forEach((k) => (R.tiny[k] = 1)); f.taps.forEach((k) => (R.taps[k] = 1));
    if (f.header && f.header.alpha < 0.8 && !f.header.blur && f.headerOver) R.headerThin++;
    R.headerOver += f.headerOver || 0; R.maxAnims = Math.max(R.maxAnims, f.anims);
    if (keepAll || i % 6 === 0) await page.screenshot({ path: path.join(dir, String(i).padStart(3, '0') + '.jpg'), type: 'jpeg', quality: 62 });
  }
  const end = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth > innerWidth + 1,
    stuck: [...document.querySelectorAll('p,h1,h2,h3,li,blockquote')].filter((e) => e.textContent.trim().length > 20 && getComputedStyle(e).display !== 'none' && +getComputedStyle(e).opacity < 0.1 && !e.closest('[hidden],[aria-hidden=true],details:not([open])')).length,
    fonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '')).filter((v, i, a) => a.indexOf(v) === i),
    bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0].replace(/["']/g, '').trim(),
    h1Font: (document.querySelector('h1') ? getComputedStyle(document.querySelector('h1')).fontFamily.split(',')[0].replace(/["']/g, '').trim() : null),
  }));
  const sys = /^(system-ui|-apple-system|blinkmacsystemfont|sans-serif|serif|georgia|times|arial|helvetica|segoe ui|roboto)/i;
  const problems = [];
  const nFT = Object.keys(R.figText).length, nTT = Object.keys(R.textText).length;
  if (nFT) problems.push(['FAIL', `figure/text overlap in ${nFT} place(s)`, Object.keys(R.figText).slice(0, 6)]);
  if (nTT) problems.push(['FAIL', `text over text in ${nTT} place(s)`, Object.keys(R.textText).slice(0, 6)]);
  if (end.overflow) problems.push(['FAIL', 'horizontal overflow']);
  if (errors.length) problems.push(['FAIL', 'page/console errors', errors.slice(0, 4)]);
  if (external.size) problems.push(['FAIL', 'external requests', [...external].slice(0, 4)]);
  const nH = Object.keys(R.hidden).length;
  if (nH) problems.push(['WARN', `${nH} text block(s) near-invisible while in the middle of the screen`, Object.keys(R.hidden).slice(0, 5)]);
  const nB = Object.keys(R.bleed).length;
  if (nB) problems.push(['WARN', `${nB} text block(s) sit over a full-screen background figure: READ the screenshots and confirm the text is legible against what is drawn behind it (use a scrim or move the figure)`, Object.keys(R.bleed).slice(0, 3)]);
  if (R.headerThin) problems.push(['WARN', `translucent header with no blur over content at ${R.headerThin} step(s)`]);
  if (Object.keys(R.tiny).length) problems.push(['WARN', 'tiny text', Object.keys(R.tiny).slice(0, 4)]);
  if (S.mobile && Object.keys(R.taps).length) problems.push(['WARN', 'tap targets under 40px', Object.keys(R.taps).slice(0, 4)]);
  if (name !== 'phone-reduced' && R.maxAnims > 14) problems.push(['WARN', `up to ${R.maxAnims} animations running at once (visual burn-out risk)`]);
  if (name === 'phone-reduced' && R.maxAnims > 3) problems.push(['FAIL', `reduced motion still runs ${R.maxAnims} animations`]);
  const first = (end.h1Font || end.bodyFont || '');
  if (first && sys.test(first) && !end.fonts.some((f) => f.toLowerCase() === first.toLowerCase())) problems.push(['WARN', `headline/body use system font "${first}" (no custom type loaded?)`]);
  report.profiles[name] = { steps: R.steps, fonts: end.fonts, problems };
  fails += problems.filter((p) => p[0] === 'FAIL').length;
  console.log(`\n== ${name}: ${R.steps} screens, fonts loaded: ${end.fonts.join(', ') || 'none'}`);
  if (!problems.length) console.log('   clean');
  for (const p of problems) console.log(`   ${p[0]}  ${p[1]}` + (p[2] ? '\n        ' + p[2].join('\n        ') : ''));
  await ctx.close();
}
await browser.close();
fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
console.log(`\n${fails ? 'FAILED' : 'PASSED'}: ${fails} failing check(s). Screenshots in ${out}/<profile>/NNN.jpg - READ them (Read tool); these gates are necessary, not sufficient.`);
process.exit(fails ? 1 : 0);
