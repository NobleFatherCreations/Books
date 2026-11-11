#!/usr/bin/env node
// Story lint: mechanical audit of an intro script before any human or critic reads it.
//   node scripts/story-lint.mjs content/fractal2/intro-v8.md
// Scene lines look like:  <!--scene H z=a:b ...--> followed by 1-2 sentences, blank line.
import fs from 'fs';
const f = process.argv[2]; const raw = fs.readFileSync(f, 'utf8');
const scenes = []; let cur = null;
for (const line of raw.split('\n')) {
  if (/^<!--scene /.test(line)) { cur = { text: [] }; scenes.push(cur); continue; }
  if (/^<!--/.test(line) || /^#/.test(line)) { cur = null; continue; }
  if (cur && line.trim()) cur.text.push(line.trim());
}
const text = scenes.map((s) => s.text.join(' ')).join('\n');
const fails = [], warns = [];
const words = text.split(/\s+/).filter(Boolean).length;
if (words > 1300) fails.push(`too long: ${words} words (max 1300)`);
scenes.forEach((s, i) => {
  const t = s.text.join(' '); const n = t.split(/\s+/).length; const sen = (t.match(/[.!?](\s|$)/g) || []).length;
  if (sen > 3) fails.push(`scene ${i + 1} has ${sen} sentences: "${t.slice(0, 50)}..."`);
  if (n > 55) fails.push(`scene ${i + 1} has ${n} words (max 55 for large type): "${t.slice(0, 50)}..."`);
});
const bad = [[/—|–/, 'em/en dash'], [/\bproved\b|\bproof that\b/i, '"proved"/"proof that" overclaim'], [/\bwill heal\b|\bcure[sd]?\b|\bguarantee/i, 'outcome promise'], [/\b(defence|behaviour|colour|honour|favour|realise|organis)/i, 'British spelling'], [/\b140\b|2,340|\bhundreds of combinations/i, 'unapproved number'], [/\bno hiding place\b/i, 'accusation framing flagged by the audit']];
for (const [re, why] of bad) { const m = text.match(re); if (m) fails.push(`${why}: "${m[0]}"`); }
const must = [[/emergency services/i, 'safety line (emergency services)'], [/never people/i, '"names patterns, never people"'], [/one person's sight|to my eye/i, 'lens framing for the spiritual layer'], [/two hundred and three/i, '203 combinations'], [/three hundred and thirty-five/i, '335 tactics'], [/two thousand seven hundred/i, '2,700 examples'], [/original frequency/i, 'original frequency payoff'], [/\bcombination/i, 'combinations introduced'], [/order/i, 'order as the weapon']];
for (const [re, why] of must) if (!re.test(text)) fails.push(`missing: ${why}`);
if ((text.match(/\bcombination/gi) || []).length < 3) warns.push('combinations mentioned fewer than 3 times');
console.log(`scenes: ${scenes.length}, words: ${words}, est. narration: ${(words / 150).toFixed(1)} min`);
warns.forEach((w) => console.log('WARN', w)); fails.forEach((x) => console.log('FAIL', x));
console.log(fails.length ? `STORY LINT FAIL (${fails.length})` : 'STORY LINT PASS'); process.exit(fails.length ? 1 : 0);
