#!/usr/bin/env python3
"""One-sentence examples for the Counterfeit slides: build the input files for the condensing agents, check their output, merge.

  counterfeit-lines.py inputs     write content/counterfeit/in-*.json (items whose source sentence is too long for one slide row)
  counterfeit-lines.py check F    check content/counterfeit/out-F.json against its input (length, one sentence, no new facts)
  counterfeit-lines.py merge      write content/counterfeit/lines.json (short sources kept verbatim + checked agent output)
  counterfeit-lines.py inputs2    write the round-2 inputs: in-l1..l4 (institutional + civilizational examples, 25 sectors),
                                  in-n1 (the 4 sectors the book gives no per-technique examples for: lines AUTHORED from the sector
                                  narrative, flagged as such), in-c1 (The Mirror and The Body chapters, one line per technique)
  counterfeit-lines.py sense TAG  spaCy full-sentence heuristics on one out-TAG.json

Religion source: the first bullet of each technique's "How it shows here" (card volumes) or the "How it appears here" cell (table volumes).
Fractal source: the individual-level example of each technique in each sector (library/fractal/index.html data blob).
A line is a single sentence of at most MAXLEN characters, in the source's own words: no new facts, no new numbers."""
import json, os, pickle, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELIG = os.path.join(ROOT, 'content/sacred-divide/religions'); OUT = os.path.join(ROOT, 'content/counterfeit')
MAXLEN = 95
STOP = set('the a an and or of to in on for with by from as at is are was were be been it its that this these those their his her they them you your we our who whom which what when where while than then so not no but if into onto over under about after before through across within without can may might will would should could also more most some any each every one two three has have had do does did'.split())


def clean(x):
    x = re.sub(r'\s*\[\d+\](?:\[\d+\])*', '', x); x = re.sub(r'\s*\[[A-Z][A-Z /\-]+(?::[^\]]*)?\]', '', x)
    return re.sub(r'\s+', ' ', re.sub(r'\*\*|\*', '', x)).strip()


def canon():
    t = open(os.path.join(RELIG, 'hare-krishna.md'), encoding='utf-8').read()
    return [re.sub(r' / .*', '', n).strip() for n in re.findall(r'^#### \d+ · (.+?)(?: \{#t-\d+\})?$', t, re.M)[:30]]


def religion_sources():
    out = {}
    for fn in sorted(os.listdir(RELIG)):
        if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md': continue
        rid = fn[:-3]; t = open(os.path.join(RELIG, fn), encoding='utf-8').read(); src = {}
        heads = [(m.start(), int(m.group(1))) for m in re.finditer(r'^#### (\d+) · ', t, re.M)][:30]
        if len(heads) == 30:
            for k, (pos, n) in enumerate(heads):
                end = heads[k + 1][0] if k + 1 < 30 else pos + 6000
                m = re.search(r'\*\*How it shows here\*\*\s*\n\s*\n((?:- .+\n?)+)', t[pos:end])
                src[n] = clean(re.findall(r'^- (.+)$', m.group(1), re.M)[0])
        else:
            sec = re.search(r'^## 12\..*?(?=^## 13\.)', t, re.S | re.M).group(0)
            for l in sec.splitlines():
                m = re.match(r'^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|([^|]*)\|', l)
                if m and 1 <= int(m.group(1)) <= 30: src[int(m.group(1))] = clean(m.group(2))
        assert len(src) == 30, (rid, len(src))
        out[rid] = src
    return out


def fractal_blob():
    h = open(os.path.join(ROOT, 'library/fractal/index.html'), encoding='utf-8', errors='ignore').read()
    j = h.find('"scales": [{"key": "ind"'); depth = 0; i = j
    while i > 0:
        i -= 1
        if h[i] == '}': depth += 1
        elif h[i] == '{':
            if depth == 0: break
            depth -= 1
    return json.JSONDecoder().raw_decode(h[i:])[0]


def fractal_sources():
    o = fractal_blob()   # sectors[].techs[].ind/inst/civ: the book's per-sector, per-technique examples at three scales
    return {s['num']: {'name': s['short'], 'src': {t['num']: clean(t['ind']) for t in s['techs']}} for s in o['sectors'] if s['techs'] and s['num'] != 1}


