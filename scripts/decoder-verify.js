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
  T("no external requests in markup (only the approved beacon)", (() => { const h = html.toString("utf8").replace(/<script[^>]*cloudflareinsights[^>]*><\/script>/, "");
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
        if (document.querySelectorAll("[role=tabpanel]").length !== 4) o.push("not four steps");
        if (document.querySelectorAll("[role=tab]").length !== 4) o.push("not four tabs");
        return o;
      }, st.sens);
      if (r.length) bad.push(st.n + ": " + r.join(", "));
      if (p._errs.length) { bad.push(st.n + ": script error " + p._errs[0]); p._errs.length = 0; }
    }
    T(`stations render cleanly at ${label} (${pick.length})`, !bad.length, bad.slice(0, 4).join(" | ") + (bad.length > 4 ? ` (+${bad.length - 4} more)` : ""));
    await ctx.close();
  }

  // ---- how long is a full read on a phone, folded?
  { const ctx = await ctxFor(390, 844); const p = await open(ctx, "#/entry/gaslighting");
    const m = await p.evaluate(() => { const panels = [...document.querySelectorAll("[role=tabpanel]")], vh = innerHeight, per = [];
      panels.forEach(x => x.hidden = true); const base = document.documentElement.scrollHeight;
      panels.forEach((x, i) => { x.hidden = false; per.push(document.documentElement.scrollHeight / vh); x.hidden = true; });
      panels.forEach(x => x.hidden = false); const all = document.documentElement.scrollHeight / vh; return { per, base: base / vh, all }; });
    const worst = Math.max(...m.per);
    T("Gaslighting on a phone: the longest single step view is ≤ 6 screens (v14: one page of 16.5)", worst <= 6, "step views " + m.per.map(x => x.toFixed(1)).join(" / ") + " screens; all four open at once " + m.all.toFixed(1)); await ctx.close(); }

  // ---- reflow: 320px wide and the Largest text size (WCAG 1.4.4 / 1.4.10)
  { const bad = [];
    for (const size of ["m", "xl"]) { const ctx = await ctxFor(320, 640, "dark"); const p = await open(ctx, "#/"); await p.evaluate(sz => document.documentElement.setAttribute("data-size", sz), size);
      for (const pg of ["#/", "#/entry/emotional-blackmail", "#/entry/pseudo-profundity-intellectual-intimidation", "#/help", "#/search", "#/map", "#/line/truth", "#/compare/gaslighting/countering", "#/routes/grooming", "#/settings", "#/safety", "#/lines/where"]) {
        await p.goto(URL0 + pg); await p.evaluate(sz => document.documentElement.setAttribute("data-size", sz), size); await p.evaluate(() => document.querySelectorAll("[role=tabpanel]").forEach(x => x.hidden = false)); await p.waitForTimeout(80);
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
    T("private: the query is not in the address", !/silent/.test(z.url)); T("private: neutral tab title", z.title === "Pattern Decoder", z.title);
    await p.goto(URL0 + "#/entry/gaslighting"); await p.waitForTimeout(100);
    T("private: station links use numbers", await p.evaluate(() => [...document.querySelectorAll("a[href^='#/']")].filter(a => /entry|line\/|compare\/|routes\/./.test(a.getAttribute("href"))).length === 0));
    await ctx.close(); }

  // ---- axe on each page type, both themes, both widths
  if (!axeSrc) { T("axe-core accessibility scan", false, "axe-core not found: run `npm i --no-save axe-core`"); }
  else {
    const pages = ["#/", "#/entry/gaslighting", "#/entry/emotional-blackmail", "#/search", "#/help", "#/map", "#/line/truth", "#/compare/gaslighting/countering", "#/routes", "#/routes/grooming", "#/lines/az", "#/lines/where", "#/saved", "#/settings", "#/safety", "#/updates"];
    const bad = [], minor = {}; let scans = 0;
    for (const scheme of ["dark", "light"]) for (const [w, h] of [[390, 844], [1440, 900]]) {
      const ctx = await ctxFor(w, h, scheme); const p = await open(ctx, "#/");
      for (const pg of pages) { await p.goto(URL0 + pg); await p.waitForTimeout(120);
        if (pg === "#/search") { await p.fill("#q", "silent treatment"); await p.waitForTimeout(250); }
        if (pg === "#/entry/gaslighting") { await p.evaluate(() => document.querySelectorAll("[role=tabpanel]").forEach(x => x.hidden = false)); }
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
      for (const pg of ["#/", "#/entry/emotional-blackmail", "#/help", "#/search", "#/line/truth", "#/map", "#/settings", "#/safety"]) { await p.goto(URL0 + pg); await p.waitForTimeout(120);
        if (pg.includes("emotional")) await p.evaluate(() => document.querySelectorAll("[role=tabpanel]").forEach(x => x.hidden = false));
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
  { const ctx = await ctxFor(390, 844); const p = await open(ctx, "#/entry/gaslighting"); await p.evaluate(() => document.querySelectorAll("[role=tabpanel]").forEach(x => x.hidden = false));
    const small = await p.evaluate(() => { const o = [], w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue; const el = n.parentElement; if (el.closest(".nf-chrome,.nf-panel,.sr-only,[hidden],script,style")) continue; const px = parseFloat(getComputedStyle(el).fontSize); if (px < 13) o.push(Math.round(px * 10) / 10 + "px " + (el.className || el.tagName)); } return o; });
    T("no text smaller than 13px (v14: 13–14px italic labels)", !small.length, small.slice(0, 4).join("; ")); await ctx.close(); }

  // ---- load timing, phone with a 4x CPU slowdown
  { const runs = [];
    for (let i = 0; i < 3; i++) { const ctx = await ctxFor(390, 844, "dark"); const p = await ctx.newPage();
      await p.addInitScript(() => { window.__lt = []; window.__lcp = 0; new PerformanceObserver(l => l.getEntries().forEach(e => window.__lt.push(e.duration))).observe({ type: "longtask", buffered: true });
        new PerformanceObserver(l => l.getEntries().forEach(e => { window.__lcp = e.startTime; })).observe({ type: "largest-contentful-paint", buffered: true }); });
      const cdp = await ctx.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
      await p.goto(URL0 + "#/"); await p.waitForFunction(() => document.querySelector("h1") && document.fonts.status === "loaded"); await p.waitForTimeout(800);
      const m = await p.evaluate(() => { const nav = performance.getEntriesByType("navigation")[0], fcp = performance.getEntriesByName("first-contentful-paint")[0];
        return { dcl: nav.domContentLoadedEventEnd, fcp: fcp ? fcp.startTime : 0, lcp: window.__lcp, longest: Math.max(0, ...window.__lt), total: window.__lt.reduce((a, b) => a + b, 0) }; });
      runs.push(m); await ctx.close(); }
    const med = k => runs.map(r => r[k]).sort((a, b) => a - b)[1];
    console.log("  timing, 4x CPU, median of 3:", ["dcl", "fcp", "lcp", "longest", "total"].map(k => k + " " + Math.round(med(k)) + "ms").join(", "), "(v14 on the same setup: headline at 3400ms, longest task 836ms, long tasks 1100ms)");
    T("home: first content in ≤ 1200 ms on a 4x slowdown", med("fcp") <= 1200, Math.round(med("fcp")) + " ms");
    T("home: largest paint in ≤ 1500 ms", med("lcp") <= 1500, Math.round(med("lcp")) + " ms");
    T("home: longest main-thread task ≤ 150 ms", med("longest") <= 150, Math.round(med("longest")) + " ms");
    T("home: total long-task time ≤ 250 ms", med("total") <= 250, Math.round(med("total")) + " ms"); }

  // ---- response to a tap: search typing and opening a station, 4x slowdown
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/search"); const cdp = await ctx.newCDPSession(p); await cdp.send("Emulation.setCPUThrottlingRate", { rate: 4 });
    const t = await p.evaluate(async () => { const q = document.querySelector("#q"); const ts = []; for (const s of ["s", "si", "sil", "sile", "silen", "silent"]) { const t0 = performance.now(); q.value = s; q.dispatchEvent(new Event("input", { bubbles: true })); await new Promise(r => setTimeout(r, 140)); ts.push(performance.now() - t0 - 140); } return ts; });
    const open1 = await p.evaluate(async () => { const t0 = performance.now(); location.hash = "#/entry/gaslighting"; await new Promise(r => { const iv = setInterval(() => { if (document.querySelector("h1.h-st")) { clearInterval(iv); r(); } }, 4); }); return performance.now() - t0; });
    T("typing in search: slowest keystroke response ≤ 200 ms (4x slowdown)", Math.max(...t) <= 200, Math.round(Math.max(...t)) + " ms");
    T("opening a station (first time, parses its line's data) ≤ 200 ms (4x slowdown)", open1 <= 200, Math.round(open1) + " ms"); await ctx.close(); }

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
    const r = await p.evaluate(() => ({ anim: document.getAnimations().length, hidden: [...document.querySelectorAll("main *")].filter(e => getComputedStyle(e).opacity === "0" && e.offsetParent).length }));
    T("reduced motion: no running animations and nothing stuck transparent", r.anim === 0 && r.hidden === 0, JSON.stringify(r)); await ctx.close(); }

  // ---- idle cost: no animation loop
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(600);
    const frames = await p.evaluate(() => new Promise(res => { let n = 0; const o = new MutationObserver(() => n++); o.observe(document.body, { subtree: true, attributes: true, childList: true, characterData: true }); const anims = document.getAnimations().length; setTimeout(() => res({ mutations: n, anims }), 3000); }));
    T("idle: nothing changes or animates on its own for 3 s", frames.mutations === 0 && frames.anims === 0, JSON.stringify(frames)); await ctx.close(); }

  await b.close();
  console.log(`\n${out.length - fails.length}/${out.length} checks passed`);
  if (fails.length) { console.log("\nFAILED:\n" + fails.join("\n")); process.exit(1); }
})().catch(e => { console.error(e); process.exit(2); });
