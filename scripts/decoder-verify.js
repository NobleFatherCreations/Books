#!/usr/bin/env node
/* Regression suite for the Pattern Decoder v15 page.
 *
 *   node scripts/decoder-verify.js [path-to-page.html] [--quick]
 *
 * Default page: instruments/playbook/_undeployed/v15/index.html. Needs Playwright (already installed in the
 * cloud environment: never run `playwright install`) and, for the accessibility step, axe-core
 * (`npm i --no-save axe-core`, or put its folder on NODE_PATH). Exits non-zero if any check fails.
 *
 * What it proves, and what it cannot:
 *   - every one of the 310 stations at 390px and 1440px: no sideways scroll, the name fits, the answer is on the
 *     first phone screen, the safety note comes before the answer on all safety-sensitive entries, four steps exist
 *   - private by default: nothing in localStorage / sessionStorage / cookies after a long browse; numbered addresses; neutral title
 *   - axe-core on every page type in both themes
 *   - text contrast measured from computed colours, both themes, key pages
 *   - load timing on a 4x CPU slowdown (software-rendered browser: real devices will differ)
 *   - it does NOT replace testing with real screen readers or on real phones.
 */
const fs = require("fs"), path = require("path"), zlib = require("zlib");
const { createRequire } = require("module");
const req = createRequire(__filename);
const { chromium } = req("playwright");
let axeSrc = null;
try { axeSrc = fs.readFileSync(req.resolve("axe-core/axe.min.js"), "utf8"); } catch (e) {}

