// first-screen fit: where the last answer chip ends at common phone sizes (must be inside the screen)
import { chromium, devices } from 'playwright';
const b = await chromium.launch(); const out = {};
for (const [n, d] of [['iPhone 13', devices['iPhone 13']], ['iPhone SE', devices['iPhone SE']], ['Pixel 7', devices['Pixel 7']], ['iPhone 15 Pro Max', devices['iPhone 15 Pro Max'] || devices['iPhone 14 Pro Max']]]) {
  const ctx = await b.newContext(d); const p = await ctx.newPage();
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3000);
  out[n] = await p.evaluate(() => { const c = [...document.querySelectorAll('.chip')].pop().getBoundingClientRect(); const bk = document.querySelector('.book3d').getBoundingClientRect(); return { screen: innerHeight, lastChipBottom: Math.round(c.bottom), bookW: Math.round(bk.width) }; });
  await ctx.close();
}
await b.close(); console.log(JSON.stringify(out));
