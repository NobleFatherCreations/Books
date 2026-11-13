# Steelman audit of "Why I Wrote This" (written 2026-11-13 by Opus 5.5)

The owner asked for the strongest case against the delivered PDF (53 pp master, 56 pp Foil), measured against everything they provided and asked for. Result: a big step up from the first build, but five important shortfalls. The blueprint (`BLUEPRINT.md`) is the fix.

## Scorecard

| What the owner asked for | Grade | One line |
|---|---|---|
| Use all the information provided | Partial | Several key sources never opened or only skimmed. |
| Flowing, coherent organization | Partial | Six movements work; two-page reference tables in the middle stall the story. |
| See the whole and find what the owner didn't | Partial | 15 connections; none tested against the research or the Fractal² data. |
| How the work helps the world through 3 levels and 30 sectors | **Missed** | No sector-by-sector or level-by-level account of the good it does. |
| How the Fractal, the playbook and the combos work together | Weak | The playbook (Pattern Decoder) got one sentence. |
| Use everything as context, then write own synthesis | Partial | Too much reused/shortened; too little synthesis. |
| Psychological levers throughout | Partial | Strong in hook, scenes, ending; absent across about 25 middle pages of tables. |
| Read and incorporate everything | **No** | Owner's origin account, the Value-and-Impact report, playbook structure, much of the War Map skipped. |
| Use every helpful skill and MCP | **No** | Promised a `no-ai-slop` pass and didn't run it. Skipped `design-director`, which the repo makes binding for visual work. |
| Ask when unsure, don't assume | Partial | Asked, then went ahead on defaults where unanswered. |

## 1. Sources missed or used badly

- **The owner's own origin account (biggest miss).** Already exists, locked, in `content/fractal2/intro-final.md` lines 271-282 ("Why I can draw this"). Never opened. A paragraph in the owner's voice was invented instead. Fix: insert verbatim, with a test that fails the build if one character differs.
- **The Value-and-Impact report** (`design/fractal2/reports/value-and-impact.html`, PDF in `library/fractal2/review/`). Attached twice, never opened. Unused: the five things The Fractal does; nine predecessors (Biderman, Freire, Illich, Forbes, Dutton and Painter, Wink, Herman, Stark, Fricker); the change-in-scale table (335 tactics, 1,005 examples per sector, 30,150 across thirty; 153 combinations in sector one, 203 on the master list); why sequences change lives; the size of the need in numbers; seven mechanisms with evidence strength; eight maps that changed things and six lessons; the traditions table with unused parallels; sixteen ways it could help nobody has named; seven risks; "what this work is worth". Fix: BLUEPRINT Part H places every piece.
- **The playbook / Pattern Decoder.** 310 entries, five parts each (In short, Understand it, Is this it?, What you can do, Go deeper), 105 with a safety-first note. Fractal²'s 300+ tactics per sector come from it. Got one sentence. Fix: new section "One tactic through every work" (Intermittent Reinforcement across Decoder, Fractal, Fractal², combinations, Playground Protectors).
- **The War Map**, pasted twice. Front 2 by sector, redirecting money, ten commons, intergenerational memory, full metrics table, sector reclamation practices, laws list were condensed or dropped. Fix: restore in the owner's wording; laws go in Reference, labelled as one possible program.
- **Owner's combo scripts.** Shortened; lost: Trauma Bond Engine vs Love Addiction Engineering; "a combo is always greater than the sum of its parts"; three architectures (early/mid/late); most tactic-by-tactic breakdowns.
- **The Fractal itself.** Unused: The Largest Body (6,260 words), The Origin's 10,000-year history, the Frequency chapter's "what it sounds like / looks like in practice", the closing monologue's "you went down, not up" and tradition-by-tradition passages; The Sacred Divide (34 traditions) only a number.
- **The Claude artifact** (shared page of combo and tactic files): read only a summary. Ten combo family names not examined; the Corporate sector's 138 combinations counted from the summary, not a file.

## 2. Flow and coherence

