# Prompt for Claude Fable — Fractal² (v3)

Open a new Claude Code session on **NobleFatherCreations/Books**, branch **claude/great-keller-jkjz8c**. Choose **Fable 5.2** if offered (otherwise 5.1) at **high** effort; use **max** for the writing and for the fact-checking judgment calls. Paste everything below the line.

---

You are taking on the most important work of the author Shae Stovell (Noble Father Creations): **Fractal²**. This prompt gives you the goals, the standard, and the hard constraints. **How you reach them is your decision.** Push your capabilities to their limit; the owner wants the best thing you are able to make, not a safe version of it.

## The three things that matter most

**1. The writing.** Reimagine the current draft (`content/fractal2/intro-v4.md`) into the most powerful piece of writing this project has. After absorbing everything in this repo, write the introduction that:
- conveys the full scope of the work already done: *The Fractal*, a cycle of 8 stages and 30 techniques at 3 nested levels across 30 sectors (2,700 examples), with its interludes (the Origin's parasite-like thought pattern that needs only a real need, a power gap and a gatekeeper and runs without a villain, separate from those who drive it on purpose; the Mirror; the Chain; the Spiritual Lens; the original frequency it buried; and the closing descent that names what every tradition tried to say);
- introduces **the most powerful map of manipulation's architecture ever made**: more than 300 tactics per sector at three levels, and the **combos**, compound systems that multiply harm, where the sequence is the weapon, and where understanding the exact mechanism is the key to healing from them and to never being caught by them;
- moves the reader through freedom, chain-breaking and sovereignty to the kingdom within, in the owner's lens (psychological freedom and spiritual awakening; true sovereignty; accountability through exposing methods, never people).

It is powerful, organized, storytelling writing, not a fictional story and not a fact report. Signpost the lens once. Make the reader feel the scope, the precision and the liberation. Keep the owner's account exactly as given (nothing added). Decide the structure, length and rhythm yourself: the earlier blueprint and v4 are inputs, not constraints.

**2. The experience.** Design and build the intro as a single scroll-driven page that is the most impressive reading experience anyone has had, on **both phone and desktop**: advanced, layered motion and effects; data visualizations that appear as the prose reaches them (for example the 30 sectors and the relationship each one captures, the 8 stages inverting into their divine principles, the nested levels, the Origin's three conditions, the Chain, counterfeit ↔ original, 30 expanding to 300+, the combo chain that compounds harm until one link breaks it, a descent toward the frequency). Choose the visual world, the techniques (SVG, Canvas, WebGL, CSS scroll-driven animation, shaders, physics, typography as motion, whatever serves) and the choreography. Every effect must carry meaning; the craft bar is Apple-level: physical, interruptible, 60 fps on a mid-range phone, nothing janky, nothing gratuitous. The phone experience is designed in its own right, not shrunk from desktop.

**3. The voice.** The owner wants the intro narrated in **their own voice**. Plan for it from the start:
- write a narration edit of the final text (spoken rhythm, breaths, pauses marked) as `content/fractal2/narration-script.md`;
- give the owner a short, plain recording guide (`content/fractal2/RECORDING-GUIDE.md`: phone or mic, room, distance, file format, how to split takes per section, how to send the files);
- design the page so narration is optional, user-started (never autoplay), and synchronized with the scroll and the visuals (sections, captions from the prose, pause/resume, speed, a clear mute), with the audio hosted on the same site (no external requests);
- until the recording exists, build the sync with a placeholder track so everything can be tested;
- ask the owner whether they also want an AI voice clone of their own voice (ElevenLabs is connected in some sessions) for future edits — only with their explicit consent, and never as a substitute for their recording unless they choose it.

## Read everything first

Start with `content/fractal2/HANDOFF.md`, then:
- `content/fractal2/owner-source/E-owner-messages-this-thread.md` (**the owner's own words; when anything conflicts, these win**);
- the scripts in `content/fractal2/owner-source/` (Spiritual Lens, War Map, inner techniques / Cage & Intent / Practice, Enlighten);
- `intro-v4.md`, `mission-draft.md`, `docs/FRACTAL2-STORY-BLUEPRINT.md`, `docs/FRACTAL-SERIES-INDEX.md`;
- the published Fractal in `library/fractal/`;
- the Entertainment & Music sector in `content/fractal/ent/` (tactic book, combo index, top 10, all 153 combo scripts, audit, review queue) and its built site and generator (`library/fractal/sectors/ent/site/`, `design/fractal-sector/`);
- Decoder v20 name data in `content/decoder-v20/`;
- `CLAUDE.md`, `sites.json`, `hub/`, the end of `MEMORY.md`.

Write a half-page "What I understood" note before you plan, so the owner can catch a misreading.

## Your tools

Take stock at the start and use what serves the work:
- **Skills:** list them; the repo's `.claude/skills/` include design and motion (`impeccable`, `apple-design`, `emil-design-eng`, `frontend-design`, `refactoring-ui`, the animation skills), accessibility and performance, writing (`copy-editing`, `no-ai-slop`), and search (`ai-seo`, `schema`, `seo-audit`, `programmatic-seo`).
- **MCP servers:** search for them with ToolSearch: Sequential Thinking, Playwright, web search and fetch, ElevenLabs, Figma (storyboards only, never the source of truth).
- **Subagents:** in `.claude/agents/`, for independent critique; dispatch one at a time.

Define a quality rubric for the writing and for the experience, score your own work against it, have an independent reviewer score it too, and iterate until both pass.

## Also in scope (complete these too)

- **Architecture.**
  - Everything under `/fractal2`: the intro, then `/fractal2/<sector>/…` for each sector's stages, families, combos, standards and A–Z, plus cross-sector indexes.
  - Move Entertainment there (its base path is in `design/fractal-sector/build.py`), with redirects from its old addresses, including `fractal-entertainment.netlify.app`.
  - Link everything by stable ids: tactic standard ids, `combo_id`, and Decoder v20 names via `alias_map.json`. That resolves the 131 unlinked tactic names in the ENT audit. Never guess a link.
  - Navigation between tactics, combos, sectors, Fractal chapters and the Decoder; downloads; a one-command path for future sectors; findability.
  - Record it in `content/fractal2/ARCHITECTURE.md`.
- **Tag resolution.** The owner should not have to verify examples. Resolve every item in `content/fractal/ent/build/review_queue.json`:
  - keep descriptive labels ("Composite", "Common pattern", "Varies by place");
  - research claims needing review against real sources: keep and cite, generalize, soften, or remove anything false or unverifiable;
  - never fabricate a source;
  - record every change in a ledger;
  - apply it only in a derived layer (never the author's files);
  - never weaken safety content.

  Make it automatic for every future sector.
- **Fix known defects:** stage 6 is "Extract" in The Fractal and "Control" in the expanded book (treat them as one stage); the technique numbers in the owner's "Practice" script don't match the published list; the Enlighten transcript has spelling errors; C144's index undercounts two tags.

## Hard constraints (non-negotiable)

- **Never deploy.** The owner names each deployment in the conversation. A preview must be private. If "live" is ambiguous, ask.
- Before any production step, fetch all branches and run `node scripts/verify-deployed.mjs`. Another session's work may be live and ahead of this branch.
- **Self-contained pages** (CLAUDE.md): no CDNs, no external scripts or runtime frameworks; self-hosted fonts; inline assets or same-site files; absolute links; the Cloudflare beacon and THE HOUSE drawer stay. Build-time tools are fine.
- **Accessibility and safety:**
  - WCAG 2.2 AA;
  - `prefers-reduced-motion` delivers everything statically;
  - every visualization has a text equivalent;
  - nothing is ever stuck invisible;
  - full keyboard and screen-reader paths;
  - no horizontal overflow at 375px.
- **Content:**
  - patterns, never people; no named villains;
  - label any scenario as a composite;
  - a short safety line;
  - contested science phrased as the owner's belief;
  - exact public numbers (2,700; more than 300 / 335 tactics per sector; more than 1,000 examples per sector; hundreds of combos: 203 on the master list, 153 in the first sector).
- Never edit the owner's scripts or the author's source files. Never change wording inside published books (connector links only, and ask first). Never modify the homepage without asking; it is another session's v17.
- **Verify before you claim anything:** Playwright screenshots on phone and desktop, light and dark, reduced motion, and at each visualization's scroll position; page errors; overflow; frame timing while scrolling; axe; links. Look at the screenshots yourself.
- Commit and push to `claude/great-keller-jkjz8c` as you go. Keep `MEMORY.md`, `content/fractal2/HANDOFF.md` and a `DECISIONS.md` current. Register the build in `sites.json` as undeployed (`pendingDeploy`).

## When to ask the owner

Use AskUserQuestion. Questions must stand on their own, in plain language, with options and your recommendation first. Batch them, and never ask what you can decide yourself.

- **After reading:** name and subtitle; whether Entertainment moves to `/fractal2/entertainment` (recommended); what "what's coming" can promise publicly; where the War Map's policy list belongs; recorded voice vs an optional clone.
- **After your design idea:** show your visual direction(s) as real screenshots on phone and desktop, ideally with a short screen recording of the scroll, and your recommendation.
- **After tag resolution:** the summary and the riskiest changes, approved once as a batch.
- **Before the final report:** anything blocking.

## After the intro and design are built: the "next" list

When the intro and the design are done, present this list to the owner. Ask which to do and in what order, starting with how the first sections should be posted. Recommend an order and say what each costs in effort.

1. **Narration in the owner's voice** (the priority): process the owner's recording (noise clean-up, levels, splitting, timing marks), sync it to the scroll, and produce captions; optionally a consented voice clone for future edits.
2. **Short videos from the visualizations:** 9:16 clips with captions for TikTok, following the clip pipeline in CLAUDE.md.
3. **A share kit:** quote cards from the strongest lines; an image per sector and per combo.
4. **A printable PDF edition** of the intro, and a combined field-guide PDF per sector, generated from source.
5. **Translations** (start with Spanish) and **a plain-language edition**.
6. **Reader paths:** survivor, parent, professional or advocate, skeptic, someone inside one now.
7. **Trauma-informed pacing:** pause points, grounding lines, a "take a break" anchor before the combos.
8. **Crisis resources by country** instead of a generic line.
9. **An optional "Spot it" self-check** from the combos' recognition tests: private, stores nothing, recognition not diagnosis. The owner decides, since some books deliberately refuse gamification.
10. **A glossary** of the owner's vocabulary, linked where each term first appears.
11. **Corrected teleprompter editions** of the owner's scripts, in a separate layer that never touches the originals.
12. **A package format contract and a validator** for incoming sector zips (Music Festivals and Spiritual Communities are next), so each one drops in cleanly.
13. **A legal and defamation risk pass** on the intro, "Why I made this" and the combo scenarios, flagged for a lawyer where needed.
14. **Licence and citation:** a licence choice, "How to cite this work", and author markup.
15. **Screenshot regression tests** so later edits can't quietly break the page.
16. **The Decoder side of the links:** "Seen in these combos" on Decoder tactic pages (needs a Decoder deploy, owner-approved).
17. **A homepage feature mock-up** and the exact card copy, for approval.
18. **A search launch kit:** Search Console and Bing submission steps, IndexNow pings, structured-data validation.
19. **Outreach** via the CLAUDE.md system: about 20 real targets with personalized drafts under 150 words; the owner sends them, never automatic.
20. **Cross-sector comparison visuals** once more sectors exist.
21. **Reading-time estimates** and a "where you left off" marker that stores nothing.
22. **A first-sections posting plan:** what goes up first (intro, Entertainment field guide, top 10), how each is announced, and the exact routing and deploy steps in plain words for the owner to approve.

## Definition of done (for this session)

- The final writing is in `content/fractal2/intro-final.md` and is the strongest thing in the project.
- The built page (source in `design/fractal2/`, output recorded in `sites.json`) works beautifully on phone and desktop, degrades gracefully, and passes every check.
- Narration script, recording guide and audio sync are ready for the owner's voice.
- Architecture, tag resolution and the ENT move are done, verified, and documented.
- The owner has a plain-language report with screenshots and a recording of the scroll, the "next" list with your recommended order, and nothing deployed.
