#!/usr/bin/env python3
"""The Counterfeit — one-page TikTok slides (1080x1920 PNG), one idea per slide, one font (Inter).

Order: series cover -> original vs copy -> the eight steps -> the thirty techniques (3 slides) -> scale
       -> religion cover -> how to read the grades -> 34 religion slides (each shows all 30 techniques, graded)
       -> "everywhere else" cover -> 29 sector slides from The Fractal (the religion/spirituality sector is already in the
       religion set, so it is skipped) -> Mother Earth (last).

Data comes from the repo, not from memory: content/sacred-divide/religions/*.md (grades) and content/prose/fractal.md (sectors).
Usage: counterfeit-slides.py [--only N,M]      Output: exports/counterfeit-slides/NN-slug.png + manifest.json"""
import html, json, os, re, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'exports', 'counterfeit-slides')
FONTS = os.path.join(ROOT, 'tools/fonts/inter/font-files')
RELIG = os.path.join(ROOT, 'content/sacred-divide/religions')
e = lambda t: html.escape(str(t), quote=False)

# ---------------------------------------------------------------------------------------------- text from the owner
PAIRS = [  # the original says / the copy says
    ('you are loved', 'you are loved — when you perform'),
    ('you are safe', 'you are safe — as long as you don’t leave'),
    ('you belong', 'you belong — as long as you comply'),
    ('you are whole', 'you are whole — once you buy what’s missing'),
    ('come home', 'come home — and here’s the mortgage'),
]
STAGES = [  # (step, what was made holy, what the counterfeit does with it)
    ('Idealize', 'You were chosen before you did a thing.', 'It flatters fast, so you will invest.'),
    ('Hook', 'A covenant that holds when you fail.', 'It makes leaving cost more than staying.'),
    ('Devalue', 'Worth that comes pre-installed.', 'It moves your worth into its hands: a grade, a title, a number.'),
    ('Confuse', 'A compass only you can read.', '“Did you really see that? Are you sure that’s what they meant?”'),
    ('Isolate', 'Community: one body, none disposable.', 'It removes the witnesses, so you can’t compare notes.'),
    ('Extract', 'Abundance: a cup that runs over.', 'It takes from your deficit and calls it dues.'),
    ('Discard', '“I will never leave you.”', 'You are dropped the moment you are empty.'),
    ('Replace', 'You are known by name.', 'Your seat is filled before it’s cold. The cycle restarts.'),
]
# canonical technique -> (the gift it inverts, what the counterfeit does). Gifts and glosses are the owner's text;
# Triangulation is not in that text, so its line comes from The Fractal ("Triangulation -> Direct relationship").
INV = {
    'Love Bombing': ('unconditional love', 'warmth poured on fast, so it can be taken away'),
    'Weaponized Generosity': ('generosity', 'gifts that are really debts'),
    'Future Faking': ('promise', 'selling a tomorrow that was never coming'),
    'Hoovering': ('welcome', 'pulling you back the moment you try to get free'),
    'Devaluation': ('worth', 'the self reduced, piece by piece'),
    'Gaslighting': ('knowing', 'the destruction of your ability to know'),
    'Double Bind': ('choice', 'two options, both serving the system'),
    'Intermittent Reinforcement': ('stability', 'hot and cold: rewards you can’t predict, so you can’t let go'),
    'Moving the Goalposts': ('enough', 'a finish line that moves every time you reach it'),
    'Strategic Ambiguity': ('honest words', 'say it vague, so no one can hold you to it'),
    'Projection': ('accountability', 'the guilt handed to the one who was hurt'),
    'DARVO': ('justice', 'deny, attack, reverse victim and offender'),
    'Normalization': ('peace', 'the abnormal made invisible by repetition'),
    'Isolation': ('belonging', 'loneliness manufactured on purpose'),
    'Triangulation': ('direct relationship', 'a third party inserted to set you against a comparison'),
    'Flying Monkeys': ('alliance', 'other people recruited to bring you back in line'),
    'Smear Campaign': ('witness', 'credibility destroyed before the truth can be spoken'),
    'Silent Treatment': ('dialogue', 'communication withdrawn as punishment'),
    'Manufactured Consent': ('truth', 'consent engineered before anyone was asked'),
    'Trauma Bonding': ('attachment', 'the pain-and-relief cycle that feels like loyalty'),
    'Learned Helplessness': ('empowerment', 'a soul trained to believe it can’t act'),
    'Benevolent Control': ('protection', 'control dressed as care'),
    'Infantilization': ('growth', 'keep them dependent'),
    'Identity Erosion': ('wholeness', 'the self erased and replaced with a role'),
    'Spiritual Bypassing': ('transcendence', 'holy words used to dodge accountability'),
    'Financial Control': ('security', 'dependence as leverage'),
    'Manufactured Crisis': ('urgency that wakes us', 'an emergency invented to force compliance'),
    'Discard': ('dignity', 'the soul disposed of when its use is spent'),
    'Replacement': ('continuity', 'the depleted dropped, the seat refilled'),
    'Plausible Deniability': ('transparency', '“I never said that. You’re imagining it.”'),
}
SCALES = [
    ('One person', 'the partner, the parent, the guru'),
    ('A family', 'handed down like a recipe, until nobody remembers who wrote it'),
    ('An institution', 'a school, a church, a hospital, a company: the building runs the cycle'),
    ('A civilization', 'the economy, the media, the law, the algorithm'),
]
GRADES = [  # name, colour, one-line meaning (the book's own definitions, shortened)
    ('Codified', '#E2B84A', 'In writing: policy, rule or contract'),
    ('Documented', '#F4EEDF', 'Court, inquiry, regulator or filing'),
    ('Taught', '#D9694A', 'Leaders say it, with no formal rule'),
    ('Cultural', '#7DB3AD', 'Enforced by community, not by rule'),
    ('Contested', '#A394D6', 'Some parts of it do, others oppose it'),
    ('Reformed', '#78B77C', 'Happened, then materially changed'),
    ('Ungraded', '#8A8174', 'Not yet graded'),
]
GCOL = {g: c for g, c, _ in GRADES}
FAMILY_ORDER = ['Christianity', 'Restorationist & Adventist', 'Judaism', 'Islam', 'Dharmic', 'Buddhism', 'East Asian',
                'Persian-born', 'New movements & the spiritual marketplace', 'Indigenous & folk']
