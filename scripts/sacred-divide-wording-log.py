#!/usr/bin/env python3
"""Write logs/wording-log/<id>.md from content/sacred-divide/edits/*.json and logs/edits-status.json.
Every edit appears as a before/after pair with its reason, grouped by type. To reject one, set its
"status" to "rejected" in the JSON (or delete it) and rebuild."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ED = os.path.join(ROOT, 'content/sacred-divide/edits'); OUT = os.path.join(ROOT, 'logs/wording-log')
st = json.load(open(os.path.join(ROOT, 'logs/edits-status.json'))) if os.path.exists(os.path.join(ROOT, 'logs/edits-status.json')) else {}
TYPES = {'meta': 'Edition and version narration removed', 'fragment': 'Fragments completed into sentences', 'gloss': 'Specialist terms glossed on first use',
         'loop': 'Loops expanded (section 13)', 'grade-rationale': 'Evidence-grade notes matched to their technique', 'label': 'Labels and headings',
         'proof': 'Proofreading (typos, punctuation, agreement)', 'clarity': 'Sentences completed or clarified', 'status': 'Time-sensitive status lines'}
os.makedirs(OUT, exist_ok=True)
def q(t): return '\n'.join('> ' + l if l else '>' for l in t.split('\n'))
def write(rid, entries, status):
    by = {}
    for e in entries: by.setdefault(e.get('type', 'clarity'), []).append(e)
    S = {r['id']: r['state'] for r in status}
    L = [f'# Wording log — {rid}', '', f'{len(entries)} edits. Reject any one by setting `"status": "rejected"` on its entry in `content/sacred-divide/edits/{rid if rid != "_all" else "_all"}.json`, then rebuild. Nothing else changes.', '']
    for t, es in by.items():
        L += [f'## {TYPES.get(t, t)} ({len(es)})', '']
        for e in es:
            L += [f'### {e["id"]} · {e.get("scope", "md")}' + (f' · §{e["section"]}' if e.get('section') else '') + f' · {e.get("status", "proposed")} · build: {S.get(e["id"], "not yet built")}',
                  '', '**Before**', '', q(e.get('before_text', e['before'])), '', '**After**', '', q(e.get('after_text', e['after'])) if e['after'] else '> *(removed)*', '', f'*Reason:* {e.get("reason", "")}', '']
    open(os.path.join(OUT, f'{rid}.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
for fn in sorted(os.listdir(ED)):
    if not fn.endswith('.json'): continue
    rid = fn[:-5]; es = json.load(open(os.path.join(ED, fn), encoding='utf-8'))
    status = [] if rid == '_all' else st.get(rid, [])
    if rid == '_all':
        agg = {}
        for v in st.values():
            for r in v: agg.setdefault(r['id'], []).append(r['found'])
        status = [{'id': k, 'state': f'applied {sum(v)} time(s) across {sum(1 for x in v if x)} volume(s)'} for k, v in agg.items()]
    write(rid, es, status)
    print(rid, len(es))
