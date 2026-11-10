# 04 — Experience, content, safety, accessibility, performance, evaluation

## P. Experience design and emotional tone
- P-01 Emotional registers to choose consciously: calm, awe, curiosity, gravity, warmth, urgency, play, intimacy, solemnity, defiance, relief, trust. Specify the intended feeling for each act or page, and what the reader should be able to *do* after.
- P-02 Reader state model: new/curious; engaged; overwhelmed; in danger; grieving; professional/skeptic; returning; skimming on a bus; reading at night in bed; sharing a device with someone unsafe. Design the default for the most vulnerable plausible reader.
- P-03 Mental models and metaphors: map, field guide, atlas, library, workshop, instrument, ritual, journey, house/rooms, deck of cards, ledger, lens. Pick one metaphor and keep it coherent through nav, language and motion.
- P-04 Pacing: opening moment (title, thesis, threshold), acts, interludes, payoffs, quiet endings, "leave the reader with a next step". Vary density: spectacle sections alternate with reading sections.
- P-05 Progressive disclosure: summary → detail → depth; three reading levels (quick / sequence / full); optional depth never blocks the main path.
- P-06 Agency and choice: reader chooses depth, order, theme, motion, audio; no forced modes; always reversible.
- P-07 Trust signals: sources, dates, method, versioning/changelog, authorship, limits ("what this is not"), honest labels (e.g. composite, depends on the terms, source checked), no false authority ("expert-reviewed" only if true).
- P-08 Shareability and keepsakes: share cards (OG images), printable one-pagers, copyable phrases, downloadable PDFs, deep links, citations.
- P-09 Delight, used sparingly: easter eggs, personality in microcopy, small rewards (not gamification where the content argues against it), well-made empty and loading states.
- P-10 Anti-patterns to avoid: dark patterns, nagging modals, autoplay, scroll-jacking that traps, infinite scroll without landmarks, hidden primary navigation, carousels hiding key content, text over busy imagery, tiny tap targets, mystery icons, cookie banners where none needed, fake urgency, fake scarcity, gamification that contradicts the subject.

## V. Content design and voice
- V-01 Voice dimensions: formal↔casual; warm↔detached; plain↔literary; authoritative↔humble; urgent↔calm. State the voice in three adjectives and three "never" phrases.
- V-02 Plain language: short sentences, active voice, one idea per paragraph, define terms at first use, reading age target (e.g. grade 8–9 for public safety content), avoid jargon and idioms.
- V-03 Structure: scannable headings that carry meaning, lead with the point, numbered steps for procedures, tables for comparisons, callouts for safety and key terms, summaries at top for long pages.
- V-04 Microcopy: buttons as verbs, helpful errors (what happened, why, how to fix), placeholders as examples not labels, empty states that guide, confirmations that state what changed.
- V-05 Labels and taxonomy: consistent names for the same thing; a glossary; reading-time and update-date labels; chapter numbering.
- V-06 Tone for hard topics: describe patterns not people; name the harm without sensationalism; avoid blaming the reader; offer next steps and resources; content notes before distressing material; avoid graphic detail unless necessary.
- V-07 Localisation readiness: avoid text in images, allow 30–40% text expansion, RTL support, locale-aware dates and numbers, translated alt text.
- V-08 Alt text, captions, transcripts, audio description for every non-text asset; figure captions that state what the figure shows and why it matters.

