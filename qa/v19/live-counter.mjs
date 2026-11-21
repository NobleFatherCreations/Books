import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage();
await p.goto('https://noblefathercreations.com/', { waitUntil: 'networkidle' }); await p.waitForTimeout(3000);
console.log(await p.evaluate(() => { const e = document.getElementById('nf-visits'); return { shown: !e.hidden, text: e.getAttribute('aria-label') || e.textContent }; }));
await b.close();
