/* Visual + behavioural verification for a single-file book.
   Checks, at 375px (touch) and 1440px, in normal and reduced-motion:
   console/page errors, horizontal overflow, elements stuck at opacity:0,
   that every hash route renders, and that the quick exit works. */
const path = require('path');
const fs = require('fs');
const { chromium } = require(require.resolve('playwright', { paths: ['/opt/node22/lib/node_modules'] }));
// /opt/pw-browsers/chromium is a launcher file, not the binary; the real one is versioned.
const CHROME = ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell']
               .find(p => fs.existsSync(p));

const file = process.argv[2];
const url = 'file://' + path.resolve(file);
const ROUTES = ['#/', '#/help', '#/card', '#/limits', '#/c/1', '#/c/2'];

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  let fails = 0;
  const bad = m => { console.log('  ✗ ' + m); fails++; };

  for (const vp of [
    { name: '375 touch', width: 375, height: 780, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
    { name: '1440', width: 1440, height: 900 },
  ]) {
    for (const motion of ['no-preference', 'reduce']) {
      for (const dark of [false, true]) {
      const ctx = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        isMobile: vp.isMobile, hasTouch: vp.hasTouch,
        deviceScaleFactor: vp.deviceScaleFactor, reducedMotion: motion,
      });
      const page = await ctx.newPage();
      const errs = [];
      // dark is a class toggle, not a media query, so it has to be set per page
      page.on('pageerror', e => errs.push('pageerror: ' + e.message));
      page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

      for (const r of ROUTES) {
        await page.goto(url + r, { waitUntil: 'load' });
        if (dark) await page.evaluate(() => document.documentElement.classList.add('dark'));
        await page.waitForTimeout(160);
        const res = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth - window.innerWidth,
          rendered: (document.getElementById('app') || {}).children?.length || 0,
          invisible: [...document.querySelectorAll('#app *')].filter(el => {
            const s = getComputedStyle(el);
            return s.opacity === '0' && el.getBoundingClientRect().height > 0;
          }).length,
          text: (document.getElementById('app') || {}).innerText?.trim().length || 0,
          // text the reader cannot see because it matches its own background
          invisibleText: (() => {
            const seen = [];
            for (const el of document.querySelectorAll('#app p, #app b, #app h1, #app h2, #app h3, #app li, #app a')) {
              if (!(el.textContent || '').trim()) continue;
              const cs = getComputedStyle(el);
              let bg = 'rgba(0, 0, 0, 0)', n = el;
              while (n && bg === 'rgba(0, 0, 0, 0)') { bg = getComputedStyle(n).backgroundColor; n = n.parentElement; }
              if (cs.color === bg) seen.push(el.tagName + '.' + String(el.className).slice(0, 30));
            }
            return seen.slice(0, 3);
          })(),
        }));
        const tag = `${vp.name}/${motion}${dark ? '/dark' : ''}${r}`;
        if (res.overflow > 1) bad(`${tag} horizontal overflow +${res.overflow}px`);
        if (res.rendered === 0) bad(`${tag} nothing rendered`);
        if (res.text < 80) bad(`${tag} only ${res.text} chars of text`);
        if (res.invisible > 0) bad(`${tag} ${res.invisible} element(s) stuck at opacity:0`);
        if (res.invisibleText.length) bad(`${tag} text the same colour as its background: ${res.invisibleText.join(', ')}`);
      }
      if (errs.length) errs.slice(0, 4).forEach(e => bad(`${vp.name}/${motion} ${e}`));
      await ctx.close();
      }
    }
  }

  // A double-escaped \\uXXXX renders as literal "\\u201c" text rather than a
  // character. Caught only by looking at the rendered text: every other check
  // passes, and the page looks fine at a glance.
  {
    const ctx0 = await browser.newContext();
    const pg = await ctx0.newPage();
    await pg.goto(url + '#/c/1', { waitUntil: 'load' });
    const src = fs.readFileSync(file, 'utf8');
    const dbl = (src.match(/\\\\u[0-9a-fA-F]{4}/g) || []).length;
    if (dbl) bad(`${dbl} double-escaped \\uXXXX sequence(s) -- these render as literal text`);
    else console.log('  ✓ no double-escaped unicode');
    // and confirm no literal escape survives into what the reader sees
    let leaked = 0;
    for (const r of ['#/c/1', '#/c/2', '#/card', '#/help']) {
      await pg.goto(url + r, { waitUntil: 'load' });
      await pg.waitForTimeout(120);
      const t = await pg.evaluate(() => document.body.innerText);
      leaked += (t.match(/\\u[0-9a-fA-F]{4}|&[a-z]{2,8};/g) || []).length;
    }
    if (leaked) bad(`${leaked} escape sequence(s) visible in the rendered text`);
    else console.log('  ✓ no escapes leak into the rendered text');
    await ctx0.close();
  }

  // quick exit must actually clear the page
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(url + '#/c/1', { waitUntil: 'load' });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  const after = await page.evaluate(() => document.body ? document.body.innerText.trim().length : 0).catch(() => 0);
  if (after > 20) bad(`Esc did not clear the page (${after} chars remain)`); else console.log('  ✓ Esc clears the page');

  const page2 = await ctx.newPage();
  await page2.goto(url + '#/c/1', { waitUntil: 'load' });
  await page2.click('#exitbtn');
  await page2.waitForTimeout(400);
  const after2 = await page2.evaluate(() => document.body ? document.body.innerText.trim().length : 0).catch(() => 0);
  if (after2 > 20) bad(`Leave button did not clear the page (${after2} chars)`); else console.log('  ✓ Leave button clears the page');

  await browser.close();
  console.log(fails ? `  FAILED (${fails})` : '  ALL VISUAL CHECKS PASS');
  process.exit(fails ? 1 : 0);
})();
