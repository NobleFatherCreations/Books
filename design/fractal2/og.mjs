// Social card for the intro: a 1200x630 capture of the page's own stage (the eight-stage ring), not a separate design.
//   node design/fractal2/og.mjs      (needs python3 design/fractal2/serve.py 8802 running)
import { createRequire } from "module"; import path from "path";
const require = createRequire(import.meta.url); const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const b = await chromium.launch({ args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
const c = await b.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, colorScheme: "dark" });
const p = await c.newPage(); await p.goto("http://127.0.0.1:8802/fractal2", { waitUntil: "load" }); await p.waitForTimeout(600);
await p.evaluate(() => { const f = document.querySelector('.fig[data-fig="cycle"]'); scrollTo(0, f.getBoundingClientRect().top + scrollY + f.getBoundingClientRect().height - innerHeight * 0.9); });
await p.waitForTimeout(2200);
await p.evaluate(() => { document.querySelector("main").style.visibility = "hidden"; document.getElementById("bar").style.display = "none"; document.getElementById("labels").style.display = "none";
  const s = document.querySelector(".nf-seal"); if (s) s.style.display = "none";
  const d = document.createElement("div"); d.style.cssText = "position:fixed;left:80px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;z-index:5;max-width:560px";
  d.innerHTML = '<p class="kicker">Noble Father Creations · Shae Stovell</p><h1 class="title" style="font-size:132px;margin:0 0 24px">Fractal<sup>2</sup></h1><p class="tagline" style="font-size:34px;margin:0">The closer you look, the more there is.</p>'; document.body.appendChild(d); });
await p.waitForTimeout(300);
await p.screenshot({ path: path.join(ROOT, "library/fractal2/site/fractal2/_a/og/intro.png") }); await b.close(); console.log("og written");
