# MEMORY — read this first, every session

This is the actual cross-session memory for this project. In this remote
environment, a new chat/session gets a fresh container — nothing outside
this git repo survives. So this file (not a plugin, not `~/.claude/`) is
what makes "remember cross-thread" real here. **Any AI picking up this repo
should read this file, `sites.json`, and `chapters.json` before doing
anything else.** Update this file as work happens — append, don't rewrite
history.

See `CLAUDE.md` for standing rules, `PROJECT-MASTER.md` for the full
category-by-category plan, `sites.json` for the live-project registry.

## Where things stand (2026-08-02)

**Live-site leak (the original urgent ask):** 3 pages (loop, scale, faith)
leak a build-instructions HTML comment. Byte-verified fixes exist in
`fixes/`. **Not deployed yet** — user wants to redeploy via GitHub packs
instead of a direct Netlify push, decision pending on tooling for that.

**Undeployed redesigns found in the user's review package** (`source/`):
- "The Catalogue" — full hub redesign, NOT live despite review doc claiming
  it was (title-only made it live somehow).
- "The Sacred Divide" — retitled/redesigned faith book, NOT live. Would fix
  the faith leak as a side effect if deployed, but that's a bigger content
  decision (title change) — user said "let me look first," so **hold, don't
  deploy, until they confirm.**
- `faith-index.html` — a third, distinct offline-only edition, 5/8 passes
  done, not deployed anywhere per the review doc.
- **Unresolved:** `source/projects/noble-father-festival.html` (wook
  redesign) has a different title than this repo's own tracked
  `festie-codex-full.html`. Not diffed yet.

**Confirmed byte-exact live matches** (safe to treat as current/accurate):
root, portals, seals, reaction-map. A real bug fix (reaction-map, dead code
from a use-before-declare) is confirmed live.

**Repos downloaded** to `tools/`: claude-howto, mattpocock/skills,
claude-code-tips, claude-code-ultimate-guide, tufte-css, lucide icons,
animate.css, two font families (Newsreader, Source Serif 4), and the two
"remember" memory-plugin repos (Digital-Process-Tools/claude-remember,
remember-md/remember) — vendored but **not activated as plugins**, see
`tools/README.md` for why. `vibehat/claude-task-manager` also vendored but
flagged as not recommended to run here (full dev-server app, not a
lightweight hook).

**Not yet done:**
- `chapters.json` only has MOVEMENT III (ch 14–19) + MOVEMENT IV's opening
  chapter (20) for the "fracture" book. Every other book's chapter list is
  still empty — needs real content, not invented.
- Subagent collection choice (wshobson/agents vs. contains-studio/agents,
  etc.) — compared, not installed. wshobson/agents (203 agents, plugin-
  installable) is the stronger single match; contains-studio/agents (40) has
  nice extras for niche-channel social distribution. Awaiting go-ahead.
- Part 6 (the numbered step-by-step action plan) — not written yet.
- The redeploy mechanism itself — user wants to use "GitHub packs" instead
  of a direct Netlify push; what that means concretely (a repo per site? a
  GitHub Action that deploys to Netlify?) hasn't been defined yet.

## Update (2026-08-02, later same day)

- Built the design system: `design/snippets.html` (self-hosted Newsreader
  serif embedded as base64, 8px spacing scale, palette tokens, reading-
  progress bar, scroll fade-ins — all native, zero requests) and
  `design/build-chapter-index.py`, which bakes `chapters.json` +
  `sites.json` data into a fully self-contained chapter-index page at
  generation time (not a runtime fetch — `file://` pages can't fetch
  sibling JSON, so this stays a build step). Proof of concept:
  `design/chapter-index-fracture.html`, the one book with real chapter data.
- Added `design/check-leak.sh` — greps for the leak markers before
  publishing anything. Ran it against every HTML file in the repo: clean.
- Wrote the Part 6 step-by-step plan into `PROJECT-MASTER.md` — 10 items,
  ordered, with `[YOU]` flags on the ones only the user can decide (GitHub
  packs definition, faith patch-vs-redesign, Catalogue deploy, subagent
  collection choice).
