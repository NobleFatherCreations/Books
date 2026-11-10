# Round 1 findability: completion report (2026-11-08)

Seven books (The Sacred Divide, Playground Protectors, The Sovereign Divine Feminine, The Fractal, The Fracture,
The Festie Codex, The Festie Bible) plus the homepage. Built, verified and pushed. **Not deployed.**

## Checklist

| # | Item | Status | Proof |
|---|---|---|---|
| 1 | Every chapter has its own page with the book's full text | ✓ 518 pages | verify_seo.py |
| 2 | Not one word of book text changed on those pages | ✓ 27,797 blocks verbatim | fidelity.py |
| 3 | Text readable without JavaScript (AI crawlers) | ✓ every page | verify_seo.py (words without JS) |
| 4 | Search title + description, unique on every page | ✓ 0 duplicates | audit_onpage.py |
| 5 | Canonical address on the real domain | ✓ | verify_seo.py |
| 6 | Share cards (Open Graph, Twitter) + og.png per book | ✓ 8 cards | verify_seo.py, screenshots |
| 7 | Structured data: Book, Chapter, Breadcrumbs, Person, Organization, WebSite, DefinedTermSet | ✓ 0 invalid | validate_schema.py vs schema.org |
| 8 | Citeable sections (ids on headings) | ✓ | verify_seo.py |
| 9 | "In plain words" answer on every chapter page | ✓ (approved #2) | content/seo/*.json |
| 10 | "Also known as" searched terms on every chapter page | ✓ (approved #4) | content/seo/*.json |
| 11 | Contents page per book; prev/next; breadcrumbs; related books | ✓ 0 orphans | audit_onpage.py |
| 12 | Links into the Pattern Decoder's tactic pages | ✓ (none from the kids' book, on purpose) | link audit |
| 13 | Library-wide Topics page (126 terms → chapters) | ✓ /topics | screenshots, axe |
| 14 | Sitemaps (9) listed in robots.txt; AI crawlers named | ✓ | hub/robots.txt |
| 15 | llms.txt map for AI assistants | ✓ | hub/llms.txt |
| 16 | IndexNow key + ping script (run after deploy) | ✓ ready | scripts/seo/indexnow.py |
| 17 | Licence: CC BY-NC-ND 4.0 on every page + in data | ✓ | verify_seo.py |
| 18 | Legal notice line on every chapter page, linking the full notice | ✓ | verify_seo.py |
| 19 | Fractal legal notice; corrections address (Fractal, Fracture, Festie Bible, Sacred Divide) | ✓ | legal audit |
| 20 | Visible byline + updated date | ✓ | screenshots |
| 21 | Menu labels correct everywhere (Sacred Divide, Decoder 310, The Listening Room) | ✓ 53 files | grep |
| 22 | Kids' pages in the book's own style, ages 5+ | ✓ | screenshots |
| 23 | Accessibility (WCAG 2.2 AA, axe) on new pages | ✓ 0 issues | a11y.js |
| 24 | Speed: LCP ~0.5s, layout shift 0–0.02 on throttled mobile | ✓ | perf.js |
| 25 | Phone + desktop, reduced motion, no errors, no overflow | ✓ | shoot.js |
| 26 | Version + update note on each page and in sites.json | ✓ | sites.json |
| 27 | Repo matches live except these pending deploys (0 drift) | ✓ | verify-deployed.mjs |

## Skills used
seo-audit, ai-seo, schema, programmatic-seo, site-architecture, web-perf, web-accessibility (axe), no-ai-slop,
link-building, directory-submissions; a reviewer agent applied ux-heuristics, web-design-guidelines,
better-accessibility, refactoring-ui and impeccable (critique) to the template. Not applicable to this job:
animation/motion skills, ponytail family (code-bloat), pick-ui-library, prototype, apple-design, emil-design-eng,
frontend-design (no new visual design beyond the books' own), grill-me, copy-editing (covered by no-ai-slop on the only new text).

## Known, honest limits
- Nobody can guarantee rankings or AI citations; they take weeks and depend on other sites linking (docs/OFFSITE-PLAN.md).
- The homepage is still 21 MB, so Google cannot read its book links (they start at 18.5 MB). Sitemaps, /topics and
  llms.txt route around it; the fix is the homepage redesign you planned.
- The books' own front pages stay heavy (Fracture 3.3 MB, Codex 14.1 MB); the chapter pages are the fast landing pages.
- The Sacred Divide's own pages have accessibility issues in their existing design (same on live today); not changed.
- Pattern Decoder parked until your update; the other books (Loop, Weighing, etc.) are round 2.
