// v19 batch 3: door hold behaviour + frames of shelves, door, tools, header. Usage: node qa/v19/b3-shots.mjs
import { chromium } from 'playwright';
const out = 'qa/v19/shots';
const b = await chromium.launch();
const errs = [], res = {};
const open = async (w, h, opts = {}) => {
  const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: opts.rm ? 'reduce' : 'no-preference', hasTouch: !!opts.touch, isMobile: !!opts.touch });
  p.on('pageerror', e => errs.push(String(e)));
  await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(400);
  return p;
};
const isOpen = p => p.evaluate(() => document.querySelector('#door').hasAttribute('data-open'));
const shots = [];
const snap = async (p, name, el) => { const f = `${out}/b3-${name}.png`; if (el) await (await p.$(el)).screenshot({ path: f }); else await p.screenshot({ path: f }); shots.push(f); };

let p = await open(1440, 900);
// header reading line + nav marker part way down
await p.evaluate(() => document.querySelector('#shelf-work').scrollIntoView({ block: 'center' })); await p.waitForTimeout(900);
const s1 = await (await p.$('#shelf-work')).boundingBox();
await p.mouse.move(s1.x + s1.width * .55, s1.y + s1.height * .5); await p.waitForTimeout(500);
await snap(p, '1-shelf-hover');
await p.mouse.move(5, 5);
// door: a short tap must not open, a hold must, a tap closes, keyboard opens straight away
const db = await p.$('#door-btn'); await db.scrollIntoViewIfNeeded(); await p.waitForTimeout(1600);
await snap(p, '2-door-shut');
const bb = await db.boundingBox(); const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
await p.mouse.move(cx, cy); await p.mouse.down(); await p.waitForTimeout(150); await p.mouse.up(); await p.waitForTimeout(300);
res.shortTapOpens = await isOpen(p);
await p.mouse.down(); await p.waitForTimeout(400); await snap(p, '3-door-holding', '#door');
await p.waitForTimeout(450); await p.mouse.up(); await p.waitForTimeout(250); await snap(p, '4-door-swing');
res.holdOpens = await isOpen(p);
await p.waitForTimeout(1200); await snap(p, '5-door-open');
await p.mouse.click(cx, cy); await p.waitForTimeout(500); res.tapCloses = !(await isOpen(p));
await db.focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(300); res.keyOpens = await isOpen(p);
await p.keyboard.press('Enter'); await p.waitForTimeout(300); res.keyCloses = !(await isOpen(p));
// tools: hover tilt + decoder scan
const tl = await p.$('.tool-playbook'); await tl.scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
const tb = await tl.boundingBox(); await p.mouse.move(tb.x + tb.width * .75, tb.y + tb.height * .3); await p.waitForTimeout(500);
await snap(p, '6-tools', '#tools');
await p.close();
p = await open(390, 844, { touch: true });
await p.evaluate(() => document.querySelector('#shelf-close').scrollIntoView({ block: 'start' })); await p.waitForTimeout(1400); await snap(p, '7-phone-shelf');
await p.evaluate(() => document.querySelector('#door').scrollIntoView({ block: 'center' })); await p.waitForTimeout(1200); await snap(p, '8-phone-door');
await p.close();
await b.close();
console.log(JSON.stringify({ res, errs }));