- A consolidated recap of the whole thread came back around (paste from
  another AI/session) claiming the leak was across all 9 named projects —
  **corrected**: it's exactly 3 pages (loop, scale, faith), none of which
  are among the 9 codenamed projects, all of which are already clean. Also
  corrected: those 3 have no repo, so "fix repo, redeploy" doesn't apply —
  already established last session, don't let it get re-asserted as fact.
- Still not pasted into any live/shipped page — `design/snippets.html` is
  ready but insertion into each book's existing markup is a separate,
  not-yet-done pass.

## Update (2026-08-02, session 3 — clarifying what's actually available)

User was (understandably) unclear on what "downloaded repos" meant in
practice. Clarified: everything lives as files in this repo, nothing has
touched the live site. Key distinction that matters going forward:

- **`tools/`** = reference material (guides, CSS, icons, fonts) — read
  when needed, not auto-active.
- **`.claude/agents/`** = real, active subagents (12 of them: design/UX,
  writing/copy, code/technical — user asked for all three categories).
  These load automatically in ANY future session on this repo, same as
  `CLAUDE.md`/`MEMORY.md` — no plugin install needed. This is the correct
  persistent mechanism in this environment (a plugin install into
  `~/.claude/plugins` would NOT survive a fresh container; a file in
  `.claude/agents/` inside the repo does).
- Still true: nothing has been deployed live. loop/scale/faith fixes sit in
  `fixes/`, unshipped, per explicit instruction to hold until design work
  is finished and "GitHub packs" is defined.

## Update (2026-08-02, session 4 — real chapter data found, one attribution corrected)

**Important correction:** the MOVEMENT III/IV chapters from the original
planning thread (14 "You are not the customer" ... 20 "Algorithmic
management") were pre-filled under `allfracture`/"All Fracture" in
`chapters.json` — **that was wrong.** They actually belong to `loop`/"The
Loop." Confirmed two ways: exact text match only in `fixes/loop.html`, and
chapter 19's own blurb literally says "The sibling of All Fracture" — i.e.
it's a different, related book, not the same one. Fixed in `chapters.json`.

**How this was found:** `loop.html` and `scale.html` author their own
chapter data as JS literals right in the page — `var MOVEMENTS=[...]`
(movement numeral/title/chapter-list/blurb) and `var CH={...}` (per-chapter
title/blurb/readMin). Wrote `design/extract-chapters.py` to parse this
straight out of the shipped HTML — real content, zero invention. Got all 47
chapters/8 movements for The Loop and all 38 chapters/6 movements for The
Weighing this way, fully populated in `chapters.json` now (title, blurb,
readMin — the only thing not present in the source is a per-chapter slug;
chapters route by number via `location.hash`, not a slug scheme).

Regenerated `design/chapter-index-loop.html` and `design/chapter-index-scale.html`
from the corrected data — both verified clean via `check-leak.sh`.

**Still todo:** fracture, wook, feminine, children, fractal, shadowroot,
playbook don't use this same MOVEMENTS/CH format (checked fracture
specifically — no match). Each needs its own format investigated before
filling in; don't assume they all match loop/scale's pattern.

**Self-correction, same session:** went looking to complete Pass 2
(typography) on `loop.html`, concluded from a CDN-link/`@import` grep that
`font-family:'Fraunces'`/`'Public Sans'` were declared but never loaded —
wrong. Missed a `<style id="embedded-fonts">` block that already has 20
proper `@font-face` rules (both families, multiple weights, base64,
zero requests). Built a redundant duplicate embed, caught it before
committing, deleted it. **Lesson recorded here so it isn't repeated:**
before assuming a font/asset is missing on any of these pages, grep for
`@font-face` and any `id="...font..."` style block, not just CDN links —
these pages self-embed things in ways that don't show up in an
external-request check. Vendored `tools/fonts/fraunces/` and
`tools/fonts/public-sans/` anyway since they're the design language's
actual chosen typefaces and harmless to have on hand for whichever other
book turns out to need them for real.

