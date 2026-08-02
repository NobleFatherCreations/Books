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

## Standing decisions (don't re-litigate these)

- Books are self-contained: no deps, no external requests, no storage,
  offline-capable.
- `garrytan/gstack` declined permanently (telemetry, daemons, curl-installer).
- Design references: Stripe Press / Aeon / Wait But Why (pending user's own
  confirmation if they'd rather name different ones).
- Outreach and publishing: human-in-the-loop always, no auto-send.
- Palette question (emerald+gold gallery vs. dark+gold+crimson books):
  explicitly deferred by user, not decided.
