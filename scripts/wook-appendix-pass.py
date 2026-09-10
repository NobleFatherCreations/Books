#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eleventh 2026-09-10 pass: the Appendix A-Z audit.

Cross-checked every "(ChN)" and "From Chapter N" tag across all 26 appendices
against ground truth extracted directly from the live book -- every counter-
drop's real chapter (the <p class="cd-name"> inside each Track) and every
Track title's real chapter. 60 of 115 tagged entries in Appendix F alone were
wrong.

THE PATTERN. Nearly every wrong tag decodes cleanly against a single shift
table, which is the same three-chapter-insertion bug (The Road at 11, The
Free One at 13, The Re-Entry Window at 20) found in every previous round --
except this time in content that was apparently never touched by any of the
five earlier passes, because those all worked on Bridges and body text, and
never opened the appendices.

    old label 1-10   -> unchanged
    old label 11      -> +1  (12)
    old label 12-17   -> +2  (14-19)
    old label 18-21   -> +3  (21-24)

Verified against Appendix F's counter-drop tags via ground truth (60/60
mismatches decode to this table or to one of two plain transcription errors
unrelated to it), then confirmed independently against Appendix G's discography
(10/10 chapter labels), and against content matching for every single-topic
appendix (K, N, O, P, R, W, Y) whose "From Chapter N" claim was checked against
what that chapter's Tracks actually contain.

THE CONFESSION ITSELF (ch23, id=wook-confession) had one leftover instance of
the older "twenty chapters" phrasing sitting two sentences after its own
already-corrected "twenty-two chapters" (fixed in an earlier round) -- a
duplicate of the same bug that survived because the earlier pass matched a
different exact string.

Run: python3 scripts/wook-appendix-pass.py   (idempotent)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# ---- 1. simple exact-string edits, global (each anchor is unique in the book) ----
SIMPLE_EDITS = [
    ("confession: vow iterations 20 -> 22, matching 'twenty-two chapters together' two sentences earlier",
     "By Chapter 23, you have made twenty iterations of the vow.",
     "By Chapter 23, you have made twenty-two iterations of the vow."),
    ("confession: 'used...on you for twenty chapters' -> twenty-two",
     "I have used the book’s persuasion techniques on you for twenty chapters.",
     "I have used the book’s persuasion techniques on you for twenty-two chapters."),
    ("apD: 'six' Safety Appendixes -> nine (9 through 17 inclusive is nine chapters, not six)",
     "All six Safety Appendixes consolidated. Chapters 9\u201317.",
     "All nine Safety Appendixes consolidated. Chapters 9\u201317."),
    ("apC: Tour-Bus Captivity is Ch17's track, not Ch15's",
     "Insta-Wook Bond + Tour-Bus Captivity (Ch2 + Ch15)",
     "Insta-Wook Bond + Tour-Bus Captivity (Ch2 + Ch17)"),
    ("apK: relabeled from Chapter 18 to Chapter 21",
     "🚨 APPENDIX K — The Anchor System And Bill Of Rights</h2><p>From Chapter 18.",
     "🚨 APPENDIX K — The Anchor System And Bill Of Rights</h2><p>From Chapter 21."),
    ("apN: relabeled from Chapter 16 to Chapter 18",
     "⚖ APPENDIX N — The Long Exit Protocol</h2><p>From Chapter 16.",
     "⚖ APPENDIX N — The Long Exit Protocol</h2><p>From Chapter 18."),
    ("apO: relabeled from Chapter 19 to Chapter 22, and its orphaned icon "
     "(a bare variation-selector left over after the base emoji was "
     "stripped somewhere along the way) replaced with a real one",
     "️ APPENDIX O — The Timeline Of Recovery</h2><p>From Chapter 19.",
     "\U0001f4c8 APPENDIX O — The Timeline Of Recovery</h2><p>From Chapter 22."),
    ("apP: relabeled from Chapter 21 to Chapter 24",
     "🚪 APPENDIX P — The Community Accountability Compact Template</h2><p>From Chapter 21.",
     "🚪 APPENDIX P — The Community Accountability Compact Template</h2><p>From Chapter 24."),
    ("apR: relabeled from Chapter 19 to Chapter 22, and its orphaned icon "
     "replaced with a real one",
     "️ APPENDIX R — The Five-Sense Ground</h2><p>From Chapter 19.",
     "\U0001f9ed APPENDIX R — The Five-Sense Ground</h2><p>From Chapter 22."),
    ("apW: relabeled from Chapter 21 to Chapter 24",
     "📖 APPENDIX W — The Institutional Betrayal Diagnostic</h2><p>From Chapter 21.",
     "📖 APPENDIX W — The Institutional Betrayal Diagnostic</h2><p>From Chapter 24."),
    ("apY: relabeled from Chapter 21 to Chapter 24",
     "🔁 APPENDIX Y — The Immune System Infrastructure Checklist</h2><p>From Chapter 21.",
     "🔁 APPENDIX Y — The Immune System Infrastructure Checklist</h2><p>From Chapter 24."),
]

