# Steelman round 1 (2026-11-23): steelman and fact check of the v5 rewrite

Scope: all 15 files (`00-start.md` to `07-tools.md`, about 109,000 words, 68 chapters) after the v5 writing pass. Read file by file in reading order, against `V5-WRITING-BRIEF.md`, `CHAPTER-DESIGN.md` and `FACTS-TO-CHECK.md`. Each file was committed on its own. A second cross-book pass then fixed repetition that only showed up across files.

Checks after the last edit: `rewrite-check.py` shows 0 problems on every file against its previous commit, and fences are balanced. `readability.py --book scale`: 0 paragraphs over 90 words, 0 chapters over their grade limit. One expected check flag: compared with the pre-steelman state, `03-iii-a` (one-thing-is-not-a-pattern) changed one Sources line, the Danger Assessment URL (.com to .org). That was a deliberate correction.

## Fix counts

| Type | Count |
|---|---|
| Accuracy (corrected, softened or sourced) | 12 |
| Safety (danger lists made consistent, counter-lines) | 5 |
| Repetition (gags, images, character names) | 27 |
| Search cannibalisation (headings, FAQ) | 2 headings + 38 FAQ answers |
| Contradictions and steelman gaps | 3 |
| Decoder close-match link text | 4 |

## Per file

**00-start.** Safety: the opening danger warn left out "a child is at risk" and only said "made leaving dangerous". It now lists Rule three's five conditions.

**01-i-a.** Safety: the danger branch of the two-errors tree ("violence, a threat, or you're physically afraid") now covers all of Rule three's conditions. Repetition: "it will find them in the cat" was the second "detector finds manipulation in X" gag in the file (after the dentist one). Rewritten. Confirmed: Nesse 2019, Kahneman and Tversky 1973 (Tom W.).

**01-i-b.** Accuracy: the text said Johnson (1995) found the central difference was "motivation". It now says what the paper argues: whether violence is part of a wider effort to control. Confirmed: Stark's "liberty crime" and "little or no physical violence". Repetition (cross-book pass): "Ama's group chat runs on red flags" was the fourth group-chat-verdict gag. Varied.

**02-ii-a.** Repetition: the biases field guide repeated the Arntz 1995 paragraph from gut-feeling-or-anxiety almost word for word. It's now a pointer. Cross-book: a "nobody has ever found peace…" kicker rewritten. Confirmed: Ross 1977 DOI, Nisbett and Wilson 1977, Dodge 1980, Downey and Feldman's quote, Kunda, Baumeister, Doron 2014, DSM-5 criterion E.

**02-ii-b.** Accuracy: MacCormack and Lindquist found the hunger effect *only* after an unpleasant image, not "mainly". Corrected. Confirmed: Yoo 2007 (35 hours, over 60%), van der Helm 2010, Stroebe 2007, Stroebe and Schut 1999, Gottman's 69%. Repetition: "even the dog looks complicit" came right after the ex's-dog gag in the previous chapter, and "a true-crime podcast" repeated chapter 1's image. Both rewritten, plus a "nobody has ever" kicker.

**03-iii-a.** Accuracy: the Danger Assessment URL is dangerassessment.org (the book printed .com). The memory-rebuild line was softened. Confirmed: DA item 1 wording, Lord, Ross and Lepper, Snyder and Swann, Nickerson, Hirt and Markman. Steelman: the evidence-ladder warn now says that having no record doesn't make what you saw count for less.

**03-iii-b.** Accuracy: the fidgeting line overstated DePaulo 2003 ("no clear relationship") and now matches it. Confirmed: Bond and DePaulo (206 studies, 54%, 61/47), Global Deception Research Team (75 countries, 43 languages), Wiseman 2012, Vrij 2008/2009, Park 2002, Serota 2010, Hancock 2004, Hancock 2009 (6,996 messages, a tenth were lies, a fifth of those were butler lies), Kruger 2005. Cross-book: "a tactic wearing its clothes" varied.

