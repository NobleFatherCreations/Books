#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retire the three banned Wook Discog tier descriptors.

The 2026-09-19 voice audit found that the Gate 9 rename was applied to the
tier LABELS (Studio Debut / Live Album / Greatest Hits Compilation, correct
in all 32) but never to the descriptor line underneath, which still read
"The Baby Wook learning the moves" / "The Seasoned Operator" / "The
Institutional Scaled-Up Version" in every chapter -- 96 lines, the same
three phrases 32 times over.

This replaces each with a chapter-specific descriptor that also does Gate 1
work: the tier framing is a joke, so the descriptor should land one. The
model is chapter 27, which already carried bespoke descriptors (The New
Crew / The Seasoned Crew / The Festival With Infrastructure) and is left
untouched here.

Idempotent: a chapter whose descriptors are already replaced is skipped, so
re-running after a partial apply is safe.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

STUDIO_OLD = '<p>Studio Debut — The Baby <mark class="mk-y">Wook</mark> learning the moves</p>'
LIVE_OLD = '<p>Live Album — The Seasoned Operator</p>'
GREAT_OLD = '<p>Greatest Hits Compilation — The Institutional Scaled-Up Version</p>'

# chapter -> (studio debut, live album, greatest hits)
D = {
 1: ("Two Chords And A Nitrous Tank",
     "Same Set, Four States, Never Holds The Tank Himself",
     "He Doesn’t Tour Anymore. He Licenses."),
 2: ("Naturally Charming, He Says, About The Technique",
     "One Hand On Your Elbow, Car Already In The Driveway",
     "The Whole Persuasion Stack, Adopted As Policy"),
 3: ("Found Out Sunday Works. Never Asked Why.",
     "Six Convergences, One Binaural Loop, No Notes",
     "Now The Programming Department Sets The Set Times"),
 4: ("Accidentally Excellent At The Care Moment",
     "Works The Thinning Crowd At Sunrise Like A Shift",
     "The Retreat Model, With A Deposit Page"),
 5: ("Brought Gummies. Liked Being The Gummies Guy.",
     "The Eight-Ball, The Framing, The Kitchen Sentence",
     "An Industry Where The Dosing Is The Business Model"),
 6: ("Nineteen, One Regional Under His Belt, Somehow A Mod",
     "Four Hundred Answered Questions, Zero Reports",
     "Every Server With A Welcome Channel And No Admin"),
 7: ("Found The One Room Where Crying Counts As Credentials",
     "Workshop Space, Bay Area, Certificate In The Bio",
     "The Healing Industry, Invoiced Quarterly"),
 8: ("A Storage Unit, A Truck Schedule, And Real Love For It",
     "The Manifesto Has A Visual Brand Now",
     "Community. Spelled Governance."),
 9: ("An Artist Collective With No Accounting",
     "White Linen, Rotating Name, Contract On His Phone",
     "Takes Thirty Percent And Calls It Exposure"),
 10: ("One Shift, One Wristband, Genuinely A Good Deal",
      "Eight Hundred Hours. Sixty Of Them Paid.",
      "An Industry Built On The Word Family And A Laminate"),
 11: ("Handing Out A Cap He Didn’t Test Either",
      "The Forty-Five-Minute Warm Guy At The Bass Stage",
      "No Receipts, Scaled To An Entire Circuit"),
 12: ("They Don’t Search Girls, He Says, Having Checked",
      "Three Components And A Sentence He Rehearsed",
      "Risk, Distributed Downward, As Standard Practice"),
 13: ("Has Not Yet Considered The Highway A Risk Environment",
      "Calls It Being Careful. It’s A Checklist.",
      "A Statewide Interdiction Program With A Budget Line"),
 14: ("Nine Minutes Of Training And A Radio",
      "Two Hundred Four-Second Calls A Weekend, Never Audited",
      "The Reflex, Written Into The Operations Manual"),
 15: ("Fronted Two Hundred Dollars. Skipped The Kit.",
      "The Skips Haven’t Cost Anything. Yet.",
      "A Supply Chain That Tests Nothing And Sells Everything"),
 16: ("A Red Solo Cup And The Beginning Of An Architecture",
      "The Mason Jar Has A Regular Spot Now",
      "Hospitality, With A Dosing Strategy"),
 17: ("Came Back Changed. Started Pouring.",
      "Twelve Years, Elders He Will Not Name, Valley Unspecified",
      "A Permissive Jurisdiction, A Price List, An NDA"),
 18: ("My Friend Can Get You Something, He Offers, Helpfully",
      "Glitter From A Tutorial, Hampton Inn On The Receipt",
      "A Task Force With A Quota And A Per Diem"),
 19: ("Learned That Indoors Is Better For Business",
      "The Beige RV Runs On A Schedule",
      "A Circuit Of Rooms Nobody Files A Report About"),
 20: ("Woke The Whole Camp And Asked The Wrong Question First",
      "An Email Address And A Clipboard At The Info Booth",
      "A Reporting Pathway Designed To End At Itself"),
 21: ("We’ll Find Each Other. And They Did.",
      "A Decade Of It Working, Which Is The Actual Problem",
      "Forty Thousand People And Not One Real Name"),
 22: ("One Free Thing, Gesturing Toward Fourteen Grams",
      "I Got You, Says The Supplier, Meaning Every Word",
      "Dependency, Bundled Into The Tour Routing"),
 23: ("A Tent, A Warm Personality, No Bus Yet",
      "The Bus Has A Hierarchy And A Sleeping Chart",
      "Kinship As Org Chart, Forty Years Deep"),
 24: ("In Love With It, Which Is Not Yet The Problem",
      "Default World Now Pronounced With A Slight Sneer",
      "An Identity You Can Only Renew At The Gate"),
 25: ("Noticed People Are Softer On The Drive Home",
      "The Window, Mapped To The Hour",
      "A Marketing Calendar Built On The Comedown"),
 26: ("First Unanswered Text. Learns Exactly The Wrong Lesson.",
      "Eleven Weeks, Four Messages, One Spare Account",
      "An Open Scene With No List And No Door"),
 # 27 already carries bespoke descriptors -- untouched
 28: ("Did The Math In Week Four And Went Quiet",
      "The Friend Group, Reorganized Without A Vote",
      "A Scene That Files Its Casualties Under Drama"),
 # NB: avoid a bare "<number> Tracks" construction here -- the continuity
 # checker reads that as a claim about the chapter's Track count.
 29: ("Ran Three Of Them Without Knowing They Were Tracks",
      "Fourteen Years In, Still Counting",
      "Everyone Who Reached The Inventory And Put It Down"),
 30: ("But He Was So Good With Me",
      "The Rebrand Tour, Now Playing A Different Circuit",
      "A Conduct Committee With A Communications Plan"),
 31: ("Forbade It. Heard Nothing All Weekend. Felt Reassured.",
      "Stopped Forbidding In 2021, Considers That Reasonable",
      "Thirty Years Of Messaging That Measurably Does Not Work"),
 32: ("Using The Techniques Without Naming Them",
      "The Thirty-One Chapters You Just Finished",
      "Every Manual On Manipulation That Skipped This Chapter"),
 33: ("First Read. Some Of It Landed. The Rest Is Pending.",
      "Ran The Briefing, And Knows Exactly Why He Ran It",
      "A Scene That Built The Infrastructure And Kept It"),
}