# ---- 2. Appendix F: every "(ChN)" counter-drop tag, verified against the
# live book's own <p class="cd-name"> markup (or, for the six entries that
# aren't formatted as a numbered counter-drop, against the chapter that
# actually names them). old -> new. ----
APF_TAGS = [
    ("The Apology Architecture (Ch20)", "The Apology Architecture (Ch23)"),
    ("The Camp Hardening Protocol (Ch13)", "The Camp Hardening Protocol (Ch15)"),
    ("The Chain Audit (Ch11)", "The Chain Audit (Ch12)"),
    ("The Closed-Door Audit (Ch20)", "The Closed-Door Audit (Ch23)"),
    ("The Community Compact (Ch21)", "The Community Compact (Ch24)"),
    ("The Compassionate Distance Protocol (Ch6)", "The Compassionate Distance Protocol (Ch2)"),
    ("The Cross-Circuit Check (Ch21)", "The Cross-Circuit Check (Ch24)"),
    ("The Deal-In-The-Open Protocol (Ch13)", "The Deal-In-The-Open Protocol (Ch15)"),
    ("The Direct Verification Protocol (Ch13)", "The Direct Verification Protocol (Ch15)"),
    ("The Documented Concern Protocol (Ch21)", "The Documented Concern Protocol (Ch24)"),
    ("The Duty Decoupler (Ch16)", "The Duty Decoupler (Ch18)"),
    ("The Emergency Card (Ch14)", "The Emergency Card (Ch16)"),
    ("The Exit Cost Audit (Ch16)", "The Exit Cost Audit (Ch18)"),
    ("The Exit Interview Protocol (Ch16)", "The Exit Interview Protocol (Ch18)"),
    ("The Five-Sense Ground (Ch19)", "The Five-Sense Ground (Ch22)"),
    ("The Friction Introduction (Ch4)", "The Friction Introduction (Ch2)"),
    ("The Friction Test (Ch15)", "The Friction Test (Ch17)"),
    ("The Full Accountability Checklist (Ch11)", "The Full Accountability Checklist (Ch12)"),
    ("The Gate Briefing (Ch18)", "The Gate Briefing (Ch21)"),
    ("The Ground-Laying Protocol (Ch19)", "The Ground-Laying Protocol (Ch22)"),
    ("The Honest Inventory (Ch20)", "The Honest Inventory (Ch23)"),
    ("The Identity Inventory (Ch17)", "The Identity Inventory (Ch19)"),
    ("The Lane-Clear Protocol (Ch15)", "The Lane-Clear Protocol (Ch17)"),
    ("The Loss Inventory (Ch19)", "The Loss Inventory (Ch22)"),
    ("The Mirror Check (Ch20)", "The Mirror Check (Ch23)"),
    ("The Named Plan (Ch14)", "The Named Plan (Ch16)"),
    ("The Named Threshold Protocol (Ch14)", "The Named Threshold Protocol (Ch16)"),
    ("The Napkin Protocol (Ch16)", "The Napkin Protocol (Ch18)"),
    ("The Open-Space Requirement (Ch13)", "The Open-Space Requirement (Ch15)"),
    ("The Own-Source Discipline (Ch15)", "The Own-Source Discipline (Ch17)"),
    ("The Parallel-Track Protocol (Ch21)", "The Parallel-Track Protocol (Ch24)"),
    ("The Plus-One Protocol (Ch13)", "The Plus-One Protocol (Ch15)"),
    ("The Recall Play (Ch11)", "The Recall Play (Ch12)"),
    ("The Regular Source Audit (Ch15)", "The Regular Source Audit (Ch17)"),
    ("The Reporting Pathway Audit (Ch21)", "The Reporting Pathway Audit (Ch24)"),
    ("The Role Audit (Ch11)", "The Role Audit (Ch12)"),
    ("The Roster Exit (Ch21)", "The Roster Exit (Ch24)"),
    ("The Run Independence Plan (Ch15)", "The Run Independence Plan (Ch17)"),
    ("The Scene-Root Check (Ch12)", "The Scene-Root Check (Ch14)"),
    ("The Sister Lou Briefing (Ch14/18)", "The Sister Lou Briefing (Ch16)"),
    ("The Smaller Season Experiment (Ch17)", "The Smaller Season Experiment (Ch19)"),
    ("The Sober Monday Rule (Ch15)", "The Sober Monday Rule (Ch17)"),
    ("The Somatic Inventory (Ch19)", "The Somatic Inventory (Ch22)"),
    ("Source-Before-Signal Protocol (Ch21) · The Source-Before-Signal Protocol (Ch21)",
     "The Source-Before-Signal Protocol (Ch24)"),
    ("The Spiral Interruption Protocol (Ch19)", "The Spiral Interruption Protocol (Ch22)"),
    ("The Spillover Ground (Ch19)", "The Spillover Ground (Ch22)"),
    ("The Three-Minute Gate (Ch11)", "The Three-Minute Gate (Ch12)"),
    ("The Translation Exercise (Ch17)", "The Translation Exercise (Ch19)"),
    ("The Tuesday-By-Tuesday Plan (Ch16)", "The Tuesday-By-Tuesday Plan (Ch18)"),
    ("The Tuesday Reconstruction (Ch17)", "The Tuesday Reconstruction (Ch19)"),
    ("The Two-Ask Ceiling (Ch12)", "The Two-Ask Ceiling (Ch14)"),
    ("The Van Rule (Ch15)", "The Van Rule (Ch17)"),
    ("The Verify-Or-Decline Protocol (Ch12)", "The Verify-Or-Decline Protocol (Ch14)"),
    ("The Voice Attribution Protocol (Ch19)", "The Voice Attribution Protocol (Ch22)"),
    ("The Walk-Through Protocol (Ch21)", "The Walk-Through Protocol (Ch24)"),
]

