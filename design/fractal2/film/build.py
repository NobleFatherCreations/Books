#!/usr/bin/env python3
"""Fractal² film: build. python3 design/fractal2/film/build.py [--words words.json]
Reads content/fractal2/intro-v15.md, lays out caption times (placeholder clock, or a word-level timestamp JSON),
builds the MSDF font data, and writes library/fractal2/site/fractal2/film.html (served locally at /fractal2/film)."""
import os, re, json, html, sys, shutil, subprocess, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
SITE = os.path.join(ROOT, 'library/fractal2/site/fractal2')
OUT = os.path.join(SITE, 'film.html')
A = '/fractal2/_a/'
BAR = 1.6
SRC = 'content/fractal2/intro-v16.md'
# extra silence before a caption (seconds): room for the picture to act alone
PRE = {'why-do-i-keep': 1.6, 'it-must-be-me': 1.4, 'what-if-it-isnt': 2.2, 'i-wrote-it-down': .3, 'idealize': 1.2,
       'thirty-techniques-carried-a': 1.6, 'i-thought-i-had': 6.0, 'i-had-only-found': 1.4}
FIRST = 4.4                                      # the launch plays before the first word
TAIL = {2: 3.5, 3: 2.0}                          # seconds kept clear at the end of a section for picture alone
BIG = {'why-do-i-keep', 'what-if-it-isnt', 'it-must-be-me', 'i-am-still-looking', 'my-original-frequency', 'that-is-the-fractal', 'now-the-map-is', 'it-made-me-who'}
SPLIT = {'idealize-hook-devalue-confuse'}        # one caption per word
MARKS = {'STOP': 'start', 'PEAK1': 'end', 'PEAK2': 'end', 'PEAK3': 'end'}

def slug(t):
    w = re.sub(r"[^a-z0-9 ]", '', t.lower().replace("'", '').replace('’', '')).split()
    return '-'.join(w[:4])

WEAK = set('a an the and of to in or my i it that with from for at by is was on as so but its his her our your'.split())
def groups(t):
    """phrase groups of about three words, breaking after punctuation where possible"""
    w = t.split(); out = []; cur = []
    for i, x in enumerate(w):
        cur.append(x)
        left = len(w) - i - 1
        weak = x.lower().strip('“"') in WEAK and left > 0
        if ((len(cur) >= 3 and (x[-1] in '.,?!:;”' or len(cur) >= 4) and left != 1) and not weak) or left == 0:
            out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out

def sentences(par):
    """one caption per sentence; very short neighbours share a caption; very long sentences break at a comma"""
    raw = [x.strip() for x in re.split(r'(?<=[.?!]")\s+|(?<=[.?!])\s+(?=["A-Z{])', par) if x.strip()]
    raw2 = []
    for x in raw:                                           # a closing quote that got separated goes back
        if x.startswith('" ') or x == '"': raw2[-1] += '"'; x = x[1:].strip()
        if x: raw2.append(x)
    out = []
    for x in raw2:
        n = len(x.split())
        if out:
            p = out[-1]; pn = len(p.split())
            if x.startswith('"') and not (p.startswith('"') and p.endswith('"')): out.append(x); continue
            if (pn + n <= 10 and n <= 4 and (pn <= 6 or p.count('.') > 1) and not (pn > 4 and p.count('.') == 1 and n == 1)) or (pn <= 3 and pn + n <= 8) or (p.startswith('"') and pn <= 5 and p.endswith('"') and pn + n <= 12) or x.startswith('{'):
                out[-1] = p + ' ' + x; continue
        out.append(x)
    fin = []
    for x in out:
        w = x.split()
        if len(w) > 19:
            cuts = [i for i, t in enumerate(w[:-1]) if t[-1] in ',:;' and 5 <= i + 1 <= len(w) - 5]
            if cuts:
                c = min(cuts, key=lambda i: abs(i + 1 - len(w) / 2)); fin.append(' '.join(w[:c + 1])); fin.append(' '.join(w[c + 1:])); continue
        fin.append(x)
    return fin

