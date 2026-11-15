#!/usr/bin/env python3
"""Fractal² film: build. python3 design/fractal2/film/build.py [--words words.json]
Reads content/fractal2/intro-v15.md, lays out caption times (placeholder clock, or a word-level timestamp JSON),
builds the MSDF font data, and writes library/fractal2/site/fractal2/film.html (served locally at /fractal2/film)."""
import os, re, json, html, sys, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
SITE = os.path.join(ROOT, 'library/fractal2/site/fractal2')
OUT = os.path.join(SITE, 'film.html')
A = '/fractal2/_a/'
BAR = 1.6
# section start times in bars (150 BPM), from content/fractal2/SUNO-VOCAL-SPEC.md
SEC_BAR = {1: 0, 2: 40, 3: 72, 4: 112, 5: 136, 6: 168, 7: 248, 8: 280, 9: 328, 10: 352, 11: 384}
END_BAR = 480
# caption pins: slug -> absolute time of the caption start (anchors), and extra silence before a caption (seconds)
PIN = {'it-started-with-a': 4.4}
PRE = {'why-do-i-keep': 1.6, 'it-must-be-me': 1.4, 'what-if-it-isnt': 2.2, 'so-i-did-the': 1.0, 'it-came-in-eight': .6, 'idealize': 1.2,
       'thirty-techniques-carried-a': 1.6, 'i-thought-i-had': 6.0, 'i-had-found-one': 1.2}
BIG = {'why-do-i-keep', 'what-if-it-isnt', 'it-must-be-me', 'i-am-still-looking', 'i-went-down', 'my-original-frequency', 'that-is-the-fractal', 'now-the-map-is'}
TAIL = {2: 3.5, 3: 2.0}                         # seconds kept clear at the end of a section for picture alone
SPLIT = {'idealize-hook-devalue-confuse'}       # one caption per word

def slug(t):
    w = re.sub(r"[^a-z0-9 ]", '', t.lower().replace("'", '').replace('’', '')).split()
    return '-'.join(w[:4])

def groups(t):
    """phrase groups of about three words, breaking after punctuation where possible"""
    w = t.split(); out = []; cur = []
    for i, x in enumerate(w):
        cur.append(x)
        left = len(w) - i - 1
        if (len(cur) >= 3 and (x[-1] in '.,?!:;' or len(cur) >= 4) and left != 1) or left == 0:
            out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def parse():
    md = open(os.path.join(ROOT, 'content/fractal2/intro-v15.md'), encoding='utf-8').read().split('\n---\n')[1]
    caps = []; sec = 0; titles = {}
    for line in md.split('\n'):
        line = line.strip()
        m = re.match(r'## (\d+)\. (.+)', line)
        if m: sec = int(m.group(1)); titles[sec] = m.group(2); continue
        if not line or line.startswith('[SCREEN') or line.startswith('#'): continue
        locked = line.startswith('[LOCKED]')
        text = re.sub(r'\s*\[(OWNER|LOCKED)[^\]]*\]\s*', ' ', line).strip()
        text = text.replace('"', '“', 1).replace('"', '”', 1) if text.count('"') == 2 else text
        text = text.replace("'", '’')
        s = slug(text)
        if s in SPLIT:
            for w in text.split(): caps.append({'text': w, 'sec': sec, 'slug': slug(w), 'big': True, 'locked': False, 'one': True})
        else:
            caps.append({'text': text, 'sec': sec, 'slug': s, 'big': s in BIG, 'locked': locked})
    return caps, titles

def layout(caps):
    """placeholder clock: about two words a second plus a breath; each section is fitted to its bars"""
    secs = sorted({c['sec'] for c in caps})
    for sec in secs:
        cs = [c for c in caps if c['sec'] == sec]
        start = SEC_BAR[sec] * BAR; end = SEC_BAR.get(sec + 1, END_BAR - 8) * BAR
        first = PIN.get(cs[0]['slug'], 0) if sec == 1 else .5
        room = end - start - first - TAIL.get(sec, 1.5)
        def run(f):
            t = 0
            for i, c in enumerate(cs):
                n = len(c['text'].split())
                t += PRE.get(c['slug'], 0) * f if i else 0
                say = 1.25 if c.get('one') else max(1.2, n / 2.1 + .3)
                c['_o'] = t; c['_say'] = say if c.get('one') else say * max(f, .8)
                t += (say + .2) if c.get('one') else max(.35 * n + 1.2 + .2, (say + .7 + min(1.0, n * .035)) * f)
            return t
        lo, hi = .4, 1.0
        if run(1.0) > room:
            for _ in range(30):
                mid = (lo + hi) / 2
                if run(mid) > room: hi = mid
                else: lo = mid
            f = lo
        else: f = 1.0
        run(f)
        for c in cs: c['t0'] = round(start + first + c['_o'], 3); c['say'] = round(c['_say'], 3)
        cs[0]['_f'] = f
    for i, c in enumerate(caps):
        nxt = caps[i + 1]['t0'] if i + 1 < len(caps) else c['t0'] + c['say'] + 3
        n = len(c['text'].split())
        need = .35 * n + 1.2                               # blueprint rule: minimum time on screen
        c['out'] = .3 if c.get('one') else .6
        c['t1'] = round(nxt - .1 if c.get('one') else min(nxt - .12, max(c['t0'] + c['say'] + 2.2, c['t0'] + need + .4)), 3)
        c['need'] = round(need, 2)
    return caps

