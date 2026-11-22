#!/usr/bin/env python3
"""Voice audit for The Long After against BOOK-MAP-v2.md section 2 ("the friend who sat through the hearing").

Per page it measures what a script can measure, and flags passages for a human read:
  short sentences       average words per sentence (spec: short) and share over 25 words
  second person         "you/your" per 100 words (spec: second person)
  concrete pictures     sections with no concrete noun from a list of everyday objects and places (spec: one picture per section)
  says it once          hedges per 1,000 words (may, might, often, usually, can, sometimes, tend) -- caution only where it matters
  never clinical        clinical/jargon words
  never cute            cheerleading words
  no "you must"         commanding the reader
  template headings     H2 headings repeated across pages (spec bans repeated template headings)
  register              crisis pages (heavy) must have no metaphors from a small list and short sentences
Writes content/longafter-v2/VOICE-AUDIT.md and prints a summary. Exit 1 if any page fails a hard rule.
"""
import re, glob, json, collections, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "content/longafter-v2"
plan = json.load(open(D / "plan.json")); CH = {c["slug"]: c for c in plan["chapters"]}
CONCRETE = set("""phone message text email letter envelope door key keys lock car bag school gate court courtroom kitchen table
bed bedroom night morning evening weekend handover child children son daughter baby doctor police officer judge lawyer solicitor
bank card cash money passport screenshot notebook paper pen app calendar record photo photos coffee café walk street shop
house home flat room window floor wall shower meal dinner breakfast tea dog cat pet friend sister brother mum dad mother father
neighbour teacher bus train office desk work job form forms list date dates birthday christmas holiday hospital clinic
""".split())
HEDGE = re.compile(r"\b(may|might|often|usually|sometimes|tend(s)? to|can be|could)\b", re.I)
CLINICAL = re.compile(r"\b(dysregulat\w*|somatic\w*|cascade|patholog\w*|maladaptive|psychoeducation|intervention(s)?|stakeholder|utili[sz]\w*|modality|cognitions?)\b", re.I)
CUTE = re.compile(r"\b(you'?ve got this|warrior|queen|slay|journey|thrive|glow up|self-care sunday)\b", re.I)
MUST = re.compile(r"(?<!if )(?<!mean )(?<!means )(?<!that )\byou (must|should)\b(?! (go back|know))", re.I)
METAPHOR = re.compile(r"\b(storm|tunnel|light at the end|rollercoaster|chapter of your life|weather|mountain|climb)\b", re.I)


def pages():
    for f in sorted(glob.glob(str(D / "[0-9]*.md"))):
        for blk in re.split(r"^=== ", open(f).read(), flags=re.M)[1:]:
            slug = blk.split("\n", 1)[0].strip()
            body = blk.split("\n---\n", 1)[1].split("\n## Sources")[0]
            yield slug, body


def prose(body):
    t = "\n".join(l for l in body.splitlines() if not l.startswith("|"))
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return re.sub(r"[*_>#]", "", t)


heads = collections.defaultdict(list)
rows, fails = [], []
for slug, body in pages():
    c = CH.get(slug, {})
    tools = c.get("part") == "tools"
    t = prose(body)
    words = t.split(); n = max(len(words), 1)
    sents = [s for line in t.splitlines() for s in re.split(r"(?<=[.!?])\s+", line.strip()) if len(s.split()) > 2]
    lens = [len(s.split()) for s in sents] or [0]
    avg = statistics.mean(lens); long_share = sum(l > 25 for l in lens) / len(lens) * 100
    you = len(re.findall(r"\byou(r|rs|rself)?\b", t, re.I)) / n * 100
    fa = lambda rx: [m.group(0) for m in rx.finditer(t)]
    hedges = len(fa(HEDGE)) / n * 1000
    clinical = fa(CLINICAL); cute = fa(CUTE); must = fa(MUST)
    secs = re.split(r"^## ", body, flags=re.M)[1:]
    no_pic = []
    for s in secs:
        h, _, rest = s.partition("\n")
        heads[h.strip().lower()].append(slug)
        ws = set(re.findall(r"[a-zé]+", rest.lower()))
        if len(rest.split()) > 60 and not (ws & CONCRETE):
            no_pic.append(h.strip())
    meta = []
    if c.get("heavy"):
        meta = fa(METAPHOR)
    score = 100
    score -= max(0, avg - 14) * 4
    score -= max(0, long_share - 5) * 1.5
    score -= max(0, 3 - you) * 6 if not tools else 0
    score -= max(0, hedges - 18) * 1.2
    score -= len(clinical) * 4 + len(cute) * 8 + len(must) * 2 + len(no_pic) * 3 + len(meta) * 5
    score = round(max(0, min(100, score)))
    hard = []
    if cute: hard.append(f"cheerleading: {sorted(set(map(str.lower, cute)))}")
    if meta: hard.append(f"metaphor on a crisis page: {sorted(set(map(str.lower, meta)))}")
    if hard: fails.append((slug, hard))
    rows.append(dict(slug=slug, words=len(words), avg=round(avg, 1), long=round(long_share), you=round(you, 1),
                     hedge=round(hedges, 1), clinical=sorted(set(map(str.lower, clinical))), must=len(must),
                     no_pic=no_pic, score=score, hard=hard))

FORMS = {"safety-plan-worksheet", "device-and-account-audit", "court-day-checklist"}
dup = {h: s for h, s in heads.items() if len(set(s) - FORMS) > 1 and h not in ("sources",)}
rows.sort(key=lambda r: r["score"])
L = ["# The Long After: voice audit", "",
     "Measured against BOOK-MAP-v2.md §2. Score is a guide for where to read first, not a verdict. Generated by `scripts/longafter-voice.py`.", "",
     f"Pages: {len(rows)}. Median score {statistics.median(r['score'] for r in rows)}. "
     f"Average sentence {statistics.mean(r['avg'] for r in rows):.1f} words. Headings repeated across pages: {len(dup)}.", "",
     "| Score | Page | Avg sentence | Over 25 words | You per 100 | Hedges per 1,000 | Clinical | 'You must/should' | Sections with no concrete picture |",
     "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['score']} | {r['slug']} | {r['avg']} | {r['long']}% | {r['you']} | {r['hedge']} | {', '.join(r['clinical']) or '-'} | {r['must']} | {'; '.join(r['no_pic']) or '-'} |")
L += ["", "## Headings repeated across pages", ""] + [f"- \"{h}\": {', '.join(sorted(set(s)))}" for h, s in sorted(dup.items())]
(D / "VOICE-AUDIT.md").write_text("\n".join(L) + "\n")
print(f"{len(rows)} pages; median score {statistics.median(r['score'] for r in rows)}; lowest:")
for r in rows[:12]:
    print(f"  {r['score']:3} {r['slug']:52} avg {r['avg']:4} long {r['long']:2}% you {r['you']:4} hedge {r['hedge']:4} must {r['must']} nopic {len(r['no_pic'])} {r['clinical'] or ''}")
print(f"repeated headings: {len(dup)}")
for s, h in fails: print("  HARD", s, h)
raise SystemExit(1 if fails else 0)
