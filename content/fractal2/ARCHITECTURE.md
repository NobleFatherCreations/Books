# Fractal² — architecture (2026-11-10)

## What is built from what

```
content/fractal2/intro-final.md ──┐
content/fractal2/sectors.json ────┼─ design/fractal2/build_intro.py ─→ library/fractal2/site/fractal2.html        (/fractal2)
design/fractal2/{tokens,intro}.css│                                    library/fractal2/site/fractal2/_a/f/      (fonts)
design/fractal2/intro.js ─────────┘                                    library/fractal2/site/fractal2/_a/au/     (narration + timing)
                                                                        content/fractal2/narration-script.md      (generated)

content/fractal/<s>/source/  (author's package, never edited)
   └ design/fractal-sector/ingest.py  → content/fractal/<s>/build/{sector.json, review_queue.json, audit.md}
   └ design/fractal-sector/derive.py  → build/{links.json, derived.json, <s>-search.json}   (+ content/fractal/<s>/nav.json settings rules)
   └ design/fractal-sector/resolve.py → content/fractal/<s>/resolution/{ledger.json, facts.json, todo.jsonl, SUMMARY.md}
   └ design/fractal-sector/build.py   → library/fractal2/site/fractal2/<slug>.html and /<slug>/**   (/fractal2/<slug>/…)
                                         library/fractal2/manifests/<s>.json, library/fractal2/redirects/
   └ design/fractal-sector/verify.mjs   (26 checks: the original 16 plus the new ones)
```

One command per sector: `design/fractal-sector/run.sh ent`. The intro: `python3 design/fractal2/build_intro.py` then `node design/fractal2/verify_intro.mjs`. Local preview of everything at production addresses: `python3 design/fractal2/serve.py 8802` → `http://127.0.0.1:8802/fractal2`.

## Addresses

- Base path `/fractal2` comes from `content/fractal2/sectors.json` → `base`. Nothing else hard-codes it.
- `/fractal2` the intro · `/fractal2/<sector>` a sector home · `/fractal2/<sector>/<page>` · shared files `/fractal2/_a/{f,d,au,og}/`.
- Pages are flat `.html` files served without the extension. Every link is absolute.

## Routing (nothing here is deployed)

1. **One new Netlify site** (suggested name `fractal2`) publishes `library/fractal2/site/`.
2. **The hub** (`noblefathercreations.com`) needs two lines above its `/fractal/*` rule, in `hub/catalogue-redesign._redirects`:
   ```
   /fractal2      https://<fractal2-site>.netlify.app/fractal2          200
   /fractal2/*    https://<fractal2-site>.netlify.app/fractal2/:splat   200
   ```
   The exact lines are generated into `library/fractal2/redirects/HUB-RULES.txt`. `hub/` is not edited by this project.
3. **The old public prototype** (`fractal-entertainment.netlify.app/fractal/entertainment/...`): `library/fractal2/redirects/old-prototype._redirects` sends every old address to its new one with a 301. Deploying that file to the old site is a production write and needs the owner's word. The hub's pending, undeployed `/fractal/entertainment` rule should be dropped in favour of step 2.
4. `robots.txt` on the hub gains one sitemap line per Fractal² sitemap when the owner publishes.

## The intro page

- **Text**: `intro-final.md`. Markers (HTML comments) place scenes, figures, step lists and connector links; see the header of that file.
- **Stage**: one WebGL canvas fixed behind the text, one field of 30,151 points (Canvas 2D fallback; no-JS and reduced-motion fallbacks are complete). Formations are functions in `intro.js` (`S.<scene>`). The scroll position sets a target; points chase it with damping, so every transition is interruptible.
- **Layout**: wide screens put the text in a left column and the stage on the right; narrow screens put the stage behind the text, dimmed during prose and bright during figures, with step cards held in the lower third.
- **Narration**: reader-started; `_a/au/intro.mp3` + `intro.sync.json`; captions come from the page text.

## The sector site

See `NAV-SPEC.md`. Reading modes are views over one document. Reader input (search, filters, "what are you noticing") never leaves the page and is never stored.

## Cross-sector

- `combo_id` (C-numbers) and tactic `standard_id` are the stable keys. They never appear to readers.
- `content/fractal2/sectors.json` registers the thirty sectors; set `built: true` and fill `id`, `slug`, `title` to add one.
- `content/fractal/_crosslinks.json` (created when a second sector exists) powers "this pattern in other sectors".

## House rules honoured

No CDN, no framework, no third-party request except the sanctioned Cloudflare beacon; self-hosted fonts; absolute links; THE HOUSE drawer and beacon on every page; a version note on each site; nothing stored on the reader's device.
