"""Resolve the inventory-style paths used in content/sacred-divide/sources/*.md.

  get(B, 'islam', 'timeline[4]')            -> religion profile field
  get(B, 'islam', 'apex.rows[1][1]')        -> V2.apex[rid]...
  get(B, 'islam', 'regional[0].law')        -> V6.regions.cards[rid]...
  get(B, 'islam', 'case trc.outcome')       -> D.cases[id=trc].outcome
  get(B, 'islam', 'tactic 12.examples[0]')  -> D.tactics[order=12].entries[idx]...
  get(B, 'islam', 'grade islam:12[1]')      -> D.graded['islam:12'][1]
  get(B, None, 'V7.succession.rows[3].current') -> absolute (D./V2./V3./V6./V7./V8.)
A path resolves to (container, key) so callers can read or assign.
"""
import json, re

BLOBS = ['CODEX_DATA', 'CODEX_V8', 'CODEX_V7', 'CODEX_V6', 'CODEX_V3', 'CODEX_V2']
ABS = {'D': 'CODEX_DATA', 'V2': 'CODEX_V2', 'V3': 'CODEX_V3', 'V6': 'CODEX_V6', 'V7': 'CODEX_V7', 'V8': 'CODEX_V8'}
TOK = re.compile(r'\.?([^.\[\]]+)|\[(\d+)\]')

def load(path):
    s = open(path, encoding='utf-8').read(); out = {}
    for n in BLOBS:
        i = s.index(f'window.{n} = ') + len(f'window.{n} = ')
        e = s.index('</script>', i)
        out[n] = json.loads(s[i:e].rstrip().rstrip(';'))
    return out

def steps(p):
    out = []
    for name, idx in TOK.findall(p):
        out.append(int(idx) if idx else name)
    return out

def root(B, rid, path):
    D = B['CODEX_DATA']
    head, _, rest = path.partition('.') if not path.startswith(('case ', 'tactic ', 'grade ')) else (path, '', '')
    if path.split('.')[0].split('[')[0] in ABS:
        first = path.split('.')[0]
        return B[ABS[first]], path[len(first):]
    if path.startswith('case '):
        cid, _, rest = path[5:].partition('.')
        return next(c for c in D['cases'] if c['id'] == cid), rest
    if path.startswith('tactic '):
        m = re.match(r'tactic (\d+)(.*)', path)
        idx = str([r['id'] for r in D['religions']].index(rid) + 1)
        t = next(t for t in D['tactics'] if t['order'] == int(m.group(1)))
        return t['entries'][idx], m.group(2)
    if path.startswith('grade '):
        m = re.match(r'grade ([\w-]+:\d+)(.*)', path)
        return D['graded'][m.group(1)], m.group(2)
    B2, B3, B6, B7 = B['CODEX_V2'], B['CODEX_V3'], B['CODEX_V6'], B['CODEX_V7']
    heads = {'apex': B2['apex'], 'unanswered': B2['unanswered'], 'compel': B3['compel'], 'revise': B3['revise'],
             'phrasebook': B6['language']['per'], 'regional': B6['regions']['cards'], 'score': B7['score'],
             'sector': D['sector']}
    first = re.match(r'[^.\[]+', path).group(0)
    if first in heads:
        return heads[first][rid], path[len(first):]
    if path.startswith('profile.'): path = path[8:]
    return next(r for r in D['religions'] if r['id'] == rid), path

def ref(B, rid, path):
    obj, rest = root(B, rid, path)
    st = steps(rest)
    if not st: raise ValueError(f'{path}: path names a whole record')
    for k in st[:-1]: obj = obj[k]
    return obj, st[-1]

def get(B, rid, path):
    o, k = ref(B, rid, path); return o[k]
