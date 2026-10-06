#!/usr/bin/env python3
"""The Sacred Divide — render a religion's Markdown file to a print-ready, navigable PDF.

    python3 scripts/sacred-divide-pdf.py sunni-islam            # one religion
    python3 scripts/sacred-divide-pdf.py --all                  # every religion file
    python3 scripts/sacred-divide-pdf.py sunni-islam --html     # stop after the HTML (for design work)

Input:  content/sacred-divide/religions/<id>.md  (from scripts/sacred-divide-export-md.py)
        content/sacred-divide/religions/_how-to-read.md
Output: library/_undeployed/sacred-divide-pdf/<id>.pdf   (+ <id>.html, the paged source)

Pipeline: Markdown → HTML (python-markdown + the conventions below) → Paged.js in Chromium lays out
A4 pages (running heads, page numbers, a table of contents with real page numbers) → Chromium prints
with clickable internal links and PDF bookmarks → pypdf checks the result.
Design lives in tools/pdf/sacred-divide.css; Paged.js and fonts are vendored in tools/pdf/ so a
build needs no network. Requirements: pip install markdown pypdf; Playwright + Chromium (preinstalled).

Markdown conventions (written by the exporter):
  ::: kind [attrs] … :::   styled box: glance lede tell question gap cites card case stage tactic
  ```timeline               rows "date | event | reading" → era strip + numbered timeline
  ```chart                  JSON {type: bar|line, title, unit, series, note, cite} → SVG chart
  [[Grade]]                 evidence-grade chip      [n] → link to Sources item n
  [OFFICIAL POLICY: …]      receipt label
"""
import html, json, math, os, re, subprocess, sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'content/sacred-divide/religions')
TOOLS = os.path.join(ROOT, 'tools/pdf')
OUTDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-pdf')
SITE = 'noblefathercreations.com/faith'

GRADES = ['Codified', 'Documented', 'Taught', 'Cultural', 'Contested', 'Reformed', 'Ungraded']
GRADE_COLOUR = {'Codified': '#7E1F2B', 'Documented': '#3B4A6B', 'Taught': '#96772F', 'Cultural': '#6C6154',
                'Contested': '#6B4A8A', 'Reformed': '#2F6B3A', 'Ungraded': '#B8B0A2'}


# ---------------------------------------------------------------- small helpers
def e(t):
    return html.escape(str(t), quote=True)


def front_matter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def year_of(label):
    t = label.lower()
    if 'present' in t and not re.search(r'\d', t):
        return 2026
    m = re.search(r'(\d{3,4})', t)
    if not m:
        return None
    y = int(m.group(1))
    if 'bce' in t or ' bc' in t:
        y = -y
    return y


# ---------------------------------------------------------------- graphics
def timeline_html(block):
    rows = [[c.strip() for c in line.split('|')] for line in block.strip().splitlines() if line.strip()]
    rows = [r + [''] * (3 - len(r)) for r in rows]
    years = [year_of(r[0]) for r in rows]
    known = [y for y in years if y is not None]
    strip = ''
    if len(known) >= 2:
        lo, hi = min(known), max(known)
        lo = math.floor(lo / 100) * 100
        hi = max(hi, lo + 100)
        W, H, pad = 1000, 96, 30
        x = lambda y: pad + (y - lo) / (hi - lo) * (W - 2 * pad)
        parts = [f'<line x1="{pad}" y1="60" x2="{W - pad}" y2="60" stroke="#96772F" stroke-width="2"/>']
        step = 100 if hi - lo <= 1600 else 200
        if hi - lo <= 300: step = 50
        for t in range(lo, hi + 1, step):
            parts.append(f'<line x1="{x(t):.1f}" y1="56" x2="{x(t):.1f}" y2="64" stroke="#96772F" stroke-width="1"/>'
                         f'<text x="{x(t):.1f}" y="82" font-size="13" fill="#6C6154" text-anchor="middle">{t if t >= 0 else f"{-t} BCE"}</text>')
        placed = []
        for i, y in enumerate(years, 1):
            if y is None: continue
            cx = x(y)
            lift = sum(1 for p in placed if abs(p - cx) < 22) % 3
            placed.append(cx)
            cy = 60 - 16 - lift * 15
            parts.append(f'<line x1="{cx:.1f}" y1="{cy + 7}" x2="{cx:.1f}" y2="60" stroke="#D7CBB6" stroke-width="1"/>'
                         f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="#7E1F2B"/>'
                         f'<text x="{cx:.1f}" y="{cy + 4:.1f}" font-size="10" fill="#fff" text-anchor="middle">{i}</text>')
        strip = (f'<figure class="fig"><div class="ftitle">History at a glance</div>'
                 f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Timeline of events">{"".join(parts)}</svg>'
                 f'<figcaption>Numbered markers match the timeline below; spacing is proportional to the years.</figcaption></figure>')
    items = ''.join(f'<li data-n="{i}"><span class="d">{inline(e(r[0]))}</span><span class="e">{inline(e(r[1]))}</span>'
                    f'<span class="r">{inline(e(r[2]))}</span></li>' for i, r in enumerate(rows, 1))
    return strip + f'<ol class="tl">{items}</ol>'