# ---- 3. Appendix G: the discography labels, same shift table ----
APG_TAGS = [
    ('<strong class="lead">Ch21:</strong>', '<strong class="lead">Ch24:</strong>'),
    ('<strong class="lead">Ch20:</strong>', '<strong class="lead">Ch23:</strong>'),
    ('<strong class="lead">Ch19:</strong>', '<strong class="lead">Ch22:</strong>'),
    ('<strong class="lead">Ch17:</strong>', '<strong class="lead">Ch19:</strong>'),
    ('<strong class="lead">Ch16:</strong>', '<strong class="lead">Ch18:</strong>'),
    ('<strong class="lead">Ch15:</strong>', '<strong class="lead">Ch17:</strong>'),
    ('<strong class="lead">Ch14:</strong>', '<strong class="lead">Ch16:</strong>'),
    ('<strong class="lead">Ch13:</strong>', '<strong class="lead">Ch15:</strong>'),
    ('<strong class="lead">Ch12:</strong>', '<strong class="lead">Ch14:</strong>'),
    ('<strong class="lead">Ch11:</strong>', '<strong class="lead">Ch12:</strong>'),
]

# ---- 4. Appendix Q: full resync with the live Confession (ch23) ----
APQ_OLD = (
    '<h2 class="zine-h sm">\U0001f5d3 APPENDIX Q — The Seventeen Moves</h2>'
    '<p>From Chapter 22. The book’s own persuasion operations, named.</p>'
    '<p>1. The Reciprocity Hook In The Disclaimer</p>'
    '<p>2. The Authority + Vivid Imagery In Chapter 1’s Cold Open</p>'
    '<p>3. The Scarcity Of The Command</p>'
    '<p>4. The Halo Of The Named Thinkers</p>'
    '<p>5. The Trauma Tax Charged In The Cold Opens</p>'
    '<p>6. The Sober Tuesday Anchoring</p>'
    '<p>7. The Pattern Confirmation Loop (Chapters 6–10)</p>'
    '<p>8. The Archetype Liking Bait (Chapters 11–16)</p>'
    '<p>9. The Commitment Escalation (Chapters 17–20)</p>'
    '<p>10. The Recurring-Cast Familiarity Engine</p>'
    '<p>11. The Watermelon Moment As Catharsis Manufacturing</p>'
    '<p>12. The Field Reports’ Identity Rotation As Inclusion Currency</p>'
    '<p>13. The Counter-Drops’ Action Bias</p>'
    '<p>14. The <mark class="mk-t">Kandi</mark> Trade Vows As Group Identification</p>'
    '<p>15. The Sunrise Sets As Sermon</p>'
    '<p>16. The Meta-Confession As Final Reciprocity Reset</p>'
)
APQ_NEW = (
    '<h2 class="zine-h sm">\U0001f5d3 APPENDIX Q — The Sixteen Moves</h2>'
    '<p>From Chapter 23. The book’s own persuasion operations, named.</p>'
    '<p>1. The Reciprocity Hook In The Disclaimer</p>'
    '<p>2. The Authority + Vivid Imagery In Chapter 1’s Cold Open</p>'
    '<p>3. The Halo Of The Named Thinkers</p>'
    '<p>4. The Trauma Tax Charged In The Cold Opens</p>'
    '<p>5. The Scarcity Of Specific Protocols</p>'
    '<p>6. The Sober Tuesday Anchoring</p>'
    '<p>7. The Pattern Confirmation Loop (Chapters 6–10)</p>'
    '<p>8. The Archetype Liking Bait</p>'
    '<p>9. The Commitment Escalation</p>'
    '<p>10. The Recurring-Cast Familiarity Engine</p>'
    '<p>11. The Watermelon Moment As Catharsis Manufacturing</p>'
    '<p>12. The Field Reports’ Identity Rotation As Inclusion Currency</p>'
    '<p>13. The Counter-Drops’ Action Bias</p>'
    '<p>14. The <mark class="mk-t">Kandi</mark> Trade Vows As Group Identification</p>'
    '<p>15. The Sunrise Sets As Sermon</p>'
    '<p>16. The Meta-Confession As Final Reciprocity Reset</p>'
)

