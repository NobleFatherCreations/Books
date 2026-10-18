# The Sacred Divide — one file per religion, and its PDF

Every religion has one Markdown file here, on one fixed 27-section skeleton. That file is the single
input for the religion's downloadable PDF, and later for its page on the redesigned site. **These
files are generated — never edit them by hand.** Edit the inputs, then rebuild.

## Rebuild

```sh
python3 scripts/sacred-divide-factcheck.py library/_undeployed/sacred-divide-v4-candidate.html \
        library/_undeployed/sacred-divide-v4-factchecked.html        # 1. book data with all corrections
python3 scripts/sacred-divide-export-md.py                           # 2. religions/<id>.md + _coverage.md
python3 scripts/sacred-divide-pdf.py sunni-islam                     # 3. one PDF  (or --all: 34 in ~2 min)
python3 scripts/sacred-divide-pdf.py sunni-islam --html              #    stop at the paged HTML (design work)
```

Requirements: `pip install markdown pypdf` (plus `pillow pypdfium2` only to preview pages as images).
Playwright + Chromium are preinstalled in this environment. Paged.js and every font are vendored in
`tools/pdf/`, so a build needs no network.

## Where content comes from

| Input | What it holds | Edit it when |
|---|---|---|
| The fact-checked book (`library/_undeployed/sacred-divide-v4-factchecked.html`) | The 27 existing religions' profiles, the 30 techniques and their grades, apex chains, turning points, phrasebook, regional cards, cases, scorecard | Via `scripts/sacred-divide-factcheck.py` only, with the finding recorded on the source page first |
| `../new-traditions/<id>.md` | The 7 new religions' full records | Directly |
| `../additions/<id>.md` | New sections the book never had: `branches`, `law`, `moneyNumbers`, `cases`, `voices`, `regional`, `leaving`, `help`, `whoHurt`, `changed` | Directly — this is where the fill work goes |
| `../sources/<id>.md` | The numbered Sources list (becomes section 26) and the claim register (per-section citations) | When a source is added — keep numbering stable |

## The skeleton (same for every religion, in this order)

1 At a glance · 2 A day inside · 3 The forefront · 4 What healthy looks like here · 5 History ·
6 Branches & variants · 7 Structure · 8 Law & state here · 9 Money · 10 Genealogy · 11 Reach ·
12 The 30 techniques · 13 The loops · 14 Say versus do · 15 Cost & cover · 16 The ledger ·
17 Who gets hurt most · 18 The middle tiers · 19 Documented cases · 20 Precedent ·
21 Voices from inside · 22 Regional variants · 23 The questions · 24 Leaving safely here ·
25 Where to get help · 26 Sources · 27 What changed on this page

An empty section still prints, with a gap notice, and a thin one prints with a "partly documented"
notice. Nothing is silently skipped. `_coverage.md` is the fill list.

## Markdown conventions the renderer understands

- `## N. Title {#slug}` for a section; `### Title` for a subsection; `#### n · Name {#t-n}` for a technique.
- `::: kind` … `:::` for a styled box. The kinds are `glance`, `lede`, `tell`, `question`, `gap`,
  `cites`, `card`, `case`, `stage` and `tactic`.
- ```` ```timeline ```` rows are `date | event | reading`. They draw as an era strip and a numbered timeline.
- ```` ```chart ```` takes JSON: `{"type": "bar"|"line", "title", "unit", "series": [[label, value]…], "note", "cite": [n…]}`.
- `[[Codified]]` and the other grade names become colored evidence chips.
- `[n]` becomes a link to Sources item *n*.
- `[OFFICIAL POLICY: …]` becomes a receipt label.
- In a case, `- **tactics:** 17, 14` becomes linked technique names.

## The PDF

Each PDF has:
- a cover;
- a contents page with real page numbers, where every entry is a link;
- a "How to read this" page;
- the 27 sections, each starting on a new page, with running heads and page numbers;
- charts, a timeline, and an index of all 30 techniques;
- clickable citations and technique links, and live source URLs;
- a full bookmark tree: sections › subsections › techniques.

Design lives in `tools/pdf/sacred-divide.css`. It uses the site's own parchment, curtain and gilt
colors and its Codex Display and Codex Caps fonts, over Newsreader. Change the look there once, and
every religion follows.

Output goes to `library/_undeployed/sacred-divide-pdf/<id>.pdf`, plus `manifest.json`. Only the
Sunni Islam example is committed; the rest are build output.

## The Download button (for the site rebuild)

The site reads `manifest.json`. Each entry holds `title`, `family`, `file`, `pages`, `bytes`,
`version`, `checked` and `sections_filled`.

- **Placement:** the button sits at the top of each religion page and uses the site's own button
  style.
- **Label:** "Download the full record (PDF · 59 pages · 2.6 MB · checked 27 Sep 2026)".
- **Deploy:** the PDFs deploy beside the page at `/faith/pdf/<id>.pdf`, as plain files. That means
  no scripts and no tracking, in keeping with the book's own rule.
- **When to rebuild:** rebuild the PDFs every time the page content changes. The version and
  checked date on the cover and in the manifest come from the same Markdown front matter, so the
  page and the PDF cannot disagree.
