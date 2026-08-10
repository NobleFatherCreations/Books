# Extracted book/tool prose

The actual written content of every Noble Father Creations book and tool,
pulled straight out of each project's own shipped source and stripped of
all HTML/CSS/JS — nothing invented, nothing summarized. This exists so any
AI (or human) can read the real words of a book without having to parse an
8MB single-file HTML app to find them.

Regenerate any time a book's content changes:
`python3 design/extract-prose-master.py --apply` (dry-run without `--apply`
prints word counts only, writes nothing).

## Coverage

| File | Words | Source | Method |
|---|---:|---|---|
| `sovereign.md` | 52,175 | `source/projects/noble-father-sovereign.html` | static HTML |
| `playground.md` | 47,128 | `source/projects/noble-father-playground.html` | static HTML |
| `festival.md` | 250,974 | `source/projects/noble-father-festival.html` | static HTML |
| `fracture.md` | 87,815 | `source/projects/noble-father-fracture.html` | static HTML |
| `loop.md` | 25,727 | `fixes/loop.html` | `BODIES[n]` template literals |
| `scale.md` | 18,781 | `fixes/scale.html` | `BODIES[n]` template literals |
| `fractal.md` | 74,682 | `source/projects/noble-father-fractal.html` | `const DATA` JS object |
| `root.md` | 340 | `source/projects/noble-father-root.html` | state-machine prompts |
| `playbook.md` | 11,387 | `content/prose/_raw/playbook.html` (fetched live — no git source exists) | `COMPENDIUM` JSON array |
| `music.md` | 46 | `content/prose/_raw/music.html` (fetched live — no git source exists) | static HTML |
| `faith.md` | 561 | `source/projects/faith-index.html` | static HTML — **partial, see below** |

`ALL-BOOKS.md` is every file above concatenated into one document.

## `faith.md` is incomplete — the one real gap

The Coercive Control Codex ("The Sacred Divide") examines 27 religious
traditions, but that per-tradition content is not stored as static HTML or
as a clean named data object the way every other book is. It sits inside a
heavily minified bundle — single-letter variable names (`A`, `B`, `C`, `D`,
`G`, `K`, `L`, `P`, `Q`...), with the actual religions array referenced as
`D.religions` from multiple renderer functions but never assigned at a
`const D=`/`var D=` top level I could find — `D` appears to arrive as a
function parameter from somewhere else in the bundle.

`faith.md` currently holds only the ~560-word front-matter (the "five
screens, about two minutes" intro). Rather than hand-parse an unverified
nested minified structure via byte-offset guessing — which risks silently
truncated or misattributed output that would then get trusted as ground
truth — I stopped and flagged it here instead. Recovering the full 27-
tradition content needs either a real JS engine to evaluate the bundle and
dump the live object, or the un-minified source if one exists somewhere.

## Two files have no git-tracked source at all

`playbook` (The Pattern Decoder) and `music` (The Listening Room) were
never checked into this repo — `sites.json` has always recorded their
`localSource` as none. Both were fetched live from
`noblefathercreations.com/playbook` and `/music` and saved to
`content/prose/_raw/` specifically so this extraction has a reproducible
input; that raw HTML is a mirror of what's currently live, not a source of
truth the way the git-tracked books are — if either project changes, these
go stale until re-fetched.

## `root.md` and `music.md` are short on purpose

The Root is an 18-step guided practice moved through once, not browsed
like chapters — its real content is short prompts, not long-form prose.
The Listening Room is a music page; the only text on it is framing copy,
not "chapters." Both extracted everything that exists; neither is missing
content the way `faith.md` is.
