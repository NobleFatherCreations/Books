#!/usr/bin/env node
// Blind comparison and five-second-test page generator (no storage, no network, answers are collected by a human).
//   node scripts/blind-compare.mjs ab   <dirA> <dirB> <outdir>     # bake-off: A vs B screenshots shown as X / Y in random order
//   node scripts/blind-compare.mjs five <image> <outdir>           # five-second test: shows the image for 5 s, then asks the questions
// Writes <outdir>/index.html (+ key.json for ab mode: which of X/Y was A). Open index.html on a phone or laptop and read the questions aloud.
import fs from 'fs'; import path from 'path';
const [mode, a, b, c] = process.argv.slice(2);
const esc = (s) => s.replace(/[&<>"]/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
const css = `body{font:17px/1.5 system-ui,sans-serif;margin:0;padding:16px;background:#111;color:#eee}h1{font-size:20px}img{max-width:100%;border-radius:8px}
.row{display:flex;gap:12px;flex-wrap:wrap}.col{flex:1 1 280px}button{font:inherit;padding:12px 18px;border-radius:10px;border:0;background:#e5c158;color:#111}ol{padding-left:20px}`;
const imgs = (d) => fs.readdirSync(d).filter((f) => /^\d+\.(jpg|png)$/.test(f)).sort();
if (mode === 'ab') {
  const outdir = c; fs.mkdirSync(outdir, { recursive: true });
  const flip = Math.random() < 0.5; const X = flip ? b : a, Y = flip ? a : b;
  const pick = (d) => { const f = imgs(d); const idx = [0, 0.15, 0.35, 0.55, 0.75, 1].map((p) => f[Math.round(p * (f.length - 1))]).filter((v, i, ar) => ar.indexOf(v) === i); return idx.map((n) => { fs.copyFileSync(path.join(d, n), path.join(outdir, (d === X ? 'X-' : 'Y-') + n)); return (d === X ? 'X-' : 'Y-') + n; }); };
  const xs = pick(X), ys = pick(Y);
  fs.writeFileSync(path.join(outdir, 'key.json'), JSON.stringify({ X: flip ? 'B' : 'A', Y: flip ? 'A' : 'B', note: 'Do not open until the judge has chosen.' }));
  fs.writeFileSync(path.join(outdir, 'index.html'), `<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Blind comparison</title><style>${css}</style>
<h1>Which would you rather use / read / trust? (X or Y)</h1><div class=row><div class=col><h2>X</h2>${xs.map((f) => `<img src="${f}" alt="X screen">`).join('<br><br>')}</div><div class=col><h2>Y</h2>${ys.map((f) => `<img src="${f}" alt="Y screen">`).join('<br><br>')}</div></div>
<h2>Ask the judge (record answers on paper)</h2><ol><li>Which looks more like a finished, professional piece? X / Y / same</li><li>Which feels more like <i>this</i> subject and not any website? X / Y</li><li>Which is easier to read? X / Y</li><li>Which would you scroll further in? X / Y</li><li>What is the one thing you'd change in each?</li></ol>`);
  console.log('wrote', path.join(outdir, 'index.html'), '(key in key.json: keep it closed until all judges answered)');
} else if (mode === 'five') {
  const outdir = b; fs.mkdirSync(outdir, { recursive: true }); fs.copyFileSync(a, path.join(outdir, 'shot' + path.extname(a)));
  fs.writeFileSync(path.join(outdir, 'index.html'), `<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Five-second test</title><style>${css}</style>
<h1>Five-second test</h1><p>Hold the phone upright. You will see one screen for five seconds. Then I will ask questions.</p><button id=go>Start</button><div id=box hidden><img src="shot${path.extname(a)}" alt="screen under test"></div>
<div id=q hidden><h2>Questions (no looking back)</h2><ol><li>What is this? Who is it for?</li><li>What do you remember seeing?</li><li>What would you do next?</li><li>One word for how it felt.</li><li>Anything confusing, ugly or hard to read?</li></ol></div>
<script>go.onclick=()=>{go.hidden=true;box.hidden=false;setTimeout(()=>{box.hidden=true;q.hidden=false},5000)}</script>`);
  console.log('wrote', path.join(outdir, 'index.html'));
} else { console.error('usage: blind-compare.mjs ab <dirA> <dirB> <out> | five <image> <out>'); process.exit(2); }
