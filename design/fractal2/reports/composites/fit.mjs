// Scales each fittable section's type so it fills 1 or 2 whole pages, then prints. Usage: node fit.mjs in.html out.pdf [safety]
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { pathToFileURL } from 'node:url'; import { resolve } from 'node:path';
const [inp, out, safetyArg] = process.argv.slice(2);
const SAFETY = Number(safetyArg || 0.93);
const b = await chromium.launch(); const p = await b.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto(pathToFileURL(resolve(inp)).href, { waitUntil: 'networkidle' });
await p.emulateMedia({ media: 'print' });
await p.evaluate(() => document.fonts.ready);
const report = await p.evaluate((SAFETY) => {
  // Letter 8.5x11in minus margins (.78in sides, .72 top, .82 bottom) at 96 px/in
  const W = (8.5 - 1.56) * 96, H = (11 - 1.54) * 96;
  document.body.style.width = W + 'px';
  const secs = [...document.querySelectorAll('.sec.fit')];
  const meas = (el, s) => { el.style.setProperty('--s', s); return el.getBoundingClientRect().height / H; };
  const res = [];
  for (const el of secs) {
    const scene = el.classList.contains('scene');
    const lo = scene ? 0.92 : 0.9, hi = 1.32;
    const SAF = el.classList.contains('cut') ? 0.89 : SAFETY;
    const h1 = meas(el, 1);
    let T;
    if (h1 <= 1.05) T = 1; else { const n = Math.ceil(h1); const f = h1 - (n - 1); T = f < 0.45 ? n - 1 : n; }
    if (meas(el, lo) > T * SAF) T += 1;
    let a = lo, z = hi;
    for (let i = 0; i < 18; i++) { const m = (a + z) / 2; if (meas(el, m) <= T * SAF) a = m; else z = m; }
    el.style.setProperty('--s', a.toFixed(3));
    res.push([el.dataset.id, T, +a.toFixed(3), +(meas(el, a) / T).toFixed(2)]);
  }
  document.body.style.width = '';
  return res;
}, SAFETY);
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close();
console.log(JSON.stringify(report)); if (errs.length) console.error(errs);
