# Cover-art pipeline

How the 2026-09 books' cover art was built, so it can be rebuilt or redone
for future books without re-deriving the process.

## Inputs (not committed -- put them in `_work/`)

- `_work/<slug>.png` -- the raw generated source art (Artlist,
  `aspect_ratio: "21:9"`, matches the `viewBox="0 0 640 280"` cover-mark
  slot). One per book.
- `design/brand/logo-noble-father.png` (committed) -- the watermark, already
  trimmed to its content bounding box.

`_work/` is gitignored: multi-megabyte source renders and intermediate
JPEGs don't belong in history. The only permanent output is what these
scripts embed directly into the book and hub HTML files, which *are*
committed.

## Pipeline

1. `compose-banners.py` -- crops each `_work/<slug>.png` to the 640:280
   cover-mark ratio, adds the "SHAE STOVELL" credit and the logo watermark,
   writes `_work/<slug>-final.jpg` + `.b64`.
2. `embed-banners.py` -- swaps the base64 payload inside each book's
   `<img class="cover-mark">` tag for the new `.b64` file. Byte-for-byte
   swap of the `src` attribute only; nothing else on the page changes.
3. `compose-jackets.py` -- builds the portrait (1:1.42) jacket used on the
   hub's Library shelf from the *same* `_work/<slug>.png` source (a
   different crop/layout, not a resize of the banner -- the banner's crop
   would lose the credit and watermark at that aspect ratio). Writes
   `_work/<slug>-jacket.jpg` + `.b64`.
4. `embed-hub-jackets.py` -- same swap as step 2, but into
   `hub/catalogue-redesign.html`'s shelf cards, matched by each card's
   `alt` text.

Run in that order. Each script asserts before writing (exactly one match
for the thing it's replacing) rather than silently no-op'ing on a mismatch.

## After running

Redeploy the 5 book Netlify sites and the hub (see `sites.json` for site
IDs), then verify:

- Escape closes the catalogue drawer without triggering the books'
  emergency exit, and still triggers it when the drawer is already closed
  (these books bind Escape to a page-blanking exit -- see
  `scripts/nf-install-chrome.py`).
- The deployed page is byte-identical to the repo copy (`curl` it and
  `wc -c`, compare to the local file size).
