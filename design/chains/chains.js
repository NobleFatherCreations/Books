(function () {
  var d = document, h = d.documentElement; h.classList.add('js');
  // Leave: replace this page so Back cannot return; Escape twice does the same
  var leaveTo = 'https://www.google.com/search?q=weather';
  function leave(ev) { if (ev) ev.preventDefault(); location.replace(leaveTo); }
  d.querySelectorAll('[data-leave]').forEach(function (a) { a.addEventListener('click', leave); });
  var esc = 0, escT;
  // menu sheet
  var sheet = d.getElementById('sheet'), btn = d.querySelector('.menu-b'), lastFocus = null;
  function openSheet() { if (!sheet) return; lastFocus = d.activeElement; sheet.hidden = false; h.classList.add('sheet-open'); btn && btn.setAttribute('aria-expanded', 'true');
    var cur = sheet.querySelector('.cur a') || sheet.querySelector('a,button'); setTimeout(function () { (sheet.querySelector('[data-close].ib') || cur).focus(); }, 0); }
  function closeSheet() { if (!sheet || sheet.hidden) return; sheet.hidden = true; h.classList.remove('sheet-open'); btn && btn.setAttribute('aria-expanded', 'false'); lastFocus && lastFocus.focus(); }
  btn && btn.addEventListener('click', function () { sheet.hidden ? openSheet() : closeSheet(); });
  sheet && sheet.addEventListener('click', function (ev) { if (ev.target.closest('[data-close]')) closeSheet(); else if (ev.target.closest('.sh-toc a')) closeSheet(); });
  d.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') { if (sheet && !sheet.hidden) { closeSheet(); return; } esc++; clearTimeout(escT); escT = setTimeout(function () { esc = 0; }, 800); if (esc >= 2) leave(); return; }
    if (sheet && !sheet.hidden && ev.key === 'Tab') { var f = sheet.querySelectorAll('a,button,summary'); var a = f[0], z = f[f.length - 1];
      if (ev.shiftKey && d.activeElement === a) { ev.preventDefault(); z.focus(); } else if (!ev.shiftKey && d.activeElement === z) { ev.preventDefault(); a.focus(); } }
    if (ev.altKey || ev.ctrlKey || ev.metaKey || /INPUT|TEXTAREA|SELECT/.test((d.activeElement || {}).tagName || '')) return;
    if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') { var l = d.querySelector('.bar a[rel=' + (ev.key === 'ArrowLeft' ? 'prev' : 'next') + ']'); if (l) location.href = l.href; }
  });
  // the House button joins the bar (the shared drawer itself is unchanged)
  var slot = d.querySelector('.house-slot'), seal = d.querySelector('.nf-seal'); if (slot && seal) slot.appendChild(seal);
  // reading progress and the section rail
  var prog = d.querySelector('.prog span'), body = d.querySelector('.ch-body');
  if (prog && body) {
    var tick = false;
    var upd = function () { tick = false; var r = body.getBoundingClientRect(), vh = innerHeight; var p = Math.min(1, Math.max(0, (vh * .35 - r.top) / (r.height - vh * .4))); prog.style.transform = 'scaleX(' + p.toFixed(4) + ')'; };
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
  }
  var rail = d.querySelectorAll('.rail a');
  if (rail.length && 'IntersectionObserver' in window) {
    var map = {}; rail.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { rail.forEach(function (a) { a.classList.remove('on'); }); var a = map[en.target.id]; a && a.classList.add('on'); } }); }, { rootMargin: '-30% 0px -60% 0px' });
    d.querySelectorAll('.ch-body .sec').forEach(function (s) { io.observe(s); });
  }
  // copy a line to say
  d.querySelectorAll('.copy').forEach(function (b) {
    b.addEventListener('click', function () { var t = b.getAttribute('data-copy'), lab = b.querySelector('span');
      var done = function () { b.classList.add('done'); lab.textContent = 'Copied'; setTimeout(function () { b.classList.remove('done'); lab.textContent = 'Copy'; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(done, function () {}); });
  });
})();
(function () {   // the margin shape appears once the title plate (which shows the same shape) has scrolled away
  var m = document.querySelector('.margin'), h = document.querySelector('.ch-head');
  if (!m || !h || !('IntersectionObserver' in window)) return;
  var big = document.querySelector('.sigfig'), vis = new Map();
  var io = new IntersectionObserver(function (es) { es.forEach(function (en) { vis.set(en.target, en.isIntersecting); });
    var away = false; vis.forEach(function (v) { if (v) away = true; }); m.classList.toggle('away', away); }, { threshold: 0.15 });
  io.observe(h); if (big) io.observe(big);
  // while reading the chain step by step, its step lights up in the margin shape
  var dots = m.querySelectorAll('.dot'), lab = m.querySelector('.margin-step');
  var steps = [].slice.call(document.querySelectorAll('.chain .link, .tl .tl-row'));
  if (!dots.length || !steps.length) return;
  var so = new IntersectionObserver(function (es) { es.forEach(function (en) { if (!en.isIntersecting) return;
      var el = en.target, list = el.parentNode.children, i = [].indexOf.call(list, el);
      dots.forEach(function (d, k) { d.classList.toggle('cur', k === i); });
      if (lab) { var nm = el.querySelector('.link-name, .tl-tac'); lab.textContent = (i + 1) + ' · ' + (nm ? nm.textContent : ''); } }); }, { rootMargin: '-35% 0px -55% 0px' });
  steps.forEach(function (s) { so.observe(s); });
})();
