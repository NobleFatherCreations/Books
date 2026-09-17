# Scenario Gap Audit — all 21 guides (v9, shipped 2026-09-17)

Live at `noblefathercreations.com/festival`, verified byte-identical to the
repo (md5 `9e55bb7963366b12a288861f16ceb802`, deploy `6aac5c9c4dba1b82032e3f83`).

**207 → 270 scenarios. ~94,900 → ~127,900 words. 63 new cards, 2–4 per guide,
no guide left out.**

## Method

Every existing card in all 21 guides was inventoried by section, hook and
archetype, then each guide was audited against what actually happens in that
category. New scenarios were written only where the gap was real — nothing was
added that restated a card already there.

## The headline finding

**The book was strong on interpersonal manipulation and thin on physical and
environmental risk.** That pattern held across almost every guide, and the
largest omissions were not subtle:

| Gap | Why it mattered |
|---|---|
| **Crowd crush** | The most lethal thing that happens at music events, and entirely absent. It is compressive asphyxia, not trampling, and the three actions that keep you alive are counterintuitive enough to need knowing in advance. |
| **The Monday drive home** | Missing from *both* S.A.F.E. and B.U.I.L.D., despite being the most dangerous hour of most people's weekend — sleep debt, residual impairment, and a microsleep the driver never experiences. |
| **Severe weather / evacuation** | A tent is not shelter from lightning, and the injuries happen in the converging crush at the main exit. |
| **Hearing damage** | The defining occupational injury of touring, permanent, and absent. |
| **Pediatric ingestion** | Edibles at a child's eye level, in a guide about family camping. |

## Per guide

| Guide | Was | New | Now | What was added |
|---|---|---|---|---|
| G.R.O.V.E. | 17 | 4 | 21 | The lift home; the walk back to the tent; the phone/charger leash; the already-vouched-for insider |
| B.A.S.S. | 16 | 3 | 19 | Male sexual victimization and its disclosure barrier; being recruited as muscle; the goad into a fight |
| R.A.V.E. | 14 | 3 | 17 | Ticket fraud at the gate; dead phone and lost group; campsite theft |
| P.R.I.D.E. | 12 | 2 | 14 | Trans searches, facilities, HRT and binding in heat; the discretion demand |
| A.C.C.E.S.S. | 10 | 3 | 13 | Service animal interference; being physically moved without consent; Deaf/HoH exclusion from audio-only safety announcements |
| S.O.B.E.R. | 6 | 3 | 9 | Accidental dosing; refusal fatigue in a rotation; prescription policing |
| R.O.O.T.S. | 5 | 3 | 8 | Appropriation worn around you; assumed to be the dealer; immigration status as leverage |
| K.I.N. | 4 | 3 | 7 | Edibles at child height; teenagers as a different job entirely; hearing, sun and the long day |
| F.L.O.W. | 8 | 3 | 11 | Partner-acro consent when you cannot object at four feet; crowd contact mid-set; unpaid fire bookings |
| C.R.E.A.T.E. | 13 | 3 | 16 | Generative style appropriation; solvents in a marquee; declining a brief without burning the circuit |
| L.E.N.S. | 5 | 3 | 8 | The photographer as the target; minors in frame; the subject who turns |
| H.E.A.L. | 6 | 3 | 9 | The client who targets the practitioner; a crisis arriving on the table; barter with no end point |
| S.O.U.N.D. | 15 | 3 | 18 | Hearing damage; gear theft on the road; promoter-supplied substances |
| M.A.R.K.E.T. | 15 | 3 | 18 | Payment fraud; weather loss and concentration risk; decisions made at hour twelve |
| H.O.L.D. | 14 | 3 | 17 | The volunteer dual role; after-shift pressure from whoever signs your hours; untrained restraint and positional asphyxia |
| B.U.I.L.D. | 6 | 3 | 9 | The drive home; strike phase; faked plant competence |
| C.A.R.E. | 7 | 3 | 10 | A death on shift; police at the tent door; the escalation threshold |
| L.E.A.D. | 8 | 3 | 11 | How to actually remove someone; a report between two members; camp money |
| E.V.E.N.T. | 7 | 3 | 10 | The report about the headliner you cannot replace; crowd density and show-stop authority; security contractor accountability |
| S.A.F.E. | 15 | 3 | 18 | Crowd crush; storms and evacuation; the Monday drive |
| H.O.M.E. | 4 | 3 | 7 | Unable to reach them; the partner rather than the parent; the substance conversation that does not close the door |

## Three cards worth flagging

**S.A.F.E. — "IF THE CROWD GETS TOO TIGHT."** The three actions are: arms up in
a guard to protect chest expansion, stay upright at all costs and never bend
down for anything, and move diagonally with the surges rather than against
them. All three are counterintuitive, which is exactly why they belong in a
book rather than in the moment.

**H.O.L.D. — "WHEN YOU HAVE TO PUT HANDS ON SOMEONE."** Positional asphyxia:
never face-down, never weight on a torso, and the person going quiet is the
warning rather than the reassurance. This is the highest-consequence thing an
untrained volunteer does, and the hi-vis creates an expectation the two-hour
briefing never met.

**E.V.E.N.T. — "THE REPORT IS ABOUT YOUR HEADLINER."** The decision that
defines an event. The cost of acting is concrete and immediate; the cost of not
acting is diffuse and deferred — and every event publicly destroyed by this was
destroyed by the cover-up rather than the incident.

## Tooling

`scripts/festie-add-batch.py` validates the fourteen-field card contract, the
acronym check letter and the guide's outline before writing anything, and
extends an outline when a scenario introduces a section the guide did not list.
It caught a stray key in one card and a check letter that did not exist in its
acronym.

## Verification

Checker at **0 errors** against 270 scenarios. Chromium at 375px and 1440px and
under reduced motion: 21 guide cards, no page errors, no horizontal overflow.
One new card from **each of the 21 guides** opened individually and confirmed
rendering its hook, clinical chip and Dark Reality block. Live bytes compared
against the repo after deploy.
