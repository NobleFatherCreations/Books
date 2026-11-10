# 02 — Foundations: layout, type, colour, imagery, icons, surfaces, density, theming

## L. Layout and structure
- L-01 Single column long-read (50–75 character measure).
- L-02 12-column grid; L-03 modular grid; L-04 baseline grid; L-05 asymmetric Swiss grid; L-06 broken/overlapping grid (intentional collision).
- L-07 Bento / tile mosaic; L-08 masonry; L-09 card grid; L-10 list/table (dense); L-11 split screen (50/50); L-12 sidebar + content; L-13 holy-grail (header, sidebar, content, footer); L-14 full-bleed sections with contained text; L-15 centered hero stack; L-16 poster layout (one big idea per screen); L-17 horizontal-scroll rail; L-18 carousel/deck; L-19 stacked cards (sticky stack); L-20 pinned stage with scrolling captions; L-21 timeline / vertical rail with nodes; L-22 radial / ring layout; L-23 map-as-layout; L-24 canvas / infinite pan-zoom; L-25 dashboard panels; L-26 magazine spread; L-27 sidenotes/marginalia (Tufte); L-28 table of contents rail; L-29 "one thing per page" (GOV.UK); L-30 sheet/drawer over content; L-31 center-stage focus with dimmed context.
- Spacing systems: 4px, 8px, modular scale, fluid `clamp()` spacing; vertical rhythm; optical alignment; safe areas; thumb zones; minimum tap target 44×44 px (Apple) / 48 dp (Material); max line length; gutter and margin tokens; container widths per breakpoint; aspect-ratio tokens.
- Breakpoint strategy: mobile-first; container queries; fluid type; orientation; foldables; large-screen (≥1920) and ultra-wide behaviour; print.
- Whitespace as design: density tiers (airy / comfortable / compact), and where each belongs.

## T. Typography
**Classifications:** humanist sans; neo-grotesque; geometric sans; grotesque (Akzidenz-style); transitional serif; Didone / modern; old-style (Garamond-type); slab; blackletter; script (formal, casual, brush); monospaced; display / decorative; condensed; wide / extended; rounded; pixel / bitmap; variable (weight, width, slant, optical size, grade); colour fonts (COLR/SVG); ornament / dingbats; stencil; inline; handwritten; "ink-trap" grotesques; transitional-sans hybrids.
- T-01 Pairing strategies: serif display + neutral sans text; sans display + serif text; mono accent for labels; single superfamily across weights; contrast through scale not through many families (max two families).
- T-02 Scale systems: modular scale (1.2 minor third → 1.5 perfect fifth), fluid scale (`clamp`), dramatic hero scale (8–20 vw), fixed vs relative.
- T-03 Text treatments: tight display tracking (−2% to −5%), loose caps tracking (+8% to +30%), small caps, old-style numerals, tabular numerals for data, hanging punctuation, drop caps, pull quotes, marginal notes, running heads, footnote systems, end-notes, hyphenation, `text-wrap: balance/pretty`, ragged-right vs justified, optical margin alignment, ligatures, swashes, stylistic sets.
- T-04 Hierarchy tools: size, weight, colour, case, spacing, position, rule lines, numbering, labels, icons.
- T-05 Reading comfort: measure 45–75 characters, line-height 1.4–1.7 for text, ≥16 px base on mobile (prefer 17–19 for long reading), contrast ≥ 4.5:1 body, avoid pure-white-on-black long reading (use off-white, slightly reduce weight in dark mode), avoid light weights for small sizes, respect user font-size settings (rem).
- T-06 Kinetic and expressive type: per-letter/per-word reveal, variable-axis animation, text on a path, type masks over video, scroll-linked weight/width, text scramble/decode, marquee, 3D extruded type, outline/stroke type, text-as-texture. Always keep a static readable fallback and reduced-motion variant.
- T-07 Loading and fallback: self-hosted WOFF2 subsets, `font-display` strategy (swap vs optional), size-adjust fallback metrics to prevent layout shift, preload the primary face, limit to ≤ 4 files.
- T-08 Web-safe system stacks: San Francisco / Segoe UI Variable / Roboto / system-ui; "native feel" stack; serif system stacks (Charter, Iowan Old Style, Georgia).
- T-09 Voice in type: formal / literary / technical / playful / neutral / authoritative; match to content and reader state.
- Foundry and typeface lineages to explore (look up current releases; licences vary): Grilli Type, Klim, Commercial Type, Pangram Pangram, Displaay, Colophon, Dinamo, Sharp Type, Lineto, Production Type, ABC Dinamo, Collletttivo (open licence), Fontshare, Google Fonts (open licence, self-host allowed), Velvetyne (open), The League of Moveable Type (open), Open Foundry. Prefer open-licence families for self-hosting.

