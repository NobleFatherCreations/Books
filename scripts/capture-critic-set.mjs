#!/usr/bin/env node
// Standard capture set for independent critics, so scores are comparable between rounds.
//   node scripts/capture-critic-set.mjs <url> <outdir>
// Writes: phone-00..15.jpg (390x844 @2x, evenly spaced), desk-00..15.jpg (1440x900), and, for every element with class "beat" or [data-critic-beat],
// beat-<n>-0..4.jpg on desktop. Waits for the camera to settle at each stop. Same positions every run.
import { createRequire } from 'module'; import fs from 'fs';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const [, , url, out] = process.argv; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
for (const [pre, vp, mob, dpr] of [['phone', { width: 390, height: 844 }, true, 2], ['desk', { width: 1440, height: 900 }, false, 1]]) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dpr, isMobile: mob, hasTouch: mob }); const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' }); await p.waitForTimeout(1500);
  const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  for (let i = 0; i < 16; i++) { await p.evaluate((v) => scrollTo(0, v), Math.round(H * i / 15)); await p.waitForTimeout(1300); await p.screenshot({ path: `${out}/${pre}-${String(i).padStart(2, '0')}.jpg`, type: 'jpeg', quality: 78 }); }
  if (pre === 'desk') {
    const beats = await p.evaluate(() => [...document.querySelectorAll('.beat,[data-critic-beat]')].map((e) => { const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.height)]; }));
    for (let n = 0; n < beats.length; n++) for (let k = 0; k < 5; k++) { await p.evaluate((v) => scrollTo(0, Math.max(0, v)), Math.round(beats[n][0] - 450 + beats[n][1] * k / 4)); await p.waitForTimeout(1300); await p.screenshot({ path: `${out}/beat-${n}-${k}.jpg`, type: 'jpeg', quality: 78 }); }
  }
  await ctx.close();
}
await b.close(); console.log('captured to', out);