def parse():
    md = open(os.path.join(ROOT, SRC), encoding='utf-8').read().split('\n---\n')[1]
    caps = []; sec = 0; titles = {}
    for line in md.split('\n'):
        line = line.strip()
        m = re.match(r'## (\d+)\. (.+)', line)
        if m: sec = int(m.group(1)); titles[sec] = m.group(2); continue
        if not line or line.startswith('[SCREEN') or line.startswith('#') or re.fullmatch(r'\([^)]*\)', line): continue
        line = re.sub(r'\s*\((?:[a-z][^)]*)\)\s*', ' ', line).strip()   # inline delivery notes
        for text in sentences(line):
            mark = None
            m = re.search(r'\s*\{(\w+)\}', text)
            if m: mark = m.group(1); text = (text[:m.start()] + text[m.end():]).strip()
            q = text.count('"')
            if q:                                           # straight quotes to curly, in pairs
                parts = text.split('"'); text = ''.join(p + ('' if i == len(parts) - 1 else ('“' if i % 2 == 0 else '”')) for i, p in enumerate(parts))
            text = text.replace("'", '’')
            s = slug(text)
            if s in SPLIT:
                for w in text.split(): caps.append({'text': w, 'sec': sec, 'slug': slug(w), 'big': True, 'locked': False, 'one': True})
            else:
                caps.append({'text': text, 'sec': sec, 'slug': s, 'big': s in BIG, 'locked': False, 'mark': mark})
    return caps, titles

