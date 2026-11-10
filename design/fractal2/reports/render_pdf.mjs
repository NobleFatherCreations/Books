// Renders a report HTML file to an A4 PDF: a full-bleed cover page, then the body with page numbers.
// Usage: node design/fractal2/reports/render_pdf.mjs <in.html> <out.pdf> "<footer title>"
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { rmSync } from 'node:fs';

const [inp, out, title = ''] = process.argv.slice(2);
const url = pathToFileURL(resolve(inp)).href;
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const cover = out.replace(/\.pdf$/, '.cover.pdf');
const body = out.replace(/\.pdf$/, '.body.pdf');

// Cover: only the first section, no margins.
await page.addStyleTag({ content: 'body>section:not(.cover){display:none}' });
await page.pdf({ path: cover, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });

// Body: everything else, with margins and a footer.
await page.reload({ waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.addStyleTag({ content: '.cover{display:none}' });
const foot = `<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7pt;color:#8a857b;padding:0 18mm;display:flex;justify-content:space-between">
<span>${title}</span><span><span class="pageNumber"></span></span></div>`;
await page.pdf({ path: body, format: 'A4', printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>', footerTemplate: foot,
  margin: { top: '19mm', right: '18mm', bottom: '21mm', left: '18mm' } });
await browser.close();

execFileSync('python3', ['-c', `
import sys
from pypdf import PdfWriter, PdfReader
w = PdfWriter()
for f in sys.argv[1:3]:
    for p in PdfReader(f).pages: w.add_page(p)
w.add_metadata({'/Title': sys.argv[4], '/Author': 'Prepared for Shae Stovell, Noble Father Creations'})
w.write(sys.argv[3])
`, cover, body, out, title]);
rmSync(cover); rmSync(body);
console.log('wrote', out);
