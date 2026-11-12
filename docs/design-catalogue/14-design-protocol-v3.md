# 14. Design protocol v3: why it changed, what it is, and the steelman record (2026-11-12)

The skill itself is `.claude/skills/design-director/SKILL.md`. This file is the reasoning, so the skill can stay short.

## What went wrong with v2, from evidence
On 2026-11-12 the owner tested four deploys of the Fractal² intro on an iPhone in one day and found new faults each time: a crash, ovals, captions that did not move, captions that moved too fast, lists that played twice, a zoom that jumped. Every one of those builds had passed everything v2 asked for.

| Missing piece in v2 | Evidence | v3 answer |
|---|---|---|
| It never played the page. Gates took screenshots at rest. | Faults were all in motion or on resize. | `scripts/film-check.mjs`: a frame-by-frame pass at thumb speed with ten checks, via a page probe `window.__film()`. |
| Its tools could not get past a Begin button. | "PASS" on 2 screens of 66. | `--click` everywhere; film-check fails when the probe is missing. |
| Nothing connected a report to a test. | Fixing "words don't move" produced "words too fast"; fixing ovals produced "zoom jumps". | Law 2 + `REGRESSIONS.md`: the report becomes a failing check first. |
| The process was optional prose, about two hours of ceremony. | It was skipped under time pressure, which is always. | One command (`scripts/film-gate.sh`) that also wraps the deploy; three tracks sized to the job. |
| It asked the owner to judge what a machine can judge, and asked design questions they could not answer. | "I'm really annoyed that I report issues and new ones pop up every time." | Law 3, `OWNER-TASTE.md`, a four-question phone card for device-only risks. |
| Skills were listed, not scheduled. | None were invoked in the failing rounds; when invoked earlier they produced a plateau at 3/5. | N6: which skill, at which step, and drop it if it changed nothing. |
| Category coverage was a 56-row form. | Filled once, never read again. | N3: ten categories, ten minutes. |
| Fixes and polish shipped together. | Each "polish" changed mechanics under an open fault list. | Fix rounds add nothing; polish is its own release, one item at a time through the gate. |
| No list of mechanics known to fail. | The same class of fault (script-positioned text, percentage canvases) came back in new forms. | "Mechanics that are banned", each with its cause. |

## Steelman record
A steelman here means: state the strongest case that the new architecture still fails, then change it until that case no longer holds.

**Round 1. "The gate only tests pages that cooperate, in a browser the owner does not use."**
- Flaw A: a page without the probe is unchecked. Fix: missing probe = FAIL, and the probe contract is part of the skill (R4).
- Flaw B: Chromium is not iOS Safari; the crash and the toolbar jump were iOS-only. Fix: proxies that did predict them (`budget`: forced layers and canvas size; `toolbar`: resize the viewport by 84 px mid-scroll; `round`: buffer aspect vs CSS aspect) + a named list of device-only risks + the phone card. Residual risk stated, not hidden.
- Flaw C: checks cover yesterday's faults only. Fix: law 2 makes the suite grow with every report; the ledger shows coverage.
Verdict after fixes: still fails on "the agent can skip it".

**Round 2. "It will be skipped or gamed, like the last gate."**
- Flaw D: nothing forces the gate before a deploy. Fix: `film-gate.sh ... -- <deploy command>` runs the deploy only after a pass; the handoff's deploy recipe uses that form.
- Flaw E: thresholds could be loosened to pass. Fix: each threshold is printed with its limit in the output and explained in the script header; changing one requires a line in `REGRESSIONS.md` saying why. A critic or the owner can see a loosened limit.
- Flaw F: the frame-rate-dependent check gave different results on a slow machine (it did, in development: 6% passed with reduced motion and failed without). Fix: smoothness is judged on the scripted camera per screen of scroll (deterministic); rendered-frame numbers are reported, not gated.
Verdict: holds for mechanics; fails on "a mechanically perfect film can still be ugly or flat".

**Round 3. "Passing the gate says nothing about beauty or feeling, which is what the owner actually wants."**
- Flaw G: true, and no script fixes it. Fix: the gate writes contact sheets and the skill requires reading them and describing frames; one independent critic with a fixed rubric and frame citations (R5); `OWNER-TASTE.md` carries what this owner finds beautiful so it is not rediscovered by trial on them.
- Flaw H: critics are noisy and can be over-trusted. Fix: a critic's claim without a frame file is ignored; scores are evidence; the owner's reaction outranks any score and is written into OWNER-TASTE the same day.
- Flaw I: the process could still be too heavy for a one-line fix. Fix: the Fix track is five steps and adds nothing unrequested.
Verdict: the remaining objections are the stated limits (beauty needs eyes; iOS needs the phone). No objection remains that a change to the architecture would remove. The steelman passes with those two limits named.

## What a stronger model could add next (not built)
1. WebKit in the container (`--engine webkit` exists in design-gates but the browser is not installed) to close most of Flaw B.
2. A contrast sampler for text drawn on canvas (the "too dim" report is the one row in REGRESSIONS with no guard).
3. Frame-sequence video of the pass for the critic, so motion is judged as motion.
4. Per-project threshold file with reasons, instead of constants in the script.
5. A "callback" rule in story-lint (an image from the opening must return at the end).