def layout(caps):
    """placeholder clock, about two words a second with breaths. Each section starts on a 4-bar line; the four anchors land on bar lines."""
    secs = sorted({c['sec'] for c in caps}); start = 0.0; SEC = {}; marks = {}
    for sec in secs:
        cs = [c for c in caps if c['sec'] == sec]
        SEC[sec] = start; t = FIRST if sec == 1 else .6
        for i, c in enumerate(cs):
            n = len(c['text'].split())
            t += PRE.get(c['slug'], 0) if i else 0
            say = 1.25 if c.get('one') else max(1.2, n / 2.1 + .3)
            if c.get('mark'):
                a = start + t + (0 if MARKS[c['mark']] == 'start' else say)
                d = math.ceil(a / BAR - 1e-6) * BAR - a; t += d; marks[c['mark']] = round(a + d, 3)
            c['t0'] = round(start + t, 3); c['say'] = round(say, 3)
            t += (say + .2) if c.get('one') else max(.35 * n + 1.95, say + .7 + min(1.0, n * .035))
        t += TAIL.get(sec, 1.5)
        start += math.ceil(t / (4 * BAR)) * 4 * BAR
    for i, c in enumerate(caps):
        nxt = caps[i + 1]['t0'] if i + 1 < len(caps) else c['t0'] + c['say'] + 3
        n = len(c['text'].split())
        need = .35 * n + 1.2                               # blueprint rule: minimum time on screen
        c['out'] = .22 if c.get('one') else .6
        c['t1'] = round(nxt - .32 if c.get('one') else min(nxt - c['out'] - .08, max(c['t0'] + c['say'] + 2.2, c['t0'] + need + .4)), 3)
        c['need'] = round(need, 2)
    return SEC, start + 8 * BAR, marks

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
    caps, titles = parse(); SEC, dur, marks = layout(caps)
    chapters = [{'n': n, 'title': titles[n], 't': round(SEC[n], 3)} for n in sorted(titles)]
    data = {
        'dur': dur, 'bar': BAR, 'marks': marks,
        'caps': [{'t0': c['t0'], 't1': c['t1'], 'say': c['say'], 'out': c['out'], 'g': [html.escape(g, quote=False) for g in groups(c['text'])], 'big': c['big'], 'locked': c['locked'], 'long': len(c['text'].split()) > 13, 'sec': c['sec'], 'n': len(c['text'].split()), 'need': c['need'], 'slug': c['slug']} for c in caps],
        'capId': {}, 'chapters': chapters,
        'assets': {'orig': [A + 'v8/img/orig.webp', A + 'v8/img/orig-m.webp'], 'core': [A + 'v8/img/orig-core.webp', A + 'v8/img/orig-core-m.webp'],
                   'logo': [A + 'v8/img/logo.webp', A + 'v8/img/logo-m.webp'], 'emb': [A + 'v8/img/emblem.webp', A + 'v8/img/emblem-m.webp'], 'font': [A + 'film/voice-msdf.png']},
        'sectors': [{'name': x['name'], 'relationship': x['relationship']} for x in json.load(open(os.path.join(ROOT, 'content/fractal2/sectors.json')))['sectors']],
        'first': ['font', 'logo', 'orig', 'core'], 'later': ['emb'], 'audio': None, 'font': font(),
    }
    for i, c in enumerate(data['caps']): data['capId'].setdefault(c['slug'], i)
    text = []; cur = 0
    for c in caps:
        if c['sec'] != cur: cur = c['sec']; text.append('<h3>%s</h3>' % html.escape(titles[cur]))
        if c.get('one'):
            if text[-1].startswith('<p class="one">'): text[-1] = text[-1][:-4] + ' ' + html.escape(c['text']) + '</p>'
            else: text.append('<p class="one">%s</p>' % html.escape(c['text']))
        else: text.append('<p>%s</p>' % html.escape(c['text'], quote=False))
    ticks = ''.join('<i style="left:%.3f%%"></i>' % (ch['t'] / dur * 100) for ch in chapters[1:])
    tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    mins = int(round(dur / 60))
    out = (tpl.replace('%%DATA%%', json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
           .replace('%%ENGINE%%', open(os.path.join(HERE, 'engine.js'), encoding='utf-8').read())
           .replace('%%SHOTS%%', open(os.path.join(HERE, 'shots.js'), encoding='utf-8').read())
           .replace('%%TEXT%%', '\n'.join(text)).replace('%%TICKS%%', ticks).replace('A %%MIN%%-minute', ('An ' if mins in (8, 11, 18) else 'A ') + str(mins) + '-minute')
           .replace('%%HUB%%', '/fractal2/entertainment').replace('%%V8%%', A + 'v8/').replace('%%V9%%', A + 'v9/'))
    open(OUT, 'w', encoding='utf-8').write(out)
    json.dump({'dur': dur, 'marks': marks, 'caps': [{k: c[k] for k in ('slug', 't0', 't1', 'say', 'need', 'sec', 'text')} for c in caps], 'chapters': chapters}, open(os.path.join(HERE, 'cues.json'), 'w'), indent=1, ensure_ascii=False)
    def mmss(x): return '%d:%04.1f' % (int(x // 60), x % 60)
    words = sum(len(c['text'].split()) for c in caps)
    print('wrote film.html %d KB; %d captions; %d words; %s (%d bars)' % (len(out) // 1024, len(caps), words, mmss(dur), round(dur / BAR)))
    rows = []
    for n in sorted(titles):
        cs = [c for c in caps if c['sec'] == n]; end = SEC.get(n + 1, dur - 8 * BAR)
        rows.append('| %d. %s | %d-%d | %s-%s | %d |' % (n, titles[n], SEC[n] / BAR + 1, end / BAR, mmss(SEC[n]), mmss(end), sum(len(c['text'].split()) for c in cs)))
    tm = ['# Fractal² film: timing sheet (generated by design/fractal2/film/build.py; provisional until the picture is locked)', '',
          '150 BPM, one bar = 1.6 s. Script: %s. %d words, %s, %d bars.' % (SRC, words, mmss(dur), round(dur / BAR)), '',
          '| Section | Bars | Time | Words |', '|---|---|---|---|'] + rows + ['| Outro | %d-%d | %s-%s | |' % (dur / BAR - 7, dur / BAR, mmss(dur - 8 * BAR), mmss(dur)), '',
          '## The four anchors', '', '| Anchor | Time | Bar |', '|---|---|---|'] + ['| %s | %s | %d |' % (k, mmss(v), round(v / BAR) + 1) for k, v in marks.items()]
    open(os.path.join(ROOT, 'content/fractal2/TIMING.md'), 'w').write('\n'.join(tm) + '\n')
    try: print('\n'.join(rows)); print(marks)
    except BrokenPipeError: pass

if __name__ == '__main__': main()