def main():
    raw = WOOK.read_text(errors="surrogateescape")
    starts = {int(m.group(1)): m.start() for m in
              re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', raw)}
    ends = {int(m.group(1)): m.start() for m in
            re.finditer(r'<i class="ch-end" data-ch="(\d+)">', raw)}

    out = []
    cursor = 0
    changed = skipped = 0
    for n in sorted(starts):
        if n not in D:
            continue
        s, e = starts[n], ends[n]
        body = raw[s:e]
        studio, live, great = D[n]
        new = body
        hits = 0
        for old, label, desc in (
            (STUDIO_OLD, "Studio Debut", studio),
            (LIVE_OLD, "Live Album", live),
            (GREAT_OLD, "Greatest Hits Compilation", great),
        ):
            if old in new:
                new = new.replace(old, f"<p>{label} — {desc}</p>", 1)
                hits += 1
        if hits == 0:
            skipped += 1
            continue
        if hits != 3:
            raise SystemExit(f"ch{n}: expected 3 tier headers, found {hits} -- aborting")
        out.append(raw[cursor:s])
        out.append(new)
        cursor = e
        changed += 1
    out.append(raw[cursor:])
    result = "".join(out)

    for banned in ("The Baby <mark", "The Seasoned Operator", "The Institutional Scaled-Up"):
        left = result.count(banned)
        if left:
            print(f"  WARNING: {banned!r} still present x{left}")

    WOOK.write_text(result, errors="surrogateescape")
    print(f"{changed} chapter(s) updated, {skipped} already done. "
          f"{changed * 3} descriptor lines rewritten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
