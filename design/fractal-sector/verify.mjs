// Fractal sector verify.  node design/fractal-sector/verify.mjs ent
// Static checks on EVERY page, browser checks on every page at 1440 and a sample at 375 + reduced motion + axe.
// Serves the publish dir the way Netlify does (extensionless -> .html). Exits 1 on any failure.
import fs from "fs"; import path from "path"; import http from "http"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const sector = process.argv[2] || "ent";
const out = path.join(ROOT, "library/fractal/sectors", sector);
const site = path.join(out, "site");
const man = JSON.parse(fs.readFileSync(path.join(out, "manifest.json"), "utf8"));
const base = man.base;
let axeSrc = null; try { axeSrc = fs.readFileSync(require.resolve("axe-core/axe.min.js", { paths: [ROOT] }), "utf8"); } catch {}
const results = []; const T = (name, ok, detail = "") => results.push({ name, ok, detail });

// ---- static ----
const files = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : p.endsWith(".html") && files.push(p); } })(site);
const urlOf = f => "/" + path.relative(site, f).replace(/\.html$/, "");
const exists = u => { u = u.split("#")[0].replace(/\/$/, ""); return fs.existsSync(path.join(site, u + ".html")) || fs.existsSync(path.join(site, u)); };
const pages = files.map(urlOf);
const strip = h => h.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "").replace(/<[^>]+>/g, " ");
let broken = [], leaks = [], seo = [], safety = [], ids = [], ld = [];
for (const f of files) {
  const h = fs.readFileSync(f, "utf8"), u = urlOf(f), text = strip(h);
  for (const m of h.matchAll(/href="(\/[^"]*)"/g)) if (m[1].startsWith(base) && !exists(m[1])) broken.push(`${u} -> ${m[1]}`);
  for (const bad of ["SPEAK]", "HARD CUT]", "[SPEAK]", "[HARD CUT]", "Credibility Audit", "{{", "#REPLACE", "data-here", "status: draft"]) if (text.includes(bad)) leaks.push(`${u}: ${bad}`);
  if (/\bC\d{3}\b/.test(text) || /href="[^"]*\bC\d{3}\b/i.test(h)) ids.push(u);
  const ent = x => x.replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
  const title = ent((h.match(/<title>([^<]*)/) || [])[1] || ""), desc = ent((h.match(/name="description" content="([^"]*)/) || [])[1] || "");
  if (!title || !desc || !h.includes('rel="canonical"') || !h.includes('og:image') || desc.length > 160) seo.push(`${u} (title ${title.length}, desc ${desc.length})`);
  try { JSON.parse(h.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]); } catch { ld.push(u); }
  const slug = u.split("/").pop(), exp = man.expect[slug];
  if (exp) {
    const hasNote = h.includes('class="safety"');
    if (exp.safety !== hasNote) safety.push(`${u}: safety note expected=${exp.safety} found=${hasNote}`);
    if (exp.safety && h.indexOf('class="safety"') > h.indexOf('id="the-scene"')) safety.push(`${u}: safety note is not at the top`);
    for (const id of ["when-to-get-help-and-where", "words-you-could-use"]) if (!h.includes(`id="${id}"`)) safety.push(`${u}: missing ${id}`);
  }
}
const sm = fs.readFileSync(path.join(site, base.slice(1), "sitemap.xml"), "utf8");
T(`${files.length} pages built, matches manifest (${man.pages})`, files.length === man.pages);
T("every internal link resolves", !broken.length, broken.slice(0, 5).join(" | "));
T("no production cues, audit text, placeholders or draft markers on any page", !leaks.length, leaks.slice(0, 5).join(" | "));
T("no internal C-numbers in reader text or URLs", !ids.length, ids.slice(0, 5).join(" | "));
T("title, description (<=160), canonical and og:image on every page", !seo.length, seo.slice(0, 5).join(" | "));
T("structured data parses on every page", !ld.length, ld.slice(0, 5).join(" | "));
T("safety notes present and first where the script has one; escalation + safer language never dropped", !safety.length, safety.slice(0, 5).join(" | "));
T(`sitemap lists every page (${(sm.match(/<loc>/g) || []).length})`, (sm.match(/<loc>/g) || []).length === files.length);
const ogMissing = man.og.filter(n => !fs.existsSync(path.join(site, base.slice(1), "og", n + ".png")));
T("social card image exists for every card", !ogMissing.length, ogMissing.slice(0, 5).join(" "));

