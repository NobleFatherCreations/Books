// v19 batch 2: hero frames. Usage: node qa/v19/b2-shots.mjs  -> qa/v19/shots/b2-*.png + b2-contact.jpg
import { chromium } from 'playwright';
const out = 'qa/v19/shots';
const b = await chromium.launch();
const errs = [];
const open = async (w, h, opts = {}) => {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: opts.rm ? 'reduce' : 'no-preference', hasTouch: !!opts.touch, isMobile: !!opts.touch });
  p.on('pageerror', e => errs.push(String(e)));
  if (opts.night) await p.addInitScript(() => { Date.prototype.getHours = () => 23; });
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'domcontentloaded' });
  return p;
};
const shots = [];
const snap = async (p, name) => { const f = `${out}/b2-${name}.png`; await p.screenshot({ path: f }); shots.push(f); };
let p = await open(1440, 900);
await p.waitForTimeout(550); await snap(p, '1-ink-0.55s');
await p.waitForTimeout(450); await snap(p, '2-ink-1.0s');
await p.waitForTimeout(2600); await snap(p, '3-rest');
await p.click('.chip[data-s="close"]'); await p.waitForTimeout(330); await snap(p, '4-riffle');
await p.waitForTimeout(260); await snap(p, '5-deal');
await p.waitForTimeout(1500); await snap(p, '6-answer');
// drag the cover open
await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(600);
const bk = await (await p.$('.book3d')).boundingBox();
await p.mouse.move(bk.x + bk.width * .8, bk.y + bk.height / 2); await p.mouse.down();
await p.mouse.move(bk.x + bk.width * .1, bk.y + bk.height / 2, { steps: 8 }); await p.waitForTimeout(350); await snap(p, '7-peek');
await p.mouse.up(); await p.close();
p = await open(1440, 900, { night: true }); await p.waitForTimeout(3600); await snap(p, '8-after-dark');
await p.close();
p = await open(390, 844, { touch: true }); await p.waitForTimeout(3600); await snap(p, '9-phone');
await p.tap('.chip[data-s="close"]'); await p.waitForTimeout(340); await snap(p, '10-phone-riffle'); await p.waitForTimeout(1800); await snap(p, '11-phone-answer');
await p.close();
p = await open(390, 844, { touch: true, rm: true }); await p.waitForTimeout(600); await snap(p, '12-phone-reduced');
await p.close();
await b.close();
console.log(JSON.stringify({ shots: shots.length, errs }));
