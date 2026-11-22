// Core Web Vitals in the lab (web-perf skill, no DevTools MCP): mobile 375px, slow-4G, 4x CPU throttle.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const url of process.argv.slice(2)) {
    const ctx = await b.newContext({ viewport: { width: 375, height: 812 } });
    const p = await ctx.newPage();
    const cdp = await ctx.newCDPSession(p);
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    let bytes = 0, reqs = 0; p.on('response', async r => { reqs++; try { bytes += (await r.body()).length } catch (e) {} });
    await p.addInitScript(() => {
      window.__v = { lcp: 0, cls: 0 };
      new PerformanceObserver(l => { for (const e of l.getEntries()) window.__v.lcp = e.startTime }).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__v.cls += e.value }).observe({ type: 'layout-shift', buffered: true });
    });
    await p.goto(url, { waitUntil: 'load', timeout: 120000 }); await p.waitForTimeout(1500);
    const v = await p.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; const f = performance.getEntriesByName('first-contentful-paint')[0];
      return { ttfb: Math.round(n.responseStart), fcp: Math.round(f ? f.startTime : 0), lcp: Math.round(window.__v.lcp), cls: +window.__v.cls.toFixed(3), html: n.transferSize || n.encodedBodySize } });
    console.log(url.replace(/^https?:\/\/[^/]+/, '').padEnd(42), `TTFB ${v.ttfb}ms  FCP ${v.fcp}ms  LCP ${v.lcp}ms  CLS ${v.cls}  requests ${reqs}  bytes ${(bytes / 1024).toFixed(0)}KB`);
    await ctx.close();
  }
  await b.close();
})();
