// batch 6.3: a mouse-wheel notch glides (scroll arrives over several frames), trackpad-sized deltas stay native, keys still work
import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
await p.mouse.move(700, 500);
await p.mouse.wheel(0, 300);
const t = [];
for (let i = 0; i < 8; i++) { t.push(await p.evaluate(() => Math.round(scrollY))); await p.waitForTimeout(50); }
await p.waitForTimeout(800); const end = await p.evaluate(() => Math.round(scrollY));
await p.mouse.wheel(0, 20); await p.waitForTimeout(100); const pad = await p.evaluate(() => Math.round(scrollY));
await p.keyboard.press('End'); await p.waitForTimeout(1500); const endKey = await p.evaluate(() => Math.round(scrollY + innerHeight - document.documentElement.scrollHeight));
console.log(JSON.stringify({ frames: t, end, afterSmallDelta: pad, endKeyGap: endKey }));
await b.close();
