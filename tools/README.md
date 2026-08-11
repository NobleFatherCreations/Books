# /tools — vendored reference repos

Downloaded for reference and reuse. **Not auto-activated** — nothing here is
symlinked or plugin-installed into `~/.claude/` yet. Each was inspected
before pulling in (checked for postinstall hooks, telemetry, daemons,
curl-to-shell installers) — see notes per repo below.

| Folder | Source | What it's for | Risk notes |
|---|---|---|---|
| `luongnv89-claude-howto/` | github.com/luongnv89/claude-howto | Claude Code guides, slash commands, code-review skill reference | Static docs/examples. Low risk. |
| `mattpocock-skills/` | github.com/mattpocock/skills | zoom-out, diagnose, triage, tdd skill patterns | Static skill definitions. Low risk. |
| `ykdojo-claude-code-tips/` | github.com/ykdojo/claude-code-tips | 40+ tips, PR-review workflow reference | Contains `scripts/setup.sh`, opt-in only, modifies `~/.claude/settings.json` if run manually. **Not run.** |
| `FlorianBruniaux-claude-code-ultimate-guide/` | github.com/FlorianBruniaux/claude-code-ultimate-guide | Extended guide reference (`exports/` dropped to save space) | Static docs. Low risk. |
| `edwardtufte-tufte-css/` | github.com/edwardtufte/tufte-css | Long-form reading typography — top pick for the books' reading pass | CSS only. No risk. |
| `lucide-icons-lucide/icons/` | github.com/lucide-icons/lucide | 3512 inline-able SVG icons (MIT) | Only `icons/` kept, not the monorepo build tooling. No risk. |
| `animate-css-animate.css/` | github.com/animate-css/animate.css | CSS keyframes to copy piecemeal | CSS only. No risk. |
| `fonts/newsreader/`, `fonts/source-serif-4/` | github.com/google/fonts (sparse checkout) | Self-hostable refined serifs for `@font-face` | Font files only. No risk. |
| `fonts/fraunces/`, `fonts/public-sans/` | github.com/google/fonts (sparse checkout) | The book's own already-chosen typefaces. **Not needed for loop.html** — that page already embeds these properly (20 `@font-face` rules, base64, see MEMORY.md correction) — kept in case another book references Fraunces/Public Sans without having embedded it yet. Check first before assuming it's missing. | Font files only. No risk. |
| `Digital-Process-Tools-claude-remember/` | github.com/Digital-Process-Tools/claude-remember | Auto session-save/compress/reload via Claude Code lifecycle hooks (`SessionStart`, `PostToolUse`, etc.) | **Hooks into Claude Code with full shell privileges** (their own README says so explicitly). Storage is local-first by default (`.remember/` in-project or `~/.remember/`), no telemetry found. Optional git-backup feature can push memory to a remote *you* configure — off by default. **Not installed/activated** — see caveat below. |
| `remember-md-remember/` | github.com/remember-md/remember | Structured "second brain" — Obsidian-compatible vault (People/Projects/Notes/Tasks/Journal, wikilinked) | Also hook-based, also local-first, no telemetry found. Naming collides with an unrelated "remember" plugin in the default `claude-plugins-official` marketplace — install carefully if you do this yourself. **Not installed/activated.** |
| `vibehat-claude-task-manager/` | github.com/vibehat/claude-task-manager | "Personal AI project manager" — Next.js web UI over Task Master CLI | **Not a lightweight hook — a full app**: dev server, WebSocket server, Signal server, `kill:dev` script implies long-running background processes. This is the same category of thing gstack was declined for. **Not recommended to run in this environment** — vendored for reference only, flag before ever activating. |

## Why the two "remember" plugins aren't activated

Both are legitimate, well-documented, and free of anything that looks like
telemetry or a background daemon — but activating a Claude Code plugin here
(`claude plugin install ...`) writes to `~/.claude/plugins/` in *this*
container's home directory, which is **not the same thing as this git
repo**. A brand-new remote session spins up a fresh container with a fresh
home directory — only what's committed to this repo carries over. So
installing these plugins in this session would not actually get you
"remembers across a new chat" the way it would on your own local machine.

