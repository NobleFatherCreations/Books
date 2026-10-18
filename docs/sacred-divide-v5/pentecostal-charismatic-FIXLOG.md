# Pentecostal & Charismatic — discrepancy fix log, 2026-10-03

Every change below is a reversible entry (PC-D001 to PC-D055) in `content/sacred-divide/edits/pentecostal-charismatic.json`; set an entry's status to `rejected` to undo it. Sources [31]–[37] were added to §26 (source 7 was re-linked, not renumbered). All 55 entries show `applied` in `logs/edits-status.json`; narration edits apply under `build_sections`.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "closed four years later" | "three years later" in §1, §3 and the narration example | D001, D002 |
| 2 (P1) | Crenshaw case reported as settled | Case rewritten: April 2024 in-principle settlement fell through over an NDA; claim against the staff member settled July 2024; claim against Hillsong continued, trial listed Feb 2025; final outcome marked "not recorded on this page". §21 and source 22 updated. FIXED WITH NEW SOURCES [32][33] | D003–D005 |
| 3 (P1) | KICC inquiries merged | Option (b): the card, §8 row and source 9 now describe the 2011–2016 inquiry the PDF covers (mismanagement over a £5m investment; interim manager 31 Jan 2014 to 14 May 2015, working alongside trustees who kept running religious activities). Narration "to run" corrected. The 2005 inquiry is no longer claimed; a primary 2005 report was not located | D006–D009 |
| 4 (P1) | Source 18 | Oyedepo (*Leadership*, 2026) and Macedo (Portal de Prefeitura, July 2026) URLs added from the fact check | D010 |
| 5 (P1) | "never an internal body" | §7 limited to independent ministries; §5 card says no church body had acted on the partnerships (Bakker was defrocked in 1987 over sexual misconduct); §23 "has ever acted on the instrument itself" | D011–D013 |
| 6 (P1) | Scorecard | Accounts P, Removal P. Safeguarding and External first stay N: nothing on the page establishes a published safeguarding policy with an external route | D014 |
| 7 (P1) | Grades / *(sourced)* | 8 Taught→Cultural; 13 Codified→Documented; 15 Taught→Cultural; 18 Codified→Documented; 25 Taught→Cultural; 26 Codified→Taught; 30 Codified→Cultural. *(sourced)* kept only on 13, 18, 26 (each names a document: the CRL report [7], the Senate review [4][31]) and removed from 3, 5, 7, 9, 10, 12, 22, 27, 30. Technique 13's counter no longer says a commission documented door-closing | D015–D031 |
| 8 (P2) | Loops | Already rebuilt (PC-L002 to L008); rechecked against §13, no further change | — |
| 9 (P2) | Size | Pew's 584 million, about a quarter of Christians, not a Protestant subset; "second-largest" removed in §1, §7; §4 and §3 aligned. Matches the Protestant / Evangelical log | D032–D035 |
| 10 (P2) | "could not compel" | "did not use its power to compel; staff said it lacked time and resources" [31]; t-18 counter says four of six ministries | D036, D037 |
| 11 (P2) | Succession watch | "seventies and eighties"; Korean founder dropped from the Now cell and the Yoido 2008 handover recorded [35], noted as not counted as a test (relation and member role not in sources) | D038 |
| 12 (P2) | Source 19 uncited | [19] added to the Children bullet and §11 cites | D039, D040 |
| 13 (P2) | Case tags | Case 5 `30`; case 3 `30, 18, 12` left as is — see below | D003 |
| 14 (P2) | Banks and airlines | Removed from §9 and §16 | D041, D042 |
| 15 (P2) | Hillsong row source | [10] and the Dec 2022 board report [34] cited | D043, D044 |
| 16 (P2) | Source 7 | Now the report itself (PMG-hosted PDF) | D045 |
| 17 (P2) | §14 wording | Checked; "this page treats those bodies separately" is accurate. No change | — |
| 18 (P3) | "criminal courts on three continents" | "courts and prosecutors on four continents" | D013 |
| 19 (P3) | ₩13.1bn | ₩13.15bn in §9, §19, §13 and source 5 (Korea Times confirms 13.15) | D046–D049 |
| 20 (P3) | RfR UK/Australia numbers | DEFERRED: shared help-line table | — |
| 21 (P3) | Faith to Faithless | No change needed (already correct) | — |
| 22 (P3) | British/American spelling | DEFERRED: house style across all volumes | — |
| 23 (P3) | AG and COGIC holders | Doug Clay (re-elected Aug 2025) [36]; J. Drew Sheard (re-elected 12 Nov 2024) [37] | D050, D051 |

Meta: `checked` and "Last checked" set to 2026-10-03 (D053, D054); §27 patch note added (D055). Sources appended: D052.

## Case 3 tag note
Item 13 offered "add the church's sabotage claim or drop 12". The claim could not be verified, so the case text was not extended, and DARVO (12) was left on the card. Please decide: drop 12 or research the church's response.

## New sources
31 Christianity Today (Jan 2011); 32 Roys Report (May 2024); 33 The Other Cheek (6 Jul 2024); 34 Hillsong Australia Board Report (Dec 2022); 35 Korea JoongAng Daily (Cho obituary); 36 AG News (Aug 2025); 37 COGIC (12 Nov 2024). Source 7 re-linked to the CRL report.

## New grade tally
Codified 0, Documented 2, Taught 10, Cultural 18 (30 techniques); three sourced to a named document. §1 Evidence row matches the §12 chips.

## Could not verify / left open
- Final outcome of the Crenshaw claim against Hillsong after the February 2025 trial listing: not found; marked not recorded.
- The 2005 KICC inquiry report (primary): not located; the card no longer claims it.
- CRL report: PMG summary page confirmed licensing and product-sale findings; the 120-page PDF itself exceeded the fetch limit and was not read in full.
- AG News (403) and Hillsong board report text: election result confirmed from search results; board report confirms the review, not the term-limit or 40% figures (those rest on the fact check, F14).
- Version number and front-matter `version: v4` not bumped (nothing deployed).
