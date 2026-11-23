# The Long After: the full process map, and what to do better next time

Written 2026-11-22. Part 1 is the record: every step from the first edition to now, in order, taken from the git history, MEMORY.md and the files in `content/longafter-v2/`. Part 2 is the review: what was redundant, what went wrong, and the order to use for the next book.

---

# Part 1. The map

## Where we began
- **First edition (v1 to v4), live since 2026-09-01.** One page of JavaScript with 45 chapters. It arrived already self-audited, with its own BOOK-MAP.md, AUDIT.md and qa.js.
- **2026-11-21, SEO round 2.** `build_jsbook.py` produced crawlable chapter pages for the seven one-page books, The Long After among them. The covers and the seal menu were refreshed.

## Stage A. Audit and outline the second edition (2026-11-21, no book text changed)
| # | Step | Output | Commit |
|---|---|---|---|
| A1 | Full audit of the old book: content, voice, design, search | audit notes | 689e4918 |
| A2 | Second-edition outline: 10 parts, 69 chapters, start pages, toolbox, voice spec, layout, keyword map | BOOK-MAP-v2.md | 8f961c40 |
| A3 | Steelman round 1 on the outline: missing readers, 14 new chapters, safety, legal, clinical, search and editorial fixes | BOOK-MAP-v2.md §11 | d4caef23, 26f3d883 |

## Stage B. Write the second edition (2026-11-22)
| # | Step | Output | Commit |
|---|---|---|---|
| B1 | Plan registry (`make_plan.py` → plan.json), content audit script, production plan | longafter-audit.py, PRODUCTION.md | 46135217 |
| B2 | Write Start here and Parts I to XI, then the toolbox, one part per commit, with the audit passing on each | 96 pages, 47,600 words | 46135217 → 4078f090 |
| B3 | Strengthen the link web: every page linked from at least 2 others | 126 Decoder links, 53 Feminine links | 5c84962f |
| B4 | Verification pass 1: helplines and key laws, 4 corrections | FACTS.md | efd9ced9 |

## Stage C. Build and polish v5 (before the expansion)
| # | Step | Output | Commit |
|---|---|---|---|
| C1 | Generator: Markdown to static pages in the Dusk to first light design, with offline search, a whole-book page and old links forwarded | build_longafter_v2.py, 100 HTML files | a303bdba |
| C2 | Citations checked against Crossref (4 corrections), 23 short chapters expanded, AI-writing pattern pass (17 rewrites) | | 043e4ef9 |
| C3 | "Use every skill and MCP" round: 15 search-gap sections from keyword research, no-ai-slop and copy-edit passes, tap-to-call numbers, design critique fixes, schema citations, Topics and llms.txt wiring, on-page SEO audit, the one-command pipeline | longafter-pipeline.sh, onpage_longafter.py | d01bc089 |

## Stage D. The owner's correction, then the expansion
The owner said: "I didn't see you expand any chapters or audit or steelman." Stage C had polished a book that was still thin. The owner then set a binding order: outline, write, voice audit, no-AI-slop, steelman, fact check, and design last.

| # | Step | Output | Commit |
|---|---|---|---|
| D1 | Tracker built and the order saved to memory and sites.json | longafter-progress.py, CHECKLIST.md, progress.json | 86efffb1 |
| D2 | Expansion outline for every chapter | EXPANSION-OUTLINE.md | (in D3) |
| D3 | First expansion pass, part by part, with the audit passing each time | 55,682 → 87,431 words | 1acb489a → 82b49c2b (12 commits) |
| D4 | Second pass: a worked example in each chapter, labelled as made up, and a closing section with a chapter-specific heading | about 96,000 words | 51446705 → f2195764 (5 commits) |

## Stage E. Audits of the finished writing
| # | Step | What it found or fixed | Commit |
|---|---|---|---|
| E1 | Voice scorecard | median 97/100, 16 repeated headings renamed, 12 concrete pictures added | c77d1dd3 |
| E2 | Duplicate check (built after the fact) | repeated sections merged or cut in 13 chapters, plus the intimate images chapter | 0cac6bc5, 122d9e17 |
| E3 | No-AI-slop pass | 18 doubled hedges cut. A blanket "often" removal **was tried and reverted** because it made claims stronger than the evidence. | fccabf34 |
| E4 | Steelman round 2 on the finished book | 15 findings, 11 gaps filled (contempt of court, criminal trials, medication, teenagers, an ex who dies, religious divorce, a shared business and more) | 8afd2556 |
| E5 | Fact check passes 3 to 6 | 4 corrections, 28 source lines added that the new sections had missed | 1515b562 |
| E6 | Rebuild and full pipeline | passing | dd9a14b9 |

## Stage F. "Covered completely, not to a word count"
The owner said the goal was full coverage, not a word count, so the work moved from adding length to checking depth.

