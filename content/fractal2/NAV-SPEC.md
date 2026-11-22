# Fractal² sector sites — navigation spec (v1, 2026-11-09)

Applies to every sector site under `/fractal2/<sector-slug>`, first built for Entertainment & Music (`ent`, slug `entertainment`). Everything here is produced by the generator (`design/fractal-sector/`), from data, so the next sector inherits it by running one command.

## 1. Who arrives, and what each needs first

| Reader | Arrives with | Needs within 10 seconds | Path |
|---|---|---|---|
| Someone inside it now | Fear, little time, maybe a watched device | A safety line, "what comes next", words to use, when to get help, a fast exit | `in-it-now` |
| A survivor looking for words | A memory that will not resolve | A way to find the pattern by what it felt like, then the full scene | `notice` → combo (full) |
| A parent or friend | Worry about someone else | Signs you can see from outside; what helps; what not to do | `worried-about-someone` |
| An artist about to sign | A document and a deadline | The patterns that live in contracts and money; the tests; the words to ask with | `before-you-sign` |
| A professional or advocate | A caseload or a class | Everything, filterable; the method; the labels; printable pages; how to cite | `patterns`, `tactics`, `method`, `take-it-with-you` |
| A skeptic | Distrust | What this is and is not; how it was made; the ordinary explanations to rule out first | `method` |
| A searcher from Google | One page, no context | That page must stand alone: what it is, where it sits, where to go next | every page |

Rule: **every page is a landing page.** Breadcrumbs, the sector switcher, search and a short safety line are on all of them.

## 2. Addresses (all absolute, base path configurable)

`BASE` is `/fractal2` (config, never hard-coded). `S` = `BASE/<sector-slug>`.

| Address | What |
|---|---|
| `BASE` | The intro (built separately by `design/fractal2/`) |
| `S` | Sector home |
| `S/start` | The ten that matter most, with scores |
| `S/patterns` | All combos: sort, filter, search |
| `S/tactics` | All tactics by stage (index of the eight stage chapters) |
| `S/map` | The living map: tactic ↔ combo graph |
| `S/notice` | "What are you noticing?" |
| `S/in-it-now`, `S/worried-about-someone`, `S/before-you-sign` | Reader paths |
| `S/method` | What this is, how it was made, what the labels mean (absorbs "sector standards") |
| `S/take-it-with-you` | Downloads and printing |
| `S/a-z` | Every tactic and combo, alphabetical (the no-JS fallback for search) |
| `S/stage-<slug>` | One chapter per stage: every tactic in it, in full (definition + three levels) |
| `S/family-<slug>` | One page per combo family |
| `S/tactic/<slug>` | One page per tactic |
| `S/<combo-slug>` | One page per combo (kept flat: these are the pages people share) |
| `BASE/_a/…` | Shared files: fonts (`f/`), search and map data (`d/`), audio (`au/`) |

Pages are flat `.html` files served without the extension (Netlify pretty URLs), as in the prototype. Combo slugs may not collide with the reserved names above; the generator asserts this.

**Old addresses.** `S_old = /fractal/entertainment/...` → 301 to the same page under `S`; `stage-control` keeps working; `standards` → `method#standards`. The generator writes these into `_redirects` for the old Netlify site and prints the hub rules needed (it never edits `hub/`).

## 3. The frame on every page

1. **Top bar** (sticky, one row, 56px): the mark `Fractal²` (→ `BASE`); the **sector switcher** (a button showing the current sector; opens a panel listing all thirty sectors from `content/fractal2/sectors.json`: built sectors link, the rest are listed as "not yet mapped" and, where The Fractal has a chapter, link there labelled "in The Fractal"); **Search**; **Leave** (quick exit: replaces the page with a neutral site; Escape twice does the same; behaviour kept from the prototype).
2. **Breadcrumbs**: `Fractal² / Entertainment & Music / …`.
3. **Footer**: the path links, The Fractal, the Pattern Decoder, the short safety line (kept from the prototype, verbatim), licence/author line, version + updates link.
4. THE HOUSE drawer and the Cloudflare beacon, exactly as now (`design/decoder-v10/assets/house.html`, `beacon.html`).

**Search.** A dialog (focus trapped, Escape closes, `role="dialog"`). Index = tactic names + "also called" + combo names + first sentence of each definition, loaded on first open from `BASE/_a/d/<sector>-search.json`. Results grouped Patterns / Tactics, keyboard navigable (arrow keys, Enter). Without JavaScript the Search control is a plain link to `S/a-z`. Nothing typed is stored or sent anywhere.

## 4. Sector home (`S`)

In order:
1. **Cover**: kicker `Fractal² · Sector 01`, the sector title, one line ("How manipulation works in music and entertainment: 335 tactics at three levels, 153 patterns where they combine, and a way out of each."), the three numbers as figures.
2. **"Where are you right now?"** Six plain doors (links, not a quiz):
   - *Something feels off and I can't name it* → `notice`
   - *I'm in it now* → `in-it-now`
   - *It happened to me and I want the words* → `start`
   - *I'm worried about someone* → `worried-about-someone`
   - *I'm about to sign something* → `before-you-sign`
   - *I work with artists, or I want to check this* → `method`
