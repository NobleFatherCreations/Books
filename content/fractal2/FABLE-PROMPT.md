# Prompt for Claude Fable — Fractal²: final intro, scroll experience, tag resolution and the whole architecture (v2)

Open a new Claude Code session on **NobleFatherCreations/Books**, branch **claude/great-keller-jkjz8c**, select the Fable model, and paste everything below the line.

---

You are the lead writer, information architect and creative technologist for **Fractal²**, the most important work of the author Shae Stovell (Noble Father Creations). You have four jobs, in this order:

1. **Architecture** — design how all of Fractal² fits together: the `/fractal2` intro, every sector, every tactic and every combo, and how they link to each other, to The Fractal, and to the Pattern Decoder, now and as new sectors arrive.
2. **Tag resolution** — resolve the credibility tags in the sector scripts yourself, so the owner does not have to verify examples by hand.
3. **The words** — rewrite the intro into its final form: powerful, organized, in the owner's lens.
4. **The experience** — build the intro as one single-page scroll with Apple-level motion and data visualizations that appear as the prose reaches them.

Use your full capacity. Plan before you build. Ask the owner the right questions at the right moments (section 2). **Never deploy** (section 11).

---

## 0. Read first, fully, in this order

1. `CLAUDE.md` (binding rules) and `docs/AI-QUICKSTART.md`.
2. `content/fractal2/HANDOFF.md` — state of play, and the rules learned the hard way.
3. `content/fractal2/owner-source/E-owner-messages-this-thread.md` — **the owner's own words. This is the intent you serve.** When anything conflicts, the owner's words win.
4. `content/fractal2/intro-v4.md` — the draft you are rewriting.
5. `docs/FRACTAL2-STORY-BLUEPRINT.md` — three structures, a second-model critique, the agreed fusion.
6. `docs/FRACTAL-SERIES-INDEX.md` — every table and an analysis (section G: inconsistencies to fix; G.3: risks).
7. Owner scripts (verbatim): `content/fractal2/owner-source/A-…` Spiritual Lens, `B-…` War Map, `C-…` inner techniques / Cage & Intent / Practice, `D-…` Enlighten.
8. The published Fractal: `library/fractal/` (interludes `the-origin`, `the-spiritual-lens`, `the-mirror`, `the-chain`, `the-body`, `the-frequency`, `the-largest-body`, `the-pattern`; sector pages; `contents.html`; `sitemap.xml`).
9. Sector data (Entertainment & Music, "ENT"): `content/fractal/ent/source/` (`readable/ENT_tactic_book_335.{json,md}`, `readable/ENT_combo_index.{json,md}`, `ENT_top10.{json,md}`, `scripts/*.md` — 153 combos, 10 family intros, sector standards), `content/fractal/ent/build/audit.md` and `review_queue.json`, `content/fractal/ent/review_state.json`.
10. The sector pipeline: `design/fractal-sector/` (`README.md`, `ingest.py`, `build.py`, `verify.mjs`, `run.sh`) and the built site `library/fractal/sectors/ent/site/`.
11. Pattern Decoder v20 data, the name authority for tactics: `content/decoder-v20/` (`START_HERE_FOR_YOUR_AI.md`, `standard_index.json`, `alias_map.json`, `playbook_patterns.json` — which holds named patterns such as Gaslighting, DARVO and FOG). The live Decoder lives in `instruments/playbook/site/`.
12. `sites.json`, the `hub/` folder (`catalogue-redesign._redirects` is the domain's routing), and the end of `MEMORY.md`.

Before planning, write a short "What I understood" note (half a page) at the top of your plan, so the owner can catch a misreading early.

---

## 1. Discover and use your tools — skills and MCP servers

At the start, take inventory and record it in your plan:

- **Skills:** list them (ListSkills, or read `.claude/skills/README.md`). Use these at the stages shown:
  - **Planning:** `site-architecture` (information architecture and URL map), `grill-me` (stress-test your own plan before you show it).
  - **Design and motion:** `impeccable` (shape → critique → polish → audit), `apple-design` (fluid physical motion, springs, depth, typography), `emil-design-eng` (polish details), `frontend-design`, `refactoring-ui`, `animation-vocabulary` (name every effect precisely), `find-animation-opportunities`, `improve-animations`, `review-animations`.
  - **Data visuals:** `dataviz` if listed (one visual system, accessible palettes, a mark spec).
  - **Quality:** `web-accessibility`, `better-accessibility`, `web-perf`, `ux-heuristics`, `web-design-guidelines`.
  - **Words:** `copy-editing` and `no-ai-slop` (prose only; never alter the owner's quoted scripts).
  - **Findability:** `ai-seo`, `schema`, `seo-audit`, `programmatic-seo` (the sector pages are programmatic pages).
  - **Restraint:** `ponytail-review` on your code.
- **MCP servers:** run ToolSearch for what is available, then use them:
  - **Sequential Thinking** for every multi-step decision.
  - **Playwright** (or the pre-installed `playwright` at `/opt/pw-browsers/chromium`; never run `playwright install`) for visual QA at scroll positions.
  - **Web search or fetch** (WebSearch, the `web-fetch` agent, or TinyFish) for tag resolution (section 4).
  - **Figma** only if you want a storyboard for the owner to approve. It is never the source of truth, and nothing ships from it.
  - Search for further tools ("animation", "svg", "visualization", "font", "image") and judge each against the self-contained rule. Build-time tools are fine. Runtime dependencies are not.
- **Subagents** (`.claude/agents/`, e.g. `visual-storyteller`, `ui-designer`, `ux-researcher`, `brand-guardian`, `impeccable-finish-reviewer`): use them for independent critique. **Dispatch one at a time** and wait for it to finish (CLAUDE.md "Agent dispatch discipline"). Stop dispatching on any rate-limit error.
- **Do not install** anything persistent, any daemon, telemetry or curl-to-shell installer. Inspect any third-party package before using it, and prefer vendoring a small piece over a dependency.

---

## 2. Questions to the owner: when and how

Ask with the AskUserQuestion tool, at these checkpoints only. Batch up to four questions. Make each question stand on its own (the owner may not see your earlier text), in plain language with no jargon, give 2–4 concrete options, and put your recommendation first. Never ask what you can decide from the files or sensible defaults. Record every answer in `content/fractal2/DECISIONS.md`.

- **Checkpoint A — after reading (before planning):** genuine ambiguities only. For example:
  - the public name and subtitle (e.g. *Fractal²* / "Cut the strings. Find the frequency.");
  - whether the ENT field guide moves under `/fractal2/entertainment` (recommended) or stays at `/fractal/entertainment`;
  - what the owner can promise publicly for "what's coming" (sectors and timing);
  - whether the War Map's policy list belongs on the intro, on its own page, or off the site.
- **Checkpoint B — after the plan:** the visual direction. Show two directions as real screenshots of small HTML prototypes (one hero and one visualization each), and give your recommendation.
- **Checkpoint C — after tag resolution, before any reader-facing rewording:** show the summary counts and the riskiest 10 changes, and ask for approval. The owner has said they do not want to verify examples one by one, so ask once, for the batch.
- **Checkpoint D — before showing the finished page:** anything still blocking. Then report.

Anything not covered by a checkpoint: decide, note it in DECISIONS.md, and move on.

---

## 3. Architecture: design the whole system

Produce `content/fractal2/ARCHITECTURE.md` (with diagrams in Mermaid or ASCII), then implement it in the generator.

**3.1 Address map**
- `/fractal2` — the intro (this page).
- `/fractal2/<sector>` — each sector home (e.g. `/fractal2/entertainment`).
- `/fractal2/<sector>/stage-<stage>` — stage pages with every tactic anchored.
- `/fractal2/<sector>/family-<family>` — the combo families.
- `/fractal2/<sector>/<combo-slug>` — combo pages.
- Plus `/fractal2/<sector>/standards`, `/a-z`, and a site-wide `/fractal2/tactics` and `/fractal2/combos` index across all sectors.
- Keep flat `.html` files and absolute links. Remember the trailing-slash proxy trap (CLAUDE.md).
- Decide whether each sector is its own Netlify site behind a hub rule (current ENT setup) or all of `/fractal2` is one site. Recommend with reasons: size, deploy isolation, the 450 MB MCP limit.
- The ENT build's base path is set in `design/fractal-sector/build.py` (`self.base = "/fractal/" + data["slug"]`). Make it a single configurable constant and plan the move to `/fractal2/<sector>`, including a permanent redirect from the old address and from `fractal-entertainment.netlify.app`.

**3.2 Identity keys (so everything can link, forever)**
- Tactics: the **standard id** (e.g. `S1-001`, also T-number `T001`) is the same across sectors. Every tactic page anchor gets a "This tactic in other sectors" link set once more sectors exist.
- Combos: **`combo_id`** (e.g. `C018`) is the same across sectors. Combo pages get "This pattern in other sectors". The hook already exists in `build.py` (`content/fractal/_crosslinks.json`); generate it automatically from every built sector.
- Names: resolve every tactic name through `content/decoder-v20/alias_map.json` and `standard_index.json`. This fixes the 131 currently unresolved combo-tactic mentions listed in `content/fractal/ent/build/audit.md`. Names that are Decoder *patterns* (Gaslighting, DARVO, FOG, Trauma Bonding…) link to their Decoder pattern page. Anything still unresolved stays plain text and is listed. **Never guess.**

**3.3 Navigation model**
- Global: the depth rail on the intro; a persistent sector switcher; breadcrumbs (`The Fractal / Fractal² / Entertainment / Exit Prevention / The Debt Prison`); a search across sectors (a prebuilt JSON index, a few KB per sector, vanilla JS).
- Lateral links:
  - tactic → combos it appears in;
  - combo → its tactics in order;
  - combo → family siblings;
  - tactic or combo → the same id in other sectors;
  - tactic → its Decoder entry;
  - sector → its chapter in The Fractal (where `library/fractal/<slug>.html` exists);
  - stage → its divine inversion (Spiritual Lens).
- Entry points:
  - the homepage feature (homepage v17 belongs to another session's work — propose the addition and ask, don't edit);
  - the Fractal's sector chapter linking to its Fractal² field guide (connector links only, ask first — never change book wording);
  - Decoder tactic pages ("See it in the music industry");
  - search engines.
- Downloads: where each sector's PDFs live (`/fractal2/<sector>/pdf/...`) and how they are offered (the "Take it with you" box). Check whether the PDFs carry the credibility labels. If not, add a cover note so a download never reads as more certain than the web page.

**3.4 Future sectors**
One command per sector (`design/fractal-sector/run.sh <sector>`). Write the checklist a future session follows to add Music Festivals and Spiritual Communities (their packages are not in the repo yet): drop the package in `content/fractal/<sector>/source/`, run, review the audit, resolve tags, regenerate the cross-links, update the intro's sector list and the sitemap.

**3.5 Findability**
- Per-page title and description patterns.
- JSON-LD: `CreativeWorkSeries` for Fractal², `Article` for combos, `DefinedTermSet` for stages.
- Sitemaps per sector plus an index.
- `llms.txt` entries.
- Canonical addresses on the final domain.
- The hub's `robots.txt` lists sitemaps through `scripts/seo/build_site.py` (`FRACTAL_SECTORS`); update it rather than hand-editing.

---

## 4. Tag resolution: so the owner never has to verify examples

The scripts contain credibility tags (ENT counts: LEGAL CLAIM 301, COMMON INDUSTRY PATTERN 228, HYPOTHETICAL COMPOSITE 191, REQUIRES SUBJECT-MATTER REVIEW 82, VERIFIED SOURCE NEEDED 16, HISTORICAL EXAMPLE TO VERIFY 1), plus 551 Credibility Audit items. All of them, in context, are in `content/fractal/ent/build/review_queue.json`.

**Goal:** every item ends with a decision, so pages can say *what is true* instead of *awaiting review*, and nothing false is published.

**Method (write `design/fractal-sector/resolve.py` and the ledger `content/fractal/<sector>/build/resolutions.json`):**

1. **Descriptive tags need no verification.** HYPOTHETICAL COMPOSITE, COMMON INDUSTRY PATTERN and LEGAL CLAIM — JURISDICTION-SPECIFIC describe the *kind* of statement. Keep them as reader labels ("Composite", "Common pattern", "Varies by place"). Check only that each label fits its sentence; flag mislabels.
2. **Claims that need checking** (REQUIRES SUBJECT-MATTER REVIEW, VERIFIED SOURCE NEEDED, HISTORICAL EXAMPLE TO VERIFY, and every Credibility Audit item). For each:
   - **(a)** Classify it: a general pattern, a specific factual claim (number, law, date, named practice), or a legal or medical statement.
   - **(b)** Research it with web search where available. Prefer primary or authoritative sources (statutes, regulators, unions and guilds, peer-reviewed work, established trade press).
   - **(c)** Give a verdict:
     - **Verified** — keep it, and store the source URL and quote in the ledger.
     - **Accurate as a general pattern** — rephrase to general wording if it was over-specific.
     - **Overstated** — soften it, in the derived copy only.
     - **False or unverifiable as stated** — remove the specific claim or replace it with an accurate general statement, in the derived copy only.
     - **Jurisdiction-dependent** — keep, with a "Varies by place" label.
   - **(d)** Record confidence, the old wording, the new wording and the reason.
3. **Never fabricate a source.** If you cannot verify a claim and cannot make it accurate by generalizing, remove it from the derived copy and list it.
4. **Never edit the author's source files.** All changes live in a derived layer that `build.py` applies, keeping the word-count round trip honest: verify against source minus recorded changes.
5. **Safety content is never weakened.** Safety notes, escalation triggers and safer response language: correct errors, never remove routes to help.
6. Set each combo's `review_state` (`unreviewed` → `ai_resolved` → owner-approved `sources_verified`; extend the states and labels in `build.py`). Reader banner wording follows the state, e.g. "Checked against public sources, [date]." Get the owner's approval of that wording at checkpoint C.
7. **Fix the defects the audit already found:**
   - C144's index undercount;
   - the 131 unresolved names (via the alias map);
   - stage 6 named "Extract" in The Fractal and "Control" in the expanded book (present it as one stage);
   - technique numbers in the owner's "Practice" script that don't match the published list (don't quote numbers).

Run this for ENT now; build it so every future sector gets the same pass automatically.

---

## 5. The words: the final intro

Rewrite `intro-v4.md` into `content/fractal2/intro-final.md`. Read intro-v4, the blueprint and the owner's messages first.

- **Register:** powerful, organized writing in the owner's lens (psychological freedom and spiritual awakening, sovereignty, accountability). Not a fictional story, not a fact report. Signpost the lens once, the way the Spiritual Lens interlude does.
- **Movements:**
  - **I. What The Fractal saw, and what it led to:**
    - the shape: 8 stages, 30 techniques, 3 nested levels, 30 sectors, 2,700 examples, the dare;
    - every need has a gate, and the distortion of your relationship with the need;
    - the **Origin**: a thought pattern and parasite that installs wherever a real need, a power gap and a gatekeeper meet, needing structures, not villains, and *separate from those who drive it on purpose* (the three categories of intent);
    - the Mirror and the Chain;
    - the original frequency;
    - what every tradition tried to say (translation, not conversion; the way *down* to the kingdom within; the author's awakening drawn as a map for others);
    - the world today; seeing as the first step.
  - **II. The true map:** more than three hundred tactics per sector at three levels. Show one tactic at all three levels using real lines.
  - **III. The weapons no one names (the heart):**
    - combos multiply harm, because each tactic disables the defence against the next;
    - the **sequence is the weapon** (use real tactic chains from the scripts);
    - why precise understanding heals: inside one now, lived one before, never lived one;
    - each counterfeit points back to what it imitated;
    - "Why I made this", with the owner's facts exactly as given, none added.
  - **Close:** what this is for; a one-line safety note; the two doors.
- **Length and pacing:** 3,500–4,500 words, paced for scroll. Short paragraphs, set pieces that pair with visuals, one idea per screen at key moments.
- **Canon vocabulary:** original frequency; counterfeit / original; false god (the pattern, never a being); gatekeeper and flaming sword; the cage and the intent; the chain; the mirror; the kingdom within; sovereignty; "same cycle, different building, every building".
- **Voice:** second person carries the reader. The author's "I" is rare and hands back to "you". Grave, warm, precise. No AI tells: no stacked "it's not X, it's Y", no tricolon every paragraph, no em-dash confetti.
- **Exact numbers:** 2,700; "more than three hundred" (335) per sector; "more than a thousand" per sector; combos "hundreds" (203 master, 153 in the first sector).
- **Guardrails:**
  - patterns, never people;
  - no named villains;
  - label any scenario as a composite;
  - a short safety line;
  - contested science phrased as the owner's belief, not fact;
  - for "The Body Knows" and the War Map policy list, follow the owner's checkpoint A answer.

---

## 6. The experience: Apple-level single-page scroll

**Quality bar — hold yourself to it explicitly:**
- 60 fps on a mid-range phone. Animate only `transform` and `opacity` (and SVG stroke offsets). No layout thrash. CLS near 0. LCP under 2 seconds on throttled mobile.
- Motion that feels physical:
  - spring or bespoke cubic-bezier easing; no linear;
  - interruptible, and scroll-linked where the meaning is progression;
  - time-based where the meaning is a reveal;
  - durations 200–900 ms;
  - staggers that read as cause and effect.
- Restraint: one hero moment per movement; everything else quiet. Every animation must *mean* something. Name each effect with `animation-vocabulary`.
- Typography: a dramatic scale, a 60–75ch measure, optical sizing, real typographic quotes and dashes; maximum two families plus one mono.
- Visual system: one accent; a strict spacing scale; consistent mark specs across all visualizations (`dataviz` / `refactoring-ui`).
- Choose one of two visual directions at checkpoint B. For example:
  - (1) an evolution of the sector field-guide look (cream paper, brush headings, highlighter) — continuity with the PDFs;
  - (2) a cinematic "descent": a dark world that grows lighter as the reader goes down, resolving into warm light at the frequency.

**Required visualizations**, each anchored to its passage, each with a full text equivalent:
1. **The fractal** resolving from one shape into nested scales (opening).
2. **The 8-stage ring** drawing itself, then **inverting** into the divine principles (Election, Covenant, Inherent Worth, Truth, Community, Abundance, Unfailing Presence, Irreplaceable Worth).
3. **Nested levels**: person ⊂ institution ⊂ civilization ⊂ pattern ⊂ person.
4. **30 gates**: each sector lights with "your relationship with ___" and its gatekeeper. Data: the dominion table in `A-…` and the 30 gardens in `the-spiritual-lens.html`. Nodes link to existing Fractal chapters.
5. **The Origin's three conditions** (need · power gap · gatekeeper) converging, and the pattern appearing where they meet.
6. **The Chain**: four generations passing the signal down.
7. **Counterfeit ↔ original pairs** (faculties table; The Frequency's 30 counter-practices).
8. **30 → 335**: the map multiplying across the 8 stages.
9. **The combo multiplier**: links that each disable the next defence; harm compounding, not adding; then one link breaks and the whole chain falls.
10. **The descent**: a depth rail and progress spine that ends at the frequency.

**Engineering (binding, from CLAUDE.md):**
- One self-contained page plus same-folder fonts if needed. No CDN, no frameworks, no external scripts.
- Inline SVG, or Canvas where SVG is too heavy. Self-hosted fonts from `tools/fonts/` (subset to woff2).
- CSS scroll-driven animations where supported, with an IntersectionObserver fallback.
- The only external request is the existing Cloudflare beacon. Keep THE HOUSE drawer (`design/decoder-v10/assets/house.html`).
- Prose lives in the HTML, not injected by JS.
- **Reduced motion delivers everything statically.** Nothing is ever stuck invisible. Full keyboard and screen-reader paths (each visualization has a text alternative or table). WCAG 2.2 AA in light and dark. 44px targets. No horizontal overflow at 375px.
- Section deep links (`/fractal2#origin`, …), a quiet progress rail with labelled markers, a collapsible mini-nav on phones, and an "updates" section with the version badge (CLAUDE.md "Patch notes & versioning").
- SEO: title, description, canonical `https://noblefathercreations.com/fractal2`, OG image (render it with Playwright), JSON-LD.

---

## 7. Process and deliverables

1. Inventory tools and skills (section 1). Write the "What I understood" note. **Checkpoint A.**
2. `content/fractal2/FINAL-PLAN.md` (Sequential Thinking): outline and word budgets, a visualization storyboard (what appears at which line), interactions, the link map, a performance budget, and risks. Stress-test it with `grill-me`. Build two direction prototypes. **Checkpoint B.**
3. `content/fractal2/ARCHITECTURE.md` + generator changes (base path, cross-links, alias resolution, search index, downloads), verified on ENT.
4. Tag resolution for ENT (section 4). **Checkpoint C.** Then apply it and rebuild ENT.
5. `content/fractal2/intro-final.md`. Run `copy-editing` and `no-ai-slop` over it.
6. Build the page: source in `design/fractal2/`, output in `library/fractal2/site/` (record the paths in `sites.json` as an undeployed project, `pendingDeploy`).
7. **Verify** (write `design/fractal2/verify.mjs`, modelled on `design/fractal-sector/verify.mjs`):
   - Playwright screenshots at 375 and 1440, light and dark, reduced motion, and at every visualization's scroll position;
   - `pageerror`, overflow and opacity-stuck checks;
   - axe-core (`npm i --no-save axe-core`);
   - every internal link resolves;
   - a long-task and frame-timing sample while scrolling;
   - ENT `run.sh` still passes, word-count round trip adjusted for recorded resolutions.

   **Look at your screenshots before you claim anything works.**
8. Critique passes: `impeccable` critique → polish; `review-animations`; `web-accessibility`; `web-perf`; one independent subagent review (`impeccable-finish-reviewer` or `visual-storyteller`). Fix what they find.
9. **Checkpoint D.** Report to the owner in plain language:
   - what you built, with screenshots;
   - the tag-resolution summary;
   - the architecture in one diagram;
   - what is ready to deploy and exactly what deploying would change (in plain words, including routing);
   - the open questions.

---

## 8. Definition of done

- The intro reads as the owner's most powerful work, organized and in their lens.
- All ten visualizations work, mean something, and degrade gracefully.
- Navigation links every tactic, combo, sector, Fractal chapter and Decoder entry by id, with nothing guessed.
- Every tag in ENT has a recorded decision, nothing false remains in reader text, and safety content is intact.
- All checks pass, screenshots have been reviewed, and nothing is deployed.

## 9. Things that are already decided (don't reopen)

- Everything lives on noblefathercreations.com; no new domains. Sector pages carry receipts and labels; the intro is the storyteller register.
- Tactics go on stage pages with anchors, not one thin page each. Combos are the pages built to rank.
- No Figma, Canva or Adobe in the build; no site frameworks; Python stdlib generator and Playwright checks.
- Production cues (`[SPEAK]`, `[HARD CUT]`) and the Credibility Audit never appear on reader pages. Internal ids are never shown to readers. Safety notes always come first.

## 10. Context you must not lose

- The ENT field guide is currently public at `fractal-entertainment.netlify.app/fractal/entertainment` (not linked or submitted anywhere). It was deployed further than the owner intended. Treat its future address as part of your architecture, and confirm it at checkpoint A.
- Hub routing for `/fractal/entertainment` is committed but not deployed (`sites.json` → `hub.pendingDeploy`). Do not deploy it. Replace it with the `/fractal2` routing in your plan.

## 11. Absolute rules

- **Do not deploy anything.** The owner names each deployment in the conversation; a preview must be private. If "live" is ambiguous, ask.
- Before any production action, fetch all branches and run `node scripts/verify-deployed.mjs`. Another chat's work may be live and ahead of this branch.
- Never edit the owner's scripts or source files. Never change wording inside published books (connector links only, ask first).
- Patterns, never people. A short safety line on every page.
- Commit and push to `claude/great-keller-jkjz8c` as you go. Update `MEMORY.md`, `content/fractal2/HANDOFF.md` and `DECISIONS.md`.
