#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ninth 2026-09-10 pass: rotate SOBER TUESDAY off the office, one card per
flagged chapter.

From content/wook-audits/wook-book-wide-additions.md, Part C. 96 of 139
Sober Tuesday cards are set in an office; the rule is capping the office at
one card in three, rotating the rest through venues the book hadn't used
(a landlord, a car dealership, a church committee, an HOA board, a family
dinner). This pass rotates the single most cliche HR/company card in each of
the fourteen chapters the audit flagged by corporate-noun density -- a first,
real pass at the rule, not the full ~40-card rotation the audit sketched;
the remaining office cards in these chapters stay as they are.

Exact string match, scoped to each chapter's bounds so identical phrasing
elsewhere in the book can't collide.

Run: python3 scripts/wook-tuesday-rotation-pass.py   (idempotent)
"""
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

# chapter -> (old exact text, new text, label)
ROTATIONS = {
 5: (
  "The manager who controls the schedule and “just happens” to give the best shifts to the people who do not complain about the manager. The supply is desirable shifts. The price is compliance. The leverage is called management.",
  "The landlord who controls which unit comes open next and “just happens” to move fastest for the tenants who never call about the leak. The supply is a better apartment. The price is silence. The leverage is called management.",
  "ch5 T6 The Plug Leverage: office -> landlord",
 ),
 6: (
  "“I feel like you’re not creating a safe space for me to share my concerns.” Said in a performance review where the concern is “your work needs to improve.” The vocabulary redefined the conversation as a trauma response rather than a feedback session.",
  "“I feel like you’re not creating a safe space for me to share my concerns.” Said at a family dinner where the concern is that you brought up something that actually happened. The vocabulary redefined the conversation as a trauma response instead of the accountability conversation it was.",
  "ch6 T2 Holding Space Hostage: performance review -> family dinner",
 ),
 7: (
  "The organization that has a beautifully worded DEI statement, a values page on its website, and a HR complaint process that routes directly back to the manager who is the subject of the complaint. The vocabulary is real. The structure makes the vocabulary impossible to use. That is the mask in an org chart.",
  "The nonprofit board that has a beautifully worded mission statement, a values page on its website, and a grievance process that routes directly back to the executive director who is the subject of the complaint. The vocabulary is real. The structure makes the vocabulary impossible to use. That is the mask in an org chart.",
  "ch7 T6 PLUR Mask, Toxic Camp: company DEI -> nonprofit board",
 ),
 8: (
  "The employment contract with a non-compete clause that covers your entire professional field for two years, drafted by the company’s own attorney, reviewed by no one on your behalf, signed on your first day when you needed the job too much to negotiate. Same document. Different font.",
  "The car loan with a prepayment-penalty clause that costs more than the interest it's replacing, drafted by the dealership's own finance office, reviewed by no one on your behalf, signed at hour three on the lot when you needed to leave too badly to read. Same document. Different font.",
  "ch8 T3 LLC Trapdoor: employment contract -> car loan",
 ),
 10: (
  "The new employee asked to sign off on something that is above their pay grade by a manager who does not want their own name on the document. “Can you just process this one?” The exposure travels down the hierarchy. The decision was made before the ask.",
  "The new son-in-law asked to store something in his garage by a father-in-law who does not want it under his own roof. “Can you just hold onto this for a bit?” The exposure travels down the family tree. The decision was made before the ask.",
  "ch10 T1 Borrowed Mule: new employee -> son-in-law",
 ),
 12: (
  "The company that says it treats its workers fairly — pays market rate, provides benefits — and therefore does not need to address the safety culture in the warehouse. The fair compensation is real. The safety accountability is also required. They are not the same thing.",
  "The gym that says it treats its members fairly — clean equipment, friendly staff — and therefore does not need to fix the emergency exit that has been chained shut for a year. The friendliness is real. The safety accountability is also required. They are not the same thing.",
  "ch12 T5 Forty-A-Cap Reframe: company/warehouse -> gym",
 ),
 13: (
  "The manager who remembers every favor and references them at performance review. The relationship where the gifts were always tracked. The moment you realize the warmth had a receipt attached to every instance of it.",
  "The uncle who remembers every favor and references them at every family gathering for the next decade. The relationship where the gifts were always tracked. The moment you realize the warmth had a receipt attached to every instance of it.",
  "ch13 T3 Reciprocity Ratchet: manager/review -> uncle/family",
 ),
 15: (
  "The job candidate referred by a colleague who met them at a conference two years ago and describes them as “great.” The “great” is a conference impression. The hire is a full-time employment commitment. The gap between the data and the decision is the chain.",
  "The babysitter referred by a neighbor who met her once at a block party two summers ago and describes her as “so sweet.” The “sweet” is a five-minute impression. The hire is unsupervised time with your kids. The gap between the data and the decision is the chain.",
  "ch15 T2 Friend-of-a-Friend Chain: job candidate -> babysitter",
 ),
 17: (
  "The IT department that centralizes all access management so that any new software, any new device, any new service requires their approval and their setup — so that the organizational dependency on their function becomes total and the function becomes immune to question. “I got you” as an organizational control mechanism. Works the same way.",
  "The HOA board member who is the only one with the key to the clubhouse, the pool schedule, and the neighborhood Facebook group password — so the whole community's dependency on him becomes total and the role becomes immune to question. “I got you” as a volunteer-committee control mechanism. Works the same way.",
  "ch17 T2 I Got You Dependency Build: IT department -> HOA board",
 ),
 18: (
  "The startup that describes itself as a “family culture” in the job posting, meaning: we expect the emotional labor of family relationships and the availability of family members, and we will use the language of belonging to extract those things without the reciprocal commitment that actual family relationships require. The culture fit interview is the El audition.",
  "The church youth group that calls itself a family and means: we expect the emotional labor of family and the availability of family, and we will use the word “covenant” to extract both without the reciprocity family actually requires. The membership interview is the El audition.",
  "ch18 T1 Family Frame: startup -> church youth group",
 ),
 19: (
  "The person who cannot imagine leaving the job that is making them miserable because “if I leave, what am I?” The answer to the question is: someone who used to work at that company and still exists. The Lock and its grammar are default-world standard issue.",
  "The person who cannot imagine leaving the marriage that is making them miserable because “if I leave, who even am I without this?” The answer to the question is: someone who used to be married and still exists. The Lock and its grammar are default-world standard issue.",
  "ch19 T2 If You Leave You're Nothing Lock: job -> marriage",
 ),
 22: (
  "The performance review where your old manager’s voice still runs in your head two years after you left that job, telling you your ideas are too ambitious, your work is not enough. The manager is gone. The performance review is gone. The voice is in the commute.",
  "The dinner table where your father's voice still runs in your head twenty years after you moved out, telling you your ideas are too ambitious, your work is not enough. The dinner table is gone. The house is sold. The voice is in the commute.",
  "ch22 T1 3 A.M. Encore: manager -> father",
 ),
 23: (
  "The work apology. “I’m sorry for any misunderstanding.” This is not an apology. This is a sentence about a misunderstanding that does not exist. The apology that actually means it says: “I did [specific thing]. I am sorry.” That sentence. In a work context. Without the explanation or the forgiveness request.",
  "The family group text apology. “Sorry if what I said came across wrong.” This is not an apology. This is a sentence about a misunderstanding that does not exist. The apology that actually means it says: “I did [specific thing]. I am sorry.” That sentence. In the family group text. Without the explanation or the forgiveness request.",
  "ch23 T3 Apology That Actually Means It: work -> family group text",
 ),
 24: (
  "The team that has an unspoken policy about which meetings one person should not be in, which clients should not be assigned to them, which projects should not have their name attached. The routing is nine years of performance review feedback that was never given. The Walk-Through is the annual people-process conversation that asks: who are we working around, and why?",
  "The youth soccer league's specific language for the annual coach evaluation, which makes it structurally difficult to name a problem as a problem because the word for the problem has been replaced with “growth area.” “Needs more patience with the younger kids.” “Communication style doesn't always land.” All of these are the missing stair in a golf shirt.",
  "ch24 T3 Missing Stair Walk-Through: office team -> youth soccer league",
 ),
}


def bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    return s.start(), e.start()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)
    applied, skipped, failed = [], [], []

    for n, (old, new, label) in sorted(ROTATIONS.items()):
        s, e = bounds(html, n)
        chunk = html[s:e]
        if old in chunk:
            assert chunk.count(old) == 1, "%s: %d matches in chapter" % (label, chunk.count(old))
            chunk = chunk.replace(old, new, 1)
            html = html[:s] + chunk + html[e:]
            applied.append(label)
        elif new in chunk:
            skipped.append(label)
        else:
            failed.append(label)

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
