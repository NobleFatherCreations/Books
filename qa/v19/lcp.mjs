// which element is the LCP, and when (same conditions as scripts/seo/perf.js)
import { chromium } from 'playwright';
const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }); const p = await ctx.newPage();
const cdp = await ctx.newCDPSession(p);
await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
await p.addInitScript(() => { window.__l = []; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__l.push([Math.round(e.startTime), e.element ? (e.element.tagName + '.' + e.element.className + ' ' + (e.url || '').split('/').pop()) : '?', e.size]); }).observe({ type: 'largest-contentful-paint', buffered: true }); });
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'load' }); await p.waitForTimeout(9000);
console.log(JSON.stringify(await p.evaluate(() => window.__l)));
await b.close();
