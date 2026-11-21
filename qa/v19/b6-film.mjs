// batch 6: phone film of the cover flight, stacking shelves and a page turn (frames at fixed scroll steps)
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const errs = [];
const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3600);
const go = async (y, name) => { await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(500); await p.screenshot({ path: `qa/v19/shots/b6-f-${name}.png` }); };
const heroBottom = await p.evaluate(() => document.querySelector('.hero').getBoundingClientRect().bottom + scrollY);
const H = 844;
const info = [];
for (const [k, f] of [['1', .3], ['2', .45], ['3', .6], ['4', .8]]) {
  const y = Math.round(heroBottom - H * .75 + H * .9 * f);
  await go(y, 'flight-' + k);
  info.push(await p.evaluate(() => ({ ghost: getComputedStyle(document.querySelector('.ghost')).visibility })));
}
const s2 = await p.evaluate(() => document.querySelector('#shelf-work').getBoundingClientRect().top + scrollY);
await go(s2 - 300, 'stack-1'); await go(s2 - 80, 'stack-2');
const t = await p.evaluate(() => document.querySelector('#tools').getBoundingClientRect().top + scrollY);
await go(t - H * .7, 'turn-1'); await go(t - H * .45, 'turn-2');
await b.close(); console.log(JSON.stringify({ info, errs }));
