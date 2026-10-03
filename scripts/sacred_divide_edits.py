"""The Sacred Divide — reversible wording edits (proofing, fragment completion, glosses, meta-narration removal).

Every edit is one entry in a JSON list, so any single edit can be rejected without touching the rest:

    content/sacred-divide/edits/_all.json    applies to every volume
    content/sacred-divide/edits/<id>.json    applies to one volume

    {"id": "CATH-W012", "scope": "md", "type": "fragment", "section": 8,
     "before": "exact text", "after": "replacement", "reason": "one line", "count": 1, "status": "proposed"}

scope   md         the exported religion Markdown (content/sacred-divide/religions/<id>.md)
        narration  the "Before you read" / "Why this matters" / question-expansion text
        howto      the shared "How to read this" page
count   how many times `before` must occur (default 1). "any" = zero or more (for global clean-ups).
status  proposed | approved | rejected. Anything but "rejected" is applied; the log shows which is which.

A miss (wrong count) never applies silently: the entry is reported as FAILED in logs/edits-status.json and,
with EDITS_STRICT=1, the build stops. Edits apply in file order, _all.json first.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EDITS = os.path.join(ROOT, 'content/sacred-divide/edits')
STATUS = os.path.join(ROOT, 'logs/edits-status.json')
_cache, _tally = {}, {}


def load(rid):
    if rid in _cache:
        return _cache[rid]
    out = []
    for fn in ('_all.json', f'{rid}.json'):
        p = os.path.join(EDITS, fn)
        if os.path.exists(p):
            for e in json.load(open(p, encoding='utf-8')):
                e = dict(e, _file=fn)
                out.append(e)
    _cache[rid] = out
    return out


def apply(text, rid, scope):
    """Apply every non-rejected edit of this scope. Counts are tallied per (rid, id) so narration, which arrives
    one box at a time, is checked once at the end by check()."""
    for e in load(rid):
        if e.get('status') == 'rejected' or e.get('scope', 'md') != scope:
            continue
        before, after = e['before'], e['after']
        if e.get('regex'):
            text, n = re.subn(before, after, text)
        else:
            n = text.count(before)
            text = text.replace(before, after)
        _tally[(rid, e['id'])] = _tally.get((rid, e['id']), 0) + n
    return text


def check(rid, scopes):
    """Compare tallies with expected counts for the scopes that have run; write the status file."""
    res = []
    for e in load(rid):
        if e.get('scope', 'md') not in scopes:
            continue
        got = _tally.get((rid, e['id']), 0)
        want = e.get('count', 1)
        if e.get('status') == 'rejected':
            state = 'rejected'
        elif want == 'any':
            state = 'applied' if got else 'no-op'
        else:
            state = 'applied' if got == want else f'FAILED (found {got}, expected {want})'
        res.append({'id': e['id'], 'scope': e.get('scope', 'md'), 'found': got, 'state': state})
    st = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
    live = {e['id'] for e in load(rid)}
    cur = {r['id']: r for r in st.get(rid, []) if r['id'] in live}   # drop entries whose edit was removed
    for r in res:
        cur[r['id']] = r
    st[rid] = list(cur.values())
    os.makedirs(os.path.dirname(STATUS), exist_ok=True)
    json.dump(st, open(STATUS, 'w'), indent=1, ensure_ascii=False)
    bad = [r for r in res if r['state'].startswith('FAILED')]
    if bad and os.environ.get('EDITS_STRICT') == '1':
        raise SystemExit(f'{rid}: {len(bad)} edit(s) failed: ' + ', '.join(r['id'] for r in bad))
    return res


def reset(rid, scope):
    for e in load(rid):
        if e.get('scope', 'md') == scope:
            _tally.pop((rid, e['id']), None)
