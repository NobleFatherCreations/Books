#!/usr/bin/env python3
"""Fractal² film: fit the owner's four Suno cues to the film clock. Re-runnable: python3 design/fractal2/film/fit_score.py

Reads the slots, anchors, silences and caption times from design/fractal2/film/cues.json (written by build.py), so it
re-fits whenever the voice re-times the film. Inputs (git-ignored): design/fractal2/film/audio/cue1..4.wav, hub-loop.wav.
Outputs:
  design/fractal2/film/audio/score.wav             full-quality score, sample 0 = film 0 (git-ignored)
  library/fractal2/site/fractal2/_a/film/score.m4a web copy for the film page (AAC, 160 kbps)
  library/fractal2/site/fractal2/_a/film/hub.m4a   hub loop, trimmed to whole bars (AAC, 128 kbps)
  design/fractal2/film/score/fit.json, FIT-REPORT.md   where each repeat was made, where each anchor landed

Rules (content/fractal2/SUNO-PROMPTS-V16.md): no tempo or pitch change. Each cue is lengthened by repeating its own
steady passages in whole 8-bar blocks at bar boundaries (equal-power crossfades of 30 ms); when a region needs a
length that is not a multiple of 8 bars, the surplus is removed as one bar-boundary jump in its steadiest stretch.
"""
import os, json, subprocess, math
import numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfiltfilt

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
AUD = os.path.join(HERE, 'audio'); OUTD = os.path.join(HERE, 'score'); WEB = os.path.join(ROOT, 'library/fractal2/site/fractal2/_a/film')
SR = 48000; BAR = 1.6; BEAT = .4; XF = .030; DUCK_DB = -5.0; TAIL = 6.0

def load(name):
    y, sr = sf.read(os.path.join(AUD, name), dtype='float32', always_2d=True); assert sr == SR, (name, sr); return y.T.copy()   # (2, n)

