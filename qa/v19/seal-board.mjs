// storyboard frames for the seal opening (iPhone 13)
import { chromium, devices } from 'playwright';
const b = await chromium.launch();
for (const f of [0, 1, 2]) {
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 2 }); const p = await ctx.newPage();
  await p.goto(`http://127.0.0.1:8765/_undeployed/hub-v19-comps/seal?f=${f}`, { waitUntil: 'networkidle' }); await p.waitForTimeout(300);
  await p.screenshot({ path: `qa/v19/shots/seal-${f}.png` }); await ctx.close();
}
await b.close();
