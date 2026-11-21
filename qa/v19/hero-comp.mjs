// two phone first screens side by side: A = now (question on the first screen), B = big book (cover ~60% wide, question just below)
import { chromium, devices } from 'playwright';
const b = await chromium.launch();
const shots = [];
for (const [n, css] of [['A', ''], ['B', '@media (max-width:900px){.stage{--bw:min(58vw,240px)!important;height:auto!important;min-height:calc(var(--bw) * 1.62);padding:24px 0 8px}.halo{width:min(96vw,420px)!important}.hero h1{font-size:40px!important}}']]) {
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 2 }); const p = await ctx.newPage();
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
  if (css) await p.addStyleTag({ content: css + ' .book3d{width:var(--bw)!important}' });
  await p.waitForTimeout(3600);
  const f = `qa/v19/shots/hero-${n}.png`; await p.screenshot({ path: f }); shots.push(f); await ctx.close();
}
await b.close();
