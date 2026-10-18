# Zoroastrianism — discrepancy fix log, 2026-10-03

Every change is a reversible entry (ZORF-D001 to ZORF-D078) in `content/sacred-divide/edits/zoroastrianism.json`; set an entry's status to `rejected` to undo it. ZORF-D078 is a narration edit; the other 77 are md edits. All 77 md entries show `applied` in `logs/edits-status.json` (none FAILED); the narration edit was checked through `foryou()` and `questions()`. The prefix is ZORF because ZOR-W/G/P/R/L/N ids already exist. Item numbers are the flat numbers in `discrepancies/zoroastrianism.md` (1-5 P1, 6-18 P2, 19-29 P3).

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "Marrying out is legal everywhere" | FIXED WITH NEW SOURCE [15]. Now legal in India and the UK; in Iran Civil Code Art. 1059 ("Marriage of a female Moslem with a non-Moslem is not allowed") means a Zoroastrian man cannot legally marry a Muslim woman | D001 |
| 2 (P1) | "attributed to God" template line | ALREADY FIXED by ZOR-P001/P002 (descent and ancient custom). Re-checked: no "God" remains in the volume. Zoroastrianism is theistic, so no change was needed in any case | |
| 3 (P1) | ZTFE 2024 income bar | FIXED. Chart now 2024 = 1,350 (GBP 1,350,097). Re-check of the other years found 2021 was also wrong (753 vs GBP 730,434); 2022 (474), 2023 (401), 2025 (479) confirmed. Source 10 now lists the figures | D002, D003 |
| 4 (P1) | "Panthaki" defined wrongly | FIXED. The term is replaced by the concept it was meant to gloss ("Who is a Parsi"); panthaki is not defined on the page (a panthaki is a priest in charge of a priestly district) | D004 |
| 5 (P1) | Four unattributed "official denial" quotations | FIXED. Presented as the page's paraphrase ("The defence, paraphrased: ...") in §3 and §15 | D007-D010 |
| 6 (P2) | Three population ranges | FIXED. §1, §7 and §4 use the sourced FEZANA 2012 range (about 111,000-122,000); the 200,000 upper bound had no source | D011, D012 |
| 7 (P2) | "decisively" | FIXED. §7 "as a contributing cause", with a note that the sources do not weigh the causes; §16 "a contributing cause". "Documented driver" in §3, §10, §14 and the loop text was not flagged and is unchanged (the narration quotes the §14 row) | D013, D014 |
| 8 (P2) | §5 card dated 2018 | FIXED. Retitled 2017 | D015 |
| 9 (P2) | Who decides who counts | FIXED. All three places now say: trustees and panchayats hold housing and facilities criteria; priests hold initiation and ritual access | D004-D006 |
| 10 (P2) | Ritual fee ladder card | FIXED. Disclosed: "Nothing is recorded; no fee schedule appears on this page." Hidden: "Not recorded on this page." | D021 |
| 11 (P2) | Honor and marriage economy card | FIXED. Card removed | D022 |
| 12 (P2) | Grades | FIXED. Regraded Cultural: 17, 20, 21, 23, 24, 25, 26, 27, 29. Technique 3 regraded Taught (its entry is mostly the tradition's own teaching; rewritten). 7 kept Cultural (the entry's own basis says the lived bind is communal). 22 kept Codified. `(sourced)` removed from 2, 15, 19, 23 (name no document); kept on 28, which now names *Petit v. Jijibhai* and *Goolrokh Gupta v. Burjor Pardiwala* | D059-D073 |
| 13 (P2) | Repeated line, stages 1 and 2 | FIXED. Stage 2 now has its own line | D023 |
| 14 (P2) | Iran card empty fields | FIXED WITH NEW SOURCE [15]. "documented" from §8; "exit" is "Not established from any public source."; "keeps it small" removed, tell restated from [9] and Art. 1059 | D024 |
| 15 (P2) | §8 Iran accountability cell | FIXED. "Not established from any public source." | D025 |
| 16 (P2) | Interim arrangements | FIXED. §22 India tell, loop 6 example and §24 item 2 now say interim arrangements were cited by counsel as available in Mumbai, Delhi, Kolkata and Pune (LiveLaw [5], read 2026-10-03; counsel's statement, details not given). "§23 question 4" carries no such sentence, so no edit there | D026-D028 |
| 17 (P2) | "judgment is reserved" | FIXED WITH NEW SOURCE [16] (Kerala Kaumudi, 12 Aug 2026). §5, §8, §19 say reserved on 14 May 2026, no verdict reported at the last check (3 Oct 2026), expected about 6 Oct. **Must be re-checked at release.** §23 does not contain the phrase | D016-D020 |
| 18 (P2) | Unsourced comparatives | FIXED. §18 diaspora "more inclusive" and §11 "female religious instructors" cut. §6 carries no such sentence | D029, D030 |
| 19 (P3) | Fragments in "Chosen by / removable by" | PARTLY FIXED. "Removable by: Nobody" (high priesthood, §7) now "Not recorded on this page." The glance cell and §7 ballot cell remain fragments: DEFERRED (scripts split the glance cell on " / ") | D031 |
| 20 (P3) | Question is a noun phrase | FIXED in §1, §3 and the narration that quotes it | D032, D078 |
| 21 (P3) | Priority claim in §3 lede | FIXED. "puts moral choice at the center of its teaching" | D033 |
| 22 (P3) | American/British spelling | DEFERRED. House style, decide once for all volumes | |
| 23 (P3) | "burial" | FIXED in the 15 technique-entry bullets (funeral rites / funerary practices). Left on the ZTFE chart note (a UK burial ground exists) | D042-D056 |
| 24 (P3) | Gujarat migration date | FIXED. "(traditional account; contested)" | D034 |
| 25 (P3) | Tags for Gupta and Petit | FIXED. Gupta 14, 28; Petit 14, 28 | D057, D058 |
| 26 (P3) | Help lines | PARTLY FIXED. Faith to Faithless hours (Wed 10am-1pm, Thu 4-7pm, Fri 8-11am; also source 11); Recovering from Religion "aims to offer a 24-hour service"; Karma Nirvana Mon-Fri 9am-5pm and remit limited to coerced marriage; "Checked" date set and the lack of an India or Iran line stated. Humanists at Risk still prints no number: DEFERRED (no source found); India/Iran lines: DEFERRED (new research, proposal E10) | D037-D041 |
| 27 (P3) | Jiyo Parsi 490 / source 7 | PARTLY FIXED WITH NEW SOURCE [17]. §8 now 534 births since 2014-15 (IANS, 10 Aug 2026, Rajya Sabha reply; Rs 37.43 crore); source 3 annotated. Source 7 and the "25,000+" electorate could not be re-read (403). A search found only that 7,364 voters took part in the 2022 election, not the roll size. Left as written and flagged | D035, D036 |
| 28 (P3) | Loop titles | DEFERRED. Frozen shared titles; a house-style decision across volumes | |
| 29 (P3) | §27 log | FIXED. Dated bullet added at the top | D077 |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D075, D076); §27 bullet D077; tally D073; sources D074.

