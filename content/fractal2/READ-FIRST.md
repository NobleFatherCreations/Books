# Fractal² — what to read, in what order (cost-efficient)

Read **Tier 1** in full before planning. Use **Tier 2** when the task needs it. **Skip** the rest. Word counts are approximate.

## Tier 1 — read fully (~22,000 words)

| # | File | Words | Why |
|---|---|---|---|
| 1 | `content/fractal2/HANDOFF.md` | 570 | State of play and hard-won rules |
| 2 | `content/fractal2/owner-source/E-owner-messages-this-thread.md` | 1,700 | **The owner's own words. They win every conflict.** |
| 3 | `content/fractal2/intro-v4.md` | 3,400 | The draft you reimagine |
| 4 | `content/fractal2/owner-source/D-enlighten-closing-monologue-transcript.md` | 1,550 | The series' ending: traditions, the descent, the frequency |
| 5 | `content/fractal2/owner-source/A-spiritual-lens-interlude-script-part1.md` | 5,600 | The counterfeit, the 8 inversions, the 30-sector dominion table, the Garden, "the body knows" |
| 6 | `CLAUDE.md` | 2,000 | Binding house rules (self-contained pages, accessibility, versioning, deploy hygiene) |
| 7 | `content/fractal/ent/source/readable/ENT_combo_index.md` | 3,800 | All 153 combos: name, family, tier, tactics, definition, safety flag |
| 8 | `content/fractal/ent/source/ENT_top10.md` | 3,000 | The ranked ten, with scores |
| 9 | `content/fractal/ent/build/audit.md` | 850 | Tag counts, fill-in blanks, the 131 unresolved names, defects |
| 10 | `content/decoder-v20/START_HERE_FOR_YOUR_AI.md` | 350 | How the Decoder's names and ids work |

## Tier 2 — read when the work needs it

- `content/fractal2/owner-source/B-part-III-the-war-map.md` (3,700): the three fronts. Needed for "what this is for" and the policy-list question.
- `content/fractal2/owner-source/C-inner-techniques-17-30-cage-intent-mirror-practice.md` (7,400): the Cage & Intent (three categories of intent), the Full Mirror, the Practice. Read the Cage & Intent section for the accountability framing.
- `docs/FRACTAL2-STORY-BLUEPRINT.md` (2,200): the second-model critique of structures. Worth reading before writing.
- `docs/FRACTAL-SERIES-INDEX.md` (8,100): use as a lookup. Section G.2 lists inconsistencies; G.3 lists risks.
- **The published Fractal** in `library/fractal/`. Read the interludes you draw on (`the-origin`, `the-mirror`, `the-chain`, `the-frequency`) and check which sector pages exist before linking.
- **ENT tactic book**: `content/fractal/ent/source/readable/ENT_tactic_book_335.json` (use it programmatically). The `.md` is 40,000 words; read only the entries you quote.
- **ENT combo scripts**: `content/fractal/ent/source/scripts/` (~467,000 words). Do **not** read them all. Read The Debt Prison (C018), Pavlovian Conditioning (C025), Grooming (C001), The Room (C193) and The Phantom Equity (C169) in full, then process the rest programmatically or through delegated packets.
- **The pipeline**: `design/fractal-sector/README.md` first, then the code as needed; the built prototype is in `library/fractal/sectors/ent/site/`.
- **Decoder data**: `content/decoder-v20/alias_map.json`, `standard_index.json`, `playbook_patterns.json` (programmatic); the live pages are in `instruments/playbook/site/`.
- `sites.json`, `hub/catalogue-redesign._redirects`, the end of `MEMORY.md`: only before touching addresses or routing.

## Skip

- `content/fractal2/mission-draft.md`: superseded by intro-v4.
- `docs/FRACTAL-SERIES-INDEX.pdf`: the same as the `.md`.
- The ENT PDFs: not in the repo, and every word is in the Markdown and JSON.
- Any JSON already covered by its `.md` twin, unless you are processing it in code.
