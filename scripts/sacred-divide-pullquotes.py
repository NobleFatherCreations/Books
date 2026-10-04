#!/usr/bin/env python3
"""Pick one verbatim pull-quote per section for every volume, written to content/sacred-divide/pullquotes/<id>.json.
The PDF builder (sacred-divide-v5-pdf) places a quote only where a page would otherwise end mostly empty.
Rules: the sentence comes word for word from the volume's own prose (a question, a "tell" block, a lede or a paragraph;
never a table or a source list), 45-140 characters, one complete sentence, no figures in brackets, no cross-references.
Catholicism keeps its approved set (inside the builder); this script only overrides the entries that went stale.
Usage: sacred-divide-pullquotes.py            (all volumes)   |   sacred-divide-pullquotes.py <id> ..."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELIG = os.path.join(ROOT, 'content/sacred-divide/religions')
OUT = os.path.join(ROOT, 'content/sacred-divide/pullquotes')
os.makedirs(OUT, exist_ok=True)

# section slug -> preferred source block order
PREFER = {'forefront': ['question'], 'structure': ['tell'], 'healthy': ['lede', 'p'], 'history': ['p'], 'branches': ['p'], 'law': ['p'],
          'money': ['bullet'], 'genealogy': ['p'], 'reach': ['bullet'], 'techniques': ['p'], 'loops': ['lede', 'p'], 'say-do': ['p', 'bullet'],
          'cost': ['bullet'], 'ledger': ['bullet'], 'tiers': ['p'], 'cases': ['p'], 'regional': ['p'], 'leaving': ['p'], 'who-gets-hurt': ['p'],
          'at-a-glance': [], 'a-day-inside': [], 'precedent': ['p'], 'voices': ['bullet'], 'questions': ['p']}


def clean(t):
    t = re.sub(r'\[\[(\w+)\]\]', r'\1', t)
    t = re.sub(r'(?:\s*\[\d+\])+', '', t)
    t = re.sub(r'\s*\[(?:[A-Z][A-Z /\-]+)(?::[^\]]*)?\]', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t); t = re.sub(r'\*(.+?)\*', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()


def sections(md):
    parts = re.split(r'^## (\d+)\. (.+?) \{#([\w-]+)\}\s*$', md, flags=re.M)
    return {parts[i + 2]: parts[i + 3] for i in range(1, len(parts) - 3, 4)}


def blocks(body):
    out = []
    for m in re.finditer(r'::: (question|tell|lede)\n(.*?)\n:::', body, re.S): out.append((m.group(1), clean(m.group(2))))
    body2 = re.sub(r'::: \w+\n.*?\n:::', '', body, flags=re.S)
    body2 = re.sub(r'```.*?```', '', body2, flags=re.S)
    for ln in body2.split('\n'):
        s = ln.strip()
        if not s or s.startswith(('|', '#', ':::', '1.', '*Tyler')): continue
        if s.startswith('- '): out.append(('bullet', clean(s[2:])))
        else: out.append(('p', clean(s)))
    return out


def good(s):
    if not (45 <= len(s) <= 140): return False
    if not re.match(r'^[A-Z"“‘’\']', s) or not s[-1] in '.?"': return False
    if re.search(r'\d{3,}|\(|\)|;|:|https?|[Ss]ection \d|technique \d|\[|\]|\bThis page\b|\bthis page\b|\bthe codex\b', s): return False
    return True


def pick(slug, body):
    sents = []
    bl = blocks(body)
    for kind in PREFER.get(slug, ['p']) + ['p']:
        for k, t in bl:
            if k != kind: continue
            if kind in ('question', 'tell'):
                if good(t): return t
                continue
            for s in re.split(r'(?<=[.?!])\s+(?=[A-Z])', t):
                if good(s): sents.append(s)
        if sents: break
    return sents[0] if sents else None


def build(rid):
    md = open(os.path.join(RELIG, rid + '.md'), encoding='utf-8').read()
    pq = {}
    for slug, body in sections(md).items():
        if slug in ('at-a-glance', 'a-day-inside', 'sources', 'changed', 'help', 'questions') and slug != 'questions': continue
        if slug not in PREFER or not PREFER[slug] and slug != 'at-a-glance': continue
        s = pick(slug, body)
        if s: pq[slug] = s
    plain = re.sub(r'\s+', ' ', re.sub(r'(?:\s*\[\d+\])+|\*+', '', md))
    for k, v in list(pq.items()):                       # every quote must occur in the volume text
        if v.rstrip('.') not in plain and v not in plain: del pq[k]
    if rid == 'catholicism':
        pq = {k: v for k, v in pq.items() if k in ('forefront', 'say-do')}
    json.dump(pq, open(os.path.join(OUT, rid + '.json'), 'w'), indent=1, ensure_ascii=False)
    return pq


if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(RELIG) if f.endswith('.md') and not f.startswith('_') and f != 'README.md')
    for r in ids:
        if r in ('protestant-evangelical', 'catholicism') and not sys.argv[1:]:
            continue                                     # hand-picked sets already in place
        print(r, len(build(r)))