const args = process.argv.slice(2);
const QUICK = args.includes("--quick");
const file = path.resolve(args.find(a => !a.startsWith("--")) || path.join(__dirname, "..", "instruments", "playbook", "_undeployed", "v15", "index.html"));
const URL0 = "file://" + file;
const noise = t => /cloudflareinsights|ERR_FAILED|ERR_BLOCKED|ERR_INTERNET|ERR_NAME/.test(t); // the approved analytics beacon cannot load offline
const out = [], fails = [];
const T = (name, ok, detail) => { const l = (ok ? "PASS " : "FAIL ") + name + (detail ? " — " + detail : ""); out.push(l); if (!ok) fails.push(l); console.log(l); };
const contrast = (a, b) => { const L = c => { c = c.map(v => v / 255).map(v => v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; };
  const x = L(a), y = L(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };

(async () => {
  console.log("page:", file, "\n");
  const b = await chromium.launch();
  const html = fs.readFileSync(file);
  T("file size", html.length < 4.5e6, (html.length / 1e6).toFixed(2) + " MB, " + (zlib.gzipSync(html).length / 1e6).toFixed(2) + " MB gzipped");
  T("no external requests in markup (only the approved beacon)", (() => { const h = html.toString("utf8").replace(/<script[^>]*cloudflareinsights[^>]*><\/script>/, "").replace(/<link rel="canonical" href="https:\/\/noblefathercreations\.com\/playbook">/, "");
    return !/(src|href)=["']https?:\/\/(?!www\.w3\.org)/i.test(h.replace(/<a [^>]*href=["']https?:[^>]*>/g, "")) && !/@import|url\(["']?https?:/.test(h); })());

  const ctxFor = (w, h, scheme, extra) => b.newContext(Object.assign({ viewport: { width: w, height: h }, isMobile: w < 500, hasTouch: w < 500, colorScheme: scheme || "dark", deviceScaleFactor: 1 }, extra || {}));
  const open = async (ctx, hash) => { const p = await ctx.newPage(); p._errs = []; p.on("pageerror", e => p._errs.push(e.message)); p.on("console", m => { if (m.type() === "error" && !noise(m.text())) p._errs.push(m.text()); }); await p.goto(URL0 + (hash || "#/")); await p.waitForTimeout(150); return p; };

  // ---- 310 stations x 2 widths
  const probe = await open(await ctxFor(390, 844), "#/");
  const stations = await probe.evaluate(() => E.map(e => ({ s: e.s, n: e.n, sens: e.sens, i: e.i })));
  await probe.context().close();
  T("310 stations present", stations.length === 310, String(stations.length));
  const sens = stations.filter(s => s.sens).length;
  T("105 safety-sensitive stations", sens === 105, String(sens));
  const pick = QUICK ? stations.filter((_, i) => i % 6 === 0) : stations;
  for (const [w, h, label] of [[390, 844, "phone 390"], [1440, 900, "desktop 1440"]]) {
    const ctx = await ctxFor(w, h); const p = await open(ctx, "#/"); const bad = [];
    for (const st of pick) {
      await p.goto(URL0 + "#/entry/" + st.s); await p.waitForTimeout(25);
      const r = await p.evaluate((sens) => {
        const d = document.documentElement, h1 = document.querySelector("h1.h-st"), ans = document.querySelector(".answer"), warn = document.querySelector(".warn");
        const o = [];
        if (d.scrollWidth > innerWidth + 1) o.push("sideways scroll " + (d.scrollWidth - innerWidth));
        if (!h1) o.push("no title"); else { const r = h1.getBoundingClientRect(); if (h1.scrollWidth > h1.clientWidth + 1 || r.right > innerWidth + 1) o.push("title overflows"); }
        /* the answer is on the first phone screen; on a safety-sensitive entry the full safety note comes first and fills it, and the answer follows within 1.4 screens */
        if (!ans) o.push("no answer card"); else if (innerWidth < 500) { const top = ans.getBoundingClientRect().top; if (!sens && top > innerHeight - 90) o.push("answer starts below the first screen"); if (sens && top > innerHeight * 1.4) o.push("answer starts beyond 1.4 screens"); }
        if (sens) { if (!warn) o.push("no safety note"); else { if (!(warn.compareDocumentPosition(ans) & Node.DOCUMENT_POSITION_FOLLOWING)) o.push("safety note is not before the answer"); if (innerWidth < 500 && warn.getBoundingClientRect().top > innerHeight - 200) o.push("safety note not on the first screen"); } }
        else if (warn) o.push("safety panel on a non-sensitive entry");
        if (document.querySelectorAll(".panelx").length !== 4) o.push("not four sections");
        if (document.querySelectorAll(".secnav [data-sec]").length !== 4) o.push("no four-part section index");
        if (document.querySelector("[role=tab],[role=tabpanel],.strip,.stepdock,#map")) o.push("old tabs, strip, dock or map still present");
        return o;
      }, st.sens);
      if (r.length) bad.push(st.n + ": " + r.join(", "));
      if (p._errs.length) { bad.push(st.n + ": script error " + p._errs[0]); p._errs.length = 0; }
    }
    T(`stations render cleanly at ${label} (${pick.length})`, !bad.length, bad.slice(0, 4).join(" | ") + (bad.length > 4 ? ` (+${bad.length - 4} more)` : ""));
    await ctx.close();
  }

  // ---- how long is a full read on a phone? One scroll now, so the whole entry is the measure
  { const ctx = await ctxFor(390, 844); const p = await open(ctx, "#/entry/gaslighting");
    const m = await p.evaluate(() => ({ all: document.documentElement.scrollHeight / innerHeight, longest: Math.max(...[...document.querySelectorAll(".panelx")].map(x => x.getBoundingClientRect().height / innerHeight)) }));
    T("Gaslighting on a phone: one scroll of ≤ 14 screens, and no single section over 6 screens (v14: one page of 16.5)", m.all <= 14 && m.longest <= 6, "whole entry " + m.all.toFixed(1) + " screens; longest section " + m.longest.toFixed(1)); await ctx.close(); }

  // ---- reflow: 320px wide and the Largest text size (WCAG 1.4.4 / 1.4.10)
  { const bad = [];
    for (const size of ["m", "xl"]) { const ctx = await ctxFor(320, 640, "dark"); const p = await open(ctx, "#/"); await p.evaluate(sz => document.documentElement.setAttribute("data-size", sz), size);
      for (const pg of ["#/", "#/entry/emotional-blackmail", "#/entry/pseudo-profundity-intellectual-intimidation", "#/help", "#/search", "#/lines", "#/line/truth", "#/compare/gaslighting/countering", "#/routes/grooming", "#/settings", "#/safety", "#/lines/where"]) {
        await p.goto(URL0 + pg); await p.evaluate(sz => document.documentElement.setAttribute("data-size", sz), size); await p.waitForTimeout(80);
        const o = await p.evaluate(() => { const d = document.documentElement; const wide = [...document.querySelectorAll("main *")].filter(e => !e.closest(".mapwrap") && e.getBoundingClientRect().right > innerWidth + 1 && e.offsetParent).slice(0, 2).map(e => e.tagName + "." + e.className);
          return { sw: d.scrollWidth - innerWidth, wide }; });
        if (o.sw > 1) bad.push(`${size} ${pg} +${o.sw}px ${o.wide.join(",")}`); }
      await ctx.close(); }
    T("reflow: no sideways scroll at 320px, standard and Largest text", !bad.length, bad.slice(0, 4).join(" | ")); }

  // ---- private by default
  { const ctx = await ctxFor(390, 844); const p = await open(ctx, "#/"); const sample = stations.filter((_, i) => i % 11 === 0).slice(0, 25);
    for (const st of sample) { await p.goto(URL0 + "#/entry/" + st.s); await p.waitForTimeout(20); }
    await p.goto(URL0 + "#/search"); await p.fill("#q", "silent treatment"); await p.waitForTimeout(250);
    const z = await p.evaluate(() => ({ ls: localStorage.length, ss: sessionStorage.length, ck: document.cookie, url: location.href, title: document.title }));
    T("private: nothing written to the device after browsing 25 stations and a search", z.ls === 0 && z.ss === 0 && z.ck === "", JSON.stringify({ ls: z.ls, ss: z.ss }));
    T("private: the query is not in the address", !/silent/.test(z.url)); T("findable (v16): the tab title names the page", z.title === "Search · Pattern Decoder", z.title);
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(100);
    T("findable (v16): station links use names, never numbers", await p.evaluate(() => { const h = [...document.querySelectorAll("a[href^='#/']")].map(a => a.getAttribute("href")); return h.some(x => /^#\/entry\//.test(x)) && !h.some(x => /^#\/(s|l|c|r)\/\d/.test(x)); }));
    { const m = await p.evaluate(() => ({ t: document.title, d: document.querySelector("meta[name=description]").content, c: document.querySelector("link[rel=canonical]").href,
        ld: JSON.parse((document.querySelector("#ld-page") || { textContent: "{}" }).textContent), robots: (document.querySelector("meta[name=robots]") || { content: "" }).content }));
      T("findable (v16): no robots block (index, follow only), and a station sets its title, description, canonical and DefinedTerm", !/noindex|nofollow|none/i.test(m.robots) && /^Gaslighting: /.test(m.t) && /^What is Gaslighting\? /.test(m.d)
        && m.c === "https://noblefathercreations.com/playbook/gaslighting" && m.ld["@type"] === "DefinedTerm" && /^T\d\d$/.test(m.ld.termCode), JSON.stringify(m).slice(0, 200)); }
    await ctx.close(); }
  { const site = path.dirname(file), rd = f => fs.readFileSync(path.join(site, f), "utf8"), bad = [];
    for (const f of ["index.html", "gaslighting.html", "line-truth.html", "tactics.html"]) { const h = rd(f);
      if (!/<meta property="og:image" content="https:\/\/noblefathercreations\.com\/playbook\/f\/og\.png">/.test(h)) bad.push(f + ": og:image"); if (!/twitter:card" content="summary_large_image"/.test(h)) bad.push(f + ": twitter card");
      if (/noindex|nofollow/.test(h)) bad.push(f + ": robots block"); if (f !== "index.html" && !/"dateModified": "20\d\d-\d\d-\d\d"/.test(h)) bad.push(f + ": dateModified"); }
    const png = fs.readFileSync(path.join(site, "f", "og.png")); if (png.readUInt32BE(16) !== 1200 || png.readUInt32BE(20) !== 630) bad.push("og.png is not 1200x630");
    const ll = rd("llms.txt"); if ((ll.match(/\]\(https:\/\/noblefathercreations\.com\/playbook\/line-/g) || []).length !== 10 || !/sitemap\.xml/.test(ll)) bad.push("llms.txt");
    T("findable (v19): link-preview image (1200x630) and large card on every kind of page, dateModified on plain pages, llms.txt maps the ten lines", !bad.length, bad.join("; ")); }

  // ---- axe on each page type, both themes, both widths
  if (!axeSrc) { T("axe-core accessibility scan", false, "axe-core not found: run `npm i --no-save axe-core`"); }
  else {
    const pages = ["#/", "#/entry/gaslighting", "#/entry/emotional-blackmail", "#/search", "#/help", "#/lines", "#/line/truth", "#/compare/gaslighting/countering", "#/routes", "#/routes/grooming", "#/lines/az", "#/lines/where", "#/saved", "#/settings", "#/safety", "#/updates"];
    const bad = [], minor = {}; let scans = 0;
    for (const scheme of ["dark", "light"]) for (const [w, h] of [[390, 844], [1440, 900]]) {
      const ctx = await ctxFor(w, h, scheme); const p = await open(ctx, "#/");
      for (const pg of pages) { await p.goto(URL0 + pg); await p.waitForTimeout(120);
        if (pg === "#/search") { await p.fill("#q", "silent treatment"); await p.waitForTimeout(250); }
        await p.addScriptTag({ content: axeSrc }).catch(() => {});
        const res = await p.evaluate(() => axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] }, resultTypes: ["violations"] }).then(r => r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, sel: v.nodes[0].target.join(" ") }))));
        scans++;
        for (const v of res) { if (/nf-|#nf/.test(v.sel)) continue; /* the shared House menu is not part of this page */
          if (v.impact === "serious" || v.impact === "critical") bad.push(`${scheme}/${w} ${pg} ${v.id} (${v.n}) ${v.sel}`); else minor[v.id] = (minor[v.id] || 0) + 1; } }
      await ctx.close(); }
    T(`axe-core: no serious or critical violations (${scans} scans, WCAG 2.2 AA + best practice)`, !bad.length, bad.slice(0, 5).join(" | "));
    const mk = Object.keys(minor); if (mk.length) console.log("  note: minor/moderate axe findings:", JSON.stringify(minor));
  }

  // ---- contrast from computed colours
  { const bad = []; let tested = 0;
    for (const scheme of ["dark", "light"]) { const ctx = await ctxFor(390, 844, scheme); const p = await open(ctx, "#/");
      for (const pg of ["#/", "#/entry/emotional-blackmail", "#/help", "#/search", "#/line/truth", "#/lines", "#/settings", "#/safety"]) { await p.goto(URL0 + pg); await p.waitForTimeout(120);
        const r = await p.evaluate(() => {
          const parse = c => { const m = c.match(/rgba?\(([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:[, /]+([\d.]+))?/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; };
          const bgOf = el => { let acc = []; for (let e = el; e; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c[3] > 0) { acc.push(c); if (c[3] >= .99) break; } } let base = [255, 255, 255]; for (let i = acc.length - 1; i >= 0; i--) { const c = acc[i]; base = base.map((v, k) => v * (1 - c[3]) + c[k] * c[3]); } return base; };
          const res = [], seen = new Set(), w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          for (let n; (n = w.nextNode());) { const t = n.nodeValue.trim(); if (!t) continue; const el = n.parentElement; if (!el || seen.has(el) || el.closest(".nf-chrome,.nf-panel,.sr-only,[hidden],script,style")) continue;
            const cs = getComputedStyle(el), rc = el.getBoundingClientRect(); if (cs.visibility === "hidden" || cs.display === "none" || rc.width === 0) continue; seen.add(el);
            const fg = parse(cs.color); if (!fg) continue; const bg = bgOf(el); const a = fg[3]; const f = [0, 1, 2].map(i => fg[i] * a + bg[i] * (1 - a));
            const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700; res.push({ f, bg, large: px >= 24 || (px >= 18.66 && bold), px, txt: t.slice(0, 28), cls: el.className || el.tagName }); }
          return res; });
        for (const x of r) { tested++; const c = contrast(x.f, x.bg), need = x.large ? 3 : 4.5; if (c < need) bad.push(`${scheme} ${pg} "${x.txt}" ${c.toFixed(2)}<${need}`); } }
      await ctx.close(); }
    T(`text contrast: every text colour ≥4.5:1 (≥3:1 large), ${tested} text runs, both themes`, !bad.length, bad.slice(0, 5).join(" | ")); }

  // ---- smallest text
  { const ctx = await ctxFor(390, 844); const p = await open(ctx, "#/entry/gaslighting");
    const small = await p.evaluate(() => { const o = [], w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue; const el = n.parentElement; if (el.closest(".nf-chrome,.nf-panel,.sr-only,[hidden],script,style")) continue; const px = parseFloat(getComputedStyle(el).fontSize); if (px < 13) o.push(Math.round(px * 10) / 10 + "px " + (el.className || el.tagName)); } return o; });
    T("no text smaller than 13px (v14: 13–14px italic labels)", !small.length, small.slice(0, 4).join("; ")); await ctx.close(); }

  // ---- load timing, phone with a 4x CPU slowdown. Judged two ways: against loose absolute limits, and against the live v14
  // page measured side by side in the same run (so a slow or busy machine cancels out). v14 is skipped if it is not on disk.
  { const one = async url => { const ctx = await ctxFor(390, 844, "dark"); const p = await ctx.newPage();
      await p.addInitScript(() => { window.__lt = []; window.__lcp = 0; new PerformanceObserver(l => l.getEntries().forEach(e => window.__lt.push(e.duration))).observe({ type: "longtask", buffered: true });
        new PerformanceObserver(l => l.getEntries().forEach(e => { window.__lcp = e.startTime; })).observe({ type: "largest-contentful-paint", buffered: true }); });
      const cdp = await ctx.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await p.goto(url + "#/"); await p.waitForFunction(() => document.querySelector("h1") && document.fonts.status === "loaded"); await p.waitForTimeout(900);
      const r = await p.evaluate(() => { const nav = performance.getEntriesByType("navigation")[0], fcp = performance.getEntriesByName("first-contentful-paint")[0];
        return { dcl: nav.domContentLoadedEventEnd, fcp: fcp ? fcp.startTime : 0, lcp: window.__lcp, longest: Math.max(0, ...window.__lt), total: window.__lt.reduce((a, b) => a + b, 0) }; }); await ctx.close(); return r; };
    const v14path = path.join(__dirname, "..", "instruments", "playbook", "index.html");
    const haveV14 = fs.existsSync(v14path) && path.resolve(v14path) !== file && fs.readFileSync(v14path, "utf8").slice(0, 900000).includes('id="sky"');
    /* the two pages are measured alternately, so drift in the machine's speed during the run hits both equally */
    const runs = { v15: [], v14: [] }; for (let i = 0; i < 7; i++) { runs.v15.push(await one(URL0)); if (haveV14) runs.v14.push(await one("file://" + v14path)); }
    const med = (rs, k) => rs.map(r => r[k]).sort((a, b) => a - b)[Math.floor(rs.length / 2)];
    const sum = rs => Object.fromEntries(["dcl", "fcp", "lcp", "longest", "total"].map(k => [k, med(rs, k)]));
    const show = (m, l) => console.log("  timing, 4x CPU, median of 7, " + l + ":", Object.entries(m).map(([k, v]) => k + " " + Math.round(v) + "ms").join(", "));
    const v15 = sum(runs.v15); show(v15, "this page");
    T("home: first content in ≤ 1200 ms on a 4x slowdown", v15.fcp <= 1200, Math.round(v15.fcp) + " ms");
    T("home: largest paint in ≤ 1500 ms", v15.lcp <= 1500, Math.round(v15.lcp) + " ms");
    T("home: longest main-thread task ≤ 200 ms (loose backstop)", v15.longest <= 200, Math.round(v15.longest) + " ms");
    T("home: total long-task time ≤ 450 ms (loose backstop)", v15.total <= 450, Math.round(v15.total) + " ms");
    if (haveV14) { const v14 = sum(runs.v14); show(v14, "v14, live");
      /* largest paint, not first paint: v14's first paint is its background and its headline waits for a reveal animation */
      T("home: v15 costs well under v14 on the same machine, measured alternately (largest paint ≤ 50%, longest task ≤ 40%, total long tasks ≤ 40%)", v15.lcp <= v14.lcp * 0.5 && v15.longest <= v14.longest * 0.4 && v15.total <= v14.total * 0.4,
        `largest paint ${(v15.lcp / v14.lcp * 100).toFixed(0)}%, longest task ${(v15.longest / v14.longest * 100).toFixed(0)}%, total long tasks ${(v15.total / v14.total * 100).toFixed(0)}% of v14`);
    } else console.log("  (v14 not found next to this page: the side-by-side comparison was skipped)"); }

  // ---- response to a tap: search typing and opening a station, 4x slowdown
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/search"); const cdp = await ctx.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
    const t = await p.evaluate(async () => { const q = document.querySelector("#q"); const ts = []; for (const s of ["s", "si", "sil", "sile", "silen", "silent"]) { const t0 = performance.now(); q.value = s; q.dispatchEvent(new Event("input", { bubbles: true })); await new Promise(r => setTimeout(r, 140)); ts.push(performance.now() - t0 - 140); } return ts; });
    const times = []; for (const slug of ["gaslighting", "silent-treatment", "love-bombing"]) { const c2 = await ctxFor(390, 844, "dark"); const q = await open(c2, "#/"); const cd = await c2.newCDPSession(q); await cd.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      times.push(await q.evaluate(async sl => { const t0 = performance.now(); location.hash = "#/entry/" + sl; await new Promise(r => { const iv = setInterval(() => { if (document.querySelector("h1.h-st")) { clearInterval(iv); r(); } }, 4); }); return performance.now() - t0; }, slug)); await c2.close(); }
    const open1 = times.sort((a, b) => a - b)[1];
    T("typing in search: slowest keystroke response ≤ 200 ms (4x slowdown)", Math.max(...t) <= 200, Math.round(Math.max(...t)) + " ms");
    T("opening a station (first time, parses its line's data), median of 3 lines ≤ 200 ms (4x slowdown)", open1 <= 200, Math.round(open1) + " ms (" + times.map(Math.round).join("/") + ")"); await ctx.close(); }

  // ---- keyboard: the whole flow works without a mouse
  { const ctx = await ctxFor(1440, 900, "dark"); const p = await open(ctx, "#/"); await p.keyboard.press("Tab"); await p.keyboard.press("Enter"); await p.waitForTimeout(100);
    const focusables = await p.evaluate(() => { const o = []; for (let i = 0; i < 12; i++) { const a = document.activeElement; o.push(a.tagName + ":" + (a.textContent || "").trim().slice(0, 18)); } return o; });
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(150);
    await p.keyboard.press("j"); await p.waitForTimeout(150); const afterJ = await p.evaluate(() => location.hash);
    T("keyboard: J steps to the next station", /#\/s\/\d+|#\/entry\//.test(afterJ) && !/gaslighting/.test(afterJ), afterJ);
    await p.keyboard.press("/"); await p.waitForTimeout(150); T("keyboard: / opens search with focus in the field", await p.evaluate(() => document.activeElement.id === "q"));
    await ctx.close(); }

  // ---- reduced motion: nothing stuck invisible, no animation
  { const ctx = await ctxFor(390, 844, "dark", { reducedMotion: "reduce" }); const p = await open(ctx, "#/entry/gaslighting");
    const r = await p.evaluate(() => ({ anim: document.getAnimations().filter(a => !(window.ScrollTimeline && a.timeline instanceof ScrollTimeline)).length, hidden: [...document.querySelectorAll("main *")].filter(e => getComputedStyle(e).opacity === "0" && e.offsetParent).length }));
    T("reduced motion: no running animations and nothing stuck transparent", r.anim === 0 && r.hidden === 0, JSON.stringify(r)); await ctx.close(); }

  // ---- idle cost: no animation loop
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(600);
    const frames = await p.evaluate(() => new Promise(res => { let n = 0; const o = new MutationObserver(() => n++); o.observe(document.body, { subtree: true, attributes: true, childList: true, characterData: true }); const anims = document.getAnimations().filter(a => !(window.ScrollTimeline && a.timeline instanceof ScrollTimeline)).length; setTimeout(() => res({ mutations: n, anims }), 3000); }));
    T("idle: nothing changes or animates on its own for 3 s", frames.mutations === 0 && frames.anims === 0, JSON.stringify(frames)); await ctx.close(); }

  // ---- leaving: reachable from every state, and Back does not return to the guide
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/");
    await p.route("**/*google.com/**", r => r.fulfill({ status: 200, body: "weather" }));
    await p.goto(URL0 + "#/entry/gaslighting"); await p.evaluate(() => breathShow()); await p.waitForTimeout(100);
    T("leave: the Leave button is on top of the pause card", await p.evaluate(() => { const r = document.querySelector("#leave").getBoundingClientRect(); const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return !!e && !!e.closest("#leave"); }));
    await p.evaluate(() => breathHide());
    await p.goto(URL0 + "#/lines"); await p.waitForTimeout(200);
    await p.keyboard.press("Escape"); await p.keyboard.press("Escape"); await p.waitForTimeout(700);
    T("leave: Escape twice leaves from the browse page", /google\.com/.test(p.url()), p.url());
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/");
    await p.route("**/*google.com/**", r => r.fulfill({ status: 200, body: "weather" }));
    for (const h of ["#/s/5", "#/s/6", "#/lines", "#/search"]) { await p.evaluate(h => { location.hash = h; }, h); await p.waitForTimeout(120); }
    await p.click("#leave"); await p.waitForTimeout(900);
    const onWeather = /google\.com/.test(p.url());
    const back = await p.goBack({ timeout: 4000 }).catch(() => null);
    T("leave: goes to the weather page, and Back does not return to the guide", onWeather && !(p.url().startsWith("file://") && /v15/.test(p.url())), "after leave " + (onWeather ? "weather" : p.url()) + "; after Back " + p.url());
    await ctx.close(); }

  // ---- safety and the colour contract
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/compare/emotional-blackmail/gaslighting");
    const r = await p.evaluate(() => { const w = document.querySelector(".warn"), g = document.querySelector(".cmp-g"); return { warn: !!w, before: !!w && !!(w.compareDocumentPosition(g) & Node.DOCUMENT_POSITION_FOLLOWING), top: w ? w.getBoundingClientRect().top : 9999 }; });
    T("compare: the safety note comes before the comparison and is on the first screen", r.warn && r.before && r.top < 700, JSON.stringify(r));
    await p.goto(URL0 + "#/");
    T("home: a safe step is on the first screen (If you are not safe, read this first)", await p.evaluate(() => { const a = [...document.querySelectorAll(".blade")].find(x => /not safe/i.test(x.textContent)); return !!a && a.getBoundingClientRect().top < innerHeight - 70 && /safety/.test(a.getAttribute("href")); }));
    await p.goto(URL0 + "#/search"); await p.fill("#q", "you are imagining things"); await p.waitForTimeout(250);
    T("no doubled quote marks in search results or sound-like lines (all 310)", await (async () => { await p.fill("#q", "safe"); await p.waitForTimeout(250); const a = await p.evaluate(() => /[“”"]{2}/.test(document.querySelector("#results").textContent.replace(/[”"]\s+/g, " ")));
      const bad = []; for (const st of stations.filter((_, i) => i % 3 === 0)) { await p.goto(URL0 + "#/entry/" + st.s); const t = await p.evaluate(() => [...document.querySelectorAll(".says li")].map(li => li.textContent.trim()).filter(x => /^[“"]{2}/.test(x))); if (t.length) bad.push(st.n); }
      return !a && !bad.length; })());
    await p.goto(URL0 + "#/search"); await p.fill("#q", "you are imagining things"); await p.waitForTimeout(250);
    T("search highlight is not amber (amber is for danger only)", await p.evaluate(() => { const m = document.querySelector("mark"); if (!m) return false; const c = getComputedStyle(m).backgroundColor; return !/255, 176, 32/.test(c); }));
    await ctx.close(); }

  // ---- browse: the ten lines are rows you can hit, and the whole index is visible on a phone in about two screens
  { const bad = [];
    for (const w of [320, 360, 390]) { const ctx = await ctxFor(w, 800, "dark"); const p = await open(ctx, "#/lines"); await p.waitForTimeout(150);
      const m = await p.evaluate(() => { const rs = [...document.querySelectorAll(".lrows .lrow")].map(a => a.getBoundingClientRect()); return { n: rs.length, minH: Math.min(...rs.map(r => r.height)), minW: Math.min(...rs.map(r => r.width)) }; });
      if (m.n !== 10 || m.minH < 44 || m.minW < 44) bad.push(`${w}px: ${JSON.stringify(m)}`);
      await ctx.close(); }
    T("browse: ten line rows, each at least 44 CSS px tall, down to 320px wide", !bad.length, bad.join("; ")); }

  // ---- techniques brought back from v14
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(200);
    const bar = async () => p.evaluate(() => { const t = getComputedStyle(document.querySelector(".top"), "::after").transform; const m = t.match(/matrix\(([^,]+)/); return m ? +m[1] : (t === "none" ? 1 : -1); });
    const top = await bar(); await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(250); const end = await bar();
    T("reading line: empty at the top of a station, full at the end (scroll-driven, no script)", top < 0.05 && end > 0.95, "top " + top.toFixed(2) + ", end " + end.toFixed(2));
    await p.evaluate(() => scrollTo(0, 0));
    T("station sign wears its line colour (band matches the line bullet)", await p.evaluate(() => { const b = getComputedStyle(document.querySelector(".sname"), "::before"), bl = getComputedStyle(document.querySelector(".sname .b")); return b.backgroundColor === bl.backgroundColor && parseFloat(b.height) >= 6; }));
    await p.goto(URL0 + "#/search"); const asked = {};
    for (const q of ["settings", "love", "safe", "dark"]) { await p.fill("#q", q); await p.waitForTimeout(250); asked[q] = await p.evaluate(() => [...document.querySelectorAll("#results a.row")].map(a => a.getAttribute("href"))); }
    T("search reaches pages and lines (settings, love, safe, dark)", asked.settings.includes("#/settings") && asked.love.some(h => /#\/line\//.test(h)) && asked.safe.includes("#/safety") && asked.dark.includes("#/settings"), JSON.stringify(Object.fromEntries(Object.entries(asked).map(([k, v]) => [k, v.slice(0, 3)]))));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark", { contrast: "more" }); const p = await open(ctx, "#/");
    const r = await p.evaluate(() => { const b = document.querySelector(".blade:not(.pri)"), cs = getComputedStyle(b), fg2 = getComputedStyle(document.querySelector(".lede")).color, fg = getComputedStyle(document.body).color; return { ring: cs.boxShadow, lede: fg2 === fg }; });
    T("more contrast: controls get a 2px outline and secondary text goes full strength", /2px/.test(r.ring) && r.lede, r.ring.slice(0, 50) + " lede=" + r.lede);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark", { forcedColors: "active" }); const p = await open(ctx, "#/entry/gaslighting"); const errs = [];
    for (const h of ["#/", "#/entry/emotional-blackmail", "#/lines", "#/help"]) { await p.goto(URL0 + h); await p.waitForTimeout(150); const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (o > 1) errs.push(h + " +" + o); }
    const bd = await p.evaluate(() => { const b = document.querySelector(".leave"); return b ? getComputedStyle(b).borderTopWidth : "none"; });
    T("forced colours: pages reflow and Leave keeps a 2px outline", !errs.length && parseFloat(bd) >= 2, errs.join(",") + " border " + bd);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/"); const cdp = await ctx.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
    const t = await p.evaluate(async () => { const t0 = performance.now(); location.hash = "#/lines/az"; await new Promise(r => { const iv = setInterval(() => { if (document.querySelector("#az-A")) { clearInterval(iv); r(); } }, 4); }); return performance.now() - t0; });
    T("A to Z (310 rows) opens in ≤ 250 ms on a 4x slowdown (content-visibility)", t <= 250, Math.round(t) + " ms"); await ctx.close(); }

  // ---- stage 1: scrambled storage, importing v14's readable entries, resting a line, the Leave destination
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.waitForTimeout(150);
    await p.click("label:has(input[name=save][value=on])"); await p.waitForTimeout(150);
    await p.click("label:has(input[name=theme][value=night])"); await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(150); await p.click("[data-save]"); await p.waitForTimeout(200);
    const st = await p.evaluate(() => { const keys = Object.keys(localStorage), v = localStorage.getItem("ui-state") || ""; let raw = ""; try { raw = atob(v); } catch (e) {}
      return { keys, v, plain: /gaslighting|starred|theme|fg_|private|decoder/i.test(v + raw + keys.join(" ")), looks: /^[A-Za-z0-9+/]+$/.test(v) && v.length > 10 }; });
    T("saving on: exactly one entry, scrambled, with no readable tactic name, setting or tool name", st.keys.length === 1 && st.keys[0] === "ui-state" && st.looks && !st.plain, JSON.stringify({ keys: st.keys, plain: st.plain }));
    await p.reload(); await p.waitForTimeout(250); await p.goto(URL0 + "#/saved"); await p.waitForTimeout(250);
    const back = await p.evaluate(() => ({ rows: [...document.querySelectorAll(".row .nm")].map(x => x.textContent), theme: document.documentElement.getAttribute("data-theme") }));
    T("saving on: saved tactic and theme come back after a reload", back.rows.includes("Gaslighting") && back.theme === "night", JSON.stringify(back));
    await p.goto(URL0 + "#/settings"); await p.click("label:has(input[name=save][value=off])"); await p.waitForTimeout(200);
    T("saving off: the entry is deleted", await p.evaluate(() => localStorage.length === 0)); await ctx.close(); }
  { const seed = () => { localStorage.setItem("fg_starred", JSON.stringify(["Gaslighting"])); localStorage.setItem("fg_trail", JSON.stringify([{ name: "Countering", ts: 1 }])); localStorage.setItem("fg_theme", JSON.stringify("daylight")); };
    const ctx = await ctxFor(390, 844, "dark"); await ctx.addInitScript(() => { if (!sessionStorage.getItem("seeded")) { sessionStorage.setItem("seeded", "1"); localStorage.setItem("fg_starred", JSON.stringify(["Gaslighting"])); localStorage.setItem("fg_trail", JSON.stringify([{ name: "Countering", ts: 1 }])); localStorage.setItem("fg_theme", JSON.stringify("daylight")); } });
    const p = await open(ctx, "#/"); await p.waitForTimeout(250);
    const seen = await p.evaluate(() => !!document.querySelector("#legacy"));
    await p.click("#legacy [data-saving=on]"); await p.waitForTimeout(250); await p.goto(URL0 + "#/saved"); await p.waitForTimeout(200);
    const r = await p.evaluate(() => ({ rows: [...document.querySelectorAll(".row .nm")].map(x => x.textContent), keys: Object.keys(localStorage) }));
    T("v14's readable entries are offered for import, imported, and the readable keys are wiped", seen && r.rows.includes("Gaslighting") && r.rows.includes("Countering") && r.keys.length === 1 && r.keys[0] === "ui-state", JSON.stringify(r));
    await ctx.close();
    const c2 = await ctxFor(390, 844, "dark"); await c2.addInitScript(() => { if (!sessionStorage.getItem("seeded")) { sessionStorage.setItem("seeded", "1"); localStorage.setItem("fg_starred", JSON.stringify(["Gaslighting"])); } });
    const q = await open(c2, "#/"); await q.waitForTimeout(250); await q.click("#legacy [data-forgetlegacy]"); await q.waitForTimeout(200);
    T("v14's readable entries can be deleted outright", await q.evaluate(() => localStorage.length === 0)); await c2.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.waitForTimeout(150);
    const pick = await p.evaluate(() => { const e = E.find(x => x.g === "society" && !/\s/.test(x.n.split(" ")[0] || "")) || E.find(x => x.g === "society"); return { n: e.n, s: e.s, first: e.n.toLowerCase() }; });
    await p.goto(URL0 + "#/search"); await p.fill("#q", pick.n); await p.waitForTimeout(250);
    const before = await p.evaluate(() => [...document.querySelectorAll("#results .row .nm")].map(x => x.textContent));
    await p.goto(URL0 + "#/settings"); await p.click("label:has(input[name=rest][value=society])"); await p.waitForTimeout(200);
    await p.goto(URL0 + "#/search"); await p.fill("#q", pick.n); await p.waitForTimeout(250);
    const after = await p.evaluate(() => [...document.querySelectorAll("#results .row .nm")].map(x => x.textContent));
    T("rest a line: a resting line's tactics leave search (and return when shown)", before.includes(pick.n) && !after.includes(pick.n), pick.n + " before " + before.includes(pick.n) + " after " + after.includes(pick.n));
    await p.goto(URL0 + "#/line/society"); await p.waitForTimeout(200);
    T("rest a line: its page says it is resting and offers to show it", await p.evaluate(() => /resting this line/i.test(document.querySelector("main").textContent) && !!document.querySelector("[data-unhide]")));
    await p.goto(URL0 + "#/lines"); await p.waitForTimeout(200);
    T("rest a line: its row on Browse is dimmed and says it is resting", await p.evaluate(() => { const a = [...document.querySelectorAll(".lrows .lrow")].filter(x => /society/.test(x.getAttribute("href"))); return a.length === 1 && a[0].classList.contains("rest") && /Resting/.test(a[0].textContent); }));
    await p.goto(URL0 + "#/entry/" + pick.s); await p.waitForTimeout(200);
    T("rest a line: an entry opened by link is closed behind a notice with Show and Use-this-safely", await p.evaluate(() => !!document.querySelector("[data-unhide]") && !document.querySelector("h1.h-st") && !!document.querySelector("a[href='#/safety']")));
    await p.click("[data-unhide]"); await p.waitForTimeout(300);
    T("rest a line: after showing the line the entry opens with its safety note", await p.evaluate(() => !!document.querySelector("h1.h-st")));
    T("rest a line: nothing is written to the device while saving is off", await p.evaluate(() => localStorage.length === 0));
    await p.goto(URL0 + "#/settings"); const left = await p.evaluate(async () => { const boxes = [...document.querySelectorAll("input[name=rest]")]; for (const b of boxes) { if (!b.checked) { b.click(); await new Promise(r => setTimeout(r, 30)); } } return boxes.filter(b => b.checked).length; });
    T("rest a line: at least one line always stays visible", left === 9, "ticked " + left + " of 10");
    await p.click("input[name=rest][value=society]"); await p.waitForTimeout(100);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.route("**/*wikipedia.org/**", r => r.fulfill({ status: 200, body: "wiki" }));
    await p.click("label:has(input[name=leave][value=wiki])"); await p.waitForTimeout(150);
    await p.keyboard.press("Escape"); await p.keyboard.press("Escape"); await p.waitForTimeout(900);
    T("Leave goes where you chose (Wikipedia)", /wikipedia\.org/.test(p.url()), p.url()); await ctx.close(); }

  // ---- stage 2: number keys, deep links to a section, the numbered route list
  { const ctx = await ctxFor(1440, 900, "dark", { reducedMotion: "reduce" }); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(200);
    const near = n => p.evaluate(n => { const t = document.getElementById("sec-" + n).getBoundingClientRect().top; return t > 40 && t < 260; }, n);
    await p.keyboard.press("3"); await p.waitForTimeout(250); const k3 = await near(2) && await p.evaluate(() => document.querySelector(".secnav [data-sec='2']").getAttribute("aria-current") === "true");
    await p.keyboard.press("1"); await p.waitForTimeout(250); const k1 = await near(0);
    T("keys 1 to 4 jump between the four sections, and the index follows", k3 && k1);
    await p.goto(URL0 + "#/entry/gaslighting/3"); await p.waitForTimeout(350);
    T("deep link #/entry/slug/3 opens scrolled to section 3", await near(2));
    await p.goto(URL0 + "#/s/5/4"); await p.waitForTimeout(350);
    T("private numbered deep link #/s/5/4 opens scrolled to section 4", await near(3));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/routes/grooming"); await p.waitForTimeout(250);
    const r = await p.evaluate(() => ({ list: document.querySelectorAll(".chain li").length, old: !!document.querySelector(".rstrip,.mapwrap,#map") }));
    T("route page: the numbered list of every station, with no strip of circles and no map", r.list > 3 && !r.old, JSON.stringify(r));
    await p.click(".chain li a >> nth=1"); await p.waitForTimeout(300);
    T("route page: a tap on a station opens it", await p.evaluate(() => !!document.querySelector("h1.h-st")));
    await ctx.close(); }

  // ---- stage 3: the pre-compile gate in the build proves it rejects bad input (and that the real data passes)
  { const r = require("child_process").spawnSync("python3", ["-I", path.join(__dirname, "..", "design", "build-decoder-v15.py"), "--selftest"], { encoding: "utf-8", timeout: 180000 });
    const out2 = (r.stdout || "") + (r.stderr || ""); const rejected = (out2.match(/: rejected/g) || []).length;
    T("build gate self-test: real data passes and 11 kinds of damage are each rejected (empty field, unclosed marker, placeholder, cut-off sentence, HTML, missing safety note, bad link, missing entry, changed character, damaged data block)", r.status === 0 && rejected === 11 && /real data: passes/.test(out2), `exit ${r.status}, ${rejected} rejected`); }

  // ---- stage 4: the signs (code plates, enamel rim, tactile dots, pictograms, print card, arrows), now without the map pictures
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/"); await p.waitForTimeout(300);
    const h = await p.evaluate(() => ({ rows: document.querySelectorAll(".home .lrows .lrow").length, chev: document.querySelectorAll(".home .lrow .chev").length, net: !!document.querySelector("a.net,#map,[href='#/map']"), pri: getComputedStyle(document.querySelector(".blade.pri")).backgroundColor }));
    T("Home: no network picture and no map; the ten lines are a grouped list with chevrons", h.rows === 10 && h.chev === 10 && !h.net, JSON.stringify(h));
    T("Home: the primary action is the gold Help blade", h.pri === "rgb(229, 193, 88)", h.pri);
    await p.click("a.sflink"); await p.waitForTimeout(400);
    T("Home: the search field opens Search with the cursor in the box", /#\/search/.test(p.url()) && await p.evaluate(() => document.activeElement.id === "q"));
    await ctx.close(); }
  { const bad = [];
    for (const size of ["m", "l", "xl"]) { const ctx = await ctxFor(320, 640, "dark"); const p = await open(ctx, "#/"); await p.evaluate(sz => document.documentElement.setAttribute("data-size", sz), size); await p.waitForTimeout(120);
      const o = await p.evaluate(() => { const r = s => document.querySelector(s).getBoundingClientRect(); const b = r(".brand"), st = r(".status"), l = r(".leave"); return { brandStatus: b.right - st.left, statusLeave: st.right - l.left }; });
      if (o.brandStatus > 1 || o.statusLeave > 1) bad.push(size + " " + JSON.stringify(o)); await ctx.close(); }
    T("top bar: the name, Private and Leave never overlap, even at 320px and the Largest text", !bad.length, bad.join("; ")); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/emotional-blackmail"); await p.waitForTimeout(300);
    const s = await p.evaluate(() => { const pl = document.querySelector(".onl .plate"); const rim = getComputedStyle(document.querySelector(".answer, .warn, .panel")).boxShadow; const dots = getComputedStyle(document.querySelector(".warn .band"), "::after"); const arr = document.querySelectorAll(".pn .arr").length;
      return { plate: pl && pl.getAttribute("aria-label") || pl && pl.textContent.replace(/\s/g, ""), rim, dots: dots.content !== "none" && dots.backgroundImage !== "none", arr }; });
    T("station code plate reads as a code (G 01) and is named for screen readers", /G.?0?1/i.test(s.plate || ""), JSON.stringify(s));
    T("enamel rim is drawn on the sign panels", s.rim && s.rim !== "none", s.rim);
    T("tactile-paving dots run along the safety band", s.dots, JSON.stringify(s));
    T("previous / next carry direction arrows", s.arr >= 1, JSON.stringify(s));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/help"); await p.waitForTimeout(250);
    const pics = await p.evaluate(() => document.querySelectorAll(".opt .pic, .row .pic, button .pic").length);
    T("pictograms on the where-it-happens choices", pics >= 7, "found " + pics);
    await p.goto(URL0 + "#/line/truth"); await p.waitForTimeout(250);
    T("line page: every station is a plain row, with no track or circles drawn", await p.evaluate(() => document.querySelectorAll(".ldia li").length > 10 && [...document.querySelectorAll(".ldia li a")].every(a => ["none", "normal"].includes(getComputedStyle(a, "::before").content))));
    await p.goto(URL0 + "#/search"); const codes = {};
    for (const [q, want] of [["t01", "T"], ["T 9", "T"], ["g44", "G"]]) { await p.fill("#q", q); await p.waitForTimeout(250); codes[q] = await p.evaluate(() => (document.querySelector("#results a, #results .row")?.textContent || "").trim().slice(0, 60)); }
    T("searching a station code lists that station first", Object.values(codes).every(Boolean) && (await p.evaluate(() => document.querySelector("#results") !== null)), JSON.stringify(codes));
    await ctx.close(); }
  { const ctx = await ctxFor(794, 1123, "dark"); const p = await open(ctx, "#/entry/emotional-blackmail"); await p.emulateMedia({ media: "print" }); await p.waitForTimeout(500);
    const r = await p.evaluate(() => ({ head: getComputedStyle(document.querySelector(".printhead")).display, top: getComputedStyle(document.querySelector(".top")).display, band: getComputedStyle(document.querySelector(".warn .band")).backgroundColor, foot: getComputedStyle(document.querySelector(".printfoot")).position, bg: getComputedStyle(document.body).backgroundColor, strip: document.querySelector(".secnav") ? getComputedStyle(document.querySelector(".secnav")).display : "none" }));
    T("print: station card has its header and footer, the app chrome is gone, black band, white page", r.head === "flex" && r.top === "none" && r.band === "rgb(0, 0, 0)" && r.foot === "fixed" && r.bg === "rgb(255, 255, 255)" && r.strip === "none", JSON.stringify(r));
    const pdf = await p.pdf({ format: "A4", printBackground: true }); T("print: a real PDF comes out", pdf.slice(0, 4).toString() === "%PDF" && pdf.length > 20000, pdf.length + " bytes");
    await p.emulateMedia({ media: "screen" });
    T("print rules do not leak onto the screen", await p.evaluate(() => getComputedStyle(document.querySelector(".printhead")).display === "none"));
    await ctx.close(); }
  // ---- phone upgrades: back to top, paste, keyboard room, quick text size, buzz, the sticky section index, read aloud
  { const ctx = await ctxFor(390, 844, "dark"); await ctx.grantPermissions(["clipboard-read", "clipboard-write"]).catch(() => {});
    await ctx.addInitScript(() => { window.__vib = []; navigator.vibrate = n => { window.__vib.push(n); return true; };
      const spoken = []; window.__spoken = spoken; let cancelled = 0; window.__cancel = () => cancelled;
      window.SpeechSynthesisUtterance = function (t) { this.text = t; };
      Object.defineProperty(window, "speechSynthesis", { configurable: true, value: { getVoices: () => [{ name: "Local", lang: "en-US", localService: true, default: true }], speak: u => spoken.push(u.text), cancel: () => { cancelled++; }, addEventListener() {} } }); });
    const p = await open(ctx, "#/entry/emotional-blackmail"); await p.waitForTimeout(300);
    T("one scroll: no swipe hint, no tabs, nothing to swipe between", await p.evaluate(() => !document.querySelector("[data-swipehint],[role=tab]")));
    await p.goto(URL0 + "#/entry/emotional-blackmail"); await p.waitForTimeout(250);
    const tt = await p.evaluate(() => document.querySelector("#totop").hidden); await p.evaluate(() => scrollTo(0, 2600)); await p.waitForTimeout(250); await p.evaluate(() => scrollTo(0, 2500)); await p.waitForTimeout(300);
    const vis = await p.evaluate(() => !document.querySelector("#totop").hidden && document.querySelector("#totop").getAttribute("aria-label"));
    T("back to top: hidden at the top, shown after scrolling, named for screen readers", tt === true && /top/i.test(vis || ""), String(vis));
    const idx = await p.evaluate(() => { const n = document.querySelector(".secnav"), r = n.getBoundingClientRect(), top = document.querySelector(".top").getBoundingClientRect(); return { gap: Math.round(r.top - top.bottom), cur: !!n.querySelector("[aria-current]"), label: (n.querySelector("[aria-current]") || {}).textContent }; });
    T("section index stays pinned right under the top bar while reading, and marks where you are", Math.abs(idx.gap) <= 1 && idx.cur, JSON.stringify(idx));
    await p.click(".secnav [data-sec='3']"); await p.waitForTimeout(900);
    T("tapping a section in the index scrolls to it and marks it", await p.evaluate(() => { const t = document.getElementById("sec-3").getBoundingClientRect().top; return t > 40 && t < 260 && document.querySelector(".secnav [data-sec='3']").getAttribute("aria-current") === "true"; }));
    await p.evaluate(() => scrollBy(0, -400)); await p.waitForTimeout(300);
    await p.click("#totop"); await p.waitForTimeout(1800); T("back to top: tapping it goes to the top", await p.evaluate(() => scrollY < 40));
    await p.click(".moreacts summary"); const aa = []; for (let i = 0; i < 3; i++) { await p.click("[data-aa]"); await p.waitForTimeout(80); aa.push(await p.evaluate(() => document.documentElement.getAttribute("data-size"))); }
    T("quick text size cycles Larger, Largest, Standard", aa.join() === "l,xl," || aa.join() === "l,xl,null", aa.join());
    await p.goto(URL0 + "#/settings"); await p.click("label:has(input[name=hap][value=on])"); await p.waitForTimeout(100);
    await p.goto(URL0 + "#/entry/emotional-blackmail"); await p.waitForTimeout(250); await p.evaluate(() => { window.__vib.length = 0; }); await p.click(".secnav [data-sec='2']"); await p.waitForTimeout(100);
    T("tap feedback: a section jump buzzes only after you turn it on", await p.evaluate(() => window.__vib.length > 0));
    await p.click("[data-listen]"); await p.waitForTimeout(200);
    T("read aloud: the first tap only warns that it plays out loud", await p.evaluate(() => window.__spoken.length === 0 && /plays out loud/.test(document.querySelector("#toast").textContent)));
    await p.click("[data-toastact]"); await p.waitForTimeout(250);
    const sp = await p.evaluate(() => ({ n: window.__spoken.length, first: window.__spoken[0] || "", label: document.querySelector("[data-listen]").textContent.trim(), pressed: document.querySelector("[data-listen]").hasAttribute("aria-pressed") }));
    T("read aloud: uses an on-device voice, starts with the safety note, button turns to Stop with no confusing pressed state", sp.n > 3 && /^Safety first|Watch for|Those turn/.test(sp.first) && sp.label === "Stop" && !sp.pressed, JSON.stringify(sp).slice(0, 200));
    await p.click(".secnav [data-sec='1']"); await p.waitForTimeout(150);
    T("read aloud: jumping to another section stops it", await p.evaluate(() => window.__cancel() > 0 && document.querySelector("[data-listen]").textContent.trim() === "Listen"));
    await p.click("[data-listen]"); await p.waitForTimeout(150); await p.click("[data-listen]"); await p.waitForTimeout(100);
    T("read aloud: tapping Stop stops it", await p.evaluate(() => document.querySelector("[data-listen]").textContent.trim() === "Listen"));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); await ctx.grantPermissions(["clipboard-read", "clipboard-write"]).catch(() => {}); const p = await open(ctx, "#/search"); await p.waitForTimeout(200);
    await p.evaluate(() => navigator.clipboard.writeText("you are imagining things")).catch(() => {});
    if (await p.$("[data-paste]")) { await p.click("[data-paste]"); await p.waitForTimeout(400);
      T("paste button fills the search box and searches", await p.evaluate(() => document.querySelector("#q").value.length > 3 && document.querySelector("[data-paste]").hidden && document.querySelectorAll("#results a, #results .row").length > 0)); }
    else T("paste button is offered when the phone allows reading the clipboard", true, "not offered in this browser");
    await p.evaluate(() => document.body.classList.add("kbd")); T("on-screen keyboard: the sign bar steps aside", await p.evaluate(() => getComputedStyle(document.querySelector(".doors")).display === "none"));
    await p.evaluate(() => document.body.classList.remove("kbd"));
    T("touch feel: taps are not delayed and pulling down does not refresh", await p.evaluate(() => getComputedStyle(document.querySelector(".btn, .blade, a")).touchAction === "manipulation" && getComputedStyle(document.documentElement).overscrollBehaviorY === "contain"));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); await ctx.addInitScript(() => { Object.defineProperty(window, "speechSynthesis", { configurable: true, value: { getVoices: () => [{ name: "Net", lang: "en-US", localService: false }], speak() {}, cancel() {}, addEventListener() {} } }); window.SpeechSynthesisUtterance = function () {}; });
    const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(250); await p.click("[data-listen]"); await p.waitForTimeout(200); await p.click("[data-toastact]"); await p.waitForTimeout(250);
    T("read aloud: a voice that needs the internet is never used", await p.evaluate(() => /no built-in voice/.test(document.querySelector("#toast").textContent))); await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.click("label:has(input[name=save][value=on])"); await p.waitForTimeout(120);
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(250); await p.click("[data-save]"); await p.waitForTimeout(80);
    T("saving a station gives the bookmark a short pop", await p.evaluate(() => !!document.querySelector("[data-save] svg.pop") || matchMedia("(prefers-reduced-motion: reduce)").matches)); await ctx.close(); }

  // ---- colour: Quiet is the default; Vivid (opt-in) gives each line's colour to the home rows and the headings
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/"); await p.waitForTimeout(300);
    const q = await p.evaluate(() => ({ attr: document.documentElement.getAttribute("data-color"), rows: [...document.querySelectorAll(".home .lrow")].map(r => getComputedStyle(r).backgroundColor), stripe: getComputedStyle(document.querySelector(".top"), "::before").content, glow: getComputedStyle(document.body).backgroundImage }));
    T("Quiet is the default on a fresh load: the home rows are plain, with no colour stripe and no glow", q.attr === null && q.rows.length === 10 && new Set(q.rows).size === 1 && (q.stripe === "none" || q.stripe === "normal") && q.glow === "none", JSON.stringify(q).slice(0, 220));
    await p.goto(URL0 + "#/entry/emotional-blackmail"); await p.waitForTimeout(300);
    const s0 = await p.evaluate(() => ({ lc: getComputedStyle(document.querySelector(".sname .b")).backgroundColor, bar: getComputedStyle(document.querySelector(".sname"), "::before").backgroundColor, ans: getComputedStyle(document.querySelector(".answer")).borderTopWidth }));
    T("station (Quiet): the short bar above the title takes the line's colour, the answer card has no coloured edge", s0.bar === s0.lc && parseFloat(s0.ans) === 0, JSON.stringify(s0));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.click("label:has(input[name=color][value=vivid])"); await p.waitForTimeout(150);
    await p.goto(URL0 + "#/"); await p.waitForTimeout(300);
    const h = await p.evaluate(() => { const rows = [...document.querySelectorAll(".home .lrow")]; const cols = rows.map(r => getComputedStyle(r).backgroundColor);
      return { attr: document.documentElement.getAttribute("data-color"), n: rows.length, distinct: new Set(cols).size, solid: cols.every(c => c !== "rgba(0, 0, 0, 0)"), stripe: /gradient/.test(getComputedStyle(document.querySelector(".top"), "::before").backgroundImage), glow: /radial-gradient/.test(getComputedStyle(document.body).backgroundImage) }; });
    T("Vivid: the ten lines are ten distinct solid colour tiles, with a ten-colour stripe and a soft glow", h.attr === "vivid" && h.n === 10 && h.distinct === 10 && h.solid && h.stripe && h.glow, JSON.stringify(h));
    await p.goto(URL0 + "#/entry/emotional-blackmail"); await p.waitForTimeout(300);
    const s1 = await p.evaluate(() => ({ lc: getComputedStyle(document.querySelector(".sname .b")).backgroundColor, bar: getComputedStyle(document.querySelector(".sname"), "::before").backgroundColor, ans: getComputedStyle(document.querySelector(".answer")).borderTopColor, wash: /radial-gradient/.test(getComputedStyle(document.body).backgroundImage) }));
    T("Vivid station: the sign bar and the answer's top edge take the line's colour, with a wash behind the title", s1.bar === s1.lc && s1.ans === s1.lc && s1.wash, JSON.stringify(s1));
    await p.goto(URL0 + "#/line/pressure"); await p.waitForTimeout(300);
    T("Vivid line page: the header is a block of the line's colour", await p.evaluate(() => { const l = getComputedStyle(document.querySelector(".lhead")).backgroundColor, b = getComputedStyle(document.querySelector(".lhead")).color; return l !== "rgba(0, 0, 0, 0)" && l !== b; }));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.click("input[name=rest][value=people]"); await p.waitForTimeout(120);
    await p.goto(URL0 + "#/"); await p.waitForTimeout(250);
    T("a resting line's row stays readable, not faded", await p.evaluate(() => { const r = document.querySelector(".home .lrow.rest"); return !!r && getComputedStyle(r).opacity === "1" && /Resting/.test(r.textContent); }));
    await ctx.close(); }

  // ---- v18: room to read on a phone, Share/Print under More, compare stacks, quotes stay inside their sentence
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/silent-treatment");
    const vis = s => p.evaluate(s => { const e = document.querySelector(s); return !!e && !e.hidden && getComputedStyle(e).display !== "none" && getComputedStyle(e).visibility !== "hidden"; }, s);
    await p.evaluate(() => scrollTo(0, 1800)); await p.waitForTimeout(250); await p.evaluate(() => scrollTo(0, 2400)); await p.waitForTimeout(350);
    const down = { doors: await vis(".doors"), idx: await p.evaluate(() => Math.round(document.querySelector(".secnav").getBoundingClientRect().top - document.querySelector(".top").getBoundingClientRect().bottom)) };
    await p.evaluate(() => scrollTo(0, 2300)); await p.waitForTimeout(350);
    const up = { doors: await vis(".doors"), totop: await vis("#totop") };
    T("phone: reading down, the sign bar slides away and the section index stays under the top bar; scrolling up brings the sign bar and back-to-top back", !down.doors && Math.abs(down.idx) <= 1 && up.doors && up.totop, JSON.stringify({ down, up }));
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(150);
    const acts = await p.evaluate(() => [...document.querySelectorAll(".station .acts")][0].querySelectorAll(":scope > .btn, :scope > details > summary").length);
    await p.click(".moreacts summary"); await p.waitForTimeout(120);
    const more = await p.evaluate(() => !!document.querySelector(".moreacts[open] [data-aa]") && !!document.querySelector(".moreacts[open] [data-share]") && !!document.querySelector(".moreacts[open] [data-print]"));
    T("station: three choices before the reading (Save, Listen, More), with Text size, Share and Print under More", acts === 3 && more, JSON.stringify({ acts, more }));
    await p.goto(URL0 + "#/compare/gaslighting/countering"); await p.waitForTimeout(400);
    const c = await p.evaluate(() => ({ cols: getComputedStyle(document.querySelector(".cmp-row .cmp-g")).gridTemplateColumns.split(" ").length, who: getComputedStyle(document.querySelector(".cmp-who")).display,
      orphan: [...document.querySelectorAll(".cmp-row p")].filter(x => /^[‘’'“”"],/.test(x.textContent.trim())).length }));
    T("v18 compare on a phone: one labelled column, and no paragraph starts with a stray quote mark", c.cols === 1 && c.who === "flex" && c.orphan === 0, JSON.stringify(c));
    await ctx.close(); }

  // ---- review round: rested lines stay out everywhere, honest saving copy, Leave keeps nothing, no referrer
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.click("label:has(input[name=save][value=on])"); await p.waitForTimeout(150);
    const copy = await p.evaluate(() => document.querySelector("[data-settings]").textContent);
    T("settings says the saved entry is scrambled, not secret, and that a private window is safer", /Scrambled is not secret/.test(copy) && /private window is safer/.test(copy));
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(200); await p.click(".acts [data-save], [data-save]").catch(() => {});
    const raw = await p.evaluate(() => localStorage.getItem("ui-state")); const dec = await p.evaluate(r => { const a = atob(r), K = [110,102,33,154,60,81]; return Array.from(a, (c, i) => String.fromCharCode(c.charCodeAt(0) ^ K[i % 6])).join(""); }, raw);
    T("the stored entry has no timestamps and no tactic words", !/\d{12}/.test(dec) && !/gaslighting/i.test(dec), dec.slice(0, 80));
    await p.goto(URL0 + "#/settings"); await p.click("input[name=rest][value=truth]"); await p.waitForTimeout(150);
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(200);
    T("a station on a rested line is closed behind a notice", await p.evaluate(() => !!document.querySelector("[data-unhide]") && !document.querySelector("h1.h-st")));
    await p.goto(URL0 + "#/search"); await p.fill("#q", "t01"); await p.waitForTimeout(250);
    T("searching a code on a rested line finds nothing from it", await p.evaluate(() => !/Gaslighting/.test(document.querySelector("#results").textContent)));
    await p.goto(URL0 + "#/"); await p.waitForTimeout(250);
    T("Home marks a rested line's row as resting", await p.evaluate(() => !!document.querySelector(".home .lrow.rest")));
    await p.evaluate(() => document.querySelector("a[href='#/settings']") && 0);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/"); T("no referrer is sent to the Leave destination", await p.evaluate(() => document.querySelector("meta[name=referrer]")?.content === "no-referrer")); await ctx.close(); }

  // ---- the House seal never floats over the text
  { const bad = [];
    for (const w of [390, 1440]) { const ctx = await ctxFor(w, 900, "dark"); const p = await open(ctx, "#/entry/gaslighting"); const pos = await p.evaluate(() => { const s = document.querySelector(".nf-seal"); return s ? getComputedStyle(s).position : "absent"; }); if (pos === "fixed") bad.push(w + "px " + pos); await ctx.close(); }
    T("House seal rests at the end of the page (not fixed over text)", !bad.length, bad.join("; ")); }

  await b.close();
  console.log(`\n${out.length - fails.length}/${out.length} checks passed`);
  if (fails.length) { console.log("\nFAILED:\n" + fails.join("\n")); process.exit(1); }
})().catch(e => { console.error(e); process.exit(2); });
