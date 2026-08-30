#!/usr/bin/env python3
"""Scan a book's chapter bodies for the AI-slop patterns in .claude/skills/no-ai-slop.

Reports counts and located examples. Detection only -- it never rewrites.
Usage: slop-scan.py books/<slug>/index.html [--list PATTERN]
"""
import re, sys, collections

BANNED_WORDS = r"delve|foster|leverage|utilize|utilise|facilitate|empower|streamline|robust|cutting-edge|paradigm shift|game changer|tapestry|realm|beacon|multifaceted|meticulous|intricate|paramount|transformative|elevate|embark|supercharge|harness|ever-evolving"
EMPTY_PHRASES = r"it's worth noting|it is worth noting|it's important to note|at the end of the day|at its core|in today's world|in the age of|in the world of|the reality is|the truth is|going forward|let's dive in"

PATTERNS = [
 ("em-dash",              r"\\u2014|—"),
 ("banned-word",          rf"\b({BANNED_WORDS})\b"),
 ("empty-phrase",         rf"({EMPTY_PHRASES})"),
 ("binary-contrast",      r"(?:isn't|is not|aren't|are not|wasn't|it's not just|not merely)\s+[^.;]{2,60}?[.;]\s*(?:It's|It is|They're|That's|Its)\b"),
 ("throat-clearing",      r"(?:^|[.\s>])(Here's the thing|Here's what I mean|Let me be clear|I'll be honest|The uncomfortable truth is|Here's a fact|Here is a fact)"),
 ("faux-insight",         r"(most people (?:never|don't|skip)|what most people get wrong|nobody tells you|the part everyone misses|and one of the least discussed|least discussed)"),
 ("colon-reveal",         r"<p>[A-Z][^.<]{5,70}:\s+[a-z]"),
 ("superficial-analysis", r",\s+(highlighting|underscoring|reflecting|showcasing|demonstrating that)\b"),
 ("importance-puffery",   r"(stands as a testament|marks a pivotal|plays a vital role|solidifies its|underscores its significance|cannot be overstated)"),
 ("metadiscourse",        r"(that (?:last )?part matters more than it sounds|the key point is|as you can see|this distinction matters|in other words|it bears repeating|worth (?:knowing|saying) (?:in advance|again))"),
 ("weasel-attribution",   r"(experts agree|industry reports suggest|many argue|widely regarded as|studies show|research (?:shows|proves)|it is well documented|well documented)"),
 ("negative-listing",     r"(?:^|>|\.\s)Not (?:a|an|the|just)\s[^.]{3,60}\.\s*(?:Not|A|An|The)\s"),
 ("dramatic-fragment",    r"(That's it\.|That's the whole thing\.|And that's|Full stop\.)"),
 ("rhetorical-setup",     r"(What if I told you|Think about it:|Plot twist:|Ask yourself:)"),
 ("summary-recap",        r"(?:^|>|\.\s)(In conclusion|Ultimately|Overall|To sum up|All in all)\b"),
 ("fake-profound-kicker", r"</p>\s*$"),   # placeholder, handled separately
 ("exclamation",          r"!"),
]

def bodies(path):
    s = open(path, encoding="utf-8").read()
    js = s.split('<script id="book-js">')[1].split("</script>")[0]
    return re.findall(r"BODIES\[(\d+)\]=`([\s\S]*?)`;", js)

def main():
    path = sys.argv[1]
    only = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--list" else None
    bs = bodies(path)
    counts = collections.Counter()
    hits = collections.defaultdict(list)
    for n, b in bs:
        for name, rx in PATTERNS:
            if name == "fake-profound-kicker":
                continue
            for m in re.finditer(rx, b, re.I):
                counts[name] += 1
                ctx = b[max(0, m.start()-70):m.end()+70].replace("\n", " ")
                hits[name].append((int(n), ctx.strip()))
    total_words = sum(len(b.split()) for _, b in bs)
    print(f"{path}  —  {len(bs)} chapters, {total_words} words")
    print("-" * 76)
    for name, _ in PATTERNS:
        if name == "fake-profound-kicker":
            continue
        c = counts[name]
        if not c:
            continue
        per_k = c / total_words * 1000
        print(f"  {name:22} {c:5}   ({per_k:5.2f} per 1k words)")
    if only:
        print()
        print(f"### {only}")
        for n, ctx in hits[only]:
            print(f"  ch{n}: ...{ctx}...")

main()
