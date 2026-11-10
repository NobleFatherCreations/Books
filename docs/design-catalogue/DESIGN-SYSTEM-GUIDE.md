# Design System Guide — how it works, why it should beat the defaults, and how to run it

**Audience:** (1) the owner, who is not a designer and needs to understand what this machine does and where their own judgment is required; (2) any AI that must run it. Section 6 is the operating script for the AI. If you are an AI without repository access, you need the folder `docs/design-catalogue/` and `scripts/design-gates.mjs` as well; this guide refers to them.

---

## 0. In one minute

You do not need to know design vocabulary. The system does three things to compensate:

1. **It interviews you first**, in plain language and with pictures, and turns your answers into design decisions.
2. **It forces the AI to look at everything that exists** (56 categories, hundreds of named techniques) and to write down, for each category, what it used, what it rejected and why. It cannot silently skip a category and fall back on habit.
3. **It makes the AI compete against itself.** It must produce *three genuinely different directions*, show you small comps, and let **you choose by looking**. Then it must beat real top-tier reference sites in a side-by-side score and survive an independent critic before calling anything finished.

Nothing can *prove* a design is "the best possible". What the system can do is raise the odds sharply and give you evidence at every step. Section 3.6 explains which evidence, and what it cannot cover.

---

## 1. Why earlier results looked horrible (so you know what this fixes)

The Fractal² intro passed every automated test and still looked generic and broke on an iPhone. The causes, from the repository record:

- The brief gave goals and adjectives ("world class", "Apple-grade") but no way to **test** them.
- Design skills were listed but never shown to be used. Nobody was required to **look at screenshots**; tests measured errors and overflow, not composition.
- The AI designed from its **memory of the average website**, so it produced the average: beige serif, thin dots for "art", text over figures.
- There was **no stop-and-show point**, so a wrong direction was built all the way through.
- It was **never tried on a real phone** before being posted.

Each of these has a named countermeasure below.

---

## 2. The pipeline

```
0 INTERVIEW  ->  1 RESEARCH  ->  2 COVERAGE + CHOICE  ->  3 THREE COMPS (you pick)
                                                              |
      6 HAND-OFF  <-  5 CRITIQUE LOOP (gates, benchmark, critic)  <-  4 BUILD
```

| Phase | What happens | Evidence it leaves |
|---|---|---|
| 0 Interview | AI asks you short rounds of questions (section 5), plays your answers back | A one-paragraph brief you corrected |
| 1 Research | AI opens 10+ real top-tier sites, screenshots them, reads them, notes techniques | `REFERENCES.md` with screenshots |
| 2 Coverage and choice | AI marks all 56 categories USE / REJECTED / N/A; writes "the obvious answer" and rejects it; scores candidates; applies the Budget | `COVERAGE.md`, `DESIGN-CHOICES.md` |
| 3 Three comps | AI builds 3 opening screens in 3 different directions; **you pick** | Side-by-side screenshots, your choice |
| 4 Build | Section by section, screenshot after each, collisions fixed at once | Screenshots read and described |
| 5 Critique loop | 3+ rounds: automated gates, benchmark vs best references, independent reviewer | Gate reports, scores, reviewer notes |
| 6 Hand-off | Real-phone checklist, notes, private preview; nothing public without your word | `PHONE-CHECK.md`, `DESIGN-NOTES.md` |

---

## 3. How the system answers each of your questions

### 3.1 "How does the AI know what is possible?"

- **`06-master-names-bible.md`** is a vocabulary of 56 categories: site genres, section types, hero types, navigation, scroll techniques, page transitions, text effects, cursor and hover effects, 3D and shader effects, backgrounds, surfaces, motion principles, cinematic techniques, data-visualisation forms, design laws, dark patterns, tools, inspiration sources, 2025–26 emerging items, and more. It was compiled from knowledge to mid-2026 plus a short search; it is long, not literally complete.
- **A list alone doesn't change behaviour**, because an AI can read it and still ignore it. So the system adds **`COVERAGE.md`**: a table with one row per category. The AI must fill every row with USE / REJECTED / N/A and a reason. Skipping a category is visible. More than 12 "N/A"s is flagged to you.
- **A name isn't knowledge.** The system forbids choosing from a name alone: the AI must **screenshot a real live example** of each shortlisted technique and read the image. This is also how it learns what a technique looks like today.
- **Refresh:** the AI searches current trend and award sources each run and adds dated findings, so the list doesn't go stale.

