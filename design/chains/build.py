#!/usr/bin/env python3
"""Fractal² manipulation-chain sector sites (combo library v1).

python3 design/chains/build.py [corp] [--theme=A|B|C] [--out=DIR] [--only=slug,slug]

Reads the owner's package verbatim (content/fractal/_packages/combo_clusters_markdown_v2/<SECTOR>/)
and writes one site per sector: a landing page with the setup information, one page per chain
(full text, author's order and headings), and one page per category.
Default output: library/fractal2/site/fractal2/<slug>.html and <slug>/... (served at /fractal2/<slug>).
Nothing here edits the owner's words. Interface wording lives in STRINGS below.
"""
import os, re, sys, json, html, math, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../..'))
PKG = os.path.join(ROOT, 'content/fractal/_packages/combo_clusters_markdown_v2')
SITE = os.path.join(ROOT, 'library/fractal2/site')
BASE = '/fractal2'
F = BASE + '/_a/f/'

SECTORS = {'corp': {'id': 'CORP', 'slug': 'corporate', 'title': 'Corporate & Consulting', 'n': 10}}

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
SEC = SECTORS[(args[0] if args else 'corp')]
THEME = opt.get('theme', 'D')
OUT = opt.get('out', SITE)
ONLY = set(opt['only'].split(',')) if opt.get('only') else None

e = lambda s: html.escape(s, quote=True)
STAGES = ['Idealize', 'Hook', 'Devalue', 'Confuse', 'Isolate', 'Extract · Control', 'Discard', 'Replace']
STAGE_KEY = {'IDEALIZE': 0, 'HOOK': 1, 'DEVALUE': 2, 'CONFUSE': 3, 'ISOLATE': 4, 'CONTROL': 5, 'EXTRACT': 5, 'DISCARD': 6, 'REPLACE': 7}

# ---------------------------------------------------------------- interface wording (owner to approve)
STRINGS = {
    'term': 'manipulation chain', 'terms': 'manipulation chains', 'Terms': 'Manipulation chains',
    'leave': 'Leave', 'menu': 'Menu', 'prev': 'Previous chain', 'next': 'Next chain',
    'in_chain': 'In this chain', 'categories': 'Categories', 'all': 'All chains',
    'read_intro': 'Read the full introduction',
    'std_open': 'Open this part of the Sector Standards',
    'copy': 'Copy', 'copied': 'Copied',
    'same_other': None,
 'orient': 'A manipulation chain is a set of tactics used in a particular order.',
    'orient_link': 'How to read one',
    'leave_end': 'Leave, at the top right, is there on every page.',
    'leave_line': 'Leave, at the top right, replaces this page at once. Escape twice does the same.',
}

# ---------------------------------------------------------------- reading the package
def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]+', ' ', s.lower())).strip()

STD = json.load(open(os.path.join(ROOT, 'content/decoder-v20/standard_index.json')))
ALIAS = json.load(open(os.path.join(ROOT, 'content/decoder-v20/alias_map.json')))
BYID = {v['standard_id']: v for v in STD.values()}
NAME2STAGE = {}
for k, v in STD.items():
    NAME2STAGE[norm(k)] = STAGE_KEY[v['stage']]
    for a in v.get('also_called', []):
        NAME2STAGE.setdefault(norm(a), STAGE_KEY[v['stage']])
for a, sid in ALIAS.items():
    if sid in BYID:
        NAME2STAGE.setdefault(norm(a), STAGE_KEY[BYID[sid]['stage']])

def stage_of(name):
    return NAME2STAGE.get(norm(name))

def front(t):
    m = re.match(r'---\n(.*?)\n---\n', t, re.S)
    meta, body = {}, t[m.end():]
    cur = None
    for line in m.group(1).split('\n'):
        if re.match(r'^\s+- ', line) and cur:
            meta.setdefault(cur, []).append(line.strip()[2:].strip())
            continue
        mm = re.match(r'^(\w+):\s*(.*)$', line)
        if mm:
            k, v = mm.group(1), mm.group(2).strip()
            if v.startswith('[') and v.endswith(']'):
                v = [x.strip() for x in v[1:-1].split(',') if x.strip()]
            meta[k] = v if v != '' else []
            cur = k
    return meta, body

def sections(body):
    body = re.sub(r'^# .*\n', '', body, count=1, flags=re.M)
    parts = re.split(r'^## (.+)$', body, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1].strip('\n')))
    return out

def words(t):
    return len(re.findall(r"[A-Za-z0-9’'][A-Za-z0-9’'\-]*", t))

def load():
    d = os.path.join(PKG, SEC['id'])
    std_meta, std_body = front(open(os.path.join(d, SEC['id'] + '_00_SECTOR_STANDARDS.md')).read())
    standards = sections(std_body)
    cats = {}
    for f in sorted(glob.glob(os.path.join(d, SEC['id'] + '_CAT*_intro.md'))):
        m, b = front(open(f).read())
        secs = sections(b)
        cats[m['category_id']] = {'id': m['category_id'], 'name': m['category_name'], 'intro': secs[0][1] if secs else '', 'chains': []}
    chains = []
    for f in sorted(glob.glob(os.path.join(d, SEC['id'] + '_C[0-9]*.md'))):
        raw = open(f).read()
        m, b = front(raw)
        slug = re.sub(r'^' + SEC['id'] + r'_C\d+_', '', os.path.basename(f)[:-3])
        secs = sections(b)
        steps = [(t, stage_of(t)) for t in m['tactics']]
        c = {'id': m['combo_id'], 'n': int(m['combo_id'][1:]), 'slug': slug, 'title': m['combo_name'], 'cat': m['category_id'],
             'catname': m['category_name'], 'tactics': m['tactics'], 'steps': steps, 'tags': m.get('tags', []), 'secs': secs,
             'safety': any(h.startswith('Safety Note') for h, _ in secs), 'words': words(b.split('\n', 2)[-1] if b.startswith('# ') else b),
             'file': f}
        chains.append(c)
    order = sorted(chains, key=lambda c: (c['cat'], c['n']))
    for c in order:
        cats[c['cat']]['chains'].append(c)
    return standards, cats, order