# ---- 5. Appendix B: the cast, rebuilt from this session's own verified
# Soundboard-chapter extraction rather than the appendix's stale numbers ----
APB_OLD = (
    'Appears in Chapters 1 (Oracle), 11 (Oracle). His signal: '
    '“Tell me what was in it. We can still help if we move now.”</p>'
    '<p>Sister Lou Mantilla — Lourdes Mantilla. Fifty-eight. Twenty-three years in recovery. Wharf Rats founding '
    'member at three regional circuits. Running the fifteen-minute briefing for eleven years without a '
    'missing-friend incident. Appears in Chapters 14 (Oracle), 18 (Full protagonist — the gate briefing). '
    'Her signal: the click of the pen.</p>'
    '<p>Mara “Hot Water” Delgado — Forty-seven. Harm-reduction auntie, ex-flow artist, ICSA-affiliated counselor. '
    'Seventeen years sitting with the long after. Appears in Chapters 4 (Oracle), 6 (Oracle), 19 (Oracle — third '
    'and final). Her signal: the electrolyte pack and the lack of judgment.</p>'
    '<p>Beans — No legal name given in the book. Twenty-three at final appearance. Auntie’s cold brew operation '
    'across seven festivals and three farmers markets. Has identified four undercover officers on instinct. Has '
    'his own small inventory item he ran the protocol on. Appears in Chapters 8 (vendor row witness), 12 '
    '(Oracle — no-scuff boots), 13 (Save witness), 15 (Oracle — second appearance), 23 (Oracle — final '
    'appearance). His signal: the granola bar and the specific gaze.</p>'
    '<p>Spool / Indigo Marchetti — Forty-one. Ten years on the lot with the wooden tray and the moonstone '
    'pendants. Never given her playa name to a doctor. Appears in Chapters 8 (Oracle), 15 (minor appearance), '
    '17 (Oracle). Her signal: “Price it like rent is due Tuesday. Because it is.”</p>'
    '<p>Yo-Yo Brennan — Yolanda Brennan. Forty-three. Twelve years running harm-reduction and camp kitchens. '
    'Dish gloves. Chapters 5 (Oracle), 6 (minor). Her signal: the look that ends the “I’m just generous” '
    'sentence.</p>'
    '<p>Nina “Patchbay” Alvarez — Forty-one. Stage manager, clipboard, zero patience for credential fraud. '
    'Chapters 2 (Oracle), 9 (minor reference). Her signal: the NICE IS NOT THE SAME THING AS SAFE sign.</p>'
)
APB_NEW = (
    'Appears in Chapters 1 (Oracle), 12 (Oracle), 24 (part of the collective). His signal: '
    '“Tell me what was in it. We can still help if we move now.”</p>'
    '<p>Sister Lou Mantilla — Lourdes Mantilla. Fifty-eight. Twenty-three years in recovery. Wharf Rats founding '
    'member at three regional circuits. Running the fifteen-minute briefing for eleven years without a '
    'missing-friend incident. Appears in Chapters 16 (Oracle), 21 (Full protagonist — the gate briefing), 24 '
    '(part of the collective). Her signal: the click of the pen.</p>'
    '<p>Mara “Hot Water” Delgado — Forty-seven. Harm-reduction auntie, ex-flow artist, ICSA-affiliated counselor. '
    'Seventeen years sitting with the long after. Appears in Chapters 4 (Oracle), 13 (Oracle), 18 (Oracle), 22 '
    '(Oracle — fourth and final). Her signal: the electrolyte pack and the lack of judgment.</p>'
    '<p>Beans — No legal name given in the book. Twenty-three at final appearance. Auntie’s cold brew operation '
    'across seven festivals and three farmers markets. Has identified four undercover officers on instinct. Has '
    'his own small inventory item he ran the protocol on. Appears in Chapters 8 (vendor row witness), 14 '
    '(Oracle — no-scuff boots), 15 (Save witness), 17 (Oracle — second appearance), 23 (Oracle), 26 (Oracle — '
    'final appearance). His signal: the granola bar and the specific gaze.</p>'
    '<p>Spool / Indigo Marchetti — Forty-one. Ten years on the lot with the wooden tray and the moonstone '
    'pendants. Never given her playa name to a doctor. Appears in Chapters 8 (Oracle), 19 (Oracle), 24 (part of '
    'the collective). Her signal: “Price it like rent is due Tuesday. Because it is.”</p>'
    '<p>Yo-Yo Brennan — Yolanda Brennan. Forty-three. Twelve years running harm-reduction and camp kitchens. '
    'Dish gloves. Chapters 5 (Oracle), 6 (minor), 24 (part of the collective). Her signal: the look that ends '
    'the “I’m just generous” sentence.</p>'
    '<p>Nina “Patchbay” Alvarez — Forty-one. Stage manager, clipboard, zero patience for credential fraud. '
    'Chapters 2 (Oracle), 15 (minor reference), 24 (part of the collective). Her signal: the NICE IS NOT THE '
    'SAME THING AS SAFE sign.</p>'
)


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    # The apG relabel walks the same "Ch11:"-style token through several
    # values in one run (e.g. old-17 becomes new-19, which is also the
    # *target* of a different rule) -- safe done once in descending order,
    # but not safe to run a second time, since "Ch19:" now means something
    # else. Guard on the whole pass instead of trying to make that step
    # re-run-safe.
    if "APPENDIX Q — The Sixteen Moves" in html:
        print("already applied (apQ already resynced to Chapter 23 / Sixteen Moves) -- nothing to do")
        return 0

    applied, skipped, failed = [], [], []

    for label, old, new in SIMPLE_EDITS:
        if old in html:
            assert html.count(old) == 1, "%s: %d matches" % (label, html.count(old))
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new in html:
            skipped.append(label)
        else:
            failed.append(label)

    for old, new in APF_TAGS:
        label = "apF: " + old
        if old in html:
            assert html.count(old) == 1, "%s: %d matches" % (label, html.count(old))
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new in html:
            skipped.append(label)
        else:
            failed.append(label)

    for old, new in APG_TAGS:
        label = "apG: " + old
        if old in html:
            assert html.count(old) == 1, "%s: %d matches" % (label, html.count(old))
            html = html.replace(old, new, 1)
            applied.append(label)
        elif new in html:
            skipped.append(label)
        else:
            failed.append(label)

    if APQ_OLD in html:
        assert html.count(APQ_OLD) == 1
        html = html.replace(APQ_OLD, APQ_NEW, 1)
        applied.append("apQ: full resync with ch23 Confession (title, chapter, 16-item list)")
    elif APQ_NEW in html:
        skipped.append("apQ resync")
    else:
        failed.append("apQ resync: anchor not found")

    if APB_OLD in html:
        assert html.count(APB_OLD) == 1
        html = html.replace(APB_OLD, APB_NEW, 1)
        applied.append("apB: cast chapter numbers rebuilt from verified Soundboard data")
    elif APB_NEW in html:
        skipped.append("apB rebuild")
    else:
        failed.append("apB rebuild: anchor not found")

    if failed:
        print("FAILED:")
        for f in failed:
            print("  ! " + f)
        return 1

    WOOK.write_text(html, errors="surrogateescape")
    print("wook: %s -> %s bytes\n" % (format(before, ","), format(len(html), ",")))
    print("applied %d:" % len(applied))
    for a in applied:
        print("  + " + a)
    if skipped:
        print("\nskipped %d (already applied)" % len(skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
