# Indigenous / Folk / Ancestral Religions — discrepancy fix log, 2026-10-03

Every change is a reversible entry (INDF-D001 to INDF-D099) in `content/sacred-divide/edits/indigenous.json`; set an entry's status to `rejected` to undo it. INDF-D060 is a narration edit; the other 98 are md edits. The prefix is INDF because IND-W/R/N/P/L/G ids already exist. After `scripts/sacred-divide-export-md.py` all 99 show `applied` in `logs/edits-status.json` (0 FAILED); `build_sections('indigenous')` ran and the narration edit applied. Rule followed: this volume covers many peoples, so claims that generalised across all of them were qualified, attributed to a named case (Canada, the US, Australia) or removed; nothing was invented to fill a gap.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1) | Grades 13-26; "(sourced)" on 2 and 30 | FIXED. Techniques 13-26 regraded Documented to Cultural with rewritten rationales (the external record is kept as context; the internal bullets have no case). 26 also regraded: its basis fits the external half only, and the page has no coercion case. "(sourced)" removed from 2, 13, 14, 17, 26, 30. §1 Evidence row rewritten | D001-D017 |
| 2 (P1) | Abuse by ceremonial figures stated as documented | FIXED by relabelling: "reported in some communities; this page cites no case; an allegation, not a finding"; receipt FORMER MEMBER TESTIMONY changed to PATTERN OBSERVED in §7 and §11; §10 card 3 and the §3 lede qualified. A named case DEFERRED (I4): new research | D019-D023 |
| 3 (P1) | Coercive patterns attributed to all Indigenous traditions | FIXED. §12 lede says the 30 entries are a framework for the group as a whole, not findings on a named people; §1 and §15 Leaving rows say "in some communities"; §11 arranged marriage and menstrual restriction recorded as unverified, not coercion by themselves; §7 Participation and technique 8 qualified | D018, D025-D028, D058 |
| 4 (P1) | "mass graves" in timeline | FIXED. "Potential unmarked graves identified since 2021, most not yet excavated"; also §3 objection | D034, D040, D045 |
| 5 (P1) | MMIWG source "external" | FIXED. Replaced with what the inquiry found [12] | D055 |
| 6 (P1) | FGM as an Indigenous-religion harm | FIXED. §6, §11, §16, §17 and the §17 narration say it is a social practice across religions and none, recorded only where defended as tradition [10] | D056-D060 |
| 7 (P1) | "only ones ... nearly exterminated" | FIXED. "Many Indigenous nations were targeted by the institutions of other religions ..." | D053 |
| 8 (P2) | "your traditions" / "almost everything" | PARTLY FIXED. §3 lede and objection now speak of Canada, the US and Australia. The second-person address elsewhere (§7 table, §23 questions) was left as direct address and carries no sweeping claim | D044-D045 |
| 9 (P2) | Potlatch/Sun Dance "by statute", "1883-1951" | FIXED WITH NEW SOURCES [18] [19]. Canada: Potlatch 1885-1951 and Sun Dance from 1895, by the Indian Act; US: 1883 Code never passed by Congress, ban dated to 1978 by NARF [5] (read). §5 timeline, card heading and text, §7, §8 | D035, D038-D039, D066-D068 |
| 10 (P2) | 3,200 wording; 4,037 | FIXED. "At least 3,200 recorded deaths ... include illness, not only abuse" in §5, §8 and source [1]; 4,037 deleted (unverifiable) | D040, D067, D096 |
| 11 (P2) | "$50 million paid" | FIXED. "provided more than $50 million in cash and in-kind contributions" | D072 |
| 12 (P2) | Boarding-school comparison | FIXED by deletion | D022 |
| 13 (P2) | "theft with incense" | FIXED. "None stated. Indigenous nations have denounced the sale of their ceremonies [8]" | D076-D077 |
| 14 (P2) | Ray: ruling versus characterization | FIXED. §5, §7, §9, §10, §19 say the court ruled on the deaths, not on appropriation | D037, D073-D074, D077, D091 |
| 15 (P2) | Lakota declaration "routinely ignored" | FIXED by replacement: the page cites no later reissue and no measure of effect (§5, §20) | D041-D042 |
| 16 (P2) | Anonymous councils and nation protocols | FIXED WITH NEW SOURCES [20] [21]: Indian Act status and band registration funding; the OCAP principles of the First Nations Information Governance Centre. §3, §7 (two rows), §20, §23 closing, loops 1 and 3. The page now says it cites no ceremony or safeguarding protocol | D046-D048, D051-D052, D054 |
| 17 (P2) | §20 "answer to the whole bind" vs §3 | FIXED. Both say the page names the bind and does not resolve it | D046, D048-D049 |
| 18 (P2) | "individuals were named" | FIXED in loop 6 summary and §14 | D080, D082 |
| 19 (P2) | "survived genocide" | FIXED to "cultural genocide" (§3, §15) | D084 |
| 20 (P2) | Unsourced timeline receipts, sterilization | FIXED by narrowing: global claim limited to the three sourced countries; forced sterilization removed (GAO 1976 and Senate sources not retrieved) | D033, D036 |
| 21 (P2) | "Several hundred million" | FIXED. §1, §4, §7 say the page cites no count and the figure depends on the definition | D030-D032 |
| 22 (P2) | Unsourced generalizations | FIXED (§7 Participation, technique 8) | D028-D029 |
| 23 (P2) | Grades of 3 and 4 | CONFIRMED, no change: Contested stands because the dispute is the page's own §3 objection and each entry's "strongest defense"; no counter-source exists on the page. Owner may prefer Cultural |  |
| 24 (P2) | Case tags | FIXED. TRC `13, 14, 24`; Ray `26`; papal apology keeps `30` but the case now says it is this codex's reading | D087-D089 |
| 25 (P2) | Motive accusation in §14 | FIXED by deletion of the accusation | D079 |
| 26 (P2) | Prediction as fact | FIXED. Labelled analysis (§14, loop 6 step 4) | D081, D083 |
| 27 (P2) | 973 deaths at 417 schools | FIXED in §8 and §19 | D069-D070 |
| 28 (P2) | Witchcraft "imported element the driver" | FIXED. UNICEF's cultural, social, economic and political causes, not ranked [11] (§11, §16, §17) | D061-D064 |
| 29 (P2) | News reports used as records | PARTLY FIXED. [9] now https; §19 record line says it is CNN's report; KJZZ added as [22]. Primary documents (Arizona v. Ray docket, CBC pledge records) DEFERRED: not found | D090, D097 |
| 30 (P2) | UN Declaration bullet in §4 | KEPT: it is supported by source [7]; no edit |  |
| 31 (P3) | Spelling | DEFERRED. House style across volumes |  |
| 32 (P3) | Composite label in §2 | FIXED | D024 |
| 33 (P3) | "Retrieval is a ceremony" | FIXED | D085 |
| 34 (P3) | "more power than any bishop" | FIXED | D086 |
| 35 (P3) | School dates | FIXED. Canada from the 1830s; US report 1819-1969; Australia missions and children's homes | D034, D075 |
| 36 (P3) | "applies everywhere" | FIXED | D065 |
| 37 (P3) | §21 has no internal critic | DEFERRED. New research (I12) |  |
| 38 (P3) | Version v5 and sites.json | DEFERRED. Outside this task; front matter `version: v4` and `sites.json` not touched |  |
| 39 (P3) | "frauds selling ceremony" | FIXED | D071 |
| Help | StrongHearts hours; missing residential-school line | StrongHearts "24/7 by call or text" FIXED; §25 check date 2026-10-03. The National Indian Residential School Crisis Line (1-866-925-4419) was NOT added: confirmed only from third-party listings, not the federal page. 988 and 9-8-8 not verified | D092-D093 |

