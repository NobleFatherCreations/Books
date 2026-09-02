/**
 * Render check for the hub after a reorder.
 *
 * The hub opens on a gate that blocks scrolling until a door is chosen, so
 * every check below picks a door first -- otherwise it would be testing the
 * entrance and reporting on the house.
 *
 * Usage: node scripts/verify-hub.mjs [file-or-url]
 */
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const target = process.argv[2] ||
  'file://' + path.join(HERE, '..', 'hub', 'catalogue-redesign.html');

const EXPECTED_SECTIONS = ['workshop', 'library', 'instruments', 'music', 'guide',
                           'maker', 'support'];
const EXPECTED_BOOKS = [
  'The Festie Bible', 'The Festie Codex', 'The Sovereign Divine Feminine',
  'Playground Protectors', 'The Fractal', 'The Fracture', 'The Loop',
  'The Weighing', 'The Sacred Divide', 'The Silence', 'At Will',
  'The Slow Take', 'The Long After', 'The Repair',
];

let failures = 0;
const fail = (m) => { failures++; console.log('  FAIL  ' + m); };
const ok = (m) => console.log('  ok    ' + m);

// Outbound HTTPS here goes through an agent proxy that Chromium does not
// read from the environment, so pass it through explicitly.
//
// Heads up: in the Claude Code remote container this still does not get you
// to the open internet -- both the `proxy` option and --proxy-server end in
// ERR_CONNECTION_RESET, so a live-URL run of this script cannot work there.
// That is the environment, not the site. Verify live by curl'ing the page
// and diffing it against the repo file, then run this against the repo file;
// they are the same bytes, so the render is the same render.
const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium',
  ...(proxy && target.startsWith('http')
    ? { proxy: { server: proxy, bypass: process.env.NO_PROXY || '' } }
    : {}),
  args: ['--ignore-certificate-errors'],
});

for (const width of [375, 1440]) {
  console.log(`\n== ${width}px ==`);
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: 'dark' });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  await page.goto(target, { waitUntil: 'load' });
  await page.waitForTimeout(1200);

  // The gate: three doors, in the new order, with the corrected words.
  const doors = await page.$$eval('.st-portal', (els) => els.map((e) => ({
    href: e.getAttribute('href'),
    word: e.querySelector('.pg-label b')?.textContent,
    name: e.querySelector('.pg-label span')?.textContent,
  })));
  const wantDoors = [['#workshop', 'Art'], ['#library', 'Book'], ['#instruments', 'Tools']];
  const doorsOk = doors.length === 3 && wantDoors.every(
    ([h, w], i) => doors[i].href === h && doors[i].word === w);
  doorsOk ? ok('three gates, Art first, words matching their destinations')
          : fail('gates wrong: ' + JSON.stringify(doors));

  await page.click('.st-portal');            // Art — unlocks the page
  await page.waitForTimeout(900);
  await page.keyboard.press('Escape');       // dismiss the walkthrough
  await page.waitForTimeout(400);

  errors.length ? fail(`console/page errors: ${errors.slice(0, 3).join(' | ')}`)
                : ok('no console or page errors');

  const order = await page.$$eval(
    'main section[id]', (els) => els.map((e) => e.id));
  const seen = order.filter((id) => EXPECTED_SECTIONS.includes(id));
  JSON.stringify(seen) === JSON.stringify(EXPECTED_SECTIONS)
    ? ok('sections in the new order: ' + seen.join(' → '))
    : fail('section order is ' + seen.join(' → '));

  const books = await page.$$eval(
    '#library .st-vol-title', (els) => els.map((e) => e.textContent.trim()));
  const shelf = books.slice(0, 14);
  JSON.stringify(shelf) === JSON.stringify(EXPECTED_BOOKS)
    ? ok('all 14 books, in the requested order')
    : fail('shelf order is ' + JSON.stringify(shelf));

  const nav = await page.$$eval('.topnav a', (els) => els.map((e) => e.getAttribute('href')));
  JSON.stringify(nav) === JSON.stringify(
    ['#workshop', '#library', '#instruments', '#music', '#guide', '#maker', '#support'])
    ? ok('top navigation matches the section order')
    : fail('top nav is ' + nav.join(' '));

  // Every nav target and every in-page anchor must actually exist.
  const dangling = await page.evaluate(() =>
    [...document.querySelectorAll('a[href^="#"]')]
      .map((a) => a.getAttribute('href'))
      .filter((h) => h.length > 1 && !document.querySelector(h))
      .filter((v, i, s) => s.indexOf(v) === i));
  dangling.length ? fail('anchors pointing at nothing: ' + dangling.join(' '))
                  : ok('every in-page anchor resolves');

  // The cover is loading="lazy", so it has no pixels until the section is
  // actually reached -- scroll to it before asking whether the art loaded.
  await page.evaluate(() => document.querySelector('#guide')?.scrollIntoView());
  await page.waitForTimeout(900);
  const guide = await page.evaluate(() => {
    const s = document.querySelector('#guide');
    if (!s) return null;
    const img = s.querySelector('.st-book-face img');
    return {
      title: s.querySelector('.st-vol-title')?.textContent.trim(),
      href: s.querySelector('.st-vol-open')?.getAttribute('href'),
      art: !!img && img.naturalWidth > 0,
      afterMusic: !!(document.querySelector('#music')
        .compareDocumentPosition(s) & Node.DOCUMENT_POSITION_FOLLOWING),
    };
  });
  guide && guide.title === 'How to Program NFC Tags' && guide.href === '/nfc/'
    && guide.art && guide.afterMusic
    ? ok('the guide section is present, below the music, with its cover loaded')
    : fail('guide section wrong: ' + JSON.stringify(guide));

  const footBooks = await page.$$eval(
    '.foot-grid ul a[href^="/"]', (els) => els.map((e) => e.getAttribute('href')));
  const libRows = footBooks.filter((h) => !['/portals', '/press', '/resin', '/nfc/'].includes(h));
  libRows.length === 14 ? ok('footer lists all 14 books')
                        : fail(`footer lists ${libRows.length} books`);
  footBooks.includes('/nfc/') ? ok('footer links the guide')
                              : fail('footer does not link the guide');

  const version = await page.textContent('#updates .updates-version');
  version.includes('v14') ? ok(`on-page version badge reads ${version.trim()}`)
                          : fail(`version badge reads ${version.trim()}`);

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - window.innerWidth);
  overflow > 1 ? fail(`horizontal overflow: ${overflow}px`) : ok('no horizontal overflow');

  await page.evaluate(async () => {
    const prev = document.documentElement.style.scrollBehavior;
    document.documentElement.style.scrollBehavior = 'auto';
    for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight * 0.8) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 60));
    }
    document.documentElement.style.scrollBehavior = prev;
  });
  await page.waitForTimeout(900);
  const invisible = await page.evaluate(() =>
    [...document.querySelectorAll('main section, .st-vol')]
      .filter((el) => el.getBoundingClientRect().height > 0 &&
                      +getComputedStyle(el).opacity === 0).length);
  invisible ? fail(`${invisible} blocks stuck at opacity:0 after scroll`)
            : ok('nothing stuck invisible after a full scroll');

  await page.evaluate(() => document.querySelector('#guide').scrollIntoView());
  await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(HERE, '..', '_work', `hub-guide-${width}.png`) });
  await page.evaluate(() => document.querySelector('#workshop').scrollIntoView());
  await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(HERE, '..', '_work', `hub-top-${width}.png`) });
  await ctx.close();
}

await browser.close();
console.log(failures ? `\n${failures} FAILURE(S)` : '\nall checks passed');
process.exit(failures ? 1 : 0);
