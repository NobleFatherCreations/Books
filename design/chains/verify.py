#!/usr/bin/env python3
"""Checks for the manipulation-chain sites. python3 design/chains/verify.py [corp]
1. Every chain page carries every word of its source file, section by section (interface additions excluded).
2. Sections appear in the author's order with the author's headings.
3. A safety note, when present, comes directly under the title, before anything else in the text.
4. Every internal link resolves to a built page (or an anchor on it). 5. No outside requests except the sanctioned beacon.
"""
import os, re, sys, glob, collections
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SITE = os.path.join(ROOT, 'library/fractal2/site')
SEC = {'corp': ('CORP', 'corporate')}[(sys.argv[1] if len(sys.argv) > 1 else 'corp')]
PKG = os.path.join(ROOT, 'content/fractal/_packages/combo_clusters_markdown_v2', SEC[0])
SKIP = {'sigcap', 'st', 'copy', 'stdbox', 'link-n', 'safety-leave', 'lbl-x', 'tl-n'}
STD_LINES = ['Plus the Universal Evidence list in the Sector Standards.', 'Apply the Universal Benign Explanations and concern tests in the Sector Standards.', 'Tier definitions and sector bodies are in the Sector Standards.']

def wordbag(t):
    t = t.replace('’', "'").replace('‘', "'")
    return collections.Counter(w.lower() for w in re.findall(r"[A-Za-z0-9']+", t) if not w.isdigit())

class Sections(HTMLParser):
    """collect text per <section id=...> inside main, skipping interface-only elements and svg"""
    def __init__(self):
        super().__init__(); self.stack = []; self.cur = None; self.text = collections.OrderedDict(); self.heads = collections.OrderedDict(); self.skip = 0; self.inh2 = False
    def handle_starttag(self, tag, a):
        a = dict(a); cls = set((a.get('class') or '').split())
        skipping = tag in ('svg', 'button', 'script', 'style') or bool(cls & SKIP)
        self.stack.append((tag, skipping))
        if skipping: self.skip += 1
        if tag == 'section' and a.get('id') and 'sec' in cls:
            self.cur = a['id']; self.text[self.cur] = ''; self.heads[self.cur] = ''
        if tag == 'h2' and self.cur: self.inh2 = True
    def handle_endtag(self, tag):
        while self.stack:
            t, sk = self.stack.pop()
            if sk: self.skip -= 1
            if t == tag: break
        if tag == 'h2': self.inh2 = False
        if tag == 'section': self.cur = None
    def handle_data(self, d):
        if self.cur and not self.skip:
            if self.inh2: self.heads[self.cur] += d
            else: self.text[self.cur] += ' ' + d

def src_sections(path):
    t = open(path).read()
    t = re.sub(r'^---\n.*?\n---\n', '', t, flags=re.S)
    t = re.sub(r'^# .*\n', '', t, count=1, flags=re.M)
    parts = re.split(r'^## (.+)$', t, flags=re.M)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]

def md_text(md):
    md = md.replace('**', '').replace('· · ·', ' ')
    md = re.sub(r'^\|[\s\-:|]+\|$', '', md, flags=re.M)
    md = re.sub(r'^\s*\d+\.\s', ' ', md, flags=re.M)
    md = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*', r'\1', md)
    return md.replace('>', ' ').replace('|', ' ')

slug_of = lambda f: re.sub(r'^%s_C\d+_' % SEC[0], '', os.path.basename(f)[:-3])
def sid(h): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', h.lower())).strip('-')

