/* =====================================================================
   gallery.js — the browsing surface.

   The navigation is generated entirely from data/facets.json. The primary
   axis (Subject) is drilled into one level at a time with a breadcrumb;
   every other axis becomes a row of filter chips. Adding an axis, a value
   or a whole new branch changes nothing here.

   Filter state lives in the URL (?subject=pets/cats&form=jar&q=white), so
   a filtered view is shareable — which matters when traffic arrives from
   a TikTok caption — and the browser's back button works.
   ===================================================================== */

import { loadCollection, sortStatues, applyFilters, findById, tagIndex } from './store.js';
import { Lightbox, escapeHTML } from './lightbox.js';
import { cardImage, detailImage } from './images.js';
import { walkValues, labelFor, trailFor, countByPath, matches } from './facets.js';

/* Pieces appended per batch. Two batches load automatically, then the
   reader asks for more — otherwise the footer, and the enquire button in
   it, can never be reached at 1000 pieces. */
const PAGE = 60;
const AUTO_BATCHES = 2;
/* Tags are free-form and grow without limit, so only the most used are
   shown until asked for. */
const TAGS_COLLAPSED = 14;

/* Internal workflow state, not something a buyer should see. */
const ADMIN = new URLSearchParams(location.search).has('admin');

const state = {
  statues: [], facets: [], site: {}, primary: null,
  filters: {}, query: '', tags: [],
  visible: [], shown: 0, batches: 0,
  dense: false,
};

let lightbox;
const el = {};

/* ------------------------------------------------------------------ */
/*  URL <-> state                                                      */
/* ------------------------------------------------------------------ */

function readURL() {
  const p = new URLSearchParams(location.search);
  state.filters = {};
  for (const axis of state.facets) {
    const v = p.get(axis.key);
    if (v) state.filters[axis.key] = v.toLowerCase();
  }
  state.query = p.get('q') || '';
  state.tags = (p.get('tags') || '').split(',').map(t => t.trim()).filter(Boolean);
  state.dense = p.get('view') === 'dense';
}

function writeURL({ replace = false } = {}) {
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(state.filters)) if (v) p.set(k, v);
  if (state.query.trim()) p.set('q', state.query.trim());
  if (state.tags.length) p.set('tags', state.tags.join(','));
  if (state.dense) p.set('view', 'dense');
  if (ADMIN) p.set('admin', '');
  const url = p.toString() ? `?${p}` : location.pathname;
  history[replace ? 'replaceState' : 'pushState']({ nav: true }, '', url);
}

/* ------------------------------------------------------------------ */
/*  Cards                                                              */
/* ------------------------------------------------------------------ */

function cardHTML(s, index) {
  const a = s.angles[0];
  const many = s.angles.length > 1;
  const img = a.fixed?.thumb ? { src: a.fixed.thumb, fallback: a.fixed.thumb } : cardImage(a);
  const label = s.title || s.id;

  return `
    <button class="piece" data-id="${escapeHTML(s.id)}" data-index="${index}"
            style="--tile-bg:${escapeHTML(a.bg || 'var(--obsidian)')}"
            aria-label="${escapeHTML(label)} — open full view">
      <div class="piece-img">
        <img src="${img.src}" data-fallback="${img.fallback}"
             alt="${escapeHTML(label)}" loading="lazy" decoding="async">
        ${many ? `<span class="angles">${s.angles.length} views</span>` : ''}
        ${ADMIN && s.needsReview ? `<span class="flag">Review</span>` : ''}
        <div class="piece-meta">
          <div class="pn">${escapeHTML(s.id)}</div>
          ${s.title ? `<div class="pt">${escapeHTML(s.title)}</div>` : ''}
        </div>
      </div>
    </button>`;
}

function bindCards(scope) {
  scope.querySelectorAll('.piece-img img').forEach(img => {
    const done = () => {
      img.classList.add('ready');
      img.closest('.piece-img')?.classList.add('loaded');
    };
    img.addEventListener('error', () => {
      if (img.dataset.fellBack === '1') { done(); return; }
      img.dataset.fellBack = '1';
      img.src = img.dataset.fallback || '';
    });
    if (img.complete && img.naturalWidth) done();
    else img.addEventListener('load', done, { once: true });
  });

  /* Desktop: begin fetching the full-size photo on hover so the click
     that follows opens something already cached. The preload carries the
     same srcset as the viewer, so the browser resolves it to the very
     same candidate — preloading one fixed width would fetch a size that
     is then never requested. */
  if (matchMedia('(hover: hover)').matches) {
    scope.querySelectorAll('.piece').forEach(card => {
      card.addEventListener('pointerenter', () => {
        if (card.dataset.warm === '1') return;
        card.dataset.warm = '1';
        const s = findById(state.statues, card.dataset.id);
        const a = s?.angles?.[0];
        if (!a) return;
        const d = detailImage(a);
        const img = new Image();
        if (d.srcset) { img.sizes = d.sizes; img.srcset = d.srcset; }
        img.src = d.src;
      }, { once: true });
    });
  }
}

