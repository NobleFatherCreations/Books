# Steelman round 3 (2026-11-23): light steelman and fact check of the v6 voice rewrite

Scope: every added or changed line in `content/longafter-v2/[01]*.md` between commit `f51c417b` and HEAD (about 2,700 added lines across 16 files), read against `V6-WRITING-BRIEF.md`.

## What was checked

1. **New factual claims.** A script pulled every number and proper noun from the added lines and checked whether it existed anywhere in the old text. Almost nothing was new. Every candidate claim was then traced to the old text or the chapter's `## Sources`. Claims checked and found supported (old text or Sources, and correct to my knowledge): DARVO named by Jennifer Freyd in 1997; NPD prevalence "under 1 in 100 to around 6 in 100"; Dutton and Painter, early 1980s; partial reinforcement "since the 1950s"; Hall's 50/200 hours to make a friend; Bill Eddy and BIFF; Karin Huffer, 1995; section 91(14) and the Domestic Abuse Act 2021; the 2020 Harm Panel report; Canada's Divorce Act, coercive control laws in California, Hawaii and Connecticut, Australia 2023; no-fault divorce in England and Wales since April 2022 (20 weeks, then six weeks and a day); Form E; MIAM exemptions; ban on cross-examination in person; religious divorce and the civil decree; Clare's Law (England and Wales, Scotland, parts of Australia); non-molestation order breach as a crime (s42A); Child Maintenance Service Direct Pay and Collect and Pay; US wage withholding and tax refund intercepts; MVDAC, VAWA, U visas; Hague 1980, ICACU, Office of Children's Issues, Reunite; prohibited steps order and all-ports alert; marital rape law (UK since 1991, every US state); ICD-11 complex PTSD; NICE on trauma-focused CBT and EMDR; CBT-I; TF-CBT and child-parent psychotherapy; AirTag and Android tracker alerts; Stalking Protection Orders; deepfake image offences in England and Wales; Report Remove; US address confidentiality programs; Dogs Trust Freedom Project, Cats Protection Paws Protect, RedRover; Duluth wheel, 1984; Hourglass 24 hours; "press 55"; every helpline number (none was new).
2. **Safety regressions.** Humour in or near safety steps, crisis content, honest checks and the heavy chapters (plan.json `heavy: true`); advice whose meaning changed; lost caveats; scripts a judge could read as hostile; lines an abuser could quote.
3. **Hostile readers.** An abuser, a judge or social worker, a therapist, and a reader of a different gender or country.
4. **Voice.** Gags repeated across chapters, AI tells, flippancy.

## Findings fixed (25)

| # | File, chapter | Quote (before) | Verdict | Fix |
|---|---|---|---|---|
| 1 | 01-i-b, Still under the same roof (heavy) | "Put a copy of your ID or passport in your bag today, ready to hand to someone you trust outside the home." | **Safety regression.** The old step moved the copy out of the house. The new one leaves it in a bag at home, where a controlling partner who searches bags can find it and learn the reader is planning to leave. | "Next time you're out, hand a copy of your ID or passport to someone you trust, or leave it at work. Don't keep it in a bag at home, where it can be found." |
| 2 | 05-v-b, Protective orders (heavy) | "save it under a plain name, like "Boiler manual"... Nobody has ever scrolled through a boiler manual for fun." | Joke inside the closing safety step of a heavy chapter. | Joke sentence cut; the plain-name tip stays. |
| 3 | 05-v-b, Police and reporting (heavy) | "or if you'd rather not spend forty minutes on hold. Never use online reporting for an emergency." | Joke right before an emergency warning. | "or if you can't wait on hold." |
| 4 | 06-vi, Pregnant, or with a new baby (heavy) | "If someone offers to bring a lasagne, the answer is yes. Same for the second lasagne." | Gag in the bullet directly above the postnatal depression and self-harm bullet. | "If someone offers to bring a meal, the answer is yes." |
| 5 | 03-iii-a, Children as the channel (heavy) | "...your child's match with a brand-new passion for the school calendar." | Joke in a heavy chapter's list of tactics, and a repeated gag. | "...your child's match to be seen there." |
| 6 | 11-xi, If you go back | "Save emergency numbers under boring names. "Pizza" works." | Light line in a list of safety steps. Saving the emergency number itself under a fake name could also slow someone down in an emergency. | "Save helpline numbers under plain names, like "Pizza"." |
| 7 | 12-tools, Device and account audit | "(Yes, the takeaway app too. It knows your address.)" | Joke in a safety checklist; third use of the delivery-app gag. | "Delivery apps store your address." |
| 8 | 12-tools, The card | "They may come back when you're doing well. Funny how that works." | Third "Funny how" in the book; flip on a one-line safety summary. | "That timing is part of the pattern." |
| 9 | 05-v-a, Family court, honestly | "the word "narcissist" won't be used in court" | Overstated (the word can come up in court). | "calling someone a narcissist won't help you in court." |
| 10 | 05-v-a, Family court, honestly | "Cue the ex's sudden, touching passion for the school calendar." | Repeated gag, and sarcasm in a section a judge-minded reader would see as point-scoring. | Cut. |
| 11 | 04-iv, Messages you don't have to answer | "Yes, even their sudden passion for the school calendar goes in pile one..." | Repeated gag; also muddled the pile logic. | "If a real question is buried in a long one, that question goes in pile one." |
| 12 | 01-i-a, The shape it takes | "Your ex's sudden passion for the school newsletter doesn't feel like anything at all." | Variant of the same gag, two lines after a "newsletter" joke. | "A friendly email to your child's teacher doesn't feel like anything at all." |
| 13 | 00-start, Where are you right now? | "...like the ex who's suddenly passionate about the school calendar." | Repeated gag; made a heavy chapter's link sound trivial. | "...and what you can do about it." |
| 14-19 | 03-iii-a, 03-iii-b, 05-v-a, 07-vii (x2), 10-x | "rehearse your defence in the shower nine times" and variants | The shower comeback appeared in nine places. | Rewritten without the shower. Kept: 04-iv grey rock (the best: "stays in the shower"), and 01-i-a (descriptive, not a joke). 06-vi's practical "in the car or the shower" became "while you wash up" (fix 19). |
| 20-21 | 00-start, 08-viii | "the 47-message essay that doesn't"; "nobody will chase you with a 47-message essay about it" | Repeated gag; the therapy one was forced. | Rewritten. Kept the instance in 06-vi apps chapter, where it does practical work. |
| 22-24 | 00-start, 07-vii, 08-viii | "Nobody's keeping score." / "Nobody's keeping a perfect record." / "Nobody's handing out marks..." | A "nobody's scoring you" kicker used six times. | Three rewritten or cut. Kept 01-i-b (medals), 00-start (quiz on chapter four) and 10-x (where "nobody is keeping score any more" is literal about a controlled home). |
| 25 | 08-viii, Finding a therapist | "walking away after one date" | Dating metaphor for therapy, tied to the cut gag. | "after one session". |

