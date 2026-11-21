import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(5000);
console.log(await p.evaluate(() => [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.left < 12 && r.top < 12 && r.width > 0 && r.width < 200 && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'; }).map(e => e.tagName + '.' + (e.className.baseVal ?? e.className) + ' ' + Math.round(e.getBoundingClientRect().width))));
await b.close();
