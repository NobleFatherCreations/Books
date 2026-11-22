# The Long After, 2nd edition: production plan

Owner, 2026-11-22: write the full book now. It should have:
- audit checkpoints for the content
- brief links to the exact passages in The Sovereign Divine Feminine that cover the same ground
- no AI slop
- the search plan fully mapped
- the pattern web (links between chapters, the Pattern Decoder and Feminine) planned ahead
- the most efficient order, step by step

## Files
- `make_plan.py` → `plan.json`. This is the structure and the single source of truth for 13 sections, 83 chapters and 96 pages. Each entry holds the web address, title, target search phrase and its variants, required Decoder pages, required Feminine passages, and the heavy flag.
- `NN-*.md`: the chapter text. Each chapter starts with `=== slug`, then header lines, then `---`, then the body.
  - Header: `title`, `question` (the reader's own question, shown under the title), `seo` (browser title, 60 characters or fewer), `short` (the short answer, 2 to 4 sentences; it also serves as the search description).
  - Body: Markdown. `## ` headings are the reader's questions where natural. `> ` marks a pull line. `> **Say:**` marks words to use.
  - Links: `[text](ch:slug)` to other chapters, `/playbook/slug` to the Decoder, `/feminine/page#anchor` to Feminine.
  - `## Sources` comes last.
- `scripts/longafter-audit.py`: the automatic checkpoint. Every part must pass it before it is committed.

## Order of work (most efficient)
1. Structure, registry and audit (done first, so links and keywords are decided once).
2. Start + Part I, the pages most readers land on first.
3. Parts II to IV (safety, how it continues, contact).
4. Parts V and VI (courts, children).
5. Parts VII and VIII (feelings; body, health and help: the heaviest chapters, written with the most care).
6. Parts IX to XI and the toolbox (A to Z and the questions page last, because they gather every chapter).
7. Whole-book audit and fact check (each source verified), then the report to the owner.
8. Next phase (separate approval): the design build (direction A) and the search layer in the generator, then gates, then deploy on the owner's word.

## Audit checkpoints (each part)
**Automatic** (`longafter-audit.py`):
- structure and the target phrase in title, short answer and body
- every link valid, including Feminine anchors; required Decoder and Feminine links present; at least 3 links to other chapters
- at least one question heading
- sources present
- filler words, dashes, sentence length and reading ease
- no prescribed feelings or timelines
- heavy chapters link to a crisis route; no method wording

**By hand, every chapter:**
- the safety review for heavy chapters (help first, nothing that increases danger, no blame)
- a fact list: every claim carries a source in `## Sources`; disputed points are labelled as disputed
- legal notes are categories plus country examples plus "search this locally"
- no diagnosis of the reader or of any named person

**Book-wide at the end:**
- duplicated passages
- consistent terms
- every chapter reachable from at least two others
- every plan keyword used once as a main target only (no two chapters chasing one search)

## The pattern web (links decided before writing)
- **Chapter to chapter:** at least 3 links in the text, at the point the reader needs them, plus "Next, if this is you" (added by the generator from the plan).
- **Chapter to Decoder:** the Decoder pages listed in `plan.json` (105 links, all verified to exist). The Decoder defines a pattern; the chapter says what to do after leaving.
- **Chapter to Feminine:** a short, plain mention where Feminine covers the same ground from inside the relationship, linked to the exact section (17 passages, anchors verified).
- **Decoder back to chapters:** added in the build phase (each Decoder page gets "After you've left: …" links to the chapters that cite it).
- **Hubs:** "What post-separation abuse is" (the subject), A to Z (the words), Questions people ask (the questions), Where are you right now? (situations).

## Search plan
Target phrases, volumes and the page-role map are in `BOOK-MAP-v2.md` §6, §7 and §11. Each chapter has exactly one main target phrase (in `plan.json`). It appears in the browser title, the first sentence of the short answer and one question heading; elsewhere only where a person would say it.

## Pipeline (2026-11-22)
`bash scripts/longafter-pipeline.sh` runs, in order, stopping at the first failure:
content audit → build → beacon → hub files (llms.txt, topics) → findability + on-page + schema → seal menu → screenshots, axe, lab speed.
Topic expansion loop: search data (Ubersuggest suggestions, Search Console via Windsor) → gap list (terms absent from the book) → sections written into the matching chapter → FACTS.md → pipeline.