### 3.2 "How does it choose?"

Procedure in `07-choosing-and-combining.md` §3:
1. Write the reader's state first (the most vulnerable plausible reader sets the floor for calm, contrast and motion).
2. Write a **concept sentence** (meaning, not mood).
3. Derive constraints (devices, safety, repo rules, performance).
4. Long-list candidates per category, with real screenshots.
5. **Score each 0–2** on Meaning, Reader fit, Feasibility, Distinctiveness, Cohesion. Anything scoring 0 on Meaning or Reader is dropped.
6. **Write a one-line reason for every strong option rejected.**
7. Assemble the set, then check the Budget.

### 3.3 "How does it combine effectively?"

Combination is where "burnt out" outputs come from, so it is rule-bound, not left to taste:
- **The Budget:** 1 concept, 1 lead style, at most 1 supporting influence, 1 signature move, 1 type system (max two families), 1 colour system with one accent, 1 motion language, and **at most 3 decorative effects visible at once**. Exceeding it needs a written reason.
- **Compatibility table:** which lead styles pair with which supports, and which never co-lead (e.g. brutalism with glass; ornament with technical).
- **Intensity map:** every section marked Loud / Medium / Quiet; at least 30% Quiet, never more than two Loud in a row. Spectacle only reads as spectacle after rest.
- **Layer-cake order for each screen:** purpose, focal point, text zone first, then figure zone, then navigation, then motion, and texture **last**.
- **Authority order when rules conflict:** safety and accessibility, reader state, concept, lead style, signature move, decoration.

### 3.4 "How do I make sure it doesn't default?"

Seven mechanisms, each a checkable artefact:
1. **"The obvious answer."** Before choosing, the AI writes what a default generator would produce for this brief (e.g. dark with gold, rings, glass cards) and must explicitly reject it, or defend it.
2. **Coverage matrix** (3.1): can't skip categories.
3. **Three genuinely different directions**, not colour variations, shown to you as comps. Comparing three real options also protects you from the first idea being accepted by default.
4. **Substitution test:** swap in another brand's logo; if nothing feels wrong, it is generic and must be redone.
5. **Anti-cliché list** (`07` §8): gold-on-black "premium", sacred geometry as decoration, floating glass cards on dark, etc. need a written justification.
6. **Reference-first:** it designs from screenshots of current top work, not from memory of the average.
7. **Benchmark score** against the best references (3.6): "distinctiveness" below 4/5 means another round.

### 3.5 "How does it ensure attention to detail?"

