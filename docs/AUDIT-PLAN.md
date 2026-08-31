# Full Audit Plan — every page, every tool, zero wasted deploys

Standing constraint: **nothing deploys until a site's entire package is
finished and reviewed.** Font fixes ride along with everything else in one
deploy per site. Verification happens locally (Playwright + a local HTTP
server) at zero Netlify cost — deploy credits are only spent once per site,
at the very end.

This plan is built on a real baseline, not estimates. Everything in the
"Baseline" section below was actually run before this plan was written.

---

## 0 · The efficiency unlock (already built)

These books are 0.1–11MB single files, which historically made them
"too big to audit" — the review package's own doc says impeccable's
detector "times out on files over ~3MB."

**That's now solved.** 85–99% of each file is embedded base64 images/fonts,
not markup. `design/prep-audit.py` strips those payloads into analysis-only
copies:

| Page | Real size | Stripped | Actual markup |
|---|---|---|---|
| catalogue (hub) | 10.7MB | 103KB | 1.0% |
| portals | 10.4MB | 114KB | 1.1% |
| faith | 4.7MB | 2.7MB | 57% |
| loop | 1.6MB | 231KB | 14.5% |

**Every one of the 16 pages now fits under the 3MB detector limit and fits
comfortably in an agent's context.** This is what makes a full audit of all
16 pages tractable instead of prohibitive.

- `design/prep-audit.py` → writes analysis views to `.audit-view/` (gitignored)
- `design/run-detector.sh` → batch-runs the detector, emits a summary table

Analysis views are **read-only**. Never edit or ship one — fixes always go
to the real source file.

---

## 1 · Baseline already captured (mechanical sweep, complete)

Ran the 59-rule deterministic detector across all 16 pages. **310 raw
findings.** No LLM, no API key, ~2 minutes, repeatable any time via
`design/run-detector.sh`.

| Page | Raw | Dominant tags |
|---|---|---|
| faith | 72 | 57 side-tab, 12 overused-font |
| faith-index | 59 | 56 side-tab |
| reaction-map | 43 | 27 overused-font, 13 side-tab |
| divide (Sacred Divide) | 36 | 34 side-tab |
| scale | 17 | 12 overused-font, 4 side-tab |
| loop | 16 | 12 overused-font, 3 side-tab |
| fractal | 14 | 11 side-tab |
| playground | 13 | 5 side-tab, 3 bounce-easing |
| sovereign | 10 | 5 side-tab |
| root | 5 | 2 overused-font, bounce-easing |
| fracture | 5 | 2 overused-font |
| portals | 5 | 2 overused-font, radial-halo |
| catalogue (hub) | 4 | 2 overused-font, gradient-text |
| festival (wook) | 4 | overused-font, layout-transition |
| seals | 4 | broken-image, dark-glow |
| festie-codex-full | 3 | layout-transition, dark-glow |

### Critical: most of the volume is NOT a defect

I checked the top findings rather than trusting the count:

- **`side-tab` (~190 instances, 61% of all findings)** — these are
  `border-left:3px solid var(--gilt)` / `var(--glow)` / `var(--wax)` /
  `#8A2432`. That is **your gold-and-crimson accent language** — callout
  boxes, chapter cards, and the "you are here" marker in THE HOUSE nav.
  `CLAUDE.md` explicitly says preserve numbered chapter cards. Mechanically
  "fixing" these would erase the brand. **Needs your judgment call, not a
  fix — see Decision D1.**
- **`overused-font` Fraunces (~60)** — the review package's bootstrap doc
  names Fraunces as the *pinned brand face*, known-deliberate. Ignore.
- **`em-dash-overuse`, `gradient-text`, `dark-glow`** — bootstrap doc lists
  all three as known-deliberate (author's voice, gold-leaf gilt identity,
  candle glows as literal light sources in the world). Ignore.
- **`broken-image` on seals — I checked it: false positive.** The `<img>`
  has no `src` attribute but JS assigns one at runtime. Not a bug. (Minor
  real note: it's a fragile pattern on a commerce hero, and
  `fetchpriority="high"` on a src-less img does nothing.)

**Genuine mechanical findings after filtering: roughly 15–20, not 310.**
Mostly `bounce-easing` (4: playground, root — dated easing),
`layout-transition` (~9), `radial-halo` (3).

