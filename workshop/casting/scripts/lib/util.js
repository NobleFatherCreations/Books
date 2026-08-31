/* Shared helpers for the ingest and category scripts. */

import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

export const PATHS = {
  statues: path.join(ROOT, 'data/statues.json'),
  facets: path.join(ROOT, 'data/facets.json'),
  site: path.join(ROOT, 'data/site.json'),
  manifest: path.join(ROOT, 'data/.ingest-manifest.json'),
  incoming: path.join(ROOT, 'incoming'),
  images: path.join(ROOT, 'assets/images/statues'),
};

/* --- terminal ----------------------------------------------------- */
const C = {
  reset: '\x1b[0m', dim: '\x1b[2m', bold: '\x1b[1m',
  gold: '\x1b[33m', green: '\x1b[32m', red: '\x1b[31m', cyan: '\x1b[36m',
};
export const say = {
  head: m => console.log(`\n${C.bold}${C.gold}${m}${C.reset}`),
  info: m => console.log(`  ${m}`),
  dim: m => console.log(`  ${C.dim}${m}${C.reset}`),
  ok: m => console.log(`  ${C.green}✓${C.reset} ${m}`),
  warn: m => console.log(`  ${C.gold}!${C.reset} ${m}`),
  err: m => console.error(`  ${C.red}✗${C.reset} ${m}`),
  step: m => console.log(`  ${C.cyan}→${C.reset} ${m}`),
};

/* --- JSON --------------------------------------------------------- */
export async function readJSON(file, fallback) {
  if (!existsSync(file)) return fallback;
  const raw = await readFile(file, 'utf8');
  if (!raw.trim()) return fallback;
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error(`${path.relative(ROOT, file)} is not valid JSON — ${err.message}`);
  }
}

/* Written with a trailing newline and two-space indent so hand edits and
   script edits produce identical formatting, keeping git diffs readable. */
export async function writeJSON(file, data) {
  await mkdir(path.dirname(file), { recursive: true });
  await writeFile(file, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

export async function hashFile(file) {
  const buf = await readFile(file);
  return createHash('sha256').update(buf).digest('hex').slice(0, 16);
}

/* --- strings ------------------------------------------------------ */
export function slugify(s) {
  return String(s).toLowerCase().trim()
    .replace(/['']/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function titleCase(s) {
  return String(s).replace(/[-_]+/g, ' ').trim()
    .replace(/\b\w/g, m => m.toUpperCase());
}

export function today() {
  return new Date().toISOString().slice(0, 10);
}

/* --- args --------------------------------------------------------- */
/* Parses `--key value`, `--key=value` and bare `--flag` into an object.
   A flag repeated more than once collects into an array, so
   `--set a=1 --set b=2` keeps both rather than the last one winning. */
export function parseArgs(argv = process.argv.slice(2)) {
  const out = { _: [] };

  const put = (key, value) => {
    if (!(key in out)) { out[key] = value; return; }
    if (Array.isArray(out[key])) out[key].push(value);
    else out[key] = [out[key], value];
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { out._.push(a); continue; }
    const eq = a.indexOf('=');
    if (eq > -1) {
      put(a.slice(2, eq), a.slice(eq + 1));
    } else {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { put(key, next); i++; }
      else put(key, true);
    }
  }
  return out;
}

/* Expands "NFC-0001..NFC-0050" into every id in between. The numeric width
   of the first id is preserved, so NFC-0001 stays four digits. */
export function expandRange(spec) {
  const m = String(spec).match(/^(.*?)(\d+)\s*\.\.\s*(?:(.*?))?(\d+)$/);
  if (!m) return null;
  const [, prefixA, startStr, prefixB, endStr] = m;
  if (prefixB && prefixB !== prefixA) return null;

  const start = parseInt(startStr, 10);
  const end = parseInt(endStr, 10);
  if (Number.isNaN(start) || Number.isNaN(end) || end < start) return null;

  const pad = startStr.length;
  const ids = [];
  for (let n = start; n <= end; n++) {
    ids.push(prefixA + String(n).padStart(pad, '0'));
  }
  return ids;
}
