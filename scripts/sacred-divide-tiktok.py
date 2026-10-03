#!/usr/bin/env python3
"""Sacred Divide — TikTok photo-carousel (1080x1920 PNG slides) for one volume.
Usage: sacred-divide-tiktok.py protestant-evangelical
Slides are plain HTML rendered by Chromium; every figure is copied from the volume's own text
(content/sacred-divide/religions/<id>.md after edits). Content stays inside TikTok's safe area
(top 160 px, bottom 400 px and right 140 px are left clear for the app's interface)."""
import html, json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, 'tools/pdf/fonts/v5')
rid = sys.argv[1]
SLIDES = json.load(open(os.path.join(ROOT, 'content/sacred-divide/tiktok', rid + '.json'), encoding='utf-8'))
OUT = os.path.join(ROOT, 'exports', 'tiktok-' + rid)
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(('.png', '.html')): os.remove(os.path.join(OUT, f))
e = html.escape

CSS = f"""
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Regular.ttf'); font-weight: 400; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Italic.ttf'); font-weight: 400; font-style: italic; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-SemiBold.ttf'); font-weight: 600; }}
@font-face {{ font-family: EBG; src: url('file://{FONTS}/EBGaramond-Bold.ttf'); font-weight: 700; }}
:root {{ --ink:#1A1714; --ox:#7B1E22; --gold:#B08A42; --cream:#FAF6EC; --rule:#D8D0BC; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1920px; background: var(--ink); }}
body {{ font-family: EBG, serif; color: var(--cream); position: relative; overflow: hidden; }}
.slide {{ position: absolute; inset: 0; padding: 170px 150px 400px 100px; display: flex; flex-direction: column; }}
.slide.light {{ background: var(--cream); color: var(--ink); }}
.slide.red {{ background: var(--ox); }}
.band {{ position: absolute; left: 0; right: 0; top: 0; height: 22px; background: var(--ox); }}
.light .band {{ background: var(--ox); }} .red .band {{ background: var(--gold); }}
.kicker {{ font-weight: 700; font-size: 34px; letter-spacing: .22em; text-transform: uppercase; color: var(--gold); margin-bottom: 44px; max-width: 660px; }}
.light .kicker {{ color: var(--ox); }} .red .kicker {{ color: var(--rule); }}
h1 {{ font-weight: 400; font-size: 156px; line-height: 1.02; letter-spacing: -.02em; }}
h2 {{ font-weight: 400; font-size: 112px; line-height: 1.06; letter-spacing: -.015em; }}
.big {{ font-weight: 400; font-size: 300px; line-height: .95; color: var(--gold); letter-spacing: -.03em; }}
.light .big {{ color: var(--ox); }}
p {{ font-size: 60px; line-height: 1.28; margin-top: 40px; }}
p.sm {{ font-size: 46px; color: var(--rule); }} .light p.sm {{ color: #5a5246; }}
em {{ color: var(--gold); font-style: italic; }} .light em {{ color: var(--ox); }}
.chain {{ margin-top: 54px; display: flex; flex-direction: column; gap: 0; }}
.chain div {{ border-top: 3px solid var(--gold); padding: 34px 0 34px; font-size: 74px; line-height: 1.12; }}
.chain div small {{ display: block; font-size: 48px; color: var(--rule); margin-top: 8px; }}
.bars {{ margin-top: 40px; display: flex; flex-direction: column; gap: 34px; }}
.bar {{ display: grid; grid-template-columns: 190px 1fr; align-items: center; gap: 24px; font-size: 56px; }} .bar > span:last-child {{ display: flex; align-items: center; }}
.bar span.t {{ height: 84px; background: var(--gold); display: block; }} .bar span.t.last {{ background: var(--ox); }}
.bar b {{ font-weight: 700; font-size: 54px; margin-left: 16px; }}
.rows {{ margin-top: 40px; }} .rows div {{ border-top: 3px solid var(--ink); padding: 30px 0; font-size: 58px; line-height: 1.2; }}
.rows div b {{ color: var(--ox); font-weight: 700; }}
.dark .rows div {{ border-top-color: var(--gold); }} .dark .rows div b {{ color: var(--gold); }}
.compact .rows div {{ padding: 16px 0; font-size: 50px; }} .compact p.sm {{ font-size: 40px; margin-top: 24px; }}
.help div {{ border-top: 3px solid var(--gold); padding: 30px 0; font-size: 52px; line-height: 1.18; }}
.help div b {{ display: block; font-size: 66px; font-weight: 700; color: var(--cream); }}
.count {{ position: absolute; top: 150px; right: 150px; font-weight: 700; font-size: 34px; letter-spacing: .18em; color: var(--rule); }} .light .count {{ color: #6b6254; }}
.spacer {{ flex: 1; }}
"""