/* ------------------------------------------------------------------ */
/*  Facet navigation                                                   */
/* ------------------------------------------------------------------ */

/* Subject is browsed one level at a time: the top level until you pick
   one, then its children. A flat wall of every nested value would be
   unusable once the taxonomy grows. */
function subjectLevel(axis) {
  const active = state.filters[axis.key];
  if (!active) return { basePath: null, values: axis.values || [] };

  for (const entry of walkValues(axis)) {
    if (entry.path !== active) continue;

    /* A branch shows its children; a leaf shows its siblings so you can
       move sideways without going back up. `basePath` is whatever those
       values hang off — NOT the active path, or a leaf's siblings would
       be addressed as pets/cats/dogs instead of pets/dogs. */
    if (entry.value.children?.length) {
      return { basePath: active, values: entry.value.children };
    }
    const parents = entry.parents;
    return parents.length
      ? { basePath: parents.map(p => p.slug).join('/'),
          values: parents[parents.length - 1].children || [] }
      : { basePath: null, values: axis.values || [] };
  }
  return { basePath: null, values: axis.values || [] };
}

function renderNav() {
  const counted = applyFilters(state.statues, state.facets, {}, state.query, state.tags);

  /* --- primary axis: breadcrumb + drill-down --- */
  const axis = state.primary;
  if (axis) {
    const active = state.filters[axis.key];
    const counts = countByPath(axis, counted);
    const { basePath, values } = subjectLevel(axis);

    const crumbs = [`<button class="crumb" data-goto="">All</button>`];
    if (active) {
      const parts = active.split('/');
      parts.forEach((_, i) => {
        const p = parts.slice(0, i + 1).join('/');
        const last = i === parts.length - 1;
        crumbs.push(`<span class="crumb-sep">›</span>` + (last
          ? `<span class="crumb on">${escapeHTML(labelFor(axis, p))}</span>`
          : `<button class="crumb" data-goto="${escapeHTML(p)}">${escapeHTML(labelFor(axis, p))}</button>`));
      });
    }
    el.crumbs.innerHTML = crumbs.join('');

    const base = basePath ? basePath + '/' : '';
    el.subjects.innerHTML = values.map(v => {
      const p = base + v.slug;
      const n = counts.get(p) || 0;
      return `<button class="chip ${state.filters[axis.key] === p ? 'on' : ''}"
                      data-axis="${escapeHTML(axis.key)}" data-value="${escapeHTML(p)}"
                      ${n ? '' : 'data-empty="1"'}>
                ${escapeHTML(v.label || v.slug)}<span class="n">${n}</span>
              </button>`;
    }).join('');
    el.subjectGroup.hidden = !values.length;
  }

  /* --- tags: free-form, derived from the pieces themselves --- */
  if (el.tagRow) {
    const scoped = applyFilters(state.statues, state.facets, state.filters, state.query, []);
    const index = tagIndex(scoped);
    const shown = state.tagsExpanded ? index : index.slice(0, TAGS_COLLAPSED);
    const chips = shown.map(({ tag, n }) => {
      const on = state.tags.includes(tag);
      return `<button class="chip ${on ? 'on' : ''}" data-tag="${escapeHTML(tag)}">
                ${escapeHTML(tag)}<span class="n">${n}</span></button>`;
    }).join('');
    const more = index.length > TAGS_COLLAPSED
      ? `<button class="linky" id="moreTags">${state.tagsExpanded
           ? 'Fewer tags' : `+${index.length - TAGS_COLLAPSED} more`}</button>`
      : '';
    el.tagRow.innerHTML = chips
      ? `<span class="facet-label">Tags</span><div class="chips">${chips}${more}</div>` : '';
    el.tagRow.hidden = !chips;
  }

  /* --- every other axis: a row of chips --- */
  el.otherFacets.innerHTML = state.facets
    .filter(a => a !== state.primary)
    .map(a => {
      const chips = [...walkValues(a)].map(({ value, path }) => {
        const n = counted.filter(s =>
          matches(a, s.facets?.[a.key], path) &&
          Object.entries(state.filters).every(([k, v]) =>
            k === a.key || !v ||
            matches(state.facets.find(x => x.key === k), s.facets?.[k], v))
        ).length;
        const on = state.filters[a.key] === path;
        return `<button class="chip ${on ? 'on' : ''}"
                        data-axis="${escapeHTML(a.key)}" data-value="${escapeHTML(path)}"
                        ${n ? '' : 'data-empty="1"'}>
                  ${escapeHTML(value.label || value.slug)}<span class="n">${n}</span>
                </button>`;
      }).join('');
      if (!chips) return '';
      return `<div class="facet-row">
                <span class="facet-label">${escapeHTML(a.label || a.key)}</span>
                <div class="chips">${chips}</div>
              </div>`;
    }).join('');
}

