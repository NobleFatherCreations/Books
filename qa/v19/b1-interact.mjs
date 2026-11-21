// v19 batch 1: portal charge with sound on (hum + haptics), then Leave silences first. Usage: node qa/v19/b1-interact.mjs
import { chromium } from 'playwright';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, hasTouch: false });
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.addInitScript(() => {
  window.__vib = []; navigator.vibrate = x => { window.__vib.push(x); return true; };
  window.__osc = 0; const A = window.AudioContext;
  window.AudioContext = class extends A { constructor(...a) { super(...a); window.__ctx = this; const o = this.createOscillator.bind(this); this.createOscillator = () => { window.__osc++; return o(); }; } };
});
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.route('https://www.google.com/**', r => r.fulfill({ contentType: 'text/html', body: 'left' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' });
await p.click('#sound-btn');
const fig = await p.$('.portal'); await fig.scrollIntoViewIfNeeded(); await p.waitForTimeout(500);
const bx = await fig.boundingBox();
await p.mouse.move(bx.x + bx.width / 2, bx.y + bx.height / 2); await p.mouse.down(); await p.waitForTimeout(1500);
const mid = await p.evaluate(() => ({ osc: window.__osc, vib: window.__vib.length, state: window.__ctx && window.__ctx.state }));
await p.mouse.up(); await p.waitForTimeout(600);
const after = await p.evaluate(() => ({ osc: window.__osc, glowing: document.querySelector('.portal').classList.contains('is-glowing') }));
await p.evaluate(() => scrollTo(0, 0));
await p.click('[data-leave]'); await p.waitForTimeout(800);
console.log(JSON.stringify({ mid, after, url: p.url(), errs }));
await b.close();
