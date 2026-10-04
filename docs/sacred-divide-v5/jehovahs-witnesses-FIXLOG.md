# Jehovah's Witnesses — discrepancy fix log, 2026-10-03

Every change is a reversible entry (JW-D001 to JW-D065) in `content/sacred-divide/edits/jehovahs-witnesses.json`; set an entry's status to `rejected` to undo it. All 65 apply (0 FAILED). Sources [23]–[28] were added to §26, and source [8] was replaced (its number is unchanged).

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Monthly hours presented as current for everyone | FIXED WITH NEW SOURCE [24]. §2 (Donna reports whether she took part; hours until Nov 2023), Stage 3 and its closing line, Stage 6, technique 8 (bullet, counter, grade note), technique 29 bullet, §18 row split into Pioneers and Regular publishers | D001–D009 |
| 2 (P1) | Two-witness rule "about property disputes" | FIXED. Now "written for accusations of any wrongdoing (Deuteronomy 19:15: 'for any iniquity, or for any sin')" in §5 and §14. Matthew 18:16 and 1 Timothy 5:19 not added | D010, D011 |
| 3 (P1) | Eight million / nine men | FIXED. Nine million members; eleven men; "Eleven men, and you may not question them." | D012–D014 |
| 4 (P1) | §9 Tithe and Missionary self-funding cards | FIXED. Both removed | D015, D016 |
| 5 (P1) | Grade mismatches | FIXED (see tally). 4 Reformed to Codified; 11 Codified to Taught; 12 Documented to Taught; 18 Documented to Cultural; 25 Codified to Taught; 29 Codified to Cultural; 7 and 24 flag cleared; flags also cleared on 14, 17, 19, 20, 21, 22, 28 (no document named); 26 regraded Codified to Documented (see item 10); 27 now names the 1966 book [23] | D017–D034 |
| 6 (P2) | "Forty years" | FIXED. "Seventy years" in §23 Q3 and narration q3 | D035, D036 |
| 7 (P2) | Conti superlative | FIXED WITH NEW SOURCE [28]. Attributed to her lawyer, limited to religious child-abuse cases | D037 |
| 8 (P2) | Case 29 tags | FIXED, differently from the suggestion. `12, 18, 28` is now `18, 30`. 12 is dropped, not kept, because the case text records no questioner attacked and technique 12 is no longer graded on this case | D038 |
| 9 (P2) | §9 "Unpaid labor" and "Legal defense" cards | FIXED. Brooklyn prices shown as reported [10][11], proceeds destination "hidden"; NDA path dropped; "donations funded the defense stays hidden" and the "member giving" source line replaced with "not recorded on this page" | D039–D042 |
| 10 (P2) | Title-holding unsourced | FIXED WITH NEW SOURCE [25]. Narrowed to "in many countries" (§9, §12 Stage 6, three loops, §16); England and Wales cited via the 2022 Kingdom Hall Trust merger; technique 26 now rests on that record | D043–D049, D031 |
| 11 (P2) | 2019 reporting policy omitted | FIXED WITH NEW SOURCE [27]. Added to the §20 promises note and §24 item 4. §23 closing left as written: it makes no claim the policy contradicts | D050, D051 |
| 12 (P2) | "Charity regulators" for Norway | FIXED. "State registration authorities" | D052 |
| 13 (P2) | Grade notes mismatched | FIXED by item 5 | — |
| 14 (P3) | Norway 3–2 | FIXED. In §8 and §22, with the majority's article 9 finding | D053, D054 |
| 15 (P3) | Japan 81% | FIXED. "More than three-quarters" (451 of 581 = 77.6%) in §8 and loop 3; the 81% base could not be confirmed | D055, D056 |
| 16 (P3) | March 2026 blood revision | FIXED WITH NEW SOURCE [26]. In §10 and §14 | D057, D058 |
| 17 (P3) | Source 8 is Wikipedia | FIXED. Replaced with *The Watchtower*, Aug 2024, study article 35. The "elders to visit" detail could not be re-verified and was dropped from the entry | D061 |
| 18 (P3) | Barnette spelling | FIXED. "Barnett family (the court record spells it Barnette)"; case name unchanged | D059 |
| 19 (P3) | 2025 spending | FIXED. £78.17m spending added beside the £38.46m income | D060 |
| 20 (P3) | Technique names in capitals | DEFERRED. House style shared by every volume; decide once | — |
| 21 (P3) | "Unusually honest activity measure" | DEFERRED, left as written. It is the page's judgment, per the list; no change requested | — |

Meta: `checked` and "Last checked" set to 2026-10-03; patch note added at the top of §27 (D063–D065). Template-leak rule (stage 8, technique 30 "attributed to God") does not apply: this tradition's authority is Jehovah. No loop summary needed rewriting.

## New grade tally (§12 chips counted)
Codified 18, Taught 7, Documented 3, Cultural 2, Reformed 0 (= 30). Sourced to a named document: 3 (techniques 4, 26, 27). §1 Evidence row updated; no other place repeats the tally.

## New sources
23 *Life Everlasting* (1966), 1975 chronology; 24 NBC News / RNS, hour reporting; 25 Fundraising UK on the Kingdom Hall Trust merger; 26 AP via Mining Journal, March 2026 blood policy; 27 JW summary to the NZ Royal Commission (2021), reporting policy; 28 KTAR/AP 2012, Conti verdict.

## Left on purpose / could not verify
- Pull-quotes `money` and `voices` in `content/sacred-divide/pullquotes/jehovahs-witnesses.json` were edited so they still match the text.
- Source [23] links a critic-run archive of the 1966 book's passages, not the book itself; [25] is trade press reporting Charity Commission data; [27] is the organization's own submission. The "since 2019" wording became "2018–2019 child-protection policy" because that is how the sources date it. The statement that the two-witness rule still governs congregational action rests on the fact-check log (F18), not on a new fetched source.
- Not re-checked: the F19 detail that "disfellowshipped" was renamed in March 2024 (the Watchtower article title uses "removed from the congregation").
