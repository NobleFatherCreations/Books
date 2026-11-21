# SEO plan: getting people who search "manipulation", "narcissistic abuse" and similar to the books and the Pattern Decoder

Owner, 2026-11-21: "How can we build the seo that leads as many ways as possible to my books or decoder when people search manipulation or narcissistic abuse etc. I want as many people to see my content as possible."

## What the site already has (the strongest assets)
- **The Pattern Decoder: 384 pages**, one per pattern, each with its own title ("Gaslighting: What It Is, What It Is Made Of and What to Do"), a description, a canonical address on the main domain and structured data. These are the pages that can rank for single searches like "gaslighting", "love bombing", "DARVO", "trauma bonding" and "silent treatment".
- **Topics A to Z** (/topics): 140 topics, each linking to the chapters and decoder pages that cover it, including "Narcissistic abuse cycle", "Coercive control", "Emotional abuse" and "Cycle of abuse".
- **14 books** with chapter pages, each with its own SEO head (scripts/seo/build_site.py).
- **robots.txt** invites every search engine and AI assistant by name; 10 sitemaps; **llms.txt** (306 lines) describes the whole site for AI assistants; an IndexNow key for instant re-indexing.

## What changed on the homepage this round
1. **Title**: "Free Books on Manipulation and Narcissistic Abuse | Noble Father Creations" (was "...Manipulation, Safety and Power"). The words people type now lead.
2. **Description**: names manipulation, narcissistic abuse, gaslighting and coercive control, and says what the reader gets.
3. **"Look up a pattern"** (under Free tools): 18 plain links, with the searched words as the link text, straight to the decoder and topic pages: narcissistic abuse, gaslighting, love bombing, trauma bonding, coercive control, silent treatment, DARVO, triangulation, hoovering, future faking, stonewalling, isolation, financial control, emotional abuse, cycle of abuse, spiritual abuse, workplace gaslighting, medical gaslighting. Plus "All 335 tactics" and "Every topic, A to Z". Links from the homepage carry the most weight a site can give; before this the homepage never linked to a single decoder pattern.
4. **Structured data**: the site record now lists those subjects ("about", each pointing at its page) and their keywords, so search engines and AI assistants can match the site to them.
5. **One h1** (the name) and the full SEO head (canonical, Open Graph, Twitter card, licence, JSON-LD) are guarded by `scripts/verify-hub.mjs`, so a build that drops them fails.

## What only the owner can do (in order of payoff)
1. **Google Search Console** (search.google.com/search-console): add the property noblefathercreations.com (DNS verification at the domain registrar), then submit `https://noblefathercreations.com/sitemap.xml`. This is how Google learns all 23 homepage addresses plus each book's and the decoder's sitemaps, and it shows which searches already find the site.
2. **Bing Webmaster Tools** (bing.com/webmasters): import from Search Console in one click. Bing also feeds ChatGPT search and DuckDuckGo.
3. **Links from other sites** are what move rankings most. The repo's outreach system (CLAUDE.md, "Outreach system": find ~20 real targets, a short personal note that leads with value to their audience, owner sends each one) fits: survivor-support blogs, therapists' resource pages, subreddit wikis (r/NarcissisticAbuse, r/emotionalabuse), domestic-abuse charities' resource lists, festival-safety groups for the Festie books. Ask me to draft the first batch; nothing is ever sent automatically.
4. **TikTok**: link individual decoder pages (for example /playbook/gaslighting) in video captions and the bio, not only the homepage. Each one is a page that can rank on its own.

## Next on-site steps (ask when wanted)
- The same "Look up a pattern" links inside each book's closing pages (connectors only, never the book's wording).
- A short definition paragraph at the top of each Topics A to Z entry (new words: owner approval needed).
- Recheck rankings in Search Console after about four weeks and add homepage links for the searches that show up.
