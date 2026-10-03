#!/usr/bin/env python3
"""Build the TikTok slide series for one volume from its own Markdown (content/sacred-divide/religions/<id>.md,
after edits). Every slide is cleaned text taken from the volume: citation numbers, receipt labels and
cross-reference parentheticals are dropped (the reader is led to the sources separately); facts are not changed.
Output: content/sacred-divide/tiktok/<id>.json, then run scripts/sacred-divide-tiktok.py <id> to render PNGs.
Usage: sacred-divide-tiktok-build.py protestant-evangelical"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rid = sys.argv[1]
MD = open(os.path.join(ROOT, 'content/sacred-divide/religions', rid + '.md'), encoding='utf-8').read()
META = re.match(r'---\n(.*?)\n---', MD, re.S).group(1)
TITLE = re.search(r'^title: "(.*)"', META, re.M).group(1)
SITE = 'noblefathercreations.com/faith'

# ------------------------------------------------------------------ text cleaning
def clean(t):
    t = re.sub(r'\[\[(\w+)\]\]', r'\1', t)
    t = re.sub(r'\*\(sourced\)\*', '', t)
    t = re.sub(r'(?:\s*\[\d+\])+', '', t)                                    # citation numbers
    t = re.sub(r'\s*\[(?:[A-Z][A-Z /\-]+)(?::[^\]]*)?\]', '', t)            # receipt labels like [INVESTIGATIVE REPORT]
    t = re.sub(r'\s*\((?:sections?|techniques?|stage)\s[^)]*\)', '', t)      # (section 9; technique 26)
    t = re.sub(r'\bIn section 2, ', 'In the day-inside story, ', t)
    t = re.sub(r' in sections? \d+(?:[ ,]*(?:and|&)? ?\d+)*', '', t)
    t = re.sub(r'(^|[.;:] )[Ss]ections? \d+(?: and \d+)? ', lambda m: m.group(1) + 'The full record ', t)
    t = re.sub(r'\b([Ss])ections? \d+(?: and \d+)? ', lambda m: 'the full record ', t)
    t = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', t)                          # links
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t); t = re.sub(r'\*(.+?)\*', r'\1', t)
    t = t.replace('The full record records', 'The full record shows').replace('“', '"').replace('”', '"').replace('’', "'")
    t = re.sub(r'\s+([.,;:])', r'\1', t); t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def sections():
    parts = re.split(r'^## (\d+)\. (.+?) \{#([\w-]+)\}\s*$', MD, flags=re.M)
    return {int(parts[i]): (parts[i + 1], parts[i + 2], parts[i + 3]) for i in range(1, len(parts), 4)}
SECS = sections()

def sec(n):
    parts = re.split(r'^## (\d+)\. .*$', MD, flags=re.M)
    for i in range(1, len(parts), 2):
        if int(parts[i]) == n: return parts[i + 1]
    raise KeyError(n)

def subs(text):
    """{heading: body} for ### subsections ('' = text before the first)."""
    out = {}; cur = ''; buf = []
    for ln in text.split('\n'):
        m = re.match(r'### (.+)', ln)
        if m: out[cur] = '\n'.join(buf); cur = m.group(1).strip(); buf = []
        else: buf.append(ln)
    out[cur] = '\n'.join(buf); return out

def table(text):
    rows = []
    for ln in text.split('\n'):
        if ln.startswith('|') and not re.match(r'^\|[\s\-|:]+\|$', ln):
            rows.append([c.strip() for c in ln.strip().strip('|').split(' | ')] if ' | ' in ln else [c.strip() for c in ln.strip().strip('|').split('|')])
    return rows

