/* =====================================================================
   lightbox.js — full-view piece viewer.

   NAVIGATION
     Arrows, arrow keys and horizontal swipes move between PIECES, across
     whatever the grid is currently filtered to. With one photo per statue
     that turns the viewer into a way to browse the whole collection
     rather than a dead end you have to close and reopen.
     When a piece does have several angles, the strip below selects them.

   LOADING
     The grid thumbnail is already decoded in the browser, so it is shown
     immediately — blurred and scaled — while the high-resolution image
     streams in behind it and fades through. The viewer never shows an
     empty frame.

   ENLARGING
     Desktop: click the photo to zoom in, move the mouse to pan.
     Phone:   pinch to zoom, the browser handles it natively.
   ===================================================================== */

import { cardImage, detailImage, masterURL } from './images.js';
import { trailFor } from './facets.js';

const SWIPE_DISTANCE = 45;
const SWIPE_DISMISS = 90;

export class Lightbox {
  constructor(root) {
    this.root = root;
    this.list = [];
    this.index = 0;
    this.angle = 0;
    this.zoomed = false;
    this.lastFocus = null;
    this.downOnBackdrop = false;

    this.el = {
      id: root.querySelector('.lb-id'),
      title: root.querySelector('.lb-title'),
      stage: root.querySelector('.lb-stage'),
      frame: root.querySelector('.lb-frame'),
      img: root.querySelector('.lb-full'),
      blur: root.querySelector('.lb-blur'),
      counter: root.querySelector('.lb-counter'),
      strip: root.querySelector('.lb-strip'),
      cat: root.querySelector('.li-cat'),
      desc: root.querySelector('.li-desc'),
      tags: root.querySelector('.li-tags'),
      prev: root.querySelector('.lb-prev'),
      next: root.querySelector('.lb-next'),
      close: root.querySelector('.lb-close'),
      zoomHint: root.querySelector('.lb-zoomhint'),
      enquire: root.querySelector('.li-enquire'),
    };

    /* Set by the gallery once data/facets.json and data/site.json load. */
    this.facets = [];
    this.email = '';

    this.#wire();
  }

  #pushed = false;

  get isOpen() { return this.root.classList.contains('show'); }
  get statue() { return this.list[this.index] || null; }

  /* ---------------- wiring ---------------- */

  #wire() {
    this.el.close.addEventListener('click', () => this.close());
    this.el.prev.addEventListener('click', e => { e.stopPropagation(); this.step(-1); });
    this.el.next.addEventListener('click', e => { e.stopPropagation(); this.step(1); });

    this.root.addEventListener('mousedown', e => {
      this.downOnBackdrop = e.target === this.root || e.target === this.el.stage;
    });
    this.root.addEventListener('click', e => {
      if (this.downOnBackdrop && (e.target === this.root || e.target === this.el.stage)) {
        this.close();
      }
    });

    this.el.strip.addEventListener('click', e => {
      const btn = e.target.closest('[data-angle]');
      if (btn) this.showAngle(Number(btn.dataset.angle));
    });

    /* The frame fills the stage, so a click inside it may still be on the
       letterboxing beside the photo. Treat that as a backdrop click and
       close, which is what people expect from a lightbox; only a click on
       the photograph itself zooms. */
    this.el.frame.addEventListener('click', e => {
      e.stopPropagation();
      if (!this.#pointOnPhoto(e)) { this.close(); return; }
      if (matchMedia('(hover: hover)').matches) this.toggleZoom();
    });
    this.el.frame.addEventListener('mousemove', e => {
      if (!this.zoomed) return;
      const r = this.el.frame.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 100;
      const y = ((e.clientY - r.top) / r.height) * 100;
      this.el.img.style.transformOrigin = `${x}% ${y}%`;
    });

    document.addEventListener('keydown', e => {
      if (!this.isOpen) return;
      if (e.key === 'Escape') { e.preventDefault(); this.zoomed ? this.toggleZoom() : this.close(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); this.step(-1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); this.step(1); }
      else if (e.key === 'Tab') this.#trapFocus(e);
    });

    window.addEventListener('popstate', () => {
      if (this.isOpen) this.close(true);
    });

    /* --- touch: swipe between pieces, swipe down to dismiss --- */
    let x0 = null, y0 = null, multi = false;
    this.el.stage.addEventListener('touchstart', e => {
      multi = e.touches.length > 1;      // pinch-zooming, leave it alone
      x0 = e.touches[0].clientX;
      y0 = e.touches[0].clientY;
    }, { passive: true });

    this.el.stage.addEventListener('touchend', e => {
      if (x0 === null || multi) { x0 = y0 = null; return; }
      const dx = e.changedTouches[0].clientX - x0;
      const dy = e.changedTouches[0].clientY - y0;
      x0 = y0 = null;
      if (Math.abs(dx) > SWIPE_DISTANCE && Math.abs(dx) > Math.abs(dy) * 1.4) {
        this.step(dx < 0 ? 1 : -1);
      } else if (dy > SWIPE_DISMISS && Math.abs(dy) > Math.abs(dx) * 1.4) {
        this.close();
      }
    }, { passive: true });
  }

