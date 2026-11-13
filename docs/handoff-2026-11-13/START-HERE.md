# START HERE: everything a new chat needs (session of 2026-11-12 to 11-13)

Repo: `NobleFatherCreations/Books`. Branch: **`claude/optimistic-clarke-86s6bg`** (canonical; push only here). Read `CLAUDE.md`, then `MEMORY.md`, then this file.
Owner: Shae Stovell (Noble Father Creations). Refers to himself as "him". Lifetime project: end the manipulation cycle by showing it whole, for free.

## 0. How to work with this owner (lessons from this session; follow them)

1. **Do what was asked, not what is easy.** The owner asked for X, got Y three times this session. Before building, restate the ask in two lines and name the files you will read.
2. **Treat pasted material as the brief, not as content to copy.** And read every source named. If an attachment is named, open it.
3. **List the skills and MCP servers you will use, and how you will save tokens, before starting.** Then actually use them.
4. **Ask questions when unsure,** but do not stall: state your defaults and proceed where the owner is silent, and flag them.
5. **Every reported fault becomes a failing check.** (Design protocol v3, `.claude/skills/design-director/SKILL.md`.) The owner must never be the tester.
6. **Steelman your own output before delivering.** Say what was and wasn't done, and why.
7. **Nothing is deployed without the owner's go-ahead.** Deploys go through `scripts/film-gate.sh` / `verify.mjs` / `nav-check.mjs`.
8. Credits are limited: put the architecture and mapping on the strongest model, and execution (reading, writing out, rendering, checking) on Opus or Sonnet. Do not spawn agents unless asked.
9. Voice: first person, short sentences, plain words. Contested science is "my belief." Never say the map ends the cycle; it ends the method's ability to stay hidden.

## 1. What was asked, in order (full text: `OWNER-MESSAGES-VERBATIM.md`)

| # | Ask | Outcome |
|---|---|---|
| 1 | Merge the original intro (v1) with the fractal-camera build (v8) into a cinematic Fractal² intro and push it live; run the design system start to finish | Done through v14, live and verified |
| 2 | Fix iPhone faults one by one (captions, crash, names, speed, jumps) | Fixed; led to design protocol v3 and machine gates |
| 3 | Run the director on the Entertainment sector site "world class, easy to navigate, complex, animated" | v3 skin built and verified; **not deployed** |
| 4 | Check all repos and branches for newer notes; handoff on rebuilding the main site | Audit done; **handoff doc not written; no sync done** |
| 5 | Turn the owner's Fractal notes into a PDF for the school psychologist friend (Von "Foil" Saunders), minus YouTube/outreach; explain the work and what it can do | First build (21 pp) missed the brief |
| 6 | Expand it: read the whole Fractal (esp. `#/frequency`), the Fractal² lead-in, the Part 1 text, the 30 impulses, the three Education combos, the series slides, two new composites for Foil; weave into one story | Final woven build (53 pp master, 56 pp Foil) |
| 7 | Steelman everything | `STEELMAN.md` (in this package) |
| 8 | Fix it with the strongest model's mapping, then let Opus/Sonnet execute | `BLUEPRINT.md` (Parts A-I) |
| 9 | Zip and handoff so a new chat has everything; commit the thread to memory | This package |

**Next work (owner said: "so we can continue on the intro site").** See section 6.

## 2. Deliverables (all in the repo, and in this zip)

| File | What | Pages |
|---|---|---|
| `pdfs/Why-I-Wrote-This.pdf` | **Master**: six movements, five combinations, no personal notes | 53 |
| `pdfs/Why-I-Wrote-This-for-Foil.pdf` | Same body + letter to Foil + his three asks | 56 |
| `pdfs/The-Fractal-Book-1-Audit.pdf` | Independent audit of Book 1, reviewer's view | 15 |
| `pdfs/Fractal2-Value-and-Impact.pdf` | Earlier (Nov 10) assessment the owner wants woven in | 25 |
| `superseded/Why-I-Wrote-The-Fractal.pdf` | First 21-page version. Superseded; do not use | 21 |
| `BLUEPRINT.md` | Architect's spec for the final revision; **Part G is the execution prompt** | |
| `NEW-CONTENT-FOR-REVIEW.md` | New-content draft written before the build (lead-in to Fractal², 30 impulses, connections) | |
| `STEELMAN.md` | Full audit of the delivered PDF | |
| `OWNER-MESSAGES-VERBATIM.md` | Every owner message, including the pasted scripts and the three combos | |
| `source/` | Build code and inputs (see section 5) | |

