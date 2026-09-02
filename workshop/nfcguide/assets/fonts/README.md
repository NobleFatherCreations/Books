# Typefaces

All three families are **SIL Open Font License 1.1**, which explicitly permits
embedding. The full licence texts sit alongside this file and **must stay with the
fonts** — that is a condition of the licence.

| Family | Weight | Role |
|---|---|---|
| **Fraunces** | 700 / 900 | The wordmark and every heading. The Noble Father display face — the same one the hub, all fourteen books and both craft sites use. |
| **Hanken Grotesk** | 400 / 600 / 700 | All body copy, UI chrome and labels. |
| **Space Mono** | 400 | Section letters, counts, and the catalogue rows in the House drawer. |

This page originally shipped with Playfair Display and Poppins. They were replaced
on 2026-09-02 so the guide reads as the same studio as everything else it links to;
their licences and reference files were removed in the same pass, because shipping
the licence for a font you no longer embed is noise, and shipping a font whose
licence you dropped is a violation.

## Why they are inlined rather than linked

The families the site actually uses are subset to the glyphs in `charset.txt` and
base64-inlined into `index.html` — 65KB of font data in total.

That is deliberate: browsers block same-origin font *files* loaded over `file://`, so
an external `.woff2` would silently fail whenever the page is opened straight from
disk — and offline-from-the-filesystem is a requirement of this site. Data URIs always
work, cost zero network requests, and remove any flash of unstyled text.

No reference `.woff2` copies are kept here any more. They were stale the moment the
inlined payloads changed, and the real sources are already in the repo under
`tools/fonts/` — which is what the cutting script reads.

## Re-cutting after a content change

`charset.txt` holds the exact glyph set the page needs. Adding a recipe with a
character outside it (an accent, a new symbol) means re-cutting. Do it with the
script rather than by hand — it instances the variable axes away, subsets, and
rewrites all six `@font-face` payloads in one pass:

```sh
# from the repo root
python3 scripts/nfcguide-fonts.py
```

If you add a glyph, add it to `charset.txt` first. The script reads that file; it
does not scan the page.
