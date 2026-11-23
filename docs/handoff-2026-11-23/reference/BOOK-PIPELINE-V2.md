# Book pipeline v2: how every revamped book is built from now on

Written 2026-11-23. It combines:
- `docs/LONGAFTER-PROCESS-MAP.md`, our own review of The Long After
- the owner's outside review, which covered audits, writing, impact, design and seven extra passes

**Use it for:** the rest of The Long After, then The Silence, At Will, The Repair and The Slow Take.

**Binding rules still apply.** CLAUDE.md, especially:
- no requests to other servers (except the Cloudflare beacon)
- nothing stored on the reader's device
- deploy only on the owner's words, naming each site

---

## 1. The outside review: what we take, change or refuse

### Taken as written
| Idea | Why |
|---|---|
| **Meso-level audit**: chapter-to-chapter arc, the handoff between chapters, concept dilution | Our audits covered sentences (micro) and the whole book (macro), never the middle. Six expansion sweeps grew The Long After to 107,000 words, so repeated half-explanations are likely. |
| **Template rhythm variety**: 3 or 4 chapter shapes, with the honest check placed where resistance peaks | Seventeen honest checks and about 80 worked examples in fixed slots become predictable. |
| **2am readability check**: paragraphs under about 60 words, no 350-word stretch without an anchor, reading grade per chapter | We measured AI tells, not overwhelm. Phones are 87% of traffic. |
| **Legal and jurisdiction audit** | The book covers contempt of court, criminal trials and religious divorce across several countries. Every legal line must say where it applies. |
| **One site manifest**: counts, titles and taglines in one file read by every build | We just had "310" stuck in about 2,100 places across every site. |
| **Dialogue decoders**: what they say, what it's doing, a neutral reply | This is the books' strength, and it ties straight into the Decoder. |
| **Closing actions as micro-decisions**: one physical step of 3 minutes or less | More useful than reflection prompts at 2am. |
| **Cross-book bridges** at the exact point situations overlap | For example: a job weaponised links to At Will, and shame turning inward links to The Repair. |
| **Print field sheets** (print CSS, no menus or chrome) | For court, therapy, and readers whose devices are watched. |
| **Triage toggle**: Full read or Just the steps | Directly serves the overwhelmed reader. It needs no storage. |
| **On-this-page menu, reading time and progress bar** on long chapters | Already in the steelman backlog. |
| **Distinct visual treatments** for the short answer, honest check, scripts and safety | The honest-check marker line was already flagged for design. |
| **Weaponization audit**: could the abuser use this page against the reader? | The highest-stakes check we never ran. |
| **Taxonomy lock**: book terms checked against the Decoder's names and aliases | The Decoder is now the shared vocabulary of the library. |
| **GEO definition blocks**: a 40 to 60 word answer straight under a question heading | We do this in short answers. Extend it to key terms inside chapters. |
| **Accessibility and text-to-speech pass** | Screen-reader names for the new controls, and citation markers read sensibly aloud. |
| **Voice fingerprint pass**: restore the sharp lines the expansions flattened | Needs a sample of the owner's raw writing. |

### Taken with changes
| Idea | Change, and why |
|---|---|
| Remove "this example is made up" from every chapter | Say it once in How to use this book, and keep a short visible tag such as *A composite story* on each example. Readers who land straight on one chapter from search never see How to use this book, and presenting invented stories as real would break trust. **The owner decides.** |
| Fonts from Google Fonts | Self-host every font (CLAUDE.md: no outside requests). Keep the books' own type choices rather than one font set for all, because each book has its own stance (BOOKS.md). |
| Remember the theme, checkbox state and triage choice in localStorage | **Refused** (CLAUDE.md: nothing personal stored on shared phones). Toggles reset on each page. The checklist works on paper through the print sheet. |
| Service worker caching the whole book offline | **Refused.** It stores the book on the device, which is a trace on a watched phone. The book already has an offline one-page edition at `/longafter/all`, and the print sheets. |
| Leave button opens a decoy tab | Keep `location.replace` (it already overwrites history). Opening a new tab leaves a second entry in history, so don't. |
| Neutral tab titles for privacy | The owner chose findable over private on 2026-10-27. Keep that, and keep the private-window advice in How to use this book. |
| Link audio from the Listening Room into heavy chapters | Only as a link, never inline or autoplay. Root practices first, because they are grounding exercises. Music tracks only if the owner wants them. |
| WCAG AAA everywhere | AA floor (CLAUDE.md). Aim for AAA on body text, but don't let AAA force a palette change on every block. |
| Copy buttons on scripts | Yes. The clipboard API stores nothing, so it's allowed. |
| Fail any insert with a paragraph over 75 words | Fail over 90 words, warn over 60. Tables, lists and legal quotes are exempt. |

### Refused
- **Generic Tailwind or Bootstrap look, and the review's fixed hex palette for all books.** Each book keeps its own design stance (CLAUDE.md: never apply one pattern to all books). The Long After keeps Dusk to first light.
- **Stock photos.** Never used, nothing to change.

