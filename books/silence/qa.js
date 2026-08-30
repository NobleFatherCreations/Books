// One validation script for the whole book. Run once per phase.
const fs=require('fs');
const file=process.argv[2]||'repair.html';
const TOTAL=+(process.argv[3]||48);
const s=fs.readFileSync(file,'utf8');
const js=s.split('<script id="book-js">')[1].split('</script>')[0];
let fail=0; const bad=m=>{console.log('  ✗ '+m); fail++;};

// structure
const mv=[...js.matchAll(/c:\[([\d,]+)\]/g)].flatMap(m=>m[1].split(',').map(Number));
const ch=[...js.matchAll(/\n ?(\d+):\{t:/g)].map(m=>+m[1]);
const seq=[...mv].sort((a,b)=>a-b).join(',');
const full=Array.from({length:TOTAL},(_,i)=>i+1).join(',');
seq===full? console.log(`  ✓ movements cover 1-${TOTAL} exactly`) : bad('movement coverage broken');
ch.length===TOTAL? console.log(`  ✓ ${TOTAL} chapter records`) : bad(`CH has ${ch.length}, expected ${TOTAL}`);
js.includes('/* ===== INSERT CHAPTERS ABOVE THIS LINE ===== */')? console.log('  ✓ anchor present'):bad('ANCHOR MISSING');
(s.match(/<script/g)||[]).length===(s.match(/<\/script>/g)||[]).length? console.log('  ✓ script tags balanced'):bad('script tags unbalanced');

// bodies + tags
const bodies=[...js.matchAll(/BODIES\[(\d+)\]=`([\s\S]*?)`;/g)];
let words=0;
for(const [,n,b] of bodies){
  words+=b.split(/\s+/).length;
  for(const t of ['p','h3','ul','ol','li','div']){
    const o=(b.match(new RegExp('<'+t+'[ >]','g'))||[]).length;
    const c=(b.match(new RegExp('</'+t+'>','g'))||[]).length;
    if(o!==c) bad(`ch${n} <${t}> ${o}/${c}`);
  }
  if(b.includes('${')) bad(`ch${n} template interpolation`);
}
console.log(`  ✓ ${bodies.length} chapters written, ${words} words`);

// AUDIT 5 — manipulation check (automated portion)
const banned=[
  [/!/g,'exclamation mark'],
  [/most people never/i,'in-group flattery'],
  [/they don'?t want you to/i,'conspiracy framing'],
  [/only \d+ (spots|left|remaining)/i,'scarcity'],
  [/you'?re not like (most|other)/i,'in-group flattery'],
  [/act now|limited time|before it'?s too late/i,'manufactured urgency'],
  [/streak|progress bar|完/i,'engagement mechanic']
];
let m5=0;
for(const [,b] of bodies) for(const [re,label] of banned){ if(re.test(b)){ bad(`AUDIT5: ${label}`); m5++; } }
if(!m5) console.log('  ✓ AUDIT 5 (automated): no manipulation patterns');

// AUDIT 1 — absolute language flag (review, not fail)
const abs=[/\bproves\b/i,/\bcauses\b/i,/\balways\b/i,/\bnever\b/i,/studies show/i,/research proves/i];
const flags=[];
for(const [,n,b] of bodies) for(const re of abs){ const h=b.match(re); if(h) flags.push(`ch${n}: "${h[0]}"`); }
console.log(`  · AUDIT 1 flags for tier review: ${flags.length}`+(flags.length?` — ${flags.slice(0,6).join(', ')}`:''));

// house rules
[/localStorage/,/sessionStorage/,/https?:\/\/(?!www\.w3)/].forEach((re,i)=>{
  const names=['localStorage','sessionStorage','external URL'];
  if(re.test(js)) bad(`house rule: ${names[i]} found`);
});
// engagement mechanics — ignore negated/disclaiming mentions ("no streak", "nothing here keeps score")
const engRe=/\b(streak|progress bar|badge|completion %)\b/gi;
let engHit=false, m;
while((m=engRe.exec(js))){
  const before=js.slice(Math.max(0,m.index-30), m.index);
  if(!/\b(no|not|nothing|never|without)\b/i.test(before)){ bad(`engagement mechanic (unnegated): "${m[0]}"`); engHit=true; }
}
if(!engHit) console.log('  ✓ no active engagement mechanics (disclaiming mentions ignored)');
console.log(fail? `\nFAILED (${fail})` : '\nALL CHECKS PASS');
process.exit(fail?1:0);
