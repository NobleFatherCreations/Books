#!/usr/bin/env python3
"""Voice and examples gate for a book's v5.1-style pass (owner protocol 2026-11-24, The Weighing).
   python3 scripts/book/voice-check.py content/scale-v2/01-i-b.md     -> one file, plus the book-wide name check
Fails (counted as problems): a `::: handle` left in, "Yes, it was ..." verdict lines in examples, country markers,
banned crutch words and filler transitions, the book praising itself, "judgment" outside link text, malformed
`::: tool` cards, and any character name used in examples in more than one chapter. Warns: "isn't X. It's Y" shapes
and short lesson-sounding last lines of examples (read them)."""
import re, sys
from pathlib import Path

STOP = set((Path(__file__).with_name("voice-stopwords.txt")).read_text().split())
FAIL = {
    "handle block left in (use ::: tool or a self-check question)": r"(?m)^::: handle\b",
    "country marker": r"£|\$\d|\bhalf (?:six|seven|eight|nine|ten|eleven|twelve)\b|five-a-side|housing association|\bsolicitor|\bthe council\b|Pembrokeshire|\bNHS\b|\bA&E\b|\bGP\b",
    "banned word": r"(?i)\b(delve|tapestry|testament|landscape|paradigm|symphony|beacon|crucible|nuanced?|multifaceted|pivotal|foster|elevate|unleash|unlock|harness|navigat\w*|underscore\w*|realm|embark|game-changer|cutting-edge|bustling|vibrant|resonat\w*)\b",
    "filler transition": r"(?i)\b(moreover|furthermore|additionally|consequently|indeed|notably)\b",
    "the book praising itself": r"(?i)\b(?:the most \w+ (?:\w+ )?(?:thing |test |page |tool )?in (?:this|the) book|more than any other \w+ in (?:this|the) book|the only \w+ in (?:this|the) book|the whole book has been|more than everything else in this book)",
}
WARN = {
    "isn't X. It's Y": r"(?i)\b(?:is|was|are)(?:n't| not) [^.;!?\n]{1,45}[.;] (?:It|That|They)(?:'s| is| are)\b",
}


def chapters(t):
    for c in re.split(r"(?m)^=== ", t)[1:]:
        yield c.split("\n", 1)[0].strip(), c.split("\n---\n", 1)[-1]


def scenes(body):
    return re.findall(r"(?ms)^::: scene[^\n]*\n(.*?)^:::\s*$", body)


def main():
    f = Path(sys.argv[1]); book = f.parent
    global ORDINARY
    import json
    plan = json.loads((book / "plan.json").read_text())["chapters"]
    ORDINARY = {c["slug"] for c in plan if c["part"] not in ("start", "tools")}
    probs, warns = [], []
    for slug, body in chapters(f.read_text()):
        prose = re.sub(r"(?ms)^## Sources.*", "", body)
        for name, p in FAIL.items():
            for m in re.finditer(p, prose):
                probs.append(f"{slug}: {name}: …{prose[max(0, m.start()-40):m.end()+30]!r}")
        for m in re.finditer(r"\bjudgment", re.sub(r"\[[^\]]*\]\([^)]*\)|\([^)]*\)", "", prose)):
            probs.append(f"{slug}: spelling: use 'judgement' outside link text")
        for name, p in WARN.items():
            for m in re.finditer(p, prose):
                warns.append(f"{slug}: {name}: …{prose[max(0, m.start()-30):m.end()+20]!r}")
        for s in scenes(prose):
            if re.search(r"(?i)\byes, (?:it|this|that|he|she) (?:was|really was)\b", s):
                probs.append(f"{slug}: example ends on a verdict ('Yes, it was ...'): put the verdict in the body once, end on what happened")
            last = re.split(r"(?<=[.!?])\s+", " ".join(s.split()))[-1]
            if len(last.split()) <= 8 and re.search(r"(?i)\b(that's|that is|it was|this is|is what)\b", last):
                warns.append(f"{slug}: example's last line may state the lesson: {last!r}")
        kinds = re.findall(r"(?m)^::: (tool|ask)\b", prose)
        if slug in ORDINARY and len(kinds) != 1:
            probs.append(f"{slug}: needs exactly one '::: tool' card (8 core chapters) or one '::: ask' self-check (all others); found {len(kinds)}")
        for a in re.findall(r"(?ms)^::: ask[^\n]*\n(.*?)^:::\s*$", prose):
            if not a.strip().startswith("Ask yourself:") or a.strip().count("\n"):
                probs.append(f"{slug}: '::: ask' holds one line starting 'Ask yourself:'")
        for card in re.findall(r"(?ms)^::: tool([^\n]*)\n(.*?)^:::\s*$", prose):
            lines = [l for l in card[1].strip().split("\n") if l.strip()]
            if not card[0].strip() or len(lines) != 2 or not lines[0].startswith("When ") or not lines[1].startswith("Ask yourself:"):
                probs.append(f"{slug}: tool card must be '::: tool NAME' then 'When ...' then 'Ask yourself: ...'")
    # book-wide: a character name may appear in one chapter's examples only
    seen = {}
    for p in sorted(book.glob("0*.md")):
        for slug, body in chapters(p.read_text()):
            for s in scenes(body):
                for n in set(re.findall(r"\b([A-Z][a-z]{2,})\b", s)) - STOP:
                    seen.setdefault(n, set()).add(slug)
    mine = {slug for slug, _ in chapters(f.read_text())}
    for n, where in sorted(seen.items()):
        if len(where) > 1 and where & mine:
            probs.append(f"name '{n}' used in examples in {len(where)} chapters: {', '.join(sorted(where))}")
    for w in warns:
        print("  warn", w)
    for p in probs:
        print("  FAIL", p)
    print(f"{f.name}: {len(probs)} problem(s), {len(warns)} warning(s)")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
