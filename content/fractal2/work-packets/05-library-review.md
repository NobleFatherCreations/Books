# Work packet 05 — read the whole library, then extend the value assessment

**Why:** the assessment in `library/fractal2/review/Fractal2-Value-and-Impact.pdf` was written from The Pattern, the closing chapters, the owner's scripts and one Fractal² sector. The owner wants the same review to rest on everything that came before: every sector chapter of The Fractal, The Fracture, and The Sacred Divide (the owner called it "the great divide"; there is no book by that name, confirm with the owner).

**Where:** this repository and branch. Everything needed is already here. Do not start a new repository. Do start a **new conversation** so the work begins with a small context and reads its notes from files.

## Sizes (measured 2026-11-10 with `corpus_extract.py`)

| Book | Path | Chapters | Words | Notes |
|---|---|---|---|---|
| The Fractal | `library/fractal/` | 26 sector chapters + 8 essays | 249,000 | The contents page says "8 essays and 26 sectors". Technology, Dating, Surveillance and Child Welfare are on the thirty-sector list but have no published page |
| The Fracture | `library/fracture/` | 14 chapters | about 90,000 | `index.html` repeats the whole book (88,000 words): skip it. 195 cited sources, in 8 of the 14 chapters |
| The Sacred Divide | `library/faith/` | 35 pages | 630,000 | Every page has the same 27 sections and says "every claim numbered to a source" |

Reading all of it in full is about 1.2 million tokens. That cannot be held in one conversation, so it is read once, chapter by chapter, into short digests that are saved, and the conclusion is written from the digests.

## Steps

1. `python3 design/fractal2/reports/corpus_extract.py fractal fracture faith` writes plain text to `content/fractal2/library-review/text/` (git-ignored). Read the text files, never the HTML: the HTML is about four times larger.
2. **Digest pass.** One chapter per pass, by a mid-tier model at medium effort, one worker at a time (project rule), each writing `content/fractal2/library-review/digests/<book>--<chapter>.md` in the format below, 350 words at most. Commit every ten digests.
   - The Fractal: all 26 sector chapters in full (The Pattern and the closing chapters are already covered).
   - The Fracture: all 14 chapters in full. For each number that carries an argument, note whether a source is attached.
   - The Sacred Divide: six pages in full (the three largest traditions, one small one, `new-age`, `indigenous`), then for the other 29 only sections 01, the safeguards and the sources, because the structure repeats. Ask the owner first if every page should be read in full: that adds about 600,000 tokens.
3. **Synthesis.** The top-tier model at high effort reads all the digests (about 35,000 tokens), re-reads five chapters in full as a check on the digests, and then:
   - adds a part to the report: the library as a whole, how the books support one another, what data each rests on, what safeguards each carries, where they disagree with each other;
   - corrects anything in the existing report that the full reading changes;
   - re-renders the PDF (`node design/fractal2/reports/render_pdf.mjs ...`), looks at every page, commits and pushes.
4. Update `STATUS.md`, `HANDOFF.md` and `MEMORY.md`.

## Digest format

```
# <book> — <chapter>
Words: N · Sources cited: N
Claim in one sentence:
What it rests on (data, records, observation, the author's lens):
Three strongest examples (one line each, with their level: one life / institution / civilization):
Safeguards present (notice line, composite labels, "not advice", safety line, patterns-not-people):
Anything stated more strongly than its support (quote it):
What this chapter adds that no other does:
Two lines worth quoting:
Who is helped most by this chapter:
```

## Rules

Read only. Do not edit any book. Deploy nothing. No named person or organisation is to be described as a villain in any digest. Mark every statement in the report as Fact, Your lens, or My judgment, as the existing report does.