def chart_svg(spec, valid):
    series = spec['series']
    labels = [s[0] for s in series]
    vals = [float(s[1]) for s in series]
    W, H, L, R, T, Bm = 1000, 380, 90, 30, 30, 50
    vmax = max(vals) or 1
    mag = 10 ** math.floor(math.log10(vmax))
    top = math.ceil(vmax / mag) * mag
    if top / 5 < mag / 2: top = math.ceil(vmax / (mag / 2)) * (mag / 2)
    y = lambda v: T + (H - T - Bm) * (1 - v / top)
    n = len(vals)
    slot = (W - L - R) / n
    base = (lambda v: f'{v / 1e6:.1f}m') if top >= 1e6 else (lambda v: f'{v / 1e3:.0f}k') if top >= 1e4 else (lambda v: f'{v:g}')
    fmt = lambda v: base(v) if (v == 0 or v >= top / 50) else f'{v:,.0f}'
    parts = []
    for k in range(6):
        v = top * k / 5
        parts.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W - R}" y2="{y(v):.1f}" stroke="#E6DDCB" stroke-width="1"/>'
                     f'<text x="{L - 10}" y="{y(v) + 5:.1f}" font-size="15" fill="#6C6154" text-anchor="end">{fmt(v)}</text>')
    for i, (lab, v) in enumerate(zip(labels, vals)):
        cx = L + slot * (i + .5)
        parts.append(f'<text x="{cx:.1f}" y="{H - Bm + 26}" font-size="15" fill="#241E17" text-anchor="middle">{e(lab)}</text>')
        if spec['type'] == 'bar':
            bw = min(slot * .56, 120)
            parts.append(f'<rect x="{cx - bw / 2:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{y(0) - y(v):.1f}" fill="{"#7E1F2B" if i == n - 1 else "#96772F"}"/>'
                         f'<text x="{cx:.1f}" y="{y(v) - 8:.1f}" font-size="17" fill="#241E17" text-anchor="middle">{fmt(v)}</text>')
    if spec['type'] == 'line':
        pts = ' '.join(f'{L + slot * (i + .5):.1f},{y(v):.1f}' for i, v in enumerate(vals))
        area = f'{L + slot * .5:.1f},{y(0):.1f} ' + pts + f' {L + slot * (n - .5):.1f},{y(0):.1f}'
        parts.append(f'<polygon points="{area}" fill="#96772F" fill-opacity=".12"/>'
                     f'<polyline points="{pts}" fill="none" stroke="#7E1F2B" stroke-width="3"/>')
        for i, v in enumerate(vals):
            cx = L + slot * (i + .5)
            parts.append(f'<circle cx="{cx:.1f}" cy="{y(v):.1f}" r="5" fill="#7E1F2B"/>')
            if v in (max(vals), min(vals)) or i == n - 1:
                parts.append(f'<text x="{cx:.1f}" y="{y(v) - 12:.1f}" font-size="14" fill="#241E17" text-anchor="middle">{fmt(v)}</text>')
    cites = ' '.join(f'<a class="cite" href="#src-{c}">{c}</a>' for c in spec.get('cite', []) if c in valid)
    return (f'<figure class="fig"><div class="ftitle">{e(spec["title"])}</div>'
            f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{e(spec["title"])}"><title>{e(spec["title"])}</title>{"".join(parts)}</svg>'
            f'<figcaption>{e(spec.get("unit", ""))}{" — " + e(spec["note"]) if spec.get("note") else ""} {cites}</figcaption></figure>')


