(function () {
  var d = document, h = d.documentElement; h.classList.add('js');
  // Leave: replace this page so Back cannot return; Escape twice does the same
  var leaveTo = 'https://www.google.com/search?q=weather';
  function leave(ev) { if (ev) ev.preventDefault(); location.replace(leaveTo); }
  d.querySelectorAll('[data-leave]').forEach(function (a) { a.addEventListener('click', leave); });
  var esc = 0, escT;

  // menu sheet: slides in from the edge it belongs to, leaves faster than it came
  var sheet = d.getElementById('sheet'), btn = d.querySelector('.menu-b'), lastFocus = null, closeT;
  function openSheet() {
    if (!sheet) return; clearTimeout(closeT); lastFocus = d.activeElement; sheet.hidden = false; h.classList.add('sheet-open');
    btn && btn.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(function () { requestAnimationFrame(function () { sheet.classList.add('open'); }); });
    setTimeout(function () { var x = sheet.querySelector('[data-close].ib'); x && x.focus(); }, 30);
  }
  function closeSheet() {
    if (!sheet || sheet.hidden) return; sheet.classList.remove('open'); h.classList.remove('sheet-open');
    btn && btn.setAttribute('aria-expanded', 'false'); closeT = setTimeout(function () { sheet.hidden = true; }, 200); lastFocus && lastFocus.focus();
  }
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

  // the chain forms as you read: path drawn to the step you are on, steps behind you lit, the thread filled
  var links = [].slice.call(d.querySelectorAll('.chain .link'));
  var forms = [].slice.call(d.querySelectorAll('[data-form] .sig, .margin .sig')).map(function (svg) {
    var p = svg.querySelector('.path'); if (!p) return null;
    var pts = (p.getAttribute('d') || '').replace(/^M/, '').split(' L').map(function (s) { var q = s.trim().split(/\s+/); return [+q[0], +q[1]]; });
    var cum = [0]; for (var i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    var len = cum[cum.length - 1] || 1;
    svg.setAttribute('data-forming', ''); p.style.strokeDasharray = len + ' ' + len;
    return { svg: svg, p: p, cum: cum, len: len, dots: svg.querySelectorAll('.dot'), nums: svg.querySelectorAll('.sig-n') };
  }).filter(Boolean);
  var marginLab = d.querySelector('.margin-step'), rows = [].slice.call(d.querySelectorAll('.tl .tl-row'));
  var reveal = d.querySelector('.reveal-name'), revealSec = d.querySelector('.sec-the-name');
  var prog = d.querySelector('.prog span'), body = d.querySelector('.ch-body');
  function frame() {
    ticking = false; var vh = innerHeight, line = vh * 0.42;
    if (prog && body) { var r = body.getBoundingClientRect(); var pr = Math.min(1, Math.max(0, (vh * .35 - r.top) / (r.height - vh * .4))); prog.style.transform = 'scaleX(' + pr.toFixed(4) + ')'; }
    if (reveal && revealSec) { var rr = revealSec.getBoundingClientRect(); var t = Math.min(1, Math.max(0, (vh * .85 - rr.top) / (vh * .45))); reveal.style.setProperty('--rv', (t * 100).toFixed(1) + '%'); }
    if (!links.length) return;
    var k = -1, frac = 0;
    for (var i = 0; i < links.length; i++) { var b = links[i].getBoundingClientRect(); if (b.top < line) { k = i; frac = Math.min(1, Math.max(0, (line - b.top) / Math.max(1, b.height))); } }
    var first = links[0].getBoundingClientRect().top, last = links[links.length - 1].getBoundingClientRect().bottom;
    var done = last < line - 40, before = first > vh;
    links.forEach(function (l, i) { l.classList.toggle('past', done || i < k || (i === k && frac > .98)); l.classList.toggle('cur', !done && i === k); });
    var row = -1; rows.forEach(function (rw, i) { var b = rw.getBoundingClientRect(); if (b.top < line && b.bottom > 0) row = i; });
    forms.forEach(function (f) {
      var n = f.dots.length, isMargin = !!f.svg.closest('.margin');
      var kk = done || before && isMargin ? n - 1 : Math.max(0, k), fr = done ? 1 : (k < 0 ? 0 : frac);
      if (before && !isMargin) { kk = 0; fr = 0; }
      var at = kk >= n - 1 ? f.len : f.cum[kk] + (f.cum[kk + 1] - f.cum[kk]) * fr;
      f.p.style.strokeDashoffset = (f.len - at).toFixed(2);
      var cur = (!done && k >= 0) ? k : (row >= 0 && isMargin ? row : -1);
      f.dots.forEach(function (dt, i) { dt.classList.toggle('on', i <= kk || done); dt.classList.toggle('cur', i === cur); });
      f.nums.forEach(function (nm, i) { nm.classList.toggle('on', i <= kk || done); });
    });
    var capStep = d.querySelector('.sigcap-step');
    if (capStep) { var ci = (!done && k >= 0) ? k : -1, cel = ci < 0 ? null : links[ci]; var cn = cel && cel.querySelector('.link-name'); capStep.textContent = cn ? (ci + 1) + ' · ' + cn.textContent : (done ? '' : (links[0].querySelector('.link-name') ? '1 · ' + links[0].querySelector('.link-name').textContent : '')); }
    if (marginLab) {
      var idx = (!done && k >= 0) ? k : row, el = idx < 0 ? null : ((!done && k >= 0) ? links[idx] : rows[idx]);
      var nm = el && el.querySelector('.link-name, .tl-tac'); marginLab.textContent = nm ? (idx + 1) + ' · ' + nm.textContent : '';
    }
  }
  var ticking = false;
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  addEventListener('resize', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  // the section rail follows the reader
  var rail = d.querySelectorAll('.rail a');
  if (rail.length && 'IntersectionObserver' in window) {
    var map = {}; rail.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { rail.forEach(function (a) { a.classList.remove('on'); }); var a = map[en.target.id]; a && a.classList.add('on'); } }); }, { rootMargin: '-30% 0px -60% 0px' });
    d.querySelectorAll('.ch-body .sec').forEach(function (s) { io.observe(s); });
  }

  // the margin shape appears once the larger shapes have scrolled away
  var m = d.querySelector('.margin');
  if (m && 'IntersectionObserver' in window) {
    var vis = new Map(), mo = new IntersectionObserver(function (es) { es.forEach(function (en) { vis.set(en.target, en.isIntersecting); });
      var away = false; vis.forEach(function (v) { if (v) away = true; }); m.classList.toggle('away', away); }, { threshold: 0.15 });
    [d.querySelector('.ch-head'), d.querySelector('.sigfig')].forEach(function (x) { x && mo.observe(x); });
  }

  // copy a line to say; if the browser refuses, select it so it can be copied by hand
  d.querySelectorAll('.copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy'), lab = b.querySelector('span');
      var done = function (msg) { b.classList.add('done'); lab.textContent = msg; setTimeout(function () { b.classList.remove('done'); lab.textContent = 'Copy'; }, 1800); };
      var fallback = function () { var p = b.parentNode.querySelector('p'); var s = getSelection(), rg = d.createRange(); rg.selectNodeContents(p); s.removeAllRanges(); s.addRange(rg); done('Selected'); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function () { done('Copied'); }, fallback); else fallback();
    });
  });
})();