fails, n = [], 0
for f in sorted(glob.glob(os.path.join(PKG, SEC[0] + '_C[0-9]*.md'))):
    slug = slug_of(f); page = os.path.join(SITE, 'fractal2', SEC[1], slug + '.html')
    if not os.path.exists(page): fails.append('%s: page missing' % slug); continue
    h = open(page).read(); P = Sections(); P.feed(h); n += 1
    src = src_sections(f)
    ids = [sid(x) for x, _ in src]
    got = list(P.text.keys())
    if got != ids: fails.append('%s: section order %s != %s' % (slug, got[:4], ids[:4]))
    for head, md in src:
        k = sid(head)
        if k not in P.text: continue
        if P.heads[k].strip() != head and k != 'the-name':
            fails.append('%s: heading "%s" shown as "%s"' % (slug, head, P.heads[k].strip()))
        a = wordbag(md_text(md)); b = wordbag(P.text[k])
        if head == 'Recognition Cue Cards':   # "SPOT IT —" is shown as the card's "Spot it" label
            b.update(wordbag(' '.join(['spot it'] * md.count('SPOT IT'))))
            b.subtract(wordbag(' '.join(['spot it'] * md.count('SPOT IT'))))
        if head == 'Where Each Tactic Happened':   # the header row is shown as a label on each stacked row
            hdr = next((l for l in md.split('\n') if l.startswith('|')), '')
            a = wordbag(md_text(md.replace(hdr, '', 1)))
        missing = a - b; extra = b - a
        if missing: fails.append('%s / %s: missing words %s' % (slug, head, dict(list(missing.items())[:6])))
        if extra: fails.append('%s / %s: added words %s' % (slug, head, dict(list(extra.items())[:6])))
    # lists keep their length: the chain's steps, numbered 1..n with the right stage, and the indicators
    vb = re.search(r'<section class="sec sec-verbal-breakdown".*?</section>', h, re.S)
    if vb:
        nums = [int(x) for x in re.findall(r'<span class="link-n">(\d+)</span>', vb.group(0))]
        n_t = len(re.findall(r'^\s+- ', open(f).read().split('---')[1], re.M))
        if nums != list(range(1, len(nums) + 1)) or len(nums) != n_t:
            fails.append('%s: chain steps numbered %s for %d tactics' % (slug, nums, n_t))
    for blk, cls in (('observable-indicators', 'ind'),):
        m2 = re.search(r'<section class="sec sec-%s".*?</section>' % blk, h, re.S)
        if m2 and m2.group(0).count('<ol class="%s">' % cls) != 1: fails.append('%s: %s split into %d lists' % (slug, blk, m2.group(0).count('<ol class="%s">' % cls)))
    if src and src[0][0].startswith('Safety Note'):
        m = h.find('class="ch-title"'); s = h.find('class="safety sec'); j = h.find('class="meta"')
        if not (m < s < j): fails.append('%s: safety note not directly under the title' % slug)
# links and requests
built = set()
for p in glob.glob(os.path.join(SITE, 'fractal2', SEC[1] + '.html')) + glob.glob(os.path.join(SITE, 'fractal2', SEC[1], '**', '*.html'), recursive=True):
    built.add('/' + os.path.relpath(p, SITE)[:-5])
bad, ext = collections.Counter(), collections.Counter()
for p in glob.glob(os.path.join(SITE, 'fractal2', SEC[1], '**', '*.html'), recursive=True) + [os.path.join(SITE, 'fractal2', SEC[1] + '.html')]:
    h = open(p).read()
    ids = set(re.findall(r'id="([^"]+)"', h))
    for href in re.findall(r'href="([^"]+)"', h):
        if href == '#': continue
        if href.startswith('#'):
            if href[1:] not in ids: bad['%s -> %s' % (os.path.basename(p), href)] += 1
        elif href.startswith('/fractal2/' + SEC[1]):
            path = href.split('#')[0]
            if path not in built: bad[href] += 1
    for src in re.findall(r'(?:src|href)="(https?://[^"]+)"', h):
        if 'noblefathercreations.com' in src or 'google.com/search' in src: continue
        ext[src] += 1
    for u in re.findall(r"src=['\"](https?://[^'\"]+)", h):
        if 'cloudflareinsights' not in u: ext[u] += 1
print('chain pages checked: %d' % n)
print('word, order, heading and safety failures: %d' % len(fails))
for x in fails[:25]: print('  ', x)
print('broken internal links: %d' % sum(bad.values()), list(bad.items())[:8])
print('outside requests other than the beacon: %d' % len(ext), list(ext)[:5])
print('VERIFY ' + ('PASS' if not fails and not bad and not ext else 'FAIL'))
