# Prompt for Claude Fable — Fractal² (FINAL)

**Setup:** new Claude Code session on **NobleFatherCreations/Books**, branch **claude/great-keller-jkjz8c**, model **Fable 5.2** (Fable 5.1 if 5.2 isn't offered), effort **high**; raise to **xhigh** only for the final writing pass and the hardest fact-checking calls. Turn on web search. Paste everything below the line.

---

You are taking on the most important work of the author Shae Stovell (Noble Father Creations): **Fractal²**. This prompt sets the outcome, the standard and the hard limits. **The method is yours.** The owner wants the best thing you are capable of making, so push to the limit of your abilities and don't settle for a safe version.

## The outcome of this session

Two things, built, working, verified and ready for the owner to review (not deployed):

**A. The intro**, at `/fractal2`: a single scroll-driven page. The reader enters through it, and it leads directly into the new site.

**B. The first sector site, fully designed and working:** Entertainment & Music at `/fractal2/entertainment`, covering all 335 tactics and all 153 combos. Its navigation is **reimagined from first principles**, it links to The Fractal and the Pattern Decoder, and it is built by a generator, so every future sector inherits the design.

Together they should feel like one world: the intro is the door, and the sector site is the map you walk into.

## A. The intro: writing, experience, voice

**The writing.** Reimagine `content/fractal2/intro-v4.md` into the most powerful writing in this project. Write it only after you have absorbed everything listed under "Read first". The intro must:

- **Convey the full scope of what was already done.** *The Fractal* maps:
  - 8 stages and 30 techniques;
  - 3 nested levels of scale;
  - 30 sectors, each the capture of a relationship with a need;
  - 2,700 examples.

  Its interludes carry the argument:
  - **The Origin:** a parasite-like thought pattern that needs only a real need, a power gap and a gatekeeper. It runs without a villain, and it is separate from the people who drive it on purpose.
  - **The Mirror and the Chain.**
  - **The Spiritual Lens:** the counterfeit and the original.
  - **The original frequency** that the pattern buried.
  - **The closing descent,** which names what every tradition tried to say.
- **Introduce the most powerful map of manipulation's architecture ever made:**
  - more than 300 tactics per sector, at three levels;
  - the **combos**: compound systems that multiply harm, where the sequence is the weapon, and where knowing the exact mechanism is the key to healing and to immunity.
- **Carry the reader** through freedom, chain-breaking and sovereignty to the kingdom within, in the owner's lens: psychological freedom and spiritual awakening; accountability through exposing methods, never people.
- **Register:** powerful, organized writing. Not a fictional story, not a fact report. Signpost the lens once.
- **The owner's own account:** keep it exactly as given. Add nothing.
- **Structure, length and rhythm** are your decisions. v4 and `docs/FRACTAL2-STORY-BLUEPRINT.md` are inputs, not templates.
- **The ending** hands the reader into the sector site, naturally.

**The experience.** Make it the most impressive reading experience anyone has had, on **both phone and desktop**, with the phone designed in its own right.

- **Layered, advanced motion,** with visualizations that appear as the prose reaches them. Candidates:
  - the 30 sectors and the relationship each one captures;
  - the 8 stages inverting into their divine principles;
  - the nested levels;
  - the Origin's three conditions;
  - the Chain;
  - counterfeit ↔ original;
  - 30 expanding to 300+;
  - the combo chain compounding harm until one broken link collapses it;
  - a descent toward the frequency.
- **Techniques are your choice:** SVG, Canvas, WebGL, shaders, CSS scroll-driven animation, physics, kinetic typography.
- **Craft bar:** Apple-level.
  - Every effect carries meaning.
  - Motion is physical and interruptible.
  - 60 fps on a mid-range phone.
  - Nothing janky, nothing gratuitous.

**The voice.** The owner wants the intro narrated in **their own voice**.

- **Narration script:** write a spoken edit of the final text (`content/fractal2/narration-script.md`), with pauses and breaths marked.
- **Recording guide:** write a plain guide (`content/fractal2/RECORDING-GUIDE.md`) covering device, room, distance, format, takes per section, and how to send the files.
- **Player:** build it so it is:
  - started by the user (never autoplay);
  - synced to the scroll and the visuals, with captions taken from the prose;
  - pausable, with speed control and mute;
  - hosted on the same site.
- **Placeholder:** use a placeholder track until the recording exists.
- **Voice clone:** ask whether the owner also wants a consented clone of their own voice for future edits. Never use it in place of their recording unless they choose to.

## B. The Entertainment & Music site: reimagine how people navigate it

The current prototype (`library/fractal/sectors/ent/site/`, built by `design/fractal-sector/`) organizes everything as stages → tactics and families → combos. **Treat that as a first draft, not the format.** Design navigation around how real people arrive and what they need:

- **A survivor looking for words** for what happened.
- **Someone inside it right now,** who needs to know what comes next and how to get out safely.
- **A parent or friend** worried about someone.
- **An artist about to sign.**
- **A professional or advocate.**
- **A skeptic.**
- **A searcher** who lands on one page from Google.

Reimagine the views and paths. Possibilities to consider, not a checklist:

- **"Start here":** the top 10, with their scores. `ENT_top10.json` holds likelihood, harm, hidden-ness and recognition.
- **Browse all 153 combos,** sortable and filterable by:
  - fit tier (A/B);
  - family;
  - setting tags (touring, crew, signing, royalties, festival…);
  - safety-critical (the 41 with safety notes).
- **"What are you noticing?":** an entry built from the combos' observable indicators and recognition tests, leading to the patterns that match. It is recognition, never diagnosis. Private: nothing stored, nothing sent.
- **A living map:** an interactive tactic ↔ combo graph showing which tactics feed which combos, and how sequences recur.
- **Combo pages in reading modes:**
  - a 2-minute version (definition, tactic chain, cue cards, what to do now);
  - the full script;
  - "show me the sequence," an animated chain built from the real tactic order.
- **Tactic pages and anchors** that answer:
  - what it looks like at each level;
  - which combos use it;
  - its Decoder entry;
  - its Fractal chapter.
- **A design ready for future sectors:** "this pattern in other sectors" and "this tactic in other sectors," keyed by `combo_id` and the tactic standard id.

**Connections (all by stable id; never guess a link):**

- **To the Decoder:** resolve names through `content/decoder-v20/` (`alias_map.json`, `standard_index.json`, `playbook_patterns.json`). The live Decoder pages are in `instruments/playbook/site/` (e.g. `/playbook/<slug>`), and it has pattern pages such as Gaslighting, DARVO and FOG. This also links the 131 names the ENT audit couldn't resolve.
- **To The Fractal:** the sector chapter (`/fractal/entertainment-and-culture`), the interludes, and the stages' divine inversions. Check `library/fractal/` and link only pages that exist.
- **Between the intro and the sector site:** shared design language, a persistent sector switcher, breadcrumbs, and search across the site.
- **Downloads:** PDFs in a "take it with you" place. Check that they carry the credibility labels, or add a cover note.

**Keep what already works:**

- Exact author word-count round trip.
- Safety notes first.
- No internal ids or production cues shown to readers.
- The 16 checks in `design/fractal-sector/verify.mjs` (extend them, don't weaken them).
- Every change goes through the generator, so future sectors get it for free.

**Credibility tags: resolve them so the owner never verifies examples by hand.** Work through every item in `content/fractal/ent/build/review_queue.json`.

1. **Keep descriptive labels** as they are: "Composite", "Common pattern", "Varies by place".
2. **Research claims that need checking** against real sources. For each one, do one of:
   - keep it and cite the source;
   - generalize it;
   - soften it;
   - remove it, if it is false or can't be verified.
3. **Never fabricate a source.**
4. **Log every change in a ledger.**
5. **Apply changes only in a derived layer.** Never edit the author's files.
6. **Never weaken safety content.**
7. **Update the reader banners** to show the new state.
8. **Automate the whole process** for every future sector.

**Known defects to fix:**

- Stage 6 is "Extract" in The Fractal and "Control" in the expanded book. Treat them as one stage.
- The technique numbers in the owner's "Practice" script don't match the published list.
- The Enlighten transcript has spelling errors.
- C144's index undercounts two tags.

**Addresses:**

- Everything lives under `/fractal2`.
- Make the base path configurable. It is currently hard-coded in `design/fractal-sector/build.py`.
- Plan redirects from the old prototype addresses, including `fractal-entertainment.netlify.app/fractal/entertainment`, which is currently public.
- Record the architecture in `content/fractal2/ARCHITECTURE.md`.

## Read first

Follow `content/fractal2/READ-FIRST.md`: read Tier 1 in full before planning, use Tier 2 when the work needs it, and skip the rest. The owner's own words (`content/fractal2/owner-source/E-owner-messages-this-thread.md`) win every conflict. Write a half-page "What I understood" note before you plan, so the owner can catch a misreading.

## Your tools

Take stock at the start, then use whatever serves the work.

- **Skills:** list them. `.claude/skills/` includes:
  - design and motion: `impeccable`, `apple-design`, `emil-design-eng`, `frontend-design`, `refactoring-ui`, and the animation skills;
  - information architecture: `site-architecture`, `ux-heuristics`;
  - accessibility and performance;
  - writing: `copy-editing`, `no-ai-slop`;
  - findability: `ai-seo`, `schema`, `seo-audit`, `programmatic-seo`.
- **MCP servers:** find them via ToolSearch.
  - Sequential Thinking.
  - Playwright.
  - Web search/fetch.
  - ElevenLabs.
  - Figma, for storyboards only. It is never the source of truth.
- **Subagents:** `.claude/agents/`, for independent critique. Dispatch one at a time.
- **Quality rubrics:** write rubrics for the writing, the experience and the navigation. Score your work against them, have an independent reviewer score it too, and iterate until both pass.

## Hard constraints (non-negotiable)

**Deployment**

- **Never deploy.** The owner names each deployment in the conversation. A preview must be private. If "live" is ambiguous, ask.
- Before any production step, fetch all branches and run `node scripts/verify-deployed.mjs`. Another session's work may be live and ahead of this branch.

**Page architecture (CLAUDE.md)**

- Pages are self-contained.
- No CDNs, external scripts or runtime frameworks.
- Self-hosted fonts.
- Absolute links.
- Keep the Cloudflare beacon and THE HOUSE drawer.
- Build-time tools are fine.

**Accessibility**

- WCAG 2.2 AA.
- Reduced motion delivers everything statically.
- Every visualization has a text equivalent.
- Nothing is ever stuck invisible.
- Full keyboard and screen-reader paths.
- No horizontal overflow at 375px.

**Content**

- Patterns, never people. No named villains.
- Label every scenario as a composite.
- A short safety line on every page.
- Contested science is phrased as the owner's belief, not as fact.
- Exact public numbers:
  - 2,700 (The Fractal);
  - more than 300 (335) tactics per sector;
  - more than 1,000 examples per sector;
  - hundreds of combos: 203 on the master list, 153 in the first sector.

**What you may not touch**

- Never edit the owner's scripts or the author's source files.
- Never change wording inside published books. Connector links only, and ask first.
- Never modify the homepage without asking. It is another session's v17.

**Verification before any claim**

Use Playwright on phone and desktop, in light, dark and reduced motion, and check:

- screenshots at every visualization and every navigation view;
- page errors;
- overflow;
- frame timing while scrolling;
- axe;
- links;
- that ENT still passes its checks.

Look at the screenshots yourself before claiming anything works.

**Housekeeping**

- Commit and push to `claude/great-keller-jkjz8c` as you go.
- Keep `MEMORY.md`, `HANDOFF.md` and a `DECISIONS.md` current.
- Register the builds in `sites.json` as undeployed (`pendingDeploy`).

## Delegate what doesn't need you (cost discipline)

You are the most capable and most expensive model in this project. Spend your effort on judgment, taste and synthesis, and hand execution to cheaper models wherever a clear spec makes that safe.

**Keep these yourself:**
- the reading and the "What I understood" note;
- the final intro writing;
- the creative direction and design system;
- the navigation design;
- the tag-resolution policy and the genuinely ambiguous claims;
- the rubrics;
- the owner questions;
- the final acceptance review.

**Hand off the rest** through self-contained work packets that a model starting cold can finish without asking:
- **Opus:** complex implementation from your specs (visual choreography, the generator refactor, verify extensions, fixes).
- **Sonnet:** bulk first-pass claim research, QA screenshot runs, UI strings, narration markup, docs.
- **Haiku:** mechanical transforms and checks.

Use subagents with a model override (`model: "opus"` / `"sonnet"` / `"haiku"`), one at a time, and stop on any rate-limit error. Or write the packets for separate sessions.

**Write these hand-off files:**
- `content/fractal2/DESIGN-SPEC.md`: tokens, type, motion language (curves, durations, staggers), and a storyboard for each visualization with acceptance criteria.
- `content/fractal2/NAV-SPEC.md`: the navigation design.
- `content/fractal2/TAG-POLICY.md`: verdict rules, worked examples, and when to escalate back to you.
- `content/fractal2/RUBRICS.md`: the rubrics.
- `content/fractal2/work-packets/NN-*.md`, one per packet, each with its goal, inputs (repo paths), output paths, done criteria, the tests to run, and "escalate if…".

Build one hero visualization yourself first, to set the bar the delegated work must match. Review every packet's output against its criteria and the rubrics before accepting it.

## When to ask the owner

Use AskUserQuestion. Each question must:

- stand on its own;
- be in plain language;
- give options, with your recommendation first.

Batch questions, and never ask what you can decide yourself.

1. **After reading:**
   - the name and subtitle;
   - what "what's coming" can promise publicly;
   - where the War Map's policy list belongs;
   - recorded voice vs. an optional clone.
2. **After your design idea:**
   - your visual direction for the intro **and** the reimagined navigation;
   - shown as real screenshots on phone and desktop, ideally with a short screen recording;
   - with your recommendation.
3. **After tag resolution:** the summary and the riskiest changes, approved once as a batch.
4. **Before the final report:** anything still blocking.

## After the build: the "next" list

Present this list to the owner, recommend an order with the effort each item takes, and ask which to do. Start with the plan for posting the first sections.

1. **Narration in the owner's voice** (the priority): process the recording, sync it, add captions; optionally a consented voice clone.
2. **9:16 video clips** from the visualizations, following the clip pipeline in CLAUDE.md.
3. **A share kit:** quote cards, plus an image per sector and per combo.
4. **PDF editions:** a printable intro, and a field-guide PDF per sector, generated from source.
5. **Translations** (Spanish first) and a **plain-language edition**.
6. **Reader paths** beyond the ones built.
7. **Trauma-informed pacing:** pause points, grounding lines, a "take a break" anchor.
8. **Crisis resources by country.**
9. **An optional "Spot it" self-check** (owner decides; some books deliberately refuse gamification).
10. **A glossary** of the owner's vocabulary, linked where each term first appears.
11. **Corrected teleprompter editions** of the scripts, in a separate layer.
12. **A package format contract and validator** for incoming sector zips (Music Festivals and Spiritual Communities are next).
13. **A legal and defamation risk pass**, flagged for a lawyer where needed.
14. **Licence, "How to cite", and author markup.**
15. **Screenshot regression tests.**
16. **"Seen in these combos" on Decoder pages** (needs an owner-approved Decoder deploy).
17. **A homepage feature mock-up and card copy.**
18. **A search launch kit:** Search Console, Bing, IndexNow, structured-data validation.
19. **Outreach:** about 20 targets with personalized drafts under 150 words; the owner sends them.
20. **Cross-sector comparison visuals** once more sectors exist.
21. **Reading time** and a "where you left off" marker that stores nothing.
22. **A first-sections posting plan:** what goes up first, how it's announced, and the routing and deploy steps in plain words, for approval.

## Definition of done

- `content/fractal2/intro-final.md` is the strongest writing in the project.
- `/fractal2` (the intro) and `/fractal2/entertainment` (the full sector site with the reimagined navigation) are built, working beautifully on phone and desktop, connected to each other and to The Fractal and the Decoder, and passing every check.
- The narration script, recording guide and audio sync are ready for the owner's voice.
- Tag resolution is done, logged and applied in the derived layer.
- `ARCHITECTURE.md`, `DECISIONS.md`, `HANDOFF.md`, `MEMORY.md` and `sites.json` are up to date.
- The owner has a plain-language report with:
  - screenshots and a scroll recording;
  - the tag-resolution summary;
  - the "next" list with your recommended order;
  - a statement that nothing is deployed.
