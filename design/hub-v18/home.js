/* Homepage v18 behaviour. Content works without this script; it only adds the interactions. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const D = JSON.parse($('#home-data').textContent);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const hasG = typeof window.gsap !== 'undefined';
  const bookBy = Object.fromEntries(D.books.map(b => [b.slug, b]));
  const toolBy = Object.fromEntries(D.tools.map(t => [t.slug, t]));

  /* ---------- Leave: one tap (or Esc twice) to a neutral page, replacing this one in history ---------- */
  const leave = () => { try { document.body.style.visibility = 'hidden'; } catch (e) {} location.replace('https://www.google.com/search?q=weather'); };
  $$('[data-leave]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); leave(); }));
  let lastEsc = 0;
  addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if (sheet.hasAttribute('data-open')) { closeSheet(); return; }
    const now = Date.now(); if (now - lastEsc < 600) leave(); lastEsc = now;
  });

  /* ---------- Phone menu ---------- */
  const sheet = $('#sheet'), menuBtn = $('#menu-btn');
  const openSheet = () => { sheet.hidden = false; requestAnimationFrame(() => sheet.setAttribute('data-open', '')); menuBtn.setAttribute('aria-expanded', 'true'); $('a', sheet).focus(); };
  const closeSheet = () => { sheet.removeAttribute('data-open'); menuBtn.setAttribute('aria-expanded', 'false'); setTimeout(() => { sheet.hidden = true; }, 320); menuBtn.focus(); };
  menuBtn.addEventListener('click', openSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  sheet.addEventListener('click', e => { if (e.target === sheet || e.target.closest('a')) closeSheet(); });
  sheet.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    const f = $$('a,button', sheet), first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- Start here: answer -> books + tool, and the hero book turns to the first one ---------- */
  const result = $('#result'), heroImg = $('#hero-cover'), heroFace = $('#hero-face');
  const pickHTML = (k, item, href) => `<a class="pick" href="${href}"><img src="${item.img}" alt="" width="96" height="143" loading="lazy" decoding="async"><span><span class="k">${k}</span><b>${item.title}</b><small>${item.line}</small></span></a>`;
  const swapCover = (src, alt, ar) => {
    document.querySelector('.book3d').style.setProperty('--ar', ar);
    if (heroImg.getAttribute('src') === src) return;
    if (!hasG || reduce.matches) { heroImg.src = src; heroImg.alt = alt; return; }
    gsap.timeline()
      .to(heroFace, { rotateY: 90, duration: .28, ease: 'power2.in' })
      .add(() => { heroImg.src = src; heroImg.alt = alt; })
      .fromTo(heroFace, { rotateY: -90 }, { rotateY: 0, duration: .42, ease: 'back.out(1.6)' });
  };
  $$('.chip').forEach(chip => chip.addEventListener('click', () => {
    const s = D.situations.find(x => x.id === chip.dataset.s);
    $$('.chip').forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
    if (!s.books.length) { result.removeAttribute('data-open'); $('#library').scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth' }); return; }
    const [a, b] = s.books.map(x => bookBy[x]); const t = toolBy[s.tool];
    $('#result-title').textContent = `For “${s.label.toLowerCase()}”`;
    $('#result-note').textContent = s.note;
    $('#result-grid').innerHTML = pickHTML('Start here', a, '/' + a.slug) + pickHTML('Or', b, '/' + b.slug) + pickHTML('Then try', t, '/' + t.slug);
    result.setAttribute('data-open', '');
    swapCover(a.imgLg, a.title + ', cover', a.w + '/' + a.h);
    if (hasG && !reduce.matches) gsap.from('#result-grid .pick', { y: 14, opacity: 0, duration: .45, stagger: .07, ease: 'power3.out', delay: .15, clearProps: 'all' });
    // show the answer: bring the panel into view if it is below the fold (phone and desktop)
    setTimeout(() => { const r = result.getBoundingClientRect(); if (r.top > innerHeight * .6) result.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' }); }, 140);
  }));

  /* ---------- The bigger picture door ---------- */
  const door = $('#door'), doorBtn = $('#door-btn');
  doorBtn.addEventListener('click', () => {
    const open = !door.hasAttribute('data-open');
    door.toggleAttribute('data-open', open);
    doorBtn.setAttribute('aria-expanded', String(open));
    doorBtn.textContent = open ? 'Close the bigger picture' : 'Open the bigger picture';
    $('#door-body').inert = !open;
    if (hasG && !reduce.matches) gsap.to('.spines i', { rotate: open ? -14 : 0, opacity: open ? .35 : 1, duration: .45, stagger: .06, ease: 'power2.out' });
    if (open && hasG && !reduce.matches) gsap.from('#door-body .bk', { y: 24, rotate: -2, opacity: 0, duration: .55, stagger: .09, ease: 'power3.out', delay: .1, clearProps: 'all' });
  });

  /* ---------- Portals: strontium charges in light, then glows and fades in the dark ---------- */
  const CHARGE_S = 1.2, GLOW_S = 7;   // hold ~1.2 s to charge fully; afterglow fades over ~7 s, like the real thing
  $$('.portal').forEach(fig => {
    const night = $('.night', fig), day = $('.day', fig), btn = $('.charge', fig), label = $('.label', btn), state = fig.parentElement.querySelector('.state');
    const v = { c: 0, g: 0 }; let chargeT, glowT;
    const paint = () => { fig.style.setProperty('--c', v.c.toFixed(3)); night.style.opacity = v.g; day.style.opacity = 1 - v.g * .92; };
    const say = t => { state.textContent = t; };
    const glow = () => {
      if (chargeT) chargeT.kill(); fig.classList.remove('is-charging');
      if (v.c < .05) { v.c = 0; paint(); label.textContent = 'Hold to charge'; say('In daylight'); return; }
      fig.classList.add('is-glowing'); btn.setAttribute('aria-pressed', 'true'); label.textContent = 'Glowing'; say('Glowing in the dark');
      if (!hasG || reduce.matches) { v.g = 1; v.c = 0; paint(); return; }   // reduced motion: it simply glows until charged again
      if (glowT) glowT.kill();
      glowT = gsap.timeline()
        .to(v, { g: Math.min(1, .35 + v.c), duration: .35, ease: 'power2.out', onUpdate: paint })
        .to(v, { c: 0, duration: .5, ease: 'power2.out', onUpdate: paint }, 0)
        .to(v, { g: 0, duration: GLOW_S * Math.max(.4, v.c), ease: 'power2.in', onUpdate: paint,
                 onComplete: () => { fig.classList.remove('is-glowing'); btn.setAttribute('aria-pressed', 'false'); label.textContent = 'Hold to charge'; say('In daylight'); } });
    };
    const charge = e => {
      if (e && e.button > 0) return;
      if (glowT) glowT.kill(); fig.classList.add('is-charging'); label.textContent = 'Charging'; say('Charging');
      if (!hasG || reduce.matches) { v.c = 1; paint(); return; }
      v.g = 0; paint();
      chargeT = gsap.to(v, { c: 1, duration: CHARGE_S * (1 - v.c), ease: 'none', onUpdate: paint, onComplete: () => { if (navigator.vibrate) navigator.vibrate(12); } });
    };
    const lamp = e => { const r = fig.getBoundingClientRect(); fig.style.setProperty('--lx', (e.clientX - r.left) + 'px'); fig.style.setProperty('--ly', (e.clientY - r.top) + 'px'); };
    fig.addEventListener('pointerdown', e => { lamp(e); try { fig.setPointerCapture(e.pointerId); } catch (x) {} charge(e); });
    fig.addEventListener('pointermove', lamp);
    fig.addEventListener('pointerup', glow);
    fig.addEventListener('pointercancel', glow);
    fig.addEventListener('contextmenu', e => e.preventDefault());
    // keyboard: Enter/Space charges fully and lets go
    btn.addEventListener('click', e => { if (e.detail === 0) { v.c = 1; glow(); } });
    paint();
  });

  /* ---------- Music ---------- */
  const audio = new Audio(); audio.preload = 'none'; let cur = null;
  const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  $$('.trk').forEach(row => {
    const btn = $('.play', row); if (btn.disabled) return;
    btn.addEventListener('click', () => {
      if (cur === row && !audio.paused) { audio.pause(); return; }
      if (cur !== row) { if (cur) cur.classList.remove('is-playing'); cur = row; audio.src = row.dataset.src; }
      audio.play().catch(() => { $('#music-note').textContent = 'That song could not start. Try another, or open the Listening Room.'; });
    });
  });
  const icon = p => p ? '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1h3v12H3zM8 1h3v12H8z"/></svg>' : '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1l10 6-10 6z"/></svg>';
  audio.addEventListener('play', () => { cur.classList.add('is-playing'); const b = $('.play', cur); b.innerHTML = icon(true); b.setAttribute('aria-label', 'Pause ' + cur.dataset.title); });
  audio.addEventListener('pause', () => { if (!cur) return; const b = $('.play', cur); b.innerHTML = icon(false); b.setAttribute('aria-label', 'Play ' + cur.dataset.title); });
  audio.addEventListener('timeupdate', () => { if (cur && audio.duration) { $('.bar i', cur).style.width = (audio.currentTime / audio.duration * 100) + '%'; $('time', cur).textContent = fmt(audio.currentTime); } });
  audio.addEventListener('ended', () => { const next = cur.nextElementSibling; if (next && !$('.play', next).disabled) $('.play', next).click(); });

  /* ---------- Where am I: nav marker + header turns to night in the Workshop ---------- */
  const navLinks = $$('.nav a'); const top = $('.top');
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = e.target.dataset.nav;
    navLinks.forEach(a => a.setAttribute('aria-current', String(a.dataset.nav === id)));
    top.classList.toggle('is-night', e.target.dataset.night === '1');
  }), { rootMargin: '-45% 0px -50% 0px' });
  $$('[data-nav]').forEach(s => s.matches('section') && io.observe(s));

  /* ---------- Motion (GSAP). Reduced motion: nothing self-running; the scroll tilt and slider stay. ---------- */
  if (!hasG) return;
  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();
  mm.add({ motion: '(prefers-reduced-motion: no-preference)', still: '(prefers-reduced-motion: reduce)' }, ctx => {
    const { motion } = ctx.conditions;
    // the one orchestrated moment: the book arrives, then turns with the scroll
    if (motion) {
      gsap.from('.book3d', { y: 40, rotateY: -60, opacity: 0, duration: 1.2, ease: 'power3.out', delay: .1 });
      // the words are readable from the first frame; only the book makes an entrance
      // a short float that settles (under 5 s, so nothing moves on its own for long: WCAG 2.2.2)
      gsap.to('.book3d', { y: -10, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3, delay: 1.3 });
      // books arrive one at a time on each shelf, once
      ScrollTrigger.batch('.shelf .bk', { start: 'top 88%', once: true,
        onEnter: els => gsap.from(els, { y: 28, rotate: -1.5, opacity: 0, duration: .6, stagger: .08, ease: 'power3.out', clearProps: 'all' }) });
    }
    gsap.to('.ribbon-track', { xPercent: -30, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: () => '+=' + innerHeight * 2.5, scrub: .8 } });
    gsap.to('#hero-face', { rotateY: -42, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom 30%', scrub: .6 } });
    gsap.to('#hero-face', { '--sheen': '0%', ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
    if (motion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
      const tx = gsap.quickTo('.book3d', 'rotationY', { duration: .8, ease: 'power3.out' }), face = document.querySelector('#hero-face');
      document.querySelector('.hero').addEventListener('pointermove', e => {
        const k = e.clientX / innerWidth; face.style.setProperty('--sheen', (100 - k * 100) + '%'); tx(-30 + (k - .5) * 10);
      });
    }
    gsap.to('.book3d', { rotateY: -8, rotateX: 2, rotateZ: 0, ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .6 } });
    gsap.fromTo('.glowline', { textShadow: '0 0 0px #86ecd200', opacity: .82 }, { textShadow: '0 0 28px #86ecd288', opacity: 1, ease: 'none',
      scrollTrigger: { trigger: '.threshold', start: 'top 80%', end: 'center center', scrub: true } });
  });
})();