- **Named failure modes F1–F14** (effect soup, collisions, specks for art, flat hierarchy, dead space, fatigue, style clash, cliché, readability sacrificed, only works on the dev machine, wrong register, inconsistent craft...). Every critique round checks each by name.
- **Automated gates** (`scripts/design-gates.mjs`): screenshots every scroll step on phone and desktop in light, dark and reduced motion; fails on figure/text overlap, text over text, errors, external requests, horizontal overflow and reduced-motion violations; warns on tiny text, small tap targets, translucent headers, unloaded fonts, too many simultaneous animations. It was tested against the broken intro and caught the real overlaps.
- **Screenshots must be read, not merely generated.** The rules forbid describing a screenshot that wasn't read.
- **Craft checklist** (`04` §T): pixel snapping, icon alignment, consistent radii and shadows, focus rings, selection colour, favicon, tab title, 404, print, social card.
- **Independent critic:** a fresh reviewer subagent sees only screenshots, the brief and the rubric (not the designer's reasoning) and names the five biggest weaknesses.
- **Real-device checklist** (`PHONE-CHECK.md`) because Chromium emulation is not iPhone Safari.

### 3.6 "How do I know it's the best possible?"

Honest answer: **you can't know, and neither can the AI.** "Best possible" isn't a measurable fact. The system substitutes five kinds of evidence, ordered from strongest:

1. **Your own eyes on real options.** Three different directions as comps; you choose. This is the highest-value step and needs no design vocabulary.
2. **Side-by-side benchmark** against the strongest real references on the same screen size, scored 1–5 on hierarchy, type, space, craft, distinctiveness, feeling; anything under 4 means another round.
3. **An independent critic** that is not invested in the design.
4. **Automated gates** (necessary, not sufficient).
5. **Documented reasoning:** concept, choices, rejections, coverage. If it later looks wrong, you can see exactly which decision to challenge.

What it cannot guarantee: that a design no one has imagined yet doesn't exist; taste differences between you and the reviewer; that the AI's screenshot reading is perfect. If something feels off to you, say so in plain words ("too busy", "cold", "feels like every site"); that is valid input and the system has a place for it (a new round).

---

## 4. The steelman (strongest case for, then strongest objections against)

**Case for.** Most AI design failures come from three causes: designing from the statistical average, having no visual feedback, and having no decision record. This system attacks each: reference screenshots replace memory; a coverage matrix and the "obvious answer" step make defaulting visible and costly; mandatory screenshot-reading, gates, a benchmark and an independent critic provide feedback; three comps and a stop point put the owner's judgment where it is strongest (choosing between real things) and weakest-needed (vocabulary). Constraint (a Budget of strong decisions) is the known cure for effect soup, since award-level work is characterised by restraint and a single memorable move.

**Objections and answers.**

| Objection | Answer / mitigation |
|---|---|
| "A checklist of 56 categories will make the AI bloat the design with everything." | The Budget and "REJECTED" are the point: coverage means *considered*, not *used*. Most rows should end REJECTED or N/A. |
| "A model can fill the coverage matrix with plausible text without really looking." | Yes, that is the main weakness. Mitigations: screenshots required per shortlisted item; independent critic; benchmark; and you can spot-check any row. Not eliminated. |
| "Rules produce competent but boring work." | Three divergent directions and the distinctiveness score push against it; the signature move rule demands one memorable gesture; the owner picks. Rules are for what to avoid; taste comes from references and your choice. |
| "The AI's self-scores are unreliable." | They are a prompt to look again, not proof; hence the independent reviewer and your own comparison of side-by-side images. |
| "Too heavy for small jobs." | Scale down: skip phases 1–2 depth for a single-component tweak, but never skip the interview, screenshot-reading and the gates. |
| "The names bible is from memory and may be dated or wrong." | The research phase refreshes it with dated entries and real screenshots; brand entries are marked "verify". |
| "Gates passed before and the result was still bad." | True. That is why they are not the finish line; the human comp choice, benchmark and critic come after them. |
| "Libraries (GSAP, WebGL helpers) are blocked by the self-contained rule, limiting what's possible." | Libraries are allowed as local copies with the owner's yes (`[LIB]`). The interview asks about this. |

---

## 5. The opening interview (the AI asks these before doing anything)

**How to run it:** use the AskUserQuestion tool, **max 4 questions per round**, 2–4 plain-language options each (the user can always type something else). Do not use design jargon in questions; explain any term in a few words. After each round, summarise in one line what you understood. After the last round, play back a one-paragraph brief and ask for corrections. Skip questions already answered in files or earlier messages. If an answer is "I don't know", offer to show pictures (see Round 2) instead.

### Round 1 — What this is and who it is for
1. **What are we making?** (a scroll story / a tool or app screen / a reading site / a showcase / something else)
2. **Who is the reader, and what state are they in when they arrive?** (curious and relaxed / stressed or in danger / professional and skeptical / mixed; may be watched on a shared device?)
3. **What should they do or feel at the end?** (understand something / take an action / feel safe / feel awe / return later)
4. **Where do they read it?** (mostly phone / mostly desktop / both equally; short visits or long sessions)

### Round 2 — Feel and taste (pictures, not words)
The AI first screenshots 8–12 very different real sites and shows them in pairs. For each pair ask "which feels closer to what you want?" (A / B / neither). Then ask:
1. **Pick up to three words** for how it should feel: calm, grave, warm, awe, sharp, playful, intimate, monumental, clinical, human, cinematic, other.
2. **Name any site, book, film or app whose look you love, and one you hate** (and say what you hate about it).
3. **Loud or quiet?** (quiet and restrained / balanced / bold and dramatic)
4. **Dark, light, or both?** (dark / light / both with the reader's choice / not sure, show me)

### Round 3 — Boundaries and safety
1. **What must never happen?** (e.g. nothing that could alarm a reader, nothing that looks like a self-help cliché, no stock imagery)
2. **Is anyone reading in an unsafe situation?** (If yes: quiet default look, Quick Exit, no tracking, no motion by default.)
3. **What is fixed and must not change?** (words, data, structure, branding)
4. **Technical limits?** (works offline and self-contained / local libraries allowed with my yes / anything goes)

### Round 4 — Ambition, motion and effort
1. **How much motion?** (almost none / gentle, meaningful / rich and cinematic / as much as it can handle on a phone)
2. **How ambitious should the main visual moment be?** (typographic only / illustrated figures / 3D or shader showpiece)
3. **What is the one thing you most want people to remember?** (free text)
4. **Review style:** do you want to see three directions as quick comps before the full build? (yes, recommended / just build one)

### Round 5 — Playback
The AI writes a one-paragraph brief, the position on each axis (quiet↔loud, warm↔cool, dense↔spacious, text-led↔figure-led, static↔choreographed, playful↔grave, familiar↔novel, dark↔light), and 3 candidate concepts in one line each. Ask: **"What's wrong or missing?"** Only then proceed.

### Mapping answers to decisions (for the AI)
- Reader state sets the floor for contrast, motion, calm and safety tags `[SAFE]` (these override style).
- Feel words + picked pairs set the lead style candidates (`01 §A/§C`), type character and colour temperature.
- Loud/quiet and motion answers set the Budget (number of feature effects) and the intensity map.
- Phone/desktop split sets the primary design target and `[IOS]` testing priority.
- "Hate" answers and "obvious answer" become the explicit reject list.
- Technical limits decide `[SC]`/`[LIB]`/`[NET]` filtering.

---

## 6. Operating script for the AI

1. Read, in order: `CLAUDE.md`, `MEMORY.md`, `docs/AI-QUICKSTART.md`, this guide, `docs/design-catalogue/00-README.md`, `07-choosing-and-combining.md`, then skim all 56 categories in `06-master-names-bible.md`, then `01`–`05` as needed.
2. Run the interview (section 5). Do not build before the playback is confirmed.
3. Research with Playwright: 10+ real reference sites including some outside the obvious genre; screenshot at 390 and 1440; **read the images**; write `REFERENCES.md`.
4. Copy `COVERAGE-TEMPLATE.md` to `content/<project>/COVERAGE.md`; fill all 56 rows.
5. Write "the obvious answer" and reject it. Write the concept sentence. Score candidates; record rejections; write `DESIGN-CHOICES.md` with the Budget and the intensity map.
6. Design **three different directions**; build an opening-screen comp for each at 390×844; show the owner side by side; the owner chooses.
7. Build the hero in the chosen direction; critique with `impeccable critique`; iterate at least three rounds; run `node scripts/design-gates.mjs <url> <outdir> --profiles phone-light,desktop-light`. Show the owner. Continue only with approval.
8. Build the rest. After every section: screenshot, read, describe in one sentence, fix collisions immediately.
9. Critique loop (3+ rounds): full gates (all five profiles), screenshots at 10+ positions on both devices, `impeccable critique` and `audit`, accessibility and performance skills. Then the **benchmark** (side-by-side vs 3 best references; score 1–5 on hierarchy, type, space, craft, distinctiveness, feeling; <4 means iterate) and the **independent critic** (one fresh reviewer subagent given only screenshots, brief and rubric; fix its five biggest points). Dispatch agents one at a time per `CLAUDE.md`.
10. Hand-off: `PHONE-CHECK.md`, `DESIGN-NOTES.md` (which skills and tools were used and what each changed), update `MEMORY.md`. Ask for a private preview. **Deploy nothing public without the owner's word.**
11. Report honestly: what was checked, what wasn't, the two screens you are least sure of.

**Never:** design from memory of a genre; choose from a name without a real example; combine two lead styles; exceed the Budget without a written reason; describe a screenshot you didn't read; change fixed content; add a network dependency.

---

## 7. What the owner does (about 5 minutes each)

1. Answer the interview (Round 1–4) and correct the playback.
2. Pick one of three comps by looking (and say what to keep from the others if you like).
3. Look at the hero screen and say "continue" or say what feels wrong in plain words.
4. Run the 10-step phone checklist on your real phone with the private preview link.
5. Say "deploy" when you are happy. Nothing goes public before that.

## 8. Known limits (stated plainly)

- "Best possible" cannot be proven; the system raises odds and gives evidence (3.6).
- The coverage matrix can be filled superficially by a model; screenshot requirements, the critic and your spot-checks are the counterweight.
- The names list is not literally complete and ages; refresh each run.
- Taste is partly personal; your comp choice and plain-word feedback are the final authority.
- Headless Chromium and its gates do not equal an iPhone; the real-phone step is required.
- Automated gates have known blind spots (e.g. judging legibility over a background figure); a human read of screenshots remains required.
