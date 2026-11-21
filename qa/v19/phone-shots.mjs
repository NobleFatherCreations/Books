// Phone-first frames (390x844, touch): shelf carousel mid-swipe, Portals row from six sets, a painted glow, tools light band, a section title rising.
import { chromium, devices } from 'playwright';
const out = 'qa/v19/shots';
const b = await chromium.launch();
const ctx = await b.newContext({ ...devices['iPhone 13'] });
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
const shots = [];
const snap = async n => { const f = `${out}/ph-${n}.png`; await p.screenshot({ path: f }); shots.push(f); };
await p.evaluate(() => document.querySelector('#shelf-close').scrollIntoView({ block: 'start' })); await p.waitForTimeout(1200);
await p.evaluate(() => { const u = document.querySelector('#shelf-close .books'); u.scrollLeft = u.clientWidth * .3; }); await p.waitForTimeout(400); await snap('1-shelf-swipe');
await p.evaluate(() => { const h = document.querySelector('#tools .sec-head'); scrollTo(0, h.getBoundingClientRect().top + scrollY - 500); }); await p.waitForTimeout(150); await snap('2-title-rise');
await p.evaluate(() => { const t = document.querySelector('.tool-playbook'); scrollTo(0, t.getBoundingClientRect().top + scrollY - 380); }); await p.waitForTimeout(700); await snap('3-tools-band');
await p.evaluate(() => document.querySelector('.workshop h3').scrollIntoView({ block: 'start' })); await p.waitForTimeout(1200);
await p.evaluate(() => scrollBy(0, -60)); await p.waitForTimeout(400); await snap('4-portals');
await p.evaluate(() => { const u = document.querySelector('.pairs'); u.scrollLeft = u.clientWidth * .45; }); await p.waitForTimeout(500); await snap('5-portals-swipe');
// press and hold the pendant in front, then let go
const figs = await p.$$('.portal'); let target = figs[0];
for (const f of figs) { const bb = await f.boundingBox(); if (bb && bb.x > 0 && bb.x < 200) { target = f; break; } }
const bb = await target.boundingBox();
const cdp = await ctx.newCDPSession(p);
const pt = { x: Math.round(bb.x + bb.width / 2), y: Math.round(bb.y + bb.height / 2) };
await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [pt] }); await p.waitForTimeout(1400);
await snap('6-charging');
await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(700); await snap('7-glow');
await b.close();
console.log(JSON.stringify({ n: shots.length, errs }));
