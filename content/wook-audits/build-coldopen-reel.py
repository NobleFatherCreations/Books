#!/usr/bin/env python3
"""Assemble the cold-open reel document: ranked running order + full text.

Pulls the CURRENT text of all 26 cold opens straight out of the live book
source, so the document can never drift from what actually shipped. Re-run
after any edit to the cold opens to regenerate.

Run: python3 content/wook-audits/build-coldopen-reel.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WOOK = ROOT / "library/wook/index.html"
OUT = ROOT / "content/wook-audits/wook-cold-opens-reel-order.md"

POV = {
    1: "Festie", 2: "Festie", 3: "Festie", 4: "Festie", 5: "Wook",
    6: "Witness", 7: "Witness", 8: "Wook", 9: "Festie", 10: "Festie",
    11: "Festie", 12: "Wook", 13: "Wook", 14: "Wook", 15: "Festie",
    16: "Festie", 17: "Wook", 18: "Festie (inside the group)", 19: "Festie",
    20: "Festie", 21: "Festie (no predator)", 22: "Festie", 23: "Festie",
    24: "Montage", 25: "Author direct address", 26: "Festie (six months later)",
}

# (episode, chapter, scene name, hook line, cut point, why it sits here)
SEASON_ONE = [
 (1, 10, "We've Been Having Problems",
  "The bag is heavier than she thought.",
  "End on: \"He knew what would happen. He rehearsed the sentence.\"",
  "Needs zero festival knowledge. A boyfriend, a gas station, a rehearsed "
  "sentence. Every viewer knows someone who has been the person in that "
  "passenger seat, which makes it the most portable thing in the book -- it "
  "plays on a true-crime channel, a relationships page, or a harm-reduction "
  "feed without changing a word. It also has a hard, clean ending, which most "
  "of these don't. Lead with your most legible episode, not your best one."),

 (2, 5, "The Eight-Ball",
  "I bring an eight-ball to every party.",
  "End on: \"I'm just generous. I bring an eight-ball to every party.\" Do not "
  "include the authorial turn that follows -- let the viewer sit in it.",
  "The POV flip is the entire sell of this book, and it lands hardest as the "
  "second thing you see, immediately after watching it happen to someone. Now "
  "you are inside the guy, and he is likeable, and he sleeps great. New this "
  "round: he catches himself using the word 'mark' twice and corrects himself "
  "both times, which is the moment the self-deception cracks on camera."),

 (3, 16, "She Said She'd Be Right Back",
  "It is 1:47 a.m. and Jess has been gone for approximately four hours and "
  "nobody in the group can remember her last name.",
  "End on: \"...decide, mutually and without discussion, never to speak of it "
  "again.\"",
  "Deliberate breather after two heavy ones, and the highest-converting "
  "episode in the series: it ends fine, it is genuinely funny in places "
  "(Marlene, the Karen-versus-Carol argument), and it hands the viewer one "
  "concrete thing to go do. This is the one that gets forwarded into a group "
  "chat two weeks before a festival, which is exactly the buying moment."),

 (4, 1, "The Tank",
  "He has been practicing the nod.",
  "End on the new courthouse beat: \"It is the last time he does it.\" That is "
  "now a better video ending than the essay close that follows.",
  "The heavyweight. By episode four the audience trusts the series enough to "
  "be handed a death. Hannah Reyes is named, which is the whole ethic of the "
  "book in one choice. The nod now pays off in a courthouse hallway, so the "
  "episode closes on an image instead of an argument."),

 (5, 14, "The Wristband Cop",
  "The wristband is real.",
  "End on: \"The close rate is the product. The guy in the sun hat is the "
  "input.\"",
  "The twist episode. The predator is the state, with a training manual, a "
  "fake Discord friend and an expense report. It recontextualizes everything "
  "before it, and the churro line keeps it from reading as a lecture. Highest "
  "share ceiling of anything in the book -- it travels well outside the scene."),

 (6, 3, "The Yurt",
  "Nadia Okafor writes memos about cognitive bias for a living.",
  "End on: \"what is the structure?\"",
  "The 'smart people too' episode, and the shortest of the heavy hitters, so "
  "it changes pace. Its closing line -- knowing the levers does not save you, "
  "only structure saves you -- is the single most screenshottable sentence in "
  "the book. New this round: her hands are shaking before she pays and she "
  "files it as cold."),

 (7, 13, "The Mason Jar",
  "His name at this festival is Cosmo.",
  "End on: \"In her interior, something happened that she does not have a word "
  "for.\"",
  "The warmest predator, which makes him the worst one. Short. The horror is "
  "that he is exactly as kind in the morning as he was at the fire. New: the "
  "sun-faded friendship bracelet he notices, correctly reads as evidence she "
  "keeps things, and proceeds anyway."),

 (8, 12, "Forty A Cap",
  "I'm not a dealer.",
  "End on: \"The Bunk Police volunteer looks at the ground. That is the "
  "answer.\"",
  "The consequence episode: one skipped twenty-minute line in a booth. The "
  "Santa-hat memory is the best single image in the book and it arrives at "
  "exactly the wrong moment for him, which is what makes it work."),

 (9, 2, "The Pre-Party",
  "Rex is not in the van. Rex sent the van.",
  "End on: \"None of that is what the twelve levers were built to test.\"",
  "Reaches an audience the others don't: anyone in music, film, or any "
  "industry with gatekeepers and 'development opportunities.' This cold open "
  "used to stop mid-decision and never say what happened to her; it now "
  "finishes, which is what makes it usable as a standalone video at all."),

 (10, 17, "The DanceSafe Pin",
  "The DanceSafe pin is on my snapback. Not ironically.",
  "End on: \"Wedge is one of the good ones. And he is building you a cage.\"",
  "The hardest one to argue with and the best test of whether your audience is "
  "actually thinking, because he is ninety-five percent genuinely good and the "
  "other five percent is hidden underneath the safety community's own "
  "infrastructure. Best comment section of the series, by a distance."),

 (11, 18, "The Kombucha",
  "She has been with the Lantern Family for three years.",
  "End on: \"She folds it into her sock.\" Keep El's own POV section out of "
  "this episode -- it is a bonus episode by itself.",
  "The darkest, placed where the audience has the context to receive it. Runs "
  "a content warning card. The napkin is the image people will still be able "
  "to describe a month later. Pairs deliberately with the finale."),

 (12, 23, "The Re-Read",
  "He is reading this book in a camp chair in his backyard on a Sunday "
  "afternoon in September.",
  "End on: \"The recognition is the point.\"",
  "The turn. Eleven episodes of watching this happen to other people, and now "
  "the man on screen is reading the same book you are being sold and finds "
  "himself in it. Shortest of the heavy episodes and the single most likely to "
  "convert a viewer into a reader, because it makes finishing the book feel "
  "like a personal test."),

 (13, 26, "The Sealed Bottle",
  "She opens her own bottles now.",
  "End on: \"The structure is what makes the magic safe to let in.\"",
  "Close on Cara: same woman as episode eleven, six months out, now the person "
  "who walks over and says 'I don't know that guy.' Pays off the series' only "
  "continuing character and sends the audience out on hope instead of dread, "
  "which is what makes people share it rather than just flinch and scroll."),
]

SEASON_TWO = [
 (14, 9, "Blue Lips", "The unicorn onesie asks the only question that matters. "
  "Now confirms whether Marco lived, which it previously did not."),
 (15, 15, "The RV", "The click that was not the door. New: 'geometry' is the "
  "word he cannot stop landing on afterward."),
 (16, 7, "Strike Day", "Twelve feet and a water bottle. New: the second before "
  "the twelve feet, where he almost doesn't."),
 (17, 8, "Sterling At The Row", "Vendor row as a hunting ground. New: the "
  "school photo taped inside the cash box."),
 (18, 11, "The Corridor", "Highway stop as a sales call. New: she recognizes "
  "the word 'ask' from her uncle's car lot."),
 (19, 4, "Safe Hands", "The sunrise bond. New: the last text he ever sends, "
  "which could have gone to anyone."),
 (20, 19, "Tuesday", "The hollowing out. New: the bass she sold in 2021 to "
  "cover a booth fee, which at the time felt like liquidity."),
 (21, 6, "Where Are You Camped", "Twenty-two minutes of weaponised "
  "vulnerability. New: Margo considers letting it go."),
 (22, 22, "The Tuesday-After", "The 3 a.m. encore in his voice, four weeks "
  "later. Heavy; needs a support-resources card."),
 (23, 20, "The Drive Home", "The thirty-six-hour window. New: his text now "
  "shows he was watching her stories all weekend without being there."),
 (24, 21, "The Gate Briefing", "Sister Lou, a clipboard, fifteen minutes. The "
  "one with no predator in it at all."),
 (25, 24, "The Napkin Network", "Five vignettes of the immune system working. "
  "Best as a mid-season anthology special."),
 (26, 25, "The Taper's Reveal", "The author confesses every technique used on "
  "the reader. Only works as a finale, and only after the rest."),
]


def strip(s):
    s = re.sub(r'</p>\s*<p[^>]*>', '\n\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    for k, v in {'&rsquo;': '’', '&lsquo;': '‘', '&rdquo;': '”', '&ldquo;': '“',
                 '&mdash;': '—', '&ndash;': '–', '&amp;': '&', '&#8217;': '’',
                 '&middot;': '·', '&hellip;': '…', '&#9834;': '♪'}.items():
        s = s.replace(k, v)
    return re.sub(r'\n{3,}', '\n\n', s).strip()


def main():
    html = WOOK.read_text(errors="surrogateescape")
    chw = {int(m.group(1)): m.start()
           for m in re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', html)}
    che = {int(m.group(1)): m.start()
           for m in re.finditer(r'<i class="ch-end" data-ch="(\d+)">', html)}
    titles = {int(m.group(1)): strip(m.group(2)) for m in re.finditer(
        r'<section class="ch-poster s\d" id="ch(\d+)">.*?<h2 class="poster-title">(.*?)</h2>',
        html, re.S)}

    drops = {}
    for n in range(1, 27):
        chunk = html[chw[n]:che[n]]
        m = re.search(r'<section class="panel pp-cream prose comp-drop">(.*?)</section>',
                      chunk, re.S)
        drops[n] = strip(m.group(1))

    def mins(n):
        return len(drops[n].split()) / 150.0

    o = []
    o.append("# Wook in Sheep's Clothing — The Cold Opens\n")
    o.append("Every cold open as it currently stands live, plus a running order "
             "built for a promotional video series rather than for the book.\n")
    o.append("Generated from the live book source, so this file cannot drift "
             "from what shipped. Regenerate with "
             "`python3 content/wook-audits/build-coldopen-reel.py`.\n")

    o.append("\n## How this order was built\n")
    o.append("Chapter order is built for a reader who starts at the beginning "
             "and goes forward. A video series has the opposite problem: every "
             "episode is somebody's first, most viewers arrive knowing nothing "
             "about festival culture, and the algorithm rewards whichever one "
             "gets finished. So this order optimizes for six things instead:\n")
    o.append("""
