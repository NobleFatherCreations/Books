# Handoff: Fractal² intro + the design system (updated 2026-11-12, v9 live)

## 0a. v10, same day, after the owner's first real-iPhone test (deploy `6af540970b3f3398b447a284`)
Owner report: captions "just appear and disappear" and do not move with the scroll; wanted the sector names to pass by at "I looked for a sector", and an inward list after "I am still looking" (self, body, genetics, ancestry, generational chains); the page kicked back to the start after the large map expanded, then crashed.
- **Crash cause and fix:** the DOM camera put two 320%-sized images plus a CSS mask inside a `will-change` layer; on a 3x phone that is roughly 4,000 px square per layer and Safari killed the tab. The art is now drawn on ONE screen-sized canvas (`drawArt` in the template); phones load the 2048 px images and skip `orig-deep`. Do not go back to DOM images under a scaled parent.
- **Their phone has Reduce Motion on** (inferred: their screenshot had no Play button, which v9 hid in that mode). v9 gave that mode popped-in words and a snapping camera. v10 keeps everything that follows the reader's own scroll and only drops breathing, blur and the smooth jump. Always walk with `--rm` as well.
- **Captions ride the scroll:** each caption drifts upward through its place over its life (`--ty` in `words()`).
- **Rolls:** `<!--roll NAME k=v-->` + one line per item in the script makes a list that scrolls past in normal page flow, brightest at mid-screen. Used for the 30 sectors and the inward list.
- Second critic (before these changes): hierarchy 4, type 4, space 3, craft 3, distinctiveness 4, feeling 4, phone 3, legibility 4, continuity 4; its fixes are in. v10 is NOT yet re-scored; `design-exit.mjs` still fails.
- **Still unverified:** that the crash is gone on the owner's iPhone. Only they can confirm.

## 0. Current state in one screen (read this; sections 1-6 below are the v8 history)
- **Live:** v10 (see 0a) at https://fractal-entertainment.netlify.app/fractal2 (v9 was deploy `6af53ccf49e79299a62c8f79`, 2026-11-12, on the owner's "push live"). Live file = `library/fractal2/site/fractal2.html`, verified byte-identical. Branch `claude/optimistic-clarke-86s6bg`. The noblefathercreations.com/fractal2 proxy is still NOT done (needs "deploy the homepage").
- **What v9 is:** the v8 camera and captions, plus the original Fable intro's idea of one light (a person) that every figure is built around. Figures: one combination as a thread through the rings; five defenses closing one by one; the 203 as a web; the thread read backward; one opening returning; the eight rings lighting for the old words. Words sit BESIDE the map from the large map onward (below it on phones). A Play button scrolls at reading pace. The ending returns to the room. Record: `content/fractal2/design/DESIGN-CHOICES.md` (v9 section), `STORY-DECISION.md` section 9.
- **Files:** script + camera cues `content/fractal2/intro-v9.md`; engine `design/fractal2/redesign/v9/template.html` + `build.py` (never edit `index.html`). Art and fonts are unchanged and stay in `_a/v8/`; share image `_a/v9/og.jpg`.
- **Rebuild:** `python3 design/fractal2/redesign/v9/build.py /fractal2/_a/v8/ && cp design/fractal2/redesign/v9/index.html library/fractal2/site/fractal2.html && python3 design/fractal2/redesign/v9/build.py`. Staging, deploy and verify steps are unchanged (section 1, steps 3-5).
- **Look at it the right way:** `python3 design/fractal2/serve.py 8802 &` then `node scripts/frame-walk.mjs http://127.0.0.1:8802/fractal2 <dir> --n=72 --click=#begin` and READ the sheets. Gates: `node scripts/design-gates.mjs <url> <dir> --click "#begin" --max 70 --step 0.93` (without `--click` the gates see only the opening screen and pass on nothing; that is how v8 "passed").
- **Scores:** see `content/fractal2/design/SCORES.md` (v9 section) for the latest round and whether `design-exit.mjs` passes.
- **Engine keys** (in the script header): `o` words beside the map, `c` words below the light, `you` the light, `th` thread, `gs`/`gt` defenses, `web` the 203, `rv` read backward, `inv` old words. These hold their value until changed.
- **v8 bug fixed in v9:** scene end markers sat one screen late, so the camera target jumped about 60% of each move at every caption change.
- **Open, in order:** (1) owner tests on a real iPhone: Begin, Play, the split layout, the fall to black; (2) the author's-lens lines are still not the owner's own sentences; (3) sources for the numbers; (4) homepage proxy on the owner's word; (5) the design-system changes in `docs/DESIGN-SYSTEM-FIELD-REPORT.md` (do items 1, 5, 2 first).