// ---- browser ----
const types = { ".html": "text/html; charset=utf-8", ".woff2": "font/woff2", ".png": "image/png", ".xml": "application/xml" };
const srv = http.createServer((q, r) => {
  let u = decodeURIComponent(q.url.split("?")[0]); let p = path.join(site, u);
  if (!path.extname(p) && fs.existsSync(p + ".html")) p += ".html";
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end("nf"); }
  r.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(r);
}).listen(0);
const port = srv.address().port, O = `http://127.0.0.1:${port}`;
const browser = await chromium.launch();
const words = s => (s.match(/[A-Za-z0-9][A-Za-z0-9'’.,%$-]*/g) || []).filter(w => !/^\d+\.$/.test(w)).length;
let errs = [], overflow = [], wc = [], hidden = [], external = [];
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.route("**/*", r => { const u = r.request().url(); if (!u.startsWith(O)) { external.push(u); return r.abort(); } return r.continue(); });
const p = await ctx.newPage(); p.on("pageerror", e => errs.push(`${p.url()}: ${e.message}`));
for (const u of pages) {
  await p.goto(O + u, { waitUntil: "load" });
  if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) overflow.push("1440 " + u);
  const slug = u.split("/").pop(), exp = man.expect[slug];
  if (exp) {
    const got = await p.evaluate(() => { const st = document.createElement("style"); st.textContent = ".tg{display:none!important}"; document.head.append(st);
      document.querySelectorAll(".toc details").forEach(d => d.open = true);
      const t = [...document.querySelectorAll("[data-src]")].filter(e => !e.parentElement.closest("[data-src]")).map(e => e.innerText).join(" "); st.remove(); return t; });
    const n = words(got); if (n !== exp.words) wc.push(`${slug}: source ${exp.words}, page ${n}`);
  }
}
T(`no page errors on ${pages.length} pages`, !errs.length, errs.slice(0, 3).join(" | "));
T("no horizontal overflow at 1440", !overflow.length, overflow.slice(0, 5).join(" "));
T(`author word count round trip on every combo (${Object.keys(man.expect).length})`, !wc.length, wc.slice(0, 6).join(" | "));
const allowedExt = /static\.cloudflareinsights\.com/;
T("no external requests except the sanctioned analytics beacon", !external.filter(u => !allowedExt.test(u)).length, external.filter(u => !allowedExt.test(u)).slice(0, 3).join(" "));

const sample = [base, `${base}/stage-control`, `${base}/a-z`, `${base}/standards`, ...pages.filter(u => u.includes("/family-")).slice(0, 2),
  `${base}/the-debt-prison`, `${base}/grooming`, `${base}/the-room`, `${base}/pavlovian-conditioning`];
let axeBad = [], ov375 = [], stuck = [];
for (const [vw, rm] of [[375, "no-preference"], [375, "reduce"], [1440, "reduce"]]) {
  const c = await browser.newContext({ viewport: { width: vw, height: 800 }, reducedMotion: rm });
  const q = await c.newPage(); q.on("pageerror", e => errs.push(e.message));
  for (const u of sample) {
    await q.goto(O + u, { waitUntil: "load" });
    if (await q.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) ov375.push(`${vw}/${rm} ${u}`);
    await q.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await q.waitForTimeout(150);
    const z = await q.evaluate(() => [...document.querySelectorAll("main *")].filter(e => getComputedStyle(e).opacity === "0" && e.offsetHeight > 0).length);
    if (z) stuck.push(`${u}: ${z}`);
    if (axeSrc && rm === "no-preference") {
      await q.addScriptTag({ content: axeSrc });
      const v = await q.evaluate(() => axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa", "best-practice"] } })
        .then(r => r.violations.filter(x => ["serious", "critical"].includes(x.impact)).map(x => `${x.id}(${x.nodes.length}) ${x.nodes[0].target.join(" ")}`)));
      v.forEach(x => axeBad.push(`${u}: ${x}`));
    }
  }
  await c.close();
}
T("no horizontal overflow at 375 (both motion settings) and 1440 reduced", !ov375.length, ov375.slice(0, 5).join(" | "));
T("nothing stuck invisible after scrolling", !stuck.length, stuck.slice(0, 5).join(" | "));
T(axeSrc ? `axe: no serious or critical violations (${sample.length} pages at 375)` : "axe-core missing (npm i --no-save axe-core)", axeSrc && !axeBad.length, axeBad.slice(0, 6).join(" | "));
await browser.close(); srv.close();

let fail = 0; for (const r of results) { if (!r.ok) fail++; console.log(`${r.ok ? "PASS" : "FAIL"}  ${r.name}${r.ok || !r.detail ? "" : "\n      " + r.detail}`); }
console.log(`\n${results.length - fail}/${results.length} checks passed`); process.exit(fail ? 1 : 0);
