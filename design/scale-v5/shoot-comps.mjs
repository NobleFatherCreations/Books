// Phone shots of each comp view: node design/scale-v5/shoot-comps.mjs [dpr]
import { createRequire } from 'module'; const { chromium } = createRequire(import.meta.url)('playwright');
const dpr = +(process.argv[2] || 1), B = 'http://127.0.0.1:8766/design/scale-v5/comps';
const views = [['cover','index',null],['contents','index','#contents'],['gradient','the-gradient','.blk-gradient'],
  ['tool','the-gradient','.blk-tool'],['sort','the-gradient','.blk-sort'],['scene','a-boundary-or-a-rule','.blk-scene'],
  ['ask','a-boundary-or-a-rule','.blk-ask'],['crisis','when-weighing-stops',null]];
const b = await chromium.launch();
for (const c of ['a','b','c']) {
  const p = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:dpr });
  for (const [n,page,sel] of views) {
    await p.goto(`${B}/${c}/${page}.html`, {waitUntil:'networkidle'}); await p.waitForTimeout(250);
    if (n==='contents') await p.evaluate(()=>{const d=document.querySelector('#contents details'); if(d) d.open=true;});
    if (sel) await p.evaluate(s=>{const e=document.querySelector(s); if(e) window.scrollTo(0, e.getBoundingClientRect().top+scrollY-110);}, sel);
    await p.waitForTimeout(200);
    await p.screenshot({ path:`design/scale-v5/comp-shots/${c}-${n}.png` });
  }
  await p.close();
}
await b.close();
