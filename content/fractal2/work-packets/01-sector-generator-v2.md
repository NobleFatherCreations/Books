# Work packet 01 — Sector site generator v2 (structure, frame, core pages)

**For:** an implementation model starting cold. **Owner of the spec:** the directing session. **Repo:** `/home/user/Books`. Do not commit or push; leave changes in the working tree and report.

## Goal

Rebuild the Fractal sector-site generator so it produces the Entertainment & Music site at `/fractal2/entertainment` with the navigation in `content/fractal2/NAV-SPEC.md` (sections 2–7, 11–13) and the shared "Deep field" design in `design/fractal2/tokens.css`. Sections 8–10 of the nav spec (`notice`, the three reader paths, `map`) are **packet 02**: in this packet create those five addresses as real, useful static pages (described under "Stubs" below) so no link is ever dead.

Everything must come out of the generator, driven by data, so a second sector builds by running one command.

## Read first (in this order)

1. `content/fractal2/NAV-SPEC.md` (the design you are implementing)
2. `design/fractal-sector/README.md`, `build.py`, `ingest.py`, `verify.mjs`, `site.js`, `style.css`, `run.sh`, `og.mjs` (the current generator)
3. `design/fractal2/tokens.css` (tokens and base; you build the component CSS on top of it), `design/fractal2/serve.py` (local preview), `design/fractal2/fonts/` (the two typefaces, already subset)
4. `content/fractal2/sectors.json` (registry of the thirty sectors)
5. `content/fractal/ent/build/sector.json` (the data; produced by `ingest.py`), `content/fractal/ent/source/ENT_top10.json`
6. `content/decoder-v20/standard_index.json`, `alias_map.json`, `playbook_patterns.json`, and the file names in `instruments/playbook/site/` (Decoder pages; a tactic's page is `/playbook/<slug>` when `<slug>.html` exists there)
7. `CLAUDE.md` (house rules), especially "Self-contained architecture" and "Patch notes & versioning"

## Hard rules

- **Never edit** anything under `content/fractal/*/source/`, `content/fractal2/owner-source/`, `library/fractal/` (published book and the old prototype output in `library/fractal/sectors/ent/` are frozen), `hub/`, `instruments/`.
- **No deploys.** No network calls from pages. No CDN, no external script, no framework, no storage (no cookies, localStorage, sessionStorage, IndexedDB). The only third-party tag is the existing Cloudflare beacon include.
- Every link absolute. Every link to a tactic, combo, Decoder page or Fractal page is resolved from an id or a file that exists. If it cannot be resolved it renders as plain text and is listed in the audit. No fuzzy matching.
- **Author words are untouched.** The exact word-count round trip (words inside `data-src` on a combo page == `reader_words` from ingest) must still hold for all 153 combos. Reading modes may hide and show sections; they may not duplicate or drop author text.
- **Safety note first** on every combo that has one, in every reading mode. Escalation Triggers and Safer Response Language are never dropped.
- No internal ids (`C018`, `T001`) or production cues visible to readers or in URLs.
- The existing 16 checks in `verify.mjs` stay (adapted to the new paths). You may add checks; you may not weaken or delete one. If a check has to change meaning, say so in your report.
- Accessibility: WCAG 2.2 AA. Keyboard path for every control. Visible focus. `prefers-reduced-motion` respected. No horizontal overflow at 375px. Nothing left at `opacity:0` if JS fails (reveal classes are added by JS only after it has run).
- Keep THE HOUSE drawer and the beacon includes exactly as the current `frame()` does.
- Build-time tools are fine (Python 3 stdlib, Node, Playwright already installed at `/opt/pw-browsers/chromium`; never run `playwright install`). `npm i --no-save axe-core` once if `axe-core` is missing.

## What to build

### A. Configuration and layout

- Base path from `content/fractal2/sectors.json` → `base` (`/fractal2`), overridable with `--base`. Nothing hard-coded. The site title string "Fractal²" and the origin come from one config block.
- Output: `library/fractal2/site/` is the publish directory shared with the intro.
  - Sector pages: `library/fractal2/site/fractal2/entertainment.html` and `library/fractal2/site/fractal2/entertainment/**`.
  - Shared: `library/fractal2/site/fractal2/_a/f/` (copy of `design/fractal2/fonts/*.woff2` + licences), `library/fractal2/site/fractal2/_a/d/ent-search.json`.
  - **Never delete the whole site directory.** The intro (`site/fractal2.html`, `site/fractal2/_a/au/`, other files) is built by another program. Clean only what this generator owns for the sector being built.
  - Manifest: `library/fractal2/manifests/ent.json` (same content as today's `manifest.json`, plus the new page groups).
  - Old-prototype redirects: write `library/fractal2/redirects/old-prototype._redirects` (for the old `fractal-entertainment` Netlify site: every old path → `https://noblefathercreations.com/fractal2/entertainment/...` 301) and `library/fractal2/redirects/HUB-RULES.txt` (the lines the hub would need). Do not touch `hub/`.
- `design/fractal-sector/run.sh ent` still does import → build → social cards → verify.
- Split `build.py` into small modules if that makes it clearer (for example `frame.py`, `pages_*.py`, `links.py`), but keep the single entry point.

### B. Derived data (in `ingest.py` or a new `derive.py`; all outputs in `content/fractal/ent/build/`)

- `links.json`: for each tactic (by `standard_id`): Decoder URL or null (resolve the tactic name through `standard_index.json`/`alias_map.json` to the Decoder page slug; a link exists only if `instruments/playbook/site/<slug>.html` exists). For each **unresolved tactic name used in a combo** (the 131 in `content/fractal/ent/build/audit.md`): resolve through `alias_map.json` (lower-cased key → standard id → that sector tactic) and through `playbook_patterns.json` (pattern pages such as Gaslighting, DARVO, FOG, Trauma Bonding live at `/playbook/<slug>`). Report how many of the 131 now link, and list the rest in `audit.md`. Exact, id-based only.
- Fractal links: sector chapter from `sectors.json` (`fractal_chapter`); per stage, the anchors `the-spiritual-lens#stage-<stage>-divine-principle-…` and `the-frequency#stage-<stage>-what-existed-before-…` found by reading the ids in `library/fractal/the-spiritual-lens.html` and `the-frequency.html` (stage 6 is `extract` there). Link only anchors that exist.
- `nav.json` → **input** config at `content/fractal/ent/nav.json`: the Settings vocabulary (NAV-SPEC §5) as explicit keyword rules over the author's `tags`. Draft it for ENT (about twelve settings); log coverage (combos per setting, combos with none).
- Per combo: position of each tactic; "patterns that share its tactics" (top 6 by shared count, ties by name); quick-read and full reading time (words/220, rounded up).
- Search index `ent-search.json`: `[{t:"p"|"t", n:name, u:url, s:stage or family, d:first sentence, a:[also called]}]`.
- Stage 6 display name "Extract · Control" (NAV-SPEC §13) via a display map; data keys stay `CONTROL`.
- C144: `audit.md` already warns that the author's index undercounts two tags for C144. Keep the warning, and make sure the page uses the counts from the script file (it does today); add one line to `audit.md` saying so.

### C. Pages (NAV-SPEC sections 3–7, 11)

Frame (top bar with mark, sector switcher, search, Leave; breadcrumbs; footer), sector home, `start`, `patterns` (filter/sort/narrow with URL query state), `tactics`, eight stage chapters, ten family pages, 153 combo pages with three reading modes and the sequence stepper, 335 tactic pages, `method` (includes the six standards with `id="standards"`), `take-it-with-you` (reads `content/fractal/ent/downloads.json` if present; today there are no PDF files in the repo, so the page explains printing and says the PDF editions are being prepared; plus a print stylesheet for combo pages), `a-z`, `sitemap.xml`, social cards.

**Stubs for packet 02** (`notice`, `in-it-now`, `worried-about-someone`, `before-you-sign`, `map`): build each as a complete static page now, using only existing data and no new claims:
- `notice`: the Settings as links into `patterns?setting=…`, plus the safety line.
- `in-it-now`: the safety line (large), the sector's "Escalation Tiers For This Sector" standard, the eight stages as a strip linking to stage chapters, links to the top ten at `#quick`.
- `worried-about-someone`: the standards' "Universal Benign Explanations" and "Concern Strengthens When", links to the 41 safety-noted patterns grouped by family.
- `before-you-sign`: patterns in the Signing and Money settings, top ten first, each linking to `#quick`; the standards' "Universal Evidence To Preserve".
- `map`: the two computed tables (tactics in the most patterns; ordered pairs appearing in 2+ patterns) with links. The interactive graph comes in packet 02; leave a clearly marked mount point `<div id="map-stage"></div>` above the tables.

### D. Interface strings

All interface words that are not the author's go in `design/fractal-sector/strings.json` (keyed, with a `"_review": "owner"` note). Plain language. No em dashes. Never claim anything about a real person or company. Keep the existing footer safety paragraph verbatim.

### E. Look and feel

Use `design/fractal2/tokens.css` as the base (prepend it; replace `/F/` with the absolute font directory `/fractal2/_a/f/`). Write the component CSS in `design/fractal-sector/sector.css`. Direction:

- Dark first, with the light theme from the tokens' `prefers-color-scheme` block. Check contrast in both.
- Newsreader (serif) for all author prose and headings; Hanken Grotesk (sans) for interface, labels, numbers. No third typeface. Kickers: small caps style in the sans (`.kicker`).
- One accent: gold. Gold means "you can act on this" (links, the active control, the way-out sections: What breaks the chain, Words you could use). Stage colours (`--s1`…`--s8`) appear only as small marks (8px dots, a 2px rule) and always next to the stage number or name as text.
- Surfaces: hairline borders (`--line`), `--bg-1` fills, radius 10px. No drop shadows, no gradients as decoration. Generous whitespace on the 8px grid. Reading measure about 62–68 characters (`--measure`).
- Numbered cards for the ten, the stages and the families (two-digit numerals in the sans, tabular).
- Motion: 0.2–0.32s, `--ease`; hover lifts of 2px at most; a reading-progress bar on combo pages; all of it off under reduced motion. Nothing animates that is not caused by the reader.
- Safety note: `--warn` 3px left rule, `--warn-wash` fill, an inline SVG alert icon, the heading "Read this first".
- Credibility labels: small outlined chips in the sans; keep the current label names and explanations for now (packet 04 changes them to the resolved states); keep the "what the labels mean" section.
- Phone (375px) is designed in its own right: the top bar stays one row (mark, switcher as an icon+short label, search icon, Leave); filters on `patterns` open in a sheet (a `<dialog>` or a disclosure), the mode control on combo pages is a full-width three-part segmented control that sticks under the top bar; touch targets at least 44px.
- Print: combo pages print black on white, quick-read sections first, URLs of links omitted, the safety line included.

### F. Versioning

On the sector home: `<section id="updates">` with badge `v2 — <today>` and two entries (v2: "Moved to Fractal² with new ways in: start by where you are, filter all 153 patterns, read any pattern in two minutes, and a page for every tactic."; v1 kept). Do **not** edit `sites.json` (the directing session does that).

## Verify (extend `design/fractal-sector/verify.mjs`)

Keep the 16. Add at least:
1. every reserved address in NAV-SPEC §2 exists; no combo slug collides with one;
2. 335 tactic pages exist and each shows three levels;
3. every `/playbook/...` and `/fractal/...` href on any page points at a file (and anchor, when present) that exists in this repo;
4. combo pages: with JS on, switching to Quick read hides the scene and keeps the safety note first; `#quick` and `#sequence` deep links select the mode; with JS off the full text is visible;
5. `patterns`: applying a filter changes the visible count and the URL query; loading that URL restores it;
6. search dialog opens, returns a result for "debt", is keyboard operable, closes on Escape and returns focus;
7. no `localStorage`/`sessionStorage`/`document.cookie`/`indexedDB`/`fetch(` to another origin in any shipped script (static scan);
8. axe: zero serious or critical violations on the sampled pages in dark and light;
9. no horizontal overflow at 375px on every page type; nothing with computed `opacity:0` after load on the sampled pages (excluding elements that are `hidden`/`aria-hidden` by design).

## Done when

- `design/fractal-sector/run.sh ent` exits 0 with every check passing; paste the full check list in your report.
- `python3 design/fractal2/serve.py 8802` then `http://127.0.0.1:8802/fractal2/entertainment` works end to end.
- Screenshots saved to `library/fractal2/review/packet01/` at 390×844 and 1440×900, dark and light, for: home, start, patterns (with a filter applied), a stage chapter, a family page, The Debt Prison in each of the three modes, a tactic page (Love Bombing), method, take-it-with-you, the search dialog open, the sector switcher open. Look at them yourself before reporting and fix what looks wrong.
- Report (final message): what you built, file list, the check output, the count of the 131 unresolved names that now link, the Settings coverage table, anything you could not do, and any place you had to interpret the spec.

## Escalate (stop and report instead of guessing) if

- a rule in "Hard rules" conflicts with the spec;
- the word-count round trip cannot hold with the reading modes as specified;
- more than 10 combos match no Setting, or a Setting would need a keyword that is really a judgment about a person;
- a Decoder or Fractal link can only be made by fuzzy matching;
- anything would require editing a frozen file or deploying.
