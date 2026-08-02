# Noble Father Creations — Standing Rules

Read `PROJECT-MASTER.md` for full context/history, `sites.json` for the live
project registry, and `chapters.json` for book/chapter data. This file is
the always-on rulebook — treat it as binding, not a suggestion.

## Self-contained architecture (non-negotiable)

Every book is: no dependencies, no external requests, no storage, fully
offline-capable — including THE HOUSE nav tab. Never add a CDN `<script>` or
`<link>` tag. Always inline:
- Fonts → self-hosted `@font-face` (see `tools/fonts/`), subset/base64 as needed.
- Icons → inline SVG (see `tools/lucide-icons-lucide/icons/`), never an icon font.
- Animation → copy CSS keyframes from `tools/animate-css-animate.css/` piecemeal;
  scroll fades use native `IntersectionObserver`, no library.
- Reading typography → Tufte CSS principles (`tools/edwardtufte-tufte-css/`).

## Design standard

Target: press.stripe.com (typography + a title/cover moment per book),
aeon.co (reading-progress bar, ~60–70 char measure), waitbutwhy.com /
The Marginalian (a real chapter-index page, a resources hub). Confirm/replace
these references with the user's own if named later.

Rules: generous whitespace, max 2 fonts with a dramatic scale, one restrained
accent only, strict 8px spacing grid, subtle micro-interactions (0.2–0.3s
hover/scroll easing). Iterate in passes — structure, type, space, motion,
then a self-critique pass ("what would a $100k agency art director cut?").
Preserve the dark theme, MOVEMENT labels, numbered chapter cards, and THE
HOUSE tab across every book.

## Book system architecture

`chapters.json` is the single source of truth (project, movement, n, title,
blurb, readMin, slug, url). Generate from it, never hand-maintain per page:
the chapter-index/contents page, Prev/Next nav, reading-progress bar, and
THE HOUSE cross-project map.

## Channel routing

- Books → warm, curious, value-first voice.
- Craft/business (NFC wax seals, candles, resin) → visual, premium,
  product-focused voice.
- Music → mood, behind-the-scenes voice.
Tag content by category at creation; never manage channels by hand.

## Clip pipeline (long video → many posts)

Input: timestamped transcript. Output: 30–50 clips (15–90s), each with
start/end time, hook title, category, virality score, caption, 5 hashtags.
Then: Claude writes an FFmpeg batch script to cut + crop to 9:16; Whisper
auto-captions; category tag routes each clip to its channel. Always surface
the top 5–10 "post first" clips. Free/open-source stack only.

## Outreach system

Loop: Analyze (core value, ideal audience, hook) → Find (~20 real targets)
→ Draft (personalized, <150 words, leads with value to *their* audience) →
Track (`outreach-tracker.csv`). **Human-in-the-loop is mandatory** — never
auto-send. Frame: "I made something free that will genuinely help the
people you serve," not self-promotion.

## Deploy hygiene

- Repo is the source of truth wherever a repo exists (currently only `wook`
  — this repo). Live must always match it.
- Never ship build-instruction comments or `#REPLACE`/`data-here`-style
  placeholders to a live page — see `sites.json` → `houseTabLeak` for
  current leak status per project, and `fixes/` for verified corrected HTML
  awaiting redeploy.
- Most projects (loop, scale, faith, playbook, etc.) are Netlify CLI/API
  deploys with **no connected GitHub repo** — confirmed via deploy metadata
  (`commit_ref: null`). A git push cannot fix them; they need a direct
  Netlify redeploy. Treat any such redeploy as a production write requiring
  explicit user go-ahead, same as any other environment-wide change.

## Safety rules

1. Inspect any third-party repo before installing — report what it does,
   whether it adds hooks/daemons/telemetry/remote-sync, whether it installs
   persistently into `~/.claude/`.
2. Never install telemetry, background daemons, remote "brain" sync, or
   curl-to-shell installers without explicit yes.
3. One-off/scoped/readable commands: just run them. Environment-wide,
   persistent, or production-writing actions: ask first.
4. Stay scoped to the current repo unless global installs/deploys are
   explicitly approved.
5. `garrytan/gstack` is declined, permanently, for this project — telemetry,
   daemons, multi-host auto-registration, curl-to-shell installer.
