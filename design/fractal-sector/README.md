# Fractal sector sites

One command turns a sector package into a verified site:

```sh
npm i --no-save axe-core            # once per container
design/fractal-sector/run.sh ent    # import + audit, build, social cards, verify (about 25 s)
design/fractal-sector/run.sh ent production   # same, applying the production publish gate
```

| Step | File | Output |
|---|---|---|
| Import + audit | `ingest.py` | `content/fractal/<s>/build/sector.json`, `review_queue.json`, `audit.md` |
| Build | `build.py`, `style.css`, `site.js` | `library/fractal/sectors/<s>/site/` (the publish dir) |
| Social cards | `og.mjs` | `site/fractal/<slug>/og/*.png` (home, 8 stages, 10 families) |
| Verify | `verify.mjs` | 16 checks; exit 1 on any failure |

## Rules the pipeline enforces

- **The author's files are never written.** `content/fractal/<s>/source/` is the package as delivered. Everything else is derived.
- **Word count round trip.** For every combo, the author words on the page must equal the words in the source (minus production cues, credibility tags and the Credibility Audit). Exact match, not approximate.
- **Safety.** If a script has "Safety Note (read first)", it renders first on the page; verify fails otherwise. Escalation Triggers and Safer Response Language are never dropped.
- **No internal ids for readers.** URLs use name slugs; C-numbers stay in the data (`combo_id` is the key of every record, for cross-sector links later).
- **Links from ids only.** Combo to tactic links use the author's reverse index first, then an exact name or alias match. Anything else renders as plain text and is listed in `audit.md`. No fuzzy matching.

## The credibility system (tags are tracked, not errors)

`content/fractal/<s>/review_state.json` (owner-maintained): one entry per combo, `unreviewed` (default), `expert_reviewed` or `sources_verified`.

- Tags become reader labels: *Composite*, *Common pattern*, *Varies by place*, and *Awaiting expert review* / *Source being checked*, which switch to *Expert reviewed* / *Source verified* as the state moves up.
- Each combo page shows its state at the top, with a legend at the bottom.
- `review_queue.json` holds every tag in context plus every Credibility Audit item: the reviewer's to-do list.
- Publish gate: `PUBLISH_STATES` in `build.py` (one line) decides which states reach production. Held-back combos get no page and appear as plain text where linked.

## Audit passes (`audit.md`)

1. Structure: all 17 sections present.
2. Safety note in the file matches the index.
3. Bracket inventory: tags go to the queue, fill-in blanks (`[X]`, `[date]`) are listed, unknown brackets are flagged. Compound tags (`[A; B]`) count as both.
4. Credibility Audit kept as data.
5. Tactic resolution (reverse index, exact, unresolved).
6. Index consistency: tag counts in the author's index vs the file.

## Addresses

The publish dir nests pages at `fractal/<slug>/...`, so the same files work on the sector's own Netlify URL and behind the hub proxy. The hub needs one rule above its `/fractal/*` line:
`/fractal/<slug>/*  https://<sector-site>.netlify.app/fractal/<slug>/:splat  200` (plus `/fractal/<slug>` for the home page).