| # | Step | Output | Commit |
|---|---|---|---|
| F1 | Completeness audit: question sections under 45 words found and deepened | 12 answers deepened | 137888f6 |
| F2 | Decoder back-link finding: 5 books are missing from the Decoder's BOOKS list | saved to memory, not built | 137888f6 |
| F3 | Tone audit (seen, safe, in the right place), 21 glossary terms, sources appendix with verified links, full link check (2,601 internal, 74 external) | TONE-AUDIT.md, longafter-sources.py, dois.json, A to Z with 65 entries | f4208789 |

## Stage G. AI-writing audit v2
| # | Step | Output | Commit |
|---|---|---|---|
| G1 | Seven outside rule sets merged into one script and run over the whole book | longafter-ai-audit.py, AI-AUDIT.md, AI-AUDIT-V2-SUMMARY.md | 29ead003 |
| G2 | Fixes: contractions 154 → 118, page-describing lines 26 → 13, three same openings in a row 44 → 29, 8 long sentences split, 3 sayings rewritten | | 29ead003 |
| G3 | Contraction pass v1 broke grammar ("where you're"), so it was reverted and rerun with a guard | | 29ead003 |

## Stage H. Accountability sections
| # | Step | Output | Commit |
|---|---|---|---|
| H1 | 17 "honest check" sections where the reader's view is most likely skewed. 18 were written; the drinking chapter's was cut as a duplicate. Explained in How to use this book. | TONE-AUDIT.md rules | 3d8e8f54 |

## Where we are now
- **107,020 words** across 97 pages, counting the appendix.
- The audit is passing, along with the SEO, on-page and schema checks. The pipeline is green.
- **Not deployed.**
- **Next:** the design phase, then the Decoder back-links, which needs approval. The AI-use disclosure is the owner's call.

## Word count over time
| Point | Words |
|---|---|
| Second edition first draft (B2) | 47,600 |
| v5 after polish (start of D) | 55,682 |
| First expansion pass (D3) | 87,431 |
| Second pass and audits (E6) | 96,674 |
| Completeness, glossary, appendix, accountability (now) | 107,020 |

## Count of passes, by kind
| Kind | How many times | Where |
|---|---|---|
| Full rebuild and pipeline | at least 6 | C1, C2, C3, E6, F3, G1 and H1 |
| AI-writing or slop passes | 5 | C2, C3 (twice: no-ai-slop and copy-edit), E3 and G1 |
| Steelman | 2 | A3 and E4 |
| Fact checking | 6 passes in FACTS.md | B4, C2, C3, E5 (passes 3 to 6) |
| Expansion of the same chapters | 4 | C2 (23 chapters), C3 (15 sections), D3 and D4, and then F1 |
| Duplicate or merge clean-up | 3 | E2, H1 and the second-pass heading renames |

---

# Part 2. Review: what to do better on the next book

## The five most costly mistakes

### 1. We built and polished before the content was settled
- **What happened.** Stage C did design critique, schema, keyword sections, tap-to-call and the pipeline on a 55,000-word book. The book then grew by 51,000 words.
- **The cost.** Every later stage meant a rebuild and full re-verification. Design critique notes made on short pages now need repeating on long ones: in-page contents, short-answer prominence and long-page readability were all found later.
- **Fix.** Freeze the content before any build or design work. Use one rough build only to check that the generator works.

### 2. "Double the words" and "cover it completely" got blurred
- **What happened.** The word target drove two expansion passes. Pass 1 often restated existing text, which led to 13 chapters of merges (E2). The completeness audit (F1) was what actually measured the owner's goal, and it came last.
- **Fix.** Make the outline a list of the questions each chapter must answer. A chapter is done when every question is answered in enough depth, with the thin-answer check passing. Report word count, but never use it as a goal.

### 3. Checks ran at the end instead of at every insert
- **What happened.** Repeated headings, duplicates, thin answers, missing sources, AI patterns and contractions were all found in batch audits after writing. Each one meant going back into finished chapters.
- **Fix.** One gate script run on every insert, which fails the insert if any check fails:
  - content audit
  - AI audit v2 thresholds
  - duplicate check
  - thin answers
  - unique headings across the book
  - every new claim has a source line
  The atomic insert tool already exists, so add these checks to it.

### 4. The same audit was rebuilt five times
- **What happened.** Each AI-writing pass (C2, C3 no-ai-slop, C3 copy-edit, E3, G1) used a different rule set. Each round found things the last one missed, so the book was swept repeatedly.
- **Fix.** Start with the v2 audit (`longafter-ai-audit.py`, seven rule sets), generalised to any book, and run it as a gate from the first chapter.

### 5. Reader needs arrived late as separate rounds
- **What happened.** Each of these came as its own owner request, and each meant a sweep through finished chapters:
  - worked examples (D4)
  - closing actions (D4)
  - the gaps found in steelman round 2 (E4)
  - the tone audit (F3)
  - the glossary and appendix (F3)
  - the accountability sections (H1)
