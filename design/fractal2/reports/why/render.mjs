// Single-pass render so internal links survive. Usage: node render.mjs in.html out.pdf
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { pathToFileURL } from 'node:url'; import { resolve } from 'node:path';
const [inp, out] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('requestfailed', r => errs.push('FAILED ' + r.url()));
await p.goto(pathToFileURL(resolve(inp)).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close(); console.log('wrote', out, errs.length ? errs : '');