- Story stalls in Movement 2: stage table, two pages of techniques, 30 impulse cards, two pages of sectors = about 8 pages of reference before anything happens.
- Movement 3 out of order: the frequency sits between "Book 1 in numbers" and the step into Fractal².
- Numbers clash between documents: PDF says 2,700 examples (owner's choice); the Book 1 audit says 2,340 published (26 of 30 sectors).
- Page 2 machine diagram labels the frequency box "Sections 5, 8"; should be "Sections 4, 8".
- No PDF bookmarks in a 53-page "interactive" document.

## 3. Seeing what the owner didn't

Done: 15 connections (8 whole-map, 7 from combinations). Genuinely new: combination families travel between sectors; every combination has the same kind of turning point; the thirty read backwards are a character curriculum; machines hand their output to each other.
Not done: test any of it against real data (count the 291 combos by family; check the turning-point claim on a sample); connect the other instruments (Decoder, Sacred Divide, Playground Protectors, Root, Loop) as one system; map how the 30 sectors prime each other across a lifetime (one paragraph and one 7-node diagram only).

## 4. How it helps the world (biggest content gap)

Asked for: detail through the 3 levels and 30 sectors. Delivered: one ripple diagram, five levels of change (mine, not the owner's three), eight "world that saw it" scenes, one reclamation practice per sector. Missing: for each of the 30 sectors, what the work does for a person, the sector's institutions, and society. Fix: BLUEPRINT Part D, a 30-row table in lifespan order.

## 5. How the three works fit together

Done: alphabet / dictionary / sentences ladder. Missing: the working relationship (Decoder holds definitions; Book 1 proves the pattern runs across thirty sectors; Fractal² applies the Decoder's tactics to each sector at three scales; combinations sequence them into lives; Playground Protectors brings it to children). Fix: "One tactic through every work" plus the four verbs (see, name, break, return).

## 6. Psychological levers

Used: open loop in the hook; second-person scenes; concrete before abstract; original-versus-copy contrast; "Stop and notice" pauses; a small ask; hopeful ending scene.
Missing or weak: the author's story (strongest trust lever); peak-end (the emotional peak was followed by about 20 pages of tables); curiosity hooks between sections; identity ("you can now see it"); the disclosure-of-levers page read as an essay instead of the last proof.

## 7. Skills and MCP servers

| Tool | Status | Why |
|---|---|---|
| `pdf`, `dataviz` | Used | Rendering; colours validated for the first draft (`#B97F00,#2A6FC9,#D4502F,#0F8F84,#9A46C4`), not re-checked for new diagrams. |
| `no-ai-slop` / `copy-editing` | Promised, not used | Skipped. |
| `design-director` | Not used | Repo rule says binding for visual work. |
| Google Drive | Not used | Owner never answered the question. |
| `sequential-thinking` | Not used | Would have helped plan the weave. |
| Canva / Adobe | Skipped on purpose | HTML pipeline gives more control at lower cost. |

## 8. Process failures

- Assumed answers to questions asked (prayer, owner's story paragraph, composites in the public edition).
- Two facts in the composites unverified: the psychologist-to-student ratio (about 1:500 recommended) and the referral-rate disparity.
- Delivered without a steelman pass.

## Further gaps found afterwards (BLUEPRINT still needs a row)

- The Largest Body and The Origin's history are not placed in the blueprint.
- The data checks are not run.
- `design-director` is not in the execution prompt.
- Decoder files not re-read.

## How the blueprint answers it (short)

1. Origin story verbatim, test-locked. 2. Value-and-Impact report woven through (Part H). 3. Decoder as the "name" verb. 4. War Map restored in the owner's words. 5. Combo theory restored. 6. Four tables become one-page summaries; full versions in Reference. 7. Frequency moved after the Fractal² step. 8. Sections 12 data tests (family count, turning point, time-or-witness tags). 9. 30 sector cards in lifespan order. 10. Ten architect insights as the spine. 11. Page grammar: picture, sentence, example, question. 12. Limits and predecessors up front for professional trust. 13. Identity line before the ask; persuasion page cut to half a page, last. 14. Fix labels, add bookmarks, cite or soften two facts.