def grade_bar(counts):
    total = sum(counts.values()) or 1
    W, x, parts, legend = 1000, 0, [], []
    for g in GRADES:
        c = counts.get(g, 0)
        if not c: continue
        w = W * c / total
        parts.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="34" fill="{GRADE_COLOUR[g]}"/>'
                     + (f'<text x="{x + w / 2:.1f}" y="23" font-size="16" fill="#fff" text-anchor="middle">{c}</text>' if w > 30 else ''))
        legend.append(f'<span class="chip g-{g.lower()}">{g} {c}</span>')
        x += w
    return (f'<figure class="fig"><div class="ftitle">How the 30 techniques are established here</div>'
            f'<svg viewBox="0 0 {W} 34" width="100%" role="img" aria-label="Evidence grades">{"".join(parts)}</svg>'
            f'<figcaption>{"".join(legend)}</figcaption></figure>')


# ---------------------------------------------------------------- inline tokens
VALID = set()
TACTIC_NAMES = {}
RCPT = re.compile(r'\[((?:OFFICIAL POLICY|COURT RECORD|GOVERNMENT REPORT|GOVERNMENT INQUIRY|FINANCIAL RECORD|REGULATORY FILING|'
                  r'ACADEMIC SOURCE|INVESTIGATIVE REPORT|LEADERSHIP STATEMENT|FORMER MEMBER TESTIMONY|PATTERN OBSERVED|'
                  r'SOURCE NEEDED|VARIES BY COMMUNITY|SURVIVOR TESTIMONY)(?: / [A-Z ]+?)*)(?:\s*[:—–-]\s*([^\]]+))?\]')


