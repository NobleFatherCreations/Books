# Where Noble Father Creations is submitted (status tracker)

Started 2026-11-23. **Status:** done / waiting on the owner / not recommended.
**Rule:** nothing is posted, emailed or filed in the owner's name without their go-ahead for that venue (CLAUDE.md outreach rule).

## Already in place on the site (checked live 2026-11-23)
- **robots.txt** allows every crawler and names the AI crawlers. It lists 17 sitemaps.
- **Sitemaps:** 1,412 live URLs.
- **llms.txt:** the hub's and the Decoder's, plus the Decoder's llms-full.txt.
- **Structured data:** books, chapters, terms, FAQs, citations and the About page. Valid on 1,125 pages.
- **Share cards:** 367 Decoder cards and one per book.
- **IndexNow key:** live at `/3b85ef6f77878fe76e9845021f786fce.txt`.
- **Problem found:** `/fractal/entertainment` redirects to `/fractal2/entertainment`, which returns 404. That's the Fractal entertainment site's own redirect, so its sitemap in robots.txt is unreachable. It was already broken before today and belongs to the Fractal² rework. **Owner decides.**

## 1. Search engines
| Where | Status | How |
|---|---|---|
| Bing (which also feeds DuckDuckGo, Yahoo, Ecosia, ChatGPT search and Copilot) | **done** | IndexNow, 1,412 URLs, 200 |
| Yandex | **done** | IndexNow, 202 |
| Seznam, Naver, Yep | **done** | The IndexNow network (api.indexnow.org, 200) shares with all members |
| Google (Search, AI Overviews, Gemini) | **done** (verified since 2026-11-09; all 16 sitemaps submitted and read with Success, 2026-11-23) | Search Console |
| Bing Webmaster Tools (reports, crawl control) | **done** (owner, 2026-11-23) | Site imported. All 16 sitemaps submitted. IndexNow shows 4.2K URLs received. Bing's one note: "lacks inbound links from high-quality domains" (fixed by section 6, not by the site). |
| Yandex Webmaster, Naver Search Advisor | optional | Verification codes only. IndexNow already reaches them. |
| Brave Search (which also feeds Claude's web search), Mojeek, Apple (Siri and Spotlight) | covered | They have no submission form. Their crawlers are allowed in robots.txt and discover the site through links. |
| Baidu | not recommended | Needs a Chinese licence, and the audience isn't there. |

## 2. AI answer engines
| Where | Status | How |
|---|---|---|
| ChatGPT, Perplexity, Claude, Copilot, Gemini | covered | Crawlers allowed, llms.txt, the Bing and Google indexes. No submission forms exist. |
| llms.txt directories (llmstxt.site, directory.llmstxt.cloud) | **waiting on the owner** | A short form or GitHub pull request each. I can draft them. Needs a yes, because it's posted in the owner's name. |
| Common Crawl (training and research data for most AI models) | covered | CCBot is allowed. It crawls on its own. |

## 3. Archives
| Where | Status | How |
|---|---|---|
| Internet Archive, Wayback Machine | **done, 42 key pages** | Anonymous "Save Page Now", one every 15 seconds. Log: `/tmp/claude-0/archive.log` (scratch). |
| Internet Archive, full texts | **waiting on the owner** | A free archive.org account, then upload each book as a PDF or EPUB under CC BY-NC-ND. They then appear in its library and in Open Library. |

## 4. Book catalogues
| Where | Status | How |
|---|---|---|
| Open Library | **waiting on the owner** | A free account. One record per book with "read online" pointing at the site. I can prepare all 14 records (title, author, description, subjects, link). |
| Goodreads | **waiting on the owner** | The owner's account, then the Author Program. Books without an ISBN can be added. |
| Google Play Books (free ebooks) | waiting on the owner, later | Needs an EPUB or PDF per book and a Partner Center account. |
| ISBNs | owner decides | Optional. Free in some countries, paid in the US (Bowker). They help with libraries and Goodreads. |

## 5. Knowledge graph and encyclopedias
| Where | Status | How |
|---|---|---|
| **Wikipedia** | **not recommended now** | Wikipedia's rules forbid writing about your own work (conflict of interest), and an article needs *significant coverage in independent sources* such as news, reviews or academic citations. An article written now would be deleted and could mark the site as spam. **Path:** get independent coverage first (press, the DV-sector listings below, academic citation of the Decoder dataset). Then someone else can request an article, or the owner can propose one on the Talk page with a conflict-of-interest disclosure. |
| Wikidata | later | Items need serious public references. Best after a DOI (Zenodo) and some independent coverage. Then items for the author, the Decoder (as a dataset) and the books. |
| Google Knowledge Panel | later | It appears once Google links the entity. Then the owner claims it. `sameAs` links speed this up (see "What I need"). |
| ORCID (author identity for researchers) | **waiting on the owner** | A free account in the owner's name. I add it to the site's `sameAs`. |
| Zenodo (a permanent DOI for the Decoder dataset and the books) | **waiting on the owner** | A free account (it can sign in with GitHub). I prepare the files and metadata. A DOI lets researchers cite it, which is a step toward Wikipedia and Wikidata. |

## 6. Directories and curated lists (people review these)
| Where | Status | How |
|---|---|---|
| Curlie (the volunteer web directory that replaced DMOZ) | **waiting on the owner** | A free form per site, in the right category. Volunteers review it, slowly. |
| DV and abuse resource libraries: VAWnet (NRCDV), NNEDV Safety Net (tech abuse), the owner's state coalition, Women's Aid UK resources | **waiting on the owner** | A personal email each (CLAUDE.md outreach: under 150 words, value first, human sends). I draft. |
| Cultic studies: ICSA resource lists | **waiting on the owner** | Same. |
| University library guides (LibGuides on coercive control, manipulation, media literacy) | **waiting on the owner** | Emails to subject librarians. I find about 20 real guides and draft. |
| GitHub "awesome" lists (psychology, mental health, media literacy, open data) | **waiting on the owner** | Pull requests from the owner's account. I prepare the entries. |
| Hugging Face and Kaggle datasets (the Decoder taxonomy) | **waiting on the owner** | The owner's accounts. Licence decision first (CC BY-NC-ND now). |

## 7. Social previews (Facebook is the top referrer)
| Where | Status | How |
|---|---|---|
| Facebook Sharing Debugger | **waiting on the owner** | Logged in, paste each changed URL, click "Scrape again", so the new Decoder cards replace the old cached previews. Start with /playbook, /playbook/gaslighting and /longafter. |
| LinkedIn Post Inspector | optional | Same idea. Needs a login. |

## What I need from the owner
1. **Google Search Console** is already verified, so no file is needed. Submit the 16 sitemaps under Sitemaps. The 17th (Fractal entertainment) is broken live, so skip it.
2. **Bing Webmaster Tools.** After Google, choose "Import from Google Search Console". Nothing to send me.
3. **Your public profile links**, for `sameAs`: Facebook page, TikTok, Instagram, YouTube, GitHub and any others you want tied to Shae Stovell and Noble Father Creations.
4. **Which accounts you'll make:** Internet Archive, Open Library, Goodreads, Zenodo, ORCID, Curlie. For each, I prepare everything so it's paste-and-submit.
5. **Yes or no for outreach drafts:** DV libraries, ICSA, librarians, awesome lists, llms.txt directories. I draft, you send.
