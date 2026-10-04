# Judaism: discrepancy fix log, 2026-10-03

Every change below is a reversible entry (JUD-D001 to JUD-D068) in `content/sacred-divide/edits/judaism.json`; set an entry's status to `rejected` to undo it. Sources [20]–[27] were added to §26. All entries show `applied` in `logs/edits-status.json` (none FAILED); `build_sections('judaism')` runs clean. One existing entry, JUD-N003, now has `count: any` because ORA is listed first in §25 and the narration sentence it patched no longer appears.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "The one exit is a civil marriage online" | FIXED WITH NEW SOURCE. §14 now names both exits (marriage abroad, registrable since the early-1960s Funk-Schlesinger ruling, and online through Utah); the ruling is also added to the §8 law row. Source [23] | D001, D002 |
| 2 (P1) | Courts "decline to apply sanctions" | FIXED WITH NEW SOURCE. Scoped: diaspora courts have no statutory sanctions; Israel's courts have held them since 1995 and apply them in some cases (rabbinate unit: 135 male refusers sanctioned in 2024, 209 in 2023). Applied in §1, §3, §10 card 1, §12 stage 6, §14 (two rows and the glossary row), §17 cross-reference, §18, §20, §23 q1. Sources [20], [21] | D003–D014, D016, D017 |
| 3 (P1) | Grades 7 and 15 Codified | FIXED. 7 Double Bind to Contested, 15 Triangulation to Cultural, each on what its own entry describes. The four *(sourced)* markers (7, 14, 15, 26) removed because none of the four names a document. Tally now Contested 22, Cultural 8, Codified 0, none sourced to a named document (counted from the chips) | D018–D022 |
| 4 (P1) | Scorecard Y, Y, Y with no evidence | FIXED. Safeguarding, External first and Reply regraded to P. The generated narration no longer says "deserves credit" (checked: with six P grades the score sentence is empty) | D023 |
| 5 (P2) | 1953 law and "first time in 1,900 years" | FIXED. Card now says the rabbinical courts; timeline row says "the enforcement of a modern state" | D024, D025 |
| 6 (P2) | Kidnapping-ring card had no source | FIXED WITH NEW SOURCE. Epstein named, convicted April 2015, sentenced to ten years that December; source [22] (Boston Globe) | D026, D027 |
| 7 (P2) | 1996 burial law is a statute | FIXED. "courts and legislature" | D029 |
| 8 (P2) | §9 pipeline cards | FIXED. The curriculum and trust-deed cards removed (nothing in the volume records them); the school-tuition card kept with its path cut to what the §9 table records and its two template lines set to "Not recorded on this page"; the certification card's "hidden" line likewise | D032–D034 |
| 9 (P2) | Youth movements "designed to shape political and marital choices" | FIXED by removal in §11 and loop 3 (no source found) | D035, D036 |
| 10 (P2) | Kashrut overlapping fees | FIXED by rewording. No fee schedule or filing found; every [FINANCIAL RECORD] attached to the overlap or reliability claim is now [PATTERN OBSERVED] and the claim says only what the page can support (§7, §9, §14, §16, §18, loop 1) | D032, D037–D044 |
| 11 (P2) | Mesirah ruling and lost standing | FIXED WITH NEW SOURCE. Now the Rabbinical Council of America's 2011 statement (mesirah does not apply; refer to secular authorities immediately) with Agudath Israel's qualified position, source [25]; the unsourced "families still lose their standing" is a question for the reader (§10, §23 q2, loop 7) | D045–D048 |
| 12 (P2) | Loop 5 title and summary | FIXED. Title "Donations to Boards to Deference to Donations", the summary as proposed, and the unsupported "value flows toward the donor class" sentence removed | D049, D050 |
| 13 (P2) | §19 tactics tags | FIXED. Cases 1 and 2 to `9, 19` (a completed conversion not recognised); case 3 to `14` on the Stage 5 text. Caveat: no §12 technique describes a statutory monopoly directly | D051–D053 |
| 14 (P2) | Population figures | FIXED. 15.8 million, 7.3 million and 6.3 million throughout, with the definition (religion, ethnicity or upbringing); the Pew attribution dropped | D054–D057 |
| 15 (P2) | "150-member" body | FIXED WITH NEW SOURCE. The size is supported (Chief Rabbinate law, 80 rabbis and 70 public representatives, source [24]); 135 to 140 votes were cast because not every member voted. Kept and cited in §7 | D030, D031 |
| 16 (P2) | Circular "which is the evidence" | FIXED in loop 2 and the Stage 7 prompt | D058, D059 |
| 17 (P3) | Mixed American / British spelling and transliteration | DEFERRED: house style across all volumes | none |
| 18 (P3) | Family row prints slugs | DEFERRED: template change shared by every volume | none |
| 19 (P3) | "Documented?" column says "Usually low" | FIXED ("Yes, and it is usually low.") in §3 and §15 | D060 |
| 20 (P3) | (sourced) on 7, 15, 14, 26 | FIXED with item 3 (all four removed) | D018–D021 |
| 21 (P3) | LGBTQ Jews in §16 only | FIXED by tying the line to what §11 and §17 record; no new claim | D061 |
| 22 (P3) | Tuition "per child" and unsourced "single income" clause | FIXED in §17 and §7 (cumulative wording, §2's $34,000 for two cross-referenced, clause removed) | D062, D063 |
| 23 (P3) | 1985 Conservative ordination unsourced | FIXED WITH NEW SOURCE: JWA, with the October 1983 faculty vote, source [26] | D028 |
| 24 (P3) | UK Chief Rabbi unnamed | FIXED WITH NEW SOURCE: Ephraim Mirvis, source [27] | D064 |
| 25 (P3) | §25 hours and ORA | FIXED. Hours for JWA and NAPAC, ORA's 1-844-OSF-LINE note, Footsteps "states no hours"; ORA listed first so the narration names it. No Israel or liberal-community line added (new research) | D065 |
| 26 (P3) | Cross-volume check with orthodox-hasidic-judaism | CHECKED, no edit needed: that volume's §1 and §7 name the dynasties (Satmar, Ger, Belz, Chabad) and say no one can remove a rebbe, matching this volume's "Nobody can remove them" row. Its exit-cost content was not re-audited here | none |

## New sources
[20] Library of Congress Law blog, 1995 enforcement law. [21] *Times of Israel*, 4 Feb 2025, get-unit sanctions. [22] *Boston Globe*, 15 Dec 2015, Epstein sentence. [23] Cardozo Supreme Court Project, *Funk-Schlesinger*. [24] Israel Democracy Institute, electoral assembly. [25] JTA, 26 July 2011, RCA and Agudath Israel on mesirah. [26] Jewish Women's Archive, Eilberg 1985. [27] Wikipedia, Ephraim Mirvis.

## New grade tally
Contested 22, Cultural 8, Codified 0 (30 techniques); none sourced to a named document. §1 Evidence row and the §12 chips agree.

## Claims not fully verified, and judgment calls
- **Year of the marriage-abroad ruling.** The discrepancy list and Wikipedia say 1962; the Cardozo case page says the Supreme Court accepted the appeal in 1963. The page says "early 1960s". The "about 20,000 couples a year" figure was not repeated: the one source read (Wikipedia, CBS data) gives about 9,200 overseas weddings registered in 2022.
- **"Diaspora courts rarely use communal sanctions"** (the owner's proposed wording) found no source; the page now says only that diaspora courts have no statutory sanctions and that it records no figure for how often they use the communal ones. The Israeli figures are for sanctions of all kinds, not imprisonment alone.
- **Kashrut fees and the mesirah "lost standing" claim** could not be sourced (no fee schedule or filing found); reworded or turned into a question.
- Source [27] is Wikipedia, used only for the office-holder's name and start date.
- The §17 "From The Women's Codex" bullet quotes another volume; it was edited here only so this volume does not repeat the overstated claim. The §2 composite still says a court "has a remedy it declines to use"; it is set in a North American suburb, so it stays consistent with the diaspora scoping.
- Left in the volume though not on the list: the certification card's path "Advisory positions at certified firms" and the Disclosed line on that card.
- Not fixed, per the brief: help-line proposals E11 (no Israel or liberal-community line), E5, E6, E9, E10, E12 (new research).