# ---------------------------------------------------------------- markdown (only the patterns found in the package)
def smart(s):
    s = re.sub(r'(^|[\s(\[{—–/])"', '\\1“', s)
    s = s.replace('"', '”')
    s = re.sub(r"(\w)'", '\\1’', s)
    s = re.sub(r"(^|[\s(\[{—–/“])'", '\\1‘', s)
    return s.replace("'", '’')

def inline(s):
    s = e(smart(s)).replace('&#x27;', '’')
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    s = re.sub(r'\[([XY])\]', r'<span class="blank" aria-label="blank \1">[\1]</span>', s)
    return s

def nxt(lines, i, pat):
    j = i
    while j < len(lines) and not lines[j].strip(): j += 1
    return j < len(lines) and re.match(pat, lines[j]) is not None

def blocks(md):
    """paragraphs, ordered and unordered lists, blockquotes, tables, bold-only lines, ornaments"""
    out, lines, i = [], md.split('\n'), 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        if re.match(r'^\d+\. ', l):   # a numbered list continues across blank lines while the next item follows
            items = []
            while i < len(lines):
                if re.match(r'^\d+\. ', lines[i]): items.append(re.sub(r'^\d+\. ', '', lines[i])); i += 1
                elif lines[i].startswith('   ') and items: items[-1] += ' ' + lines[i].strip(); i += 1
                elif not lines[i].strip() and nxt(lines, i, r'^\d+\. '): i += 1
                else: break
            out.append(('ol', items)); continue
        if l.startswith('- '):
            items = []
            while i < len(lines):
                if lines[i].startswith('- '): items.append(lines[i][2:]); i += 1
                elif lines[i].startswith('  ') and items: items[-1] += ' ' + lines[i].strip(); i += 1
                elif not lines[i].strip() and nxt(lines, i, r'^- '): i += 1
                else: break
            out.append(('ul', items)); continue
        if l.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i].lstrip('>').strip()); i += 1
            out.append(('quote', ' '.join(q))); continue
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                if not re.match(r'^\|[\s\-:|]+\|$', lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            out.append(('table', rows)); continue
        if l.strip() == '· · ·':
            out.append(('orn', None)); i += 1; continue
        if re.match(r'^\*\*[^*]+\*\*$', l.strip()):
            out.append(('boldline', l.strip()[2:-2])); i += 1; continue
        p = [l]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(\d+\. |- |>|\|)', lines[i]) and lines[i].strip() != '· · ·' and not re.match(r'^\*\*[^*]+\*\*$', lines[i].strip()):
            p.append(lines[i]); i += 1
        out.append(('p', p))
    return out

def P(lines, cls=''):
    return '<p%s>%s</p>' % (' class="%s"' % cls if cls else '', '<br>'.join(inline(x) for x in lines))

def generic(md, cls=''):
    h = []
    for k, v in blocks(md):
        if k == 'p': h.append(P(v))
        elif k == 'ol': h.append('<ol class="ol">' + ''.join('<li>%s</li>' % inline(x) for x in v) + '</ol>')
        elif k == 'ul': h.append('<ul class="ul">' + ''.join('<li>%s</li>' % inline(x) for x in v) + '</ul>')
        elif k == 'quote': h.append('<blockquote class="analogy"><p>%s</p></blockquote>' % inline(v))
        elif k == 'orn': h.append('<p class="orn" aria-hidden="true">· · ·</p>')
        elif k == 'boldline': h.append('<p class="scene"><span>%s</span></p>' % inline(v))
        elif k == 'table': h.append(table(v))
    return ''.join(h)

def table(rows):
    head, body = rows[0], rows[1:]
    t = '<div class="tl" role="list">'
    for r in body:
        n, tac = r[0], r[1] if len(r) > 1 else ''
        scene, moment = (r[2] if len(r) > 2 else ''), (r[3] if len(r) > 3 else '')
        t += ('<div class="tl-row" role="listitem"><span class="tl-n">%s</span><div class="tl-body"><p class="tl-tac">%s</p>'
              '<p class="tl-scene"><span class="lbl lbl-x">%s</span> %s</p><p class="tl-moment"><span class="lbl lbl-x">%s</span> %s</p></div></div>') % (
            inline(n), inline(tac), e(head[2] if len(head) > 2 else 'Scene'), inline(scene), e(head[3] if len(head) > 3 else 'The moment'), inline(moment))
    return t + '</div>'

# ---------------------------------------------------------------- visuals
STAGE_VAR = ['--s1', '--s2', '--s3', '--s4', '--s5', '--s6', '--s7', '--s8']

def signature(steps, size=240, labelled=False, uid='s', names=False):
    """The chain's own shape. Eight rings are the eight stages (Idealize innermost, Replace outermost), drawn as
    alternating bands; each step sits on its stage's ring, steps run clockwise from the top in order; a step that
    spans several stages sits at the centre. Start: an open ring. End: filled gold."""
    rad = lambda k: 14 + k * 4.6
    n = len(steps)
    pts = []
    for i, (name, st) in enumerate(steps):
        a = -math.pi / 2 + 2 * math.pi * i / n
        r = rad(st) if st is not None else 0
        pts.append((50 + r * math.cos(a), 50 + r * math.sin(a), st, a))
    g = ['<svg class="sig%s" viewBox="0 0 100 100" width="%d" height="%d" role="img" aria-label="%s">' % (
        ' sig-l' if labelled else '', size, size, e('The shape of this chain: %d steps across the eight stages of the cycle' % n))]
    for k in range(8):
        g.append('<circle cx="50" cy="50" r="%.2f" class="band guide b%d"/>' % (rad(k), k % 2))
    for k in range(8):
        g.append('<circle cx="50" cy="50" r="%.2f" class="ring guide"/>' % rad(k))
    nums = []
    if labelled:
        for i, (x, y, st, a) in enumerate(pts):
            tx, ty = x + 5.6 * math.cos(a), y + 5.6 * math.sin(a)
            if st is None: tx, ty = x + 4.2, y - 3.6
            nums.append((tx, ty))
    if names:   # each stage name on its own ring, like contour labels: the clear spot nearest the gap after the last step
        placed = []
        dots = [(x, y) for x, y, _, _ in pts]
        segs = list(zip(dots, dots[1:]))
        pref = -math.pi / 2 - math.pi / n
        def clear(cx, cy, w, h, strict=True):
            for x, y in dots:
                if abs(x - cx) < w / 2 + 4.2 and abs(y - cy) < h / 2 + 4.2: return False
            for (ax, ay), (bx2, by2) in (segs if strict else []):   # keep clear of the chain's own path
                for t in range(0, 41):
                    px, py = ax + (bx2 - ax) * t / 40, ay + (by2 - ay) * t / 40
                    if abs(px - cx) < w / 2 + 1.2 and abs(py - cy) < h / 2 + 1.1: return False
            for (bx, by, bw, bh) in placed:
                if abs(bx - cx) < (bw + w) / 2 + .8 and abs(by - cy) < (bh + h) / 2 + .4: return False
            for nx_, ny_ in nums:   # never on a step number
                if abs(nx_ - cx) < w / 2 + 2.4 and abs(ny_ - cy) < h / 2 + 2.4: return False
            return True
        for k in range(8):
            word = STAGES[k].split(' ')[0]
            w, h = len(word) * 2.1 + 1.4, 3.9   # measured: Bricolage sentence case at 3.6px
            best = None
            inner = (-5, -8, -11, -14) if k == 0 else ()   # the innermost ring may place its name in the empty core
            for strict, off in [(True, o) for o in (0, 1.4, -1.4, 2.1, -2.1) + inner] + [(False, o) for o in (0, 1.4, -1.4)]:   # on the ring line first, then within its band; last resort may cross a path line, never a dot
                for j in range(0, 72):
                    for sgn in ((1, -1) if j else (1,)):
                        a = pref + sgn * j * math.pi / 36
                        rr = rad(k) + off
                        cx, cy = 50 + rr * math.cos(a), 50 + rr * math.sin(a)
                        if 2 < cx - w / 2 and cx + w / 2 < 98 and 2 < cy - h / 2 and cy + h / 2 < 98 and clear(cx, cy, w, h, strict):
                            best = (cx, cy); break
                    if best: break
                if best: break
            scale = 1.0
            if best and not strict_found(best, w, h, clear):   # no clear spot at full size: try a slightly smaller name, then the spot the path crosses least
                cands = []
                for sc in (1.0, .88, .78, .68):
                    ww, hh = w * sc, h * sc
                    for off in (0, 1.4, -1.4, 2.1, -2.1, 2.6, -2.6) + ((-5, -8, -11, -14) if k == 0 else ()):
                        for j in range(72):
                            a = 2 * math.pi * j / 72; rr = rad(k) + off
                            cx, cy = 50 + rr * math.cos(a), 50 + rr * math.sin(a)
                            if 2 < cx - ww / 2 and cx + ww / 2 < 98 and 2 < cy - hh / 2 and cy + hh / 2 < 98 and clear(cx, cy, ww, hh, False):
                                hits = sum(1 for (ax, ay), (bx2, by2) in segs for t in range(41) if abs(ax + (bx2 - ax) * t / 40 - cx) < ww * .58 + 1.2 and abs(ay + (by2 - ay) * t / 40 - cy) < hh * .58 + 1.0)
                                cands.append((hits, 1 - sc, abs(a - pref), cx, cy, sc))
                    if any(c[0] == 0 for c in cands): break
                if cands:
                    c0 = min(cands); best, scale = (c0[3], c0[4]), c0[5]; w, h = w * scale, h * scale
            if best:
                placed.append((best[0], best[1], w, h))
                g.append('<text x="%.2f" y="%.2f" class="sig-st"%s>%s</text>' % (best[0], best[1] + 1.0 * scale, '' if scale == 1 else ' style="font-size:%.2fpx"' % (3.3 * scale), e(word)))
    d = 'M' + ' L'.join('%.2f %.2f' % (x, y) for x, y, _, _ in pts)
    g.append('<path d="%s" class="path"/>' % d)
    for i, (x, y, st, a) in enumerate(pts):
        cls = 'dot' + (' start' if i == 0 else '') + (' end' if i == n - 1 else '') + (' many' if st is None else '')
        g.append('<circle cx="%.2f" cy="%.2f" r="%s" class="%s"/>' % (x, y, '2.9' if i in (0, n - 1) else '2.2', cls))
        if labelled:
            tx, ty = nums[i]
            g.append('<text x="%.2f" y="%.2f" class="sig-n">%d</text>' % (tx, ty + 1.3, i + 1))
    g.append('</svg>')
    return ''.join(g)

def strict_found(pt, w, h, clear):
    return clear(pt[0], pt[1], w, h, True)

def scale_icon(k):
    c = ''.join('<circle cx="12" cy="12" r="%d" class="%s"/>' % (r, 'on' if j <= k else '') for j, r in enumerate((3.5, 7, 10.5)))
    return '<svg class="scale" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % c

ICON = {
    'link': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 7H7a5 5 0 0 0 0 10h2M15 7h2a5 5 0 0 1 0 10h-2M8 12h8"/></svg>',
    'broken': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 7H7a5 5 0 0 0-2 9.6M15 17h2a5 5 0 0 0 2-9.6M8 3l1.5 3M16 21l-1.5-3M3 8l3 1.5M21 16l-3-1.5"/></svg>',
    'clip': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5 12.6 20a5.5 5.5 0 0 1-7.8-7.8l8.5-8.5a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6l7.8-7.8"/></svg>',
    'eye': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
    'scale': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M5 21h14M7 7h10M7 7l-3 7a3 3 0 0 0 6 0Zm10 0-3 7a3 3 0 0 0 6 0Z"/></svg>',
    'say': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg>',
    'left': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
    'right': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    'menu': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg>',
    'x': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    'copy': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/></svg>',
    'q': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/></svg>',
}

# ---------------------------------------------------------------- section treatments
def std_ref(text, standards, keys):
    """the author's fixed reference line, followed by the referenced Standards text, expandable in place"""
    got = [(h, b) for h, b in standards if h in keys]
    inner = ''.join('<h3 class="std-h">%s</h3>%s' % (e(h), generic(b)) for h, b in got)
    return ('<p class="stdref">%s</p><details class="stdbox"><summary>%s</summary><div class="stdbody">%s'
            '<p class="stdlink"><a href="%s/%s#standards">The full Sector Standards</a></p></div></details>') % (
        inline(text), e(STRINGS['std_open']), inner, BASE, SEC['slug'])

STD_REFS = {
    'Plus the Universal Evidence list in the Sector Standards.': ['Universal Evidence To Preserve'],
    'Apply the Universal Benign Explanations and concern tests in the Sector Standards.': ['Universal Benign Explanations', 'Concern Strengthens When', 'Concern Weakens When'],
    'Tier definitions and sector bodies are in the Sector Standards.': ['Escalation Tiers For This Sector'],
}

def pull_std(md, standards):
    tail = ''
    for line, keys in STD_REFS.items():
        if line in md:
            md = md.replace(line, '').rstrip()
            tail = std_ref(line, standards, keys)
    return md, tail

def sec_before(md):
    h = []
    facts = []
    for k, v in blocks(md):
        if k == 'p' and len(v) == 1 and re.match(r'^\*\*[^*]+\*\* ', v[0]):
            m = re.match(r'^\*\*([^*]+)\*\* (.*)$', v[0]); facts.append((m.group(1), m.group(2)))
        elif k == 'p' and len(v) == 1 and re.match(r'^\*[^*].*\*$', v[0].strip()):
            if facts: h.append(factcard(facts)); facts = []
            h.append('<p class="promise">%s</p>' % inline(v[0].strip()[1:-1]))
        else:
            if facts: h.append(factcard(facts)); facts = []
            h.append(generic_block(k, v))
    if facts: h.append(factcard(facts))
    return ''.join(h)

def factcard(facts):
    return '<dl class="facts">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (inline(a.rstrip('.')), inline(b)) for a, b in facts) + '</dl>'

def generic_block(k, v):
    return generic(blocks_to_md(k, v))

def blocks_to_md(k, v):
    if k == 'p': return '\n'.join(v)
    if k == 'ol': return '\n'.join('%d. %s' % (i + 1, x) for i, x in enumerate(v))
    if k == 'ul': return '\n'.join('- ' + x for x in v)
    if k == 'quote': return '> ' + v
    if k == 'orn': return '· · ·'
    if k == 'boldline': return '**%s**' % v
    return ''

def sec_name(md):
    m = re.search(r'\*\*(.+?)\*\*', md)
    pre = md[:m.start()] if m else ''
    post = md[m.end():] if m else ''
    return '<p class="reveal">%s <span class="reveal-name">%s</span>%s</p>' % (
        inline(pre.strip()), e(m.group(1)) if m else inline(md), inline(post.strip()))

def sec_breakdown(md, c):
    bl = blocks(md)
    h = []
    for k, v in bl:
        if k == 'ol':
            h.append('<ol class="chain">')
            for i, item in enumerate(v):
                m = re.match(r'^\*\*(.+?)\*\*\s*[—–-]\s*(.*)$', item)
                name, rest = (m.group(1), m.group(2)) if m else ('', item)
                st = c['steps'][i][1] if i < len(c['steps']) else stage_of(name)
                stage = ('<span class="st">%s</span>' % STAGES[st]) if st is not None else '<span class="st st-many">Several stages</span>'
                h.append('<li class="link" data-i="%d"><span class="link-n">%d</span><div class="link-body"><h3 class="link-name">%s</h3>%s<p>%s</p></div></li>' % (
                    i, i + 1, inline(name), stage, inline(rest)))
            h.append('</ol>')
        else:
            h.append(generic_block(k, v))
    sig = '<figure class="sigfig" data-form>%s<figcaption class="sigcap"><span class="sigcap-step" aria-hidden="true"></span><span class="sigcap-txt">Each ring is a stage, from Idealize at the centre to Replace on the outside. The numbers follow the chain in order.</span></figcaption></figure>' % signature(c['steps'], 320, True, names=True)
    return sig + ''.join(h)

def legend():
    return '<ol class="legend">' + ''.join('<li style="--c:var(%s)"><span></span>%s</li>' % (STAGE_VAR[k], STAGES[k]) for k in range(8)) + '<li class="lg-many"><span></span>Several stages</li></ol>'

def sec_order(md):
    bl = blocks(md)
    h, last_q = [], max([i for i, (k, _) in enumerate(bl) if k == 'quote'] or [-1])
    for i, (k, v) in enumerate(bl):
        if k == 'quote':
            h.append('<blockquote class="analogy"><p>%s</p></blockquote>' % flipit(v))
        elif k == 'p' and i > last_q >= 0:
            h.append(P(v, 'closing'))
        else:
            h.append(generic_block(k, v))
    return ''.join(h)

def flipit(v):
    parts = re.split(r'(Flip it:)', v, maxsplit=1)
    if len(parts) == 3:
        return '%s <span class="flip"><strong>%s</strong>%s</span>' % (inline(parts[0].strip()), e(parts[1]), inline(parts[2]))
    return inline(v)

def sec_cards(md):
    cards, cur = [], None
    for line in md.split('\n'):
        s = line.strip()
        m = re.match(r'^\*\*SPOT IT\s*[—–-]\s*(.+?):?\*\*:?$', s)
        if m:
            cur = {'t': m.group(1).rstrip(':'), 'ask': '', 'concern': ''}; cards.append(cur); continue
        if cur is None or not s: continue
        if s.startswith('Ask:'): cur['ask'] = s[4:].strip()
        elif s.startswith('Concern rises if:'): cur['concern'] = s[len('Concern rises if:'):].strip()
        else: cur['concern'] += (' ' if cur['concern'] else '') + s
    h = '<div class="cards">'
    for i, c in enumerate(cards):
        h += ('<article class="card"><p class="card-k">Spot it</p><h3 class="card-t">%s</h3>'
              '<p class="card-ask"><span class="lbl">Ask</span>%s</p><p class="card-c"><span class="lbl">Concern rises if</span>%s</p></article>') % (
            inline(c['t']), inline(c['ask']), inline(c['concern']))
    return h + '</div>'

def sec_escalation(md):
    h = '<ol class="tiers">'
    rest = []
    for k, v in blocks(md):
        if k == 'p' and re.match(r'^\*\*([A-Z]+\s*→\s*[A-Z]+):\*\*', v[0]):
            m = re.match(r'^\*\*([A-Z]+)\s*→\s*([A-Z]+):\*\*\s*(.*)$', ' '.join(v))
            lvl = {'LOW': 1, 'MODERATE': 2, 'HIGH': 3}.get(m.group(1), 1)
            h += '<li class="tier t%d"><p class="tier-l"><span>%s</span><span class="arr" aria-label="to">→</span><span>%s</span></p><p>%s</p></li>' % (
                lvl, e(m.group(1)), e(m.group(2)), inline(m.group(3)))
        else:
            rest.append(generic_block(k, v))
    return h + '</ol>' + ''.join(rest)

def sec_say(md):
    h = []
    for k, v in blocks(md):
        if k == 'ul':
            h.append('<ul class="says">' + ''.join('<li><p>%s</p><button type="button" class="copy" data-copy="%s">%s<span>%s</span></button></li>' % (
                inline(x), e(re.sub(r'\*', '', x).strip('"“”')), ICON['copy'], e(STRINGS['copy'])) for x in v) + '</ul>')
        else:
            h.append(generic_block(k, v))
    return ''.join(h)

def sec_iconlist(md, icon, cls):
    h = []
    for k, v in blocks(md):
        if k == 'ul':
            h.append('<ul class="ilist %s">' % cls + ''.join('<li>%s<span>%s</span></li>' % (ICON[icon], inline(x)) for x in v) + '</ul>')
        else:
            h.append(generic_block(k, v))
    return ''.join(h)

def sec_indicators(md):
    h = []
    for k, v in blocks(md):
        if k == 'ol':
            h.append('<ol class="ind">' + ''.join('<li><span>%s</span></li>' % inline(x) for x in v) + '</ol>')
        else:
            h.append(generic_block(k, v))
    return ''.join(h)

def sec_reflection(md):
    return '<div class="reflect">%s</div>' % generic(md)

def render_section(head, md, c, standards):
    md, tail = pull_std(md, standards)
    if head == 'Before the Story': body = sec_before(md)
    elif head == 'Cold Open': body = '<div class="story">%s</div>' % generic(md)
    elif head == 'The Name': body = sec_name(md)
    elif head == 'Definition': body = '<div class="lede">%s</div>' % generic(md)
    elif head == 'Verbal Breakdown': body = sec_breakdown(md, c)
    elif head in ('Why This Order', 'Why the System Produces This Order'): body = sec_order(md)
    elif head == 'On Purpose': body = '<div class="vignette">%s</div>' % generic(md)
    elif head == 'Observable Indicators': body = sec_indicators(md)
    elif head.startswith('Evidence To Preserve'): body = sec_iconlist(md, 'clip', 'evidence')
    elif head.startswith('False-Positive Check'): body = sec_iconlist(md, 'scale', 'fp')
    elif head == 'Recognition Cue Cards': body = sec_cards(md)
    elif head == 'Chain Breakers': body = sec_iconlist(md, 'broken', 'breakers')
    elif head.startswith('Escalation Triggers'): body = sec_escalation(md)
    elif head == 'Safer Response Language': body = sec_say(md)
    elif head == 'Reflection': body = sec_reflection(md)
    else: body = generic(md)
    lvl = {'Individual Level': 0, 'Institutional Echo': 1, 'Civilizational Echo': 2}.get(head)
    icon = scale_icon(lvl) if lvl is not None else ''
    sid = slugify(head)
    cls = 'sec sec-' + sid + (' act' if head in ACT else '')
    return '<section class="%s" id="%s" aria-labelledby="h-%s"><h2 id="h-%s" class="sec-h">%s<span>%s</span></h2>%s%s</section>' % (
        cls, sid, sid, sid, icon, e(head), body, tail)

def slugify(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')

ACT = {'Observable Indicators', 'Evidence To Preserve — Additions', 'False-Positive Check — Specific', 'Recognition Cue Cards', 'Chain Breakers', 'Escalation Triggers — Specific', 'Safer Response Language'}
GROUP_START = {'Verbal Breakdown', 'Observable Indicators', 'Where Each Tactic Happened'}
JUMP = ['Recognition Cue Cards', 'Chain Breakers', 'Escalation Triggers — Specific', 'Safer Response Language']

# ---------------------------------------------------------------- page frame
def short_cat(name):
    return re.sub(r'\s+Composites$', '', name)

def read_min(w):
    return max(1, round(w / 230))

def page(title, desc, body, canonical, extra_class=''):
    css = open(os.path.join(HERE, 'chains.css')).read() + THEMES[THEME]
    js = open(os.path.join(HERE, 'chains.js')).read()
    house = open(os.path.join(ROOT, 'design/decoder-v10/assets/house.html')).read().replace('data-nf-page="playbook"', 'data-nf-page="fractal2"')
    beacon = open(os.path.join(ROOT, 'design/decoder-v10/assets/beacon.html')).read()
    return ('<!doctype html><html lang="en" data-theme-dir="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>%s</title><meta name="description" content="%s"><link rel="canonical" href="https://noblefathercreations.com%s">'
            '<meta name="color-scheme" content="%s"><link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>'
            '<style>%s</style></head><body class="%s">%s%s<script>%s</script>%s</body></html>') % (
        THEME, e(title), e(desc), canonical, 'light dark' if THEME == 'B' else 'dark light', FONT_PRELOAD[THEME], css, extra_class, body,
        house, js, beacon)

def topbar(c=None, prev=None, nxt=None):
    s = SEC
    nav = ''
    if c:
        nav = ('<a class="ib" href="%s" rel="prev" aria-label="%s: %s">%s</a><a class="ib" href="%s" rel="next" aria-label="%s: %s">%s</a>') % (
            url(prev), e(STRINGS['prev']), e(prev['title']), ICON['left'], url(nxt), e(STRINGS['next']), e(nxt['title']), ICON['right'])
    return ('<header class="bar"><div class="bar-in"><a class="brand" href="%s/hub"><span class="mark">Fractal²</span></a>'
            '<a class="sector" href="%s/%s">%s</a><div class="bar-r">%s'
            '<span class="house-slot"></span>'
            '<button class="ib menu-b" type="button" aria-expanded="false" aria-controls="sheet" aria-label="%s">%s<span class="ib-l">%s</span></button>'
            '<a class="leave" href="https://www.google.com/search?q=weather" data-leave>%s</a></div></div>'
            '<div class="prog" aria-hidden="true"><span></span></div></header>') % (
        BASE, BASE, s['slug'], e(s['title']), nav, e(STRINGS['menu']), ICON['menu'], e(STRINGS['menu']), e(STRINGS['leave']))

def url(c):
    return '%s/%s/%s' % (BASE, SEC['slug'], c['slug'])

def caturl(cat):
    return '%s/%s/categories/%s' % (BASE, SEC['slug'], slugify(short_cat(cat['name'])))

def sheet(cats, c=None, nav=None):
    inner = ''
    if c and nav:
        inner += '<nav class="sh-pn" aria-label="Previous and next chain">%s</nav>' % nav
    if c:
        inner += '<section class="sh-sec"><h2 class="sh-h">%s</h2><ol class="sh-toc">%s</ol></section>' % (
            e(STRINGS['in_chain']), ''.join('<li%s><a href="#%s">%s</a></li>' % (' class="gs"' if h in GROUP_START else '', slugify(h), e(h)) for h, _ in c['secs']))
    inner += '<section class="sh-sec"><h2 class="sh-h">%s</h2>' % e(STRINGS['categories'])
    for cat in cats.values():
        open_ = ' open' if c and c['cat'] == cat['id'] else ''
        inner += '<details class="sh-cat"%s><summary><span>%s</span><span class="cnt">%d</span></summary><ol>%s</ol><a class="sh-catlink" href="%s">About this category</a></details>' % (
            open_, e(short_cat(cat['name'])), len(cat['chains']),
            ''.join('<li%s><a href="%s"%s>%s</a></li>' % (' class="cur"' if c and x['id'] == c['id'] else '', url(x), ' aria-current="page"' if c and x['id'] == c['id'] else '', e(x['title'])) for x in cat['chains']),
            caturl(cat))
    inner += '</section><p class="sh-home"><a href="%s/%s">%s home</a> · <a href="%s/%s#all">%s</a></p>' % (BASE, SEC['slug'], e(SEC['title']), BASE, SEC['slug'], e(STRINGS['all']))
    return ('<div class="sheet" id="sheet" hidden><div class="sh-scrim" data-close></div><nav class="sh-panel" aria-label="%s"><div class="sh-top"><p class="sh-title">%s</p>'
            '<span class="sh-actions"><a class="leave" href="https://www.google.com/search?q=weather" data-leave>%s</a><button class="ib" type="button" data-close aria-label="Close menu">%s</button></span></div>%s</nav></div>') % (e(STRINGS['menu']), e(SEC['title']), e(STRINGS['leave']), ICON['x'], inner)

def footer(standards):
    disc = dict(standards).get('Sector Disclaimer', '')
    return '<footer class="foot"><div class="foot-in"><div class="disc">%s</div><p class="ver">Version 1 · 2026-11-20 · <a href="%s/%s#updates">What changed</a></p></div></footer>' % (
        generic(disc), BASE, SEC['slug'])

# ---------------------------------------------------------------- pages
def safety_html(head, md):
    """the author's safety note: its first sentence set large, the Leave line right under it, the rest at reading size"""
    paras = [p for p in md.strip().split('\n\n') if p.strip()]
    first = paras[0].strip() if paras else ''
    m = re.match(r'^(.+?[.!?])(\s+)(.*)$', first, re.S)
    lead, restp = (m.group(1), m.group(3)) if m else (first, '')
    rest = '\n\n'.join(([restp] if restp.strip() else []) + paras[1:])
    sid = slugify(head)
    return ('<section class="safety sec sec-%s" id="%s" aria-labelledby="h-%s"><h2 id="h-%s" class="sec-h"><span class="safe-ic" aria-hidden="true"></span><span>%s</span></h2>'
            '<p class="safety-lead">%s</p><p class="safety-leave">%s</p>%s</section>') % (sid, sid, sid, sid, e(head), inline(lead), e(STRINGS['leave_line']), generic(rest))

def chain_page(c, i, order, cats, standards):
    prev, nxt = order[i - 1], order[(i + 1) % len(order)]
    cat = cats[c['cat']]
    pos = cat['chains'].index(c) + 1
    secs = c['secs']
    safety = ''.join(safety_html(h, b) for h, b in secs if h.startswith('Safety Note'))
    rest = [(h, b) for h, b in secs if not h.startswith('Safety Note')]
    jump = ''.join('<a href="#%s">%s</a>' % (slugify(h), e(h)) for h in JUMP if any(x == h for x, _ in rest))
    rail = ''.join('<li%s><a href="#%s">%s</a></li>' % (' class="gs"' if h in GROUP_START else '', slugify(h), e(h)) for h, _ in rest)
    head = ('<div class="ch-head"><div class="ch-txt">'
            '<h1 class="ch-title">%s</h1>%s<p class="meta"><a href="%s">%s</a><span>%d tactics, about %d minutes to read</span></p>'
            '<p class="orient">%s <a href="%s/%s#read">%s</a></p>'
            '<nav class="jump" aria-label="Jump to"><span class="jump-l">Jump to</span>%s</nav></div>'
            '<div class="ch-sig">%s</div></div>') % (
        e(c['title']), safety, caturl(cat), e(short_cat(cat['name'])),
        len(c['tactics']), read_min(c['words']), e(STRINGS['orient']), BASE, SEC['slug'], e(STRINGS['orient_link']), jump, signature(c['steps'], 340, True, names=True))
    body_secs = ''.join(render_section(h, b, c, standards) for h, b in rest) + '<p class="end-leave">' + e(STRINGS['leave_end']) + '</p>'
    endnav = ('<nav class="endnav" aria-label="More chains"><a class="en prev" href="%s" rel="prev"><span class="en-k">%s %s</span><span class="en-t">%s</span></a>'
              '<a class="en next" href="%s" rel="next"><span class="en-k">%s %s</span><span class="en-t">%s</span></a></nav>') % (
        url(prev), ICON['left'], e(STRINGS['prev']), e(prev['title']), url(nxt), e(STRINGS['next']), ICON['right'], e(nxt['title']))
    endnav = endnav.replace('<span class="en-t">%s</span></a>' % e(prev['title']), '<span class="en-t">%s</span><span class="en-sig">%s</span></a>' % (e(prev['title']), signature(prev['steps'], 56)), 1)
    endnav = endnav.replace('<span class="en-t">%s</span></a></nav>' % e(nxt['title']), '<span class="en-t">%s</span><span class="en-sig">%s</span></a></nav>' % (e(nxt['title']), signature(nxt['steps'], 56)), 1)
    margin = '<aside class="margin" aria-hidden="true"><div class="margin-in">%s<p class="margin-t">%s</p><p class="margin-m">%d tactics</p><p class="margin-step"></p></div></aside>' % (signature(c['steps'], 200), e(c['title']), len(c['tactics']))
    main = ('%s<main id="main" class="chain-page"><article class="ch">%s<div class="ch-grid"><aside class="rail" aria-label="Sections"><p class="rail-h">%s</p><ol>%s</ol></aside>'
            '<div class="ch-body">%s</div>%s</div></article>%s</main>%s%s') % (
        topbar(c, prev, nxt), head, e(STRINGS['in_chain']), rail, body_secs, margin, endnav, footer(standards),
        sheet(cats, c, '<a href="%s" rel="prev"><span class="lbl">%s</span>%s</a><a href="%s" rel="next"><span class="lbl">%s</span>%s</a>' % (url(prev), e(STRINGS['prev']), e(prev['title']), url(nxt), e(STRINGS['next']), e(nxt['title']))))
    title = '%s · %s · Fractal²' % (c['title'], SEC['title'])
    desc = 'A %s in %s: %d tactics in order, told as a story, with what to notice and what to do.' % (STRINGS['term'], SEC['title'].lower(), len(c['tactics']))
    return page(title, desc, main, url(c), 'is-chain')

def card(c):
    return ('<li class="ccard"><a href="%s"><span class="cc-sig">%s</span><span class="cc-t">%s</span><span class="cc-m">%d tactics, %d minutes%s</span></a></li>') % (
        url(c), signature(c['steps'], 88), e(c['title']), len(c['tactics']), read_min(c['words']),
        '<span class="cc-safe">Begins with a safety note</span>' if c['safety'] else '')

def az_key(t):
    return re.sub(r'^(the|a|an)\s+', '', re.sub(r'^[^a-z0-9]+', '', t.lower()).replace('"', '').replace('“', '').replace('”', ''))

def field(order, featured):
    """all chains at once: every path overlaid on the eight rings, one traced in gold (the shapes are the data)"""
    rad = lambda k: 14 + k * 4.6
    def path(c):
        n = len(c['steps']); pts = []
        for i, (_, st) in enumerate(c['steps']):
            a = -math.pi / 2 + 2 * math.pi * i / n; r_ = rad(st) if st is not None else 0
            pts.append('%.1f %.1f' % (50 + r_ * math.cos(a), 50 + r_ * math.sin(a)))
        return 'M' + ' L'.join(pts)
    g = ['<svg class="field" viewBox="0 0 100 100" role="img" aria-label="%s">' % e('All %d chains drawn over the eight stages; one is traced in gold' % len(order))]
    for k in range(8):
        g.append('<circle cx="50" cy="50" r="%.2f" class="band guide b%d"/><circle cx="50" cy="50" r="%.2f" class="ring guide"/>' % (rad(k), k % 2, rad(k)))
    g.append('<g class="all">' + ''.join('<path d="%s"/>' % path(c) for c in order if c is not featured) + '</g>')
    g.append('<path class="feat" d="%s"/>' % path(featured))
    g.append('</svg>')
    return ''.join(g)

def landing(cats, order, standards):
    total = len(order)
    std_html = ''.join('<details class="stdsec" id="std-%s"><summary>%s</summary><div>%s</div></details>' % (slugify(h), e(h), generic(b)) for h, b in standards if h != 'Sector Disclaimer')
    catdoors = ''.join(('<li class="door"><a href="%s"><span class="door-n" aria-hidden="true">%s</span><span class="door-t">%s</span><span class="door-c">%d chains</span>'
                        '<span class="door-x">%s</span></a></li>') % (caturl(cat), signature(cat['chains'][0]['steps'], 40), e(short_cat(cat['name'])), len(cat['chains']),
                        ', '.join(e(x['title']) for x in cat['chains'][:3])) for k, cat in enumerate(cats.values()))
    az = sorted(order, key=lambda c: az_key(c['title']))
    letters, groups = [], ''
    cur = None
    for c in az:
        L = az_key(c['title'])[0].upper()
        if L != cur:
            if cur: groups += '</ol></div>'
            groups += '<div class="azg" id="az-%s"><h3 class="azl">%s</h3><ol class="azlist">' % (L, L); letters.append(L); cur = L
        groups += '<li><a href="%s"><span class="az-t">%s</span><span class="az-m">%d tactics%s</span></a></li>' % (url(c), e(c['title']), len(c['tactics']), '<span class="cc-safe">, safety note</span>' if c['safety'] else '')
    groups += '</ol></div>'
    groups = '<div class="az">' + groups + '</div>'
    sample = next(c for c in order if c['slug'] == 'emotional-debt-spiral') if any(c['slug'] == 'emotional-debt-spiral' for c in order) else order[0]
    anatomy = ''.join('<li><span class="an-h">%s</span></li>' % e(h) for h, _ in sample['secs'] if not h.startswith('Safety'))
    body = open(os.path.join(HERE, 'landing.html')).read()
    rep_extra = {'%%FIELD%%': field(order, sample), '%%ICON_LEFT%%': ICON['left'], '%%ICON_RIGHT%%': ICON['right'], '%%ICON_MENU%%': ICON['menu'],
                 '%%ICON_LEAVE%%': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"/></svg>',
                 '%%ICON_JUMP%%': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v14M6 12l6 6 6-6"/></svg>',
                 '%%ICON_HISTORY%%': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5M12 7v5l3 2"/></svg>',
                 '%%ICON_NOTE%%': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16.5v.5"/></svg>',
                 '%%ICON_SOS%%': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'}
    for k, v in rep_extra.items():
        body = body.replace(k, v)
    rep = {
        '%%TOTAL%%': str(total), '%%SECTOR%%': e(SEC['title']), '%%DOORS%%': catdoors, '%%LETTERS%%': ''.join('<a href="#az-%s">%s</a>' % (l, l) for l in letters),
        '%%AZ%%': groups, '%%STANDARDS%%': std_html, '%%LEGEND%%': legend(), '%%SIG%%': signature(sample['steps'], 420, True, names=True),
        '%%SAMPLE%%': e(sample['title']), '%%SAMPLEURL%%': url(sample), '%%ANATOMY%%': anatomy, '%%MEDIAN%%': str(read_min(sorted(c['words'] for c in order)[len(order) // 2])),
        '%%SAFE%%': str(sum(c['safety'] for c in order)), '%%FIRST%%': url(order[0]),
    }
    for k, v in rep.items():
        body = body.replace(k, v)
    main = topbar() + '<main id="main" class="landing">' + body + '</main>' + footer(standards) + sheet(cats)
    return page('%s · Fractal²' % SEC['title'], 'How manipulation is used in %s: %d manipulation chains, each a full story with what to notice and what to do.' % (SEC['title'].lower(), total),
                main, '%s/%s' % (BASE, SEC['slug']), 'is-landing')

def category_page(cat, k, cats, standards):
    keys = list(cats)
    prv, nx = cats[keys[k - 1]], cats[keys[(k + 1) % len(keys)]]
    bl = [b for b in cat['intro'].split('\n\n') if b.strip()]
    first, rest = bl[0] if bl else '', '\n\n'.join(bl[1:])
    catfig = '<figure class="cat-fig">%s</figure>' % field(cat['chains'], cat['chains'][0])
    body = ('<main id="main" class="cat-page"><div class="cat-top"><header class="cat-head"><h1 class="cat-title">%s</h1><p class="meta cat-meta"><a href="%s/%s#categories">%s</a><span>%d chains</span></p>'
            '<div class="cat-intro">%s<details class="more"><summary>%s</summary>%s</details></div></header>' + catfig + '</div>'
            '<ol class="cgrid">%s</ol><nav class="endnav" aria-label="More categories"><a class="en prev" href="%s"><span class="en-k">%s Previous category</span><span class="en-t">%s</span></a>'
            '<a class="en next" href="%s"><span class="en-k">Next category %s</span><span class="en-t">%s</span></a></nav></main>') % (
        e(cat['name']), BASE, SEC['slug'], e(SEC['title']), len(cat['chains']), generic(first), e(STRINGS['read_intro']), generic(rest), ''.join(card(c) for c in cat['chains']),
        caturl(prv), ICON['left'], e(short_cat(prv['name'])), caturl(nx), ICON['right'], e(short_cat(nx['name'])))
    return page('%s · %s · Fractal²' % (short_cat(cat['name']), SEC['title']), 'The %s category in %s: %d manipulation chains.' % (short_cat(cat['name']).lower(), SEC['title'], len(cat['chains'])),
                topbar() + body + footer(standards) + sheet(cats), caturl(cat), 'is-cat')

# ---------------------------------------------------------------- themes (the three directions compared before building)
FONTFACE = {
    'bricolage': '@font-face{font-family:"BG";src:url(%schains-bricolage.woff2) format("woff2");font-weight:500 700;font-stretch:84%% 100%%;font-display:swap}' % F,
    'sourceserif': '@font-face{font-family:"SS";src:url(%schains-sourceserif.woff2) format("woff2");font-weight:400 700;font-display:swap}@font-face{font-family:"SS";src:url(%schains-sourceserif-italic.woff2) format("woff2");font-weight:400 600;font-style:italic;font-display:swap}' % (F, F),
}
FONT_PRELOAD = {'D': F + 'chains-sourceserif.woff2'}   # directions A, B and C were compared and set aside (see content/fractal2/design/CHAINS-DESIGN-RECORD.md)
THEMES = {
 # D. Chosen after round 1: A's dark chassis and gold, B's type (Bricolage Grotesque display and labels, Source Serif 4 reading).
 'D': FONTFACE['bricolage'] + FONTFACE['sourceserif'] + '''
:root{--bg:#0d0f14;--bg2:#13161e;--card:#161a24;--ink:#ebe6dc;--ink2:#cfc9bd;--mut:#a4a196;--line:#272c39;--line2:#353b4c;--accent:#e9c27a;--accent-ink:#1a1306;--accent-grad:#f3d59b;--glow-1:rgba(233,194,122,.25);--edge-hi:rgba(255,255,255,.06);
--s1:#e7c77e;--s2:#e6a55a;--s3:#db7f4e;--s4:#d2615f;--s5:#bc6a8a;--s6:#96a6cf;--s7:#7c98da;--s8:#a6b9ee;--warm:#eba57f;--warm-bg:rgba(235,165,127,.08);
--serif:"SS",Georgia,serif;--display:"BG",system-ui,sans-serif;--sans:"BG",system-ui,sans-serif;--mono:"BG",system-ui,sans-serif;--disp-w:700;--disp-opsz:96;--title-style:normal;color-scheme:dark}
@media (prefers-color-scheme:light){:root{--bg:#f3f4f2;--bg2:#e9ebe8;--card:#fbfbfa;--ink:#15181d;--ink2:#30343c;--mut:#585c66;--line:#d6d9d4;--line2:#c3c7c0;--accent:#8a5f00;--accent-ink:#fff;--accent-grad:#a87610;--glow-1:rgba(138,95,0,.18);--edge-hi:rgba(0,0,0,.04);
--s1:#8a6312;--s2:#9a5512;--s3:#9a441a;--s4:#932c31;--s5:#7d3557;--s6:#435684;--s7:#2d4a8c;--s8:#344b85;--warm:#9a441a;--warm-bg:rgba(154,68,26,.06);color-scheme:light}}
''',
}

def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(s)

def main():
    standards, cats, order = load()
    root = os.path.join(OUT, 'fractal2')
    n = 0
    for i, c in enumerate(order):
        if ONLY and c['slug'] not in ONLY: continue
        write(os.path.join(root, SEC['slug'], c['slug'] + '.html'), chain_page(c, i, order, cats, standards)); n += 1
    if not ONLY or 'landing' in ONLY:
        write(os.path.join(root, SEC['slug'] + '.html'), landing(cats, order, standards)); n += 1
    for k, cat in enumerate(cats.values()):
        if ONLY and 'cats' not in ONLY: continue
        write(os.path.join(root, SEC['slug'], 'categories', slugify(short_cat(cat['name'])) + '.html'), category_page(cat, k, cats, standards)); n += 1
    unmapped = sum(1 for c in order for _, s in c['steps'] if s is None)
    print('theme %s: wrote %d pages; %d chains; steps without one stage: %d of %d' % (THEME, n, len(order), unmapped, sum(len(c['steps']) for c in order)))

if __name__ == '__main__':
    main()
