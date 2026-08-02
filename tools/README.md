# /tools — vendored reference repos

Downloaded for reference and reuse in the books' premium-design pass. **Not
auto-loaded as Claude skills/agents** — nothing here is symlinked into
`~/.claude/`. Each was inspected before pulling in: no postinstall hooks, no
telemetry, no daemons, no curl-to-shell installers run.

| Folder | Source | What it's for |
|---|---|---|
| `luongnv89-claude-howto/` | github.com/luongnv89/claude-howto | Claude Code guides, slash commands, code-review skill reference |
| `mattpocock-skills/` | github.com/mattpocock/skills | zoom-out, diagnose, triage, tdd skill patterns |
| `ykdojo-claude-code-tips/` | github.com/ykdojo/claude-code-tips | 40+ tips, PR-review workflow reference (contains `scripts/setup.sh` — **not run**, opt-in only, modifies `~/.claude/settings.json` if you choose to run it) |
| `FlorianBruniaux-claude-code-ultimate-guide/` | github.com/FlorianBruniaux/claude-code-ultimate-guide | Extended guide reference (pre-rendered `exports/` dropped to save space) |
| `edwardtufte-tufte-css/` | github.com/edwardtufte/tufte-css | Long-form reading typography — top pick for the books' reading pass |
| `lucide-icons-lucide/icons/` | github.com/lucide-icons/lucide | 3512 inline-able SVG icons (MIT). Only the `icons/` folder was kept — the build tooling wasn't. |
| `animate-css-animate.css/` | github.com/animate-css/animate.css | CSS keyframes to copy piecemeal — don't link the whole file, extract just the classes used |
| `fonts/newsreader/` | github.com/google/fonts (ofl/newsreader, sparse checkout) | Self-hostable refined serif — variable font, embed via `@font-face` |
| `fonts/source-serif-4/` | github.com/google/fonts (ofl/sourceserif4, sparse checkout) | Alternate self-hostable serif option |

## Not pulled

- **wshobson/agents**, **VoltAgent/awesome-claude-code-subagents**,
  **contains-studio/agents**, **davila7/claude-code-templates** (subagent
  collections) — inspection pending, hold for your go-ahead per the safety
  rules.
- **zebbern/claude-code-guide** — mentioned in the thread but not in your
  final Part 2 list; ask if you want it too.
- Full **google/fonts** monorepo — multi-GB; only sparse-checked-out the two
  font families actually needed.
