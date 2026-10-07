# The Sacred Divide — release status, 7 Oct 2026

Live now: **v4** (deployed 29 Sep 2026): 34 PDFs at `noblefathercreations.com/faith/pdf/<id>.pdf`, A4, 2,742 pages in total.
In progress: **v5**, branch `claude/sacred-divide-v5-redesign`: 34 PDFs rebuilt today (7 Oct, 04:31 UTC) into `library/_undeployed/sacred-divide-v5/`, US Letter, 4,353 pages in total. Nothing has been deployed. `sites.json` still says v4.

## 1. State of the rebuild and the information check (today)

- **PDFs:** all 34 rebuilt from the current Markdown (regenerated with 0 FAILED edits across md and narration). All 34 pass PDF/UA-1 (veraPDF); type sizes and palette inside the design scale in all 34 (`PDF-BUILD-REPORT.md`).
- **Scan of all 34 finished PDFs for leftovers:** no placeholders, no build notes, no unresolved citation markers, no ligature glyphs, no old Faith to Faithless number (020 3675 0959), no old Muslim Women's Network number (0303 330 0288), no `[GOVERNMENT REPORT]` tags. The verified Faith to Faithless freephone (0800 448 0748) appears in 30 volumes. Empty table cells print as a dash, on purpose.
- **Parsi Supreme Court verdict (re-checked today):** still reserved. Searches on 7 Oct found no pronouncement; the court has said it will await the nine-judge outcome. The pages state "reserved on 14 May 2026, no verdict reported at the last check". **Check once more on the day of release** and update the Zoroastrianism volume (§5, §8, §19 and source 16) if the verdict has come down.
- **Not repeated today:** a visual review of every page. Only the unification-church and hare-krishna contact sheets have been read by eye; the other 32 volumes were checked by measurement (page fill, type sizes, PDF/UA) only.

## 2. What is left before reposting

**A. Owner decisions (these hold up a clean release)**
1. House style: one spelling (American or British; the PDF is tagged en-GB but text is mostly American) and voice rules (defences/counters as questions or imperatives, aphoristic captions).
2. Grading frame: keep the six grades as they are (already decided: strict rule, no upward regrades). Still open: whether to add a lower label for techniques with no documented case, and whether weak loop cards belong among the seven (Soka Gakkai, Taoism).
3. Convert §12 in the seven table-format volumes (Ahmadiyya, Anglicanism, Dawoodi Bohra, Oriental Orthodoxy, Plymouth Brethren, Soka Gakkai, Unification Church) to the card format used by the other 27. Needs new per-technique text.
4. Shared template wording (flagged in every volume): the "documented cases… court, regulator or inquiry record" caption, the "attributed to God" line in stage 8 and technique 30 for non-theistic traditions, the precedent caption, and the "mistakes are logged" caption.
5. Deploy: go-ahead for a Netlify redeploy (no connected repo, so a git push cannot publish); version bump to v5 and the matching on-page "What changed on this page" entry, done together in one commit.

**B. Open sourcing items (named in the fix logs; 121 deferred entries across 33 volumes)**
- Buddhism: the Sri Lanka Mahanayaka election and the "US centres exempt" claims have no source.
- Unification Church: technique 1 is graded Documented on a single scholarly source.
- Taoism: cases 2 and 3 rest on one outlet (Bitter Winter); the 2023 venue measures and 2026 closures could not be sourced independently; the disclosure scorecard is all "no".
- New Age: the "Retreat and ceremony tourism" card is thinly sourced after correction; Indigenous §15 "Documented? Yes" now carries a note but needs a real source.
- Shinto: `[GOVERNMENT REPORT]` receipts were relabelled, not independently sourced; the Shinto Directive and State Shinto sources are Wikipedia/secondary summaries.
- Soka Gakkai: McLaughlin source page numbers cannot be verified; §19 (cases) is thin.
- Catholicism: Chiclayo complaint omitted (new content), "stronger than the laws of the Republic" apology unverified.
- Wider: many volumes lean on secondary or Wikipedia sources in §26; SNAP's toll-free line (1-877-762-7432) is unverified; Zoroastrianism electorate figure (25,000+) could not be re-read.

**C. New research or content, not yet started** (see `gaps-unfilled.md`, `expansion-proposals.md`): first-person "voices from inside" for Taoism, Soka Gakkai and others; thin §19 for several volumes; one-line lists in §8/§20.

**D. Design pass (v5 layout)**: about 26% of pages still carry more than 15% empty space (1,146 of 4,353 pages) after the compact section-opener change; remaining slack is mostly section ends before full-page dividers, loop diagrams and keep-together boxes. Needs a decision on how aggressive to be (letting boxes split, shorter dividers).

**E. Housekeeping**: HyperFrames skills not installed (needs a Bash permission rule from the owner); an uncommitted Canva design still holds an old deck (can be cancelled); zips in `exports/` (3 PDF zips + text/fix-logs zip) were built on 5 Oct and must be rebuilt from today's PDFs.

## 3. What changed: live v4 → v5 (working copy)

