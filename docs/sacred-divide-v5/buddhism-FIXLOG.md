# Buddhism — discrepancy fix log, 2026-10-03

Every change is a reversible entry (BUDF-D001 to BUDF-D058) in `content/sacred-divide/edits/buddhism.json`; set an entry's status to `rejected` to undo it. BUDF-D027, D043, D044, D046 and D058 are narration edits. All 53 md entries show `applied` in `logs/edits-status.json` (none FAILED) and the narration edits apply through `foryou()` and `questions()`. Four sources, [19] to [22], were added to §26. (BUDF-D050 intentionally has count 2: the identical Size cell appears in §1 and §7.)

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "Every documented failure ... set aside for charisma" (§3, §23) | FIXED. "Each of the teacher-misconduct cases ... in favor of a teacher's authority"; the same universal claim in the §7 tell also narrowed | D001–D003 |
| 2 (P1) | Nine grades | FIXED. 16–22 and 24 regraded Taught to Cultural, 23 Codified to Cultural (24: the entry's own claim is applied practice), 28 note rewritten ("cases seldom reach a record"). `(sourced)` removed from 14, 23, 25, 26; kept on 6 (Vinaya) and 12 (note now names the Lewis Silkin report [6]). §1 Evidence row recomputed | D004–D018 |
| 3 (P1) | Thai Supreme Patriarch as apex; "Crown" chosen/removable | FIXED. §1 says no single office leads Buddhism and points to the Tibetan Buddhism and Soka Gakkai volumes; removal claim replaced by "sources do not say"; same fix in §7 table, §7 lede, §8, §22, loop 4 and narration | D019–D025, D027 |
| 4 (P2) | Loop 7 unevidenced | FIXED by marking the gap in the summary (page records no instance of persecution being cited against a critic; pattern observed). Steps untouched. No sourced instance found | D028 |
| 5 (P2) | §5 Ambedkar figure; Wirathu "largely did not restrain" | FIXED WITH NEW SOURCES. Ambedkar: 400,000 to 500,000 [21]. Wirathu: barred from preaching for a year by the State Sangha Maha Nayaka Committee, March 2017 [20]; Sri Lankan authorities' actions stated as not recorded | D029–D032 |
| 6 (P2) | "Organizational collapse" vs "survived" | FIXED. §20 now "organizational upheaval" in "some of them" | D033 |
| 7 (P2) | "Most of the West" are charities | FIXED. "which many are in the UK" | D034 |
| 8 (P2) | §19 tags | FIXED. Case 1 `26`; case 3 `—`; case 4 `—` (the proposed 11, 16 describe treatment of critics and do not fit hate speech either) | D035–D037 |
| 9 (P2) | UK/Australia/Canada, ACNC unsourced | FIXED by narrowing to the UK [6]; ACNC removed. The ACNC site returned 503, so no Australian source was added | D038, D039 |
| 10 (P2) | Empty receipt cell | FIXED. [PATTERN OBSERVED], as for the same claim in §3 | D040 |
| 11 (P2) | Myanmar law cell "—" | FIXED. "No law on the monastic order is recorded here", with the 2017 committee ban [20] | D041 |
| 12 (P2) | Ordination "closed to women in major traditions" | FIXED. "Not recognized in Thailand or by some other national sanghas" (§14 and narration q3, who-gets-hurt) | D042–D044 |
| 13 (P2) | "Audited and never is" | FIXED. "rarely is" (§23); narration "whose accounts are rarely public" and "so rarely shows" | D045, D046, D058 |
| 14 (P2) | "Crazy wisdom ... never once" | FIXED. States what the page records instead | D047 |
| 15 (P2) | "Almost all donations" | FIXED. "Most ... (£1.89m of £2.23m in the latest year)" | D048 |
| 16 (P2) | "centers annex the schedule" | FIXED. "put that schedule to use" (sense taken from the entry) | D049 |
| 17 (P3) | Spelling mix | DEFERRED. House style shared by the other volumes; decide once for all | |
| 18 (P3) | Family row prints slugs | DEFERRED. Same line in every family volume; template change | |
| 19 (P3) | Unsourced "near 500 million" | FIXED WITH NEW SOURCE. Replaced in §1, §4, §7 by Pew's 2012 count (about 488 million for 2010) [19] and Pew's own statement that its later estimates exclude folk-tradition practitioners | D050, D051 |
| 20 (P3) | 94 years without the cap | FIXED WITH NEW SOURCE, qualified. A later appeal report gives a 20-year term [22]; the 20-year cap itself is not stated on the page | D052 |
| 21 (P3) | Blackmail case outcome | FIXED by marking the gap. No court outcome for the woman found | D053 |
| 22 (P3) | Supreme Patriarch about 99 | FIXED. Check-again note in §1 and §22 | D019, D026 |
| 23 (P3) | §25 hours / ICSA number | No change. Shared lines covered by the global corrections; numbers verified correct | |
| 24 (P3) | Timeline and Who holds what fragments | DEFERRED. Optional rewrite of label-style cells; not reflowed (same as the Jainism volume) | |
| 25 (P3) | §4 needs new sources | DEFERRED. New research the owner has not asked for | |
| Template | "attributed to God" (stage 8, technique 30) | No edit needed. Already replaced earlier (they read "the dharma, the lineage, or skillful means"); no "God" text remains | |
| Pipeline | §9 cards | No change, per the discrepancy file (both fit). Note: the Merit economy card says "Nothing is disclosed" while §9 cites a public charity register; left because loop 1 quotes the card | |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D055, D056); dated bullet at the top of §27 (D057); sources appended (D054). The §1 Evidence row is D018.

## New sources
19 Pew, *Global Religious Landscape* (2012) · 20 Anadolu Agency, Wirathu preaching ban (11 Mar 2017) · 21 Wikipedia, Deekshabhoomi (Ambedkar conversion figures) · 22 Bangkok Post, appeal report on the ex-National Office of Buddhism head.

## New grade tally
Taught 6 (3, 4, 5, 7, 25, 26), Cultural 21, Contested 2 (14, 15), Documented 1 (12), Codified 0 (30). Two techniques are sourced to a named document (6 and 12). §1 Evidence row matches the §12 chips (counted with grep: 30 chips; 2 `(sourced)` marks).

## Left on purpose / caveats
- Source [22] was reached through a search snippet only; the Bangkok Post page returned HTTP 451 to the fetch tool. The 20-year figure rests on that snippet and the earlier fact-check note, so the sentence says "may be shorter".
- Source [19] was confirmed through search results, not a direct fetch; the Pew 2012 page says nothing here about folk religion, so the page does not tie the 488 million to it.
- Sources [20] (fetched) and [21] (fetched, Wikipedia) are as stated; [21] is a secondary source.
- Technique 24 was regraded Cultural on the entry's own claim; Taught is arguable.
- Every technique except 3, 4, 5, 7, 25 and 26 is now Cultural or Contested, which flattens the grading; the owner may prefer another frame.
- Not changed: the Sri Lanka Mahanayaka election claim (F20) and the US-churches-exempt claim in §22 remain unsourced.
- `build_sections('buddhism')` could not be run: the Python `markdown` module is missing (not installed, as instructed). Narration edits were checked through `foryou()` and `questions()`.
- Front matter `version: v4` and sites.json were not touched (outside this task).
