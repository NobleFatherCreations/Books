import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(4000);
console.log(await p.evaluate(() => ({ html: document.querySelector('h1').innerHTML.slice(0, 300), col: [...document.querySelectorAll('h1 *')].slice(0, 8).map(e => getComputedStyle(e).color + ' ' + getComputedStyle(e).opacity) })));
await b.close();
