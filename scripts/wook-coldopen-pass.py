#!/usr/bin/env python3
"""The 2026-09-10 cold-open pass on Wook in Sheep's Clothing.

Two kinds of change, applied together because they were reviewed together:

CONTINUITY FIXES -- six defects found by reading all 26 cold opens against
their paired "Tales From ... The Save" resolutions:
  1. Ch1's "bandana guys" flee the climax having never been introduced.
  2. Ch2's cold open never resolves -- the only one of 26 that doesn't.
  3. Ch1 says the book has twenty-three chapters. It has twenty-six.
  4. Ch24/Ch25 say "twenty-one chapters" where twenty-four precede Ch25.
     (3 and 4 are the same artifact: the Encore grew from 3 chapters to 6
     and these callbacks were never re-counted.)
  5. Ch10 cites Ch4+Ch5 for a motif Ch5 does not contain (it's Ch3+Ch4).
  6. Ch25's recurring-cast confession cites chapter numbers for Beans,
     Mara and Sister Lou that match no arrangement the book has ever had.
     De-specified rather than re-numbered, so it cannot rot again.

CRAFT PASS -- per-POV vernacular and one concrete "raw detail" per cold
open. The book has one authorial rhythm across all 26 chapters, which is
deliberate; the problem was that every POV also shared one *vocabulary*.
Festies now think in scene shorthand (sherpa, the ask, geometry) instead
of having it explained to them; Wook-POV chapters get the operator
vocabulary only Ch14 previously had (the mark, stepping on it); Witness
chapters get the hesitation beat that makes their competence cost
something.

Name collisions fixed in the same pass: four Priyas, two Caras, two
Okonkwos, two "Tales From The Gate Line" titles.

Run: python3 scripts/wook-coldopen-pass.py
Idempotent: re-running is a no-op (every edit checks for its own result).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

applied, skipped = [], []


def sub(html, label, old, new, count=1):
    """Replace `old` with `new`, asserting it appears exactly `count` times."""
    global applied, skipped
    if new in html and old not in html:
        skipped.append(label)
        return html
    found = html.count(old)
    assert found == count, f"{label}: expected {count} of {old[:60]!r}, found {found}"
    applied.append(label)
    return html.replace(old, new, count)


def chapter_bounds(html, n):
    s = re.search(r'<div class="chwrap s\d" data-ch="%d">' % n, html)
    e = re.search(r'<i class="ch-end" data-ch="%d">' % n, html)
    assert s and e, f"chapter {n} bounds not found"
    return s.start(), e.start()


def sub_in_chapter(html, n, label, old, new, count=1):
    """Same as sub() but scoped to one chapter -- for renames where the
    same string legitimately appears elsewhere in the book."""
    global applied, skipped
    a, b = chapter_bounds(html, n)
    chunk = html[a:b]
    if new in chunk and old not in chunk:
        skipped.append(label)
        return html
    found = chunk.count(old)
    assert found == count, f"{label}: expected {count} of {old[:60]!r} in ch{n}, found {found}"
    applied.append(label)
    return html[:a] + chunk.replace(old, new, count) + html[b:]


def sub_in_save(html, n, label, old, new, count=1):
    """Scoped to a chapter's 'Tales From ... The Save' section only."""
    global applied, skipped
    a, b = chapter_bounds(html, n)
    m = re.search(r'<section class="panel pp-cream prose inter-tales">.*?</section>',
                  html[a:b], re.S)
    assert m, f"ch{n}: no inter-tales section"
    sa, sb = a + m.start(), a + m.end()
    chunk = html[sa:sb]
    if new in chunk and old not in chunk:
        skipped.append(label)
        return html
    found = chunk.count(old)
    assert found == count, f"{label}: expected {count} of {old[:60]!r} in ch{n} Save, found {found}"
    applied.append(label)
    return html[:sa] + chunk.replace(old, new, count) + html[sb:]


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    # ---------------------------------------------------------------
    # CHAPTER 1 -- The Tank
    # ---------------------------------------------------------------
    # FIX 1: the bandana guys now exist before they flee.
    html = sub(html, "ch1 bandana guys planted",
        "<p>Set break hits at 8:14 p.m. Pacific time.</p>",
        "<p>Two guys from the shade canopy get up around eight without being asked "
        "&mdash; bandanas tied low, the same practiced way, neither of them having said "
        "ten words to Daniel all evening &mdash; and start running the balloon rig off "
        "the second tank. Hopper does not introduce them. They do not introduce "
        "themselves. Daniel reads this as them being busy.</p>"
        "<p>Set break hits at 8:14 p.m. Pacific time.</p>")

    # FIX 3: the book has twenty-six chapters.
    html = sub(html, "ch1 chapter count 23->26",
        "in all twenty-three chapters",
        "in all twenty-six chapters")

    # CRAFT: Festie vernacular -- Daniel reaches for the scene's own word.
    html = sub(html, "ch1 sherpa",
        "<p>That is the first yes.</p>",
        "<p>That is the first yes.</p>"
        "<p>Somewhere in the back of his head, in the part still narrating his own tour "
        "to an audience that does not exist, Daniel thinks: <em>Hopper&rsquo;s basically "
        "my sherpa out here.</em> He will think about that word again in October, in a "
        "hallway outside a courtroom in Douglas County, and it will not sound the same.</p>")

    # CRAFT: pay off "practicing the nod."
    html = sub(html, "ch1 nod callback",
        "was now being handed back to him by a public defender in a county he had never been to.</p>",
        "was now being handed back to him by a public defender in a county he had never been to.</p>"
        "<p>In the hallway outside the courtroom, Daniel does the nod. At his own public "
        "defender. Slow and deliberate, <em>I have been around, I know what&rsquo;s "
        "good</em> &mdash; eighteen days of practice firing off on schedule at a man "
        "holding a folder with his name on it. He catches it half a second after his chin "
        "comes back up.</p><p>It is the last time he does it.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 2 -- The Pre-Party
    # ---------------------------------------------------------------
    # CRAFT: give Solenne one thing to lose that isn't a booking.
    html = sub(html, "ch2 mother detail",
        "She has been awake since five-thirty a.m.",
        "Her mother calls on Sundays at ten and Solenne has not missed one in four years, "
        "including the Sunday she had food poisoning and took the call sitting on a "
        "bathroom floor in Reseda.</p>"
        "<p>She has been awake since five-thirty a.m.")

    # FIX 2: the cold open resolves.
    html = sub(html, "ch2 RESOLUTION",
        "she cannot identify where one ended and the next one started.</p>",
        "she cannot identify where one ended and the next one started.</p>"
        "<p>She does not have a ride that is not the Sprinter, and the Sprinter is "
        "Rex&rsquo;s, and the festival is forty minutes of dark hills away.</p>"
        "<p>She Venmos eight hundred dollars at 11:52 p.m. from the edge of the pool deck "
        "&mdash; a partial hold on one of the two slots, everything left in her checking "
        "account after rent &mdash; and tells Marcus the rest comes Friday, once a client "
        "payment clears. Marcus says of course, no rush, and he means it the way a "
        "landlord means no rush on an account he has already decided to collect.</p>"
        "<p>Rex hugs her on the way out. Same hug. One arm, shoulder-press, <em>you belong "
        "here.</em></p>"
        "<p>Monday, nothing. Wednesday, nothing. Thursday she sends a plain <em>checking in "
        "on the timeline</em> and watches it sit on delivered for six hours and then stop "
        "saying delivered at all, because a number that has already paid does not need to "
        "stay reachable.</p>"
        "<p>She never gets the eight hundred back. She never gets the slot. She plays four "
        "warehouse sets that summer, none of them Meridian, and she is a month late on rent "
        "twice before September. She misses three Sundays in a row and tells her mother it "
        "is a scheduling thing.</p>"
        "<p>She does not tell the story for a long time, because the story she would have to "
        "tell is not the story she wants people to have about her judgment.</p>"
        "<p>Solenne Baptiste is twenty-six years old and she is sharp and she is good at her "
        "job. None of that is what the twelve levers were built to test.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 3 -- The Yurt
    # ---------------------------------------------------------------
    # CRAFT: put the body in the scene before the decision.
    html = sub(html, "ch3 hands",
        "<p>By 5:47 a.m. she has Venmo",
        "<p>Her hands are doing something she notices and files as cold. The yurt is "
        "sixty-one degrees, she has had no water since midnight and no food since the "
        "pancake, and her blood sugar has been running on cactus tea and a threatening "
        "candle for nine hours. The tremor in her fingers as she opens the app is not "
        "cold. She files it as cold. That is the last executive function she performs "
        "before the transaction.</p>"
        "<p>By 5:47 a.m. she has Venmo")

    # ---------------------------------------------------------------
    # CHAPTER 4 -- Safe Hands
    # ---------------------------------------------------------------
    # CRAFT: the ghost has a voice, and it is nothing.
    html = sub(html, "ch4 ghost text",
        "disappears by week four.</p>",
        "disappears by week four.</p>"
        "<p>The last message Jade ever gets from him arrives eleven days later at 4:12 in "
        "the afternoon and says: <em>hey sorry been dealing with some stuff. hope "
        "tour&rsquo;s treating you good.</em> No question mark. Nothing to answer. She "
        "reads it maybe forty times looking for the part that is for her specifically and "
        "does not find it, because there isn&rsquo;t one. It is a message that could go to "
        "anyone, which is the truest thing he ever sent her.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 5 -- The Eight-Ball  (Wook POV)
    # ---------------------------------------------------------------
    # CRAFT: the operator's real vocabulary, and the lie about it.
    html = sub(html, "ch5 the mark",
        "<p>I have not pushed once.</p>",
        "<p>There is an older word for what she is. My uncle ran a room like this out of "
        "a bar in Reseda for eleven years before the liver took him, and he would have "
        "called her the mark. I do not use that word. I have never used that word. I want "
        "that on the record, in whatever record this is.</p>"
        "<p>I have used it twice tonight, in my head, and corrected myself both times.</p>"
        "<p>I have not pushed once.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 6 -- Where Are You Camped  (Witness POV)
    # ---------------------------------------------------------------
    # CRAFT: competence should cost something.
    html = sub(html, "ch6 hesitation",
        "<p><strong class=\"lead\">Margo says:</strong> “Asher. I’ve really appreciated you sharing tonight.",
        "<p>Here is the part Margo does not say out loud, tonight or ever: she considers "
        "letting it go. For about a second and a half she runs the whole thing &mdash; "
        "that she is fifty-one hours into a four-day event, that Devon and Jules are both "
        "right there and either of them could take this, that she has done this exact "
        "thing at this exact hour for fifteen years and has never once been thanked for "
        "it. There is a version of tonight where she says <em>oh, I&rsquo;m up near the "
        "north gate</em> and lets the next six hours belong to somebody else.</p>"
        "<p>The tiredness is real. The tiredness has a case.</p>"
        "<p>She does it anyway. That is what the fifteen years actually bought &mdash; not "
        "the seeing. Anybody can learn the seeing. The doing-it-anyway on the night you "
        "are too tired to want to.</p>"
        "<p><strong class=\"lead\">Margo says:</strong> “Asher. I’ve really appreciated you sharing tonight.")

    # ---------------------------------------------------------------
    # CHAPTER 7 -- Strike Day  (Witness POV)
    # ---------------------------------------------------------------
    html = sub(html, "ch7 hesitation",
        "<p>He puts down the parachute.",
        "<p>He does not move for a moment. Nine years at this camp and he has watched this "
        "conversation happen from a distance three separate times and every time he has "
        "told himself it was not his to interrupt. The ninth year is heavy. The parachute "
        "is right here in his hands and folding it is a task that would keep him honestly "
        "busy for another twenty minutes.</p>"
        "<p>The twelve feet is not the hard part. The twelve feet takes four seconds.</p>"
        "<p>The hard part is the second before it.</p>"
        "<p>He puts down the parachute.")

    # ---------------------------------------------------------------
    # CHAPTER 8 -- Sterling At The Row  (Wook POV)
    # ---------------------------------------------------------------
    # CRAFT: he sees her clearly and proceeds anyway.
    html = sub(html, "ch8 cash box photo",
        "<p>She needs the money, and she needs to believe in the thing.</p>",
        "<p>Taped inside the lid of her cash box, facing her, where only she can see it: a "
        "school photo of a kid, maybe nine, gap in the front teeth, that maroon backdrop "
        "every school portrait in America has used since 1994. Brother, going by the age "
        "gap. She looks at it once while she is counting her float and her face does "
        "something that is not for anybody at this festival.</p>"
        "<p>I note it. I will not use it. Using the kid would be crude and would also work, "
        "and the difference between me and the men in the CONSCIOUS hats is that I know "
        "both of those things and still do not do it. I would like credit for that. There "
        "is nobody here to give it to me, so I give it to myself, and then I go to work "
        "on her.</p>"
        "<p>She needs the money, and she needs to believe in the thing.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 9 -- Blue Lips
    # ---------------------------------------------------------------
    # FIX: Marco's outcome is stated. The teaching beat still lands first.
    html = sub(html, "ch9 Marco resolved",
        "<p>The Free Cap Funnel is real.",
        "<p>Eli said yes.</p>"
        "<p>Her name was Robin, she had a nursing-school ID in her fanny pack, and she got "
        "Marco onto his side and the Zendo onto the radio inside ninety seconds. He was in "
        "the medical tent by 3:24 and on a saline drip by 3:40 and he woke up angry and "
        "embarrassed and alive at nine in the morning. He does not remember any of it.</p>"
        "<p>Eli remembers all of it. Eli specifically remembers the ninety seconds where he "
        "did not yet know what he was going to do.</p>"
        "<p>The Free Cap Funnel is real.")

    # Sadie's surname collided with Jess Okonkwo in ch16.
    html = sub_in_chapter(html, 9, "ch9 Sadie surname",
        "Sadie Okonkwo", "Sadie Adeyemi")

    # ---------------------------------------------------------------
    # CHAPTER 10 -- We've Been Having Problems
    # ---------------------------------------------------------------
    # FIX 5: Ch5 has no such passage. Ch3 and Ch4 do.
    html = sub(html, "ch10 cross-ref 4+5 -> 3+4",
        "described in Chapter 4 and Chapter 5",
        "described in Chapter 3 and Chapter 4")

    # Duplicate Save title (ch9 already uses "The Gate Line").
    html = sub_in_chapter(html, 10, "ch10 Save title",
        "Tales From The Gate Line", "Tales From The Turnout")

    # ---------------------------------------------------------------
    # CHAPTER 11 -- The Corridor
    # ---------------------------------------------------------------
    # CRAFT: Maya names the move herself instead of the narrator naming it.
    html = sub(html, "ch11 the ask",
        "from studying hydrology, but from feeling the current.</p>",
        "from studying hydrology, but from feeling the current.</p>"
        "<p>The word that arrives in her head, fully formed, is <em>ask</em>. Not request. "
        "Not question. <em>Ask</em>, the way her uncle used it about closing car deals in "
        "Modesto &mdash; the specific noun for the moment you find out the friendly part "
        "was the runway. She has been in a sales conversation for four minutes and has "
        "only now been told.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 12 -- Forty A Cap
    # ---------------------------------------------------------------
    # Third Priya in the book; this one becomes Devi Raman.
    html = sub_in_chapter(html, 12, "ch12 Priya Suresh -> Devi Raman",
        "Priya Suresh", "Devi Raman")
    a, b = chapter_bounds(html, 12)
    n_priya = html[a:b].count("Priya")
    if n_priya:
        html = sub_in_chapter(html, 12, "ch12 remaining Priya -> Devi",
            "Priya", "Devi", count=n_priya)

    # ---------------------------------------------------------------
    # CHAPTER 13 -- The Mason Jar  (Wook POV)
    # ---------------------------------------------------------------
    html = sub(html, "ch13 bracelet",
        "<p>The window is where Cosmo spends most of his time.</p>",
        "<p>The window is where Cosmo spends most of his time.</p>"
        "<p>She has a friendship bracelet on her right wrist that is not kandi. Embroidery "
        "floss, four colors, the flat braid a kid learns at camp, and it is old &mdash; "
        "sun-faded on the top side and not the bottom, which means years. Somebody made it "
        "for her a long time ago and she has not taken it off since. That is a person who "
        "keeps things.</p>"
        "<p>He clocks it the way he clocks everything, and it changes nothing.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 15 -- The RV
    # ---------------------------------------------------------------
    html = sub(html, "ch15 geometry",
        "<p>He sits on the tire.</p>",
        "<p>He sits on the tire.</p>"
        "<p>The word he keeps landing on is <em>geometry</em>. Four feet to the door and "
        "two men between him and it. He is twenty-three and he has never once had to think "
        "about the geometry of a room, and now he is going to think about it in every room "
        "for years, which is the part of tonight that actually follows him home.</p>")

    # Dev's friend was a fourth Priya.
    html = sub_in_chapter(html, 15, "ch15 friend Priya -> Nabila",
        "Priya", "Nabila", count=html[chapter_bounds(html, 15)[0]:chapter_bounds(html, 15)[1]].count("Priya"))

    # ---------------------------------------------------------------
    # CHAPTER 16 -- She Said She'd Be Right Back
    # ---------------------------------------------------------------
    # CRAFT: Marlene gets to be a person.
    html = sub(html, "ch16 Marlene line",
        "“Good morning. I’m Marlene. There’s chamomile.”</p>",
        "“Good morning. I’m Marlene. There’s chamomile.”</p>"
        "<p>And then, because thirty-seven years of ninth graders does not switch off: "
        "“You slept like someone who needed it. Don’t apologize for that. "
        "I’ve had two husbands and neither one of them could do it.”</p>")

    # ---------------------------------------------------------------
    # CHAPTER 17 -- The DanceSafe Pin  (Wook POV)
    # ---------------------------------------------------------------
    html = sub(html, "ch17 stepping on it",
        "<p>This is the one I do not discuss in the FAQ.</p>",
        "<p>This is the one I do not discuss in the FAQ.</p>"
        "<p>The word for it in the trade is stepping on it. You step on a thing to make it "
        "go further. Everyone in the supply chain above me steps on everything, which is "
        "the entire reason my testing protocol exists in the first place, and there is a "
        "version of that sentence where that fact does moral work on my behalf.</p>"
        "<p>I have used that version of the sentence. I am using it right now.</p>")

    # ---------------------------------------------------------------
    # CHAPTER 18 -- The Kombucha
    # ---------------------------------------------------------------
    # The Save's protagonist shared a name with the Drop's victim, who
    # carries an arc through Ch21, Ch24 and Ch26. The Save's is now Wren.
    a, b = chapter_bounds(html, 18)
    m = re.search(r'<section class="panel pp-cream prose inter-tales">.*?</section>', html[a:b], re.S)
    n_cara = m.group(0).count("Cara")
    html = sub_in_save(html, 18, "ch18 Save Cara -> Wren", "Cara", "Wren", count=n_cara)

    # ---------------------------------------------------------------
    # CHAPTER 19 -- Tuesday
    # ---------------------------------------------------------------
    # CRAFT: name the specific thing she lost, not just the absence of it.
    html = sub(html, "ch19 the bass",
        "<p>Before that weekend, she liked music.",
        "<p>Before that weekend she played bass. Badly, in a four-piece that practiced in a "
        "storage unit in San Leandro on Wednesdays. They were not good and it did not "
        "matter, because Wednesday was the point. She sold the bass in 2021 to cover a "
        "booth fee. She could not have told you at the time that she was selling it. It "
        "felt like liquidity.</p>"
        "<p>Before that weekend, she liked music.")

    # ---------------------------------------------------------------
    # CHAPTER 20 -- The Drive Home
    # ---------------------------------------------------------------
    # CRAFT: the text should show he was watching all weekend without being there.
    html = sub(html, "ch20 Damian text",
        "“How was it? Been thinking about you.”",
        "“watched your stories all weekend. you looked free out there. been thinking "
        "about you.”")

    # ---------------------------------------------------------------
    # CHAPTER 22 -- The Tuesday-After
    # ---------------------------------------------------------------
    a, b = chapter_bounds(html, 22)
    n_priya = html[a:b].count("Priya")
    html = sub_in_chapter(html, 22, "ch22 Priya -> Simone", "Priya", "Simone", count=n_priya)

    # ---------------------------------------------------------------
    # CHAPTER 24 -- The Napkin Network
    # ---------------------------------------------------------------
    html = sub(html, "ch24 MOU",
        "memorandum of understanding with county allows.</p>",
        "memorandum of understanding with county allows. The MOU. Three pages, mostly "
        "definitions, and every safety coordinator on the circuit can quote the weak part "
        "of it from memory.</p>")

    # FIX 4a: the bridge into Ch25.
    html = sub(html, "ch24 bridge count 21->24",
        "sitting inside for twenty-one chapters",
        "sitting inside for twenty-four chapters")

    # ---------------------------------------------------------------
    # CHAPTER 25 -- The Taper's Reveal
    # ---------------------------------------------------------------
    # FIX 4b/4c: twenty-four chapters precede this one.
    html = sub(html, "ch25 opening count 21->24",
        "We have spent twenty-one chapters together.",
        "We have spent twenty-four chapters together.")
    html = sub(html, "ch25 body count 21->24",
        "been saying to this book for twenty-one chapters",
        "been saying to this book for twenty-four chapters")

    # FIX 6: de-specify the recurring-cast claim so it cannot go stale again.
    html = sub(html, "ch25 recurring cast de-specified",
        "<p>Beans appears in Chapters 8, 12, 13, and 15.</p>"
        "<p>Mara appears in Chapters 4, 6, and 19.</p>"
        "<p>Sister Lou appears in Chapters 14, 16, and 18.</p>",
        "<p>Beans came back. So did Mara. So did Sister Lou.</p>")

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes")
    print(f"\napplied {len(applied)}:")
    for a_ in applied:
        print(f"  + {a_}")
    if skipped:
        print(f"\nalready present, skipped {len(skipped)}:")
        for s in skipped:
            print(f"  = {s}")


if __name__ == "__main__":
    sys.exit(main())
