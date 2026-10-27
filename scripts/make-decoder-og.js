#!/usr/bin/env node
/* Draws the 1200x630 link-preview image for the Pattern Decoder (design/decoder-v15/assets/og.png).
 *   node scripts/make-decoder-og.js        (needs Playwright; run `python3 design/build-decoder-v15.py` first for the icon)
 * The image is committed; the build copies it to /playbook/f/og.png. Re-run only if the wording or look changes. */
const fs = require("fs"), os = require("os"), path = require("path"), { createRequire } = require("module"), { chromium } = createRequire(__filename)("playwright");
const root = path.join(__dirname, "..");
const f = p => "file://" + path.join(root, p);
const html = `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:O;font-weight:600 800;src:url(${f("design/decoder-v15/assets/overpass-var.woff2")})}
@font-face{font-family:A;font-weight:400 700;src:url(${f("design/decoder-v15/assets/atkinson-next-var.woff2")})}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#050507;color:#F2F0EA;position:relative;overflow:hidden;font-family:A}
.g{position:absolute;inset:0;background:radial-gradient(760px 420px at 12% -8%,rgba(229,193,88,.20),transparent 70%),radial-gradient(620px 360px at 100% 100%,rgba(229,193,88,.10),transparent 70%)}
.b{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:18px;font:800 34px O}.b img{width:56px;height:56px;border-radius:50%}
h1{position:absolute;left:72px;top:196px;width:960px;font:800 104px/1.02 O;letter-spacing:-.03em}
p{position:absolute;left:72px;top:416px;width:900px;font:400 36px/1.4 A;color:#A8A69E}
.u{position:absolute;left:72px;bottom:44px;display:flex;align-items:center;gap:20px;font:800 26px O;color:#E5C158}.u i{width:64px;height:8px;border-radius:8px;background:#E5C158}
</style><div class="g"></div><div class="b"><img src="${f("instruments/playbook/site/f/icon.webp")}">Pattern Decoder</div>
<h1>Put a name to what is happening.</h1><p>310 manipulation and control tactics, in plain words: how to tell if one fits, and what you can do.</p>
<div class="u"><i></i>noblefathercreations.com/playbook</div>`;
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  const tmp = path.join(os.tmpdir(), "decoder-og.html"); fs.writeFileSync(tmp, html);   /* file:// assets load only from a file page */
  await p.goto("file://" + tmp); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(root, "design/decoder-v15/assets/og.png") }); await b.close(); })();