## Q. Safety, privacy and trauma-informed design [SAFE]
Applies to anything on coercive control, abuse, health, minors, or any reader who may be monitored.
- Q-01 Quick Exit: fixed, always visible, one tap/keyboard (Esc ×2 is a common idiom, declare it), navigates with `location.replace` to a neutral site so Back doesn't return; consider clearing in-page state; explain it once, neutrally.
- Q-02 Quiet default: neutral, low-visibility visual identity by default; bright or distinctive themes are opt-in; neutral `<title>` and favicon option; no revealing share previews by default.
- Q-03 No tracking/cookies/storage; no third-party calls (this repo already forbids) ; no push notifications; no accounts; no emailed reminders that could be seen.
- Q-04 Safe-browsing guidance page: private browsing, history, shared devices, clearing, "leave no trace" limits stated honestly.
- Q-05 Trauma-informed principles in UX: safety, trustworthiness, choice, collaboration, empowerment, cultural humility. Concretely: content notes before heavy content; user control over motion/audio/images; no surprise autoplay or sudden movement; clear exits from every state; gentle error language; no forced disclosure; no countdowns or urgency.
- Q-06 Crisis resources: visible, region-aware list; verified numbers; "if you are in immediate danger" line placed first on relevant pages; never claim the site is a substitute for help.
- Q-07 Minors: no interactions that collect data; age-appropriate language; reporting and help routes; separate audience-language rules per book (project rule: never change a book's own audience language).
- Q-08 Claims: no promise of safety, immunity or cure; "documented across", never "proved" unless proved; label composites; no named living people; patterns not people.

## R. Accessibility (WCAG 2.2 AA minimum; aim for AAA where cheap)
- R-01 Perceivable: text alternatives; captions/transcripts; contrast 4.5:1 / 3:1; resize to 200% and 400% reflow; text spacing override; no information by colour alone; orientation not locked; `prefers-color-scheme`, `prefers-contrast`, `forced-colors`, `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-reduced-data` honoured.
- R-02 Operable: full keyboard operation; visible `:focus-visible` rings (≥ 3:1, not clipped); logical focus order; skip links; no keyboard traps; target size ≥ 24×24 CSS px minimum (44 preferred); dragging has alternatives; no time limits or provide controls; pause/stop/hide for moving content; no flashing; focus not obscured by sticky headers (`scroll-padding`).
- R-03 Understandable: language attribute; consistent navigation and labels; predictable behaviour; error identification and suggestion; no unexpected context change.
- R-04 Robust: semantic HTML first; landmarks; headings in order; ARIA only to fill gaps; names/roles/values; live regions used sparingly; test with VoiceOver (iOS/macOS), TalkBack, NVDA.
- R-05 Cognitive accessibility: plain language, chunking, consistent patterns, minimal distractions, undo, clear progress, no memory demands.
- R-06 Testing: axe-core, Lighthouse a11y, keyboard-only pass, screen-reader pass, zoom pass, reduced-motion pass, high-contrast pass, grayscale pass, colour-blind simulation.

## S. Performance and resilience (budgets; IDs PF-xx)
- PF-01 Targets (mid-range phone, throttled 4G): LCP ≤ 2.5 s (aim ≤ 1.5 s); CLS ≤ 0.1 (aim ~0); INP ≤ 200 ms; total initial transfer ≤ 200 KB for text pages (heavier for showcase pages, but progressive); JS ≤ 100 KB gzip initial where possible.
- PF-02 Tactics: inline critical CSS; defer non-critical; subset and preload fonts; responsive images; lazy-load below the fold; avoid layout thrash; `content-visibility: auto`; `will-change` sparingly; GPU-friendly animation (transform/opacity); cap particle counts and canvas resolution by device; pause offscreen animation (IntersectionObserver); frame-budget aware loops; 60 fps target, 30 fps graceful fallback.
- PF-03 Resilience: works without JS (readable content); works offline (self-contained); progressive enhancement; graceful WebGL → Canvas → static fallback; print stylesheet; low-power mode and `prefers-reduced-data` variants.
- PF-04 Device realism: test on a real iPhone (Safari) and a mid-range Android; account for address-bar collapse, safe areas, notch, dynamic island, keyboard overlays, landscape, text-size settings, battery saver.

## T. Evaluation: how to critique a screen (use after every round)
Look at the screenshot, then answer in writing:
1. **First 3 seconds:** what is this, whose is it, what do I do? Cover the logo: could it belong to anyone?
2. **Hierarchy:** one clear focal point? Does the eye path follow intent?
3. **Type:** scale contrast, measure, leading, weight discipline, orphans/widows, fallback flash.
4. **Space:** rhythm, alignment to grid, dead zones, crowding, collisions (text over figure, label over text, anything under a sticky header).
5. **Colour:** accent discipline, contrast, dark/light parity, greyscale test.
6. **Imagery/figures:** compositional focus, quality at 2×/3×, consistency of style.
7. **Motion:** purpose per animation, timing, interruptibility, reduced-motion plan, jank on a throttled CPU.
8. **Interaction:** all states present, targets, one-handed reach, gesture conflicts.
9. **Navigation:** can I tell where I am, go back, leave, find something specific?
10. **Content:** is every line necessary, true, kind, plain? Are safety lines present and first where required?
11. **Craft details:** pixel snapping, icon alignment, consistent radii, focus rings, selection colour, scrollbar styling, overscroll, favicon, tab title, social card, 404, print.
12. **Delight vs noise:** what would a ruthless art director cut?
Automated gates (necessary, not sufficient): axe, console errors, overflow at 375/1440, nothing stuck at opacity 0, reduced-motion run, bounding-box overlap checks between figure stage and text, Lighthouse, real-phone checklist.
