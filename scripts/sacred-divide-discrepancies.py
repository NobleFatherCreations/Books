#!/usr/bin/env python3
"""Collect the P1 items from docs/sacred-divide-v5/discrepancies/<id>.md into one register, ranked by volume,
so the owner can decide them in one sitting. The full items stay in the per-volume files."""
import os, re
D = 'docs/sacred-divide-v5/discrepancies'; OUT = 'docs/sacred-divide-v5/P1-REGISTER.md'
L = ['# P1 register — every critical item across the edited volumes', '',
     'One line per item: where it is and what is wrong. The proposed wording, the evidence and the reason are in the per-volume file linked beside each volume. Catholicism\'s items are in `DISCREPANCIES.md`. Nothing listed here has been changed in the text unless the item says so.', '']
tot = 0
for fn in sorted(os.listdir(D)):
    if not fn.endswith('.md'): continue
    s = open(os.path.join(D, fn), encoding='utf-8').read()
    m = re.search(r'^## P1.*?\n(.*?)(?=^## )', s, re.S | re.M)
    if not m: continue
    items = re.findall(r'^\d+\.\s+(.*?)(?=^\d+\.\s|\Z)', m.group(1), re.S | re.M)
    L += [f'## {fn[:-3]} ({len(items)}) — [full file](discrepancies/{fn})', '']
    for it in items:
        first = re.sub(r'\s+', ' ', it).strip()
        first = re.split(r'(?<=[a-z0-9\)\]"”])\s→', first)[0]
        L.append(f'- {first[:420]}')
        tot += 1
    L.append('')
L.insert(3, f'**{tot} P1 items** across {sum(1 for f in os.listdir(D) if f.endswith(".md"))} volumes, plus Catholicism.\n')
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(tot)
