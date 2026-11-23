#!/usr/bin/env python3
"""AI-writing audit v2 for The Long After. Combines, without installing any of them:
  - yotamgutman/ai-free-writing-checklist   word and phrase lists
  - blader/humanizer (26 patterns)           structure tells: not-X-but-Y, closers, sayings, run-ups, triads, repeated openings,
                                             dashes, stacked qualifiers, hyphen pairs, bold labels, decorative headings,
                                             heading restated, writing about the document, chatbot residue, Q-and-punch
  - solanabr/writer-style-skill              burstiness (sentence-length spread) and opener variety
  - danielrosehill/My-Tone-Of-Voice          paragraph-length variety
  - zoharbabin/brand-voice                   second person, max 25-word sentences, contractions, no exclamation marks
  - houtini-ai/ai-detect                     model score, run separately (scripts/longafter-ai-detect.py)
Reports per page and per pattern, writes content/longafter-v2/AI-AUDIT.md and AI-AUDIT.json (for before/after compare).
"""
import re, glob, json, statistics, collections, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "content/longafter-v2"
plan = json.load(open(D / "plan.json")); CH = {c["slug"]: c for c in plan["chapters"]}

WORDS = """additionally|align with|bolstered|crucial|deep dive|delve\\w*|enduring|enhance\\w*|garner\\w*|interplay|intricate|intricacies|
landscape|meticulous\\w*|pivotal|quietly|robust|showcas\\w*|tapestry|testament|underscor\\w*|valuable|vibrant|firstly|moreover|furthermore|
subsequently|specifically|consequently|importantly|indeed|notably|essentially|ultimately|certainly|comprehensive|holistic|
innovative|leverag\\w*|utili[sz]\\w*|elevat\\w*|unleash\\w*|harness\\w*|foster\\w*|unlock\\w*|vital|optimi[sz]\\w*|
streamlin\\w*|navigat\\w*|unravel\\w*|embark\\w*|cultivat\\w*|illuminat\\w*|elucidat\\w*|realm|nestled|bustling|ever-evolving|daunting|
complexities|best-in-class|cutting-edge|game-changer|seamless\\w*|empower\\w*|journey|genuinely|truly|actually""".replace("\n", "")
WORD_RX = re.compile(r"\b(" + WORDS + r")\b", re.I)
SOFT_WORDS = re.compile(r"\b(ensure\w*|essential|key|highlight(s|ed|ing)?|explore\w*|generally|powerful|in order to|when it comes to|remember that|to put it simply)\b", re.I)
PATTERNS = {
    "not X but Y": r"\b(?:it'?s|this is|that'?s|it was|they'?re)\s+not\s+[^.;]{1,40}[.;,]\s*(?:it'?s|it is|they'?re|that'?s)\b|\bnot because\b[^.]{1,60}\.\s*because\b",
    "staged run-up": r"\b(here'?s the thing|the truth is|the reality is|the bottom line|let'?s be honest|make no mistake)\b",
    "faux insight": r"\b(nobody tells you|what no one tells you|most people (miss|don'?t realise|get wrong))\b",
    "Q-and-punch": r"\?\s+(?:The answer|Simple|Easy|Yes|No)\b[^.!?]{0,25}[.!]",
    "writing about the document": r"\b(this chapter|this section|this page|in this chapter|below, you'?ll find)\b",
    "chatbot residue": r"\b(i hope this helps|great question|as an ai|feel free to|let me know)\b",
    "inflated significance": r"\b(plays a (vital|key|crucial) role|stands as|marks a (pivotal|turning)|serves as a (reminder|testament))\b",
    "borrowed authority": r"\b(experts (agree|say)|studies show|research shows|it is widely (known|accepted))\b",
    "stacked qualifiers": r"\b(could potentially|may possibly|might perhaps|can sometimes possibly|it'?s possible that .{0,30}\bmay\b)\b",
    "exclamation": r"!\s",
}
CPAT = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}


def pages():
    for f in sorted(glob.glob(str(D / "[0-9]*.md"))):
        for blk in re.split(r"^=== ", re.sub(r"^:::.*\n", "", open(f).read(), flags=re.M), flags=re.M)[1:]:
            slug = blk.split("\n", 1)[0].strip()
            body = blk.split("\n---\n", 1)[1].split("\n## Sources")[0].split("\n## Research and books")[0]
            yield slug, body


def clean(t):
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)


