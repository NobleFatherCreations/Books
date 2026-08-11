# /design — the book design system

Self-contained building blocks for the premium-design pass, built from
`tools/edwardtufte-tufte-css/`, `tools/fonts/newsreader/`, and native
browser APIs only. Nothing here makes a network request when shipped.

- **`snippets.html`** — paste-in bundle: self-hosted `@font-face` (Newsreader,
  base64-embedded, ~1.2MB), an 8px spacing scale, dark+gold+crimson palette
  tokens, a reading-progress bar, and scroll fade-ins (native
  `IntersectionObserver`, no library). Drop the whole file's contents into
  any chapter page — style block anywhere in `<head>`, the `<div id="nfc-progress">`
  and `<script>` near `</body>`.
- **`build-snippets.py`** — regenerates `snippets.html` from the vendored
  font. Run it if the font or the embedded CSS/JS changes; don't hand-edit
  the generated file.
- **`build-chapter-index.py <slug>`** — generates a self-contained
  chapter-index page for one book from `chapters.json` + `sites.json` (THE
  HOUSE nav is inlined with real URLs, not fetched). Data is baked in at
  generation time — the shipped page never fetches JSON. Example output:
  `chapter-index-fracture.html`, built from the one book with real chapter
  data filled in so far.

## Why generation, not runtime fetch

The books' rule is zero external requests, and `chapters.json` living
same-origin doesn't get around that cleanly (a page opened via
`file://double-click`, which the review package explicitly calls out as the
expected review method, can't `fetch()` a sibling JSON file — CORS blocks
it). So `chapters.json` stays the *authoring* source of truth, and these
scripts bake its data into a fully self-contained HTML file at generation
time. Same discipline as the rest of the site: one file, opens anywhere, no
requests.

## Not yet done

- Only `fracture` has real chapter data (blurb/readMin/slug are still null
  for chapters 14–20, and every other book is empty) — see `chapters.json`
  → `todo`. Re-run `build-chapter-index.py` per book once that's filled in.
- These snippets haven't been pasted into any live/shipped page yet —
  that's a per-page editing pass, not done automatically here, since each
  existing page has its own hand-authored structure to slot them into.
