# Catholicism — discrepancy fix log, 2026-10-03

Every change below is a reversible entry (CATH-D001 to CATH-D047) in `content/sacred-divide/edits/catholicism.json`; set an entry's status to `rejected` to undo it. All 47 apply (none FAILED); the two narration edits (D009, D016) apply in `build_sections('catholicism')`. Items are numbered as in `docs/sacred-divide-v5/DISCREPANCIES.md` (copied to `discrepancies/catholicism.md`); H-numbers are from `hostile-review/catholicism.md`.

| # | Item | Resolution | Edits |
|---|---|---|---|
| 1 (P1), H1 | Thesis question had a counter-example (Cardinal Law, 2002) | FIXED WITH NEW SOURCE. Question now reads "Cardinal Law resigned in 2002 under public pressure [44]. Which bishop has ever been removed by Rome, under a published rule, for keeping the files sealed?" in §1 and §3; §23 question 2 and its narration, and Loop 6 step 4, brought into line. §20 already speaks only of "a bishop actually removed under" a rule, so it needed no change | D001, D003–D005, D008–D010 |
| 2 (P1), H2 | "Rome removed not one bishop" | FIXED WITH NEW SOURCE. §14 now records Law's resignation [44], the 2021 sanctions on two Polish bishops who had already resigned [45], and says only that no removal from office for the transferring is recorded on the page | D001, D006, D007 |
| 3 (P1), H3 | "44 dioceses and orders in bankruptcy" | FIXED. §8, §9, §22 and source [11] now say 44 have filed, 15 cases pending (Penn State, March 2026, re-read). "Since 2004" from the proposal was left out: the page does not state it | D002, D011–D013 |
| 4 (P1), H4, H14 | "Four national inquiries … and the United States" | FIXED. Australia, France and Ireland national inquiries plus US state grand juries, in the §3 and §14 say-do rows, the §17 table and the §17 narration | D014–D016 |
| 5 (P1), H5 | Philippines annulment row | FIXED WITH NEW SOURCE [43]. Civil annulment or declaration of nullity is the legal route; a church annulment has no civil effect | D017 |
| 6 (P1), H6 | Grades stronger than entries | FIXED. 8, 9, 13 Documented→Codified; 10 Documented→Cultural (rationale rewritten); 16 and 29 Codified→Cultural (16 rewritten); 17 Codified→Documented (cites [13][14][15]). *(sourced)* removed from 12, 19, 22, 25, 26, 28, 30 (no named document); canon 1024 [1] now named in 15 and 23, the Index [25] in 14, the inquiries [13][14][15] in 18 | D018–D036 |
| 8 (P2) | Church-tax case tagged 2, 26 | FIXED. Tag 2 removed (Weaponized Generosity does not fit a tax case); 26 stays | D037 |
| 9 (P2), H7 | Celibacy "every abuse inquiry" | FIXED WITH NEW SOURCE [47]. Now: Australia's Royal Commission found compulsory celibacy had contributed to abuse when combined with other risk factors and asked the Holy See to consider voluntary celibacy for diocesan clergy [14]; the John Jay study for the US bishops found it was not a cause [47] | D038, D039 |
| 10 (P2), H8 | "Lifetime tenure" | FIXED WITH NEW SOURCE [46]. Diocesan bishops are asked to offer resignation at 75 (can. 401 §1, text read on vatican.va) | D040, D041 |
| 11 (P2) | Grade notes vs chips | Resolved by item 6 | D018–D024 |
| 14 (P3) | NAPAC hours | FIXED. Mon–Thu 10am–9pm, Fri 10am–6pm, closed weekends (napac.org.uk, read 2026-10-03) | D042 |
| F16 (outside the list) | "roughly 80 million Catholics" in §22 | FIXED WITH NEW SOURCE [48]. PSA 2020 census: 85.6 million, 78.8%; now "roughly 86 million" | D043, D044 |
| H9 | Chiclayo complaint omitted | DEFERRED. Adding it is new content (expansion proposal E2): it needs a CONTESTED-grade entry with the diocese's published response, which has not been researched | — |
| H12 | Becciu status in §23 and pull-quotes | No change to the page: §23 question 3 makes no claim the March 2026 ruling affects. See "For the owner" below on pull-quotes | — |
| H13 | "Stronger than the laws of the Republic" and the later apology | DEFERRED. Could not verify the apology in this pass; nothing asserted | — |
| 7, 12, 13, 15, 16 | Template, build-script, other-volume and house-style items | DEFERRED. Each needs a decision across volumes or build work outside this volume's files | — |

Meta: `checked:` and "Last checked" set to 2026-10-03; dated bullet added at the top of §27 (D045–D047).

## New sources (end of §26)
43 Respicio & Co. on church annulment and civil effect (Philippines) · 44 CNN, Law's resignation, 13 Dec 2002 · 45 Catholic World Report, Polish bishops sanctioned, 29 Mar 2021 · 46 Code of Canon Law can. 401 §1 · 47 John Jay College, *Causes and Context* (2011) · 48 Philippine Statistics Authority, 2020 census religious affiliation. Source [11] was re-worded in place (no renumbering).

## New grade tally
Codified 18, Documented 6, Cultural 5, Reformed 1 (total 30; counted by grep from the §12 chips). Techniques sourced to a named document: 4 (14, 15, 18, 23). The §1 Evidence row matches; no other place on the page repeats the tally.

## For the owner
- **Pull-quotes will now be stale.** `scripts/sacred-divide-pdf-v5.py` (lines 113 and 124) holds Catholicism's pull-quotes inside the script, and they quote the old thesis question and "not one bishop removed by Rome". I did not touch `scripts/`. They need replacing before the PDF is rebuilt (`scripts/sacred-divide-pdf-abdurahman.py` line 170 also paraphrases the old question).
- The thesis question is now a negative claim about the whole Church. Vos estis has been in force since 2019 and I found no removal under it, but I could not prove the negative; the §14 sentence is therefore worded "no bishop is recorded on this page".
- Not in the list, left unchanged: the §10 secrecy card still says "Every inquiry reached that conclusion independently", which is the same kind of overstatement as item 9, and §10's annulment card says the tribunal "performs no legal function", which may not hold in every country (some concordats give church annulments civil recognition); neither was checked. Both are candidates for the next round.
- Claims marked NOT CHECKED in `logs/fact-check/catholicism.md` (F17, F18) were not re-read.
- The Catholic World Report page returned a server error when fetched; the sanctions and the 2020 resignations were confirmed through several other outlets' reports of the same decision (Crux, CatholicPhilly, Notes from Poland), and the CNN page was blocked (HTTP 451), so Law's resignation was confirmed through search results quoting it.
