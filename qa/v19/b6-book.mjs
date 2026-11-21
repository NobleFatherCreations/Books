// batch 6.1: close-ups of the hero book (phone + desktop, at rest and part-scrolled)
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const errs = [];
for (const [name, opts] of [['d', { viewport: { width: 1440, height: 900 } }], ['m', { ...devices['iPhone 13'] }]]) {
  const ctx = await b.newContext(opts); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(String(e)));
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3600);
  const shot = async n => { const r = await (await p.$('.stage')).boundingBox(); await p.screenshot({ path: `qa/v19/shots/b6-book-${name}-${n}.png`, clip: { x: r.x, y: Math.max(0, r.y), width: r.width, height: r.height } }); };
  await shot('rest');
  await p.evaluate(() => scrollTo({ top: innerHeight * .25, behavior: 'instant' })); await p.waitForTimeout(900); await shot('scroll');
  await ctx.close();
}
await b.close(); console.log(JSON.stringify({ errs }));