/* ------------------------------------------------------------------ */
/*  Grid                                                               */
/* ------------------------------------------------------------------ */

function describeSelection() {
  const bits = [];
  for (const axis of state.facets) {
    const v = state.filters[axis.key];
    if (v) bits.push(trailFor(axis, v).join(' › '));
  }
  if (state.tags.length) bits.push(state.tags.join(' + '));
  if (state.query.trim()) bits.push(`“${state.query.trim()}”`);
  return bits.join(' · ');
}

function renderGrid(reset = true) {
  if (reset) {
    state.visible = sortStatues(
      applyFilters(state.statues, state.facets, state.filters, state.query, state.tags));
    state.shown = 0;
    state.batches = 0;
    el.grid.innerHTML = '';

    const n = state.visible.length;
    el.count.textContent = `${n} ${n === 1 ? 'piece' : 'pieces'}`;
    const sel = describeSelection();
    el.selection.textContent = sel;
    el.selection.hidden = !sel;
    el.clear.hidden = !sel;
  }

  el.grid.classList.toggle('dense', state.dense);

  if (!state.visible.length) {
    el.empty.hidden = false;
    el.more.hidden = true;
    return;
  }
  el.empty.hidden = true;

  const batch = state.visible.slice(state.shown, state.shown + PAGE);
  if (batch.length) {
    const frag = document.createElement('div');
    frag.innerHTML = batch.map((s, i) => cardHTML(s, state.shown + i)).join('');
    bindCards(frag);
    while (frag.firstElementChild) el.grid.appendChild(frag.firstElementChild);
    state.shown += batch.length;
    state.batches++;
  }

  const left = state.visible.length - state.shown;
  el.more.hidden = left <= 0;
  el.more.textContent = left > 0
    ? `Show ${Math.min(PAGE, left)} more — ${left} remaining` : '';
  el.status.textContent = `${state.shown} of ${state.visible.length} shown`;
}

function update({ replace = false } = {}) {
  writeURL({ replace });
  renderNav();
  renderGrid(true);
}

/* ------------------------------------------------------------------ */
/*  Boot                                                               */
/* ------------------------------------------------------------------ */

async function init() {
  Object.assign(el, {
    crumbs: document.getElementById('crumbs'),
    subjects: document.getElementById('subjects'),
    subjectGroup: document.getElementById('subjectGroup'),
    otherFacets: document.getElementById('otherFacets'),
    tagRow: document.getElementById('tagRow'),
    search: document.getElementById('search'),
    clear: document.getElementById('clearFilters'),
    density: document.getElementById('density'),
    grid: document.getElementById('grid'),
    empty: document.getElementById('empty'),
    more: document.getElementById('more'),
    sentinel: document.getElementById('sentinel'),
    count: document.getElementById('count'),
    selection: document.getElementById('selection'),
    status: document.getElementById('status'),
    total: document.getElementById('totalCount'),
  });

  lightbox = new Lightbox(document.getElementById('lightbox'));

  /* Interactions are wired BEFORE the fetch, so a data problem cannot
     leave the page inert with a dead menu and dead filters. */
  wireChrome();

  let data;
  try {
    data = await loadCollection();
  } catch (err) {
    el.empty.hidden = false;
    el.empty.innerHTML = `<div class="eh">The collection could not be loaded</div>
      <p>${escapeHTML(err.message)}</p>`;
    console.error(err);
    return;
  }

  Object.assign(state, data);
  /* The viewer needs the taxonomy to label a piece and the address to
     send an enquiry to. */
  lightbox.facets = state.facets;
  lightbox.email = state.site?.email || '';
  readURL();

  el.total.textContent = state.statues.length
    ? `${state.statues.length} ${state.statues.length === 1 ? 'piece' : 'pieces'}`
    : 'The collection is waiting for its first pour';
  el.search.value = state.query;
  el.density.setAttribute('aria-pressed', String(state.dense));

  renderNav();
  renderGrid(true);
  openFromURL();
}

