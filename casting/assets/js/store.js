/* =====================================================================
   store.js — loads and normalises the collection.

   Everything the gallery renders comes from three JSON files:
     data/statues.json    the pieces
     data/facets.json     the taxonomy — which axes exist and their values
     data/site.json       name, contact, links

   No axis, value or label is named anywhere in the JavaScript or the
   HTML. Renaming "Cats" or adding a whole new axis is a data edit.
   ===================================================================== */

import { matches, primaryAxis } from './facets.js';

const DATA = {
  statues: '/data/statues.json',
  facets: '/data/facets.json',
  site: '/data/site.json',
};

async function getJSON(url, fallback) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) {
    if (fallback !== undefined) return fallback;
    throw new Error(`${url} → HTTP ${res.status}`);
  }
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${url} is not valid JSON. Check for a trailing comma.`);
  }
}

/* --- normalisation ------------------------------------------------- */

/* A photo is stored as its master path and nothing else — every rendered
   size is derived at runtime by images.js.

   Three written forms are accepted so the JSON stays comfortable to edit
   by hand and older entries keep working:
     "…/main.webp"                        a bare path
     { master: "…/main.webp" }            what the ingest script writes
     { detail: "…", thumb: "…" }          pre-derived paths (legacy)
*/
function normaliseAngle(angle, i) {
  if (typeof angle === 'string') {
    return { label: `View ${i + 1}`, master: angle, width: null, height: null, bg: null };
  }
  const master = angle.master || angle.detail || angle.src || angle.thumb;
  return {
    label: angle.label || `View ${i + 1}`,
    master,
    /* Real renditions written at ingest: [{w, src}, …] smallest first. */
    sizes: Array.isArray(angle.sizes)
      ? angle.sizes.filter(x => x && x.src && x.w).sort((a, b) => a.w - b.w)
      : null,
    width: angle.width ?? null,
    height: angle.height ?? null,
    /* Dominant colour sampled from the photo at ingest, used to paint the
       tile behind it so off-spec framing letterboxes into its own ground. */
    bg: angle.bg || null,
    alt: angle.alt || null,
    fixed: angle.thumb && angle.detail
      ? { thumb: angle.thumb, detail: angle.detail }
      : null,
  };
}

function normaliseStatue(raw) {
  /* One malformed entry must not blank the whole gallery, so anything
     unusable is skipped rather than thrown on. A non-developer editing a
     large JSON file by hand is the likeliest source of an outage. */
  if (!raw || typeof raw !== 'object') return null;

  const id = String(raw.id || '').trim();
  if (!id) return null;

  const angles = Array.isArray(raw.angles)
    ? raw.angles.map(normaliseAngle).filter(a => a && a.master)
    : [];
  if (!angles.length) return null;

  /* Legacy single-category entries are read as a subject, so a
     collection ingested before the facet model still displays. */
  const facets = { ...(raw.facets || {}) };
  if (!Object.keys(facets).length && raw.category) facets.subject = String(raw.category);

  return {
    id,
    title: raw.title || null,
    facets,
    tags: Array.isArray(raw.tags) ? raw.tags.filter(t => typeof t === 'string') : [],
    angles,
    dateAdded: raw.dateAdded || null,
    description: raw.description || null,
    needsReview: raw.needsReview === true,
    /* Pre-lowered haystack so search over 1000 pieces stays instant. */
    _search: [id, raw.title, raw.description, ...(raw.tags || []),
              ...Object.values(facets)].filter(Boolean).join(' ').toLowerCase(),
  };
}

/* --- public API ---------------------------------------------------- */

export async function loadCollection() {
  const [rawStatues, rawFacets, site] = await Promise.all([
    getJSON(DATA.statues),
    getJSON(DATA.facets, []),
    getJSON(DATA.site, {}),
  ]);

  const statues = (Array.isArray(rawStatues) ? rawStatues : [])
    .map(normaliseStatue)
    .filter(Boolean);

  const facets = (Array.isArray(rawFacets) ? rawFacets : [])
    .filter(a => a && a.key);

  return { statues, facets, site, primary: primaryAxis(facets) };
}

/* Newest first, then by id so order is stable between reloads. */
export function sortStatues(list) {
  return [...list].sort((a, b) => {
    const d = (b.dateAdded || '').localeCompare(a.dateAdded || '');
    return d !== 0 ? d : a.id.localeCompare(b.id);
  });
}

/**
 * Apply the active facet selections and the search box.
 * @param {object} filters  { [axisKey]: path }
 * @param {string} query
 */
export function applyFilters(statues, facets, filters, query, tags = []) {
  const q = String(query || '').trim().toLowerCase();
  const terms = q ? q.split(/\s+/) : [];
  const want = tags.filter(Boolean);

  return statues.filter(s => {
    for (const axis of facets) {
      const v = filters[axis.key];
      if (!v) continue;
      if (!matches(axis, s.facets?.[axis.key], v)) return false;
    }
    /* Tags narrow: picking "witchy" and "frog" means both, not either. */
    if (want.length && !want.every(t => s.tags.includes(t))) return false;
    /* Every search term must appear somewhere, so "white cat" narrows. */
    return terms.every(t => s._search.includes(t));
  });
}

/** Distinct tags with counts, most used first — the tag filter reads this. */
export function tagIndex(statues) {
  const counts = new Map();
  for (const s of statues) for (const t of s.tags) counts.set(t, (counts.get(t) || 0) + 1);
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([tag, n]) => ({ tag, n }));
}

export function findById(statues, id) {
  if (!id) return null;
  const needle = String(id).toLowerCase();
  return statues.find(s => s.id.toLowerCase() === needle) || null;
}
