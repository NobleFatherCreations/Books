# Sikhism — discrepancy fix log, 2026-10-03

Every change is a reversible entry (SIK-D001 to SIK-D053) in `content/sacred-divide/edits/sikhism.json`; set an entry's status to `rejected` to undo it. SIK-D006, D034 and D053 are narration edits. All 50 md entries show `applied` in `logs/edits-status.json` (none FAILED) and the narration edits apply through `foryou()` and `questions()`. One new source, [18], was added to §26.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "Removed two predecessors" / "Two Jathedars removed in 2025" | FIXED. One removal: Giani Raghbir Singh, 7 March 2025 [3]. §1, §7, §8, §19 title, §22 and the narration now say so. The Damdama Sahib removal of Harpreet Singh is not added (no source read this round) | D001–D005, D006 |
| 2 (P1) | Stale murder conviction in §7 and §10 | Already applied earlier (SIK-P001, P002); §19 case and §20 row now also show it as overturned | D013, D016 |
| 3 (P1) | Diaspora transparency contradictions | FIXED WITH NEW SOURCE. §4 now says diaspora gurdwaras are run by elected committees, many registered charities, and that the page does not record which publish accounts [18]; §2 scene no longer asserts the 2019 court case or that nobody has ever published accounts; §20 row and loop 1 rewritten; §22 UK tell qualified | D007–D012 |
| 4 (P2) | Budget "up 17%" | FIXED. About 15% in 2023–24 (988 to 1,138.14), about 11% in 2024–25, about 10% in 2025–26 | D017 |
| 5 (P2) | Journalist-murder conviction in §19 / §20 | FIXED WITH NEW SOURCE. Case dates 2017–2026; murder conviction shown as overturned on 7 March 2026; §20 row names Chhatrapati, shot in 2002, and says the appeal did not concern the rape conviction [6] | D013, D016 |
| 6 (P2) | §19 Case 3 title | FIXED (see item 1) | D004 |
| 7 (P2) | t27 Contested | FIXED. Regraded Cultural | D018 |
| 8 (P2) | t19 Reformed *(sourced)* | FIXED. Regraded Cultural; the Amrit safeguard is stated as sitting beside the pressure | D019 |
| 9 (P2) | t26 Documented *(sourced)* | FIXED. Regraded Cultural; golak revenues pointed to §9 as a separate matter | D020 |
| 10 (P2) | t28 Contested *(sourced)* | FIXED. Regraded Cultural; chhaikka kept as the single institutional exception, citing [4] | D021, D022, D023 (also removes (sourced) from t16, t22) |
| 11 (P2) | §2 scene court case, "nobody publishes accounts" | FIXED (see item 3) | D008 |
| 12 (P2) | Source 6 pointed to the Hinduism page | FIXED. Source 6 now describes the Newsgram report directly | D048 |
| 13 (P3) | "One of Punjab's largest deras" | FIXED. Dera Sacha Sauda, headquartered at Sirsa in Haryana with a large following in Punjab (§19; §10 and narration also) | D013, D015, D053 |
| 14 (P3) | Khalra convictions; Kala Afghana 2003 | Khalra FIXED (five upheld, one acquitted, 2007; source 13 text corrected). Kala Afghana 2003 is correct (hukamnama 10 July 2003): no change | D036, D037 |
| 15 (P3) | Multani "settled the law" | FIXED. States the school-ban holding | D035 |
| 16 (P3) | Roll "halved" | FIXED. "Fallen by almost half", about 46%, in §8 (twice), §21, §22 and narration | D030–D034 |
| 17 (P3) | UK charity accounts public | FIXED WITH NEW SOURCE. Filing threshold and England and Wales scope [18]; OSCR named for Scotland from general knowledge, not cited | D011, D012, D049 |
| 18 (P3) | §24 item 3 legal force | FIXED by qualifying: the page now says it cites no legal source on the legal effect | D038 |
| 19 (P3) | "Every abuse ... forbidden" / "strongest ... of any reader" | FIXED. "Most of" in §3 and §23, with account-keeping named as an exception; "strongest" replaced | D025–D027 |
| 20 (P3) | §5 card "founder" | Already applied earlier | — |
| 21 (P3) | Early childhood vs infancy | FIXED. "Early childhood" everywhere (§11 wording kept) | D042–D045 |
| 22 (P3) | "Every political party"; "convictions arrived only after evidence became unbearable" | FIXED. "Political parties"; second replaced by the sourced fact that the 2017 conviction concerned 2002 assaults [6] | D039, D040 |
| 23 (P3) | Case 1 tactics 12, 22, 28 | FIXED. Set to `—` | D014 |
| 24 (P3) | Loop 6 "returning" | FIXED. "Publicly withdrawing its support" | D041 |
| 25 (P3) | §9 "ashram" card | FIXED. Renamed "Dera economy"; the unsupported Disclosed and Hidden lines read "Not recorded on this page" | D046, D047 |
| 26 (P3) | §15 ledger "Rare" | DEFERRED. Ratings left as written per the discrepancy note; house style |  |
| 27 (P3) | Spelling and "seva/sewa" variants | DEFERRED. House style shared by the other volumes; decide once for all |  |
| 28 (P3) | Timeline 1539–1604, Amritsar undated | No change. Not an error; no source read for 1577 |  |
| Template | "attributed to God" (stage 8, technique 30) | FIXED. Now attributed to culture and family honor | D028, D029 |
| Help | Hours and Recovering from Religion numbers | No change. Shared lines, covered by the global corrections |  |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D050, D051); dated bullet added at the top of §27 (D052). The §1 Evidence row is D024.

## New source
18 GOV.UK, Charity Commission, "Charity reporting and accounting: the essentials" (CC15d).
Source 6 was rewritten (not renumbered); source 13's note corrected.

## New grade tally
Cultural 30, Documented 0, Contested 0, Reformed 0 (30). No technique is sourced to a named document. §1 Evidence row matches the §12 chips (counted with grep: 30 chips, 30 Cultural, no `(sourced)` marks left).

## Left on purpose / caveats
- Every technique is now Cultural. That follows the entries' own content (family and community pressure) but flattens the page; the owner may want a different grading frame.
- The Raghbir Singh removal, the Chhatrapati details and the 2017 conviction rest on Newsgram [6] and ThePrint [3]; the "now before the Supreme Court" line is from the earlier fact-check (ETV Bharat, Supreme Today) and is not cited on the page.
- "Receipt" tags `[COURT RECORD: diaspora gurdwara disputes]` in §7, §9 and §16 still name no case; no source was found this round.
- The Charity Commission page was reached through search results, not a direct fetch; the OSCR remark is not sourced.
- `build_sections('sikhism')` could not be run: the Python `markdown` module is missing (not installed, as instructed). Narration edits were checked through `sacred_divide_narration` instead.
- Front matter `version: v4` and sites.json were not touched (outside this task).