def slide_html(s, i, n):
    kind = s.get('style', 'dark') + (' compact' if s.get('compact') else '')
    body = ''
    if s['type'] == 'cover':
        body = f"<div class=kicker>The Sacred Divide · The full record</div><h1>{s['title']}</h1><p class=sm style='margin-top:60px'>{s['sub']}</p><div class=spacer></div><p><em>{s['hook']}</em></p>"
    elif s['type'] == 'big':
        body = f"<div class=kicker>{s['kicker']}</div><div class=big>{s['big']}</div><h2 style='margin-top:30px'>{s['head']}</h2><p>{s['text']}</p>" + (f"<p class=sm>{s['note']}</p>" if s.get('note') else '')
    elif s['type'] == 'chain':
        rows = ''.join(f"<div>{r[0]}<small>{r[1]}</small></div>" for r in s['rows'])
        body = f"<div class=kicker>{s['kicker']}</div><h2>{s['head']}</h2><div class=chain>{rows}</div>" + (f"<p>{s['text']}</p>" if s.get('text') else '')
    elif s['type'] == 'bars':
        mx = max(b[1] for b in s['bars'])
        bars = ''.join(f"<div class=bar><span>{b[0]}</span><span><span class='t{' last' if j == len(s['bars']) - 1 else ''}' style='width:{b[1] / mx * 470:.0f}px'></span><b>{b[2]}</b></span></div>" for j, b in enumerate(s['bars']))
        body = f"<div class=kicker>{s['kicker']}</div><h2>{s['head']}</h2><div class=bars>{bars}</div><p>{s['text']}</p>"
    elif s['type'] == 'rows':
        rows = ''.join(f"<div><b>{r[0]}</b> {r[1]}</div>" for r in s['rows'])
        body = f"<div class=kicker>{s['kicker']}</div><h2>{s['head']}</h2><div class=rows>{rows}</div>" + (f"<p class=sm>{s['note']}</p>" if s.get('note') else '')
    elif s['type'] == 'quote':
        body = f"<div class=kicker>{s['kicker']}</div><h2 style='font-size:84px'>{s['quote']}</h2><p class=sm>{s['note']}</p>"
    elif s['type'] == 'help':
        rows = ''.join(f"<div><b>{r[0]}</b>{r[1]}</div>" for r in s['rows'])
        body = f"<div class=kicker>{s['kicker']}</div><h2>{s['head']}</h2><div class=help style='margin-top:40px'>{rows}</div><p class=sm>{s['note']}</p>"
    return f"<!doctype html><meta charset=utf-8><title>{rid} {i}</title><style>{CSS}</style><div class='slide {kind}'><div class=band></div><div class=count>{i} / {n}</div>{body}</div>"

n = len(SLIDES)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    for i, s in enumerate(SLIDES, 1):
        h = slide_html(s, i, n)
        path = os.path.join(OUT, f'slide-{i:02d}.html'); open(path, 'w', encoding='utf-8').write(h)
        pg.goto('file://' + path); pg.wait_for_timeout(300)
        over = pg.evaluate("""() => { const s=document.querySelector('.slide'); const k=[...s.children].map(c=>c.getBoundingClientRect().bottom); return [Math.max(...k), s.scrollHeight] }""")
        pg.screenshot(path=os.path.join(OUT, f'slide-{i:02d}.png'))
        flag = ' <-- OVERFLOWS safe area' if over[0] > 1920 - 400 + 20 else ''
        print(f'slide {i:02d}: content bottom {over[0]:.0f}px (safe limit 1520){flag}')
    b.close()
