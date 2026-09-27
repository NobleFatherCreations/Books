#!/usr/bin/env python3
"""The Sacred Divide — export one Markdown file per religion, on the fixed page skeleton.

Output: content/sacred-divide/religions/<id>.md   (one per religion, 34)
        content/sacred-divide/religions/_coverage.md   (which sections are filled, per religion)

Inputs, merged in this order:
  1. the fact-checked book  (library/_undeployed/sacred-divide-v4-factchecked.html) — the 27 existing religions
  2. content/sacred-divide/new-traditions/<id>.md — the 7 new religions (their own `## field` records)
  3. content/sacred-divide/additions/<id>.md — new sections written for the full page (branches, law, money in
     numbers, cases, voices, regional cards, leaving safely, help, what changed)
  4. content/sacred-divide/sources/<id>.md — the numbered Sources list and the claim register (per-section cites)

The religion files are generated: edit the inputs, never the output. They are the single input for the
PDF (scripts/sacred-divide-pdf.py) and, later, for the redesigned site.

Markdown conventions the PDF renderer relies on (see content/sacred-divide/religions/README.md):
  ## N. Title {#slug}      a section; ### Title {#slug} a subsection
  ::: kind ... :::         a styled container (tell, lede, gap, cites, tactic, card, case, stage, glance)
  ```timeline / ```chart   data blocks drawn as graphics
  [[Grade]]                an evidence-grade chip;  [n] a citation of Sources item n
  [OFFICIAL POLICY: …]     an evidence-type receipt, kept from the book

Usage: python3 scripts/sacred-divide-export-md.py [book.html]
"""
import json, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sacred_divide_paths as P

BOOK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'library/_undeployed/sacred-divide-v4-factchecked.html')
CONTENT = os.path.join(ROOT, 'content/sacred-divide')
OUT = os.path.join(CONTENT, 'religions')
CHECKED = '2026-09-27'
VERSION = 'v4'

# ---------------------------------------------------------------- families (order = cycle order)
FAMILIES = [
    ('christianity-family', 'Christianity', ['christianity', 'catholicism', 'eastern-orthodoxy', 'oriental-orthodoxy', 'anglicanism',
                                             'protestant-evangelical', 'pentecostal-charismatic', 'plymouth-brethren']),
    ('restorationist', 'Restorationist & Adventist', ['mormonism', 'jehovahs-witnesses', 'seventh-day-adventism']),
    ('islam-family', 'Islam', ['islam', 'sunni-islam', 'shia-islam', 'ahmadiyya', 'dawoodi-bohra']),
    ('judaism-family', 'Judaism', ['judaism', 'orthodox-hasidic-judaism']),
    ('dharmic', 'Dharmic', ['hinduism', 'hare-krishna', 'sikhism', 'jainism']),
    ('buddhism-family', 'Buddhism', ['buddhism', 'tibetan-buddhism', 'soka-gakkai']),
    ('east-asian', 'East Asian', ['taoism', 'confucianism', 'shinto']),
    ('persian', 'Persian-born', ['zoroastrianism', 'bahai']),
    ('new-movements', 'New movements & the spiritual marketplace', ['scientology', 'new-age', 'unification-church']),
    ('indigenous-family', 'Indigenous & folk', ['indigenous']),
]
FAMILY_OF = {rid: (fid, fname, members) for fid, fname, members in FAMILIES for rid in members}

# ---------------------------------------------------------------- the page skeleton
SECTIONS = [
    ('at-a-glance', 'At a glance'), ('a-day-inside', 'A day inside'), ('forefront', 'The forefront'),
    ('healthy', 'What healthy looks like here'), ('history', 'History'), ('branches', 'Branches & variants'),
    ('structure', 'Structure'), ('law', 'Law & state here'), ('money', 'Money'), ('genealogy', 'Genealogy'),
    ('reach', 'Reach'), ('techniques', 'The 30 techniques'), ('loops', 'The loops'), ('say-do', 'Say versus do'),
    ('cost', 'Cost & cover'), ('ledger', 'The ledger'), ('who-gets-hurt', 'Who gets hurt most'),
    ('tiers', 'The middle tiers'), ('cases', 'Documented cases'), ('precedent', 'Precedent'),
    ('voices', 'Voices from inside'), ('regional', 'Regional variants'), ('questions', 'The questions'),
    ('leaving', 'Leaving safely here'), ('help', 'Where to get help'), ('sources', 'Sources'),
    ('changed', 'What changed on this page'),
]
SLUG_N = {slug: i for i, (slug, _) in enumerate(SECTIONS, 1)}