def good(s):
    return len(s) <= MAXLEN and s[-1] in '.”"' and s.lstrip('"“‘\'')[:1].isupper() and len(re.findall(r'[.!?](?:\s+[A-Z“"]|$)', s)) <= 1 and '…' not in s and ' — ' not in s[:0]


def words(s):
    return [w[:5] for w in re.findall(r"[a-z0-9']+", s.lower()) if w not in STOP and len(w) > 2]


def problems(line, src, authored=False):
    p = []
    if len(line) > MAXLEN: p.append(f'{len(line)} chars (max {MAXLEN})')
    if not line or line[-1] not in '.”"': p.append('does not end with a full stop')
    if len(re.findall(r'[.!?](?:["”]?\s+[A-Z“"])', line)) > 0: p.append('more than one sentence')
    if '…' in line or '...' in line: p.append('ellipsis')
    if re.search(r'\[\d', line): p.append('citation marker')
    if authored: return p
    sw = set(words(src)); lw = words(line)
    new = [w for w in lw if w not in sw]
    if lw and len(new) / len(lw) > 0.45: p.append('too many words not in the source: ' + ', '.join(sorted(set(new))[:6]))
    nums = set(re.findall(r'\d[\d,.]*', line)) - set(re.findall(r'\d[\d,.]*', src))
    if nums: p.append('number not in source: ' + ', '.join(nums))
    return p


def cmd_inputs():
    names = canon(); R = religion_sources(); F = fractal_sources(); os.makedirs(OUT, exist_ok=True)
    pending_r = {rid: {n: s for n, s in src.items() if not good(s)} for rid, src in R.items()}
    pending_f = {num: {n: s for n, s in d['src'].items() if not good(s)} for num, d in F.items()}
    json.dump({'names': names, 'religions': R, 'fractal': {str(k): v for k, v in F.items()}}, open(os.path.join(OUT, 'sources.json'), 'w'), indent=1, ensure_ascii=False)
    rids = [r for r in R if pending_r[r]]
    batches = [rids[i::4] for i in range(4)]
    for i, b in enumerate(batches, 1):
        json.dump({'kind': 'religion', 'items': {rid: {str(n): {'technique': names[n - 1], 'source': s} for n, s in pending_r[rid].items()} for rid in b}}, open(os.path.join(OUT, f'in-r{i}.json'), 'w'), indent=1, ensure_ascii=False)
    nums = [n for n in F if pending_f[n]]
    for i, b in enumerate([nums[0::2], nums[1::2]], 1):
        json.dump({'kind': 'fractal', 'items': {str(num): {'sector': F[num]['name'], 'lines': {str(n): {'technique': names[n - 1], 'source': s} for n, s in pending_f[num].items()}} for num in b}}, open(os.path.join(OUT, f'in-f{i}.json'), 'w'), indent=1, ensure_ascii=False)
    print('religion lines to condense:', sum(len(v) for v in pending_r.values()), 'of', 34 * 30, '| fractal:', sum(len(v) for v in pending_f.values()), 'of', sum(len(d['src']) for d in F.values()))


LEVELS = {'ind': 'Individual', 'inst': 'Institutional', 'civ': 'Civilizational'}


def closing_sources():
    """The Mirror (each technique turned on yourself) and The Body (each technique's somatic signature): the text under each technique heading."""
    C = {c['slug']: c for c in fractal_blob()['closings']}; out = {}
    for s in ('mirror', 'body'):
        cur = None; d = {}
        for x in C[s]['blocks']:
            if x['t'] == 'tech': cur = x['n']; d[cur] = []
            elif x['t'] in ('h', 'stage'): cur = None
            elif cur and x['t'] == 'p': d[cur].append(re.sub(r'<[^>]+>', '', x['x']))
        assert len(d) == 30, (s, len(d))
        out[s] = {n: clean(' '.join(v)) for n, v in d.items()}
    return out