function wireChrome() {
  /* Facet chips and breadcrumbs */
  document.getElementById('filters').addEventListener('click', e => {
    const chip = e.target.closest('[data-axis]');
    if (chip) {
      const { axis, value } = chip.dataset;
      state.filters[axis] = state.filters[axis] === value ? null : value;
      if (!state.filters[axis]) delete state.filters[axis];
      update();
      return;
    }
    if (e.target.id === 'moreTags') {
      state.tagsExpanded = !state.tagsExpanded;
      renderNav();
      return;
    }
    const tagBtn = e.target.closest('[data-tag]');
    if (tagBtn) {
      const t = tagBtn.dataset.tag;
      state.tags = state.tags.includes(t)
        ? state.tags.filter(x => x !== t) : [...state.tags, t];
      update();
      return;
    }
    const crumb = e.target.closest('[data-goto]');
    if (crumb) {
      const to = crumb.dataset.goto;
      if (to) state.filters[state.primary.key] = to;
      else delete state.filters[state.primary.key];
      update();
    }
  });

  /* Search — debounced so typing stays smooth over a large collection */
  let t;
  el.search.addEventListener('input', () => {
    clearTimeout(t);
    t = setTimeout(() => {
      state.query = el.search.value;
      update({ replace: true });
    }, 160);
  });
  el.search.addEventListener('keydown', e => {
    if (e.key === 'Escape') { el.search.value = ''; state.query = ''; update({ replace: true }); }
  });

  el.clear.addEventListener('click', () => {
    state.filters = {}; state.query = ''; state.tags = []; el.search.value = '';
    update();
  });

  el.density.addEventListener('click', () => {
    state.dense = !state.dense;
    el.density.setAttribute('aria-pressed', String(state.dense));
    writeURL({ replace: true });
    el.grid.classList.toggle('dense', state.dense);
  });

  el.more.addEventListener('click', () => {
    const first = state.shown;
    renderGrid(false);
    /* Move focus to the first newly added tile so keyboard and screen
       reader users are not dropped back at the top of the grid. */
    el.grid.children[first]?.focus();
  });

  el.grid.addEventListener('click', e => {
    const card = e.target.closest('.piece');
    if (!card) return;
    const i = Number(card.dataset.index);
    lightbox.open(state.visible, Number.isFinite(i) ? i : 0);
  });

  /* Auto-append only the first couple of batches. Past that the reader
     asks, which keeps the footer reachable and the tab order finite. */
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      if (entries.some(en => en.isIntersecting)
          && state.batches < AUTO_BATCHES
          && state.shown < state.visible.length) {
        renderGrid(false);
      }
    }, { rootMargin: '500px' }).observe(el.sentinel);
  }

  /* Drawer */
  const drawer = document.getElementById('drawer');
  const scrim = document.getElementById('scrim');
  const menuBtn = document.getElementById('menuBtn');
  const closeDrawer = () => {
    drawer.classList.remove('show');
    scrim.classList.remove('show');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.focus();
  };
  menuBtn.addEventListener('click', () => {
    drawer.classList.add('show');
    scrim.classList.add('show');
    menuBtn.setAttribute('aria-expanded', 'true');
    drawer.querySelector('a,button')?.focus();
  });
  scrim.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && drawer.classList.contains('show')) closeDrawer();
  });
  drawer.addEventListener('click', e => {
    const b = e.target.closest('[data-axis]');
    if (b) {
      state.filters = { [b.dataset.axis]: b.dataset.value };
      update(); closeDrawer();
    } else if (e.target.closest('[data-close]')) closeDrawer();
  });

  /* Back/forward through filter states */
  window.addEventListener('popstate', () => {
    if (lightbox?.isOpen) return;   // the viewer handles its own history
    readURL();
    el.search.value = state.query;
    renderNav();
    renderGrid(true);
  });
}

/* Deep links: /statues/NFC-0001 and #NFC-0001 both open that piece. */
function openFromURL() {
  const fromHash = location.hash.replace(/^#/, '');
  const fromPath = location.pathname.match(/\/statues\/([^/]+)\/?$/)?.[1];
  const id = fromHash || (fromPath && fromPath !== 'index.html' ? fromPath : '');
  if (!id) return;
  const piece = findById(state.statues, decodeURIComponent(id));
  if (!piece) return;
  let list = state.visible;
  let i = list.indexOf(piece);
  if (i === -1) { list = sortStatues(state.statues); i = list.indexOf(piece); }
  lightbox.open(list, Math.max(0, i));
}

document.addEventListener('DOMContentLoaded', init);
