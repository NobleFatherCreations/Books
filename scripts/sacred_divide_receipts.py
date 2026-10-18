"""Keep D.receiptIndex in step with the religion profiles it quotes.

The index (the Receipts page) is derived data: one entry per tagged sentence,
tag stripped, text cut at ~230 characters, grouped by receipt type. It was
generated once and never regenerated, so an edit to a profile leaves a stale
copy behind. `pin` finds, before any edits, the profile string each entry was
taken from; `refresh` rebuilds each entry from that same string afterwards —
re-cutting the text, re-reading the tag's detail, moving the entry if its
receipt type changed, and dropping it if the string no longer carries a tag.
The original selection and order are kept; nothing new is added.
"""
import re

TAG = re.compile(r'\s*\[([A-Z][A-Z /]+?)(?:\s*[—:-]\s*([^\]]*))?\]')
TYPES = {'OFFICIAL POLICY': 'Official policy', 'PATTERN OBSERVED': 'Pattern observed',
         'INVESTIGATIVE REPORT': 'Investigative report', 'ACADEMIC SOURCE': 'Academic source',
         'GOVERNMENT REPORT': 'Government inquiry', 'COURT RECORD': 'Court record',
         'FINANCIAL RECORD': 'Financial record', 'LEADERSHIP STATEMENT': 'Leadership statement',
         'FORMER MEMBER TESTIMONY': 'Former member testimony', 'SOURCE NEEDED': 'Source needed'}
FIELD = {'authority': 'authority', 'money': 'money', 'exit': 'exit', 'benefits': 'whoBenefits', 'health': 'healthy',
         'info': 'info', 'children': 'children', 'gender': 'gender', 'pays': 'whoPays', 'leverage': 'leverage',
         'origin': 'origin'}


def _cut(t):
    return t if len(t) <= 230 else t[:230]


def _strip(t):
    return TAG.sub('', t).strip()


def _candidates(r, at):
    """(key, body-text, tag-text) for every string an entry in section `at` could quote."""
    if at == 'timeline':
        for i, row in enumerate(r.get('timeline', [])):
            yield ('timeline', i), row[1], row[2] if len(row) > 2 else ''
            yield ('timeline2', i), _strip(row[2]) if len(row) > 2 else '', row[2] if len(row) > 2 else ''
    elif at == 'genealogy':
        for i, g in enumerate(r.get('genealogy', [])):
            for k, t in g.items():
                if isinstance(t, str): yield ('genealogy', i, k), _strip(t), t
    else:
        v = r.get(FIELD[at]); v = v if isinstance(v, list) else [v]
        for i, t in enumerate(v):
            if isinstance(t, str): yield (at, i), _strip(t), t


def _norm(t):
    return re.sub(r'\s+([.,;:)])', r'\1', t).rstrip('…').strip()


def pin(D):
    """Return, per entry, the profile location it quotes (or None if not found).

    Exact match first; then, for entries an earlier build already edited, the
    candidate sharing the longest common prefix (at least 12 characters)."""
    rel = {r['id']: r for r in D['religions']}
    pins = []
    for kind, lst in D['receiptIndex'].items():
        for e in lst:
            want = _norm(e['text'])
            hit, best = None, 11
            cands = list(_candidates(rel[e['rid']], e['at']))
            for key, body, _ in cands:
                b = _norm(body)
                if b and (b == want or (len(want) >= 200 and b.startswith(want))):
                    hit = key; break
            if hit is None:
                for key, body, _ in cands:
                    b = _norm(body); n = 0
                    while n < min(len(b), len(want)) and b[n] == want[n]: n += 1
                    if n > best: hit, best = key, n
            pins.append((kind, e, hit))
    return pins


def _lookup(r, key):
    if key[0] == 'timeline':
        row = r['timeline'][key[1]]; return row[1], row[2] if len(row) > 2 else ''
    if key[0] == 'timeline2':
        row = r['timeline'][key[1]]; return _strip(row[2]), row[2]
    if key[0] == 'genealogy':
        t = r['genealogy'][key[1]][key[2]]; return _strip(t), t
    v = r[FIELD[key[0]]]; t = v[key[1]] if isinstance(v, list) else v
    return _strip(t), t


def refresh(D, pins, order):
    """Rebuild the index from pinned locations; returns (index, moved, dropped)."""
    rel = {r['id']: r for r in D['religions']}
    out, moved, dropped = {}, [], []
    for kind, e, key in pins:
        if key is None:
            out.setdefault(kind, []).append(e); continue
        body, tagged = _lookup(rel[e['rid']], key)
        m = TAG.search(tagged)
        new_kind = TYPES.get(m.group(1).split('/')[0].strip()) if m else None
        if not new_kind:
            # untagged or a non-evidence tag ("[VARIES BY COMMUNITY]") was indexed as a pattern;
            # an entry whose evidence tag has been removed leaves the index
            if kind == 'Pattern observed' and (m or key[0] == 'timeline'): new_kind = kind
            else: dropped.append(e['text'][:60]); continue
        text = body if len(body) <= 230 else body[:230].rstrip() + '…'
        ne = dict(e, text=text, detail=(m.group(2) or '').strip() if m and m.group(2) else '')
        if new_kind != kind: moved.append((e['text'][:50], kind, new_kind))
        out.setdefault(new_kind, []).append(ne)
    return {k: out[k] for k in order if k in out}, moved, dropped
