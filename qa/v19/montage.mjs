// film the opening montage on a phone (frames over time), the settled doors on desktop, and the reduced-motion version
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const errs = [];
const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'domcontentloaded' });
const t0 = Date.now(); const times = [400, 900, 1500, 2200, 2900, 3500, 3900, 4600, 5600];
for (const [k, t] of times.entries()) { const w = t - (Date.now() - t0); if (w > 0) await p.waitForTimeout(w); await p.screenshot({ path: `qa/v19/shots/mt-${k}.png` }); }
const done = await p.evaluate(() => !document.querySelector('.doors').classList.contains('is-montage'));
await ctx.close();
const d = await b.newPage({ viewport: { width: 1440, height: 900 } }); d.on('pageerror', e => errs.push(String(e)));
await d.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await d.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await d.waitForTimeout(6000); await d.screenshot({ path: 'qa/v19/shots/mt-desktop.png' });
const rm = await b.newContext({ ...devices['iPhone 13'], reducedMotion: 'reduce' }); const q = await rm.newPage();
await q.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await q.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await q.waitForTimeout(500); await q.screenshot({ path: 'qa/v19/shots/mt-reduced.png' });
await b.close(); console.log(JSON.stringify({ done, errs }));
