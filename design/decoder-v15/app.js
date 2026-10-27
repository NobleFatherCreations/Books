"use strict";
/* Pattern Decoder v15 — Wayfinding.
   One offline page. Every route is a hash, so back, forward and bookmarks work. Groups are lines,
   tactics are stations, related tactics in other groups are interchanges, sequences are routes.
   Private by default: nothing is written to the device until the reader turns saving on. Since v16 the guide is
   meant to be found, so addresses always carry the tactic's name (#/entry/gaslighting) and the tab title, meta
   description, canonical link and JSON-LD follow the page (seo() below); the old numbered addresses (#/s/12)
   still open. See docs/DECODER-V15-ARCHITECTURE.html and docs/DECODER-SEO.md. */
const D = JSON.parse(document.getElementById("data").textContent);
const $ = (s, el) => (el || document).querySelector(s);
const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));

/* ---------- text helpers (carried over from v14) ---------- */
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");}
function expandContractions(s){
  return s.replace(/\bwon['’]t\b/g,"will not").replace(/\bcan['’]t\b/g,"can not").replace(/\bshan['’]t\b/g,"shall not").replace(/n['’]t\b/g," not")
    .replace(/['’]re\b/g," are").replace(/['’]ve\b/g," have").replace(/['’]ll\b/g," will").replace(/\bi['’]m\b/g,"i am").replace(/['’]d\b/g," would").replace(/['’]s\b/g,"");
}
function norm(s){return expandContractions((s||"").toLowerCase()).replace(/[^a-z0-9]+/g," ").trim();}
function safeDecode(s){try{return decodeURIComponent(s)}catch(e){return String(s||"")}}
function curly(s){return String(s).replace(/(^|[\s(—-])"/g,"$1“").replace(/"/g,"”").replace(/(^|[\s(])'/g,"$1‘").replace(/'/g,"’");}
const H = s => esc(curly(s));
/* One line of "it can sound like". Lines the data already quotes get no second quote mark; lines that open with a quote and then narrate are shown as written. */
const sayLi = t => { t=String(t||"").trim(); const st=/^["“‘]/.test(t), en=/["”’]$/.test(t); return st&&!en?'<li class="nq">'+H(t)+'</li>':'<li>'+H(unq(t))+'</li>'; };
const unq = t => { t=String(t||"").trim(); return /^["“‘]/.test(t)&&/["”’]$/.test(t)?t.replace(/^["“‘]\s*/,"").replace(/\s*["”’]$/,""):t; };
function slugify(s){return (s||"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/(^-+|-+$)/g,"")||"x";}
/* A sentence ends at . ! or ? (plus any closing quotes) only when a space or the end follows, so 'did this happen?', stays one sentence. */
function sentences(t){ const m=String(t||"").match(/(?:[^.!?]|[.!?]+["'”’)]*(?=[^\s"'”’)]))+(?:[.!?]+["'”’)]*|$)\s*/g); return (m||[String(t||"")]).map(x=>x.trim()).filter(Boolean); }
/* The answer comes first: the first sentence of an explanation is bold, long paragraphs break every two sentences. */
function prose(t){
  const ss=sentences(t); if(!ss.length) return "";
  let out='<p><strong>'+H(ss[0])+'</strong>'+(ss[1]?' '+H(ss[1]):'')+'</p>';
  for(let i=2;i<ss.length;i+=2) out+='<p>'+H(ss[i])+(ss[i+1]?' '+H(ss[i+1]):'')+'</p>';
  return out;
}
function leadLi(t){ t=String(t||""); const m=t.match(/^(.{6,64}?)(\s[—–-]\s|:\s|,\s)/); return m?'<strong>'+H(m[1])+'</strong>'+H(m[2]+t.slice(m[0].length)):H(t); }
const P = {
  arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>', back:'<path d="M19 12H5M11 6l-6 6 6 6"/>', prev:'<path d="m15 6-6 6 6 6"/>', next:'<path d="m9 6 6 6-6 6"/>',
  close:'<path d="M18 6 6 18M6 6l12 12"/>', copy:'<rect x="9" y="9" width="11" height="11" rx="1"/><path d="M5 15V5a1 1 0 0 1 1-1h9"/>',
  share:'<path d="M12 3v13M7 8l5-5 5 5"/><path d="M5 13v7h14v-7"/>', print:'<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8"/><path d="M7 14h10v7H7z"/>',
  up:'<path d="M12 19V5M6 11l6-6 6 6"/>', paste:'<rect x="6" y="5" width="12" height="16"/><path d="M9 5V3h6v2"/>', volume:'<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/>', stop:'<rect x="6" y="6" width="12" height="12"/>',
  save:'<path d="M6 3h12v18l-6-4-6 4z"/>', saved:'<path fill="currentColor" d="M6 3h12v18l-6-4-6 4z"/>',
  tri:'<path d="M12 3 2 20h20z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
  eyeoff:'<path d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6z"/><circle cx="12" cy="12" r="2.6"/><path d="M4 4l16 16"/>', cmp:'<path d="M8 3v18M16 3v18M3 8h5M16 16h5"/>', exit:'<path d="M14 4h5v16h-5"/><path d="M3 12h11M9 7l-5 5 5 5"/>', search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', map:'<circle cx="6" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M6 8v4a4 4 0 0 0 4 4h6"/><circle cx="18" cy="6" r="2"/><path d="M18 8v8"/>',
};
const ic = (n,cls) => '<svg class="i'+(cls?' '+cls:'')+'" viewBox="0 0 24 24" aria-hidden="true">'+P[n]+'</svg>';

/* ---------- indexes ---------- */
const E = D.entries, BY = {}, BY_SLUG = {};
E.forEach((e,i)=>{ e.i=i; BY[e.n]=e; BY_SLUG[e.s]=e; });
const LINES = D.lines, LINE = {};
LINES.forEach((l,i)=>{ l.i=i; LINE[l.k]=l; l.st=l.order.map(n=>BY[n]); });
const SET = {}; D.settings.forEach(s=>SET[s.k]=s);
const ALIAS_SLUG = {}; Object.keys(D.aliases).forEach(a=>ALIAS_SLUG[slugify(a)]=D.aliases[a]);
const PATS_OF = {}; D.recipes.forEach((r,ri)=>{ r.i=ri; r.c.forEach(n=>(PATS_OF[n]=PATS_OF[n]||[]).push(ri)); });
let _ALPHA=null; const alpha=()=>_ALPHA||(_ALPHA=[...E].sort((a,b)=>a.n.localeCompare(b.n)));
const crossRel = e => (e.rel||[]).filter(n=>BY[n]&&BY[n].g!==e.g).map(n=>BY[n]);
/* Full entries load per line, the first time a station on that line opens. */
const LCACHE = {};
function full(e){
  if(e.F) return e.F;
  if(!LCACHE[e.g]){ const el=document.getElementById("L-"+e.g); LCACHE[e.g]=el?JSON.parse(el.textContent):{}; }
  e.F=Object.assign({}, e.f, LCACHE[e.g][e.n]||{}); return e.F;
}

/* ---------- the device store: private unless the reader turns saving on ----------
   When saving is on, everything lives in ONE entry called "ui-state". Its value is scrambled (not encrypted) and holds only
   numbers: saved and recent tactics are short hashes of their slugs, and no setting is stored as a word. This hides it from a
   glance, not from someone who knows how: the scrambling key is in this page, and the hashes are of public names. Turning
   saving off deletes the entry. Nothing here records when anything was read. */
const store=(()=>{
  const KEY="ui-state", XK=[110,102,33,154,60,81], SHORT={breath:"b",theme:"th",size:"sz",space:"sp",motion:"mo",leave:"lv",hap:"hp",color:"co"};
  let mem={}, ok=false, on=false, legacy=0, frozen=false;
  try{ localStorage.setItem("__t","1"); localStorage.removeItem("__t"); ok=true; }catch(e){}
  const fnv=t=>{ let h=2166136261; for(let i=0;i<t.length;i++){ h^=t.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h.toString(36); };
  let HM=null; const hmap=()=>HM||(HM=Object.fromEntries(E.map(e=>[fnv(e.s),e.n])));
  const toH=n=>{ const e=BY[canon(n)]; return e?fnv(e.s):null; }, fromH=h=>hmap()[h]||null;
  const scramble=u=>u.map((b,i)=>b^XK[i%XK.length]);
  const enc=o=>{ let t=""; scramble(new TextEncoder().encode(JSON.stringify(o))).forEach(b=>{ t+=String.fromCharCode(b); }); return btoa(t).replace(/=+$/,""); };
  const dec=t=>{ try{ const a=atob(t), u=new Uint8Array(a.length); for(let i=0;i<a.length;i++) u[i]=a.charCodeAt(i); return JSON.parse(new TextDecoder().decode(scramble(u))); }catch(e){ return null; } };
  const pack=()=>{ const o={on:1};
    if(mem.starred) o.s=mem.starred.map(toH).filter(Boolean);
    if(mem.trail) o.t=mem.trail.map(t=>toH(t.name)).filter(Boolean);
    if(mem.hidden) o.h=mem.hidden.map(k=>LINE[k]?LINE[k].i:-1).filter(i=>i>=0);
    Object.keys(SHORT).forEach(k=>{ if(k in mem) o[SHORT[k]]=mem[k]; }); return o; };
  const unpack=o=>{ const m={};
    if(Array.isArray(o.s)) m.starred=o.s.map(fromH).filter(Boolean);
    if(Array.isArray(o.t)) m.trail=o.t.map(x=>({name:fromH(Array.isArray(x)?x[0]:x)})).filter(x=>x.name);
    if(Array.isArray(o.h)) m.hidden=o.h.map(i=>LINES[i]&&LINES[i].k).filter(Boolean);
    Object.keys(SHORT).forEach(k=>{ if(SHORT[k] in o) m[k]=o[SHORT[k]]; }); return m; };
  const persist=()=>{ if(on&&ok) try{ localStorage.setItem(KEY,enc(pack())); }catch(e){} };
  /* v14 kept readable fg_* entries; they are only ever imported or deleted, never written */
  const old=k=>{ try{ const v=localStorage.getItem("fg_"+k); return v===null?undefined:JSON.parse(v); }catch(e){ return undefined; } };
  const wipeOld=()=>{ if(!ok) return; try{ for(let n=localStorage.length-1;n>=0;n--){ const k=localStorage.key(n); if(k&&k.indexOf("fg_")===0) localStorage.removeItem(k); } }catch(e){} };
  if(ok){ try{ const t=localStorage.getItem(KEY); if(t!==null){ const o=dec(t); if(o&&o.on===1){ on=true; mem=unpack(o); } } }catch(e){}
    if(on) wipeOld(); else { const a=old("starred"), b=old("trail"); legacy=(Array.isArray(a)?a.length:0)+(Array.isArray(b)?b.length:0); } }
  return {
    get saving(){ return on; }, get legacy(){ return legacy; },
    get(k,d){ return (k in mem)?mem[k]:d; },
    set(k,v){ if(frozen) return; mem[k]=v; persist(); },
    setSaving(v){
      if(v&&!on){ const a=old("starred"), b=old("trail");
        if(Array.isArray(a)) mem.starred=[...new Set((mem.starred||[]).concat(a.map(canon)))].filter(n=>BY[n]);
        if(Array.isArray(b)){ const cur=mem.trail||[]; mem.trail=cur.concat(b.filter(x=>x&&x.name&&BY[canon(x.name)]&&!cur.some(c=>c.name===canon(x.name))).map(x=>({name:canon(x.name)}))); }
        on=true; legacy=0; wipeOld(); persist(); }
      else if(!v&&on){ on=false; if(ok) try{ localStorage.removeItem(KEY); }catch(e){} wipeOld(); mem.starred=[]; mem.trail=[]; }
    },
    forgetLegacy(){ wipeOld(); legacy=0; },
    clearLists(){ const snap={starred:mem.starred||[], trail:mem.trail||[]}; this.set("starred",[]); this.set("trail",[]); return snap; },
    restore(snap){ this.set("starred",snap.starred); this.set("trail",snap.trail); },
    forgetAll(){ mem={}; frozen=true; },
  };
})();
const canon = n => D.aliases[n]||n;
const starred = () => store.get("starred",[]).map(canon).filter(n=>BY[n]);
const isSaved = n => starred().includes(n);
function toggleSave(n){ let s=starred(); s=s.includes(n)?s.filter(x=>x!==n):[n].concat(s); store.set("starred",s); return s.includes(n); }
/* Rest a line: the reader hides whole lines they are not ready to read about. They stay out of search, matches and lists
   until shown again. Nothing here rates how intense a tactic is; the choice is entirely the reader's. At least one line stays visible. */
const hiddenSet=()=>new Set(store.get("hidden",[]));
function setHidden(k,on){ let h=store.get("hidden",[]); h=on?[...new Set(h.concat(k))]:h.filter(x=>x!==k); if(on&&h.length>=LINES.length) return false; store.set("hidden",h); return true; }
const LEAVE_TO={weather:["A weather search","https://www.google.com/search?q=weather"],wiki:["Wikipedia","https://en.wikipedia.org/wiki/Main_Page"],blank:["A blank page","about:blank"]};
function logTrail(n){ if(!store.saving) return; const t=store.get("trail",[]).filter(x=>x&&x.name!==n); t.unshift({name:n}); store.set("trail",t.slice(0,100)); }

/* ---------- addresses: always names since v16 (old numbered addresses still open) ---------- */
const stH = e => "#/entry/"+e.s;
const lnH = l => "#/line/"+l.k;
const cpH = (a,b) => "#/compare/"+a.s+"/"+b.s;
const rtH = r => "#/routes/"+r.s;
const readable = e => location.href.split("#")[0]+"#/entry/"+e.s;

/* ---------- small renderers ---------- */
const bullet = (l,cls) => '<span class="b'+(cls?' '+cls:'')+'" data-g="'+l.k+'" aria-hidden="true">'+l.letter+'</span>';
const lineName = l => l.letter+' line, '+l.label;
/* A line's drawn glyph, so lines differ by shape as well as by colour and letter. */
const emblem = (l,cls) => '<span class="emb'+(cls?' '+cls:'')+'" data-g="'+l.k+'" aria-hidden="true"><svg viewBox="0 0 24 24">'+l.emb+'</svg></span>';
/* A station code, the way a stop is numbered on a platform: the line's letter, then two digits for its place on the line. */
const pad2 = n => String(n).padStart(2,"0");
const plate = (l,n) => '<span class="plate" data-g="'+l.k+'" role="img" aria-label="Station code '+l.letter+' '+pad2(n)+'"><b>'+l.letter+'</b>'+pad2(n).split("").map(d=>'<i>'+d+'</i>').join("")+'</span>';
/* Pictogram signs for where something has been happening. */
const WPIC = {
  relationship:'<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
  family:'<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
  work:'<rect x="3" y="7" width="18" height="12"/><path d="M9 7V5h6v2M3 13h18"/>',
  social:'<circle cx="8" cy="9" r="3"/><circle cx="16.5" cy="10" r="2.5"/><path d="M2.5 19c.5-3.5 3-5 5.5-5s5 1.5 5.5 5M14.5 15c2.5-.5 5 .8 6 4"/>',
  online:'<rect x="7" y="3" width="10" height="18"/><path d="M11 18h2"/>',
  self:'<circle cx="12" cy="8" r="4"/><path d="M4.5 21c.7-4.5 3.7-6.5 7.5-6.5s6.8 2 7.5 6.5"/>',
  groups:'<circle cx="12" cy="7" r="2.5"/><circle cx="5.5" cy="10" r="2"/><circle cx="18.5" cy="10" r="2"/><path d="M7.5 20c.3-3.5 2-5.5 4.5-5.5s4.2 2 4.5 5.5M2 18c.2-2.5 1.5-4 3.5-4M22 18c-.2-2.5-1.5-4-3.5-4"/>',
  society:'<rect x="4" y="4" width="16" height="16"/><path d="M8 9h8M8 13h8M8 17h5"/>',
  unsure:'<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7v.5"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
};
WPIC.friends=WPIC.social;
const pic = k => '<span class="pic" aria-hidden="true"><svg viewBox="0 0 24 24">'+(WPIC[k]||WPIC.unsure)+'</svg></span>';
function rowHTML(e,o){ o=o||{}; const l=LINE[e.g];
  return '<a class="row" href="'+stH(e)+'" data-vt data-g="'+e.g+'">'+bullet(l)+'<span class="rt"><b class="nm">'+H(e.n)+'</b>'+
    '<small>'+(o.snip!=null?o.snip:H(e.sub||e.f.short_definition))+'</small>'+(o.why?'<span class="why">'+o.why+'</span>':'')+'</span>'+
    '<span class="sr-only">, '+esc(lineName(l))+(e.sens?', safety first':'')+'</span>'+(e.sens?ic("tri","tri"):'')+'</a>';
}
const rows = (list,o) => '<div class="rows">'+list.map(e=>rowHTML(e,o)).join("")+'</div>';
let FOLD_N = 0;
function fold(items,cls,n,render){
  if(!items||!items.length) return ""; n=n||3; render=render||leadLi; const id="f"+(++FOLD_N);
  const lis=items.map((x,i)=>'<li'+(i>=n?' hidden':'')+'>'+render(x)+'</li>').join("");
  return '<ul class="ul '+(cls||"")+'" id="'+id+'">'+lis+'</ul>'+(items.length>n?'<button class="linkbtn fold-btn" type="button" data-fold="'+id+'" data-n="'+n+'" aria-expanded="false" aria-controls="'+id+'">Show all '+items.length+'</button>':'');
}
const tick = t => '<label><input type="checkbox"><span>'+leadLi(t)+'</span></label>';
const blk = (title,inner,cls) => inner?'<div class="blk"><h3'+(cls?' class="'+cls+'"':'')+'>'+title+'</h3>'+inner+'</div>':"";
/* The first use of each glossary term becomes a button that opens a plain explanation under it. */
function gloss(html){
  const used=new Set();
  return html.replace(/<(p|li)>([\s\S]*?)<\/\1>/g,(m,tag,inner)=>{ let defs="";
    Object.keys(D.glossary).forEach(t=>{ if(used.has(t)) return;
      const re=new RegExp("\\b("+t.replace(/ /g,"\\s")+"s?)\\b","i");
      if(re.test(inner.replace(/<[^>]+>/g," "))&&re.test(inner)&&!/<(button|a|label) /.test(inner)){ used.add(t); const id="g-"+t.replace(/ /g,"-");
        inner=inner.replace(re,'<button type="button" class="term" data-term="'+id+'" aria-expanded="false" aria-controls="'+id+'">$1</button>');
        defs+='<span class="term-def" id="'+id+'" hidden><b>'+t.charAt(0).toUpperCase()+t.slice(1)+':</b> '+esc(D.glossary[t])+'</span>'; } });
    return "<"+tag+">"+inner+defs+"</"+tag+">"; });
}
function foot(){
  return '<footer class="foot"><p>A free guide by Noble Father Creations. It is a reading aid, not a diagnosis, a legal opinion or therapy. If you are in danger, contact emergency services.</p>'+
    '<nav aria-label="More"><a href="#/safety">Use this safely</a><a href="/playbook/tactics">Every tactic on its own page</a><a href="#/lines">All lines</a><a href="#/routes">Patterns seen together</a><a href="#/updates">Service updates ('+esc(D.version)+')</a><a href="#/settings">Settings</a></nav></footer>';
}
const notFound = () => '<div class="view"><h1 class="h-page">That page is not here.</h1><p class="lede">The link may be out of date or cut short.</p><div class="blades"><a class="blade pri" href="#/"><span class="bt"><b>Go to the start</b></span><span class="ar">'+ic("arrow")+'</span></a><a class="blade" href="#/search"><span class="bt"><b>Search instead</b></span><span class="ar">'+ic("arrow")+'</span></a></div></div>';

/* ---------- search (v14 engine: names, everyday words, what people say, then the rest) ---------- */
const STOP = new Set(D.stop);
const SAME={text:"messag",dm:"messag",chat:"messag",email:"messag",boyfriend:"partner",girlfriend:"partner",husband:"partner",wife:"partner",spouse:"partner",ex:"partner",
  boss:"manag",supervisor:"manag",mom:"parent",mum:"parent",dad:"parent",mother:"parent",father:"parent",cell:"phone",mobile:"phone",
  yell:"shout",scream:"shout",ignor:"silen",cash:"money",paycheck:"money",wage:"money"};
function stem(w){w=w.length>4?w.replace(/(ings|ing|edly|ed|ies|es|s|ly)$/,""):w.replace(/s$/,"");return SAME[w]||w;}
const stems = t => new Set(t.split(" ").filter(Boolean).map(stem));
const stemLine = t => t.split(" ").filter(Boolean).map(stem).join(" ");
const searchTokens = n => n.split(" ").filter(w=>w.length>2&&!STOP.has(w));
/* The search index is built in slices while the page is idle (no slice over ~25 ms on a slow phone). A search that
   arrives before it is finished completes the rest first. */
const HAY=[], STEMS=[];
function indexSlice(n){ for(let i=HAY.length,end=Math.min(E.length,i+n);i<end;i++){ const e=E[i];
  const h={name:norm(e.n), names:[norm(e.n)].concat((e.abs||[]).map(norm)), said:norm((e.f.what_it_sounds_like||[]).join(" ")), words:norm((e.kw||[]).join(" ")),
    all:norm([e.n,(e.abs||[]).join(" "),e.sub||"",(e.kw||[]).join(" "),e.f.short_definition,e.f.plain_language_summary,(e.f.what_it_sounds_like||[]).join(" ")].join(" "))};
  HAY[i]=h; STEMS[i]={name:stems(h.name),words:stems(h.words),said:stems(h.said),all:stems(h.all),wline:stemLine(h.words),sline:stemLine(h.said)}; } }
function buildIndex(){ if(HAY.length<E.length) indexSlice(E.length); }
function buildIndexIdle(){ if(HAY.length>=E.length) return; indexSlice(16); setTimeout(buildIndexIdle,24); }
function fuzzy(n){
  const toks=searchTokens(n).map(stem); if(!toks.length) return []; const HID=hiddenSet();
  const w=n.split(" ").map(stem), grams=[];
  for(let i=0;i<w.length-1;i++){ grams.push(w[i]+" "+w[i+1]); if(i<w.length-2) grams.push(w[i]+" "+w[i+1]+" "+w[i+2]); }
  const scored=[];
  E.forEach((e,i)=>{ if(HID.has(e.g)) return; const st=STEMS[i]; let hits=0,score=0;
    toks.forEach(t=>{ if(!st.all.has(t)) return; hits++; score+=st.name.has(t)?4:st.words.has(t)?3.5:st.said.has(t)?3:1; });
    if(!hits) return; grams.forEach(g=>{ if(st.wline.includes(g)) score+=8; else if(st.sline.includes(g)) score+=6; });
    scored.push({e,hits,score}); });
  const need=toks.length<=2?toks.length:Math.min(3,Math.ceil(toks.length/2));
  const kept=scored.filter(x=>x.hits>=need).sort((a,b)=>b.score-a.score||b.hits-a.hits||a.e.n.localeCompare(b.e.n));
  const top=kept.length?kept[0].score:0;
  return kept.filter(x=>x.score>=Math.max(2,top*.5)).slice(0,12).map(x=>x.e);
}
function search(q){
  buildIndex(); const n=norm(String(q||"").slice(0,400)), HID=hiddenSet();
  if(!n) return {list:[],n};
  let list=[];
  if(n.replace(/ /g,"").length>=2){
    list=E.map((e,i)=>{ const h=HAY[i]; if(HID.has(e.g)||!h.all.includes(n)) return null;
      const r=h.names.some(x=>x===n)?0:h.names.some(x=>x.startsWith(n))?1:h.names.some(x=>x.includes(n))?2:h.words.includes(n)?3:h.said.includes(n)?4:5; return {e,r}; })
      .filter(Boolean).sort((a,b)=>a.r-b.r||a.e.n.localeCompare(b.e.n)).map(x=>x.e);
    if(n.length<4&&list.length>40) list=[];
  }
  if(list.length<5&&n.split(" ").length>1){ const seen=new Set(list); fuzzy(n).forEach(e=>{ if(!seen.has(e)&&list.length<12) list.push(e); }); }
  const cm=n.replace(/ /g,"").match(/^([a-z])0?(\d{1,2})$/);   /* a station code such as T09 */
  if(cm){ const ln=LINES.find(l=>l.letter.toLowerCase()===cm[1]), st=ln&&!hiddenSet().has(ln.k)&&ln.st[+cm[2]-1]; if(st) list=[st].concat(list.filter(x=>x!==st)); }
  return {list,n};
}
/* Show the words that matched: the quote it sounds like, or the subtitle, with the shared words marked. */
function snippet(e,n){
  const toks=new Set(searchTokens(n).map(stem)); if(!toks.size&&n) toks.add(stem(n));
  const mark=t=>H(t).replace(/[A-Za-z’']+/g,w=>toks.has(stem(norm(w)))?'<mark>'+w+'</mark>':w);
  const hit=t=>{ const s=stems(norm(t)); for(const x of toks) if(s.has(x)) return true; return norm(t).includes(n); };
  const q=(e.f.what_it_sounds_like||[]).find(hit); if(q){ const t=q.trim(), st=/^["“‘]/.test(t), en=/["”’]$/.test(t); return st?mark(t):'“'+mark(t)+'”'; }
  if(e.sub&&hit(e.sub)) return mark(e.sub);
  return mark(e.sub||e.f.short_definition);
}
let SEARCH_Q = "";
/* Search also reaches the lines and the pages, the way v14's command menu did. */
const PAGES=[["Help me figure it out","#/help","guide questions where feel not sure"],["Browse all lines","#/lines","map network lines stations"],["Saved","#/saved","bookmarks kept recent"],
  ["Use this safely","#/safety","safety danger emergency help leave exit privacy"],["Settings","#/settings","text size larger night day dark light colours motion spacing saving private"],
  ["Service updates","#/updates","what changed version news"],["Patterns seen together","#/routes","sequences combine order recipes"],["All lines, A to Z","#/lines/az","alphabetical list index"],
  ["Where it happens","#/lines/where","relationship family work online settings"],["The most common","#/lines/common","popular frequent starting point"]];
function jumpFor(n){ if(!n||n.replace(/ /g,"").length<3) return {list:[],strong:false}; const out=[];
  LINES.forEach(l=>{ if(norm(l.label+" "+l.blurb+" "+l.letter+" line").includes(n)) out.push({line:l,t:norm(l.label)}); });
  PAGES.forEach(p=>{ if(norm(p[0]+" "+p[2]).includes(n)) out.push({page:p,t:norm(p[0])}); });
  return {list:out.slice(0,4), strong:out.some(j=>j.t.startsWith(n))}; }
function jumpHTML(j){ return !j.list.length?"":'<h2 class="k">Lines and pages</h2><div class="rows">'+j.list.map(x=>x.line?
  '<a class="row" href="'+lnH(x.line)+'" data-g="'+x.line.k+'">'+bullet(x.line)+'<span class="rt"><b class="nm">'+esc(x.line.label)+'</b><small>'+esc(x.line.letter)+' line · '+x.line.order.length+' stations</small></span></a>':
  '<a class="row" href="'+x.page[1]+'"><span class="b n" aria-hidden="true">'+ic("arrow")+'</span><span class="rt"><b class="nm">'+esc(x.page[0])+'</b><small>Page</small></span></a>').join("")+'</div>'; }
function resultsHTML(){
  const r=search(SEARCH_Q), jump=jumpFor(r.n);
  const rec=store.saving?store.get("trail",[]).map(t=>BY[canon(t.name)]).filter(Boolean).slice(0,3):[];
  if(!r.n) return (rec.length?'<h2 class="k">Recently read</h2>'+rows(rec):'')+'<h2 class="k">Try one of these</h2><div class="rows">'+D.tries.map(t=>'<button class="row" type="button" data-try="'+esc(t)+'"><span class="rt"><b class="nm">'+H(t)+'</b></span>'+ic("arrow")+'</button>').join("")+'</div>'+
    '<div class="blades"><a class="blade quiet" href="#/help"><span class="bt"><b>Not sure what to type?</b><small>Answer two short questions instead</small></span><span class="ar">'+ic("arrow")+'</span></a></div>';
  if(!r.list.length) return jumpHTML(jump)+'<div class="empty"><p><strong>'+(jump.list.length?'No tactic matched those words.':'Nothing matched those words.')+'</strong> Try fewer or plainer words, describe what was said or done, or answer two short questions.</p></div><div class="blades"><a class="blade quiet" href="#/help"><span class="bt"><b>Help me figure it out</b></span><span class="ar">'+ic("arrow")+'</span></a></div>';
  const o=e=>({snip:snippet(e,r.n)});
  return (jump.strong?jumpHTML(jump):'')+'<h2 class="k">Best match</h2>'+rows([r.list[0]].map(e=>e),{snip:snippet(r.list[0],r.n)})+(r.list.length>1?'<h2 class="k">Also</h2><div class="rows">'+r.list.slice(1).map(e=>rowHTML(e,o(e))).join("")+'</div>':'')+(jump.strong?'':jumpHTML(jump));
}
function countText(){ const r=search(SEARCH_Q), n=r.list.length+jumpFor(r.n).list.length; return !r.n?"":n?n+(n===1?" match":" matches"):"No matches"; }
function viewSearch(){
  return '<div class="view"><h1 class="h-page" tabindex="-1">Search</h1>'+
    '<form class="sfield" role="search" data-search><label class="sr-only" for="q">Search the guide</label>'+ic("search")+
    '<input id="q" type="search" enterkeyhint="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="What was said, or a name" value="'+esc(SEARCH_Q)+'">'+
    '<button class="clr" type="button" data-clear aria-label="Clear search"'+(SEARCH_Q?'':' hidden')+'>'+ic("close")+'</button>'+
    (navigator.clipboard&&navigator.clipboard.readText?'<button class="pst" type="button" data-paste'+(SEARCH_Q?' hidden':'')+'>'+ic("paste")+'Paste</button>':'')+'</form>'+
    '<p class="count" id="scount" role="status">'+countText()+'</p><div id="results">'+resultsHTML()+'</div>'+
    '<p class="note" style="margin-top:2rem">What you type stays on this phone. It is never sent anywhere or added to the address. You can also type a station code, like T09.</p></div>';
}

/* ---------- help me figure it out: two questions, then matches with reasons ---------- */
let GUIDE = {step:0, where:null, feels:[], more:false, err:false};
const FEEL = {}; D.feelings.forEach(f=>FEEL[f.key]=f);
const WHERE = {}; D.feelingGroups.forEach(g=>WHERE[g.key]=g);
function matches(){
  const tally={}, why={};
  GUIDE.feels.forEach(k=>(D.narrow[k]||[]).forEach((n,rank)=>{ n=canon(n); if(!BY[n]) return; tally[n]=(tally[n]||0)+10-Math.min(rank,9)/2; (why[n]=why[n]||[]).push(FEEL[k]?FEEL[k].label:k); }));
  const set=GUIDE.where&&D.feelToSetting[GUIDE.where];
  Object.keys(tally).forEach(n=>{ if(set&&(BY[n].w||[]).includes(set)) tally[n]+=3; });
  const HID=hiddenSet();
  return Object.keys(tally).filter(n=>!HID.has(BY[n].g)).sort((a,b)=>tally[b]-tally[a]||a.localeCompare(b)).slice(0,15).map(n=>({e:BY[n], why:why[n], here:!!(set&&(BY[n].w||[]).includes(set))}));
}
function viewHelp(){
  const g=GUIDE, bar='<div class="gsteps" aria-hidden="true">'+[0,1,2].map(i=>'<i class="'+(i<=g.step?"on":"")+'"></i>').join("")+'</div>';
  const stepTxt='<p class="sr-only">Step '+(g.step+1)+' of 3</p>';
  if(g.step===0) return '<div class="view">'+bar+stepTxt+'<h1 class="h-page" tabindex="-1">Where has this been happening?</h1><p class="lede">There are no wrong answers. Nothing you pick is saved.</p>'+
    '<div class="opts">'+D.feelingGroups.map(x=>'<button class="opt" type="button" data-where="'+x.key+'">'+pic(x.key)+'<span>'+H(x.label)+'</span>'+ic("arrow")+'</button>').join("")+
    '<button class="opt" type="button" data-where="">'+pic("unsure")+'<span>I’m not sure, or more than one</span>'+ic("arrow")+'</button></div></div>';
  if(g.step===1){
    const pool=D.feelings.filter(f=>!g.where||f.group===g.where);
    return '<div class="view">'+bar+stepTxt+'<h1 class="h-page" tabindex="-1">Which of these sound familiar?</h1><p class="lede">Pick as many as fit. Each one adds possibilities.</p>'+
      '<form data-feels><fieldset style="border:0;padding:0;margin:0"><legend class="sr-only">Things that sound familiar</legend><div class="feels">'+
      pool.map(f=>'<label><input type="checkbox" name="feel" value="'+f.key+'"'+(g.feels.includes(f.key)?' checked':'')+'><span>'+H(f.label)+'</span></label>').join("")+'</div></fieldset>'+
      '<div class="gbar"><button class="btn line" type="button" data-gstep="0">Back</button><span class="'+(g.err?'err':'small muted')+'" id="gcount" role="status">'+(g.err?'Pick at least one first':(g.feels.length?g.feels.length+' picked':''))+'</span>'+
      '<button class="btn pri" type="submit">Show my matches</button></div></form></div>';
  }
  const list=matches(), top=list.slice(0,3), rest=list.slice(3);
  const whyHTML=m=>'Matches <b>'+m.why.slice(0,2).map(H).join('</b>, <b>')+'</b>'+(m.here&&g.where?', and <b>'+H((WHERE[g.where]||{}).label||"")+'</b>':'');
  const sens=list.slice(0,6).some(m=>m.e.sens)||hiddenSet().size>0;
  return '<div class="view">'+bar+stepTxt+'<h1 class="h-page" tabindex="-1">'+(list.length?'Your closest matches':'Nothing matched yet')+'</h1>'+
    '<div class="picked" aria-label="Your answers">'+(g.where?'<a href="#/help" data-gstep="0">'+H(WHERE[g.where].label)+'<span class="chg">Change</span></a>':'')+
    g.feels.map(k=>'<button type="button" data-unfeel="'+k+'" aria-label="Remove: '+esc(FEEL[k]?FEEL[k].label:k)+'">'+H(FEEL[k]?FEEL[k].label:k)+ic("close")+'</button>').join("")+
    '<button type="button" data-gstep="1">Add more</button></div>'+
    (sens?'<div class="warn" role="note"><div class="band">'+ic("tri")+'If you feel unsafe</div><div class="body"><p>If you are afraid of someone, reach a person you trust, a local support service, or emergency services if you are in immediate danger. <a href="#/safety">More on staying safe</a></p></div></div>':'')+
    (list.length?'<div class="rows">'+top.map(m=>rowHTML(m.e,{why:whyHTML(m)})).join("")+'</div>':'<p class="lede">Try adding another answer.</p>')+
    (rest.length?(g.more?'<h2 class="k">More possible matches</h2><div class="rows">'+rest.map(m=>rowHTML(m.e,{why:whyHTML(m)})).join("")+'</div>':'<button class="linkbtn" type="button" data-gmore>Show '+rest.length+' more possible matches</button>'):'')+
    '<div class="blades" style="margin-top:2rem">'+
    '<button class="blade quiet" type="button" data-greset><span class="bt"><b>Start over</b></span></button></div></div>';
}

/* ---------- a station ---------- */
const visRel=(e,HID)=>crossRel(e).filter(r=>!HID.has(r.g));
const RESP=[["soft_clarification","Ask about it gently"],["firm_boundary","Set a clear limit"],["disengagement","Step back"],["support_seeking","Get support"],["workplace_or_professional","At work, school or with services"]];
const STEPS=[["fit","Is this it?"],["understand","Understand"],["do","What to do"],["deeper","Go deeper"]];
function stepPanels(e){
  const HID=hiddenSet(), f=full(e), notIt=f.this_may_not_be_it_when||[], says=f.what_it_sounds_like||[], pats=(PATS_OF[e.n]||[]).map(i=>D.recipes[i]), x=visRel(e,HID), same=(e.rel||[]).filter(n=>BY[n]&&BY[n].g===e.g).map(n=>BY[n]);
  const scriptH={verify:"A check to run before you share or act",self:"Words to say to yourself",say:"Words you could use"}[e.kind];
  return [
    '<h2>Is this it?</h2><p class="hint">One moment proves very little. Weigh it honestly, in both directions. Tick what fits, just for yourself: nothing is counted or kept.</p>'+
      blk("Signs it might be this",fold(f.this_may_be_it_when,"chk",3,tick),"tw")+
      blk("Signs it is probably something else",fold(notIt.concat(f.less_concerning_if||[]),"chk",3,tick),"aw")+
      blk("Questions to ask yourself",fold(f.discernment_questions,"qs"))+
      '<details class="more"><summary>More ways to weigh it</summary>'+
      blk("More worrying if",fold(f.more_concerning_if))+
      blk("What shows up over time",fold(f.pattern_over_time_signs))+
      blk("What else it could be",(f.what_it_is_not&&f.what_it_is_not.length?'<h4 class="small muted" style="margin:0 0 .5rem">What it is not</h4>'+fold(f.what_it_is_not):'')+
        (f.innocent_or_ordinary_possibilities&&f.innocent_or_ordinary_possibilities.length?'<h4 class="small muted" style="margin:1.5rem 0 .5rem">Ordinary explanations</h4>'+fold(f.innocent_or_ordinary_possibilities):'')+
        (f.common_false_positives&&f.common_false_positives.length?'<h4 class="small muted" style="margin:1.5rem 0 .5rem">Often mistaken for this</h4>'+fold(f.common_false_positives):''))+'</details>',
    '<h2>Understand it</h2><p class="hint">What it is, why it matters, and how it shows up.</p>'+
      blk("What it is",'<div class="text">'+prose(f.expanded_definition)+'</div>')+
      blk("Why it matters",'<div class="text">'+prose(f.why_this_matters)+'</div>')+
      blk("How it shows up",fold(f.what_it_is))+
      (says.length>2?blk("More things people say",'<ul class="says">'+says.slice(2).map(sayLi).join("")+'</ul>'):""),
    '<h2>What you can do</h2><p class="hint">'+(e.sens?'Read the safety note at the top first. If speaking up could make things worse, skip the wording below and talk to someone you trust or a local support service.':'Pick what fits. You do not owe anyone a confrontation.')+'</p>'+
      '<div class="blk script"><h3>'+scriptH+'</h3><blockquote id="bs">'+H(String(f.boundary_script||"").replace(/^Verification script[^:]*:\s*/i,""))+'</blockquote><div class="acts"><button class="btn" type="button" data-copy="bs">'+ic("copy")+'Copy the words</button></div></div>'+
      blk("Ways to respond",'<div class="resp">'+RESP.map(r=>f.response_options&&f.response_options[r[0]]?'<div><h4>'+r[1]+'</h4><p>'+H(f.response_options[r[0]])+'</p></div>':'').join("")+'</div>')+
      blk("Is it changing?",'<div class="text">'+prose(f.boundary_respect_check)+prose(f.repair_check)+'</div>')+
      (!e.sens?blk("When to take it more seriously",'<div class="text">'+prose(f.safety_note)+'</div>'):""),
    '<h2>Go deeper</h2><p class="hint">How it works, what it can do to you, and its close relatives.</p>'+
      blk("How it works",'<div class="text">'+prose(f.psychological_mechanism)+'</div>')+
      blk("How it can affect you",'<div class="text">'+prose(f.possible_impact_on_receiver)+'</div>')+
      blk("Telling it apart from its neighbours",'<div class="text">'+prose(f.how_to_distinguish_from_related)+'</div>'+
        (same.length?'<h4 class="small muted" style="margin:1.5rem 0 .5rem">Close on the same line</h4><div class="rows">'+same.slice(0,4).map(r=>'<div class="xrow">'+rowHTML(r)+'<a class="cmp" href="'+cpH(e,r)+'">Compare</a></div>').join("")+'</div>':'')+
        (x.length?'<p class="small muted" style="margin-top:1rem">Look-alikes on other lines are under <a href="#chg" data-jump>Change here for</a>.</p>':''))+
      blk("Using this label fairly",fold(f.misuse_warning))+
      (pats.length?blk("Patterns it is part of",'<div class="rows">'+pats.slice(0,6).map(r=>'<a class="row" href="'+rtH(r)+'"><span class="rt"><b class="nm">'+H(r.n)+'</b><small>'+r.c.length+' tactics that often appear together</small></span></a>').join("")+'</div>'):""),
  ];
}
function viewStation(e,stepArg){
  if(!e) return notFound();
  if(hiddenSet().has(e.g)){ const l=LINE[e.g]; return '<div class="view" data-g="'+e.g+'"><div class="notice"><h2>This station is on a line you are resting</h2><p>You chose to set the '+esc(lineName(l))+' aside, so this page is closed until you are ready. Nothing is deleted. Use this safely stays open whatever you hide.</p><div class="acts"><button class="btn pri" type="button" data-unhide="'+e.g+'">Show the line</button><a class="btn line" href="#/safety">Use this safely</a></div></div></div>'; }
  logTrail(e.n);
  const l=LINE[e.g], f=full(e), si=l.order.indexOf(e.n), prev=l.st[si-1], next=l.st[si+1], says=f.what_it_sounds_like||[], saved=isSaved(e.n);
  const HID=hiddenSet(), xAll=crossRel(e), x=xAll.filter(r=>!HID.has(r.g)), w=(e.w||[]).map(k=>SET[k]&&SET[k].label).filter(Boolean), pats=(PATS_OF[e.n]||[]).map(i=>D.recipes[i]);
  SEC_JUMP=Math.max(0,Math.min(3,(parseInt(stepArg,10)||1)-1))||null;   /* an old /entry/name/3 address scrolls to that section */
  const panels=stepPanels(e);
  return gloss('<article class="view station" data-g="'+e.g+'" aria-labelledby="st-h">'+
    '<div class="printhead" aria-hidden="true"><b>Pattern Decoder</b><span>'+bullet(l)+emblem(l)+esc(lineName(l))+' · Station '+(si+1)+' of '+l.order.length+'</span></div>'+
    '<header class="sname"><div class="sign">'+bullet(l,"lg")+'<div><h1 class="h-st" id="st-h" tabindex="-1">'+H(e.n)+'</h1>'+(e.sub?'<p class="sub">'+H(e.sub)+'</p>':'')+'</div></div>'+
      '<p class="onl">On the <a href="'+lnH(l)+'">'+esc(lineName(l))+'</a>'+plate(l,si+1)+'</p>'+
      (HID.has(e.g)?'<p class="restnote">You have rested this line. <button class="linkbtn" type="button" data-unhide="'+e.g+'">Show the line</button></p>':'')+
      '</header>'+
    (e.sens?'<section class="warn" role="note" aria-labelledby="w-h"><h2 class="band" id="w-h">'+ic("tri")+'Safety first</h2><div class="body">'+prose(f.safety_note)+'<p class="small"><a href="#/safety">How to use this guide safely</a></p></div></section>':'')+
    '<section class="answer" aria-label="In short"><div class="sum">'+prose(f.plain_language_summary)+'</div>'+
      (says.length?'<h2 class="k">It can sound like</h2><ul class="says">'+says.slice(0,2).map(sayLi).join("")+'</ul>':'')+
      (e.abs&&e.abs.length?'<p class="alsoc">Also called '+e.abs.map(H).join(", ")+'</p>':'')+'</section>'+
    '<div class="acts"><button class="btn" type="button" data-save="'+esc(e.n)+'" aria-pressed="'+saved+'">'+ic(saved?"saved":"save")+(saved?'Saved':'Save')+'</button>'+
      (CAN_SPEAK?'<button class="btn" type="button" data-listen>'+ic("volume")+'Listen</button>':'')+
      '<details class="moreacts"><summary class="btn">More<span class="sr-only"> ways to keep this</span></summary>'+
        '<button class="btn" type="button" data-aa><span class="aa" aria-hidden="true">Aa</span>Text size<span class="sr-only">, now '+SIZE_NAME[PREF.size]+'. Tap to change.</span></button>'+
        '<button class="btn" type="button" data-share>'+ic("share")+'Share link</button><button class="btn" type="button" data-print>'+ic("print")+'Print</button></details></div>'+
    '<div class="sections"><nav class="secnav" aria-label="On this page">'+STEPS.map((s,i)=>'<button type="button" data-sec="'+i+'">'+s[1]+'</button>').join("")+'</nav>'+
    '<div class="steps">'+panels.map((p,i)=>'<section class="panelx" id="sec-'+i+'">'+p+'</section>').join("")+'</div></div>'+
    '<aside class="side" aria-label="Around this station">'+
      (x.length||xAll.length?'<section class="xchg" id="chg"><h2 class="k" style="margin-top:0">Change here for</h2><p class="small muted" style="margin-bottom:.5rem">Look-alikes on other lines</p><div class="rows">'+
        x.slice(0,6).map(r=>'<div class="xrow">'+rowHTML(r)+'<a class="cmp" href="'+cpH(e,r)+'" aria-label="Compare '+esc(e.n)+' with '+esc(r.n)+'">Compare</a></div>').join("")+'</div>'+
        (xAll.length>x.length?'<p class="small muted" style="margin-top:.75rem">'+(xAll.length-x.length)+(xAll.length-x.length===1?' look-alike is':' look-alikes are')+' on lines you rested. <a href="#/settings">Settings</a> shows them again.</p>':'')+'</section>':'')+
      '<section class="facts"><dl>'+(w.length?'<div><dt>Where it happens</dt><dd>'+w.map(esc).join(", ")+'</dd></div>':'')+
        (pats.length?'<div><dt>Seen in '+pats.length+(pats.length===1?' pattern':' patterns')+'</dt><dd>'+pats.slice(0,3).map(r=>'<a href="'+rtH(r)+'">'+H(r.n)+'</a>').join(", ")+'</dd></div>':'')+'</dl></section></aside>'+
    '<nav class="pn" aria-label="Along the '+esc(lineName(l))+'">'+(prev?'<a href="'+stH(prev)+'" data-vt data-pg="prev"><span class="arr">'+ic("prev")+'</span><span class="pt"><small>Previous in this line</small><b>'+H(prev.n)+'</b></span></a>':'<span></span>')+
      (next?'<a class="nx" href="'+stH(next)+'" data-vt data-pg="next"><span class="pt"><small>Next in this line</small><b>'+H(next.n)+'</b></span><span class="arr">'+ic("next")+'</span></a>':'')+'</nav>'+
    '<div class="printfoot" aria-hidden="true">A reading aid, not a diagnosis, a legal opinion or therapy. If you are in danger, contact emergency services.</div>'+
  '</article>');
}
/* One scroll, four sections. The sticky index jumps to a section and follows the reader down the page. */
let SEC_JUMP=null, SECNAV=null;
function jumpSec(n){ const s=document.getElementById("sec-"+n); if(!s) return; if(SPK.on) speakStop(); hap(6); s.scrollIntoView({block:"start",behavior:motionOK()?"smooth":"auto"}); }
function secSpy(){
  const on=$(".station")&&SECNAV&&document.contains(SECNAV); if(!on){ document.body.classList.remove("reading"); return; }
  const edge=SECNAV.getBoundingClientRect().bottom+24; let cur=-1;   /* a section counts as current once its top is just under the index */
  $$(".panelx").forEach((s,i)=>{ if(s.getBoundingClientRect().top<=edge) cur=i; });
  $$("[data-sec]",SECNAV).forEach((b,i)=>{ if(i===cur) b.setAttribute("aria-current","true"); else b.removeAttribute("aria-current"); });
  /* reading down: the sign bar steps aside; scrolling up brings it back */
  document.body.classList.toggle("reading",cur>=0&&!UP);
}

/* ---------- compare two look-alikes ---------- */
function viewCompare(a,b){
  if(!a||!b||a===b) return notFound();
  const fa=full(a), fb=full(b), la=LINE[a.g], lb=LINE[b.g];
  const col=(e,l,inner)=>'<div data-g="'+e.g+'"><p class="cmp-who" aria-hidden="true">'+bullet(l,"sm")+H(e.n)+'</p>'+inner+'</div>';
  const row=(title,fn)=>'<section class="cmp-row"><h2>'+title+'</h2><div class="cmp-g">'+col(a,la,fn(a,fa))+col(b,lb,fn(b,fb))+'</div></section>';
  return '<div class="view"><h1 class="h-page" tabindex="-1">'+H(a.n)+' or '+H(b.n)+'?</h1><p class="lede">Side by side, from what each entry already says.</p>'+
    (a.sens||b.sens?'<div class="warn" role="note"><div class="band">'+ic("tri")+'Safety first</div><div class="body"><p>'+[a,b].filter(e=>e.sens).map(e=>H(e.n)).join(" and ")+' can travel with real danger. Read the safety note on '+((a.sens&&b.sens)?'each':'that')+' entry before acting on anything here.</p></div></div>':'')+
    '<div class="cmp-g">'+[a,b].map(e=>'<div data-g="'+e.g+'"><a class="nm" href="'+stH(e)+'">'+bullet(LINE[e.g],"sm")+'<span>'+H(e.n)+'</span>'+(e.sens?ic("tri","tri"):'')+'</a><p class="small muted" style="margin-top:.5rem">'+esc(LINE[e.g].label)+'</p></div>').join("")+'</div>'+
    row("In short",(e,f)=>'<p>'+H(f.plain_language_summary)+'</p>')+
    row("It can sound like",(e,f)=>'<ul class="says">'+(f.what_it_sounds_like||[]).slice(0,2).map(sayLi).join("")+'</ul>')+
    row("Signs it might be this",(e,f)=>fold((f.this_may_be_it_when||[]).slice(0,3),"tw",3))+
    row("How to tell them apart",(e,f)=>'<div class="text">'+prose(f.how_to_distinguish_from_related)+'</div>')+
    '</div>';
}

/* ---------- lines ---------- */
function viewLine(l){
  if(!l) return notFound();
  if(hiddenSet().has(l.k)) return '<div class="view" data-g="'+l.k+'"><div class="lhead">'+bullet(l,"lg")+'<div><h1 class="h-page" tabindex="-1" style="margin-bottom:.5rem">'+esc(l.label)+'</h1></div></div>'+
    '<div class="notice"><h2>You are resting this line</h2><p>Its stations are out of search, matches and lists, so nothing from it turns up until you are ready. Nothing is deleted. Use this safely stays open whatever you hide.</p><div class="acts"><button class="btn pri" type="button" data-unhide="'+l.k+'">Show this line</button><a class="btn line" href="#/safety">Use this safely</a></div></div></div>';
  const ix=l.st.filter(e=>crossRel(e).length).length;
  return '<div class="view" data-g="'+l.k+'"><div class="lhead">'+bullet(l,"lg")+'<div><h1 class="h-page" tabindex="-1" style="margin-bottom:.5rem">'+esc(l.label)+'</h1><p class="lede" style="margin:0">'+esc(l.blurb)+'</p></div></div>'+
    '<p class="small muted">'+esc(l.letter)+' line · '+l.order.length+' stations · '+ix+' with places to change. Stations next to each other are closely related.</p>'+
    '<div class="legend" aria-hidden="true"><span>'+bullet(LINE[l.k==="truth"?"control":"truth"],"sm")+'Look-alikes on another line</span><span>'+ic("tri","tri")+'Safety first</span></div>'+
    '<ol class="glist ldia">'+l.st.map(e=>{ const xs=[...new Set(crossRel(e).map(r=>r.g))];
      return '<li><a href="'+stH(e)+'" data-vt><span class="nm">'+H(e.n)+'</span>'+(e.sens?ic("tri","tri"):'')+
        (xs.length?'<span class="xb" aria-hidden="true">'+xs.slice(0,4).map(g=>bullet(LINE[g],"sm")).join("")+'</span>':'')+
        '<span class="sr-only">'+(e.sens?', safety first':'')+(xs.length?', change here for '+xs.map(g=>LINE[g].letter+' line').join(", "):'')+'</span></a></li>'; }).join("")+'</ol>'+
    '<div class="blades" style="margin-top:2rem">'+
    '<button class="blade quiet" type="button" data-hide="'+l.k+'"><span class="pict">'+ic("eyeoff")+'</span><span class="bt"><b>Rest this line for now</b><small>Hide it from search, matches and lists until you show it</small></span></button></div></div>';
}
function lineRows(){ const HID=hiddenSet(); return '<ol class="lrows glist">'+LINES.map(l=>'<li><a class="lrow'+(HID.has(l.k)?' rest':'')+'" href="'+lnH(l)+'">'+bullet(l)+'<span class="lt"><b>'+esc(l.label)+'</b><small>'+(HID.has(l.k)?'Resting. Hidden from search and matches. Open to show it.':esc(l.blurb))+'</small></span><span class="n">'+l.order.length+'</span>'+ic("next","chev")+'</a></li>').join("")+'</ol>'; }
function viewLines(tab){
  const HID=hiddenSet();
  const tabs=[["","By line"],["az","A to Z"]], other=[["#/lines/where","By where it happens","The settings where tactics turn up"],["#/lines/common","The most common","What shows up most across documented patterns"],["#/routes","Patterns seen together","Tactics that often arrive in a sequence"]];
  let body="";
  if(tab==="az"){ const by={}; alpha().filter(e=>!HID.has(e.g)).forEach(e=>{ const c=/[a-z]/i.test(e.n.charAt(0))?e.n.charAt(0).toUpperCase():"#"; (by[c]=by[c]||[]).push(e); });
    const ks=Object.keys(by);
    body='<nav class="seg" aria-label="Jump to a letter">'+ks.map(c=>'<a href="#az-'+c+'" data-jump>'+c+'</a>').join("")+'</nav>'+
      ks.map(c=>'<h2 class="h-sec" id="az-'+c+'" style="margin:2rem 0 .5rem">'+c+'</h2>'+rows(by[c])).join(""); }
  else if(tab==="where") body=D.settings.map(s=>{ const list=E.filter(e=>!HID.has(e.g)&&(e.w||[]).includes(s.k)).sort((a,b)=>b.pop-a.pop||a.n.localeCompare(b.n));
    return '<h2 class="h-sec">'+pic(s.k)+esc(s.label)+'</h2><p class="small muted" style="margin-bottom:.75rem">'+esc(s.blurb)+' '+list.length+' tactics.</p>'+fold(list,"rows-f",6,e=>rowHTML(e)).replace('class="ul rows-f"','class="rows"'); }).join("");
  else if(tab==="common") body='<p class="lede">A starting point: the tactics that show up most often across the documented patterns.</p>'+rows(D.common.map(n=>BY[n]).filter(e=>e&&!HID.has(e.g)));
  else body='<p class="lede">Ten lines, one for each kind of tactic. Every tactic is a station on its line.</p>'+lineRows()+
    '<h2 class="h-sec">Other ways in</h2><ul class="glist">'+other.map(o=>'<li><a class="lrow" href="'+o[0]+'"><span class="lt"><b>'+o[1]+'</b><small>'+o[2]+'</small></span>'+ic("next","chev")+'</a></li>').join("")+'</ul>';
  const sub=tab==="where"?"By where it happens":tab==="common"?"The most common":"";
  return '<div class="view"><h1 class="h-page" tabindex="-1">'+(sub||"Browse")+'</h1>'+(sub?'':'<nav class="seg" aria-label="Ways to list">'+tabs.map(t=>'<a href="#/lines'+(t[0]?'/'+t[0]:'')+'"'+((tab||"")===t[0]?' aria-current="page"':'')+'>'+t[1]+'</a>').join("")+'</nav>')+body+'</div>';
}


/* ---------- routes ---------- */
function viewRoutes(r){
  if(r){ const HV=hiddenSet(), RC=r.c.filter(n=>BY[n]&&!HV.has(BY[n].g)), skipped=r.c.length-RC.length; 
    return '<div class="view wide"><h1 class="h-page" tabindex="-1">'+H(r.n)+'</h1><p class="lede">'+H(r.d)+'</p>'+
      '<p class="note">These tactics are often seen together, in roughly this order. It is a pattern, not a prediction: nothing here says what will happen next in your situation.</p>'+
      (skipped?'<p class="note">'+skipped+(skipped===1?' tactic is':' tactics are')+' on a line you are resting, so '+(skipped===1?'it is':'they are')+' left out. Settings shows them again.</p>':'')+
      '<ol class="chain" style="margin-top:2rem">'+RC.map(n=>{ const e=BY[n]; return e?'<li><a href="'+stH(e)+'" data-vt data-g="'+e.g+'"><span class="rt" style="display:flex;flex-direction:column;gap:.25rem"><b class="nm" style="font:800 1.0625rem/1.25 var(--sign);display:flex;gap:.5rem;align-items:center">'+bullet(LINE[e.g],"sm")+H(e.n)+'</b><small class="muted">'+H(e.f.short_definition)+'</small></span></a></li>':''; }).join("")+'</ol></div>'; }
  return '<div class="view"><h1 class="h-page" tabindex="-1">Patterns seen together</h1><p class="lede">Tactics rarely arrive alone. These '+D.recipes.length+' documented patterns show tactics that often appear together, and roughly in what order. They describe what has been seen, never what will happen.</p>'+
    '<div class="rows rlist">'+D.recipes.map(r=>'<a class="row" href="'+rtH(r)+'"><span class="rt"><b class="nm">'+H(r.n)+'</b><small>'+H(r.d)+'</small></span><span class="n">'+r.c.length+'</span></a>').join("")+'</div></div>';
}

/* ---------- saved ---------- */
function viewSaved(){
  if(!store.saving) return '<div class="view"><h1 class="h-page" tabindex="-1">Saved</h1><p class="lede">Saving is off, so nothing you read or save is kept on this device. This is the safer choice if anyone else might use this phone.</p>'+
    (store.legacy?legacyNotice():'')+
    '<div class="notice"><h2>Want to keep tactics for later?</h2><p>Turning saving on keeps the tactics you save, what you recently read and your settings on this device only. They are kept in a scrambled entry, which hides them from a glance but is not secret: someone who knows how could read which tactics you saved and which lines you rested. You can turn saving off again in Settings, and that deletes all of it.</p><div class="acts"><button class="btn pri" type="button" data-saving="on">Turn on saving</button></div></div></div>';
  const HV=hiddenSet(), st=starred().map(n=>BY[n]).filter(e=>!HV.has(e.g)), tr=store.get("trail",[]).map(t=>BY[canon(t.name)]).filter(e=>e&&!HV.has(e.g)).slice(0,24);
  return '<div class="view"><h1 class="h-page" tabindex="-1">Saved</h1><p class="lede">Kept on this device only. Clearing your browser data clears these too.</p>'+
    '<h2 class="h-sec">Saved tactics</h2>'+(st.length?rows(st):'<p class="empty">Tap Save on any station to keep it here.</p>')+
    '<h2 class="h-sec">Recently read</h2>'+(tr.length?rows(tr):'<p class="empty">Stations you open will show up here.</p>')+
    (st.length||tr.length?'<div class="acts" style="margin-top:2rem"><button class="btn line" type="button" data-clearlists>Delete saved and recent</button></div>':'')+'</div>';
}
function legacyNotice(){ return '<div class="notice" id="legacy"><h2>This device has '+store.legacy+' saved and recent tactics from an earlier visit</h2><p>Earlier versions of the guide kept these automatically. Keep them and turn saving on, or delete them from this device.</p>'+
  '<div class="acts"><button class="btn pri" type="button" data-saving="on">Keep them, turn saving on</button><button class="btn line" type="button" data-forgetlegacy>Delete them</button></div></div>'; }

/* ---------- use this safely ---------- */
function viewSafety(){
  const p=t=>'<p>'+t+'</p>', h=t=>'<h2>'+t+'</h2>';
  return '<div class="view read"><h1 class="h-page" tabindex="-1">Use this guide safely</h1><p class="lede">What applies to every entry, said once.</p>'+
    '<section class="warn" aria-labelledby="sf-h"><h2 class="band" id="sf-h" style="margin:0;font-size:1rem">'+ic("tri")+'If you are not safe</h2><div class="body"><p>If any of this involves threats, being watched or tracked, being cut off from people or money, housing or immigration status, sex, pressure toward self-harm, or fear for your safety, reach a real person: someone you trust, a local support service, a legal or workplace resource, or emergency services if you are in immediate danger. Entries marked with the warning sign start with their safety note.</p></div></section>'+
    '<section class="exitplate" aria-labelledby="lv-h"><h2 class="band" id="lv-h" style="margin:0;font-size:1rem">Leaving quickly</h2><div class="body"><p>The green <strong>Leave</strong> button at the top of every page switches straight to a weather page and clears what this page was holding. On a keyboard, press Escape twice. It needs a connection to show the weather page; without one it shows a blank page. It steps back over the pages you opened here before it leaves, but it cannot erase that you visited: your browser may still list this site, and its forward history may still hold pages from here, so a private browsing window is safer still.</p></div></section>'+
    h("What this guide is")+p("A reading aid. It helps you put a name to something that happened, see what else it could be, and decide what to do next. Some entries are about everyday relationships; others are about workplaces, online life and influence on a whole society.")+
    h("What it is not")+p("It is not a diagnosis, a legal opinion or therapy. It cannot tell you what another person meant, what they are like, or whether you are in danger. Only you, and the people you trust, can weigh that.")+
    h("A signal, not a verdict")+p("One example of a pattern is a reason to look more closely, not proof of motive or character. Every entry says what its tactic is not, because most of these behaviors also have ordinary explanations. Please do not use a label from this guide to attack, shame, threaten, expose or get back at someone.")+
    h("The lines and the patterns")+p("Lines group tactics of one kind, and tactics next to each other in a line are closely related. A pattern shows tactics that are often seen together. None of it predicts what a particular person will do.")+
    h("The search box")+p("Pasting in something that was said to you finds entries whose wording is close to it. That is a pointer to read further, never a finding. What you type is never added to the address bar or your history, and never sent anywhere.")+
    h("Your privacy")+p("There is no account. Saving is off unless you turn it on: until then nothing is written to this device. Page addresses and the tab title show what you are reading, and your browser keeps them in its history, so a private window is the safest way to read. The page counts anonymous visits; nothing you read, type or save is sent anywhere.")+
    p('If you turn saving on, your saved tactics, recent reading and settings stay on this device only. Turning it off in <a href="#/settings">Settings</a> deletes all of it.')+
    h("If your connection drops")+p("This guide is one file. Once it has loaded, it keeps working with no connection, because every page you can move to is already inside it. Keep the tab open. It does not install anything on your phone and it keeps no copy of itself in the browser's cache, on purpose: anything left on a device can be found. If you reload the page while offline, your browser may not be able to open it.")+
    h("Taking a pause")+p("After about twenty minutes of steady reading, the guide suggests a short pause. You can keep reading straight away, or switch the reminder off in Settings.")+'</div>';
}
function viewUpdates(){
  return '<div class="view read"><h1 class="h-page" tabindex="-1">Service updates</h1><p><span class="ver">'+esc(D.version)+' · '+esc(D.date)+'</span></p><ul class="ul upd">'+D.updates.map(u=>'<li>'+u+'</li>').join("")+'</ul></div>';
}

/* ---------- settings ---------- */
function viewSettings(){
  const ch=(name,cur,opts)=>'<div class="ch">'+opts.map(o=>'<label><input type="radio" name="'+name+'" value="'+o[0]+'"'+(cur===o[0]?' checked':'')+'>'+o[1]+'</label>').join("")+'</div>';
  return '<div class="view set"><h1 class="h-page" tabindex="-1">Settings</h1><form data-settings>'+
    '<fieldset><legend>Saving on this device</legend>'+ch("save",store.saving?"on":"off",[["off","Off (private)"],["on","On"]])+
      '<p class="help">'+(store.saving?'Saved tactics, recent reading and these settings are kept on this device in a scrambled entry. Scrambled is not secret: someone who knows how could read which tactics you saved and which lines you rested. A private window is safer. Turning saving off deletes all of it.':'Nothing is written to this device. Page addresses and the tab title still show what you are reading, so a private window is safer.')+'</p></fieldset>'+
    '<fieldset><legend>Colours</legend>'+ch("theme",PREF.theme,[["auto","Match my phone"],["night","Night"],["day","Day"]])+'</fieldset>'+
    '<fieldset><legend>Colour strength</legend>'+ch("color",PREF.color,[["quiet","Quiet"],["vivid","Vivid"]])+'<p class="help">Quiet keeps colour to small marks. It is easier on the eyes at night and draws less attention on a shared screen. Vivid adds each line’s colour to the headings and the home list.</p></fieldset>'+
    '<fieldset><legend>Text size</legend>'+ch("size",PREF.size,[["m","Standard"],["l","Larger"],["xl","Largest"]])+'</fieldset>'+
    '<fieldset><legend>Line spacing</legend>'+ch("space",PREF.space,[["normal","Standard"],["roomy","Roomier"]])+'</fieldset>'+
    '<fieldset><legend>Motion</legend>'+ch("motion",PREF.motion,[["auto","Match my phone"],["reduce","Reduce"]])+'<p class="help">Nothing moves on its own either way. Reduce also removes the short slides when you tap.</p></fieldset>'+
    (navigator.vibrate?'<fieldset><legend>Tap feedback</legend>'+ch("hap",store.get("hap",false)?"on":"off",[["off","Off"],["on","A small buzz when you tap"]])+'<p class="help">Only some phones can do this. On the others it does nothing.</p></fieldset>':'')+
    '<fieldset><legend>Reading pause</legend>'+ch("breath",store.get("breath",true)?"on":"off",[["on","Suggest a pause after 20 minutes"],["off","Off"]])+'</fieldset>'+
    '<fieldset><legend>Rest a line</legend><div class="ch rest">'+LINES.map(l=>'<label><input type="checkbox" name="rest" value="'+l.k+'"'+(hiddenSet().has(l.k)?' checked':'')+'>'+bullet(l,"sm")+esc(l.label)+'</label>').join("")+'</div>'+
      '<p class="help">Tick the lines you are not ready to read about. They stay out of search, matches and lists until you untick them. Nothing is deleted, Use this safely stays open, and some entries on a resting line can involve danger, so if you are unsure leave it visible.'+(store.saving?'':' Saving is off, so this is remembered only until you close the page.')+'</p></fieldset>'+
    '<fieldset><legend>The Leave button goes to</legend>'+ch("leave",store.get("leave","weather"),[["weather","A weather search"],["wiki","Wikipedia"],["blank","A blank page"]])+'<p class="help">It needs a connection; without one it shows a blank page. No web page can promise to leave no trace in your browser, so a private browsing window is safer still.</p></fieldset>'+
    '</form></div>';
}
const PREF={theme:"auto",size:"m",space:"normal",motion:"auto",color:"quiet"};
function loadPrefs(){ Object.keys(PREF).forEach(k=>{ const v=store.get(k,null); if(v) PREF[k]=v; }); applyPrefs(); }
function applyPrefs(){ const r=document.documentElement;
  PREF.theme==="auto"?r.removeAttribute("data-theme"):r.setAttribute("data-theme",PREF.theme);
  PREF.size==="m"?r.removeAttribute("data-size"):r.setAttribute("data-size",PREF.size);
  PREF.space==="roomy"?r.setAttribute("data-space","roomy"):r.removeAttribute("data-space");
  PREF.motion==="reduce"?r.setAttribute("data-motion","reduce"):r.removeAttribute("data-motion");
  PREF.color==="vivid"?r.setAttribute("data-color","vivid"):r.removeAttribute("data-color"); }
const motionOK = () => PREF.motion!=="reduce" && !matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- home ---------- */
const HOME_SRC = (()=>{ const h=document.getElementById("home-src"); return h?h.outerHTML:""; })();
function viewHome(){ return HOME_SRC; }
function fillHome(){
  const c=$("#continue"); if(!c) return;
  if(store.legacy){ c.innerHTML=legacyNotice(); return; }
  const HID=hiddenSet(), t=store.saving?store.get("trail",[]).map(x=>BY[canon(x.name)]).filter(e=>e&&!HID.has(e.g)):[];
  c.innerHTML=t.length?'<div class="continue"><span class="small muted">Continue where you left off:</span></div>'+rows([t[0]]):"";
  $$("#main .lrow").forEach(a=>{ const key=a.getAttribute("href").split("/").pop(), l=LINE[key]; if(l){ a.setAttribute("href",lnH(l)); if(HID.has(l.k)){ a.classList.add("rest"); const sm=$("small",a); if(sm) sm.textContent="Resting. Hidden from search and matches. Open to show it."; } } });
}

/* ---------- router ---------- */
function parse(){ const raw=(location.hash||"").replace(/^#\/?/,""); const p=raw.split("/").map(safeDecode); return {view:p[0]||"",a:p[1]||"",b:p[2]||""}; }
const byNum = (arr,n) => /^\d+$/.test(n)?arr[+n]:undefined;
function stationFrom(slug){ if(BY_SLUG[slug]) return BY_SLUG[slug]; const a=ALIAS_SLUG[slug]; return a&&BY[a]; }
/* Old v9 and v14 addresses keep working. */
function legacy(r){
  const m={guide:"help",narrow:"help",feeling:"help",sky:"lines",map:"lines",constellation:"lines",index:"lines/az",all:"lines/az",common:"lines/common",core:"lines/common",
    where:"lines/where",patterns:r.a?"routes/"+r.a:"routes",about:"safety",trail:"saved"};
  if(r.view==="browse") return r.a&&LINE[r.a]?"line/"+r.a:"lines";
  if(r.view==="category") return r.a&&D.catToGroup[r.a]?"line/"+D.catToGroup[r.a]:"lines";
  if(r.view==="entry"&&!BY_SLUG[r.a]&&ALIAS_SLUG[r.a]&&BY[ALIAS_SLUG[r.a]]) return "entry/"+BY[ALIAS_SLUG[r.a]].s;
  return m[r.view];
}
const ROUTES={
  "":()=>viewHome(), help:()=>viewHelp(), search:()=>viewSearch(), saved:()=>viewSaved(), safety:()=>viewSafety(), settings:()=>viewSettings(), updates:()=>viewUpdates(),
  lines:r=>viewLines(r.a), line:r=>viewLine(LINE[r.a]), l:r=>viewLine(byNum(LINES,r.a)),
  entry:r=>viewStation(stationFrom(r.a),r.b), s:r=>viewStation(byNum(E,r.a),r.b),
  compare:r=>viewCompare(stationFrom(r.a),stationFrom(r.b)), c:r=>viewCompare(byNum(E,r.a),byNum(E,r.b)),
  routes:r=>viewRoutes(r.a?D.recipes.find(x=>x.s===r.a)||null:null), r:r=>viewRoutes(byNum(D.recipes,r.a)),
};
function ctx(r){ /* what a page is called, and which door it belongs to */
  const st=r.view==="entry"?stationFrom(r.a):r.view==="s"?byNum(E,r.a):null;
  const ln=r.view==="line"?LINE[r.a]:r.view==="l"?byNum(LINES,r.a):null;
  const rt=r.view==="routes"&&r.a?D.recipes.find(x=>x.s===r.a):r.view==="r"?byNum(D.recipes,r.a):null;
  const label = st?st.n : ln?ln.label : rt?rt.n : ({"":"the start",help:GUIDE.step===2?"your matches":"Help",search:SEARCH_Q?"your search":"Search",lines:"Browse",routes:"Patterns",
    saved:"Saved",safety:"Use this safely",settings:"Settings",updates:"Service updates",compare:"the comparison",c:"the comparison"})[r.view]||"the previous page";
  const door={help:"help",search:"search",line:"browse",l:"browse",lines:"browse",routes:"browse",r:"browse",saved:"saved"}[r.view];
  const parent = st?{h:lnH(LINE[st.g]),label:LINE[st.g].label} : ln?{h:"#/lines",label:"Browse"} : rt?{h:"#/routes",label:"Patterns"} : null;
  const title = st?st.n : ln?ln.label : rt?rt.n : ({help:"Help me figure it out",search:"Search",lines:"Browse",routes:"Patterns seen together",saved:"Saved",safety:"Use this safely",settings:"Settings",updates:"Service updates"})[r.view];
  return {label,door,parent,title,station:st};
}
let STACK=[], LASTDOOR=null, FIRST=true, PENDING_VT=null;
const SCROLL={};
function backSign(c){
  if(STACK.length>1) return '<a class="back" href="'+STACK[STACK.length-2].h+'" data-back>'+ic("back")+'Back to '+esc(STACK[STACK.length-2].label)+'</a>';
  if(c.parent) return '<a class="back" href="'+c.parent.h+'">'+ic("back")+esc(c.parent.label)+'</a>';
  return "";
}
function render(){
  if(LEAVING) return;
  let r=parse();
  const to=legacy(r); if(to){ try{ history.replaceState(null,"","#/"+to); }catch(e){} r=parse(); }
  const key=location.hash||"#/";
  if(STACK.length>1&&STACK[STACK.length-2].h===key) STACK.pop(); else if(!STACK.length||STACK[STACK.length-1].h!==key) STACK.push({h:key,label:""});
  STACK=STACK.slice(-30);
  const c=ctx(r); STACK[STACK.length-1].label=c.label;
  if(c.door) LASTDOOR=c.door; if(!r.view) LASTDOOR=null;
  const fn=ROUTES[r.view], html=(fn?fn(r):notFound());
  const main=$("#main");
  const go=()=>{ main.innerHTML=(r.view?backSign(c):"")+html+foot(); };
  const vtEl=PENDING_VT; PENDING_VT=null;
  if(vtEl&&document.startViewTransition&&motionOK()&&!FIRST){
    vtEl.style.viewTransitionName="st";
    const t=document.startViewTransition(()=>{ vtEl.style.viewTransitionName=""; go(); const h=$(".h-st"); if(h) h.style.viewTransitionName="st"; sweep(vtEl); after(r,c,key); });
    t.finished.then(()=>{ const h=$(".h-st"); if(h) h.style.viewTransitionName=""; }).catch(()=>{});
  } else { if(!(FIRST&&!r.view)) go(); else main.insertAdjacentHTML("beforeend",foot()); sweep(vtEl); after(r,c,key); }
}
/* After a tap on a row, the station sign's line-colour band draws in from the left (the contract's one signature moment). */
function sweep(tapped){ if(!tapped||!motionOK()) return; const s=$(".sname"); if(s) s.classList.add("sweep"); }
/* ---------- findability (v16): tab title, description, canonical and JSON-LD follow the page ----------
   The canonical for a station or line is its plain page (/playbook/gaslighting, /playbook/line-truth), which the
   build writes beside this one; those are what search engines and AI crawlers read. Titles match the plain pages. */
const SITE="https://noblefathercreations.com/playbook";
const HOME_SEO={t:document.title,d:($("meta[name=description]")||{}).content||""};
const clip=(s,n)=>{ s=String(s||"").replace(/\s+/g," ").trim(); if(s.length<=n) return s; const c=s.slice(0,n-1); return c.slice(0,c.lastIndexOf(" ")).replace(/[,;:.]$/,"")+"…"; };
function setMeta(sel,v){ const m=$(sel); if(m) m.setAttribute(m.tagName==="LINK"?"href":"content",v); }
function seo(r,c){
  const st=c.station, ln=!st&&(r.view==="line"?LINE[r.a]:r.view==="l"?byNum(LINES,r.a):null);
  const t=st?st.n+": Signs, Examples and What to Do · Pattern Decoder" : ln?ln.label+": "+ln.order.length+" Tactics · Pattern Decoder" : c.title?c.title+" · Pattern Decoder" : HOME_SEO.t;
  const d=st?clip("What is "+st.n+"? "+st.f.short_definition,160) : ln?clip(ln.blurb,160) : HOME_SEO.d;
  const u=st?SITE+"/"+st.s : ln?SITE+"/line-"+ln.k : SITE;
  document.title=t;
  setMeta("meta[name=description]",d); setMeta("link[rel=canonical]",u);
  setMeta('meta[property="og:title"]',t); setMeta('meta[property="og:description"]',d); setMeta('meta[property="og:url"]',u);
  const old=$("#ld-page"); if(old) old.remove();
  if(!st) return;
  const l=LINE[st.g], ld=document.createElement("script");
  ld.type="application/ld+json"; ld.id="ld-page";
  ld.textContent=JSON.stringify({"@context":"https://schema.org","@type":"DefinedTerm","@id":u+"#term","name":st.n,"url":u,
    "termCode":l.letter+pad2(l.order.indexOf(st.n)+1),"description":st.f.short_definition,
    ...(st.abs&&st.abs.length?{"alternateName":st.abs}:{}),"inDefinedTermSet":{"@id":SITE+"#set"}});
  document.head.appendChild(ld);
}
function after(r,c,key){
  seo(r,c);
  document.body.dataset.page=c.station?"station":(r.view||"home"); document.body.dataset.g=c.station?c.station.g:"";
  $$(".doors a").forEach(a=>{ if(a.dataset.door===(c.door||(c.station||r.view==="compare"||r.view==="c"?LASTDOOR:null))) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); });
  if(!r.view) fillHome();
  noWidows($("#main"));
  if(r.view==="search"){ const q=$("#q"); if(q&&!FIRST) q.focus(); }
  else if(!FIRST){ const h=$("#main h1"); if(h){ if(!h.hasAttribute("tabindex")) h.tabIndex=-1; h.focus({preventScroll:true}); } }
  window.scrollTo(0, SCROLL[key]&&POPPED?SCROLL[key]:0); POPPED=false;
  SECNAV=$(".secnav"); if(c.station&&SEC_JUMP){ const sec=document.getElementById("sec-"+SEC_JUMP); if(sec) sec.scrollIntoView({block:"start"}); } SEC_JUMP=null;
  phoneTouches();
  FIRST=false;
}
/* How many pages of this visit sit behind this one, kept in history.state so a reload does not lose count. */
let DEPTH=(history.state&&history.state.d)||0;
let POPPED=false;
addEventListener("popstate",()=>{ POPPED=true; });
addEventListener("hashchange",(ev)=>{ if(LEAVING) return;
  try{ if(!history.state||history.state.d==null) history.replaceState({d:DEPTH+1},""); DEPTH=history.state.d; }catch(e){}
  try{ SCROLL[new URL(ev.oldURL).hash||"#/"]=scrollY; }catch(e){} render(); });
function nav(h){ if(location.hash===h) render(); else location.hash=h; }
function announce(t){ const a=$("#announce"); a.textContent=""; setTimeout(()=>{ a.textContent=t; },60); }
function noWidows(root){ $$("p,li,small,.sum p",root).forEach(el=>{ const n=el.lastChild; if(n&&n.nodeType===3){ const m=n.nodeValue.match(/^([\s\S]*\S)\s+(\S+\s*)$/); if(m&&m[2].length<=10&&m[1].length>24) n.nodeValue=m[1]+"\u00a0"+m[2]; } }); }
let TOAST_T=null;
function toast(msg,act,fn){ const t=$("#toast"); t.innerHTML=esc(msg)+(act?'<button type="button" data-toastact>'+esc(act)+'</button>':''); t.classList.add("on"); TOAST_FN=fn||null; clearTimeout(TOAST_T); TOAST_T=setTimeout(()=>t.classList.remove("on"),act?9000:2200); }
let TOAST_FN=null;
function copyText(text,msg){ const done=()=>toast(msg); try{ navigator.clipboard.writeText(text).then(done,()=>fallback()); }catch(e){ fallback(); }
  function fallback(){ const ta=document.createElement("textarea"); ta.value=text; ta.style.position="fixed"; ta.style.opacity="0"; document.body.appendChild(ta); ta.select(); try{ document.execCommand("copy"); done(); }catch(e){ toast("Could not copy. Select the text and copy it instead."); } ta.remove(); } }
function statusUI(){ const s=$("#status"); if(!s) return; const on=store.saving;
  s.dataset.on=on?"save":"priv"; $(".st-t",s).textContent=on?"Saving on":"Private";
  s.setAttribute("aria-label",on?"Saving is on: saved tactics and settings are kept on this device. Open settings":"Private: nothing is saved on this device. Open settings"); }
function setSaving(v){ store.setSaving(v); if(v) Object.keys(PREF).forEach(k=>store.set(k,PREF[k])); statusUI(); }

/* ---------- phone touches: each is caused by a tap or a scroll, none moves on its own ---------- */
const SIZE_NAME={m:"Standard",l:"Larger",xl:"Largest"};
function hap(ms){ if(store.get("hap",false)&&navigator.vibrate){ try{ navigator.vibrate(ms||8); }catch(e){} } }
/* back to the top, after a couple of screens of scrolling */
const TOTOP=document.createElement("button"); TOTOP.id="totop"; TOTOP.className="totop"; TOTOP.type="button"; TOTOP.hidden=true;
TOTOP.setAttribute("aria-label","Back to the top of this page"); TOTOP.innerHTML=ic("up"); document.body.appendChild(TOTOP);
let TT=false;
let LASTY=0, UP=false;
addEventListener("scroll",()=>{ if(TT) return; TT=true; requestAnimationFrame(()=>{ TT=false; const y=scrollY; let show=!TOTOP.hidden;
  if(y<LASTY-2) UP=true; else if(y>LASTY+2) UP=false;
  if(y<=innerHeight*1.5) show=false; else if(y<LASTY-2) show=true; else if(y>LASTY+2) show=false; LASTY=y;
  if(TOTOP.hidden===show) TOTOP.hidden=!show; secSpy(); }); },{passive:true});
TOTOP.addEventListener("click",()=>{ scrollTo({top:0,behavior:motionOK()?"smooth":"auto"}); hap(6); const h=$("#main h1"); if(h) h.focus({preventScroll:true}); });
/* when the on-screen keyboard is up, the sign bar steps out of the way so the search box keeps its room */
if(window.visualViewport){ const vv=visualViewport, chk=()=>document.body.classList.toggle("kbd",innerHeight-vv.height>140&&vv.scale<=1.01&&/^(INPUT|TEXTAREA)$/.test((document.activeElement||{}).tagName||""));
  vv.addEventListener("resize",chk); addEventListener("focusout",()=>setTimeout(chk,80)); }
/* read aloud, with a voice that lives on the phone. A voice that streams from the internet is never used, so nothing is sent anywhere. */
const CAN_SPEAK="speechSynthesis" in window&&"SpeechSynthesisUtterance" in window;
let SPK={on:false};
function localVoice(){ const vs=speechSynthesis.getVoices().filter(v=>v.localService), lang=(document.documentElement.lang||"en").slice(0,2).toLowerCase();
  return vs.find(v=>v.lang.toLowerCase().startsWith(lang)&&v.default)||vs.find(v=>v.lang.toLowerCase().startsWith(lang))||null; }
function speakStop(){ SPK.on=false; try{ speechSynthesis.cancel(); }catch(e){} $$("[data-listen]").forEach(b=>{ b.innerHTML=ic("volume")+"Listen"; }); }
function speakBlocks(){ const out=[];
  [$(".warn"),$(".answer"),$(".steps")].filter(Boolean).forEach(r=>{
    $$("h2,h3,h4,p,li,blockquote",r).forEach(el=>{ if(el.querySelector("h2,h3,h4,p,li,blockquote")||el.closest("[hidden]")||el.closest(".sr-only")) return;
      const d=el.closest("details"); if(d&&!d.open&&!el.closest("summary")) return;
      const t=el.textContent.replace(/\s+/g," ").trim(); if(t.length>1) out.push(t); }); });
  return out; }
function speak(){
  if(!CAN_SPEAK) return; if(SPK.on){ speakStop(); return; }
  if(!SPK.warned){ SPK.warned=true; toast("This plays out loud. Use headphones if anyone is near.","Read aloud",speak); return; }
  let tried=false;
  const go=()=>{ if(tried) return; tried=true; const v=localVoice(); if(!v){ toast("Your phone has no built-in voice for this, so nothing can be read aloud."); return; }
    const blocks=speakBlocks(); if(!blocks.length) return; SPK.on=true;
    $$("[data-listen]").forEach(b=>{ b.innerHTML=ic("stop")+"Stop"; });
    blocks.forEach((t,i)=>{ const u=new SpeechSynthesisUtterance(t); u.voice=v; u.lang=v.lang; u.rate=.95; if(i===blocks.length-1) u.onend=speakStop; u.onerror=()=>{ if(SPK.on) speakStop(); }; speechSynthesis.speak(u); });
    toast("Reading aloud from your phone's speaker","Stop",speakStop); };
  if(speechSynthesis.getVoices().length) go(); else { speechSynthesis.addEventListener("voiceschanged",go,{once:true}); setTimeout(go,600); }
}
document.addEventListener("visibilitychange",()=>{ if(document.hidden&&SPK.on) speakStop(); });
function phoneTouches(){ if(SPK.on) speakStop(); TOTOP.hidden=true; LASTY=scrollY; UP=false; secSpy(); }

/* ---------- leaving quickly ---------- */
let LEAVING=false;
function leave(){ if(LEAVING) return; LEAVING=true;
  const dest=(LEAVE_TO[store.get("leave","weather")]||LEAVE_TO.weather)[1];   /* read before memory is cleared */
  try{ try{ speechSynthesis.cancel(); }catch(e){} store.forgetAll(); SEARCH_Q=""; GUIDE={step:0,where:null,feels:[]}; document.title="Weather"; document.body.style.visibility="hidden"; }catch(e){}
  const url=navigator.onLine?dest:"about:blank", n=DEPTH; let gone=false;
  const go=()=>{ if(!gone){ gone=true; location.replace(url); } };
  /* step back over every page of this visit first, so Back from the weather page does not land in the guide;
     the replace waits for that step to finish (popstate), with a timer only as a fallback. The page is hidden meanwhile. */
  if(n>0){ addEventListener("popstate",go,{once:true}); history.go(-n); setTimeout(go,700); } else go(); }
let LAST_ESC=0;

/* ---------- events ---------- */
document.addEventListener("click",ev=>{
  const t=ev.target, a=t.closest("a"), b=t.closest("button");
  { const li=t.closest("[data-href]"); if(li&&!a&&!b){ nav(li.dataset.href); return; } }
  if(t.closest("#leave,[data-leave]")){ leave(); return; }
  if(a&&a.hasAttribute("data-back")&&STACK.length>1){ ev.preventDefault(); history.back(); return; }
  if(a&&a.hasAttribute("data-vt")&&ev.detail>0){ PENDING_VT=a.querySelector(".nm,span")||a; }
  if(a&&a.hasAttribute("data-jump")){ ev.preventDefault(); const el=document.getElementById(a.getAttribute("href").slice(1)); if(el){ el.tabIndex=-1; el.scrollIntoView(); el.focus({preventScroll:true}); } return; }
  if(!b) { if(a&&a.hasAttribute("data-gstep")){ ev.preventDefault(); GUIDE.step=+a.dataset.gstep; render(); } return; }
  const d=b.dataset;
  if(d.fold!=null){ const ul=document.getElementById(d.fold), open=b.getAttribute("aria-expanded")==="true";
    const n=+(d.n||3); $$(":scope>li",ul).forEach((li,i)=>{ if(i>=n) li.hidden=open; }); b.setAttribute("aria-expanded",!open); b.textContent=open?"Show all "+ul.children.length:"Show fewer"; if(!open){ const li=ul.children[n]; if(li){ const f=li.querySelector("input,a"); if(f) f.focus(); } } return; }
  if(d.term){ const el=document.getElementById(d.term), o=b.getAttribute("aria-expanded")==="true"; el.hidden=o; b.setAttribute("aria-expanded",!o); return; }
  if(d.sec!=null){ jumpSec(+d.sec); return; }
  if(d.save!=null){ if(!store.saving){ toast("Saving is off, so nothing is kept on this device.","Turn on saving",()=>{ setSaving(true); const on=toggleSave(d.save); toast(on?"Saved on this device":"Removed"); render(); }); return; }
    const on=toggleSave(d.save); b.setAttribute("aria-pressed",on); b.innerHTML=ic(on?"saved":"save")+(on?"Saved":"Save"); hap(10); if(on&&motionOK()){ const sv=b.querySelector("svg"); if(sv) sv.classList.add("pop"); } toast(on?"Saved on this device":"Removed from saved"); return; }
  if(d.share!=null){ const e=ctx(parse()).station; if(!e) return; const url=readable(e);
    if(navigator.share){ navigator.share({title:e.n,url}).catch(()=>{}); } else copyText(url,"Link copied"); return; }
  if(d.print!=null){ window.print(); return; }
  if(d.paste!=null){ navigator.clipboard.readText().then(t=>{ t=(t||"").trim().slice(0,400); if(!t){ toast("There was nothing to paste."); return; } SEARCH_Q=t; const q=$("#q"); if(q) q.value=t; updateResults(true); const cb=$("[data-clear]"); if(cb) cb.focus({preventScroll:true}); }).catch(()=>toast("Your phone did not allow pasting. Press and hold in the box instead.")); return; }
  if(d.aa!=null){ const order=["m","l","xl"], nx=order[(order.indexOf(PREF.size)+1)%3]; PREF.size=nx; store.set("size",nx); applyPrefs(); { const so=$(".sr-only",b); if(so) so.textContent=", now "+SIZE_NAME[nx]+". Tap to change."; } hap(8); toast("Text size: "+SIZE_NAME[nx]); return; }
  if(d.listen!=null){ speak(); return; }
  if(d.copy){ copyText($("#"+d.copy).textContent,"Copied"); return; }
  if(d.try){ SEARCH_Q=d.try; const q=$("#q"); if(q){ q.value=SEARCH_Q; } updateResults(true); return; }
  if(d.clear!=null){ SEARCH_Q=""; const q=$("#q"); q.value=""; q.focus(); updateResults(true); return; }
  if(d.where!=null){ GUIDE.where=d.where||null; GUIDE.feels=GUIDE.feels.filter(k=>!GUIDE.where||(FEEL[k]&&FEEL[k].group===GUIDE.where)); GUIDE.step=1; GUIDE.err=false; render(); return; }
  if(d.gstep!=null){ GUIDE.step=+d.gstep; GUIDE.err=false; render(); return; }
  if(d.unfeel){ GUIDE.feels=GUIDE.feels.filter(k=>k!==d.unfeel); if(!GUIDE.feels.length) GUIDE.step=1; render(); return; }
  if(d.gmore!=null){ GUIDE.more=true; render(); return; }
  if(d.greset!=null){ GUIDE={step:0,where:null,feels:[],more:false,err:false}; render(); return; }
  if(d.hide){ if(setHidden(d.hide,true)){ render(); toast(LINE[d.hide].label+" is resting. It is out of search, matches and lists until you show it.","Undo",()=>{ setHidden(d.hide,false); render(); }); } else toast("At least one line has to stay visible."); return; }
  if(d.unhide){ setHidden(d.unhide,false); render(); toast(LINE[d.unhide].label+" is shown again"); return; }
  if(d.saving){ setSaving(d.saving==="on"); toast(d.saving==="on"?"Saving is on for this device":"Saving is off"); render(); return; }
  if(d.forgetlegacy!=null){ store.forgetLegacy(); statusUI(); toast("Deleted from this device"); render(); return; }
  if(d.clearlists!=null){ const snap=store.clearLists(); render(); toast("Saved and recent deleted","Undo",()=>{ store.restore(snap); render(); }); return; }
  if(d.toastact!=null){ $("#toast").classList.remove("on"); if(TOAST_FN) TOAST_FN(); TOAST_FN=null; return; }
  if(d.breath){ breathHide(); if(d.breath==="off") store.set("breath",false); return; }
});
const updateResults=(()=>{ let t; return (now)=>{ clearTimeout(t); const run=()=>{ const r=$("#results"); if(!r) return; r.innerHTML=resultsHTML(); const c=$("#scount"); if(c) c.textContent=countText();
  const cl=$("[data-clear]"); if(cl) cl.hidden=!SEARCH_Q; const ps=$("[data-paste]"); if(ps) ps.hidden=!!SEARCH_Q; }; if(now) run(); else t=setTimeout(run,90); }; })();
document.addEventListener("input",ev=>{ if(ev.target.id==="q"){ SEARCH_Q=ev.target.value; updateResults(); } });
document.addEventListener("submit",ev=>{ ev.preventDefault();
  if(ev.target.matches("[data-search]")){ const first=$("#results a.row"); if(first) first.focus(); return; }
  if(ev.target.matches("[data-feels]")){ if(!GUIDE.feels.length){ GUIDE.err=true; render(); return; } GUIDE.step=2; GUIDE.more=false; render(); }
});
document.addEventListener("change",ev=>{ const t=ev.target;
  if(t.name==="feel"){ const k=t.value; GUIDE.feels=t.checked?[...new Set(GUIDE.feels.concat(k))]:GUIDE.feels.filter(x=>x!==k); GUIDE.err=false; const c=$("#gcount"); if(c){ c.className="small muted"; c.textContent=GUIDE.feels.length?GUIDE.feels.length+" picked":""; } return; }
  if(t.closest("[data-settings]")){
    if(t.name==="save"){ setSaving(t.value==="on"); toast(t.value==="on"?"Saving is on for this device":"Saving is off. Everything kept on this device was deleted."); render(); return; }
    if(t.name==="breath"){ store.set("breath",t.value==="on"); return; }
    if(t.name==="hap"){ store.set("hap",t.value==="on"); hap(14); return; }
    if(t.name==="leave"){ store.set("leave",t.value); toast("The Leave button now goes to "+LEAVE_TO[t.value][0].toLowerCase()); return; }
    if(t.name==="rest"){ if(!setHidden(t.value,t.checked)){ t.checked=false; toast("At least one line has to stay visible."); } else toast(t.checked?LINE[t.value].label+" is resting":LINE[t.value].label+" is shown again"); return; }
    PREF[t.name]=t.value; store.set(t.name,t.value); applyPrefs(); }
});
document.addEventListener("keydown",ev=>{
  const inField=/^(INPUT|TEXTAREA|SELECT)$/.test((ev.target.tagName||""))||ev.target.isContentEditable;
  if(ev.key==="Escape"){ const now=Date.now(); if(now-LAST_ESC<1000){ leave(); return; } LAST_ESC=now; if(!$("#breath").hidden) breathHide(); return; }
  if((ev.key==="k"&&(ev.metaKey||ev.ctrlKey))||(ev.key==="/"&&!inField)){ ev.preventDefault(); nav("#/search"); setTimeout(()=>{ const q=$("#q"); if(q) q.focus(); },0); return; }
  if(inField||ev.metaKey||ev.ctrlKey||ev.altKey) return;
  if(/^[1-4]$/.test(ev.key)&&$(".station")){ jumpSec(+ev.key-1); return; }
  if((ev.key==="j"||ev.key==="k")&&$(".station")){ const pg=$('[data-pg="'+(ev.key==="j"?"next":"prev")+'"]'); if(pg) nav(pg.getAttribute("href")); }
});

/* Printing opens every step, fold and section, then puts them back. */
let PRINT_STATE=null;
addEventListener("beforeprint",()=>{ PRINT_STATE={lis:$$("li[hidden]"),det:$$("details").map(d=>d.open)};
  $$("li[hidden]").forEach(li=>li.hidden=false); $$("details").forEach(d=>d.open=true); });
addEventListener("afterprint",()=>{ if(!PRINT_STATE) return; PRINT_STATE.lis.forEach(li=>li.hidden=true); $$("details").forEach((d,i)=>d.open=PRINT_STATE.det[i]); PRINT_STATE=null; });

/* ---------- a pause after a long stretch of reading (optional) ---------- */
const BREATH_AFTER=20*60*1000; let READ_MS=0, LAST_ACT=Date.now(), BREATH_RET=null;
["scroll","keydown","pointerdown"].forEach(k=>addEventListener(k,()=>{ LAST_ACT=Date.now(); },{passive:true}));
setInterval(()=>{ if(document.hidden||Date.now()-LAST_ACT>60000||!store.get("breath",true)) return; READ_MS+=5000; if(READ_MS>=BREATH_AFTER) breathShow(); },5000);
function breathShow(){ const b=$("#breath"); if(!b.hidden) return; BREATH_RET=document.activeElement; b.hidden=false; $("[data-breath=go]").focus(); }
function breathHide(){ const b=$("#breath"); if(b.hidden) return; b.hidden=true; READ_MS=0; if(BREATH_RET&&BREATH_RET.focus) BREATH_RET.focus(); }

/* ---------- start ---------- */
loadPrefs(); statusUI();
$("#doorlines").innerHTML='<p>Lines</p>'+LINES.map(l=>'<a href="#/line/'+l.k+'" data-lk="'+l.k+'">'+bullet(l,"sm")+esc(l.label)+'</a>').join("");
function fixDoorLines(){ $$("#doorlines a").forEach(a=>a.setAttribute("href",lnH(LINE[a.dataset.lk]))); }
addEventListener("hashchange",fixDoorLines);
function start(){ fixDoorLines(); render(); setTimeout(buildIndexIdle,300); }
if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",start); else start();
