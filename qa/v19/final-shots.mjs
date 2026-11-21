// final round shots: the wax seal, the Look up a pattern block (phone), the Catalogue open
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(4500);
await p.screenshot({ path: 'qa/v19/shots/fin-1-doors.png' });
const s = await p.$('.nf-seal'); await s.screenshot({ path: 'qa/v19/shots/fin-seal.png' });
await p.evaluate(() => { const e = document.querySelector('#lookup'); scrollTo({ top: e.getBoundingClientRect().top + scrollY - 80, behavior: 'instant' }); }); await p.waitForTimeout(800);
await p.screenshot({ path: 'qa/v19/shots/fin-2-lookup.png' });
await p.tap('.nf-seal'); await p.waitForTimeout(700); await p.screenshot({ path: 'qa/v19/shots/fin-3-catalogue.png' });
await b.close(); console.log(JSON.stringify(errs));
