# DISCREPANCIES — awaiting the owner's decision

Format: **[Location]** what is wrong → what it should be → why it matters. Nothing below has been changed in the text.
Errors (something is wrong) and omissions (something is missing) are kept apart: omissions are in `expansion-proposals.md` and `gaps-unfilled.md`.
Evidence for each Catholicism item is in `logs/fact-check/catholicism.md` (F-numbers).

## P1 · Critical (factually exposed, or breaks the codex's own rules)

0. **[26 volumes, §25 and §26 — APPLIED, needs sign-off]** Faith to Faithless listed as 020 3675 0959 → the helpline is freephone **0800 448 0748**, open on set days only (Humanists UK, checked 2026-09-29) → a wrong help-line number in the section people use in a crisis. Because of the real-world risk, this one correction has been applied (edits ALL-F01, ALL-F02); reject it in `_all.json` if you disagree. Opening hours differ between Humanists UK pages, so the text says "set hours, see website" rather than stating them.

1. **[Catholicism §1, §3, §20 — the thesis question]** "Who above the rank of bishop has ever lost office for keeping them sealed?" → Cardinal Law resigned as Archbishop of Boston in 2002 over his cover-up, and the pope accepted it (F5). Proposed wording: "Cardinal Law resigned in 2002 under public pressure. Which bishop has ever been removed by Rome, under a published rule, for keeping the files sealed?" → The volume's central question currently has a known counter-example, which a hostile reader will use to dismiss the whole page.
2. **[Catholicism §14]** "Rome removed not one bishop for having done the transferring" → in 2021 the Holy See sanctioned two Polish bishops after Vos estis inquiries, though both had already resigned (F6). Proposed: "Rome has sanctioned bishops after they resigned, but has removed none from office for the transferring itself." → The claim is defensible only in its narrowest reading.
3. **[Catholicism §8, §9]** "44 dioceses and orders in bankruptcy" / "US dioceses in bankruptcy: 44" → 44 dioceses and religious organisations have *filed* since 2004; 15 cases are pending (F2). Proposed §9: "US dioceses and religious orders that have filed for bankruptcy since 2004: 44 as of March 2026 (15 still pending) [11]." Match §8 and §22 to it. → The same figure appears three ways in one volume, and two of them overstate.
4. **[Catholicism §17 table, §17 narration, §3 table]** "four national inquiries (Australia, France, Ireland and the United States)" → the volume's own §22 says the US had no federal inquiry (F7). Proposed: "national inquiries in Australia, France and Ireland, and state grand juries in the United States". → Internal contradiction on the volume's heaviest finding.
5. **[Catholicism §8 Philippines]** "Annulment through church tribunals is the main route out of a marriage" → a church annulment has no civil effect; the legal route is a civil annulment or declaration of nullity (F8). Proposed: "With no divorce law, the legal route out of a marriage is a civil annulment or declaration of nullity; a church annulment is needed to remarry in church but has no civil effect [23]." → Real-world consequence for a Filipino reader relying on this row.
6. **[Catholicism §12 — evidence-weighting rule]** The grades on these techniques are stronger or different from what their entries support once each carries its own rationale (grades unchanged; rationales corrected under CATH-R-edits):
   - 8 Intermittent Reinforcement, 9 Moving the Goalposts, 10 Strategic Ambiguity, 13 Normalization — graded **Documented**, but what each rests on is published teaching (points to **Codified**) or observed practice (points to **Cultural**); no inquiry documents the pattern itself.
   - 16 Flying Monkeys, 29 Replacement — graded **Codified**, but the behaviour is community practice with no written rule (points to **Cultural**).
   - 17 Smear Campaign — graded **Codified**, but its basis is inquiry findings (points to **Documented**).
   The §1 tally (Codified 18, Documented 9, Cultural 2, Reformed 1) changes with any regrade.

## Per-volume discrepancy files
Eastern Orthodoxy: `discrepancies/eastern-orthodoxy.md` (P1 4, P2 9, P3 7). Headline items: Pew's ~260 million includes Oriental Orthodoxy (Eastern alone ~208 million); Georgia's Ilia II died in March 2026 and Shio III was elected in May; the EU dropped Kirill from its 21st sanctions package in July 2026; four technique grades stronger than their basis.

## P2 · Structural (inconsistent, incomplete, or weakens comparison)

7. **[25 of 34 volumes, §12]** One grade rationale reused under several different techniques (544 techniques in total). Catholicism is corrected in this round (CATH-R002 … R029); the other 24 volumes need the same pass. This is a template-level flaw.
8. **[Catholicism §19]** The church-tax case lists `tactics: 2, 26`. Technique 2 (Weaponized Generosity) does not fit a tax case; 26 Financial Control does. Decide whether 2 should be removed or another number was meant.
9. **[Catholicism §10]** Celibacy "a configuration every abuse inquiry identified as an accountability risk" — "every" is not shown by the cited reports (F14).
10. **[Catholicism §16]** "lifetime tenure" — bishops must offer resignation at 75 (F15).
11. **[Catholicism §12 grade notes for 8, 9, 10, 13]** Now state a written-rule basis under a Documented chip. Visible to a careful reader until item 6 is decided.
12. **[Site and PDF build]** The v5 PDF script still carries its own copy of the Loop 2 text; loops now live in the Markdown source (CATH-L001–L008). Remove the copy when design work resumes.
13. **[ahmadiyya, anglicanism §12]** Techniques are a single table ("Mechanism / Grade / How it appears here …") while the other 32 volumes use one card per technique. A comparator blocker.

## P3 · Refinement

14. **[Catholicism §25]** Recovering from Religion also serves Canada; NAPAC is not 24/7 (the table does not claim it is). Optional: add hours.
15. **[All volumes, spelling]** American spelling dominates, with British forms in places (programme, enrolment, secularisation). The PDF is tagged en-GB. Choose one house spelling.
16. **[Narration templates]** Several captions end on an aphoristic line ("the response is information", "tells you more than the answer does"). This matches the house voice and has been left alone; flag if you want them plainer.

## Corrections to earlier notes
- The "ligature glyph" defect reported earlier does not exist (a locale artefact of `grep`).
- "Error 2" (11 vs 12 sourced techniques) is not reproducible; 11 is correct.
