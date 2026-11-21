import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(4500);
await p.evaluate(() => document.querySelector('#shelf-work').scrollIntoView()); await p.waitForTimeout(800);
console.log(await p.evaluate(() => ({ top: document.querySelector('.top').getBoundingClientRect().top, y: scrollY, vv: visualViewport.offsetTop })));
await b.close();
