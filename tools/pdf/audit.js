// Layout audit for a Paged.js build (no PDF written): flags overflow past the page box, headings
// stranded at the foot of a page, near-empty pages inside a section, tables whose header row is
// alone on a page, and blank pages. usage: node tools/pdf/audit.js <page.html>
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require(require.resolve('playwright', { paths: ['/opt/node22/lib/node_modules', process.cwd()] }));
const CHROME = ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome', '/opt/pw-browsers/chromium'].find(p => fs.existsSync(p) && fs.statSync(p).isFile());
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.woff': 'font/woff', '.ttf': 'font/ttf', '.png': 'image/png' };
(async () => {
  const pageFile = process.argv[2], root = path.dirname(path.resolve(pageFile));
  const server = http.createServer((req, res) => {
    const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
    if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
  }).listen(0, '127.0.0.1');
  await new Promise(r => server.on('listening', r));
  const browser = await chromium.launch(CHROME ? { executablePath: CHROME } : {});
  const page = await browser.newPage();
  await page.goto(`http://127.0.0.1:${server.address().port}/${path.basename(pageFile)}`);
  await page.waitForFunction(() => window.__paged === true, null, { timeout: 600000 });
  await page.evaluate(() => document.fonts.ready);
  const r = await page.evaluate(() => {
    const out = { pages: 0, overflow: [], stranded: [], sparse: [], loneHeader: [], blank: [], tail: [] };
    const pages = [...document.querySelectorAll('.pagedjs_page')]; out.pages = pages.length;
    pages.forEach((pg, i) => {
      const n = i + 1, area = pg.querySelector('.pagedjs_page_content'); if (!area) return;
      const box = area.getBoundingClientRect();
      const els = [...area.querySelectorAll('*')].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; });
      // overflow: any element's right edge more than 2px past the content box
      els.forEach(e => { const b = e.getBoundingClientRect(); if (b.right > box.right + 2 && b.left < box.right - 5 && b.width < box.width * 1.5 && !e.closest('svg')) out.overflow.push({ page: n, tag: e.tagName + '.' + (e.className || ''), by: Math.round(b.right - box.right), text: (e.textContent || '').trim().slice(0, 50) }); });
      // how much of the page is used
      const leaf = els.filter(e => !e.children.length || e.tagName === 'P' || e.tagName === 'TR');
      const bottom = leaf.reduce((m, e) => Math.max(m, e.getBoundingClientRect().bottom), box.top);
      const fill = (bottom - box.top) / box.height;
      const text = (area.innerText || '').trim();
      if (!text.length) out.blank.push(n);
      // a page that ends a section is allowed to be short; flag a short page whose next page does not open a section
      const next = pages[i + 1], nextOpens = next && next.querySelector('section.sec > h2, .front h1, .cover');
      const opensHere = pg.querySelector('section.sec > h2, .front h1, .cover');
      if (fill < 0.30 && next && !nextOpens && !opensHere) out.sparse.push({ page: n, fill: Math.round(fill * 100) });
      // a section's last few lines spilling onto a page of their own
      if (fill < 0.15 && !opensHere && text.length) out.tail.push({ page: n, fill: Math.round(fill * 100), text: text.slice(0, 60) });
      // headings stranded at the bottom: the last visible block on the page is a heading or a box label
      const blocks = els.filter(e => /^(H2|H3|H4|P|LI|TABLE|DIV|FIGURE|UL|OL)$/.test(e.tagName));
      const last = blocks.sort((a, b) => a.getBoundingClientRect().bottom - b.getBoundingClientRect().bottom).pop();
      if (last && /^H[234]$/.test(last.tagName) && next) out.stranded.push({ page: n, text: last.textContent.trim().slice(0, 50) });
      // a table fragment on this page that has only its header row
      area.querySelectorAll('table').forEach(t => { if (t.querySelector('thead') && !t.querySelector('tbody tr')) out.loneHeader.push({ page: n, text: t.innerText.trim().slice(0, 50) }); });
    });
    return out;
  });
  await browser.close(); server.close();
  console.log(JSON.stringify(r));
})().catch(e => { console.error(e); process.exit(1); });
