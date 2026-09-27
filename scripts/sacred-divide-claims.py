#!/usr/bin/env python3
"""Claim inventory for The Sacred Divide, one file per religion.

Usage: python3 scripts/sacred-divide-claims.py <book.html> <out_dir>

Walks every embedded data blob and gathers each string that belongs to one
religion (its profile, its tactic entries, grades, cases, apex, regional card,
phrasebook, succession/promise rows, and any cross-cutting row that names it).
Each string is split into sentences; sentences carrying a date, a number, a
receipt tag, or a named proper noun are marked "checkable" and get a claim id
(<rid>-NNN). The fact-check files in content/sacred-divide/sources/ cite these
ids. Regenerating is safe: ids are stable for unchanged text (hash-based).
"""
import hashlib, json, os, re, sys

BLOBS = ['CODEX_DATA', 'CODEX_V8', 'CODEX_V7', 'CODEX_V6', 'CODEX_V3', 'CODEX_V2']

# words that identify a religion inside cross-cutting prose
KEYWORDS = {
    'christianity': [], 'catholicism': ['Catholic', 'Vatican', 'pope', 'Pope'],
    'eastern-orthodoxy': ['Orthodox Church', 'Patriarch', 'Eastern Orthodox'],
    'protestant-evangelical': ['Evangelical', 'Southern Baptist', 'Protestant'],
    'pentecostal-charismatic': ['Pentecostal', 'Charismatic', 'Hillsong'],
    'islam': [], 'sunni-islam': ['Sunni', 'al-Azhar', 'Saudi'], 'shia-islam': ['Shia', 'Shiʿa', 'Iran'],
    'judaism': [], 'orthodox-hasidic-judaism': ['Hasidic', 'Haredi', 'Orthodox Jewish', 'get '],
    'hinduism': ['Hindu'], 'buddhism': [], 'tibetan-buddhism': ['Tibetan', 'Shambhala', 'Rigpa'],
    'sikhism': ['Sikh', 'SGPC'], 'jainism': ['Jain'], 'taoism': ['Taoist', 'Daoist'],
    'confucianism': ['Confucian'], 'shinto': ['Shinto', 'Yasukuni'], 'zoroastrianism': ['Zoroastrian', 'Parsi'],
    'bahai': ['Baháʼí', 'Baha'], 'mormonism': ['Latter-day', 'LDS', 'Mormon'],
    'seventh-day-adventism': ['Adventist'], 'jehovahs-witnesses': ["Jehovah", 'Watch Tower', 'Watchtower'],
    'scientology': ['Scientology', 'Sea Org'], 'hare-krishna': ['ISKCON', 'Krishna'],
    'new-age': ['New Age', 'ayahuasca', 'NXIVM'], 'indigenous': ['Indigenous', 'residential school'],
}
TAG = re.compile(r'\[(COURT RECORD|GOVERNMENT REPORT|GOVERNMENT INQUIRY|OFFICIAL POLICY|FINANCIAL RECORD|REGULATORY FILING|'
                 r'ACADEMIC SOURCE|INVESTIGATIVE REPORT|LEADERSHIP STATEMENT|FORMER MEMBER TESTIMONY|PATTERN OBSERVED|SOURCE NEEDED)[^\]]*\]', re.I)
CHECK = re.compile(r'\d|\[[A-Z ]{6,}|\b(?:[A-Z][a-zà-ɏʼ\'’-]+\s){1,}[A-Z][a-z]')
HTML = re.compile(r'<[^>]+>')
# where every sentence is a factual claim, whatever its wording
FACTUAL = re.compile(r'^(profile\.(neutral|origin|authority|money|exit|whoBenefits|timeline|demographics|info|children|gender|'
                     r'moneyTable|exitTable|whoPays|genealogy|roster|differential|victories)|case |apex|regional|sector|compel|'
                     r'succession|promises|score)')


def load(path):
    s = open(path, encoding='utf-8').read(); out = {}
    for n in BLOBS:
        i = s.index(f'window.{n} = ') + len(f'window.{n} = ')
        e = s.index('</script>', i)
        out[n] = json.loads(s[i:e].rstrip().rstrip(';'))
    return out


def leaves(o, path):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f'{path}[{i}]')


def sentences(text):
    text = HTML.sub('', text).strip()
    parts = re.split(r'(?<=[.;!?])\s+(?=[A-Z“"(\[])', text)
    return [p.strip() for p in parts if len(p.strip()) > 3]


def main(src, out_dir):
    B = load(src); D = B['CODEX_DATA']; V2, V3, V6, V7 = B['CODEX_V2'], B['CODEX_V3'], B['CODEX_V6'], B['CODEX_V7']
    os.makedirs(out_dir, exist_ok=True)
    summary = []
    for k, r in enumerate(D['religions'], 1):
        rid, idx = r['id'], str(k)
        items = list(leaves({f: v for f, v in r.items() if f not in ('id', 'family')}, 'profile'))
        for t in D['tactics']:
            if idx in t['entries']:
                items += leaves(t['entries'][idx], f"tactic {t['order']} ({t['name']})")
        for key, g in D['graded'].items():
            if key.split(':')[0] == rid:
                items += leaves(g[:2], f'grade {key}')
        if rid in D['sector']: items += leaves(D['sector'][rid], 'sector')
        for c in D['cases']:
            if c['tradition'] == rid:
                items += leaves({f: c[f] for f in ('title', 'when', 'what', 'source', 'outcome')}, f"case {c['id']}")
        for name, blob in (('apex', V2['apex']), ('unanswered', V2['unanswered']), ('compel', V3['compel']),
                           ('revise', V3['revise']), ('phrasebook', V6['language']['per']),
                           ('regional', V6['regions']['cards']), ('score', V7['score'])):
            if rid in blob: items += leaves(blob[rid], name)
        kws = KEYWORDS.get(rid, []) + [r['name']]
        for vol in ('women', 'medical', 'lgbtq', 'convert', 'exitatlas', 'promises', 'succession', 'levers', 'errors'):
            for p, s in leaves(V7[vol], vol):
                if any(w in s for w in kws):
                    items.append((p, s))
        seen, rows = set(), []
        for p, s in items:
            for sent in sentences(s):
                h = hashlib.sha1(sent.encode()).hexdigest()[:6]
                if h in seen: continue
                seen.add(h)
                rows.append((p, sent, bool(FACTUAL.match(p) or CHECK.search(sent)), h))
        chk = [x for x in rows if x[2]]
        lines = [f"# Claim inventory — {r['name']}", '',
                 f'Generated by `scripts/sacred-divide-claims.py` from `{os.path.basename(src)}`. Do not edit by hand;',
                 f'the fact-check lives in `../{rid}.md`, which cites these ids.', '',
                 f'{len(rows)} sentences, {len(chk)} checkable (a date, a number, a receipt tag or a proper noun).', '',
                 '| id | where | claim |', '|---|---|---|']
        for p, sent, c, h in rows:
            if c:
                lines.append(f"| `{rid}-{h}` | {p} | {sent.replace('|', '/')} |")
        lines += ['', '## Not flagged as checkable (interpretive or generic)', '']
        lines += [f"- {p}: {sent}" for p, sent, c, h in rows if not c]
        open(os.path.join(out_dir, f'{rid}.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        summary.append((r['name'], len(rows), len(chk)))
    for n, a, b in summary:
        print(f'{n:45} {a:4} sentences {b:4} checkable')


if __name__ == '__main__':
    main(*sys.argv[1:3])