3. **Start here**: the top ten as a ranked list. Each row: rank, name, the "why it ranks" line, four small score bars (likelihood, harm, hidden, recognised; each out of 5, with the number as text), `2-minute read` and `full pattern` links. The scoring method sentence sits under the list ("editorial judgments, not statistics").
4. **Three ways to browse**: Patterns (153) · Tactics (335, eight stages) · The map.
5. **The eight stages** as a single horizontal band of eight segments sized by tactic count, each a link (on a phone: a vertical list of eight rows with the count bar).
6. **Take it with you** and **method** links; updates (`<section id="updates">`, version badge, per CLAUDE.md).

## 5. Patterns (`S/patterns`)

One list of all combos. Server-rendered in full (works without JS); JS adds:
- **Filter**: fit (All / Native to this sector / Adapted — reader words for tier A/B, with a one-line explanation), family (10), setting (see below), "has a safety note" (41), number of tactics.
- **Sort**: A–Z, family, most tactics, the ten first.
- **Type-to-narrow** on name + definition.
- A live count ("47 of 153 patterns"), announced politely to screen readers (`aria-live="polite"`). Filter state is mirrored in the URL query so a filtered view can be shared; nothing is stored.

Each row/card: name, family, first sentence of the definition, the tactic chain as small stage-coloured dots (with the count as text), a safety mark where one exists.

**Settings** are a small, sector-specific vocabulary derived from the author's `tags` by explicit keyword rules in `content/fractal/<sector>/nav.json` (derived config, deterministic, reviewable). For ENT, about twelve: Signing & contracts · Money, royalties & accounting · Touring & crew · Festivals & venues · Management & labels · Credit & authorship · Reputation & online · Complaints, NDAs & retaliation · Young performers & families · Health, body & safety · Group & belonging · Fans & volunteers. A combo may carry several. Combos that match no rule are listed in the build log; the page still shows them under "All".

## 6. A combo page (`S/<combo-slug>`)

One document, three **reading modes** over the same words (no text is duplicated, so the author word count still matches exactly):

| Mode | Shows | For |
|---|---|---|
| **Quick read** (`#quick`) | Safety note, What it is, The tactics in order, Spot it, What breaks the chain, When to get help, Words you could use | Someone with two minutes |
| **The sequence** (`#sequence`) | The tactics in order as a stepper: one link of the chain in focus at a time, with its "functions by / concern rises when" lines, then "Why this order" | Seeing how the order works |
| **Full pattern** (default) | Everything, in the author's order | Reading it properly |

- A segmented control under the header switches modes (buttons with `aria-pressed`); the mode is reflected in the URL hash so "send the two-minute version" is a link. With no JS, the full pattern shows.
- **Safety note first**, always, in every mode (verify enforces).
- Header: family (link), name, "in the music and entertainment industry", the chain (each tactic a link to its tactic page, stage-coloured dot + stage number as text), reading time for quick and full.
- **Credibility banner** shows the resolved state from the tag-resolution ledger (see `TAG-POLICY.md`), not the raw tag.
- **The sequence stepper**: Previous / Next buttons, the chain drawn as linked nodes, position announced ("Step 3 of 6"); a "Play" button auto-advances (user-started only; pauses on any input; absent under reduced motion). Under reduced motion or no JS it is the ordinary numbered list.
- After the text: **the tactics in it** (ordered, linked); **this pattern in other sectors** (from `content/fractal/_crosslinks.json`, keyed by `combo_id`; hidden while only one sector exists); **patterns that share its tactics** (top 6 by shared tactic count, computed); **more in this family**; what the labels mean.
- Prev/next within the family.

## 7. A tactic page (`S/tactic/<slug>`)

