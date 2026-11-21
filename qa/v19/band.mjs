import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(4500);
await p.screenshot({ path: 'qa/v19/shots/seal-closed.png' });
const y = await p.evaluate(() => document.querySelector('#shelf-work').getBoundingClientRect().top + scrollY - 70);
await p.evaluate(y => scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(1200); await p.screenshot({ path: 'qa/v19/shots/band.png' });
console.log(await p.evaluate(() => { const e = document.elementFromPoint(200, 20); return e.tagName + '.' + e.className + ' top=' + document.querySelector('.top').getBoundingClientRect().top; }));
await b.close();
