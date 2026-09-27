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
  await page.goto(url);
  await page.waitForFunction(() => window.__paged === true, null, { timeout: 600000 });
  await page.evaluate(() => document.fonts.ready);
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