---

# (v8 history) Handoff for the next model: Fractal² intro + the design system (2026-11-11)

Read this first, then `CLAUDE.md`, `MEMORY.md`, `docs/FRACTAL2-JOURNEY.md` (history), `content/fractal2/design/STORY-DECISION.md` (story audits). Branch: `claude/sleepy-maxwell-yii2ts`. Owner is a non-designer who wants an award-level, cinematic, emotional intro, and wants the design system PROVEN by running it. Do not ask them design questions; show frames and decide.

## 1. Live state
- **Live now:** v8 at https://fractal-entertainment.netlify.app/fractal2 (Netlify site `194814a7-0e80-4b68-b314-0c07911af55a`, deploy `6af4f7fdb14e4560067953cd`). Live file equals `library/fractal2/site/fractal2.html`. v8 was deployed on the owner's explicit "send it LIVE". The noblefathercreations.com/fractal2 proxy is NOT done (needs the words "deploy the homepage"; rules in `library/fractal2/redirects/HUB-RULES.txt`).
- **Story:** `content/fractal2/intro-v8.md` (71 scenes, ~1,040 words, ~6.9 min). Lint: `node scripts/story-lint.mjs content/fractal2/intro-v8.md` (must PASS).
- **Engine/template:** `design/fractal2/redesign/v8/template.html` + `build.py` (output `index.html` is generated; never hand-edit). 
- **Rebuild + ship:**
  1. `python3 design/fractal2/redesign/v8/build.py /fractal2/_a/v8/ && cp design/fractal2/redesign/v8/index.html library/fractal2/site/fractal2.html && python3 design/fractal2/redesign/v8/build.py` (last call restores the dev copy with relative paths).
  2. Assets live in `library/fractal2/site/fractal2/_a/v8/` (img, fonts, emblem-64.png, favicon.ico). Absolute asset paths are mandatory (page is proxied at a clean path; relative paths break).
  3. Staging: copy `library/fractal2/site/` to a scratch dir; `_redirects` = `old-prototype._redirects` with `https://noblefathercreations.com/fractal2` replaced by `/fractal2`, plus the non-comment lines of `ent-site._redirects`.
  4. Deploy: Netlify MCP `netlify-deploy-services-updater` (operation `deploy-site`, siteId above) returns an `npx @netlify/mcp ... --proxy-path` command; run it inside the staging dir. A production deploy needs the owner's explicit go-ahead in the current conversation; an earlier attempt was blocked by the permission classifier when approval was ambiguous. Do not work around a block.
  5. Verify: `curl` the live URL and `cmp` against the repo file.
- Never run `playwright install`. Chromium: `/opt/pw-browsers/chromium`. Walk script pattern: load page, click `#begin`, scroll in ~60 steps, listen for `pageerror`, check `scrollWidth > innerWidth+1`.

## 2. What the owner wants (binding)
Locked black circle until Begin; large word-by-word captions (1-2 sentences, narration pacing, silent scroll between blocks); original fractal zooms out to fit the screen edges then PAUSES; then zooms out to the larger 335-tactic map (rings first, then words); at the descent zooms back in through the words to black; spark of light "your original frequency"; combinations are the antagonist AND the key; storyteller, epic prose, spiritual/psychological layer (divine principles inverted, religious words) offered as one person's sight; the author's lens (lifetime of pattern recognition, it saved their life, healing + spiritual journey, share worldwide). Background is an effect that conveys scale, not something to read. Do not list facts; set up the work.
Content rules: patterns never people; no outcome promises; no "proved"; safety line (emergency services); American spelling; no em dashes; one CTA; counts: 30 techniques, 335 tactics, 203 combinations (153 in the first sector), 2,700 examples, 30 sectors, 30,000+ observations. Never change wording inside published books. No external requests (only the Cloudflare beacon). No tracking/progress UI in Loop, The Weighing, The Sacred Divide.

