# Psychologist audit — the four new books

*Pass run 2026-08-30. Five findings per book, each tested against that
book's own brief (`BOOK-MAP.md` → THE BRIEF) rather than a generic
standard, because all four state different objectives and different
failure conditions.*

Evidence comes from `scripts/book-structure.py` (chapter length spread,
device distribution, help-routing coverage, repeated chapter shapes) and
`scripts/slop-scan.py`, plus reading the briefs and a sample of chapters
in each book. Where a finding is an inference rather than something the
structure proves, it says so.

**Status key:** `APPLIED` — fixed in this pass. `OPEN` — real, not done
this round, with the reason.

---

## The finding that spans all four books

**None of the four has a way out of the page.** `safety/exit` matched in
0 chapters in all four books, and none has an exit affordance in the page
chrome either.

Three of these four audiences are, by their own briefs, plausibly reading
on a monitored device:

- *The Long After* — its own chapter 2 documents that the period right
  after leaving is when escalation happens. Shared devices, accounts, and
  a co-parent with access are the normal case, not the edge case.
- *The Silence* — a partner who checks his phone is a pattern the book
  itself describes.
- *The Repair* — read in a house where the person harmed still lives.

This library already knows this. The Codex edition
(`source/projects/faith-index.html`) was deliberately built with no shared
site chrome because it is "sometimes read by people monitored at home."
That reasoning was never carried into these four.

`APPLIED` — Esc-to-leave plus a one-line note on the contents screen, in
all four. No storage, no history entry, nothing that contradicts the
"nothing here keeps score" line each book opens its own source with.

---

## THE LONG AFTER

*45 chapters · 211 words/chapter · post-separation abuse*
Brief: the most patient voice in the pipeline. Read slowly, re-read,
"often opened at 2am." Must route to real help wherever it brushes crisis.

**1. The help bar routes to a chapter, not to help.** `APPLIED`
The persistent bar reads *"If this has become more than aftermath, help
exists right now"* and links to `#/c/28` — which is prose about clinical
help. A reader who clicks that line at 2am because they need help right
now gets an essay. The book can't hardcode a phone number (it has no
jurisdiction), but it can do what *At Will* chapter 35 already does well:
name the category of service and route the search. That is one click
instead of one chapter.

**2. Two of forty-five chapters carry a `try`.** `APPLIED (partial)`
Movement III is "The systems" — courts, documentation, housing, benefits
— seven chapters of the most action-dense material in the book, with
almost no actionable device anywhere in it. Documentation is the clearest
case: the book tells the reader a record matters and never shows them
what one entry looks like. This is the exact failure mode *The Repair*
names as its enemy — a reader finishes, feels understood, and does
nothing — arriving in a book that never named it.

**3. The keepable card advertises the book as unfinished.** `APPLIED`
*Corrected mid-pass.* My first version of this finding said the book hands
the reader nothing keepable. That was wrong — Appendix A ("The card")
exists, is good, and already carries the documentation instruction. The
actual defect is that the card contains a live section headed **"Filling
in as the book is written"**, listing Movement III and the rebuilding
material as still to come, on a book whose own footer says all forty-five
chapters are complete. A reader consulting the one page meant to be kept
is told the book is a work in progress. *At Will* shipped the identical
block, and there the very next heading delivers exactly what the stale
list promises.
Removed from both. Separately: chapter 16 told the reader a record
matters without ever showing one, so the card's instruction had nothing
concrete behind it — a four-line entry template is now in the chapter.

**4. Nineteen of forty-five chapters are the identical shape.** `OPEN`
`p · h3 · p · pull · h3 · p`, nineteen times. In a book read
non-linearly at 2am over a period of years, identical shape means
identical weight, and the reader can't triage. Chapter 28 (clinical
crisis) and chapter 2 (the escalation window) look exactly like chapter
23 (sleep). *The Repair* solved this without trying — 48 chapters, 48
distinct shapes — because its chapters were specced individually.
Not done this round: it is a rewrite of roughly 19 chapters, and doing it
badly would cost more than the flat shape does.

**5. The escalation warning is the most important thing in the book and
it is in chapter 2.** `APPLIED`
Chapter 2 tells the reader that things commonly get harder right after
leaving — and it is right that this is the load-bearing fact. But a
reader who arrives at chapter 30 in the middle of an escalation has no
route back to it, and the book's own structure means most readers arrive
non-linearly. The fact needs to be reachable from where the reader
actually is, not only from where the book put it.

---

## THE SILENCE

*46 chapters · 248 words/chapter · men in coercive relationships*
Brief: plain, direct, unadorned. "A friend giving him a straight answer."
Never "brave." The hardest sentence: *this exists alongside the book for
women, not instead of it.*

