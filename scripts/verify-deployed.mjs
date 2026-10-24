#!/usr/bin/env node
/* =====================================================================
   verify-deployed — is what is committed here the thing being served?

   Ported from the Wookbook repo (scripts/verify-deployed.mjs) and adapted
   to this repo's registry and layout. A commit is not a deploy: this makes
   the gap between them visible.

   Reads sites.json and compares, byte for byte, each project's committed
   file with what its live URL returns:
     - repoPath / localSource   the file we edit and deploy
     - liveSnapshot             a capture, for sites with no source here
     - a directory repoPath     index.html, plus every other top-level
                                .html in it when there is more than one
                                (the faith book is a set of pages)

   A project marked "pendingDeploy" in sites.json is KNOWN to be ahead of
   live (committed, awaiting the owner's go-ahead). It is reported, but it
   does not count as an unexplained drift.

     node scripts/verify-deployed.mjs            # everything
     node scripts/verify-deployed.mjs loop       # one, by slug
     node scripts/verify-deployed.mjs --quiet    # only problems

   Exit: 0 all in sync · 1 unexplained drift · 2 unreachable · 4 only
   known pending deploys remain.
   ===================================================================== */

import { readFile, readdir } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const execFileP = promisify(execFile);
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const args = process.argv.slice(2);
const QUIET = args.includes('--quiet');
const ONLY = args.filter((a) => !a.startsWith('-'));
const C = process.stdout.isTTY
  ? { d: '\x1b[2m', r: '\x1b[0m', g: '\x1b[32m', y: '\x1b[33m', red: '\x1b[31m', b: '\x1b[1m' }
  : { d: '', r: '', g: '', y: '', red: '', b: '' };

async function fetchLive(url) {
  try {
    const { stdout } = await execFileP('curl', ['-sS', '--compressed', '-L', '--max-time', '120',
      '-A', 'Mozilla/5.0 (verify-deployed)', url], { maxBuffer: 1 << 29, encoding: 'buffer' });
    return stdout;
  } catch { return null; }
}

const sites = JSON.parse(await readFile(path.join(ROOT, 'sites.json'), 'utf8'));
const targets = [
  { slug: 'hub', ...sites.hub },
  ...sites.projects,
  ...(sites.craftBusiness || []).map((c) => ({ slug: c.netlifySite, ...c })),
  ...(sites.otherLiveSites || []).map((c) => ({ slug: c.netlifySite, ...c })),
].filter((t) => (ONLY.length ? ONLY.includes(t.slug) : true));

/* what to compare for one target: a list of { rel, abs, url, kind } */
async function pairs(t) {
  const base = t.url.replace(/\/$/, '');
  if (t.liveSnapshot) return [{ rel: t.liveSnapshot, abs: path.join(ROOT, t.liveSnapshot), url: t.url, kind: 'snapshot' }];
  const p = t.repoPath || t.localSource;
  if (!p || /\(/.test(p)) return [];
  const abs = path.join(ROOT, p);
  if (!existsSync(abs)) return [{ rel: p, abs, url: t.url, kind: 'missing' }];
  if (!statSync(abs).isDirectory()) return [{ rel: p, abs, url: t.url, kind: 'source' }];
  const html = (await readdir(abs)).filter((f) => f.endsWith('.html')).sort();
  const files = html.length > 1 ? html : ['index.html'];
  return files.map((f) => ({ rel: path.join(p, f), abs: path.join(abs, f), url: f === 'index.html' ? t.url : `${base}/${f}`, kind: 'source' }));
}

console.log(`\n${C.b}Noble Father Creations — is the repo what is live?${C.r}\n`);
const synced = [], drifted = [], pending = [], unreachable = [], unchecked = [];

for (const t of targets) {
  const label = String(t.slug || '?').padEnd(28);
  const list = await pairs(t);
  if (!list.length) { unchecked.push(t.slug); console.log(`  ${C.y}?${C.r}  ${label} ${C.d}nothing recorded to compare against${C.r}`); continue; }
  let bad = null, n = 0;
  for (const it of list) {
    if (it.kind === 'missing') { bad = { why: `${it.rel} is not on disk` }; break; }
    const [local, live] = [await readFile(it.abs), await fetchLive(it.url)];
    if (live === null || !live.length) { bad = { why: `could not fetch ${it.url}`, unreachable: true }; break; }
    n++;
    if (!local.equals(live)) { bad = { why: `${it.rel} ${local.length > live.length ? `has ${local.length - live.length} bytes MORE than live` : `is ${live.length - local.length} bytes shorter than live`}`, kind: it.kind }; break; }
  }
  if (!bad) { synced.push(t.slug); if (!QUIET) console.log(`  ${C.g}✓${C.r}  ${label} ${C.d}${n} file${n > 1 ? 's' : ''} identical to live${list[0].kind === 'snapshot' ? ' (snapshot)' : ''}${C.r}`); }
  else if (bad.unreachable) { unreachable.push(t.slug); console.log(`  ${C.y}!${C.r}  ${label} ${C.y}${bad.why}${C.r}`); }
  else if (t.pendingDeploy) { pending.push(t.slug); console.log(`  ${C.y}~${C.r}  ${label} ${C.y}PENDING DEPLOY${C.r} ${C.d}— ${bad.why}; ${t.pendingDeploy.note.split('.')[0]}.${C.r}`); }
  else { drifted.push(t.slug); console.log(`  ${C.red}✗${C.r}  ${label} ${C.red}${bad.kind === 'snapshot' ? 'CHANGED SINCE CAPTURE' : 'DRIFTED'}${C.r} — ${bad.why}`); }
}

console.log(`\n${C.b}── summary ──${C.r}  in sync ${synced.length} · pending deploy ${pending.length} · drifted ${drifted.length} · unreachable ${unreachable.length} · unchecked ${unchecked.length}\n`);
if (drifted.length) { console.log(`${C.red}Unexplained drift: ${drifted.join(', ')}. Decide which side is right before editing either.${C.r}\n`); process.exit(1); }
if (unreachable.length) process.exit(2);
if (pending.length) process.exit(4);
