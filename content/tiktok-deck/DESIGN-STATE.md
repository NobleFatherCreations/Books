# TikTok book deck: design state

**State (2026-11-20, v4):** 110 slides plus three owner videos, about 21 minutes in total, 1080×1920, built by `python3 content/tiktok-deck/build.py`. The output goes to `out/` (full video plus 16 per-book MP4s; git-ignored).

## Concept
A gold-on-black "field guide poster". Every slide shows the brand (a round logo badge and the wordmark), one large serif headline with a gold italic turn, one proof block, and the site link set large as a signed footer.

## Budget (design-director, 07 section 2)
- **Lead style:** editorial luxury, in the manner of Stripe Press.
- **Signature move:** an "in miniature" proof card that shows a real entry from the book.
- **Type:** Instrument Serif for headlines, Hanken Grotesk for body text.
- **Accent:** gold (#e0b55e and #f4d58a).
- **Effects:** a blurred glow from each book's cover, plus a hairline frame. No motion.

## Slide types
Each book runs:
1. Cover, with the brand bar above it.
2. Hook card: cover thumbnail, title, subtitle and the stat numbers.
3. Four or five highlight slides. Each section has a label, a headline, and one block, which is prose, bullets, items, the SOVEREIGN acrostic, a proof card, or big stats.

The intro has four cards and the outro has one. The outro carries Cash App $shaestovell and Venmo @noblefather.

## Owner rules for this deck
- Logo on every slide.
- A big website link.
- No slide counters.
- Covers at book size (2:3).
- Marketing tone with no AI slop.
- 5–7 slides per book (The Fractal may have more).
- Show a real example wherever one exists.
- Cover the audience and what makes each book unique.

## Checks
`render.mjs` fails a slide if the body or the safe area overflows (more than 1 px or 4 px respectively) or if an image is broken. It logs a fill percentage for each slide in `build/manifest.json`. A fill under about 60% means there is room for another highlight.

**Safe area:** text is kept within x 72–912 and y 150–1440.

## Critic round 1
Scores: hierarchy 3, brand 3, distinctiveness 2, consistency 4, copy 3, safe zone 4.

Applied:
- Replaced the contrast-style and triad headlines.
- Relabelled the Fracture stats.
- Added the brand bar to the cover slides.
- Raised the size of small labels and the link (68 px).
- Made the cover-colour glow stronger.

Not applied:
- **Per-book accent colours:** they would break the gold brand identity.
- **Cutting The Fractal to 7 slides:** the owner allowed it more.

## Open
- The covers taken from the PDF are about 600 px wide and slightly soft. Swap in originals if the owner has them.
- A second critic round has not been run.

## v4: owner assets (assets/)
- `banner.jpg`: the Noble Father Creations banner. It is the header on every slide, blended with `mix-blend-mode: lighten` so its black background disappears.
- `signature-gold.png`: the owner's signature recoloured gold on a transparent background. It appears wherever the name is shown: intro card 1, the About the Author slide, and the end.
- `author-face.jpg`: the "manipulation face" word-art portrait, used on the About the Author slide (after the intro). The bio is the owner's own words from the catalogue PDF.
- `hippy-angel.png`: cut out from `hippy-angel-source.jpg` by flood-filling the background from the image edges. It is an accent on The Festie Codex hook card and its "What it is" slide.
- `angel-6s.mov`: opens the video (upscaled from 480×854; its own audio is kept).
- `end-12s.mp4`: plays after the outro card (its own audio is kept).
- `signature-draw.mp4`: played at 3× speed (about 5 s). The white paper is removed (negated luma used as alpha) and the ink is drawn in gold over the end card, which holds for 2.5 s.