**03-iii-c.** Repetition: the Bartlett 1932 paragraph appeared twice in this file. The second one is now a pointer. Confirmed: Loftus and Palmer (32% vs 14%), Talarico and Rubin, Köbis 2021, Chesney and Citron, Echterhoff 2005, Rathje 2021.

**04-iv-a** (contains a heavy chapter). Safety: the safety gate had no line for Rule three's "cut off from people who could help / leaving made difficult". Both the line and its explanation are added. Repetition: "In the whole history of relationships… has never once" and "silent treatment in its everyday clothes" rewritten. Confirmed: Campbell 2003, Lewicki 2016 DOI.

**04-iv-b.** Accuracy: Swan and Snow's "largest group" was described more precisely than the study supports. Softened. Repetition: the character name Tamsin was used in two different scenes (03-iii-c, 04-iv-b). Renamed to Bronwen. "In a new font" was repeated from the grief letter and is now "new letterhead". Confirmed: Keltner 2003, Milton 2012, Smith and Freyd 2014, the Hotline's position.

**04-iv-c.** Accuracy: the scholarly objection to BITE is now sourced (Barker 1984, *The Making of a Moonie*). Repetition: "like a horoscope with your name typed in" repeated the horoscope gag (03-iii-b) and is now "mail merge". "According to the short-video economy" was used word for word in 01-i-b and has been varied. Confirmed: Hall 2019, Tepper 2000, FTC on MLMs.

