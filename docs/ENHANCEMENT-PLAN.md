# Enhancement Plan — full review + per-page plan

Written after reviewing everything currently in the repo: `sites.json`,
`chapters.json`, `BOOKS.md`, `source/` (the review package), `fixes/`,
`design/`, and the full toolkit now available (`impeccable`, the
emilkowalski animation/design skills, `ponytail`, Playwright, the vendored
fonts/icons/CSS). This is the outline requested — priority order: main hub,
portal page, loop (+ one more book), then the rest.

---

## Headline finding: a real, live rule violation — bigger than the original leak

Checked every page in `source/` (the review package) plus this repo's own
`festie-codex-full.html` for Google Fonts CDN links. Result:

| File | Google Fonts `<link>` count |
|---|---|
| catalogue (undeployed hub redesign) | 3 |
| divide (Sacred Divide) | 1 |
| festival (wook redesign) | 3 |
| fractal | 3 |
| fracture | 3 |
| playground | 3 |
| **portals — LIVE right now** | 3 |
| reaction-map — LIVE right now | 3 |
| root — LIVE right now | 3 |
| seals — LIVE right now | 3 |
| sovereign | 3 |
| **`festie-codex-full.html` — this repo's own tracked "wook" file** | 2 |

**11 of the 12 files checked violate the self-contained rule** — the exact
rule CLAUDE.md calls non-negotiable. This isn't a style nitpick: it's an
external request (breaks "no dependencies, no external requests, no
storage"), it silently degrades to system-font fallback if the CDN is
unreachable (exactly what the review package's own doc admits happened
during its build — "fonts don't load in my sandbox... never seen real
Fraunces"), and it sends every visitor's IP to Google on page load.

**`loop.html` and `scale.html` are the only ones done right** — 20 proper
self-hosted `@font-face` rules, zero external font requests, confirmed
earlier this session. They're the model to match, not the exception.

**Fix approach** (already proven working — this is exactly what
`design/build-snippets.py` and the (aborted, but methodologically correct)
Loop font investigation already did): swap each `<link href="fonts.googleapis...">`
for a self-hosted, base64 `@font-face` block using fonts already vendored
in `tools/fonts/` where possible.

| Font needed | Have it? |
|---|---|
| Fraunces | ✅ `tools/fonts/fraunces/` |
| Newsreader | ✅ `tools/fonts/newsreader/` |
| Public Sans | ✅ `tools/fonts/public-sans/` |
| Hanken Grotesk | ❌ need to pull |
| Jost | ❌ need to pull |
| IBM Plex Mono | ❌ need to pull |
| Space Mono | ❌ need to pull |

Four more font families needed (all on Google's own `google/fonts` repo,
same sparse-checkout method already used 4 times this session — low
effort). **This should happen before any other visual work on these pages**
— polishing a page that's still phoning out to Google is polishing on a
broken foundation, same logic as fixing the leak before decorating.

---

## What we now have (full inventory, for context)

- **Data layer**: `sites.json` (verified project registry), `chapters.json`
  (real chapter data for loop + scale, extracted not invented), `BOOKS.md`
  (per-book content/stance — read before touching any page).
- **Design system**: `design/snippets.html` (font+spacing+progress-bar+
  fade-ins, self-contained), `design/build-chapter-index.py` (generates a
  self-contained contents page from `chapters.json`), `design/check-leak.sh`
  (pre-publish leak gate).
- **Skills**: `impeccable` (23 design commands + a live PostToolUse/Stop
  detector hook, now actually running), `emil-design-eng` + `apple-design`
  + `improve-animations` + `review-animations` + `find-animation-opportunities`
  + `animation-vocabulary` + `pick-ui-library` + `prototype` (Emil Kowalski's
  motion/craft skills), `ponytail` family (anti-bloat).
- **Agents**: 16 in `.claude/agents/` — design/UX, writing, code review,
  plus impeccable's own support crew.
- **Assets**: fonts (Newsreader, Source Serif 4, Fraunces, Public Sans,
  League Gothic, Inter), icons (Lucide, Feather, Tabler, Heroicons),
  animation (animate.css, Hover.css, Magic), baseline CSS (modern-normalize,
  open-color), Playwright + Chromium for verification.
- **Known unresolved**: the wook discrepancy (this repo's `festie-codex-full.html`
  vs. `source/projects/noble-father-festival.html`) — still not diffed,
  now doubly relevant since I need to know which one to fix the font issue
  on, or both.

---

## 1 · Main hub ("The Catalogue")

**Status**: fully redesigned already (`source/projects/noble-father-catalogue.html`,
10.7MB) but **not deployed** — the live hub is still the old 4.47MB version.
This is the highest-leverage item on this whole list: the creative work is
*done*, it just needs to ship.

**Before shipping, in order:**
1. **Fix the Google Fonts CDN dependency** (3 links: Fraunces, Hanken
   Grotesk, Space Mono) — self-host all three. Have Fraunces already; need
   Hanken Grotesk + Space Mono.
2. **Run `impeccable audit`** on it — a11y, performance, responsive checks
   the review doc's own session never got to verify (it explicitly flags
   "never seen in real Fraunces" as an open risk).
3. **Playwright verification pass** (the checklist now in `CLAUDE.md`):
   screenshot at 375px/1440px, console-error check, horizontal-overflow
   check, `reducedMotion:'reduce'` re-check. The review doc claims "all 11
   deployed and verified serving" for other pages but this one's own status
   doesn't check out (title made it live, the actual file didn't) —
   don't repeat that gap here.
