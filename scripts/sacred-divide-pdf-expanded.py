#!/usr/bin/env python3
"""The Sacred Divide — expanded edition PDFs, for every religion, addressed to no one in particular.

Same page as the standard PDF (scripts/sacred-divide-pdf.py), plus the reader narration from
scripts/sacred_divide_narration.py:

  - "Before you read" — a short box at the top of each of the 27 sections: what the section shows.
  - "Why this matters to you" — a box at the END of each section: where the section lands on an
    ordinary reader (member, donor, parent, voter, someone thinking of leaving), with a question.
  - Section 23's hard questions expanded into cards: the question, why it is asked, and an example
    already on the page.

It uses the review-copy typography (tools/pdf/sacred-divide-personal.css: bigger, blacker type;
boxes may break across pages so pages fill) plus tools/pdf/sacred-divide-expanded.css for the
"why this matters" box. No recipient, no personal preface, no Salafi layer — those belong to the
named review copies in scripts/sacred-divide-pdf-abdurahman.py.

build_sections(rid) is also what scripts/sacred-divide-site.py uses, so the site and the PDFs
narrate identically.

Usage:  python3 scripts/sacred-divide-pdf-expanded.py <id> [<id> …]   |   --all
Output: library/_undeployed/sacred-divide-pdf/expanded/<id>-expanded.pdf (+ manifest.json there)
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, 'tools/pdf')
OUTDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-pdf/expanded')
SITE = 'noblefathercreations.com/faith'

spec = importlib.util.spec_from_file_location('sdp', os.path.join(HERE, 'sacred-divide-pdf.py'))
sdp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdp)
sys.path.insert(0, HERE)
import sacred_divide_narration as narr  # noqa: E402

e, inline, md_to_html = sdp.e, sdp.inline, sdp.md_to_html
SRC = sdp.SRC


def ids_all():
    return sorted(f[:-3] for f in os.listdir(SRC) if f.endswith('.md') and not f.startswith('_') and f != 'README.md')


# ---------------------------------------------------------------- narration boxes
def intro_box(text):
    return f'<div class="box note-a intro"><span class="lbl">{e(narr.INTRO_LABEL)}</span>{md_to_html(text)}</div>'


def foryou_box(text):
    return f'<aside class="box foryou"><span class="lbl">{e(narr.FORYOU_LABEL)}</span>{md_to_html(text)}</aside>'


def hardq_cards(content, expansions):
    """The numbered question list → cards; '### In closing' onward stays as markdown."""
    m = re.search(r'^\s*1\.\s.*?(?=\n### )', content, re.S)
    if not m:
        return md_to_html(content)
    items = [it.strip().replace('\n', ' ') for it in re.findall(r'^\d+\.\s+(.*?)(?=^\d+\.\s|\Z)', m.group(0), re.M | re.S)]
    cards = []
    for i, q in enumerate(items, 1):
        x = expansions.get(i, {})
        body = ''
        if x.get('why'):
            body += f'<h4>Why this is asked</h4><p>{inline(e(x["why"]))}</p>'
        if x.get('example'):
            body += f'<h4 class="ex">Example already on this page</h4><p>{inline(e(x["example"]))}</p>'
        cards.append(f'<div class="box hardq"><div class="qhead"><div class="qn">Question {i} of {len(items)}</div>'
                     f'<div class="qtext">{inline(e(q))}</div></div>{body}</div>')
    return ''.join(cards) + md_to_html(content[m.end():])


# ---------------------------------------------------------------- the 27 sections, narrated
def build_sections(rid):
    """[(num, title, slug, body_html, subs)] with narration placed before/after each section body."""
    raw = open(os.path.join(SRC, f'{rid}.md'), encoding='utf-8').read()
    narr.EDITS.reset(rid, 'narration')
    meta, body = sdp.front_matter(raw)
    src_part = re.search(r'^## \d+\. Sources \{#sources\}\n(.*?)(?=^## \d+\.)', body, re.S | re.M)
    sdp.VALID = {int(n) for n in re.findall(r'^\s*(\d+)\.\s', src_part.group(1), re.M)} if src_part else set()
    tech = re.search(r'^## \d+\. The 30 techniques \{#techniques\}\n(.*?)(?=^## \d+\.)', body, re.S | re.M)  # §12 only; §13 loop cards share the heading shape
    sdp.TACTIC_NAMES = {int(n): re.sub(r'\s*\{#.*', '', t) for n, t in re.findall(r'^#### (\d+) · (.+)$', tech.group(1) if tech else body, re.M)}
    parts = re.split(r'^## (\d+)\. (.+?) \{#([\w-]+)\}\s*$', body, flags=re.M)
    out = []
    for i in range(1, len(parts), 4):
        num, title, slug, content = parts[i], parts[i + 1], parts[i + 2], parts[i + 3]
        h = hardq_cards(content, narr.questions(rid)) if slug == 'questions' else md_to_html(content)
        if slug == 'sources':
            h = sdp.sources_ids(h)
        if slug == 'cases':
            h = re.sub(r'(<strong>tactics:</strong>)\s*([\d, ]+)', lambda m: m.group(1) + ' ' + ', '.join(
                f'<a class="tlink" href="#t-{n.strip()}">{n.strip()} · {sdp.TACTIC_NAMES.get(int(n), "")}</a>' for n in m.group(2).split(',') if n.strip()), h)
            h = re.sub(r'(<strong>grade:</strong>)\s*(\w+)', lambda m: f'{m.group(1)} <span class="chip g-{m.group(2).lower()}">{m.group(2)}</span>', h)
        if slug == 'at-a-glance':
            h = sdp.score_cells(h)
        if slug == 'techniques':
            grades = re.findall(r'<span class="chip g-(\w+)">', h)
            counts = {}
            for g in grades:
                counts[g.title()] = counts.get(g.title(), 0) + 1
            index = re.findall(r'<h4 id="t-(\d+)">\d+ · (.+?)</h4>', h)
            grade_of = dict(re.findall(r'id="t-(\d+)">.*?<span class="chip g-(\w+)">', h, re.S))
            grid = ''.join(f'<a href="#t-{n}"><span class="n">{n}</span><span class="nm">{nm}</span>'
                           f'<span class="chip g-{grade_of.get(n, "ungraded")}">{grade_of.get(n, "ungraded").title()}</span></a>' for n, nm in index)
            lead = (sdp.grade_bar(counts) if counts else '') + (f'<h3 id="techniques-index">All thirty at a glance</h3><div class="tgrid">{grid}</div>' if grid else '')
            h = re.sub(r'(</p>)', r'\1' + lead.replace('\\', '\\\\'), h, count=1) if lead else h
        if slug != 'techniques':
            k = [0]

            def add_id(m, slug=slug, k=k):
                k[0] += 1
                return f'<h3 id="{slug}-{k[0]}">{m.group(1)}</h3>'
            h = re.sub(r'<h3>(.*?)</h3>', add_id, h)
        # short tables (the scorecard, most ledgers) never split across a page; see sacred-divide-expanded.css
        def tag_table(m):
            body = m.group(1)
            head = re.search(r'<tr>(.*?)</tr>', body, flags=re.S)
            cls = (['short'] if body.count('<tr>') <= int(os.environ.get('SHORTROWS', '9')) else []) + (['wide'] if head and head.group(1).count('<th') >= 6 else [])
            return (f'<table class="{" ".join(cls)}">' if cls else '<table>') + body + '</table>'
        h = re.sub(r'<table>(.*?)</table>', tag_table, h, flags=re.S)
        subs = re.findall(r'<h3 id="([\w-]+)">(.*?)</h3>', h)
        intro, fy = narr.intro(rid, slug), narr.foryou(rid, slug)
        h = (intro_box(intro) if intro else '') + h + (foryou_box(fy) if fy else '')
        out.append((num, title, slug, h, subs))
    narr.EDITS.check(rid, {'narration'})
    return out, meta


PREFACE = """This is the record of {name} in *The Sacred Divide*. It has 27 sections, the same 27 used for every tradition, so that any section can be set beside the same section for another. Every fact is sourced.

