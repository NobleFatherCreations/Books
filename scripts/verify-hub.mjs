// Homepage v18 checks (owner-reported faults become checks first: docs/hub-redesign/REGRESSIONS.md).
// Usage: node scripts/verify-hub.mjs http://127.0.0.1:8765/   (serve with: python3 scripts/seo/serve.py 8765)
import { chromium } from 'playwright';

const url = process.argv[2] || 'http://127.0.0.1:8765/';
let fails = 0;
const ok = (m) => console.log('  ok   ', m);
const fail = (m) => { fails++; console.log('  FAIL ', m); };
const ANCHORS = ['start-here', 'library', 'instruments', 'tools', 'music', 'workshop', 'art', 'guide', 'support', 'manifesto', 'maker'];

const browser = await chromium.launch();
for (const [name, w, h] of [['375', 375, 812], ['1440', 1440, 900]]) {
  console.log(`== ${name}px ==`);
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  // The Cloudflare beacon can't report from a local test address; that is expected and fine on the real domain.
  page.on('console', (m) => { if (m.type() === 'error' && !/cloudflareinsights|net::ERR_FAILED|api\/visits/.test(m.text())) errors.push(m.text()); });
  await page.route('**/api/visits', (r) => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  const kb = (await page.evaluate(() => document.documentElement.outerHTML.length)) / 1024;
  kb < 260 ? ok(`homepage HTML ${kb.toFixed(0)} KB`) : fail(`homepage HTML ${kb.toFixed(0)} KB (budget 260)`);

  const missing = await page.evaluate((ids) => ids.filter((i) => !document.getElementById(i)), ANCHORS);
  missing.length ? fail('old anchors missing: ' + missing.join(' ')) : ok('every old anchor still resolves');

  (await page.$('#updates')) ? fail('version/update notes are on the homepage') : ok('no version/update notes (owner 2026-11-20)');
  (await page.$('#nf-visits')) ? ok('visit counter present') : fail('visit counter missing');
  (await page.$('script[src*="cloudflareinsights.com/beacon"]')) ? ok('Cloudflare beacon present') : fail('Cloudflare beacon missing');

  const ext = await page.evaluate(() => [...document.querySelectorAll('script[src],link[rel~="stylesheet"],link[rel~="preload"],link[rel~="icon"],img[src],audio[src],video[src],source[src]')]
    .map((e) => e.src || e.href).filter((u) => /^https?:/.test(u) && !u.startsWith(location.origin) && !/cloudflareinsights/.test(u)));
  ext.length ? fail('outside requests: ' + ext.join(' ')) : ok('no outside requests besides the beacon');

  // Fault 2026-11-20: book covers cut off at the left and right edges
  const cropped = await page.evaluate(() => [...document.querySelectorAll('.bk img,.pick img,.tool img,#hero-cover')].filter((i) => i.naturalWidth)
    .filter((i) => { const bw = i.offsetWidth, bh = i.offsetHeight; return bw && Math.abs(bw / bh - i.naturalWidth / i.naturalHeight) > 0.02; })
    .map((i) => i.src.split('/').pop()));
  cropped.length ? fail('covers cropped: ' + cropped.join(' ')) : ok('every cover shows whole (frame matches the image)');

  // Owner: someone looking for one book must not meet the bigger-picture books by default
  const bigVisible = await page.evaluate(() => { const b = document.querySelector('#door-body'); return b.getBoundingClientRect().height > 2 || !b.inert; });
  bigVisible ? fail('bigger-picture books visible before the door is opened') : ok('bigger-picture books stay behind the door');

  // Fault 2026-11-21: NFC guide must come before the Press and the Casting; no pendant pictures on those two
  const order = await page.$$eval('.wk-row > *', (els) => els.map((e) => e.querySelector('h3')?.textContent));
  order[0] === 'How to Program NFC Tags' ? ok('NFC guide card comes first in the Workshop row') : fail('Workshop row order: ' + order.join(', '));
  const soonImgs = await page.$$eval('.card.soon img', (els) => els.length);
  soonImgs ? fail('Press/Casting cards show a picture (should be their own icons)') : ok('Press and Casting use their own icons, no pendant pictures');

  // nav: every top item scrolls on this page (the NFC trip passes the other sections)
  const nav = await page.$$eval('.nav a', (els) => els.map((e) => e.getAttribute('href')));
  nav.every((h) => h.startsWith('#')) ? ok('top navigation stays on the page: ' + nav.join(' ')) : fail('nav leaves the page: ' + nav.join(' '));

  const sheetFocusable = await page.evaluate(() => { const s = document.querySelector('#sheet'); return getComputedStyle(s).display !== 'none' && !s.hasAttribute('data-open'); });
  sheetFocusable ? fail('closed phone menu is still in the tab order') : ok('closed phone menu is out of the tab order');

  await page.click('.chip[data-s="close"]'); await page.waitForTimeout(700);
  const picks = await page.$$eval('#result-grid .pick', (e) => e.length);
  picks === 3 ? ok('an answer shows two books and a tool') : fail(`answer shows ${picks} picks`);

  const H = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += h * 0.7) { await page.evaluate((y) => scrollTo(0, y), y); await page.waitForTimeout(90); }
  await page.waitForTimeout(700);
  const stuck = await page.evaluate(() => [...document.querySelectorAll('main *')].filter((e) => getComputedStyle(e).opacity === '0'
    && e.getBoundingClientRect().height > 0 && !e.matches('.pair input, .portal .night, .portal .lamp')).length);
  stuck ? fail(`${stuck} elements stuck invisible after a full scroll`) : ok('nothing stuck invisible after a full scroll');
  const small = await page.evaluate(() => [...document.querySelectorAll('a,button')].filter((e) => { const r = e.getBoundingClientRect(); return r.width && r.height && (r.height < 44 || r.width < 44) && !e.closest('.legal,.skip'); }).map((e) => e.textContent.trim().slice(0, 24)));
  small.length ? fail('tap targets under 44px: ' + small.slice(0, 6).join(' | ')) : ok('every tap target is at least 44px');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  overflow > 1 ? fail(`horizontal overflow ${overflow}px`) : ok('no horizontal overflow');
  errors.length ? fail('console/page errors: ' + errors.slice(0, 3).join(' | ')) : ok('no console or page errors');
  await page.close();
}
await browser.close();
console.log(fails ? `\n${fails} FAILURE(S)` : '\nall checks passed');
process.exit(fails ? 1 : 0);
