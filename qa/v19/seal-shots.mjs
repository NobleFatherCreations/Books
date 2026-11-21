// the seal and the Catalogue on a phone: closed (bottom corner) and open
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(4500);
await p.screenshot({ path: 'qa/v19/shots/seal-closed.png' });
await p.evaluate(() => document.querySelector('#shelf-work').scrollIntoView()); await p.waitForTimeout(600); await p.screenshot({ path: 'qa/v19/shots/seal-scrolled.png' });
await p.tap('.nf-seal'); await p.waitForTimeout(700); await p.screenshot({ path: 'qa/v19/shots/seal-open.png' });
await p.evaluate(() => document.querySelector('#nf-panel').scrollTo(0, 99999)); await p.waitForTimeout(300); await p.screenshot({ path: 'qa/v19/shots/seal-open-end.png' });
await b.close(); console.log(JSON.stringify(errs));
