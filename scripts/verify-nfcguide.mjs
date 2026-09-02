/**
 * Visual + behavioural check for the NFC guide, run before any deploy.
 *
 * Checks the things a structure test cannot see: that the page actually
 * paints, that nothing overflows sideways, that no request leaves the
 * machine, and that the two drawers this page now carries -- its own
 * section menu and the catalogue -- do not fight over Escape or the
 * bottom-right corner.
 *
 * Usage: node scripts/verify-nfcguide.mjs [file-or-url]
 */
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const target = process.argv[2] ||
  'file://' + path.join(HERE, '..', 'workshop', 'nfcguide', 'index.html');

const WIDTHS = [375, 1440];
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

for (const width of WIDTHS) {
  for (const reduce of [false, true]) {
    const label = `${width}px${reduce ? ' reduced-motion' : ''}`;
    console.log(`\n== ${label} ==`);
    const ctx = await browser.newContext({
      viewport: { width, height: 900 },
      colorScheme: 'dark',
      reducedMotion: reduce ? 'reduce' : 'no-preference',
    });
    const page = await ctx.newPage();

    const errors = [];
    const external = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('request', (r) => {
      const u = r.url();
      if (!u.startsWith('file://') && !u.startsWith('data:') &&
          !u.startsWith(target.replace(/[^/]*$/, ''))) external.push(u);
    });

    await page.goto(target, { waitUntil: 'load' });
    await page.waitForTimeout(reduce ? 300 : 900);

    errors.length ? fail(`console/page errors: ${errors.slice(0, 3).join(' | ')}`)
                  : ok('no console or page errors');
    external.length ? fail(`external requests: ${external.slice(0, 3).join(' | ')}`)
                    : ok('no external requests');

    // Real content painted, not an empty shell.
    const recipes = await page.locator('#grid > li').count();
    recipes > 50 ? ok(`recipe index rendered (${recipes} cards)`)
                 : fail(`recipe index looks empty (${recipes} cards)`);

    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - window.innerWidth);
    overflow > 1 ? fail(`horizontal overflow: ${overflow}px`) : ok('no horizontal overflow');

    // Scroll the whole page, then check nothing was left invisible by a
    // reveal engine that never fired.
    await page.evaluate(async () => {
      // The page sets scroll-behavior:smooth, so a plain scrollTo loop just
      // retargets one animation and the page barely moves -- which reads as
      // "content stuck invisible" when nothing ever scrolled to it.
      const prev = document.documentElement.style.scrollBehavior;
      document.documentElement.style.scrollBehavior = 'auto';
      for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight * 0.8) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 60));
      }
      window.scrollTo(0, 0);
      document.documentElement.style.scrollBehavior = prev;
    });
    await page.waitForTimeout(2800);
    const invisible = await page.evaluate(() =>
      [...document.querySelectorAll('section, .panel, .rcard, article')]
        .filter((el) => el.getBoundingClientRect().height > 0 &&
                        +getComputedStyle(el).opacity === 0).length);
    invisible ? fail(`${invisible} elements stuck at opacity:0 after scroll`)
              : ok('nothing stuck invisible after a full scroll');

    // The catalogue drawer: opens, carries all twenty, closes on Escape.
    const seal = page.locator('#nf-chrome .nf-seal');
    if (await seal.count()) {
      await seal.click();
      await page.waitForTimeout(reduce ? 120 : 420);
      const open = await page.locator('#nf-chrome.nf-open').count();
      const rows = await page.locator('#nf-panel .nf-row').count();
      open ? ok('catalogue drawer opens') : fail('catalogue drawer did not open');
      rows === 20 ? ok('catalogue lists 20 volumes') : fail(`catalogue has ${rows} rows`);
      await page.keyboard.press('Escape');
      await page.waitForTimeout(reduce ? 120 : 320);
      (await page.locator('#nf-chrome.nf-open').count())
        ? fail('Escape did not close the catalogue')
        : ok('Escape closes the catalogue');
    } else fail('no catalogue drawer on the page');

    // Escape must still reach the guide's own recipe sheet.
    const card = page.locator('#grid > li').first();
    if (await card.count()) {
      await card.click();
      await page.waitForTimeout(reduce ? 150 : 500);
      const sheetOpen = await page.locator('.sheet.on').count();
      if (sheetOpen) {
        ok('recipe sheet opens');
        await page.keyboard.press('Escape');
        await page.waitForTimeout(reduce ? 150 : 400);
        (await page.locator('.sheet.on').count())
          ? fail('Escape did not close the recipe sheet')
          : ok('Escape closes the recipe sheet');
      } else fail('recipe sheet did not open on click');
    }

    // The seal must not sit on top of the back-to-top button.
    const collide = await page.evaluate(() => {
      const a = document.querySelector('#nf-chrome .nf-seal');
      const b = document.querySelector('.totop');
      if (!a || !b) return null;
      const r = a.getBoundingClientRect(), s = b.getBoundingClientRect();
      return !(r.right < s.left || s.right < r.left ||
               r.bottom < s.top || s.bottom < r.top);
    });
    collide === true ? fail('seal overlaps the back-to-top button')
                     : ok('seal and back-to-top do not overlap');

    await page.screenshot({
      path: path.join(HERE, '..', '_work',
        `nfcguide-${width}${reduce ? '-reduced' : ''}.png`),
      fullPage: false,
    });
    await ctx.close();
  }
}

// Light mode, once, at the wider size.
{
  console.log('\n== light mode, 1440px ==');
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
  const page = await ctx.newPage();
  await page.goto(target, { waitUntil: 'load' });
  await page.click('#themeBtn');
  await page.waitForTimeout(400);
  const theme = await page.evaluate(() => document.documentElement.dataset.theme);
  theme === 'light' ? ok('light mode applies') : fail(`theme is ${theme}`);
  await page.screenshot({ path: path.join(HERE, '..', '_work', 'nfcguide-light.png') });
  await ctx.close();
}

await browser.close();
console.log(failures ? `\n${failures} FAILURE(S)` : '\nall checks passed');
process.exit(failures ? 1 : 0);
