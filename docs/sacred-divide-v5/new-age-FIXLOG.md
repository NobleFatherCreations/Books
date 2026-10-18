# New Age — discrepancy fix log, 2026-10-03

Every change is a reversible entry (NEWF-D001 to NEWF-D096) in `content/sacred-divide/edits/new-age.json`; set an entry's status to `rejected` to undo it. NEWF-D094 to D096 are narration edits; the other 93 are md edits. The prefix is NEWF because NEW-W/G/N ids already exist. After `scripts/sacred-divide-export-md.py` all 96 show `applied` in `logs/edits-status.json` (0 FAILED). The Python `markdown` module is missing and was not installed, so `build_sections('new-age')` was not run; narration edits were checked through `foryou()`, `intro()`, `questions()` and `sacred_divide_edits.check()` (all applied once). Rule followed: where a source supports a claim it is kept (Ray's conviction, Raniere's 120 years, Goop's $145,000, Herbalife's $200 million, the Embassy alert); where it does not, the claim is qualified or removed. No gaps were filled by invention.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Shared §9 pipeline cards | FIXED. "Front organization" and "Publishing and media arm" removed; "Graded spiritual services" Path rewritten to what §9 records (participant to teacher's company, rest "not recorded on this page"). Retreat and Certification cards kept | D068-D070 |
| 2 (P1) | Teal Swan in a COURT RECORD row | FIXED. Name removed | D020 |
| 3 (P1) | Children prosecutions/deaths receipt, related unsourced receipts | FIXED. Claim replaced by "this page cites no case"; loop 3 summary, step 4, break-point text, §16, §17 matched. Unsourced "ACADEMIC SOURCE" receipts on misinformation (timeline, §5 card, §11, §16, §17) changed to PATTERN OBSERVED and "this page cites no study". "Widely reported and rarely prosecuted" replaced. A verified case was not sought (new research not asked for) | D009, D021-D032 |
| 4 (P1) | "Sourced" techniques / Taught grades with no named text | FIXED by regrading (no manifestation text is in §26). Taught 3-8, 11-13, 25 to Cultural; "(sourced)" removed from 6, 9, 10, 12, 25, 26, 28; 26 Documented to Cultural. §1 Evidence row rewritten | D071-D085 |
| 5 (P1) | Corporate owners at the top | FIXED. §1 "Who's in charge", "Chosen by / removable by", §7 lede and office row now say no office exists and the page cites no source for any body that appoints, owns or removes teachers. Narration §7 and question 5 example matched. Narration §1 is generated from the table and now reads correctly without a patch | D033-D036, D038, D095-D096 |
| 6 (P1) | "Conviction followed by rebrand" | FIXED. Replaced by what the page records (no body removed a teacher; courts convicted Ray and Raniere). Prediction labelled analysis. Loop 6 summary, steps 4 and 5 matched | D040-D044 |
| 7 (P2) | Pew figure | FIXED. Four beliefs named, "belief not membership", 2018 stated (§1, §6, §7); source 1 note corrected to Pew's text as read (about four in ten each for psychics and spiritual energy; the 41/42 split could not be retrieved) | D002, D004-D006 |
| 8 (P2) | Growth, revenue concentration, "very large revenues" | FIXED by removal | D007-D008, D009 |
| 9 (P2) | Ray listed as current | FIXED WITH NEW SOURCE [15] (KJZZ). "Died in January 2025" in §1, §7, §9, §19. Date left as "January": KJZZ says 4 January, other reports 3 January | D001, D010-D013, D016-D017 |
| 10 (P2) | §19 case 1 characterisations | FIXED. Now what [2] supports: three deaths, up to $10,000 paid; the page cites no record of training or safety arrangements. Record line changed from "Arizona court records" to the CNN verdict report | D014-D015 |
| 11 (P2) | NXIVM overstated | FIXED. "Convicted of racketeering and sex trafficking [3]"; stage 7 "convictions ... including racketeering that rested on branding". CNN was blocked to me; NXIVM charges rest on the existing DOJ source [3] and the fact-check log | D018-D019 |
| 12 (P2) | Herbalife and Goop as New Age evidence | FIXED by labelling in §6, §8, §9, §19 and loop 5: neither is a spiritual organization; Goop settled without admitting liability (read: Spokesman-Review 2018) | D045-D051 |
| 13 (P2) | Scorecard all N | FIXED. All six cells "?" | D052 |
| 14 (P2) | "No totals exist [1]" | FIXED. "This page cites no total for the market." | D053 |
| 15 (P2) | Grade bases | FIXED with item 4 (4, 7, 8, 11, 13 Cultural; 26 Cultural with a basis that says no financial-control case is cited) | D071-D084 |
| 16 (P2) | §15 ledger "Yes" | FIXED. "Reported by former members" | D054-D056 |
| 17 (P2) | §21 "from inside" | PARTLY FIXED. Sentence added saying only Edmondson is an insider; narration intro rewritten. The "Voices from inside" heading is a shared title and was left. Insider voices from the wider market DEFERRED: new research | D057, D096 |
| 18 (P2) | "Words used here" generalizations | FIXED by softening | D058-D059 |
| 19 (P2) | Loops 4 and 5 | FIXED. Loop 4 summary states that no conversion into leverage is recorded; loop 5 no longer calls affiliate labor unpaid. No text moved between cards; card titles left | D064-D065 |
| 20 (P2) | Case tags | FIXED. Case 1: 13, 26; case 3: 3 (the text supports 3; the item's "13, 26 and 3" was read as case 1 = 13, 26 and case 3 = 3) | D066-D067 |
| 21 (P3) | Spelling | DEFERRED. House style across volumes | |
| 22 (P3) | "$10K"/"$10K+"; NXIVM date ranges | DEFERRED. Each range is defensible for its purpose; needs a house decision | |
| 23 (P3) | "diaspora appropriation" | DEFERRED. Left as read; unclear wording needs an editorial decision | |
| 24 (P3) | Empty receipt cells | FIXED. Certification pyramids and Platforms and algorithms: PATTERN OBSERVED | D038-D039 |
| 25 (P3) | Ownership / The market fragment | FIXED with item 5 | D034 |
| 26 (P3) | Unsourced superlatives | FIXED. "Higher bar than most traditions", "no crueler doctrine", "no better immunity", "most complete victim-blaming instrument", "no one is responsible until someone is dead" | D037, D060-D063 |
| 27 (P3) | Peru / §22 coverage | DEFERRED. The Embassy page was not opened (search summaries only) and no Peruvian law was found; §22 coverage needs new research | |
| 28 (P3) | Techniques 1 and 2 duplicate bullets | DEFERRED. Wording of the analytic voice; not a factual error | |
| 29 (P3) | Shared-template narration | PARTLY FIXED (§1, §7, §21, q5). §9, §15, §20 intros left: house-style across volumes | D095-D096 |
| 30 (P3) | Help lines | FIXED. Faith to Faithless hours (Humanists UK page read); Recovering from Religion US/Canada, UK and Australia numbers and "tries to offer a 24-hour service" for chat (page read); RAINN "24 hours a day" (search summaries only, site refused access); ICSA "contact is through its website". Source 13 hours added | D003, D089-D092 |
| 12 of template | "Attributed to God" (stage 8, technique 30) | CHECKED, no change: both already say spirit, the universe or the higher self | |

Template leaks (brief step 9): stage 8 and technique 30 already name the tradition's own authority. §9 pipeline cards handled under item 1.

Meta: `checked:` and "Last checked" set to 2026-10-03 (D086, D087); §25 "Checked" date (D088); dated bullet at the top of §27 (D093).

## New sources
15 KJZZ, 6 Jan 2025, on Ray's death (read).

## New grade tally
Cultural 30, Taught 0, Documented 0 (grep of the 30 `**Evidence grade.**` chips; zero `(sourced)`). The §1 Evidence row matches ("None of the 30 techniques is sourced to a named document. All 30 are graded Cultural."). The tally is repeated nowhere else.

## Left on purpose / caveats
- Not verified by me: Raniere's appeal outcomes (Courthouse News refused access, not added); RAINN hours; the Embassy alert wording; the NXIVM associates' pleas.
- The Retreat and ceremony tourism card still says funds go to "offshore or personal accounts" and "the safety record ... hidden"; no source in the volume, but the brief limited card edits to the ones that do not fit the tradition.
- §9 table retreat row and §11 sentences such as "screening is often inadequate" remain unsourced beyond the Embassy alert.
- Front matter `version: v4` and `sites.json` not touched.