def grid(y):
    """first downbeat (s) and the per-bar features. Beat period from the tracker (fit by least squares); the downbeat is the beat phase with the most low-band (kick) onset."""
    m = librosa.resample(y.mean(0), orig_sr=SR, target_sr=22050); sr = 22050; hop = 256
    oe = librosa.onset.onset_strength(y=m, sr=sr, hop_length=hop)
    _, beats = librosa.beat.beat_track(onset_envelope=oe, sr=sr, hop_length=hop, start_bpm=150, units='time', tightness=400)
    k = np.round((beats - beats[0]) / BEAT); c = np.linalg.lstsq(np.vstack([np.ones_like(k), k]).T, beats, rcond=None)[0]
    S = np.abs(librosa.stft(m, n_fft=2048, hop_length=hop)); fr = librosa.fft_frequencies(sr=sr, n_fft=2048)
    lo = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[fr < 150]), sr=sr, hop_length=hop); tt = librosa.frames_to_time(np.arange(len(lo)), sr=sr, hop_length=hop)
    sc = [np.interp(np.arange(c[0] + ph * c[1], tt[-1], 4 * c[1]), tt, lo).mean() for ph in range(4)]
    o = (c[0] + int(np.argmax(sc)) * c[1]) % BAR
    S2 = np.abs(librosa.stft(m, n_fft=1024, hop_length=64)); f2 = librosa.fft_frequencies(sr=sr, n_fft=1024)        # refine the phase at 3 ms resolution (the same measure the report uses)
    l2 = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S2[f2 < 150]), sr=sr, hop_length=64); t2 = librosa.frames_to_time(np.arange(len(l2)), sr=sr, hop_length=64)
    offs = np.arange(-.08, .0801, .002); o = (o + offs[int(np.argmax([np.interp(np.arange(o + d, t2[-1], BAR), t2, l2).sum() for d in offs]))]) % BAR
    nb = int((y.shape[1] / SR - o) // BAR)
    mf = librosa.feature.mfcc(y=m, sr=sr, n_mfcc=13, hop_length=hop); rms = librosa.feature.rms(y=m, hop_length=hop)[0]; ft = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    feats, db = [], []
    for b in range(nb):
        i0, i1 = np.searchsorted(ft, o + b * BAR), np.searchsorted(ft, o + (b + 1) * BAR)
        feats.append(mf[:, i0:i1].mean(1)); db.append(20 * np.log10(rms[i0:i1].mean() + 1e-6))
    bl = np.interp(o + np.arange(nb) * BAR, tt, librosa.util.normalize(lo))
    return {'o': float(o), 'period': float(c[1]), 'nb': nb, 'f': np.array(feats), 'db': np.array(db), 'kick': bl, 'phase_scores': [float(x) for x in sc]}

def lift(G, b, w=4):
    """how strongly the music enters at bar b: energy of the next w bars over the last w, plus the kick on the downbeat"""
    db = G['db']; a = db[max(0, b - w):b]; n = db[b:b + w]
    if len(a) == 0 or len(n) == 0: return -99.
    return float(n.mean() - a.mean() + 2.0 * G['kick'][b])

def seam_cost(G, j, L=8):
    """repeating bars j..j+L-1 means bar j follows bar j+L-1: good when bar j sounds like bar j+L, and the block is steady"""
    f, db = G['f'], G['db']
    if j + L >= G['nb']: return 9e9
    return float(np.linalg.norm(f[j] - f[j + L]) / 10 + abs(db[j] - db[j + L]) + 1.5 * np.std(db[j:j + L]))

def fill(G, lo, hi, L, avoid=()):
    """source bar indices for a region lo..hi-1 stretched (or cut) to exactly L bars. Returns (bars, edits)."""
    n = hi - lo; edits = []; seq = list(range(lo, hi))
    if L == n: return seq, edits
    q = max(0, math.ceil((L - n) / 8)); cand = sorted((seam_cost(G, j), j) for j in range(lo, hi - 8) if not any(j <= a < j + 9 for a in avoid))
    used = []
    for _, j in cand:                                        # distinct, non-overlapping blocks first; if the region is short, the best blocks play a third time
        if len(used) >= q: break
        if all(abs(j - u) >= 8 for u in used): used.append(j)
    base = list(used); k = 0
    while len(used) < q and base: used.append(base[k % len(base)]); k += 1
    for j in sorted(used, reverse=True):
        i = seq.index(j + 7); seq[i + 1:i + 1] = list(range(j, j + 8)); edits.append({'kind': 'repeat', 'bars': [j, j + 7]})
    surplus = len(seq) - L
    if surplus > 0:                                          # one jump forward over `surplus` bars, where the music is steadiest (bar after the jump sounds like the bar it replaces)
        best = None
        for i in range(1, len(seq) - surplus - 1):
            a, b = seq[i - 1], seq[i + surplus]
            if any(seq[k] in avoid for k in range(i, i + surplus)): continue
            if b != a + 1 and b <= a: continue
            c = float(np.linalg.norm(G['f'][seq[i]] - G['f'][b]) / 10 + abs(G['db'][seq[i]] - G['db'][b]))
            if best is None or c < best[0]: best = (c, i)
        i = best[1]; edits.append({'kind': 'skip', 'bars': [seq[i], seq[i + surplus - 1]]}); del seq[i:i + surplus]
    return seq, edits

def render(y, G, seq, tail=0.0):
    """concatenate source bars; equal-power crossfades of XF at every jump; returns (2, n) at exact 1.6 s per bar"""
    n = int(round(len(seq) * BAR * SR)) + int(tail * SR); out = np.zeros((2, n), np.float32); h = int(XF * SR / 2)
    runs = []; s = 0
    for i in range(1, len(seq) + 1):
        if i == len(seq) or seq[i] != seq[i - 1] + 1: runs.append((s, i)); s = i
    for ri, (a, b) in enumerate(runs):
        src0 = int(round((G['o'] + seq[a] * BAR) * SR)); dst0 = int(round(a * BAR * SR)); ln = int(round((b - a) * BAR * SR))
        extra = int(tail * SR) if ri == len(runs) - 1 else 0
        pre = h if ri > 0 else 0; post = h if ri < len(runs) - 1 else 0
        s0 = max(0, src0 - pre); s1 = min(y.shape[1], src0 + ln + post + extra); seg = y[:, s0:s1].copy(); d0 = dst0 - (src0 - s0)
        L = seg.shape[1]; w = np.ones(L, np.float32)
        if pre: tt = np.linspace(0, 1, 2 * pre, dtype=np.float32); w[:2 * pre] = np.sin(tt * np.pi / 2)
        if post: tt = np.linspace(0, 1, 2 * post, dtype=np.float32); w[L - 2 * post:] = np.cos(tt * np.pi / 2) if not extra else w[L - 2 * post:]
        e = min(n, d0 + L); out[:, max(0, d0):e] += (seg * w)[:, max(0, -d0):e - d0]
    return out

def downbeat_offset(x, t, w0, w1, sr=SR):
    """measured: the nearest kick downbeat to film time t (ms), from the rendered score itself"""
    a = max(0, int((w0 - .4) * sr)); b = min(x.shape[1], int((w1 + .4) * sr))                 # inside the anchor's own cue only
    m = librosa.resample(x[:, a:b].mean(0), orig_sr=sr, target_sr=22050)
    S = np.abs(librosa.stft(m, n_fft=1024, hop_length=64)); fr = librosa.fft_frequencies(sr=22050, n_fft=1024)
    lo = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[fr < 150]), sr=22050, hop_length=64); tt = librosa.frames_to_time(np.arange(len(lo)), sr=22050, hop_length=64) + a / sr
    best = None
    for off in np.arange(-.2, .2001, .002):                 # phase of the 1.6 s grid that best fits the kicks around t
        g = t + off + np.arange(math.ceil((w0 - t) / BAR), int((w1 - t) / BAR) + 1) * BAR; v = np.interp(g, tt, lo).sum()   # the anchor's grid, across its cue
        if best is None or v > best[0]: best = (v, off)
    return round(best[1] * 1000, 1)

