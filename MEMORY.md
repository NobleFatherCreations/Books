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

## Update (2026-08-02, session 10 — first 3 fixes executed and verified)

Executed the top 3 items from VISION.md's impact-ordered sequence, in full,
with real browser verification (not just static checks) before committing.
Nothing deployed to Netlify per explicit instruction — all changes are
local/committed only.

1. **Reading measure fixed** on loop.html + scale.html: `.reader` was
   inheriting `.wrap`'s 760px width (~89ch) — added a scoped
   `.reader{max-width:65ch}` override (didn't touch `.wrap` itself, which
   is shared by the hub/nav chrome) plus `.body{font-size:19px;
   line-height:1.65}` per VISION.md's specific numbers.
2. **67+ in-prose chapter cross-references linked** — wrote
   `design/link-chapter-refs.py`, a conservative regex transform (whitelist
   of number words 1-47, only matches inside `var BODIES`, skips anything
   already linked) that also resolves cross-book refs ("Chapter 17 of *The
   Weighing*") to the sibling book's real URL via `sites.json`. Found and
   fixed a real bug during this: naive "already-linked" lookback produced 3
   nested `<a><a>` tags in loop.html when two refs sat close together —
   fixed the detection logic (find nearest preceding `<a`, check if IT
   closed, not "does `</a>` appear anywhere in a fixed window") and
   verified true idempotency (running twice = 0 new links, confirmed on
   scratch copies before touching the real files again).
3. **Self-hosted the fonts on catalogue + portals** — wrote
   `design/self-host-fonts.py` (per-page manifest, only embeds families the
   page's own CSS actually uses, variable fonts where available so one file
   covers a full weight range instead of embedding every static weight).
   Removed all Google Fonts `<link>` tags, replaced with base64 `@font-face`.

**Real browser verification** (Playwright + Chromium, direct script since
the MCP server's default Chrome channel isn't installed here — used
`executablePath: '/opt/pw-browsers/chromium'` per the documented pattern):
all 4 pages (catalogue, portals, loop, scale) — **zero external network
requests** (confirms the CDN fix actually works, not just "no link tag in
the source"), zero real console/page errors (one false alarm: local test
server's missing favicon.ico, irrelevant to the real host), zero horizontal
overflow at 375px and 1440px. Screenshots read and confirmed: Fraunces
renders correctly (visible italic display serif + gilt gradient on the hub
— this is the first time anyone has actually seen it render; the original
design session's own sandbox blocked Google Fonts and it was never
verified), the 65ch measure is visibly narrower and more readable, "Chapter
four" appears as a real blue link in chapter 14's body.

**Pulled 4 more font families as distinctive candidates** (not applied
anywhere yet, offered as options): Instrument Serif, Bricolage Grotesque,
Young Serif, Spectral — all in `tools/fonts/`.

Font transform scripts (`design/self-host-fonts.py`) currently only have
manifests for catalogue + portals. The same CDN violation exists on 8 more
pages (root, seals, reaction-map, sovereign, fractal, fracture, playground,
festival, divide) — same pattern, not yet run.

## Update (2026-08-02, session 11 — CDN font fix now complete across all 11 pages)

Extended `design/self-host-fonts.py` with manifests for the remaining 9
pages (root, seals, reaction-map, sovereign, fractal, fracture, playground,
festival, divide/Sacred Divide) — every page identified in the original
headline finding is now fixed. Needed 15 more font families (each
redesigned page turns out to have its own distinct pairing already chosen
— Cormorant Garamond/Outfit/DM Mono for Sovereign, Bricolage Grotesque/
Spectral/IBM Plex for Fractal, Bangers/Baloo 2/Nunito/Patrick Hand for
Playground, Anton/Bungee/Shrikhand/Permanent Marker/Caveat for Festival —
which is actually good news for the "nine worlds" idea in VISION.md, they
already have distinct identities, just weren't self-hosted). One font
(Permanent Marker) was under `apache/` not `ofl/` in google/fonts — found
via `git ls-tree`, not guessed.

**Full verification, all 11 pages**: real Playwright browser pass — zero
external network requests on every single page (confirms the fix actually
works, not just "no link tag in source"), zero horizontal overflow.
Screenshots read and confirmed on 2 visually opposite pages (Playground's
illustrated kids cover with Bangers, Sovereign's dark elegant Cormorant
Garamond field-guide cover) — both render their real fonts correctly.

**One real pre-existing bug found, unrelated to this fix**: reaction-map
references `assets/mark-512.png`, `logo-hero.png`, 3 favicon sizes via
relative paths that don't exist in this repo — confirmed via curl that the
**live site also 404s on these same assets**, so it's not something I
broke, and not caused by the font fix. Not repaired (don't have the actual
image files) — flagged for later, noted here so it isn't rediscovered as
new.

The headline finding from ENHANCEMENT-PLAN.md is now fully closed: **0 of
16 pages load external fonts** (was 11 of 16). `festie-codex-full.html`
(this repo's own wook file) is the only one not yet touched — still
blocked on the unresolved wook-vs-festival discrepancy.

## Update (2026-08-02, session 12 — library index built; content-review agents dispatched)

Built `design/build-library-index.py` — the Wait But Why "make the scale
visible" move from VISION.md. One self-contained page mapping the whole
corpus, generated from `sites.json` + `chapters.json`. Fixed a real
consistency bug before committing: first draft's copy said "Nine works"
while the grid showed 11, because Playbook (a lookup tool) and Music (a
media page) were lumped in with the 9 actual books — contradicts `BOOKS.md`'s
own analysis that neither is a book. Split into a "9 books" primary grid +
a separate "Living Tools" section. Verified: leak-clean, valid HTML, zero
horizontal overflow, Fraunces renders correctly (screenshot confirmed).

Dispatched 2 background subagents (general-purpose — the ux-researcher/
brand-guardian/content-creator agent names from .claude/agents/ aren't
appearing in this session's available subagent list for some reason, worth
checking next session) to do an information-architecture read of Loop and
Scale's actual chapter content: sequencing, scaffolding gaps, pull-quote
placement, cross-referencing opportunities, Appendix A completeness.
Explicitly instructed not to touch/reword prose - structural findings
only. Writing reports to .audit-view/loop-content-review.md and
.audit-view/scale-content-review.md (gitignored, analysis only). Check
their findings before starting marginalia/pull-quote work.

Next up: marginalia (Tufte-style side notes), per-book cover moments for
books that don't have one, wiring chapter-index/library-index links into
each live page's own nav.

## Update (2026-08-02, session 13 — Scale content review applied, Loop review in)

**Scale's content-review agent finished** (`.audit-view/scale-content-review.md`,
343 lines, exceptional quality — exact chapter numbers and exact quoted
sentences throughout). Resolved a real open question: Scale's no-
gamification stance is confirmed VERBATIM in source ("House rules: no
streaks, no progress %, no nags, no tracking") — updated `BOOKS.md`
accordingly (was marked "unconfirmed"). Also found Scale's Appendix A field
card only covers 13/38 chapters (Movements II and V entirely absent,
chapter 34 — "the only mechanism that keeps improving after you finish the
book" — missing from the one artifact meant to be kept), and that the
Loop↔Scale citation relationship is one-directional: Loop cites Scale ~8
times by name/anchor, Scale never once names or links Loop despite naming
other siblings (Fractal, the Codex) inline.

**Applied the 4 safest, most concrete findings to `fixes/scale.html`**,
verified with exact-text matching before touching anything (each `assert
count==1` before replacing):
- 3 unstyled load-bearing sentences (chs. 24, 28, 36) converted from plain
  `<p>` to the book's own existing `.pull` styling — zero words changed,
  just the wrapper tag, matching the pattern already used 40+ times
  elsewhere in the same file.
- Chapter 19's existing unlinked tease ("That is a different book, and it
  is coming") now links to Loop's URL — again zero words changed, just
  wrapped in `<a href>`.
Verified with Playwright: scrolled to and screenshotted the actual
rendered chapter 19 link (reads naturally, styled as a real in-text link)
and chapter 24's new pull-quote (matches the visual pattern of the other
~44 pulls in the file exactly). Not yet done: the 3 remaining findings
that need actual design work rather than a markup swap (Movement IV's
7-test comparison table, the evidence-tiers table, the field card's
missing 25 chapters) — those are `AUDIT-PLAN.md`/`VISION.md`-scale design
tasks, not markup fixes, saved for the marginalia/table-building pass.

**Loop's content-review agent also finished** (`.audit-view/loop-content-review.md`)
— not yet read/applied this update, next up. Headline items from its own
summary: 5 chapters (2,6,8,11,19) have a stronger candidate sentence than
their current pull-quote; 3 real missing cross-references (ch.34/35→
Sovereign, ch.18→ch.16, ch.36→ch.4); Appendix A is missing ch.8's
notification exercise, which the book itself calls "the highest-value ten
minutes in this book."

## Update (2026-08-02, session 13 cont. — Loop content review applied)

**Loop's content-review report read and applied.** Same exceptional
quality as Scale's. Applied:
- **Fixed a real bug in `design/link-chapter-refs.py`**: `NUM_WORDS` never
  had bare "thirty" or "forty" as keys (only compounds like
  "thirty-one"..."thirty-nine" were generated) — so "Chapter thirty" and
  "Chapter forty" mentions were silently never linked. This is exactly the
  5 mechanical gaps the content-review agent found independently by
  reading the prose. Fixed the generator to also emit the bare tens word,
  reran on both loop.html and scale.html (0 new for scale, confirming it
  wasn't affected), verified idempotency again.
- **5 pull-quote upgrades** (ch2, 6, 8, 11, 43 — ch43 not ch19 as
  mis-numbered in my own head, double check against the file if resuming):
  ch43 and ch11 were clean standalone-paragraph swaps like Scale's. Ch6 and
  ch8 required splitting a paragraph (the flagged sentence was mid-
  paragraph, not the whole thing) — extracted the flagged sentence into
  its own `.pull` div, kept every remaining word as a following `<p>`,
  zero prose changed, just re-shaped into 2 blocks from 1. Ch2's flagged
  sentence lives inside a `<li>` in a 4-item parallel list — decided
  against breaking list structure to force a block-level `.pull`; instead
  added `<strong>` emphasis in place (matching the emphasis pattern already
  used on each list item's lead clause), preserving structure. Verified
  with Playwright screenshots on ch2 and ch6 — the ch6 split reads
  completely naturally.
- **Deliberately NOT applied**: the 3 "see also" sibling-book links
  (ch34/35→Sovereign, ch18→ch16 internal, ch36→ch4 internal) — unlike
  Scale's ch19 fix, these have no existing text to wrap; adding them
  would mean writing new marginalia sentences, which crosses into content
  the review agents were told not to touch. Held for the marginalia
  component build (next phase) rather than hacked in as ad-hoc inline text.
- **Also not applied** (needs real component/table design, same as
  Scale's deferred items): stage-map component, ch19 money-chain diagram,
  Movement IV mechanism table, claim-status markers, ch45/Appendix-C
  bidirectional linking, Movement VII roadmap marker, Appendix A expansion.

Both `.audit-view/*-content-review.md` files stay gitignored (analysis
only) but their findings are now recorded here + applied to the actual
source where safe to do mechanically.

## Update (2026-08-02, session 14 — Phase A: marginalia component built and applied)

Presented a 9-phase roadmap to the user (A: marginalia, B: table/diagram
findings, C: content reviews for remaining books, D: clear blockers
(wook diff, faith decision), E: cover moments, F: wire real navigation
in, G: multi-agent design QA, H: full verification sweep, I: deploy).
Executing in that order, starting with A.

**Built `design/marginalia.html`** — a Tufte CSS sidenote pattern
*adapted*, not copied: Tufte's original assumes a wide page with a
permanently reserved margin column; these books use a centered ~65ch
`.reader` column with empty space on both sides at wide viewports instead.
Positions notes absolutely relative to `.reader`'s own right edge (needed
adding `position:relative` to `.reader`, which the earlier measure-fix
pass hadn't set). Below 1200px there's no room beside the column, so it
falls back to Tufte's own accessible checkbox-toggle technique (tap the
marker, note expands inline) — same no-JS mechanism, different geometry.
Uses the book's own `--ink2`/`--line`/`--card`/`--glow` custom properties
so it matches each page's existing palette automatically.

**Verified on a standalone test harness first** (2 notes, both viewport
sizes, checked for collision) before touching any real file — wide: both
notes render beside their reference point with no overlap; narrow: tap-to-
reveal works, zero horizontal overflow either way.

**Applied to the 4 "see also" cross-references both content-review agents
flagged but I'd held back** (they needed new text, unlike the Scale ch19
fix which just wrapped existing prose) — reasoned this through explicitly:
a clearly-marked, visually-separate editorial cross-reference apparatus
(margin note) is standard book-making craft, not a rewrite of the frozen
prose — no chapter body sentence is touched, every note is new, separate,
side-column content:
- Loop ch35 → Sovereign (feminine slug), Loop ch18 → internal ch16,
  Loop ch36 → internal ch4.
- Scale ch9 → "related, but different" marker back to ch8 (the
  grief-vs-memory-rewrite pairing the report flagged as unmarked).

Verified on the REAL pages (not just the test harness) with Playwright:
all 4 notes visible, zero console errors, zero horizontal overflow at
1440px; screenshotted one in full and confirmed it sits exactly beside its
reference paragraph without disrupting reading flow; also verified the
mobile (375px) tap-to-reveal fallback on the same instance — works
correctly, styled consistently with the site's existing `.pull`/`.warn`
card pattern.

`design/add-marginalia.py` is idempotent and reusable — re-running skips
already-present notes and CSS, so it's safe to extend with more
books/notes later (e.g. once Phase B/C surface more candidates) without
redoing this pass.

**Phase A complete.** Next: Phase B (the table/diagram findings — Scale's
Movement IV test comparison + evidence-tiers table; Loop's stage-map,
money-chain diagram, Movement IV mechanism table, danger-checklist
marker) — these need real component design, picking up now.

## Update (2026-08-03, session 15 — Phase B: table/diagram components, in progress)

Built a new reusable `.cmp-table` CSS component (added independently to
both `fixes/scale.html` and `fixes/loop.html`'s own `<style>` blocks,
ported to each book's own palette — Scale: `--bronze`/`--wax` accents on
`--paper2` background; Loop: `--brass`/`--wax`/`--glow` on `--panel`
background — matching each book's existing `.pull`/`.warn`/`.try`
convention rather than a shared cross-book style). Structure: scrollable
wrapper (`overflow-x:auto`, table `min-width` set so it never blows out
`.reader`'s own width — this is how it stays clean at 375px, confirmed
via the `scrollWidth > innerWidth` check on `document.documentElement`,
not just eyeballing it) + real `<table>` with a `.k`-style label caption
above it, matching the site's existing all-caps mono section-label
convention.

Applied so far (each is genuinely new structural content — not a markup
change to existing prose — built where the content-review agent's report
specified the content and rough placement, but the exact wording/design is
mine):
- **Scale ch.20** — Movement IV's 7-test comparison table (test / what
  you do / healthy signal / coercive signal), one row per ch.21-27, each
  test name linking to its chapter. Placed at the end of ch.20 (movement's
  opening chapter), right after the existing "Testing without escalating"
  section — matches the report's suggested placement exactly.
- **Scale ch.12** — 3-tier evidence table (record / observation /
  impression), placed at the chapter's own close.
- **Loop ch.24** — Movement IV's "5 rooms" domain-sweep table (work /
  play / services / commerce / politics, one row per ch.20-24), placed at
  the movement's close (end of ch.24, right before the `MOVEMENT V`
  comment marker).
- **Loop ch.5 + the Appendix A counter-card** — the existing `.stages`
  eight-stage pill-list read as a flat list despite the chapter's whole
  point being that it's a *loop* (Replace → next user → Idealise again).
  Added arrow connectors between stages plus a loop-back glyph (↻) after
  the last one, with an accessible `title` attribute rather than visible
  text for the "loops back" meaning — kept this to pure structural
  markup so it doesn't count as new prose. Both instances (ch.5's own
  version and the condensed labels on the counter-card) updated for
  consistency.

All four verified with the same rigor as Phase A: `check-leak.sh` clean,
`<table>` tag-balance checked, then real Playwright renders at 1440px and
375px — zero console/page errors, zero external network requests, zero
horizontal overflow, all table rows present — with actual screenshots
read back (not just asserted) before committing. Each is its own commit,
pushed to `claude/gstack-setup-0nzwbn` after every commit (not batched) so
nothing sits unpushed.

Playwright setup note for future sessions: the MCP server's default
config looks for a `chrome` channel binary that isn't installed here —
use raw Node scripts instead, with `executablePath:
'/opt/pw-browsers/chromium'` and a symlink at `node_modules/playwright` →
`/opt/node22/lib/node_modules/playwright` (ESM `import` resolution needs
the real node_modules path, `NODE_PATH` alone isn't enough). Added
`node_modules/` to `.gitignore` since this symlink shouldn't be committed.

**Still open in Phase B** (per the two `.audit-view/*-content-review.md`
reports, not yet built): Loop ch.19 money-chain diagram, Loop
danger-checklist shared visual marker (chs 2/20/37 — the same warning
restated three times unmarked as a pattern), Loop Movement VII's 4-box
roadmap marker (ch.38/41 seam). Then Phase C (chapter-data extraction
format for the other 7 books) is next after Phase B closes out.

**Correction to the paragraph above:** the "danger-checklist shared
visual marker (chs 2/20/37)" item is Scale's, not Loop's — mixed up
during context compaction earlier in this session. Loop's actual
remaining scaffolding item was the Movement VII 4-box roadmap marker at
ch.38/41. Both are now built (see below); noting the correction here
rather than silently editing history.

## Update (2026-08-03, session 15 continued — Phase B complete)

Finished all remaining Phase B items:

- **Loop ch.19** — visual money-chain diagram (agency → DSP → exchange →
  SSP → verification → data suppliers → platform → creator), numbered
  1-8, "the creator" end-node marked in `--wax` since the chapter's own
  pull-quote says they get the smallest share and carry all the risk.
  New `.chain`/`.link`/`.arrow` component (reused for the item below).
- **Loop ch.38** — Movement VII's 3-box roadmap (Strategy 1/2/3 → ch.39/
  40/42) plus a dashed `.chain-note` explicitly placing ch.41 as "what
  running Strategy 2 feels like," not a fourth strategy — resolves the
  exact hesitation the report flagged.
- **Scale ch.2/20/37** — the real "danger-checklist" item (see
  correction above): the same danger-condition checklist is deliberately
  restated three times in different words (ch.2 rule three, ch.20 risk
  check, ch.37 full-strength stop list) "so that no matter where you
  open the book, the floor is within reach" — but wasn't visually marked
  as the same list. Added a shared inline `octagon-alert` icon (from the
  already-vetted self-hosted lucide set) at each site, `aria-label`'d,
  zero prose changed.
- **Scale ch.10 ↔ ch.20** — ch.10's 6-question pre-flight ("fit to judge
  right now?") had no persistent surface elsewhere despite Movement IV's
  tests depending on it. Added a marginalia cross-reference at ch.20's
  risk check.
- **Bug fix, found incidentally:** `fixes/scale.html`'s marginalia CSS
  (from the Phase A pass) referenced `var(--glow)`, which is Loop's
  accent var — Scale has no `--glow`, it uses `--bronze`/`--bronze2`.
  Root-caused to `design/add-marginalia.py` hardcoding `--glow`
  regardless of book. Fixed the live file directly and parameterized the
  script (`ACCENT_VAR = {"loop": "--glow", "scale": "--bronze2"}`) so
  future runs/books don't reintroduce it.

All items verified with the same rigor as the rest of Phase B —
`check-leak.sh`, Playwright at 1440px/375px, zero console/page errors,
zero external requests, zero horizontal overflow, screenshots actually
read back before committing. Each change is its own commit, pushed
immediately after.

**Phase B is now fully complete** — both content-review reports'
table/diagram/marker findings are built and live in `fixes/*.html` (not
yet deployed — deploy is still Phase I, gated on the user's
still-undefined "GitHub packs" mechanism and on explicit sign-off).

**Next: Phase C** — investigate chapter-data extraction format for the
remaining 7 books (fracture, feminine/sovereign, fractal, playground,
wook/festival, root, faith — faith itself is on hold per the user's
"let me look first," so treat it as lowest priority / skip until asked),
then dispatch content-review subagents for whichever have a real,
extractable chapter format. `BOOKS.md` flags fracture and feminine as
the next candidates.
