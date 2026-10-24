"use strict";
/* Pattern Decoder v15 — Wayfinding.
   One offline page. Every route is a hash, so back, forward and bookmarks work. Groups are lines,
   tactics are stations, related tactics in other groups are interchanges, sequences are routes.
   Private by default: nothing is written to the device until the reader turns saving on, and while it is
   off the addresses are numbers (#/s/12), not names. See docs/DECODER-V15-ARCHITECTURE.html. */
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
function slugify(s){return (s||"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/(^-+|-+$)/g,"")||"x";}
function sentences(t){ const m=String(t||"").match(/[^.!?]+(?:[.!?]+["”’)]*|$)\s*/g); return (m||[String(t||"")]).map(x=>x.trim()).filter(Boolean); }
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
  save:'<path d="M6 3h12v18l-6-4-6 4z"/>', saved:'<path fill="currentColor" d="M6 3h12v18l-6-4-6 4z"/>',
  tri:'<path d="M12 3 2 20h20z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>',
  cmp:'<path d="M8 3v18M16 3v18M3 8h5M16 16h5"/>', search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', map:'<circle cx="6" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M6 8v4a4 4 0 0 0 4 4h6"/><circle cx="18" cy="6" r="2"/><path d="M18 8v8"/>',
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
const ALPHA = [...E].sort((a,b)=>a.n.localeCompare(b.n));
const crossRel = e => (e.rel||[]).filter(n=>BY[n]&&BY[n].g!==e.g).map(n=>BY[n]);
/* Full entries load per line, the first time a station on that line opens. */
const LCACHE = {};
function full(e){
  if(e.F) return e.F;
  if(!LCACHE[e.g]){ const el=document.getElementById("L-"+e.g); LCACHE[e.g]=el?JSON.parse(el.textContent):{}; }
  e.F=Object.assign({}, e.f, LCACHE[e.g][e.n]||{}); return e.F;
}

/* ---------- the device store: private unless the reader turns saving on ---------- */
const store=(()=>{
  let mem={}, ok=false, on=false, legacy=0;
  try{ localStorage.setItem("__t","1"); localStorage.removeItem("__t"); ok=true; }catch(e){}
  const read=k=>{ try{ const v=localStorage.getItem("fg_"+k); return v===null?undefined:JSON.parse(v); }catch(e){ return undefined; } };
  const wipe=()=>{ if(!ok) return; try{ for(let n=localStorage.length-1;n>=0;n--){ const k=localStorage.key(n); if(k&&k.indexOf("fg_")===0) localStorage.removeItem(k); } }catch(e){} };
  if(ok){ try{ on=localStorage.getItem("fg_save")==="1"; }catch(e){}
    if(!on){ const s=read("starred"), t=read("trail"); legacy=(Array.isArray(s)?s.length:0)+(Array.isArray(t)?t.length:0); } }
  return {
    get saving(){ return on; }, get legacy(){ return legacy; },
    get(k,d){ if(k in mem) return mem[k]; if(on){ const v=read(k); if(v!==undefined){ mem[k]=v; return v; } } return d; },
    set(k,v){ mem[k]=v; if(on&&ok) try{ localStorage.setItem("fg_"+k,JSON.stringify(v)); }catch(e){} },
    setSaving(v){
      if(v&&!on){ ["starred","trail"].forEach(k=>{ const old=read(k); if(Array.isArray(old)){ const cur=mem[k]||[]; mem[k]=k==="starred"?[...new Set(cur.concat(old))]:cur.concat(old.filter(o=>!cur.some(c=>c.name===o.name))); } });
        on=true; legacy=0; if(ok) try{ localStorage.setItem("fg_save","1"); Object.keys(mem).forEach(k=>localStorage.setItem("fg_"+k,JSON.stringify(mem[k]))); }catch(e){} }
      else if(!v&&on){ on=false; wipe(); }
    },
    forgetLegacy(){ wipe(); legacy=0; },
    clearLists(){ const snap={starred:mem.starred||this.get("starred",[]), trail:mem.trail||this.get("trail",[])}; this.set("starred",[]); this.set("trail",[]); return snap; },
    restore(snap){ this.set("starred",snap.starred); this.set("trail",snap.trail); },
    forgetAll(){ mem={}; },
  };
})();
const canon = n => D.aliases[n]||n;
const starred = () => store.get("starred",[]).map(canon).filter(n=>BY[n]);
const isSaved = n => starred().includes(n);
function toggleSave(n){ let s=starred(); s=s.includes(n)?s.filter(x=>x!==n):[n].concat(s); store.set("starred",s); return s.includes(n); }
function logTrail(n){ if(!store.saving) return; const t=store.get("trail",[]).filter(x=>x&&x.name!==n); t.unshift({name:n,ts:Date.now()}); store.set("trail",t.slice(0,100)); }

/* ---------- addresses: names when saving, numbers when private ---------- */
const stH = e => store.saving ? "#/entry/"+e.s : "#/s/"+e.i;
const lnH = l => store.saving ? "#/line/"+l.k : "#/l/"+l.i;
const cpH = (a,b) => store.saving ? "#/compare/"+a.s+"/"+b.s : "#/c/"+a.i+"/"+b.i;
const rtH = r => store.saving ? "#/routes/"+r.s : "#/r/"+r.i;
const readable = e => location.href.split("#")[0]+"#/entry/"+e.s;

/* ---------- small renderers ---------- */
const bullet = (l,cls) => '<span class="b'+(cls?' '+cls:'')+'" data-g="'+l.k+'" aria-hidden="true">'+l.letter+'</span>';
const lineName = l => l.letter+' line, '+l.label;
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
    '<nav aria-label="More"><a href="#/safety">Use this safely</a><a href="#/lines">All lines</a><a href="#/routes">Patterns seen together</a><a href="#/updates">Service updates ('+esc(D.version)+')</a><a href="#/settings">Settings</a></nav></footer>';
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
let HAY=null, STEMS=null;
function buildIndex(){ if(HAY) return;
  HAY=E.map(e=>({name:norm(e.n), names:[norm(e.n)].concat((e.abs||[]).map(norm)), said:norm((e.f.what_it_sounds_like||[]).join(" ")), words:norm((e.kw||[]).join(" ")),
    all:norm([e.n,(e.abs||[]).join(" "),e.sub||"",(e.kw||[]).join(" "),e.f.short_definition,e.f.plain_language_summary,(e.f.what_it_sounds_like||[]).join(" ")].join(" "))}));
  STEMS=HAY.map(h=>({name:stems(h.name),words:stems(h.words),said:stems(h.said),all:stems(h.all),wline:stemLine(h.words),sline:stemLine(h.said)}));
}
function fuzzy(n){
  const toks=searchTokens(n).map(stem); if(!toks.length) return [];
  const w=n.split(" ").map(stem), grams=[];
  for(let i=0;i<w.length-1;i++){ grams.push(w[i]+" "+w[i+1]); if(i<w.length-2) grams.push(w[i]+" "+w[i+1]+" "+w[i+2]); }
  const scored=[];
  E.forEach((e,i)=>{ const st=STEMS[i]; let hits=0,score=0;
    toks.forEach(t=>{ if(!st.all.has(t)) return; hits++; score+=st.name.has(t)?4:st.words.has(t)?3.5:st.said.has(t)?3:1; });
    if(!hits) return; grams.forEach(g=>{ if(st.wline.includes(g)) score+=8; else if(st.sline.includes(g)) score+=6; });
    scored.push({e,hits,score}); });
  const need=toks.length<=2?toks.length:Math.min(3,Math.ceil(toks.length/2));
  const kept=scored.filter(x=>x.hits>=need).sort((a,b)=>b.score-a.score||b.hits-a.hits||a.e.n.localeCompare(b.e.n));
  const top=kept.length?kept[0].score:0;
  return kept.filter(x=>x.score>=Math.max(2,top*.5)).slice(0,12).map(x=>x.e);
}
function search(q){
  buildIndex(); const n=norm(String(q||"").slice(0,400));
  if(!n) return {list:[],n};
  let list=[];
  if(n.replace(/ /g,"").length>=2){
    list=E.map((e,i)=>{ const h=HAY[i]; if(!h.all.includes(n)) return null;
      const r=h.names.some(x=>x===n)?0:h.names.some(x=>x.startsWith(n))?1:h.names.some(x=>x.includes(n))?2:h.words.includes(n)?3:h.said.includes(n)?4:5; return {e,r}; })
      .filter(Boolean).sort((a,b)=>a.r-b.r||a.e.n.localeCompare(b.e.n)).map(x=>x.e);
    if(n.length<4&&list.length>40) list=[];
  }
  if(list.length<5&&n.split(" ").length>1){ const seen=new Set(list); fuzzy(n).forEach(e=>{ if(!seen.has(e)&&list.length<12) list.push(e); }); }
  return {list,n};
}
/* Show the words that matched: the quote it sounds like, or the subtitle, with the shared words marked. */
function snippet(e,n){
  const toks=new Set(searchTokens(n).map(stem)); if(!toks.size&&n) toks.add(stem(n));
  const mark=t=>H(t).replace(/[A-Za-z’']+/g,w=>toks.has(stem(norm(w)))?'<mark>'+w+'</mark>':w);
  const hit=t=>{ const s=stems(norm(t)); for(const x of toks) if(s.has(x)) return true; return norm(t).includes(n); };
  const q=(e.f.what_it_sounds_like||[]).find(hit); if(q) return '“'+mark(q)+'”';
  if(e.sub&&hit(e.sub)) return mark(e.sub);
  return mark(e.sub||e.f.short_definition);
}
let SEARCH_Q = "";
function resultsHTML(){
  const r=search(SEARCH_Q);
  if(!r.n) return '<h2 class="k">Try one of these</h2><div class="rows">'+D.tries.map(t=>'<button class="row" type="button" data-try="'+esc(t)+'"><span class="rt"><b class="nm">'+H(t)+'</b></span>'+ic("arrow")+'</button>').join("")+'</div>'+
    '<div class="blades"><a class="blade quiet" href="#/help"><span class="bt"><b>Not sure what to type?</b><small>Answer two short questions instead</small></span><span class="ar">'+ic("arrow")+'</span></a></div>';
  if(!r.list.length) return '<div class="empty"><p><strong>Nothing matched those words.</strong> Try fewer or plainer words, describe what was said or done, or answer two short questions.</p></div><div class="blades"><a class="blade quiet" href="#/help"><span class="bt"><b>Help me figure it out</b></span><span class="ar">'+ic("arrow")+'</span></a></div>';
  const o=e=>({snip:snippet(e,r.n)});
  return '<h2 class="k">Best match</h2>'+rows([r.list[0]].map(e=>e),{snip:snippet(r.list[0],r.n)})+(r.list.length>1?'<h2 class="k">Also</h2><div class="rows">'+r.list.slice(1).map(e=>rowHTML(e,o(e))).join("")+'</div>':'');
}
function countText(){ const r=search(SEARCH_Q); return !r.n?"":r.list.length?r.list.length+(r.list.length===1?" match":" matches"):"No matches"; }
function viewSearch(){
  return '<div class="view"><h1 class="h-page" tabindex="-1">Search</h1>'+
    '<form class="sfield" role="search" data-search><label class="sr-only" for="q">Search the guide</label>'+ic("search")+
    '<input id="q" type="search" enterkeyhint="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="What was said or done, or a name" value="'+esc(SEARCH_Q)+'">'+
    '<button class="clr" type="button" data-clear aria-label="Clear search"'+(SEARCH_Q?'':' hidden')+'>'+ic("close")+'</button></form>'+
    '<p class="count" id="scount" role="status">'+countText()+'</p><div id="results">'+resultsHTML()+'</div>'+
    '<p class="note" style="margin-top:2rem">What you type stays on this phone. It is never sent anywhere or added to the address.</p></div>';
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
  return Object.keys(tally).sort((a,b)=>tally[b]-tally[a]||a.localeCompare(b)).slice(0,15).map(n=>({e:BY[n], why:why[n], here:!!(set&&(BY[n].w||[]).includes(set))}));
}
function viewHelp(){
  const g=GUIDE, bar='<div class="gsteps" aria-hidden="true">'+[0,1,2].map(i=>'<i class="'+(i<=g.step?"on":"")+'"></i>').join("")+'</div>';
  const stepTxt='<p class="sr-only">Step '+(g.step+1)+' of 3</p>';
  if(g.step===0) return '<div class="view">'+bar+stepTxt+'<h1 class="h-page" tabindex="-1">Where has this been happening?</h1><p class="lede">There are no wrong answers. Nothing you pick is saved.</p>'+
    '<div class="opts">'+D.feelingGroups.map(x=>'<button class="opt" type="button" data-where="'+x.key+'">'+H(x.label)+ic("arrow")+'</button>').join("")+
    '<button class="opt" type="button" data-where="">I’m not sure, or more than one'+ic("arrow")+'</button></div></div>';
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
  const sens=list.slice(0,6).some(m=>m.e.sens);
  return '<div class="view">'+bar+stepTxt+'<h1 class="h-page" tabindex="-1">'+(list.length?'Your closest matches':'Nothing matched yet')+'</h1>'+
    '<div class="picked" aria-label="Your answers">'+(g.where?'<a href="#/help" data-gstep="0">'+H(WHERE[g.where].label)+' · change</a>':'')+
    g.feels.map(k=>'<button type="button" data-unfeel="'+k+'" aria-label="Remove: '+esc(FEEL[k]?FEEL[k].label:k)+'">'+H(FEEL[k]?FEEL[k].label:k)+ic("close")+'</button>').join("")+
    '<button type="button" data-gstep="1">Add more</button></div>'+
    (sens?'<div class="warn" role="note"><div class="band">'+ic("tri")+'If you feel unsafe</div><div class="body"><p>Some of these can come with real danger. If you are afraid of someone, reach a person you trust, a local support service, or emergency services if you are in immediate danger.</p><p><a href="#/safety">More on staying safe</a></p></div></div>':'')+
    (list.length?'<div class="rows">'+top.map(m=>rowHTML(m.e,{why:whyHTML(m)})).join("")+'</div>':'<p class="lede">Try adding another answer.</p>')+
    (rest.length?(g.more?'<h2 class="k">More possible matches</h2><div class="rows">'+rest.map(m=>rowHTML(m.e,{why:whyHTML(m)})).join("")+'</div>':'<button class="linkbtn" type="button" data-gmore>Show '+rest.length+' more possible matches</button>'):'')+
    '<div class="blades" style="margin-top:2rem">'+(list.length?'<button class="blade" type="button" data-maplit>'+'<span class="pict">'+ic("map")+'</span><span class="bt"><b>See them on the map</b><small>Matches often cluster on one or two lines</small></span><span class="ar">'+ic("arrow")+'</span></button>':'')+
    '<button class="blade quiet" type="button" data-greset><span class="bt"><b>Start over</b></span></button></div></div>';
}

/* ---------- a station ---------- */
const RESP=[["soft_clarification","Ask about it gently"],["firm_boundary","Set a clear limit"],["disengagement","Step back"],["support_seeking","Get support"],["workplace_or_professional","At work, school or with services"]];
const STEPS=[["fit","Is this it?"],["understand","Understand it"],["do","What you can do"],["deeper","Go deeper"]];
let STEP=0;
function stepPanels(e){
  const f=full(e), notIt=f.this_may_not_be_it_when||[], says=f.what_it_sounds_like||[], pats=(PATS_OF[e.n]||[]).map(i=>D.recipes[i]), x=crossRel(e), same=(e.rel||[]).filter(n=>BY[n]&&BY[n].g===e.g).map(n=>BY[n]);
  const scriptH={verify:"A check to run before you share or act",self:"Words to say to yourself",say:"Words you could use"}[e.kind];
  return [
    '<h2>Is this it?</h2><p class="hint">One moment proves very little. Weigh it honestly, in both directions. Tick what fits, just for yourself: nothing is counted or kept.</p>'+
      blk("Signs it might be this",fold(f.this_may_be_it_when,"chk",3,tick),"tw")+
      blk("Signs it is probably something else",fold(notIt.concat(f.less_concerning_if||[]),"chk",3,tick),"aw")+
      blk("Questions to ask yourself",fold(f.discernment_questions,"qs"))+
      blk("More worrying if",fold(f.more_concerning_if))+
      blk("What shows up over time",fold(f.pattern_over_time_signs))+
      blk("What else it could be",(f.what_it_is_not&&f.what_it_is_not.length?'<h4 class="small muted" style="margin:0 0 .5rem">What it is not</h4>'+fold(f.what_it_is_not):'')+
        (f.innocent_or_ordinary_possibilities&&f.innocent_or_ordinary_possibilities.length?'<h4 class="small muted" style="margin:1.5rem 0 .5rem">Ordinary explanations</h4>'+fold(f.innocent_or_ordinary_possibilities):'')+
        (f.common_false_positives&&f.common_false_positives.length?'<h4 class="small muted" style="margin:1.5rem 0 .5rem">Often mistaken for this</h4>'+fold(f.common_false_positives):'')),
    '<h2>Understand it</h2><p class="hint">What it is, why it matters, and how it shows up.</p>'+
      blk("What it is",'<div class="text">'+prose(f.expanded_definition)+'</div>')+
      blk("Why it matters",'<div class="text">'+prose(f.why_this_matters)+'</div>')+
      blk("How it shows up",fold(f.what_it_is))+
      (says.length>2?blk("More things people say",'<ul class="says">'+says.slice(2).map(s=>'<li>'+H(s)+'</li>').join("")+'</ul>'):""),
    '<h2>What you can do</h2><p class="hint">'+(e.sens?'Read the safety note at the top first. If speaking up could make things worse, skip the wording below and talk to someone you trust or a local support service.':'Pick what fits. You do not owe anyone a confrontation.')+'</p>'+
      '<div class="blk script"><h3>'+scriptH+'</h3><blockquote id="bs">'+H(String(f.boundary_script||"").replace(/^Verification script[^:]*:\s*/i,""))+'</blockquote><div class="acts"><button class="btn" type="button" data-copy="bs">'+ic("copy")+'Copy the words</button></div></div>'+
      blk("Ways to respond",'<div class="resp">'+RESP.map(r=>f.response_options&&f.response_options[r[0]]?'<div><h4>'+r[1]+'</h4><p>'+H(f.response_options[r[0]])+'</p></div>':'').join("")+'</div>')+
      blk("Is it changing?",'<div class="text">'+prose(f.boundary_respect_check)+prose(f.repair_check)+'</div>')+
      (!e.sens?blk("When to take it more seriously",'<div class="text">'+prose(f.safety_note)+'</div>'):""),
    '<h2>Go deeper</h2><p class="hint">How it works, what it can do to you, and its close relatives.</p>'+
      blk("How it works",'<div class="text">'+prose(f.psychological_mechanism)+'</div>')+
      blk("How it can affect you",'<div class="text">'+prose(f.possible_impact_on_receiver)+'</div>')+
      blk("Telling it apart from its neighbours",'<div class="text">'+prose(f.how_to_distinguish_from_related)+'</div>'+
        (same.length||x.length?'<div class="rows" style="margin-top:1rem">'+same.concat(x).slice(0,6).map(r=>'<div class="xrow">'+rowHTML(r)+'<a class="cmp" href="'+cpH(e,r)+'">Compare</a></div>').join("")+'</div>':''))+
      blk("Using this label fairly",fold(f.misuse_warning))+
      (pats.length?blk("Patterns it is part of",'<div class="rows">'+pats.slice(0,6).map(r=>'<a class="row" href="'+rtH(r)+'"><span class="rt"><b class="nm">'+H(r.n)+'</b><small>'+r.c.length+' tactics that often appear together</small></span></a>').join("")+'</div>'):""),
  ];
}
function viewStation(e){
  if(!e) return notFound();
  logTrail(e.n);
  const l=LINE[e.g], f=full(e), si=l.order.indexOf(e.n), prev=l.st[si-1], next=l.st[si+1], says=f.what_it_sounds_like||[], saved=isSaved(e.n);
  const x=crossRel(e), w=(e.w||[]).map(k=>SET[k]&&SET[k].label).filter(Boolean), pats=(PATS_OF[e.n]||[]).map(i=>D.recipes[i]);
  STEP=0;
  const strip='<nav class="strip" aria-label="Position on the '+esc(lineName(l))+'">'+
      (prev?'<a href="'+stH(prev)+'" data-vt data-pg="prev">'+ic("prev")+'<span>'+H(prev.n)+'</span></a>':'<span class="nolink">Start of line</span>')+
      '<span class="pos">Station '+(si+1)+' of '+l.order.length+'</span>'+
      (next?'<a class="nx" href="'+stH(next)+'" data-vt data-pg="next"><span>'+H(next.n)+'</span>'+ic("next")+'</a>':'<span class="nolink nx">End of line</span>')+
      '<div class="track" aria-hidden="true">'+(prev?'<i class="st"></i><i class="ln"></i>':'<i class="st end"></i>')+'<i class="st here"></i>'+(next?'<i class="ln"></i><i class="st"></i>':'<i class="st end"></i>')+'</div></nav>';
  const panels=stepPanels(e);
  return gloss('<article class="view station" data-g="'+e.g+'" aria-labelledby="st-h">'+
    '<header class="sname"><div class="sign">'+bullet(l,"lg")+'<div><h1 class="h-st" id="st-h" tabindex="-1">'+H(e.n)+'</h1>'+(e.sub?'<p class="sub">'+H(e.sub)+'</p>':'')+'</div></div>'+
      '<p class="onl">On the <a href="'+lnH(l)+'">'+esc(lineName(l))+'</a></p>'+strip+
      '<div class="acts"><button class="btn" type="button" data-save="'+esc(e.n)+'" aria-pressed="'+saved+'">'+ic(saved?"saved":"save")+(saved?'Saved':'Save')+'</button>'+
      '<button class="btn" type="button" data-share>'+ic("share")+'Share link</button><button class="btn" type="button" data-print>'+ic("print")+'Print</button></div></header>'+
    (e.sens?'<section class="warn" role="note" aria-labelledby="w-h"><h2 class="band" id="w-h">'+ic("tri")+'Safety first</h2><div class="body">'+prose(f.safety_note)+'<p class="small"><a href="#/safety">How to use this guide safely</a></p></div></section>':'')+
    '<section class="answer" aria-label="In short"><div class="sum">'+prose(f.plain_language_summary)+'</div>'+
      (says.length?'<h2 class="k">It can sound like</h2><ul class="says">'+says.slice(0,2).map(s=>'<li>'+H(s)+'</li>').join("")+'</ul>':'')+
      (e.abs&&e.abs.length?'<p class="alsoc">Also called '+e.abs.map(H).join(", ")+'</p>':'')+'</section>'+
    '<div class="steps" data-steps><div class="tabs" role="tablist" aria-label="Read this entry in four steps">'+
      STEPS.map((s,i)=>'<button role="tab" type="button" id="t-'+i+'" aria-controls="p-'+i+'" aria-selected="'+(i===0)+'" tabindex="'+(i===0?0:-1)+'"><span class="no">'+(i+1)+'</span>'+s[1]+'</button>').join("")+
      '</div><div class="stepbar" aria-hidden="true"><i style="--p:.25"></i></div>'+
      panels.map((p,i)=>'<section class="panelx" role="tabpanel" id="p-'+i+'" aria-labelledby="t-'+i+'" tabindex="0"'+(i?' hidden':'')+'>'+p+
        (i<3?'<div class="stepnav"><button class="btn pri" type="button" data-step="'+(i+1)+'">Next: '+STEPS[i+1][1]+ic("arrow")+'</button></div>':'')+'</section>').join("")+'</div>'+
    '<aside class="side" aria-label="Around this station">'+
      (x.length?'<section class="xchg"><h2 class="k" style="margin-top:0">Change here for</h2><p class="small muted" style="margin-bottom:.5rem">Look-alikes on other lines</p><div class="rows">'+
        x.slice(0,6).map(r=>'<div class="xrow">'+rowHTML(r)+'<a class="cmp" href="'+cpH(e,r)+'" aria-label="Compare '+esc(e.n)+' with '+esc(r.n)+'">Compare</a></div>').join("")+'</div></section>':'')+
      '<section class="facts"><dl>'+(w.length?'<div><dt>Where it happens</dt><dd>'+w.map(esc).join(", ")+'</dd></div>':'')+
        (pats.length?'<div><dt>Seen in '+pats.length+(pats.length===1?' pattern':' patterns')+'</dt><dd>'+pats.slice(0,3).map(r=>'<a href="'+rtH(r)+'">'+H(r.n)+'</a>').join(", ")+'</dd></div>':'')+'</dl></section></aside>'+
    '<nav class="pn" aria-label="Along the '+esc(lineName(l))+'">'+(prev?'<a href="'+stH(prev)+'" data-vt><small>Previous station</small><b>'+H(prev.n)+'</b></a>':'<span></span>')+
      (next?'<a class="nx" href="'+stH(next)+'" data-vt><small>Next station</small><b>'+H(next.n)+'</b></a>':'')+'</nav>'+
  '</article>');
}
function setStep(n,from,anim){
  const root=$("[data-steps]"); if(!root||n<0||n>3) return;
  const tabs=$$("[role=tab]",root), panels=$$("[role=tabpanel]",root);
  tabs.forEach((t,i)=>{ const on=i===n; t.setAttribute("aria-selected",on); t.tabIndex=on?0:-1; if(i===STEP&&i!==n) t.classList.add("seen"); });
  panels.forEach((p,i)=>{ p.hidden=i!==n; p.classList.remove("in-l","in-r"); });
  if(anim&&motionOK()&&n!==STEP){ void panels[n].offsetWidth; panels[n].classList.add(n>STEP?"in-r":"in-l"); }
  STEP=n; $(".stepbar i",root).style.setProperty("--p",(n+1)/4);
  announce("Step "+(n+1)+" of 4: "+STEPS[n][1]);
  if(from==="next"){ const t=tabs[n]; t.focus({preventScroll:true}); root.scrollIntoView({block:"start",behavior:motionOK()?"smooth":"auto"}); }
}

/* ---------- compare two look-alikes ---------- */
function viewCompare(a,b){
  if(!a||!b||a===b) return notFound();
  const fa=full(a), fb=full(b), la=LINE[a.g], lb=LINE[b.g];
  const col=(e,l,inner)=>'<div data-g="'+e.g+'">'+inner+'</div>';
  const row=(title,fn)=>'<section class="cmp-row"><h2>'+title+'</h2><div class="cmp-g">'+col(a,la,fn(a,fa))+col(b,lb,fn(b,fb))+'</div></section>';
  return '<div class="view"><h1 class="h-page" tabindex="-1">'+H(a.n)+' or '+H(b.n)+'?</h1><p class="lede">Side by side, from what each entry already says.</p>'+
    '<div class="cmp-g">'+[a,b].map(e=>'<div data-g="'+e.g+'"><a class="nm" href="'+stH(e)+'">'+bullet(LINE[e.g],"sm")+'<span>'+H(e.n)+'</span></a><p class="small muted" style="margin-top:.5rem">'+esc(LINE[e.g].label)+'</p></div>').join("")+'</div>'+
    row("In short",(e,f)=>'<p>'+H(f.plain_language_summary)+'</p>')+
    row("It can sound like",(e,f)=>'<ul class="says">'+(f.what_it_sounds_like||[]).slice(0,2).map(s=>'<li>'+H(s)+'</li>').join("")+'</ul>')+
    row("Signs it might be this",(e,f)=>fold((f.this_may_be_it_when||[]).slice(0,3),"tw",3))+
    row("How to tell them apart",(e,f)=>'<div class="text">'+prose(f.how_to_distinguish_from_related)+'</div>')+
    (a.sens||b.sens?'<div class="warn" role="note"><div class="band">'+ic("tri")+'Safety first</div><div class="body"><p>'+[a,b].filter(e=>e.sens).map(e=>H(e.n)).join(" and ")+' can travel with real danger. Read the safety note on '+((a.sens&&b.sens)?'each':'that')+' entry before acting on anything here.</p></div></div>':'')+
    '</div>';
}

/* ---------- lines ---------- */
function viewLine(l){
  if(!l) return notFound();
  const ix=l.st.filter(e=>crossRel(e).length).length;
  return '<div class="view" data-g="'+l.k+'"><div class="lhead">'+bullet(l,"lg")+'<div><h1 class="h-page" tabindex="-1" style="margin-bottom:.5rem">'+esc(l.label)+'</h1><p class="lede" style="margin:0">'+esc(l.blurb)+'</p></div></div>'+
    '<p class="small muted">'+esc(l.letter)+' line · '+l.order.length+' stations · '+ix+' with places to change. Stations next to each other are closely related.</p>'+
    '<div class="legend" aria-hidden="true"><span><i class="pl" style="box-shadow:inset 0 0 0 .1875rem var(--lc)"></i>Station</span><span><i></i>Change here for other lines</span><span>'+ic("tri","tri")+'Safety first</span></div>'+
    '<ol class="ldia">'+l.st.map(e=>{ const xs=[...new Set(crossRel(e).map(r=>r.g))];
      return '<li><a href="'+stH(e)+'" data-vt'+(xs.length?' class="ix"':'')+'><span class="nm">'+H(e.n)+'</span>'+(e.sens?ic("tri","tri"):'')+
        (xs.length?'<span class="xb" aria-hidden="true">'+xs.slice(0,4).map(g=>bullet(LINE[g],"sm")).join("")+'</span>':'')+
        '<span class="sr-only">'+(e.sens?', safety first':'')+(xs.length?', change here for '+xs.map(g=>LINE[g].letter+' line').join(", "):'')+'</span></a></li>'; }).join("")+'</ol>'+
    '<div class="blades" style="margin-top:2rem"><a class="blade quiet" href="#/map"><span class="pict">'+ic("map")+'</span><span class="bt"><b>See this line on the map</b></span><span class="ar">'+ic("arrow")+'</span></a></div></div>';
}
function lineRows(){ return '<ol class="lrows">'+LINES.map(l=>'<li><a class="lrow" href="'+lnH(l)+'">'+bullet(l)+'<span class="lt"><b>'+esc(l.label)+'</b><small>'+esc(l.blurb)+'</small></span><span class="n">'+l.order.length+'</span></a></li>').join("")+'</ol>'; }
function viewLines(tab){
  const tabs=[["","By line"],["az","A to Z"],["where","Where it happens"],["common","Most common"]];
  let body="";
  if(tab==="az"){ const by={}; ALPHA.forEach(e=>{ const c=/[a-z]/i.test(e.n.charAt(0))?e.n.charAt(0).toUpperCase():"#"; (by[c]=by[c]||[]).push(e); });
    const ks=Object.keys(by);
    body='<nav class="seg" aria-label="Jump to a letter">'+ks.map(c=>'<a href="#az-'+c+'" data-jump>'+c+'</a>').join("")+'</nav>'+
      ks.map(c=>'<h2 class="h-sec" id="az-'+c+'" style="margin:2rem 0 .5rem">'+c+'</h2>'+rows(by[c])).join(""); }
  else if(tab==="where") body=D.settings.map(s=>{ const list=E.filter(e=>(e.w||[]).includes(s.k)).sort((a,b)=>b.pop-a.pop||a.n.localeCompare(b.n));
    return '<h2 class="h-sec">'+esc(s.label)+'</h2><p class="small muted" style="margin-bottom:.75rem">'+esc(s.blurb)+' '+list.length+' tactics.</p>'+fold(list,"rows-f",6,e=>rowHTML(e)).replace('class="ul rows-f"','class="rows"'); }).join("");
  else if(tab==="common") body='<p class="lede">A starting point: the tactics that show up most often across the documented patterns.</p>'+rows(D.common.map(n=>BY[n]).filter(Boolean));
  else body='<p class="lede">Ten lines, one for each kind of tactic. Every tactic is a station on its line.</p>'+lineRows();
  return '<div class="view"><h1 class="h-page" tabindex="-1">All lines</h1><nav class="seg" aria-label="Ways to list">'+tabs.map(t=>'<a href="#/lines'+(t[0]?'/'+t[0]:'')+'"'+((tab||"")===t[0]?' aria-current="page"':'')+'>'+t[1]+'</a>').join("")+'</nav>'+body+'</div>';
}

/* ---------- the map: ten lines side by side, stations in line order ---------- */
let MAPLIT=null, MAPSEL=-1, MAPROUTE=null;
function mapGeom(land){
  const g={land, pts:[]};
  if(land){ g.w=96+44*21; g.h=40+LINES.length*52; LINES.forEach((l,li)=>l.st.forEach((e,si)=>{ g.pts[e.i]={x:76+si*21,y:36+li*52}; })); }
  else { g.w=LINES.length*36+8; g.h=56+Math.max(...LINES.map(l=>l.order.length))*15; LINES.forEach((l,li)=>l.st.forEach((e,si)=>{ g.pts[e.i]={x:22+li*36,y:52+si*15}; })); }
  return g;
}
function mapSVG(){
  const land=innerWidth>=900, g=mapGeom(land), lit=new Set(MAPLIT||MAPROUTE||[]);
  let s='<svg class="map'+(lit.size?' dim':'')+'" id="map" viewBox="0 0 '+g.w+' '+g.h+'" role="group" aria-label="Network map of all '+E.length+' stations. Use the arrow keys to move between stations and Enter to open one.">';
  LINES.forEach((l,li)=>{ const a=g.pts[l.st[0].i], b=g.pts[l.st[l.st.length-1].i];
    s+='<g data-g="'+l.k+'"><line class="ln" x1="'+a.x+'" y1="'+a.y+'" x2="'+b.x+'" y2="'+b.y+'"/>'+
      '<g class="bl" aria-hidden="true"><circle cx="'+(land?28:a.x)+'" cy="'+(land?a.y:20)+'" r="12"/><text x="'+(land?28:a.x)+'" y="'+((land?a.y:20)+4.5)+'">'+l.letter+'</text></g></g>'; });
  if(MAPROUTE){ s+='<polyline class="route" points="'+MAPROUTE.map(i=>g.pts[i].x+","+g.pts[i].y).join(" ")+'"/>'; }
  s+='<g id="xl"></g>';
  E.forEach(e=>{ const p=g.pts[e.i], ix=crossRel(e).length>0;
    const entry=MAPSEL>=0?MAPSEL:(lit.size?[...lit][0]:LINES[0].st[0].i);
    s+='<a href="'+stH(e)+'" data-i="'+e.i+'" data-g="'+e.g+'" tabindex="'+(e.i===entry?0:-1)+'" class="'+(lit.has(e.i)?'lit':'')+(e.i===MAPSEL?' sel':'')+'" aria-label="'+esc(e.n+", "+lineName(LINE[e.g]))+'">'+
      '<circle class="st'+(ix?' ix':'')+'" cx="'+p.x+'" cy="'+p.y+'" r="5.5"/></a>'; });
  return s+'</svg>';
}
function drawInterchanges(i){
  const svg=$("#map"), gx=$("#xl"); if(!svg||!gx) return; const g=mapGeom(svg.viewBox.baseVal.width>svg.viewBox.baseVal.height), e=E[i], a=g.pts[i];
  gx.innerHTML=crossRel(e).map(r=>{ const b=g.pts[r.i], mx=(a.x+b.x)/2, my=(a.y+b.y)/2, bend=g.land?-24:24;
    return '<path class="xl draw" d="M'+a.x+' '+a.y+' Q'+(mx+(g.land?0:bend))+' '+(my+(g.land?bend:0))+' '+b.x+' '+b.y+'"/>'; }).join("");
  $$("path",gx).forEach(p=>p.style.setProperty("--len",Math.ceil(p.getTotalLength())));
}
function viewMap(){
  const note=MAPLIT?'<div class="maptools"><span class="small"><b>Showing your '+MAPLIT.length+' matches.</b></span><button class="linkbtn" type="button" data-mapclear>Show every station</button></div>':'';
  return '<div class="view wide"><h1 class="h-page" tabindex="-1">The map</h1><p class="lede">Ten lines, one for each kind of tactic. Lines that share the most look-alikes run side by side. Tap any station to see it and where you can change.</p>'+
    note+'<div class="legend"><span><i class="pl"></i>Station</span><span><i></i>Change here for other lines</span></div><div class="mapwrap">'+mapSVG()+'</div>'+
    '<h2 class="h-sec">Every line as a list</h2>'+lineRows()+'</div>';
}
function openSheet(i){
  const e=E[i], l=LINE[e.g], x=crossRel(e), sh=$("#sheet");
  MAPSEL=i; $$("#map a.sel").forEach(a=>a.classList.remove("sel")); const a=$('#map a[data-i="'+i+'"]'); if(a) a.classList.add("sel");
  drawInterchanges(i);
  sh.innerHTML='<span class="grab" data-grab aria-hidden="true"></span><button class="x" type="button" data-sheetclose aria-label="Close">'+ic("close")+'</button><div class="in" data-g="'+e.g+'">'+
    '<div class="sign" style="display:flex;gap:.75rem;align-items:flex-start">'+bullet(l)+'<div><h2 id="sheet-h" style="font-size:1.5rem;line-height:1.1">'+H(e.n)+'</h2>'+(e.sub?'<p class="muted">'+H(e.sub)+'</p>':'')+'</div></div>'+
    (e.sens?'<p class="small" style="display:flex;gap:.5rem;align-items:center">'+ic("tri","tri")+'<span>Safety first: this entry starts with its safety note.</span></p>':'')+
    '<p>'+H(e.f.plain_language_summary)+'</p>'+
    '<a class="blade pri" href="'+stH(e)+'"><span class="bt"><b>Open this station</b></span><span class="ar">'+ic("arrow")+'</span></a>'+
    (x.length?'<h3 class="k" style="margin:0">Change here for</h3><div class="rows">'+x.slice(0,5).map(r=>rowHTML(r)).join("")+'</div>':'')+'</div>';
  SHEET_RET=a; if(!sh.open){ try{ sh.showModal(); }catch(err){ sh.setAttribute("open",""); } }
  sh.scrollTop=0; const t=$("#sheet-h"); if(t){ t.tabIndex=-1; t.focus(); }
}
let SHEET_RET=null;
function closeSheet(){ const sh=$("#sheet"); if(sh.open) sh.close(); }

/* ---------- routes ---------- */
function viewRoutes(r){
  if(r){ MAPROUTE=r.c.map(n=>BY[n]&&BY[n].i).filter(x=>x!=null);
    const html='<div class="view wide"><h1 class="h-page" tabindex="-1">'+H(r.n)+'</h1><p class="lede">'+H(r.d)+'</p>'+
      '<p class="note">These tactics are often seen together, in roughly this order. It is a pattern, not a prediction: nothing here says what will happen next in your situation.</p>'+
      '<ol class="chain" style="margin-top:2rem">'+r.c.map(n=>{ const e=BY[n]; return e?'<li><a href="'+stH(e)+'" data-vt data-g="'+e.g+'"><span class="rt" style="display:flex;flex-direction:column;gap:.25rem"><b class="nm" style="font:800 1.0625rem/1.25 var(--sign);display:flex;gap:.5rem;align-items:center">'+bullet(LINE[e.g],"sm")+H(e.n)+'</b><small class="muted">'+H(e.f.short_definition)+'</small></span></a></li>':''; }).join("")+'</ol>'+
      '<h2 class="h-sec">On the map</h2><div class="mapwrap">'+mapSVG()+'</div></div>';
    MAPROUTE=null; return html; }
  return '<div class="view"><h1 class="h-page" tabindex="-1">Patterns seen together</h1><p class="lede">Tactics rarely arrive alone. These '+D.recipes.length+' documented patterns show tactics that often appear together, and roughly in what order. They describe what has been seen, never what will happen.</p>'+
    '<div class="rows rlist">'+D.recipes.map(r=>'<a class="row" href="'+rtH(r)+'"><span class="rt"><b class="nm">'+H(r.n)+'</b><small>'+H(r.d)+'</small></span><span class="n">'+r.c.length+'</span></a>').join("")+'</div></div>';
}

/* ---------- saved ---------- */
function viewSaved(){
  if(!store.saving) return '<div class="view"><h1 class="h-page" tabindex="-1">Saved</h1><p class="lede">Saving is off, so nothing you read or save is kept on this device. This is the safer choice if anyone else might use this phone.</p>'+
    (store.legacy?legacyNotice():'')+
    '<div class="notice"><h2>Want to keep tactics for later?</h2><p>Turning saving on keeps the tactics you save, what you recently read and your settings on this device only. You can turn it off again in Settings, and that deletes all of it.</p><div class="acts"><button class="btn pri" type="button" data-saving="on">Turn on saving</button></div></div></div>';
  const st=starred().map(n=>BY[n]), tr=store.get("trail",[]).map(t=>BY[canon(t.name)]).filter(Boolean).slice(0,24);
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
    '<section class="exitplate" aria-labelledby="lv-h"><h2 class="band" id="lv-h" style="margin:0;font-size:1rem">Leaving quickly</h2><div class="body"><p>The green <strong>Leave</strong> button at the top of every page switches straight to a weather page and clears what this page was holding. On a keyboard, press Escape twice. It cannot erase that you visited: your browser may still list this site in its history, so a private browsing window is safer still.</p></div></section>'+
    h("What this guide is")+p("A reading aid. It helps you put a name to something that happened, see what else it could be, and decide what to do next. Some entries are about everyday relationships; others are about workplaces, online life and influence on a whole society.")+
    h("What it is not")+p("It is not a diagnosis, a legal opinion or therapy. It cannot tell you what another person meant, what they are like, or whether you are in danger. Only you, and the people you trust, can weigh that.")+
    h("A signal, not a verdict")+p("One example of a pattern is a reason to look more closely, not proof of motive or character. Every entry says what its tactic is not, because most of these behaviors also have ordinary explanations. Please do not use a label from this guide to attack, shame, threaten, expose or get back at someone.")+
    h("The map and the patterns")+p("Lines group tactics of one kind, and stations next to each other are closely related. A pattern shows tactics that are often seen together. None of it predicts what a particular person will do.")+
    h("The search box")+p("Pasting in something that was said to you finds entries whose wording is close to it. That is a pointer to read further, never a finding. What you type is never added to the address bar or your history, and never sent anywhere.")+
    h("Your privacy")+p("There is no account. Saving is off unless you turn it on: until then nothing is written to this device, the page addresses use numbers instead of tactic names, and the tab shows only the guide's name. The page counts anonymous visits; nothing you read, type or save is sent anywhere.")+
    p('If you turn saving on, your saved tactics, recent reading and settings stay on this device only. Turning it off in <a href="#/settings">Settings</a> deletes all of it.')+
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
      '<p class="help">'+(store.saving?'Saved tactics, recent reading and these settings are kept on this device. Turning saving off deletes all of it.':'Nothing is written to this device. Addresses use numbers instead of tactic names, and the tab shows only the guide\'s name.')+'</p></fieldset>'+
    '<fieldset><legend>Colours</legend>'+ch("theme",PREF.theme,[["auto","Match my phone"],["night","Night"],["day","Day"]])+'</fieldset>'+
    '<fieldset><legend>Text size</legend>'+ch("size",PREF.size,[["m","Standard"],["l","Larger"],["xl","Largest"]])+'</fieldset>'+
    '<fieldset><legend>Line spacing</legend>'+ch("space",PREF.space,[["normal","Standard"],["roomy","Roomier"]])+'</fieldset>'+
    '<fieldset><legend>Motion</legend>'+ch("motion",PREF.motion,[["auto","Match my phone"],["reduce","Reduce"]])+'<p class="help">Nothing moves on its own either way. Reduce also removes the short slides when you tap.</p></fieldset>'+
    '<fieldset><legend>Reading pause</legend>'+ch("breath",store.get("breath",true)?"on":"off",[["on","Suggest a pause after 20 minutes"],["off","Off"]])+'</fieldset>'+
    '</form></div>';
}
const PREF={theme:"auto",size:"m",space:"normal",motion:"auto"};
function loadPrefs(){ Object.keys(PREF).forEach(k=>{ const v=store.get(k,null); if(v) PREF[k]=v; }); applyPrefs(); }
function applyPrefs(){ const r=document.documentElement;
  PREF.theme==="auto"?r.removeAttribute("data-theme"):r.setAttribute("data-theme",PREF.theme);
  PREF.size==="m"?r.removeAttribute("data-size"):r.setAttribute("data-size",PREF.size);
  PREF.space==="roomy"?r.setAttribute("data-space","roomy"):r.removeAttribute("data-space");
  PREF.motion==="reduce"?r.setAttribute("data-motion","reduce"):r.removeAttribute("data-motion"); }
const motionOK = () => PREF.motion!=="reduce" && !matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- home ---------- */
const HOME_SRC = (()=>{ const h=document.getElementById("home-src"); return h?h.outerHTML:""; })();
function viewHome(){ return HOME_SRC; }
function fillHome(){
  const c=$("#continue"); if(!c) return;
  if(store.legacy){ c.innerHTML=legacyNotice(); return; }
  const t=store.saving?store.get("trail",[]).map(x=>BY[canon(x.name)]).filter(Boolean):[];
  c.innerHTML=t.length?'<div class="continue"><span class="small muted">Continue where you left off:</span></div>'+rows([t[0]]):"";
  $$("#main .lrow").forEach(a=>{ const l=LINE[a.getAttribute("href").split("/").pop()]; if(l) a.setAttribute("href",lnH(l)); });
}

/* ---------- router ---------- */
function parse(){ const raw=(location.hash||"").replace(/^#\/?/,""); const p=raw.split("/").map(safeDecode); return {view:p[0]||"",a:p[1]||"",b:p[2]||""}; }
const byNum = (arr,n) => /^\d+$/.test(n)?arr[+n]:undefined;
function stationFrom(slug){ if(BY_SLUG[slug]) return BY_SLUG[slug]; const a=ALIAS_SLUG[slug]; return a&&BY[a]; }
/* Old v9 and v14 addresses keep working. */
function legacy(r){
  const m={guide:"help",narrow:"help",feeling:"help",sky:"map",constellation:"lines",index:"lines/az",all:"lines/az",common:"lines/common",core:"lines/common",
    where:"lines/where",patterns:r.a?"routes/"+r.a:"routes",about:"safety",trail:"saved"};
  if(r.view==="browse") return r.a&&LINE[r.a]?"line/"+r.a:"lines";
  if(r.view==="category") return r.a&&D.catToGroup[r.a]?"line/"+D.catToGroup[r.a]:"lines";
  if(r.view==="entry"&&!BY_SLUG[r.a]&&ALIAS_SLUG[r.a]&&BY[ALIAS_SLUG[r.a]]) return "entry/"+BY[ALIAS_SLUG[r.a]].s;
  return m[r.view];
}
const ROUTES={
  "":()=>viewHome(), help:()=>viewHelp(), search:()=>viewSearch(), map:()=>viewMap(), saved:()=>viewSaved(), safety:()=>viewSafety(), settings:()=>viewSettings(), updates:()=>viewUpdates(),
  lines:r=>viewLines(r.a), line:r=>viewLine(LINE[r.a]), l:r=>viewLine(byNum(LINES,r.a)),
  entry:r=>viewStation(stationFrom(r.a)), s:r=>viewStation(byNum(E,r.a)),
  compare:r=>viewCompare(stationFrom(r.a),stationFrom(r.b)), c:r=>viewCompare(byNum(E,r.a),byNum(E,r.b)),
  routes:r=>viewRoutes(r.a?D.recipes.find(x=>x.s===r.a)||null:null), r:r=>viewRoutes(byNum(D.recipes,r.a)),
};
function ctx(r){ /* what a page is called, and which door it belongs to */
  const st=r.view==="entry"?stationFrom(r.a):r.view==="s"?byNum(E,r.a):null;
  const ln=r.view==="line"?LINE[r.a]:r.view==="l"?byNum(LINES,r.a):null;
  const rt=r.view==="routes"&&r.a?D.recipes.find(x=>x.s===r.a):r.view==="r"?byNum(D.recipes,r.a):null;
  const label = st?st.n : ln?ln.label : rt?rt.n : ({"":"the start",help:GUIDE.step===2?"your matches":"Help",search:SEARCH_Q?"your search":"Search",map:"the map",lines:"All lines",routes:"Patterns",
    saved:"Saved",safety:"Use this safely",settings:"Settings",updates:"Service updates",compare:"the comparison",c:"the comparison"})[r.view]||"the previous page";
  const door={help:"help",search:"search",map:"map",line:"map",l:"map",lines:"map",routes:"map",r:"map",saved:"saved"}[r.view];
  const parent = st?{h:lnH(LINE[st.g]),label:LINE[st.g].label} : ln?{h:"#/lines",label:"All lines"} : rt?{h:"#/routes",label:"Patterns"} : null;
  const title = st?st.n : ln?ln.label : rt?rt.n : ({help:"Help me figure it out",search:"Search",map:"The map",lines:"All lines",routes:"Patterns seen together",saved:"Saved",safety:"Use this safely",settings:"Settings",updates:"Service updates"})[r.view];
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
    const t=document.startViewTransition(()=>{ vtEl.style.viewTransitionName=""; go(); const h=$(".h-st"); if(h) h.style.viewTransitionName="st"; after(r,c,key); });
    t.finished.then(()=>{ const h=$(".h-st"); if(h) h.style.viewTransitionName=""; }).catch(()=>{});
  } else { if(!(FIRST&&!r.view)) go(); else main.insertAdjacentHTML("beforeend",foot()); after(r,c,key); }
}
function after(r,c,key){
  document.title=store.saving&&c.title?c.title+" · Pattern Decoder":"Pattern Decoder";
  $$(".doors a").forEach(a=>{ if(a.dataset.door===(c.door||(c.station||r.view==="compare"||r.view==="c"?LASTDOOR:null))) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); });
  if(!r.view) fillHome();
  noWidows($("#main"));
  if(r.view==="search"){ const q=$("#q"); if(q&&!FIRST) q.focus(); }
  else if(!FIRST){ const h=$("#main h1"); if(h){ if(!h.hasAttribute("tabindex")) h.tabIndex=-1; h.focus({preventScroll:true}); } }
  window.scrollTo(0, SCROLL[key]&&POPPED?SCROLL[key]:0); POPPED=false;
  if(r.view==="map"&&MAPSEL>=0&&!$('#map a[data-i="'+MAPSEL+'"]')) MAPSEL=-1;
  if(r.view==="map"&&MAPSEL>=0) drawInterchanges(MAPSEL);
  FIRST=false;
}
let POPPED=false;
addEventListener("popstate",()=>{ POPPED=true; });
addEventListener("hashchange",(ev)=>{ try{ SCROLL[new URL(ev.oldURL).hash||"#/"]=scrollY; }catch(e){} closeSheet(); render(); });
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

/* ---------- leaving quickly ---------- */
function leave(){ try{ store.forgetAll(); SEARCH_Q=""; GUIDE={step:0,where:null,feels:[]}; document.title="Weather"; $("#main").innerHTML=""; }catch(e){}
  location.replace("https://www.google.com/search?q=weather"); }
let LAST_ESC=0;

/* ---------- events ---------- */
document.addEventListener("click",ev=>{
  const t=ev.target, a=t.closest("a"), b=t.closest("button");
  if(t.closest("#leave")){ leave(); return; }
  if(a&&a.hasAttribute("data-back")&&STACK.length>1){ ev.preventDefault(); history.back(); return; }
  if(a&&a.hasAttribute("data-vt")&&ev.detail>0){ PENDING_VT=a.querySelector(".nm,span")||a; }
  if(a&&a.dataset.i!=null&&a.closest("#map")){ ev.preventDefault(); openSheet(+a.dataset.i); return; }
  if(t.closest("#map")&&!a){ const svg=$("#map"), pt=svg.createSVGPoint(); pt.x=ev.clientX; pt.y=ev.clientY; const p=pt.matrixTransform(svg.getScreenCTM().inverse());
    const g=mapGeom(svg.viewBox.baseVal.width>svg.viewBox.baseVal.height); let best=-1,bd=1e9; g.pts.forEach((q,i)=>{ const d=(q.x-p.x)**2+(q.y-p.y)**2; if(d<bd){bd=d;best=i;} });
    if(best>=0&&bd<22*22) openSheet(best); return; }
  if(a&&a.hasAttribute("data-jump")){ ev.preventDefault(); const el=document.getElementById(a.getAttribute("href").slice(1)); if(el){ el.tabIndex=-1; el.scrollIntoView(); el.focus({preventScroll:true}); } return; }
  if(!b) { if(a&&a.hasAttribute("data-gstep")){ ev.preventDefault(); GUIDE.step=+a.dataset.gstep; render(); } return; }
  const d=b.dataset;
  if(d.fold!=null){ const ul=document.getElementById(d.fold), open=b.getAttribute("aria-expanded")==="true";
    const n=+(d.n||3); $$(":scope>li",ul).forEach((li,i)=>{ if(i>=n) li.hidden=open; }); b.setAttribute("aria-expanded",!open); b.textContent=open?"Show all "+ul.children.length:"Show fewer"; if(!open){ const li=ul.children[n]; if(li){ const f=li.querySelector("input,a"); if(f) f.focus(); } } return; }
  if(d.term){ const el=document.getElementById(d.term), o=b.getAttribute("aria-expanded")==="true"; el.hidden=o; b.setAttribute("aria-expanded",!o); return; }
  if(b.getAttribute("role")==="tab"){ setStep(+b.id.slice(2),"tab",ev.detail>0); return; }
  if(d.step){ setStep(+d.step,"next",true); return; }
  if(d.save!=null){ if(!store.saving){ toast("Saving is off, so nothing is kept on this device.","Turn on saving",()=>{ setSaving(true); const on=toggleSave(d.save); toast(on?"Saved on this device":"Removed"); render(); }); return; }
    const on=toggleSave(d.save); b.setAttribute("aria-pressed",on); b.innerHTML=ic(on?"saved":"save")+(on?"Saved":"Save"); toast(on?"Saved on this device":"Removed from saved"); return; }
  if(d.share!=null){ const e=ctx(parse()).station; if(!e) return; const url=readable(e);
    if(navigator.share){ navigator.share({title:e.n,url}).catch(()=>{}); } else copyText(url,"Link copied"); return; }
  if(d.print!=null){ window.print(); return; }
  if(d.copy){ copyText($("#"+d.copy).textContent,"Copied"); return; }
  if(d.try){ SEARCH_Q=d.try; const q=$("#q"); if(q){ q.value=SEARCH_Q; } updateResults(true); return; }
  if(d.clear!=null){ SEARCH_Q=""; const q=$("#q"); q.value=""; q.focus(); updateResults(true); return; }
  if(d.where!=null){ GUIDE.where=d.where||null; GUIDE.feels=GUIDE.feels.filter(k=>!GUIDE.where||(FEEL[k]&&FEEL[k].group===GUIDE.where)); GUIDE.step=1; GUIDE.err=false; render(); return; }
  if(d.gstep!=null){ GUIDE.step=+d.gstep; GUIDE.err=false; render(); return; }
  if(d.unfeel){ GUIDE.feels=GUIDE.feels.filter(k=>k!==d.unfeel); if(!GUIDE.feels.length) GUIDE.step=1; render(); return; }
  if(d.gmore!=null){ GUIDE.more=true; render(); return; }
  if(d.greset!=null){ GUIDE={step:0,where:null,feels:[],more:false,err:false}; render(); return; }
  if(d.maplit!=null){ MAPLIT=matches().map(m=>m.e.i); MAPSEL=-1; nav("#/map"); return; }
  if(d.mapclear!=null){ MAPLIT=null; render(); return; }
  if(d.sheetclose!=null){ closeSheet(); return; }
  if(d.saving){ setSaving(d.saving==="on"); toast(d.saving==="on"?"Saving is on for this device":"Saving is off"); render(); return; }
  if(d.forgetlegacy!=null){ store.forgetLegacy(); statusUI(); toast("Deleted from this device"); render(); return; }
  if(d.clearlists!=null){ const snap=store.clearLists(); render(); toast("Saved and recent deleted","Undo",()=>{ store.restore(snap); render(); }); return; }
  if(d.toastact!=null){ $("#toast").classList.remove("on"); if(TOAST_FN) TOAST_FN(); TOAST_FN=null; return; }
  if(d.breath){ breathHide(); if(d.breath==="off") store.set("breath",false); return; }
});
const updateResults=(()=>{ let t; return (now)=>{ clearTimeout(t); const run=()=>{ const r=$("#results"); if(!r) return; r.innerHTML=resultsHTML(); const c=$("#scount"); if(c) c.textContent=countText();
  const cl=$("[data-clear]"); if(cl) cl.hidden=!SEARCH_Q; }; if(now) run(); else t=setTimeout(run,90); }; })();
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
    PREF[t.name]=t.value; store.set(t.name,t.value); applyPrefs(); }
});
document.addEventListener("keydown",ev=>{
  const inField=/^(INPUT|TEXTAREA|SELECT)$/.test((ev.target.tagName||""))||ev.target.isContentEditable;
  if(ev.key==="Escape"){ if($("#sheet").open||!$("#breath").hidden){ if(!$("#breath").hidden) breathHide(); return; }
    const now=Date.now(); if(now-LAST_ESC<1000){ leave(); return; } LAST_ESC=now; return; }
  if((ev.key==="k"&&(ev.metaKey||ev.ctrlKey))||(ev.key==="/"&&!inField)){ ev.preventDefault(); nav("#/search"); setTimeout(()=>{ const q=$("#q"); if(q) q.focus(); },0); return; }
  const tab=ev.target.closest&&ev.target.closest("[role=tab]");
  if(tab&&["ArrowLeft","ArrowRight","Home","End"].includes(ev.key)){ ev.preventDefault(); const n=ev.key==="Home"?0:ev.key==="End"?3:(STEP+(ev.key==="ArrowRight"?1:-1)+4)%4; setStep(n); $("#t-"+n).focus(); return; }
  const ma=ev.target.closest&&ev.target.closest("#map a");
  if(ma&&["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].includes(ev.key)){ ev.preventDefault(); const e=E[+ma.dataset.i], l=LINE[e.g], si=l.order.indexOf(e.n), land=innerWidth>=900;
    const along=(land?["ArrowLeft","ArrowRight"]:["ArrowUp","ArrowDown"]).indexOf(ev.key);
    let n;
    if(along>=0){ n=l.st[Math.max(0,Math.min(l.st.length-1,si+(along?1:-1)))]; }
    else { const dir=(land?(ev.key==="ArrowDown"):(ev.key==="ArrowRight"))?1:-1, l2=LINES[Math.max(0,Math.min(LINES.length-1,l.i+dir))]; n=l2.st[Math.min(si,l2.st.length-1)]; }
    const na=$('#map a[data-i="'+n.i+'"]'); ma.tabIndex=-1; na.tabIndex=0; na.focus(); return; }
  if(inField||ev.metaKey||ev.ctrlKey||ev.altKey) return;
  if((ev.key==="j"||ev.key==="k")&&$(".station")){ const pg=$('[data-pg="'+(ev.key==="j"?"next":"prev")+'"]'); if(pg) nav(pg.getAttribute("href")); }
});
document.addEventListener("focusin",ev=>{ const svg=$("#map"); if(svg&&ev.target===svg){ const a=$("#map a.sel")||$("#map a"); a.tabIndex=0; a.focus(); } });
/* swipe between steps; drag the sheet down to close it */
let SW=null;
document.addEventListener("pointerdown",ev=>{
  const p=ev.target.closest(".panelx"); if(p&&ev.pointerType!=="mouse") SW={x:ev.clientX,y:ev.clientY,t:Date.now(),k:"step"};
  if(ev.target.closest("[data-grab]")){ const sh=$("#sheet"); SW={y:ev.clientY,t:Date.now(),k:"sheet"}; sh.style.transition="none"; try{ ev.target.setPointerCapture(ev.pointerId); }catch(e){} }
},{passive:true});
document.addEventListener("pointermove",ev=>{ if(SW&&SW.k==="sheet"){ const dy=ev.clientY-SW.y, sh=$("#sheet"); sh.style.transform="translateY("+(dy>0?dy:dy/(1-dy/40)/3)+"px)"; } },{passive:true});
document.addEventListener("pointerup",ev=>{ if(!SW) return; const s=SW; SW=null;
  if(s.k==="step"){ const dx=ev.clientX-s.x, dy=ev.clientY-s.y; if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.6&&Date.now()-s.t<800) setStep(STEP+(dx<0?1:-1),"swipe",true); return; }
  const dy=ev.clientY-s.y, v=dy/Math.max(1,Date.now()-s.t), sh=$("#sheet");
  sh.style.transition=motionOK()?"transform .22s var(--ease-sheet)":"none";
  if(dy>120||v>.5){ sh.style.transform="translateY(100%)"; setTimeout(()=>{ closeSheet(); sh.style.transform=""; sh.style.transition=""; },motionOK()?200:0); }
  else sh.style.transform="";
});
$("#sheet").addEventListener("close",()=>{ const r=SHEET_RET; SHEET_RET=null; if(r&&document.contains(r)){ $$("#map a").forEach(x=>x.tabIndex=-1); r.tabIndex=0; r.focus(); } });
$("#sheet").addEventListener("click",ev=>{ if(ev.target===ev.currentTarget) closeSheet(); });

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
function start(){ fixDoorLines(); render(); if("requestIdleCallback" in window) requestIdleCallback(buildIndex); else setTimeout(buildIndex,800); }
if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",start); else start();
addEventListener("resize",(()=>{ let t, w=innerWidth>=900; return ()=>{ clearTimeout(t); t=setTimeout(()=>{ const nw=innerWidth>=900; if(nw!==w&&$("#map")){ w=nw; render(); } w=nw; },200); }; })());