def bullets(text): return [clean(re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', l)) for l in text.split('\n') if re.match(r'^\s*(?:[-*]|\d+\.)\s+', l)]
def paras(text):
    out = []
    for blk in re.split(r'\n\s*\n', text):
        b = blk.strip()
        if not b or b.startswith(('|', ':::', '```', '- ', '1.', '#')): continue
        out.append(clean(b))
    return [p for p in out if p]

def cards(text):
    res = []
    for m in re.finditer(r'::: card\n(.*?)\n:::', text, re.S):
        blk = m.group(1); title = re.search(r'^#{3,4} (.+)$', blk, re.M).group(1).strip()
        fields = {k: clean(v) for k, v in re.findall(r'\*\*([^*]+?)\.\*\*\s*(.+?)(?=\n\n\*\*|\n\n\d\.|\Z)', blk, re.S)}
        res.append((clean(title), fields, blk))
    return res

# ------------------------------------------------------------------ slide makers
def chunk(items, size_of, limit):
    limit = limit * 0.8   # lighter slides: keeps type large enough to read on a phone
    groups, cur, n = [], [], 0
    for it in items:
        s = size_of(it)
        if cur and n + s > limit: groups.append(cur); cur, n = [], 0
        cur.append(it); n += s
    if cur: groups.append(cur)
    return groups

def title_n(head, i, n): return head if i == 1 else f'{head} (cont.)'

def rows_slides(kicker, head, rows, limit=760, note=None, style='dark'):
    rows = [(a, re.sub(r'([^.!?"\'\s])\s+(Does|Sees|Is asked to|Could refuse|Chosen by|Removable by|Why it matters to you|The question|The denial|Compounded by|What it does|Said plainly|Inside|Who|Status|Cost|When): ', r'\1. \2: ', b)) for a, b in rows]
    groups = chunk(rows, lambda r: len(r[0]) + len(r[1]) + 20, limit)
    return [{'type': 'rows', 'style': style, 'kicker': kicker, 'head': title_n(head, i + 1, len(groups)), 'rows': g, **({'note': note} if note and i == len(groups) - 1 else {})} for i, g in enumerate(groups)]

def bullet_slides(kicker, head, items, intro=None, limit=950, note=None, style='dark'):
    groups = chunk(items, lambda s: len(s) + 30, limit - (len(intro) if intro else 0))
    return [{'type': 'bullets', 'style': style, 'kicker': kicker, 'head': title_n(head, i + 1, len(groups)), **({'intro': intro} if intro and i == 0 else {}), 'items': g, **({'note': note} if note and i == len(groups) - 1 else {})} for i, g in enumerate(groups)]

def text_slides(kicker, head, ps, limit=900, style='dark', note=None):
    groups = chunk(ps, lambda s: len(s) + 40, limit)
    return [{'type': 'text', 'style': style, 'kicker': kicker, 'head': title_n(head, i + 1, len(groups)), 'paras': g, **({'note': note} if note and i == len(groups) - 1 else {})} for i, g in enumerate(groups)]

def table_rows(text, labels=None, skip=(), join=' '):
    """Table -> [(label, text)] where label is column 1 and the rest is joined; labels = header words to prefix."""
    t = table(text)
    hdr, body_ = t[0], t[1:]
    out = []
    for r in body_:
        parts = []
        for ci, c in enumerate(r[1:], 1):
            if ci in skip or not c: continue
            c = clean(c)
            if not c: continue
            parts.append((f'{hdr[ci]}: ' if labels and labels.get(ci) else '') + c)
        out.append((clean(r[0]), join.join(parts)))
    return out

POSTS = []
def post(id_, title, slides, style_cycle=True):
    for i, s in enumerate(slides):
        s.setdefault('style', 'dark')
    POSTS.append({'id': id_, 'title': title, 'slides': slides})

def cover(part, total, name, sub, hook):
    return {'type': 'cover', 'series': f'Part {part} of {total}', 'title': name, 'sub': sub, 'hook': hook}

NPOSTS = 7

# ================================================================== PART 1 — structure
g = subs(sec(1))
glance = {clean(r[0]): clean(r[1]) for r in table(g[''])[1:] if len(r) > 1}
P1 = [cover(1, NPOSTS, 'Who is in charge', f'{TITLE}: size, structure, history and law. A record of institutions, money and power, not of anyone\'s faith.', 'Swipe for the record →')]
P1.append({'type': 'text', 'kicker': 'What this is', 'head': 'Institutions, not belief', 'paras': ['The Sacred Divide examines institutions, offices, money and power in every religion, laid out the same way so any section can be compared.', 'It does not judge anyone\'s faith or the truth of any belief. Every claim is graded for how it is established, and every figure is sourced and dated.'], 'style': 'light'})
P1.append({'type': 'big', 'style': 'light', 'kicker': 'How big', 'big': '800M', 'head': 'Protestants worldwide', 'text': 'Pew counted 801 million in 2011, and up to 1 billion on wider definitions. Its 584 million Pentecostal and charismatic Christians span every tradition, Catholics included, so they are not a subset of that total.'})
P1.append({'type': 'bullets', 'kicker': 'Who is in charge', 'head': 'The founder\'s chair', 'items': ['In most independent churches the top office is the founder\'s chair, held by the founder or the founder\'s family.', 'Megachurch pulpits (very large churches) have passed to spouses and sons in several churches.']})
P1.append({'type': 'chain', 'kicker': 'Chosen by / removable by', 'head': 'In an independent church, there is no bishop.', 'rows': [['The founder', 'plus a board he selected'], ['The board he appointed', 'is the body that can remove him'], ['The Senate\'s Grassley inquiry', 'documented this arrangement and could not penetrate it']]})
P1.append({'type': 'text', 'kicker': 'Money in one line', 'head': 'Tithes and seed-faith', 'paras': ['Tithing, giving a tenth of income, is preached as a covenant obligation.', 'The prosperity gospel, the teaching that faith and giving bring health and wealth, turns giving into an investment product, with seed-faith donations promising divine returns.']})
P1.append({'type': 'text', 'kicker': 'Leaving in one line', 'head': 'The cost of leaving', 'paras': ['Leaving can cost the total social world that megachurches deliberately build: groups, childcare, schools and employment.'], 'style': 'light'})
P1.append({'type': 'quote', 'style': 'red', 'kicker': 'The unanswered question', 'quote': 'If membership is voluntary and the church has nothing to hide, why did departing staff have to sign non-disclosure agreements?'})
P1.append({'type': 'rows', 'kicker': 'The evidence', 'head': '30 techniques, graded', 'rows': [['2 Documented.', 'Court judgment, government inquiry, regulatory action or financial filing.'], ['18 Taught.', 'Repeated leadership instruction from the platform, publications or curriculum, without a formal rule.'], ['10 Cultural.', 'Community enforcement the institution neither mandates nor prevents.']], 'note': 'Two of the 30 are sourced to a named document.'})
P1.append({'type': 'rows', 'style': 'light', 'kicker': 'Disclosure scorecard', 'head': 'Six yes-or-no questions', 'rows': [['Accounts: Partial.', 'True of some parts of the tradition, or in some jurisdictions.'], ['Pay: No.', 'Not established from any public source.'], ['Safeguarding: Partial.', ''], ['External first: Partial.', ''], ['Removal: Partial.', ''], ['Reply: Partial.', '']], 'note': 'Yes means established from a public source. No means not established from any public source.'})
dayinside = [clean(p) for p in re.split(r'\n\s*\n', subs(sec(2))[''])[1:] if p.strip()]
P1 += text_slides('A day inside', 'Tyler, a worship leader', [dayinside[0], dayinside[1], dayinside[2]], limit=1100)
P1 += text_slides('A day inside', 'Tuesday, continued', [dayinside[3], dayinside[4], dayinside[5]], limit=1100)
obj = subs(sec(3))['The strongest objection, answered']
P1 += text_slides('The strongest objection', 'You are cherry-picking', [clean(x) for x in re.findall(r'\*\*[^*]+\*\*\s*[^\n]+', obj)], limit=1000, style='light')
heal = sec(4)
hp = paras(heal)
P1 += bullet_slides('What healthy looks like', 'Plural elders, open books', ['Plural elders: authority shared among several elders.', 'Open books and outside audits.', 'Pastors on published salaries.', 'A tradition with its own press, which has exposed its own: Christianity Today reported the rise and fall of Mars Hill and the investigation of RZIM\'s founder.', 'Survivor-led movements such as #ChurchToo have pressed for accountability.'], limit=1100)
P1 += bullet_slides('Credit where it is due', 'Standards already met', ['Southern Baptist messengers voted for an independent investigation of their own Executive Committee. Its report was published in 2022, and the Executive Committee then released its list of accused ministers.', 'Ravi Zacharias International Ministries commissioned an outside investigation of its late founder and made the finding public.', 'In 2013 Alan Chambers apologized to gay people and shut down Exodus International.', 'In 2018 Joshua Harris discontinued his own bestseller, I Kissed Dating Goodbye.', 'In England and Wales, churches that are registered charities file public accounts.'], limit=1200)
P1 += text_slides('History', 'From Reformation to megachurch', [clean(paras(sec(5))[0])], limit=1200, style='light')
tl = [ [c.strip() for c in l.split(' | ')] for l in re.search(r'```timeline\n(.*?)```', sec(5), re.S).group(1).strip().split('\n')]
P1 += rows_slides('History · timeline', 'Timeline', [(clean(a), clean(b) + ' ' + clean(c)) for a, b, c in tl], limit=800)
mom = cards(sec(5))
for t, f, blk in mom:
    P1.append({'type': 'text', 'kicker': 'Moments in the room', 'head': t, 'paras': [clean(re.sub(r'^#### .*\n', '', blk).split('\n\n**')[0].strip())] + ([clean(blk.split('**Why it matters.**')[1])] if '**Why it matters.**' in blk else []), 'style': 'dark'})
# branches
br = table(subs(sec(6))[''])
P1 += rows_slides('Branches & variants', 'Where authority sits', [(clean(r[0]), clean(r[1]) + ' Authority: ' + clean(r[2])) for r in br[1:]], limit=800, style='light')
ss = subs(sec(7))
P1 += rows_slides('Structure', 'Size and shape', [(clean(r[0]), clean(r[1])) for r in table(ss['Size and shape'])[1:]], limit=900)
P1 += bullet_slides('Structure', 'Authority', bullets(ss['Authority']), style='light')
top = table(ss['The top of the chain'])
P1 += rows_slides('Structure · the top of the chain', 'Who sits in each office', [(clean(r[0]), f'Who: {clean(r[1])} Chosen by: {clean(r[2])} Removable by: {clean(r[3])}') for r in top[1:]], limit=900)
tell = re.search(r'::: tell\n(.*?)\n:::', ss['The top of the chain'], re.S).group(1)
P1.append({'type': 'quote', 'style': 'red', 'kicker': 'The tell', 'quote': clean(tell)})
who = table(ss['Who holds what'])
P1 += rows_slides('Structure · who holds what', 'Who holds what', [(clean(r[0]), f'{clean(r[3])} Why it matters to you: {clean(r[4])}') for r in who[1:]], limit=800, style='light')
law = table(sec(8))
P1 += rows_slides('Law & state', 'What the law does', [(clean(r[0]), clean(r[1]) + ' The question: ' + clean(r[2])) for r in law[1:]], limit=800)
P1 += text_slides('Law & state', 'Who can compel an answer', [clean(paras(subs(sec(8))['Who can compel an answer'])[0])], limit=900, style='light')
post('part-1-structure', 'Part 1: Who is in charge', P1)

# ================================================================== PART 2 — money, origins, reach
m = subs(sec(9))
P2 = [cover(2, NPOSTS, 'Money, origins and reach', 'Where the money comes from, where each practice began, and what the institution reaches into.', 'Swipe →')]
P2 += bullet_slides('Money', 'Where it comes from', bullets(m['Where it comes from']), limit=1100)
flow = table(m['Follow the money'])
P2 += rows_slides('Money · follow the money', 'Five flows', [(clean(r[0]), f'{clean(r[1])} {clean(r[2])} {clean(r[3])}') for r in flow[1:]], limit=900, style='light')
for t, f, blk in cards(m['Pipelines this tradition shares']):
    P2.append({'type': 'rows', 'kicker': 'Money · pipelines this tradition shares', 'head': t, 'rows': [('Source.', f.get('Source', '')), ('Path.', f.get('Path', '')), ('Disclosed.', f.get('Disclosed', '')), ('Hidden.', f.get('Hidden', ''))], 'style': 'dark'})
P2.append({'type': 'bars', 'kicker': 'Money in numbers', 'head': 'Southern Baptist members', 'bars': [['2006', 16.3, '16.3M'], ['2023', 12.98, '12.98M'], ['2024', 12.7, '12.7M'], ['2025', 12.33, '12.33M']], 'text': '2025 was the 19th year of decline in a row, from the denomination\'s own Annual Church Profile.', 'style': 'dark'})
P2 += bullet_slides('Money in numbers', 'Giving, missions and abroad', [re.sub(r'^[A-Za-z ,]+:\s', lambda x: x.group(0), b) for b in bullets(m['Money in numbers'].split('```', 2)[-1])], limit=1200, style='light')
for t, f, blk in cards(sec(10)):
    P2.append({'type': 'rows', 'kicker': 'Genealogy · where it came from', 'head': t, 'rows': [('Origin.', f.get('Origin', '')), ('What it was for.', f.get('What it was for', '')), ('Why that reason expired.', f.get('Why that reason expired', '')), ('Who benefits now.', f.get('Who benefits now', ''))], 'style': 'dark'})
r = subs(sec(11))
for h in ('Information', 'Children', 'Bodies'):
    P2 += bullet_slides('Reach', h, bullets(r[h]), limit=1050, style='light' if h == 'Children' else 'dark')
post('part-2-money-origins-reach', 'Part 2: Money, origins and reach', P2)

# ================================================================== PARTS 3-4 — the 30 techniques
tech = sec(12)
stage_parts = re.split(r'^### Stage (\d) · (\w+) \{#stage-\d\}\s*$', tech, flags=re.M)
STAGES = []
for i in range(1, len(stage_parts), 3):
    STAGES.append((int(stage_parts[i]), stage_parts[i + 1], stage_parts[i + 2]))
intro12 = clean(paras(tech.split('### Stage 1')[0])[0])
def tech_slides(stage_no, stage_name, body_):
    out = []
    sm = re.search(r'::: stage\n(.*?)\n:::', body_, re.S)
    if sm:
        blk = sm.group(1); lead = clean(re.match(r'\*\*(.+?)\*\*', blk).group(1)) if blk.startswith('**') else ''
        rest = [clean(x) for x in re.split(r'\n\s*\n', blk)[1:]]
        out.append({'type': 'text', 'style': 'red', 'kicker': f'Stage {stage_no} of 8', 'head': stage_name, 'paras': [lead] + rest})
    for tm in re.finditer(r'#### (\d+) · (.+?) \{#t-\d+\}\n(.*?)(?=\n:::|\n#### \d+ ·|\Z)', body_, re.S):
        n, name, tb = int(tm.group(1)), clean(tm.group(2)), tm.group(3)
        defn = clean(re.match(r'\s*\*(.+?)\*', tb).group(1))
        items = [clean(x) for x in re.findall(r'^- (.+)$', tb.split('**The strongest defense.**')[0], re.M)]
        dfn = clean(re.search(r'\*\*The strongest defense\.\*\*\s*(.+)', tb).group(1))
        ctr = clean(re.search(r'\*\*The counter\.\*\*\s*(.+)', tb).group(1))
        gm = re.search(r'\*\*Evidence grade\.\*\*\s*\[\[(\w+)\]\]\s*(.+)', tb)
        out.append({'type': 'tech_a', 'style': 'dark', 'kicker': f'Stage {stage_no} · {stage_name} · technique {n} of 30', 'num': str(n), 'name': name, 'defn': defn, 'items': items})
        out.append({'type': 'tech_b', 'style': 'light', 'kicker': f'Stage {stage_no} · {stage_name}', 'num': str(n), 'name': name, 'defense': dfn, 'counter': ctr, 'grade': gm.group(1), 'why': clean(gm.group(2))})
    return out
S = {n: tech_slides(n, name, b) for n, name, b in STAGES}
P3 = [cover(3, NPOSTS, 'The 30 techniques, stages 1 to 4', 'Thirty named techniques from domestic-abuse and social-psychology research, applied to institutions, in the eight stages of the cycle. Each is graded for this tradition.', 'Swipe →'), {'type': 'text', 'kicker': 'The 30 techniques', 'head': 'How to read them', 'paras': [intro12, 'Each technique shows how it appears here, gives the institution\'s strongest defense, then the counter, then an evidence grade: Documented, Taught or Cultural.'], 'style': 'light'}]
for n in (1, 2, 3, 4): P3 += S[n]
P4 = [cover(4, NPOSTS, 'The 30 techniques, stages 5 to 8', 'Isolate, extract, discard, replace: the techniques that follow, each with its defense, its counter and its evidence grade.', 'Swipe →')]
for n in (5, 6, 7, 8): P4 += S[n]
# split to <= 35
def split_post(id_, title, slides, parts, kind):
    if len(slides) <= 35: post(id_, title, slides); return
    cut = len(slides) // 2
    # cut at a technique boundary (before a tech_a or stage slide)
    while slides[cut]['type'] not in ('tech_a',) and not (slides[cut]['type'] == 'text' and slides[cut].get('style') == 'red'): cut += 1
    a, b = slides[:cut], [dict(slides[0], series=slides[0]['series'])] + slides[cut:]
    post(id_ + 'a', title + ' (first half)', a); post(id_ + 'b', title + ' (second half)', b)
split_post('part-3-techniques-stages-1-4', 'Part 3: Techniques, stages 1 to 4', P3, 0, 't')
split_post('part-4-techniques-stages-5-8', 'Part 4: Techniques, stages 5 to 8', P4, 0, 't')

# ================================================================== PART 5 — loops, say vs do, cost
P5 = [cover(5, NPOSTS, 'The loops, and the gap between word and record', 'How the practices connect into seven loops, what leaders say against what the record shows, and what leaving costs.', 'Swipe →')]
loops = sec(13)
P5.append({'type': 'text', 'style': 'light', 'kicker': 'The loops', 'head': 'Seven loops', 'paras': ['Each step makes the next one easier, and the last step feeds the first. The loops are analysis built from findings recorded elsewhere, labeled as an observed pattern, not a documented finding.']})
for t, f, blk in cards(loops):
    steps = [clean(x) for x in re.findall(r'^\d\. (.+)$', blk, re.M)]
    lead = clean(re.search(r'####.*\n\n(.+)', blk).group(1))
    P5.append({'type': 'steps', 'style': 'dark', 'kicker': 'Loop · how it runs', 'head': t, 'intro': lead, 'items': steps})
    ex = f.get('An example from this page', ''); why = f.get('Why it closes', ''); brk = f.get('Where it could be broken, and by whom', '')
    feeds = clean(re.search(r'\*\*Techniques that feed it\.\*\*\s*(.+)', blk).group(1)) if '**Techniques that feed it.**' in blk else ''
    P5.append({'type': 'rows', 'style': 'light', 'kicker': 'Loop · why it closes', 'head': t, 'rows': [('Techniques that feed it.', feeds), ('Why it closes.', why), ('Where it could be broken.', brk), ('An example.', ex)]})
sd = subs(sec(14))
P5 += rows_slides('Say versus do', 'What they say, what the record shows', [(clean(r[0]), clean(r[1])) for r in table(sd['What they say, what the record shows'])[1:]], limit=800)
th = sd['Accountability or theatre?']
P5.append({'type': 'rows', 'style': 'light', 'kicker': 'Say versus do', 'head': 'Accountability or theatre?', 'rows': [(clean(a) + '.', clean(b)) for a, b in re.findall(r'\*\*([^*]+?)\.\*\*\s*(.+)', th)]})
P5 += rows_slides('Say versus do', 'Words used here', [(clean(r[0]), f'Inside: {clean(r[1])} What it does: {clean(r[2])} Said plainly: {clean(r[3])}') for r in table(sd['Words used here'])[1:]], limit=900)
ct = subs(sec(15))
P5 += rows_slides('Cost & cover', 'The ledger of exit', [(clean(r[0]) + f' ({clean(r[1])})', f'{clean(r[2])} The denial: {clean(r[3])}') for r in table(ct['The ledger of exit'])[1:]], limit=900, style='light')
P5 += rows_slides('Cost & cover', 'How the cost is denied', [(clean(r[0]) + f' ({clean(r[1])})', clean(r[2])) for r in table(ct['How the cost is denied'])[1:]], limit=800)
post('part-5-loops-say-do-cost', 'Part 5: Loops, say versus do, cost', P5)

# ================================================================== PART 6 — ledger, who is hurt, tiers, cases
L = subs(sec(16)); H = subs(sec(17)); T = sec(18)
P6 = [cover(6, NPOSTS, 'Who benefits, who pays, and the record', 'The ledger of benefit and cost, who is hurt most, the people in the middle tiers, and six documented cases.', 'Swipe →')]
P6 += bullet_slides('The ledger', 'Who benefits', bullets(L['Who benefits']), limit=1100)
P6 += bullet_slides('The ledger', 'Money out, leverage back', bullets(L['Money out, leverage back']), limit=1000, style='light')
P6 += bullet_slides('The ledger', 'Who pays', bullets(L['Who pays']), limit=1100)
P6 += rows_slides('Who gets hurt most', 'Where the weight lands', [(clean(r[0]), f'{clean(r[1])} Compounded by: {clean(r[2])}') for r in table(H['Where the weight lands'])[1:]], limit=800, style='light')
for h, b in H.items():
    if h.startswith('From The'): P6 += bullet_slides('Who gets hurt most', h, bullets(b), limit=900)
tt = table(T)
P6 += text_slides('The middle tiers', 'People who carry out the work', [clean(paras(T)[0])], limit=900, style='light')
P6 += rows_slides('The middle tiers', 'What each tier sees and could refuse', [(clean(r[0]), f'Does: {clean(r[1])} Sees: {clean(r[2])} Is asked to: {clean(r[3])} Could refuse: {clean(r[4])}') for r in tt[1:]], limit=800)
for cm in re.finditer(r'::: case\n(.*?)\n:::', sec(19), re.S):
    blk = cm.group(1); ti = clean(re.search(r'###\s+(.+)', blk).group(1))
    f = {k: clean(v) for k, v in re.findall(r'- \*\*(\w+):\*\*\s*(.+)', blk)}
    rows = [('When.', f.get('when', '')), ('What.', f.get('what', '')), ('Outcome.', f.get('outcome', '')), ('Evidence grade.', f.get('grade', ''))]
    P6.append({'type': 'rows', 'style': 'dark', 'kicker': 'Documented case', 'head': ti, 'rows': rows})
post('part-6-ledger-cases', 'Part 6: Ledger, who is hurt, cases', P6)

# ================================================================== PART 7 — precedent, voices, regions, questions, leaving, help
P7 = [cover(7, NPOSTS, 'What can change, and what you can do', 'Precedent for change, voices from inside, three countries, the questions to ask, how to leave safely, and where to get help.', 'Swipe →')]
pr = subs(sec(20))
P7 += rows_slides('Precedent', 'It has been broken before', [(clean(r[0]), f'Who: {clean(r[1])} When: {clean(r[2])}. Cost: {clean(r[3])}') for r in table(pr['It has been broken before'])[1:]], limit=900, style='light')
P7 += rows_slides('Precedent', 'Promises on the record', [(clean(r[0]), f'{clean(r[1])}. Status: {clean(r[2])}. {clean(r[3])}') for r in table(pr['Promises on the record'])[1:]], limit=900)
P7.append({'type': 'quote', 'style': 'red', 'kicker': 'What would change this page', 'quote': clean(paras(pr['What would change this page'])[0])})
P7 += bullet_slides('Voices from inside', 'People who spoke', bullets(sec(21)), limit=1100, style='light')
for t, f, blk in cards(sec(22)):
    items = [clean(x) for x in re.findall(r'^- \*\*\w+:\*\* (.+)$', blk, re.M)]
    labs = re.findall(r'^- \*\*(\w+):\*\*', blk, re.M)
    rows = [(l.capitalize() + '.', i) for l, i in zip(labs, items)]
    P7 += rows_slides('Regional variants', t, rows, limit=900)
q = [clean(x) for x in re.findall(r'^\d\. (.+)$', sec(23).split('### In closing')[0], re.M)]
P7 += bullet_slides('The questions', 'Six questions to ask', q, limit=1100, style='light')
closing = paras(sec(23).split('### In closing')[1])
P7 += text_slides('In closing', 'The priesthood of all believers', closing, limit=900)
lv = [clean(re.sub(r'^\d\.\s*', '', x)) for x in re.findall(r'^\d\. .+$', sec(24), re.M)]
P7 += bullet_slides('Leaving safely', 'Practical guidance, not legal advice', lv, limit=1100, style='light')
P7.append({'type': 'help', 'style': 'red', 'kicker': 'If this is your story', 'head': 'Where to get help', 'rows': [['Recovering from Religion', '(844) 368-2848 · US, Canada and online'], ['Faith to Faithless (UK)', '0800 448 0748 · freephone, set hours'], ['SNAP', 'Survivors of clergy abuse · snapnetwork.org'], ['ICSA', 'Former members of high-control groups · internationalculticstudies.org'], ['Childhelp', '1-800-422-4453 · child abuse'], ['RAINN', '1-800-656-4673 · sexual assault']], 'note': f'Full record, sources and PDF: {SITE}'})
post('part-7-change-questions-help', 'Part 7: What can change, and what you can do', P7)

out = os.path.join(ROOT, 'content/sacred-divide/tiktok', rid + '.json')
json.dump({'posts': POSTS}, open(out, 'w'), indent=1, ensure_ascii=False)
for p in POSTS: print(f"{p['id']}: {len(p['slides'])} slides")
print('total', sum(len(p['slides']) for p in POSTS))
