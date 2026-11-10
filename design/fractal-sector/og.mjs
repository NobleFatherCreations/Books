// Render social cards: library/fractal2/build/<s>/og-src/*.html -> library/fractal2/site/<base>/og/*.png (1200x630).
import fs from "fs"; import path from "path"; import { createRequire } from "module";
const { chromium } = createRequire(import.meta.url)("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const man = JSON.parse(fs.readFileSync(path.join(ROOT, "library/fractal2/manifests", (process.argv[2] || "ent") + ".json"), "utf8"));
const dest = path.join(ROOT, "library/fractal2/site", man.base.slice(1), "og"); fs.mkdirSync(dest, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 }, colorScheme: "dark" });
for (const n of man.og) {
  await p.goto("file://" + path.join(ROOT, man.og_src, n + ".html")); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(dest, n + ".png") });
}
await b.close(); console.log(`${man.og.length} social cards -> ${dest}`);
