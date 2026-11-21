/* Homepage v18 behaviour. Content works without this script; it only adds the interactions.
   Motion layers on the hero book (never two tweens on one property):
   .book-in  = entrance + short float (y, opacity)   .book-tilt = mouse tilt (rotationY)
   .book3d   = scroll tilt                            #hero-face = scroll cover swing   .leaf = answer turn */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const D = JSON.parse($('#home-data').textContent);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const hasG = typeof window.gsap !== 'undefined';
  const smooth = () => (reduce.matches ? 'auto' : 'smooth');
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
  const sheet = $('#sheet'), menuBtn = $('#menu-btn'); let hideT;
  const openSheet = () => { clearTimeout(hideT); sheet.hidden = false; requestAnimationFrame(() => sheet.setAttribute('data-open', '')); menuBtn.setAttribute('aria-expanded', 'true'); $('a', sheet).focus(); };
  const closeSheet = () => { sheet.removeAttribute('data-open'); menuBtn.setAttribute('aria-expanded', 'false'); clearTimeout(hideT); hideT = setTimeout(() => { sheet.hidden = true; }, 320); menuBtn.focus(); };
  menuBtn.addEventListener('click', openSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  sheet.addEventListener('click', e => { if (e.target === sheet || e.target.closest('a')) closeSheet(); });
  sheet.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    const f = $$('a,button', sheet), first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- Start here: answer -> books + tool; the hero book turns to the first one, then the answer comes into view ---------- */
  const result = $('#result'), heroImg = $('#hero-cover'), leaf = $('#hero-leaf'), book = $('.book3d'), status = $('#result-status');
  let turnT;
  const pickHTML = (k, item, href) => `<a class="pick" href="${href}"><img src="${item.img}" alt="" width="96" height="143" loading="lazy" decoding="async"><span><span class="k">${k}</span><b>${item.title}</b><small>${item.line}</small></span></a>`;
  // bring only the top of the card into view, never a long jump
  const reveal = () => { const r = result.getBoundingClientRect(), over = r.top + Math.min(r.height, 220) - innerHeight; if (over > 0) scrollBy({ top: over + 24, behavior: smooth() }); };
  const swapCover = (src, alt, ar, done) => {
    if (heroImg.getAttribute('src') === src) { done(); return; }
    if (!hasG || reduce.matches) { book.style.setProperty('--ar', ar); heroImg.src = src; heroImg.alt = alt; done(); return; }
    if (turnT) turnT.progress(1).kill();
    turnT = gsap.timeline({ onComplete: done })
      .to(leaf, { rotateY: 90, duration: .26, ease: 'power2.in' })
      .add(() => { book.style.setProperty('--ar', ar); heroImg.src = src; heroImg.alt = alt; })
      .fromTo(leaf, { rotateY: -90 }, { rotateY: 0, duration: .42, ease: 'back.out(1.4)' });
  };
  const setOpen = open => { result.toggleAttribute('data-open', open); result.inert = !open; };
  setOpen(false);
  $$('.chip').forEach(chip => chip.addEventListener('click', () => {
    const s = D.situations.find(x => x.id === chip.dataset.s);
    $$('.chip').forEach(c => c.setAttribute('aria-pressed', String(c === chip)));
    if (!s.books.length) {
      // collapse instantly so the scroll lands on the library, not mid-way
      result.style.transition = 'none'; setOpen(false); void result.offsetHeight;
      $('#library').scrollIntoView({ behavior: smooth() });
      requestAnimationFrame(() => { result.style.transition = ''; });
      status.textContent = ''; return;
    }
    const [a, b] = s.books.map(x => bookBy[x]); const t = toolBy[s.tool];
    $('#result-title').textContent = `For “${s.label.toLowerCase()}”`;
    $('#result-note').textContent = s.note;
    $('#result-grid').innerHTML = pickHTML('Start here', a, '/' + a.slug) + pickHTML('Or', b, '/' + b.slug) + pickHTML('Then try', t, '/' + t.slug);
    status.textContent = `Three suggestions for ${s.label.toLowerCase()}: ${a.title}, ${b.title}, and ${t.title}.`;
    setOpen(true);
    if (hasG && !reduce.matches) gsap.from('#result-grid .pick', { y: 14, opacity: 0, duration: .45, stagger: .07, ease: 'power3.out', delay: .1, clearProps: 'all' });
    swapCover(a.imgLg, a.title + ', cover', a.w + '/' + a.h, () => setTimeout(reveal, reduce.matches ? 0 : 120));
  }));
  $('#redo').addEventListener('click', () => { const c = $('.chip[aria-pressed="true"]') || $('.chip'); $('#ask').scrollIntoView({ behavior: smooth(), block: 'center' }); c.focus({ preventScroll: true }); });

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
  const CHARGE_S = 1.2, GLOW_S = 7;   // hold ~1.2 s to charge fully; the afterglow fades over ~7 s, fast at first then slow, like the real thing
  $$('.portal').forEach(fig => {
    const li = fig.parentElement, night = $('.night', fig), day = $('.day', fig), btn = $('.charge', li), label = $('.label', btn), live = $('.portal-status', li), name = fig.dataset.name;
    const v = { c: 0, g: 0 }; let chargeT, glowT, held = false;
    const paint = () => { const c = v.c.toFixed(3); fig.style.setProperty('--c', c); btn.style.setProperty('--c', c); night.style.opacity = v.g; day.style.opacity = 1 - v.g * .92; };
    const rest = () => { fig.classList.remove('is-glowing', 'is-charging'); label.textContent = 'Hold to charge'; };
    const glow = () => {
      if (!held) return; held = false;
      if (chargeT) chargeT.kill(); fig.classList.remove('is-charging');
      if (v.c < .05) { v.c = 0; v.g = 0; paint(); rest(); return; }
      fig.classList.add('is-glowing'); label.textContent = 'Glowing'; live.textContent = `${name} is glowing in the dark.`;
      if (!hasG || reduce.matches) { v.g = 1; v.c = 0; paint(); return; }   // reduced motion: it simply glows until charged again
      if (glowT) glowT.kill();
      glowT = gsap.timeline()
        .to(v, { g: Math.min(1, .35 + v.c), duration: .35, ease: 'power2.out', onUpdate: paint })
        .to(v, { c: 0, duration: .5, ease: 'power2.out', onUpdate: paint }, 0)
        .to(v, { g: 0, duration: GLOW_S * Math.max(.4, v.c), ease: 'power1.out', onUpdate: paint, onComplete: () => { rest(); live.textContent = ''; } });
    };
    const charge = () => {
      if (held) return; held = true;
      if (glowT) glowT.kill(); fig.classList.add('is-charging'); label.textContent = 'Charging';
      if (!hasG || reduce.matches) { v.c = 1; v.g = 0; paint(); return; }
      if (v.g > 0) gsap.to(v, { g: 0, duration: .25, ease: 'power2.out', onUpdate: paint });   // from glowing back to the light, no snap
      chargeT = gsap.to(v, { c: 1, duration: CHARGE_S * (1 - v.c), ease: 'none', onUpdate: paint, onComplete: () => { if (navigator.vibrate) navigator.vibrate(12); } });
    };
    const lamp = e => { const r = fig.getBoundingClientRect(); fig.style.setProperty('--lx', (e.clientX - r.left) + 'px'); fig.style.setProperty('--ly', (e.clientY - r.top) + 'px'); };
    [fig, btn].forEach(el => {
      el.addEventListener('pointerdown', e => {
        if (e.button > 0) return;
        if (el === fig) lamp(e); else { fig.style.setProperty('--lx', '50%'); fig.style.setProperty('--ly', '50%'); }
        try { el.setPointerCapture(e.pointerId); } catch (x) {}
        charge();
      });
      el.addEventListener('pointerup', glow);
      el.addEventListener('pointercancel', glow);
      el.addEventListener('contextmenu', e => e.preventDefault());
    });
    fig.addEventListener('pointermove', lamp);
    // keyboard: hold Space or Enter to charge, let go to glow
    btn.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); fig.style.setProperty('--lx', '50%'); fig.style.setProperty('--ly', '50%'); charge(); } });
    btn.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); glow(); } });
    btn.addEventListener('blur', glow);
    paint();
  });

  /* ---------- Music ---------- */
  const audio = new Audio(); audio.preload = 'none'; let cur = null;
  const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  $$('.trk').forEach(row => {
    const btn = $('.play', row); if (!btn) return;
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
  audio.addEventListener('ended', () => { const next = cur.nextElementSibling; if (next && $('.play', next)) $('.play', next).click(); });

  /* ---------- Where am I: nav marker + header turns to night in the Workshop ---------- */
  const navLinks = $$('.nav a'); const top = $('.top');
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = e.target.dataset.nav;
    navLinks.forEach(a => a.setAttribute('aria-current', String(a.dataset.nav === id)));
    top.classList.toggle('is-night', e.target.dataset.night === '1');
  }), { rootMargin: '-45% 0px -50% 0px' });
  $$('[data-nav]').forEach(s => s.matches('section') && io.observe(s));

  /* ---------- Motion (GSAP). Reduced motion: nothing self-running; scroll-linked motion stays. ---------- */
  if (!hasG) return;
  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();
  mm.add({ motion: '(prefers-reduced-motion: no-preference)', still: '(prefers-reduced-motion: reduce)' }, ctx => {
    const { motion } = ctx.conditions;
    const cleanups = [];
    if (motion) {
      // the one orchestrated moment: the book arrives, floats briefly (under 5 s), then rests
      gsap.from('h1 .ln>span', { yPercent: 110, duration: 1.1, stagger: .14, ease: 'expo.out', delay: .2 });
      gsap.from('.lede, .ask, .chips', { y: 18, duration: .8, stagger: .1, ease: 'expo.out', delay: .7 });
      gsap.from('.book-in', { y: -70, opacity: 0, duration: 1.1, ease: 'expo.out', delay: .5 });
      gsap.from('.book-tilt', { rotationY: -34, duration: 1.4, ease: 'expo.out', delay: .5 });
      // the cover lifts slightly, as if about to open, then settles: the scroll does the real opening
      gsap.fromTo('.book-tilt', { rotationX: 0 }, { rotationX: -6, duration: .55, ease: 'power2.inOut', delay: 1.6, yoyo: true, repeat: 1 });
      // the title strip drifts in once on arrival (4 s, then it follows the scroll)
      gsap.from('.ribbon-track', { x: 220, duration: 4, ease: 'power2.out' });
      gsap.to('.book-in', { y: -10, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3, delay: 1.7 });
      // shelf books arrive one at a time, once; hidden before the first paint of the shelf so they never blink
      gsap.set('.shelf .bk', { opacity: 0, y: 28, rotate: -1.5 });
      ScrollTrigger.batch('.shelf .bk', { start: 'top 92%', once: true,
        onEnter: els => gsap.to(els, { opacity: 1, y: 0, rotate: 0, duration: .6, stagger: .08, ease: 'power3.out', overwrite: true }) });
      const onFocus = e => { const bk = e.target.closest && e.target.closest('.shelf .bk'); if (bk) gsap.to(bk, { opacity: 1, y: 0, rotate: 0, duration: .2, overwrite: true }); };
      document.addEventListener('focusin', onFocus); cleanups.push(() => document.removeEventListener('focusin', onFocus));
      if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
        const tx = gsap.quickTo('.book-tilt', 'rotationY', { duration: .8, ease: 'power3.out' }), face = $('#hero-face'), hero = $('.hero');
        const onMove = e => { const k = e.clientX / innerWidth; face.style.setProperty('--sheen', (100 - k * 100) + '%'); tx((k - .5) * 10); };
        hero.addEventListener('pointermove', onMove); cleanups.push(() => hero.removeEventListener('pointermove', onMove));
      }
    }
    gsap.to('.ribbon-track', { xPercent: -45, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: () => '+=' + innerHeight * 1.6, scrub: .8 } });
    gsap.fromTo('.book3d', { rotateY: -30, rotateX: 7, rotateZ: -3 }, { rotateY: -8, rotateX: 2, rotateZ: 0, ease: 'none', immediateRender: false,
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .6 } });
    gsap.fromTo('#hero-face', { rotateY: 0, '--sheen': '100%' }, { rotateY: -42, '--sheen': '0%', ease: 'none', immediateRender: false,
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom 30%', scrub: .6, onUpdate: st => book.classList.toggle('is-open', st.progress > .02) } });
    gsap.fromTo('.glowline', { opacity: .82 }, { opacity: 1, ease: 'none', scrollTrigger: { trigger: '.threshold', start: 'top 80%', end: 'center center', scrub: true } });
    return () => cleanups.forEach(f => f());
  });
})();