**1. The book's own hardest constraint has no test.** `APPLIED`
The brief states it plainly: if any chapter could be quoted to argue that
women's services should be cut, that chapter needs rewriting. That is a
checkable property and nothing checked it. `qa.js` tests for manipulation
patterns, exclamation marks and engagement mechanics, but not for the one
failure this particular book was written to avoid.
Added to `qa.js` as AUDIT 6: comparative-suffering constructions,
zero-sum services framing, and grievance rhetoric are flagged everywhere
except chapter 3, which is the one chapter licensed to state the position.
**The book passes it clean** — the constraint was held in the writing all
along, it simply had nothing verifying it. The value is in the next
revision, not this one.

**2. Sixteen binary contrasts, and this is the audience least able to
tolerate them.** `APPLIED (slop pass)`
"It's not X, it's Y" at 1.40 per 1,000 words — the highest in the set
outside *The Repair*. That cadence is the rhetorical signature of the
content this book is most trying not to be mistaken for. A man who has
already been pitched by manosphere material recognises the rhythm before
he processes the sentence, and the brief's own answer is "plain, direct,
unadorned." The binary contrast is none of those.

**3. Chapter 17 is the chapter most likely to be read minutes before an
event, and it defers.** `APPLIED`
"The police call" opens with a genuine emergency warning, then says
*"Everything in chapter fifteen applies here directly."* A cross-reference
is a reasonable device in most of this book. It is the wrong device in the
one chapter a reader opens under maximum cognitive load, possibly with
police already on the way. That chapter has to stand alone.

**4. No exit.** `APPLIED` — see the cross-book finding above.

**5. The book ends by telling the reader what to conclude.** `APPLIED`
*"Go and build the life. It's the whole of what's on offer, and it's more
than enough to be worth having."* Forty-five chapters of not instructing
a man about his feelings, then a closing imperative and a verdict on
whether what he's been given is enough. The brief says: say what happened,
then say what to do. The close does neither — it does a third thing the
rest of the book is careful not to do.

---

## AT WILL

*47 chapters · 201 words/chapter · the coercive workplace*
Brief: read "on a lunch break or in a car in the car park before a
shift." Teach the pattern universally, route the specifics.

**1. Zero help routing of any kind, across forty-seven chapters.**
`APPLIED`
No crisis line, no clinician, no helpline, nothing — the only route out of
this book is a labour ministry. The other three books in this set all
route somewhere. A reader sitting in a car park before a shift, which is
the brief's own image of this reader, is not in a neutral state, and
Movement IV ("Who is doing it") and the bullying and humiliation material
in Movement II are the parts of this subject that do the most
psychological damage. Naming a labour regulator is the right route for the
employment problem and the wrong one for the person.

**2. Four of forty-seven chapters carry a `try` — and Movement VI is
called "Your options."** `APPLIED (partial)`
Eight chapters about the moves available to the reader, with an actionable
device in almost none of them. The book's stated objective is that a
reader "know the actual sequence of moves available to them." Explaining
a move and equipping someone to make it are different, and this book
currently does the first.

**3. The sequencing constraint is better covered than I first credited.**
`CORRECTED — partially APPLIED`
My first version of this finding said the ordering rule is taught as prose
where it should be a safety rule. Checking the text: chapter 37 already
carries it as a `warn` box, and it is well written — it names the
retaliation risk, says document first, and warns about timing around
review cycles. Appendix A carries the full ordering too. The finding as
originally written was wrong.
What survives it: chapter 36, the documentation chapter the whole sequence
depends on, described what to record without showing a single entry. Same
gap as *The Long After* chapter 16, same fix — a four-line template now
sits in the chapter.

**4. Eleven chapters share one shape, and Movement II is ten chapters of
"the moves."** `OPEN`
Ten consecutive same-shaped chapters describing ten different tactics will
read as one long list, which is the opposite of what a taxonomy is for.
Same reason as *The Long After* #4: not done this round because doing it
properly is a rewrite, not a formatting change.

**5. The book closes on collective action, which is correct and in the
wrong place.** `APPLIED`
Chapter 47 argues that individual remedies don't change the incentive
structure. That is true, it is the honest conclusion, and it matches what
*The Loop* independently concluded. But it is the last thing the reader
reads, and the reader opened this book because something is happening to
*them*. Ending there tells someone in personal distress that their own
remedy won't fix anything. The analysis stays; it stops being the final
word.

---

## THE REPAIR

*48 chapters · 579 words/chapter · people who have done harm*
Brief: relief is the enemy. Behaviour change measured in months by the
people affected, not insight, not remorse.
**This is the strongest of the four by a wide margin** — 48 distinct
chapter shapes, a `try` in 58% of chapters, lists in 68%. The findings
below are sharper because the book is better, not worse.

**1. The prose style manufactures the exact thing the book calls its
enemy.** `APPLIED (slop pass)`
48 binary contrasts and 36 colon reveals — by a distance the highest
density in the set. Both are insight-shaped devices: they produce the
click of understanding without adding information. In any other book
that is a style note. In this one it is a content problem, because the
book's own standing rule is that a paragraph which makes the reader feel
better without changing what they do on Thursday must be cut, and these
two devices are how prose does that.

