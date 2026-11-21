// v19 batch 1 screenshots: header switches at desktop and phone, the phone menu with Still and Sound.
import { chromium } from 'playwright';
const out = process.argv[2] || 'qa/v19/shots';
const b = await chromium.launch();
const shot = async (w, h, name, fn) => {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(2600);
  if (fn) await fn(p);
  await p.screenshot({ path: `${out}/${name}.png`, clip: { x: 0, y: 0, width: w, height: name === 'm-sheet' ? h : Math.min(h, 520) } });
  await p.close();
};
await shot(1440, 900, 'd-header');
await shot(1440, 900, 'd-still-sound', async p => { await p.click('#sound-btn'); await p.waitForTimeout(300); await p.hover('#still-btn'); });
await shot(1440, 900, 'd-night', async p => { await p.evaluate(() => document.querySelector('.workshop').scrollIntoView()); await p.waitForTimeout(800); await p.click('#sound-btn'); await p.waitForTimeout(300); });
await shot(390, 844, 'm-header');
await shot(390, 844, 'm-sheet', async p => { await p.click('#menu-btn'); await p.waitForTimeout(400); await p.click('#sheet-sound'); await p.waitForTimeout(300); });
await b.close();
