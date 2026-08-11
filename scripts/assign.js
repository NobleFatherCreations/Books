#!/usr/bin/env node
/* =====================================================================
   assign.js — file pieces onto facet axes after ingest.

   Folders in incoming/ already do most of this automatically. This is
   for the corrections afterwards: a batch shot before you decided on a
   category, a piece filed in the wrong place, a whole axis added later.

     npm run assign -- --list
     npm run assign -- --range NFC-0001..NFC-0050 --set subject=pets/cats
     npm run assign -- --ids NFC-0007,NFC-0012 --set form=jar
     npm run assign -- --unfiled subject --set subject=skulls
     npm run assign -- --range NFC-0001..NFC-0020 --set finish=white
     npm run assign -- --clear subject --ids NFC-0009

   Several --set flags may be combined; each names one axis.
   Add --dry-run to preview. Values are checked against data/facets.json,
   so a typo is refused rather than quietly making a piece unreachable.
   ===================================================================== */

import { PATHS, say, readJSON, writeJSON, parseArgs, expandRange } from './lib/util.js';
import { findValue, walkValues, countByPath } from './lib/facets.js';

const args = parseArgs();
const DRY = args['dry-run'] === true;

const asList = v => (Array.isArray(v) ? v : v ? [v] : []);

function resolveIds(statues) {
  if (args.range) {
    const ids = expandRange(args.range);
    if (!ids) { say.err(`Could not read the range "${args.range}"`); process.exit(1); }
    return ids;
  }
  if (args.ids) return String(args.ids).split(',').map(s => s.trim()).filter(Boolean);
  if (args.unfiled) {
    const key = String(args.unfiled);
    return statues.filter(s => !s.facets?.[key]).map(s => s.id);
  }
  if (args.all) return statues.map(s => s.id);
  return null;
}

async function main() {
  const statues = await readJSON(PATHS.statues, []);
  const facets = await readJSON(PATHS.facets, []);
  const axes = new Map(facets.map(a => [a.key, a]));

  /* ---- --list ---- */
  if (args.list) {
    say.head(`Collection — ${statues.length} piece(s)`);
    for (const axis of facets) {
      const counts = countByPath(axis, statues);
      const unfiled = statues.filter(s => !s.facets?.[axis.key]).length;
      say.info(`${axis.label || axis.key}  (${axis.key})`);
      for (const { value, path, depth } of walkValues(axis)) {
        say.dim(`  ${'  '.repeat(depth)}${String(counts.get(path) || 0).padStart(4)}  ${path}`);
      }
      if (unfiled) say.dim(`  ${String(unfiled).padStart(4)}  (not filed)`);
    }
    return;
  }

  const ids = resolveIds(statues);
  if (!ids) {
    say.err('Choose what to change: --range, --ids, --unfiled <axis> or --all');
    process.exit(1);
  }

  const byId = new Map(statues.map(s => [String(s.id).toUpperCase(), s]));

  /* ---- --clear <axis> ---- */
  if (args.clear) {
    const key = String(args.clear);
    if (!axes.has(key)) { say.err(`No facet axis "${key}"`); process.exit(1); }
    let n = 0;
    for (const id of ids) {
      const s = byId.get(String(id).toUpperCase());
      if (s?.facets?.[key]) { delete s.facets[key]; n++; }
    }
    say.ok(`Cleared ${key} on ${n} piece(s)`);
    if (!DRY) await writeJSON(PATHS.statues, statues);
    else say.warn('DRY RUN — nothing written');
    return;
  }

  /* ---- --tags a,b,c  /  --untag a,b ---- */
  if (args.tags || args.untag) {
    const add = String(args.tags || '').split(',').map(t => t.trim().toLowerCase()).filter(Boolean);
    const drop = new Set(String(args.untag || '').split(',')
      .map(t => t.trim().toLowerCase()).filter(Boolean));
    let n = 0;
    for (const id of ids) {
      const s = byId.get(String(id).toUpperCase());
      if (!s) continue;
      const before = JSON.stringify(s.tags || []);
      /* --replace-tags swaps the whole set; otherwise tags accumulate,
         which is what you want when tagging a batch a trait at a time. */
      const base = args['replace-tags'] ? [] : (s.tags || []);
      s.tags = [...new Set([...base, ...add])].filter(t => !drop.has(t)).sort();
      if (JSON.stringify(s.tags) !== before) n++;
    }
    say.ok(`${n} piece(s) retagged`);
    if (!DRY) await writeJSON(PATHS.statues, statues);
    else say.warn('DRY RUN — nothing written');
    if (!args.set) return;
  }

  /* ---- --set axis=value ---- */
  const sets = {};
  for (const pair of asList(args.set)) {
    const i = String(pair).indexOf('=');
    if (i < 0) { say.err(`--set needs axis=value, got "${pair}"`); process.exit(1); }
    const key = pair.slice(0, i).trim();
    const value = pair.slice(i + 1).trim().toLowerCase();

    const axis = axes.get(key);
    if (!axis) {
      say.err(`No facet axis "${key}". Declared axes: ${[...axes.keys()].join(', ')}`);
      process.exit(1);
    }
    /* Refuse a value the taxonomy does not declare — filing a piece at a
       path no filter offers would silently hide it from the site. */
    if (!findValue(axis, value)) {
      say.err(`"${value}" is not a declared value of "${key}".`);
      say.info('Valid values:');
      for (const { path } of walkValues(axis)) say.dim(`  ${path}`);
      process.exit(1);
    }
    sets[key] = value;
  }

  if (!Object.keys(sets).length) {
    say.err('Nothing to set. Use --set axis=value, or --clear axis.');
    process.exit(1);
  }

  let changed = 0;
  const missing = [];
  for (const id of ids) {
    const s = byId.get(String(id).toUpperCase());
    if (!s) { missing.push(id); continue; }
    s.facets ||= {};
    let touched = false;
    for (const [k, v] of Object.entries(sets)) {
      if (s.facets[k] !== v) { s.facets[k] = v; touched = true; }
    }
    if (touched) changed++;
  }

  say.head(`Filing ${ids.length} piece(s)`);
  for (const [k, v] of Object.entries(sets)) say.ok(`${k} = ${v}`);
  say.info(`${changed} piece(s) changed`);
  if (missing.length) {
    say.warn(`${missing.length} id(s) not in the collection — ignored`);
    say.dim(missing.slice(0, 10).join(', ') + (missing.length > 10 ? ' …' : ''));
  }

  if (DRY) { say.warn('DRY RUN — nothing written'); return; }
  await writeJSON(PATHS.statues, statues);
  say.ok('data/statues.json updated');
  say.dim('Then rebuild the pages:  npm run pages');
}

main().catch(err => { say.err(err.stack || err.message); process.exit(1); });
