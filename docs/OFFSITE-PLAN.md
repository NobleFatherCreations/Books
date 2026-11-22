# Off-site plan: links and mentions (2026-11-08)

The on-site work makes every chapter findable. Ranking and AI citation also depend on other trusted sites
linking to or mentioning the books. Nothing here is automated: every message is a draft the owner approves and
sends (CLAUDE.md "Outreach system"). No paid links, no link swaps, no "write for us" networks.

## 1. Free foundations (owner, about an hour, do first)

| Step | Where | Why |
|---|---|---|
| Verify the domain by DNS, submit all 9 sitemaps (listed in robots.txt) | Google Search Console, Bing Webmaster Tools | Bing feeds ChatGPT search, Copilot and DuckDuckGo; Google feeds Gemini and AI Overviews. Shows which searches find each page. |
| Turn on IndexNow in Bing Webmaster Tools | Bing | New and updated pages reach Bing (and Yandex, Naver) in minutes instead of weeks. |
| Upload the PDFs (Sacred Divide has 34; others can be printed to PDF) | Internet Archive (archive.org), CC BY-NC-ND 4.0 | The licence allows it; archive.org is heavily crawled and cited, and each item links home. |
| List the free books | Open educational resource catalogues: OER Commons, MERLOT | Free, licensed, educational: exactly what they list. |
| List `/llms.txt` (live once the hub is deployed) | llmstxt.site, directory.llmstxt.cloud, llmstxthub.com (use its site form) | Where AI tooling looks for site maps written for models. |
| Add the author and each book as items | Wikidata (free, anyone can edit; cite the book's own page) | Wikidata feeds search engines' knowledge panels and AI training data. Neutral facts only: title, author, licence, URL. |
| Add each book as a record | Open Library (openlibrary.org, free) | A library catalogue entry that links to the free online edition. |
| Same name, bio and link everywhere | TikTok bio, any profile | Engines match "Shae Stovell / Noble Father Creations" across sites (consensus). |

Skipped on purpose (directory-submissions skill, adapted): Product Hunt, G2/Capterra, SaaS/AI-tool directories and
paid "submission packages". They are for software and would be the wrong category for free books.

## 2. Resource pages that fit each book (verify each page exists before drafting)

| Book | Organisations whose readers it serves |
|---|---|
| The Festie Codex, The Festie Bible | DanceSafe, Zendo Project, Fireside Project, Bunk Police (all already credited in the Codex), festival harm-reduction teams, r/festivals and r/aves wikis |
| Playground Protectors | School counsellors' associations, PTA resource pages, Stomp Out Bullying, PACER's National Bullying Prevention Center, Common Sense Media (all already named in its Resources) |
| The Sovereign Divine Feminine | Domestic-abuse charities' "further reading" pages, coercive-control education projects, survivor communities |
| The Sacred Divide | Faith to Faithless, Recovering from Religion, Journey Free, cult-recovery associations (ICSA), religious-studies course reading lists |
| The Fracture, The Fractal | Economic-inequality newsletters and reading lists, media-literacy educators, librarians' subject guides |

## 3. Draft template (under 150 words, value to their readers first)

> Subject: A free resource for [their audience]
>
> Hi [name], I read your [page name] and the way you [specific thing they do]. I wrote a free, ad-free guide,
> [book], that your readers may find useful: [one chapter that matches their page, with its link]. Every chapter has
> its own page, it works offline, and it is free to share under a Creative Commons licence. If it fits your
> resources list, I would be grateful for a mention. Either way, thank you for the work you do.
> Shae Stovell, noblefathercreations.com

Track each one in `outreach-tracker.csv` (target, page, chapter offered, date sent, reply).

## 4. What to measure (monthly, no tracking code needed)

- Search Console and Bing: impressions and clicks per chapter page; queries with impressions but no clicks are the
  titles to rewrite.
- Referring sites (Search Console "Links").
- AI check: ask ChatGPT, Perplexity, Claude and Gemini 10 real questions (for example "what is DARVO", "how do I
  help a friend having a bad trip", "is my church high-control"), 3 runs each; note whether a book is cited.