All links, `## Sources` sections, `:::` fences, composite note lines and honest-check openers are untouched.

## Left for the owner (9)

These are almost all **pre-existing** lines the rewrite carried over. I didn't change them because the right answer is a judgment call or needs a source check.

1. **05-v-a, Systems abuse:** "Some states, including Georgia and Washington, have laws aimed at abusive litigation in family cases." Washington (RCW 26.51, 2020) is right. I can't confirm Georgia. Tennessee's Abusive Civil Action law (2018) is the other one I know of. Check, and consider "Washington and Tennessee".
2. **03-iii-a, Money as the channel:** "The application fee is waived" for domestic abuse. The Child Maintenance Service £20 fee was removed for everyone in February 2024. This is still true for the reader, but it's out of date. Consider "There's no application fee."
3. **06-vi (Pregnant) and 08-viii (When it's more than aftermath):** "asking for help won't mean your baby is taken away" and "won't mean your children are taken away". These are absolute promises in crisis content. They reassure, which matters, but a social worker would say "very unlikely" or "isn't a reason on its own". Decide whether accuracy or reassurance wins here.
4. **08-viii:** "Fit matters more than anything else in how well therapy works." The therapeutic relationship is a strong predictor, but "more than anything else" overstates it. Consider "Fit is one of the biggest factors in how well therapy works."
5. **11-xi, If you go back:** "It doesn't make this attempt less likely to hold." This is reassuring but unsupported, and nothing in Sources backs it. Consider "Plenty of people leave for good after going back."
6. **09-ix, The friends who didn't believe you:** the opener and a later paragraph both use "But he's always been so nice to me" / "Of course he was". The brief cites this as a model line, so I kept it. Two male-ex lines close together may read as gendered to a male reader. Consider neutralising the second.
7. **02-ii, Intimate images:** "increasingly a crime" became "in many places it's now a crime" for deepfakes. That's defensible (England and Wales, the US TAKE IT DOWN Act, Australia), so I left it.
8. **02-ii, Surveillance:** "If the heating keeps changing itself at odd hours, now you know who to suspect." A light line in a safety list. I kept it because it gives the reader a real sign to look for. Cut it if you'd rather keep every safety list joke-free.
9. **10-x, Pets:** "Funny how someone who never once walked the dog suddenly can't live without him" sits just before "Threats to hurt a pet". The brief names this as a model detail, so I kept it. It's worth a second look given what follows it.

## Hostile-reader read

- **Abuser quoting the page:** the counter-notes the rewrite added ("If they ever quote this back...") are calm and work. No script I read would look hostile to a judge. Every `::: decoder` reply supports the other parent's time with the children or keeps to arrangements.
- **Judge or social worker:** the main risk was sarcasm about the other parent (the school-calendar gag in Family court). It's gone.
- **Other countries:** UK and US specifics are labelled by place, or followed by "depends where you live". Composite stories that use Cafcass or council housing are fine as stories.
- **Gender:** examples alternate well across the book. The one cluster is item 6 above.

## Verdict

The rewrite is factually clean. It added almost no new facts, and the ones it did add check out. Where it reworded legal lines, it often scoped them better (Clare's Law, the Stalking Protection Order story placed in England). Its real problems were gags it reused across chapters (shower, school calendar, the 47-message essay, "nobody's keeping score"), a handful of jokes inside safety steps in heavy chapters, and one closing action that had become riskier. All of those are fixed. With the nine owner items decided, the book is ready for the next step.

Checks after edits: `python3 scripts/longafter-audit.py`: 0 failing. `rewrite-check.py` on all 14 edited files: 0 problems each. The AI audit wasn't run, so AI-AUDIT files are unchanged.
