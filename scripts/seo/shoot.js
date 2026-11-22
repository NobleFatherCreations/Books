// Visual verification (CLAUDE.md pattern): 375 + 1440 screenshots, page errors, horizontal overflow,
// stuck opacity:0, reduced-motion pass, failed requests. Usage: node shoot.js outdir url [url...]
const { chromium } = require('playwright');
(async () => {
  const [out, ...urls] = process.argv.slice(2);
  const browser = await chromium.launch();
  const report = [];
  for (const url of urls) {
    for (const [w, h, rm] of [[375, 812, 'no-preference'], [1440, 900, 'no-preference'], [375, 812, 'reduce']]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: rm });
      const page = await ctx.newPage();
      const errs = [], failed = [];
      page.on('pageerror', e => errs.push(String(e).slice(0, 160)));
      page.on('requestfailed', r => failed.push(r.url().slice(0, 120)));
      page.on('response', r => { if (r.status() >= 400) failed.push(r.status() + ' ' + r.url().slice(0, 120)); });
      await page.goto(url, { waitUntil: 'load', timeout: 60000 });
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 15)); } window.scrollTo(0, 0); });
      await page.waitForTimeout(300);
      const m = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth > innerWidth + 1,
        stuck: [...document.querySelectorAll('main *, article *')].filter(e => getComputedStyle(e).opacity === '0' && e.textContent.trim()).length,
        h1: document.querySelectorAll('h1').length, title: document.title,
      }));
      const name = url.replace(/^https?:\/\/[^/]+\//, '').replace(/\//g, '_') || 'home';
      if (rm === 'no-preference') await page.screenshot({ path: `${out}/${name}-${w}.png`, fullPage: false });
      report.push({ url, w, rm, ...m, errs, failed: [...new Set(failed)].filter(u => !u.includes('cloudflareinsights')) });
      await ctx.close();
    }
  }
  await browser.close();
  for (const r of report) console.log(JSON.stringify(r));
})();