4. **Fix the wook discrepancy first if it touches shared hub chrome** —
   the hub links to every book including wook; confirm which wook file is
   canonical before the hub's own nav is considered final.
5. Deploy — held pending your redeploy-mechanism decision ("GitHub packs").

**After the foundation's solid**, the existing redesign already covers most
of what `BOOKS.md`'s Stripe Press guidance wants (physical book-object
cards, a considered opening moment) — this is finishing, not rebuilding.

---

## 2 · Portal page ("The Portals" / "The Vitrine")

**Status**: live now, byte-verified. The signature "Light Line" drag
interaction is the whole page — per the review doc, "look at: drag the
brass line across a pendant. That is the page."

**Priority order:**
1. **Same font fix as the hub** — 4 font families loaded via CDN: Fraunces,
   Newsreader, Jost, IBM Plex Mono. Have Fraunces and Newsreader already;
   need Jost and IBM Plex Mono. This is live in production right now, so
   it's the most urgent instance of the headline finding.
2. **Use the new animation skills on the Light Line/torch specifically** —
   `review-animations` and `find-animation-opportunities` are built for
   exactly this kind of signature interaction; worth a dedicated pass since
   motion *is* the product here, not decoration on top of it.
3. **Verify the touch/tilt equivalents actually fire** — the review doc
   says it built them but "hover effects do not exist on phones" is listed
   under "what to be skeptical of." Playwright can check the code path
   exists; can't fully simulate touch/tilt, so this needs your eyes on a
   real phone too.
4. **Flagging, not deciding**: the review doc notes there's no price shown
   anywhere on the page ("Enquire" only) and suggests price bands might
   convert better. That's a business call, not a design one — surfacing it
   here rather than changing it unasked.
5. Once verified, this page is in good shape — smallest gap of the three
   priority pages, mostly a font-hosting fix plus verification, not a
   rebuild.

---

## 3 · Loop (and The Weighing as the natural second book)

**Status**: best-built page in the whole project on fundamentals (real
self-hosted fonts, own fade-ins, real chapter data now in `chapters.json`)
— but the *design-system integration* (Pass 1/3 from the earlier 10-pass
plan) isn't finished: `design/chapter-index-loop.html` exists as a
generated proof-of-concept but isn't wired into the actual live page.

**Priority order:**
1. **Ship the leak fix** — still the only actual defect on this page,
   already byte-verified in `fixes/loop.html`, blocked on the same
   redeploy-mechanism decision as everything else.
2. **No font work needed** — already correct, the reference case.
3. **Integrate real chapter navigation into the live page**, not just the
   standalone demo: a "chapter N of 47" position indicator is fine (it's
   wayfinding, not the progress-bar/completion-percentage mechanic the book
   explicitly refuses) — but confirm that distinction holds before building
   it; re-read the book's own stance in `BOOKS.md` first.
4. **Do the same for Scale** — same author, same MOVEMENTS/CH data
   structure, same real chapter data now available, same integration gap.
   Check Scale for its own stance statements first (flagged as unconfirmed
   in `BOOKS.md`) before assuming Loop's "no progress bar" rule carries
   over — it might, might not.
5. **`improve-animations` pass** on both — Loop already has `.fx-reveal`
   fade-ins; worth a proper Emil-Kowalski-standard review now that the
   skill is actually installed, rather than assuming "it has motion" means
   "the motion is right."

---

## Everything else — condensed, per `BOOKS.md`'s existing findings

| Book | Top action |
|---|---|
| Faith (Coercive Control Codex) | Same font-CDN issue (1 link on the Sacred Divide file) + your still-pending "look at Sacred Divide first" decision. Don't touch until you've reviewed it. |
| Playground Protectors | Font-CDN fix only — its gamification is correct as-is per `BOOKS.md`, don't apply the "remove gamification" instinct here. |
| The Root | Font-CDN fix; it's a guided practice, don't add a contents-page nav (per `BOOKS.md`). |
| Fractal, Fracture, Sovereign | Font-CDN fix; each already has partial Stripe Press treatment (drop cap, chapter rules, cover entrances) worth finishing rather than replacing. Chapter data not yet extracted for any of the three. |
| Wook | Blocked on the discrepancy diff before anything else. |
| Playbook, Music | Not yet investigated at all — structure unknown, don't assume book-shaped treatment fits either. |

---

## Immediate next step

The font-CDN fix is the one thing that's (a) urgent — it's live now on 4+
production pages, (b) mechanical and low-risk to execute (same pattern
already proven on this session), and (c) a prerequisite for every other
item above. Recommend starting there. I have 3 of 7 needed font families
already; want me to pull the remaining 4 (Hanken Grotesk, Jost, IBM Plex
Mono, Space Mono) and prepare the self-hosted embeds, the same way I did
for the rest — holding actual deployment for your redeploy-mechanism call?
