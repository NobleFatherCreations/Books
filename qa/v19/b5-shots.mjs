// v19 batch 5 (phone first): NFC tap demo, stamp + pour, counter roll, signature, back to the light, glow secret.
import { chromium, devices } from 'playwright';
const out = 'qa/v19/shots';
const b = await chromium.launch();
const ctx = await b.newContext({ ...devices['iPhone 13'] });
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
const res = {};
const snap = async n => p.screenshot({ path: `${out}/b5-${n}.png` });
const to = async (sel, off = 0) => { await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - o, behavior: 'instant' }); }, [sel, off]); };
await to('.card.guide', 120); await p.waitForTimeout(700); await snap('1-tap');
await p.waitForTimeout(500); await snap('2-tap-rings');
await to('.making', 300); await p.waitForTimeout(650); await snap('3-making');
// the counter only fills on the real domain: fill it the same way the counter script does, then watch it roll
await to('footer', 200); await p.waitForTimeout(300);
await p.evaluate(() => { const e = document.getElementById('nf-visits'); e.textContent = '1,284 visits to Noble Father Creations'; e.hidden = false; });
await p.evaluate(() => { const e = document.getElementById('nf-visits'); window.scrollTo({ top: e.getBoundingClientRect().top + scrollY - 500, behavior: 'instant' }); });
await p.waitForTimeout(250); await snap('4-counter-rolling');
await p.waitForTimeout(1800); await snap('5-counter');
res.counterLabel = await p.evaluate(() => document.getElementById('nf-visits').getAttribute('aria-label'));
await to('footer', 300); await p.waitForTimeout(600); await snap('6-footer');
// glow secret by three taps on "Alive in the dark."
await to('.threshold', 0); await p.waitForTimeout(600);
const gl = await (await p.$('.glowline')).boundingBox();
for (let i = 0; i < 3; i++) { await p.touchscreen.tap(gl.x + 40, gl.y + gl.height / 2); await p.waitForTimeout(120); }
await p.waitForTimeout(1500); await snap('7-glow-secret');
res.eggOpacity = await p.evaluate(() => getComputedStyle(document.querySelector('.egg')).opacity);
// back to the light
await p.waitForTimeout(3500);
await to('footer', 0); await p.waitForTimeout(400);
await p.tap('#up'); await p.waitForTimeout(1600);
res.backToTopY = await p.evaluate(() => Math.round(scrollY));
await b.close();
console.log(JSON.stringify({ res, errs }));