  /* ---------------- opening ---------------- */

  /**
   * @param {object[]} list   the pieces currently on screen, in grid order
   * @param {number}   index  which one to show
   */
  open(list, index = 0) {
    if (!Array.isArray(list) || !list.length) return;
    this.lastFocus = document.activeElement;
    this.list = list;
    this.index = Math.max(0, Math.min(index, list.length - 1));

    this.root.classList.add('show');
    this.root.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    this.render();
    this.el.close.focus();
  }

  render() {
    const s = this.statue;
    if (!s) return;

    this.setZoom(false);
    this.angle = 0;

    this.el.id.textContent = s.id;
    this.el.title.textContent = s.title || 'Untitled piece';
    /* The facet trail, e.g. "Pets › Cats · Incense Burners". */
    this.el.cat.textContent = (this.facets || [])
      .map(a => s.facets?.[a.key] ? trailFor(a, s.facets[a.key]).join(' › ') : null)
      .filter(Boolean).join('  ·  ') || 'New arrival';
    this.el.desc.textContent = s.description || '';
    this.el.desc.hidden = !s.description;
    this.el.tags.innerHTML = s.tags.map(t => `<span>${escapeHTML(t)}</span>`).join('');

    /* Someone looking at a piece full-screen is as close to buying as
       this site gets, so the way to ask about it belongs right here. */
    if (this.el.enquire) {
      const url = `${location.origin}/statues/${s.id}/`;
      this.el.enquire.href =
        `mailto:${this.email}?subject=${encodeURIComponent(
          `Enquiry — ${s.id}${s.title ? ` (${s.title})` : ''}`)}` +
        `&body=${encodeURIComponent(`I'm interested in this piece:\n${url}\n\n`)}`;
    }

    /* Position within the filtered collection, not within one piece. */
    this.el.counter.textContent = `${this.index + 1} / ${this.list.length}`;
    this.el.counter.hidden = this.list.length < 2;
    this.el.prev.hidden = this.list.length < 2;
    this.el.next.hidden = this.list.length < 2;

    /* The angle strip is only meaningful for a piece shot from several
       sides. With one photo per statue it stays out of the way. */
    const many = s.angles.length > 1;
    this.el.strip.hidden = !many;
    this.el.strip.innerHTML = many
      ? s.angles.map((a, i) => `
          <button class="lb-thumb" data-angle="${i}" aria-label="${escapeHTML(a.label)}">
            <img src="${cardImage(a).src}" alt="" loading="lazy" decoding="async">
          </button>`).join('')
      : '';

    this.showAngle(0);
    this.#preloadNeighbours();

    /* Push once when the viewer opens, replace while stepping. Android's
       hardware back and the iOS back-swipe then close the viewer rather
       than leaving the site — and 40 arrow presses do not become 40 back
       presses to escape. */
    if (this.#pushed) history.replaceState({ lb: s.id }, '', `#${s.id}`);
    else { history.pushState({ lb: s.id }, '', `#${s.id}`); this.#pushed = true; }
  }

  showAngle(i) {
    const s = this.statue;
    if (!s) return;
    const n = s.angles.length;
    this.angle = ((i % n) + n) % n;
    const a = s.angles[this.angle];

    this.setZoom(false);

    /* 1. Instant: the grid thumbnail, already decoded, blurred behind. */
    this.el.blur.src = a.fixed?.thumb || cardImage(a).src;

    /* 2. Then the real thing, faded in once decoded. */
    const detail = a.fixed?.detail
      ? { src: a.fixed.detail, srcset: '', sizes: '', fallback: a.fixed.detail }
      : detailImage(a);

    const img = this.el.img;
    img.classList.remove('ready');
    img.removeAttribute('srcset');

    /* If the transform endpoint is unavailable — running the plain static
       server, or a misconfigured deploy — drop to the committed master so
       the viewer still shows the photo. */
    img.onerror = () => {
      if (img.dataset.fellBack === '1') return;
      img.dataset.fellBack = '1';
      img.removeAttribute('srcset');
      img.src = detail.fallback || masterURL(a);
    };
    img.onload = () => { img.classList.add('ready'); };

    delete img.dataset.fellBack;
    img.alt = a.alt || `${s.title || s.id}${many(s) ? ` — ${a.label}` : ''}`;
    if (detail.srcset) {
      img.sizes = detail.sizes;
      img.srcset = detail.srcset;
    }
    img.src = detail.src;

    if (img.complete && img.naturalWidth) img.classList.add('ready');

    this.el.strip.querySelectorAll('.lb-thumb')
      .forEach((b, j) => b.classList.toggle('on', j === this.angle));
  }

  /* Warm the neighbouring pieces so a swipe lands on a decoded image.

     The preload carries the same srcset and sizes as the real render, so
     the browser resolves it to the identical candidate and the cache
     entry is actually reused. Preloading one fixed width instead would
     often fetch a size that is then never requested. */
  #preloadNeighbours() {
    for (const d of [1, -1]) {
      const s = this.list[this.index + d];
      if (!s?.angles?.length) continue;
      const a = s.angles[0];
      if (a.fixed?.detail) { new Image().src = a.fixed.detail; continue; }

      const detail = detailImage(a);
      const img = new Image();
      if (detail.srcset) { img.sizes = detail.sizes; img.srcset = detail.srcset; }
      img.src = detail.src;
    }
  }

  step(d) {
    if (!this.isOpen || this.list.length < 2) return;
    const n = this.list.length;
    this.index = ((this.index + d) % n + n) % n;
    this.render();
  }

  /* ---------------- zoom ---------------- */

  /* Where the photo actually paints inside the frame, given object-fit:
     contain. Anything outside that rect is empty backdrop. */
  #pointOnPhoto(e) {
    const img = this.el.img;
    if (!img.naturalWidth || this.zoomed) return true;

    const r = this.el.frame.getBoundingClientRect();
    const scale = Math.min(r.width / img.naturalWidth, r.height / img.naturalHeight);
    const w = img.naturalWidth * scale;
    const h = img.naturalHeight * scale;
    const x = r.left + (r.width - w) / 2;
    const y = r.top + (r.height - h) / 2;

    return e.clientX >= x && e.clientX <= x + w
        && e.clientY >= y && e.clientY <= y + h;
  }

  toggleZoom() { this.setZoom(!this.zoomed); }

  setZoom(on) {
    this.zoomed = on;
    this.el.frame.classList.toggle('zoomed', on);
    this.el.img.style.transformOrigin = on ? this.el.img.style.transformOrigin : '50% 50%';
    if (this.el.zoomHint) {
      this.el.zoomHint.textContent = on ? 'Click to zoom out' : 'Click to enlarge';
    }
  }

  /* ---------------- closing ---------------- */

  close(fromPopState = false) {
    /* Unwinding our own history entry is what makes the URL correct
       again; when the pop is what closed us, it is already gone. */
    if (this.#pushed && !fromPopState) { this.#pushed = false; history.back(); return; }
    this.#pushed = false;
    this.setZoom(false);
    this.root.classList.remove('show');
    this.root.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (this.lastFocus && this.lastFocus.isConnected) this.lastFocus.focus();
  }

  #trapFocus(e) {
    const items = [...this.root.querySelectorAll(
      'button:not([hidden]), [href], input, [tabindex]:not([tabindex="-1"])')]
      .filter(n => n.offsetParent !== null);
    if (!items.length) return;
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }
}

const many = s => s.angles.length > 1;

export function escapeHTML(s) {
  return String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}