def cmd_inputs2():
    names = canon(); o = fractal_blob(); full = [s for s in o['sectors'] if s['techs'] and s['num'] != 1]
    items = {f"{s['num']}-{lv}": {'sector': s['short'], 'level': LEVELS[lv], 'lines': {str(t['num']): {'technique': names[t['num'] - 1], 'source': clean(t[lv])} for t in s['techs']}}
             for s in full for lv in ('inst', 'civ')}
    keys = list(items); per = -(-len(keys) // 4)
    for i in range(4):
        json.dump({'kind': 'fractal', 'items': {k: items[k] for k in keys[i * per:(i + 1) * per]}}, open(os.path.join(OUT, f'in-l{i + 1}.json'), 'w'), indent=1, ensure_ascii=False)
    gap = [s for s in o['sectors'] if not s['techs']]
    json.dump({'kind': 'fractal', 'authored': True,
               'note': 'The Fractal gives these sectors a narrative but no per-technique examples. Lines here are written new from the narrative, the sector\'s controls/impulse and each technique\'s definition, so they are flagged as authored, not quoted.',
               'items': {f"{s['num']}-{lv}": {'sector': s['short'], 'level': LEVELS[lv], 'controls': s['controls'], 'impulse': s['impulse'], 'narrative': clean(s['narrative']),
                                              'lines': {str(n): {'technique': names[n - 1], 'source': o['essence'][str(n)]} for n in range(1, 31)}}
                         for s in gap for lv in LEVELS}}, open(os.path.join(OUT, 'in-n1.json'), 'w'), indent=1, ensure_ascii=False)
    C = closing_sources()
    json.dump({'kind': 'fractal', 'items': {
        'mirror': {'sector': 'The Mirror (the technique turned on yourself; write in the second person, "You ...")', 'lines': {str(n): {'technique': names[n - 1], 'source': s} for n, s in C['mirror'].items()}},
        'body': {'sector': 'The Body (the technique as the body feels it: its somatic signature; prefer the "Somatic Signature" passage)', 'lines': {str(n): {'technique': names[n - 1], 'source': s} for n, s in C['body'].items()}}}},
        open(os.path.join(OUT, 'in-c1.json'), 'w'), indent=1, ensure_ascii=False)
    print('l1-l4:', len(keys) * 30, 'lines; n1:', len(gap) * 90, 'authored lines; c1: 60 lines')


def items_of(inp):
    d = json.load(open(inp, encoding='utf-8'))
    if d['kind'] == 'religion':
        for rid, its in d['items'].items():
            for n, v in its.items(): yield rid, n, v['source']
    else:
        for num, sec in d['items'].items():
            for n, v in sec['lines'].items(): yield num, n, v['source']


def cmd_check(tag):
    inp = os.path.join(OUT, f'in-{tag}.json'); outp = os.path.join(OUT, f'out-{tag}.json')
    out = json.load(open(outp, encoding='utf-8')); bad = 0; n = 0; au = json.load(open(inp, encoding='utf-8')).get('authored', False)
    for a, b, src in items_of(inp):
        n += 1; line = out.get(a, {}).get(b)
        if line is None: print('MISSING', a, b); bad += 1; continue
        pr = problems(line, src, au)
        if pr: bad += 1; print(f'{a} #{b}: {line!r} -> ' + '; '.join(pr))
    print(f'{n} lines checked, {bad} with problems')
    return bad


def cmd_merge():
    R = religion_sources(); F = fractal_sources(); res = {'religions': {rid: dict(src) for rid, src in R.items()}, 'fractal': {str(k): dict(v['src']) for k, v in F.items()}}
    res['religions'] = {rid: {str(n): s for n, s in d.items()} for rid, d in res['religions'].items()}
    res['fractal'] = {k: {str(n): s for n, s in d.items()} for k, d in res['fractal'].items()}
    miss = 0
    for tag in ['l1', 'l2', 'l3', 'l4', 'n1', 'c1']:   # round 2: other scales, the gap sectors, The Mirror and The Body
        p = os.path.join(OUT, f'out-{tag}.json')
        if not os.path.exists(p): continue
        for a, d in json.load(open(p, encoding='utf-8')).items():
            if a in ('mirror', 'body'): res.setdefault(a, {}).update(d); continue
            num, lv = a.split('-'); res.setdefault('fractal' if lv == 'ind' else 'fractal_' + lv, {}).setdefault(num, {}).update(d)
    for tag in ['r1', 'r2', 'r3', 'r4', 'f1', 'f2']:
        p = os.path.join(OUT, f'out-{tag}.json')
        if not os.path.exists(p): continue
        out = json.load(open(p, encoding='utf-8')); key = 'religions' if tag[0] == 'r' else 'fractal'
        for a, d in out.items():
            for b, line in d.items(): res[key][a][b] = line
    fxp = os.path.join(OUT, 'fixes.json')   # hand fixes after a human read of every line; applied last
    if os.path.exists(fxp):
        for key, d in json.load(open(fxp, encoding='utf-8')).items():
            for a, dd in d.items():
                for b, line in dd.items(): res[key][a][b] = line
    for key in res:
        for a, d in res[key].items():
            for b, line in (d.items() if isinstance(d, dict) else [('', d)]):   # mirror/body are flat {n: line}
                if not good(line): miss += 1; print('not slide-ready:', key, a, b, repr(line))
    json.dump(res, open(os.path.join(OUT, 'lines.json'), 'w'), indent=1, ensure_ascii=False)
    print('merged; lines still not slide-ready:', miss)


def sense_flags(nlp, line):
    """Heuristics for "a full sentence that makes sense": a subject and a finite/main verb, no dangling last word, balanced quotes."""
    doc = nlp(line); f = []
    toks = [t for t in doc if not t.is_punct]
    if len(toks) < 4: f.append('too short')
    if not any(t.pos_ in ('VERB', 'AUX') for t in toks): f.append('no verb')
    elif not any(t.dep_ in ('nsubj', 'nsubjpass', 'expl', 'csubj') for t in toks) and not (toks and toks[0].pos_ == 'VERB' and toks[0].tag_ == 'VB'): f.append('no subject')
    if toks and toks[-1].pos_ in ('ADP', 'CCONJ', 'SCONJ', 'DET', 'PART', 'AUX') and toks[-1].text.lower() not in ('off', 'up', 'out', 'back', 'in', 'on'): f.append('ends on ' + toks[-1].text)
    if line.count('"') % 2 or line.count('“') != line.count('”') or line.count('(') != line.count(')'): f.append('unbalanced quotes/brackets')
    if re.search(r'\s[,.;:]|,,|\.\.|, ?\.|\band\.|\bor\.|\bthe\.', line): f.append('stray punctuation')
    return f


def cmd_sense_tag(tag):
    import spacy
    nlp = spacy.load('en_core_web_sm'); n = bad = 0
    for a, d in json.load(open(os.path.join(OUT, f'out-{tag}.json'), encoding='utf-8')).items():
        for b, line in sorted(d.items(), key=lambda kv: int(kv[0])):
            n += 1; fl = sense_flags(nlp, line)
            if fl: bad += 1; print(f'{a} #{b}: {line!r} -> ' + '; '.join(fl))
    print(f'{n} lines examined, {bad} flagged')


def cmd_sense():
    import spacy
    nlp = spacy.load('en_core_web_sm'); R = religion_sources(); F = fractal_sources()
    res = {'religions': {k: {str(n): t for n, t in v.items()} for k, v in R.items()}, 'fractal': {str(k): {str(n): t for n, t in v['src'].items()} for k, v in F.items()}}
    for tag in ['r1', 'r2', 'r3', 'r4', 'f1', 'f2']:
        p = os.path.join(OUT, f'out-{tag}.json')
        if os.path.exists(p):
            for a, d in json.load(open(p, encoding='utf-8')).items():
                for b, line in d.items(): res['religions' if tag[0] == 'r' else 'fractal'][a][str(b)] = line
    n = bad = 0
    for key in res:
        for a, d in res[key].items():
            for b, line in sorted(d.items(), key=lambda kv: int(kv[0])):
                if key == 'fractal' and len(line) > MAXLEN: continue      # not yet condensed
                n += 1; fl = sense_flags(nlp, line)
                if fl: bad += 1; print(f'{key[:3]} {a} #{b}: {line!r} -> ' + '; '.join(fl))
    print(f'{n} lines examined, {bad} flagged for a human read')


if __name__ == '__main__':
    if sys.argv[1] == 'sense' and len(sys.argv) > 2: cmd_sense_tag(sys.argv[2])
    else: {'inputs': cmd_inputs, 'inputs2': cmd_inputs2, 'merge': cmd_merge, 'sense': cmd_sense}.get(sys.argv[1], lambda: cmd_check(sys.argv[2]))()
