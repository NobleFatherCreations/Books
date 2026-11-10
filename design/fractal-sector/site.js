(function(){
"use strict";
var d=document,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return [].slice.call((r||d).querySelectorAll(s))};
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
d.querySelectorAll('.name-line strong').forEach(function(e){e.classList.add('hl')});

/* Leave: replace the page with a neutral site. Escape twice does the same. */
var lv=$('#leave');
if(lv){lv.addEventListener('click',function(){d.title='Weather';d.body.style.visibility='hidden';
  location.replace(navigator.onLine?'https://www.google.com/search?q=weather':'about:blank')});
  addEventListener('keydown',function(e){if(e.key!=='Escape'||$('#nf-chrome.nf-open')||$('dialog[open]')||$('#sw[open]'))return;
    var n=Date.now();if(n-(window.__esc||0)<600)lv.click();window.__esc=n})}

/* Sector switcher: a disclosure; Escape and an outside click close it. */
var sw=$('#sw');
if(sw){addEventListener('keydown',function(e){if(e.key==='Escape'&&sw.open){sw.open=false;$('summary',sw).focus();e.stopPropagation()}},true);
  d.addEventListener('click',function(e){if(sw.open&&!sw.contains(e.target))sw.open=false})}

/* Reading progress */
var bar=$('.progress span');
if(bar){var f=function(){var h=d.documentElement,m=h.scrollHeight-h.clientHeight;bar.style.width=(m>0?h.scrollTop/m*100:0)+'%'};
  addEventListener('scroll',f,{passive:true});f()}

/* On-this-page highlight */
var toc=$$('.toc a[href^="#"]');
if(toc.length&&'IntersectionObserver' in window){var map={};toc.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){toc.forEach(function(a){a.classList.remove('on')});
    var a=map[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-20% 0px -70% 0px'});
  Object.keys(map).forEach(function(id){var el=d.getElementById(id);if(el)io.observe(el)})}
var td=$('.toc details');if(td&&matchMedia('(max-width:63.99rem)').matches)td.removeAttribute('open');

/* A to Z filter */
var q=$('#q');
if(q){var li=$$('#az li'),none=$('#none');
  q.addEventListener('input',function(){var v=q.value.trim().toLowerCase(),shown=0;
    li.forEach(function(l){var ok=!v||l.getAttribute('data-k').indexOf(v)>-1||l.textContent.toLowerCase().indexOf(v)>-1;l.hidden=!ok;if(ok)shown++});
    none.hidden=shown>0})}

/* Search: a dialog over the sector index, loaded on first open (same origin). Nothing typed is stored or sent. */
var sb=$('#sbtn'),dlg=$('#search');
if(sb&&dlg&&dlg.showModal){
  var sq=$('#sq'),sr=$('#sr'),idx=null,opener=null,loading=false;
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var render=function(){var v=sq.value.trim().toLowerCase();
    if(!idx){sr.innerHTML='<p>'+esc(sr.getAttribute('data-loading')||'')+'</p>';return}
    if(!v){sr.innerHTML='';return}
    var hits=idx.filter(function(x){return x.n.toLowerCase().indexOf(v)>-1||x.a.join(' ').toLowerCase().indexOf(v)>-1||x.d.toLowerCase().indexOf(v)>-1})
      .sort(function(a,b){var an=a.n.toLowerCase().indexOf(v),bn=b.n.toLowerCase().indexOf(v);an=an<0?99:an;bn=bn<0?99:bn;return an-bn||a.n.localeCompare(b.n)});
    var g=function(t,h){var xs=hits.filter(function(x){return x.t===t}).slice(0,8);if(!xs.length)return '';
      return '<h3>'+h+'</h3><ul>'+xs.map(function(x){return '<li><a href="'+esc(x.u)+'"><b>'+esc(x.n)+'</b><small>'+esc(x.s)+' · '+esc(x.d)+'</small></a></li>'}).join('')+'</ul>'};
    var h=g('p',sr.getAttribute('data-p'))+g('t',sr.getAttribute('data-t'));
    sr.innerHTML=h||'<p>'+esc(sr.getAttribute('data-empty'))+'</p>'};
  var load=function(){if(idx||loading)return;loading=true;
    fetch(d.body.getAttribute('data-search'),{credentials:'same-origin'}).then(function(r){return r.json()}).then(function(j){idx=j;render()})
      .catch(function(){loading=false})};
  sb.addEventListener('click',function(e){e.preventDefault();opener=sb;dlg.showModal();sq.focus();load();render()});
  addEventListener('keydown',function(e){if((e.key==='/'&&!/input|textarea|select/i.test(d.activeElement.tagName))||(e.key==='k'&&(e.metaKey||e.ctrlKey))){if(!dlg.open){e.preventDefault();sb.click()}}});
  dlg.addEventListener('close',function(){if(opener)opener.focus()});
  dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
  sq.addEventListener('input',render);
  dlg.addEventListener('keydown',function(e){if(e.key!=='ArrowDown'&&e.key!=='ArrowUp')return;var ls=$$('a',sr);if(!ls.length)return;
    var i=ls.indexOf(d.activeElement);e.preventDefault();
    if(e.key==='ArrowDown')(i<0?ls[0]:ls[Math.min(i+1,ls.length-1)]).focus();else if(i<=0)sq.focus();else ls[i-1].focus()})}

/* Patterns: filter, sort, narrow; state mirrored in the URL query (nothing stored). */
var pf=$('#pf'),pl=$('#plist');
if(pf&&pl){
  var rows=$$('.prow',pl),count=$('#count'),pnone=$('#pnone'),total=+pl.getAttribute('data-total'),tpl=pl.getAttribute('data-tpl');
  var fl=$('#filters');if(fl&&matchMedia('(min-width:48rem)').matches)fl.open=true;
  var F=['q','fit','family','setting','n','sort','safety'];
  var get=function(){var o={};F.forEach(function(k){var el=pf.elements[k];if(!el)return;
    if(el.type==='checkbox')o[k]=el.checked?'1':'';else o[k]=el.value||''});if(o.sort==='az')o.sort='';return o};
  var set=function(o){F.forEach(function(k){var el=pf.elements[k];if(!el)return;var v=o[k]||'';
    if(el.type==='checkbox')el.checked=v==='1';else if(el.length&&el[0]&&el[0].type==='radio'){$$('input[name="'+k+'"]',pf).forEach(function(r){r.checked=r.value===v})}
    else{el.value=v;if(el.tagName==='SELECT'&&el.selectedIndex<0)el.selectedIndex=0}})};
  var apply=function(push){var o=get(),v=o.q.trim().toLowerCase(),shown=0;
    rows.forEach(function(r){var n=+r.getAttribute('data-n'),ok=true;
      if(o.fit&&r.getAttribute('data-fit')!==o.fit)ok=false;
      if(ok&&o.family&&r.getAttribute('data-fam')!==o.family)ok=false;
      if(ok&&o.setting&&(' '+r.getAttribute('data-set')+' ').indexOf(' '+o.setting+' ')<0)ok=false;
      if(ok&&o.safety&&r.getAttribute('data-safety')!=='1')ok=false;
      if(ok&&o.n&&!((o.n==='short'&&n<=5)||(o.n==='mid'&&n>=6&&n<=7)||(o.n==='long'&&n>=8)))ok=false;
      if(ok&&v&&r.getAttribute('data-q').indexOf(v)<0)ok=false;
      r.hidden=!ok;if(ok)shown++});
    var key={'':function(r){return r.getAttribute('data-name')},family:function(r){return r.getAttribute('data-fam')+' '+r.getAttribute('data-name')},
      most:function(r){return (100-r.getAttribute('data-n'))+' '+r.getAttribute('data-name')},ten:function(r){return ('0'+r.getAttribute('data-rank')).slice(-2)+' '+r.getAttribute('data-name')}}[o.sort]||function(r){return r.getAttribute('data-name')};
    rows.slice().sort(function(a,b){var x=key(a),y=key(b);return x<y?-1:x>y?1:0}).forEach(function(r){pl.appendChild(r)});
    count.textContent=tpl.replace('{n}',shown).replace('{total}',total);pnone.hidden=shown>0;
    if(push){var p=new URLSearchParams();F.forEach(function(k){if(o[k])p.set(k,o[k])});var s=p.toString();
      history.replaceState(null,'',location.pathname+(s?'?'+s:''))}};
  var init={};new URLSearchParams(location.search).forEach(function(v,k){init[k]=v});set(init);
  pf.addEventListener('input',function(){apply(true)});pf.addEventListener('change',function(){apply(true)});
  $('#pf-reset').addEventListener('click',function(){set({});apply(true)});
  apply(false)}

/* Combo pages: three reading modes over the same words, and the sequence stepper. */
var cb=$('#combo');
if(cb){
  var btns=$$('.modes button'),steps=$$('.steps>li',cb),mount=$('.stepper-mount',cb),bd=$('.breakdown',cb);
  var lab=function(k){return cb.getAttribute('data-'+k)||k},cur=0,timer=null,st=null;
  var stopPlay=function(){if(timer){clearInterval(timer);timer=null;if(st)st.play.textContent=lab('play');}};
  var show=function(i){if(!st)return;cur=Math.max(0,Math.min(steps.length-1,i));
    steps.forEach(function(li,j){li.classList.toggle('cur',j===cur)});
    st.nodes.forEach(function(b,j){if(j===cur)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')});
    st.pos.textContent=lab('step').replace('{n}',cur+1).replace('{total}',steps.length);
    st.prev.disabled=cur===0;st.next.disabled=cur===steps.length-1};
  var build=function(){if(st||RM||!steps.length||!mount)return;
    var box=d.createElement('div');box.className='stepper';box.setAttribute('role','group');box.setAttribute('aria-label',lab('mode-seq'));
    var ol=d.createElement('ol');ol.className='st-nodes';
    var nodes=steps.map(function(li,j){var b=d.createElement('button');b.type='button';var a=li.querySelector('strong');
      b.innerHTML='<span aria-hidden="true">'+(j+1)+'</span><span class="vh">'+lab('step').replace('{n}',j+1).replace('{total}',steps.length)+(a?': '+a.textContent:'')+'</span>';
      b.addEventListener('click',function(){stopPlay();show(j)});var x=d.createElement('li');x.appendChild(b);ol.appendChild(x);return b});
    var row=d.createElement('div');row.className='st-row';
    var pos=d.createElement('p');pos.className='st-pos';pos.setAttribute('aria-live','polite');pos.style.margin='0';
    var mk=function(t){var b=d.createElement('button');b.type='button';b.className='btn';b.textContent=t;return b};
    var prev=mk(lab('prev')),next=mk(lab('next')),play=mk(lab('play'));
    prev.addEventListener('click',function(){stopPlay();show(cur-1)});next.addEventListener('click',function(){stopPlay();show(cur+1)});
    play.addEventListener('click',function(){if(timer){stopPlay();return}play.textContent=lab('pause');
      timer=setInterval(function(){if(cur>=steps.length-1){stopPlay();return}show(cur+1)},6000)});
    row.appendChild(pos);row.appendChild(prev);row.appendChild(next);row.appendChild(play);
    box.appendChild(ol);box.appendChild(row);mount.appendChild(box);
    box.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){stopPlay();show(cur+1)}else if(e.key==='ArrowLeft'){stopPlay();show(cur-1)}});
    ['pointerdown','keydown','wheel','touchstart'].forEach(function(t){addEventListener(t,function(e){if(timer&&!(e.target===play))stopPlay()},{passive:true})});
    st={box:box,nodes:nodes,pos:pos,prev:prev,next:next,play:play}};
  var setMode=function(m,fromHash){if(['quick','seq','full'].indexOf(m)<0)m='full';cb.setAttribute('data-mode',m);
    btns.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-mode')===m?'true':'false')});
    if(m==='seq'){build();if(st){bd.classList.add('seq-on');st.box.hidden=false;show(cur)}}
    else{stopPlay();if(bd)bd.classList.remove('seq-on');if(st)st.box.hidden=true}
    if(!fromHash){var h=m==='quick'?'#quick':m==='seq'?'#sequence':'';history.replaceState(null,'',location.pathname+location.search+h)}};
  var fromHash=function(){var h=location.hash.slice(1);
    if(h==='quick')setMode('quick',true);else if(h==='sequence')setMode('seq',true);
    else if(h==='full'||!h)setMode('full',true);
    else{var t=d.getElementById(h),dm=cb.getAttribute('data-mode');if(t&&dm!=='full'){var sec=t.closest('[data-m]');if(sec&&(' '+sec.getAttribute('data-m')+' ').indexOf(' '+dm+' ')<0)setMode('full',true)}}};
  btns.forEach(function(b){b.addEventListener('click',function(){setMode(b.getAttribute('data-mode'));var m=$('.modes');if(m&&m.getBoundingClientRect().top<0)scrollTo(0,cb.offsetTop)})});
  addEventListener('hashchange',fromHash);fromHash()}
})();
