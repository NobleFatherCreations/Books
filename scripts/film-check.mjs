#!/usr/bin/env node
// FILM CHECK: plays a scroll film the way a thumb does and FAILS on the faults a person would report.
// It exists because screenshots and static gates passed builds whose motion was broken on a real phone.
//   node scripts/film-check.mjs <url> [--click=#begin] [--vp=390x844] [--rm] [--speed=26] [--json=out.json]
// The page must expose window.__film() (see design/fractal2/redesign/v9/template.html): numbers describing what is on screen.
// Checks (each one is a real defect an owner reported, turned into a test):
//   errors        no page errors, failed requests or sideways overflow
//   round         the picture is not stretched (canvas pixel aspect = its CSS aspect), also after a toolbar-sized height change
//   toolbar       a browser toolbar sliding in or out does not move or rescale the picture
//   smooth        the camera never jumps: the scripted zoom per screen of scroll and the per-frame move of the center stay under limits
//   pace          moving captions travel at the reader's scroll speed (never faster), and stay readable long enough at Play speed
//   reveal        every caption shows all of its words, and stays complete for at least 38% of a screen of scroll
//   once          nothing plays twice: every caption and every sequence item (sector name, list line) is on screen in ONE unbroken stretch
//   flicker       the picture's brightness does not pump up and down with every caption
//   end           the end is reachable, the page is not locked there, and scrolling back up works
//   budget        no per-element compositor layers; picture canvases are no bigger than the screen
import { createRequire } from 'module'; import fs from 'fs';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const [, , url, ...rest] = process.argv; const o = Object.fromEntries(rest.map((a) => { const m = a.match(/^--([a-z]+)(?:=(.*))?$/); return [m[1], m[2] ?? '1']; }));
const [vw, vh] = (o.vp || '390x844').split('x').map(Number); const STEP = +(o.speed || 26); const mob = vw < 700;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: mob ? 3 : 1, isMobile: mob, hasTouch: mob, reducedMotion: o.rm ? 'reduce' : 'no-preference' });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights/.test(m.text())) errs.push(m.text()); });
p.on('response', (r) => { if (r.status() >= 400 && !/cloudflareinsights/.test(r.url())) errs.push(r.status() + ' ' + r.url()); });
await p.goto(url, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' }); await p.waitForTimeout(800);
if (o.click) { await p.click(o.click); await p.waitForTimeout(1800); }
const R = []; const add = (name, ok, detail) => R.push({ name, ok, detail });
const film = () => p.evaluate(() => window.__film && window.__film());
if (!(await film())) { console.log('FILM CHECK FAIL: the page does not expose window.__film()'); process.exit(1); }
const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
const atRest = async () => { for (let i = 0; i < 50; i++) { await p.waitForTimeout(150); const f = await film(); if (f.settled && Math.abs(Math.log(f.z / f.tz)) < 0.002) return f; } return film(); };
const aspectOK = (f) => Math.abs((f.artBuf[0] / f.artBuf[1]) / (f.artCss[0] / f.artCss[1]) - 1) < 0.01;
// --- round + toolbar ---
await p.evaluate((y) => scrollTo(0, y), Math.round(H * 0.3)); const f0 = await atRest();
await p.setViewportSize({ width: vw, height: vh - 84 }); await p.waitForTimeout(500); const f1 = await atRest();
await p.setViewportSize({ width: vw, height: vh }); await p.waitForTimeout(500); const f2 = await atRest();
add('round', aspectOK(f0) && aspectOK(f1) && aspectOK(f2), `canvas ${f0.artBuf.join('x')} shown at ${f0.artCss.join('x')}; after toolbar change ${f1.artBuf.join('x')} at ${f1.artCss.join('x')}`);
add('toolbar', Math.abs(f1.cy - f0.cy) < 2 && Math.abs(f1.cx - f0.cx) < 2 && Math.abs(Math.log(f1.z / f0.z)) < 0.01, `center moved ${(f1.cy - f0.cy).toFixed(1)}px, scale ${f0.z.toFixed(3)} -> ${f1.z.toFixed(3)} when the viewport lost 84px`);
// --- one continuous pass at thumb speed, sampled every frame, inside the page ---
await p.evaluate(() => scrollTo(0, 0)); await atRest();   // start the pass from rest, or leftovers of the previous test are counted as a replay
const pass = await p.evaluate(async (STEP) => {
  const H = document.documentElement.scrollHeight - innerHeight; const out = { frames: 0, worstT: 0, atT: 0, worstZ: 0, atZ: 0, worstC: 0, atC: 0, caps: {}, seq: {}, opSwings: 0, maxLayers: 0, lagMax: 0 };
  let prev = null, lastOpDir = 0, lastOpExt = null;
  await new Promise((res) => { let y = 0; const tick = () => { y = Math.min(H, y + STEP); scrollTo(0, y); const f = window.__film(); out.frames++;
    if (prev) { const dz = Math.abs(Math.log(f.z / prev.z)), dc = Math.hypot(f.cx - prev.cx, f.cy - prev.cy); if (dz > out.worstZ) { out.worstZ = dz; out.atZ = y; } const dt = Math.abs(Math.log(f.tz / prev.tz)) / Math.max(1, f.y - prev.y) * innerHeight; if (dt > out.worstT) { out.worstT = dt; out.atT = y; } if (dc > out.worstC) { out.worstC = dc; out.atC = y; }
      const dop = f.op - prev.op; if (Math.abs(dop) > 0.004) { const dir = Math.sign(dop); if (lastOpExt === null) lastOpExt = prev.op; if (dir !== lastOpDir && lastOpDir !== 0) { if (Math.abs(prev.op - lastOpExt) > 0.2) out.opSwings++; lastOpExt = prev.op; } lastOpDir = dir; } }
    out.lagMax = Math.max(out.lagMax, Math.abs(Math.log(f.z / f.tz))); out.maxLayers = Math.max(out.maxLayers, f.layers);
    for (const c of f.caps) { const k = c.i; const r = out.caps[k] || (out.caps[k] = { hold: c.hold, of: c.of, h: c.h, runs: 0, last: -9, maxShown: 0, firstTop: c.top, firstY: y, lastTop: c.top, lastY: y, fullAtTop: null });
      if (r.last !== out.frames - 1) r.runs++; r.last = out.frames; r.maxShown = Math.max(r.maxShown, c.shown); r.lastTop = c.top; r.lastY = y; if (c.shown === c.of && r.fullAtTop === null) r.fullAtTop = c.top; if (c.shown === c.of) r.fullY = (r.fullY || 0) + (prev ? Math.max(0, f.y - prev.y) : 0); }
    for (const kind of ['sec', 'inw', 'orig']) for (const i of f.seq[kind]) { const k = kind + ':' + i; const r = out.seq[k] || (out.seq[k] = { runs: 0, last: -9 }); if (r.last !== out.frames - 1) r.runs++; r.last = out.frames; }
    prev = f; if (y >= H) res(); else requestAnimationFrame(tick); }; requestAnimationFrame(tick); });
  return out; }, STEP);
const CLIM = Math.max(16, 0.017 * Math.max(vw, vh));   // a slide of the whole picture may cover at most 1.7% of the screen per frame
const screensPerSec = STEP * 60 / vh;
// the scripted camera is judged per screen of scroll (deterministic); the rendered frames are judged for jumps of the picture's center
add('smooth', pass.worstT <= 2.4 && pass.worstC <= CLIM, `fastest scripted zoom ${pass.worstT.toFixed(2)}x-log per screen of scroll (limit 2.4) at ${(100 * pass.atT / H).toFixed(1)}%; largest one-frame center move ${pass.worstC.toFixed(1)}px (limit ${CLIM.toFixed(0)}) at ${(100 * pass.atC / H).toFixed(1)}%; at ${screensPerSec.toFixed(1)} screens/s the largest rendered one-frame scale change was ${(pass.worstZ * 100).toFixed(1)}%`);
const caps = Object.entries(pass.caps); const moving = caps.filter(([, c]) => !c.hold);
const fast = moving.map(([k, c]) => [k, c.lastY === c.firstY ? 1 : Math.abs((c.lastTop - c.firstTop) / (c.lastY - c.firstY))]).filter(([, r]) => r > 1.06);
const PLAY = 0.115 * vh; const shortRead = moving.filter(([, c]) => c.fullAtTop !== null && ((c.fullAtTop + c.h) / PLAY) < 1.2 + c.of * 0.26);
add('pace', fast.length === 0 && shortRead.length === 0, fast.length ? `${fast.length} caption(s) move faster than the scroll (worst ${Math.max(...fast.map((x) => x[1])).toFixed(2)}x), first #${fast[0][0]}` : shortRead.length ? `${shortRead.length} caption(s) leave too soon to read at Play speed, first #${shortRead[0][0]}` : `${moving.length} moving captions travel at scroll speed; all readable at Play speed`);
const unrevealed = caps.filter(([, c]) => c.maxShown < c.of);
const brief = caps.filter(([, c]) => !c.hold && (c.fullY || 0) < 0.38 * vh);
add('reveal', unrevealed.length === 0 && brief.length === 0, brief.length && !unrevealed.length ? `${brief.length} caption(s) are complete for less than 38% of a screen of scroll, first #${brief[0][0]} (${Math.round(brief[0][1].fullY || 0)}px)` : unrevealed.length ? `${unrevealed.length} caption(s) never showed all their words, first #${unrevealed[0][0]} (${unrevealed[0][1].maxShown}/${unrevealed[0][1].of})` : `all ${caps.length} captions showed every word`);
const twiceC = caps.filter(([, c]) => c.runs > 1), twiceS = Object.entries(pass.seq).filter(([, s]) => s.runs > 1);
add('once', twiceC.length === 0 && twiceS.length === 0, twiceC.length || twiceS.length ? `appeared more than once: ${[...twiceC.map(([k]) => 'caption #' + k), ...twiceS.map(([k]) => k)].slice(0, 6).join(', ')}` : `${caps.length} captions and ${Object.keys(pass.seq).length} sequence items each appeared once`);
add('flicker', pass.opSwings <= 10, `picture brightness reversed direction ${pass.opSwings} time(s) by more than 20% (limit 10; captions number ${caps.length})`);
// --- end: reachable, unlocked, can go back ---
await p.waitForTimeout(600); const fe = await film(); const yEnd = fe.y;
if (mob) { await p.mouse.move(vw / 2, vh / 2); } await p.mouse.wheel(0, -900); await p.waitForTimeout(500); const yBack = (await film()).y;
add('end', yEnd >= H - 4 && !fe.locked && yBack < yEnd - 300, `reached ${Math.round(yEnd)}/${Math.round(H)}; scrolled back up by ${Math.round(yEnd - yBack)}px`);
// --- settle: after stopping anywhere, the camera arrives where the script says ---
let settleBad = 0; for (const q of [0.12, 0.37, 0.61, 0.9]) { await p.evaluate((y) => scrollTo(0, y), Math.round(H * q)); await p.waitForTimeout(1500); const f = await film(); if (Math.abs(Math.log(f.z / f.tz)) > 0.01) settleBad++; }
add('settle', settleBad === 0, settleBad ? `${settleBad} of 4 stops did not settle on the scripted camera` : 'camera settles on the scripted position at 4 stops');
const over = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
add('errors', errs.length === 0 && !over, errs.length ? errs.slice(0, 3).join(' | ') : over ? 'sideways overflow' : 'no page errors, failed requests or sideways overflow');
const cv = await p.evaluate(() => [...document.querySelectorAll('canvas')].map((c) => c.width * c.height)); const screenPx = vw * vh * 4;
add('budget', pass.maxLayers === 0 && cv.every((n) => n <= screenPx * 1.05), `${pass.maxLayers} forced layers; ${cv.length} canvases, largest ${(Math.max(...cv) / 1e6).toFixed(1)} MP (screen at 2x = ${(screenPx / 1e6).toFixed(1)} MP)`);
await b.close();
const fails = R.filter((r) => !r.ok); const tag = `${vw}x${vh}${o.rm ? ' reduced-motion' : ''}`;
for (const r of R) console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name.padEnd(8)} ${r.detail}`);
console.log(fails.length ? `FILM CHECK FAIL (${fails.length}) [${tag}, ${(H / vh).toFixed(0)} screens, ${pass.frames} frames]` : `FILM CHECK PASS [${tag}, ${(H / vh).toFixed(0)} screens, ${pass.frames} frames]`);
if (o.json) fs.writeFileSync(o.json, JSON.stringify({ url, tag, results: R, pass }, null, 1));
process.exit(fails.length ? 1 : 0);
