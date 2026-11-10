/* "What are you noticing?" Runs entirely in this page. Nothing is stored and nothing is sent. */
(function(){
var d=document,box=d.getElementById('nt'),raw=d.getElementById('nt-data');if(!box||!raw)return;
var D=JSON.parse(raw.textContent),STR=JSON.parse(box.getAttribute('data-strings'));
var list=d.getElementById('nt-list'),res=d.getElementById('nt-res'),q=d.getElementById('nt-q'),count=d.getElementById('nt-count'),more=d.getElementById('nt-more'),clear=d.getElementById('nt-clear');
var sets={},ticked={},limit=24;
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var rows=[];D.forEach(function(c,ci){c.i.forEach(function(t,ii){rows.push({k:ci+'.'+ii,c:ci,t:t,l:t.toLowerCase()})})});
function matches(){var on=Object.keys(sets).filter(function(k){return sets[k]}),words=q.value.toLowerCase().split(/\s+/).filter(function(w){return w.length>1});
  if(!on.length&&!words.length)return null;
  return rows.filter(function(r){var c=D[r.c];
    if(on.length&&!on.some(function(s){return c.s.indexOf(s)>-1}))return false;
    return words.every(function(w){return r.l.indexOf(w)>-1})})}
function fill(a,b){return a.replace('{n}',b)}
function draw(){var m=matches(),tk=Object.keys(ticked);
  var show=[],seen={};rows.forEach(function(r){if(ticked[r.k]){show.push(r);seen[r.k]=1}});
  var extra=m?m.filter(function(r){return !seen[r.k]}):[];
  var cut=extra.slice(0,limit);show=show.concat(cut);
  list.innerHTML=show.map(function(r){return '<li><label><input type="checkbox" data-k="'+r.k+'"'+(ticked[r.k]?' checked':'')+'><span>'+esc(r.t)+'</span></label></li>'}).join('');
  count.textContent=m===null&&!tk.length?STR.nt_pick:fill(STR.nt_shown,show.length)+(extra.length>cut.length?' '+fill(STR.nt_signs,extra.length-cut.length):'');
  more.hidden=extra.length<=cut.length;clear.hidden=!tk.length;
  var score={};tk.forEach(function(k){var ci=+k.split('.')[0];score[ci]=(score[ci]||0)+1});
  /* the same sign can be worded alike in several patterns: count close matches too */
  var tw=tk.map(function(k){var p=k.split('.');return D[p[0]].i[p[1]].toLowerCase()});
  var ids=Object.keys(score).sort(function(a,b){return score[b]-score[a]||D[a].n.localeCompare(D[b].n)}).slice(0,12);
  res.innerHTML=ids.length?ids.map(function(ci){var c=D[ci];
    return '<li><p class="nt-n"><a href="'+esc(c.u)+'">'+esc(c.n)+'</a>'+(c.sf?' <span class="tg tg-warn">'+esc(STR.nt_safety)+'</span>':'')+'</p><p class="ui meta">'+esc(fill(STR.nt_match,score[ci]).replace('{t}',tk.length))+' · '+esc(c.f)+'</p><p class="ui"><a href="'+esc(c.u)+'#quick">'+esc(STR.nt_quick)+'</a> · <a href="'+esc(c.u)+'">'+esc(STR.nt_full)+'</a></p></li>'}).join(''):'<li class="ui meta">'+esc(STR.nt_none)+'</li>'}
box.hidden=false;var fb=d.getElementById('nt-fallback');if(fb)fb.hidden=true;
box.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;var k=b.getAttribute('data-set');sets[k]=!sets[k];b.setAttribute('aria-pressed',sets[k]?'true':'false');limit=24;draw()});
q.addEventListener('input',function(){limit=24;draw()});
list.addEventListener('change',function(e){var k=e.target.getAttribute('data-k');if(!k)return;if(e.target.checked)ticked[k]=1;else delete ticked[k];draw();var again=list.querySelector('input[data-k="'+k+'"]');if(again)again.focus()});
more.addEventListener('click',function(){limit+=24;draw()});
clear.addEventListener('click',function(){ticked={};draw();q.focus()});
draw();
})();