## Important — not a uniform design pass across all books

`loop.html` ("The Loop," about manipulative engagement mechanics)
**explicitly refuses to have a reading-progress bar, streaks, or completion
percentage, as a matter of the book's own argument** — direct quote from
its own text: "this book has no streaks, no progress bar, no completion
percentage, no badge... no stored reading position." Found this while
checking whether to add the generic `design/snippets.html` progress bar to
it — did NOT add it. **Do not paste the standard progress-bar snippet into
this book.** Its existing scroll fade-ins (`.fx-reveal`) are a different,
unrelated thing (a subtle entrance effect, not a gamification mechanic) and
are fine as-is.

**General lesson:** the 10-pass design plan assumes uniform treatment
across all 9 books. That's wrong. Check each book's own content/stance
before applying ANY visual pattern — some of these books make deliberate
anti-pattern choices that are part of their argument, not oversights to
"fix." Read before pasting, every time.

## Update (2026-08-02, session 5 — tools requested by video/dictated message)

User asked (via a garbled dictated message) to install "Gastown," "Playwright
MCP," "grill me skill," and "ponytail globally." Investigated all three
named repos before touching anything:

- **Gastown declined** — inspected `gastownhall/gastown`: a Docker daemon
  (`command: sleep infinity`, mounts real home dir, dashboard on :8080),
  OpenTelemetry architecture, background "Deacon" supervisor doing
  "continuous patrol cycles," installs hooks across every repo it manages.
  Same risk category as gstack. User confirmed: leave it out.
- **Ponytail added** — inspected `dietrichgebert/ponytail`: legitimate
  over-engineering/bloat-prevention skill (YAGNI-first decision ladder), not
  a billing hack despite how the dictated description made it sound. No
  postinstall scripts, no network calls anywhere in its code. 6 skills
  copied to `.claude/skills/` (ponytail, -review, -audit, -help, -debt,
  -gain); full repo vendored to `tools/dietrichgebert-ponytail/`.
- **grill-me added** — already had `mattpocock/skills` vendored; copied the
  `grill-me` skill to `.claude/skills/grill-me/`. Trivial, stateless.
- **Playwright** — already natively pre-installed in this environment
  (confirmed: Chromium at `/opt/pw-browsers/chromium`, matches exactly what
  the review package's own bootstrap doc describes using). Added
  `@playwright/mcp` as a project-scoped MCP server via `.mcp.json` too,
  since that's what was explicitly asked for by name.

**Found something important while investigating:** the review package
includes `source/docs/CLAUDE-DESIGN-BOOTSTRAP.md` and
`DESIGN-CAPABILITIES.md` — a full bootstrap doc from whatever session/
environment produced the review package, listing **16 design skills**
(`impeccable` plus 15 taste/style/imagegen skills) that were installed
*somewhere*, but the doc gives no GitHub URL or package source for any of
them — just names and how to invoke them via the `Skill` tool. **Do not
guess a URL for these** — asked the user where they actually came from.
This doc is otherwise valuable: it independently confirms the sites.json
Netlify mapping (matches exactly), and documents real verification
patterns (the 375px/1440px screenshot check, console-error check, etc.) —
folded the verification pattern into `CLAUDE.md` directly since it's useful
regardless of whether `impeccable` itself gets sourced.

Also worth remembering: this doc explicitly lists `divide→thenobledivide`
as an intended deploy target — corroborates the earlier finding that "The
Sacred Divide" was meant to replace the old faith content at that site, but
per direct verification it never actually landed there (still serving old
content) despite the doc's blanket "all eleven deployed" claim.

## Update (2026-08-02, session 6 — impeccable sourced, big batch download)

Found the real source for `impeccable`: `github.com/pbakaus/impeccable`.
Inspected — Apache 2.0, disclosed anonymous "choice ping" telemetry only
(opt-out via `IMPECCABLE_NO_TELEMETRY`/`DO_NOT_TRACK`), no daemon. Its own
repo dogfoods itself and ships a pre-built `.claude/skills/impeccable/` +
4 support agents — copied those directly rather than reconstructing from
source. **Caveat:** the reference docs (the useful part — 23 command
guides) work as-is; the deterministic `detect.mjs` and `live` browser-
iteration scripts need `npm install` run inside
`.claude/skills/impeccable/scripts/` first, not done yet (would pull in
css-tree/htmlparser2/marked etc., not vetted yet).

Also inspected and added `geopopos/higgsfield_ai_mcp` (small, legitimate,
needs the user's own Higgsfield API key to do anything — wired into
`.mcp.json` with empty placeholders, inert until real credentials added).

Downloaded everything else remaining from the original wishlist: two more
font families, 3 more icon sets, 2 more animation libraries, modern-
normalize, open-color, zebbern's guide, and both remaining subagent
collections (VoltAgent's 154-agent catalog and davila7's — pulled only the
`agents/` folder from davila7 since the full repo is a 161MB CLI+dashboard
product, not just agents). Neither collection was turned into active
`.claude/agents/` entries — 16 are already active; adding 150+ more would
be redundant. Browse `tools/` and pull specific ones by name if a role is
missing. unDraw wasn't found as a clonable repo (tried 3 names, all failed
at the proxy auth layer, not a 404 — stopped rather than keep guessing).