**What actually gives cross-session memory in this environment:**
`MEMORY.md` at the repo root (git-committed, loaded by any session that
reads this repo). That's the real fix for "find stuff cross-thread" here —
see that file.

If you want the two "remember" plugins running on *your own local machine*
(where Claude Code sessions persist on the same disk), install them there
directly per their READMEs — that's the environment they're built for.

## Batch 2 (2026-08-02) — impeccable, Higgsfield MCP, and the rest of the original wishlist

| Folder | Source | What it's for | Risk notes |
|---|---|---|---|
| `dietrichgebert-ponytail/` | github.com/dietrichgebert/ponytail | Full source for the 6 ponytail skills already wired into `.claude/skills/` | No postinstall, no network calls in hooks/MCP code. MIT. |
| `geopopos-higgsfield_ai_mcp/` | github.com/geopopos/higgsfield_ai_mcp | MCP server for Higgsfield AI image/video generation | Third-party (unofficial), small (fastmcp/httpx/dotenv only), calls only `platform.higgsfield.ai`. **Needs your own `HF_API_KEY`/`HF_SECRET`** (paid account) to do anything — inert without it. Wired into `.mcp.json` with empty placeholders. |
| *(impeccable itself lives in `.claude/skills/impeccable/` + `.claude/agents/impeccable-*.md`, not here — see `.claude/skills/README.md`)* | github.com/pbakaus/impeccable | Real source of the "impeccable" design skill named in the review package's own bootstrap doc | Apache 2.0. Disclosed anonymous "choice ping" telemetry, opt-out via `IMPECCABLE_NO_TELEMETRY`/`DO_NOT_TRACK` env var, fire-and-forget, never blocks. No daemon. |
| `fonts/league-gothic/` | github.com/theleagueof/league-gothic | League of Moveable Type font | Font files only. |
| `fonts/inter/` | github.com/rsms/inter (sparse: `docs/font-files`) | Inter UI sans | Font files only. |
| `feathericons-feather/` | github.com/feathericons/feather | Minimal icon set (Lucide's origin) | SVG only. |
| `tabler-icons/icons/` | github.com/tabler/tabler-icons (sparse: outline+filled) | Large icon set | SVG only. |
| `tailwindlabs-heroicons/` | github.com/tailwindlabs/heroicons | Tailwind-team icon set | SVG only. |
| `IanLunn-Hover/` | github.com/IanLunn/Hover | Pure-CSS hover effects | CSS only. |
| `miniMAC-magic/` | github.com/miniMAC/magic | CSS-only entrance animations | CSS only. |
| `sindresorhus-modern-normalize/` | github.com/sindresorhus/modern-normalize | Cross-browser CSS reset | CSS only. |
| `yeun-open-color/` | github.com/yeun/open-color | Balanced open color palette (reference for the dark/gold/crimson system) | CSS/JSON only. |
| `zebbern-claude-code-guide/` | github.com/zebbern/claude-code-guide | Setup/workflow reference | Static docs. |
| `VoltAgent-awesome-claude-code-subagents/` | github.com/VoltAgent/awesome-claude-code-subagents | 154+ subagent catalog, browsable | Static `.md` agent defs, not installed as active agents — 12 already are (see `.claude/agents/`), adding 150+ more would be redundant bloat. Browse and pull individually if a specific role is missing. |
| `davila7-claude-code-templates-agents/` | github.com/davila7/claude-code-templates (only the `agents/` folder, not the full 161MB CLI+dashboard repo) | 29 category folders incl. `ffmpeg-clip-team` (relevant to the clip pipeline), `podcast-creator-team`, `deep-research-team` | Static `.md` agent defs. Not installed as active agents, same reasoning as VoltAgent's. |

**Not pulled — unDraw.** Tried `undraw/undraw.github.io` and two other
guessed names; none exist as a public git repo (proxy returned an auth
prompt, not a 404, suggesting they're genuinely not there in that form).
Not worth guessing further — illustrations aren't essential to the design
system, and unDraw is normally used via their web picker, not a repo clone.
If you have the actual URL, send it and I'll pull it.