# claim-register "Section" words -> skeleton sections (for per-section citations)
CITE_MAP = [
    (r'size|demograph|adherent|member', 'structure'), (r'timeline|origin|turning|history', 'history'),
    (r'apex|roster|authority|structure|succession|officeholder', 'structure'),
    (r'money|pipeline|scorecard|finance|tax|kirchensteuer', 'money'), (r'genealog', 'genealogy'),
    (r'\binfo|children|gender|reach|bod', 'reach'), (r'tactic|grade|cycle|technique', 'techniques'),
    (r'loop', 'loops'), (r'phrasebook|language|say', 'say-do'), (r'exit|cost|deniab', 'cost'),
    (r'benefit|leverage|pays|ledger', 'ledger'), (r'differential|hurt', 'who-gets-hurt'), (r'tier', 'tiers'),
    (r'\bcase', 'cases'), (r'victor|precedent|promise', 'precedent'), (r'regional|card', 'regional'),
    (r'hard question|compel|question', 'questions'), (r'healthy', 'healthy'),
    (r'sector|forefront|unanswered', 'forefront'), (r'\blaw\b', 'law'), (r'branch', 'branches'),
]

KEYWORDS = {  # for pulling a religion's rows out of the cross-cutting volumes
    'catholicism': ['Catholic', 'Vatican', 'pope', 'Pope'], 'eastern-orthodoxy': ['Orthodox Church', 'Patriarch'],
    'protestant-evangelical': ['Evangelical', 'Southern Baptist', 'Protestant'],
    'pentecostal-charismatic': ['Pentecostal', 'Charismatic', 'Hillsong', 'prosperity'],
    'sunni-islam': ['Sunni', 'al-Azhar', 'Muslim', 'Islam'], 'shia-islam': ['Shia', 'Shiʿa', 'Iran', 'Najaf'],
    'islam': ['Muslim', 'Islam'], 'orthodox-hasidic-judaism': ['Hasidic', 'Haredi', 'agunah', 'yeshiva'],
    'judaism': ['Jewish', 'Judaism', 'rabbi', 'Rabbi'], 'hinduism': ['Hindu', 'Sabarimala'],
    'tibetan-buddhism': ['Tibetan', 'Shambhala', 'Rigpa', 'Panchen', 'Dalai'], 'buddhism': ['Buddhis'],
    'sikhism': ['Sikh', 'SGPC'], 'jainism': ['Jain'], 'taoism': ['Taoist', 'Daoist'], 'confucianism': ['Confucian'],
    'shinto': ['Shinto', 'Yasukuni'], 'zoroastrianism': ['Zoroastrian', 'Parsi'], 'bahai': ['Bahá', 'Universal House'],
    'mormonism': ['Latter-day', 'LDS', 'Mormon'], 'seventh-day-adventism': ['Adventist'],
    'jehovahs-witnesses': ['Jehovah', 'Watch Tower', 'Watchtower', 'blood'], 'scientology': ['Scientology', 'Sea Org'],
    'hare-krishna': ['ISKCON', 'Krishna'], 'new-age': ['New Age', 'ayahuasca', 'NXIVM', 'sweat-lodge', 'wellness'],
    'indigenous': ['Indigenous', 'residential school', 'residential-school'], 'christianity': ['Christian'],
    'anglicanism': ['Anglican', 'Church of England', 'Canterbury'], 'ahmadiyya': ['Ahmadi'],
    'dawoodi-bohra': ['Bohra'], 'soka-gakkai': ['Soka'], 'unification-church': ['Unification'],
    'oriental-orthodoxy': ['Coptic', 'Oriental Orthodox'], 'plymouth-brethren': ['Brethren'],
}


# ---------------------------------------------------------------- helpers
SMALL = {'a', 'an', 'the', 'of', 'to', 'and', 'or', 'in', 'on', 'for'}


def title_case(t):
    words = t.lower().split(' ')
    return ' '.join(w if (i and w in SMALL) else (w[:1].upper() + w[1:]) for i, w in enumerate(words)).replace('Darvo', 'DARVO')


