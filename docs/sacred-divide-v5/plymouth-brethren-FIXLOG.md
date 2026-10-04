# Plymouth Brethren Christian Church — discrepancy fix log, 2026-10-03

Every change is a reversible entry (PB-D001 to PB-D049) in `content/sacred-divide/edits/plymouth-brethren.json`; set an entry's status to `rejected` to undo it. All 49 apply (none FAILED) in `logs/edits-status.json`; the narration edit (D016) applies in `build_sections('plymouth-brethren')`. Items are numbered as in `discrepancies/plymouth-brethren.md`. New sources [19]–[22] were added at the end of §26; sources [1], [4] and [5] were re-worded in place (no renumbering).

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Fabricated-looking "Not a Brethren business" quotation | FIXED. Both places now quote the church's recorded words (ABC, 15 Sep 2025, re-read): "The church does not run any businesses and does not employ anyone." Source [5] note records the statements | D001, D002 (+ source 5 edit) |
| 2 (P1) | ANAO request shown as open | FIXED WITH NEW SOURCE [21]. §8, §9, follow-the-money row, §14 "Last ran", loop 3 and case 5 now say the request was declined (Aug 2024, 2024–25 work program; Rationalist Society re-read) | D003–D008 |
| 3 (P1) | "roughly 8,000 left" | FIXED WITH NEW SOURCE [19]. Number removed in all places (§5 ×3, §6, technique 18, loop 6, §21, narration q6); replaced with "many left; in Scotland only about 200 of 3,000 members stayed with the leader" (Wikipedia, PBCC page re-read). The discourses.org.uk PDF was again unreachable (503) | D009–D016 |
| 4 (P1) | Source [1] membership | FIXED. Source note now says "over 50,000" is the church's own figure as relayed by Wikipedia and the biography page states none. The "about 55,000" figure was not confirmed (church site bot-checks), so it was not used | D017 |
| 5 (P2) | §12 is a table, not cards | DEFERRED: rebuilding 30 cards with definitions and grade notes is new content (proposal E4), not asked for | — |
| 6 (P2) | "Cultural (weak)"; no Evidence row | FIXED. Technique 1 graded Cultural; §1 Evidence row added with the new tally | D018, D048 |
| 7 (P2) | Grade-basis mismatches | FIXED. 17 Contested→Documented; 28 Documented→Taught; 13 Documented→Taught; 23 stays Cultural, but its [4] citation now supports only the friendship rule, technology and education attributed to former members | D018–D022 |
| 8 (P2) | 2025–26 election omitted | FIXED WITH NEW SOURCE [22]. Timeline row, say-do row and Q3 updated (committee named the church a "significant third party"; director denied the allegations at the 21 Aug 2026 hearing; church declined earlier hearings per AAP). §22 NZ tell and narration left unchanged (still accurate) | D023–D025 |
| 9 (P2) | AEC finding omitted | FIXED. AEC finding (spending disclosed by Willmac Enterprises, no outstanding obligation; AEC page re-read) added to §3, §8 and §20; "exposed" replaced. The NZ Chief Electoral Officer police referral was NOT added: the Wikipedia article read does not state it | D026–D028 |
| 10 (P2) | "We do not prevent…" cited to [4] | FIXED. Re-cited to [5] in technique 6, §14, §15 (×2 incl. ledger/denial rows) and §24; source [4] no longer claims the statement | D029–D035 |
| 11 (P2) | "Australia (largest)" | FIXED (UK listed first, no ranking claim) | D036 |
| 12 (P2) | Loops | FIXED. Loop 1 and 5 summaries and loop 7 step 5 rewritten to match what the steps record. Loop 5's thin base is stated in the summary, not padded | D037–D039 |
| 13 (P2) | Narration case-count line | DEFERRED: shared template; the brief says no patch for it | — |
| 14 (P3) | §1 Chosen by/removable by fragment | DEFERRED: deliberate (caption and scripts split on " / ") | — |
| 15 (P3) | Family row lower-case ids | DEFERRED: generated value shared across volumes | — |
| 16 (P3) | Uncited non-member staff | FIXED (56,000 per the church's own account, relayed by Wikipedia [1]) | D040 |
| 17 (P3) | "family courts" | FIXED (removed) | D041 |
| 18 (P3) | "Mr Hales" inside quotation marks | FIXED (technique 30 and the §15 denial table) | D042, D043 |
| 19 (P3) | "8,000 left" in technique 18 | FIXED with item 3 | D013 |
| 20 (P3) | Source 9 syndicated copy | FIXED WITH NEW SOURCE [20]. Crikey original not reachable; Baucher Consulting confirms the raid on 19 March; cited alongside [9] in §8 and §9 | D044, D045, D046 |
| 21 (P3) | §27 entry naming sections | DEFERRED: shared pattern across volumes | — |
| 22 (P3) | American spelling | NO CHANGE (already decided; "authorised" only in quotations) | — |

Meta: `checked:` and "Last checked" set to 2026-10-03; dated bullet at the top of §27 (D047–D049).

## New sources (end of §26)
19 Wikipedia, PBCC / Exclusive Brethren (1970 division) · 20 Baucher Consulting (ATO raid, 19 March) · 21 ANAO correspondence and Rationalist Society (audit declined) · 22 AAP/Canberra Times and The Mandarin (2026 committee).

## New grade tally
Cultural 13, Documented 10, Taught 7 (total 30; counted from the §12 grade column; the table has no `Evidence grade` lines, so no techniques are "sourced to a named document" markers and the §1 row omits that count). Before: Cultural 12, Cultural (weak) 1, Documented 11, Taught 5, Contested 1. The §1 Evidence row matches; nothing else repeats the tally.

## For the owner
- Not verified: the ANAO PDF's date (14 Aug 2024) rests on the earlier fact-check and the Rationalist article, whose fetched summary gave the reasons but not the date; the "more than 200 assemblies" seceding claim was not used; the exact JSCEM interim-report wording rests on The Mandarin's reporting, and the committee report itself was not read.
- Technique 23's grade could arguably be Taught if [4] is read to state all three as rules.
- Case `tactics:` lines (proposal E6), the §12 card rebuild (E4) and Australian school funding figure (E7) were not done.
