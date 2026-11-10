#!/usr/bin/env python3
"""Audit the compiled design bundle: referenced paths exist, no stray placeholders, categories line up, key sections present.
   python3 scripts/audit-design-bundle.py        (exit 1 on problems)"""
import os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, 'docs', 'design-catalogue', 'bundle')
problems, notes = [], []
docs = {os.path.basename(p): open(p, encoding='utf-8').read() for p in sorted(glob.glob(os.path.join(B, '[1-5]-*.md')))}
roots = ('scripts/', 'docs/', 'references/', 'content/', 'design/', 'library/', 'tools/', 'instruments/', '.claude/', 'vendor/', 'hub/', 'workshop/')
seen = {}
for name, t in docs.items():
    for m in re.finditer(r'`([^`\n]{3,120})`', t):
        s = m.group(1).strip()
        s = re.sub(r'[,;:)]+$', '', s)
        if not s.startswith(roots) or any(c in s for c in '<>*{}|') or ' ' in s or '…' in s or '...' in s:
            continue
        p = s.split('#')[0].rstrip('/')
        if re.search(r'\.(py|mjs|js|md|json|html|jsonl|sh|css|txt)$', p) or os.path.isdir(os.path.join(ROOT, p)) or p.endswith('/'):
            seen.setdefault(p, set()).add(name)
missing = []
for p, ns in sorted(seen.items()):
    if not os.path.exists(os.path.join(ROOT, p)) and not glob.glob(os.path.join(ROOT, p)):
        missing.append((p, sorted(ns)))
# paths that are intentionally templates or future project files
allowed_missing = ('content/<project>', 'content/fractal2/REFERENCES.md', 'content/fractal2/DESIGN-CHOICES.md', 'content/fractal2/COVERAGE.md', 'content/fractal2/PHONE-CHECK.md',
                   'content/fractal2/DESIGN-DIRECTION-v2.md', 'vendor/MANIFEST.json', 'vendor/<pkg>', 'content/fractal2/DESIGN-NOTES.md')
for p, ns in missing:
    if p.startswith(allowed_missing) or p.startswith('references/shots'):
        continue
    problems.append(f'referenced path does not exist: {p}  (in {", ".join(ns)})')
# placeholders
for name, t in docs.items():
    for m in re.finditer(r'\b(TODO|TBD|FIXME|XXX|lorem ipsum)\b', t):
        problems.append(f'placeholder {m.group(1)} in {name}')
# coverage rows vs bible categories
bible = re.findall(r'^#{3,5} (\d+)\. ', docs['2-CATALOGUE.md'], re.M)
cov = re.findall(r'^\| (\d+) \| ', docs['3-RULES-PROCESS-GATES.md'], re.M)
if len(set(bible)) != 56:
    notes.append(f'names bible categories found: {len(set(bible))} (expected 56; heading depth may differ)')
if len(set(cov)) < 56:
    problems.append(f'coverage template rows found: {len(set(cov))} (expected >= 56)')
# key sections
need = {'1-START-HERE.md': ['Glossary', 'Ten questions', 'Master prompt', 'opening interview', 'Using this outside'],
        '2-CATALOGUE.md': ['Master names bible', 'Techniques'],
        '3-RULES-PROCESS-GATES.md': ['Choosing and combining', 'Bake-off', 'iOS plan', 'Coverage template', 'Template: OWNER-TASTE.md', 'Template: PHONE-CHECK.md'],
        '4-DATA-AND-RESOURCES.md': ['Award winners', 'Free resources directory', 'Reference library'],
        '5-HTML-BOOKS-PLAYBOOK.md': ['Non-negotiables', 'Per-book design seeds', 'PASTE-READY PROMPT']}
for d, keys in need.items():
    for k in keys:
        if k.lower() not in docs[d].lower():
            problems.append(f'{d}: missing section text "{k}"')
# script options documented vs implemented
gates = open(os.path.join(ROOT, 'scripts', 'design-gates.mjs')).read()
for flag in ['--baseline', '--engine', '--profiles', '--max', '--no-motion', '--no-pixels']:
    if flag not in gates:
        problems.append(f'documented gates flag not implemented: {flag}')
print('documents:', {k: len(v.split()) for k, v in docs.items()})
print('distinct repo paths referenced:', len(seen), '| missing (after allowances):', len([1 for p, _ in missing if not (p.startswith(allowed_missing) or p.startswith('references/shots'))]))
for n in notes:
    print('NOTE', n)
for p in problems:
    print('PROBLEM', p)
print('AUDIT', 'FAILED' if problems else 'PASSED')
sys.exit(1 if problems else 0)
