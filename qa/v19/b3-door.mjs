// v19 batch 3: film the door swing (frames every 120 ms after the hold completes)
import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
const db = await p.$('#door-btn'); await db.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
await p.evaluate(() => document.querySelector('#door').scrollIntoView({ block: 'center' })); await p.waitForTimeout(500);
const bb = await db.boundingBox();
await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await p.mouse.down(); await p.waitForTimeout(720);
const info = [];
for (let i = 0; i < 6; i++) {
  info.push(await p.evaluate(() => { const l = document.querySelector('.door-l'), w = document.querySelector('.leafs'); const r = l.getBoundingClientRect(); return { vis: getComputedStyle(w).visibility, t: getComputedStyle(l).transform.slice(0, 40), w: Math.round(r.width), h: Math.round(r.height) }; }));
  await p.screenshot({ path: `qa/v19/shots/b3-swing-${i}.png`, clip: { x: 0, y: Math.max(0, bb.y - 260), width: 1440, height: 520 } });
  await p.waitForTimeout(120);
}
await p.mouse.up();
console.log(JSON.stringify(info));
await b.close();
