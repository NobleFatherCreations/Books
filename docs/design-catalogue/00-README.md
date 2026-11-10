# Design catalogue — how to use it (read this first)

A master vocabulary of visual design, interaction and experience choices, so a build starts by **choosing deliberately from the full menu** instead of defaulting to "dark, serif, beige, cards".

**Honest limits.** This is compiled from the model's knowledge (cut-off mid-2026). "Current" trends move monthly and brand sites change without notice. Treat every brand entry as a lead to verify by opening the live site and screenshotting it (see Refresh protocol). Nothing here is a substitute for looking at real screens.

## Files

| File | Covers |
|---|---|
| `01-styles-and-brands.md` | Named visual styles and movements; what major brands, publishers, studios and design systems are known for; award-site genres |
| `02-foundations.md` | Layout, grids, type, colour, imagery, illustration, icons, surfaces and effects, density, theming |
| `03-motion-interaction-navigation.md` | Motion principles and techniques, scroll storytelling, interaction models, gestures, navigation, components, feedback, sound and haptics |
| `04-experience-content-quality.md` | Mental models, emotional tone, content and voice, onboarding, search, forms, errors, trauma-informed and safety design, accessibility, performance, evaluation |
| `06-master-names-bible.md` | **Start here for "what exists".** 56 categories of pure names: site genres, section types, hero types, nav, scroll techniques, page transitions, text effects, cursor and hover effects, 3D/shader effects, backgrounds, motion vocabulary, cinematic techniques, data-viz forms, design laws, dark patterns, tools, inspiration sources, 2025–26 emerging items |
| `07-choosing-and-combining.md` | **The intelligence layer.** Why outputs burn out (failure modes F1–F14), the Budget (1 lead, 1 signature, ≤3 feature effects), selection procedure, compatibility rules, composing and pacing, recipes, anti-cliché list, acceptance criteria |
| `PROMPT-MASTER.md` | The reusable prompt to start any design session (phases, tools, hard rules). Also invokable as the `/design-director` skill |
| `DESIGN-SYSTEM-GUIDE.md` | **Give this to another AI (and read it yourself).** How the whole system works, the steelman and objections, the opening interview question bank, the operating script, and what the owner must do |
| `COVERAGE-TEMPLATE.md` | One row per category of the names bible; the AI must mark every row USE / REJECTED / N/A so nothing is silently skipped |
| `09-award-winners-data.md` | **Raw data:** verified Awwwards Site of the Year winners 2017–2025, 2024–25 scores, and component profiles of the winners with evidence labels (what each was actually made of), recurring patterns, and a research queue for what is still missing |
| `10-system-gaps-and-improvements.md` | The ten biggest weaknesses of this design system and how to fix them, in suggested order |
| `05-techniques.md` | Concrete web techniques (CSS, JS, SVG, canvas, WebGL, fonts, media) with a self-containment rating for this repo |

Every item has an ID (`S-12`, `T-07`, `M-31`). Cite IDs in your design-direction document so choices are traceable.

## Constraint tags (this repo, from `CLAUDE.md`)

- **[SC]** self-contained: fine as is (plain HTML/CSS/JS/SVG, inline or local files).
- **[LIB]** needs a library copied in as a local file (permissive licence, state size). Ask the owner before adding anything heavy.
- **[NET]** needs a network request at run time. **Not allowed** (only the Cloudflare beacon is sanctioned).
- **[SAFE]** relevant to safety-sensitive pages (coercive-control, abuse, minors): see file 04, section Q.
- **[IOS]** known iOS Safari pitfalls; test on a real phone.

## The selection method (do this in order)

1. **Write the brief in 8 lines.** Who is the reader, what state are they in (calm, curious, stressed, in danger, on a shared device), what must they do or feel, on what device, how long a session, what the content is (chapters, tools, data, stories), what must never happen, what the owner has already said.
2. **Choose a position on each axis** (see Axes below). Write one sentence per axis. Do not skip axes; a skipped axis defaults to generic.
3. **Pick from the catalogue, three candidates per category that matters** (style, type, colour, layout, motion, navigation, imagery). For each, note why it fits and the one risk. Reject on purpose, and write why.
4. **Compose a coherent set**, not a collage. Two strong styles clash unless one leads. Limit: one lead style, one supporting influence, one signature move.
5. **Run the constraint filter**: tags above, accessibility minimums (file 04 section R), performance budget (file 04 section S), the project rules, anything the owner forbade.
6. **Prototype one hero screen on a phone-size and a desktop-size canvas**, screenshot, read the image, critique against file 04 section T. Only then scale.
7. **Record the choices** in `DESIGN-CHOICES.md` for that project using the template at the end of this file.

## Axes (choose a position on each, in words)

Quiet ↔ loud · Warm ↔ cool · Human/handmade ↔ engineered/precise · Dense ↔ spacious · Text-led ↔ image-led ↔ figure-led · Static ↔ choreographed · Playful ↔ grave · Familiar ↔ novel · Intimate ↔ monumental · Dark ↔ light (and whether both) · Flat ↔ dimensional · Editorial ↔ product ↔ cinematic ↔ tool · Guided linear ↔ free exploration · Reassuring ↔ provocative · Timeless ↔ of-the-moment.

## Refresh protocol (do before trusting "current")

1. Open 8–12 live reference sites for the job with Playwright; screenshot at 390 and 1440; read the images.
2. Search recent design-trend write-ups and award-site (Awwwards, FWA, CSS Design Awards, Site Inspire, Godly, Lapa Ninja, Mobbin, Page Flows, Dribbble/Behance trends, Typewolf, Fonts In Use, Pentagram/Collins case studies); note what changed since this file's date.
3. Add what you learned to the catalogue with date and source. Never delete an entry; mark it dated.

## Template: `DESIGN-CHOICES.md`

```
Brief (8 lines):
Axes (one sentence each):
Lead style: [ID] why / risk
Supporting influence: [ID]
Signature move: [ID]
Type: display [ID], text [ID], mono/aux [ID]; scale; measure
Colour: [ID], tokens (light/dark), contrast table
Layout & grid: [IDs]
Imagery / illustration / icons: [IDs]
Motion: principles [IDs], durations/easings, reduced-motion plan
Navigation & interaction: [IDs]
Content voice & safety: [IDs]
Rejected (with reasons):
Constraint filter results:
Hero-screen screenshot paths and critique notes:
```


## Gates script
`node scripts/design-gates.mjs <url> <outdir> [--profiles phone-light,desktop-dark,...] [--max 60]` screenshots every scroll step on phone and desktop (light, dark, reduced motion) and fails on figure/text collisions, text over text, page errors, external requests, overflow and reduced-motion violations; warns on tiny text, small tap targets, translucent headers, background-figure legibility, unloaded fonts and too many simultaneous animations. Always read the screenshots it saves.
