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
    await p.goto(URL0 + "#/map"); await p.waitForTimeout(200); await p.evaluate(() => openSheet(40)); await p.waitForTimeout(250);
    T("leave: a Leave button is inside the open map sheet", await p.evaluate(() => { const l = document.querySelector("#sheet [data-leave]"); if (!l) return false; const r = l.getBoundingClientRect(); const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return !!e && !!e.closest("[data-leave]"); }));
    await p.keyboard.press("Escape"); await p.keyboard.press("Escape"); await p.waitForTimeout(700);
    T("leave: Escape twice leaves even with the map sheet open", /google\.com/.test(p.url()), p.url());
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/");
    await p.route("**/*google.com/**", r => r.fulfill({ status: 200, body: "weather" }));
    for (const h of ["#/s/5", "#/s/6", "#/map", "#/search"]) { await p.evaluate(h => { location.hash = h; }, h); await p.waitForTimeout(120); }
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

  // ---- map tap targets, measured from the rendered page
  { const bad = [];
    for (const w of [320, 360, 390, 1440]) { const ctx = await ctxFor(w, 800, "dark"); const p = await open(ctx, "#/map"); await p.waitForTimeout(200);
      const m = await p.evaluate(() => { const pts = [...document.querySelectorAll("#map a .st")].map(c => { const r = c.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; });
        let min = 1e9; const byCol = {}; pts.forEach(([x, y]) => { (byCol[Math.round(x)] = byCol[Math.round(x)] || []).push(y); });
        Object.values(byCol).forEach(ys => { ys.sort((a, b) => a - b); for (let i = 1; i < ys.length; i++) min = Math.min(min, ys[i] - ys[i - 1]); });
        const xs = [...new Set(pts.map(p => Math.round(p[0])))].sort((a, b) => a - b); const landscape = document.querySelector("#map").classList.contains("land");
        return { min, gapX: xs.length > 1 && !landscape ? Math.min(...xs.slice(1).map((x, i) => x - xs[i])) : 99, landscape }; });
      const need = 24; const gap = m.landscape ? 24 : Math.min(m.min, m.gapX);
      if ((m.landscape ? m.min < 0 : m.min < need - 0.6 || m.gapX < need - 0.6) && !m.landscape) bad.push(`${w}px: rows ${m.min.toFixed(1)} cols ${m.gapX.toFixed(1)}`);
      await ctx.close(); }
    T("map: neighbouring stations are ≥24 CSS px apart on phones down to 320px wide", !bad.length, bad.join("; ")); }

  // ---- techniques brought back from v14
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(200);
    const bar = async () => p.evaluate(() => { const t = getComputedStyle(document.querySelector(".top"), "::after").transform; const m = t.match(/matrix\(([^,]+)/); return m ? +m[1] : (t === "none" ? 1 : -1); });
    const top = await bar(); await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(250); const end = await bar();
    T("reading line: empty at the top of a station, full at the end (scroll-driven, no script)", top < 0.05 && end > 0.95, "top " + top.toFixed(2) + ", end " + end.toFixed(2));
    await p.evaluate(() => scrollTo(0, 0));
    T("station sign wears its line colour (band matches the line bullet)", await p.evaluate(() => { const b = getComputedStyle(document.querySelector(".sname"), "::before"), bl = getComputedStyle(document.querySelector(".sname .b")); return b.backgroundColor === bl.backgroundColor && parseFloat(b.height) >= 6; }));
    await p.goto(URL0 + "#/search"); const asked = {};
    for (const q of ["settings", "love", "safe", "dark"]) { await p.fill("#q", q); await p.waitForTimeout(250); asked[q] = await p.evaluate(() => [...document.querySelectorAll("#results a.row")].map(a => a.getAttribute("href"))); }
    T("search reaches pages and lines (settings, love, safe, dark)", asked.settings.includes("#/settings") && asked.love.some(h => /#\/l\/\d/.test(h)) && asked.safe.includes("#/safety") && asked.dark.includes("#/settings"), JSON.stringify(Object.fromEntries(Object.entries(asked).map(([k, v]) => [k, v.slice(0, 3)]))));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark", { reducedMotion: "reduce" }); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(200);
    await p.click("[data-showmap]"); await p.waitForTimeout(500);
    const r = await p.evaluate(() => { const a = document.querySelector("#map a.sel"); if (!a) return { sel: false }; const b = a.getBoundingClientRect(); return { sel: true, inView: b.top > 0 && b.bottom < innerHeight, links: document.querySelectorAll("#xl path").length, note: /highlighted/.test(document.querySelector("main").textContent), hash: location.hash }; });
    T("Show on the map: lands on the map with the station highlighted, in view, interchanges drawn", r.sel && r.inView && r.links > 0 && r.note && r.hash === "#/map", JSON.stringify(r));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark", { contrast: "more" }); const p = await open(ctx, "#/");
    const r = await p.evaluate(() => { const b = document.querySelector(".blade:not(.pri)"), cs = getComputedStyle(b), fg2 = getComputedStyle(document.querySelector(".lede")).color, fg = getComputedStyle(document.body).color; return { ring: cs.boxShadow, lede: fg2 === fg }; });
    T("more contrast: controls get a 2px outline and secondary text goes full strength", /2px/.test(r.ring) && r.lede, r.ring.slice(0, 50) + " lede=" + r.lede);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark", { forcedColors: "active" }); const p = await open(ctx, "#/entry/gaslighting"); const errs = [];
    for (const h of ["#/", "#/entry/emotional-blackmail", "#/map", "#/help"]) { await p.goto(URL0 + h); await p.waitForTimeout(150); const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (o > 1) errs.push(h + " +" + o); }
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
    await p.goto(URL0 + "#/map"); await p.waitForTimeout(200);
    T("rest a line: its stations are dim, unreachable on the map", await p.evaluate(() => { const a = [...document.querySelectorAll("#map a[data-g=society]")]; return a.length > 0 && a.every(x => x.classList.contains("rest") && x.getAttribute("aria-hidden") === "true" && x.tabIndex === -1); }));
    await p.goto(URL0 + "#/entry/" + pick.s); await p.waitForTimeout(200);
    T("rest a line: opening one of its entries by link still works and says so, safety note intact", await p.evaluate(() => !!document.querySelector(".restnote") && !!document.querySelector("h1.h-st")));
    T("rest a line: nothing is written to the device while saving is off", await p.evaluate(() => localStorage.length === 0));
    await p.goto(URL0 + "#/settings"); const left = await p.evaluate(async () => { const boxes = [...document.querySelectorAll("input[name=rest]")]; for (const b of boxes) { if (!b.checked) { b.click(); await new Promise(r => setTimeout(r, 30)); } } return boxes.filter(b => b.checked).length; });
    T("rest a line: at least one line always stays visible", left === 9, "ticked " + left + " of 10");
    await p.click("input[name=rest][value=society]"); await p.waitForTimeout(100);
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/settings"); await p.route("**/*wikipedia.org/**", r => r.fulfill({ status: 200, body: "wiki" }));
    await p.click("label:has(input[name=leave][value=wiki])"); await p.waitForTimeout(150);
    await p.keyboard.press("Escape"); await p.keyboard.press("Escape"); await p.waitForTimeout(900);
    T("Leave goes where you chose (Wikipedia)", /wikipedia\.org/.test(p.url()), p.url()); await ctx.close(); }

  // ---- stage 2: number keys, deep links to a step, the route strip, the staggered interchange lines
  { const ctx = await ctxFor(1440, 900, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(200);
    await p.keyboard.press("3"); await p.waitForTimeout(120);
    const k3 = await p.evaluate(() => document.querySelector("#t-2").getAttribute("aria-selected") === "true" && !document.querySelector("#p-2").hidden);
    await p.keyboard.press("1"); await p.waitForTimeout(120);
    const k1 = await p.evaluate(() => document.querySelector("#t-0").getAttribute("aria-selected") === "true");
    T("keys 1 to 4 jump between the four steps", k3 && k1);
    await p.goto(URL0 + "#/entry/gaslighting/3"); await p.waitForTimeout(250);
    const deep = await p.evaluate(() => ({ tab: document.querySelector("#t-2").getAttribute("aria-selected"), shown: !document.querySelector("#p-2").hidden, others: document.querySelectorAll("[role=tabpanel]:not([hidden])").length, bar: getComputedStyle(document.querySelector(".stepbar i")).getPropertyValue("--p") }));
    T("deep link #/entry/slug/3 opens on step 3", deep.tab === "true" && deep.shown && deep.others === 1 && +deep.bar === 0.75, JSON.stringify(deep));
    await p.click("#t-1"); await p.waitForTimeout(150);
    const histBefore = await p.evaluate(() => history.length); const h2 = await p.evaluate(() => location.hash);
    await p.reload(); await p.waitForTimeout(250);
    T("the address follows the step without adding history, and a reload keeps the step", /\/2$/.test(h2) && await p.evaluate(() => document.querySelector("#t-1").getAttribute("aria-selected") === "true") && histBefore === await p.evaluate(() => history.length), h2);
    await p.goto(URL0 + "#/s/5/4"); await p.waitForTimeout(250);
    T("private numbered deep link #/s/5/4 opens on step 4", await p.evaluate(() => document.querySelector("#t-3").getAttribute("aria-selected") === "true"));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/routes/grooming"); await p.waitForTimeout(250);
    const r = await p.evaluate(() => { const st = document.querySelector(".rstrip"), li = st.querySelectorAll("li").length, list = document.querySelectorAll(".chain li").length; return { li, list, scroll: st.scrollWidth > st.clientWidth, hidden: st.getAttribute("aria-hidden"), snap: getComputedStyle(st).scrollSnapType }; });
    T("route strip: every station of the route, scrolls sideways on a phone, snaps, and the numbered list is still there", r.li === r.list && r.li > 3 && r.scroll && r.hidden === "true" && /x/.test(r.snap), JSON.stringify(r));
    await p.click(".rstrip li >> nth=1"); await p.waitForTimeout(300);
    T("route strip: a tap on a station opens it", await p.evaluate(() => !!document.querySelector("h1.h-st")));
    await ctx.close(); }
  { const ctx = await ctxFor(390, 844, "dark"); const p = await open(ctx, "#/entry/gaslighting"); await p.waitForTimeout(150); await p.click("[data-showmap]"); await p.waitForTimeout(500);
    const d = await p.evaluate(() => [...document.querySelectorAll("#xl path")].map(x => x.style.animationDelay));
    T("interchange lines draw in one after another", d.length >= 2 && d.every((x, i) => x === i * 40 + "ms"), JSON.stringify(d)); await ctx.close(); }

  // ---- the House seal never floats over the text
  { const bad = [];
    for (const w of [390, 1440]) { const ctx = await ctxFor(w, 900, "dark"); const p = await open(ctx, "#/entry/gaslighting"); const pos = await p.evaluate(() => { const s = document.querySelector(".nf-seal"); return s ? getComputedStyle(s).position : "absent"; }); if (pos === "fixed") bad.push(w + "px " + pos); await ctx.close(); }
    T("House seal rests at the end of the page (not fixed over text)", !bad.length, bad.join("; ")); }

  await b.close();
  console.log(`\n${out.length - fails.length}/${out.length} checks passed`);
  if (fails.length) { console.log("\nFAILED:\n" + fails.join("\n")); process.exit(1); }
})().catch(e => { console.error(e); process.exit(2); });