def main():
    os.makedirs(OUTD, exist_ok=True)
    C = json.load(open(os.path.join(HERE, 'cues.json'))); dur = C['dur']; M = C['marks']; ch = {c['n']: c['t'] for c in C['chapters']}
    STOP, PK1, PK2, PK3, S11 = M['STOP'], M['PEAK1'], M['PEAK2'], M['PEAK3'], ch[11]
    cap = {c['slug']: c for c in C['caps']}; bot = cap['and-at-the-bottom']
    SIL = [(STOP, STOP + 2 * BAR), (math.floor(bot['t0'] / BAR - 1e-6) * BAR - BAR, math.ceil(bot['t1'] / BAR - 1e-6) * BAR)]
    slots = [('cue1.wav', 0.0, STOP), ('cue2.wav', STOP, PK2), ('cue3.wav', PK2, S11), ('cue4.wav', S11, dur)]
    for a in (STOP, PK1, PK2, PK3, S11, dur): assert abs(a / BAR - round(a / BAR)) < 1e-6, ('anchor off the bar grid', a)
    total = int(round((dur + TAIL) * SR)); mix = np.zeros((2, total), np.float32); rep = {'film_dur': dur, 'sr': SR, 'bar': BAR, 'silences': SIL, 'cues': []}
    for name, t0, t1 in slots:
        y = load(name); G = grid(y); N = int(round((t1 - t0) / BAR)); nb = G['nb']; info = {'cue': name, 'slot': [t0, t1], 'bars_slot': N, 'bars_cue': nb, 'first_downbeat_s': round(G['o'], 3), 'beat_period_s': round(G['period'], 5)}
        if name == 'cue1.wav':                                # the question: build to the STOP; hard cut there
            seq, ed = fill(G, 0, nb, N); info['anchor'] = None
        elif name == 'cue2.wav':                              # the strongest entry of the cue lands on PEAK1
            p = int(round((PK1 - t0) / BAR)); a = max(range(max(8, p // 2), min(nb - 40, p + 24)), key=lambda b: lift(G, b)); info['lift_bar'] = a; info['lift_score'] = round(lift(G, a), 2)   # an entry the pre-anchor music can reach without looping its intro
            if a >= p: pre, e1 = list(range(a - p, a)), ([{'kind': 'skip', 'bars': [0, a - p - 1]}] if a > p else [])
            else: pre, e1 = fill(G, 0, a, p)
            post, e2 = fill(G, a, nb, N - p, avoid=(a,)); seq, ed = pre + post, e1 + e2; info['anchor'] = {'name': 'PEAK1', 'film_s': PK1}
        elif name == 'cue3.wav':                              # starts on PEAK2 with its strongest opening; its biggest lift on PEAK3
            s0 = max(range(0, 9), key=lambda b: float(G['db'][b:b + 2].mean()) + 2.0 * float(G['kick'][b]))      # a drop on 'down': the loudest early downbeat with a kick (the owner's cue 3 fades in, so its biggest *change* was a quiet bar); p = int(round((PK3 - t0) / BAR))
            a = max(range(max(s0 + 16, int(nb * .55)), nb - 6), key=lambda b: lift(G, b)); info['opening_bar'] = s0; info['lift_bar'] = a; info['lift_score'] = round(lift(G, a), 2)   # the release lives in the cue's last part (the F major lift)
            pre, e1 = fill(G, s0, a, p, avoid=(s0,)); post, e2 = fill(G, a, nb, N - p, avoid=(a,)); seq, ed = pre + post, e1 + e2
            if s0: ed.insert(0, {'kind': 'start', 'bars': [s0, s0]})
            info['anchor'] = {'name': 'PEAK3', 'film_s': PK3}
        else:                                                 # the map: its own ending lands on the film's last bar, ring-out after
            seq, ed = fill(G, 0, nb, N); info['anchor'] = None
        x = render(y, G, seq, tail=TAIL if name == 'cue4.wav' else 0.0)
        r = np.sqrt(np.mean(x[:, :int(N * BAR * SR)] ** 2)) + 1e-9; x *= (10 ** (-20 / 20)) / r      # level-match the cues (about -20 dBFS RMS each)
        if name != 'cue4.wav':                                # hard edge at the slot end (a 12 ms fade so it does not click)
            e = int(round(N * BAR * SR)); f = int(.012 * SR); x = x[:, :e]; x[:, e - f:] *= np.linspace(1, 0, f, dtype=np.float32)
            if name == 'cue2.wav':                            # the two-bar pull-in under "So I stopped trying to climb out, and I went down": 9 dB down so the drop on 'down' lands
                g = int(round(2 * BAR * SR)); x[:, e - g:] *= np.linspace(1, 10 ** (-9 / 20), g, dtype=np.float32)
        else:
            f = int(TAIL * SR); x[:, -f:] *= np.linspace(1, 0, f, dtype=np.float32) ** 2
        f = int(.006 * SR); x[:, :f] *= np.linspace(0, 1, f, dtype=np.float32)
        d0 = int(round(t0 * SR)); mix[:, d0:d0 + x.shape[1]] += x[:, :total - d0]
        info['edits'] = [dict(e, film_s=None) for e in ed]
        for e in info['edits']:                                # where the edit sits in film time (the first output bar that plays it)
            try:
                if e['kind'] == 'repeat': k = [i for i, b in enumerate(seq) if b == e['bars'][0]][1]
                elif e['kind'] == 'skip': k = 0 if e['bars'][0] == 0 else next((i + 1 for i in range(len(seq) - 1) if seq[i] < e['bars'][0] and seq[i + 1] > e['bars'][1]), len(seq))
                else: k = 0
                e['film_s'] = round(t0 + k * BAR, 1)
            except (ValueError, IndexError): e['film_s'] = round(t0, 1)
        info['seq_runs'] = []; s = 0
        for i in range(1, len(seq) + 1):
            if i == len(seq) or seq[i] != seq[i - 1] + 1: info['seq_runs'].append([seq[s], seq[i - 1]]); s = i
        rep['cues'].append(info); print(name, 'slot', N, 'bars from', nb, 'edits', [(e['kind'], e['bars'], e['film_s']) for e in info['edits']])
    for a, b in SIL: mix[:, int(round(a * SR)):int(round(b * SR))] = 0.0      # true digital silence
    # duck 300 Hz to 3 kHz wherever a caption is on screen, so the voice will sit on top (zero-phase band split, 150 ms ramps)
    sos = butter(4, [300, 3000], btype='bandpass', fs=SR, output='sos'); band = sosfiltfilt(sos, mix, axis=1).astype(np.float32)
    tt = np.arange(total) / SR; on = np.zeros(total, np.float32)
    for c in C['caps']: on[int(c['t0'] * SR):int(min(c['t1'], dur) * SR)] = 1
    k = int(.15 * SR); on = np.convolve(on, np.ones(k, np.float32) / k, 'same'); g = 1 - (1 - 10 ** (DUCK_DB / 20)) * on
    mix = mix - band * (1 - g)
    for a, b in SIL: mix[:, int(round(a * SR)):int(round(b * SR))] = 0.0
    pk = float(np.abs(mix).max()); mix *= min(1.0, .891 / pk)                 # peak at -1 dBFS at most
    sf.write(os.path.join(AUD, 'score.wav'), mix.T, SR, subtype='PCM_16')
    rep['anchors'] = []
    for nm, t, w0, w1 in [('PEAK1', PK1, PK1 - 25.6, PK1 + 25.6), ('PEAK2', PK2, PK2, PK2 + 32), ('PEAK3', PK3, PK3 - 51.2, S11)]: rep['anchors'].append({'name': nm, 'film_s': t, 'window_s': [w0, w1], 'nearest_downbeat_ms': downbeat_offset(mix, t, w0, w1)})
    rep['anchors'].append({'name': 'STOP', 'film_s': STOP, 'cut': 'hard cut; silence to %.1f s' % (STOP + 2 * BAR), 'level_after_db': round(20 * np.log10(np.abs(mix[:, int(STOP * SR) + 10:int((STOP + 3) * SR)]).max() + 1e-12), 1)})
    rep['silence_check'] = [{'span': [a, b], 'max_abs': float(np.abs(mix[:, int(round(a * SR)):int(round(b * SR))]).max())} for a, b in SIL]
    os.makedirs(WEB, exist_ok=True)
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(AUD, 'score.wav'), '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', os.path.join(WEB, 'score.m4a')])
    # the hub loop: whole bars from its first downbeat, a short crossfade of its end into its start
    hy = load('hub-loop.wav'); HG = grid(hy); nbh = HG['nb']; s0 = int(round(HG['o'] * SR)); L = int(round(nbh * BAR * SR)); lp = hy[:, s0:s0 + L].copy(); f = int(.05 * SR)
    if s0 >= f: lp[:, -f:] = lp[:, -f:] * np.linspace(1, 0, f, dtype=np.float32) + hy[:, s0 - f:s0] * np.linspace(0, 1, f, dtype=np.float32)
    r = np.sqrt(np.mean(lp ** 2)) + 1e-9; lp *= min((10 ** (-22 / 20)) / r, .891 / (np.abs(lp).max() + 1e-9))
    sf.write(os.path.join(AUD, 'hub.wav'), lp.T, SR, subtype='PCM_16')
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(AUD, 'hub.wav'), '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', os.path.join(WEB, 'hub.m4a')])
    rep['hub'] = {'bars': nbh, 'first_downbeat_s': round(HG['o'], 3), 'loop_s': round(L / SR, 3)}
    rep['web'] = {'score.m4a': os.path.getsize(os.path.join(WEB, 'score.m4a')), 'hub.m4a': os.path.getsize(os.path.join(WEB, 'hub.m4a'))}
    rep['score_wav_s'] = round(total / SR, 3)
    json.dump(rep, open(os.path.join(OUTD, 'fit.json'), 'w'), indent=1, default=float)
    md = ['# Fractal² score: fit report (written by design/fractal2/film/fit_score.py; re-run after any re-timing)', '',
          'Film %.1f s; score %.1f s (sample 0 = film 0; the rest is cue 4\'s ring-out). 150 BPM, bar 1.6 s. No tempo or pitch change: every edit is a whole-bar cut with a 30 ms equal-power crossfade.' % (dur, total / SR), '',
          '## Anchors (offset of the nearest kick downbeat, measured on the rendered score)', '', '| Anchor | Film time | Nearest downbeat |', '|---|---|---|']
    md += ['| %s | %.1f s | %+.1f ms |' % (a['name'], a['film_s'], a['nearest_downbeat_ms']) for a in rep['anchors'] if 'nearest_downbeat_ms' in a]
    md += ['| STOP | %.1f s | hard cut, digital silence to %.1f s (peak after cut %s dBFS) |' % (STOP, STOP + 2 * BAR, rep['anchors'][-1]['level_after_db']), '',
           'Silences: ' + ', '.join('%.1f-%.1f s (max sample %g)' % (s['span'][0], s['span'][1], s['max_abs']) for s in rep['silence_check']) + '.', '',
           'Captions duck 300 Hz-3 kHz by %g dB (150 ms ramps).' % -DUCK_DB, '', '## Edits per cue', '']
    for c in rep['cues']:
        md.append('**%s** (slot %.1f-%.1f s, %d bars from a %d-bar cue; first downbeat at %.3f s%s)' % (c['cue'], c['slot'][0], c['slot'][1], c['bars_slot'], c['bars_cue'], c['first_downbeat_s'],
                  (', biggest lift at cue bar %d' % c['lift_bar']) if 'lift_bar' in c else '')); md.append('')
        for e in c['edits']: md.append('- %s cue bars %d-%d, heard at film %.1f s' % ({'repeat': 'repeat of', 'skip': 'skip over', 'start': 'start at'}[e['kind']], e['bars'][0] + 1, e['bars'][1] + 1, e['film_s']))
        md.append('- played as cue bars: ' + ', '.join('%d-%d' % (a + 1, b + 1) for a, b in c['seq_runs'])); md.append('')
    md.append('Hub loop: %d whole bars (%.1f s) from its first downbeat at %.3f s, end crossfaded into the start.' % (nbh, L / SR, HG['o']))
    md.append(''); md.append('Web copies: score.m4a %.1f MB, hub.m4a %.1f MB.' % (rep['web']['score.m4a'] / 1e6, rep['web']['hub.m4a'] / 1e6))
    open(os.path.join(OUTD, 'FIT-REPORT.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md[:12]))

if __name__ == '__main__': main()
