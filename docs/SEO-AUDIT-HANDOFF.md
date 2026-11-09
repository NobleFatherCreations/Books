# Audit brief: findability work on noblefathercreations.com (2026-11-08 → 11-09)

You are auditing work done by a previous AI session to make seven free books findable by search engines and AI
assistants (Google, Bing, ChatGPT, Claude, Perplexity, Gemini). Be skeptical: verify every claim below yourself.
Repo: `NobleFatherCreations/Books`, branch `claude/fervent-cori-gu2uzi`. Read `CLAUDE.md` (binding project rules) and
the newest entries at the end of `MEMORY.md` first.

## 1. What the owner asked for, and decided

- Maximum findability for the free books, with no change to the books' own text or stance.
- Round 1 = exactly seven books: The Sacred Divide (`/faith`), Playground Protectors (`/children`), The Sovereign
  Divine Feminine (`/feminine`), The Fractal (`/fractal`), The Fracture (`/fracture`), The Festie Codex (`/wook`),
  The Festie Bible (`/festival`). Everything else is round 2. The Pattern Decoder (`/playbook`) is parked for the
  owner's own update.
- Licence: **CC BY-NC-ND 4.0** (free, credit required, no selling, no edited copies).
- Analytics: cookieless only (the existing Cloudflare beacon + Search Console/Bing via DNS). No Google Analytics
  (COPPA risk on the children's book).
- Disclaimers: one short notice line on every chapter page linking to the book's full notice.
- Approved new writing: an "In plain words" answer and an "Also known as" line of searched terms on each chapter
  page. Chapter names must not change.
- Playground Protectors pages must stay as kid-like as possible, ages 5+.
- Homepage: intro video as a background (not blocking), all books first, an Art button that opens `/portals`,
  and a simple "Start here" chooser.

## 2. What was built (per book)

Each book keeps its own page/app unchanged in look. The build ADDS:

- one plain HTML page per chapter, `library/<book>/<slug>.html`, served at `/<book>/<slug>` (never
  `<slug>/index.html`, because a trailing-slash redirect would escape the proxy prefix);
- `contents.html`, `sitemap.xml`, `og.png` (1200×630 share card), subset WOFF2 fonts in `f/`;
- on the book's own `index.html`: title, description, canonical, Open Graph, Twitter card and JSON-LD, all tagged
  `data-seo` so rebuilds replace them; the licence line; a version bump with an on-page update note.

| Book | Version | Plain pages | Builder | Notes to check |
|---|---|---|---|---|
| The Fracture | v6 | 13 episodes | `scripts/seo/build_fracture.py` | Sources per episode as `<cite>` + JSON-LD `citation`; Episodes 9–10 state sources not yet attached (book's own note); corrections address added to its legal notice |
| Sovereign Divine Feminine | v6 | 46 (42 chapters + Preface, Rescue, Appendix B, C) | `build_feminine.py` | Replaced a live template placeholder `Copyright (c) [Year] [Author Name]`; fixed 5 double-escaped `&amp;amp;`, a broken Appendix B sentence, an old children's-book title |
| Playground Protectors | v6 | 35 (28 missions + 7 guides) | `build_children.py` | Pages reuse the book's own mission markup and stylesheet (`book.css`, `img/`); Shaela speech bubble; ages 5+ in JSON-LD; small label colours deepened for contrast on these pages only; no Decoder links (kids) |
| The Festie Codex | v15 | 64 (33 chapters, essays, confession, 22 appendices) | `build_wook.py` | Track names promoted to headings; appendices under 120 words skipped |
| The Fractal | v4 | 34 (essays + 26 finished sectors + Mirror) | `build_fractal.py` | Rendered from the book's own `DATA` JSON; 4 sectors the book marks "in production" get no page; first Editorial & Legal Notice added |
| The Festie Bible | v11 | 291 (21 guides + 270 scenarios) | `build_festival.py` | Rendered from `FESTIE_DATA`; "In plain words" = the book's own "What's Actually Happening"; v11 entry added inside its data |
| The Sacred Divide | v6 | (already 34 pages) | `build_faith.py` | Tagged in place, no text moved; must run AFTER `scripts/sacred-divide-site.py` (chained in `sites.json` buildCommand); deploy also needs `pdf/`, `codex.html`, `favicon.ico` |

Shared code: `scripts/seo/seo_common.py` (page template, JSON-LD, fonts, share cards, sitemap, `inject_index`).
New writing lives ONLY in `content/seo/<book>.json` (`plain`, `aka`). Site-wide: `scripts/seo/build_site.py`
(robots.txt with 9 sitemaps, `llms.txt`, `/topics` page with 126 terms, homepage head + og), `scripts/seo/build_hub.py`
(homepage v17).

## 3. Live status (verify!)

- **Live and verified 2026-11-09** (`node scripts/verify-deployed.mjs <book>`): all seven books, 530 pages,
  byte-identical to the repo. Deploy IDs are in `sites.json` → `lastDeploy`.
- **Also live:** The Loop (only a name/menu-label fix). It went live without the owner's clear agreement; they were
  unhappy. The Weighing was left pending on purpose.
- **NOT live:** the homepage (v16 head + v17 redesign), and with it `robots.txt`, root `sitemap.xml`, `llms.txt`,
  `/topics`, `og.png`, the IndexNow key file. The permission classifier blocked it and the owner hasn't approved it.
  IndexNow has NOT been pinged.
- In progress at hand-off: a design-skills review of the v17 homepage (apple-design, emil-design-eng, impeccable,
  ux-heuristics, refactoring-ui, find-animation-opportunities, better-accessibility, web-perf). Its fixes were not yet
  applied.

## 4. How to audit (commands)

Run from `/home/user/Books`. Preview server mirroring live paths: `python3 scripts/seo/serve.py 8765 &`.
Playwright and Chromium are preinstalled (never run `playwright install`). If ESM imports fail, link Playwright with
`ln -sfn $(npm root -g)/playwright node_modules/playwright`.

| Question | Command | Expected |
|---|---|---|
| Is live what the repo says? | `node scripts/verify-deployed.mjs fracture feminine children wook fractal festival faith` | 7 in sync |
| Findability basics on every page | `python3 scripts/seo/verify_seo.py fracture feminine children wook fractal festival faith` | all pass |
| Book text unchanged | `python3 scripts/seo/fidelity.py <book> <original index.html or git rev:path>` (originals: the book's `index.html` at a commit before 2026-11-08, e.g. `git show 98dc754a:library/fracture/index.html > /tmp/o.html`) | 0 not found |
| Duplicates, orphans, alt text | `python3 scripts/seo/audit_onpage.py` | 0 / 0 / 0 |
| Structured data validity | download `https://schema.org/version/latest/schemaorg-current-https.jsonld`, then `python3 scripts/seo/validate_schema.py <file>` | no invalid types/properties |
| Accessibility | `node scripts/seo/a11y.js <urls>` | `TOTAL {}` on new pages |
| Speed (throttled mobile) | `node scripts/seo/perf.js <urls>` | LCP < 2.5s, CLS < 0.1 |
| Visual (375/1440, reduced motion) | `node scripts/seo/shoot.js <outdir> <urls>` | no errors, overflow or stuck opacity |
| Homepage (local) | `node scripts/verify-hub.mjs http://127.0.0.1:8765/` | all ok |

Rebuild everything (idempotent): `for b in fracture feminine children wook fractal festival faith; do python3 scripts/seo/build_$b.py; done; python3 scripts/seo/build_hub.py; python3 scripts/seo/build_site.py`

## 5. Things a skeptical auditor should check

1. **Text fidelity.** `fidelity.py` skips classes `aka`, `plain`, `kid-say`, `byline`, `notice`, `nav` (the owner-approved
   additions). Confirm nothing else is skipped and the original used for comparison is truly pre-change.
2. **Accuracy of the new writing** in `content/seo/*.json`. Each "In plain words" line must match what the chapter
   actually says, and each "Also known as" term must be fair. Sensitive: the Fracture (no living person may be named
   in titles, descriptions or summaries), the Sacred Divide (neutral terms only), the children's book (5+ language).
3. **Legal.** `docs/LEGAL-AUDIT-2026-11-08.md`. Notices must appear on every chapter page; the Fracture and Fractal
   notices offer corrections to `dapperdadnfc@gmail.com` (already public on the Festie Bible). Open gaps not in round
   1: At Will, The Root and The Slow Take lack advice disclaimers; Suno rights for the music are unresolved.
4. **Duplicate content.** Each chapter page canonicalises to itself; each book also exists at `*.netlify.app`.
   Confirm the canonical tags point to `https://noblefathercreations.com/...`.
5. **Routing.** Spot-check `/book/slug` (no trailing slash) for 200 on the live domain, plus `/book/f/*.woff2`,
   `/children/book.css`, `/children/img/*`, `/faith/pdf/*.pdf`, `/faith/codex`.
6. **Project rules** (`CLAUDE.md`): no external requests except the sanctioned Cloudflare beacon; Loop and Weighing
   must have no progress UI; children's gamification untouched; THE HOUSE menu present on chapter pages (copied as
   the exact `#nf-chrome` element; an earlier bug copied the whole Festie Bible app into every page; check it's fixed:
   Festie pages should be about 40 KB).
7. **Homepage v17** (`hub/catalogue-redesign.html`, 0.18 MB). Media moved to `hub/media/` and `hub/f/`; the song has
   `preload="none"` and plays on tap; the intro video is muted, looping and hidden under reduced motion; the gate and
   tour are disabled (the tour is kept `inert`); card facts are updated (Festie Bible 21/270, Codex 33, Sacred Divide
   34). Deploying it must include `media/`, `f/`, `_redirects`, `robots.txt`, `sitemap.xml`, `llms.txt`, `og.png`,
   `topics.html` and `3b85ef6f77878fe76e9845021f786fce.txt`, or live files get deleted.
8. **Honest limits.** Nothing guarantees ranking or AI citation. Off-site steps are owner-only and human-in-the-loop
   (`docs/OFFSITE-PLAN.md`): Search Console and Bing verification by DNS, sitemap submission, IndexNow after the
   homepage is live, resource-page outreach drafts (never auto-sent).

## 6. Key documents

`docs/SEO-AEO-PLAN.md` (plan + owner decisions) · `docs/SEO-ROUND1-REPORT.md` (completion checklist) ·
`docs/LEGAL-AUDIT-2026-11-08.md` · `docs/OFFSITE-PLAN.md` · `BOOKS.md` (findability layer per book) ·
`sites.json` (versions, changelogs, deploy IDs, pending flags) · `MEMORY.md` (dated log, newest at the end).