**Before each section**, a short note says what the section is built to show, so you know what you are looking at before you read the detail.

**After each section**, a note headed *Why this matters to you* points at the part of the section most likely to touch an ordinary reader: a member, a donor, a parent, a voter, someone thinking about leaving, or someone outside forming an opinion. It usually ends with a question. The questions are not traps. They are the ones a careful reader would ask anyway.

**The hard questions** in section 23 are set out one at a time: the question, why it is asked, and an example already documented in this record.

Where a note states a fact, the fact comes from this record's own tables and cited sources or, in a few places, from a well-known research finding named in the text. Corrections are logged, with their dates, in the last section, *What changed on this page*."""


def build_html(rid):
    secs_data, meta = build_sections(rid)
    name = meta.get('title', rid)
    toc, secs = [], []
    for num, title, slug, h, subs in secs_data:
        toc.append((num, title, slug, subs))
        secs.append(f'<section class="sec" id="sec-{slug}"><h2 id="{slug}"><span class="num">Section {int(num):02d}</span>'
                    f'<span class="t">{e(title)}</span></h2>{h}</section>')
    howto = md_to_html(open(os.path.join(SRC, '_how-to-read.md'), encoding='utf-8').read())

    def toc_item(num, title, slug, subs):
        sub_links = ''.join('<a href="#%s">%s</a>' % (sid, re.sub(r'<[^>]+>', '', st)) for sid, st in subs[:14])
        return (f'<li><a class="sec" href="#{slug}"><span class="n">{int(num):02d}</span><span class="t">{e(title)}</span>'
                f'<span class="dots"></span></a>' + (f'<div class="subs">{sub_links}</div>' if subs else '') + '</li>')
    toc_html = '<ol>' + ''.join(toc_item(*t) for t in toc) + '</ol>'
    lede = re.search(r'<div class="box lede">\s*<p>(.*?)</p>', secs[2] + secs[3], re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else ''
    if len(blurb) > 260:
        blurb = blurb[:257].rsplit(' ', 1)[0] + '…'
    cover = (f'<div class="cover"><div class="band"></div><img class="mark" src="mark.png" alt="">'
             f'<div class="eyebrow">The Sacred Divide</div><div class="for">The full record</div>'
             f'<h1>{e(name)}</h1><div class="family">{e(meta.get("family", ""))} family</div><div class="rule"></div>'
             f'<div class="tagline">Honor the faith · Name the machinery</div><div class="blurb">{e(blurb)}</div>'
             f'<div class="meta"><span>{e(meta.get("version", ""))} · checked {e(meta.get("checked", ""))}</span><span>{SITE}</span></div></div>')
    preface = f'<div class="front preface"><h1 id="preface">Before you begin</h1>{md_to_html(PREFACE.replace("{name}", name))}</div>'
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(name)} — The Sacred Divide</title>
<meta name="author" content="Noble Father Creations"><meta name="subject" content="{e(name)}: the full record, expanded with reader narration">
<link rel="stylesheet" href="sacred-divide.css">
<link rel="stylesheet" href="sacred-divide-personal.css">
<link rel="stylesheet" href="sacred-divide-expanded.css">
<script>
// print.js lays the book out, measures it, and reloads with ?snug=<section ids>&brk=<table numbers> when a
// section spills a few lines onto a page of its own or a table's header row is left alone at a page foot.
window.PagedConfig = {{ auto: true, before: () => {{
  const q = new URLSearchParams(location.search), list = k => (q.get(k) || '').split(',').filter(Boolean);
  list('snug').forEach(v => {{ const [id, lvl] = v.split(':'), s = document.getElementById(id); if (s) s.classList.add('snug' + (lvl === '1' ? '' : lvl)); }});
  const tables = document.querySelectorAll('table');
  tables.forEach((t, i) => t.dataset.ti = i);
  list('brk').forEach(i => {{ const t = tables[+i]; if (!t) return; const p = t.previousElementSibling;
    (p && /^H[34]$/.test(p.tagName) ? p : t).classList.add('newpage'); }});
}}, after: () => {{ window.__paged = true; }} }};
</script>
<script src="paged.polyfill.js"></script></head><body>
{cover}
{preface}
<div class="front toc"><h1 id="contents">Contents</h1>{toc_html}</div>
<div class="front howto">{howto}</div>
{"".join(secs)}
</body></html>'''
    return doc, name, meta


def render(rid, html_only=False):
    os.makedirs(OUTDIR, exist_ok=True)
    doc, name, meta = build_html(rid)
    page = os.path.join(TOOLS, f'.build-exp-{rid}.html')
    open(page, 'w', encoding='utf-8').write(doc)
    if html_only:
        print(page)
        return page
    out_pdf = os.path.join(OUTDIR, f'{rid}-expanded.pdf')
    subprocess.run(['node', os.path.join(TOOLS, 'print.js'), page, out_pdf, name], check=True)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter(clone_from=PdfReader(out_pdf))
    w.add_metadata({'/Title': f'{name} — The Sacred Divide', '/Author': 'Noble Father Creations',
                    '/Subject': f'The full record for {name}: 27 sections, sourced.',
                    '/Keywords': f'The Sacred Divide; {name}; {meta.get("family", "")}; {meta.get("version", "")}'})
    marks = json.load(open(out_pdf.replace('.pdf', '.marks.json')))
    os.remove(out_pdf.replace('.pdf', '.marks.json'))
    w._root_object.pop('/Outlines', None)
    parent = {}
    for m in marks:
        if not m['page']:
            continue
        pg, text = m['page'] - 1, m['text']
        sec = re.match(r'^SECTION (\d+)\s*(.*)$', text, re.I)
        if m['level'] == 1:
            parent[1] = parent[2] = w.add_outline_item(text, pg); parent[3] = None
        elif sec:
            parent[2] = w.add_outline_item(f'{int(sec.group(1)):02d} · {sec.group(2)}', pg); parent[3] = None
        elif m['level'] == 2 and parent.get(1) is not None:
            w.add_outline_item(text, pg, parent=parent[1])
        elif m['level'] == 3 and parent.get(2) is not None:
            parent[3] = w.add_outline_item(text, pg, parent=parent[2])
        elif m['level'] == 4 and (parent.get(3) or parent.get(2)) is not None:
            w.add_outline_item(text, pg, parent=parent.get(3) or parent[2])
    w.page_mode = '/UseOutlines'
    with open(out_pdf, 'wb') as f:
        w.write(f)
    r = PdfReader(out_pdf)
    print(f'{out_pdf}: {len(r.pages)} pages')
    man_path = os.path.join(OUTDIR, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    man[rid] = {'title': name, 'family': meta.get('family', ''), 'file': os.path.basename(out_pdf), 'pages': len(r.pages),
                'bytes': os.path.getsize(out_pdf), 'version': meta.get('version', ''), 'checked': meta.get('checked', '')}
    json.dump(dict(sorted(man.items())), open(man_path, 'w'), indent=1, ensure_ascii=False)
    os.remove(page)
    return out_pdf


if __name__ == '__main__':
    args = sys.argv[1:]
    ids = ids_all() if '--all' in args else [a for a in args if not a.startswith('--')]
    for rid in ids:
        render(rid, '--html' in args)
