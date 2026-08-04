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

## Update (2026-08-03, session 15 continued — Decision D4 resolved, Phase C running in background)

**Phase D item closed:** the wook discrepancy. Diffed this repo's own
tracked `festie-codex-full.html` against
`source/projects/noble-father-festival.html` and found they're the same
document at different revision stages, not divergent content — heading
diff showed exactly one addition (the House catalogue nav panel), and
stripped-text-length comparison matched almost exactly (1,503,766 vs
1,504,366 chars, the ~600-char delta being that same nav panel's text).
`source/projects/`'s copy already had two fixes this repo's tracked copy
never received: THE HOUSE catalogue nav wired in, and fonts self-hosted
(no more Google Fonts CDN link, 11 `@font-face` blocks embedded instead).
git log showed only two "Add files via upload" commits on the repo's
copy — no independent edit history at risk. Backed up the original,
copied the corrected version over, verified with Playwright (clean at
1440px/375px, zero console/page errors, zero external requests, House
nav confirmed present, no Google Fonts reference) — one `scrollWidth`
overflow flag at 375px turned out to be a false positive worth noting
for future verification passes: a pre-existing off-canvas nav drawer
(`.panel-nav`, this book's own "Setlist" side-nav, not the House
catalogue) parked off-screen via `left:-333px` rather than a transform,
which trips the scrollWidth heuristic even though `body{overflow-x:
hidden}` already fully contains it (confirmed `scrollX` stays `0` on a
scroll attempt) — not a regression, just a case where the usual
overflow check needs a second look (is `overflow-x:hidden` set
somewhere in the ancestor chain?) before concluding it's real.
Committed and pushed. This also clears the way for wook's still-pending
font-CDN fix (now already done, since the synced copy has no CDN
reference) and any future wook design-review pass.

Hit the Bash permission classifier blocking `git add
festie-codex-full.html` repeatedly (isolated, no compound commands) —
likely the file size (5.7MB replacing 2.2MB looks like a large
binary-ish diff to the classifier). Per the tool's own guidance, stopped
and explained to the user rather than working around it; a retry on a
later turn went through cleanly, so this may just be intermittent for
large file diffs rather than a hard block — worth knowing for future
large-file operations in this repo.

**Phase C: the background structural-survey agent is still running**
(dispatched via Explore, checking Sovereign/Fractal/Playground/
Festival/Root/Divide's data structure — Divide/faith deliberately
scoped to structure-only, no content engagement, per the standing
hold). Its report will determine which of the remaining books get a
real chapter-by-chapter content-review pass vs. need a different
approach (Fracture already confirmed to need a different approach: 13
single-scroll "plates," no hash router, no MOVEMENTS/CH/BODIES data
structure).

## Update (2026-08-03, session 15 continued — both content-review reports fully closed out)

While Phase C's background survey ran, went back through both
`.audit-view/*-content-review.md` reports' own "Summary for the
design/navigation pass" sections item-by-item and closed out everything
that wasn't a table/diagram (those were Phase B). Found several items
already done — either by the parallel session or from before this
session's Phase A/B — and verified rather than assumed:

**Loop** (10-item list, §2-5): stage-map/chain/table (Phase B), pulls at
ch6/8/11/43 (already done), roadmap marker (Phase B) — all confirmed.
Built the remainder: ch2 and ch19 pull upgrades (self-declared "most
consequential sentence" and cross-book unifying claim, both previously
buried in `<li>`/`<strong>`); ch34→Sovereign marginalia note (ch35 had
one from Phase A, ch34 didn't, report flagged both); claim-status
marginalia markers at ch24/26/27 pointing to Appendix C (generic
wording, not asserting which bucket each claim falls in, since Appendix
C's own categorization is the source of truth); bidirectional ch45↔
Appendix C companion links (added a line to the JS-generated Appendix C
header, not just a marginalia note, since that page isn't frozen
chapter prose). All 5 mechanical "chapter thirty/forty" link fixes
confirmed already fixed (the NUM_WORDS bug fix from earlier this
session).

**Scale** (5-item ranked list, §2-5): 7-test table, evidence-tiers
table, danger-checklist marker, ch10 pre-flight cross-ref (all Phase B).
Pull-quote upgrades at ch17/24/28/36 confirmed already applied. Built
the remainder: the big one was **field-card completeness** — Movement
II (chs 6-11, "the instrument is you") and Movement V (chs 28-31) were
entirely absent from the one-page field card, and ch34's calibration
record ("the only mechanism in the book that keeps improving after you
finish reading it," per the chapter's own text) was the report's
single clearest miss. Added 2 new card sections in book order plus a
dedicated ch34 section, matching the card's existing terse h3+list
voice exactly (verified via screenshot, not just assumed to look
right). Also added the 3 missing Loop cross-reference marginalia notes
(ch17, 33, 35 — ch19 already had one) since Scale never once named or
linked Loop despite being Loop's most-cited source book.

**Both reports' full recommendation lists are now built**, not just the
Phase B table/diagram subset. Same verification rigor throughout:
check-leak, Playwright at 1440/375px, zero console/page errors, zero
external requests, zero overflow, screenshots actually read back.
Committed in 2 batches (one per book), pushed after each.

Also resolved along the way: Decision D1 (side-tab accent-border
pattern) — user explicitly confirmed via AskUserQuestion it's
intentional brand identity, not an AI-tell; added a project-wide
`impeccable` `ignore-rule side-tab` in `.impeccable/config.json` so the
design hook stops re-flagging an already-settled pattern.

**Noted for future sessions:** a parallel/concurrent session appears to
be working this same repo and branch alongside this one (it
independently resolved Decision D4 — the wook/festival sync — while
this session was mid-Phase-B, and both merged cleanly with no
conflicts). Always `git fetch` before pushing and merge cleanly rather
than force-pushing; so far every divergence has merged without
conflicts since both sessions touch different chapters/files.

**Phase C's background structural survey is still the next real
unblock** — once it reports which of Sovereign/Fractal/Playground/
Festival/Root have an extractable chapter format, dispatch
content-review subagents for those (Divide/faith stays hands-off per
the standing hold; Fracture already confirmed to need a different,
non-chapter-based review approach).

## Standing craft principle (2026-08-03, added mid-session 15) — emotional/tension craft, scoped

User shared a social-media carousel (Inna, "5 skills for Claude
content") teaching **emotional calibration** (pick the target feeling
before writing, brief it explicitly) and **tension engineering**
(engineer a curiosity gap, rate it 1-10, rewrite until it's a 9), plus
**adversarial editing** (two self-critique passes: "most skeptical
reader" then "senior editor, one structural change that makes this 40%
stronger"). Asked for my honest opinion on whether/how to apply these
to the books.

**My pushback, which the user then refined rather than overruled:**
tension engineering and emotional calibration, as taught in that
carousel, are literally the attention-engineering playbook Loop's
entire thesis is about (ch2: "somebody chose a number, then a search
process found what held people best"). Applying them to Loop's or
Scale's actual prose — beyond just violating the standing
never-reword-frozen-chapters rule — would mean quietly using the exact
manipulation mechanism those books argue against, on the books
themselves. A real credibility risk, not a style nitpick, given faith
and Scale both stake claims on being the thing that doesn't do this.

**User's resolution, which is the standing rule going forward:** the
only legitimate use of emotional weight / structural tension *within*
the books' own writing is to help the reader **feel the actual cost of
manipulation and the importance of resisting it**, or to make a
mechanism land hard enough to be *remembered and understood* —
never to manufacture scroll-compulsion or engagement for its own sake.
Service of comprehension and retention, not service of attention
capture. This is a real distinction, not a rationalization: build
tension toward understanding a stake, not toward withholding
resolution to keep someone scrolling.

**Where this actually applies, going forward:**
- **Any future new writing** (new books, new chapters, marketing/cover
  copy, the clip pipeline's hook titles, outreach drafts) — calibrate
  the target feeling and structural tension explicitly, in service of
  the reader understanding/retaining the stakes.
- **Content-review passes on existing books** (Phase C onward): when
  flagging a passage as pull-quote-worthy or scaffolding-worthy, the
  test is now explicit — does elevating this help the stake land and
  stick, not just "is this quotable." (Already did this instinctively
  on Loop ch2/ch19's pull-quote upgrades this session — the self-
  declared "most consequential sentence" and the cross-book unifying
  claim — without naming the principle; naming it now so it's applied
  deliberately rather than by accident.)
- **Never** as a retroactive rewrite pass on frozen chapter prose, and
  never in service of virality/engagement metrics for their own sake —
  that would be the exact thing these books are warning readers about.

**Adversarial editing** (the two-pass self-critique) is unreservedly
adopted as a standing QA step for any new writing this project
produces — no thematic conflict, it's just disciplined critique.

Carousel only showed skills 1, 2, and 5 of what it framed as a 5-skill
list — 3 and 4 not seen, may be worth asking the user for if relevant
later.

**Dispatched immediately after establishing this principle:** two
background subagents applying it to Loop and Scale specifically —
distinct from the earlier information-architecture reviews (all of
which are already built), this pass looks only for passages where a
real stake (manipulation's cost, the cost of misjudging someone) is
underweighted in presentation relative to its importance, using only
existing CSS components (`.pull`/`.warn`/`.try`/etc., no new ones).
Reports land at `.audit-view/loop-emotional-weight-review.md` and
`.audit-view/scale-emotional-weight-review.md` (both gitignored,
report-only, no file edits by the agents themselves) — act on findings
the same way Phase B's findings were actioned: exact-quote anchors,
existing component only, full Playwright verification before
committing.

**Both agents finished and both reports were fully applied** the same
session — 10 findings on Loop (skipped one, ch33, which the agent
itself flagged as informational-only with no vehicle recommended),
11 on Scale (including the largest single item: a `.cmp-table` at
ch3 pairing the book's false-negative/false-positive cost paragraphs
side by side — its foundational "both errors are real" thesis had
never been visually reinforced before). All markup-only, verified via
`check-leak.sh` + tag-balance checks + full Playwright sweeps (20
checks for Loop, 22 for Scale) before each of the two commits. One
genuine bug caught mid-edit and fixed before committing: an early
`.pull`-duplication edit on Loop ch20 accidentally split a `<ul>` mid-list
via a `</ul>`+hidden-`<ul>` hack — caught by a `<ul>` open/close tag-count
check, reverted, and redone correctly by inserting the new `.pull` after
the list's real closing tag instead.

This closes out a genuinely new, third review pass on both books (after
the info-architecture review and the Phase B table/diagram build) —
worth noting for Phase C: when the survey identifies which of the other
7 books get a content-review agent, that agent's brief should probably
ask for stakes-legibility findings in the same pass rather than as a
separate follow-up round, now that this session has proven the
two-pass pattern works but takes real time to run twice.

## Update (2026-08-03/04, session 15 continued — hub luxury elevation, Phase 1 shipped)

User asked for a full "million-dollar luxury" audit + elevation of the
**main home page** — confirmed via `sites.json` this means
`source/projects/noble-father-catalogue.html` ("The Catalogue," codename
"The Study"), the undeployed hub redesign intended to replace
noblefathercreations.com, NOT the currently-live hub. Safe to edit
freely since nothing here is live yet.

**Dispatched 6 parallel specialist audit agents** (Visual, Motion,
Brand/Emotion, UX/IA, Performance/A11y, Competitive Benchmark) plus did
my own independent read in parallel (grep/python measurement against a
fresh `design/prep-audit.py` strip — 12.4MB real file, 103KB real
markup). **Mid-run, the session hit its API rate limit** (reset
10:30pm UTC) and all 5 still-running agents were killed simultaneously.
3 of 5 (Motion, UX, Benchmark) had already finished writing their full
reports before termination — worth knowing: a "failed" task-notification
doesn't mean no output landed, check `.audit-view/` before assuming a
report is lost. Only Visual and Performance never got to write.
Brand/Emotion had already completed cleanly earlier. All reports live
at `.audit-view/hub-audit-{visual,motion,brand,ux,performance,
benchmark}.md` (gitignored) plus my own `.audit-view/hub-audit-mine-
{tokens,content}.md`.

**The earlier Phase C structural-survey agent (dispatched much earlier
this session, checking Sovereign/Fractal/Playground/Festival/Root/
Divide's data format) also disappeared from tracking somewhere across
this — `TaskOutput` returned "no task found" for its ID.** Not
recovered; needs re-dispatching fresh, this was flagged honestly to
the user rather than fabricating a status for it.

**My own independent findings (verified by direct search/measurement,
not agent-reported) were the highest-leverage items and got implemented
first:**
- **The Loop and The Weighing — the catalogue's two most complete,
  most polished books — were entirely absent from the hub.** Zero
  occurrences anywhere in the markup. Added as Library cards 07/08,
  using each book's own icon glyph (Loop's refresh-ring, Scale's
  balance-scale) rather than inventing new iconography — screenshotted
  and confirmed they render indistinguishably in craft from the
  hand-illustrated covers around them. Updated hero colophon 6->8 and
  the closer card's title/copy.
- **"Saves your place" was about to become a false blanket claim** —
  Loop and Scale refuse localStorage on principle (it's literally in
  Loop's own hero vows: "Nothing stored... Free forever"), unlike the
  other 6 books which do persist reading position. Rather than just
  drop the tag, turned it into a printed detail: "Two keep no record
  at all, on purpose — and say why inside." Turns a would-be
  inconsistency into evidence of the brand's own thesis.
- **Two duplicate `:root` token systems** (13 tokens defined twice,
  identically — `--ink`/`--nf-ink` etc., 7 `!important`s fighting
  between layers) and **no real type scale** (5 section headings that
  should be identical each hand-tuned to a different clamp() value; 60+
  distinct font-size values total) — recorded but NOT yet consolidated,
  this is a bigger systemic pass for next time, not done this session.

**Brand/Emotion agent's top finding, fixed immediately:** the "now
playing" widget autoplayed audio, and where blocked, bound the page's
**next click/touchstart/keydown ANYWHERE in the document** to starting
music — converting an unrelated interaction into consent for a
different action. This is, by name, the manipulation pattern Loop's
own thesis indicts. Removed entirely: widget is silent by default,
visible immediately, only ever starts on an explicit tap of its own
toggle. Also removed the now-dead "Tap anywhere to start the music"
prompt/CSS/JS.

**Motion agent's top finding, fixed and verified by actual reproduction
(not just trusting the report):** the `.reveal` IntersectionObserver had
no fallback — a fast scroll or hash-jump (clicking a nav link, landing
on a shared `#section` URL) could move the viewport past an element
without the observer ever firing, leaving it **permanently** stuck at
`opacity:0` even after scrolling back to it. Reproduced exactly as
described (click "Support" in nav -> scroll to top -> Library/Workshop
headings invisible), then fixed by porting the sweep-fallback pattern
the page's *other* reveal engine (`.nf-r`) already had, lowering
threshold from `.12` to `0`, and adding resize/hashchange/pageshow/
timeout triggers to *both* engines. Also guarded an unguarded
`document.getElementById('yr')` line sitting before the reveal IIFE in
the same `<script>` tag — if that element ever went missing in a future
edit, it would throw and take every `.reveal` on the page down with it
silently, a real single-point-of-failure. Re-verified after the fix:
0 stuck anywhere across a full-page walkthrough at both viewports.

**UX agent independently converged on the exact idea the user asked
for** ("offer two options right at the top — Library or Workshop —
so the craft business isn't buried at the bottom") before either the
user or I saw the other's reasoning — its own measured numbers: craft
buyers had to scroll past 7,085px (9,682px mobile) of book content
before reaching the Workshop. Built the fork: two prominent CTAs in
the hero ("Start reading" / "See the objects"), plus made the existing
colophon stat row navigable to the same 3 destinations (zero new
sections, 3 independent above-the-fold routes).

**Also fixed:** nav order contradicted DOM order (nav sent visitors to
Support then backwards to The Maker) — swapped nav links to match DOM
(cheaper fix; the fuller fix, moving Maker after Support as an
unnumbered colophon per my own finding C5, is deferred, bigger
structural change). Missing-space markup bug (`class="x"href=...`) on
every card's open-link, 13+12 instances including the 2 I added myself
(copied the bug from the pattern I was matching) — fixed globally.

Every single change this pass was verified before committing: exact-
match Python scripts (Read-then-Edit isn't viable on a 12.4MB file, so
this session used the same "count==1 assert, dry-run then --apply"
pattern established earlier for `fixes/*.html`), `check-leak.sh`, and
real Playwright reproduction of the *specific* failure being fixed (not
just a generic smoke test) before and after. 5 commits, each pushed
immediately: audio+books+fork, reveal-bug fix, nav-order+markup-hygiene.

**Explicitly NOT done yet, recorded so it isn't lost:**
- Visual and Performance/A11y audits never got to run — re-dispatching
  now that the rate limit has reset (confirmed via `date -u`, well past
  10:30pm UTC).
- Type-scale/token-system consolidation (my own finding) — real but
  large, deferred.
- The rest of Motion's findings (M4: ~30% of the motion CSS targets
  dead selectors from a pre-"Study"-system layer, including a
  fully-written hero stagger that never executes; M6-M11: easing/
  duration token consolidation, hover-state parity, staggered
  choreography) — read but not yet implemented.
- The rest of UX's findings beyond the fork (colophon nav, wayfinding,
  CTA hierarchy elsewhere on the page, mobile drawer purpose) and all
  of Brand's other findings (numbering inconsistencies elsewhere like
  `NFC · 06` appearing twice pre-fix, the hero's "inventory dashboard"
  framing, no correspondence channel for the Press, "The Maker" filed
  as an About blurb with "Follow on TikTok" as its loudest CTA) — not
  yet actioned.
- Benchmark agent's signature-moment recommendation — not yet reviewed
  in depth or acted on.
- Full report synthesis into one prioritized action plan (the user's
  original brief's "Phase 2 — Strategic Report" deliverable) — not
  yet written as a standalone document; findings exist across 6+ files
  in `.audit-view/` but haven't been consolidated.

## Update (2026-08-04, session 15 continued — hub Performance findings, image resize shipped)

Visual and Performance audits (re-dispatched after the rate-limit reset)
both completed; findings implemented so far: dead CSS deletion (~9KB,
9 anchor-bounded regions from a superseded design generation, careful
to preserve `.manifesto h2`'s italic via an explicit rule since it was
accidentally inherited from a dead block), `.st-door.primary` metal-
gradient fill, mobile colophon spacing/grid fix, and the background MP3
re-encode (175.7kbps -> 128kbps CBR, 12.4MB -> 10.06MB file).

**This pass: resized the 4 most oversized cover images + the Venmo QR**
per Performance's §2 finding. Did NOT trust the report's raw numbers —
recomputed each image's genuinely-safe target size myself using proper
`object-fit:cover` math (`scale = max(2*renderW/nativeW,
2*renderH/nativeH)` for 2x-retina), which excluded ~6 other images the
report's naive area-ratio metric had flagged as "oversampled" but were
actually undersized once aspect-ratio mismatch was accounted for (4
teaser images, Festie Codex, Music portrait — left untouched). PIL
JPEG quality=85 was tried first and *increased* size on some images
(source was already compressed harder) — dropped to quality=72, which
gave real net savings everywhere:
- Sovereign cover 692x1000->603x872 (95.2KB->66.0KB)
- Playground cover 667x1000->594x891 (143.6KB->105.7KB)
- All Fracture cover 1000x1000->872x872 (248.9KB->173.7KB)
- Sacred Divide cover 640x1147->594x1064 (174.8KB->152.2KB)
- Venmo QR 560x560->208x208 PNG (102.4KB->45.0KB)
Total ~217KB saved. Verified: visual side-by-side of original vs.
resized (no artifacts at display size, QR stays scannable-crisp),
Playwright check of all 5 images' rendered `naturalWidth/Height` +
zero console/page errors + zero external requests + no overflow.
Committed and pushed (`9acca62`).

**Tooling note:** a full-page Playwright sweep (scroll whole page +
`img.decode()` on every image) hung for 20+ minutes on this file with
no output — GPU process pegged near 100% CPU under swiftshader
software rendering, almost certainly from the page's own infinite
`.nf-leaf`/`.nf-seal` CSS animations (Performance audit's own §9
finding: non-compositable properties `background-position`/`box-
shadow` force continuous repaint) fighting for the single core. Killed
it and switched to a leaner targeted script — `reducedMotion:'reduce'`
context, `scrollIntoViewIfNeeded` + `decode()` with a 5s per-image
race-timeout only on the specific images being checked, no full-page
walk. Completed in seconds. Use this leaner pattern for future spot-
checks on this file; reserve the full-page sweep for pre-commit final
verification only, and expect it to be slow (minutes, not seconds)
until §9's animation-compositing fix ships.

Remaining Performance findings not yet done: #3 "The Fractal" cover
needs a better source image (not a resize fix), #7 font subsetting
(~500-650KB).
Remaining Visual findings: Fraunces on-load hero animation, rem/px
unit split, eyebrow-tracking consolidation, 8px spacing tokens,
`--gutter` on `.st-hero`, `--brass-dim` token, breakpoint consolidation.

## Update (2026-08-04, session 15 continued — Performance/A11y punch list cleared)

Shipped 8 more items from `.audit-view/hub-audit-performance.md`'s
summary table in one pass (commit `30a2f94`): the 3 remaining High-
priority a11y items (#4 `<noscript>` reveal fallback, #5 footer
heading h4->h3, #6 drawer focus trap), both Medium items that don't
touch the signature `.nf-leaf` hero animation (#8 brand-logo PNG
dedup ~120KB, #9 `.nf-seal` box-shadow->transform/opacity swap), and
all 4 remaining Low items (#10 `preload="none"`, #11 tap targets
44x44, #12 drawer contrast, #13 duplicate `alt`). Verified with a
single Playwright pass covering both a normal context and a separate
`javaScriptEnabled:false` context (confirmed all 21 previously-stuck
elements now render with JS off), plus real keyboard-driven Tab/
Shift+Tab testing of the new focus trap and a real click-through of
the audio toggle to confirm `preload="none"` didn't break playback.
Screenshot-verified the two visually-changed elements (Maker portrait,
open drawer).

**Deliberately left `.nf-leaf` (item #9's other half) unfixed** — the
hero H1's "light travels across the letterforms" gold gradient-text
sweep animates `background-position` on a `background-clip:text`
element, which is genuinely non-compositable, but rewriting the
technique (e.g. crossfading two offset gradient layers via opacity)
risks a visible regression to a signature hero moment I can't verify
carefully enough in one pass without more dedicated iteration+visual
review. Recorded here rather than silently dropped — worth a focused
pass on its own, not bundled into a punch-list sweep.

**Tooling note for future spot-checks on this file:** a full-page-scroll
Playwright sweep (walk the whole page + `img.decode()` every image) hit
a 20+ minute hang this session with the GPU process pegged near 100%
CPU (almost certainly the `.nf-leaf`/`.nf-seal` infinite animations
under swiftshader software rendering — `.nf-seal`'s repaint cost is
now fixed above, `.nf-leaf`'s isn't). Switched to a leaner pattern:
`reducedMotion:'reduce'` context, target only the specific elements
being verified (`scrollIntoViewIfNeeded` + `decode()` with a 5s
race-timeout per image, or no scroll at all when only DOM/computed-
style state matters), finished in seconds. Reserve a real full-page
walk for final pre-ship verification only.

Remaining Performance findings: #3 Fractal cover source image, #7 font
subsetting, and the `.nf-leaf` half of #9 (above). Remaining Visual
findings unchanged from the note above this entry.

## Update (2026-08-04, session 15 continued — Brand audit's C1 numbering fix)

User asked (a) for a link another agent could use to see book/site
content without Claude, and (b) to explain findings/decisions more
clearly going forward rather than terse commit-log style. Answered
both directly in chat (gave `https://noblefathercreations.com` + the
per-book live URLs from `sites.json`, noted the hub redesign itself
isn't deployed there yet; gave a full plain-language synthesis of all
6 audits' findings since the "Phase 2 Strategic Report" had never
actually been written up for the user, which is why the audits felt
opaque to them).

Implemented Brand audit's **C1** (its own "Highest priority... pure
bookkeeping, no design risk" finding): replaced the ambiguous
`NFC · NN` accession prefix — which had two real duplicate numbers
(Sacred Divide/Portals both `06`, Loop/Press both `07`) plus two
`00`s in Instruments, and which collided with "NFC" meaning the
near-field-communication chip elsewhere on the same page — with three
separate non-colliding registers: `VOL. I–VIII` (Library, 8 books),
`TOOL 01–02` (Decoder, Root), `PIECE 01–02` (Portals, Press). Applied
identically to card badges and the drawer index. **Also discovered
and fixed a real omission of my own**: the drawer catalogue index
still only listed 11 rows (numbered II–XIII with I/V never used) and
was missing The Loop and The Weighing entirely — added to the Library
grid earlier this session but never added to this index. Added both
missing rows; drawer now lists all 13 real items (8 Library + 2 Tools
+ 2 Workshop + Music as an unnumbered coda) in the same order as the
page. Verified by reading every badge/row back out of the live DOM
via Playwright (zero dupes, zero gaps, page/panel order match) and
screenshotting both surfaces. Commit `c8ab88b`.

## Update (2026-08-04, session 15 continued — dispatched content review + prose extraction for the other 5 books)

User asked to (1) run the same content-review treatment already done
for Loop/Scale on Sovereign, Fractal, Playground, Festival, and Root —
proofreading, content analysis, and comprehension/reading-psychology
review — (2) get an actual full-text extraction of the books' real
prose (not a summary), kept in sync as prose changes, and (3)
dispatch a design/UI specialist on book-wide chapter navigation +
resources hub + visual polish, which had been asked for earlier this
session and dropped from the roadmap by mistake. User also corrected
me: **The Root is a guided-practice tool, not a chapter book** — do
not force book/IA framing onto it (this matches `BOOKS.md`'s own
existing note, just hadn't been carried into the actual task list).

**Prose extraction, built and shipped this pass:**
`design/extract-prose.py`-equivalent (script currently only in
scratchpad, not committed — see note below) walks each book's
base64-stripped `.audit-view/*.html` copy with BeautifulSoup, strips
`script`/`style`/`svg`/`nav`/`aria-hidden` chrome, converts headings
to markdown headers and paragraphs/list items/blockquotes to text in
document order. Worked cleanly for **Sovereign (50.3K words), Playground
(47.1K), Festival (251K across ~139 entries), Fracture (87.7K)** —
sent to the user as one consolidated file. **Failed (near-zero output)
for Fractal and Root** — confirmed via grep that both store their real
content in JS data objects (`const DATA=`/`CHAPTERS=`/`TECHS=` for
Fractal; `const THEMES=`/`BODY_AREAS=`/`CONSCIOUSNESS=`/etc. for Root),
not static HTML — an HTML-walking extractor can't see it. Folded a
manual JS-literal extraction into those two books' content-review
agent briefs instead of writing a second script blind, since those
agents need to read that data closely anyway.

**Keeping the prose file in sync going forward — done, not just
planned:** committed three durable, re-runnable scripts (mirroring
`design/extract-chapters.py`'s existing precedent): `design/
extract-prose.py` (BeautifulSoup HTML walk, for the 4 static-HTML
books), `design/extract-prose-fractal.py` (Fractal's content turned
out to be a JS `const DATA = {...}` that's actually valid JSON —
parsed directly via `json.JSONDecoder().raw_decode`), `design/
extract-prose-root.py` (Root's content is a genuine branching JS state
machine — 18 real steps confirmed via its own `nextId()` switch
statement, prompts pulled from its `shell(title, subtitle, ...)` call
sites via a small string-literal parser, plus its `WHO`/`ORIGIN`/
`CONSCIOUSNESS`/`THEMES` option arrays). `design/extract-prose-all.py`
runs all three and concatenates to `.audit-view/prose/ALL-BOOKS.md`
(gitignored output, committed script) — **this is the one command to
run after any prose-changing commit to any of these 6 books**, then
re-deliver the file to the user. Tested end-to-end from the committed
scripts before considering this done — all 6 books extracted cleanly
(Sovereign 50.3K words, Playground 47.1K, Festival 251K, Fracture
87.7K, Fractal 74.7K, Root 1.6K + its branching option content) —
512,546 words total, delivered to the user.

**Dispatched 7 background agents in parallel** (all report-only,
mirroring the Loop/Scale review precedent — no source-file edits by
the agents themselves):
1. Sovereign content-review (`.audit-view/sovereign-content-review.md`)
2. Playground content-review, explicitly framed as gamification-
   appropriate (opposite stance from the adult books)
   (`.audit-view/playground-content-review.md`)
3. Festival content-review, framed for its ~139-entry glossary format
   rather than sequential chapters, told to flag the wook/festival
   title/file discrepancy explicitly if still present
   (`.audit-view/festival-content-review.md`)
4. Fracture content-review, with an extra "sourcing/rigor" priority
   tier given its 195-citation journalistic-credibility claim
   (`.audit-view/fracture-content-review.md`)
5. Fractal — JS-data extraction to `.audit-view/fractal-fulltext.md`
   **plus** content-review to `.audit-view/fractal-content-review.md`,
   framed as an interactive lookup tool not a linear read
6. Root — JS-data extraction to `.audit-view/root-fulltext.md` **plus**
   content-review to `.audit-view/root-content-review.md`, explicitly
   framed as a guided-practice tool (linear, once-through, no
   chapter-index thinking) per the user's correction above
7. `ui-designer` agent: book-wide navigation (chapter index/contents,
   prev/next, THE HOUSE cross-project tab, resources hub — per
   CLAUDE.md's chapters.json-driven architecture) + visual-
   impressiveness audit across Sovereign/Playground/Festival/Fracture/
   Fractal/Root plus Loop/Scale for consistency comparison, briefed
   with each book's established design stance from `BOOKS.md` so it
   doesn't re-flag intentional choices (Loop/Scale's no-progress-bar
   stance, Playground's gamification, Root's non-chapter format) as
   defects (`.audit-view/books-nav-visual-audit.md`)

**All 7 agents died simultaneously, seconds after dispatch** — a
session-wide API usage-limit hit, reset flagged as "6:20am (UTC)"
(checked `date -u`: dispatched at 15:32 UTC, so reset is ~15 hours
out, next-day). None wrote any output before termination (checked
`.audit-view/` — nothing new). Same class of interruption as the
mid-session rate limit hit earlier (hub audits), but this time zero
partial output survived since these had barely started. Scheduled a
`send_later` wakeup for after the reset time to re-dispatch all 7 —
recorded here in case that reminder is lost/the session ends first:
**re-dispatch the same 7 agent briefs (Sovereign/Playground/Festival/
Fracture content-reviews, Fractal/Root content-reviews — content
extraction for those two is now moot, already done by hand above, so
trim that part from their briefs on re-dispatch — and the ui-designer
book-wide nav+visual audit) once capacity is confirmed back** (check
`date -u` against the reset time before retrying, and don't re-fire
all 7 simultaneously again if a smaller batch would be safer).

When these do land: same pattern as Loop/Scale — read each report,
implement findings via exact-quote-anchored edits reusing each book's
own existing CSS components, verify with `check-leak.sh` + Playwright
before each commit, then run `python3 design/extract-prose-all.py`
and re-deliver the updated file per the sync note above.

**Deliberately not touched, and told to the user explicitly rather
than silently skipped:** the Brand audit's other high-value findings
all require either (a) real facts about the business I don't have —
an email address, city, resin type/cure time, chip rewrite count,
actual founding year, a photograph of the maker's hands — or (b) a
first-person "signed note" that would put words in the real business
owner's mouth, which isn't mine to fabricate; or (c) larger structural
calls (dissolving "Instruments" into the Library as a second shelf,
moving Support into the footer, making Maker the final chapter,
rewriting the hero headline/mantra/colophon) that deserve their own
dedicated visual-iteration pass rather than being bundled into a
numbering fix. All recorded as open, prioritized, in the chat
response — not just in this file.
