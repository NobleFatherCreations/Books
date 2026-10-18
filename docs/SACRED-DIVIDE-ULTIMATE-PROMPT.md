# The Sacred Divide — master prompt

Paste everything below the line into a fresh Claude Code session opened on
the `NobleFatherCreations/Books` repo. It is written to be run in phases,
with a stop for approval after each one.

---

You are the editor-in-chief, fact-checker, information architect and lead
front-end engineer for **The Sacred Divide** (live at
`noblefathercreations.com/faith`, Netlify site `thenobledivide`). It is a
single-file, offline-capable book that maps the *institutional machinery*
built around religious faith — offices, money, policy, exit costs — not the
faith itself. Its motto: *"honor the faith, name the machinery."* It
explicitly is not an argument against God, not a case that any faith is
false, and not a campaign to get anyone to leave.

Your job has four parts: an **information audit**, a **proofreading and
fact-checking audit**, a **navigation and information-layout redesign**
(built around family home pages), and an **expansion plan** (missing
religions and new sections). Work in the phases below. **Stop at the end of
each phase, report, and wait for my approval before continuing.**

## 0. Before anything else — read, don't assume

1. Read `CLAUDE.md` (binding rules), `MEMORY.md` (especially the 2026-09-27 entry), `BOOKS.md` (faith section), and `sites.json` → `faith` (including `pendingRelease`).
2. Read `docs/SACRED-DIVIDE-AUDIT-2026-09-27.md` and `docs/SACRED-DIVIDE-REDESIGN-ANALYSIS-2026-09-27.md`. They are your **starting brief, not settled truth**. Every factual lead marked *(verify)* must be confirmed or dropped.
3. Get the **live** file with `curl` (Playwright can't reach external HTTPS here). Compare it with `library/_undeployed/sacred-divide-v4-candidate.html` and establish which is live. Never assume `library/faith/index.html` is live: as of 2026-09-27 it is an old lineage.
4. Understand the data model before editing. The book's content is six embedded JSON blobs (`window.CODEX_DATA`, `CODEX_V2`, `CODEX_V3`, `CODEX_V6`, `CODEX_V7`, `CODEX_V8`) that round-trip byte-exactly through `json.loads` / `json.dumps(ensure_ascii=False)`. Religions live in `CODEX_DATA.religions` (33 fields each). The 18 acts are defined in the `ACTS` array. The 30 mechanisms are in `CODEX_DATA.tactics[*].entries[<1-based religion index>]`. Grades are in `CODEX_DATA.graded["<id>:<n>"]`, documented cases in `CODEX_DATA.cases`. Per-religion extras are keyed by id in V2 (apex, unanswered), V3 (turning, compel, revise), V6 (language.per, regions.cards) and V7 (score, the volumes).
5. **Edit only through a script** (extend `scripts/sacred-divide-v4.py` or write its v5 successor). Parse the blobs, change the data, re-serialize, and make every replacement assert that it matched. Never hand-edit the 3MB HTML.

**Standing rules for this whole task:**

- **Name:** always "The Sacred Divide". Never "The Coercive Control Codex" or "Coercive Control Index".
- **Architecture:** single self-contained HTML; no CDN `<script>`/`<link>`; fonts and icons inline; works offline.
- **Owner decisions:** the Cloudflare visit counter **stays**. Every privacy statement must say exactly what is true: no accounts, no cookies, an anonymous visit count, and the place saver on the device only.
- **Section saver:** `#sd-place-js` (localStorage key `sd-place`, off-switch `sd-place-off`, toggle beside "Show the introduction again") **stays**. Extend it; don't remove it.
- **No engagement mechanics:** no streaks, badges, "% complete", notifications, or gamified progress. This book is about coercive design and must never use it.
- **Naming rule for people:** public record only, offices before persons, nobody named on an unadjudicated allegation, no private individuals named.
- **Evidence tags:** every claim keeps a receipt tag ([COURT RECORD], [GOVERNMENT REPORT], [OFFICIAL POLICY], [FINANCIAL RECORD], [REGULATORY FILING], [ACADEMIC SOURCE], [INVESTIGATIVE REPORT], [LEADERSHIP STATEMENT], [FORMER MEMBER TESTIMONY], [PATTERN OBSERVED]). Tags must match the actual source type.
- **Deploying** is a production write. Build and verify, then ask. When a deploy happens, bump `sites.json` version + changelog **and** add the matching on-page entry (`CODEX_DATA.changeMind.log`) in the same commit.
- **Subagents:** at most one at a time (see "Agent dispatch discipline" in CLAUDE.md).

## Phase 1 — Information audit (completeness and consistency)

Produce `docs/audit/INFO-AUDIT.md` containing:

1. **Coverage matrix:** religions × every field and cross-reference (33 record fields, 30 mechanism entries, 30 grades, apex, unanswered, turning, compel, revise, sector, phrasebook, regional card, cases, volume rows, scorecard). Mark each cell full / thin / missing / malformed. Flag any religion below the median on any row.
2. **Duplication map:** content repeated across umbrella and branch pages (for example the 2022 death in custody on Islam *and* Shia; zakat on Islam *and* Sunni). Propose which page owns each item.
3. **Consistency checks:**
   - every count in prose against the data (and a list of every hardcoded number to convert into a computed one)
   - every cross-reference id resolves
   - every act renders for every religion
   - no leftover drafting text: search for "your file", "the file", "Got it", "I'll", numbered instructions, stray " ." spacing
   - officeholder names are dated and flagged as fast-moving
4. **Balance check per religion:** ratio of harm claims to `healthy` / `victories` / sector-defense concessions. Flag pages that read as one-sided compared with the book's own stated standard.

## Phase 2 — Proofreading and fact-checking audit

Produce `docs/audit/FACT-CHECK.md` and a machine-readable `docs/audit/claims.json`.

1. **Extract every checkable claim:** dates, numbers, names, offices, laws, court cases, inquiries, quotations, and "all / never / no one" absolutes. Record religion, field, text and current tag for each.
2. **Verify each** against a primary or high-quality secondary source (judgment, statute, official report, regulator filing, peer-reviewed or university-press scholarship, sustained investigative reporting). Record: verdict (confirmed / corrected / softened / unverifiable → cut or mark *verify*), the source (title, publisher, date, URL), and the corrected text.
3. **Hunt overclaims first.** Absolutes like "publishes no accounts anywhere", "no scholar ever…" or "the norm, not the exception" are the fastest way to lose an insider reviewer. Rewrite each to what the record supports, keeping the sharp point.
4. **Proofread** for grammar, spelling, transliteration consistency (Qur'an / Qurʾan; marjaʿ; Shia / Shiʿa — pick one house style per term and apply it everywhere), British vs American spelling (pick one), punctuation, and repeated words.
5. **Insider-review flags:** list passages a devout member of each tradition would most likely dispute. For each, give the strongest good-faith objection and whether the text already answers it.
6. **Output Error Ledger entries** (`CODEX_V7.errors.corrections`) for every substantive correction: date found, date fixed, what it said, what it says now, who established it. First confirm how the renderer displays that list, and whether the case list and its counters recount automatically, before adding entries or cases.
7. **Priority:** the Islam, Sunni and Shia sections go first. They are about to be reviewed by a Muslim reader.

## Phase 3 — Navigation and information-layout redesign

The goal: a reader who chooses a religion finds any answer about it in ≤3
taps and always knows where they are. Related religions are grouped on
**family home pages** with a button to each member (for example, one Islam
page with buttons to Sunni, Shia, Ahmadiyya, Sufi Orders and Dawoodi Bohra).
The same pattern applies to every family that can be grouped.

1. **Generate at least five genuinely different layouts** (not variations of one). Include at minimum: question-first, family-tree, compare-first matrix, situation-first, single-page dossier, and at least one hybrid. The brief's own shortlist (A–F) is a floor, not a ceiling. Try to beat it.
2. **Define weighted criteria before scoring:**
   - findability of a religion-specific answer
   - orientation
   - family comparison
   - preserving the argument (pattern first, fairness, **never a harm league table**)
   - mobile ergonomics
   - single-file buildability from data
   - scaling to 35+ religions
   - calm / no engagement mechanics
   - accessibility (WCAG 2.2 AA, keyboard, screen reader, reduced motion)
3. **Score in three rounds:**
   - (a) the weighted matrix
   - (b) at least five reader walkthroughs, counting taps and places visited: a Sunni woman in the UK asking about religious-only marriage; an Ahmadi reader looking for their own community; a researcher comparing money across one family; an ex-Jehovah's Witness on a phone in a hurry; a parent worried about a child's religious school; plus any you add
   - (c) an adversarial critique of the leader, with a fix for each objection

   Show your work. Pick the winner only after round (c).
4. **Specify the winner** in `docs/redesign/NAV-SPEC.md`:
   - the family taxonomy (every current religion and every proposed addition assigned to one family, with "related family" links for religions that straddle two)
   - routes (keep `#/r/<id>/<act>` stable; add `#/f/<family>`)
   - page templates: family hub, religion page, act page
   - the "At a glance" card
   - question tiles mapped to acts
   - the 18 acts grouped into chapters
   - the same-topic switcher within a family
   - the auto-built "elsewhere in the book about this religion" panel
   - breadcrumbs and the sticky topic rail / mobile bottom sheet
   - a slimmer dock and sidebar
   - scoped search
   - **computed counts everywhere**
   - how the section saver labels and restores the new routes

   Include 375px and 1440px wireframes as ASCII or inline SVG.
5. **Build it only after I approve the spec.** Generate hubs, tiles, panels and switchers from the data, not hand-written HTML per religion. Keep existing content and routes working.

**Verify** at 375px (touch) and 1440px, in normal and reduced motion:

- no `pageerror`
- no horizontal overflow (`scrollWidth > innerWidth + 1`)
- nothing stuck at `opacity:0` after scroll
- every family hub, every religion page and every act renders
- every tile's target exists
- the saver restores family, religion and act routes
- keyboard-only navigation works

Read the screenshots you take before calling anything verified. Also fix the known bug where roster tables break words mid-word at desktop width.

## Phase 4 — Expansion plan (missing religions and new sections)

1. **Missing religions.** Using the fillability test in the analysis doc (§4), evaluate every candidate listed there, and look for any it missed. Search systematically by family and by region (Africa, Latin America, East and Southeast Asia, the Caucasus, diasporas).

   For each candidate, output:
   - estimated size, with a dated source
   - the family it belongs to
   - grade: Full / Partial / Thin, act by act, naming which of the 18 acts would be thin
   - the anchor documentary records (at least two court, inquiry or regulator sources for Full)
   - risks (sensitivity, contested record, post-atrocity community, colonial-stigma risk)
   - recommendation: add / add later / mention elsewhere / exclude, with a reason

   Draft a public "Why isn't X here?" note from the exclusions.
2. **For each approved addition, produce a complete record** with every field the existing 27 have:
   - all 33 fields
   - the 30 mechanism entries with defenses and counters
   - 30 graded cells
   - apex, unanswered, turning points, compel, revise, sector defense
   - phrasebook entries
   - a regional card where the record exists
   - at least two documented cases

   Hold it to the same evidence and naming rules, and flag every *(verify)*. Start with Ahmadiyya, then Anglicanism, Dawoodi Bohra and Sufi Orders. Recommend an insider reader for each before publication.
3. **New and strengthened sections inside every religion.** Evaluate the 14 in the analysis doc (§5), and add any you find:
   - At a glance
   - What healthy looks like here
   - Law & state here
   - Money in numbers
   - ≥3 documented cases
   - Voices from inside
   - Branches & variants
   - Regional variants for all
   - Who gets hurt most (volume rows pulled in)
   - Leaving safely here
   - Where to get help
   - Words used here
   - Sources for this page
   - What changed on this page

   For each: what it contains, why it matters, which data already exists vs. what needs research, a build priority, and one fully worked example on the Sunni Islam page.

## Deliverables and reporting

- `docs/audit/INFO-AUDIT.md`, `docs/audit/FACT-CHECK.md`, `docs/audit/claims.json`, `docs/redesign/NAV-SPEC.md`, `docs/redesign/EXPANSION.md`
- the build script and the rebuilt candidate HTML
- the verification output and screenshots
- updated `MEMORY.md`, `BOOKS.md` and `sites.json`

At the end of each phase, report in plain language:

1. what you found
2. what you changed (with counts)
3. what you could not verify
4. what needs my decision

Lead with the three things that matter most. Do not deploy anything
without my explicit go-ahead in that phase.
