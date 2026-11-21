// screenshot the three opening-screen comps at iPhone 13 size
import { chromium, devices } from 'playwright';
const b = await chromium.launch();
for (const n of ['a', 'b', 'c']) {
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 2 }); const p = await ctx.newPage();
  await p.goto(`http://127.0.0.1:8765/_undeployed/hub-v19-comps/${n}`, { waitUntil: 'networkidle' }); await p.waitForTimeout(400);
  await p.screenshot({ path: `qa/v19/shots/comp-${n}.png` }); await ctx.close();
}
await b.close();