---

## 2. The revised order for any book: 10 steps

1. **Intake (one session).**
   - Read the book, BOOKS.md and the live URLs.
   - Map every cross-book link: Decoder BOOKS, Feminine links, Topics, llms.txt, seal menu.
   - Collect the owner's decisions:
     - depth goal
     - AI disclosure
     - composite-story wording
     - which blocks are in
     - deploy scope, by site name
     - a raw writing sample for the voice pass
   - Run keyword research now, while the Ubersuggest and Windsor quotas are fresh.
   - Start the tracker.
2. **Spec.**
   - The voice spec.
   - The book's `book.json` (section 4).
   - Which chapter shapes it uses (section 3).
   - The gate thresholds.
   - Its entry in `site_manifest.json`.
3. **Outline.**
   - Each chapter gets: its questions (the definition of done), its shape, where the honest check sits (if any), its cross-book bridges and its Decoder links.
   - **Arc check:** the outline reads in an order that builds Stabilise, then Recognise, then Defend, then Rebuild. Each chapter's last line hands off to the next.
   - **Steelman round 1** with the full panel of hostile readers (listed in the process map), including the abuser reading over the reader's shoulder.
   - The owner signs off.
4. **Write, part by part, through the gate** (section 5). Every insert fails if it breaks a rule. Sources and DOIs go in as claims are written.
5. **Meso pass**, a reading pass the tools only support:
   - Read the last paragraph of chapter N and the first of N+1, all the way through.
   - Cut concepts explained twice to one full explanation plus links.
   - Vary the shapes where three chapters in a row match.
6. **Safety and trust passes:**
   - weaponization
   - legal jurisdiction
   - tone (seen, safe, in the right place)
   - steelman round 2
   - taxonomy lock against the Decoder
   - voice fingerprint against the owner's sample
7. **Generated extras:** sources appendix, glossary, print field sheets, link check.
8. **Content freeze.** The owner confirms the writing is finished.
9. **Build and design in one pass**, using the shared book shell (section 6):
   - Prototype two chapters first, check them at 375 and 1440 wide, then roll out.
   - Run the accessibility, text-to-speech, OpSec, speed and screenshot checks.
10. **Batch the other sites, then deploy on the owner's words.**
    - Before deploying, list every site that changed and why, and ask about each one.
    - A shared-menu change is its own separate decision.
    - After the deploy: verify live, IndexNow, `sites.json`.

---

## 3. The chapter template system (the "new book template")

Every chapter keeps two fixed things:
- the **short answer** (the first thing on the page)
- the **sources** (the last thing on the page)

Everything between them follows one of four shapes. Pick the shape that suits the reader's state in that chapter. No more than two chapters in a row share a shape.

| Shape | Opens with | Best for | Order of blocks |
|---|---|---|---|
| **Scenario-first** | A short composite scene (60 to 120 words) | Feelings, the trauma bond, going back | scene, short answer, questions, honest check (where resistance peaks), what helps, micro-decision |
| **Question-first** | The short answer, then the questions people search | Practical and legal chapters, findability | short answer, questions, dialogue decoder, composite example, micro-decision |
| **Myth and reality** | A belief the reader may hold | Labels ("is my ex a narcissist?"), court myths, "they'll change" | short answer, myths each followed by what's true, honest check, what to do, micro-decision |
| **Tool** | The tool itself (a checklist, script set or plan) | Documentation, safety plans, court prep | short answer, the tool (with a print sheet), how to use it, common mistakes, micro-decision |

### Blocks
Each block is written in Markdown as a fenced block, which the generator turns into a styled element. Writers never hand-write HTML.

````
::: short            the short answer (40-60 words, quotable alone)
::: scene            a composite story; the generator adds the "A composite story" tag
::: honest           an honest check; the generator adds the standard opening line
::: decoder          dialogue decoder:  > They say: ...  / What it's doing: ... / A neutral reply: ...
::: action           micro-decision: one physical step, 3 minutes or less ("Before you close this page")
::: safety           calm safety card with tap-to-call numbers for the reader's country list
::: sheet name       content that also goes into the printable field sheet named "name"
::: bridge book:slug a cross-book link with one sentence on why ("If your ex is going after your job ...")
::: steps            content kept when the triage toggle is set to "Just the steps"
````

**The triage rule.** "Just the steps" keeps these blocks and hides everything else:
- `short`, `steps`, `decoder`, `action`, `safety`
- lists and tables

The generator marks them, so no hand-tagging is needed.

### Rules every chapter meets (enforced by the gate)
- **Every legal or medical claim** says where it applies ("In England and Wales …") or links to the country page.
- **The closing micro-decision** is a concrete action, never a reflection prompt.
- **Composite stories** are tagged. Real people and real cases are never described.
- **Every honest check** follows the four safety rules in `content/longafter-v2/TONE-AUDIT.md`:
  - about the present
  - a blame-free opener
  - private questions with no verdicts
  - a gentle next step
- **At least one handoff line** to the next chapter or a bridge.

---