report, totals = {}, collections.Counter()
for slug, body in pages():
    tools = CH.get(slug, {}).get("part") == "tools"
    b = clean(body)
    lines = b.splitlines()
    prose_lines = [l for l in lines if l.strip() and not l.startswith(("|", "#", "- ", "☐", "1.", "2.", "3.", "4.", "5.", "6.", "7.")) and not re.match(r"^\d+\.", l)]
    prose = "\n".join(prose_lines)
    words = max(1, len(b.split()))
    f = collections.Counter()
    for m in WORD_RX.finditer(b): f["word: " + m.group(1).lower()] += 1
    for k, rx in CPAT.items():
        n = len(rx.findall(re.sub(r'"[^"]*"', '""', b)))   # ignore quoted speech
        if n: f[k] += n
    f["dash"] = len(re.findall(r"[—–]", b))
    # one-line dramatic closers: a paragraph of 1-5 words that ends a section or follows a longer paragraph
    paras = [p.strip() for p in re.split(r"\n\s*\n", b) if p.strip() and not p.lstrip().startswith(("#", "|", "-", ">", "☐", "*This example"))]
    f["one-line closer"] = sum(1 for p in paras if len(p.split()) <= 5 and p.endswith(".") and not p.startswith("**"))
    # sayings that sound deep: short pull quotes (blockquote, not a Say box) under 18 words
    f["saying (pull quote)"] = sum(1 for q in re.findall(r"^> (?!\*\*Say)(.+)$", body, re.M) if len(q.split()) < 18 and "Say" not in q)
    # bold labels on list items
    f["bold label list item"] = len(re.findall(r"^- \*\*[^*]{2,40}\*\*", body, re.M))
    # decorative headings (Title Case over 3 words)
    for h in re.findall(r"^## (.+)$", body, re.M):
        ws = [w for w in h.split() if w[0].isalpha()]
        if len(ws) >= 4 and sum(w[0].isupper() for w in ws[1:]) >= len(ws[1:]) - 0 and len(ws[1:]) >= 3:
            f["Title Case heading"] += 1
    # heading restated in first sentence
    for h, nxt in re.findall(r"^## (.+)\n(.+)$", body, re.M):
        hw = set(re.findall(r"[a-z]{4,}", h.lower())); nw = set(re.findall(r"[a-z]{4,}", nxt.split(".")[0].lower()))
        if hw and len(nxt.split(".")[0].split()) <= 8 and len(hw & nw) / len(hw) >= 0.6:
            f["heading restated"] += 1
    # triads: "a, b and c" lists inside sentences
    f["triad"] = len(re.findall(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+(?: \w+)?[.,]", prose))
    # repeated sentence openings (3 in a row)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", " ".join(prose.split())) if len(s.split()) > 2]
    first = [s.split()[0].lower().strip('"*') for s in sents]
    f["3 openings in a row"] = sum(1 for i in range(len(first) - 2) if first[i] == first[i + 1] == first[i + 2])
    # rhythm
    lens = [len(s.split()) for s in sents]
    burst = statistics.pstdev(lens) if len(lens) > 5 else 99
    plen = [len(p.split()) for p in paras if not p.startswith(">")]
    pvar = statistics.pstdev(plen) if len(plen) > 4 else 99
    f["over 25 words"] = sum(1 for l in lens if l > 25)
    contractions = len(re.findall(r"\b\w+'(s|re|ve|ll|d|t|m)\b", b)) / words * 100
    you = len(re.findall(r"\byou(r|rs|rself)?\b", b, re.I)) / words * 100
    soft = len(SOFT_WORDS.findall(b))
    hard = sum(v for k, v in f.items() if k.startswith("word: ")) + sum(f[k] for k in PATTERNS) + f["dash"]
    score = hard / words * 1000
    report[slug] = {"words": words, "tells_per_1000": round(score, 2), "burstiness": round(burst, 1), "para_spread": round(pvar, 1),
                    "contractions_per_100": round(contractions, 1), "you_per_100": round(you, 1), "soft_words": soft,
                    "findings": dict(f), "tools": tools}
    for k, v in f.items():
        if v: totals[k.split(":")[0] if k.startswith("word:") else k] += v
    for k, v in f.items():
        if k.startswith("word: ") and v: totals[k] += v

json.dump({"pages": report, "totals": totals}, open(D / "AI-AUDIT.json", "w"), indent=1)
rows = sorted(report.items(), key=lambda x: -x[1]["tells_per_1000"])
low_burst = [s for s, r in report.items() if r["burstiness"] < 4 and not r["tools"]]
adv_burst = [s for s, r in report.items() if 4 <= r["burstiness"] < 6 and not r["tools"]]
L = ["# AI-writing audit v2", "", "Generated by `scripts/longafter-ai-audit.py`. Combined rules from seven sources (see the script header).", "",
     "## Totals across the book", "", "| Pattern | Count |", "|---|---|"]
for k, v in sorted(totals.items(), key=lambda x: -x[1]):
    if not k.startswith("word: "): L.append(f"| {k} | {v} |")
L += ["", "Words from the AI vocabulary lists: " + ", ".join(f"{k[6:]} ({v})" for k, v in totals.most_common() if k.startswith("word: ")), "",
      f"Rhythm: pages with machine-even sentence lengths (spread under 4 words): {len(low_burst)} {low_burst}. Advisory band 4-6: {len(adv_burst)}.", "",
      "## Pages, most tells first", "", "| Page | Tells per 1,000 words | Sentence spread | Paragraph spread | Contractions per 100 | Top findings |", "|---|---|---|---|---|---|"]
for s, r in rows:
    top = ", ".join(f"{k} {v}" for k, v in sorted(r["findings"].items(), key=lambda x: -x[1]) if v)[:160]
    L.append(f"| {s} | {r['tells_per_1000']} | {r['burstiness']} | {r['para_spread']} | {r['contractions_per_100']} | {top} |")
(D / "AI-AUDIT.md").write_text("\n".join(L) + "\n")
print("totals:", {k: v for k, v in totals.items() if not k.startswith("word: ")})
print("vocab:", [(k[6:], v) for k, v in totals.most_common(25) if k.startswith("word: ")])
print("median tells/1000:", statistics.median(r["tells_per_1000"] for r in report.values()),
      "| median sentence spread:", statistics.median(r["burstiness"] for r in report.values() if not r["tools"]),
      "| machine-even pages:", len(low_burst))
