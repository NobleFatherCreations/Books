# Findability plan: search engines + AI assistants (2026-11-08)

Status: **PLAN ONLY. Nothing built, nothing deployed.** Owner answered 2026-11-08; see §0, which overrides the rest where they differ.

Goal: anyone asking Google, Bing, ChatGPT, Claude, Perplexity or Gemini about manipulation, coercive
control, workplace coercion, elder abuse, leaving, repair, etc. lands on the free book/chapter that answers it.

---

## 0. Owner decisions (2026-11-08) — these override anything below

- **Round 1 = six books only, "fully tagged as much as possible":** The Sovereign Divine Feminine, Playground Protectors,
  The Festie Bible, The Festie Codex (wook), The Fractal, The Fracture. Every other book waits for round 2, after
  these six are fully done.
- **Homepage: later**, as part of a navigation redesign. Not in round 1. (The 15 MB problem stays open until then.)
- **Analytics: allowed** ("allow full analytics"). Which tool still to confirm (children's book makes cookie-based tools a
  legal problem). The books' own "no tracking" wording must be updated wherever a book gains analytics, so it stays true.
- **Safety books (round 2): full findability, plus a reader-facing toggle** ("discreet mode") — e.g. neutral tab title and
  no history entries while on. Crawlers always see the real titles, so the toggle costs no findability.
- **License:** free forever, credit to Shae Stovell, books updated over time. Exact licence still to confirm.
  JSON-LD will carry `isAccessibleForFree: true`, `author`/`copyrightHolder` Shae Stovell, `dateModified`, `version`.

### Round-1 order (by how each book stores its text, measured 2026-11-08)

