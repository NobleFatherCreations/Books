// Fractal² sector verify.  node design/fractal-sector/verify.mjs ent
// Static checks on EVERY page, browser checks on every page at 1440, a sample at 375 + reduced motion + axe, and the
// behaviour checks for the new navigation (modes, filters, search). Serves the publish dir the way Netlify does
// (extensionless -> .html). Exits 1 on any failure.
import fs from "fs"; import path from "path"; import http from "http"; import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const sector = process.argv[2] || "ent";
const site = path.join(ROOT, "library/fractal2/site");
const man = JSON.parse(fs.readFileSync(path.join(ROOT, "library/fractal2/manifests", sector + ".json"), "utf8"));
const base = man.base, root = man.root;
let axeSrc = null; try { axeSrc = fs.readFileSync(require.resolve("axe-core/axe.min.js", { paths: [ROOT] }), "utf8"); } catch {}
const results = []; const T = (name, ok, detail = "") => results.push({ name, ok: !!ok, detail });

// ---- static (this sector's own pages only: the intro is built by another program) ----
const secDir = path.join(site, base.slice(1));
const files = [path.join(site, base.slice(1) + ".html")];
(function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : p.endsWith(".html") && files.push(p); } })(secDir);
const urlOf = f => "/" + path.relative(site, f).replace(/\.html$/, "");
const exists = u => { u = u.split("#")[0].split("?")[0].replace(/\/$/, ""); return fs.existsSync(path.join(site, u + ".html")) || (fs.existsSync(path.join(site, u)) && fs.statSync(path.join(site, u)).isFile()); };
const pages = files.map(urlOf);
const strip = h => h.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "").replace(/<[^>]+>/g, " ");
const idCache = {};
const idsOf = f => idCache[f] || (idCache[f] = new Set([...fs.readFileSync(f, "utf8").matchAll(/id="([^"]+)"/g)].map(m => m[1])));
let broken = [], leaks = [], seo = [], safety = [], ids = [], ld = [], xlinks = [], storage = [], xcount = 0;
for (const f of files) {
  const h = fs.readFileSync(f, "utf8"), u = urlOf(f), text = strip(h);
  for (const m of h.matchAll(/href="(\/[^"]*)"/g)) {
    const href = m[1];
    if (href.startsWith(base) && !exists(href)) broken.push(`${u} -> ${href}`);
    const pm = href.match(/^\/(playbook|fractal)(?:\/([^#?]*))?(?:#(.*))?$/);
    if (pm) {
      xcount++;
      const dir = pm[1] === "playbook" ? path.join(ROOT, "instruments/playbook/site") : path.join(ROOT, "library/fractal");
      const file = pm[2] ? path.join(dir, pm[2] + ".html") : path.join(dir, "index.html");
      if (!fs.existsSync(file)) xlinks.push(`${u} -> ${href} (no file)`);
      else if (pm[3] && !idsOf(file).has(pm[3])) xlinks.push(`${u} -> ${href} (no anchor)`);
    }
  }
  for (const bad of ["SPEAK]", "HARD CUT]", "[SPEAK]", "[HARD CUT]", "Credibility Audit", "{{", "#REPLACE", "data-here", "status: draft"]) if (text.includes(bad)) leaks.push(`${u}: ${bad}`);
  if (/\b[CT]\d{3}\b/.test(text) || /href="[^"]*\b[CT]\d{3}\b/i.test(h)) ids.push(u);
  const ent = x => x.replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
  const title = ent((h.match(/<title>([^<]*)/) || [])[1] || ""), desc = ent((h.match(/name="description" content="([^"]*)/) || [])[1] || "");
  if (!title || !desc || !h.includes('rel="canonical"') || !h.includes('og:image') || desc.length > 160) seo.push(`${u} (title ${title.length}, desc ${desc.length})`);
  try { JSON.parse(h.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]); } catch { ld.push(u); }
  for (const s of h.matchAll(/<script(?![^>]*application\/ld\+json)[^>]*>([\s\S]*?)<\/script>/g)) {
    const js = s[1];
    for (const bad of ["localStorage", "sessionStorage", "document.cookie", "indexedDB"]) if (js.includes(bad)) storage.push(`${u}: ${bad}`);
    for (const fm of js.matchAll(/fetch\(\s*(['"`])(https?:)?\/\//g)) storage.push(`${u}: fetch to another origin`);
  }
  const slug = u.slice(base.length + 1), exp = man.expect[slug];
  if (exp) {
    const hasNote = h.includes('class="safety"');
    if (exp.safety !== hasNote) safety.push(`${u}: safety note expected=${exp.safety} found=${hasNote}`);
    if (exp.safety && h.indexOf('class="safety"') > h.indexOf('id="the-scene"')) safety.push(`${u}: safety note is not at the top`);
    if (exp.safety && !/class="safety"[^>]*data-m="quick seq full"/.test(h)) safety.push(`${u}: safety note not in every reading mode`);
    for (const id of ["when-to-get-help-and-where", "words-you-could-use"]) if (!h.includes(`id="${id}"`)) safety.push(`${u}: missing ${id}`);
  }
}
const sm = fs.readFileSync(path.join(secDir, "sitemap.xml"), "utf8");
T(`${files.length} pages built, matches manifest (${man.pages})`, files.length === man.pages);
T("every internal link resolves", !broken.length, broken.slice(0, 5).join(" | "));
T("no production cues, audit text, placeholders or draft markers on any page", !leaks.length, leaks.slice(0, 5).join(" | "));
T("no internal C- or T-numbers in reader text or URLs", !ids.length, ids.slice(0, 5).join(" | "));
T("title, description (<=160), canonical and og:image on every page", !seo.length, seo.slice(0, 5).join(" | "));
T("structured data parses on every page", !ld.length, ld.slice(0, 5).join(" | "));
T("safety notes present and first where the script has one; escalation + safer language never dropped", !safety.length, safety.slice(0, 5).join(" | "));
T(`sitemap lists every page (${(sm.match(/<loc>/g) || []).length})`, (sm.match(/<loc>/g) || []).length === files.length);
const ogMissing = man.og.filter(n => !fs.existsSync(path.join(secDir, "og", n + ".png")));
T("social card image exists for every card", !ogMissing.length, ogMissing.slice(0, 5).join(" "));
// new static checks
const reserved = ["", "start", "patterns", "tactics", "map", "notice", "in-it-now", "worried-about-someone", "before-you-sign", "method", "take-it-with-you", "a-z",
  ...man.groups.stages, ...man.groups.families];
const missingRes = reserved.filter(p => !exists(p ? `${base}/${p}` : base));
const collide = man.groups.combos.filter(s => man.reserved.includes(s) || /^(stage|family)-/.test(s));
T(`every reserved address exists (${reserved.length}); no combo slug collides with one`, !missingRes.length && !collide.length, [...missingRes, ...collide].join(" "));
let tacBad = [];
for (const p of man.groups.tactics) { const h = fs.readFileSync(path.join(secDir, p + ".html"), "utf8"); const n = (h.match(/class="lv lv-/g) || []).length; if (n !== 3) tacBad.push(`${p}: ${n} levels`); }
T(`${man.groups.tactics.length} tactic pages exist and each shows three levels`, man.groups.tactics.length === 335 && !tacBad.length, tacBad.slice(0, 5).join(" | "));
T(`every /playbook and /fractal link (${xcount}) points at a file and anchor in this repo`, !xlinks.length, xlinks.slice(0, 5).join(" | "));
T("no storage, cookies or cross-origin fetch in any shipped script", !storage.length, storage.slice(0, 5).join(" | "));

// ---- browser ----
const types = { ".html": "text/html; charset=utf-8", ".woff2": "font/woff2", ".png": "image/png", ".xml": "application/xml", ".json": "application/json" };
const srv = http.createServer((q, r) => {
  let u = decodeURIComponent(q.url.split("?")[0]); let p = path.join(site, u);
  if (!path.extname(p) && fs.existsSync(p + ".html")) p += ".html";
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end("nf"); }
  r.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(r);
}).listen(0);
const port = srv.address().port, O = `http://127.0.0.1:${port}`;
const browser = await chromium.launch();
const words = s => (s.match(/[A-Za-z0-9][A-Za-z0-9'’.,%$-]*/g) || []).filter(w => !/^\d+\.$/.test(w)).length;
let errs = [], overflow = [], wc = [], external = [];
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
await ctx.route("**/*", r => { const u = r.request().url(); if (!u.startsWith(O)) { external.push(u); return r.abort(); } return r.continue(); });
const p = await ctx.newPage(); p.on("pageerror", e => errs.push(`${p.url()}: ${e.message}`));
for (const u of pages) {
  await p.goto(O + u, { waitUntil: "load" });
  if (await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) overflow.push("1440 " + u);
  const exp = man.expect[u.slice(base.length + 1)];
  if (exp) {
    const got = await p.evaluate(() => { const st = document.createElement("style"); st.textContent = ".tg{display:none!important}"; document.head.append(st);
      document.querySelectorAll(".toc details").forEach(d => d.open = true);
      const t = [...document.querySelectorAll("[data-src]")].filter(e => !e.parentElement.closest("[data-src]")).map(e => e.innerText).join(" "); st.remove(); return t; });
    const n = words(got); if (n !== exp.words) wc.push(`${u}: source ${exp.words}, page ${n}`);
  }
}
T(`no page errors on ${pages.length} pages`, !errs.length, errs.slice(0, 3).join(" | "));
T("no horizontal overflow at 1440", !overflow.length, overflow.slice(0, 5).join(" "));
T(`author word count round trip on every combo (${Object.keys(man.expect).length})`, !wc.length, wc.slice(0, 6).join(" | "));
const allowedExt = /static\.cloudflareinsights\.com/;
T("no external requests except the sanctioned analytics beacon", !external.filter(u => !allowedExt.test(u)).length, external.filter(u => !allowedExt.test(u)).slice(0, 3).join(" "));

const fam = man.groups.families, tac = man.groups.tactics;
const sample = [base, `${base}/start`, `${base}/patterns`, `${base}/tactics`, `${base}/stage-control`, `${base}/a-z`, `${base}/method`, `${base}/take-it-with-you`,
  `${base}/notice`, `${base}/in-it-now`, `${base}/worried-about-someone`, `${base}/before-you-sign`, `${base}/map`,
  `${base}/${fam[0]}`, `${base}/${fam[1]}`, `${base}/tactic/love-bombing`, `${base}/${tac[200]}`,
  `${base}/the-debt-prison`, `${base}/grooming`, `${base}/the-room`, `${base}/pavlovian-conditioning`];
let axeBad = [], ov375 = [], stuck = [];
const runAxe = async q => { await q.addScriptTag({ content: axeSrc });
  return q.evaluate(() => axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa", "best-practice"] } })
    .then(r => r.violations.filter(x => ["serious", "critical"].includes(x.impact)).map(x => `${x.id}(${x.nodes.length}) ${x.nodes[0].target.join(" ")}`))); };
const zeroOpacity = q => q.evaluate(() => [...document.querySelectorAll("main *")].filter(e => getComputedStyle(e).opacity === "0" && e.offsetHeight > 0
  && !e.closest("[hidden],[aria-hidden=true]")).length);
for (const [vw, rm, cs] of [[375, "no-preference", "light"], [375, "no-preference", "dark"], [375, "reduce", "light"], [1440, "reduce", "dark"]]) {
  const c = await browser.newContext({ viewport: { width: vw, height: 800 }, reducedMotion: rm, colorScheme: cs });
  const q = await c.newPage(); q.on("pageerror", e => errs.push(e.message));
  for (const u of sample) {
    await q.goto(O + u, { waitUntil: "load" });
    if (await q.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) ov375.push(`${vw}/${rm}/${cs} ${u}`);
    // axe runs at the top of the page: after scrolling, sticky bars legitimately sit over links and axe reads that as overlap
    if (axeSrc && rm === "no-preference") (await runAxe(q)).forEach(x => axeBad.push(`${cs} ${u}: ${x}`));
    await q.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await q.waitForTimeout(150);
    const z = await zeroOpacity(q); if (z) stuck.push(`${u}: ${z}`);
  }
  await c.close();
}
T("no horizontal overflow at 375 (both motion settings) and 1440 reduced", !ov375.length, ov375.slice(0, 5).join(" | "));
T("nothing stuck invisible after scrolling", !stuck.length, stuck.slice(0, 5).join(" | "));
T(axeSrc ? `axe: no serious or critical violations (${sample.length} pages at 375, light and dark)` : "axe-core missing (npm i --no-save axe-core)", axeSrc && !axeBad.length, axeBad.slice(0, 6).join(" | "));

// ---- new behaviour checks ----
const B = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const b = await B.newPage(); b.on("pageerror", e => errs.push(e.message));
const dp = `${O}${base}/the-debt-prison`;
let modeBad = [];
await b.goto(dp, { waitUntil: "load" });
await b.click('.modes button[data-mode="quick"]');
let s = await b.evaluate(() => ({ scene: getComputedStyle(document.getElementById("the-scene")).display, hash: location.hash,
  first: [...document.querySelectorAll(".combo-body > *")].find(e => getComputedStyle(e).display !== "none")?.id,
  safety: !!document.querySelector(".safety"), help: getComputedStyle(document.getElementById("when-to-get-help-and-where")).display,
  words: getComputedStyle(document.getElementById("words-you-could-use")).display }));
if (s.scene !== "none") modeBad.push("quick read shows the scene");
if (s.hash !== "#quick") modeBad.push("quick read not in the URL hash");
if (s.help === "none" || s.words === "none") modeBad.push("quick read drops help or words");
const gr = `${O}${base}/grooming`;
await b.goto(gr + "#quick", { waitUntil: "load" });
s = await b.evaluate(() => ({ pressed: document.querySelector('.modes [aria-pressed="true"]').dataset.mode,
  first: [...document.querySelectorAll(".combo-body > *")].find(e => getComputedStyle(e).display !== "none")?.id }));
if (s.pressed !== "quick") modeBad.push("#quick deep link does not select Quick read");
if (s.first !== "safety") modeBad.push("safety note not first in Quick read (got " + s.first + ")");
await b.goto(gr + "#sequence", { waitUntil: "load" });
s = await b.evaluate(() => ({ pressed: document.querySelector('.modes [aria-pressed="true"]').dataset.mode,
  first: [...document.querySelectorAll(".combo-body > *")].find(e => getComputedStyle(e).display !== "none")?.id,
  pos: document.querySelector(".st-pos")?.textContent, links: document.querySelectorAll(".chain li").length, visibleSteps: [...document.querySelectorAll(".steps>li")].filter(li => getComputedStyle(li).display !== "none").length }));
if (s.pressed !== "seq") modeBad.push("#sequence deep link does not select The sequence");
if (s.first !== "safety") modeBad.push("safety note not first in The sequence");
if ((s.pos || "") !== `Step 1 of ${s.links}` || s.visibleSteps !== 1) modeBad.push(`stepper not showing one step (${s.pos}, ${s.visibleSteps})`);
await b.click(".st-row .btn:nth-of-type(2)").catch(() => {});
const noJs = await browser.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false });
const nj = await noJs.newPage(); await nj.goto(gr + "#quick", { waitUntil: "load" });
s = await nj.evaluate(() => ({ scene: getComputedStyle(document.getElementById("the-scene")).display, modes: getComputedStyle(document.querySelector(".modes")).display,
  hidden: [...document.querySelectorAll("[data-src]")].filter(e => e.offsetHeight === 0 && !e.closest(".toc")).length }));
if (s.scene === "none" || s.modes !== "none" || s.hidden) modeBad.push(`without JS the full text is not all visible (${JSON.stringify(s)})`);
T("combo modes: Quick read hides the scene, safety note first in every mode; #quick and #sequence deep links work; no JS shows the full text", !modeBad.length, modeBad.join(" | "));

let patBad = [];
await b.goto(`${O}${base}/patterns`, { waitUntil: "load" });
const before = await b.textContent("#count");
await b.selectOption('select[name="setting"]', "signing");
const after = await b.textContent("#count"), url = b.url();
if (before === after) patBad.push("count did not change");
if (!/setting=signing/.test(url)) patBad.push("URL query not updated: " + url);
await b.goto(url, { waitUntil: "load" });
const restored = await b.evaluate(() => [document.getElementById("count").textContent, document.querySelector('select[name="setting"]').value]);
if (restored[0] !== after || restored[1] !== "signing") patBad.push("reload did not restore: " + restored.join(" / "));
T(`patterns: a filter changes the count (${before} -> ${after}) and the URL; loading that URL restores it`, !patBad.length, patBad.join(" | "));

let srBad = [];
await b.goto(`${O}${base}/method`, { waitUntil: "load" });
await b.focus("#sbtn"); await b.keyboard.press("Enter");
if (!(await b.evaluate(() => document.getElementById("search").open))) srBad.push("dialog did not open");
await b.keyboard.type("debt");
await b.waitForFunction(() => document.querySelectorAll("#sr a").length > 0, null, { timeout: 4000 }).catch(() => srBad.push("no result for debt"));
await b.keyboard.press("ArrowDown");
if (!(await b.evaluate(() => document.activeElement.closest("#sr") !== null))) srBad.push("ArrowDown does not reach the results");
await b.keyboard.press("Escape");
const after2 = await b.evaluate(() => [document.getElementById("search").open, document.activeElement.id]);
if (after2[0]) srBad.push("Escape did not close");
if (after2[1] !== "sbtn") srBad.push("focus did not return (got " + after2[1] + ")");
T("search dialog opens, finds 'debt', is keyboard operable, closes on Escape and returns focus", !srBad.length, srBad.join(" | "));
await B.close(); await noJs.close();

// axe at 1440 in dark and light, and every page type at 375 for overflow and opacity right after load
let axe2 = [], typeBad = [];
for (const cs of ["dark", "light"]) {
  const c = await browser.newContext({ viewport: { width: 1440, height: 900 }, colorScheme: cs }); const q = await c.newPage();
  for (const u of sample) { await q.goto(O + u, { waitUntil: "load" }); if (axeSrc) (await runAxe(q)).forEach(x => axe2.push(`${cs} ${u}: ${x}`)); }
  for (const [u, h] of [[`${base}/the-debt-prison#quick`, "quick"], [`${base}/the-debt-prison#sequence`, "seq"]]) { await q.goto(O + u, { waitUntil: "load" }); if (axeSrc) (await runAxe(q)).forEach(x => axe2.push(`${cs} ${h}: ${x}`)); }
  await c.close();
}
T(axeSrc ? `axe: no serious or critical violations at 1440, dark and light (${sample.length + 2} views each)` : "axe-core missing", axeSrc && !axe2.length, axe2.slice(0, 6).join(" | "));
const typePages = [base, `${base}/start`, `${base}/patterns`, `${base}/tactics`, `${base}/stage-idealize`, `${base}/${fam[3]}`, `${base}/tactic/love-bombing`,
  `${base}/the-debt-prison`, `${base}/the-debt-prison#quick`, `${base}/the-debt-prison#sequence`, `${base}/method`, `${base}/take-it-with-you`, `${base}/a-z`,
  `${base}/notice`, `${base}/in-it-now`, `${base}/worried-about-someone`, `${base}/before-you-sign`, `${base}/map`];
{
  const c = await browser.newContext({ viewport: { width: 375, height: 812 }, colorScheme: "dark" }); const q = await c.newPage();
  for (const u of typePages) { await q.goto(O + u, { waitUntil: "load" }); await q.waitForTimeout(100);
    if (await q.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) typeBad.push("overflow " + u);
    const z = await zeroOpacity(q); if (z) typeBad.push(`opacity:0 x${z} ${u}`); }
  await c.close();
}
T(`every page type at 375: no horizontal overflow, nothing at opacity 0 after load (${typePages.length} views)`, !typeBad.length, typeBad.slice(0, 5).join(" | "));
T("no page errors in the sample and behaviour runs", !errs.length, errs.slice(0, 3).join(" | "));
await browser.close(); srv.close();

let fail = 0; for (const r of results) { if (!r.ok) fail++; console.log(`${r.ok ? "PASS" : "FAIL"}  ${r.name}${r.ok || !r.detail ? "" : "\n      " + r.detail}`); }
console.log(`\n${results.length - fail}/${results.length} checks passed`); process.exit(fail ? 1 : 0);