In the repo these live under `library/fractal2/review/` (PDFs) and `design/fractal2/reports/why/` (code, blueprint). Slides used: `exports/counterfeit-slides/fractal/00{2,3,4,5}-*.png`.

## 3. The PDF, as built (structure of the 53-page master)

Hook ("If I told you someone was love-bombing you…" → "That's one machine") → index with reading paths and the machine map → six movements:
1. **How it started**: why these books exist (owner's "stake" paragraph was my invention; to be replaced by the verbatim Part VI account).
2. **What I noticed**: eight stages + garden and gate; thirty techniques as original/inversion/practice tables; thirty original impulses (cards); thirty sectors.
3. **How it expanded**: numbers; three levels and four transmission channels; the frequency and body states; **"From the map to the life"** (the lead-in to Fractal²: 30 techniques = alphabet, 300+ tactics = dictionary, 150+ combos per sector = sentences; ladder diagram; why the blueprint is published).
4. **What I see now**: why order matters; **five combinations in full** (owner's: Trauma Bond Engine, Normalization Engine, Public Shaming Ritual; mine, for Foil: **The Paper Child** and **The Calling Trap**) each with scene, chain diagram, why-this-order, institutional and civilizational echo, tests, chain breakers, question; school-machines diagram; 15 connections.
5. **What this could do**: clean systems, war map, children and schools, what this can become, **"The world that saw it"** (eight scenes).
6. **I need help**: four asks; then Reference (tools, worksheet, self-audit, three lenses, limits, series slides, persuasion levers disclosed).
Foil edition adds a letter at the front and "Three asks" at the back (introductions to reviewers; advice on non-pathologizing youth framing; route for Playground Protectors into schools).
Form fields: 16 typeable boxes, 24 checkboxes, 32 internal links. No bookmarks yet.

## 4. Facts and numbers (verified this session unless marked)

- **The Fractal (Book 1):** 34 chapters (26 sector chapters + 8 essays: Pattern, Origin, Spiritual Lens, Mirror, Body, Chain, Frequency, Largest Body), 245,383 words. 30 techniques per sector chapter, 3 levels each. Published sectors 26 of 30 (missing: Technology, Dating, Surveillance, Child Welfare) so 2,340 examples are published, not 2,700. Owner wants "30 sectors, 2,700 examples" used; say "26 published, 4 in production" once.
- **Fractal²:** first finished sector = Entertainment & Music: 335 tactics, 1,005 worked examples (tactic × 3 levels), 153 combinations (203 on the master list), 41 of the first 153 carry safety notes. Second sector (per the owner's shared artifact): Corporate & Consulting, 138 combinations, 335 tactics. 291 combos written so far. Ten combo families: Capture & Attachment; Exit Prevention & Entrapment; Conditioning & Behavioral Shaping; Reality Distortion & Perception Control; Accountability Evasion; Social Warfare; Institutional & Systemic; Digital & Technological; Identity & Psychological Destruction; Specialized Exploitation. Live pages: `library/fractal2/site/fractal2/entertainment/` (518 pages). Owner's script says "253 tactics" for the Education interlude; use "300+".
- **Pattern Decoder** (live at noblefathercreations.com/playbook; `sites.json` says v20 at `instruments/playbook/site`, while `CLAUDE.md` still says v14: stale, fix it): 310 entries, five parts each, 105 safety-sensitive. Built by `design/build-decoder-v10.py`.
- **Playground Protectors** (`library/children/`, live at noblefathercreations.com/children, v6; prose in `content/prose/playground.md`): 28 missions, 4 worlds; written for the owner's daughter.
- **Sacred Divide:** 34 traditions × 27 sections.
- **Defects in the published Fractal (not fixed; owner to decide):** (1) one-line definitions of **Spiritual Bypassing** and **Financial Control** swapped on all 26 sector pages; (2) counts (above); (3) zero outside sources in any chapter; (4) "This is by design" ×8 in The Pattern contradicts The Origin ("no intent required"); (5) The Mirror numbers techniques differently from sector chapters; (6) two orders (stage-based grouping in The Origin vs 1-30).
- **Unverified in the composites:** school-psychologist ratio ~1:500 (NASP guidance) and the referral-disparity claim. Cite or soften before print.

## 5. Rebuild commands

```bash
cd design/fractal2/reports/why
python3 final.py master && python3 final.py foil          # -> final-master.html, final-foil.html
node render.mjs final-master.html /tmp/m.pdf               # single pass keeps internal links
python3 fields.py /tmp/m.pdf ../../../../library/fractal2/review/Why-I-Wrote-This.pdf
# same for foil -> Why-I-Wrote-This-for-Foil.pdf
```
- `data.py`: tables (30 techniques, 30 sectors, stages), from The Fractal's own tables.
- `build.py master|foil`: first-draft sections; `final.py` reuses them by id and reorders, adds new sections.
- `base.css` (copied from `reports/value-and-impact.html` styles) + `extra.css`.
- Colour palette for diagrams validated with `dataviz`: `#B97F00,#2A6FC9,#D4502F,#0F8F84,#9A46C4`.
- Needs: Playwright Chromium (`/opt/pw-browsers/chromium`), `pypdf`, `pdfplumber`, `pdftoppm`.
- Audit PDF source: `design/fractal2/reports/fractal1-audit.body.html` (+ shared CSS from the value-and-impact report).

## 6. The intro site (where to continue)

- **Live:** https://fractal-entertainment.netlify.app/fractal2 (intro, v14) and `/fractal2/entertainment` (518 pages, **still the v2 sector site**). Netlify site `fractal-entertainment` (194814a7-0e80-4b68-b314-0c07911af55a), deploy `6af58fe7d43ad699fbcbf1c9`. The hub noblefathercreations.com (Netlify 58596923-a3a6-4f9e-9e9f-e934a1920aed) proxies clean paths to project sites via `hub/catalogue-redesign._redirects`. Homepage proxy only on the owner's "deploy the homepage".
- **Source:** `design/fractal2/redesign/v9/{template.html,build.py}`, script `content/fractal2/intro-v9.md`. Built: `library/fractal2/site/fractal2.html`; assets `library/fractal2/site/fractal2/_a/v8/` and `_a/v9/`.
- **Rebuild:** `python3 design/fractal2/redesign/v9/build.py /fractal2/_a/v8/ && cp design/fractal2/redesign/v9/index.html library/fractal2/site/fractal2.html && python3 design/fractal2/redesign/v9/build.py`
- **Deploy only via** `scripts/film-gate.sh <local url> '#begin' content/fractal2/intro-v9.md -- <deploy cmd>` (Netlify MCP deploy returns an `npx @netlify/mcp@latest …` command run from a staging dir of `library/fractal2/site` plus a composed `_redirects`). Gates: `scripts/film-check.mjs`, `nav-check.mjs`, `frame-walk.mjs`, `design-gates.mjs --click`.
- **Docs to read first:** `docs/FABLE-HANDOFF.md` sections 0a-0d; `.claude/skills/design-director/SKILL.md` (v3); `content/fractal2/design/{REGRESSIONS,OWNER-TASTE,DESIGN-CHOICES,SCORES,STORY-DECISION}.md`; `docs/DESIGN-SYSTEM-FIELD-REPORT.md`.
- **Entertainment v3 skin:** built and verified (verify.mjs 27/27, nav-check pass) under `library/fractal2/site/fractal2/entertainment*`; generator `design/fractal-sector/`. Committed as WIP. **Not deployed.** Not critic-scored.
- **Open owner items for the intro:** the owner's own sentences for the author's-lens captions; sound decision; the hub page the final "Enter the map" button should lead to (currently `/fractal2/entertainment`); real-iPhone confirmation the crash is gone; v14 not critic-scored (`design-exit.mjs` fails); update `sites.json` `fractal2-ent` for v3 and fix the stale `fractal-ent`.
- **How this PDF work feeds the intro:** the lead-in ("thirty was the alphabet… dictionary… sentences"), the four verbs (see / name / break / return), the owner's origin account (Part VI of `intro-final.md`, test-locked), the hook ("That's not three tactics. That's one machine."), and the sector cards can inform the intro's copy and the hub page. Do not change Part VI text.

## 7. Still not done from earlier in the session

- **Handoff document for rebuilding the main site** (noblefathercreations.com hub + all projects + proxy rules + deploy/verify procedure). Facts: hub site ID above; hub `_redirects`; project site IDs and versions are in `sites.json`; `HUB-RULES.txt`.
- **Cross-branch/repo sync.** Findings: Books branch `claude/optimistic-clarke-86s6bg` is the canonical superset; GitHub default branch (`claude/wookbook-castings-consolidate-4zyo0d`, sha 98dc754a) is stale; `sleepy-maxwell-yii2ts` is a strict ancestor (the branch the owner was told to point Fable at). Four branches hold small unique content: import `content/fractal2/work-packets/06-sector-rewrite-and-audit-brief.md` (peaceful-planck 4cde740c) and `design/copyedit/{BRIEF.md,BRIEF-FIX.md,mkfix.py}` + `docs/DECODER-CONTENT-FLAGS.md` (friendly-albattani d82a7d42/c36a9f6d; open decisions: Vivid vs Quiet default colour, clinical sign-off on medical symptom lists, no real-phone/screen-reader test). `find-skills` (kind-cerf): inspect, and require an explicit yes. Fast-forwarding other branches and pushing pointer notes to Wookbook/Castings/Fantasy needs the owner's explicit permission. Castings repo = Books `workshop/casting` (no action); Fantasy is an unrelated novel repo; Wookbook is a stale predecessor.
- **Stale items:** `sites.json` (fractal-ent, fractal2-ent), `CLAUDE.md` sentence "currently only `wook`", `docs/AI-QUICKSTART.md` pointers.

## 8. To finish the PDF: run `BLUEPRINT.md` Part G

Blueprint adds (summary): verbatim origin story; Value-and-Impact woven through (Part H); one tactic through every work; 30 sector impact cards in lifespan order; full War Map in the owner's words; restored combo theory; data tests (combos per family; turning-point check on 10; time-or-witness tags); four one-page summaries with full tables in Reference; frequency moved after the Fractal² step; limits and predecessors up front; identity line before the ask; persuasion page last and half length; bookmarks; fixed label. **Add to the blueprint before running:** a row for The Largest Body and The Origin's history, and `design-director` + `no-ai-slop` in the skills list. Defaults (owner may overrule): origin story verbatim; prayer not in the body (six lines quoted in the blueprint-publishing passage); laws list in Reference only; Paper Child and Calling Trap in both editions.

## 9. Skills and MCPs

Use: `pdf`, `dataviz`, `no-ai-slop`, `design-director` (visual work). Repo skills (`.claude/skills/`): impeccable, grill-me, ponytail family. Avoid: Canva/Adobe/Gamma (rebuilds layouts that exist), helper agents (cost). Ask before connecting Google Drive (the owner's combo book `ENT_combo_book.pdf`, 39 MB, is in the owner's Drive). Netlify MCP for deploys only on the owner's go-ahead; its schemas must be reloaded with ToolSearch when needed.
