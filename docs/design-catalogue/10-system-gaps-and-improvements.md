# 10 — The ten biggest gaps and improvements in the design system

Written 2026-11-10, after building the catalogue, the rules, the gates script and the guide. These are the weaknesses I would fix first, ranked by how much they threaten the goal ("award-level, not generic, and the owner can trust it").

For each: **Gap → Why it matters → Fix → Effort.**

## 1. Nobody has proved the system works
- **Gap:** the process has never been run end to end, and there is no comparison against "no system".
- **Why:** every rule here is a plausible guess. Without a test, we could be adding ceremony that doesn't improve the result.
- **Fix:** a **bake-off** on one real brief (for example the Fractal² intro): Run A uses the plain brief; Run B uses `/design-director`. Same model, same time budget. The owner judges blind (screenshots labelled X and Y). Record which system rules were followed and which results the owner preferred; adjust the rules from the evidence.
- **Effort:** one design session of each kind plus 15 minutes of the owner's time.

## 2. The reference library is names and text, not images
- **Gap:** the catalogue and the winners data describe sites in words. The model never *sees* a standard of excellence unless it screenshots a site that session.
- **Why:** taste is learned from looking. Words let it recite techniques while still drawing something average.
- **Fix:** build `references/` with real screenshots (390 and 1440) of 50–100 vetted sites across genres, each with a one-line "what to steal / what to avoid", plus a small script that re-captures them. The benchmark step compares new work against these images side by side. Start with the 13 researched winners in `09`.
- **Effort:** a few hours of Playwright capture; refresh quarterly.

## 3. Award winners are the wrong benchmark for many jobs
- **Gap:** the `09` data shows winners score highest on animation (7.2–9.6) and lowest on accessibility and semantics (6.4–7.6). The system risks pushing reading, care and tool pages toward spectacle.
- **Why:** the Fractal² intro is a long read for possibly stressed readers; spectacle can hurt it.
- **Fix:** maintain **benchmark sets per job type**: (a) showcase/story (award winners), (b) reading-first (Aeon, The Marginalian, Quanta, NYT long-reads, Stripe Press), (c) tools/product (Linear, Stripe docs, Vercel), (d) public-service and care (GOV.UK, NHS, crisis services). The interview picks the set; the benchmark step compares only within it.
- **Effort:** half a day to assemble and capture the sets.

## 4. The self-contained rule has no explicit library policy
- **Gap:** most winning sites run on Three.js, GSAP, Unity pipelines, custom WebGL. `CLAUDE.md` forbids external requests and expects no dependencies; the catalogue says "ask the owner". Nobody has decided.
- **Why:** without a decision, a model either breaks the rules or falls back to CSS-only, which caps quality and produces the generic look.
- **Fix:** the owner decides one of: (A) no libraries, native only; (B) a small **approved local stack** vendored into the repo (for example a minimal WebGL helper plus a GSAP-class animation library) with licences and size budgets recorded; (C) per-project approval. Write the decision into `CLAUDE.md` and the guide. Add a `vendor/` folder policy with checksums.
- **Effort:** 10 minutes of the owner's decision; an hour to vendor and document.