def font():
    """MSDF atlas of the caption serif, built once and cached in the site assets"""
    dst = os.path.join(SITE, '_a/film'); os.makedirs(dst, exist_ok=True)
    png = os.path.join(dst, 'voice-msdf.png'); js = os.path.join(HERE, 'voice-msdf.json')
    if not (os.path.exists(png) and os.path.exists(js)):
        tmp = os.environ.get('MSDF_DIR')
        if not tmp: raise SystemExit('font atlas missing: run with MSDF_DIR=<dir with msdf-bmfont-xml installed>')
        cs = ''.join(chr(i) for i in range(32, 127)) + '²·’‘“”…—–éā'
        open(os.path.join(tmp, 'cs.txt'), 'w', encoding='utf-8').write(cs)
        shutil.copy(os.path.join(SITE, '_a/v9/instrument.ttf'), os.path.join(tmp, 'voice.ttf'))
        subprocess.check_call(['npx', 'msdf-bmfont', '-f', 'json', '-o', 'voice', '-i', 'cs.txt', '-s', '72', '-r', '10', '-t', 'msdf', '-m', '1024,1024', '-p', '2', 'voice.ttf'], cwd=tmp)
        shutil.copy(os.path.join(tmp, 'voice.png'), png)
        j = json.load(open(os.path.join(tmp, 'voice.json')))
        ids = {c['id'] for c in j['chars']}
        compact = {'size': j['info']['size'], 'base': j['common']['base'], 'w': j['common']['scaleW'], 'h': j['common']['scaleH'], 'range': j['distanceField']['distanceRange'],
                   'c': {str(c['id']): [c['x'], c['y'], c['width'], c['height'], c['xoffset'], c['yoffset'], c['xadvance']] for c in j['chars']},
                   'k': {'%d,%d' % (k['first'], k['second']): k['amount'] for k in j.get('kernings', []) if k['first'] in ids and k['second'] in ids and k['first'] < 256 and k['second'] < 256 and abs(k['amount']) >= 1}}
        json.dump(compact, open(js, 'w'), separators=(',', ':'))
    return json.load(open(js))

def main():
    caps, titles = parse(); layout(caps)
    dur = END_BAR * BAR
    chapters = [{'n': n, 'title': titles[n], 't': next(c['t0'] for c in caps if c['sec'] == n) - (.0 if n > 1 else 4.4)} for n in sorted(titles)]
    data = {
        'dur': dur, 'bar': BAR,
        'caps': [{'t0': c['t0'], 't1': c['t1'], 'say': c['say'], 'out': c['out'], 'g': [html.escape(g, quote=False) for g in groups(c['text'])], 'big': c['big'], 'locked': c['locked'], 'sec': c['sec'], 'n': len(c['text'].split()), 'need': c['need'], 'slug': c['slug']} for c in caps],
        'capId': {}, 'chapters': chapters,
        'assets': {'orig': [A + 'v8/img/orig.webp', A + 'v8/img/orig-m.webp'], 'core': [A + 'v8/img/orig-core.webp', A + 'v8/img/orig-core-m.webp'],
                   'logo': [A + 'v8/img/logo.webp', A + 'v8/img/logo-m.webp'], 'emb': [A + 'v8/img/emblem.webp', A + 'v8/img/emblem-m.webp'], 'font': [A + 'film/voice-msdf.png']},
        'first': ['font', 'logo', 'orig', 'core'], 'later': ['emb'], 'audio': None, 'font': font(),
    }
    for i, c in enumerate(data['caps']): data['capId'].setdefault(c['slug'], i)
    text = []
    cur = 0
    for c in caps:
        if c['sec'] != cur: cur = c['sec']; text.append('<h3>%s</h3>' % html.escape(titles[cur]))
        if c.get('one'):
            if text[-1].startswith('<p class="one">'): text[-1] = text[-1][:-4] + ' ' + html.escape(c['text']) + '</p>'
            else: text.append('<p class="one">%s</p>' % html.escape(c['text']))
        else: text.append('<p>%s</p>' % html.escape(c['text'], quote=False))
    ticks = ''.join('<i style="left:%.3f%%"></i>' % (ch['t'] / dur * 100) for ch in chapters[1:])
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    out = (tpl.replace('%%DATA%%', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
           .replace('%%ENGINE%%', open(os.path.join(HERE, 'engine.js'), encoding='utf-8').read())
           .replace('%%SHOTS%%', open(os.path.join(HERE, 'shots.js'), encoding='utf-8').read())
           .replace('%%TEXT%%', '\n'.join(text)).replace('%%TICKS%%', ticks)
           .replace('%%HUB%%', '/fractal2/entertainment').replace('%%V8%%', A + 'v8/').replace('%%V9%%', A + 'v9/'))
    open(OUT, 'w', encoding='utf-8').write(out)
    json.dump({'dur': dur, 'caps': [{k: c[k] for k in ('slug', 't0', 't1', 'say', 'need', 'sec', 'text')} for c in caps], 'chapters': chapters}, open(os.path.join(HERE, 'cues.json'), 'w'), indent=1, ensure_ascii=False)
    print('wrote film.html %d KB; %d captions; %.1f s; last caption ends %.1f s' % (len(out) // 1024, len(caps), dur, caps[-1]['t1']))
    for n in sorted(titles):
        cs = [c for c in caps if c['sec'] == n]; nx = SEC_BAR.get(n + 1, END_BAR - 8) * BAR
        short = [c['slug'] for c in cs if c['t1'] - c['t0'] < c['need'] and not c.get('one')]
        print('  sec %2d %-28s %7.1f -> %7.1f  (next %7.1f) pace x%.2f%s%s' % (n, titles[n][:28], cs[0]['t0'], cs[-1]['t1'], nx, cs[0].get('_f', 1), '  OVER' if cs[-1]['t0'] + cs[-1]['say'] > nx else '', '  SHORT:' + ','.join(short) if short else ''))

if __name__ == '__main__': main()