1. **Cold-start legibility.** Can someone who has never been to a festival
   follow it with no setup? The most legible episode goes first, even if it
   isn't the best one.
2. **Hook speed.** How many seconds to the first *wait, what?*
3. **Recognition transfer.** Does it make a viewer with no connection to the
   scene recognize somebody in their own life? That is what drives shares.
4. **Payload.** Does it actually land, or does it only explain?
5. **Rotation.** POV and tone alternate deliberately. Two victim episodes back
   to back flattens; victim → predator → breather does not.
6. **Ending on the right beat.** Most of these cold opens close with the
   chapter's thesis. For video you almost always want to cut on the last
   *narrative* beat and let the argument stay in the book. A suggested cut
   point is given for every episode below.
""")

    o.append("\n---\n\n# Season One — the thirteen\n")
    for ep, ch, name, hook, cut, why in SEASON_ONE:
        o.append(f"\n## EP {ep} — Chapter {ch}: “{name}”\n")
        o.append(f"*{POV[ch]} POV · {len(drops[ch].split()):,} words · "
                 f"~{mins(ch):.0f} min read-aloud*\n")
        o.append(f"\n**Open on:** “{hook}”\n")
        o.append(f"\n**Why here:** {why}\n")
        o.append(f"\n**Cut point:** {cut}\n")

    o.append("\n---\n\n# Season Two — the rest\n")
    o.append("\nOrdered, but with less at stake in the ordering — by this point "
             "the audience is bought in and each of these can stand alone.\n")
    for ep, ch, name, note in SEASON_TWO:
        o.append(f"\n**EP {ep} — Chapter {ch}: “{name}”** "
                 f"*({POV[ch]} POV · ~{mins(ch):.0f} min)* — {note}\n")

    o.append("\n---\n\n# Production notes\n")
    o.append("""