The Edits column is derived from each entry's `reason`, which names the item number.

Template leaks (brief step 9): stage 8 and technique 30 already name the ancestors, the spirits and tradition; no change. The §9 "Retreat and ceremony tourism" card fits this volume and was kept.

Meta: `checked:`, "Last checked" row and §25 date set to 2026-10-03; dated bullet at the top of §27 (D093-D095, patch note D099).

## New sources
18 The Canadian Encyclopedia, Potlatch Ban (dates confirmed via search summary; page body did not load). 19 Gladue Centre, University of Saskatchewan (Sun Dance, 1895; search summary). 20 Indigenous Services Canada, registration administration (search summary). 21 First Nations Information Governance Centre, OCAP (page returned 403; read through search summaries). 22 KJZZ, 6 Jan 2025 (from the fact-check log).

## New grade tally
Cultural 27, Contested 3, Documented 0 (grep of the 30 chips; zero `(sourced)`). The §1 Evidence row matches ("None of the 30 techniques is sourced to a named document"). The tally is repeated nowhere else.

## Caveats
- NARF [5] was read: it says Congress never passed the Code and dates the ban 1883 to 1978. The 1934 policy change (item F12) was not verified and is not stated.
- The §15 ledger still shows "Documented? Yes" for identity and misfortune attribution without a source; not on the discrepancy list, left.
- "Money in one line" and the §9 retreat row keep their INVESTIGATIVE REPORT receipts without a named source.
