# BOOKS — per-book content summary + reference-site adaptation plan

**This is the file to point another AI at for "what's built into each
book."** It's the one place that summarizes actual confirmed content,
theme, and design stance per book — not just URLs (that's `sites.json`) or
raw chapter data (that's `chapters.json`). Read `MEMORY.md` first for
overall project status, then this file for book-specific work.

Confidence is labeled per book: **confirmed** = verified against the book's
own live/source HTML directly in this session. **from review doc** =
taken from the user-supplied `source/REVIEW-SUMMARY.md`, not independently
re-verified against content. **inferred** = guessed from tagline/title
only — do not treat as fact, check before acting.

---

## The 3 references, and what they actually mean per pass

- **Stripe Press** → typography weight + "this is a real object" feel: a
  title/cover page, dramatic type scale, considered physical presentation.
- **Aeon** → long-form reading comfort: optimal measure (~60–70 char),
  line-height, and (where appropriate) a position/progress indicator.
- **Wait But Why** → wayfinding across many chapters: a real contents page,
  "chapter N of M," a resources hub.

None of these are default-on. Each book gets checked against its own
stance before any of the three gets applied — see Loop below for why that
matters.

---

## loop — The Loop **[confirmed, deeply]**

*"The machine that learns you."* 47 chapters, 8 movements. Content: algorithmic
manipulation, engagement-mechanic design, ad auctions, dark patterns.

**Design status:** already excellent. Self-hosted Fraunces + Public Sans,
20 proper `@font-face` rules, own scroll fade-ins (`.fx-reveal`), own
sticky nav bar, own THE HOUSE tab (was the source of the original leak,
fix ready in `library/loop/index.html`).

**Explicit stance (its own text):** *"this book has no streaks, no
progress bar, no completion percentage, no badge... no stored reading
position."* This is the book's argument, not an oversight.

**Reference adaptation:**
- Stripe Press (cover/type) — ✅ fine to consider, doesn't touch the
  engagement-mechanic taboo. Type scale already strong.
- Aeon (reading comfort minus progress bar) — ✅ measure/line-height fine.
  ❌ **do not add a progress bar, chapter-position counter, or completion
  indicator of any kind.**
- Wait But Why (contents page) — ✅ fine, a table of contents is
  navigation, not a progress mechanic — but keep it a plain list, not a
  gamified "X of 47 read" tracker.

## scale — The Weighing **[confirmed: chapter data, design status, and stance]**

*"How to be right about people."* 38 chapters, 6 movements — calibration,
judgment, evidence-weighing. Real chapter data extracted, same MOVEMENTS/CH
format as Loop (same author, same hand-built engine).

**Design status:** fonts self-hosted (fixed this session). Stance
**confirmed** by a dedicated content-review pass (2026-08-02, see
`.audit-view/scale-content-review.md`): the book states its own house
rules verbatim — *"House rules: no streaks, no progress %, no nags, no
tracking"* (code comment) plus matching hero/footer badges ("No account ·
No tracking · Nothing stored · Works offline · Free forever"). Same
no-gamification stance as Loop, confirmed rather than inferred. It does
show a plain "N of 38" position locator in the chapter crumb — that's a
location marker, not a progress bar, and should stay that way.

That same review also found: Loop cites Scale ~8 times by name and by
direct anchor link (chs. 16, 17, 33, 35 especially — ch. 44 even frames
itself as "The Weighing, applied to this book's own material"), but Scale
never once names or links back to Loop anywhere in its 38 chapters, despite
naming other siblings (Fractal, the Codex) inline elsewhere. Chapter 19's
closing line is an unlinked tease that clearly means Loop ("that is a
different book, and it is coming") — the natural place for a reciprocal
link. Also: Scale's Appendix A field card only draws from 13 of 38
chapters — Movements II and V are completely absent, and chapter 34 (which
the text itself calls "the only mechanism that keeps improving after you
finish the book") is missing from the one artifact meant to be kept.

**Reference adaptation:** stance is now confirmed clean — all 3 references
apply without conflict (calibration/judgment content doesn't call for an anti-progress
stance the way Loop's does, but confirm, don't assume).

## faith — The Coercive Control Codex **[confirmed]**

25–27 traditions × tactics matrix, evidence-graded. **Confirmed in the
book's own text:** *"It will not measure you. No analytics, no tracking,
no storage, no external requests."* Same self-contained ethos as Loop, even
more explicit. A related but distinct edition (`library/_undeployed/faith-offline-edition.html`,
5/8 passes done) adds: *"no engagement mechanics"* full stop, and
deliberately carries **no shared site chrome at all** (hand-to-person,
offline, sometimes read by people monitored at home).

**Design status (live page):** still has the leaked HOUSE-tab comment
(fix ready, unshipped). A full redesign exists (`library/_undeployed/sacred-divide-faith-redesign.html`,
"The Sacred Divide") — parchment + dark theme, three-register tactic
entries — not deployed, your call pending ("let me look first").

**Reference adaptation:**
- Stripe Press — ⚠️ a cover/title moment is fine in spirit, but keep it
  restrained — this book's whole design language (per Sacred Divide's own
  notes) is about *evidentiary* weight, not luxury-object feel. Gilt rules
  and stamps, not glow effects.
- Aeon — ✅ reading comfort/measure, yes. ❌ no progress bar (same logic as
  Loop, arguably stronger — this book is explicitly anti-tracking).
- Wait But Why — ✅ but the "resources hub" idea fits especially well here
  given the gambling/crisis-support callout pattern already established —
  a calm, findable resources section matters more than usual.

## children — Playground Protectors **[from review doc]**

Kids' book on manipulation/tricky people, written for two audiences at
once (kids + accompanying adults, with an "adult fog" mechanic that hides
adult-register passages from children specifically). Per the review doc:
already has power-up bursts, confetti tied to its own "lighting a mission"
mechanic, per-world weather, comic-panel staggered entrances.

**This is the opposite case from Loop: gamification is *correct* here.**
It's a children's book — motion, reward, and delight are appropriate to
the audience, not a manipulation pattern to avoid.

**Reference adaptation:**
- Stripe Press — ❌ mostly doesn't fit; "premium object" restraint reads
  as cold for a kids' book. Skip.
- Aeon — ❌ optimal adult-prose measure doesn't apply; this isn't long-form
  reading for adults.
- Wait But Why — ✅ partially — the "worlds/missions" structure could use
  a clear map, but keep it playful, not the calm-editorial WBW style.
- **This book mostly doesn't want any of the 3 references as-is.** Treat
  it as its own design language; the review doc's existing work already
  fits it better than importing outside patterns would.

## wook — The Festie Codex **[from review doc + this repo's own file]**

Festival & field harm reduction. Per review doc: "zine-style hard-shadow
buttons." **Unresolved discrepancy** (see `MEMORY.md`): this repo's own
tracked `festie-codex-full.html` has a different title than the review
package's `library/wook/index.html` — diff before doing
any design work here.

**Reference adaptation (tentative, pending the diff above):**
- Stripe Press — ⚠️ likely wrong fit — "zine" aesthetic is intentionally
  raw/DIY, not premium-polished. Don't smooth this one over by default.
- Aeon — probably fine for any long-form sections, unconfirmed.
- Wait But Why — likely useful if content is chapter-like; unconfirmed
  structure.

## fractal — The Fractal **[from review doc]**

"The architecture, 29 sectors wide." Per review doc: already has "cover
entrances and pull-quote marks" — i.e., a Stripe-Press-like cover moment is
already partially built.

**Reference adaptation:** Stripe Press — ✅ already partially applied,
extend rather than redo. Aeon/WBW — unconfirmed, no chapter data extracted
yet (checked directly: no MOVEMENTS/CH pattern found).

## fracture — The Fracture (was "All Fracture", then "The Fracture Everywhere"; shortened to "The Fracture" 2026-08-12) **[from review doc]**

"The wealth transfer · 195 citations." Title in review doc: "All Fracture
— The Reading Edition" (old title). Per review doc: has a "Fraunces drop cap"
already — a Stripe-Press-style typographic flourish already exists.

**Reference adaptation:** Stripe Press — ✅ partially done (drop cap).
Aeon — likely a strong fit given "Reading Edition" framing suggests it's
meant for sustained reading already. Wait But Why — the "sibling of Loop"
relationship (per Loop's own chapter 19 blurb) suggests cross-linking
between the two would help both books' navigation. **No chapter data
extracted yet — different authoring format than Loop/Scale, confirmed by
direct check.**

## feminine — The Sovereign Divine Feminine **[from review doc]**

42 chapters, recovery for women. Per review doc: "brass chapter rules"
already exist — another partial Stripe Press treatment in place.

**Reference adaptation:** Stripe Press — ✅ partially done, extend. Aeon —
likely fits (42 chapters implies sustained long-form reading). Wait But
Why — a real contents page would help at 42 chapters; no chapter data
extracted yet.

## shadowroot — The Root **[from review doc, deeply described]**

18-step guided shadow-work practice, not a conventional chapter book —
described in the review doc as having a "plumb line" depth visualization,
breathing exercise synced to a 12-second count, body-map interaction.

**This is a guided tool/practice, not a reading book.** Forcing Wait But
Why's "contents page" framing onto an 18-step sequential practice would
work against its design (you're meant to move through it in order, once,
not browse it like a table of contents).

**Reference adaptation:** Stripe Press — maybe for an opening/closing
moment only. Aeon — the reading-comfort typography still applies to its
prose passages. Wait But Why — ❌ skip; a step sequence isn't a chapter
index.

## playbook — The Pattern Decoder **[inferred from tagline only]**

"349 tactics · type what happened." Tagline suggests an interactive
lookup/matching tool (you describe a situation, it identifies the tactic),
not a linear book. **Not independently investigated this session.**

**Reference adaptation:** Unconfirmed — likely more Wait But Why (findable,
searchable) than Aeon (this probably isn't meant to be read start-to-finish).
Check its actual structure before planning further.

## music — The Listening Room **[confirmed: rebuilt from the audio itself, 2026-08-12]**

"Sorted by what each song is for." Not a book — a media page, and the only
project whose payload is not a single HTML file (176 mp3s alongside it). The
3 book-shaped references mostly don't apply; the press.stripe.com "title/cover
moment" does, and drove the record-sleeve treatment.

**Content (measured, not inferred):** 176 tracks, 14h 50m, recovered from the
user's Drive folder `14TecSqJSZOlYlT7bHPsKqBdHsGdUC0ea` ("MP3 music") plus its
`dad` and `New` subfolders. 183 files seen; 7 pairs turned out to be the same
Suno generation saved under two names (identified by the `id=` in the ID3
comment) and were collapsed to one track each, the discarded name kept in
`alsoKnownAs`. **Durations come from `ffprobe`, never estimated.** Titles are
derived from filenames — 173 of 176 files have no ID3 title, only a
"made with suno" comment carrying a real creation date and generation id.

**Six shelves, by purpose not genre** (the one editorial layer — assigned from
title keywords, since these files carry no genre metadata):
The Reckoning (39) · The Descent (23) · The Frequency (38) ·
The Dragon Cycle (10) · The Festival Floor (52) · The Tender Room (14).
A seventh catch-all shelf, The Wider Catalogue, exists in the data model but is
currently empty and does not render.

**Design stance:** dark, brass single accent, Fraunces + Karla only (timecodes
use `tabular-nums` rather than a third face). Per-track sleeve art is generated
from the shelf's hue, so colour actually encodes which shelf a track is on. This
book WANTS a player and real motion — it is the opposite case to Loop and faith,
which refuse interactive flourish. Autoplay is forbidden here (a past autoplay
hijack was a real bug on the hub).

**Architecture note — the exception to "one self-contained file":** the audio
cannot be inlined, so it is the only external request any project makes. Every
audio URL is therefore ABSOLUTE (`https://noblemusic.netlify.app/audio/…`),
because the page is served both at its own domain and at
`noblefathercreations.com/music` through a proxy rewrite.

**Generated, not hand-maintained:** `python3 scripts/build-music.py` reads
`deploy/music/MANIFEST.json` and writes `deploy/music/index.html` and
a single copy at `instruments/music/index.html`. Do not hand-edit
either output.

---

## Priority order for finishing this plan

1. Diff wook's two candidate files (blocking any wook design work).
2. ~~Check scale for its own stance statements~~ — done, confirmed clean
   (2026-08-02).
3. Extract chapter data for fracture/feminine (both already have partial
   Stripe Press treatment per the review doc — worth finishing what's
   started before adding new patterns).
4. Investigate playbook/root/music structure directly rather than relying
   on tagline inference.

---

# The 2026-08 intake — five new books

All five arrived complete and self-audited (each ships its own
`BOOK-MAP.md`, `AUDIT.md` and `qa.js`), from one shared scaffold. They live
in `library/<slug>/` (the site's own "Library" section — see `CLAUDE.md`'s
repo-layout rule) rather than in a flat `source/projects/`, because each is a
directory with its spec and its test alongside the page.

**None of them is deployed.** They are in the repo, they pass their own
`qa.js` and a Playwright check, and they have no HOUSE tab yet — that has to
come from the generator, not another hand-paste, per the rule this repo
already has and the 2026-08-12 audit's root cause.

Read `library/PSYCHOLOGIST-AUDIT.md` for the content findings,
`library/PROOFREAD-NOTES.md` for what the prose pass changed and what it
deliberately left, `library/DESIGN.md` for the design reasoning, and
`library/BOOK-TEMPLATE-NOTES.md` for what book six must carry from the start.

## longafter — The Long After **[confirmed, worked on directly]**

*"What happens once you have left."* 45 chapters, 7 movements, ~9.6k words.
Post-separation abuse: the coercion changing channel rather than stopping,
the systems (courts, documentation, housing, benefits), what the body is
doing, and rebuilding over years. Sits after *Sovereign*, which ends at the
door.

**Stance:** the most patient voice in the library. Its own brief: read
slowly, re-read, "often opened at 2am." Never prescriptive about feelings,
never a universal timeline.

**Design:** Newsreader, self-hosted. The loosest leading and most air of the
five; movement breaks drawn as a horizon that fades out at both ends. The
one book of the five that keeps a card grid — a held container is right
here. Dusk/plum.

**Reference adaptation:** Stripe Press cover moment ✅. Aeon measure ✅.
Wait But Why contents ✅. No stance conflict — this book has no
anti-gamification argument to violate, unlike Loop.

## silence — The Silence **[confirmed, worked on directly]**

*"For men in coercive relationships."* 46 chapters, 7 movements, ~11.4k
words. Recognition, what actually exists to help, and what to do. Sits
beside *Sovereign*, explicitly not instead of it.

**Stance — and this one is load-bearing:** its brief names the single
hardest sentence in the book, *this exists alongside the book for women,
not instead of it*, and the rule that any chapter quotable as an argument
for cutting women's services needs rewriting. That is now a test:
`qa.js` AUDIT 6 flags comparative-grievance constructions everywhere except
chapter 3, which is licensed to state the position once. **The book passes
it clean.**

**Design:** Source Serif 4. The only book of the five whose design argument
is subtraction — no italic hero, no cards, a plain ruled list, tighter
measure. Its brief asks for *less* literary, on purpose. Cool blue-grey.

## atwill — At Will **[confirmed, worked on directly]**

*"The coercive workplace."* 47 chapters, 7 movements, ~9.5k words. Runs
*The Fractal*'s eight-stage architecture on a job, the way *The Loop* did
for platforms. Teaches the pattern universally and routes the specifics,
because employment law varies by country and often by region.

**Stance:** names when nobody is choosing the harm — when an incentive
structure produces it with no villain required — and does not let that
excuse anyone who is choosing. Read "on a lunch break or in a car in the
car park before a shift."

**Design:** Spectral. A working file: a rule under the masthead like a form
header, movement titles underscored in full ink, chapters as filed rows.
Orderly rather than cold. Navy/brass.

## repair — The Repair **[confirmed, worked on directly]**

*"For the person on the other side of it."* 48 chapters, 7 movements, ~27.7k
words — nearly three times the density of the others, and structurally the
strongest of the five before any work: 48 distinct chapter shapes, a `try`
in 58% of chapters.

**Stance:** relief is the enemy. Success is behaviour change measured over
months by the people affected, not insight and not remorse. The brief's
standing rule: *if a paragraph would make the reader feel better about
themselves without changing what they will do on Thursday, cut it.* It
blocks two exits by name — "I'm a monster" and "I'm actually fine."

**Design:** Crimson Text. A ledger, because chapter 2 writes the brief
itself: *"That is a record, not an identity."* Hairline rules, numerals in
their own column, every radius squared off, nothing raised, accent reserved
for danger. **No warmth that could read as absolution** — that applies to
the design as much as the prose. Stone/oxblood.

**Do not soften chapters 2, 5 and 47.** The book says so and it is right:
they are what stop it being used as a shield.

## slowtake — The Slow Take **[confirmed, worked on directly]**

*"Elder financial exploitation, for the adult child."* 45 chapters, 7
movements, ~10k words.

**The design decision that makes it findable:** it is not written for the
person it is happening to. An older adult being isolated and exploited is
the least likely person to search for a book about it; their adult child is
the one who searches.

**Stance — held, never resolved:** *autonomy is not safety, and safety is
not the only value.* An older adult keeps the right to make bad decisions
and trust the wrong person. Guardianship removes legal personhood and is
itself frequently abused. A book that picks a side produces either readers
who steamroll a competent adult or readers who watch and call it choice.
Chapter 42 ("Am I the one benefiting?") is not optional — it exists because
an adult child who is themselves the exploiter would read this.

**Design:** Hanken Grotesk — **the only book in the library not set in a
serif**, and the reason is the reader, not taste: a frightened, exhausted
adult child scanning on a phone for what to do next is doing
reference-manual reading, not linear reading. Chapters hang off a
continuous vertical thread, because a record built entry by entry over
months is what the book is asking for. Warm cream/olive/brass.