def inline(t):
    """Tokens inside already-escaped or trusted text."""
    t = re.sub(r'\[\[(\w+)\]\]', lambda m: f'<span class="chip g-{m.group(1).lower()}">{m.group(1)}</span>', t)
    t = RCPT.sub(lambda m: f'<span class="rcpt">{m.group(1)}{" · <i>" + m.group(2).strip() + "</i>" if m.group(2) else ""}</span>', t)
    t = re.sub(r'\[(\d{1,3})\](?!\()', lambda m: f'<a class="cite" href="#src-{m.group(1)}">{m.group(1)}</a>'
               if int(m.group(1)) in VALID else m.group(0), t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<em>\1</em>', t)
    return t


# ---------------------------------------------------------------- markdown → html
def md_to_html(text):
    blocks = []

    def stash(h):
        blocks.append(h)
        return f'\n\n@@BLOCK{len(blocks) - 1}@@\n\n'

    text = re.sub(r'^```timeline\n(.*?)^```', lambda m: stash(timeline_html(m.group(1))), text, flags=re.S | re.M)
    text = re.sub(r'^```chart\n(.*?)^```', lambda m: stash(chart_svg(json.loads(m.group(1)), VALID)), text, flags=re.S | re.M)
    # containers: ::: kind attrs … :::
    text = re.sub(r'^::: *(\w+)[^\n]*\n', lambda m: f'<div class="box {m.group(1)}" markdown="1">\n\n', text, flags=re.M)
    text = re.sub(r'^:::\s*$', '\n</div>\n', text, flags=re.M)
    md = markdown.Markdown(extensions=['tables', 'attr_list', 'md_in_html', 'fenced_code', 'sane_lists'],
                           extension_configs={'sane_lists': {}}, tab_length=4)
    md.lazy_ol = False
    out = md.convert(text)
    out = re.sub(r'<p>@@BLOCK(\d+)@@</p>', lambda m: blocks[int(m.group(1))], out)
    out = re.sub(r'@@BLOCK(\d+)@@', lambda m: blocks[int(m.group(1))], out)
    # links: bare URLs and autolinks become clickable external links
    out = re.sub(r'(?<!["=>])(https?://[^\s<)\]]+[^\s<)\].,;])', r'<a class="ext" href="\1">\1</a>', out)
    out = re.sub(r'<a href="(https?://[^"]+)">', r'<a class="ext" href="\1">', out)
    # tokens in text (not inside tags)
    out = re.sub(r'>([^<]+)<', lambda m: '>' + inline(m.group(1)) + '<', out)
    return out


def sources_ids(sec_html):
    """Give every Sources list item an id matching its printed number."""
    def fix_ol(m):
        start = int(re.search(r'start="(\d+)"', m.group(1)).group(1)) if 'start=' in m.group(1) else 1
        items = re.split(r'(<li>)', m.group(2))
        n, res = start, []
        for it in items:
            if it == '<li>':
                res.append(f'<li id="src-{n}" value="{n}">'); n += 1
            else:
                res.append(it)
        return m.group(1) + ''.join(res) + '</ol>'
    return re.sub(r'(<ol[^>]*>)(.*?)</ol>', fix_ol, sec_html, flags=re.S)


def score_cells(h):
    def row(m):
        # a cell is a bare grade letter, or a letter followed by its note ("P (UK register) [13]"); keep the note in a span
        return re.sub(r'<td>([YPN?])((?:\s.*?)?)</td>', lambda c: f'<td class="s{c.group(1) if c.group(1) != "?" else "Q"}">{c.group(1)}' + (f'<span class="sn">{c.group(2).strip()}</span>' if c.group(2).strip() else '') + '</td>', m.group(0), flags=re.S)
    return re.sub(r'<table>(\s*<thead>\s*<tr>\s*<th>Accounts</th>.*?)</table>', lambda m: '<table class="score">' + row(m)[7:], h, flags=re.S)


# ---------------------------------------------------------------- page assembly
def build_html(rid):
    global VALID
    raw = open(os.path.join(SRC, f'{rid}.md'), encoding='utf-8').read()
    meta, body = front_matter(raw)
    name = meta.get('title', rid)
    src_part = re.search(r'^## \d+\. Sources \{#sources\}\n(.*?)(?=^## \d+\.)', body, re.S | re.M)
    VALID = {int(n) for n in re.findall(r'^\s*(\d+)\.\s', src_part.group(1), re.M)} if src_part else set()

    global TACTIC_NAMES
    # Only the 30 technique headings (section 12). The loop cards in section 13 use the same '#### N · name'
    # shape and used to overwrite entries 1-7 with loop names (v4 bug: 'tactics: 2' read 'Fear to Dependence to Fear').
    tech = re.search(r'^## \d+\. The 30 techniques \{#techniques\}\n(.*?)(?=^## \d+\.)', body, re.S | re.M)
    TACTIC_NAMES = {int(n): re.sub(r'\s*\{#.*', '', t) for n, t in re.findall(r'^#### (\d+) · (.+)$', tech.group(1) if tech else body, re.M)}
    # split into the 27 sections
    parts = re.split(r'^## (\d+)\. (.+?) \{#([\w-]+)\}\s*$', body, flags=re.M)
    sections = [(parts[i], parts[i + 1], parts[i + 2], parts[i + 3]) for i in range(1, len(parts), 4)]
    toc, secs = [], []
    for num, title, slug, content in sections:
        h = md_to_html(content)
        if slug == 'sources': h = sources_ids(h)
        if slug == 'cases':
            h = re.sub(r'(<strong>tactics:</strong>)\s*([\d, ]+)', lambda m: m.group(1) + ' ' + ', '.join(
                f'<a class="tlink" href="#t-{n.strip()}">{n.strip()} · {TACTIC_NAMES.get(int(n), "")}</a>' for n in m.group(2).split(',') if n.strip()), h)
            h = re.sub(r'(<strong>grade:</strong>)\s*(\w+)', lambda m: f'{m.group(1)} <span class="chip g-{m.group(2).lower()}">{m.group(2)}</span>', h)
        if slug == 'at-a-glance': h = score_cells(h)
        if slug == 'techniques':
            grades = re.findall(r'<span class="chip g-(\w+)">', h)
            counts = {}
            for g in grades: counts[g.title()] = counts.get(g.title(), 0) + 1
            index = re.findall(r'<h4 id="t-(\d+)">\d+ · (.+?)</h4>', h)
            grade_of = dict(re.findall(r'id="t-(\d+)">.*?<span class="chip g-(\w+)">', h, re.S))
            grid = ''.join(f'<a href="#t-{n}"><span class="n">{n}</span><span class="nm">{nm}</span>'
                           f'<span class="chip g-{grade_of.get(n, "ungraded")}">{grade_of.get(n, "ungraded").title()}</span></a>' for n, nm in index)
            lead = (grade_bar(counts) if counts else '') + (f'<h3 id="techniques-index">All thirty at a glance</h3><div class="tgrid">{grid}</div>' if grid else '')
            h = re.sub(r'(</p>)', r'\1' + lead.replace('\\', '\\\\'), h, count=1) if lead else h
        subs = re.findall(r'<h3 id="([\w-]+)">(.*?)</h3>', h)
        if slug != 'techniques':  # h3s without ids get one, so the TOC can link to them
            k = [0]
            def add_id(m):
                k[0] += 1
                return f'<h3 id="{slug}-{k[0]}">{m.group(1)}</h3>'
            h = re.sub(r'<h3>(.*?)</h3>', add_id, h)
            subs = re.findall(r'<h3 id="([\w-]+)">(.*?)</h3>', h)
        toc.append((num, title, slug, subs))
        secs.append(f'<section class="sec" id="sec-{slug}"><h2 id="{slug}"><span class="num">Section {int(num):02d}</span><span class="t">{e(title)}</span></h2>{h}</section>')

    howto = md_to_html(open(os.path.join(SRC, '_how-to-read.md'), encoding='utf-8').read())
    def toc_item(num, title, slug, subs):
        sub_links = ''.join('<a href="#%s">%s</a>' % (sid, re.sub(r'<[^>]+>', '', st)) for sid, st in subs[:14])
        return (f'<li><a class="sec" href="#{slug}"><span class="n">{int(num):02d}</span><span class="t">{e(title)}</span>'
                f'<span class="dots"></span></a>' + (f'<div class="subs">{sub_links}</div>' if subs else '') + '</li>')
    toc_html = '<ol>' + ''.join(toc_item(*t) for t in toc) + '</ol>'
    lede = re.search(r'<div class="box lede">\s*<p>(.*?)</p>', secs[3], re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else ''
    if len(blurb) > 260: blurb = blurb[:257].rsplit(' ', 1)[0] + '…'
    cover = (f'<div class="cover"><div class="band"></div><img class="mark" src="mark.png" alt="">'
             f'<div class="eyebrow">The Sacred Divide</div><h1>{e(name)}</h1>'
             f'<div class="family">{e(meta.get("family", ""))} family</div><div class="rule"></div>'
             f'<div class="tagline">Honor the faith · Name the machinery</div><div class="blurb">{e(blurb)}</div>'
             f'<div class="meta"><span>{e(meta.get("version", ""))} · checked {e(meta.get("checked", ""))}</span><span>{SITE}</span></div></div>')
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(name)} — The Sacred Divide</title>
<meta name="author" content="Noble Father Creations"><meta name="subject" content="{e(name)}: the full record from The Sacred Divide">
<link rel="stylesheet" href="sacred-divide.css">
<script>window.PagedConfig = {{ auto: true, after: () => {{ window.__paged = true; }} }};</script>
<script src="paged.polyfill.js"></script></head><body>
{cover}
<div class="front toc"><h1 id="contents">Contents</h1>{toc_html}</div>
<div class="front howto">{howto}</div>
{"".join(secs)}
</body></html>'''
    return doc, name, meta


def render(rid, html_only=False):
    os.makedirs(OUTDIR, exist_ok=True)
    doc, name, meta = build_html(rid)
    # the HTML sits beside the vendored assets so relative paths resolve; it is also a readable web version
    page = os.path.join(TOOLS, f'.build-{rid}.html')
    open(page, 'w', encoding='utf-8').write(doc)
    out_pdf = os.path.join(OUTDIR, f'{rid}.pdf')
    if html_only:
        print(page); return page
    subprocess.run(['node', os.path.join(TOOLS, 'print.js'), page, out_pdf, name], check=True)
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(out_pdf)
    w = PdfWriter(clone_from=r)
    w.add_metadata({'/Title': f'{name} — The Sacred Divide', '/Author': 'Noble Father Creations',
                    '/Subject': f'The full record for {name}: history, structure, money, the 30 techniques, cases and sources.',
                    '/Keywords': f'The Sacred Divide; {name}; {meta.get("family", "")}; {meta.get("version", "")}'})
    # bookmarks: contents, how to read, then each section with its subsections (and each technique)
    marks = json.load(open(out_pdf.replace('.pdf', '.marks.json')))
    os.remove(out_pdf.replace('.pdf', '.marks.json'))
    w._root_object.pop('/Outlines', None)
    parent = {}
    for m in marks:
        if not m['page']: continue
        pg, text = m['page'] - 1, m['text']
        sec = re.match(r'^SECTION (\d+)\s*(.*)$', text, re.I)
        if m['level'] == 1:                       # Contents, How to read this
            parent[1] = parent[2] = w.add_outline_item(text, pg); parent[3] = None
        elif sec:                                  # the 27 sections
            parent[2] = w.add_outline_item(f'{int(sec.group(1)):02d} · {sec.group(2)}', pg); parent[3] = None
        elif m['level'] == 2 and parent.get(1) is not None:   # headings inside How to read this
            w.add_outline_item(text, pg, parent=parent[1])
        elif m['level'] == 3 and parent.get(2) is not None:
            parent[3] = w.add_outline_item(text, pg, parent=parent[2])
        elif m['level'] == 4 and (parent.get(3) or parent.get(2)) is not None:
            w.add_outline_item(text, pg, parent=parent.get(3) or parent[2])
    w.page_mode = '/UseOutlines'
    with open(out_pdf, 'wb') as f: w.write(f)
    r = PdfReader(out_pdf)
    links = sum(1 for p in r.pages for a in (p.get('/Annots') or []) if a.get_object().get('/Subtype') == '/Link')
    def count(o):
        return sum(count(x) if isinstance(x, list) else 1 for x in o)
    print(f'{out_pdf}: {len(r.pages)} pages, {links} links, {count(r.outline)} bookmarks')
    # manifest the site's Download button reads: one entry per religion
    man_path = os.path.join(OUTDIR, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    man[rid] = {'title': name, 'family': meta.get('family', ''), 'file': f'{rid}.pdf', 'pages': len(r.pages),
                'bytes': os.path.getsize(out_pdf), 'version': meta.get('version', ''), 'checked': meta.get('checked', ''),
                'sections_filled': meta.get('sections_filled', '')}
    json.dump(dict(sorted(man.items())), open(man_path, 'w'), indent=1, ensure_ascii=False)
    os.remove(page)
    return out_pdf


if __name__ == '__main__':
    args = sys.argv[1:]
    html_only = '--html' in args
    ids = [a for a in args if not a.startswith('--')]
    if '--all' in args:
        ids = sorted(f[:-3] for f in os.listdir(SRC) if f.endswith('.md') and not f.startswith('_') and f != 'README.md')
    for rid in ids:
        render(rid, html_only)
