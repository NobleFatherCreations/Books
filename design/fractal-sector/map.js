/* The living map. Pick a pattern: its tactics light up and are joined in order. Pick a tactic: every pattern that uses it lights up.
   Pointer, touch and keyboard all drive the same selection. Nothing is stored or sent. */
(function(){
var d=document,svg=d.getElementById('map'),raw=d.getElementById('map-data');if(!svg||!raw)return;
var D=JSON.parse(raw.textContent),STR=JSON.parse(d.getElementById('map-str').textContent),NS='http://www.w3.org/2000/svg';
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
var tEls=[].slice.call(svg.querySelectorAll('.mt')),cEls=[].slice.call(svg.querySelectorAll('.mc')),path=d.getElementById('map-path'),panel=d.getElementById('map-panel');
var selC=d.getElementById('map-c'),selT=d.getElementById('map-t'),ctl=d.getElementById('map-ctl');ctl.hidden=false;
var uses=D.t.map(function(){return []});D.c.forEach(function(c,ci){c[5].forEach(function(ti,pos){if(ti>=0)uses[ti].push([ci,pos])})});
var cur=null,step=-1;
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
function el(n,a){var e=d.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}
function clearMarks(){tEls.forEach(function(e){e.classList.remove('on','dim')});cEls.forEach(function(e){e.classList.remove('on','dim')});path.textContent='';svg.classList.remove('sel')}
function showCombo(ci,keepStep){var c=D.c[ci];clearMarks();svg.classList.add('sel');cur={k:'c',i:ci};if(!keepStep)step=-1;
  cEls[ci].classList.add('on');
  var pts=[];c[5].forEach(function(ti,pos){if(ti>=0){tEls[ti].classList.add('on');pts.push([D.t[ti][3],D.t[ti][4],pos,ti])}});
  if(pts.length>1){var dstr='M'+pts.map(function(p){return p[0]+' '+p[1]}).join(' L');var p=el('path',{d:dstr,'class':'mp'});path.appendChild(p);
    if(!RM&&p.getTotalLength){var L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L;p.getBoundingClientRect();p.style.transition='stroke-dashoffset .9s cubic-bezier(.16,1,.3,1)';p.style.strokeDashoffset=0}}
  path.appendChild(el('line',{x1:D.c[ci][3],y1:D.c[ci][4],x2:pts.length?pts[0][0]:D.c[ci][3],y2:pts.length?pts[0][1]:D.c[ci][4],'class':'mp0'}));
  pts.forEach(function(p){var g=el('g',{'class':'mn'+(p[2]===step?' cur':'')});g.appendChild(el('circle',{cx:p[0],cy:p[1],r:17}));var t=el('text',{x:p[0],y:p[1]+7,'text-anchor':'middle'});t.textContent=p[2]+1;g.appendChild(t);path.appendChild(g)});
  var items=c[5].map(function(ti,pos){var name=c[6][pos];
    return '<li'+(pos===step?' class="cur"':'')+'>'+(ti>=0?'<span class="sd" style="--c:var(--s'+D.t[ti][2]+')"></span><a href="'+esc(D.t[ti][1])+'">'+esc(name)+'</a> <span class="meta">'+esc(STR.map_stage)+' '+D.t[ti][2]+'</span>':esc(name)+' <span class="meta">'+esc(STR.map_not_on)+'</span>')+'</li>'}).join('');
  panel.innerHTML='<p class="kicker">'+esc(c[2])+'</p><h2><a href="'+esc(c[1])+'">'+esc(c[0])+'</a></h2><p class="ui meta">'+esc(STR.map_seq.replace('{n}',c[5].length))+'</p><ol class="map-seq">'+items+'</ol>'+
    '<p class="map-btn"><button type="button" class="btn" data-a="prev">'+esc(STR.map_prev)+'</button> <button type="button" class="btn" data-a="next">'+esc(STR.map_next)+'</button> <button type="button" class="btn" data-a="clear">'+esc(STR.map_clear)+'</button></p>'+
    (step>=0?'<p class="ui" id="map-step">'+esc(STR.map_step.replace('{a}',step+1).replace('{b}',c[5].length))+': '+esc(c[6][step])+'</p>':'');
  selC.value=String(ci);selT.value=''}
function showTactic(ti){var t=D.t[ti];clearMarks();svg.classList.add('sel');cur={k:'t',i:ti};step=-1;tEls[ti].classList.add('on');
  uses[ti].forEach(function(u){cEls[u[0]].classList.add('on');path.appendChild(el('line',{x1:t[3],y1:t[4],x2:D.c[u[0]][3],y2:D.c[u[0]][4],'class':'mp0'}))});
  var items=uses[ti].map(function(u){var c=D.c[u[0]];return '<li><a href="'+esc(c[1])+'">'+esc(c[0])+'</a> <span class="meta">'+esc(STR.map_step.replace('{a}',u[1]+1).replace('{b}',c[5].length))+'</span> <button type="button" class="lnk" data-c="'+u[0]+'">'+esc(STR.map_open)+'</button></li>'}).join('');
  panel.innerHTML='<p class="kicker"><span class="sd" style="--c:var(--s'+t[2]+')"></span>'+esc(STR.map_stage)+' '+t[2]+' · '+esc(D.stages[t[2]-1])+'</p><h2><a href="'+esc(t[1])+'">'+esc(t[0])+'</a></h2><p class="ui meta">'+esc(uses[ti].length?STR.map_uses.replace('{n}',uses[ti].length):STR.map_none_uses)+'</p><ul class="map-seq">'+items+'</ul><p class="map-btn"><button type="button" class="btn" data-a="clear">'+esc(STR.map_clear)+'</button></p>';
  selT.value=String(ti);selC.value=''}
function reset(){clearMarks();cur=null;step=-1;selC.value='';selT.value='';panel.innerHTML='<p class="ui">'+esc(panel.getAttribute('data-hint')||'')+'</p>'}
panel.setAttribute('data-hint',panel.textContent.trim());
function nearest(ev){var r=svg.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width*1000,y=(ev.clientY-r.top)/r.height*1000,best=null,bd=Math.max(26,22000/r.width);bd*=bd;
  D.c.forEach(function(c,i){var dd=(c[3]-x)*(c[3]-x)+(c[4]-y)*(c[4]-y);if(dd<bd){bd=dd;best={k:'c',i:i}}});
  D.t.forEach(function(t,i){var dd=(t[3]-x)*(t[3]-x)+(t[4]-y)*(t[4]-y);if(dd<bd){bd=dd;best={k:'t',i:i}}});return best}
svg.addEventListener('click',function(e){var n=nearest(e);if(!n){reset();return}if(n.k==='c')showCombo(n.i);else showTactic(n.i)});
selC.addEventListener('change',function(){if(selC.value==='')reset();else showCombo(+selC.value)});
selT.addEventListener('change',function(){if(selT.value==='')reset();else showTactic(+selT.value)});
function go(dir){if(!cur||cur.k!=='c')return;var n=D.c[cur.i][5].length;step=Math.max(0,Math.min(n-1,step+dir));showCombo(cur.i,true)}
panel.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var a=b.getAttribute('data-a');
  if(a==='prev'||a==='next'){go(a==='next'?1:-1);var nb=panel.querySelector('[data-a="'+a+'"]');if(nb)nb.focus()}else if(a==='clear'){reset();selC.focus()}else if(b.hasAttribute('data-c')){showCombo(+b.getAttribute('data-c'));var h=panel.querySelector('h2 a');if(h)h.focus()}});
d.getElementById('map-stage').addEventListener('keydown',function(e){if(!cur||cur.k!=='c'||/select|input/i.test(e.target.tagName))return;if(e.key==='ArrowRight'){e.preventDefault();go(1)}else if(e.key==='ArrowLeft'){e.preventDefault();go(-1)}});
var q=location.hash.match(/^#p=(\d+)$/);if(q&&D.c[+q[1]])showCombo(+q[1]);
})();
