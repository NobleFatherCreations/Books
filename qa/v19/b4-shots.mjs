// v19 batch 4: threshold burn frames, painted glow on a Portal, sparks, lights off, UV lamp. Usage: node qa/v19/b4-shots.mjs
import { chromium } from 'playwright';
const out = 'qa/v19/shots';
const b = await chromium.launch();
const errs = [];
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
const ty = await p.evaluate(() => document.querySelector('.threshold').getBoundingClientRect().top + scrollY);
const shots = [];
for (const [i, off] of [[1, -700], [2, -450], [3, -200], [4, 100]]) {
  await p.evaluate(y => scrollTo(0, y), ty + off); await p.waitForTimeout(700);
  const f = `${out}/b4-${i}-burn.png`; await p.screenshot({ path: f }); shots.push(f);
}
// paint a stroke of light across the first pendant, then let go
const fig = await p.$('.portal'); await fig.scrollIntoViewIfNeeded(); await p.evaluate(() => scrollBy(0, 150)); await p.waitForTimeout(600);
const bx = await fig.boundingBox();
await p.mouse.move(bx.x + bx.width * .3, bx.y + bx.height * .35); await p.mouse.down();
await p.mouse.move(bx.x + bx.width * .6, bx.y + bx.height * .55, { steps: 20 }); await p.waitForTimeout(250);
await p.screenshot({ path: `${out}/b4-5-charging.png` });
await p.mouse.up(); await p.waitForTimeout(450);
await p.screenshot({ path: `${out}/b4-6-painted-glow.png` });
for (let i = 0; i < 14; i++) await p.mouse.move(bx.x + bx.width * (.3 + i * .03), bx.y + bx.height * (.4 + Math.sin(i) * .1));
await p.waitForTimeout(80); await p.screenshot({ path: `${out}/b4-7-sparks.png` });
// full charge on the second pendant -> lights off
await p.waitForTimeout(7000);
const f2 = (await p.$$('.portal'))[1]; const b2 = await f2.boundingBox();
await p.mouse.move(b2.x + b2.width / 2, b2.y + b2.height / 2); await p.mouse.down(); await p.waitForTimeout(1500); await p.mouse.up(); await p.waitForTimeout(900);
await p.screenshot({ path: `${out}/b4-8-lights-off.png` });
const veil = await p.evaluate(() => getComputedStyle(document.querySelector('.veil')).opacity);
// UV lamp passing over the third pendant, then leaving it
await p.waitForTimeout(4000);
const f3 = (await p.$$('.portal'))[2]; const b3 = await f3.boundingBox();
for (let i = 0; i <= 20; i++) await p.mouse.move(b3.x + b3.width * (.15 + i * .035), b3.y + b3.height * (.5 + Math.sin(i / 3) * .2));
await p.waitForTimeout(150); await p.screenshot({ path: `${out}/b4-9-uv.png` });
await p.mouse.move(b3.x + b3.width / 2, b3.y + b3.height + 140); await p.waitForTimeout(500);
await p.screenshot({ path: `${out}/b4-10-uv-glow.png` });
await b.close();
console.log(JSON.stringify({ veil, errs }));