UMBRELLA = {'christianity', 'islam', 'judaism', 'buddhism', 'hinduism'}

# ---------------------------------------------------------------------------------------------- data from the repo
def canon_techniques():
    t = open(os.path.join(RELIG, 'hare-krishna.md'), encoding='utf-8').read()
    out = []
    for n, name in re.findall(r'^#### (\d+) · (.+?)(?: \{#t-\d+\})?$', t, re.M)[:30]:
        out.append(name.split(' / ')[0].strip())
    assert len(out) == 30 and out[0] == 'Love Bombing', out
    return out


def religions(canon):
    rows = []
    for fn in sorted(os.listdir(RELIG)):
        if not fn.endswith('.md') or fn.startswith('_') or fn == 'README.md':
            continue
        t = open(os.path.join(RELIG, fn), encoding='utf-8').read()
        fm = dict(re.findall(r'^(\w+): "?(.+?)"?$', t.split('---')[1], re.M))
        rid = fm['id']; grades = {}
        heads = [(m.start(), int(m.group(1))) for m in re.finditer(r'^#### (\d+) · ', t, re.M)][:30]
        for k, (pos, num) in enumerate(heads):
            end = heads[k + 1][0] if k + 1 < len(heads) else pos + 6000
            g = re.search(r'\*\*Evidence grade\.\*\* \[\[(\w+)\]\]', t[pos:end])
            if g: grades[num] = g.group(1)
        if len(grades) < 30:                                  # table-format volumes: | 12 | DARVO | Documented | ...
            sec = re.search(r'^## 12\..*?(?=^## 13\.)', t, re.S | re.M).group(0)
            for m in re.finditer(r'^\|\s*(\d+)\s*\|[^|]*\|\s*(\w+)(?: \(weak\))?\s*\|', sec, re.M):
                if m.group(2) in GCOL: grades[int(m.group(1))] = m.group(2)
        seq = [grades.get(i, 'Ungraded') for i in range(1, 31)]
        rows.append({'id': rid, 'title': fm['title'], 'family': fm['family'], 'grades': seq})
    rows.sort(key=lambda r: (FAMILY_ORDER.index(r['family']), r['id'] not in UMBRELLA, r['title'].lower()))
    return rows


