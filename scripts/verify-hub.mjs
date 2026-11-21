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
  // v19: count audio contexts and vibration calls so the checks can see them
  await page.addInitScript(() => {
    window.__ac = 0; window.__vib = 0;
    const A = window.AudioContext; if (A) window.AudioContext = class extends A { constructor(...x) { super(...x); window.__ac++; } };
    navigator.vibrate = () => { window.__vib++; return true; };
  });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  const kb = (await page.evaluate(() => document.documentElement.outerHTML.length)) / 1024;
  kb < 380 ? ok(`homepage HTML ${kb.toFixed(0)} KB (budget 380)`) : fail(`homepage HTML ${kb.toFixed(0)} KB (budget 380)`);

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
    && e.getBoundingClientRect().height > 0 && !e.matches('.pair input, .portal .night, .portal .lamp, .portal .glowpaint, .portal .glint, .tapdemo *, .door .burst, .tool .scan, .tool .glare')).map(e => e.className.baseVal ?? e.className));
  stuck.length ? fail(`${stuck.length} elements stuck invisible after a full scroll: ${stuck.slice(0, 6).join(', ')}`) : ok('nothing stuck invisible after a full scroll');
  const small = await page.evaluate(() => [...document.querySelectorAll('a,button')].filter((e) => { const r = e.getBoundingClientRect(); return r.width && r.height && (r.height < 44 || r.width < 44) && !e.closest('.legal,.skip'); }).map((e) => e.textContent.trim().slice(0, 24)));
  small.length ? fail('tap targets under 44px: ' + small.slice(0, 6).join(' | ')) : ok('every tap target is at least 44px');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  overflow > 1 ? fail(`horizontal overflow ${overflow}px`) : ok('no horizontal overflow');
  // owner 2026-11-21: "ensure that all seo is still intact" (the SEO head is written by scripts/seo/build_site.py: build with sites.json hub.buildCommand)
  const seo = await page.evaluate(() => { const q = (s) => document.querySelector(s); const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map((x) => { try { return JSON.parse(x.textContent); } catch (e) { return null; } });
    return { canonical: q('link[rel=canonical]')?.href, ogImage: q('meta[property="og:image"]')?.content, ogTitle: !!q('meta[property="og:title"]'), twitter: !!q('meta[name="twitter:card"]'), desc: (q('meta[name=description]')?.content || '').length, title: document.title.length, ld: ld.filter(Boolean).length, h1: document.querySelectorAll('h1').length }; });
  seo.canonical === 'https://noblefathercreations.com/' && seo.ogImage && seo.ogTitle && seo.twitter && seo.desc >= 70 && seo.title >= 20 && seo.ld >= 1 && seo.h1 === 1 ? ok('SEO head intact: title, description, canonical, Open Graph, Twitter card, JSON-LD, one h1') : fail('SEO head: ' + JSON.stringify(seo));
  // owner 2026-11-21: "seo that leads as many ways as possible to my books or decoder when people search manipulation or narcissistic abuse"
  const look = await page.$$eval('.lookups a', (a) => a.map((x) => x.getAttribute('href')));
  look.length >= 15 && look.every((h) => /^\/(playbook|topics)/.test(h)) ? ok(`Look up a pattern: ${look.length} links into the Pattern Decoder and Topics`) : fail('lookups: ' + JSON.stringify(look));
  // owner 2026-11-21: "the navigation symbol that was previously on my website still there and can navigate anyone to any other book or page"
  await page.evaluate(() => scrollTo({ top: 0, behavior: 'instant' }));
  await page.click('.nf-seal'); await page.waitForTimeout(500);
  const cat = await page.evaluate(() => { const p = document.querySelector('#nf-panel'); const links = [...p.querySelectorAll('.nf-toc:not(.nf-toc-page) a')].map((a) => a.getAttribute('href'));
    return { open: document.querySelector('.nf-seal').getAttribute('aria-expanded'), n: links.length, all: links.every((h) => /^https:\/\/noblefathercreations\.com\//.test(h)) }; });
  await page.keyboard.press('Escape'); await page.waitForTimeout(400);
  const shut = await page.evaluate(() => document.querySelector('.nf-seal').getAttribute('aria-expanded'));
  cat.open === 'true' && cat.n >= 21 && cat.all && shut === 'false' && page.url().startsWith(url) ? ok(`the seal opens the Catalogue: ${cat.n} books and pages, Escape closes it (and does not leave)`) : fail('seal Catalogue: ' + JSON.stringify({ ...cat, shut }));
  // owner 2026-11-21: "the first thing people see ... doesn't assume they are there for a book": the first screen is the name and four doors
  const first = await page.evaluate(() => { scrollTo({ top: 0, behavior: 'instant' }); const h = document.querySelectorAll('h1'); const t = [...document.querySelectorAll('.door-grid .door-t')].map((a) => [a.textContent.trim(), a.getBoundingClientRect().top < innerHeight]);
    return { h1: h.length === 1 ? h[0].textContent.trim() : h.length, doors: t }; });
  first.h1 === 'Noble Father Creations' && first.doors.length === 4 && first.doors.every((x) => x[1]) ? ok('first screen: the name and four doors (Library, Portals, Listening Room, NFC guide)') : fail('first screen: ' + JSON.stringify(first));
  // owner 2026-11-21: "pull portal pendants from different sets at least so they aren't all the same"
  const sets = await page.$$eval('.portal', (f) => f.map((x) => x.dataset.set || ''));
  const distinct = new Set(sets.filter(Boolean)).size;
  sets.length >= 3 && distinct === sets.length ? ok(`Portals come from ${distinct} different sets`) : fail(`Portals sets not distinct: [${sets.join(', ')}]`);
  // v19 batch 3: the door opens with a press-and-hold for pointers, but keyboard and screen readers open it straight away
  await page.focus('#door-btn'); await page.keyboard.press('Enter'); await page.waitForTimeout(300);
  const kOpen = await page.evaluate(() => document.querySelector('#door').hasAttribute('data-open'));
  await page.keyboard.press('Enter'); await page.waitForTimeout(300);
  const kShut = await page.evaluate(() => !document.querySelector('#door').hasAttribute('data-open'));
  kOpen && kShut ? ok('keyboard opens and closes the bigger-picture door at once') : fail(`door by keyboard: open ${kOpen}, closed again ${kShut}`);
  // v19 foundations (owner 2026-11-21: every effect, made switchable)
  (await page.evaluate(() => window.__ac)) === 0 ? ok('no sound starts without a tap (rule 5)') : fail('an audio context started without a tap');
  await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(300);
  await page.click('#still-btn'); await page.waitForTimeout(400);
  const st = await page.evaluate(() => ({ cls: document.documentElement.classList.contains('is-still'), pressed: document.querySelector('#still-btn').getAttribute('aria-pressed'),
    running: gsap.getTweensOf('.book-in, .book-tilt, .ribbon-track').filter(t => t.isActive() && !t.scrollTrigger).length }));
  st.cls && st.pressed === 'true' && st.running === 0 ? ok('Still stops every self-running effect') : fail('Still did not stop motion: ' + JSON.stringify(st));
  if (w > 900) await page.click('#sound-btn'); else { await page.click('#menu-btn'); await page.waitForTimeout(350); await page.click('#sheet-sound'); }
  await page.waitForTimeout(200);
  const so = await page.evaluate(() => ({ ac: window.__ac, still: document.documentElement.classList.contains('is-still'), pressed: document.querySelector('#sheet-sound').getAttribute('aria-pressed') }));
  so.ac === 1 && !so.still && so.pressed === 'true' ? ok('Sound starts on a tap and lifts Still') : fail('Sound switch: ' + JSON.stringify(so));
  if (w <= 900) { await page.click('#sheet-still'); } else await page.click('#still-btn');
  await page.waitForTimeout(200);
  (await page.evaluate(() => document.querySelector('#sound-btn').getAttribute('aria-pressed'))) === 'false' ? ok('Still also silences sound') : fail('Still left sound on');
  if (w <= 900) { await page.click('#sheet-still'); await page.click('#sheet-close'); } else await page.click('#still-btn');
  await page.waitForTimeout(400);
  errors.length ? fail('console/page errors: ' + errors.slice(0, 3).join(' | ')) : ok('no console or page errors');
  await page.close();
}
await browser.close();
console.log(fails ? `\n${fails} FAILURE(S)` : '\nall checks passed');
process.exit(fails ? 1 : 0);
