// Render social cards: library/fractal/sectors/<sector>/og-src/*.html -> site/<base>/og/*.png (1200x630).
import fs from "fs"; import path from "path"; import { createRequire } from "module";
const { chromium } = createRequire(import.meta.url)("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const out = path.join(ROOT, "library/fractal/sectors", process.argv[2] || "ent");
const man = JSON.parse(fs.readFileSync(path.join(out, "manifest.json"), "utf8"));
const dest = path.join(out, "site", man.base.slice(1), "og"); fs.mkdirSync(dest, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
for (const n of man.og) {
  await p.goto("file://" + path.join(out, "og-src", n + ".html")); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(dest, n + ".png") });
}
await b.close(); console.log(`${man.og.length} social cards -> ${dest}`);