**05-v.** Cannibalisation: "Is getting defensive a sign of guilt?" is now "Does getting defensive make me look guilty?" (the accused's angle, a different search). "Am I the toxic one, or the victim?" is now "What if I'm both the one hurting and the one hurt?" Contradiction: the opener said "for forty-three chapters every tool… pointed outward", which contradicted Movement II (the instrument is you). Reworded. Repetition: the "in the whole history of boxing" kicker and "your group chat met him twice" (third "met him twice") were varied. Confirmed: Pronin and Kugler, Haslam 2016, Sunstein 2002.

**06-vi-a.** Accuracy: Project Mirabal's "control through money fell by only three per cent" couldn't be confirmed. It's softened to "among the things that changed least", which the project summary supports. Tetlock's "90% → 70%" is now attributed to his own summary. Confirmed: Fischhoff, Slovic and Lichtenstein (100% sure, 70 to 85% right), Babcock 2004 (5%), Roberts 2017, Hogg 2014, Mellers 2014. Repetition: Beatriz's ex moved to Lisbon, the same city as 02-ii-b's Lisbon weekend. Changed to Valencia.

**06-vi-b** (contains a heavy chapter). Repetition: "So does your dentist" was the third dentist gag. Changed. Reused names (Uncle Rob, Tom, Sam, and Tobias next to Tobi) were changed. Ring-light, group-chat and "met the partner twice" gags varied. Safety: the danger list in when-weighing-stops matches Rule three, and the chapter has no humour. Confirmed: the Goldwater Rule (1973), the 2020 Harm Panel (1,200+ responses), the Hotline and BWSS positions, Campbell 2003.

**07-tools.** Cannibalisation: all 38 FAQ answers had copied the chapter openers word for word. Each is now a fresh two-to-three-sentence summary. The coercive-control answer now says "little or no physical violence", which matches the chapter. Decoder links: four close matches relabelled (see FACTS-TO-CHECK). Safety: the field card's three rules match chapter 2 word for word, and its danger definition matches Rule three, as do the 60-second weigh and the weighing sheet.

## Safety audit (book-wide)

- **Floor rules**: rules one and two are quoted the same way in 00-start, chapter 2, before-you-test, when-youre-the-one-accused, when-weighing-stops and the field card.
- **Danger conditions**: violence or threat, child at risk, cut off from help, leaving made hard, physical fear. They now match across chapter 2, before-you-test (fixed), when-weighing-stops, helping-someone-else-weigh, the field card, the 60-second weigh, the weighing sheet and 00-start (fixed).
- **Doubt tools**: base rates, three explanations, boring explanations, difference, the mirror, biases, gut and intent each keep a line saying they don't apply in danger.
- **Phone numbers**: none in the book. Help is "the domestic abuse service where you live" plus `/longafter/find-help`.
- **Diagnosis**: no character or reader is diagnosed. The chapters that discuss "narcissist" argue against diagnosing at a distance.
- **Humour**: none in the three heavy chapters, and none in the warn blocks I read. The chapter after chapter 2 opens on a dry line ("Welcome to having relationships") across a chapter break. I left it.
- **Hand-to-a-victim pages**: every chapter whose tool could be quoted to make a reader doubt themselves carries a counter-line. Examples are "If someone hands you this chapter…", the "trained to take the blame" warn in am-i-the-one-doing-it, and the survivor-accounts inversion in secondhand-accounts.

## Steelman objections, by movement

**I. Why weigh at all.** *"A book about doubting your reads hands abusers a script."* Answered. The three rules come before any argument, and the compare table quotes the abuser's lines beside the rule that beats each one. Every doubt tool repeats the floor. Several cases end with "yes, it was" (two-errors, conflict-or-control). *"The gradient trivialises abuse by putting it on a scale with rudeness."* Answered: the gradient's warn says threats skip the dial, and "deflating" gets its own section.

**II. The instrument is you.** *"Calling a survivor's alarm 'trauma' pathologises them."* Answered: "It isn't saying your alarm is wrong… that would be the same move the people who hurt you made", plus the warn "If someone tells you it's just your past". *"The biases chapter makes everyone doubt everything."* Answered by "Can bias make me miss abuse?", which points out that several biases push toward excuses.

**III. What counts.** *"The evidence ladder puts survivors' testimony at the bottom, because coercion leaves no record."* Partly answered before (observation is "real evidence", and secondhand-accounts has the survivor-accounts inversion). Now fully answered: the ladder warn says a missing record doesn't downgrade what you saw. *"The research is cherry-picked."* Every number was re-checked. Five were corrected or softened, the BITE critique is now sourced, and `limits` names what would change the book's mind.

**IV. The tests that work.** *"Telling victims to test an abuser gets people hurt."* Answered by the gate before every test, now with the missing isolation/leaving line, and by "If you can't bring yourself to run this, you already know." *"The naming test punishes ordinary defensiveness."* Answered: "defensive and engaged is normal".

**V. The mirror.** *"Asking 'am I the toxic one?' invites the controlled partner to blame themselves."* Answered by the "trained to take the blame" warn, the slow-and-specific standard, and the Ngozi case.

**VI. Living calibrated.** *"'Can people change?' encourages going back."* Answered: the chapter takes no side, a warn says nobody is owed your presence while they try, and the Mirabal finding about everyday control is stated. *"'Assessment is not decision' licenses accusing without evidence."* Answered: "Proof is for accusations." *"The humour trivialises."* Answered by keeping humour out of the heavy chapters, the warns and the safety lines, and by the repetition pass, which cut the gags that had become tics.

## FACTS-TO-CHECK

All 15 items are marked in `FACTS-TO-CHECK.md`. Summary: 12 resolved (5 by correction or softening: MacCormack and Lindquist, the Danger Assessment URL, Mirabal, the Tetlock attribution, the BITE source; the rest confirmed), 1 noted (field card length), 2 open (below).

## Needs the owner

1. **/feminine/the-harm-ladder** as a bridge for the-gradient: the page exists, but it isn't in COVERAGE-MAP section 8. Decide at freeze.
2. **research/SEARCH-DEMAND.md** still routes "lying" and "overreacting" to older chapters. Not edited, because it is outside this pass's files.
3. **Sources are additive-only**, so known-good DOIs (for example Kelly and Johnson 2008) couldn't be added to existing lines without failing the check. If the owner wants DOIs filled in, allow Sources edits for one commit.
4. **before-you-test** short and recall still say the gate checks "four things" while the checklist has seven lines. It's consistent (four core questions plus extras), but the owner may prefer "the gate" without a number.
5. **Stylistic tic, not fixed everywhere**: "X in Y's clothes" and "stapled to it" still appear a handful of times. They're varied enough now, but they're worth a look at freeze.