## 5. Motion is not verified
- **Gap:** the gates take screenshots at rest and count running animations. Nothing checks that motion looks good, stays in sync with scroll, or holds frame rate.
- **Why:** "no motion without meaning" and "buttery" are core to top-tier work and to the original complaint ("no animations").
- **Fix:** extend the gates to record **filmstrips** (frame sequences while scrolling at a fixed rate), contact sheets the model must read, **frame-time and long-task measurements under CPU throttling**, and a scroll-sync check (does the figure's progress match scroll position). Optionally record a short Playwright video for the owner.
- **Effort:** a day of scripting.

## 6. The gates check collisions, not pixels
- **Gap:** overlap tests use element boxes. They can't see what is drawn behind text, whether the palette is coherent, or whether type sizes are chaotic.
- **Why:** legibility over a background figure was flagged only as "read the screenshot".
- **Fix:** add **pixel-level checks**: contrast sampled from the rendered image behind every text block (not just CSS colours); dominant-colour count (limit hues); distinct font-size count and scale-ratio audit; whitespace and visual-weight maps; saliency check (does one focal region dominate); token consistency (radii, shadows, spacing); a perceptual diff against the owner-approved hero to catch regressions.
- **Effort:** one to two days.

## 7. There is no real iPhone Safari test in the loop
- **Gap:** all testing is Chromium emulation, yet the owner's complaint came from iOS Safari.
- **Why:** iOS differs (viewport units, sticky, backdrop-filter, memory, scroll-linked effects).
- **Fix:** (a) check whether Playwright's WebKit engine can be used in this environment (instructions forbid `playwright install`; test if a WebKit build is already present); (b) otherwise provide a **private preview link** plus the 10-step phone checklist as a mandatory gate, with the owner's screenshots fed back into the loop; (c) consider a cloud real-device service if the owner approves.
- **Effort:** an hour to check; ongoing owner time of five minutes per round.

## 7b. (grouped with 7) Performance on weak phones
- The performance budget is stated but not measured on a throttled mid-range phone profile in the gates. Add Lighthouse mobile runs and a CPU 4× throttle pass to the script.

## 8. Critique comes from the same kind of mind
- **Gap:** the "independent critic" is another instance of the same model family. Blind spots are correlated, and self-scores drift upward.
- **Why:** it can approve what a human finds ugly.
- **Fix:** add a **five-second test** protocol with real people (three friends see a screenshot for five seconds on a phone and answer: what is this, what do you remember, what felt off); a **blind A/B** where the critic sees two unlabeled designs; and keep the owner's plain-word reactions as the final authority. Log every critique outcome so the rules can be tuned.
- **Effort:** 15 minutes of other people's time per round.

## 9. Nothing remembers the owner's taste or the lessons between sessions
- **Gap:** each new session re-interviews from scratch; lessons from rejected designs are lost; long runs get compacted mid-way.
- **Why:** repeating mistakes is why the owner is frustrated; very long sessions lose state.
- **Fix:** create `OWNER-TASTE.md` (the owner's confirmed likes/dislikes, A/B pair results, banned clichés, favourite references, words they use for problems and what each meant), updated after every round, and read before the interview so it only asks what is new. Add `DESIGN-STATE.md` per project (phase, decisions, open issues, next step) committed after every phase so any session can resume. Add a **feedback log** mapping plain-word complaints ("too busy", "cold") to concrete rule changes.
- **Effort:** two hours to set up; a few minutes per round to maintain.

## 10. No asset pipeline: the best sites depend on assets the AI can't easily make
- **Gap:** winners rely on bespoke photography, 3D models, illustration and sound (Opal's photography and 3D; Igloo's Houdini-generated ice and sound design; Persepolis's historian-built reconstruction). The system describes styles but has no plan for producing the assets, so the AI substitutes thin dots, gradients and stock-looking shapes.
- **Why:** this is a direct cause of "specks for art" and generic output.
- **Fix:** add an **asset strategy** step before choosing: for each visual, state whether it is (a) generated in code (particles, procedural geometry, SVG, shaders, data-driven figures), (b) generated with an image or video tool (with rights and disclosure rules), (c) needs commissioned or owner-supplied work, or (d) typographic only. Mark placeholders clearly, and design so the layout works with strong typography alone if assets are weak. Document available generation tools (Figma, Adobe, ElevenLabs, Canva, Higgsfield when connected) and their limits. Add procedural-asset recipes (growth algorithms, flow fields, SDF text, noise, point clouds from glyphs) to the catalogue's techniques with working code snippets.
- **Effort:** a day for recipes; ongoing per project.

---

## Suggested order
1. Decide the library policy (item 4) — 10 minutes, unlocks quality.
2. Run the bake-off (item 1) on the Fractal² intro — gives evidence and fixes the live site.
3. Build `references/` (item 2) and benchmark sets (item 3).
4. Create `OWNER-TASTE.md` and `DESIGN-STATE.md` (item 9).
5. Extend the gates for motion and pixels (items 5, 6), then check iOS options (item 7).
6. Add the five-second human test and asset strategy (items 8, 10).
