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
  const smooth = () => (calm() ? 'auto' : 'smooth');
  const bookBy = Object.fromEntries(D.books.map(b => [b.slug, b]));
  const toolBy = Object.fromEntries(D.tools.map(t => [t.slug, t]));

  /* ---------- v19 foundations: Still switch, sound (off until tapped), haptics, device tier ----------
     Still stops every self-running effect and every sound for this visit. Nothing is saved (no storage, no cookies). */
  const root = document.documentElement;
  let still = false, rebuild = () => {};
  const calm = () => reduce.matches || still;
  root.dataset.tier = (() => { try { const ok = !!document.createElement('canvas').getContext('webgl2'); return ok && (navigator.deviceMemory || 8) >= 4 && (navigator.hardwareConcurrency || 8) >= 4 ? 'high' : 'low'; } catch (e) { return 'low'; } })();

  // sound: synthesised in the page (no files), created only by a tap on the Sound switch (browser rule + homepage rule 5)
  const snd = (() => {
    let ac = null, out = null, on = false;
    const ensure = () => {
      if (!ac) { const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; ac = new AC(); out = ac.createGain(); out.gain.value = .55; out.connect(ac.destination); }
      if (ac.state === 'suspended') ac.resume(); return ac;
    };
    const tone = (f, dur, type = 'sine', vol = .15, to) => {
      const t = ac.currentTime, o = ac.createOscillator(), g = ac.createGain();
      o.type = type; o.frequency.setValueAtTime(f, t); if (to) o.frequency.exponentialRampToValueAtTime(to, t + dur);
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + .006); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
      o.connect(g).connect(out); o.start(t); o.stop(t + dur + .02);
    };
    const noise = (dur, f, q, vol, sweep) => {
      const t = ac.currentTime, len = Math.ceil(ac.sampleRate * dur), b = ac.createBuffer(1, len, ac.sampleRate), d = b.getChannelData(0);
      for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
      const src = ac.createBufferSource(), bp = ac.createBiquadFilter(), g = ac.createGain();
      src.buffer = b; bp.type = 'bandpass'; bp.frequency.setValueAtTime(f, t); if (sweep) bp.frequency.exponentialRampToValueAtTime(sweep, t + dur); bp.Q.value = q;
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + dur * .2); g.gain.exponentialRampToValueAtTime(.0001, t + dur);
      src.connect(bp).connect(g).connect(out); src.start(t);
    };
    const kit = {
      tick: () => tone(2200, .035, 'triangle', .05),
      press: () => { tone(140, .14, 'sine', .3, 55); noise(.05, 900, 1.2, .08); },
      page: () => noise(.22, 3200, .8, .09, 1400),
      door: () => { noise(.7, 260, .6, .12, 520); tone(70, .6, 'sine', .08, 90); },
      full: () => tone(1320, .09, 'sine', .07),
      chime: () => { tone(660, 1.6, 'sine', .07); tone(990, 1.9, 'sine', .035); tone(1485, 2.2, 'sine', .015); }
    };
    return {
      get on() { return on; },
      set(v) { on = v && !still; if (on) ensure(); else if (ac) ac.suspend(); },
      play(name) { if (!on || still || !ac) return; try { kit[name](); } catch (e) {} },
      // a held tone that rises with the charge; returns a handle the Portals drive
      hum() {
        if (!on || still || !ac) return { set() {}, stop() {} };
        const t = ac.currentTime, o = ac.createOscillator(), o2 = ac.createOscillator(), g = ac.createGain();
        o.type = 'sine'; o2.type = 'triangle'; o.frequency.value = 110; o2.frequency.value = 220.7;
        g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(.06, t + .08);
        o.connect(g); o2.connect(g); g.connect(out); o.start(); o2.start();
        return {
          set(p) { const n = ac.currentTime; o.frequency.setTargetAtTime(110 + p * 330, n, .05); o2.frequency.setTargetAtTime(220.7 + p * 660, n, .05); g.gain.setTargetAtTime(.04 + p * .05, n, .05); },
          stop() { const n = ac.currentTime; g.gain.setTargetAtTime(0, n, .06); o.stop(n + .4); o2.stop(n + .4); }
        };
      },
      kill() { on = false; try { if (ac) ac.close(); } catch (e) {} ac = null; }
    };
  })();

  // haptics: Android/Chrome vibrate; iPhone has no vibration API, so a hidden native switch gives one system tick on a real tap
  const isIOS = /iP(hone|ad|od)/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  let tickLabel = null;
  const buzz = (p = 8) => {
    if (still) return;
    if ('vibrate' in navigator) { try { navigator.vibrate(p); } catch (e) {} return; }
    if (!isIOS) return;
    if (!tickLabel) {
      tickLabel = document.createElement('label'); tickLabel.setAttribute('aria-hidden', 'true');
      tickLabel.style.cssText = 'position:fixed;left:-9999px;top:0;width:1px;height:1px;overflow:hidden;opacity:0;pointer-events:none';
      const i = document.createElement('input'); i.type = 'checkbox'; i.setAttribute('switch', ''); i.tabIndex = -1; tickLabel.appendChild(i); document.body.appendChild(tickLabel);
    }
    const had = document.activeElement; tickLabel.click(); if (had && had.focus) had.focus({ preventScroll: true });
  };

  { const h = new Date().getHours(); if (h >= 21 || h < 6) root.classList.add('after-dark'); }
  // chips: a hidden copy of the label rolls in on hover (aria-hidden, so the name is read once)
  $$('.chip').forEach(c => { const t = c.textContent; c.innerHTML = `<span class="rl"><span>${t}</span><span aria-hidden="true">${t}</span></span>`; });
  const stillBtns = $$('#still-btn, #sheet-still'), soundBtns = $$('#sound-btn, #sheet-sound');
  const showSound = () => soundBtns.forEach(b => b.setAttribute('aria-pressed', String(snd.on)));
  soundBtns.forEach(b => b.addEventListener('click', () => { if (still && !snd.on) setStill(false); snd.set(!snd.on); showSound(); snd.play('tick'); buzz(6); }));
  const setStill = v => {
    still = v; stillBtns.forEach(b => b.setAttribute('aria-pressed', String(v))); root.classList.toggle('is-still', v);
    if (v) { snd.set(false); showSound(); }
    rebuild();
  };
  stillBtns.forEach(b => b.addEventListener('click', () => { buzz(6); setStill(!still); }));
  // any tap on a real control gets a quiet tick (sound only when Sound is on)
  document.addEventListener('click', e => { if (e.target.closest('.chip, .btn, .pick, .bk a, .tool, .nav a, .menu-btn, .redo, .door-btn, .card a')) snd.play('tick'); });

  /* ---------- Leave: one tap (or Esc twice) to a neutral page, replacing this one in history ---------- */
  const leave = () => { try { snd.kill(); if (window.gsap) gsap.globalTimeline.pause(); } catch (e) {} try { document.body.style.visibility = 'hidden'; } catch (e) {} location.replace('https://www.google.com/search?q=weather'); };
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
  const reveal = () => { const first = $('#result-grid .pick'); if (!first) return; const over = first.getBoundingClientRect().bottom + 24 - innerHeight; if (over > 0) scrollBy({ top: Math.min(over, Math.round(innerHeight * .46)), behavior: smooth() }); };
  const swapCover = (src, alt, ar, done) => {
    if (heroImg.getAttribute('src') === src) { done(); return; }
    if (!hasG || calm()) { book.style.setProperty('--ar', ar); heroImg.src = src; heroImg.alt = alt; done(); return; }
    if (turnT) turnT.progress(1).kill();
    const pages = $$('.riffle i', book);
    turnT = gsap.timeline({ onComplete: () => { book.classList.remove('is-turning'); gsap.set(pages, { rotateY: 0 }); done(); } })
      .add(() => { book.classList.add('is-turning'); snd.play('page'); buzz(6); })
      .to(leaf, { rotateY: -100, duration: .3, ease: 'power2.in' })
      .fromTo(pages, { rotateY: 0, z: .5 }, { rotateY: -178, duration: .34, stagger: .055, ease: 'power1.inOut' }, '-=.05')
      .add(() => { book.style.setProperty('--ar', ar); heroImg.src = src; heroImg.alt = alt; snd.play('page'); }, '-=.12')
      .to(leaf, { rotateY: 0, duration: .5, ease: 'back.out(1.3)' }, '-=.08');
  };
  // the answer heading decodes from press type into the words (about 0.5 s)
  const GLYPHS = 'abcdefghijklmnopqrstuvwxyz§¶†‡';
  let scrT;
  const scramble = (el, text) => {
    clearInterval(scrT); let f = 0; const n = 14;
    scrT = setInterval(() => {
      f++; const k = Math.floor(text.length * f / n);
      el.innerHTML = text.slice(0, k) + '<span class="sc" aria-hidden="true">' + [...text.slice(k)].map(ch => ch === ' ' ? ' ' : GLYPHS[Math.floor(Math.random() * GLYPHS.length)]).join('') + '</span>';
      if (f >= n) { clearInterval(scrT); el.textContent = text; }
    }, 36);
  };
  const setOpen = open => { result.toggleAttribute('data-open', open); result.inert = !open; };
  setOpen(false);
  $$('.chip').forEach(chip => chip.addEventListener('click', () => {
    const s = D.situations.find(x => x.id === chip.dataset.s);
    $$('.chip').forEach(c => c.setAttribute('aria-pressed', String(c === chip))); buzz(8);
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
    if (hasG && !calm()) {
      const br = book.getBoundingClientRect(), bx = br.left + br.width / 2, by = br.top + br.height / 2;
      $$('#result-grid .pick').forEach((pk, i) => {
        const r = pk.getBoundingClientRect();
        gsap.from(pk, { x: bx - (r.left + r.width / 2), y: by - (r.top + r.height / 2), rotation: -10 + i * 7, scale: .35, opacity: 0, duration: .75, delay: .18 + i * .09, ease: 'expo.out', clearProps: 'all' });
      });
      scramble($('#result-title'), `For “${s.label.toLowerCase()}”`);
    }
    swapCover(a.imgLg, a.title + ', cover', a.w + '/' + a.h, () => setTimeout(reveal, calm() ? 0 : 120));
  }));
  $$('.chip').forEach(c => c.addEventListener('pointerdown', e => {
    if (calm() || !hasG) return;
    const r = c.getBoundingClientRect(), ring = document.createElement('span');
    ring.className = 'seal'; ring.style.left = (e.clientX - r.left) + 'px'; ring.style.top = (e.clientY - r.top) + 'px'; c.appendChild(ring);
    gsap.fromTo(ring, { scale: .2, opacity: 1 }, { scale: Math.max(r.width, r.height) / 6, opacity: 0, duration: .6, ease: 'power2.out', onComplete: () => ring.remove() });
  }));
  $('#redo').addEventListener('click', () => { const c = $('.chip[aria-pressed="true"]') || $('.chip'); $('#ask').scrollIntoView({ behavior: smooth(), block: 'center' }); c.focus({ preventScroll: true }); });

  /* ---------- The bigger picture door ---------- */
  const door = $('#door'), doorBtn = $('#door-btn');
  const doorLbl = $('.lbl', doorBtn), leafs = $('.leafs', door);
  let holdT = null, held = false, fromPointer = false;
  const swing = () => {
    if (!hasG || calm()) return;
    leafs.style.height = $('.door-head', door).offsetHeight + 'px'; leafs.classList.add('is-on');
    gsap.timeline({ onComplete: () => { leafs.classList.remove('is-on'); gsap.set('.door-l, .door-r, .door .burst', { clearProps: 'all' }); leafs.style.height = ''; } })
      .fromTo('.door .burst', { opacity: 0, scaleX: 1 }, { opacity: 1, scaleX: 3, duration: .25, ease: 'power2.out' })
      .to('.door-l', { rotateY: -96, duration: 1.15, ease: 'power2.inOut' }, .15)
      .to('.door-r', { rotateY: 96, duration: 1.15, ease: 'power2.inOut' }, .15)
      .to('.door .burst', { scaleX: 60, opacity: 0, duration: 1, ease: 'power2.out' }, .45);
  };
  const toggleDoor = () => {
    const open = !door.hasAttribute('data-open'); snd.play('door'); buzz(open ? [10, 40, 16] : 8);
    if (open) swing();
    door.toggleAttribute('data-open', open);
    doorBtn.setAttribute('aria-expanded', String(open));
    doorLbl.textContent = open ? 'Close the bigger picture' : 'Open the bigger picture';
    $('#door-body').inert = !open;
    if (hasG && !calm()) gsap.to('.spines i', { rotate: open ? -14 : 0, opacity: open ? .35 : 1, duration: .45, stagger: .06, ease: 'power2.out' });
    if (open && hasG && !calm()) gsap.from('#door-body .bk', { y: 24, rotate: -2, opacity: 0, duration: .55, stagger: .09, ease: 'power3.out', delay: .4, clearProps: 'all' });
  };
  const HOLD_S = .7;
  doorBtn.addEventListener('pointerdown', e => {
    if (e.button > 0) return; fromPointer = true;
    if (door.hasAttribute('data-open')) return;   // closing is a plain tap
    held = false; doorLbl.textContent = 'Keep holding';
    const v = { h: 0 };
    holdT = (hasG ? gsap.to(v, { h: 1, duration: HOLD_S, ease: 'none', onUpdate: () => doorBtn.style.setProperty('--h', v.h), onComplete: () => { held = true; doorBtn.style.setProperty('--h', 0); toggleDoor(); } }) : null);
    if (!hasG) { held = true; toggleDoor(); }
    buzz(5);
  });
  const endHold = () => {
    if (holdT && !held) { holdT.kill(); doorBtn.style.setProperty('--h', 0); if (!door.hasAttribute('data-open')) doorLbl.textContent = 'Open the bigger picture'; }
    holdT = null;
  };
  doorBtn.addEventListener('pointerup', endHold); doorBtn.addEventListener('pointerleave', endHold); doorBtn.addEventListener('pointercancel', endHold);
  doorBtn.addEventListener('click', () => {
    // a click that followed a pointer press was handled by the hold; keyboard and screen readers open straight away
    if (fromPointer) { fromPointer = false; if (door.hasAttribute('data-open') && !held) toggleDoor(); held = false; return; }
    toggleDoor();
  });
  $$('.shelf .books').forEach(ul => ul.addEventListener('scrollend', () => { if (ul.scrollWidth > ul.clientWidth + 4) { buzz(4); snd.play('tick'); } }));

  /* ---------- Portals: strontium charges in light, then glows and fades in the dark ----------
     v19: the glow is painted. Where the light touched is where it glows: a small charge map masks the night photo on a canvas,
     and the canvas fades with the afterglow curve. Under Still / reduced motion the whole photo simply glows (the v18 behaviour). */
  const CHARGE_S = 1.2, GLOW_S = 7;   // hold ~1.2 s to charge fully; the afterglow fades over ~7 s, fast at first then slow, like the real thing
  const veil = document.createElement('div'); veil.className = 'veil'; veil.setAttribute('aria-hidden', 'true'); document.body.appendChild(veil);
  let lightsOffDone = false;
  // the first full charge of the visit: the rest of the page goes dark for a moment so the pendant glows alone (Leave now stays above it)
  const lightsOff = li => {
    if (lightsOffDone || calm() || !hasG) return; lightsOffDone = true;
    li.classList.add('is-raised');
    gsap.timeline({ onComplete: () => li.classList.remove('is-raised') })
      .to(veil, { opacity: .93, duration: .6, ease: 'power2.out' })
      .to(veil, { opacity: 0, duration: 1.4, ease: 'power2.inOut' }, '+=2.2');
  };
  const DPR = Math.min(2, devicePixelRatio || 1);
  $$('.portal').forEach(fig => {
    const li = fig.parentElement, night = $('.night', fig), day = $('.day', fig), btn = $('.charge', li), label = $('.label', btn), live = $('.portal-status', li), name = fig.dataset.name;
    const v = { c: 0, g: 0 }; let chargeT, glowT, held = false, hum = null, buzzT = 0, trickle = false;
    // layers: the painted glow, the afterglow trail, a moving glint
    const mk = (tag, cls) => { const e = document.createElement(tag); e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; };
    const cv = mk('canvas', 'glowpaint'), tr = mk('canvas', 'trail'), glint = mk('span', 'glint');
    fig.insertBefore(cv, $('.lamp', fig)); fig.appendChild(tr); fig.appendChild(glint);
    const gx = cv.getContext('2d'), tx = tr.getContext('2d');
    const map = document.createElement('canvas'); map.width = map.height = 96; const mx = map.getContext('2d');
    let S = 0, px = .5, py = .5, brushR = .2, parts = [], trRaf = 0;
    const sizeCv = () => { const w = Math.round(fig.clientWidth * DPR); if (w && w !== S) { S = w; cv.width = cv.height = tr.width = tr.height = w; } };
    const painted = () => !calm() && night.complete && night.naturalWidth > 0;
    const paintAt = (x, y, r, a) => { const g = mx.createRadialGradient(x * 96, y * 96, 0, x * 96, y * 96, Math.max(1, r * 96)); g.addColorStop(0, `rgba(255,255,255,${a})`); g.addColorStop(1, 'rgba(255,255,255,0)'); mx.fillStyle = g; mx.fillRect(0, 0, 96, 96); };
    const redraw = () => {
      sizeCv(); gx.globalCompositeOperation = 'source-over'; gx.clearRect(0, 0, S, S);
      if (!painted()) return;
      gx.drawImage(night, 0, 0, S, S); gx.globalCompositeOperation = 'destination-in'; gx.drawImage(map, 0, 0, S, S);
    };
    const clearMap = () => { mx.clearRect(0, 0, 96, 96); redraw(); };
    const paint = () => {
      const c = v.c.toFixed(3); fig.style.setProperty('--c', c); btn.style.setProperty('--c', c);
      if (painted()) { cv.style.opacity = v.g; night.style.opacity = 0; } else { night.style.opacity = v.g; cv.style.opacity = 0; }
      day.style.opacity = 1 - v.g * .92; glint.style.opacity = (v.g * .55).toFixed(3);
    };
    const rest = () => { fig.classList.remove('is-glowing', 'is-charging'); label.textContent = 'Hold to charge'; };
    // while held, the light spreads out from the finger and soaks in
    const soak = () => { if (!held) return; brushR = Math.min(.8, brushR + .012); paintAt(px, py, brushR, .16); redraw(); requestAnimationFrame(soak); };
    const decay = (peak, len, done) => {
      if (glowT) glowT.kill();
      glowT = gsap.timeline()
        .to(v, { g: peak, duration: .35, ease: 'power2.out', onUpdate: paint })
        .to(v, { c: 0, duration: .5, ease: 'power2.out', onUpdate: paint }, 0)
        .to(v, { g: 0, duration: len, ease: 'power1.out', onUpdate: paint, onComplete: () => { rest(); live.textContent = ''; clearMap(); if (done) done(); } });
    };
    const glow = () => {
      if (!held) return; held = false; if (hum) { hum.stop(); hum = null; } clearTimeout(buzzT);
      if (chargeT) chargeT.kill(); fig.classList.remove('is-charging');
      if (v.c < .05) { v.c = 0; v.g = 0; paint(); rest(); clearMap(); return; }
      fig.classList.add('is-glowing'); label.textContent = 'Glowing'; snd.play('chime');
      live.textContent = `${name} is glowing in the dark.`;
      if (!hasG || calm()) { v.g = 1; v.c = 0; paint(); return; }   // reduced motion: it simply glows until charged again
      const full = v.c > .97;
      decay(Math.min(1, .35 + v.c), GLOW_S * Math.max(.4, v.c));
      if (full) lightsOff(li);
    };
    const charge = () => {
      if (held) return; held = true; trickle = false;
      if (glowT) glowT.kill(); fig.classList.add('is-charging'); label.textContent = 'Charging';
      hum = snd.hum(); buzz(6);
      // Android: a pulse that quickens as the charge rises (iPhone gets one tick at the start and one at full)
      if ('vibrate' in navigator && !still) { let gap = 220; const pulse = () => { buzz(6); gap = Math.max(60, gap * .8); buzzT = setTimeout(pulse, gap); }; buzzT = setTimeout(pulse, gap); }
      if (!hasG || calm()) { v.c = 1; v.g = 0; mx.fillStyle = '#fff'; mx.fillRect(0, 0, 96, 96); paint(); return; }
      if (v.g > 0) gsap.to(v, { g: 0, duration: .25, ease: 'power2.out', onUpdate: paint });   // from glowing back to the light, no snap
      brushR = .2; requestAnimationFrame(soak);
      chargeT = gsap.to(v, { c: 1, duration: CHARGE_S * (1 - v.c), ease: 'none', onUpdate: () => { paint(); if (hum) hum.set(v.c); }, onComplete: () => { clearTimeout(buzzT); buzz(18); snd.play('full'); } });
    };
    const at = e => { const r = fig.getBoundingClientRect(); px = gsap.utils.clamp(0, 1, (e.clientX - r.left) / r.width); py = gsap.utils.clamp(0, 1, (e.clientY - r.top) / r.height); fig.style.setProperty('--lx', px * 100 + '%'); fig.style.setProperty('--ly', py * 100 + '%'); };
    // afterglow trail: moving over a glowing pendant sheds a few sparks of light
    const sparks = () => {
      trRaf = 0; sizeCv(); tx.clearRect(0, 0, S, S); tx.globalCompositeOperation = 'lighter';
      parts = parts.filter(q => (q.life -= 1 / 60) > 0);
      for (const q of parts) { q.x += q.vx; q.y += q.vy; q.vy -= .00012; const a = q.life * q.life; tx.fillStyle = `rgba(180,255,236,${(a * .9).toFixed(3)})`; tx.beginPath(); tx.arc(q.x * S, q.y * S, q.r * DPR * (1 + (1 - q.life)), 0, 6.283); tx.fill(); }
      if (parts.length) trRaf = requestAnimationFrame(sparks);
    };
    const shed = () => {
      if (calm() || v.g < .15 || parts.length > 80) return;
      for (let i = 0; i < 2; i++) parts.push({ x: px, y: py, vx: (Math.random() - .5) * .006, vy: (Math.random() - .5) * .006, r: .8 + Math.random() * 1.6, life: .7 + Math.random() * .5 });
      if (!trRaf) trRaf = requestAnimationFrame(sparks);
    };
    [fig, btn].forEach(el => {
      el.addEventListener('pointerdown', e => {
        if (e.button > 0) return;
        if (el === fig) at(e); else { px = py = .5; fig.style.setProperty('--lx', '50%'); fig.style.setProperty('--ly', '50%'); }
        try { el.setPointerCapture(e.pointerId); } catch (x) {}
        charge();
      });
      el.addEventListener('pointerup', glow);
      el.addEventListener('pointercancel', glow);
      el.addEventListener('contextmenu', e => e.preventDefault());
    });
    const fine = matchMedia('(hover: hover) and (pointer: fine)');
    fig.addEventListener('pointermove', e => {
      at(e); fig.style.setProperty('--gx', px * 100 + '%'); fig.style.setProperty('--gy', py * 100 + '%');
      shed();
      // the UV lamp: just passing over a pendant charges it a little where the light falls
      if (!held && fine.matches && !calm() && v.g < .05) { paintAt(px, py, .14, .06); redraw(); trickle = true; }
    });
    fig.addEventListener('pointerleave', () => { if (trickle && !held && v.g < .05 && !calm() && hasG) { trickle = false; fig.classList.add('is-glowing'); decay(.5, GLOW_S * .55); } });
    // keyboard: hold Space or Enter to charge, let go to glow
    btn.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); px = py = .5; fig.style.setProperty('--lx', '50%'); fig.style.setProperty('--ly', '50%'); charge(); } });
    btn.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); glow(); } });
    btn.addEventListener('blur', glow);
    new ResizeObserver(() => { sizeCv(); redraw(); }).observe(fig);
    paint();
  });
  // phones that allow it without asking (Android): tilting the phone moves the glint across every glowing pendant
  if ('DeviceOrientationEvent' in window && typeof DeviceOrientationEvent.requestPermission !== 'function' && !matchMedia('(pointer: fine)').matches) {
    const portals = $$('.portal');
    addEventListener('deviceorientation', e => { if (e.gamma == null || calm()) return; const x = 50 + gsap.utils.clamp(-40, 40, e.gamma * 1.4), y = 50 + gsap.utils.clamp(-40, 40, (e.beta - 45) * 1.2); portals.forEach(f => { f.style.setProperty('--gx', x + '%'); f.style.setProperty('--gy', y + '%'); }); });
  }
  // the UV lamp follows the pointer through the dark Workshop (desktop)
  if (matchMedia('(hover: hover) and (pointer: fine)').matches && hasG) {
    const uv = document.createElement('div'); uv.className = 'uv'; uv.setAttribute('aria-hidden', 'true'); document.body.appendChild(uv);
    const ux = gsap.quickTo(uv, 'x', { duration: .35, ease: 'power3.out' }), uy = gsap.quickTo(uv, 'y', { duration: .35, ease: 'power3.out' });
    const wk = $('.workshop');
    wk.addEventListener('pointerenter', () => uv.classList.add('is-on'));
    wk.addEventListener('pointerleave', () => uv.classList.remove('is-on'));
    wk.addEventListener('pointermove', e => { ux(e.clientX); uy(e.clientY); });
  }

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
  const navLinks = $$('.nav a'); const top = $('.top'), pill = $('.nav .pill');
  const movePill = () => {
    const a = $('.nav a[aria-current="true"]'); if (!a || !pill || !a.offsetParent) { if (pill) pill.style.opacity = 0; return; }
    $('.nav').classList.add('has-pill');
    const to = { x: a.offsetLeft, width: a.offsetWidth, opacity: 1 };
    if (hasG && !calm() && pill.style.opacity === '1') gsap.to(pill, { ...to, duration: .45, ease: 'expo.out', overwrite: true }); else { gsap ? gsap.set(pill, to) : 0; pill.style.opacity = 1; }
  };
  addEventListener('resize', () => { const a = $('.nav a[aria-current="true"]'); if (a && pill && hasG) gsap.set(pill, { x: a.offsetLeft, width: a.offsetWidth }); });
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    const id = e.target.dataset.nav;
    navLinks.forEach(a => a.setAttribute('aria-current', String(a.dataset.nav === id)));
    movePill();
    top.classList.toggle('is-night', e.target.dataset.night === '1');
  }), { rootMargin: '-45% 0px -50% 0px' });
  $$('[data-nav]').forEach(s => s.matches('section') && io.observe(s));

  /* ---------- Hero helpers (called inside the motion build; each returns its cleanup) ---------- */
  const stage = $('.stage');
  function dust() {
    const cv = document.createElement('canvas'); cv.className = 'dust'; cv.setAttribute('aria-hidden', 'true'); stage.prepend(cv);
    const g = cv.getContext('2d'), dpr = Math.min(2, devicePixelRatio || 1);
    let W = 0, H = 0, raf = 0, on = true, t = 0;
    const N = root.dataset.tier === 'high' ? 46 : 22, motes = [];
    const cap = $('figcaption', stage);
    const size = () => { const r = stage.getBoundingClientRect(), ch = cap && cap.offsetParent ? cap.offsetHeight + 16 : 0; if (Math.round(r.width) === W && Math.round(r.height - ch) === H) return; W = Math.round(r.width); H = Math.round(r.height - ch); cv.width = W * dpr; cv.height = H * dpr; cv.style.width = W + 'px'; cv.style.height = H + 'px'; };
    size();
    for (let i = 0; i < N; i++) motes.push({ x: Math.random(), y: Math.random(), r: .5 + Math.random() * 1.4, v: .00025 + Math.random() * .0006, ph: Math.random() * 6.28, a: .15 + Math.random() * .45 });
    const glow = root.classList.contains('after-dark') ? '134,236,210' : '231,199,125';
    const draw = () => {
      raf = requestAnimationFrame(draw); if (!on) return; t += 1;
      g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
      for (const m of motes) {
        m.y -= m.v; if (m.y < -.05) { m.y = 1.05; m.x = Math.random(); }
        const x = (m.x + Math.sin(t * .006 + m.ph) * .02) * W, y = m.y * H;
        const d = Math.hypot(x / W - .5, y / H - .45), lit = Math.max(0, 1 - d * 1.9);   // brighter inside the lamp's circle
        g.fillStyle = `rgba(${glow},${(m.a * (.25 + lit)).toFixed(3)})`; g.beginPath(); g.arc(x, y, m.r, 0, 6.283); g.fill();
      }
    };
    const io = new IntersectionObserver(([e]) => { on = e.isIntersecting && !document.hidden; }); io.observe(stage);
    const vis = () => { on = !document.hidden; }; document.addEventListener('visibilitychange', vis);
    const ro = new ResizeObserver(size); ro.observe(stage);
    draw();
    return () => { cancelAnimationFrame(raf); io.disconnect(); ro.disconnect(); document.removeEventListener('visibilitychange', vis); cv.remove(); };
  }
  function peek() {
    let x0 = null, w = 1, id = null, maxed = false;
    const ry = gsap.quickTo(leaf, 'rotateY', { duration: .25, ease: 'power3.out' });
    const down = e => { if ((turnT && turnT.isActive()) || e.button > 0) return; x0 = e.clientX; w = book.getBoundingClientRect().width; id = e.pointerId; maxed = false; book.classList.add('is-peek'); gsap.killTweensOf(leaf); };
    const move = e => { if (x0 === null || e.pointerId !== id) return; const a = gsap.utils.clamp(-80, 0, (e.clientX - x0) / w * 110); if (a < -20) { try { book.setPointerCapture(id); } catch (x) {} } ry(a); if (a <= -79 && !maxed) { maxed = true; buzz(10); snd.play('page'); } };
    const up = () => { if (x0 === null) return; x0 = null; gsap.to(leaf, { rotateY: 0, duration: .9, ease: 'elastic.out(1,.55)', overwrite: true, onComplete: () => book.classList.remove('is-peek') }); };
    book.addEventListener('pointerdown', down); book.addEventListener('pointermove', move); book.addEventListener('pointerup', up); book.addEventListener('pointercancel', up); book.addEventListener('lostpointercapture', up);
    return () => { ['pointerdown', 'pointermove', 'pointerup', 'pointercancel', 'lostpointercapture'].forEach((ev, i) => book.removeEventListener(ev, [down, move, up, up, up][i])); gsap.set(leaf, { rotateY: 0 }); book.classList.remove('is-peek'); };
  }

  /* ---------- Motion (GSAP). Reduced motion: nothing self-running; scroll-linked motion stays. ---------- */
  if (!hasG) return;
  gsap.registerPlugin(ScrollTrigger, SplitText, DrawSVGPlugin);
  let mm = gsap.matchMedia(), firstBuild = true;
  const build = () => mm.add({ motion: '(prefers-reduced-motion: no-preference)', still: '(prefers-reduced-motion: reduce)' }, ctx => {
    const motion = ctx.conditions.motion && !still, entrance = motion && firstBuild;
    const cleanups = [];
    if (entrance) {
      // the headline is set letter by letter like wet ink: each letter rises into its line and dries from brass to paper
      const h1 = $('h1'), lns = $$('h1 .ln');
      h1.setAttribute('aria-label', h1.textContent.replace(/\s+/g, ' ').trim()); lns.forEach(l => l.setAttribute('aria-hidden', 'true'));
      const hs = SplitText.create('h1 .ln>span', { type: 'words,chars', aria: 'none' });
      const unsplit = () => { hs.revert(); h1.removeAttribute('aria-label'); lns.forEach(l => l.removeAttribute('aria-hidden')); };
      cleanups.push(unsplit);
      gsap.timeline({ delay: .15, onComplete: unsplit })
        .from(hs.chars, { yPercent: 115, duration: .9, stagger: .022, ease: 'expo.out' })
        .from(hs.chars, { color: '#e7c77d', duration: 1.3, stagger: .022, ease: 'power1.in' }, .25);
      gsap.from('.lede, .ask, .chips', { y: 18, duration: .8, stagger: .1, ease: 'expo.out', delay: .7 });
      gsap.from('.book-in', { y: -70, opacity: 0, duration: 1.1, ease: 'expo.out', delay: .5 });
      gsap.from('.book-tilt', { rotationY: -34, duration: 1.4, ease: 'expo.out', delay: .5 });
      // the cover lifts slightly, as if about to open, then settles: the scroll does the real opening
      gsap.fromTo('.book-tilt', { rotationX: 0 }, { rotationX: -6, duration: .55, ease: 'power2.inOut', delay: 1.6, yoyo: true, repeat: 1 });
      // the title strip drifts in once on arrival (4 s, then it follows the scroll)
      gsap.from('.ribbon-track', { x: 220, duration: 4, ease: 'power2.out' });
      gsap.to('.book-in', { y: -10, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3, delay: 1.7 });
      // the shadow on the floor tightens as the book rises, and comes in with it
      gsap.from('.floor', { opacity: 0, scale: .4, duration: 1.1, ease: 'expo.out', delay: .5 });
      gsap.to('.floor', { scale: .82, opacity: .65, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3, delay: 1.7 });
      // shelf books arrive one at a time, once; hidden before the first paint of the shelf so they never blink
      gsap.set('.shelf .bk', { opacity: 0, y: 28, rotate: -1.5 });
      ScrollTrigger.batch('.shelf .bk', { start: 'top 92%', once: true,
        onEnter: els => { gsap.to(els, { opacity: 1, y: 0, rotate: 0, duration: .6, stagger: .08, ease: 'power3.out', overwrite: true });
          gsap.fromTo(els.map(e => $('.glint', e)), { xPercent: -130 }, { xPercent: 130, duration: 1.1, stagger: .08, ease: 'power2.inOut', delay: .35 }); } });
    }
    if (entrance) {
      const onFocus = e => { const bk = e.target.closest && e.target.closest('.shelf .bk'); if (bk) gsap.to(bk, { opacity: 1, y: 0, rotate: 0, duration: .2, overwrite: true }); };
      document.addEventListener('focusin', onFocus); cleanups.push(() => document.removeEventListener('focusin', onFocus));
    }
    if (motion) {
      const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
      // the title strip leans with scroll speed
      const sk = gsap.quickTo('.ribbon-track', 'skewX', { duration: .5, ease: 'power3.out' });
      ScrollTrigger.create({ trigger: document.body, start: 'top top', end: 'bottom bottom', onUpdate: st => sk(gsap.utils.clamp(-8, 8, st.getVelocity() / -300)) });
      // the light under the door breathes three times when it comes into view
      ScrollTrigger.create({ trigger: '#door', start: 'top 80%', once: true, onEnter: () => gsap.fromTo('.door .seam', { opacity: .35 }, { opacity: 1, duration: 1.2, yoyo: true, repeat: 5, ease: 'sine.inOut' }) });
      // the decoder scans its page once when it arrives, and again on hover
      const scan = () => gsap.fromTo('.tool .scan', { top: '0%', opacity: 1 }, { top: '100%', duration: 1.1, ease: 'power1.inOut', onComplete: () => gsap.set('.tool .scan', { opacity: 0 }) });
      ScrollTrigger.create({ trigger: '.tool-playbook', start: 'top 80%', once: true, onEnter: scan });
      const tp = $('.tool-playbook'); if (tp && fine) { tp.addEventListener('pointerenter', scan); cleanups.push(() => tp.removeEventListener('pointerenter', scan)); }
      if (fine) {
        // shelf spotlight + covers turn toward the pointer
        $$('.shelf').forEach(sh => {
          const covs = $$('.cov', sh);
          const mv = e => { const r = sh.getBoundingClientRect(); sh.style.setProperty('--sx', (e.clientX - r.left) + 'px'); sh.style.setProperty('--sy', (e.clientY - r.top) + 'px');
            covs.forEach(c => { const cr = c.getBoundingClientRect(); const k = gsap.utils.clamp(-1, 1, (e.clientX - (cr.left + cr.width / 2)) / 400); c.style.setProperty('--ty', (k * 10).toFixed(2) + 'deg'); }); };
          const lv = () => { sh.style.removeProperty('--sx'); sh.style.removeProperty('--sy'); covs.forEach(c => c.style.removeProperty('--ty')); };
          sh.addEventListener('pointermove', mv); sh.addEventListener('pointerleave', lv);
          cleanups.push(() => { sh.removeEventListener('pointermove', mv); sh.removeEventListener('pointerleave', lv); lv(); });
        });
        // tool cards tilt with a glare that follows the pointer
        $$('.tool').forEach(t => {
          const mv = e => { const r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
            t.style.setProperty('--ry', ((x - .5) * 6).toFixed(2) + 'deg'); t.style.setProperty('--rx', ((.5 - y) * 6).toFixed(2) + 'deg'); t.style.setProperty('--gx', (x * 100) + '%'); t.style.setProperty('--gy', (y * 100) + '%'); };
          const lv = () => ['--rx', '--ry'].forEach(k => t.style.removeProperty(k));
          t.addEventListener('pointermove', mv); t.addEventListener('pointerleave', lv);
          cleanups.push(() => { t.removeEventListener('pointermove', mv); t.removeEventListener('pointerleave', lv); lv(); });
        });
      }
      // dust in the lamplight around the book (canvas sized in pixels from the stage box; pauses off-screen and under Still)
      cleanups.push(dust());
      // drag the cover open by hand (mouse or a sideways swipe); it springs shut when let go
      cleanups.push(peek());
      if (fine) {
        // chips lean toward the pointer
        $$('.chip').forEach(c => {
          const mx = gsap.quickTo(c, '--mx', { duration: .4, ease: 'power3.out', unit: 'px' }), my = gsap.quickTo(c, '--my', { duration: .4, ease: 'power3.out', unit: 'px' });
          const mv = e => { const r = c.getBoundingClientRect(); mx((e.clientX - r.left - r.width / 2) * .22); my((e.clientY - r.top - r.height / 2) * .3); };
          const lv = () => { mx(0); my(0); };
          c.addEventListener('pointermove', mv); c.addEventListener('pointerleave', lv);
          cleanups.push(() => { c.removeEventListener('pointermove', mv); c.removeEventListener('pointerleave', lv); c.style.removeProperty('--mx'); c.style.removeProperty('--my'); });
        });
      } else if ('DeviceOrientationEvent' in window && typeof DeviceOrientationEvent.requestPermission !== 'function') {
        // phones that allow it without asking (Android): tilting the phone tilts the book
        const gy = gsap.quickTo('.book-tilt', 'rotationY', { duration: .9, ease: 'power3.out' }), gx = gsap.quickTo('.book-tilt', 'rotationX', { duration: .9, ease: 'power3.out' });
        let live = false; const t0 = setTimeout(() => { live = true; }, 3000);
        const or = e => { if (!live || e.gamma == null) return; gy(gsap.utils.clamp(-14, 14, e.gamma * .5)); gx(gsap.utils.clamp(-8, 8, (e.beta - 45) * -.2)); };
        addEventListener('deviceorientation', or);
        cleanups.push(() => { clearTimeout(t0); removeEventListener('deviceorientation', or); });
      }
      if (fine) {
        const tx = gsap.quickTo('.book-tilt', 'rotationY', { duration: .8, ease: 'power3.out' }), face = $('#hero-face'), hero = $('.hero');
        const fx = gsap.quickTo('.floor', 'x', { duration: .8, ease: 'power3.out' });
        const onMove = e => { const k = e.clientX / innerWidth; face.style.setProperty('--sheen', (100 - k * 100) + '%'); tx((k - .5) * 10); fx((k - .5) * -24); };
        hero.addEventListener('pointermove', onMove); cleanups.push(() => hero.removeEventListener('pointermove', onMove));
      }
    }
    gsap.fromTo('.progress i', { scaleX: 0 }, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: document.documentElement, start: 'top top', end: 'bottom bottom', scrub: .3 } });
    ScrollTrigger.create({ start: 200, end: 'max', onToggle: st => top.classList.toggle('is-compact', st.isActive) });
    $$('.shelf .rule path').forEach(pth => gsap.fromTo(pth, { drawSVG: '0%' }, { drawSVG: '100%', ease: 'none', scrollTrigger: { trigger: pth.closest('.shelf'), start: 'top 85%', end: 'top 55%', scrub: .5 } }));
    gsap.fromTo('.tool .roots path', { drawSVG: '0%' }, { drawSVG: '100%', stagger: .08, ease: 'none', scrollTrigger: { trigger: '.tool-shadowroot', start: 'top 85%', end: 'bottom 60%', scrub: .5 } });
    const ls = SplitText.create('.lede', { type: 'words', aria: 'none' });
    gsap.fromTo(ls.words, { color: '#cbbda4' }, { color: '#f6eedf', stagger: .1, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: '35% top', scrub: .5 } });
    gsap.to('.ribbon-track', { xPercent: -45, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: () => '+=' + innerHeight * 1.6, scrub: .8 } });
    gsap.fromTo('.book3d', { rotateY: -30, rotateX: 7, rotateZ: -3 }, { rotateY: -8, rotateX: 2, rotateZ: 0, ease: 'none', immediateRender: false,
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .6 } });
    gsap.fromTo('#hero-face', { rotateY: 0, '--sheen': '100%' }, { rotateY: -42, '--sheen': '0%', ease: 'none', immediateRender: false,
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom 30%', scrub: .6, onUpdate: st => book.classList.toggle('is-open', st.progress > .02) } });
    gsap.fromTo('.glowline', { opacity: .82 }, { opacity: 1, ease: 'none', scrollTrigger: { trigger: '.threshold', start: 'top 80%', end: 'center center', scrub: true } });
    {
      const th = $('.threshold'), burn = $('.threshold .burn'), gl = $('.glowline'), lit = $('.threshold .lit');
      // stars of phosphor: six layers of tiny dots (plain CSS backgrounds), each layer comes out as the dark deepens
      const layers = Array.from({ length: 6 }, (_, k) => {
        // a small tile of dots repeated; each layer has its own tile size so the repeat never lines up
        const i = document.createElement('i'), n = 4, dots = [], tw = 260 + k * 47, thh = 210 + k * 39;
        for (let d = 0; d < n; d++) { const r = (.6 + Math.random() * 1.1).toFixed(1); dots.push(`radial-gradient(circle at ${Math.round(Math.random() * 100)}% ${Math.round(Math.random() * 100)}%,#86ecd2cc 0 ${r}px,#0000 ${(+r + .8).toFixed(1)}px)`); }
        i.style.backgroundImage = dots.join(','); i.style.backgroundSize = `${tw}px ${thh}px`; $('.threshold .stars').appendChild(i); return { i, t: .12 + k * .13 };
      });
      const drawStars = p => layers.forEach(L => { L.i.style.opacity = gsap.utils.clamp(0, 1, (p - L.t) * 5).toFixed(3); });
      ScrollTrigger.create({ trigger: th, start: 'top 85%', end: 'bottom 70%', scrub: true, onUpdate: st => {
        const p = st.progress;
        burn.style.setProperty('--b', (130 - p * 145).toFixed(1));
        gl.style.setProperty('--gl', p.toFixed(3));
        lit.style.color = `rgb(${Math.round(236 - p * 60)},${Math.round(226 - p * 58)},${Math.round(207 - p * 54)})`;
        drawStars(p);
      }, onRefresh: st => drawStars(st.progress) });
    }
    firstBuild = false;
    return () => cleanups.forEach(f => f());
  });
  build();
  rebuild = () => { mm.revert(); mm = gsap.matchMedia(); build(); };
})();