- **Fix.** Put them in the chapter template from day one:
  - short answer
  - the questions
  - a worked example, labelled as made up
  - an honest check where the reader's view is likely bent
  - a closing action
  - sources
  - glossary terms flagged as they are written

  Run steelman round 1 with the full list of hostile readers on the outline: lawyer (by country), criminal justice advocate, clinician, teenager, a reader whose ex has died, a reader of faith, a self-employed reader, the 2am phone reader, and the abuser reading over the reader's shoulder. Round 2 should then find almost nothing.

## Smaller lessons
| Problem | What to do next time |
|---|---|
| Regex rewrites of prose (removing "often", contraction pass v1) needed reverts | Never apply blanket rewrites to prose. Generate a list of proposed edits, review them, then apply. Every rewrite gets a grammar guard. |
| `git checkout` failed because an untracked file matched the glob | Restore tracked files only: `git checkout -- $(git ls-files '<glob>')`. |
| Insert anchors were mistaken for headings | Keep the atomic insert, and add a dry run that prints where each block will land. |
| Helpers lived in the scratchpad (merge, rehead, thin, contract, run_detect, slop, heads) and would be lost | Move them into `scripts/book/` with a `--book` flag. |
| Every script is hard-wired to longafter (audit, voice, dupes, AI audit, sources, progress, pipeline, onpage, build) | Generalise once into `scripts/book/*.py --book <slug>` with a per-book config (paths, voice spec, crisis pages). This is the biggest time saving for book two. |
| A Decoder back-link gap was found halfway through | Map every cross-book link at intake: Decoder BOOKS, Feminine links, hub topics and llms.txt, the seal menu. Then batch all the rebuilds of other sites into one approved deploy. |
| A markup change broke `build_site.py` seal_menu | The pipeline already runs hub files. Add a check that topics.html has no "None" entries. |
| A background agent hit the usage limit mid-review | For long text, use scripts in the main session. Use agents only for short, self-contained reviews, one at a time (CLAUDE.md). |
| Ubersuggest allows 3 reports a day, and the Windsor trial covers only 30 days | Run keyword research on day one, during outlining, so quota limits don't hold up writing. |
| The owner couldn't see the progress early on ("I didn't see you expand...") | Start the tracker and running checklist on day one, and report from it at every update. |
| The AI detector score kept tempting us to treat it as a target | Record it as information only. Plain, warm writing scores "AI" on light models. |
| Owner decisions surfaced late (AI disclosure, accountability, examples, target length) | Ask an intake questionnaire before outlining. |

## The order to use for the next book
1. **Intake** (one session). Collect:
   - the current book's state
   - live URLs and redirects
   - the cross-book link map
   - owner decisions: depth goal, disclosure, which template sections are in, and the deploy scope
   - keyword research, done now while the quotas are fresh

   Start the tracker.
2. **Spec.** Write the voice spec, the chapter template (Mistake 5) and the gate settings. Generalise the scripts if this book is the first since The Long After.
3. **Outline.**
   - parts and chapters
   - the questions each chapter must answer (this is the definition of done)
   - keywords mapped to those questions

   Run steelman round 1 with the full list of hostile readers, then get owner sign-off.
4. **Write, part by part.** Every insert goes through the gate (Mistake 3). Add sources and Crossref DOIs as claims are written. Commit and log each part in the tracker.
5. **Whole-book reading passes.** Read one or two chapters end to end, then do the tone audit and steelman round 2. These should be light by now.
6. **Generated extras.** Sources appendix, glossary, link check.
7. **Content freeze.** The owner confirms the writing is finished.
8. **Build, SEO, design, browser checks**, in a single pass. Design uses the template elements: the honest-check box, in-page contents and the short answer.
9. **Batch the work on other sites** (Decoder back-links, hub files), then deploy on the owner's words.

## What this would have saved on The Long After (rough estimate)
- **Rebuilds and full pipelines:** from 6 or more down to about 2.
- **AI-writing passes:** from 5 down to 1 gate plus 1 final report.
- **Expansion sweeps of finished chapters:** from 6 (C2, C3, D3, D4, F1 and H1) down to 1 writing pass.
- **Merge clean-up:** most of E2 avoided.
- **Overall:** roughly a third to a half of the passes over finished text would not have been needed, and the owner would not have had to correct direction twice (Stages D and F).

## What worked and should be kept
- **One part per commit, with the audit passing.** Every step can be traced and reverted.
- **The atomic insert tool.** It saved us from the anchor mistakes.
- **The one-command pipeline** that stops at the first failure.
- **The tracker and CHECKLIST.md**, once they existed.
- **Crossref matching with a DOI cache**, and the sources appendix generated from each chapter's sources.
- **Reverting rather than patching** whenever a mass edit went wrong.
- **Safety rules written into the template:** crisis links, no prescribing, blame-free honest checks.
