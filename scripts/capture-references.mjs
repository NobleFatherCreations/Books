#!/usr/bin/env node
// Capture the benchmark reference library: hero + 2 scroll positions at phone (390) and desktop (1440) for every site in references/sites.json.
//   node scripts/capture-references.mjs [--set reading-first] [--only slug,slug] [--out references/shots]
// Output: references/shots/<set>/<slug>/{phone,desktop}-{0,1,2}.jpg  and references/shots/index.json (status per site).
// Public pages only. Respect each site's terms; screenshots are for private study and benchmarking, not republishing.
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path';
const require = createRequire(import.meta.url); const { chromium } = require('playwright');
const args = process.argv.slice(2); const opt = (k, d) => { const i = args.indexOf('--' + k); return i > -1 ? args[i + 1] : d; };
const cfg = JSON.parse(fs.readFileSync(new URL('../references/sites.json', import.meta.url)));
const only = (opt('only', '') || '').split(',').filter(Boolean); const wantSet = opt('set', '');
const outDir = opt('out', 'references/shots'); fs.mkdirSync(outDir, { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const index = {};
for (const [setName, set] of Object.entries(cfg.sets)) {
  if (wantSet && wantSet !== setName) continue;
  for (const s of set.sites) {
    if (only.length && !only.includes(s.slug)) continue;
    const dir = path.join(outDir, setName, s.slug); fs.mkdirSync(dir, { recursive: true });
    const st = { url: s.url, ok: [], err: null };
    for (const [pname, vp, mobile] of [['phone', { width: 390, height: 844 }, true], ['desktop', { width: 1440, height: 900 }, false]]) {
      const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile, userAgent: undefined });
      const page = await ctx.newPage();
      try {
        await page.goto(s.url, { timeout: 40000, waitUntil: 'domcontentloaded' });
        await page.waitForTimeout(3500);
        // best-effort: decline cookie/consent banners so screenshots show the design (rejects, never accepts tracking where a reject button exists)
        for (const re of [/^(reject all|reject additional cookies|reject analytics cookies|reject|decline|decline all|no thanks|only necessary|necessary only|deny)$/i, /^(accept all|accept|got it|i agree|ok|okay|continue)$/i]) {
          const btn = page.getByRole('button', { name: re }).first();
          if (await btn.count().catch(() => 0)) { await btn.click({ timeout: 1500 }).catch(() => {}); await page.waitForTimeout(600); break; }
        }
        for (let i = 0; i < 3; i++) {
          await page.evaluate((y) => scrollTo(0, y), i === 0 ? 0 : i * vp.height * 1.1);
          await page.waitForTimeout(i === 0 ? 300 : 1200);
          await page.screenshot({ path: path.join(dir, `${pname}-${i}.jpg`), type: 'jpeg', quality: 62 });
          st.ok.push(`${pname}-${i}`);
        }
      } catch (e) { st.err = (st.err || '') + `${pname}: ${String(e).split('\n')[0].slice(0, 80)} `; }
      await ctx.close();
    }
    index[`${setName}/${s.slug}`] = st; console.log(setName, s.slug, st.ok.length + '/6', st.err || '');
  }
}
await b.close();
const ip = path.join(outDir, 'index.json'); const prev = fs.existsSync(ip) ? JSON.parse(fs.readFileSync(ip)) : {};
fs.writeFileSync(ip, JSON.stringify({ ...prev, ...index }, null, 1));
