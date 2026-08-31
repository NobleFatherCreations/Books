# What the next book needs to carry from the start

Five books came through the same scaffold and arrived with the same five
gaps. Fixing them per book fixes one instance each time. This is the list
to build in, so book six does not arrive with them again.

**1. A way off the page.** Esc and a `Leave` button in the persistent bar,
blanking the document then `location.replace('about:blank')`. Not an
outside site: every one of these books forbids external URLs in its own
`qa.js`, and they are offline-first. Plus one dimmed line on the contents
screen saying it exists and that a private window is worth two minutes.
Every book in this set has readers plausibly on a device someone else
checks.

**2. A `#/help` route, not a chapter link.** The persistent bar in all five
books said some version of "help exists right now" and linked to a chapter,
so a reader who clicks it in the state that made them click it gets an
essay. The page that works is the one *At Will* chapter 35 and the Codex
already model: the category of body that exists nearly everywhere, plus the
search string that finds the real one where the reader is. No invented
services, no phone numbers, no jurisdiction guessed.

**3. A record template wherever the book says to keep a record.** Every
book with a documentation chapter told the reader a record matters and
showed them nothing. Four lines, same day, written to survive someone
disputing it: when, what was observed (not inferred), who else knew, what
it changed.

**4. No "filling in as the book is written" on a finished book.** Three of
five shipped a live section in Appendix A advertising the book as
incomplete — twice with the very next heading already delivering the list.
The `stub` chapter path and the "in progress" tile label are also dead code
in all five now that every chapter is written.

**5. The safeguard chapter needs a route, not a position.** *The Repair*'s
shield check is chapter 47 of 48; *The Slow Take*'s "Am I the one
benefiting?" is 42 of 45. Both books say in their own briefs that the
reader will need these early. A chapter reachable only in sequence is not
reachable at the moment it is needed.

**Also carry:** self-hosted subset fonts rather than a system stack (see
`scripts/embed-fonts.py`), typographic quotes (`scripts/smarten.py`), and a
dash budget under about 3 per 1,000 words of prose
(`scripts/dedash.py`, `scripts/slop-scan.py`). Two buttons on the contents
screen, not seven.