Total repo size is now large (~180MB+) mostly from vendored reference
material in `tools/` — all inert reference/available-but-not-auto-run,
same pattern as everything added before it.

## Update (2026-08-02, session 7 — headline finding + ENHANCEMENT-PLAN.md)

Added `emilkowalski/skills` (8 real animation/design skills — the source of
"emil-design-eng"), ran the actual `npx impeccable install` CLI (updated
the skill to the real released build, wired a PostToolUse/Stop design-
detector hook, moved it from `.claude/settings.local.json` to
`.claude/settings.json` so it's actually committed/shared). Skipped a
duplicate GitHub MCP setup — this environment already provides
`mcp__github__*` natively, no PAT needed or available.

**Big finding while reviewing everything for the enhancement plan:** 11 of
12 checked pages in `source/` (the review package) — including this repo's
own tracked `festie-codex-full.html` — load fonts via a live Google Fonts
CDN `<link>`, a real violation of the self-contained rule (external
request, breaks offline, leaks visitor IPs to Google). This is bigger than
the original comment leak: it's live in production right now on portals,
seals, reaction-map, root (all confirmed byte-exact-live earlier), not just
sitting in an undeployed file. `loop.html`/`scale.html` are the only pages
that do this correctly (self-hosted, 20 real `@font-face` rules). Full
writeup and per-page priority plan in `ENHANCEMENT-PLAN.md` — read that
before starting any visual work on hub/portals/loop, in that order, per the
user's explicit request.

Need 4 more font families to fix this (Hanken Grotesk, Jost, IBM Plex Mono,
Space Mono) — not pulled yet, offered to do it, awaiting go-ahead.

## Standing decisions (don't re-litigate these)

- Books are self-contained: no deps, no external requests, no storage,
  offline-capable.
- `garrytan/gstack` declined permanently (telemetry, daemons, curl-installer).
- Design references: Stripe Press / Aeon / Wait But Why (pending user's own
  confirmation if they'd rather name different ones).
- Outreach and publishing: human-in-the-loop always, no auto-send.
- Palette question (emerald+gold gallery vs. dark+gold+crimson books):
  explicitly deferred by user, not decided.

## Update (2026-08-02, session 8 — full audit baseline + AUDIT-PLAN.md)

User: nothing deploys until each site's whole package is reviewed and
finished (font fixes ride along in one deploy per site — protecting Netlify
deploy credits). Wants every new tool/agent used intelligently, not
exhaustively.

**Efficiency unlock found and built:** these pages are 0.1–11MB but 85–99%
of that is embedded base64. `design/prep-audit.py` strips payloads into
`.audit-view/` (gitignored, analysis-only, never ship or edit these). The
11MB hub becomes 103KB of real markup. **This defeats the "detector times
out over 3MB" limit the review doc reported — all 16 pages are now
auditable.** `design/run-detector.sh` batch-runs the detector.

**Baseline captured: 310 raw findings across 16 pages.** BUT most volume is
not defect:
- `side-tab` (~190, 61% of all findings) = `border-left:3px solid
  var(--gilt)/var(--glow)/#8A2432` — this is the project's OWN gold/crimson
  accent language (callouts, chapter cards, the "you are here" nav marker).
  CLAUDE.md says preserve chapter cards. **Do not mass-fix these** — it's
  decision D1 in AUDIT-PLAN.md, pending user. My recommendation: keep as-is.
- Fraunces `overused-font` (~60), `em-dash-overuse`, `gradient-text`,
  `dark-glow` = all named known-deliberate in the review package's own
  bootstrap doc. Ignore.
- `broken-image` on seals: **checked, false positive** — JS sets the src at
  runtime.
- Genuinely actionable mechanical findings: ~15–20, mostly `bounce-easing`
  (playground, root), `layout-transition`, `radial-halo`.

Also confirmed: faith.html (23 @font-face) and faith-index (3) are ALSO
correctly self-hosted, joining loop/scale. So 4 of 16 pages are compliant;
11 violate via Google Fonts CDN (1 page, festie-codex-full, is the repo's
own copy and also violates).

`AUDIT-PLAN.md` has the full plan: one reviewer per concern (no overlapping
opinions — explicitly lists which agents NOT to use and why), 6 phases,
page order, and 4 decisions needed. Local Playwright verification keeps
deploy cost at zero until Phase 6.

## Update (2026-08-02, session 9 — VISION.md, fresh art-direction read)

User pushed back (fairly): I'd been auditing compliance instead of showing
what these could become. Also said the bootstrap doc's parameters and the
"no dependencies" rule were set before current analysis and are open to
reconsideration. Asked for my own fresh opinion + how the 3 references
apply specifically.

**Read the actual prose for the first time.** Findings that reframe
everything:
- **Both books are COMPLETE**: Loop 47/47 chapters (~27,500 words), Scale
  38/38. Not works in progress. 193 section headings, 53 pull quotes, 38
  lists in Loop.
- Writing quality is genuinely high — Stripe Press tier.
- **Reading measure is ~89 characters/line** (760px @ 17px). Optimal is
  60–70. Highest-impact fix available, one CSS change, affects all ~85
  chapters.
- **67 in-prose cross-references ("as in chapter four") are plain text**,
  not links. Plus 12 mentions of sibling books (Weighing 8x, Fractal 2x,
  All Fracture, Playground). The corpus is already a web; the HTML doesn't
  know it. This is the Wait But Why opportunity and it's nearly free.

**My position on dependencies** (recorded so it isn't re-litigated): keep
self-contained, but for a real reason — everything in the vision is doable
with native APIs, so the constraint costs nothing and makes the privacy/
offline claim true, which for books about surveillance IS the argument.
BUT the rule is currently fiction on 11/16 pages (Google Fonts CDN) — they
have the costs without the benefit. Finish it or drop the pretense.

**On Fraunces**: detector flags it as overused; I disagree in context —
generic-ness comes from default usage (one weight, no optical sizing), not
the face. Keep it, but actually use the SOFT/WONK variable axes.

`VISION.md` has the full map: each reference applied concretely
(Stripe Press = objects/covers/per-book identity; Aeon = 65ch measure,
rhythm, marginalia via already-vendored Tufte; WBW = link the 67 refs,
library index across all 9), what "finished" looks like per surface, and
an impact-ordered sequence. Top 3 (measure, cross-ref linking, self-host
fonts) are mechanical and low-risk — recommended regardless of other
decisions.
