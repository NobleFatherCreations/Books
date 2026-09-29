#!/usr/bin/env python3
"""The Sacred Divide v5 — redesigned print edition (US Letter). One stylesheet (tools/pdf/sacred-divide-v5.css),
a per-volume theme, and the same build_sections() the site uses, so the text is identical to v4 except where
the wording log records a proposed edit.

Usage: python3 scripts/sacred-divide-pdf-v5.py catholicism
Output: library/_undeployed/sacred-divide-v5/<id>.pdf
"""
import importlib.util, math, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'sacred-divide-pdf-expanded.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
e = ex.e
ex.OUTDIR = os.path.join(ROOT, 'library/_undeployed/sacred-divide-v5')

# ---- proposed wording (mockup only): Loop 2 for Catholicism, built ONLY from techniques 5, 8, 20, 21 in the same volume.
LOOPS = {
 ('catholicism', 2): {
  'steps': [
   'Sin and confession are installed in childhood. Children are bonded early through fear of sin, reverence for priests and sacramental dependency, before they can weigh the teaching.',
   'The conscience is kept under permanent examination. Sexual teaching makes ordinary desire evidence of spiritual disorder, so there is always something to confess.',
   'Absolution runs through one route. Grave sin is taught to sever a person from grace, and the only authorized way back is confession to an ordained man, then penance.',
   'Relief arrives and wears off. The peace is real, and by Friday the anxiety has returned; the guilt, relief and returning guilt keep the penitent in weekly orbit.',
   'The debt regenerates. The institution is both the source of the shame and the distributor of mercy, so each act of relief renews the need for the next one.'],
  'feeds': [(5, 'Devaluation'), (8, 'Intermittent Reinforcement'), (20, 'Trauma Bonding'), (21, 'Learned Helplessness')],
  'closes': 'A repeating pattern would end when the penitent stopped. This one closes because the only relief on offer comes from the office that defines the debt. Devaluation creates the need, Intermittent Reinforcement meters the relief, Trauma Bonding ties the relief to the source of the wound, and Learned Helplessness teaches the penitent to endure rather than leave.',
  'breaks': 'The loop needs all four parts. It weakens wherever one is removed: where forgiveness can be sought from a source other than the office that names the sin (the person), or where the institution stops treating frequency of confession as the measure of devotion (the institution). This paragraph is analysis, not a documented finding.',
  'example': 'The volume’s own example is the scrupulous Catholic who finds confession relieving one week and anxious again by Friday.',
 }}


def wrap(text, n=11):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return lines + [cur]

