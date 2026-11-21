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
    if (v) { snd.set(false); showSound(); if (window.__nfAudio) window.__nfAudio.pause(); }
    rebuild();
  };
  stillBtns.forEach(b => b.addEventListener('click', () => { buzz(6); setStill(!still); }));
  // any tap on a real control gets a quiet tick (sound only when Sound is on)
  document.addEventListener('click', e => { if (e.target.closest('.chip, .btn, .pick, .bk a, .tool, .nav a, .menu-btn, .redo, .door-btn, .card a')) snd.play('tick'); });

  /* ---------- Leave: one tap (or Esc twice) to a neutral page, replacing this one in history ---------- */
  const leave = () => { try { snd.kill(); document.querySelectorAll('audio').forEach(a => a.pause()); if (window.__nfAudio) window.__nfAudio.pause(); if (window.gsap) gsap.globalTimeline.pause(); } catch (e) {} try { document.body.style.visibility = 'hidden'; } catch (e) {} location.replace('https://www.google.com/search?q=weather'); };
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

  /* ---------- v19 batch 5: footer, counter, support, motif, the glow secret ---------- */
  // back to the light: up to the top (the burn reverses with the scroll)
  $('#up').addEventListener('click', () => { buzz(8); snd.play('page'); scrollTo({ top: 0, behavior: smooth() }); setTimeout(() => $('.brand').focus({ preventScroll: true }), calm() ? 0 : 900); });
  // support: a few coins jump from the button (it still opens the link)
  $$('.pay .btn').forEach(a => a.addEventListener('click', () => {
    buzz([6, 30, 6]); snd.play('full');
    if (calm() || !hasG) return;
    const r = a.getBoundingClientRect();
    for (let i = 0; i < 9; i++) {
      const c = document.createElement('span'); c.className = 'coin'; document.body.appendChild(c);
      gsap.fromTo(c, { x: r.left + r.width / 2, y: r.top + r.height / 2, scale: .6 }, { x: `+=${(Math.random() - .5) * 180}`, y: `-=${70 + Math.random() * 110}`, scale: 1, duration: .5, ease: 'power2.out', onComplete: () => gsap.to(c, { y: '+=160', opacity: 0, duration: .55, ease: 'power2.in', onComplete: () => c.remove() }) });
    }
  }));
  // the visit counter (filled on the real domain) rolls its digits into place when it comes into view
  // the counter block is added after this script by scripts/visit-counter.py, so wait for the page to finish parsing
  const setupVisits = () => { const visits = document.getElementById('nf-visits');
  if (visits) {
    const roll = () => {
      const m = visits.textContent.match(/^([\d,]+)(.*)$/); if (!m || visits.querySelector('.odo')) return;
      visits.setAttribute('aria-label', visits.textContent);
      const cols = [...m[1]].map(ch => /\d/.test(ch) ? `<span data-d="${ch}">${'0123456789'.split('').map(n => `<b>${n}</b>`).join('')}</span>` : `<span><b>${ch}</b></span>`).join('');
      visits.innerHTML = `<span class="odo" aria-hidden="true">${cols}</span><span aria-hidden="true">${m[2]}</span>`;
      const go = () => visits.querySelectorAll('.odo>span[data-d]').forEach((c, i) => { c.style.transitionDelay = (i * 90) + 'ms'; c.style.transform = `translateY(-${c.dataset.d * 1.5}em)`; });
      if (calm()) { visits.querySelectorAll('.odo>span').forEach(c => c.style.transition = 'none'); go(); return; }
      new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { o.disconnect(); requestAnimationFrame(go); } }).observe(visits);
    };
    new MutationObserver(roll).observe(visits, { childList: true, characterData: true, subtree: true, attributes: true, attributeFilter: ['hidden'] });
  } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupVisits); else setupVisits();
  // a small seal mark recurs in each section title (decorative; it turns as the page scrolls)
  const SEAL = '<svg viewBox="0 0 64 64"><path fill="currentColor" d="M32 4l4.6 3.4 5.6-.9 2.6 5 5.3 2-.3 5.7 3.9 4.1-2.4 5.2 2.4 5.2-3.9 4.1.3 5.7-5.3 2-2.6 5-5.6-.9L32 60l-4.6-3.4-5.6.9-2.6-5-5.3-2 .3-5.7-3.9-4.1 2.4-5.2-2.4-5.2 3.9-4.1-.3-5.7 5.3-2 2.6-5 5.6.9z"/></svg>';
  $$('.sec-head h2, .workshop h3, .support h2').forEach(h => h.insertAdjacentHTML('beforeend', `<span class="motif" aria-hidden="true">${SEAL}</span>`));
  // the glow secret: type "glow" (or tap "Alive in the dark." three times) and the lights go out for a moment
  const egg = document.createElement('div'); egg.className = 'egg'; egg.setAttribute('aria-hidden', 'true'); document.body.appendChild(egg);
  for (let k = 0; k < 4; k++) { const i = document.createElement('i'), dots = []; for (let n = 0; n < 6; n++) { const r = (.7 + Math.random() * 1.2).toFixed(1); dots.push(`radial-gradient(circle at ${Math.round(Math.random() * 100)}% ${Math.round(Math.random() * 100)}%,#86ecd2 0 ${r}px,#0000 ${(+r + 1).toFixed(1)}px)`); } i.style.backgroundImage = dots.join(','); i.style.backgroundSize = `${180 + k * 53}px ${150 + k * 41}px`; egg.appendChild(i); }
  let eggOn = false;
  const lightsOut = () => {
    if (eggOn || calm() || !hasG) return; eggOn = true; buzz([10, 60, 10, 60, 30]); snd.play('chime');
    gsap.timeline({ onComplete: () => { eggOn = false; } })
      .to(egg, { opacity: .96, duration: .6, ease: 'power2.out' })
      .fromTo(egg.children, { opacity: 0 }, { opacity: 1, duration: .5, stagger: .35, ease: 'power1.out' }, .3)
      .to(egg, { opacity: 0, duration: 1.4, ease: 'power2.inOut' }, '+=1.8');
  };
  let typed = '';
  addEventListener('keydown', e => { if (e.target.closest && e.target.closest('input,textarea,[contenteditable]')) return; typed = (typed + (e.key || '')).slice(-4).toLowerCase(); if (typed === 'glow') lightsOut(); });
  let taps = [];
  $('.glowline').addEventListener('pointerup', () => { const n = performance.now(); taps = taps.filter(t => n - t < 700); taps.push(n); if (taps.length >= 3) { taps = []; lightsOut(); } });

  /* ---------- Music: every song can be found and played here; a small bar keeps it going while you read ---------- */
  const audio = new Audio(); audio.preload = 'none'; let cur = null; window.__nfAudio = audio;
  const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  const PLAYI = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1l10 6-10 6z"/></svg>', PAUSEI = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1h3v12H3zM8 1h3v12H8z"/></svg>';
  const nowbar = $('#nowbar'), npPlay = $('#np-play'), npTitle = $('#np-title'), npProg = $('#np-prog'), note = $('#music-note');
  const rows = () => $$('.trk[data-src]');
  const setIcon = (row, playing) => { const b = $('.play', row); if (!b) return; b.innerHTML = playing ? PAUSEI : PLAYI; b.setAttribute('aria-label', (playing ? 'Pause ' : 'Play ') + row.dataset.title); };
  const start = row => {
    if (cur && cur !== row) { cur.classList.remove('is-playing'); setIcon(cur, false); }
    if (cur !== row) { cur = row; audio.src = row.dataset.src; }
    audio.play().catch(() => { if (note) note.textContent = 'That song could not start. Try another, or open the Listening Room.'; });
  };
  document.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('.trk .play'); if (!b) return;
    const row = b.closest('.trk'); if (cur === row && !audio.paused) audio.pause(); else start(row);
  });
  npPlay.addEventListener('click', () => { if (!cur) return; if (audio.paused) audio.play().catch(() => {}); else audio.pause(); });
  const next = () => { const all = rows(); const i = all.indexOf(cur); const n = all[(i + 1) % all.length]; if (n) start(n); };
  $('#np-next').addEventListener('click', next);
  audio.addEventListener('play', () => { cur.classList.add('is-playing'); setIcon(cur, true); nowbar.hidden = false; npTitle.textContent = cur.dataset.title; npPlay.innerHTML = PAUSEI; npPlay.setAttribute('aria-label', 'Pause ' + cur.dataset.title); if (note) note.textContent = ''; });
  audio.addEventListener('pause', () => { if (!cur) return; setIcon(cur, false); npPlay.innerHTML = PLAYI; npPlay.setAttribute('aria-label', 'Play ' + cur.dataset.title); });
  audio.addEventListener('timeupdate', () => { if (!cur || !audio.duration) return; const k = audio.currentTime / audio.duration * 100; const bar = $('.bar i', cur); if (bar) bar.style.width = k + '%'; npProg.style.width = k + '%'; const t = $('time', cur); if (t) t.textContent = fmt(audio.currentTime); });
  audio.addEventListener('ended', next);
  audio.addEventListener('error', () => { if (note) note.textContent = 'That song could not start. Try another, or open the Listening Room.'; });
  // all songs, by shelf: built the first time someone opens the list
  const allBtn = $('#all-btn'), allBox = $('#all-songs');
  allBtn.addEventListener('click', () => {
    const open = allBox.hidden;
    if (open && !allBox.childElementCount) {
      const S = D.songs, esc = x => x.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
      allBox.innerHTML = S.shelves.map((name, si) => `<h3>${esc(name)}</h3><ul class="tracks">` + S.t.filter(t => t[3] === si).map(t =>
        `<li class="trk" data-src="/music/audio/${esc(t[1])}" data-title="${esc(t[0])}"><button class="play" type="button" aria-label="Play ${esc(t[0])}">${PLAYI}</button><span><span class="t">${esc(t[0])}</span><span class="s">${esc(name)}</span></span><time>${fmt(t[2])}</time><span class="bar" aria-hidden="true"><i></i></span></li>`).join('') + '</ul>').join('');
    }
    allBox.hidden = !open; allBtn.setAttribute('aria-expanded', String(open));
    allBtn.textContent = open ? 'Show fewer songs' : `Show all ${D.songs.t.length} songs`;
    if (!open) $('#music').scrollIntoView({ behavior: smooth() });
  });

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

  // batch 6.2: as you scroll down from the hero, a copy of the cover flies and lands on its own place on the shelf
  function flight() {
    const ghost = document.createElement('img'); ghost.className = 'ghost'; ghost.alt = ''; ghost.setAttribute('aria-hidden', 'true'); document.body.appendChild(ghost);
    let tgt = null, tgtImg = null, src = ''; const desk = matchMedia('(min-width: 901px)');
    const pick = () => {
      if (heroImg.getAttribute('src') === src) return tgt; src = heroImg.getAttribute('src');
      const bk = D.books.find(b => b.imgLg === src); tgt = bk ? $(`.shelf .bk[href="/${bk.slug}"] .cov`) : null; tgtImg = tgt && $('img', tgt);
      if (tgt) ghost.src = $('img', tgt).currentSrc || $('img', tgt).src; return tgt;
    };
    const cap = $('.stage figcaption');
    const show = (inFlight) => { ghost.style.visibility = inFlight ? 'visible' : 'hidden'; if (cap) cap.style.visibility = inFlight ? 'hidden' : ''; book.style.visibility = inFlight ? 'hidden' : ''; if (tgtImg) tgtImg.style.visibility = inFlight ? 'hidden' : ''; };
    const near = () => { const t = pick(); if (!t) return false; const gap = t.getBoundingClientRect().top - $('.hero').getBoundingClientRect().bottom; return gap < innerHeight * 1.6; };
    const st = ScrollTrigger.create({ trigger: '.hero', start: 'bottom 75%', end: () => '+=' + Math.round(innerHeight * .9), onUpdate: s => {
      const p = s.progress;
      if (p <= 0 || p >= 1 || !near()) { show(false); return; }
      const a = book.getBoundingClientRect(), b = tgt.getBoundingClientRect(), e = gsap.parseEase('power2.inOut')(p);
      if (!desk.matches && (a.bottom > 0 || b.top > innerHeight)) { show(false); return; }
      const chips = $('.chips').getBoundingClientRect();
      if (chips.bottom > 0 && chips.top < innerHeight && !desk.matches) { show(false); return; }
      ghost.style.opacity = Math.min(1, p * 6).toFixed(2);
      const w = a.width + (b.width - a.width) * e, x = a.left + (b.left - a.left) * e, y = a.top + (b.top - a.top) * e;
      ghost.style.width = b.width + 'px'; ghost.style.height = b.height + 'px';
      ghost.style.transform = `translate(${x}px,${y}px) scale(${w / b.width}) rotate(${(-6 * (1 - e)).toFixed(2)}deg)`;
      show(true);
    }, onLeave: () => show(false), onLeaveBack: () => show(false) });
    return () => { st.kill(); show(false); ghost.remove(); };
  }
  // batch 6.3: desktop wheels glide (trackpads, keyboards, scrollbars and phones keep their own native scrolling)
  function glide() {
    let target = scrollY, cur = scrollY, raf = 0, active = false;
    const max = () => document.documentElement.scrollHeight - innerHeight;
    const step = () => {
      cur += (target - cur) * .12;
      if (Math.abs(target - cur) < .5) { cur = target; active = false; raf = 0; scrollTo({ top: cur, behavior: 'instant' }); return; }
      scrollTo({ top: cur, behavior: 'instant' }); raf = requestAnimationFrame(step);
    };
    const wheel = e => {
      if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY) || sheet.hasAttribute('data-open')) return;
      const d = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaMode === 2 ? e.deltaY * innerHeight : e.deltaY;
      if (e.deltaMode === 0 && Math.abs(d) < 50 && !active) return;   // small, continuous deltas are a trackpad: leave them native
      e.preventDefault();
      if (!active) { cur = target = scrollY; active = true; }
      target = gsap.utils.clamp(0, max(), target + d);
      if (!raf) raf = requestAnimationFrame(step);
    };
    const keyOrBar = () => { if (active) { cancelAnimationFrame(raf); raf = 0; active = false; } };
    addEventListener('wheel', wheel, { passive: false }); addEventListener('keydown', keyOrBar); addEventListener('pointerdown', keyOrBar);
    return () => { removeEventListener('wheel', wheel); removeEventListener('keydown', keyOrBar); removeEventListener('pointerdown', keyOrBar); cancelAnimationFrame(raf); };
  }

  /* ---------- Motion (GSAP). Reduced motion: nothing self-running; scroll-linked motion stays. ---------- */
  if (!hasG) return;
  gsap.registerPlugin(ScrollTrigger, SplitText, DrawSVGPlugin);
  let mm = gsap.matchMedia(), firstBuild = true;
  const build = () => mm.add({ motion: '(prefers-reduced-motion: no-preference)', still: '(prefers-reduced-motion: reduce)' }, ctx => {
    const motion = ctx.conditions.motion && !still, entrance = motion && firstBuild;
    const cleanups = [];
    if (entrance) {
      // the opening montage: the logo figures are dealt one after another, then the four that stand for each door fly into place.
      // Under five seconds, any tap, scroll, key or focus skips straight to the doors.
      const doorsEl = $('.doors'), deckImgs = $$('.deck img'), tiles = $$('.door-t');
      // a slow phone that only gets here late has already painted the doors: never replay over them, just keep the doors
      const late = performance.now() > 1400 || scrollY > 40;
      if (!late) doorsEl.classList.add('is-montage');
      const mt = gsap.timeline({ paused: late, onComplete: () => { doorsEl.classList.remove('is-montage'); deckImgs.forEach(i => gsap.set(i, { clearProps: 'all' })); off(); } });
      // the first figure is on screen at once (it is the page's largest picture); each later one lands a touch smaller, so none outgrows it
      gsap.set(deckImgs[0], { xPercent: -50, yPercent: -50, rotation: -6, autoAlpha: 1 });
      deckImgs.slice(1).forEach((im, n) => { const k = n + 1; mt.fromTo(im, { xPercent: -50, yPercent: -46, scale: .98, rotation: k % 2 ? 4 : -4, autoAlpha: 0 },
        { yPercent: -50, scale: .96, rotation: k % 2 ? 2.5 : -2.5, autoAlpha: 1, duration: .32, ease: 'power3.out' }, .3 + (k - 1) * .38); });
      mt.add(() => {
        const box = doorsEl.getBoundingClientRect();
        tiles.forEach(t => {
          const im = $(`.deck img[data-logo="${t.dataset.logo}"]`), r = t.getBoundingClientRect(), ir = im.getBoundingClientRect();
          gsap.to(im, { x: r.left + r.width / 2 - (ir.left + ir.width / 2), y: r.top + r.height / 2 - (ir.top + ir.height / 2), scaleX: r.width / ir.width * (im._gsap.scaleX || 1), scaleY: r.height / ir.height * (im._gsap.scaleY || 1), rotation: 0, borderRadius: 12, duration: .75, ease: 'expo.inOut' });
        });
        deckImgs.filter(im => !tiles.some(t => t.dataset.logo === im.dataset.logo)).forEach(im => gsap.to(im, { autoAlpha: 0, scale: .9, duration: .4 }));
      }, '+=.15');
      mt.to({}, { duration: .8 });
      mt.from('.doors-head > *', { y: 24, opacity: 0, duration: .7, stagger: .08, ease: 'expo.out' }, '-=.9');
      const skip = () => { if (mt.progress() < 1) mt.progress(1); };
      if (late) mt.progress(1);
      const evs = ['pointerdown', 'wheel', 'keydown', 'touchstart'];
      const off = () => { evs.forEach(ev => removeEventListener(ev, skip)); removeEventListener('scroll', skip); doorsEl.removeEventListener('focusin', skip); };
      evs.forEach(ev => addEventListener(ev, skip, { passive: true })); addEventListener('scroll', skip, { passive: true }); doorsEl.addEventListener('focusin', skip);
      cleanups.push(() => { mt.progress(1); off(); });
      // the book's own entrance now plays when the Library opening scrolls into view
      const h1 = $('.hero .h1'), lns = $$('.hero .h1 .ln');
      h1.setAttribute('aria-label', h1.textContent.replace(/\s+/g, ' ').trim()); lns.forEach(l => l.setAttribute('aria-hidden', 'true'));
      const hs = SplitText.create('.hero .h1 .ln>span', { type: 'words,chars', aria: 'none' });
      const unsplit = () => { hs.revert(); h1.removeAttribute('aria-label'); lns.forEach(l => l.removeAttribute('aria-hidden')); };
      cleanups.push(unsplit);
      const ent = gsap.timeline({ paused: true, onComplete: unsplit })
        .from(hs.chars, { yPercent: 115, duration: .9, stagger: .022, ease: 'expo.out' }, 0)
        .from(hs.chars, { color: '#e7c77d', duration: 1.3, stagger: .022, ease: 'power1.in' }, .25)
        .from('.lede, .ask, .chips', { y: 18, duration: .8, stagger: .1, ease: 'expo.out' }, .55)
        .from('.book-in', { y: -70, opacity: 0, duration: 1.1, ease: 'expo.out' }, .35)
        .from('.book-tilt', { rotationY: -34, duration: 1.4, ease: 'expo.out' }, .35)
        .from('.floor', { opacity: 0, scale: .4, duration: 1.1, ease: 'expo.out' }, .35)
        .fromTo('.book-tilt', { rotationX: 0 }, { rotationX: -6, duration: .55, ease: 'power2.inOut', yoyo: true, repeat: 1 }, 1.45)
        .to('.book-in', { y: -10, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3 }, 1.55)
        .to('.floor', { scale: .82, opacity: .65, duration: 1.1, ease: 'sine.inOut', yoyo: true, repeat: 3 }, 1.55);
      ScrollTrigger.create({ trigger: '.hero', start: 'top 75%', once: true, onEnter: () => ent.play() });
      // the title strip drifts in once on arrival (4 s, then it follows the scroll)
      gsap.from('.ribbon-track', { x: 220, duration: 4, ease: 'power2.out' });
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
      if (!fine) {
        // phones: a carousel turn. Covers and pendants turn toward the centre of their row as the thumb scrolls it,
        // the one in front sits a little larger, and the phone ticks when a row settles.
        const rows = [...$$('.shelf .books').map(ul => [ul, $$('.cov', ul), 'cov']), ...$$('.pairs').map(ul => [ul, $$('.portal', ul), 'portal'])];
        rows.forEach(([ul, items, kind]) => {
          let raf = 0;
          const turn = () => {
            raf = 0; const r = ul.getBoundingClientRect(), mid = r.left + (kind === 'cov' ? r.width * .25 : r.width * .45);
            items.forEach(el => { const b = el.getBoundingClientRect(), k = gsap.utils.clamp(-1, 1, (b.left + b.width / 2 - mid) / (r.width * .6));
              if (kind === 'cov') { el.style.setProperty('--ty', (k * -22).toFixed(2) + 'deg'); el.style.setProperty('--cs', (1 - Math.abs(k) * .08).toFixed(3)); }
              else el.style.setProperty('--ps', (1 - Math.abs(k) * .07).toFixed(3)); });
          };
          const on = () => { if (!raf) raf = requestAnimationFrame(turn); };
          ul.addEventListener('scroll', on, { passive: true }); turn();
          const settle = () => { buzz(4); snd.play('tick'); };
          if (kind === 'portal') ul.addEventListener('scrollend', settle);
          cleanups.push(() => { ul.removeEventListener('scroll', on); ul.removeEventListener('scrollend', settle); items.forEach(el => ['--ty', '--cs', '--ps'].forEach(v => el.style.removeProperty(v))); });
        });
        // tools: a band of light crosses each card as it passes through the screen, and the card settles flat
        $$('.tool').forEach(t => {
          gsap.fromTo(t, { '--gx': '0%', '--go': 0 }, { '--gx': '100%', ease: 'none', scrollTrigger: { trigger: t, start: 'top 90%', end: 'bottom 20%', scrub: .4,
            onUpdate: st => t.style.setProperty('--go', (Math.sin(st.progress * Math.PI) * .9).toFixed(3)) } });
          gsap.fromTo(t, { '--rx': '8deg' }, { '--rx': '0deg', ease: 'none', scrollTrigger: { trigger: t, start: 'top 95%', end: 'top 60%', scrub: .4 } });
        });
      }
      // NFC guide: a phone comes down onto a wax seal, the seal answers in rings, a note appears on the screen (twice, then rests)
      const td = gsap.timeline({ paused: true, repeat: 1, repeatDelay: .4 })
        .fromTo('.td-phone', { y: -18 }, { y: 6, duration: .55, ease: 'power2.in' })
        .add(() => buzz(5))
        .fromTo('.td-rip circle', { scale: 1, opacity: .9, svgOrigin: '80 84' }, { scale: 2.6, opacity: 0, duration: .9, stagger: .18, ease: 'power2.out' })
        .to('.td-screen', { opacity: .5, duration: .3 }, '<')
        .to('.td-note', { opacity: 1, duration: .3 }, '<+.1')
        .to('.td-phone', { y: -18, duration: .6, ease: 'power2.out' }, '+=.4')
        .to('.td-screen', { opacity: .08, duration: .4 }, '<')
        .to('.td-note', { opacity: 0, duration: .3 }, '<');
      ScrollTrigger.create({ trigger: '.card.guide', start: 'top 75%', once: true, onEnter: () => td.play(0) });
      // The Press stamps down; The Casting pours and its figure rises
      const [sealIco, castIco] = $$('.mk .mk-ico');
      ScrollTrigger.create({ trigger: '.making', start: 'top 85%', once: true, onEnter: () => {
        if (sealIco) gsap.timeline().fromTo(sealIco, { scale: 1.6, rotation: -25, opacity: 0 }, { scale: .88, rotation: 0, opacity: 1, duration: .35, ease: 'power3.in' }).to(sealIco, { scale: 1, duration: .5, ease: 'elastic.out(1,.4)' }).add(() => buzz(6), '<');
        if (castIco) { const ps = $$('path', castIco); gsap.fromTo(ps, { drawSVG: '0%' }, { drawSVG: '100%', duration: .9, stagger: .15, ease: 'power2.inOut', delay: .2 }); }
      } });
      cleanups.push(flight());
      if (!matchMedia('(min-width: 901px)').matches) $$('.shelf').forEach(sh => gsap.fromTo(sh, { y: 40, scale: .97 }, { y: 0, scale: 1, ease: 'none', scrollTrigger: { trigger: sh, start: 'top 100%', end: 'top 60%', scrub: .4 } }));
      if (fine) cleanups.push(glide());
      // stacking shelves: the shelf being covered sinks back a little as the next one slides over it
      const shelfEls = $$('.shelf');
      if (matchMedia('(min-width: 901px)').matches) shelfEls.slice(0, -1).forEach((sh, i) => gsap.fromTo(sh, { scale: 1, filter: 'brightness(1)' }, { scale: .95, filter: 'brightness(.55)', ease: 'none',
        scrollTrigger: { trigger: shelfEls[i + 1], start: 'top 40%', end: () => 'top ' + ($('.top').offsetHeight + 8) + 'px', scrub: .3 } }));
      // page turn: Tools, The Listening Room and the support panel arrive with a diagonal edge sweeping down, like a turning page
      if (matchMedia('(min-width: 901px)').matches) $$('#tools, #music, #support').forEach(sec => gsap.fromTo(sec, { clipPath: 'polygon(0% 0%, 100% 0%, 100% 0%, 0% 35%)' }, { clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 135%)', ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top 95%', end: 'top 25%', scrub: .4, onLeave: () => gsap.set(sec, { clipPath: 'none' }), onEnterBack: () => {} } }));
      // section titles rise line by line into a mask as they arrive (once), on every screen
      $$('.sec-head h2, .workshop h3, .support h2').forEach(h => {
        const sp = SplitText.create(h, { type: 'lines', mask: 'lines', aria: 'none' });
        gsap.from(sp.lines, { yPercent: 105, duration: .9, stagger: .1, ease: 'expo.out', scrollTrigger: { trigger: h, start: 'top 88%', once: true }, onComplete: () => sp.revert() });
        cleanups.push(() => sp.revert());
      });
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
        // desktop: a ring follows the pointer, grows over anything you can press, and turns green in the dark
        const cur = document.createElement('div'); cur.className = 'cur'; cur.setAttribute('aria-hidden', 'true'); document.body.appendChild(cur);
        const cx = gsap.quickTo(cur, 'x', { duration: .2, ease: 'power3.out' }), cy = gsap.quickTo(cur, 'y', { duration: .2, ease: 'power3.out' });
        const cm = e => { cur.classList.add('is-on'); cx(e.clientX); cy(e.clientY); cur.classList.toggle('is-big', !!(e.target.closest && e.target.closest('a,button,.portal,.book3d'))); cur.classList.toggle('is-night', !!(e.target.closest && e.target.closest('[data-night]'))); };
        const cl = () => cur.classList.remove('is-on');
        addEventListener('pointermove', cm); document.addEventListener('pointerleave', cl);
        cleanups.push(() => { removeEventListener('pointermove', cm); document.removeEventListener('pointerleave', cl); cur.remove(); });
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
    // the guide's cover lifts like a page as it arrives; the signature writes itself across as the footer comes up
    gsap.fromTo('.card.guide img', { rotateX: 14, transformPerspective: 900 }, { rotateX: 0, ease: 'none', scrollTrigger: { trigger: '.card.guide', start: 'top 95%', end: 'top 45%', scrub: .5 } });
    gsap.fromTo('.sig', { '--sig': '100%' }, { '--sig': '0%', ease: 'none', scrollTrigger: { trigger: 'footer', start: 'top 95%', end: 'top 50%', scrub: .5 } });
    gsap.to('.motif', { rotation: 360, ease: 'none', scrollTrigger: { trigger: document.documentElement, start: 'top top', end: 'bottom bottom', scrub: 1 } });
    const ls = SplitText.create('.lede', { type: 'words', aria: 'none' });
    gsap.fromTo(ls.words, { color: '#cbbda4' }, { color: '#f6eedf', stagger: .1, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top 60%', end: '30% top', scrub: .5 } });
    gsap.to('.ribbon-track', { xPercent: -45, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: () => '+=' + innerHeight * 1.6, scrub: .8 } });
    // the spine catches more light as the book turns toward the reader
    gsap.fromTo('.book3d', { rotateY: -30, rotateX: 7, rotateZ: -3, '--spl': .75 }, { rotateY: -8, rotateX: 2, rotateZ: 0, '--spl': 1.25, ease: 'none', immediateRender: false,
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
