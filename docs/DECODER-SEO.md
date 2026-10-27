# Pattern Decoder: how it is findable (v16, 2026-10-27)

The owner decided the guide should be found by search engines and AI assistants, so the privacy shield was dropped:
no more `noindex`, no more neutral tab title or numbered addresses. The reader app's design is unchanged.

## Why plain pages, not just meta tags in the app

The app is one 3.3 MB page with hash routes (`#/entry/gaslighting`). Search engines treat everything after `#` as the
same page, and most AI crawlers (GPTBot, ClaudeBot, PerplexityBot) do not run JavaScript. Changing the app's title
and JSON-LD per route (which v16 also does) cannot give 310 tactics 310 addresses. So the build also writes:

| Address | What it is |
|---|---|
| `/playbook` | the reader app (descriptive title, canonical, Open Graph, `DefinedTermSet` + `WebApplication` JSON-LD, a `<noscript>` index of links) |
| `/playbook/<slug>` (310) | the full entry in plain HTML (about 33 KB): safety note first where sensitive, the answer, signs both ways, questions, what it is, what you can do, fair use of the label, look-alikes, previous/next on the line. JSON-LD `DefinedTerm` (with `termCode` such as `T01`), `WebPage`, `BreadcrumbList`. A white button opens the same entry in the app. |
| `/playbook/line-<key>` (10) | the line's stations in order (`CollectionPage` + `ItemList`) |
| `/playbook/tactics` | every tactic grouped by line |
| `/playbook/sitemap.xml` | the 322 addresses above |
| `/robots.txt`, `/sitemap.xml` (hub) | robots allows everyone and names the AI crawlers explicitly; both sitemaps are listed |

Titles: `<Tactic>: Signs, Examples and What to Do · Pattern Decoder`. Descriptions: `What is <Tactic>? <short definition>`
(clipped at 160). The tactic name goes first in the title on purpose, because Google cuts titles at about 60 characters.
The owner's draft template began with `Line <Roman numeral> |`. v15 lines are lettered, not numbered, and putting the
line first would push the words people search for out of view. "Sovereign exit strategy" was left out of descriptions
because the entries do not use that phrase.

## Files

- `design/decoder_pages.py` lays out the plain pages and sitemap. Content comes only from the build's own entry
  assembly, so no word is invented or changed. All links are absolute (`/playbook/...`) because of the proxy.
- `design/build-decoder-v15.py` writes `instruments/playbook/site/`, which is the publish directory. The plain pages
  have their own gate: no placeholders in visible text, no `noindex`, every tactic has a page, and the sitemap count
  is right.
- `design/decoder-v15/app.js` `seo()` sets the title, description, canonical, Open Graph and DefinedTerm for each route.
- `scripts/build-root-sitemap.py` builds `hub/sitemap.xml` from the hub's `_redirects`.
- `scripts/decoder-verify.js` (109 checks) now asserts the findable contract instead of the old private one.

## Deploying

The playbook folder goes up whole (`instruments/playbook/site`, 324 files) to `noblepatterns`. The hub goes up as
`index.html` + `_redirects` + `robots.txt` + `sitemap.xml`. Netlify serves `/gaslighting` from `gaslighting.html`
without a redirect (verified through the proxy), so do not switch to `gaslighting/index.html`: a trailing-slash
redirect would escape the `/playbook` prefix.

## Still to do (not code)

- Submit both sitemaps in Google Search Console and Bing Webmaster Tools (this needs the owner's account).
- Ranking and AI citation take weeks and depend on links from other sites; nothing here can promise them.
- What readers lost: a monitored browser's tabs and history now show the tactic's name. Settings and the safety page
  say so, and recommend a private window. Leave is unchanged.
