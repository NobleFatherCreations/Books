# Fractal² sector sites

One command turns a sector package into a verified site under `/fractal2/<sector-slug>`:

```sh
npm i --no-save axe-core            # once per container
design/fractal-sector/run.sh ent    # import + audit, derive, build, social cards, verify (a few minutes)
design/fractal-sector/run.sh ent production [--base /fractal2]
python3 design/fractal2/serve.py 8802   # then http://127.0.0.1:8802/fractal2/entertainment
```

The navigation design is `content/fractal2/NAV-SPEC.md`; the look is `design/fractal2/tokens.css` ("Deep field") plus `sector.css`.

| Step | File | Output |
|---|---|---|
| Import + audit | `ingest.py` | `content/fractal/<s>/build/sector.json`, `review_queue.json`, `audit.md` |
| Derived navigation data | `derive.py` (reads `content/fractal/<s>/nav.json`) | `build/links.json` (Decoder + Fractal links, resolved chains), `build/derived.json` (settings, positions, shared patterns, reading times, map tables), a section appended to `audit.md` |
| Build | `build.py` → `lib.py`, `frame.py`, `pages_index.py`, `pages_combo.py`, `pages_tactic.py`, `sector.css`, `site.js`, `strings.json` | `library/fractal2/site/fractal2/<slug>.html` + `<slug>/**`, `fractal2/_a/f/` (fonts), `fractal2/_a/d/<s>-search.json`; `library/fractal2/manifests/<s>.json`; `library/fractal2/redirects/` |
| Social cards | `og.mjs` | `site/fractal2/<slug>/og/*.png` (home, 8 stages, 10 families) |
| Verify | `verify.mjs` | 26 checks; exit 1 on any failure |

`library/fractal2/site/` is shared with the intro (built by `design/fractal2/`). The generator cleans only the sector's own outputs, never the whole directory.

## Adding a sector

Drop the package in `content/fractal/<id>/source/`, write `content/fractal/<id>/nav.json` (settings rules and the sector phrases), set `id`, `slug`, `title`, `built: true` in `content/fractal2/sectors.json`, run `design/fractal-sector/run.sh <id>`.

## Rules the pipeline enforces

- **The author's files are never written.** Everything outside `source/` is derived.
- **Word count round trip.** For every combo, the author words on the page (inside `data-src`) equal `reader_words` from ingest. The three reading modes only show and hide sections; no text is duplicated or dropped.
- **Safety.** The safety note renders first and carries every reading mode; Escalation Triggers and Safer Response Language are never dropped.
- **No internal ids for readers.** No C- or T-numbers in reader text or URLs.
- **Links from ids only.** Tactic names resolve through the author's reverse index, exact names, then the Decoder's `alias_map.json` (its own key format) to a standard id; Decoder pages link only if the file exists in `instruments/playbook/site/`; Fractal anchors only if the id exists in the published file. Anything else is plain text and listed in `audit.md`. No fuzzy matching.
- **Interface words** are in `strings.json` (owner review); sector phrases in `nav.json`.

## Settings

`content/fractal/<s>/nav.json` → `settings`: a pattern is in a setting when one of the author's tags is listed there, exactly. Coverage is printed by `derive.py` and written to `audit.md`.

## The credibility system

`content/fractal/<s>/review_state.json` (owner-maintained): `unreviewed` (default), `expert_reviewed` or `sources_verified`. Tags become reader labels (packet 04 replaces these with the resolved states). Publish gate: `PUBLISH_STATES` in `lib.py`.

## Addresses and redirects

Pages are flat `.html` served extensionless (Netlify pretty URLs). `library/fractal2/redirects/old-prototype._redirects` sends every old `/fractal/<slug>/…` path of the prototype site to the new address (301); `<s>-site._redirects` holds the in-site rules (`stage-extract`, `standards`) to merge into the publish dir's `_redirects`; `HUB-RULES.txt` lists the lines the hub would need. Nothing here edits `hub/`.
