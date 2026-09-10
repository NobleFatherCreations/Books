#!/usr/bin/env python3
"""Fourth 2026-09-10 pass: the name collisions, and the sentence one of them broke.

scripts/wook-continuity-check.py flagged Dani and Marcus as each doing duty
for four unrelated characters. Reading those out chapter by chapter turned up
two more (Nadia x3, Sam x3) and one genuinely broken sentence.

The broken sentence is the reason this matters beyond tidiness. Chapter 2 has
two different Marcuses INSIDE ONE CHAPTER -- the silent Sprinter driver and
Marcus Veld, the man running the twenty-five-thousand-dollar pitch -- and a
later Track collapsed under the ambiguity into:

    "Marcus's Marcus gives the opened drink before he mentions twenty-five."

which is not a sentence. It sits in a parallel construction (Hopper feeds
Daniel before the tank; Rex books the Sprinter) and the drink is Rex's -- he
hands her the already-opened Topo Chico -- so the true version names both men.

Which name survives, and why:
  Marcus  -> Marcus Veld keeps it. He is central to ch2 and is researched by
             name in that chapter's Save.
  Dani    -> ch4's keeps it. She is the one who delivers the hard truth about
             Kai's pattern; the other three are walk-ons.
  Nadia   -> ch3's Okafor and ch10's Chen both keep it. Both have surnames,
             and ch16 refers back to Chen by first name. ch20's is a walk-on.
  Sam     -> ch12's keeps it. He is the vetted source the whole Save turns on.
  River   -> left alone deliberately. ch4 jokes that River is the kind of
             name that sounds "less like a name and more like a brand of
             mushroom jerky," which makes the repetition a feature.

Run: python3 scripts/wook-name-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# chapter -> [(old, new, why)]
RENAMES = {
    1:  [("Dani", "Tamsin", "Priya's friend; ch4's Dani is the keeper")],
    11: [("Marcus", "Emmett", "Save protagonist; ch2's Marcus Veld is the keeper"),
         ("Sam", "Bode", "Leila's college friend; ch12's Sam is the keeper")],
    12: [("Marcus", "Deon", "Maddie's boyfriend; ch2's Marcus Veld is the keeper")],
    16: [("Marcus", "Wes", "one of the searching friends"),
         ("Dani", "Rosa", "Yusuf's friend, the one who photographs her wristband"),
         ("Sam", "Hal", "the friend whose phone dies")],
    20: [("Nadia", "Ines", "walk-on; ch3 Okafor and ch10 Chen both keep the name")],
    22: [("Dani", "Junie", "the friend who sends the voice notes")],
}

# Global edits that are not chapter-scoped renames.
EDITS = [
    # ch2's silent driver, so the chapter stops having two Marcuses.
    ("ch2: Sprinter driver Marcus -> Boyd",
     "driven by a guy named Marcus who does not talk",
     "driven by a guy named Boyd who does not talk"),

    # The sentence the collision broke. Rex hands over the opened drink;
    # Marcus makes the ask.
    ("ch2: repair 'Marcus's Marcus' sentence",
     "Marcus’s Marcus gives the opened drink before he mentions twenty-five.",
     "Rex gives the opened drink before Marcus mentions twenty-five."),

    # ch21 credits the wristband photo to ch16's Save character, renamed above.
    ("ch21: wristband credit Dani -> Rosa",
     "By Dani photographing the wristband",
     "By Rosa photographing the wristband"),
]

applied, skipped, failed = [], [], []


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    # Straight edits first -- the ch2 driver rename has to happen before the
    # chapter-scoped Marcus logic would otherwise see two different people.
    for label, old, new in EDITS:
        if old in html:
            assert html.count(old) == 1, f"{label}: {html.count(old)} matches"
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new in html:
            skipped.append(label)
        else:
            failed.append(label)

    for n, pairs in sorted(RENAMES.items()):
        a, b = bounds(html, n)
        chunk = html[a:b]
        for old, new, why in pairs:
            hits = len(re.findall(r'\b' + re.escape(old) + r'\b', chunk))
            if not hits:
                if re.search(r'\b' + re.escape(new) + r'\b', chunk):
                    skipped.append(f"ch{n}: {old} -> {new}")
                else:
                    failed.append(f"ch{n}: {old} -> {new} (neither name present)")
                continue
            chunk = re.sub(r'\b' + re.escape(old) + r'\b', new, chunk)
            applied.append(f"ch{n}: {old} -> {new} (x{hits}) — {why}")
        html = html[:a] + chunk + html[b:]

    if failed:
        print("FAILED:")
        for f in failed:
            print(f"  ! {f}")
        return 1

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes\n")
    print(f"applied {len(applied)}:")
    for a_ in applied:
        print(f"  + {a_}")
    if skipped:
        print(f"\nskipped {len(skipped)} (already applied):")
        for s in skipped:
            print(f"  = {s}")


if __name__ == "__main__":
    sys.exit(main())