| # | Book | Structure | Work |
|---|---|---|---|
| 1 | **The Fracture** | Static HTML, 3.4 MB, 21 clean sections with ids (`ep0`…), 88k words, 195 sources | Pilot: chapter pages split from sections, `<cite>`, `citation` JSON-LD. Simplest clean split. |
| 2 | **Sovereign Divine Feminine** | Static, 4.5 MB, 70 sections, 414 ids; no meta description | Same splitter as Fracture. |
| 3 | **Playground Protectors** | Static, 4.2 MB, 242 sections, **no `<h1>`**, no meta description | Same splitter; add the h1; `audience` schema for kids + grown-ups; gamification untouched. |
| 4 | **The Fractal** | JS data (`CHAPTERS`, `DATA`), 7.7 MB, ~1.3k words visible to crawlers | Own generator from the JS data. |
| 5 | **The Festie Bible** | Entirely JS (`FESTIE_DATA`, `SCENARIO_INDEX`, `RESOURCES`), 176 words visible | Own generator: one page per guide/scenario. |
| 6 | **The Festie Codex** | Static, **14.1 MB, text starts at 11.7 MB, last heading at 14.1 MB** (1 MB under Google's cut-off), 683 sections | Biggest; chapter pages also fix the size risk. Last so the splitter is proven first. |

Every one of the six gets: title/description/canonical/OG/Twitter card, og.png cover card, `Book` + `Chapter` +
`BreadcrumbList` JSON-LD, heading ids, per-chapter plain pages, contents page, per-book sitemap (added to robots.txt and
root sitemap), `<noscript>` contents in the app, cross-links to related books and Decoder tactic pages, llms.txt entry,
version bump + on-page update note. Then verify-seo, Playwright 375/1440, deploy (owner go-ahead), verify-deployed.

## 1. What the audit found (measured 2026-11-08, not assumed)

| # | Finding | Why it matters |
|---|---|---|
| 1 | **9 of 17 sites send crawlers ~200 words.** loop, scale, longafter, silence, atwill, repair, slowtake, festival, fractal keep their text inside JavaScript (`var CH/BODIES`, `const CHAPTERS`). | GPTBot, ClaudeBot and PerplexityBot do not run JavaScript. To them these books are a title and a nav bar. **This is the biggest problem by far.** |
| 2 | **Every book is one URL.** Chapters are `#hash` routes or one long page (Fracture = 88k words on one address). | Search engines treat `#` as the same page. No chapter can rank for the question it answers, and an AI can only cite "the book", not the passage. |
| 3 | **The homepage is 21.3 MB, and its `<h1>` and every book link sit after 18.5 MB.** 21.2 MB of it is base64 images. | Googlebot reads only the first **15 MB** of an HTML file. Google currently sees the homepage with **no heading and no links to any book**. Also a very slow phone load. |
| 4 | No book root has a canonical, Open Graph image or JSON-LD (only the Decoder does). 4 have no meta description (feminine, children, fractal; shadowroot has one). 0 headings carry `id`s outside the Decoder/faith. | Shares show no card; engines can't tell these are free Books by Shae Stovell; nothing is deep-linkable. |
| 5 | Every site is also reachable at its own `*.netlify.app` address. | Duplicate copies; a canonical tag pointing at noblefathercreations.com fixes it. |
| 6 | No `/llms.txt`. robots.txt and the root sitemap are already good (AI crawlers named, 23 URLs + Decoder's 322). | llms.txt is cheap; no engine has confirmed it as a ranking signal. |
| 7 | **Drift:** live `playbook` = Decoder v19 (branch `claude/intelligent-turing-9z46ea`), live `faith` = Sacred Divide v5 (branch `claude/sacred-divide-v5-redesign`). Neither is merged into this branch. loop/scale have small undeployed edits (9 and 27 bytes). | **Any deploy of playbook or faith from this branch would roll live back.** Must merge first. |
| 8 | The Decoder is already done right (v16): 310 plain tactic pages, 10 line pages, sitemap, DefinedTerm JSON-LD. | It is the template for everything below. |

## 2. What we take from the pasted prompts, and what we don't

**Keep (real and useful):** heading/section `id`s; per-page title, description, canonical, Open Graph,
Twitter card; JSON-LD (`Book`, `Chapter`, `WebPage`, `BreadcrumbList`, `WebSite` + `Organization` with
`hasPart` on the homepage); `<cite>` around The Fracture's sources; cross-links between books and to
Decoder tactic pages; llms.txt; a verifier script that scores every page.

**Drop, with reasons:**
- **Renaming files (Step E).** Every book is `index.html` on its own Netlify site, proxied at
  `/loop`, `/atwill`… Renaming breaks the proxy, every link already out there, `sites.json` and
  `verify-deployed`. Book addresses stay as they are; *new* chapter pages get descriptive slugs.
- **`rel="citation"` / `rel="related"`.** Not link types any crawler reads. Plain links with good anchor text do the work.
- **"Semantic priority hints" in sitemaps.** Google ignores `<priority>`. Accurate `<lastmod>` is what counts.
- **A custom `semantic_site_map.json` / `ol-index.json`.** No crawler fetches a custom JSON file. JSON-LD in the page + llms.txt cover it.
- **"License: free to the world".** Needs a real license name (question 3).
- **One hand-edit per file, type 'y' to continue.** Hand-editing 88k-word files heading by heading is how
  corruption got into these books before. Instead: one generator per book engine, run on one book, review,
  ship, verify, then the next. Same control, no hand edits.
- **The 310 tactics.** Already done (Decoder v16).

## 3. The method (same as the Decoder, which already works)

The reader experience does not change. Each book keeps its app at `/slug`. The build **adds** plain HTML pages
generated from the book's own text, so no word is invented:

```
/atwill                         the book as it is today, plus head metadata + JSON-LD + <noscript> contents
/atwill/<chapter-slug>          one plain page per chapter: full text, heading ids, prev/next,
                                "open in the book" button, quick-exit button, Chapter JSON-LD
/atwill/contents                every chapter grouped by movement (the real chapter-index page CLAUDE.md asks for)
/atwill/sitemap.xml             listed in robots.txt
/atwill/og.png                  1200×630 cover card
```

Rules learned the hard way (from MEMORY): pages are `slug.html` served as `/atwill/slug`, never
`slug/index.html` (a trailing-slash redirect escapes the proxy prefix); all links absolute (`/atwill/...`);
canonical always `https://noblefathercreations.com/...`; generated from data, never hand-maintained.

Measurement needs **no tracking code**: Google Search Console and Bing Webmaster Tools verify by a DNS record
and report queries, impressions and clicks from their side. The Cloudflare beacon already counts visits.

## 4. Order of work

**Phase 0 — prerequisites (no reader-visible change)**
1. Merge `claude/intelligent-turing-9z46ea` (Decoder v19) and `claude/sacred-divide-v5-redesign` into this
   branch; `verify-deployed` must show playbook and faith in sync. Look at the loop/scale pending diffs.
2. Install the vetted SEO skills (repo-scoped, `.claude/skills/`): `seo-audit`, `ai-seo`, `schema`,
   `programmatic-seo`, `directory-submissions`, `link-building` from coreyhaines31/marketingskills @96798cf
   (MIT, plain markdown, no hooks/scripts/telemetry; it is the source of the already-installed `site-architecture`).
3. `scripts/verify-seo.mjs`: baseline scorecard per page (words a non-JS crawler sees, title/desc length,
   canonical, OG, JSON-LD validity, heading ids, content offset < 15 MB, safety exit present). Add to `npm run check`.

**Phase 1 — the homepage (one deploy, biggest single fix)**
4. Get the hub under ~3 MB: recompress the inline images (WebP/AVIF), keep them inline so the
   self-contained rule holds. Put the `<h1>` and book links early.
5. Hub `<head>`: canonical, OG card, `WebSite` + `Organization` + `ItemList`/`hasPart` of every book.
6. `/llms.txt` (plain list of every book, chapter index and the Decoder with one-line descriptions).
   Root sitemap becomes a sitemap index of each book's sitemap.

**Phase 2 — books, one per round** (each round: build → verify-seo → Playwright 375/1440 → deploy →
verify-deployed → version bump in `sites.json` + on-page updates note, same commit)

| Order | Book | Why here | Notes |
|---|---|---|---|
| 1 | **At Will** (atwill) | Pilot. Highest-intent searches ("my boss is…"), smallest book on the shared engine. | Builds the generator for the 7-book engine. |
| 2–5 | **The Long After, The Silence, The Slow Take, The Repair** | Same engine → near-free once the pilot works. Coercive-control topics with heavy search demand. | All have a quick-exit button; it goes on every chapter page. |
| 6–7 | **The Loop, The Weighing** | Same engine; ship their pending edits with it. | **No progress bar or "N read" anywhere** (their stated stance). Prev/next and contents only. Add the missing Weighing → Loop link. |
| 8 | **The Fracture** | 88k words, one URL, 195 citations. | Static text already; split by chapter, wrap sources in `<cite>`, `citation` in JSON-LD. |
| 9 | **The Sacred Divide** | Already multi-page (486 pages) after the v5 merge. | Mostly head metadata + JSON-LD. Sensitive subject: descriptions from its own text only. |
| 10–11 | **Sovereign Divine Feminine, Playground Protectors** | Static text, one URL each. | Children's book: plain-language titles, `audience` schema; keep its gamification as is. |
| 12 | **The Fractal** | `const CHAPTERS` format, own generator. | |
| 13–14 | **Festie Bible, Festie Codex** | Different formats; Codex is 14 MB (check the 15 MB line). | |
| 15 | **The Root, Listening Room, workshop pages** | Head metadata only. Root is a practice, not chapters; music isn't a search target for this goal. | |
| — | **Pattern Decoder** | Done. Only gains incoming links from book chapters to its tactic pages. | |

**Phase 3 — off-page (where ranking actually comes from)**
7. Owner: Search Console + Bing Webmaster via DNS; submit sitemaps. Optional IndexNow key file (a static file, no tracking).
8. Outreach through the existing human-in-the-loop system: resource lists at DV/elder-abuse/workplace orgs,
   libraries, therapist directories. Drafts only, never auto-sent.
9. After 4–6 weeks: read Search Console queries, rewrite titles/descriptions for pages with impressions and no clicks.

## 5. Risks and how each is handled

| Risk | Handling |
|---|---|
| Deploying playbook/faith from this branch undoes v19/v5 | Phase 0 merge; `verify-deployed` before every deploy. |
| Chapter titles visible in browser history on a monitored device | Same trade-off the owner accepted for the Decoder; quick-exit + "use a private window" note on every page. **Owner decision (Q2).** |
| Duplicate content (app vs chapter pages vs *.netlify.app) | Self-canonical on each chapter page; canonical to the domain everywhere. |
| Books become multi-file sites | `slug.html` + absolute links (the Decoder's proven pattern); register as a directory `localSource` in `sites.json`. Each book stays well under the 450 MB deploy limit. |
| Breaking a book's stance | Per-book checklist from BOOKS.md before each round (Loop/Weighing: no progress UI; Root: not chapters; children: gamification stays). |
| AI quotes something wrong | Titles, descriptions and Q&A text come only from the book's own sentences, as with the Decoder. |
| Self-contained rule | JSON-LD is inline; og.png is a file the page *names*, not a request it makes; no CDN, no fonts from outside. |
| Overpromising | No tool can guarantee ranking or AI citation. Expect weeks, and it depends on links from other sites. |

## 6. Questions for the owner

1. Tracking rule: keep unchanged? (Nothing above needs tracking.)
2. Safety books: separate findable chapter pages (titles show in history), or only the book's front door?
3. License to declare in JSON-LD.
4. Homepage images: recompress and keep inline, or move to image files?