**2. The reader's instrument for the relief test exists — at chapter 47.**
`CORRECTED — APPLIED`
My first version said the book gives the reader no way to run the relief
test on themselves. Wrong: chapter 47, "The people who use this book as a
shield," is exactly that instrument, and it is the sharpest chapter in the
book — citing it in arguments, telling them you're reading it, fluency
without change, reframing, the book as the work, producing it as evidence.
The defect is placement, not absence. The book's own audit says the reader
will reach for a comfortable exit *within days*; the check for that is
forty-six chapters deep, reachable only in sequence. Now on the contents
screen as its own route, so it is available on day three.

**3. The two exits are named once, in chapter 2, and never re-tested.**
`APPLIED`
The audit's own words: the reader "will reach for one of the two within
days." The book knows this will happen and has nothing waiting where it
happens — Movement V (Stopping) and Movement VII (The rest of your life)
are exactly where "I'm actually fine" reasserts and neither checks for it.

**4. Chapter 37 carries the serious-harm material and is thinly
reachable.** `APPLIED`
It is linked from the top bar and cross-referenced from 34 and 36. For
the one chapter in the book that handles danger-to-others markers, in a
book whose readers are by definition people who have caused harm, three
routes in a 48-chapter book is thin.

**5. Nothing routes the person who arrives from the other side.** `OPEN`
Chapter 5 turns away four reader-motives, all of them versions of the
person who did the harm. The predictable fifth reader is the person it was
done to, checking what this book says about them — a book about their
situation, written for the other party. There is no line anywhere pointing
them to *The Long After* or *Sovereign*.
Not applied: where this goes is a real editorial decision (chapter 5 is
`[H]` and its turning-away is load-bearing), and it is the one finding
here I'd want the author's call on rather than mine.

---

## THE SLOW TAKE

*45 chapters · 221 words/chapter · elder financial exploitation*
Brief: written for the **adult child**, not the person it is happening to,
because "an elderly parent being isolated and exploited is, by the nature
of the harm, the least likely person to go looking for a book about it."
Voice steady, warm, unhurried, never clinical, never alarmist. The hardest
problem, stated once and never abandoned: *autonomy is not safety, and
safety is not the only value.*

**1. Zero reporting routes across forty-five chapters.** `APPLIED`
This is the subject with the most developed reporting infrastructure of the
five — adult protective services, adult safeguarding, an elder-abuse
helpline, and every large bank's own financial-abuse team — and the book
named none of them as a route. The bar pointed at chapter 33. A reader who
has just realised what is happening needs the category and the search
string, not a chapter. Now a `#/help` page, with the bank row placed second
because it is usually the fastest intervention actually available.

**2. Chapter 36 calls a record "the single most useful thing you can
create" and never shows one.** `APPLIED`
Third book in the set with this exact gap. The version here needed one
extra thing the other two did not: this reader is recording observations
about a parent whose competence is in dispute, so the template insists on
observed rather than inferred — *"asked me twice in one visit who had been
paying the gas bill,"* not *"seemed confused about the money."* A record of
observations survives someone disputing the interpretation. A record of
conclusions does not.

**3. Chapter 42 is the safeguard the brief calls "not optional," at 42 of
45.** `APPLIED`
"Am I the one benefiting?" is the chapter that exists because an adult
child exploiting a parent could use this book as a manual to spot what a
sibling might notice. It is a genuinely good chapter with a real self-audit
in it. It was reachable only by reading forty-one chapters first. Now on
the contents screen, next to chapter 40 — which is the other decision this
reader actually has to make.

**4. The stale card block, for the third time in five books.** `APPLIED`
"Filling in as the book is written," listing the full action sequence and
the reporting routes as still to come, on a finished book — and, exactly as
in *At Will*, the very next heading on the same card already delivers the
list it promises. Three of five books shipped this identical defect, which
makes it a property of the scaffold rather than three separate oversights.

**5. `try` in three of forty-five chapters, with Movement VI titled
"Acting."** `OPEN`
Same shape as the other books, and sharpest here: this reader is not
reading to understand, they are reading to find out what to do this week.
One template was added (finding 2). The rest is a real content pass rather
than a formatting change, so it is named and left.

---

## The finding that only appears with five books side by side

Four defects show up in three or more of the five, in the same form, and
one shows up in all five:

| defect | books affected |
|---|---|
| no way off the page | all five |
| the persistent help bar points at a chapter, not at help | all five |
| a documentation chapter that never shows an entry | The Long After, At Will, The Slow Take |
| "Filling in as the book is written" on a finished book | The Long After, At Will, The Slow Take |
| the book's own safeguard chapter placed at the very end | The Repair (47/48), The Slow Take (42/45) |

These are not five books with similar oversights. They are one scaffold's
gaps, inherited five times. The practical consequence: fixing them in a
book fixes one instance, and the sixth book will arrive with all of them
again unless the scaffold changes. `books/BOOK-TEMPLATE-NOTES.md` records
what a new book needs to carry from the start.