## 4. Tooling to build once, before the next book (`scripts/book/`)

Generalise the Long After scripts. Each takes `--book <slug>` and reads `content/<book>/book.json`:

```json
{
  "slug": "silence", "title": "The Silence", "parts": "plan.json",
  "voice": "BOOK-MAP-v2.md#2", "audience": "fathers cut off from their children",
  "crisis_pages": ["if-youre-not-safe-right-now"], "countries": ["UK", "US", "IE", "CA", "AU", "NZ"],
  "shapes_allowed": ["scenario", "question", "myth", "tool"], "honest_checks": true,
  "gate": {"para_warn": 60, "para_fail": 90, "anchor_every": 350, "grade_max": {"crisis": 8, "default": 9, "legal": 11}},
  "bridges": {"atwill": "work", "repair": "guilt", "longafter": "after leaving"},
  "design": {"theme": "own", "fonts": "own"}
}
```

| Script | From | Adds |
|---|---|---|
| `book/audit.py` | longafter-audit.py | Readability for 2am: paragraph length, anchor spacing, reading grade per chapter. Jurisdiction check on legal words. Handoff line present. |
| `book/ai_audit.py` | longafter-ai-audit.py | Unchanged rules. Run as a gate, not afterwards. |
| `book/meso.py` | new | The arc report: last and first paragraphs side by side, the shape sequence, and concepts defined in more than one chapter (repeated definitions of the same term). |
| `book/dupes.py`, `book/voice.py`, `book/sources.py`, `book/progress.py` | existing | `--book` |
| `book/insert.py` | longafter-insert.py | Runs the gate on every insert, all-or-nothing, with a dry run that shows where each block lands. |
| `book/taxonomy.py` | new | Every bolded term and glossary entry checked against Decoder names and aliases. Flags drift. |
| `book/build.py` | build_longafter_v2.py | The shared book shell (section 6). Renders the blocks. Builds print sheets. |
| `site_manifest.json` plus `scripts/manifest-check.py` | new | One file for titles, taglines and counts (the Decoder's count comes from its own build). nf-catalogue.py, build_site.py, build_home.py and every book's "related" line read it. The check fails if any page disagrees. |
| `book/pipeline.sh` | longafter-pipeline.sh | The same stages, plus manifest-check, decoder-relink and the meso report. **It never reverts the homepage.** |

Move the scratchpad helpers in here too: merge, rehead, thin and contract.

---

## 5. The gate: runs on every insert, and the insert is refused on any failure

- **Content audit:** voice, banned words, prescribing, crisis links, links resolve.
- **AI audit v2 thresholds.**
- **Duplicates:** within the chapter and across neighbouring chapters.
- **Unique headings** across the book.
- **Thin answers:** questions answered in under 45 words.
- **Readability for 2am:**
  - paragraphs: warn over 60 words, fail over 90
  - fail if more than 350 words go by without an anchor
  - reading grade within the chapter's band
- **Sources:** every new claim has one. Every legal or medical claim names where it applies.
- **Blocks valid:** short answer present, a micro-decision present, an allowed shape, tagged composites.

---

## 6. The shared book shell (built once; each book keeps its own look)

**Mechanics shared by every book:**
- **Triage toggle:** Full read or Just the steps. No storage.
- **On long chapters:** an on-this-page menu, reading time and a top-edge progress bar.
- **Distinct block styles:** the short-answer card, honest-check card (warm and recessed, never alarming), dialogue-decoder bubbles with a Copy button, the micro-decision card and a calm safety card.
- **Citations:** shown as small numbered markers that open inline (keyboard and screen reader friendly), with the full list still at the end.
- **Print CSS and field sheets:** A4 and US Letter, no chrome.
- **Section links:** each heading gets a readable anchor and a small share link.
- **Desktop rail at 1100px and wider:** chapter, part, jump links and Leave.
- **Phones:** a thumb-reachable dock.
- **Leave:** `location.replace`, plus Escape twice.
- **Part emblems:** theme-aware inline SVG in the book's own visual language, plus simple diagrams where a sequence or cycle helps (for example the DARVO sequence).

**Owned by each book:** palette, fonts, the cover moment, emblems and motion (BOOKS.md, docs/design-catalogue). Run the design through the `/design-director` skill and `13-html-books-playbook.md`.

**Checks:**
- axe (WCAG 2.2 AA) and keyboard
- reduced motion
- a 375 and 1440 screenshot review
- text-to-speech readout of two chapters
- an OpSec check: the beacon is the only outside request, nothing is stored, Leave overwrites history
- perf.js

---

## 7. Order for the four books after The Long After
Do them one at a time, each through steps 1 to 10:

1. **The Silence.** It is closest to The Long After (separation, children, courts), so it reuses the most tooling and bridges.
2. **At Will.** Work. Bridges from The Long After's job chapters.
3. **The Repair.** For people doing harm. The weaponization and tone passes matter most here.
4. **The Slow Take.** Later life. Pensions and inheritance link back from The Long After.

The owner may choose a different order. Ask at intake.
