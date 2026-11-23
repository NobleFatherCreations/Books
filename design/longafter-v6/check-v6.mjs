// Guards for "v6 fix round 1 (critic)" in library/longafter/DESIGN-STATE.md.
// Needs scripts/seo/serve.py on :8765.  NODE_PATH="$(npm root -g)" node design/longafter-v6/check-v6.mjs
import { createRequire } from 'module';
import { readFileSync } from 'fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const U = 'http://127.0.0.1:8765/longafter/';
const PLAN = JSON.parse(readFileSync(new URL('../../content/longafter-v2/plan.json', import.meta.url)));
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };

// colour maths
const hex = h => { h = h.trim().replace('#', ''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255); };
const lin = c => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const lum = rgb => { const [r, g, b] = rgb.map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const oklch = rgb => {
  const [r, g, b] = rgb.map(lin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
  return [L, Math.hypot(A, B), (Math.atan2(B, A) * 180 / Math.PI + 360) % 360];
};
const mix = (a, b, t) => a.map((v, i) => v * (1 - t) + b[i] * t);   // color-mix(in srgb, a (1-t), b t)

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: 'dark', isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(e.message));
const dockTop = () => p.evaluate(() => document.querySelector('.dock').getBoundingClientRect().top);

// 1. dock fully opaque
await p.goto(U + 'the-trauma-bond');
const dockBg = await p.evaluate(() => getComputedStyle(document.querySelector('.dock')).backgroundColor);
const alpha = /rgba/.test(dockBg) ? parseFloat(dockBg.split(',')[3]) : 1;
ok(alpha === 1, `1 dock background alpha is 1 (${dockBg})`);
ok(await p.evaluate(() => document.querySelectorAll('.bar .leave, .dock .leave').length === 2), '1 both phone Leave buttons present (bar + dock)');

// 2. decoder Copy above the dock when the reply is scrolled into view (every reply on the decoder pages)
let worst = Infinity, n2 = 0;
for (const s of ['co-parenting-or-parallel-parenting', 'family-court-honestly', 'grey-rock-and-written-only-contact', 'handovers', 'hoovering',
  'messages-you-dont-have-to-answer', 'the-narrative-campaign', 'when-they-say-youre-the-abuser', 'words-you-can-use', 'your-day-in-court']) {
  await p.goto(U + s);
  const count = await p.locator('.dv-reply').count();
  for (let i = 0; i < count; i++) {
    const r = await p.evaluate(i => {
      const e = document.querySelectorAll('.dv-reply')[i]; e.scrollIntoView({ block: 'end' });
      const b = e.querySelector('.dv-copy').getBoundingClientRect(), d = document.querySelector('.dock').getBoundingClientRect();
      return d.top - b.bottom;
    }, i);
    worst = Math.min(worst, r); n2++;
  }
}
ok(n2 > 0 && worst >= 0, `2 Copy button fully above the dock on ${n2} replies (worst gap ${worst.toFixed(1)}px)`);

// 3. checklists are real checkboxes, 44px hit area, no ☐, nothing stored
await p.goto(U + 'court-day-checklist');
const c3 = await p.evaluate(() => {
  const lis = [...document.querySelectorAll('ul.checks li')];
  const bad = lis.filter(li => { const l = li.querySelector('label'), i = l && l.querySelector('input[type=checkbox]'); return !i || l.getBoundingClientRect().height < 44 || l.getBoundingClientRect().width < 44; });
  return { n: lis.length, bad: bad.length, box: document.body.innerText.includes('☐') };
});
ok(c3.n > 0 && c3.bad === 0, `3 ${c3.n} checklist lines are labelled checkboxes with >=44px hit area (${c3.bad} bad)`);
ok(!c3.box, '3 no ☐ in the rendered text');
const url0 = p.url();
if (!(await p.locator('ul.checks input[type=checkbox]').count())) { ok(false, '3 no checkboxes to tick: skipping the tick, print and storage checks'); } else {
const boxes = p.locator('ul.checks input[type=checkbox]');
await boxes.nth(0).scrollIntoViewIfNeeded(); await p.locator('ul.checks label').nth(0).tap(); await boxes.nth(2).check();
ok(await boxes.nth(0).isChecked() && await boxes.nth(2).isChecked(), '3 tapping a line ticks its box');
await p.locator('.dock [data-mode-toggle]').click(); await p.locator('.dock [data-mode-toggle]').click();
await p.locator('.tools [data-discreet]').click(); await p.locator('.tools [data-discreet]').click();
const st = await p.evaluate(() => [localStorage.length, sessionStorage.length, document.cookie]);
const ck = await ctx.cookies();
ok(st[0] === 0 && st[1] === 0 && st[2] === '' && ck.length === 0 && p.url() === url0,
  `3 after ticking and toggles: localStorage ${st[0]}, sessionStorage ${st[1]}, cookies "${st[2]}"/${ck.length}, URL unchanged`);
await p.emulateMedia({ media: 'print' });
const printed = await p.evaluate(() => { const i = document.querySelector('ul.checks input:checked'), cs = getComputedStyle(i, null);
  return { bg: cs.backgroundImage, border: cs.borderTopWidth }; });
ok(printed.bg === 'none' && parseFloat(printed.border) > 0, `3 print shows an empty box even when ticked (${JSON.stringify(printed)})`);
await p.emulateMedia({ media: 'screen' });
await p.reload();
ok(!(await boxes.nth(0).isChecked()), '3 ticks reset on reload (memory only)');
}

// 4. ruled lines pitched from the computed line-height
for (const vw of [390, 1440]) {
  await p.setViewportSize({ width: vw, height: 900 });
  await p.goto(U + 'the-trauma-bond');
  const r = await p.evaluate(() => [...document.querySelectorAll('article .blk-action p')].map(e => {
    const cs = getComputedStyle(e), t = document.createElement('i'); t.style.cssText = 'display:block;height:1lh'; e.appendChild(t);
    const lh = t.getBoundingClientRect().height; t.remove();
    return { lh, css: parseFloat(cs.lineHeight), img: cs.backgroundImage !== 'none', size: cs.backgroundSize };
  }));
  ok(r.length && r.every(x => x.img && Math.abs(x.lh - x.css) < 0.5 && /1lh|px/.test(x.size)), `4 at ${vw}px rules on each step paragraph, pitch = line-height ${r[0] && r[0].css}px (${r[0] && r[0].size})`);
}
await p.setViewportSize({ width: 390, height: 844 });

// 5. hour signature: link contrast >= 4.5 on every part, neighbouring accents differ, sky text AA
const parts = PLAN.parts.filter(x => /^[ivx]+$/.test(x.id));
const accs = [];
for (const part of parts) {
  await p.goto(U + part.chapters[0]);
  const v = await p.evaluate(() => { const cs = getComputedStyle(document.documentElement), b = getComputedStyle(document.body);
    const rgb = s => s.match(/\d+/g).slice(0, 3).map(Number).map(x => x.toString(16).padStart(2, '0')).join('');
    const a = document.querySelector('article a:not(.tel)'), loc = document.querySelector('.loc a'), by = document.querySelector('.by');
    return { acc: cs.getPropertyValue('--acc'), s1: cs.getPropertyValue('--s1'), s2: cs.getPropertyValue('--s2'), bg: rgb(b.backgroundColor),
      link: a ? rgb(getComputedStyle(a).color) : null, sky: [loc, by, document.querySelector('.sky h1'), document.querySelector('.sky .q')].filter(Boolean).map(e => rgb(getComputedStyle(e).color)) }; });
  const bg = hex(v.bg), link = hex(v.link || v.acc), s2 = hex(v.s2), bottom = mix(s2, hex(v.acc), 0.22);
  const cl = contrast(link, bg);
  const skyMin = Math.min(...v.sky.flatMap(c => [contrast(hex(c), hex(v.s1)), contrast(hex(c), s2), contrast(hex(c), bottom)]));
  ok(cl >= 4.5, `5 Part ${part.id.toUpperCase()} link ${v.link} on page ${v.bg}: ${cl.toFixed(2)}:1`);
  ok(skyMin >= 4.5, `5 Part ${part.id.toUpperCase()} sky text on ${v.s1}->${v.s2.trim()} (and accent foot): min ${skyMin.toFixed(2)}:1`);
  accs.push([part.id, v.acc.trim(), oklch(hex(v.acc))]);
}
for (let i = 1; i < accs.length; i++) {
  const [a, b] = [accs[i - 1][2], accs[i][2]];
  const dh = Math.abs(b[2] - a[2]), dl = Math.abs(b[0] - a[0]);
  ok(dh >= 4 || dl >= 0.03, `5 accent ${accs[i - 1][0]}->${accs[i][0]} (${accs[i - 1][1]}->${accs[i][1]}): hue step ${dh.toFixed(1)}deg, lightness step ${dl.toFixed(3)}`);
}

// 6. short answer above the dock on first load, every chapter page
const slugs = PLAN.chapters.map(c => c.slug);
const late = [];
for (const s of slugs) {
  await p.goto(U + s);
  const r = await p.evaluate(() => { const sh = document.querySelector('.short'), d = document.querySelector('.dock');
    return sh && d ? d.getBoundingClientRect().top - sh.getBoundingClientRect().top : null; });
  if (r !== null && r <= 0) late.push(`${s} (${r.toFixed(0)}px)`);
}
const tops = [];
for (const s of ['the-trauma-bond', 'family-court-honestly', 'court-day-checklist', 'money-from-zero', 'leaving-was-the-middle']) {
  await p.goto(U + s);
  tops.push([s, await p.evaluate(() => document.querySelector('.short').getBoundingClientRect().top)]);
}
ok(tops.every(t => t[1] <= 422), '6 compact header: short answer starts in the top half of the screen (<=422px): ' + tops.map(t => t[0] + ' ' + t[1].toFixed(0)).join(', '));
ok(late.length === 0, `6 short answer top above the dock at 390x844 on all ${slugs.length} pages` + (late.length ? `; late on ${late.length}: ${late.slice(0, 8).join(', ')}` : ''));

ok(errs.length === 0, 'no page errors ' + errs.slice(0, 3).join(' | '));
await browser.close();
console.log(fails ? `${fails} FAILED` : 'ALL PASS');
process.exit(fails ? 1 : 0);
