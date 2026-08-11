#!/usr/bin/env node
/* =====================================================================
   validate-data.js — sanity-check the collection data.

   Run after hand-editing statues.json or facets.json:
       npm run validate

   Catches the mistakes that hand editing actually produces: a duplicate
   id, a category that no longer exists, a missing image file, a piece
   with no angles.
   ===================================================================== */

import { existsSync } from 'node:fs';
import path from 'node:path';
import { PATHS, ROOT, say, readJSON } from './lib/util.js';
import { findValue, walkValues } from './lib/facets.js';

const problems = [];
const notes = [];

function fail(m) { problems.push(m); }
function note(m) { notes.push(m); }

const statues = await readJSON(PATHS.statues, []);
const facets = await readJSON(PATHS.facets, []);

if (!Array.isArray(statues)) fail('statues.json must be a JSON array.');
if (!Array.isArray(facets)) fail('facets.json must be a JSON array.');

const axes = new Map();
for (const a of facets) {
  if (!a || typeof a !== 'object') { fail('facets.json holds a non-object entry.'); continue; }
  if (!a.key) { fail('A facet axis is missing its "key".'); continue; }
  if (axes.has(a.key)) fail(`Duplicate facet axis "${a.key}".`);
  axes.set(a.key, a);

  const seen = new Set();
  for (const { value, path } of walkValues(a)) {
    if (!value.slug) fail(`Axis "${a.key}" has a value with no slug.`);
    if (seen.has(path)) fail(`Axis "${a.key}" declares "${path}" twice.`);
    seen.add(path);
    if (!value.label) note(`"${a.key}/${path}" has no label — the slug will show instead.`);
  }
}
if (facets.length && !facets.some(a => a.primary)) {
  note('No axis is marked "primary" — the first one will drive the main navigation.');
}

const ids = new Set();
let unfiled = 0, missingImages = 0, review = 0;

for (const s of statues) {
  if (!s || typeof s !== 'object') { fail('statues.json holds a non-object entry.'); continue; }

  if (!s.id) { fail('A piece is missing its "id".'); continue; }
  if (ids.has(String(s.id).toUpperCase())) fail(`Duplicate piece id "${s.id}".`);
  ids.add(String(s.id).toUpperCase());

  if (!Array.isArray(s.angles) || !s.angles.length) {
    fail(`"${s.id}" has no angles — it will not appear in the gallery.`);
    continue;
  }

  for (const a of s.angles) {
    const paths = typeof a === 'string'
      ? [a]
      : [a.master, ...(a.sizes || []).map(x => x?.src),
         a.thumb, a.detail].filter(Boolean);
    if (typeof a === 'object' && !paths.length) {
      fail(`"${s.id}" has an angle with no image path.`);
      continue;
    }
    for (const p of paths) {
      /* Remote URLs and Netlify Image CDN transforms are generated on
         request, so there is nothing on disk to check. Verify the master
         the transform points at instead. */
      if (/^https?:\/\//.test(p)) continue;
      let target = p;
      if (p.startsWith('/.netlify/images')) {
        const url = new URL(p, 'https://local');
        target = url.searchParams.get('url');
        if (!target) { fail(`"${s.id}" has a CDN URL with no source: ${p}`); continue; }
      }
      const abs = path.join(ROOT, decodeURIComponent(target).replace(/^\//, ''));
      if (!existsSync(abs)) { fail(`"${s.id}" references a missing file: ${target}`); missingImages++; }
    }
  }

  const assigned = s.facets && typeof s.facets === 'object' ? s.facets : {};
  if (!Object.keys(assigned).length) unfiled++;
  for (const [key, value] of Object.entries(assigned)) {
    const axis = axes.get(key);
    if (!axis) {
      fail(`"${s.id}" uses facet axis "${key}", which is not declared in facets.json. ` +
           `It will not be filterable.`);
    } else if (!findValue(axis, value)) {
      fail(`"${s.id}" is filed at ${key}="${value}", which that axis does not declare. ` +
           `The piece will be unreachable from the navigation.`);
    }
  }

  if (s.needsReview) review++;
}

say.head('Collection data check');
say.info(`${statues.length} piece(s) across ${facets.length} facet axis/axes`);
if (unfiled) say.info(`${unfiled} piece(s) not filed on any axis`);
if (review) say.warn(`${review} piece(s) still flagged for review`);
if (missingImages) say.warn(`${missingImages} missing image file(s)`);

for (const n of notes) say.warn(n);

if (problems.length) {
  say.head(`${problems.length} problem(s) found`);
  for (const p of problems) say.err(p);
  process.exit(1);
}

say.ok('Data is valid.');
