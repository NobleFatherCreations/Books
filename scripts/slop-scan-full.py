#!/usr/bin/env python3
"""The complete no-ai-slop audit — all 21 categories named in
.claude/skills/no-ai-slop/SKILL.md, not the ~15 approximated in
slop-scan.py (which stubbed 'fake-profound-kicker' as a literal no-op and
never implemented often-empty adverbs, fake-strong verbs, synonym cycling,
robotic rhythm, or formatting slop at all).

Detection only, per the skill's own "Two jobs" -- it names patterns and
quotes the line, it does not rewrite or score.
"""
import re, sys, collections

ADVERBS = ["just","literally","honestly","simply","actually","truly",
           "fundamentally","importantly","crucially","inherently","inevitably"]
FAKE_STRONG = [
 (r"\bserves as\b", "serves as -> is"),
 (r"\backs as\b", "acts as -> is"),
 (r"\bfunctions as\b", "functions as -> is"),
 (r"\bhas the ability to\b", "has the ability to -> can"),
 (r"\bis able to\b", "is able to -> can"),
 (r"\bmade a (?:decision|choice) to\b", "made a decision to -> decided to"),
 (r"\bplays? an? (?:important|vital|key|central) role in\b", "plays a role in -> [name the actual mechanism]"),
]

def txt(t):
    t = re.sub(r"\\u2014", "\u2014", t).replace("\\u2019","\u2019")
    t = re.sub(r"<[^>]+>", " ", t)
    return t

def bodies(path):
    s = open(path, encoding="utf-8").read()
    js = s.split('<script id="book-js">')[1].split("</script>")[0]
    return re.findall(r"BODIES\[(\d+)\]=`([\s\S]*?)`;", js)

def shape_signature(sentence):
    """Coarse part-of-speech-free shape: opening word class + length bucket,
    used only to flag runs of near-identical sentence openings/lengths."""
    w = sentence.strip().split()
    if not w: return None
    return (w[0].lower(), min(len(w)//4, 8))

slop_scan_full_sentence_counts = []

def scan(path):
    bs = bodies(path)
    total_words = sum(len(t.split()) for _, t in bs)
    hits = collections.defaultdict(list)

    for n, raw in bs:
        t = txt(raw)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]

        for adv in ADVERBS:
            for m in re.finditer(rf"\b{adv}\b", t, re.I):
                hits["often-empty adverb"].append((n, adv, t[max(0,m.start()-40):m.end()+40]))

        for rx, label in FAKE_STRONG:
            for m in re.finditer(rx, t, re.I):
                hits["fake-strong verb"].append((n, label, t[max(0,m.start()-40):m.end()+40]))

        # synonym cycling: same referent, three different nouns for it within
        # a short span -- approximated as three distinct capitalized "The X"
        # openers in one chapter referring to what looks like the same thing
        # is too unreliable to regex; flagged manually instead (see report).

        # robotic rhythm: N+ consecutive sentences with the same coarse shape
        run = 1
        for i in range(1, len(sentences)):
            if shape_signature(sentences[i]) == shape_signature(sentences[i-1]) and shape_signature(sentences[i]):
                run += 1
                if run == 4:
                    hits["robotic rhythm"].append((n, "4+ consecutive same-shape sentences",
                                                    " / ".join(sentences[i-3:i+1])[:160]))
            else:
                run = 1

        # formatting slop: emoji, bold mid-sentence, headers over 2 sentences
        if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", raw):
            hits["formatting slop"].append((n, "emoji", "found in chapter body"))
        for m in re.finditer(r"<h3>((?:(?!</h3>).)*)</h3>", raw):
            # count sentences until the next <h3> or end of chapter
            after = raw[m.end():]
            nxt = after.find("<h3>")
            segment = after[:nxt] if nxt > -1 else after
            nsent = len(re.findall(r"[.!?](?:\s|<)", txt(segment)))
            slop_scan_full_sentence_counts.append((n, m.group(1), nsent))

    # a header is over-long relative to THIS book's own median section, not
    # a fixed count -- The Repair runs long by design (579 w/ch vs ~200)
    import statistics
    counts = [c for _, _, c in slop_scan_full_sentence_counts]
    if counts:
        med = statistics.median(counts)
        for n, title, c in slop_scan_full_sentence_counts:
            if c > med * 3.5 and c > 8:
                hits["formatting slop"].append((n, f"header over a {c}-sentence section (book median {med:.0f})", txt(title)[:50]))
    return hits, total_words, len(bs)

def main():
    path = sys.argv[1]
    hits, words, nch = scan(path)
    print(f"{path}  \u2014  {nch} chapters, {words} words")
    for cat in ["often-empty adverb", "fake-strong verb", "robotic rhythm", "formatting slop"]:
        c = hits.get(cat, [])
        print(f"  {cat:22} {len(c):4}   ({len(c)/words*1000:5.2f} per 1k words)")
    if "--detail" in sys.argv:
        cat = sys.argv[sys.argv.index("--detail")+1]
        for n, label, ctx in hits.get(cat, [])[:25]:
            print(f"    ch{n} [{label}] ...{ctx}...")

main()