---

## 2 · The real headline finding (unchanged, now quantified)

**11 of 16 pages load fonts from Google's CDN**, violating the
self-contained rule. Live in production right now on portals, seals,
reaction-map, and root.

Correct already (self-hosted, zero external font requests): **loop (20
`@font-face`), scale (20), faith (23), faith-index (3)**. These are the
model.

Fonts needed to fix the rest — 3 of 7 already vendored:

| Font | Have it? |
|---|---|
| Fraunces, Newsreader, Public Sans | ✅ `tools/fonts/` |
| Hanken Grotesk, Jost, IBM Plex Mono, Space Mono | ❌ pull via sparse checkout |

---

## 3 · Reviewer assignment — one owner per concern, no overlap

The trap to avoid: running ui-designer *and* ux-researcher *and*
brand-guardian *and* emil-design-eng *and* `impeccable critique` on the same
page produces five overlapping opinions and burns budget for one answer.
Each concern below has exactly **one** owner.

| # | Concern | Owner | Cost | Why this one |
|---|---|---|---|---|
| R1 | Deterministic anti-patterns | `detect.mjs` | free | Mechanical, done, re-runnable |
| R2 | Self-contained rule compliance | grep gate + `check-leak.sh` | free | Binary rules — external requests, storage, leaked comments |
| R3 | Bloat: are 11MB pages justified? | `/ponytail-audit` | low | 99% base64 — is every asset earning its bytes? Directly relevant to load time on mobile |
| R4 | Visual + UX craft, per page | `/impeccable critique` then `/impeccable polish` | med | Its entire purpose; 23 commands; already installed and hooked |
| R5 | a11y / performance / responsive | `/impeccable audit` | med | Covers all three; avoids a separate a11y agent |
| R6 | Motion quality (existing) | `/review-animations` (Emil) | med | Purpose-built, higher craft bar than a generic pass |
| R7 | Motion gaps (missing) | `/find-animation-opportunities` | low | Read-only, proposes exact values, doesn't implement |
| R8 | Cross-book brand consistency | `brand-guardian` agent | med | The only reviewer that reasons *across* the 9 books at once |
| R9 | Mobile reality | `mobile-developer` agent + Playwright @375px | med | Traffic is TikTok; hover effects don't exist on phones |
| R10 | Microcopy only (labels, errors, nav) | `/impeccable clarify` | low | **Chapter prose is frozen** — this touches nav/labels only |
| R11 | Final gate per page | `impeccable-finish-reviewer` agent | med | Literally designed as the finish gate |

**Deliberately NOT used, and why:**
- `pick-ui-library` — the books forbid dependencies; picking a library is
  the wrong move here by definition.
- `content-creator` / `content-marketer` — chapter prose is frozen per
  `CLAUDE.md`. These would push changes you don't want.
- `security-auditor` / `test-writer-fixer` / `architect-review` — static
  self-contained HTML with no backend, no auth, no test suite. Nothing for
  them to audit. (One exception: `security-auditor` is worth a *single*
  cross-cutting pass on the faith book's four hard rules, since those are
  effectively a privacy threat model.)
- `prototype` / `overdrive` / `bolder` — generative, not audit. Reach for
  them only if a specific page comes back needing a rebuild.

---

## 4 · The sequence

### Phase 1 — Cross-cutting, done once for the whole project
Batch work that would otherwise be repeated 11–16 times.

1. **D1 decision (blocking, yours):** the `side-tab` question. See Decisions.
2. Pull the 4 missing font families (sparse checkout, ~5 min).
3. Build a reusable self-hosted `@font-face` block per font.
4. Write one Python transform that swaps CDN `<link>` → embedded
   `@font-face` — following the review package's own established pattern
   (`scripts/` transforms with a `MARK` constant, idempotent, rerunnable,
   never hand-edit the big files).
5. **R8 brand-guardian pass** across all books at once — cross-book
   consistency is inherently a single job, not 16.
6. **R3 ponytail-audit** on the two 10MB pages (hub, portals) — asset
   weight is the same question for both.

### Phase 2 — Per-page review (the deep work)
Run per page, in the priority order you set. For each page:

1. `R2` compliance gate (free, instant)
2. `R4` impeccable critique → the page's design verdict
3. `R5` impeccable audit → a11y/perf/responsive
4. `R6`/`R7` motion review + gaps — **skip for pages whose stance forbids
   motion** (see `BOOKS.md`: faith is explicitly anti-engagement-mechanic)
5. `R9` mobile pass
6. `R10` microcopy (nav/labels only)
7. Consolidate into one fix list per page, ordered by impact

**Efficiency rule:** run R4/R5/R6 findings into a *single* consolidated fix
list per page before touching code. Don't fix-verify-fix-verify six times.

### Phase 3 — Implement
Apply fixes per page via transform scripts (never hand-editing multi-MB
files), fonts included. Re-run R1 + R2 after each page — both are free.

### Phase 4 — Verify locally (zero deploy cost)
Per `CLAUDE.md`'s verification pattern, using Playwright + Chromium against
a local `python3 -m http.server`:
- Screenshot 375px and 1440px, and *actually read them*
- `pageerror` listener → zero console errors
- `scrollWidth > innerWidth + 1` → no horizontal scroll
- Nothing stuck at `opacity:0` after scrolling past
- Re-check under `reducedMotion:'reduce'`
- **Verify zero external requests** — the whole point; a network panel with
  no third-party hits is the proof the font fix worked

### Phase 5 — Finish gate
`R11 impeccable-finish-reviewer` per page. A page is "packaged" only when
it passes. Then, and only then, it's deploy-eligible.

### Phase 6 — Deploy, once per site
One deploy per site containing everything: fonts + leak fix + design work.
11 sites → 11 deploys total, the practical minimum. Still gated on your
"GitHub packs" decision about mechanism.

---

## 5 · Page order

Your stated priority, with the reasoning intact:

1. **Hub (catalogue)** — redesign already built, never deployed; 103KB of
   real markup; only 4 raw findings. Highest leverage, lowest effort.
2. **Portals** — live, 114KB real markup, 5 findings, but the Light Line
   drag interaction is the product → R6/R7 motion review matters most here.
3. **Loop** — cleanest foundation (fonts already correct); needs the leak
   fix shipped and chapter-nav integration. Also the reference page others
   should match.
4. **Scale** — same engine, same data structure as Loop; do it immediately
   after so the two stay consistent.

Then, grouped by how much is already known:
5. Root, seals, reaction-map, sovereign, fractal, fracture (font fix +
   standard pass; several already have partial Stripe Press treatment worth
   finishing rather than replacing)
6. Playground (font fix + the 3 bounce-easing findings; **keep its
   gamification** — correct for a children's book per `BOOKS.md`)
7. Faith / Sacred Divide — blocked on your "let me look first" decision
8. Wook — blocked on the unresolved file discrepancy
9. Playbook, Music — structure never investigated; scope before planning

---

## 6 · Decisions needed from you

**D1 — the side-tab question (blocking Phase 1).**
~190 instances of a 3px gold/crimson left border. The detector calls it the
single most recognizable AI-generated-UI tell. Your own design language uses
it as the callout/chapter-card/"you are here" marker, and `CLAUDE.md` says
preserve chapter cards. Options:
- **(a) Keep as-is** — it's the brand, detector finding is a false positive
  at scale. Add it to the known-deliberate list and move on. *(My
  recommendation — it's load-bearing brand identity across 9 books, and the
  gilt/crimson palette makes it read as intentional rather than generic.)*
- **(b) Refine** — keep the accent concept, change the execution (e.g.
  a gilt hairline rule, or an inset marker) so it stops matching the
  generic pattern while staying recognizably yours.
- **(c) Remove** — highest risk; would visibly change all 9 books.

**D2 — deploy mechanism.** Still undefined ("GitHub packs"). Doesn't block
Phases 1–5; blocks only Phase 6.

**D3 — faith / Sacred Divide.** Still pending your review of the redesign.

**D4 — wook discrepancy.** Two candidate files, different titles. One
diff resolves it; want me to just run that?

---

## 7 · What I'd start on right now, with no further input

Everything in Phase 1 except D1: pull the 4 fonts, build the font transform,
run the cross-book brand-guardian pass, and run ponytail-audit on the two
10MB pages. None of it touches a live site, none of it depends on the open
decisions, and it unblocks every page that follows.
