# Ahmadiyya — discrepancy fix log, 2026-10-03

Every change is a reversible entry (AHM-D001 to AHM-D056; D053–D056 are the meta, patch note and sources) in `content/sacred-divide/edits/ahmadiyya.json`; set an entry's status to `rejected` to undo it. All apply (none FAILED); narration edits (D007, D021) apply under `build_sections('ahmadiyya')`. Sources [31]–[35] were added at the end of §26.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Pakistan "uncounted" | FIXED WITH NEW SOURCE. Now "undercounted: the 2023 census recorded 162,684 Ahmadis, and many boycott" [31] | D003 |
| 2 (P1) | Unlocated quotation | FIXED. Checked the guide PDF: the phrase is not in it. Replaced with its own words ("the basic and compulsory Chanda … obligatory upon every earning Ahmadi") in §9, Follow the money, source [1] note and narration; arrears rule added from the guide (proposal E4) | D004–D007; arrears D008 |
| 3 (P1) | Boycott cited to [12] | FIXED. [12] kept for the expulsion only; the boycott is attributed to former members in §12 (Discard, 7, 28, 30), §10, §14, §15, §16, §17, §21, §22, §24, loop 4 and narration, receipt [FORMER MEMBER TESTIMONY] | D009–D022, D030 |
| 4 (P2) | §12 is a table, not cards | DEFERRED: rebuilding §12 as thirty cards is a structural redesign (proposal E5), not a fix |  |
| 5 (P2) | No Evidence row; "Ungraded" | FIXED. 18 now Cultural; §1 Evidence row added | D027, D031 |
| 6 (P2) | Grade-basis mismatches | FIXED. 9 and 19 Codified (19 with new source [33]); 10 Codified after the guide's own "voluntary / obligatory" text was cited [1]; 13 Taught; 17 Taught (not Documented: a community's own article is not a court, inquiry or filing under the codex definitions); 22 and 14 kept (mixed/defensible basis); 28 kept Codified, with the boycott half marked as testimony | D023–D026, D028, D029 |
| 7 (P2) | [17] has no global figure | FIXED WITH NEW SOURCE. Cited to a reference-work summary [32] and described as such; [17] no longer cited anywhere (left in §26) | D001, D002 |
| 8 (P2) | §15 women marrying out | FIXED. [11] (Al Islam) gives women no permission | D032 |
| 9 (P2) | Narration "Five cases" | FIXED. The generator counted the bold "Internal machinery" line; it is now a plain note, so the narration reads "Four documented cases". Loop 6 quotation matched | D033, D036 |
| 10 (P2) | Loop summaries | FIXED. Loops 2, 4, 5 summaries now match their steps (interfaith events, security/construction and "parents teach" were not recorded) | D037–D039 |
| 11 (P2) | Currency | FIXED WITH NEW SOURCE. May 2025 timeline row and §22 line [34] (proposal E2) | D040, D041 |
| 12 (P2) | Receipts without sources | FIXED WITH NEW SOURCE. [9] and [5] on cases 1–2; §11 school receipt now [31], "violence at school" removed (not supported) | D034, D035, D042–D044 |
| 13 (P3) | UK title | FIXED ("National President (Amir)") | D045, D046 |
| 14 (P3) | Qadian / Ludhiana | FIXED | D002 |
| 15 (P3) | FY2025 entity | FIXED WITH NEW SOURCE as a sentence in §9 [35]; chart unchanged (proposal E1) | D047 |
| 16 (P3) | Chosen by / removable by | DEFERRED: structural (scripts split on " / ") |  |
| 17 (P3) | Family row IDs | DEFERRED: generated shared template |  |
| 18 (P3) | §7 label cells | DEFERRED: register-style labels left for scanning; decision needed |  |
| 19 (P3) | "centre" | FIXED (§22 only; Islam and Sunni defer spelling as house style) | D048 |
| 20 (P3) | §8 courts sentence | FIXED, now cites the Supreme Court judgment [5] | D049 |
| Shared | EXMNA row | FIXED: "Local affiliate support groups (listed on its site)" (checked on exmuslims.org). Islam and Sunni still say "Vetted private communities" | D050 |
| Shared | Islam-family alignment | Karma Nirvana hours and the Faith to Faithless number added as in Islam/Sunni. No NU, Diyanet, Pew, al-Azhar or Naseeha text in this volume | D051, D052 |

Not taken from the proposals: E5, E7 (no `tactics:` lines in this list-format §19), E8–E12 (new research).

## New sources
[31] UK Home Office CPIN, Ahmadis in Pakistan (Mar 2025) · [32] Wikipedia, "Ahmadiyya" (size summary) · [33] Waqf-e-Nau reconfirmation at fifteen · [34] USCIRF statement, 24 May 2025 · [35] Charity Commission, 1208543 financial history.

## New grade tally
Cultural 18, Taught 7, Codified 5, Contested 0, Ungraded 0 (counted from the §12 grade cells). "None of the 30 techniques is sourced to a named document."

## Not verified
- The 1208543 FY2025 figures (£41.46m, £31.65m) come from the 30 Sept fact-check log; the register blocks direct fetch.
- The global 10–20 million range has no primary count; it rests on a Wikipedia summary.
- The Munir, Zaheeruddin and Lahore/Cikeusik dates were not re-read.
