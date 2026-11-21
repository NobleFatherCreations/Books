import { chromium } from 'playwright';
const b = await chromium.launch(); 
for (const w of [320,375,390]) {
const p = await b.newPage({ viewport: { width: w, height: 800 } });
await p.goto('http://127.0.0.1:8765/');
console.log(w, JSON.stringify(await p.evaluate(() => ['.brand','#sound-btn','#still-btn','.menu-btn','.leave','.top .wrap'].map(s => { const r = document.querySelector(s).getBoundingClientRect(); return [s, Math.round(r.left), Math.round(r.width)]; }))), await p.evaluate(()=>document.documentElement.scrollWidth));
}
await b.close();