def loop_svg(n, title):
    """1:1 scale (1 user unit = 1pt) so the 9pt labels are exactly 9pt on the page."""
    parts = [p.strip() for p in title.split(' to ')]
    if len(parts) > 1 and parts[0].lower() == parts[-1].lower(): parts = parts[:-1]
    k = len(parts); W, H, cx, cy, rx, ry = 221, 181, 110.5, 90.5, 66, 56
    pos = [(cx + rx * math.sin(2 * math.pi * i / k), cy - ry * math.cos(2 * math.pi * i / k)) for i in range(k)]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Loop {n}: {e(", then ".join(parts))}, and back to the start">'
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#7B1E22"/></marker></defs>']
    for i in range(k):
        a0, a1 = 2 * math.pi * i / k, 2 * math.pi * (i + 1) / k; d = 0.46 if k > 2 else 0.7
        s0, s1 = a0 + d, a1 - d
        p0 = (cx + rx * math.sin(s0), cy - ry * math.cos(s0)); p1 = (cx + rx * math.sin(s1), cy - ry * math.cos(s1))
        out.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rx} {ry} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="#7B1E22" stroke-width="1" marker-end="url(#ah)"/>')
    for i, (x, y) in enumerate(pos):
        lines = wrap(parts[i], 11); h = 11 * len(lines) + 10; w = 64
        out.append(f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" fill="#FAF6EC" stroke="#1A1714" stroke-width=".4"/>')
        for j, ln in enumerate(lines):
            out.append(f'<text x="{x:.1f}" y="{y-h/2+12.5+11*j:.1f}" text-anchor="middle" font-size="9" fill="#1A1714">{e(ln)}</text>')
        out.append(f'<rect x="{x-w/2-1:.1f}" y="{y-h/2-1:.1f}" width="13" height="13" fill="#7B1E22"/><text x="{x-w/2+5.5:.1f}" y="{y-h/2+8.5:.1f}" text-anchor="middle" font-size="7.5" fill="#FAF6EC">{i+1}</text>')
    out.append(f'<text x="{cx}" y="{cy+8}" text-anchor="middle" font-size="26" fill="#7B1E22">{n}</text></svg>')
    return ''.join(out)

def loops_html(rid, h):
    def one(m):
        n, title, text = int(m.group(1)), m.group(2), m.group(3)
        x = LOOPS.get((rid, n)); svg = loop_svg(n, title)
        if not x:
            return f'<div class="loop"><h3>{n} · {title}</h3><div class="row">{svg}<div><p>{text}</p></div></div></div>'
        steps = ''.join(f'<li>{e(s)}</li>' for s in x['steps'])
        feeds = ', '.join(f'<a class="tlink" href="#t-{t}">{t} · {e(nm)}</a>' for t, nm in x['feeds'])
        return (f'<div class="loop long"><h3>{n} · {title}</h3><span class="prop">Proposed expansion · pending review</span>'
                f'<div class="row">{svg}<div><p>{text}</p><p class="feeds"><b>Techniques that feed it</b>{feeds}</p></div></div>'
                f'<h4>How it runs</h4><ol class="steps">{steps}</ol><h4>Why it closes</h4><p>{e(x["closes"])}</p>'
                f'<h4>Where it could be broken, and by whom</h4><p>{e(x["breaks"])}</p><h4>An example from this page</h4><p>{e(x["example"])}</p></div>')
    return re.sub(r'<div class="box card">\s*<h4>(\d+) · (.+?)</h4>\s*<p>(.*?)</p>\s*</div>', one, h, flags=re.S)

def tactics_html(h):
    def one(m):
        blk = m.group(0)
        g = re.search(r'<p><strong>Evidence grade\.</strong>(.*?)</p>', blk, re.S)
        if not g: return blk
        blk = blk.replace(g.group(0), '')
        note = '<p class="gradenote"><strong>Evidence grade</strong>' + g.group(1) + '</p>'
        return re.sub(r'(</h4>\s*<p><em>.*?</em></p>)', lambda k: k.group(1) + note, blk, count=1, flags=re.S)
    return re.sub(r'<div class="box tactic">.*?</div>', one, h, flags=re.S)

def rose(accent='#B08A42', size=None):
    petals = ''.join(f'<path transform="rotate({i*30} 100 100)" d="M100 100 C 86 78, 86 48, 100 30 C 114 48, 114 78, 100 100 Z" fill="none" stroke="{accent}" stroke-width=".9"/>' for i in range(12))
    rings = ''.join(f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="{accent}" stroke-width=".8"/>' for r in (94, 70, 22))
    return f'<svg class="orn" viewBox="0 0 200 200" role="img" aria-label="Twelve-fold geometric ornament">{rings}{petals}<circle cx="100" cy="100" r="3" fill="{accent}"/></svg>'


PALETTE = {'#1A1714': (26, 23, 20), '#7B1E22': (123, 30, 34), '#B08A42': (176, 138, 66), '#FAF6EC': (250, 246, 236), '#D8D0BC': (216, 208, 188)}

def snap(hexv):
    h = hexv.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return min(PALETTE, key=lambda k: sum((a - c) ** 2 for a, c in zip((r, g, b), PALETTE[k])))

def conform_svg(m):
    svg = m.group(0)
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not vb: return svg
    W = float(vb.group(1)); target_w = 306.0; k = target_w / W
    svg = re.sub(r'(fill|stroke|stop-color)="(#[0-9A-Fa-f]{3,6})"', lambda x: f'{x.group(1)}="{snap(x.group(2))}"', svg)
    def fs(x):
        n = float(x.group(1)) * k
        t = 9.0 if n >= 8.2 else 7.5
        return f'font-size="{t / k:.2f}"'
    svg = re.sub(r'font-size="([\d.]+)"', fs, svg)
    svg = re.sub(r'width="100%"', f'width="{target_w}pt"', svg, count=1)
    return svg

def words(html): return len(re.sub(r'<[^>]+>', ' ', html).split())

def matrix_html(h):
    def one(m):
        heads = re.findall(r'<th>(.*?)</th>', m.group(0)); cells = re.findall(r'<td class="s(\w)">(.*?)</td>', m.group(0))
        word = {'Y': 'Yes', 'P': 'Partial', 'N': 'No', '?': 'Not assessable'}
        cls = {'Y': 'sY', 'P': 'sP', 'N': 'sN', '?': 'sQ'}
        th = ''.join(f'<th scope="col">{hh}</th>' for hh in heads)
        td = ''.join(f'<td class="{cls.get(t, "sQ")}">{word.get(t, t)}</td>' for _, t in cells)
        return f'<table class="matrix short"><thead><tr>{th}</tr></thead><tbody><tr>{td}</tr></tbody></table>'
    h = re.sub(r'<table class="score">.*?</table>', one, h, flags=re.S)
    return re.sub(r'(</table>)\s*<p>(<strong>Y</strong>)', r'\1<p class="legend">\2', h)

def datapage(h):
    """Full-page evidence map: four DATUM squares + all thirty techniques by stage, grade shown by shape as well as fill."""
    tokens = re.findall(r'<h3 id="stage-(\d+)">Stage \d+ · (.+?)</h3>|<h4 id="t-(\d+)">\d+ · (.+?)</h4>|<span class="chip g-(\w+)">', h)
    rows, cur, tech = [], None, {}
    last = None
    for st, sname, tn, tname, g in tokens:
        if st: cur = [int(st), sname, []]; rows.append(cur)
        elif tn: last = [int(tn), tname, 'ungraded']; (cur[2] if cur else rows.append([0, '', []]) or rows[-1][2]).append(last)
        elif g and last is not None and last[2] == 'ungraded': last[2] = g
    counts = {}
    for r in rows:
        for t in r[2]: counts[t[2]] = counts.get(t[2], 0) + 1
    order = ['codified', 'documented', 'taught', 'cultural', 'contested', 'reformed', 'ungraded']
    datums = ''.join(f'<div class="datum"><b>{counts[g]}</b><span>{g}</span></div>' for g in order if counts.get(g))
    body = ''.join(f'<div class="stagerow"><div class="st">Stage {r[0]}<b>{e(r[1])}</b></div><div class="cells">' + ''.join(
        f'<a class="c-{t[2]}" href="#t-{t[0]}"><i>{t[0]}</i><span>{e(t[1])}<br><span class="micro">{t[2]}</span></span></a>' for t in r[2]) + '</div></div>' for r in rows)
    return (f'<div class="datapage"><h3 id="evidence-map">How the thirty techniques are established here</h3><div class="datums">{datums}</div>'
            f'{body}</div>')

def build_html(rid):
    secs_data, meta = ex.build_sections(rid); name = meta.get('title', rid)
    toc, secs = [], []
    stats = {'primer': 0, 'lead': 0, 'consequence': 0, 'afterword': 0}
    for num, title, slug, h, subs in secs_data:
        if slug == 'loops': h = loops_html(rid, h)
        if slug == 'techniques':
            h = tactics_html(h)
            h = re.sub(r'<figure class="fig">.*?</figure>\s*<h3 id="techniques-index">.*?</h3>\s*<div class="tgrid">.*?</div>(?=\s*<h3 id="stage-1">)', '', h, flags=re.S)
            dp = datapage(h)
        else: dp = ''
        if slug == 'at-a-glance': h = matrix_html(h)
        if slug == 'a-day-inside': h = re.sub(r'(<p><em>[^<]*</em></p>\s*<p>)(\w)', r'\1<span class="dc" aria-hidden="true">\2</span><span class="sr-first">\2</span>', h, count=1)
        # the unanswered question becomes a Quote page
        qm = re.search(r'<div class="box question">\s*<p>(.*?)</p>\s*</div>', h, re.S)
        if qm and slug == 'forefront':
            h = re.sub(r'<h3 id="[\w-]+">The unanswered question</h3>\s*', '', h)
            h = h.replace(qm.group(0), f'<div class="quote-page"><span class="lbl">The unanswered question</span><p class="question">{qm.group(1)}</p></div>')
        # narration boxes: PRIMER / CONSEQUENCE only within the 55-word cap; longer text is body text
        im = re.match(r'\s*<div class="box note-a intro"><span class="lbl">(.*?)</span>(.*?)</div>', h, re.S)
        lead = ''
        if im:
            h = h[im.end():]
            if words(im.group(2)) <= 55: lead = f'<div class="primer"><span class="lbl">{im.group(1)}</span>{im.group(2)}</div>'; stats['primer'] += 1
            else: lead = f'<div class="lead-in"><span class="lbl">{im.group(1)}</span>{im.group(2)}</div>'; stats['lead'] += 1
        fm = re.search(r'<aside class="box foryou"><span class="lbl">(.*?)</span>(.*?)</aside>', h, re.S)
        tail = ''
        if fm:
            h = h.replace(fm.group(0), '')
            if words(fm.group(2)) <= 55: tail = f'<aside class="consequence"><span class="lbl">{fm.group(1)}</span>{fm.group(2)}</aside>'; stats['consequence'] += 1
            else: tail = f'<aside class="consequence long"><span class="lbl">{fm.group(1)}</span>{fm.group(2)}</aside>'; stats['afterword'] += 1
        h = re.sub(r'(<h[34][^>]*>(?:(?!</h[34]>).)*</h[34]>)\s*(<div class="box (?:case|card|tell|stage)"[^>]*>(?:(?!<div).)*?</div>)', r'<div class="keep">\1\2</div>', h, flags=re.S) if slug not in ('techniques', 'loops') else h
        h = re.sub(r'<table class="short( wide)?">((?:(?!</table>).)*)</table>', lambda m: ('<table class="long">' if m.group(2).count('<tr>') > 4 else m.group(0)[:m.group(0).index('>')+1]) + m.group(2) + '</table>', h, flags=re.S)
        toc.append((num, title, slug, subs))
        div = f'<div class="divider-page" aria-hidden="true">{rose("#B08A42")}</div>' if slug in ('techniques', 'sources') else ''
        big = slug in ('techniques', 'sources') or words(h) > 1900
        secs.append(f'{div}<section class="sec" id="sec-{slug}"><div class="{"opener-page" if big else "opener-band"}"><h2 id="{slug}"><span class="num">{int(num):02d}</span><span class="t">{e(title)}</span></h2><div class="orn-rule"></div></div>{dp}{lead}{h}{tail}</section>')
    howto = ex.md_to_html(open(os.path.join(ex.SRC, '_how-to-read.md'), encoding='utf-8').read())
    def toc_item(num, title, slug, subs):
        sl = ''.join('<a href="#%s">%s</a>' % (s, re.sub(r'<[^>]+>', '', t)) for s, t in subs[:14])
        return (f'<li><a class="sec" href="#{slug}"><span class="n">{int(num):02d}</span><span class="t">{e(title)}</span><span class="dots"></span></a>' + (f'<div class="subs">{sl}</div>' if subs else '') + '</li>')
    lede = re.search(r'<div class="box lede">\s*<p>(.*?)</p>', ''.join(secs), re.S)
    blurb = re.sub(r'<[^>]+>', '', lede.group(1)) if lede else ''
    if len(blurb) > 260: blurb = blurb[:257].rsplit(' ', 1)[0] + '…'
    cover = (f'<div class="cover"><div class="band"></div>{rose()}<div class="eyebrow">The Sacred Divide</div>'
             f'<div class="for">The full record · with reader narration</div><h1>{e(name)}</h1><div class="family">{e(meta.get("family", ""))} family</div>'
             f'<div class="rule"></div><div class="tagline">Honor the faith · Name the machinery</div><div class="blurb">{e(blurb)}</div>'
             f'<div class="meta"><span>v5 draft · text checked {e(meta.get("checked", ""))}</span><span>{ex.SITE}</span></div></div>')
    preface = f'<div class="front preface"><h1 id="preface">How this edition works</h1>{ex.md_to_html(ex.PREFACE.replace("{name}", name))}</div>'
    colophon = ('<div class="front colophon"><h1 id="colophon">Colophon</h1><p>Set in EB Garamond (SIL Open Font License), regular, italic and bold, with true small capitals and old-style figures in text and lining tabular figures in tables. '
                'Laid out with Paged.js in Chromium from the same Markdown that feeds the website. US Letter, single-sided, tagged for accessibility and checked against PDF/UA-1 with veraPDF. '
                f'Built {date.today().isoformat()}. Text checked {e(meta.get("checked", ""))}.</p><p>Palette: ink, oxblood, gold, cream, rule. Seven type sizes. Rules of 0.4 pt and 2 pt only.</p></div>')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{e(name)} — The Sacred Divide</title>
<meta name="author" content="Noble Father Creations"><meta name="subject" content="{e(name)}: the full record">
<link rel="stylesheet" href="sacred-divide-v5.css">
<script>
window.PagedConfig = {{ auto: true, before: () => {{
  const q = new URLSearchParams(location.search), list = k => (q.get(k) || '').split(',').filter(Boolean);
  list('snug').forEach(v => {{ const [id, lvl] = v.split(':'), s = document.getElementById(id); if (s) s.classList.add('snug' + (lvl === '1' ? '' : lvl)); }});
  const tables = document.querySelectorAll('table'); tables.forEach((t, i) => t.dataset.ti = i);
  list('brk').forEach(i => {{ const t = tables[+i]; if (!t) return; const p = t.previousElementSibling; (p && /^H[34]$/.test(p.tagName) ? p : t).classList.add('newpage'); }});
}}, after: () => {{
  document.querySelectorAll('.pagedjs_margin, .pagedjs_margin-content').forEach(m => m.setAttribute('aria-hidden', 'true'));
  // a CONSEQUENCE panel that closes a section grows to the page foot, so the section ends on a deliberate dark block
  document.querySelectorAll('.pagedjs_page').forEach(pg => {{
    const c = pg.querySelector('.consequence'), area = pg.querySelector('.pagedjs_page_content'); if (!c || !area) return;
    const free = area.getBoundingClientRect().bottom - c.getBoundingClientRect().bottom;
    if (free > 8) {{ c.style.minHeight = (c.getBoundingClientRect().height + free - 2) + 'px'; c.classList.add('fill'); }}
  }});
  window.__paged = true; }} }};
</script><script src="paged.polyfill.js"></script></head><body>
{cover}{preface}<div class="front toc"><h1 id="contents">Contents</h1><ol>{"".join(toc_item(*t) for t in toc)}</ol></div><div class="front howto">{howto}</div>{"".join(secs)}{colophon}</body></html>"""
    # heading levels must not skip (PDF/UA 7.4.2)
    last = [1]
    def lvl(m):
        n = int(m.group(1)); attrs = m.group(2) or ''
        if n > last[0] + 1:
            fixed = last[0] + 1; last[0] = fixed
            return f'<h{fixed}{attrs} class="look{n}">{m.group(3)}</h{fixed}>'
        last[0] = n; return m.group(0)
    doc = re.sub(r'<h([1-6])((?: [^>]*)?)>(.*?)</h\1>', lvl, doc, flags=re.S)
    doc = re.sub(r'<figure class="fig">(.*?)</figure>', lambda m: '<figure class="fig" role="img" aria-label="' + re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1)))[:300].strip().replace('"', '') + '">' + m.group(1) + '</figure>', doc, flags=re.S)
    doc = re.sub(r'<svg[^>]*viewBox="0 0 [\d.]+ [\d.]+"[^>]*width="100%"[^>]*>.*?</svg>', conform_svg, doc, flags=re.S)
    print('narration boxes:', stats)
    return doc, name, meta

def accessibility_pass(path, title):
    """Document-level PDF/UA hygiene: language, title display, XMP with the PDF/UA id, and a /Contents string on every link."""
    import pikepdf
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        pdf.Root.Lang = pikepdf.String('en')
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
        with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
            m['dc:title'] = title; m['dc:creator'] = ['Noble Father Creations']; m['dc:language'] = ['en']
            m['{http://www.aiim.org/pdfua/ns/id/}part'] = '1'
        n = 0
        for i, page in enumerate(pdf.pages):
            for a in page.get('/Annots', []):
                if a.get('/Subtype') != '/Link' or '/Contents' in a: continue
                act = a.get('/A')
                if act is not None and '/URI' in act: a.Contents = pikepdf.String('External link: ' + str(act.URI))
                else: a.Contents = pikepdf.String('Jump to a section or source on another page of this document')
                n += 1
        pdf.save(path)
    return n

ex.build_html = build_html
if __name__ == '__main__':
    for rid in [a for a in sys.argv[1:] if not a.startswith('--')]:
        out = ex.render(rid, '--html' in sys.argv)
        if out and not '--html' in sys.argv:
            print('links given a description:', accessibility_pass(out, f'{rid.replace("-", " ").title()} — The Sacred Divide'))
            import sacred_divide_pdfua as UA
            print('artifact blocks, list items restructured:', UA.run(out))
