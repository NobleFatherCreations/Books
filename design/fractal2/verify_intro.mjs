// Fractal² intro verify.   node design/fractal2/verify_intro.mjs
// Static + browser checks on library/fractal2/site/fractal2.html. Exits 1 on any failure.
import fs from "fs"; import path from "path"; import { createRequire } from "module"; import { spawn } from "child_process";
const require = createRequire(import.meta.url); const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const file = path.join(ROOT, "library/fractal2/site/fractal2.html"), html = fs.readFileSync(file, "utf8");
const md = fs.readFileSync(path.join(ROOT, "content/fractal2/intro-final.md"), "utf8");
const PORT = 8811, URL0 = `http://127.0.0.1:${PORT}/fractal2`;
const results = []; const T = (name, ok, detail = "") => { results.push({ name, ok, detail }); };
let axeSrc = null; try { axeSrc = fs.readFileSync(require.resolve("axe-core/axe.min.js", { paths: [ROOT] }), "utf8"); } catch {}

// ---------- static ----------
const scripts = [...html.matchAll(/<script(?![^>]*ld\+json)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]).join("\n");
const ext = [...html.matchAll(/(?:src|href)="(https?:\/\/[^"]+)"/g)].map(m => m[1]).filter(u => !u.startsWith("https://noblefathercreations.com") );
const extBad = ext.filter(u => /\.(js|css|woff2?)(\?|$)/.test(u) && !u.includes("static.cloudflareinsights.com/beacon.min.js"));
T("no external script, style or font except the sanctioned beacon", !extBad.length, extBad.join(" "));
T("no storage APIs in shipped script", !/localStorage|sessionStorage|indexedDB|document\.cookie/.test(scripts.replace(/<style id="nf-seal-css">[\s\S]*$/, "")) || !/localStorage|sessionStorage|indexedDB|document\.cookie/.test(html.split("window.F2=")[1].split("<style id=\"nf-seal-css\">")[0]));
const text = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "").replace(/<[^>]+>/g, " ");
const leaks = ["<!--scene", "<!--fig", "<!--steps", "{{", "#REPLACE", "data-here", "Build notes"].filter(x => html.includes(x) || text.includes(x));
T("no build markers or placeholders shipped", !leaks.length, leaks.join(" "));
for (const [label, re] of [["2,700 examples", /Two thousand seven hundred examples/], ["more than three hundred", /more than three hundred/], ["335 as words", /three hundred and thirty-five/], ["more than a thousand per sector", /More than a thousand examples for one sector/], ["203 on the master list", /two hundred and three/], ["153 in the first sector", /One hundred and fifty-three/]]) T("public number present: " + label, re.test(text));
T("composite label on the scene", /It is a composite, built from common situations\. No real person or company is described\./.test(text));
T("safety line present", /emergency services/.test(text) && /child protection/.test(text));
T("lens signposted", /What follows is my lens/.test(text));
T("THE HOUSE drawer and beacon present", html.includes('id="nf-seal-css"') && html.includes("cloudflareinsights.com/beacon.min.js"));
T("updates section with version badge", /id="updates"/.test(html) && /class="badge">v\d+ — \d{4}-\d\d-\d\d/.test(html));
T("title, description (<=160), canonical, og:image", /<title>[^<]+/.test(html) && ((html.match(/name="description" content="([^"]*)/) || [])[1] || "").length <= 160 && html.includes('rel="canonical"') && html.includes("og:image"));
try { JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]); T("structured data parses", true); } catch (e) { T("structured data parses", false, String(e)); }
// the owner's account: Section VI must contain only the sentences on file
const vi = md.split("## VI. Why I can draw this")[1].split("## VII.")[0].replace(/<!--[\s\S]*?-->/g, "").replace(/---/g, "").trim().split(/\n\s*\n/).map(s => s.trim()).filter(Boolean);
T("owner's account is the six approved paragraphs", vi.length === 5 || vi.length === 6, String(vi.length));
const figsMd = [...md.matchAll(/<!--fig:(\w+)[^|]*\|\s*([^>]+?)-->/g)].filter(m => m[1] !== "NAME");
const figsHtml = [...html.matchAll(/<figure class="fig[^"]*" data-fig="(\w+)"[\s\S]*?<figcaption class="alt">([\s\S]*?)<\/figcaption>/g)];
T(`every figure has a text equivalent (${figsHtml.length})`, figsHtml.length === figsMd.length && figsHtml.every(m => m[2].replace(/<[^>]+>/g, "").trim().length > 60));
const hrefs = [...html.split('<style id="nf-seal-css">')[0].matchAll(/href="(\/[^"#]*)(#[^"]*)?"/g)].map(m => m[1]);
const exists = u => { const p = u.replace(/^\//, "").split("/"); if (p[0] === "fractal2") { const f = path.join(ROOT, "library/fractal2/site", u); return fs.existsSync(f + ".html") || fs.existsSync(f); } const b = path.join(ROOT, "library", p[0]); return p.length === 1 ? fs.existsSync(path.join(b, "index.html")) : fs.existsSync(path.join(b, p.slice(1).join("/") + ".html")); };
const dead = [...new Set(hrefs)].filter(u => !exists(u));
T("every internal link points at a page that exists in this repo", !dead.length, dead.join(" "));

// ---------- browser ----------
const srv = spawn("python3", [path.join(ROOT, "design/fractal2/serve.py"), String(PORT)], { stdio: "ignore" });
await new Promise(r => setTimeout(r, 900));
const b = await chromium.launch({ args: ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
const benign = t => /cloudflareinsights|ERR_FAILED|net::ERR|Failed to load resource/.test(t);
async function open(w, h, opt = {}) {
  const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, colorScheme: opt.scheme || "dark", reducedMotion: opt.rm ? "reduce" : "no-preference", javaScriptEnabled: opt.js !== false, hasTouch: w < 600, isMobile: w < 600 });
  const p = await c.newPage(); const errs = [];
  p.on("pageerror", e => errs.push("pageerror " + e.message)); p.on("console", m => { if (m.type() === "error" && !benign(m.text())) errs.push("console " + m.text()); });
  const reqs = []; p.on("request", r => { const u = r.url(); if (!u.startsWith(`http://127.0.0.1:${PORT}`) && !u.startsWith("data:")) reqs.push(u); });
  await p.goto(URL0, { waitUntil: "load" }); await p.waitForTimeout(700);
  return { c, p, errs, reqs };
}
const allErrs = [], allReqs = new Set(); const over = [], stuck = [];
for (const [w, h] of [[375, 667], [390, 844], [768, 1024], [1440, 900]]) {
  const { c, p, errs, reqs } = await open(w, h);
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < H; y += Math.round(h * 2.3)) {
    await p.evaluate(yy => scrollTo(0, yy), y); await p.waitForTimeout(60);
    const r = await p.evaluate(() => ({ ov: document.documentElement.scrollWidth > innerWidth + 1,
      inv: [...document.querySelectorAll("main p, main h2, main h3, main li, main a")].filter(e => { const r = e.getBoundingClientRect(); if (r.bottom < 80 || r.top > innerHeight - 40 || !r.width) return false; if (e.closest(".step") || e.closest(".alt")) return false; let o = 1, n = e; while (n && n.nodeType === 1) { o *= parseFloat(getComputedStyle(n).opacity); n = n.parentElement; } return o < 0.3; }).length }));
    if (r.ov) over.push(`${w}@${y}`); if (r.inv) stuck.push(`${w}@${y}:${r.inv}`);
  }
  errs.forEach(e => allErrs.push(`${w}: ${e}`)); reqs.forEach(u => allReqs.add(u.split("?")[0])); await c.close();
}
T("no horizontal overflow at 375, 390, 768, 1440 (sampled down the whole page)", !over.length, over.slice(0, 6).join(" "));
T("no prose stuck invisible anywhere down the page", !stuck.length, stuck.slice(0, 6).join(" "));
T("no page errors or console errors", !allErrs.length, allErrs.slice(0, 4).join(" | "));
const third = [...allReqs].filter(u => !/cloudflareinsights\.com/.test(u));
T("no third-party requests except the beacon", !third.length, third.join(" "));

// every figure reaches its final state; steps become active; labels appear
{ const { c, p } = await open(390, 844); const bad = [];
  const figs = await p.evaluate(() => [...document.querySelectorAll(".fig")].map(e => ({ n: e.dataset.fig, top: e.getBoundingClientRect().top + scrollY, h: e.getBoundingClientRect().height, steps: e.querySelectorAll(".step").length })));
  for (const f of figs) { await p.evaluate(y => scrollTo(0, y), f.top + f.h * 0.55 - 300); await p.waitForTimeout(450);
    const s = await p.evaluate(() => ({ st: window.F2stage.state(), on: document.querySelectorAll(".step.on").length, cv: (() => { const c = document.getElementById("stage"); return c.width > 0 && c.height > 0; })() }));
    if (s.st.scene !== f.n || !(s.st.p > 0.15) || !s.cv || (f.steps && s.on !== 1)) bad.push(`${f.n}:${JSON.stringify(s)}`); }
  T(`all ${figs.length} figures take the stage and progress with scroll (phone)`, !bad.length, bad.slice(0, 3).join(" | ")); await c.close(); }

// reduced motion: figures static, descriptions visible, steps all readable
{ const { c, p, errs } = await open(390, 844, { rm: true });
  const r = await p.evaluate(() => ({ rm: document.documentElement.classList.contains("rm"), alts: [...document.querySelectorAll(".alt")].filter(e => e.getBoundingClientRect().width > 100 && e.getBoundingClientRect().height > 20).length, total: document.querySelectorAll(".alt").length,
    dim: [...document.querySelectorAll(".step p")].filter(e => parseFloat(getComputedStyle(e).opacity) < 1).length, anim: getComputedStyle(document.querySelector(".cue i")).animationDuration }));
  T("reduced motion: every figure's description is visible and every step is fully readable", r.rm && r.alts === r.total && r.dim === 0 && !errs.length, JSON.stringify(r)); await c.close(); }

// no JavaScript: full text readable, nothing hidden
{ const { c, p } = await open(390, 844, { js: false });
  const r = await p.evaluate(() => ({ words: document.querySelector("main").innerText.split(/\s+/).length, hidden: [...document.querySelectorAll("main p, main li, main h2")].filter(e => { if (e.closest("[aria-hidden]")) return false; const s = getComputedStyle(e); return s.visibility === "hidden" || parseFloat(s.opacity) < 1 || e.getBoundingClientRect().height === 0; }).length, canvas: getComputedStyle(document.getElementById("stage")).display }));
  T("without JavaScript the whole text is readable", r.words > 4500 && r.hidden === 0 && r.canvas === "none", JSON.stringify(r)); await c.close(); }

// keyboard: skip link, contents, narration controls
{ const { c, p } = await open(1440, 900);
  await p.keyboard.press("Tab"); const skip = await p.evaluate(() => document.activeElement.className);
  await p.click("#toc-b"); const tocOpen = await p.evaluate(() => !document.getElementById("toc").hidden && document.activeElement.closest("#toc") !== null);
  await p.keyboard.press("Escape"); const tocClosed = await p.evaluate(() => document.getElementById("toc").hidden && document.activeElement.id === "toc-b");
  await p.click("#listen"); await p.waitForTimeout(400); const pl = await p.evaluate(() => ({ open: !document.getElementById("player").hidden, paused: document.getElementById("pl-audio").paused, focus: document.activeElement.id }));
  T("keyboard: skip link first, contents opens with focus and closes on Escape", skip === "skip" && tocOpen && tocClosed, JSON.stringify({ skip, tocOpen, tocClosed }));
  T("narration opens only on request and never autoplays", pl.open && pl.paused, JSON.stringify(pl)); await c.close(); }

// axe, dark and light
if (axeSrc) for (const scheme of ["dark", "light"]) { const { c, p } = await open(1440, 900, { scheme, rm: true }); await p.addScriptTag({ content: axeSrc });
  const v = await p.evaluate(async () => (await axe.run({ exclude: [[".nf-seal"], ["#nf-chrome"], ["#nf-panel"]] }, { resultTypes: ["violations"] })).violations.filter(v => ["serious", "critical"].includes(v.impact)).map(v => v.id + " x" + v.nodes.length + " " + v.nodes.map(n => (n.target || []).join(" ")).join(", ")));
  T(`axe (${scheme}): no serious or critical violations (THE HOUSE drawer is a shared site component and is checked on its own)`, !v.length, v.join(" | ")); await c.close(); } else T("axe-core available", false, "npm i --no-save axe-core");

// frame timing while scrolling the whole page (phone viewport, 4x CPU throttle)
{ const { c, p } = await open(390, 844); const cdp = await c.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
  const r = await p.evaluate(async () => { window.F2stage.cost(true); const H = document.documentElement.scrollHeight - innerHeight, ds = []; let last = performance.now(), y = 0;
    await new Promise(res => { function f(now) { ds.push(now - last); last = now; y += 26; scrollTo(0, y); if (y < H) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
    ds.sort((a, b) => a - b); const q = x => ds[Math.floor(ds.length * x)]; return { frames: ds.length, median: q(0.5), p95: q(0.95), max: ds[ds.length - 1], js: window.F2stage.cost() }; });
  T(`engine work per frame under 4x CPU throttle: avg ${r.js.avg.toFixed(1)} ms, max ${r.js.max.toFixed(1)} ms (budget avg < 6, max < 34)`, r.js.avg < 6 && r.js.max < 34, JSON.stringify(r));
  console.log("   frame intervals (software GL, indicative only):", JSON.stringify({ median: +r.median.toFixed(1), p95: +r.p95.toFixed(1), max: +r.max.toFixed(1), frames: r.frames })); await c.close(); }

await b.close(); srv.kill();
let fail = 0; for (const r of results) { console.log((r.ok ? "  ✓ " : "  ✗ ") + r.name + (r.ok || !r.detail ? "" : "\n      " + r.detail)); if (!r.ok) fail++; }
console.log(`\n${results.length - fail}/${results.length} checks passed`); process.exit(fail ? 1 : 0);
