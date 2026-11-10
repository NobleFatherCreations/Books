// Review material for the owner: a scroll recording and stills of the intro.
//   node design/fractal2/record.mjs <outdir> [phone|desktop]      (needs python3 design/fractal2/serve.py 8802 running)
// Writes <outdir>/intro-<device>.webm (convert with ffmpeg) and <outdir>/stills-<device>/NN-<figure>.png
import { createRequire } from "module"; import fs from "fs"; import path from "path";
const require = createRequire(import.meta.url); const { chromium } = require("playwright");
const out = process.argv[2], dev = process.argv[3] || "phone";
const vp = dev === "phone" ? { width: 390, height: 844 } : { width: 1280, height: 720 };
fs.mkdirSync(path.join(out, "stills-" + dev), { recursive: true });
const b = await chromium.launch({ args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });

// stills: every figure at its final state
{ const c = await b.newContext({ viewport: vp, deviceScaleFactor: 2, colorScheme: "dark", hasTouch: dev === "phone", isMobile: dev === "phone" });
  const p = await c.newPage(); await p.goto("http://127.0.0.1:8802/fractal2", { waitUntil: "load" }); await p.waitForTimeout(900);
  await p.screenshot({ path: path.join(out, "stills-" + dev, "00-title.png") });
  const figs = await p.evaluate(() => [...document.querySelectorAll(".fig")].map(e => ({ n: e.dataset.fig, top: e.getBoundingClientRect().top + scrollY, h: e.getBoundingClientRect().height })));
  let i = 1;
  for (const f of figs) { await p.evaluate(y => scrollTo(0, y), f.top + f.h - vp.height * (f.h > vp.height * 2.2 ? 1.25 : 1.05)); await p.waitForTimeout(1700);
    await p.screenshot({ path: path.join(out, "stills-" + dev, String(i++).padStart(2, "0") + "-" + f.n + ".png") }); }
  await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(1500);
  await p.screenshot({ path: path.join(out, "stills-" + dev, String(i).padStart(2, "0") + "-enter.png") });
  await c.close(); console.log("stills", i + 1); }

// recording: one steady scroll down the whole page
{ const c = await b.newContext({ viewport: vp, deviceScaleFactor: 1, colorScheme: "dark", hasTouch: dev === "phone", isMobile: dev === "phone", recordVideo: { dir: out, size: vp } });
  const p = await c.newPage(); await p.goto("http://127.0.0.1:8802/fractal2", { waitUntil: "load" }); await p.waitForTimeout(1500);
  await p.evaluate(() => { const s = document.querySelector(".nf-seal"); if (s) s.style.display = "none"; });
  const speed = dev === "phone" ? 520 : 560;      // px per second
  await p.evaluate(async sp => { const H = document.documentElement.scrollHeight - innerHeight; let t0 = performance.now(), y = 0;
    await new Promise(res => { function f(now) { y = Math.min(H, (now - t0) / 1000 * sp); scrollTo(0, y); if (y < H) requestAnimationFrame(f); else setTimeout(res, 2500); } requestAnimationFrame(f); }); }, speed);
  const v = p.video(); await c.close(); const src = await v.path(); fs.renameSync(src, path.join(out, "intro-" + dev + ".webm")); console.log("video", "intro-" + dev + ".webm"); }
await b.close();