**Format and design**
- Page size A4 → US Letter. Pages 2,742 → 4,353 (average 81 → 128 per volume); words 586,584 → 1,035,550 in the PDFs (larger type, per-section notes and captions, scorecards, loops drawn out).
- New shared design system: one palette, seven-step type scale, dark "Why this matters" boxes, pull quotes, loop diagrams, evidence-grade chips and legend, cover with colophon.
- Tagged for accessibility (PDF/UA-1, all 34 pass), with figure descriptions, real table headers and bookmarks.
- Opening matter reorganised ("Before you begin", Contents, "How to read this", then the grades, receipts, method and citations explained).
- Section openers compacted (no more forced full-page openers).

**Content (all reversible edits in `content/sacred-divide/edits/`: 7,559 wording and fact edits across 34 volumes)**
- 34 per-volume discrepancy passes (P1 critical, P2 structural, P3 refinement), each with a fix log and a numbered edit trail. Headline fixes: Catholicism thesis question (Cardinal Law, 2002), bankruptcy and inquiry counts made consistent, Philippines annulment row; Parsi verdict wording; Shinto Supreme Court date; Orthodox counts and officeholders (Georgia, Kirill sanction); grade changes where the entry did not support the grade (e.g. Protestant/Evangelical tally now Taught 18 / Cultural 10 / Documented 2).
- Help-line corrections everywhere: Faith to Faithless (freephone 0800 448 0748 with verified opening hours), Muslim Women's Network (0800 999 5786), Recovering from Religion region (US, Canada and online).
- Grades re-weighed against the strict rule; the shared guide now explains that a mostly-Cultural volume means "no named document makes the institution responsible", not "cleared". Rationale notes now follow each grade chip.
- Open-source check on 6 Oct: Taoism certification card, Buddhism merit card, New Age retreat card and Indigenous ledger corrected; Shinto sources 25 and 26 added.
- Scorecard cells now keep their notes; empty cells show a dash; the §19 "tactics" label bug (technique names overwritten by loop names) fixed.
- Each volume's "What changed on this page" (§27) lists the corrections for readers.

**Not changed**
- The 27 sections and their order, the 34 traditions in 10 families, the "never rank" rule, and the one-PDF-per-tradition URL pattern (`/faith/pdf/<id>.pdf`).

## 4. Per-volume numbers

| Volume | v4 pages | v5 pages | v4 words | v5 words | Edits (v5) |
|---|---|---|---|---|---|
| ahmadiyya | 57 | 95 | 12,585 | 21,865 | 192 |
| anglicanism | 55 | 97 | 11,830 | 21,970 | 227 |
| bahai | 84 | 132 | 17,310 | 30,423 | 262 |
| buddhism | 87 | 133 | 18,198 | 30,824 | 200 |
| catholicism | 96 | 152 | 20,845 | 35,490 | 124 |
| christianity | 88 | 145 | 20,030 | 34,656 | 237 |
| confucianism | 83 | 131 | 17,250 | 30,293 | 213 |
| dawoodi-bohra | 50 | 86 | 10,983 | 19,918 | 209 |
| eastern-orthodoxy | 87 | 136 | 19,282 | 33,049 | 194 |
| hare-krishna | 85 | 130 | 17,838 | 31,417 | 247 |
| hinduism | 89 | 140 | 18,931 | 32,039 | 213 |
| indigenous | 90 | 138 | 18,950 | 35,418 | 238 |
| islam | 95 | 147 | 20,419 | 34,291 | 249 |
| jainism | 83 | 128 | 16,572 | 28,088 | 185 |
| jehovahs-witnesses | 92 | 140 | 19,237 | 33,800 | 225 |
| judaism | 86 | 135 | 18,495 | 31,214 | 230 |
| mormonism | 92 | 145 | 20,261 | 34,866 | 254 |
| new-age | 85 | 136 | 18,153 | 34,919 | 262 |
| oriental-orthodoxy | 57 | 98 | 11,840 | 22,712 | 215 |
| orthodox-hasidic-judaism | 90 | 134 | 18,963 | 33,158 | 233 |
| pentecostal-charismatic | 91 | 144 | 20,877 | 36,727 | 196 |
| plymouth-brethren | 46 | 87 | 10,455 | 22,454 | 208 |
| protestant-evangelical | 92 | 144 | 20,059 | 37,202 | 201 |
| scientology | 84 | 140 | 18,024 | 32,796 | 347 |
| seventh-day-adventism | 89 | 139 | 19,495 | 34,123 | 167 |
| shia-islam | 93 | 141 | 19,857 | 33,448 | 240 |
| shinto | 83 | 129 | 17,020 | 29,149 | 209 |
| sikhism | 82 | 131 | 17,696 | 29,833 | 210 |
| soka-gakkai | 45 | 83 | 9,611 | 17,990 | 210 |
| sunni-islam | 96 | 148 | 21,344 | 35,739 | 246 |
| taoism | 84 | 129 | 17,377 | 29,710 | 214 |
| tibetan-buddhism | 89 | 135 | 18,364 | 32,110 | 209 |
| unification-church | 53 | 93 | 11,220 | 23,211 | 274 |
| zoroastrianism | 84 | 132 | 17,213 | 30,648 | 199 |