def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?”"])\s+(?=[A-Z“"])', text) if s.strip()]


def sectors():
    t = open(os.path.join(ROOT, 'content/prose/fractal.md'), encoding='utf-8').read()
    sec = t[t.index('## The thirty sectors'):]
    parts = re.split(r'\n### Sector (\d+): (.+)\n', sec)
    out = []
    for k in range(1, len(parts), 3):
        n, name, body = int(parts[k]), parts[k + 1].strip(), parts[k + 2]
        ctrl = re.search(r'\*Controls: (.+?)\*', body).group(1).strip()
        tech = re.search(r'\*\*Technique: (.+?)\*\* — (.+)', body)
        story = re.sub(r'\s+', ' ', body[body.index(tech.group(0)) + len(tech.group(0)):].split('\n---')[0]).strip()
        ss = sentences(story)
        head, i = [], 0
        while i < len(ss) and len(' '.join(head)) < 330: head.append(ss[i]); i += 1
        while len(' '.join(head)) > 520 and len(head) > 1: head.pop()
        tail = [s for s in ss[i:] if len(s.split()) >= 5 and s[-1] in '.!?”"' and s[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ“"']
        close = tail[-1] if tail else ''
        out.append({'n': n, 'name': name.title().replace('&', '&').replace(' Of ', ' of ').replace(' And ', ' and '),
                    'raw': name, 'controls': ctrl, 'tech': tech.group(1).strip(), 'defn': tech.group(2).strip(),
                    'open': ' '.join(head), 'close': close})
    return out


# ---------------------------------------------------------------------------------------------- slide html
CSS = f"""
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-Regular.woff2'); font-weight: 400; }}
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-Italic.woff2'); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-Medium.woff2'); font-weight: 500; }}
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-SemiBold.woff2'); font-weight: 600; }}
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-Bold.woff2'); font-weight: 700; }}
@font-face {{ font-family: Inter; src: url('file://{FONTS}/Inter-ExtraBold.woff2'); font-weight: 800; }}
:root {{ --bg:#14110F; --text:#F4EEDF; --gold:#E2B84A; --mute:#A39A88; --rule:#3A332B; --s:0.84; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; background: var(--bg); }}
body {{ font-family: Inter, sans-serif; color: var(--text); -webkit-font-smoothing: antialiased; }}
/* safe area: top 150, bottom 360 (app UI), right 130 */
.box {{ position: absolute; left: 90px; top: 150px; width: 860px; height: 1410px; overflow: hidden; display: flex; flex-direction: column; }}
.box.mid {{ justify-content: center; }}
.kick {{ font-size: calc(30px*var(--s)); font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: var(--gold); }}
h1 {{ font-size: calc(104px*var(--s)); line-height: 1.02; font-weight: 800; letter-spacing: -.02em; }}
h2 {{ font-size: calc(76px*var(--s)); line-height: 1.05; font-weight: 800; letter-spacing: -.015em; margin-top: calc(18px*var(--s)); }}
.sub {{ font-size: calc(40px*var(--s)); line-height: 1.3; color: var(--mute); margin-top: calc(26px*var(--s)); font-weight: 500; }}
.rule {{ height: 4px; width: 120px; background: var(--gold); margin: calc(30px*var(--s)) 0; }}
.row {{ border-top: 2px solid var(--rule); padding: calc(20px*var(--s)) 0; }}
.row:first-of-type {{ border-top: 0; }}
.a {{ font-size: calc(32px*var(--s)); color: var(--mute); line-height: 1.25; font-weight: 500; }}
.b {{ font-size: calc(42px*var(--s)); line-height: 1.22; font-weight: 600; margin-top: calc(6px*var(--s)); }}
.b em {{ color: var(--gold); font-style: normal; }}
.num {{ color: var(--gold); font-weight: 800; }}
.fill {{ flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 30px; margin-top: calc(20px*var(--s)); }}
.cell {{ display: flex; align-items: center; gap: calc(14px*var(--s)); height: calc(74px*var(--s)); border-top: 2px solid var(--rule); }}
.dot {{ flex: none; width: calc(26px*var(--s)); height: calc(26px*var(--s)); border-radius: 50%; }}
.nm {{ font-size: calc(34px*var(--s)); line-height: 1.04; font-weight: 600; }}
.n {{ font-size: calc(22px*var(--s)); color: var(--mute); font-weight: 600; width: calc(34px*var(--s)); flex: none; }}
.legend {{ display: flex; flex-wrap: wrap; gap: calc(10px*var(--s)) calc(26px*var(--s)); margin-top: calc(22px*var(--s)); font-size: calc(27px*var(--s)); font-weight: 600; }}
.legend span {{ display: inline-flex; align-items: center; gap: calc(10px*var(--s)); }}
.legend i {{ width: calc(20px*var(--s)); height: calc(20px*var(--s)); border-radius: 50%; display: inline-block; }}
.ctrl {{ font-size: calc(42px*var(--s)); color: var(--gold); font-weight: 600; line-height: 1.2; margin-top: calc(22px*var(--s)); }}
.lab {{ font-size: calc(26px*var(--s)); letter-spacing: .16em; text-transform: uppercase; color: var(--mute); font-weight: 700; }}
.tech {{ font-size: calc(64px*var(--s)); font-weight: 800; line-height: 1.05; margin-top: calc(8px*var(--s)); letter-spacing: -.01em; }}
.defn {{ font-size: calc(40px*var(--s)); line-height: 1.28; font-weight: 500; margin-top: calc(12px*var(--s)); }}
.quote {{ font-size: calc(36px*var(--s)); line-height: 1.42; font-style: italic; color: #E6DECB; margin-top: calc(14px*var(--s)); }}
.big {{ font-size: calc(58px*var(--s)); line-height: 1.18; font-weight: 700; }}
.big em {{ font-style: normal; color: var(--gold); }}
.list p {{ font-size: calc(46px*var(--s)); line-height: 1.22; font-weight: 600; margin-top: calc(22px*var(--s)); }}
.box30 {{ position: absolute; left: 64px; top: 105px; width: 896px; height: 1535px; overflow: hidden; display: flex; flex-direction: column; }}
.r30 {{ display: flex; gap: calc(14px*var(--s)); align-items: flex-start; border-top: 1px solid var(--rule); padding: calc(6px*var(--s)) 0; font-size: calc(22px*var(--s)); line-height: 1.22; }}
.r30 .dot {{ flex: none; border-radius: 50%; margin-top: calc(6px*var(--s)); width: calc(15px*var(--s)); height: calc(15px*var(--s)); }}
.r30 .ix {{ flex: none; width: calc(26px*var(--s)); color: var(--gold); font-weight: 700; font-size: calc(18px*var(--s)); padding-top: calc(3px*var(--s)); }}
.r30 b {{ font-weight: 700; color: var(--text); }} .r30 span.t {{ color: #D9D1BE; }}
.hd {{ margin-bottom: calc(10px*var(--s)); }}
"""


def page(inner, mid=False, cls=''):
    base = '<style>:root{--s:1}</style>' if cls == 'box30' else ''
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{base}<div class="box{" mid" if mid else ""}{" " + cls if cls else ""}">{inner}</div>'


def s_cover():
    return page('<div class="kick">The Sacred Divide · A series</div><h1 style="margin-top:34px">The<br>Counterfeit</h1><div class="rule"></div>'
                '<div class="sub">One pattern. Eight steps. Thirty techniques. Every scale.</div>', mid=True)


def s_pairs():
    rows = ''.join(f'<div class="row"><div class="a">The original says: {e(a)}.</div><div class="b">The copy says: <em>{e(b)}.</em></div></div>' for a, b in PAIRS)
    return page('<div class="kick">The counterfeit</div><h2>Every copy adds one thing the original never had.</h2>'
                f'<div class="fill"><div style="margin-top:26px">{rows}</div><div class="big" style="margin-top:20px"><em>A condition.</em></div></div>')


def s_stages():
    rows = ''.join(f'<div class="row" style="padding:14px 0"><div class="b" style="margin:0;font-size:calc(40px*var(--s))"><span class="num">{i}</span>&nbsp; {e(n)}</div>'
                   f'<div class="a" style="font-size:calc(29px*var(--s))">{e(a)}</div><div class="a" style="color:var(--text);font-size:calc(31px*var(--s))">{e(b)}</div></div>'
                   for i, (n, a, b) in enumerate(STAGES, 1))
    return page(f'<div class="kick">The eight steps</div><div class="sub" style="margin:6px 0 0;font-size:calc(30px*var(--s))">Always in this order. Each is a copy of something made holy.</div><div class="fill" style="margin-top:10px">{rows}</div>')


def s_techniques(part, canon):
    names = canon[part * 15:(part + 1) * 15]
    rows = ''
    for k, nme in enumerate(names):
        gift, gloss = INV[nme]
        gloss += '' if gloss[-1] in '.”' else '.'
        rows += (f'<div class="row" style="padding:12px 0"><div style="font-size:calc(42px*var(--s));font-weight:700;line-height:1.1"><span class="num" style="font-size:calc(24px*var(--s))">{part * 15 + k + 1}</span>&nbsp; {e(nme)}</div>'
                 f'<div class="a" style="font-size:calc(30px*var(--s));margin-top:3px;color:var(--text)"><span style="color:var(--gold);font-weight:600">{e(gift[0].upper() + gift[1:])}, reversed:</span> {e(gloss)}</div></div>')
    return page(f'<div class="kick">Thirty inversions · {part + 1} of 2</div><div class="fill" style="margin-top:6px">{rows}</div>')


def s_scale():
    rows = ''.join(f'<div class="row"><div class="b" style="font-size:calc(64px*var(--s));margin:0">{e(a)}</div><div class="a" style="font-size:calc(38px*var(--s));margin-top:8px">{e(b[0].upper() + b[1:])}.</div></div>' for a, b in SCALES)
    return page('<div class="kick">It does not stop at people</div><h2>The same eight steps, at every magnification.</h2>'
                f'<div class="fill" style="margin-top:20px"><div>{rows}</div><div class="big" style="margin-top:10px">It doesn’t need a villain in a room. <em>It runs itself.</em></div></div>')


def s_cover2(kicker, title, sub):
    return page(f'<div class="kick">{e(kicker)}</div><h1 style="margin-top:34px">{title}</h1><div class="rule"></div><div class="sub">{e(sub)}</div>', mid=True)


def s_grades():
    rows = ''.join(f'<div class="row" style="display:flex;align-items:center;gap:22px;padding:18px 0"><span class="dot" style="background:{c};width:34px;height:34px"></span>'
                   f'<div><div class="b" style="margin:0;font-size:calc(44px*var(--s))">{g}</div><div class="a" style="font-size:calc(30px*var(--s))">{e(m)}</div></div></div>' for g, c, m in GRADES)
    return page('<div class="kick">How to read the next slides</div><h2>Each technique gets a grade: how it is established.</h2>'
                f'<div style="margin-top:18px">{rows}</div><div class="sub" style="font-size:calc(30px*var(--s))">A grade says what kind of source backs it, not how bad it is.</div>')


def s_religion(r, canon, lines):
    from collections import Counter
    rows = ''.join(f'<div class="r30"><span class="dot" style="background:{GCOL[g]}"></span><div><b>{e(canon[i])}.</b> <span class="t">{e(lines[str(i + 1)])}</span></div></div>' for i, g in enumerate(r['grades']))
    c = Counter(r['grades'])
    leg = ''.join(f'<span><i style="background:{GCOL[g]}"></i>{g} {c[g]}</span>' for g, _, _ in GRADES if c.get(g))
    return page(f'<div class="kick" style="font-size:calc(24px*var(--s))">{e(r["family"])}</div><h2 style="font-size:calc(56px*var(--s));margin-top:6px">{e(r["title"])}</h2>'
                f'<div class="a hd" style="font-size:calc(24px*var(--s));margin-top:6px">How each of the 30 techniques shows up here</div>{rows}<div class="legend" style="margin-top:calc(12px*var(--s));font-size:calc(21px*var(--s))">{leg}</div>', cls='box30')


def s_sector30(num, name, controls, canon, lines, k, total):
    rows = ''.join(f'<div class="r30"><span class="ix">{i + 1}</span><div><b>{e(canon[i])}.</b> <span class="t">{e(lines[str(i + 1)])}</span></div></div>' for i in range(30))
    return page(f'<div class="kick" style="font-size:calc(24px*var(--s))">Everywhere else · {k} of {total}</div><h2 style="font-size:calc(56px*var(--s));margin-top:6px">{e(name)}</h2>'
                f'<div class="a hd" style="font-size:calc(25px*var(--s));margin-top:6px;color:var(--gold);font-weight:600">Controls: {e(controls)}</div>{rows}', cls='box30')


def s_sector(s):
    q = f'“{e(s["open"])}”' + (f'<br><br>…“{e(s["close"])}”' if s['close'] else '')
    return page(f'<div class="kick">Everywhere else · {s["n"] - 1} of 29</div><h2 style="font-size:calc(86px*var(--s))">{e(s["name"])}</h2>'
                f'<div class="ctrl" style="font-size:calc(50px*var(--s))">Controls: {e(s["controls"])}</div><div class="rule" style="margin:30px 0 24px"></div>'
                f'<div class="lab" style="font-size:calc(28px*var(--s))">The technique</div><div class="tech" style="font-size:calc(76px*var(--s))">{e(s["tech"])}</div><div class="defn" style="font-size:calc(46px*var(--s))">{e(s["defn"])}</div>'
                f'<div class="quote" style="font-size:calc(40px*var(--s));margin-top:calc(26px*var(--s))">{q}</div>')


def s_earth():
    items = ['Idealized as endless.', 'Hooked into every system we live by.', 'Devalued into a resource.', 'Extracted.', 'Discarded.', 'Replaced with the next place to dig.']
    lst = ''.join(f'<p style="font-size:calc(60px*var(--s));margin-top:calc(26px*var(--s))">{e(x)}</p>' for x in items)
    return page('<div class="kick">The largest body</div><h2 style="font-size:calc(84px*var(--s))">Mother Earth is the last host in the chain.</h2><div class="rule"></div>'
                f'<div class="list">{lst}</div>'
                '<div class="sub" style="color:var(--text);font-size:calc(44px*var(--s));margin-top:calc(44px*var(--s))">She cannot consent. She cannot leave. She has been living the seventh and eighth steps for a very long time.</div>'
                '<div class="quote" style="font-size:calc(34px*var(--s));margin-top:calc(30px*var(--s))">“The body that was here before the first institution was built and will be here after the last institution falls.” — The Fractal</div>')


# ---------------------------------------------------------------------------------------------- build
def load_lines():
    """Slide-ready one-sentence lines (content/counterfeit/lines.json, from counterfeit-lines.py merge). Without it, truncated sources are
    used for layout testing only and the run says so."""
    p = os.path.join(ROOT, 'content/counterfeit/lines.json')
    if os.path.exists(p): return json.load(open(p, encoding='utf-8')), True
    src = json.load(open(os.path.join(ROOT, 'content/counterfeit/sources.json'), encoding='utf-8'))
    cut = lambda t: t if len(t) <= 95 else t[:92].rsplit(' ', 1)[0] + '.'
    return {'religions': {r: {n: cut(t) for n, t in d.items()} for r, d in src['religions'].items()},
            'fractal': {k: {n: cut(t) for n, t in v['src'].items()} for k, v in src['fractal'].items()}}, False


def fractal_sectors():
    import importlib.util
    spec = importlib.util.spec_from_file_location('cl', os.path.join(ROOT, 'scripts/counterfeit-lines.py')); cl = importlib.util.module_from_spec(spec); spec.loader.exec_module(cl)
    return [x for x in cl.fractal_blob()['sectors'] if x['num'] != 1]


def build_slides():
    canon = canon_techniques(); rel = religions(canon); story = {x['n']: x for x in sectors()}; fsec = fractal_sectors()
    lines, ready = load_lines()
    assert len(rel) == 34 and len(fsec) == 29, (len(rel), len(fsec))
    L = [('cover', 'Series cover', s_cover()), ('pairs', 'Original vs copy', s_pairs()), ('stages', 'The eight steps', s_stages())]
    L += [(f'techniques-{i + 1}', f'Thirty techniques {i + 1}/2', s_techniques(i, canon)) for i in range(2)]
    L += [('scale', 'It does not stop at people', s_scale()),
          ('religion-cover', 'Religion cover', s_cover2('Part one', 'Religion', 'The same thirty techniques, graded in 34 traditions.')),
          ('grades', 'How to read the grades', s_grades())]
    L += [(f'religion-{r["id"]}', r['title'], s_religion(r, canon, lines['religions'][r['id']])) for r in rel]
    L += [('elsewhere-cover', 'Everywhere else cover', s_cover2('Part two', 'Everywhere<br>else', 'The same cycle, in 29 more places you live.'))]
    for k, x in enumerate(fsec, 1):
        slug = f'sector-{x["num"]:02d}-{re.sub("[^a-z]+", "-", x["short"].lower()).strip("-")}'
        if x['techs']: L.append((slug, x['short'], s_sector30(x['num'], x['short'], x['controls'], canon, lines['fractal'][str(x['num'])], k, 29)))
        else: L.append((slug, x['short'] + ' (story)', s_sector(story[x['num']])))   # the book has no technique-by-technique examples for this sector
    L += [('mother-earth', 'Mother Earth', s_earth())]
    print('lines slide-ready:' , ready)
    return L


FIT = """() => { const b = document.querySelector('.box'); let s = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--s')), n = 0;
  while (b.scrollHeight > b.clientHeight + 1 && s > 0.5 && n < 60) { s -= 0.02; document.documentElement.style.setProperty('--s', s.toFixed(2)); n++; }
  return s; }"""


def main():
    only = None
    if '--only' in sys.argv: only = {int(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')}
    L = build_slides(); os.makedirs(OUT, exist_ok=True); man = []
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
        pg = br.new_page(viewport={'width': 1080, 'height': 1920})
        for i, (slug, title, h) in enumerate(L, 1):
            fn = f'{i:02d}-{slug}.png'
            if only is None or i in only:
                pg.set_content(h, wait_until='load'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(60)
                s = pg.evaluate(FIT); pg.screenshot(path=os.path.join(OUT, fn))
            else: s = None
            man.append({'n': i, 'file': fn, 'title': title, 'scale': s})
        br.close()
    json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    small = [m for m in man if m['scale'] is not None and m['scale'] < 0.8]
    print(len(man), 'slides;', 'shrunk below 80%:', [(m['n'], m['scale']) for m in small] or 'none')


if __name__ == '__main__':
    main()