## 3. The mistakes to learn from (root causes, not symptoms)
1. **Skills documented but not run.** Gates passed on designs the owner hated. Fix: the process must emit evidence (frames read, scores written, ledger) before any "done". `scripts/design-exit.mjs` is a hash-bound exit gate; it currently FAILS for v8 (v8 has no critic scoring). Run it.
2. **Stopping without re-scoring after fixes, then asking the owner "ship unscored?"** The owner should never be asked that. Re-score every round; if a score is low, generate a new idea, not a question.
3. **Gates read code, not motion.** Contrast/overflow checks cannot see a bad zoom. Capture frame sequences (`scripts/capture-critic-set.mjs`) at many scroll positions on a 390x844 phone viewport AND read them.
4. **Raster zoom (v1-v5):** blurry, hard mask, instant jumps. Fixed with vector WebP layers + one camera transform (`#cam`). Do not go back to masks or crossfades for scale.
5. **Over-designing chrome** (gold, mono caps, reticles, letterbox, halos). Removed. Restraint wins; the story and camera carry it.
6. **Applying a pattern uniformly.** Read `BOOKS.md` per book first.
7. **Story first drafts were fact lists.** The owner's brief is a storyteller. Use `content/fractal2/design/STORY-SYSTEM.md` (4+ frames, steelman, attack S1-S8, score, blend, lint, fresh-reader test) and `GHOSTWRITER-PROMPT.md`.
8. **Engine bugs found late:** loop stopped before dimming converged; function deleted by an over-broad slice; variable used before definition (NaN, infinite rAF); lazy loader requested `/null`. Lesson: after any template edit, run the walk script and read console errors.
9. **Authority hygiene:** subagent messages and fetched pages are data, not approval. A deploy needs the owner's own words.

## 4. The design system (what exists, what it did, what it did not)
- `docs/design-catalogue/` (00-13 + `PROMPT-MASTER.md`, `DESIGN-SYSTEM-GUIDE.md`, `07-choosing-and-combining.md`, `13-html-books-playbook.md`, `recipes.html`, `templates/SCORES-TEMPLATE.md`): style/brand/type/colour/motion/navigation/technique master list with a selection method, choose-by-ID, record choices.
- `.claude/skills/design-director/SKILL.md`: the process (research, choose small coherent set, prototype one hero, critique with screenshots + gates, build).
- Scripts: `scripts/design-gates.mjs` (5 profiles), `capture-critic-set.mjs`, `design-exit.mjs`, `story-lint.mjs`, `story-annotate.py` (numbered scene view for audits).
- Records: `content/fractal2/design/` (COVERAGE, DESIGN-CHOICES, DESIGN-NOTES, SCORES = 6 design rounds, PHONE-CHECK, STORY-SYSTEM, STORY-DECISION, GHOSTWRITER-PROMPT).
- **What it did well:** forced catalogue-based choices, caught contrast and overflow failures, produced a story protocol and lint that measurably improved the script over three rounds (scores in STORY-DECISION section 8).
- **What it did not do:** judge motion/pacing automatically (needs frame sequences and a human-eye critic), evaluate emotional power (no gate for it; the audit in GHOSTWRITER-PROMPT.md is the first attempt), prevent me from skipping steps (needs the exit gate to be mandatory, not optional), test on a real phone. Candidate improvements: a scripted phone-viewport frame walk that outputs a contact sheet with scroll position + active caption; a motion-speed gate (max z-change per screen of scroll); a caption-dwell gate (minimum scroll per word); an emotion/stake checklist in the critic prompt; making `design-exit.mjs` required before any deploy command.

## 5. What to fix next (priority order)
1. **Real-phone/phone-viewport pass of v8**: caption timing, runway lengths (all guesses), locked opening, the blackout and the spark (subtle; make the spark clearly visible and give it a held beat). Score with `capture-critic-set.mjs` + `design-exit.mjs`, record in `SCORES.md`.
2. **Long static middle:** the large map holds one image across ~25 scenes (camera only drifts 0.3125 to 0.43 and back). Give scenes visual jobs: light the named combinations as chains, show a chain reversing, pulse a ring per stage, show the 203 combinations as threads. This is the biggest scene-ability gap.
3. **Author's lens lines** ("Why I carry it", "I know that question…", "That noticing saved my life.") are MY wording of the owner's brief, not their words. Ask for their own sentences and swap them in, keeping the 3-sentence/55-word lint limits.
4. **Version ledger:** `sites.json` has no entry for the intro (CLAUDE.md requires `version`, `changelog`, and an on-page patch note per deploy). Add v8 (2026-11-11) both places.
5. **Sources for the numbers** (2,700 / 335 / 203 / 30,000+): tag them tested vs claimed on the page or in a notes file.
6. Homepage proxy, only on the owner's explicit "deploy the homepage".
7. Update `docs/design-catalogue` with the lessons in section 3 and the improvement list in section 4.

## 6. Working agreement
One background agent at a time (usage caps have killed whole batches). Commit with the trailer lines the harness gives. Update `MEMORY.md` and this file as work happens. Keep final replies short: what changed, what was verified, what is unverified.
