#!/usr/bin/env node
// EXIT GATE for the design process. A build may only be handed off when this passes.
//   node scripts/design-exit.mjs <SCORES.md> <file-or-dir> [<file-or-dir> ...]
// SCORES.md must contain one fenced ```json block: {"threshold":4,"rounds":[{"round":1,"date":"..","sha":"<sha256 of the build files>","scores":{"hierarchy":4,..},"weaknesses":[{"id":"W1","text":"..","status":"open|fixed-verified"}]}]}
// PASS requires: latest round's sha == the current files' sha (i.e. the CURRENT build was scored), every score >= threshold, every weakness fixed-verified.
// Print the sha to record with:  node scripts/design-exit.mjs --sha <file-or-dir> ...
import fs from 'fs'; import path from 'path'; import crypto from 'crypto';
const args = process.argv.slice(2);
const files = (p) => fs.statSync(p).isDirectory() ? fs.readdirSync(p).flatMap((f) => (/\.(html|css|js|py)$/.test(f) ? files(path.join(p, f)) : fs.statSync(path.join(p, f)).isDirectory() ? files(path.join(p, f)) : [])) : [p];
const sha = (paths) => { const h = crypto.createHash('sha256'); for (const f of paths.flatMap(files).sort()) { h.update(f); h.update(fs.readFileSync(f)); } return h.digest('hex'); };
if (args[0] === '--sha') { console.log(sha(args.slice(1))); process.exit(0); }
const [scoresPath, ...targets] = args;
const md = fs.readFileSync(scoresPath, 'utf8'); const m = md.match(/```json\s*([\s\S]*?)```/);
const fail = (msg) => { console.error('EXIT GATE FAIL:', msg); process.exit(1); };
if (!m) fail('no json block in ' + scoresPath);
const L = JSON.parse(m[1]); const th = L.threshold ?? 4; const r = L.rounds?.[L.rounds.length - 1];
if (!r) fail('no scored rounds: the build is UNSCORED');
const cur = sha(targets);
if (r.sha !== cur) fail(`the build changed after round ${r.round} was scored (scored ${r.sha.slice(0, 10)}, now ${cur.slice(0, 10)}): re-score before hand-off`);
const low = Object.entries(r.scores).filter(([, v]) => v < th); if (low.length) fail('scores below ' + th + ': ' + low.map(([k, v]) => `${k}=${v}`).join(', ') + ' -> run the low-score protocol (3 candidate fixes, test, choose), then re-score');
const open = (r.weaknesses || []).filter((w) => w.status !== 'fixed-verified'); if (open.length) fail('open weaknesses: ' + open.map((w) => w.id).join(', '));
console.log(`EXIT GATE PASS: round ${r.round}, all ${Object.keys(r.scores).length} scores >= ${th}, no open weaknesses, scored build = current build`);
