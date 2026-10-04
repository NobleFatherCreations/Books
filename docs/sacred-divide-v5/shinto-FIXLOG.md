# Shinto — discrepancy fix log, 2026-10-03

Every change is a reversible entry (SHNF-D001 to SHNF-D067) in `content/sacred-divide/edits/shinto.json`; set an entry's status to `rejected` to undo it. SHNF-D015, D030 and D031 are narration edits; the other 64 are md edits. All show `applied` in `logs/edits-status.json` (none FAILED); the narration edits were checked through `foryou()`, `intro()` and `questions()` and `sacred_divide_edits.check()`. Eight sources, [17] to [24], were added to §26. The prefix is SHNF because SHN-W/G/P/R/L/N ids already exist.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "5 of 30 sourced" with no named document | FIXED. `(sourced)` removed from techniques 2, 11, 19, 22, 30; §1 now "None of the 30 techniques is sourced to a named document" | D001-D006 |
| 2 (P1) | Techniques 11 and 19 graded Reformed on State Shinto, entries describe present-day pressure | FIXED. Both regraded Cultural on the entry's own basis; tally recomputed | D001, D003, D004 |
| 3 (P1) | "single most dangerous capture", "within a single generation" | FIXED. "One of the most severe cases of a state capturing a religious tradition"; "within about seven decades" in §3 lede and answer, §10, stage 7 and 8, §14, §23 question 5 and its narration | D007, D008, D010-D015 |
| 4 (P1) | "culture, not religion" as official self-description | FIXED. "is how many participants describe it" (§15) | D019 |
| 5 (P1) | "staff ... dismissed; dismissals voided" | FIXED. One research chief dismissed, a colleague demoted, the dismissal voided; §1, §7 table, §5 card. Source 12 and §19 agree | D016-D018 |
| 6 (P1) | "untaxed" | FIXED. Removed | D020 |
| 7 (P1) | Amulet sales fund the constitutional agenda | FIXED by qualifying. Nippon.com [8] (read 2026-10-03) calls Shinto Seiji Renmei the association's political arm and says nothing of its funding, so the page now says funding "is not recorded on this page". §7 two rows, §9 money table, stage 6, §18 priests row, loop 1 (summary, step 2, step 4, example), narration for-you structure and money | D021-D031 |
| 8 (P1) | Korean and Taiwanese conscripts "enshrined without consent" | FIXED WITH NEW SOURCES [17] (Tanaka, APJ: "without consultation with family members", Osaka District Court 2004) and [18] (Korea Times, Seoul suit Dec 2025; earlier Japanese suits dismissed as time-barred). Wording now "without consulting their families"; §17 and loop 7 | D032, D033, D052, D053 |
| 9 (P1) | "attributed to God" (stage 8, technique 30) | ALREADY FIXED by SHN-P002 and SHN-P003 (kami, ancestors and custom). Re-checked: no "God" remains in the volume. No new edit | |
| 10 (P1) | Ritual fee ladder path | NO CHANGE NEEDED. The path (Officiant, Shrine, Shrine family income) makes no claim of remittance to Jinja Honcho. Loop 1 step 2 did claim Jinja Honcho is sustained by the money; that is corrected under item 7 | D027 |
| 11 (P2) | Funeral monopoly card | FIXED. Card removed (it described Buddhist temples) | D034 |
| 12 (P2) | Political mobilization card | FIXED. Mailing-list and data-sharing lines replaced with what [8] records: shrine standing, Jinja Honcho to Shinto Seiji Renmei to legislators; funding stated as not recorded | D035 |
| 13 (P2) | "Decades of losing cases" | FIXED. "Decades of litigation, with Supreme Court wins in 1997 and 2010 [4]" | D036 |
| 14 (P2) | Whistleblower vindication already met | FIXED. §20 now asks for structural reform of the association's governance and notes the dismissal is already voided; loop 6 matched | D037, D038 |
| 15 (P2) | Source 10 label vs URL | FIXED. Relabelled Wikipedia, "Sayako Kuroda" (read 2026-10-03: replaced Atsuko Ikeda on 19 June 2017) | D039 |
| 16 (P2) | Sources 1 and 12 identical; 2021-22 steps unsupported | FIXED WITH NEW SOURCE [19] (Shinano Mainichi/Kyodo, 25 Apr 2022: judgment voiding the dismissal final). Source 1 annotation cut back to the March 2021 article; "Sept 2021" High Court date removed | D040, D041, D054 |
| 17 (P2) | Case 1 tag 17 (Smear Campaign) | FIXED. Tag dropped (28, 30 remain); the matching link removed from loop 6's feeder list | D042, D043 |
| 18 (P2) | Bare "None / Yes" in Documented? column | DEFERRED. Data flags shared with other volumes; completing them is a house-style decision | |
| 19 (P2) | British/American spelling mix | DEFERRED. House style, decide once for all volumes | |
| 20 (P2) | Unification Church dissolution missing from §8 | FIXED WITH NEW SOURCES [20] (Adnkronos, High Court 4 Mar 2026) and [21] (Kyunghyang, Supreme Court 23 Jun 2026). Added to the Religious corporations row; the "Civil Code" ground is reported by the sources and I did not state the statute myself | D044, D055, D056 |
| 21 (P2) | Imprisonment of Christians, no source | FIXED WITH NEW SOURCE [22] (Sumimoto, IJPS: Christian teachers and students arrested, Soka Gakkai founders imprisoned for rejecting compulsory State Shinto worship). Receipt changed from GOVERNMENT REPORT to ACADEMIC SOURCE at stage 7, §16, and cited at §17 | D045-D047, D057 |
| 22 (P3) | "largest counting discrepancy in the codex" | FIXED. "The two counts differ by a wide margin" (§1 and §7) | D048, D049 |
| 23 (P3) | "eighty years ago" | FIXED. "more than eighty years ago" (stays true) | D009 |
| 24 (P3) | Yasukuni "Independent", no source | FIXED WITH NEW SOURCE [23] (Wikipedia: independent religious corporation since 1946) | D050, D058 |
| 25 (P3) | "within about six months" | FIXED. Chart note now counts from the second sale | D051 |
| 26 (P3) | "codex" in reader text | DEFERRED. Shared template usage | |
| 27 (P3) | Help lines | PARTLY FIXED. (a) Japan: TELL Lifeline row added (number and hours read on its own page, 2026-10-03; English only; not religion-specific), and the section states no Japanese-language line has been checked. (b) Faith to Faithless hours added (Wed 10am-1pm, Thu 4-7pm, Fri 8-11am). (c) Recovering from Religion "aims to offer a 24-hour service". (d) ICSA unchanged (it has no helpline number; DEFERRED). Yorisoi Hotline not added: hours vary by day and I read them only on a third-party wiki page. "Checked" date set to 2026-10-03 | D059-D064 |
| 28 (P3) | Grade notes kept | NO CHANGE. Notes for 3 and 4 were already separated by SHN-R001 | |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D065, D066); dated bullet at the top of §27 (D067).

