/* =====================================================================
   facets.js — the taxonomy.

   The collection is classified on several INDEPENDENT axes at once. A
   single piece is, for example, both  subject = pets/cats  and
   form = incense-burner. A one-category-per-piece model cannot express
   that, which is why pieces carry a `facets` object rather than a
   `category` string.

   Every axis is declared in data/facets.json. Adding an axis, adding a
   value, renaming a label or nesting a child is a data edit — no code in
   this repo names a subject or a type.

       [{ key, label, hierarchical, primary, values: [
            { slug, label, description, children? } ] }]

   Hierarchical values are addressed by a "/"-joined path: "pets/cats".
   A piece filed at "pets/cats" matches a filter for "pets" as well.
   ===================================================================== */

/** Walk every value in an axis, depth-first, yielding {value, path, depth, parents}. */
export function* walkValues(axis, values = axis.values, parents = []) {
  for (const v of values || []) {
    const path = [...parents.map(p => p.slug), v.slug].join('/');
    yield { value: v, path, depth: parents.length, parents };
    if (v.children?.length) yield* walkValues(axis, v.children, [...parents, v]);
  }
}

/** Flat list of every declared path in an axis, e.g. ["pets","pets/cats"]. */
export function axisPaths(axis) {
  return [...walkValues(axis)].map(e => e.path);
}

/** Find one value by its path. Returns {value, path, depth, parents} or null. */
export function findValue(axis, path) {
  if (!path) return null;
  const want = String(path).toLowerCase();
  for (const entry of walkValues(axis)) {
    if (entry.path.toLowerCase() === want) return entry;
  }
  return null;
}

const slug = s => String(s).toLowerCase().trim()
  .replace(/['']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

/**
 * Match a single folder segment against one axis, by slug OR by label.
 *
 * Folders get named the way a person writes — "Incense Burners", "Jars &
 * Containers" — while slugs are singular and machine-shaped
 * ("incense-burner"). Matching the label too is what stops a correctly
 * named folder from being read as an unknown value and inventing a
 * duplicate branch of the taxonomy.
 *
 * `under` scopes the search to the children of an already-matched parent
 * so "Cats" only matches beneath "Pets".
 */
export function findSegment(axis, segment, under = null) {
  const want = slug(segment);
  if (!want) return null;

  for (const entry of walkValues(axis)) {
    if (under !== null && entry.parents.map(p => p.slug).join('/') !== under) continue;
    if (entry.value.slug.toLowerCase() === want) return entry;
    if (entry.value.label && slug(entry.value.label) === want) return entry;
  }
  return null;
}

/** Human label for a path: "pets/cats" → "Cats". Falls back to the slug. */
export function labelFor(axis, path) {
  const hit = findValue(axis, path);
  if (hit) return hit.value.label || hit.value.slug;
  const leaf = String(path || '').split('/').pop() || '';
  return leaf.replace(/[-_]/g, ' ').replace(/\b\w/g, m => m.toUpperCase());
}

/** Full label trail: "pets/cats" → ["Pets","Cats"]. */
export function trailFor(axis, path) {
  const hit = findValue(axis, path);
  if (!hit) return [labelFor(axis, path)];
  return [...hit.parents.map(p => p.label || p.slug), hit.value.label || hit.value.slug];
}

/**
 * Does a piece's value satisfy a filter?
 * Hierarchical axes match on prefix, so filtering "pets" returns every
 * cat and dog too. Non-hierarchical axes match exactly.
 */
export function matches(axis, pieceValue, filterPath) {
  if (!filterPath) return true;
  if (!pieceValue) return false;
  const p = String(pieceValue).toLowerCase();
  const f = String(filterPath).toLowerCase();
  if (!axis?.hierarchical) return p === f;
  return p === f || p.startsWith(f + '/');
}

/** The axis intended as the main navigation. Falls back to the first. */
export function primaryAxis(facets) {
  return facets.find(a => a.primary) || facets[0] || null;
}

/**
 * Add a value to an axis, creating parents as needed. Returns the value.
 * Used by ingest when a folder introduces a subject that is not yet
 * declared, so nothing a photographer invents gets silently dropped.
 */
export function ensureValue(axis, path, { label } = {}) {
  const parts = String(path).split('/').filter(Boolean);
  let list = axis.values ||= [];
  let node = null;

  parts.forEach((slug, i) => {
    node = list.find(v => v.slug === slug);
    if (!node) {
      node = {
        slug,
        label: i === parts.length - 1 && label
          ? label
          : slug.replace(/[-_]/g, ' ').replace(/\b\w/g, m => m.toUpperCase()),
        description: null,
      };
      if (axis.hierarchical) node.children = [];
      list.push(node);
    }
    if (i < parts.length - 1) {
      node.children ||= [];
      list = node.children;
    }
  });

  return node;
}

/** Count pieces per path, propagating child counts up to parents. */
export function countByPath(axis, statues) {
  const counts = new Map();
  for (const s of statues) {
    const v = s.facets?.[axis.key];
    if (!v) continue;
    const parts = String(v).split('/');
    /* A cat counts toward "pets" as well as "pets/cats". */
    for (let i = 1; i <= parts.length; i++) {
      const p = parts.slice(0, i).join('/');
      counts.set(p, (counts.get(p) || 0) + 1);
    }
  }
  return counts;
}
