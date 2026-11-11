# Noble Father Creations: brand kit v1 (the character holds the Fractal)

**The mark.** The hatted character from the Noble Father Creations header, holding a gold wax seal that is stamped with **the original Fractal** (8 stages, 30 techniques). It joins the maker (the wax-seal and NFC craft) to the work (the Fractal). The original header, character, wax rim and circuit glow are untouched; only the seal's medallion changed (the NFC chip became the Fractal dial). Regenerate or adjust with `python3 brand/make_brand.py`; originals are in `brand/source/`.

## Files (`brand/out/`)
| File | Size | Use |
|---|---|---|
| `header-primary-2000.jpg` (and `fractal-seal-30-3000.jpg`, `fractal-seal-30-full.png` at 5504×3072) | 16:9 | Main banner: site home, press kit, channel art, Shopify/Workshop header |
| `og-card-1200x630.jpg` | 1200×630 | Social share card (Open Graph/Twitter) for every project |
| `avatar-character-seal-1080.jpg` | 1080² | Profile picture, podcast/video avatar, sticker |
| `emblem-512/256/192/128/64/32.png`, `favicon.ico` | circle, transparent | Favicon, site header mark (30 px), app icon, wax-seal product mark. Clean ring version: legible at small sizes |
| `dial-30-900.png` | circle, transparent | The labelled dial for large uses: intro, covers, merch, wax seal engraving |
| `fractal-seal-clean-*` | 16:9 | Alternate header using the clean ring emblem in the seal |

## Where it shows up (wire these in; nothing here is deployed yet)
1. **Favicon + header mark on every site** (hub, books, Decoder, Listening Room, Workshop, Fractal²): `favicon.ico`, `emblem-64.png` beside the project name (already used in the zoom prototype).
2. **Social card:** `og-card-1200x630.jpg` as the default `og:image`/`twitter:image` (books keep their own card where they have one; the hub, Workshop and Fractal² use this).
3. **Home page hero (hub):** `header-primary-2000.jpg`, with the zoom prototype's "dial" as the intro's centrepiece.
4. **Fractal² intro:** the original dial is the stage; the emblem is the header mark.
5. **THE HOUSE nav tab:** the emblem as the tab icon.
6. **Workshop (NFC wax seals):** the dial as the seal engraving and the product photography reference.
7. **Channel art and avatars** (YouTube, Instagram, TikTok, Spotify): header and avatar files.
8. **Book colophons:** the emblem small, beside the author line; never on the cover art itself.

## Rules
- Keep the character and wordmark proportions; do not recolour, crop the hat, or add effects over the seal.
- Clear space around the emblem: at least half its diameter. Minimum sizes: header 600 px wide; emblem 24 px.
- The emblem (clean ring) for anything under 128 px; the labelled dial only at 400 px or larger.
- On light grounds, place the emblem on a dark circle or the dark artwork; the artwork is designed for dark grounds.
- Not for the children's book, which keeps its own look (owner rule); safety books use the emblem only in the colophon (discreet mode: omit).

## Palette used with the mark (from the intro build)
Ground navy `#0A0F1E` · cream `#EFE6D2` · gold `#E9B949` / light gold `#F4D58A` (matches the header lettering when sampled) · stage colours stay inside Fractal figures only.

## Open items
- A fully re-rendered, single-pass illustration of the character holding the Fractal (instead of a composite) can be generated with the connected image tools; it costs credits and risks changing the wordmark, so the composite is the safe master.
- A transparent-background cut-out of the character (for overlays on pages) needs a masking pass.
- Confirm the palette and usage rules, and whether the Fractal seal should replace the NFC chip on the Workshop product pages.
