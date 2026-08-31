/* Live audit of every hosted page.
   Loads each URL in headless Chromium at 375px (touch) and 1440px, and in
   reduced-motion, and reports: page/console errors, horizontal overflow,
   elements left at opacity:0 after a full scroll, internal links that go
   nowhere, leaked build placeholders, and missing viewport/lang. */
const fs = require('fs');
const { chromium } = require(require.resolve('playwright', { paths: ['/opt/node22/lib/node_modules'] }));
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const PROXY = process.env.HTTPS_PROXY || process.env.https_proxy;

const TARGETS = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const LEAKS = [/#REPLACE/i, /data-here/i, /<!--\s*(BUILD|INSTRUCTION|TODO|PASTE)/i,
               /LOREM IPSUM/i, /\bTKTK\b/, /being written/i, /coming soon/i];

(async () => {
  const browser = await chromium.launch({
    executablePath: CHROME,
    proxy: PROXY ? { server: PROXY } : undefined,
    args: ['--ignore-certificate-errors'],
  });
  const report = [];

  for (const t of TARGETS) {
    const found = [];
    let status = null, bytes = 0, title = '';
    for (const vp of [{ n: '375', w: 375, h: 780, mob: true }, { n: '1440', w: 1440, h: 900 }]) {
      for (const motion of ['no-preference', 'reduce']) {
        const ctx = await browser.newContext({
          viewport: { width: vp.w, height: vp.h }, isMobile: vp.mob, hasTouch: vp.mob,
          deviceScaleFactor: vp.mob ? 2 : 1, reducedMotion: motion,
          ignoreHTTPSErrors: true,
        });
        const page = await ctx.newPage();
        const errs = [];
        page.on('pageerror', e => errs.push('pageerror: ' + String(e.message).slice(0, 160)));
        page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 160)); });
        page.on('requestfailed', r => {
          const u = r.url();
          // this sandbox has no egress, so a third-party request failing here is
          // not a finding -- that the page makes one at all is the finding
          if (!/favicon/.test(u)) errs.push('EXTERNAL REQUEST: ' + u.slice(0, 120));
        });
        try {
          const resp = await page.goto(t.url, { waitUntil: 'load', timeout: 45000 });
          status = resp ? resp.status() : null;
          await page.waitForTimeout(700);
          // Scroll-reveal pages hide everything below the fold until an
          // IntersectionObserver fires, so a fast scroll then a single count
          // reports hundreds of false positives. Step down, let each screen
          // settle, and only ever count what is actually in the viewport.
          let stuckWorst = 0, stuckSample = [];
          const screens = Math.min(14, Math.ceil(
            await page.evaluate(() => document.body.scrollHeight / window.innerHeight)) + 1);
          for (let i = 0; i < screens; i++) {
            const r = await page.evaluate(() => [...document.querySelectorAll('body *')]
              .filter(el => {
                const st = getComputedStyle(el), b = el.getBoundingClientRect();
                return st.opacity === '0' && st.visibility !== 'hidden' && st.display !== 'none'
                  && b.top < innerHeight - 20 && b.bottom > 20 && b.height > 4
                  && (el.textContent || '').trim().length > 12;
              }).map(e => String(e.className || e.tagName).slice(0, 50)));
            if (r.length > stuckWorst) { stuckWorst = r.length; stuckSample = r.slice(0, 2); }
            await page.evaluate(() => window.scrollBy(0, window.innerHeight * 0.7));
            await page.waitForTimeout(1400);   // longer than the longest stagger delay measured (1.05s)
          }
          await page.evaluate(() => window.scrollTo(0, 0));
          await page.waitForTimeout(250);
          const r = await page.evaluate(() => {
            return {
              overflow: document.documentElement.scrollWidth - window.innerWidth,

              html: document.documentElement.outerHTML.length,
              title: document.title,
              lang: document.documentElement.lang || '',
              viewport: !!document.querySelector('meta[name="viewport"]'),
              text: (document.body.innerText || '').trim().length,
              anchors: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
              ids: [...document.querySelectorAll('[id]')].map(e => e.id),
            };
          });
          bytes = r.html; title = r.title;
          const tag = `${vp.n}/${motion}`;
          if (r.overflow > 1) found.push(`${tag} horizontal overflow +${r.overflow}px`);
          if (stuckWorst > 0) found.push(`${tag} ${stuckWorst} in-viewport element(s) stuck at opacity:0 after settling (${stuckSample.join(', ')})`);
          if (r.text < 200) found.push(`${tag} only ${r.text} chars of visible text`);
          if (motion === 'no-preference' && vp.n === '1440') {
            if (!r.viewport) found.push('no viewport meta');
            if (!r.lang) found.push('no lang attribute on <html>');
            if (!r.title) found.push('empty <title>');
            // in-page anchors that point at nothing
            const dead = r.anchors.filter(h => h && h.startsWith('#') && h.length > 1
              && !h.startsWith('#/') && !r.ids.includes(h.slice(1)));
            if (dead.length) found.push(`dead in-page anchors: ${[...new Set(dead)].slice(0, 6).join(' ')}`);
            const html = await page.content();
            for (const rx of LEAKS) {
              const m = html.match(rx);
              if (m) found.push(`leaked placeholder: ${JSON.stringify(m[0].slice(0, 50))}`);
            }
          }
        } catch (e) {
          found.push(`LOAD FAILED (${vp.n}/${motion}): ${String(e.message).slice(0, 140)}`);
        }
        if (errs.length) found.push(...[...new Set(errs)].slice(0, 5).map(e => `${vp.n}/${motion} ${e}`));
        await ctx.close();
      }
    }
    const uniq = [...new Set(found)];
    report.push({ slug: t.slug, url: t.url, status, kb: Math.round(bytes / 1024), title, findings: uniq });
    console.log(`\n### ${t.slug}  (${status}, ${Math.round(bytes / 1024)} KB)  ${t.url}`);
    console.log(`    ${title}`);
    if (!uniq.length) console.log('    clean');
    else uniq.forEach(f => console.log('    ✗ ' + f));
  }
  await browser.close();
  fs.writeFileSync(process.argv[3] || '/tmp/live-audit.json', JSON.stringify(report, null, 1));
  const bad = report.filter(r => r.findings.length);
  console.log(`\n==== ${report.length} pages, ${bad.length} with findings, ${report.reduce((a, r) => a + r.findings.length, 0)} findings total`);
})();
