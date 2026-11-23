# The Weighing: expansion outline (v5 target about 60,000 words)

Baseline 21,692 words in 38 chapters and 6 movements (plus 2 appendices). Owner intake 2026-11-23: about 60k words, new chapters allowed, voice "sharp thinking partner with more than normal humor that's blunt and no filter", worked-example label chosen at content freeze.

Inputs: `READABILITY.md`, `MESO.md`, `WORKLIST.md`, `research/SEARCH-DEMAND.md`, and the August content review (BOOKS.md: the field card drew from 13 of 38 chapters, with Movements II and V missing).

## Budget

| Block | Words |
|---|---:|
| Existing 38 chapters, grown from about 570 to about 1,000 each | 38,000 |
| 11 new chapters at about 1,100 | 12,000 |
| Start here (2 pages) | 1,800 |
| Toolbox (field card rebuilt, limits, questions, A to Z, 2 printable sheets) | 7,000 |
| **Total** | **about 59,000** |

## What every existing chapter gets (the writing pass, one agent per file)

1. **One worked example**: a short made-up scene in a `::: scene` block, opening with the label line (owner picks the wording at freeze; drafts below). It must show the chapter's tool being used on a real-feeling case, including one where the answer turns out to be "yes, it really was manipulation". The book can't only teach doubt.
2. **A closing step.** 12 chapters have no exercise now: you-learned-to-see, this-book-in-the-wrong-hands, the-discipline-of-three-explanations, secondhand-accounts, before-you-test-is-testing-safe, is-it-you-or-is-it-everyone, difference-is-not-malice, institutions-weigh-differently, being-wrong-well, certainty-is-the-tell, when-weighing-stops, trust-as-a-skill-you-rebuild.
3. **A handoff**: the last block links onward (7 of 40 do now).
4. **Headings in the reader's words** where they fit: "Am I the toxic one?", "Is it my gut or my anxiety?", "Red flag or just a flaw?" (SEARCH-DEMAND.md). Existing headings with inbound links stay word for word.
5. **A `question:` and `seo:` header** for each chapter (needed for the chapter page and the search index).
6. **Voice**: blunt, funny, precise. No jokes in or next to the three heavy chapters (this-book-in-the-wrong-hands, before-you-test-is-testing-safe, when-weighing-stops) or any safety line.
7. Break up the 30 paragraphs of 61 to 90 words. Fix the 2 legal lines that name no place.

## New chapters (11)

| Movement | Slug | Working title | The reader's question | Why |
|---|---|---|---|---|
| I | red-flag-flaw-or-dealbreaker | Red flag, flaw or dealbreaker | Is this a red flag or am I being picky? | "red flag vs flaw", "red flag vs dealbreaker" |
| II | gut-feeling-or-anxiety | Gut feeling or anxiety | How do I tell intuition from anxiety, OCD or old fear? | "trusting your gut vs anxiety" is the biggest gut cluster |
| II | when-people-say-youre-overreacting | When people say you're overreacting | How do I know if I'm overreacting? | "am i overreacting" (203 phrasings) |
| III | can-you-tell-when-someone-is-lying | Can you tell when someone is lying? | How do I tell if someone is lying to me? | largest cluster (235); honest answer: tells barely beat chance, so check the account against the record |
| III | reading-a-text-message | Reading a text message | What does this message actually mean? | "lying over text", tone, read receipts, reply times |
| IV | weighing-someone-new | Weighing someone new | How do I trust my read on a date or a new friend? | promised bridge from The Long After ("Dating again, and trusting your own read") |
| IV | weighing-family | Weighing your own family | Is my parent controlling or just difficult? | "am i overreacting about my parents" |
| IV | weighing-a-boss | Weighing a boss | Bad boss or a controlling one? | bridge to At Will |
| IV | weighing-a-friend | Weighing a friend | Is this friendship one-sided or just a hard season? | friendship gap |
| VI | weighing-after-youve-left | Weighing after you've left | How do I trust anyone again? | bridge to The Long After |
| VI | changing-your-mind-out-loud | Changing your mind out loud | How do I tell people I got it wrong, or right? | closes the being-wrong-well / assessment arc |

## Start here (new part)

- **What are you trying to weigh?** Six tiles (a partner, someone new, family, a friend, a boss or a group, yourself), each opening the 3 or 4 chapters that matter most. "In danger right now?" sits above the tiles and links to when-weighing-stops.
- **How to use this book.** What it is, what it isn't, the house rules (no streaks, no progress, no tracking), and the link to the limits page.

## Toolbox (new part; replaces "Appendices")

- **The field card**, rebuilt to draw from all six movements. It now includes Movement II (whose alarm is this? sensor or smoke alarm? the state you're judging from) and Movement V (the self-audit, translating the vocabulary, who benefits), plus chapter 34's track record.
- **The limits of this instrument** (existing; updated chapter numbers).
- **Questions people ask**: about 30 short answers in the reader's own search words, each linking to its chapter (FAQ schema).
- **A to Z**: the book's terms (base rate, the gradient, naming test, smoke alarm and so on), linked to the Pattern Decoder where a name matches.
- **The weighing sheet** (printable): the two-sided question, three explanations, the four pattern dimensions, assessment versus decision.
- **Your track record sheet** (printable): the three-line log from chapter 34, plus the fourth line.

## Worked-example label: drafts for the owner (pick at freeze)

1. "Made up, but you've met these people."
2. "A made-up case. Real enough to sting."
3. "Fiction, assembled from very common facts."
4. "Not a real person. A very real pattern."
5. "Invented for this page. Recognised by most readers."

## Order of work

Phase 0.5 builder next (`scripts/seo/build_scale_v2.py` on `scripts/book/shell.py`, Weighing skin), proven against the extracted text with `text-diff.py`. Then the new pages are written as pages first, existing files in reading order (one agent per file; brief in `V5-WRITING-BRIEF.md`; pilot on 01-i), Start here and Toolbox last. Then steelman and fact check, rebuild, every check, and content freeze.
