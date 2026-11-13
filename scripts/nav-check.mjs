#!/usr/bin/env node
// NAV CHECK: for multi-page sites. Visits a set of pages on phone and desktop and FAILS on navigation faults a person would hit.
//   node scripts/nav-check.mjs <origin> <path> [<path> ...] [--rm]
// Checks per page: no errors or failed requests; no sideways overflow; a section nav is visible (dock on phone, bar on desktop) with
// exactly one current item or none; every nav and ring link resolves (HTTP 200); tap targets in the nav are at least 44px; the fixed
// dock does not cover the end of the page or the Leave button; the ring (if present) has 8 named links and answers the keyboard;
// with reduced motion nothing keeps moving; headings exist and h1 is single; display font actually loaded.
import { createRequire } from 'module'; const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const args = process.argv.slice(2); const rm = args.includes('--rm'); const [origin, ...paths] = args.filter((a) => !a.startsWith('--'));
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }); let fails = 0; const seen = new Map();
const ok200 = async (ctx, u) => { if (!seen.has(u)) { const r = await ctx.request.get(u).catch(() => null); seen.set(u, r ? r.status() : 0); } return seen.get(u); };
for (const [tag, w, h, mob] of [['phone', 390, 844, true], ['desktop', 1440, 900, false]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mob, hasTouch: mob, colorScheme: 'dark', reducedMotion: rm ? 'reduce' : 'no-preference' });
  for (const path of paths) { const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('response', (r) => { if (r.status() >= 400 && !/cloudflareinsights/.test(r.url())) errs.push(r.status() + ' ' + r.url()); });
    await p.goto(origin + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(rm ? 300 : 1500);
    const r = await p.evaluate((mob) => { const vis = (e) => { if (!e) return false; const s = getComputedStyle(e), q = e.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && q.width > 0 && q.height > 0; };
      const nav = [...document.querySelectorAll('.dock,.snav')].find(vis); const links = nav ? [...nav.querySelectorAll('a')] : [];
      const small = links.filter((a) => { const q = a.getBoundingClientRect(); return q.height < 44 || q.width < 44; }).length;
      const ring = [...document.querySelectorAll('.ring')].find(vis); const rl = ring ? [...ring.querySelectorAll('a.rb')] : [];
      const leave = document.getElementById('leave'), dock = document.querySelector('.dock'); let covers = false;
      if (vis(dock) && leave) { const a = dock.getBoundingClientRect(), c = leave.getBoundingClientRect(); covers = !(c.bottom <= a.top || c.top >= a.bottom); }
      scrollTo(0, document.documentElement.scrollHeight); const last = document.querySelector('footer.foot'); const lq = last ? last.getBoundingClientRect() : null; const dq = vis(dock) ? dock.getBoundingClientRect() : null;
      const hidden = lq && dq ? lq.bottom > dq.top + 2 : false; scrollTo(0, 0);
      const moving = document.getAnimations().filter((a) => a.playState === 'running' && (a.effect?.getComputedTiming().iterations === Infinity)).length;
      return { nav: !!nav, links: links.map((a) => a.href), cur: nav ? nav.querySelectorAll('[aria-current]').length : -1, small, ring: !!ring, ringLinks: rl.map((a) => new URL(a.getAttribute("href"), location.href).href), ringNamed: rl.filter((a) => (a.getAttribute('aria-label') || '').length > 8).length,
        over: document.documentElement.scrollWidth > innerWidth + 1, covers, hidden, moving, h1: document.querySelectorAll('h1').length, font: document.fonts.check('40px Voice') }; }, mob);
    const bad = []; if (errs.length) bad.push('errors: ' + errs.slice(0, 2).join(' | ')); if (r.over) bad.push('sideways overflow'); if (!r.nav) bad.push('no section nav visible'); if (r.cur > 1) bad.push(r.cur + ' current items');
    if (r.small) bad.push(r.small + ' nav targets under 44px'); if (r.covers) bad.push('dock covers Leave'); if (r.hidden) bad.push('dock hides the end of the page'); if (r.h1 !== 1) bad.push(r.h1 + ' h1'); if (!r.font) bad.push('display font not loaded');
    if (r.ring && (r.ringLinks.length !== 8 || r.ringNamed !== 8)) bad.push('ring has ' + r.ringLinks.length + ' links, ' + r.ringNamed + ' named'); if (rm && r.moving) bad.push(r.moving + ' endless animations under reduced motion');
    for (const u of [...new Set([...r.links, ...r.ringLinks])]) { const s = await ok200(ctx, u); if (s !== 200) bad.push(s + ' ' + u); }
    if (r.ring) { await p.focus('.ring a.rb'); const lab = await p.evaluate(() => document.querySelector('.ring .rc-l').textContent); if (/stages/i.test(lab) && !(await p.evaluate(() => document.querySelector('.ring').classList.contains('has-cur')))) bad.push('ring does not answer keyboard focus'); }
    if (bad.length) { fails++; console.log(`FAIL  ${tag.padEnd(7)} ${path}  ${bad.join('; ')}`); } await p.close(); }
  await ctx.close(); }
await b.close(); console.log(fails ? `NAV CHECK FAIL (${fails})` : `NAV CHECK PASS [${paths.length} pages x phone+desktop${rm ? ', reduced motion' : ''}]`); process.exit(fails ? 1 : 0);
