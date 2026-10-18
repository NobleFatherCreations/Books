# Jainism — discrepancy fix log, 2026-10-03

Every change is a reversible entry (JAIN-D001 to JAIN-D064) in `content/sacred-divide/edits/jainism.json`; set an entry's status to `rejected` to undo it. JAIN-D017 and D018 are narration edits (the Surat date). All 62 md entries and both narration edits show `applied` (none FAILED); the narration edits were checked through `foryou()` and `questions()`. Sources [13]–[17] were added to §26.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Grades 19, 23, 26; stray `(sourced)` on 13, 14 | FIXED. 23 Contested to Cultural; 26 Codified to Cultural; 19 Documented to Cultural (its bullets are about dietary restraint; the litigation is pointed to §8). `(sourced)` removed from 13, 14, 19, 23, 26. §1 row recomputed | D001–D006 |
| 2 (P1) | §5 "1974" Anuvrat card | FIXED WITH NEW SOURCE. Retitled "1949 — The Anuvrat movement", dated 1 March 1949 [13]; "the model" and "no institutional enforcement" reduced to what is recorded | D007–D010 |
| 3 (P1) | "February 2026" Surat stay | FIXED WITH NEW SOURCE. Stay granted December 2025 by a family court, ceremony planned 8 February 2026 [17]; §8, §19 (title, dates, record, outcome), §20, §22, §24 and narration (law, q4). The Tribune report shows no later order, and the page says so | D011–D018 |
| 4 (P1) | §22 India tell | FIXED. "Three of the questions on this page, santhara, child initiation and abuse by a monk, have reached a court." | D019 |
| 5 (P1) | "No clergy... no excommunication apparatus" | FIXED WITH NEW SOURCES. §3 and §15 now say the monastic orders enforce nothing but community councils have imposed boycotts, citing a Thane case (June 2026) [14] and the Maharashtra 2016 Act [15]; loop 6 step 2 and technique 28 matched. Karnataka's law was not added (not verified) | D020–D023 |
| 6 (P2) | Loop 6 summary | FIXED. "Ordinary lapses are adjusted silently and go unrecorded; where a crime is involved, the courts act." Loop steps untouched | D024 |
| 7 (P2) | Loop 7 minority-status premise | FIXED by marking the gap: summary says the page records no instance. No sourced instance found | D025 |
| 8 (P2) | "attributed to God" (stage 8, technique 30) | FIXED. Now "karma and the ascetic tradition" | D026, D027 |
| 9 (P2) | §19 tactics tags | FIXED. Santhara `7, 25`; diksha `19, 22`; monk case `—` (neither 15 nor 22 describes a rape conviction; same choice as the Sikhism volume) | D028–D030 |
| 10 (P2) | Three dates for the litigation | FIXED. Card now "2008–2025", cited [4]; source 4 now says "2008" (The Federal gives the 2008 observation; no 2011 or 2012 ruling found in it) | D031–D033 |
| 11 (P2) | Terapanth listed beside Svetambara | FIXED. Glance and §7 row say the Terapanth is itself Svetambara | D034, D035 |
| 12 (P2) | Unsupported trust and philanthropy claims | FIXED by cutting or qualifying: "oldest continuously operating", "substantial/significant wealth", "concentrated board control", "publish little", "far exceeds its size" in §1, §5 timeline, §6-§9, §16, §20, §22 and loops 1, 4, 5. Replaced with "this page names no trust and cites no accounts" where the gap matters. P3-21 ("the money always does") included | D036–D053 |
| 13 (P2) | Oshwal 2025 figures | FIXED WITH NEW SOURCE. 2025 income £2.10m and spending about £1.7m confirmed on OpenCharities [16]; the £662,580 donations and exact £1.74m figures removed (bullet and loop 4 example). Chart kept | D054, D055 |
| 14 (P2) | "School admission" in the §9 pipeline card | FIXED. "Marriage access and business credit" | D056 |
| 15 (P2) | Conviction wording (§21, §19, §24) | FIXED. "with other evidence"; "went to the room where she was alone"; "a court has convicted a monk" | D057–D059 |
| 16 (P2) | "Lineage designation / Nobody below" fragment | DEFERRED. Scripts split on " / "; needs a change to the split logic for all volumes | |
| 17 (P2) | Grade notes 13, 14, 15 | Covered by item 1 (13, 14 lost `(sourced)`; 15 untouched, its note states its own basis) | D004, D005 |
| 18 (P3) | Timeline fragments | DEFERRED. Optional; timeline block not reflowed | |
| 19 (P3) | Spelling variants | DEFERRED. House style shared by other volumes | |
| 20 (P3) | "A widow's silence" | FIXED. "A woman's silence" (widows appear nowhere else). The "etiquette" closer left as written | D060 |
| 21 (P3) | "The money always does" | FIXED (see item 12) | D053 |
| 22 (P3) | Nita "young woman" | Already fixed (JAI-N001) | |
| 23 (P3) | §25 hours | No change. Shared help lines, covered by the global corrections; no India line exists (not invented) | |
| 24 (P3) | §22 UK card | No action needed | |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D062, D063); dated bullet at the top of §27 (D064); sources 13–17 appended (D061).

## New sources
13 Acharya Tulsi / Anuvrat, 1 March 1949 (Wikipedia) · 14 Navbharat Live, Thane boycott of a Jain family (8 Jun 2026) · 15 Maharashtra Social Boycott Act 2016 (India Code) · 16 OpenCharities, Oshwal Association · 17 The Week / PTI, Surat interim stay (10 Dec 2025).

## New grade tally
Cultural 28, Taught 2 (3 and 4), Documented 0, Contested 0, Codified 0 (30). No technique is sourced to a named document. §1 Evidence row matches the §12 chips (grep: 30 chips, 28 Cultural, 2 Taught, no `(sourced)` left).

## Left on purpose / caveats
- The Anuvrat date rests on a Wikipedia page (search-result summary, not read in full); Britannica was not found to carry it.
- The Tribune fetch gave the stay date as 22 December 2025, which conflicts with The Week (a Monday before 10 Dec); the page says only "December 2025".
- The Thane boycott (source 14) is a complaint report; no FIR had been registered. The text says boycotts "have been imposed", on the strength of this one case plus the statute's purpose; the Karnataka statute is not cited.
- Oshwal 2021–2023 chart values were not re-checked (only 2024 in the earlier log, 2025 now). The Charity Commission register still returns 403.
- The §14 prediction and loop 6 step 5 ("trust accounts remain unpublished") and the scorecard "N" are left: they are a prediction and a "not established" mark.
- The §19 monk case now has no technique tag.
- Bombay HC 2012 ruling not found; only the 2008 observation is stated.
- `build_sections('jainism')` could not be run (Python `markdown` module missing, not installed); narration checked through `sacred_divide_narration`.
- Front matter `version: v4` and sites.json not touched.
