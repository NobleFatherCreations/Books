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

## Not pulled

- **wshobson/agents**, **VoltAgent/awesome-claude-code-subagents**,
  **contains-studio/agents**, **davila7/claude-code-templates** (subagent
  collections) — inspection done (see prior conversation), hold for your
  go-ahead before installing.
- **zebbern/claude-code-guide** — mentioned in the thread but not in your
  final Part 2 list; ask if you want it too.
- Full **google/fonts** monorepo — multi-GB; only sparse-checked-out the two
  font families actually needed.
