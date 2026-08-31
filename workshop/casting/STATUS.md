# Where this project stands

Branch: `claude/site-completion-status-1laz0d`

## Done

The site is complete and fully populated. All 294 photographs in the
Drive folder are ingested, classified, and tagged.

- **Portable static site.** Plain HTML/CSS/JS, no build step, no
  framework, no host lock-in. See `DEPLOYING.md` for moving it to any
  account or host.
- **Facet taxonomy** in `data/facets.json` — Subject (hierarchical),
  Type (statue / pillar / container), Finish (hand-painted / unpainted).
  No axis or value is named anywhere in the code.
- **Free-form tags**, filterable and searchable.
- **Image pipeline** — auto-centres each piece against the velvet
  backdrop, applies an adaptive tone curve, writes three WebP renditions
  (600 / 1200 / 2000).
- **A real page per piece** at `statues/<id>/index.html` with its own
  `og:image` social card, so links shared to TikTok or Facebook preview
  the actual statue. Plus `sitemap.xml` and `robots.txt`.
- **Gallery** — subject drill-down with rolled-up counts, type/finish/tag
  filters, search, compact density mode, URL state, and a full-screen
  viewer that browses between pieces with a prefilled enquire link.
- **293 pieces, all filed.** NFC-0001 through NFC-0294, minus NFC-0280
  (removed — see below). See the subject breakdown below.

## Filing and tagging (for future batches)

Folder path sets facets at ingest, matched by slug *or* human label:

```
incoming/Creatures/Dragons/Statue/IMG_1234.JPG
  → subject=creatures/dragons, form=statue
```

Or afterwards:

```bash
npm run assign -- --list
npm run assign -- --range NFC-0295..NFC-0320 --set subject=creatures/dragons
npm run assign -- --ids NFC-0300 --tags "witchy,skull,candle"
npm run validate
npm run pages          # rebuild pages + social cards after any change
```

## Decisions already made

- **Shoot JPEG, not HEIC.** This sharp build decodes only `.avif` under
  heif, so iPhone defaults fail. Settings › Camera › Formats › "Most
  Compatible". Ingest detects HEIC and explains rather than crashing.
- **Duplicate resolved:** `IMG_5492` and `IMG_5506` were the same crowned
  toad. Kept 5506 — sharper eyes and jacket — dropped 5492. `IMG_5492`
  was excluded from this batch's ingest for the same reason.
- **Subjects are built from the actual work**, not guessed. The
  taxonomy grew from 8 leaf subjects to the real spread of the
  collection: Birds (ducks, owls, other birds), Creatures (dragons,
  frogs & toads, cats, dogs, foxes, mice, lions, monkeys, turtles,
  snakes, unicorns, pigs, other creatures), Folk (figures, gnomes,
  reapers, skeletons, masks), Objects (books, flowers, hearts, hands,
  eyes, robots, torsos, containers, other objects).
- **Type finally has real pillar and container pieces** — candle
  cauldrons, mugs, planters, bowls, hand-shaped holders — not just
  statues. 49 containers, 4 pillars, 240 statues.
- **Auto-reframe isn't reliable on metallic/monochrome pieces.** The
  crop heuristic detects the subject by saturation against the black
  velvet backdrop; a bronze, silver, or gray statue can fail that test
  almost everywhere except one small colored detail (an eye, a mouth),
  so the crop zooms into that detail instead of the whole piece. This
  hit 33 of the 286 new photos. Each was re-rendered with
  `--no-reframe` (full original framing, tone curve still applied) and
  then reclassified from the corrected image — some subjects changed
  once the actual piece was visible. If this recurs at scale, the fix
  belongs in `scripts/lib/reframe.js`: fall back to the original frame
  when the detected region's *aspect ratio* is extreme relative to the
  photo, not just when its *size* is implausible.
- **NFC-0280 was removed, not filed.** Even after the re-crop it showed
  no statue — an empty shot of the inside of the light tent (LED strip,
  velvet, no piece). A photographer's misfire, not a 294th piece.
- **The book stack (NFC-0008) is filed as a statue.** If its open book
  forms a usable pocket it should become a container — one command.

## Checks

```bash
npm run validate    # ids, missing files, undeclared facet values
npm run serve       # http://localhost:8080/statues
```
