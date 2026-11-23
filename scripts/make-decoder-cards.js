#!/usr/bin/env node
/* Share cards (1200x630) for every Decoder tactic and pattern, from design/decoder-og/cards.json (written by the build).
 *   node scripts/make-decoder-cards.js [--force]     then rebuild: python3 design/build-decoder-v15.py
 * A card is redrawn only when its data changed (hash in design/decoder-og/cache.json). Uses the pre-installed Playwright. */
const fs = require("fs"), path = require("path"), crypto = require("crypto"), { createRequire } = require("module");
const { chromium } = createRequire(__filename)("playwright");
const root = path.join(__dirname, ".."), dir = path.join(root, "design/decoder-og");
const cards = JSON.parse(fs.readFileSync(path.join(dir, "cards.json"), "utf8"));
const cacheP = path.join(dir, "cache.json"), force = process.argv.includes("--force");
const cache = !force && fs.existsSync(cacheP) ? JSON.parse(fs.readFileSync(cacheP, "utf8")) : {};
const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const f = p => "file://" + path.join(root, p);
const page = c => {
  const L = c.n.length, size = L <= 10 ? 96 : L <= 18 ? 72 : L <= 30 ? 58 : 48;
  return `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:O;font-weight:600 800;src:url(${f("design/decoder-v15/assets/overpass-var.woff2")})}
@font-face{font-family:A;font-weight:400 700;src:url(${f("design/decoder-v15/assets/atkinson-next-var.woff2")})}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#050507;color:#F2F0EA;font-family:A;overflow:hidden;position:relative}
.bar{position:absolute;left:0;top:0;width:1200px;height:12px;background:${c.c}}
.top{position:absolute;left:72px;right:72px;top:56px;display:flex;align-items:center;gap:20px;font:800 26px O;letter-spacing:.08em;text-transform:uppercase;color:#A8A69E}
.bul{width:64px;height:64px;border-radius:50%;background:${c.c};color:#050507;display:grid;place-items:center;font:800 34px O;letter-spacing:0}
.top .r{margin-left:auto;color:#E5C158}
h1{position:absolute;left:72px;top:170px;width:540px;font:800 ${size}px/1.04 O;letter-spacing:-.025em}
p{position:absolute;left:72px;bottom:120px;width:500px;font:400 34px/1.38 A;color:#C9C6BD}
.u{position:absolute;left:72px;bottom:56px;font:800 22px O;color:#E5C158}
.by{position:absolute;left:72px;bottom:20px;font:700 22px O;color:#A8A69E}
.fig{position:absolute;right:-24px;top:0;height:630px}
.top .r{position:relative;z-index:1}
</style><img class="fig" src="${f("design/brand/figure-panel.png")}"><div class="bar"></div><div class="top"><div class="bul">${c.letter}</div><span>${esc(c.code)}&nbsp; · &nbsp;${esc(c.kind)}</span><span class="r">Pattern Decoder</span></div>
<h1>${esc(c.n)}</h1><p>${esc(c.d)}</p><div class="u">noblefathercreations.com/playbook</div><div class="by">Shae Stovell<b style="font-weight:inherit;margin:0 .45em">·</b>Noble Father Creations</div>`;
};
(async () => {
  const todo = cards.filter(c => { const h = crypto.createHash("sha256").update(JSON.stringify(c)).digest("hex").slice(0, 16);
    c.h = h; return force || cache[c.s] !== h || !fs.existsSync(path.join(dir, c.s + ".jpg")); });
  if (!todo.length) { console.log(`share cards: all ${cards.length} up to date`); return; }
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  const tmp = path.join(dir, ".card.html");
  for (const c of todo) {
    fs.writeFileSync(tmp, page(c)); await p.goto("file://" + tmp); await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => { const h = document.querySelector("h1"), q = document.querySelector("p"); return h.getBoundingClientRect().bottom > q.getBoundingClientRect().top - 16; });
    if (over) await p.evaluate(() => { const h = document.querySelector("h1"); h.style.fontSize = (parseFloat(getComputedStyle(h).fontSize) * 0.8) + "px"; });
    await p.screenshot({ path: path.join(dir, c.s + ".jpg"), type: "jpeg", quality: 82 }); cache[c.s] = c.h;
  }
  await b.close(); fs.unlinkSync(tmp);
  fs.writeFileSync(cacheP, JSON.stringify(cache, null, 0));
  console.log(`share cards: ${todo.length} drawn, ${cards.length - todo.length} unchanged`);
})();
