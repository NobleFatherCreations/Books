# Search and AI reach: the maximum plan (2026-11-21)

Goal (owner): the highest chance that noblefathercreations.com, the books and the Pattern Decoder show up at the top of search engines and in AI answers for manipulation, narcissistic abuse, gaslighting, coercive control and related searches.

Ground rules that stay: every title, description and answer is taken from the books' own sentences (nothing invented); no tracking added (Cloudflare beacon only); Leave now on every page; owner approves new wording; deploys only on the owner's word.

## Where things stand (measured today)
- Search-ready: homepage, Pattern Decoder (380 pages), The Sovereign Divine Feminine, The Fracture, The Festie Codex, The Festie Bible, The Sacred Divide, Playground Protectors; The Fractal needs a sitemap tidy-up.
- **Not search-ready: The Long After, The Silence, The Repair, At Will, The Slow Take, The Loop, The Weighing.** One page each, text inside JavaScript: crawlers and AI assistants see about 200 words, no title card, no description, no structured data.
- Google Search Console and Bing Webmaster: verified by the owner. IndexNow ping runs after deploys.

## Progress
- 2026-11-21: **Round 2 built** (scripts/seo/build_jsbook.py + jsbook_extract.js): 316 chapter pages across the seven books, each with title, description, canonical, Chapter/Book/Breadcrumb data, share card, sitemap, contents page; every chapter links into the Pattern Decoder (423 links, plus a fallback link on chapters that name no pattern); robots.txt lists 17 sitemaps; llms.txt lists every chapter. verify_seo passes on all 7, schema valid on 531 pages, axe clean. **Not deployed** (needs the owner's word: 7 book sites + the homepage for robots/llms).

## Priority order (biggest gain first)
| # | Work | Why it moves rankings | Skill / tool |
|---|---|---|---|
| 1 | **Round 2: crawlable chapter pages for the 7 one-page books** (titles, descriptions, canonical, Book + Chapter + BreadcrumbList data, share card, sitemap, Leave now on every page) | These are the coercive-control books with the most search demand and they are invisible today | existing `scripts/seo/build_*.py` pattern; `programmatic-seo`, `schema`; gate `verify_seo.py` |
| 2 | **The link web**: every chapter links to the Decoder pages it covers; every Decoder page lists the chapters that cover it; related-chapter links between books | Internal links tell Google which page answers which search, and pass strength to the pages that should rank | `site-architecture`, `information-architecture`; a link-map script from the books' own text |
| 3 | **Topics A to Z as real pages** (/topics/gaslighting, 140 of them) instead of anchors on one page, each gathering the chapters and Decoder entries for that topic | 140 more pages that can each rank for one search | `programmatic-seo` |
| 4 | **Answer-first for AI**: a short plain answer at the top of each Decoder and topic page (already in the Decoder), `llms-full.txt` (the full readable text for AI assistants), a Markdown copy of each chapter | AI assistants quote pages that answer in the first lines and that they can read without running code | `ai-seo` |
| 5 | **Entity signals**: Person and Organization data with `sameAs` links (TikTok and any other profiles), consistent author name on every page, a short About page | Helps Google and AI treat Shae Stovell and Noble Father Creations as a known source | `schema` |
| 6 | **Trust and freshness**: real last-modified dates in sitemaps (today every URL shows the build date); one tactic count everywhere (310 / 335 / 380 disagree) | Accurate signals; contradictions cost trust | `seo-audit` |
| 7 | **Links from other sites** (the strongest ranking factor): survivor blogs, therapists' resource pages, abuse charities' resource lists, subreddit wikis, festival-safety groups; free-resource directories | Nothing on the site can substitute for these | `link-building`, `directory-submissions`; drafts in Gmail, sent by the owner (never automatic); tracker in `outreach-tracker.csv` |
| 8 | **Video and social**: TikTok captions and YouTube descriptions that link single Decoder pages, titles in the words people search | Video results and social links bring readers and links | vidIQ MCP (titles, keywords), Metricool MCP (scheduling, owner approves) |

## Measuring it (no tracking added)
- **Which crawlers visit, and which pages**: Netlify request logs (Netlify MCP observability: top user agents and URLs), monthly report of Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot visits.
- **Rankings and search terms**: Google Search Console. There is no Search Console tool connected here; connecting one (for example through the Composio connector, if the owner wants) would let me read which searches show the site and at what position.
- **AI answers**: a monthly check of what ChatGPT search, Perplexity and Google AI answers say for 20 target searches (TinyFish MCP web search / monitors; uses credits).
- Visits: the homepage counter and `scripts/cf-analytics.py` (Cloudflare).

## Doing it more efficiently
- One deploy command per site: build, run the gates (`verify-hub.mjs`, `verify_seo.py`, `validate_schema.py`), deploy, compare live bytes, ping IndexNow. Today these are separate steps I run by hand.
- Run `verify_seo.py` over every book in one go and fail the build on any regression (the homepage already has this in `verify-hub.mjs`).
- Build round-2 books from one shared generator instead of one script per book (the seven share the same JavaScript data shape).
- Skills not yet used for this, and what each adds: `programmatic-seo` (topic and chapter pages at scale), `schema` (Book/Chapter/FAQ/Person data), `ai-seo` (answer-first structure, llms-full.txt), `link-building` and `directory-submissions` (off-site), `site-architecture` (the link web), `content-marketer` agent (outreach notes and social copy for owner approval).
