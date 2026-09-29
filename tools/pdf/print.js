// Print a Paged.js-laid-out HTML file to PDF with Chromium (Playwright, preinstalled).
// usage: node tools/pdf/print.js <page.html> <out.pdf> "<title>"
// Paged.js fetches stylesheets with XHR, which Chromium blocks on file:// — so the page's folder is
// served on a throwaway localhost port for the length of the print.
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require(require.resolve('playwright', { paths: ['/opt/node22/lib/node_modules', process.cwd()] }));
const CHROME = ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/opt/pw-browsers/chromium'].find(p => fs.existsSync(p) && fs.statSync(p).isFile());
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.woff': 'font/woff', '.ttf': 'font/ttf', '.png': 'image/png', '.svg': 'image/svg+xml' };
(async () => {
  const [pageFile, out] = process.argv.slice(2);
  const root = path.dirname(path.resolve(pageFile));
  const server = http.createServer((req, res) => {
    const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
    if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  }).listen(0, '127.0.0.1');
  await new Promise(r => server.on('listening', r));
  const url = `http://127.0.0.1:${server.address().port}/${path.basename(pageFile)}`;
  const browser = await chromium.launch(CHROME ? { executablePath: CHROME } : {});
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|404/.test(m.text())) errors.push(m.text()); });
  // Trial layouts: find a section whose last few lines spill onto a page of their own, or a table whose
  // header row sits alone at a page foot, and reload with that section set tighter (?snug=) or that
  // table moved to a fresh page (?brk=). Pages without the hook in their PagedConfig ignore the query.
  const snug = new Map(), brk = new Set();
  let issues = null;
  for (let pass = 0; pass < 4; pass++) {
    const q = new URLSearchParams();
    if (snug.size) q.set('snug', [...snug].map(([id, l]) => `${id}:${l}`).join(','));
    if (brk.size) q.set('brk', [...brk].join(','));
    await page.goto(url + (q.toString() ? '?' + q : ''));
    await page.waitForFunction(() => window.__paged === true, null, { timeout: 600000 });
    await page.evaluate(() => document.fonts.ready);
    issues = await page.evaluate(() => {
      const out = { tails: [], lone: [] }, pages = [...document.querySelectorAll('.pagedjs_page')];
      pages.forEach((pg, i) => {
        const area = pg.querySelector('.pagedjs_page_content'); if (!area) return;
        const box = area.getBoundingClientRect(), text = (area.innerText || '').trim();
        const leaf = [...area.querySelectorAll('*')].filter(e => { const b = e.getBoundingClientRect(); return b.height > 0 && (!e.children.length || e.tagName === 'P' || e.tagName === 'TR'); });
        const fill = (leaf.reduce((m, e) => Math.max(m, e.getBoundingClientRect().bottom), box.top) - box.top) / box.height;
        const sec = area.querySelector('section.sec');
        if (fill < 0.15 && text && !pg.querySelector('section.sec > h2, .front h1, .cover') && sec) out.tails.push({ page: i + 1, id: sec.dataset.id || sec.id });
        area.querySelectorAll('table[data-ti]').forEach(t => { if (t.querySelector('thead') && !t.querySelector('tbody tr')) out.lone.push({ page: i + 1, ti: t.dataset.ti }); });
      });
      return out;
    });
    let changed = false;
    for (const t of issues.tails) { const l = snug.get(t.id) || 0; if (t.id && l < 2) { snug.set(t.id, l + 1); changed = true; } }
    for (const t of issues.lone) if (!brk.has(t.ti)) { brk.add(t.ti); changed = true; }
    if (!changed) break;
  }
  if (snug.size || brk.size) console.log(`fitted: ${snug.size} section(s) tightened, ${brk.size} table(s) moved; left: ${issues.tails.length} short tail(s) ${JSON.stringify(issues.tails.map(t => t.page))}, ${issues.lone.length} lone header(s)`);
  const pages = await page.evaluate(() => document.querySelectorAll('.pagedjs_page').length);
  // where each heading landed, for the PDF bookmark tree (Paged.js pages are .pagedjs_page, 1-based)
  const marks = await page.evaluate(() => [...document.querySelectorAll('h1[id], h2[id], h3[id], h4[id^="t-"]')].map(h => {
    const pg = h.closest('.pagedjs_page');
    return { id: h.id, level: +h.tagName[1], text: h.innerText.replace(/\s+/g, ' ').trim(), page: pg ? +pg.dataset.pageNumber : null };
  }));
  fs.writeFileSync(out.replace(/\.pdf$/, '.marks.json'), JSON.stringify(marks));
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, outline: true, tagged: true });
  await browser.close(); server.close();
  if (errors.length) console.error('page errors:', errors.slice(0, 5));
  console.log(`laid out ${pages} pages → ${out}`);
})().catch(e => { console.error(e); process.exit(1); });
