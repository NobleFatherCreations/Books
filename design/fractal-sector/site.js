(function(){
var lv=document.getElementById('leave');
if(lv){lv.addEventListener('click',function(){document.title='Weather';document.body.style.visibility='hidden';
location.replace(navigator.onLine?'https://www.google.com/search?q=weather':'about:blank')});
addEventListener('keydown',function(e){if(e.key!=='Escape'||document.querySelector('#nf-chrome.nf-open'))return;
var n=Date.now();if(n-(window.__esc||0)<600)lv.click();window.__esc=n})}
var bar=document.querySelector('.progress span');
if(bar){var f=function(){var h=document.documentElement,m=h.scrollHeight-h.clientHeight;bar.style.width=(m>0?h.scrollTop/m*100:0)+'%'};
addEventListener('scroll',f,{passive:true});f()}
var toc=document.querySelectorAll('.toc a[href^="#"]');
if(toc.length&&'IntersectionObserver' in window){var map={};toc.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){toc.forEach(function(a){a.classList.remove('on')});
var a=map[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-20% 0px -70% 0px'});
Object.keys(map).forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el)})}
var d=document.querySelector('.toc details');if(d&&matchMedia('(max-width:63.99rem)').matches)d.removeAttribute('open');
var q=document.getElementById('q');
if(q){var li=[].slice.call(document.querySelectorAll('#az li')),none=document.getElementById('none');
q.addEventListener('input',function(){var v=q.value.trim().toLowerCase(),shown=0;
li.forEach(function(l){var ok=!v||l.getAttribute('data-k').indexOf(v)>-1||l.textContent.toLowerCase().indexOf(v)>-1;l.hidden=!ok;if(ok)shown++});
none.hidden=shown>0})}
})();
