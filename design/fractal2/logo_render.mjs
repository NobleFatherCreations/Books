// Render the logo SVG to PNG with the pre-installed Chromium.   node design/fractal2/logo_render.mjs <svg> <png> <size>
import { createRequire } from "module"; import fs from "fs";
const require = createRequire(import.meta.url); const { chromium } = require("playwright");
const [, , svgPath, pngPath, sizeArg] = process.argv; const size = +sizeArg || 4096;
const svg = fs.readFileSync(svgPath, "utf8");
const b = await chromium.launch();
const view = 1024, scale = size / view;
const c = await b.newContext({ viewport: { width: view, height: view }, deviceScaleFactor: scale });
const p = await c.newPage();
await p.setContent(`<!doctype html><html><body style="margin:0;background:#04050d">${svg.replace(/width="\d+" height="\d+"/, 'width="1024" height="1024"')}</body></html>`, { waitUntil: "load" });
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
await p.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: view, height: view } });
await b.close(); console.log("rendered", pngPath, size);