Answers four questions, in order:
1. **What it is**: stage (number + name, linked), name, definition, "also called".
2. **What it looks like at each level**: Individual / Institutional / Civilizational (the author's three examples).
3. **Which patterns use it**: every combo containing it, with its position ("step 2 of 6 in The Debt Prison"). If none: "Not part of a mapped pattern in this sector yet."
4. **Where else to read about it**: its **Pattern Decoder** entry (resolved by standard id through `content/decoder-v20/`; link only if the page file exists in `instruments/playbook/site/`); **The Fractal**: the sector chapter (`/fractal/<chapter>` from `sectors.json`), and for the stage, the divine inversion (`/fractal/the-spiritual-lens#stage-…`) and what existed before (`/fractal/the-frequency#stage-…`), each only if that anchor exists in the published file; **this tactic in other sectors** (by standard id; hidden while one sector exists).
- Prev/next within the stage; link back to the stage chapter anchor.

Stage chapters (`S/stage-<slug>`) keep the full entries (definition + three levels), each headed by a link to its tactic page.

## 8. "What are you noticing?" (`S/notice`)

Purpose: recognition, never diagnosis. Private by construction: runs in the page, stores nothing, sends nothing; the page says so in one line.

- Data: every combo's **Observable Indicators** (bullets) and **Recognition Cue Card** titles and questions, extracted at build time.
- Step 1: pick an area (the Settings vocabulary) and/or type a word ("statement", "password", "everyone says it's standard").
- Step 2: matching indicators appear as a list of checkboxes, each in the author's exact words. Tick what fits.
- Step 3: "Patterns that share what you ticked": ranked by number of ticked signs they contain, shown as "3 of your 5 signs appear in The Debt Prison", each with `2-minute read` and `full pattern`.
- Fixed copy above results: "These are places to start reading. A match is not proof of anything, and it says nothing about anyone's intent. Each pattern has a 'Before you read too much into it' section; read that too."
- Safety line and a link to `in-it-now` stay visible.
- No scores, no streaks, no "result" language, nothing shareable about the reader.
- Without JS: the page lists the Settings as links into `patterns?setting=…`.

## 9. Reader paths

Generated views over existing data; the only new words are short interface lines (kept in `design/fractal-sector/strings.json`, flagged for owner review).

- **`in-it-now`**: the safety line, large; the sector's escalation tiers (from the standards); "what tends to come next" (the eight stages as a strip; pick the one that sounds like now, and see the next stage's description and the patterns that live there); the "Words you could use" and "When to get help" sections of the ten most likely patterns (linked, not copied); Leave button explained.
- **`worried-about-someone`**: what you can see from outside (Observable Indicators of the 41 safety-noted patterns and the ten, grouped by Setting, linked to source patterns); the standards' "ordinary explanations to rule out"; young-performer patterns surfaced first when the Setting applies; child-protection line.
- **`before-you-sign`**: combos in Signing & contracts and Money, royalties & accounting, ordered by the top ten first; for each: the two Spot-it tests and one "Words you could use" line (linked to the pattern), plus the standards' "what to keep".

## 10. The living map (`S/map`)

- **What it shows**: all tactics on a ring, grouped into eight stage arcs sized by count; all combos as points inside, grouped by family. Select a combo: its tactics light up and are joined **in order**, numbered, so the path of the sequence through the stages is visible. Select a tactic: every combo that uses it lights up. A side panel (below the map on a phone) names the selection and links to its page.
- **How sequences recur**: two short computed tables under the map (also the text equivalent): "Tactics that appear in the most patterns" (top 15) and "Pairs that most often follow each other" (ordered pairs appearing in 2+ patterns).
- **Controls**: pointer/tap; full keyboard path (a searchable select of combos and of tactics drives the same selection; arrow keys step along a selected sequence); `aria-live` summary of the selection. Canvas or SVG, generator's choice; 60 fps on a mid-range phone; under reduced motion selections change without animation.
- **Phone**: the ring fits 343px with dots only; all text lives in the panel below; no horizontal scroll.
- Data from `BASE/_a/d/<sector>-map.json`, or inline for this one page.

## 11. Method (`S/method`) and Take it with you

- **Method**: what this is and is not; how the tactics and patterns were written; the fit tiers; what each label means and the current resolution numbers (from the ledger); the six sector standards (author's text, with `id="standards"` anchors); how to cite; licence; contact for corrections.
- **Take it with you**: files listed in `content/fractal/<sector>/downloads.json` (title, file, size, note). Each PDF is listed only if the file exists; a cover note states that printed copies carry the same labels as the site and gives the date. A print stylesheet makes every combo page print cleanly as a hand-out (quick-read sections on page one).

## 12. Cross-sector readiness

- Every combo record carries `combo_id`; every tactic `standard_id`. `content/fractal/_crosslinks.json` and the search index are keyed by them.
- `content/fractal2/sectors.json` is the registry: `[{n, id, slug, title, relationship, fractal_chapter, built}]` for all thirty. The switcher, the intro's atlas and "in other sectors" read it.
- Adding a sector = drop the package in `content/fractal/<id>/source/`, add `nav.json`, set `built: true`, run `design/fractal-sector/run.sh <id>`.

## 13. Stage 6

The Fractal calls stage 6 **Extract**; the expanded tactic book calls it **Control**. They are one stage. The site shows it as **Extract · Control** wherever a stage name is displayed, keeps the slug `stage-control` (with `stage-extract` redirecting to it), and the stage chapter carries one line: "The Fractal calls this stage Extract. The expanded map calls it Control: the rules, money and information that do the extracting." (Interface line; owner to confirm.)

## 14. Acceptance (see `RUBRICS.md` → Navigation)

Each of the seven readers can reach what they need in two taps from the sector home; every page stands alone; every view works with keyboard and screen reader; no horizontal overflow at 375px; every link is resolved from an id or an existing file, never guessed.
