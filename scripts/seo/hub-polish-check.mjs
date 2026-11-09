// Phone check for the homepage polish fixes: before (hub/_before.html) vs after (/), 375px, touch.
// Usage: node scripts/seo/hub-polish-check.mjs <shots-dir>   (needs scripts/seo/serve.py on :8765)
import { chromium } from 'playwright';
const OUT = process.argv[2] || '_work';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [tag, url] of [['before', 'http://127.0.0.1:8765/_before.html'], ['after', 'http://127.0.0.1:8765/']]) {
  const c = await b.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, colorScheme: 'dark', hasTouch: true, isMobile: true });
  const p = await c.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const r = {};
  r.heroOpacity = await p.$eval('.st-hero-inner', (e) => getComputedStyle(e).opacity);
  r.colophonOpacity = await p.$$eval('.st-colophon li', (ls) => ls.map((l) => getComputedStyle(l).opacity).join(','));
  r.music = await p.$eval('#npToggle', (m) => [m.getAttribute('aria-label'), m.dataset.playing || '-'].join(' | '));
  await p.screenshot({ path: `${OUT}/${tag}-01-hero.png` });
  await p.tap('.topnav a[href="#start-here"]'); await p.waitForTimeout(1200);
  r.startH = await p.$eval('#start-h', (e) => Math.round(e.getBoundingClientRect().top));
  r.mastH = await p.$eval('.masthead', (e) => Math.round(e.getBoundingClientRect().height));
  r.current = await p.$$eval('.topnav a[aria-current]', (l) => l.map((a) => a.textContent).join(','));
  await p.screenshot({ path: `${OUT}/${tag}-02-start.png` });
  const s = await p.$$('#start-here > .wrap > details > summary');
  await s[0].tap(); await p.waitForTimeout(400); await s[1].tap(); await p.waitForTimeout(600);
  r.openTop = await p.$$eval('#start-here > .wrap > details[open]', (l) => l.length);
  await p.screenshot({ path: `${OUT}/${tag}-03-start-open.png` });
  await p.evaluate(() => document.querySelector('#music').scrollIntoView()); await p.waitForTimeout(1200);
  r.currentAtMusic = await p.$$eval('.topnav a[aria-current]', (l) => l.map((a) => a.textContent).join(','));
  r.navScroll = await p.$eval('.masthead .topnav', (n) => Math.round(n.scrollLeft));
  r.mastHScrolled = await p.$eval('.masthead', (e) => Math.round(e.getBoundingClientRect().height));
  await p.screenshot({ path: `${OUT}/${tag}-04-music.png` });
  await p.tap('#npToggle', { force: true }).catch(() => {}); await p.waitForTimeout(500);
  r.musicAfterTap = await p.$eval('#npToggle', (m) => [m.getAttribute('aria-label'), m.dataset.playing || '-'].join(' | '));
  r.errors = errs.length;
  console.log(tag, JSON.stringify(r));
  await c.close();
}
const c = await b.newContext({ viewport: { width: 375, height: 812 }, reducedMotion: 'reduce' }); const p = await c.newPage();
await p.goto('http://127.0.0.1:8765/'); await p.waitForTimeout(800);
console.log('reduced-motion', await p.$eval('.st-hero-inner', (e) => getComputedStyle(e).opacity), await p.$eval('.st-hero-video', (e) => getComputedStyle(e).display));
await b.close();
