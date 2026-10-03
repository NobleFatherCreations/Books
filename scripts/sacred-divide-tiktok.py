#!/usr/bin/env python3
"""Sacred Divide — TikTok photo carousels (1080x1920 PNG slides) for one volume.
Usage: sacred-divide-tiktok.py protestant-evangelical
Reads content/sacred-divide/tiktok/<id>.json ({"posts": [{"id","title","slides":[...]}]}), written by
scripts/sacred-divide-tiktok-build.py from the volume's own text. TikTok allows up to 35 images per photo post,
so the series is split into posts. Text auto-fits: each slide is zoomed down until it clears the bottom safe area.
Safe area: top 160 px, bottom 400 px and right 140 px are left clear of the app's interface."""
import html, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'tools/pdf/fonts/v5')
rid = sys.argv[1]
DATA = json.load(open(os.path.join(ROOT, 'content/sacred-divide/tiktok', rid + '.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'exports', 'tiktok-' + rid)
e = lambda t: html.escape(str(t), quote=False)
SAFE_BOTTOM = 1520
MIN_ZOOM = 0.62

CSS = f"""
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Regular.ttf'); font-weight: 400; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Italic.ttf'); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-SemiBold.ttf'); font-weight: 600; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Bold.ttf'); font-weight: 700; }}
:root {{ --ink:#1A1714; --ox:#7B1E22; --gold:#B08A42; --cream:#FAF6EC; --rule:#D8D0BC; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; background: var(--ink); }}
body {{ font-family: EBG, serif; color: var(--cream); position: relative; overflow: hidden; }}
.slide {{ position: absolute; inset: 0; padding: 170px 150px 400px 100px; background: var(--ink); color: var(--cream); }}
.slide.light {{ background: var(--cream); color: var(--ink); }}
.slide.red {{ background: var(--ox); }}
.band {{ position: absolute; left: 0; right: 0; top: 0; height: 22px; background: var(--ox); }}
.red .band {{ background: var(--gold); }}
.count {{ position: absolute; top: 150px; right: 150px; font-weight: 700; font-size: 34px; letter-spacing: .18em; color: var(--rule); }} .light .count {{ color: #6b6254; }}
.fit {{ width: 830px; }}
.kicker {{ font-weight: 700; font-size: 34px; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: 40px; max-width: 640px; line-height: 1.25; }}
.light .kicker {{ color: var(--ox); }} .red .kicker {{ color: var(--rule); }}
h1 {{ font-weight: 400; font-size: 156px; line-height: 1.02; letter-spacing: -.02em; }}
h2 {{ font-weight: 400; font-size: 100px; line-height: 1.06; letter-spacing: -.015em; }}
h3 {{ font-weight: 600; font-size: 66px; line-height: 1.1; }}
.big {{ font-weight: 400; font-size: 300px; line-height: .95; color: var(--gold); letter-spacing: -.03em; }} .light .big {{ color: var(--ox); }}
p {{ font-size: 56px; line-height: 1.28; margin-top: 36px; }}
p.sm {{ font-size: 44px; color: var(--rule); }} .light p.sm {{ color: #5a5246; }}
p.def {{ font-style: italic; color: var(--gold); font-size: 54px; margin-top: 26px; }} .light p.def {{ color: var(--ox); }}
em {{ color: var(--gold); font-style: italic; }} .light em {{ color: var(--ox); }}
.num {{ font-size: 190px; line-height: .9; color: var(--gold); letter-spacing: -.03em; }} .light .num {{ color: var(--ox); }}
ul.b {{ list-style: none; margin-top: 34px; }} ul.b li {{ position: relative; padding: 0 0 0 40px; margin-bottom: 26px; font-size: 52px; line-height: 1.24; }}
ul.b li::before {{ content: ''; position: absolute; left: 0; top: 24px; width: 16px; height: 16px; background: var(--gold); }} .light ul.b li::before {{ background: var(--ox); }}
ol.s {{ list-style: none; counter-reset: n; margin-top: 34px; }} ol.s li {{ counter-increment: n; position: relative; padding: 0 0 0 78px; margin-bottom: 26px; font-size: 52px; line-height: 1.24; }}
ol.s li::before {{ content: counter(n); position: absolute; left: 0; top: 4px; width: 52px; height: 52px; border: 3px solid var(--gold); color: var(--gold); font-weight: 700; font-size: 34px; line-height: 46px; text-align: center; }}
.light ol.s li::before {{ border-color: var(--ox); color: var(--ox); }}
.chain {{ margin-top: 50px; }} .chain div {{ border-top: 3px solid var(--gold); padding: 34px 0; font-size: 74px; line-height: 1.12; }}
.chain div small {{ display: block; font-size: 48px; color: var(--rule); margin-top: 8px; }}
.bars {{ margin-top: 40px; display: flex; flex-direction: column; gap: 34px; }}
.bar {{ display: grid; grid-template-columns: 190px 1fr; align-items: center; gap: 24px; font-size: 56px; }} .bar > span:last-child {{ display: flex; align-items: center; }}
.bar .t {{ height: 84px; background: var(--gold); display: block; }} .bar .t.last {{ background: var(--ox); }} .bar b {{ font-weight: 700; font-size: 54px; margin-left: 16px; }}
.rows {{ margin-top: 36px; }} .rows div {{ border-top: 3px solid var(--ink); padding: 28px 0; font-size: 54px; line-height: 1.2; }}
.rows div b {{ color: var(--ox); font-weight: 700; }} .dark .rows div, .red .rows div {{ border-top-color: var(--gold); }} .dark .rows div b {{ color: var(--gold); }} .red .rows div b {{ color: var(--cream); }}
.chip {{ display: inline-block; font-weight: 700; font-size: 40px; letter-spacing: .14em; text-transform: uppercase; border: 4px solid var(--gold); color: var(--gold); padding: 6px 22px; margin-top: 30px; }}
.chip.documented {{ background: var(--gold); color: var(--ink); }} .chip.cultural {{ border-color: var(--rule); color: var(--rule); }}
.light .chip {{ border-color: var(--ox); color: var(--ox); }} .light .chip.documented {{ background: var(--ox); color: var(--cream); }} .light .chip.cultural {{ border-color: #6b6254; color: #6b6254; }}
.lab {{ font-weight: 700; font-size: 36px; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); margin-top: 44px; }}
.light .lab {{ color: var(--ox); }}
.help div {{ border-top: 3px solid var(--gold); padding: 28px 0; font-size: 52px; line-height: 1.18; }} .help div b {{ display: block; font-size: 66px; font-weight: 700; color: var(--cream); }}
.spacer {{ height: 380px; }}
"""

def lab(x): return x if x[-1:] in '.:?!)"' else x + '.'

def body(s):
    t = s['type']; k = f"<div class=kicker>{e(s['kicker'])}</div>" if s.get('kicker') else ''
    note = f"<p class=sm>{e(s['note'])}</p>" if s.get('note') else ''
    if t == 'cover':
        return f"<div class=kicker>The Sacred Divide · {e(s['series'])}</div><h1>{e(s['title'])}</h1><p class=sm style='margin-top:60px'>{e(s['sub'])}</p><div class=spacer></div><p><em>{e(s['hook'])}</em></p>"
    if t == 'big':
        return f"{k}<div class=big>{e(s['big'])}</div><h2 style='margin-top:30px'>{e(s['head'])}</h2><p>{e(s['text'])}</p>{note}"
    if t == 'chain':
        return f"{k}<h2>{e(s['head'])}</h2><div class=chain>" + ''.join(f"<div>{e(r[0])}<small>{e(r[1])}</small></div>" for r in s['rows']) + '</div>'
    if t == 'quote':
        return f"{k}<h2 style='font-size:84px'>{e(s['quote'])}</h2>{note}"
    if t == 'bars':
        mx = max(b[1] for b in s['bars'])
        bars = ''.join(f"<div class=bar><span>{e(b[0])}</span><span><span class='t{' last' if j == len(s['bars']) - 1 else ''}' style='width:{b[1] / mx * 470:.0f}px'></span><b>{e(b[2])}</b></span></div>" for j, b in enumerate(s['bars']))
        return f"{k}<h2>{e(s['head'])}</h2><div class=bars>{bars}</div><p>{e(s['text'])}</p>"
    if t == 'rows':
        return f"{k}<h2>{e(s['head'])}</h2><div class=rows>" + ''.join(f"<div><b>{e(lab(r[0]))}</b> {e(r[1])}</div>" for r in s['rows']) + f"</div>{note}"
    if t == 'bullets':
        return f"{k}<h2>{e(s['head'])}</h2>" + (f"<p>{e(s['intro'])}</p>" if s.get('intro') else '') + '<ul class=b>' + ''.join(f'<li>{e(i)}</li>' for i in s['items']) + f'</ul>{note}'
    if t == 'steps':
        return f"{k}<h2>{e(s['head'])}</h2>" + (f"<p>{e(s['intro'])}</p>" if s.get('intro') else '') + '<ol class=s>' + ''.join(f'<li>{e(i)}</li>' for i in s['items']) + f'</ol>{note}'
    if t == 'text':
        return f"{k}<h2>{e(s['head'])}</h2>" + ''.join(f'<p>{e(x)}</p>' for x in s['paras']) + note
    if t == 'tech_a':
        return f"{k}<div class=num>{e(s['num'])}</div><h3 style='margin-top:14px'>{e(s['name'])}</h3><p class=def>{e(s['defn'])}</p><div class=lab>How it shows here</div><ul class=b style='margin-top:20px'>" + ''.join(f'<li>{e(i)}</li>' for i in s['items']) + '</ul>'
    if t == 'tech_b':
        parts = s.get('parts', ['defense', 'counter', 'grade']); h = f"{k}<h3>{e(s['num'])} · {e(s['name'])}{' (cont.)' if parts[0] == 'grade' else ''}</h3>"
        if 'defense' in parts: h += f"<div class=lab>The strongest defense</div><p style='margin-top:14px'>{e(s['defense'])}</p>"
        if 'counter' in parts: h += f"<div class=lab>The counter</div><p style='margin-top:14px'>{e(s['counter'])}</p>"
        if 'grade' in parts: h += f"<div class=lab>Evidence grade</div><span class='chip {s['grade'].lower()}'>{e(s['grade'])}</span><p class=sm style='margin-top:20px'>{e(s['why'])}</p>"
        return h
    if t == 'help':
        return f"{k}<h2>{e(s['head'])}</h2><div class=help style='margin-top:36px'>" + ''.join(f"<div><b>{e(r[0])}</b>{e(r[1])}</div>" for r in s['rows']) + f"</div>{note}"
    raise SystemExit('unknown slide type ' + t)

def page(s, i, n):
    return f"<!doctype html><meta charset=utf-8><style>{CSS}</style><div class='slide {s.get('style', 'dark')}'><div class=band></div><div class=count>{i} / {n}</div><div class=fit>{body(s)}</div></div>"

FIT = """() => { const f = document.querySelector('.fit'); let z = 1; f.style.zoom = z;
  const bottom = () => f.getBoundingClientRect().bottom;
  while (bottom() > %d && z > 0.45) { z = Math.round((z - 0.02) * 100) / 100; f.style.zoom = z; }
  return [z, bottom()]; }""" % SAFE_BOTTOM

import re as _re
THRESH = 0.75
def halves(xs):
    m = (len(xs) + 1) // 2
    return xs[:m], xs[m:]
def base_head(h): return _re.sub(r' \((?:\d of \d|cont\.)\)$', '', h)
def split(s):
    t = s['type']
    if t in ('bullets', 'steps') and len(s['items']) > 1:
        a, b = halves(s['items'])
        return [dict(s, items=a, note=None), dict(s, items=b, intro=None, head=base_head(s['head']) + ' (cont.)')]
    if t == 'rows' and len(s['rows']) > 1:
        a, b = halves(s['rows'])
        return [dict(s, rows=a, note=None), dict(s, rows=b, head=base_head(s['head']) + ' (cont.)')]
    if t == 'text':
        ps = s['paras']
        if len(ps) == 1:
            sents = _re.split(r'(?<=[.!?]) ', ps[0])
            if len(sents) < 2: return [s]
            ps = [' '.join(sents[:(len(sents) + 1) // 2]), ' '.join(sents[(len(sents) + 1) // 2:])]
        a, b = halves(ps)
        return [dict(s, paras=a, note=None), dict(s, paras=b, head=base_head(s['head']) + ' (cont.)')]
    if t == 'tech_a' and len(s['items']) > 1:
        a, b = halves(s['items'])
        return [dict(s, items=a), {'type': 'bullets', 'style': s['style'], 'kicker': s['kicker'], 'head': f"{s['num']} · {s['name']} (cont.)", 'items': b}]
    if t == 'tech_b' and s.get('parts', ['defense', 'counter', 'grade']) == ['defense', 'counter', 'grade']:
        return [dict(s, parts=['defense', 'counter']), dict(s, parts=['grade'])]
    if t == 'tech_b' and s.get('parts') == ['defense', 'counter']:
        return [dict(s, parts=['defense']), dict(s, parts=['counter'])]
    return [s]

total = 0; warn = []
os.makedirs(OUT, exist_ok=True)
for fn in os.listdir(OUT):
    pth = os.path.join(OUT, fn)
    if os.path.isfile(pth) and fn.endswith(('.png', '.html')): os.remove(pth)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    def measure(sl):
        open('/tmp/_fit.html', 'w', encoding='utf-8').write(page(sl, 1, 1))
        pg.goto('file:///tmp/_fit.html'); pg.wait_for_timeout(60)
        return pg.evaluate(FIT)[0]
    def fit_all(slides):
        out = []
        for sl in slides:
            if measure(sl) >= THRESH: out.append(sl); continue
            parts = split(sl)
            out += fit_all(parts) if len(parts) > 1 else parts
        return out
    posts = []
    for post in DATA['posts']:
        sl = fit_all(post['slides'])
        # keep every post at 35 images or fewer
        while len(sl) > 35:
            cut = len(sl) // 2
            while sl[cut]['type'] not in ('tech_a', 'rows', 'bullets', 'steps', 'text') or sl[cut].get('head', '').endswith('(cont.)') or sl[cut]['type'] == 'tech_b': cut += 1
            first = dict(post, slides=sl[:cut], id=post['id'] + '-a'); posts.append(first)
            sl = [dict(sl[0], series=sl[0].get('series', '') + ' · continued')] + sl[cut:]; post = dict(post, id=post['id'] + '-b')
        posts.append(dict(post, slides=sl))
    for post in posts:
        d = os.path.join(OUT, post['id']); os.makedirs(d, exist_ok=True)
        for fn in os.listdir(d): os.remove(os.path.join(d, fn))
        n = len(post['slides'])
        assert n <= 35, f"{post['id']} has {n} slides; TikTok allows 35"
        for i, s in enumerate(post['slides'], 1):
            hp = os.path.join(d, f'slide-{i:02d}.html'); open(hp, 'w', encoding='utf-8').write(page(s, i, n))
            pg.goto('file://' + hp); pg.wait_for_timeout(120)
            z, bot = pg.evaluate(FIT)
            pg.screenshot(path=os.path.join(d, f'slide-{i:02d}.png')); os.remove(hp)
            if z < THRESH: warn.append((post['id'], i, z))
            total += 1
        print(f"{post['id']}: {n} slides", flush=True)
    json.dump({'posts': posts}, open(os.path.join(OUT, 'series.json'), 'w'), indent=1, ensure_ascii=False)
    b.close()
print('total slides:', total)
print('slides shrunk below %.2f (consider splitting):' % MIN_ZOOM, warn or 'none')