## C. Colour
- C-01 Models: HSL/HSB, OKLCH/OKLab (perceptual; preferred for scales), Display-P3 wide gamut, CIELAB, sRGB; `color-mix()`, relative colour syntax, `light-dark()`.
- C-02 Schemes: monochrome; analogous; complementary; split-complementary; triadic; tetradic; neutral + one accent; duotone; tonal (Material) palettes; triad of semantic colours (success/warn/danger/info); gradient families; "earth/ink/paper" palettes; "neon on dark"; "pastel soft"; "high-key / low-key".
- C-03 Systems: design tokens (primitive → semantic → component); 10–12 step neutral scale; accent ramps; surface elevation tints in dark mode; border and divider opacity tokens; overlay and scrim tokens; focus ring token; selection and highlight tokens.
- C-04 Accessibility: WCAG 2.2 contrast (4.5:1 text, 3:1 large text and UI components); APCA as a guide not law; do not rely on colour alone; colour-blind safe palettes (check protanopia/deuteranopia/tritanopia); dark-mode contrast limits; forced-colors / high-contrast mode support.
- C-05 Theming: light, dark, auto (`prefers-color-scheme`), user override, high-contrast, reduced-transparency, "quiet/low-visibility" mode (for privacy-sensitive readers [SAFE]), time-of-day themes, content-derived accent (ambient).
- C-06 Meaning and culture: red (danger, urgency), gold (value, ceremony), green (safety, growth), blue (trust, calm), purple (spiritual, luxury), black (gravity, premium), warm cream (paper, humane), saturated neons (energy, nightlife). Check cultural variation and the reader's state; for crisis audiences prefer calm and non-alarming.
- C-07 Gradients: linear, radial, conic, mesh, noise-grain, animated gradient, text gradient, border gradient; banding avoidance (dither/noise).
- C-08 Rules of thumb: one accent; 60-30-10 distribution; reserve the strongest colour for the single most important action; avoid pure #000 / #fff backgrounds for long reading; test greyscale.

## I. Imagery, illustration, iconography
- I-01 Photography: documentary; editorial portrait; still life; macro; aerial; architectural; cinematic film-still; archival/found; duotone-treated; cutout (background removed); grain-treated. Art-direction rules: consistent light, crop, colour grade.
- I-02 Illustration styles: flat vector; line art / monoline; hand-drawn ink; woodcut/linocut; watercolour; gouache; collage; paper-cut; 3D render; clay; isometric; low-poly; pixel; scientific plate; comic/panel; infographic icons; abstract geometric; generative; textural risograph; blueprints; botanical.
- I-03 Diagrams and figures: annotated figure; exploded view; cutaway; flow diagram; network graph; radial/sunburst; Sankey; chord; treemap; small multiples; timeline; map; matrix/heatmap; ring/orbit diagram; scatter field; isotype/pictogram; waffle; beeswarm; ridgeline; slope chart; stream graph.
- I-04 Iconography: outline (Lucide, Feather, Heroicons, Phosphor), filled, duotone, 3D, pictographic, hand-drawn, emoji-adjacent; stroke width consistency (1.5–2 px at 24 px), optical alignment, 24 px grid, labelled icons beat unlabelled ones. Inline SVG only in this repo [SC].
- I-05 Logo/brand marks: wordmark, monogram, emblem, seal, glyph system, responsive logo, animated logo; favicon and app-icon set; social card system.
- I-06 Patterns and textures: grain, halftone, grid, dots, topographic lines, hatching, paper fibre, noise, scanlines, mesh, moiré, guilloché, ornamental borders, tessellation.
- I-07 Image delivery: AVIF/WebP, responsive `srcset`, art-direction with `<picture>`, aspect-ratio boxes to prevent shift, blur-up/LQIP, lazy loading, SVG for line art, inlined critical imagery.
- I-08 Ethics: no real people's likeness without rights; label composites; avoid stereotyping; AI-generated imagery must be disclosed and rights-checked.

## F. Surfaces, depth and effects
- F-01 Elevation systems: shadow scales (ambient + key), tonal elevation, border-only elevation, layered glass.
- F-02 Materials: paper, glass (blur + refraction + specular edge), metal, ink, stone, fabric, plastic, light/neon, smoke, water, foil, wax.
- F-03 Effects: backdrop blur, gradient glow, inner shadows, bevels, outlines, grain, vignette, chromatic aberration, halftone, duotone, displacement, bloom, glitch, scanlines, depth-of-field blur, parallax layers, reflections, caustics, refractive glass, lens flare.
- F-04 Shape language: sharp rectilinear; rounded (4–8 px, 12–16 px, pill); superellipse (squircle); organic blobs; hand-drawn wobble; circular/radial; diagonal cuts; notched/ticket edges.
- F-05 Borders and rules: hairline (0.5–1 px), double rule, dashed, dotted, offset hard shadow, gradient border, ornamental border.
- F-06 Density tiers and component sizing: airy / comfortable / compact; tap-target floor.
- F-07 Use-with-care effects: heavy blur (battery/GPU), animated filters on large areas, many overlapping transparencies (iOS paint cost), `backdrop-filter` stacking [IOS].
- Always provide: reduced-transparency and forced-colors fallbacks; solid-colour fallback where blur is unsupported.
