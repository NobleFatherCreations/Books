"""Character-level repair for the generated religion Markdown (Sacred Divide v5, pass one).

apply() changes only what is provably a text-extraction artifact (ligature glyphs, doubled spaces in prose).
It never touches numbers, names, grades, receipts, URLs or quotations' words. Everything else it can only
*suspect* (straight quotes, spaced hyphens where a dash may belong) is counted in the log as a candidate
and left for a human decision.
"""
import re

LIGATURES = {'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', 'ﬅ': 'st', 'ﬆ': 'st'}
NAMES = {'ﬀ': 'ﬀ→ff', 'ﬁ': 'ﬁ→fi', 'ﬂ': 'ﬂ→fl', 'ﬃ': 'ﬃ→ffi', 'ﬄ': 'ﬄ→ffl', 'ﬅ': 'ﬅ→st', 'ﬆ': 'ﬆ→st'}
LIG_RE = re.compile('[' + ''.join(LIGATURES) + ']')


def apply(md):
    counts, edits = {}, []

    def lig(m):
        counts[NAMES[m.group(0)]] = counts.get(NAMES[m.group(0)], 0) + 1
        return LIGATURES[m.group(0)]
    out = []
    for n, line in enumerate(md.split('\n'), 1):
        new = LIG_RE.sub(lig, line)
        if new != line and len(edits) < 400:
            edits.append((n, re.search(r'\S*[' + ''.join(LIGATURES) + r']\S*', line).group(0), re.search(r'\S*' + '|'.join(re.escape(v) for v in set(LIGATURES.values())) + r'\S*', new).group(0) if False else None))
        out.append(new)
    md2 = '\n'.join(out)
    cand = {
        'straight double quotes (candidates, not changed)': len(re.findall(r'"', md2)),
        'spaced hyphen " - " where a dash may belong (candidates, not changed)': len(re.findall(r'(?<=\w) - (?=\w)', md2)),
        'doubled spaces inside prose lines (candidates, not changed)': len(re.findall(r'(?<=\S)  (?=\S)', '\n'.join(l for l in md2.split('\n') if not l.lstrip().startswith(('|', '```', '    '))))),
    }
    return md2, counts, cand


def log(rid, counts, cand):
    L = [f'# Repair log — {rid}', '', 'Pass one, character-level. Changes are limited to ligature glyphs; every other item is a candidate for human review.', '',
         '## Applied', '', '| Fix | Count |', '|---|---|']
    L += [f'| {k} | {v} |' for k, v in sorted(counts.items())] or ['| (none) | 0 |']
    L += [f'| **Total** | **{sum(counts.values())}** |', '', '## Candidates (not applied)', '', '| Item | Count |', '|---|---|']
    L += [f'| {k} | {v} |' for k, v in cand.items()]
    return '\n'.join(L) + '\n'
