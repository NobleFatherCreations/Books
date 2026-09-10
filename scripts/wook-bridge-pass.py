#!/usr/bin/env python3
"""Fifth 2026-09-10 pass: the Bridges, and the drafting artifacts that explain everything.

Auditing tone across the non-cold-open sections turned up the worst defect in
the book so far, and then the reason for it.

THE DEFECT. Sixteen of the twenty-five Bridges -- the black card at the end of
every chapter that tells the reader what is coming next -- point at the wrong
chapter. Not subtly: at the end of Chapter 20 the book says "Chapter 18 is the
briefing," sending the reader backwards into a chapter they finished two
chapters ago. Every one of them has the RIGHT CONTENT for chapter n+1 and a
stale number, so the fix is numeric in fifteen cases.

THE REASON, found in the manuscript itself. Three chapters were inserted late
-- The Road (now 11), The Free One (now 13) and The Re-Entry Window (now 20) --
and each still carries the editor's note saying where to slot it in:

    "Placement: Between Chapter 10 (The Tampon Bag) and Chapter 11 (The Batch)."

Those notes are live on the page. So is this, at the end of Chapter 6:

    "Chapters that are NEW or significantly changed from the draft version in
     the uploaded files:  Now beginning Chapter 7."

which is raw drafting handoff text sitting in a published book. Inserting
those three chapters is what shifted everything after them, and nothing that
named a chapter number was renumbered. That single event is behind every stale
count, every wrong cross-reference and every misdirected Bridge found in this
round and the three before it.

Chapter 10's Bridge is the one exception: its content teases The Batch, because
it was written before The Road was slotted in between them. It needs new
sentences, not a new number.

Also fixes Sister Lou, who is forty-nine in one Soundboard attribution and
fifty-eight everywhere else, including her own chapter.

Run: python3 scripts/wook-bridge-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# Bridges whose content already matches chapter n+1: chapter -> (stale, correct)
RENUMBER = {
    11: ("11", "12"), 12: ("12", "13"), 13: ("12", "14"), 14: ("13", "15"),
    15: ("14", "16"), 16: ("15", "17"), 17: ("16", "18"), 18: ("17", "19"),
    19: ("21", "20"),
    20: ("18", "21"), 21: ("19", "22"), 22: ("20", "23"), 23: ("21", "24"),
    24: ("22", "25"), 25: ("23", "26"),
}

# Editorial scaffolding to strip, keeping the reader-facing sentence that
# was wrapped up inside it.
PLACEMENT = [
    ("ch11", "Placement: Between Chapter 10 (The Tampon Bag) and Chapter 11 (The Batch). "
             "The gate is not the first vulnerability point. The highway is.",
             "The gate is not the first vulnerability point. The highway is."),
    ("ch13", "Placement: Between Chapter 11 (The Batch) and Chapter 12 (The Undercover). "
             "This chapter is about a trade you didn’t know you were making.",
             "This chapter is about a trade you didn’t know you were making."),
    ("ch20", "Placement: Between Chapter 17 (The Festie Hollowing) and the Intermission "
             "Before the Encore. The festival ends. The window opens. This chapter is "
             "about what lives in it.",
             "The festival ends. The window opens. This chapter is about what lives in it."),
]

applied, skipped, failed = [], [], []


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    # --- Bridges that only need renumbering -----------------------------
    for n, (stale, correct) in sorted(RENUMBER.items()):
        a, b = bounds(html, n)
        m = re.search(r'<section class="panel pp-black prose bridge">.*?</section>',
                      html[a:b], re.S)
        assert m, f"ch{n}: no bridge"
        sa, sb = a + m.start(), a + m.end()
        bridge = html[sa:sb]
        if f"Chapter {correct}" in bridge and f"Chapter {stale}" not in bridge:
            skipped.append(f"ch{n} bridge")
            continue
        hits = bridge.count(f"Chapter {stale}")
        if not hits:
            failed.append(f"ch{n} bridge: no 'Chapter {stale}' found")
            continue
        bridge = bridge.replace(f"Chapter {stale}", f"Chapter {correct}")
        html = html[:sa] + bridge + html[sb:]
        applied.append(f"ch{n} bridge: Chapter {stale} -> {correct} (x{hits})")

    # --- Chapter 10's bridge teases the wrong chapter entirely ----------
    old10 = ("Raya pulled over. Chapter 12 is the cap that cost forty dollars and the "
             "guy who did not test it and his name in a screenshot going around the "
             "festival and the Bunk Police volunteer who looks at the ground.")
    new10 = ("Raya pulled over. Chapter 11 is seven hours of I-5 with four people in one "
             "car who have four different ideas about what is in it, and an unmarked "
             "Explorer at mile marker 231 whose driver has been trained to be warm at "
             "you for exactly as long as it takes.")
    if old10 in html:
        html = html.replace(old10, new10, 1)
        applied.append("ch10 bridge: rewritten to tease The Road, not The Batch")
    elif new10 in html:
        skipped.append("ch10 bridge")
    else:
        failed.append("ch10 bridge: anchor not found")

    # --- Editorial placement notes -------------------------------------
    for label, old, keep in PLACEMENT:
        if old in html:
            html = html.replace(old, keep, 1)
            applied.append(f"{label}: stripped editor's Placement note, kept the line")
        elif keep in html and old not in html:
            skipped.append(f"{label} placement")
        else:
            failed.append(f"{label} placement note: anchor not found")

    # --- Raw drafting handoff text, live on the page --------------------
    draft = ("<p>Chapters that are NEW or significantly changed from the draft version "
             "in the uploaded files:</p><p>Now beginning Chapter 7.</p>")
    if draft in html:
        html = html.replace(draft, "", 1)
        applied.append("ch6: removed drafting handoff text from the published page")
    else:
        skipped.append("ch6 drafting artifact")

    # --- Sister Lou is fifty-eight -------------------------------------
    lou = "Sister Lou Mantilla, forty-nine, founding member of the sober crew protocol"
    if lou in html:
        html = html.replace(lou, "Sister Lou Mantilla, fifty-eight, founding member of "
                                 "the sober crew protocol", 1)
        applied.append("ch16: Sister Lou 49 -> 58, matching her own chapter")
    else:
        skipped.append("Sister Lou age")

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
        print(f"\nskipped {len(skipped)} (already applied)")


if __name__ == "__main__":
    sys.exit(main())
