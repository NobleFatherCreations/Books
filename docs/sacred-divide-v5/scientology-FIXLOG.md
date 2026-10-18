# Scientology — discrepancy fix log, 2026-10-03

Every change is a reversible entry (SCIF-D001 to SCIF-D167) in `content/sacred-divide/edits/scientology.json`; set an entry's status to `rejected` to undo it. SCIF-D148 to D159 are narration edits; the other 155 are md edits. All md edits show `applied` in `logs/edits-status.json` (no FAILED). Narration edits were checked through `foryou()`, `intro()`, `questions()` and `sacred_divide_edits.check()` (all applied once each, including the earlier SCI-N entries). `build_sections('scientology')` was not run: the Python `markdown` module is missing and was not installed, as instructed. The prefix is SCIF because SCI-W/G/P/R/L/N/C ids already exist. Ten sources, [18] to [27], were added at the end of §26. Rule followed throughout: where a source supports a claim it is kept (the convictions, the 2,200 suits, the $12.5 million, Masterson's conviction and sentence, the French fraud conviction); where it does not, the claim is attributed, qualified, or removed.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | "Everything comes from policies and court records" | FIXED. Lede and "strongest objection" answer now say the page rests on court records, policies, reporting and former members' accounts, and that receipts say which | D001-D002 |
| 2 (P1) | "Published" prices / price lists | FIXED WITH NEW SOURCE [25] (*Hernandez v. Commissioner*, 1989: the church charges "fixed donations", "set forth in schedules"). Now "fixed donations set out in schedules; former members describe them escalating into six figures". §7 row, §9 card and flow, §10 card, §12 stage 6, techniques 2, 3, 26, §14 | D010, D017-D020, D027-D029, D091, D167 |
| 3 (P1) | Snow White superlative (six places) | FIXED. Ranking cut; the 1979 convictions kept, now with charges as the court record gives them and new source [26] | D030-D034, D158 |
| 4 (P1) | Exemption placed in Snow White's outcome | FIXED. §19 outcome ends "Convictions and prison sentences."; §20 cell is "The convicted officials served prison sentences" | D035-D036 |
| 5 (P1) | "Proof of what the policy authorizes" | FIXED. "The convictions show what eleven senior officials did" | D031-D032 |
| 6 (P1) | "Reviewable administrative decision" | FIXED WITH NEW SOURCE [18] (26 U.S.C. §7121: final and conclusive unless fraud, malfeasance or misrepresentation). §5 card, §8, §22 regulator and tell | D038-D041 |
| 7 (P1) | Private investigation attributed to church disclosures and court records | FIXED. Now "as the New York Times reported in 1997, private detectives investigating agency personnel [2]". Related "documented" investigator claims in §10, §11, §14, §15 split by receipt | D011, D037, D050-D052 |
| 8 (P1) | "Litigation pressure rather than ordinary review"; "taxpayers subsidize" | FIXED. Replaced with what [2] reports (closing agreement after about 2,200 suits). "Subsidize" and "discloses nothing" removed. Loop 4 steps and summary rewritten to match (item 46) | D042-D049 |
| 9 (P1) | Motive ("rebranded as religion", "fee structure from the first year") | FIXED. Dates from [9] (Dianetics 1950, first church 1954); motive claims now "critics argue" | D020-D026 |
| 10 (P1) | Masterson appeal "pending in 2026" on a 2023 source | FIXED WITH NEW SOURCE [21] (Tony Ortega, 17 May 2026: set for oral argument 25 June 2026). Stated as "set for oral argument; this page records no ruling" because the argument and the absence of a ruling by 3 Oct were not opened by me. §8, §19, §21, §24, source 5 note | D053, D056-D059 |
| 11 (P1) | Masterson tags 30, 16, 17; church conduct implied | FIXED. Tags dropped (shown as "—"); card says the accusers' allegations about the church are the subject of a separate civil suit with no finding | D053 |
| 12 (P1) | Disconnection stated as fact with [OFFICIAL POLICY], no letter cited | FIXED WITH NEW SOURCE [27]. "According to the founder's policy letters as quoted by former members and in reporting [10], members are required to cut contact...; the church says disconnection is voluntary [27]". §1, §3 (both tables), §10, §14, §15 (bullet, ledger, "how the cost is denied"), §16, §17, techniques 10, 15, stage 7, narration cost, q1. [27] is a critic's blog summarising the church's position; it was reached through a search summary, not opened | D003-D006, D013-D016, D078-D079, D093, D126, D128, D148, D152-D153 |
| 13 (P1) | Sea Org "monastic orders do not bill"; "indenture" | FIXED. Absolute and legal characterisation removed; now "former staff describe...; this page cites no response from the church". Related "only exit fee in this codex" cut | D092, D094, D119-D120 |
| 14 (P1) | "Fair game" receipt with no court record; church position missing | FIXED WITH NEW SOURCES [19] (HCOPL 21 Oct 1968, church's reading) and [20] (*Rathbun*, Texas 2015, ABA Journal). Timeline 1960s and 1995-2000s rows, technique 17 (Documented kept: it now names Rathbun), §15 ledger and denial table | D008, D014, D064-D066 |
| 15 (P1) | Unsourced quotations in the church's voice | FIXED. Quotation marks removed; positions paraphrased and tied to [27] or marked "not cited on this page"; a note under the §14 table says the first column is a paraphrase | D003-D004, D007-D009, D011-D012 |
| 16 (P1) | Front organizations "with the affiliation omitted" | FIXED. Qualified to "some programmes have been alleged to operate without naming their link; this page names no report" (receipt [PATTERN OBSERVED]). §6 text unchanged (it already only links the programmes). §7, §9 card, §16, §18 | D098-D101 |
| 17 (P1) | §11 allegations stated as findings | FIXED. Attributed to former members and the *Bixler* allegations; "no finding" stated. Police-report bullet no longer carries [COURT RECORD] | D121-D122, D125 |
| 18 (P1) | Germany: labour-law basis, out-of-date monitoring | FIXED WITH NEW SOURCES [22], [23]. Federal Labour Court (1995) in labour law only; federal observation ended 15 May 2026; Bavaria continues. [23] not opened (reached via the fact-check log). Employment-law restriction claim removed (no source). §8 row, §22 card | D129-D132 |
| 19 (P1) | "No refund route", "unrefunded" | FIXED. "Former members say they could not recover advance payments" | D007, D127 |
| 20 (P1) | Grade bases | FIXED. See tally below. Regraded to Contested (reports rather than written policy or court records): 4, 8, 12, 18, 20, 22, 26, 27, 29. 11 moved Documented to Codified (Snow White does not show the labelling of critics). 19 and 25 trimmed to their codified element. 2, 3, 9, 16 kept Codified with notes rewritten. 6 and 7 kept Codified (the entry's own basis is written policy). 17 kept Documented and now names *Rathbun* | D027-D029, D066-D088, D147 |
| 21 (P2) | "Tens of thousands worldwide" | FIXED. "No audited worldwide figure is cited on this page"; "one of the largest claim/reality gaps" removed. §1, §4, §7. "Hundreds of thousands of dollars" also attributed to former members' estimates | D108, D110, D112, D151 |
| 22 (P2) | Australia 2016 only | FIXED WITH NEW SOURCE [24] ("1,655 in 2021"; Tony Ortega, 2022, not opened by me, via the fact-check log). §1, §6, §7 | D109 |
| 23 (P2) | "Thirty-eight years", "forty years" | FIXED. Thirty-nine; "forty years" now "since 1987" | D113-D114 |
| 24 (P2) | "Everyone counted is inside the fee structure" | FIXED | D111 |
| 25 (P2) | CSI row "RTC chooses / RTC can remove" | FIXED by qualifying: "Not recorded on this page" (no source found) | D107 |
| 26 (P2) | Defections 2009-2015 vs Rinder 2007 | FIXED. "2007-2015" and "2007-present" | D116-D117 |
| 27 (P2) | France: allegation phrasing beside a conviction | PARTLY FIXED. Now "The court found... guilty of organised fraud for preying financially on followers" (SBS read). Individuals' two-year suspended sentences and €30,000 fines DEFERRED: the cited SBS page does not state them and I did not verify them | D062-D063, D159 |
| 28 (P2) | Supreme Court denial attributed to *Garcia* | FIXED, not extended. The cited Horvitz & Levy page records only the California Supreme Court denial (20 Apr 2022); the US Supreme Court cert denial is not on any page I read, so it is no longer asserted. Source 3 and the §19 outcome corrected | D055, D061 |
| 29 (P2) | Case tags | FIXED. Snow White 17; Masterson none; *Bixler/Garcia* 18 | D054, D055 |
| 30 (P2) | Blank receipts (CST, Author Services) | FIXED by qualifying ("this page cites no source for its holdings"). No source found | D105-D106 |
| 31 (P2) | §9 pipeline cards 1, 4, 5 | FIXED. Rewritten around what §7, §9 and §16 record; card 2 and 3 also corrected | D018, D099, D102-D104 |
| 32 (P2) | Male-dominated leadership; Hubbard on homosexuality | FIXED by removal (no source; a sourced version needs new research) | D123-D124 |
| 33 (P2) | Stage 5 "no outside income..." and stage 8 "new recruit takes your slot" | FIXED. First attributed to former members, second removed; loops 3 and 5 steps matched | D089-D090, D095-D097 |
| 34 (P2) | "There will be no removal" | FIXED | D114-D115 |
| 35 (P2) | Independent field "without disconnection..." | FIXED. States that no source is cited | D135 |
| 36 (P2) | §26 sources | PARTLY FIXED. [1] dead link flagged and pointed to [26]; [3] and [5] corrected; ten sources added. DEFERRED: replacing [6]-[8] (Wikipedia, critics' blogs) with the ONS, ABS, Bavarian/federal reports and the Labour Court decision; page numbers for [10] — needs new research | D059, D061, D142-D143 |
| 37 (P2) | Help lines | PARTLY FIXED, as in the Baháʼí log. Faith to Faithless hours added (Wed 10:00-13:00, Thu 16:00-19:00, Fri 08:00-11:00, from the Humanists UK page via the fact-check log); Recovering from Religion "tries to offer a 24-hour chat and call service" and UK/Australia numbers (as printed in the Baháʼí volume, not re-checked here); RAINN "free, confidential, 24 hours a day" (search result, page returned 403); ICSA "Contact is through its website". "Checked" date set. Whether Recovering from Religion covers Canada is not established and is left | D136-D141 |
| 38 (P2) | §4 "healthy" section thin | DEFERRED. Needs new research (proposal S11) the owner has not asked for | |
| 39 (P2) | Narration q1 and q4 | FIXED. Also q2, q3, q5, q6 examples matched to the corrected text | D152-D159 |
| 40 (P2) | "How it shows here" bullets assert practice as fact | DEFERRED, in part. The grade notes and the stage and §11 claims are attributed; the ~120 per-technique bullets are the volume's analytic voice and need a house-style decision across volumes | D076 only |
| 41 (P3) | Spelling | DEFERRED. House style, decide once for all volumes | |
| 42 (P3) | "Two decades of litigation" | FIXED | D118 |
| 43 (P3) | Duplicate bullets, techniques 2 and 3 | FIXED | D133-D134 |
| 44 (P3) | Aphoristic closers | DEFERRED. House style (stage-8 "That is not a limitation... it is the reason it works" etc. are the volume's argument voice). Stage 6 and 7 closers were rewritten only where they stated an allegation as fact | D092, D094 |
| 45 (P3) | "This codex" | DEFERRED. House style across volumes | |
| 46 (P3) | Loop 4 summary | FIXED (summary and steps 3 and "why it closes"); no text moved between cards | D047-D049 |
| 47 (P3) | Composite "man who signed at seventeen" | FIXED in the narration; loop 3 already says the day inside is a composite | D149 |
| 48 (P3) | §20 row 2 belongs to a different question | NO CHANGE to the row's structure; its cost cell is now accurate (D036) | D036 |
| 49 (P3) | Safeguarding scorecard cell | DEFERRED. Needs research on whether the church publishes a safeguarding policy | |
| 50 (P3) | Template leaks | CHECKED, no change. "Attributed to God" is not present: stage 8 and technique 30 already name Hubbard's writings (SCI-P003, SCI-P004). Pipeline card 1 "congregation" fixed under item 31. No build-marker text found | |

Meta: `checked:` and "Last checked" set to 2026-10-03 (D144, D145); dated bullet at the top of §27 (D146); cite lists D160-D166.

## New sources
18 26 U.S.C. §7121 (Cornell LII; read). 19 Wikipedia, Fair game (Scientology) (read; quotes HCOPL 21 Oct 1968). 20 ABA Journal, Rathbun (read). 21 Tony Ortega, 17 May 2026 (read). 22 Handelsblatt, 15 May 2026 (read). 23 evangelisch.de, 16 May 2026 (not opened). 24 Tony Ortega, 1 July 2022 (not opened). 25 *Hernandez v. Commissioner*, 490 U.S. 680 (read, FindLaw). 26 Wikipedia, Operation Snow White (read, convictions only). 27 Mike Rinder's blog (not opened; search summary only).

## New grade tally
Codified 20, Documented 1, Contested 9, Taught 0, Cultural 0 (grep of the 30 `**Evidence grade.**` chips; zero `(sourced)`). The §1 Evidence row matches ("None of the 30 techniques is sourced to a named document"). The tally is repeated nowhere else.

## Left on purpose / caveats
- Not verified by me: the individuals' sentences in the French case; the US Supreme Court cert denial in *Bixler* (not asserted); whether the Masterson appeal was decided after 25 June 2026; the Bavarian continuation (source 23); the 2021 Australian count (source 24); the church's position on disconnection (source 27 is a critic's summary); church statements on refunds, donations and the 1968 label (only the 1968 letter and its dispute are sourced, via Wikipedia).
- Source 26 and 19 are Wikipedia; both are labelled as such and used only for the facts quoted above.
- "Fixed donations" and "set forth in schedules" are from a 1989 opinion describing 1972 practice; the page does not say the figures are current, and "published" is not asserted anywhere.
- Spelling and "organization/organisation" mix left as found in the new text, following the local spelling of each passage.
- Front matter `version: v4` and `sites.json` not touched (outside this task).
