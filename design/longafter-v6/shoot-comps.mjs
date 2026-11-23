// Phone screenshots of the v6 comps (375x812, dark, DSF 2). Needs serve-comps.py on :8766.
// NODE_PATH="$(npm root -g)" node design/longafter-v6/shoot-comps.mjs
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8766/design/longafter-v6/comps';
const OUT = new URL('./comps/shots/', import.meta.url).pathname;
export const SHOTS = [
  ['index', 'top', null], ['index', 'choices', 'section[aria-labelledby="w-h"]'],
  ['the-trauma-bond', 'top', null], ['the-trauma-bond', 'scene', '.blk-scene'],
  ['the-trauma-bond', 'honest', '.blk-honest'], ['the-trauma-bond', 'action', '.blk-action'],
  ['family-court-honestly', 'decoder', '.blk-decoder'], ['family-court-honestly', 'honest', '.blk-honest'],
  ['court-day-checklist', 'top', null], ['court-day-checklist', 'sheet', '.blk-sheet'],
  ['abuse-or-a-hard-breakup', 'bridge', '.blk-bridge'],
];
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, colorScheme: 'dark', isMobile: true, hasTouch: true });
const page = await ctx.newPage();
const errs = [];
page.on('pageerror', e => errs.push(e.message));
page.on('request', r => { const u = r.url(); if (!u.startsWith('http://127.0.0.1') && !u.startsWith('data:') && !u.includes('cloudflareinsights.com')) errs.push('external: ' + u); });
for (const v of ['a', 'b', 'c']) {
  for (const [p, name, sel] of SHOTS) {
    await page.goto(`${BASE}/${v}/${p}.html`, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    const ow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
    if (ow) errs.push(`overflow ${v}/${p}`);
    if (sel) await page.evaluate(s => { const e = document.querySelector(s); scrollTo(0, e.getBoundingClientRect().top + scrollY - (s.startsWith('section') ? 70 : 110)); }, sel);
    else await page.evaluate(() => scrollTo(0, 0));
    await page.waitForTimeout(150);
    await page.screenshot({ path: `${OUT}${v}-${p}-${name}.png` });
  }
}
console.log(errs.length ? errs.join('\n') : 'no errors, no external requests, no overflow');
await browser.close();