def esc_cell(t):
    return str(t).replace('|', '\\|').replace('\n', ' ').strip()


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    out += ['| ' + ' | '.join(esc_cell(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)


def bullets(items):
    return '\n'.join(f'- {i}' for i in items if i)


def box(kind, body, attrs=''):
    return f'::: {kind}{(" " + attrs) if attrs else ""}\n{body.strip()}\n:::'


def strip_html(t):
    return re.sub(r'<[^>]+>', '', t or '')


def fields_md(path):
    """Parse a `## field` record into {field: raw markdown}. Field names are lowercased first words."""
    if not os.path.exists(path):
        return {}
    text = open(path, encoding='utf-8').read()
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r'^## (.+?)\s*$', line)
        if m:
            if cur is not None:
                out[cur] = '\n'.join(buf).strip()
            name = m.group(1)
            key = re.split(r'[\s(]', name.strip(), 1)[0]
            cur = {'Cross-references': 'xref', 'The': 'mechanisms' if '30 mechanisms' in name else 'the',
                   'Sources': 'sources', 'Fact-check': 'factcheck', 'LGBTQ': 'lgbtq'}.get(key, key)
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = '\n'.join(buf).strip()
    return {k: v.rstrip('-').strip() for k, v in out.items()}


def xref_parts(md):
    """Split a new-tradition Cross-references block on its **label** lines."""
    parts, cur, buf = {}, None, []
    for line in md.splitlines():
        m = re.match(r'^\*\*([a-z][a-z ()≥0-9]+?)\*\*:?\s*(.*)$', line)
        if m:
            if cur: parts[cur] = '\n'.join(buf).strip()
            cur = m.group(1).split(' (')[0].strip()
            buf = [m.group(2)] if m.group(2) else []
        elif cur:
            buf.append(line)
    if cur: parts[cur] = '\n'.join(buf).strip()
    return parts


def sources_block(path):
    """(numbered source lines as markdown, {section: [n]}, corrections list) from a sources/<id>.md page."""
    if not os.path.exists(path):
        return '', {}, []
    s = open(path, encoding='utf-8').read()
    m = re.search(r'^## Sources \(reader-facing[^\n]*\n(.*?)(?=^---\s*$|^## )', s, re.S | re.M)
    body = m.group(1).strip() if m else ''
    cites = {}
    reg = re.search(r'^## Claim register\s*\n(.*?)(?=^---\s*$|^## )', s, re.S | re.M)
    if reg:
        for row in reg.group(1).splitlines():
            cells = [c.strip() for c in row.strip().strip('|').split('|')]
            if len(cells) < 4 or cells[0] in ('Section', '') or set(cells[0]) <= set('-'):
                continue
            nums = [int(x) for x in re.findall(r'(?<![A-Za-z] )\b(\d{1,3})\b', cells[-1])
                    if not re.search(r'[A-Za-z]+ ' + x, cells[-1])]
            for part in re.split(r'[/,;—]', cells[0].lower()):
                for rx, slug in CITE_MAP:
                    if re.search(rx, part):
                        cites.setdefault(slug, set()).update(nums)
                        break
    corr = re.search(r'^## Corrections to apply in the next build[^\n]*\n(.*?)(?=^## |\Z)', s, re.S | re.M)
    corrections = re.findall(r'^\d+\.\s+(.*)$', corr.group(1), re.M) if corr else []
    return body, {k: sorted(v) for k, v in cites.items()}, corrections


def cite_line(nums, valid):
    nums = [n for n in nums if n in valid]
    if not nums:
        return ''
    return box('cites', 'Sources for this section: ' + ' '.join(f'[{n}]' for n in nums))


def source_numbers(md):
    return {int(n) for n in re.findall(r'^\s*(\d+)\.\s', md, re.M)}


# ---------------------------------------------------------------- the book record for one religion
def book_record(B, rid):
    D, V2, V3, V6, V7 = B['CODEX_DATA'], B['CODEX_V2'], B['CODEX_V3'], B['CODEX_V6'], B['CODEX_V7']
    rel = next((r for r in D['religions'] if r['id'] == rid), None)
    if not rel:
        return None
    idx = str([r['id'] for r in D['religions']].index(rid) + 1)
    kw = KEYWORDS.get(rid, []) + [rel['name']]
    vol_rows = {}
    for vol in ('women', 'medical', 'lgbtq'):
        for d in V7[vol].get('domains', []):
            for r in d.get('record', []):
                if any(k in r for k in kw):
                    vol_rows.setdefault(V7[vol]['title'], []).append(f"*{d.get('name', '')}* — {r}")
    for d in V6['children'].get('domains', []):
        for r in d.get('record', []):
            t = f'{r[0]}: {r[1]}' if isinstance(r, list) else r
            if any(k in t for k in kw):
                vol_rows.setdefault("The Children's Codex", []).append(f"*{d.get('name', '')}* — {t}")
    return {
        'rel': rel, 'idx': idx,
        'tactics': [(t, t['entries'].get(idx), D['graded'].get(f'{rid}:{t["order"]}'), D['tacticMeta'].get(str(t['order'])))
                    for t in sorted(D['tactics'], key=lambda t: t['order'])],
        'stages': D['stages'], 'loops': D['loops'], 'apex': V2['apex'].get(rid), 'unanswered': V2['unanswered'].get(rid),
        'compel': V3['compel'].get(rid), 'revise': V3['revise'].get(rid), 'turning': V3['turning'].get(rid),
        'phrase': V6['language']['per'].get(rid), 'cards': V6['regions']['cards'].get(rid, []),
        'score': V7['score'].get(rid), 'score_cols': V7['scorecard']['cols'], 'score_key': dict(V7['scorecard']['key']),
        'sector': D['sector'].get(rid), 'cases': [c for c in D['cases'] if c.get('tradition', '') == rid],
        'coverage': next((c for c in D['coverage'] if c.get('id', '') == rid), None),
        'pipelines': [p for p in D['pipelines'] if rid in p.get('religions', [])],
        'succession': [r for r in V7['succession']['rows'] if any(k in json.dumps(r, ensure_ascii=False) for k in kw)],
        'promises': [r for r in V7['promises']['rows'] if any(k in r[0] for k in kw)],
        'vol_rows': vol_rows, 'tac_names': {t['order']: title_case(t['name']) for t in D['tactics']},
        'grade_vocab': {g[0]: g[2] for g in D['gradeVocab']},
    }


# ---------------------------------------------------------------- section writers
def md_religion(B, rid):
    book = book_record(B, rid)
    new = fields_md(os.path.join(CONTENT, 'new-traditions', f'{rid}.md'))
    add = fields_md(os.path.join(CONTENT, 'additions', f'{rid}.md'))
    xr = xref_parts(new.get('xref', '')) if new else {}
    if book:
        src_md, cites, corrections = sources_block(os.path.join(CONTENT, 'sources', f'{rid}.md'))
    else:
        src_md, cites, corrections = new.get('sources', ''), {}, []
    valid = source_numbers(src_md)
    r = book['rel'] if book else None
    name = r['name'] if r else re.sub(r'^# (.+?) —.*', r'\1', open(os.path.join(CONTENT, 'new-traditions', f'{rid}.md')).readline().strip())
    fid, fname, members = FAMILY_OF[rid]
    S = {slug: [] for slug, _ in SECTIONS}
    tacs = book['tac_names'] if book else {}

    def put(slug, *blocks):
        S[slug].extend(b for b in blocks if b and b.strip())

    def sub(slug, title, body):
        if body and body.strip():
            S[slug].append(f'### {title}\n\n{body.strip()}')

    if book:
        rel, dem = r, r['demographics']
        # 1 at a glance
        apex0 = (book['apex'] or {}).get('rows', [[]])[0] if book['apex'] else []
        cov = book['coverage'] or {}
        glance = [['Size', strip_html(dem.get('adherents', ''))]]
        if apex0:
            glance.append(["Who's in charge", f'{apex0[0]} — {apex0[1]}'])
            glance.append(['Chosen by / removable by', f'{apex0[2]} / {apex0[3]}'])
        glance += [['Money in one line', rel['money'][0]], ['Leaving in one line', rel['exit'][0]]]
        if book['unanswered']: glance.append(['The unanswered question', book['unanswered']])
        if cov: glance.append(['Evidence', f"{cov['n']} of 30 techniques sourced to a named document; grades: " +
                                ', '.join(f'{g} {n}' for g, n in cov['by'])])
        glance.append(['Family', f'{fname} — ' + ', '.join(members)])
        glance.append(['Last checked', CHECKED])
        put('at-a-glance', box('glance', table(['', ''], glance)))
        if book['score']:
            put('at-a-glance', '### Disclosure scorecard\n\n' + table([c[0] for c in book['score_cols']], [book['score']]) +
                '\n\n' + ' · '.join(f'**{k}** {v}' for k, v in book['score_key'].items()))
        # 2 day
        d = rel['day']
        put('a-day-inside', f"*{d.get('name', '')} · {d.get('when', '')} · {d.get('where', '')}*", *d['para'])
        # 3 forefront
        put('forefront', box('lede', rel['opening']))
        if book['unanswered']: sub('forefront', 'The unanswered question', box('question', book['unanswered']))
        if rel['language']:
            l0 = rel['language'][0]
            sub('forefront', 'The widest gap between word and record', table(['They say', 'The record shows', 'Receipt'], [[l0['say'], l0['do'], l0['receipt']]]))
        if rel['exitTable']:
            e0 = rel['exitTable'][0]
            sub('forefront', 'One cost of leaving, beside its denial', table(['Cost', 'Documented?', 'Detail', 'The official denial'], [e0]))
        if book['sector']:
            s = book['sector']
            sub('forefront', 'The strongest objection, answered', f"**The objection.** {s.get('attack', '')}\n\n**What is true in it.** {s.get('concede', '')}\n\n**The answer.** {s.get('answer', '')}")
        # 4 healthy
        put('healthy', box('lede', rel['neutral']), bullets(rel['healthy']))
        # 5 history
        put('history', rel['origin'])
        sub('history', 'Timeline', '```timeline\n' + '\n'.join(' | '.join(c.replace('|', '/') for c in row) for row in rel['timeline']) + '\n```')
        if book['turning']:
            sub('history', 'Moments in the room', '\n\n'.join(
                box('card', f"#### {t[0]} — {t[1]}\n\n{t[2]}\n\n**Why it matters.** {t[3]}") for t in book['turning']))
        # 6 branches
        put('branches', dem.get('branches', ''))
        # 7 structure
        sub('structure', 'Size and shape', table(['', ''], [[k.title(), strip_html(v)] for k, v in dem.items() if k != 'branches']))
        sub('structure', 'Authority', bullets(rel['authority']))
        if book['apex']:
            a = book['apex']
            sub('structure', 'The top of the chain', box('lede', a.get('lede', '')) + '\n\n' +
                table(['Office', 'Who sits in it now', 'Chosen by', 'Removable by'], a['rows']) + '\n\n' + box('tell', a.get('tell', '')))
        sub('structure', 'Who holds what', table(['Entity', 'Type', 'Holder', 'Holds', 'Why it matters to you', 'Receipt'],
                                                [[x.get('entity', ''), x.get('type', ''), x.get('holder', ''), x.get('holds', ''), x.get('sector', ''), x.get('receipt', '')] for x in rel['roster']]))
        for row in book['succession']:
            sub('structure', 'Succession watch', table(['Office', 'Now', 'Mechanism', 'Prediction', 'What would falsify it'],
                                                      [[row.get('office', ''), row.get('current', ''), row.get('mechanism', ''), row.get('predict', ''), row.get('test', '')]]))
        # 8 law
        if book['compel']: sub('law', 'Who can compel an answer', book['compel'])
        # 9 money
        sub('money', 'Where it comes from', bullets(rel['money']))
        sub('money', 'Follow the money', table(['Flow', 'Stated purpose', 'How it controls', 'Who benefits'], rel['moneyTable']))
        if book['pipelines']:
            sub('money', 'Pipelines this tradition shares', '\n\n'.join(
                box('card', f"#### {p.get('name', '')}\n\n**Source.** {p.get('source', '')}\n\n**Path.** {' → '.join(p['path'])}\n\n"
                            f"**Disclosed.** {p.get('discloses', '')}\n\n**Hidden.** {p.get('hides', '')}") for p in book['pipelines']))
        # 10 genealogy
        put('genealogy', '\n\n'.join(box('card', f"#### {g.get('mechanism', '')}\n\n**Origin.** {g.get('origin', '')}\n\n**What it was for.** {g.get('thenPurpose', '')}\n\n"
                                                 f"**Why that reason expired.** {g.get('expired', '')}\n\n**Who benefits now.** {g.get('benefitsNow', '')}") for g in rel['genealogy']))
        # 11 reach
        sub('reach', 'Information', bullets(rel['info']))
        sub('reach', 'Children', bullets(rel['children']))
        sub('reach', 'Bodies', bullets(rel['gender']))
        # 12 techniques
        put('techniques', 'Thirty named techniques from domestic-abuse and social-psychology research, applied to institutions, '
                          'in the eight stages of the cycle. Each carries an evidence grade for this tradition.')
        by_stage = {c.get('n', ''): c for c in rel['cycle']}
        for st in book['stages']:
            c = by_stage.get(st.get('n', ''), {})
            body = [box('stage', f"**{st.get('essence', '')}**\n\n{c.get('shows', '')}\n\n*What it asks of you:* {c.get('you', '')}")]
            for n in st['tactics']:
                t, e, g, meta = book['tactics'][n - 1]
                if not e: continue
                grade = f"[[{g[0]}]] {g[1]}" + (' *(sourced)*' if g[2] == 'sourced' else '') if g else '[[Ungraded]]'
                body.append(box('tactic', f"#### {n} · {title_case(t['name'])} {{#t-{n}}}\n\n*{meta.get('def', '')}*\n\n"
                                          f"**How it shows here**\n\n{bullets(e['examples'])}\n\n"
                                          f"**The strongest defense.** {' '.join(e['defenses'])}\n\n"
                                          f"**The counter.** {' '.join(e['counters'])}\n\n**Evidence grade.** {grade}", f'n={n}'))
            sub('techniques', f"Stage {st.get('n', '')} · {st.get('name', '').title()} {{#stage-{st.get('n', '')}}}", '\n\n'.join(body))
        # 13 loops
        put('loops', '\n\n'.join(box('card', f"#### {l.get('n', '')} · {l.get('name', '')}\n\n{rel['loopHere'].get(str(l.get('n', '')), '')}") for l in book['loops']))
        # 14 say-do
        sub('say-do', 'What they say, what the record shows', table(['They say', 'The record shows', 'Receipt'], [[x.get('say', ''), x.get('do', ''), x.get('receipt', '')] for x in rel['language']]))
        ch = rel['chairHere']
        sub('say-do', 'Accountability or theatre?', f"**Last time the chair ran.** {ch.get('lastRan', '')}\n\n**Who holds the chair now.** {ch.get('chairNow', '')}\n\n**Prediction.** {ch.get('predict', '')}")
        if book['phrase']:
            sub('say-do', 'Words used here', table(['Term', 'What it means inside', 'What it does', 'Said plainly'], book['phrase']))
        # 15 cost
        sub('cost', 'What leaving costs', bullets(rel['exit']))
        sub('cost', 'The ledger of exit', table(['Cost', 'Documented?', 'Detail', 'The official denial'], rel['exitTable']))
        sub('cost', 'How the cost is denied', table(['Channel', 'Level', 'Note'], rel['deniability']))
        # 16 ledger
        sub('ledger', 'Who benefits', bullets(rel['whoBenefits']))
        sub('ledger', 'Money out, leverage back', bullets(rel['leverage']))
        sub('ledger', 'Who pays', bullets(rel['whoPays']))
        # 17 who gets hurt
        sub('who-gets-hurt', 'Where the weight lands', table(['Who', 'How', 'What it compounds with'], [[x.get('who', ''), x.get('how', ''), x.get('compounds', '')] for x in rel['differential']]))
        for vol, rows in book['vol_rows'].items():
            sub('who-gets-hurt', f'From {vol}', bullets(rows))
        # 18 tiers
        put('tiers', table(['Role', 'Does', 'Sees', 'Is asked to', 'Could refuse'], [[x.get('role', ''), x.get('does', ''), x.get('sees', ''), x.get('asked', ''), x.get('couldRefuse', '')] for x in rel['tiers']]))
        # 19 cases
        for c in book['cases']:
            put('cases', box('case', f"### {c.get('title', '')}\n\n- **when:** {c.get('when', '')}\n- **what:** {c.get('what', '')}\n- **record:** {c.get('source', '')}\n"
                                     f"- **outcome:** {c.get('outcome', '')}\n- **tactics:** {', '.join(map(str, c['tactics']))}\n- **grade:** {c.get('grade', '')}"))
        # 20 precedent
        sub('precedent', 'It has been broken before', table(['What', 'Who', 'When', 'What it cost'], [[v.get('what', ''), v.get('who', ''), v.get('when', ''), v.get('cost', '')] for v in rel['victories']]))
        if book['promises']:
            sub('precedent', 'Promises on the record', table(['Commitment', 'Made', 'Status', 'Note'], book['promises']))
        if book['revise']: sub('precedent', 'What would change this page', book['revise'])
        # 22 regional
        for c in book['cards']:
            put('regional', box('card', f"### {c.get('place', '')}\n\n- **apex:** {c.get('apex', '')}\n- **law:** {c.get('law', '')}\n- **documented:** {c.get('documented', '')}\n"
                                        f"- **exit:** {c.get('exit', '')}\n- **regulator:** {c.get('regulator', '')}\n- **tell:** {c.get('tell', '')}"))
        # 23 questions
        put('questions', '\n'.join(f'{i}. {q}' for i, q in enumerate(rel['hardQuestions'], 1)))
        sub('questions', 'In closing', '\n\n'.join(rel['closing']))
        # per-section citations from the claim register
        for slug, nums in cites.items():
            line = cite_line(nums, valid)
            if line and S.get(slug): S[slug].append(line)
    elif new:
        # the 7 new religions: their own fields, slotted into the same skeleton
        dem = new.get('demographics', '')
        glance = [['Size', (re.search(r'\*\*adherents:\*\*\s*(.*)', dem) or [None, ''])[1]], ['Family', f'{fname} — ' + ', '.join(members)],
                  ['The unanswered question', xr.get('unanswered', '')], ['Last checked', CHECKED]]
        put('at-a-glance', box('glance', table(['', ''], [g for g in glance if g[1]])))
        if xr.get('scorecard'): put('at-a-glance', '### Disclosure scorecard\n\n' + xr['scorecard'])
        put('a-day-inside', new.get('day', ''))
        put('forefront', box('lede', new.get('opening', '')))
        if xr.get('unanswered'): sub('forefront', 'The unanswered question', box('question', xr['unanswered']))
        if xr.get('sector defense'): sub('forefront', 'The strongest objection, answered', xr['sector defense'])
        put('healthy', box('lede', new.get('neutral', '')), new.get('healthy', ''))
        put('history', new.get('origin', ''))
        sub('history', 'Timeline', new.get('timeline', ''))
        sub('history', 'Moments in the room', xr.get('turning points', ''))
        put('branches', (re.search(r'\*\*branches:\*\*\s*(.*)', dem) or [None, ''])[1])
        sub('structure', 'Size and shape', dem)
        sub('structure', 'Authority', new.get('authority', ''))
        sub('structure', 'The top of the chain', xr.get('apex', '') + ('\n\n' + box('tell', xr['tell']) if xr.get('tell') else ''))
        sub('structure', 'Who holds what', new.get('roster', ''))
        if xr.get('compel'): sub('law', 'Who can compel an answer', xr['compel'])
        sub('money', 'Where it comes from', new.get('money', ''))
        sub('money', 'Follow the money', new.get('moneyTable', ''))
        put('genealogy', new.get('genealogy', ''))
        sub('reach', 'Information', new.get('info', ''))
        sub('reach', 'Children', new.get('children', ''))
        sub('reach', 'Bodies', new.get('gender', ''))
        sub('reach', 'LGBTQ+', new.get('lgbtq', ''))
        sub('techniques', 'The eight stages here', new.get('cycle', ''))
        sub('techniques', 'All thirty, graded', new.get('mechanisms', ''))
        put('loops', new.get('loopHere', ''))
        sub('say-do', 'What they say, what the record shows', new.get('language', ''))
        sub('say-do', 'Accountability or theatre?', new.get('chairHere', ''))
        sub('say-do', 'Words used here', xr.get('phrasebook', ''))
        sub('cost', 'What leaving costs', new.get('exit', ''))
        sub('cost', 'The ledger of exit', new.get('exitTable', ''))
        sub('cost', 'How the cost is denied', new.get('deniability', ''))
        sub('ledger', 'Who benefits', new.get('whoBenefits', ''))
        sub('ledger', 'Money out, leverage back', new.get('leverage', ''))
        sub('ledger', 'Who pays', new.get('whoPays', ''))
        sub('who-gets-hurt', 'Where the weight lands', new.get('differential', ''))
        put('tiers', new.get('tiers', ''))
        put('cases', xr.get('documented cases', ''))
        sub('precedent', 'It has been broken before', new.get('victories', ''))
        if xr.get('revise'): sub('precedent', 'What would change this page', xr['revise'])
        if xr.get('regional cards'): put('regional', box('gap', 'Proposed cards, not yet written: ' + xr['regional cards']))
        put('questions', new.get('hardQuestions', ''))
        sub('questions', 'In closing', new.get('closing', ''))

    # additions (new sections, both kinds of religion)
    if add.get('branches'): put('branches', add['branches'])
    if add.get('law'): S['law'].insert(0, add['law'])
    if add.get('moneyNumbers'): sub('money', 'Money in numbers', add['moneyNumbers'])
    if add.get('cases'):
        put('cases', '\n\n'.join(box('case', blk.strip()) for blk in re.split(r'(?=^### )', add['cases'], flags=re.M) if blk.strip()))
    if add.get('voices'): put('voices', add['voices'])
    if add.get('regional'):
        put('regional', '\n\n'.join(box('card', blk.strip()) for blk in re.split(r'(?=^### )', add['regional'], flags=re.M) if blk.strip()))
    if add.get('whoHurt'): sub('who-gets-hurt', 'More on who gets hurt', add['whoHurt'])
    if add.get('leaving'): put('leaving', add['leaving'])
    if add.get('help'): put('help', add['help'])
    if src_md: put('sources', src_md)
    changed = add.get('changed') or (bullets([f'**{CHECKED} — fact-check pass 1:** {c}' for c in corrections]) if corrections else '')
    if new and new.get('factcheck') and not add.get('changed'):
        changed = new['factcheck']
    put('changed', changed)

    # ---------------------------------------------------------------- assemble
    filled = {slug: bool(S[slug]) for slug, _ in SECTIONS}
    # thin sections: present but below the page standard — shown with a notice, counted as partial
    partial = set()
    if filled['law'] and not add.get('law'): partial.add('law')
    if filled['branches'] and not add.get('branches'): partial.add('branches')
    n_cases = len(book['cases']) if book else 0
    n_cases += len(re.findall(r'^### ', add.get('cases', ''), re.M))
    if new and xr.get('documented cases'): n_cases += len(re.findall(r'^\d+\. ', xr['documented cases'], re.M))
    if filled['cases'] and n_cases < 3: partial.add('cases')
    if filled['regional'] and not (book and book['cards']) and not add.get('regional'): partial.add('regional')
    if filled['money'] and not add.get('moneyNumbers'): partial.add('money')
    for slug in partial:
        S[slug].insert(0, box('gap', f'**Partly documented for {name}.** This section is below the page standard and is on the fill list.'))
    n_filled = sum(filled.values())
    status = {slug: ('partial' if slug in partial else 'filled' if ok else 'missing') for slug, ok in filled.items()}
    fm = ['---', f'id: {rid}', f'title: "{name}"', f'family: "{fname}"', f'family_id: {fid}',
          'family_members: [' + ', '.join(members) + ']', f'version: {VERSION}', f'checked: {CHECKED}',
          f'sections_filled: {n_filled}/{len(SECTIONS)}',
          'missing: [' + ', '.join(s for s, ok in filled.items() if not ok) + ']',
          'partial: [' + ', '.join(sorted(partial)) + ']', '---', '']
    body = [f'# {name} {{#top}}', '']
    for i, (slug, title) in enumerate(SECTIONS, 1):
        body.append(f'## {i}. {title} {{#{slug}}}')
        body.append('')
        if S[slug]:
            body.append('\n\n'.join(S[slug]))
        else:
            body.append(box('gap', f'**Not yet documented for {name}.** This section is on the fill list — see `religions/_coverage.md`.'))
        body.append('')
    return '\n'.join(fm + body) + '\n', status


def how_to_read(B):
    """The shared front matter every religion's PDF opens with: grades, receipt types, method."""
    D = B['CODEX_DATA']
    out = ['# How to read this {#how-to-read}', '',
           'Every religion in The Sacred Divide is laid out the same way, in the same 27 sections, so that any section '
           'can be compared across religions. This file examines institutions, offices, money and power. It does not '
           'judge anyone\'s faith or the truth of any belief.', '',
           '## Evidence grades {#grades}', '',
           'Each of the 30 techniques carries a grade for how it is established in this tradition.', '']
    out += [f'- [[{g[0]}]] {g[2]}' for g in D['gradeVocab']]
    out += ['', '## Receipts {#receipts}', '', 'Bracketed labels such as [OFFICIAL POLICY] name the kind of source a claim rests on.', '']
    out += [f'- **{t[0]}.** {t[1]}' for t in D['receiptTypes']]
    out += ['', '## Method {#method}', ''] + [f'- {m}' for m in D['methodology']]
    out += ['', '## Citations {#citations}', '',
            'A number in brackets, such as [12], links to item 12 in this religion\'s Sources, at the end of the file. '
            'Every source was checked for this edition.', '']
    return '\n'.join(out) + '\n'


def main():
    B = P.load(BOOK)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, '_how-to-read.md'), 'w', encoding='utf-8').write(how_to_read(B))
    import base64
    mark = B['CODEX_DATA']['img']['mkLg'].split(',', 1)[1]
    open(os.path.join(ROOT, 'tools/pdf/mark.png'), 'wb').write(base64.b64decode(mark))
    rows, order = [], [rid for _, _, members in FAMILIES for rid in members]
    for rid in order:
        md, filled = md_religion(B, rid)
        open(os.path.join(OUT, f'{rid}.md'), 'w', encoding='utf-8').write(md)
        rows.append((rid, filled))
    head = ['Religion'] + [str(SLUG_N[s]) for s, _ in SECTIONS] + ['Filled']
    lines = ['# Coverage — which sections each religion has', '',
             f'Generated by `scripts/sacred-divide-export-md.py` on {date.today()}. ✅ filled to the page standard · ◐ partial (thin; shows a notice) · ⏳ empty (shows a gap notice in the PDF).', '',
             'Sections: ' + ' · '.join(f'{SLUG_N[s]} {t}' for s, t in SECTIONS), '',
             '| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for rid, filled in rows:
        mark = {'filled': '✅', 'partial': '◐', 'missing': '⏳'}
        lines.append('| ' + ' | '.join([rid] + [mark[filled[s]] for s, _ in SECTIONS] +
                                       [f"{sum(v == 'filled' for v in filled.values())}/{len(SECTIONS)}"]) + ' |')
    totals = {s: sum(f[s] == 'filled' for _, f in rows) for s, _ in SECTIONS}
    lines.append('| **religions with it** | ' + ' | '.join(str(totals[s]) for s, _ in SECTIONS) + f' | {sum(totals.values())}/{len(SECTIONS) * len(rows)} |')
    open(os.path.join(OUT, '_coverage.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'wrote {len(rows)} religion files; {sum(totals.values())} of {len(SECTIONS) * len(rows)} sections filled')
    for s, t in SECTIONS:
        print(f'  {SLUG_N[s]:>2} {t:<32} {totals[s]}/{len(rows)}')


if __name__ == '__main__':
    main()