**Runtimes.** Read-aloud estimates above assume 150 words per minute, which is
an unhurried narration pace. These are long for short-form: the shortest is
Chapter 23 at about seven minutes, the longest Chapter 18 at seventeen. Three
usable formats:

- **Full narration** (7–17 min) for YouTube or a podcast feed. Cut at the point
  noted for each episode.
- **The first 90 seconds** as the short-form hook, ending on the cliff, with the
  full version linked. Chapters 10, 5, 16, 14 and 23 all have a natural 90-second
  break already in them.
- **Single-line cards.** Several of these have one sentence that carries the
  whole episode — "He rehearsed the sentence," "I'm just generous," "nobody
  can remember her last name," "The wristband is real." Those work as standalone
  text posts pointing at the video.

**Content warnings.** Episodes 4, 11 and 22 need one on the front. Chapter 18
(EP 11) specifically depicts drugging and assault; Chapter 22 (Season Two)
depicts the aftermath. Put support resources in the description, not just at
the end of the video.

**What not to spoil.** Chapter 25 confesses the persuasion techniques the book
used on the reader. It is the best single piece of writing in the book and it
only works if the audience has already been through the others, so it must stay
last. Do not use it as a hook, a teaser, or a trailer.

**The one continuing character.** Cara appears in Chapters 18, 21, 24 and 26.
EP 11 and EP 13 are her, six months apart. If the series does nothing else with
continuity, do that pairing — it is the only arc in the book that resolves
across chapters, and it is what turns a set of cautionary tales into a story.
""")

    o.append("\n---\n\n# The cold opens, in book order\n")
    o.append("\nFull current text of all twenty-six.\n")
    for n in range(1, 27):
        ep = next((e for e, c, *_ in SEASON_ONE if c == n), None)
        ep = ep or next((e for e, c, *_ in SEASON_TWO if c == n), None)
        o.append(f"\n---\n\n## Chapter {n}: {titles.get(n, '?')}\n")
        o.append(f"*{POV[n]} POV · {len(drops[n].split()):,} words · "
                 f"~{mins(n):.0f} min · reel position: EP {ep}*\n\n")
        o.append(drops[n] + "\n")

    OUT.write_text("".join(o))
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