## New sources
15 International-Divorce.com, Iran Family Law (Civil Code Art. 1059). 16 Kerala Kaumudi, 12 Aug 2026 (reserved 14 May 2026, verdict expected by 6 Oct). 17 IANS, 10 Aug 2026 (534 births). Appended after source 14; nothing renumbered.

## New grade tally
Codified 9 (2, 14, 15, 16, 18, 19, 22, 28, 30), Cultural 20, Taught 1 (technique 3); grep of the 30 `**Evidence grade.**` chips agrees. One technique is `(sourced)` (28). The §1 Evidence row matches; the tally is repeated nowhere else.

## Left on purpose / caveats
- Verdict timing: the nine-judge bench's verdict was expected about 6 October; re-check before release.
- Article 1059 was read on a secondary site (the USIP Iran Primer returned 503); it quotes the Civil Code. Whether UK law allows marrying out is stated without a source (general knowledge).
- ZTFE figures for 2021-2024 were read from the OpenCharities mirror and a search summary of the register; the register page returned 403.
- Panthaki: the correct definition rests on a search summary of Encyclopaedia Iranica; the Iranica page returned 403, so it is not cited on the page.
- Unchanged and not on the list: "documented driver of the decline" (§3, §10, §14), "faster than any external pressure has managed" (§17), "took care of its poor better than almost any comparable group" (F20), menstrual seclusion (F21), "persecuted minority" vs "recognized" vs "discriminated" for Iran (F22), unsourced "acceptance practices" in Iran (§4, §20), and the proposals E3, E5-E9, E11 (new research).
- `build_sections('zoroastrianism')` could not be run: the Python `markdown` module is missing (not installed, as instructed). The narration edit was checked through `foryou()` and `questions()`.
- Front matter `version` and sites.json not touched (outside this task).