## New sources
17 Tanaka, APJ: Japan Focus (Yasukuni, Taiwanese plaintiffs, 2004). 18 Korea Times (23 Dec 2025). 19 Shinano Mainichi/Kyodo (25 Apr 2022). 20 Adnkronos (4 Mar 2026). 21 Kyunghyang Shinmun (23 Jun 2026). 22 Sumimoto, IJPS. 23 Wikipedia, Yasukuni Shrine. 24 TELL Lifeline.

## New grade tally
Cultural 30, Reformed 0 (grep: 30 `**Evidence grade.**` chips, all Cultural, zero `(sourced)`). The §1 Evidence row matches. Tally repeated nowhere else.

## Left on purpose / caveats
- Not fully verified: the Supreme Court date of 21 April 2022 and the Tokyo High Court upholding the ruling rest on search-engine summaries of Kyodo/ANN reports. Those pages could not be opened. Source 19's page confirms only that the voiding of the dismissal is final as of April 2022, and the §19 line "upheld on appeal and final in 2022" is kept with [19].
- Not verified: the 2006 Taiwanese suit in Osaka (Japan Times returned 402), so only the 2004 Osaka case in [17] is cited.
- TELL Lifeline hours are copied as printed (Friday to 02:00); I did not confirm them elsewhere.
- Unchanged and not on the list: "highest-deniability configuration in the codex" (technique 30), "clearest case in this codex" and "codex's clearest proof" (§5, §10), other `[GOVERNMENT REPORT]` receipts with no source entry (§5 timeline, §7 State Shinto row, §10, §11), "Suggested offerings are disclosed" on the Ritual fee ladder, "your children's schooling" in stage 6, and the unsourced "traditional family provisions" lobbying claim. Flagged for the owner.
- `build_sections('shinto')` could not be run: the Python `markdown` module is missing (not installed, as instructed). Narration edits were checked through `foryou()`, `intro()`, `questions()` and `sacred_divide_edits.check()`.
- Front matter `version: v4` and sites.json not touched (outside this task).
