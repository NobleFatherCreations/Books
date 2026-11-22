# Pattern Decoder v21: one rebuild, one deploy (proposal, 2026-11-22, nothing built)

Live: v20 (2026-11-09). This round adds the five missing books' back-links, and bundles every other Decoder change found in the same audit, so the Decoder only needs to be rebuilt and redeployed once.

## What the audit found (measured, not guessed)
| Finding | Number |
|---|---|
| Books whose chapters link to the Decoder but get no link back ("Where this comes up in the books") | 5: longafter (65 pages), silence (34), atwill (22), repair (34), slowtake (34) |
| Links from the books that point at an old address and only reach the page through a redirect | 121 of 1,155 (fractal 71, feminine 30, wook 12, festival 7, fracture 1). No links are broken. |
| hub/llms.txt still says "310 tactics" | It's now 335 tactics plus 32 patterns |
| Sitemap `lastmod` is the same date (2026-11-09) on all 380 URLs | No signal of which pages actually changed |
| Page titles over 70 characters (cut off in search results) | 153 of 380 |
| Single tactics that link to the patterns they belong to | 0. Patterns link down to their parts, but nothing links back up. |
| Decoder 404 page | none |
| Research sources on tactic pages | none. The Long After already has 40 DOI-verified sources, and several match Decoder entries directly (see C1). |
| Long After A to Z entries that link to the Decoder | 0 |

## A. Must do (the back-links themselves)
1. **Add the five books to `BOOKS`** in `design/decoder_v20.py` (longafter, silence, atwill, repair, slowtake). This adds about 394 back-links.
2. **Fix the 10-item cap without cutting any book.** Each book gets one visible row showing its strongest chapter, and its other chapters go in a `<details>` "More from this book". The JSON-LD `citation` list is uncapped.
3. **Update the 121 book links to the final addresses**, using the `_redirects` map. This only changes links in the generated book pages, never book wording (owner rule). It saves a redirect hop for readers and passes link value directly.

## B. Search and AI findability
1. **"Part of these patterns" on single tactics.** For example, each part of Gaslighting links back up to the Gaslighting page. This sends internal links to the most-searched pages (Gaslighting, DARVO, FOG, Trauma Bonding).
2. **Shorter titles.** Where the name is long, drop ": Signs, Examples and What to Do" and keep "<Tactic> · Pattern Decoder" when the full title would go over about 65 characters. This fixes 153 titles.
3. **A real `lastmod`.** Use a hash of each page's content, and only change the date when the page actually changes. Store the hashes in a small JSON file in `design/`.
4. **A fuller llms.txt, plus a new llms-full.txt.**
   - llms.txt: list every tactic and pattern as a link with its one-line definition. That's 367 lines, the format AI crawlers read best.
   - llms-full.txt: the plain short answer, signs and safety note for each entry.

   Fix the hub llms.txt count at the same time.
5. **JSON-LD additions:**
   - `isPartOf` from each tactic to the pattern terms it belongs to
   - `subjectOf` pointing to the book chapters
   - `dateModified` per page, taken from B3
   - each tactic's "What is X?" answer and its "Signs it might be this" list as `FAQPage`. This is text already on the page, so it's allowed.
6. **A 404 page** for the Decoder, with search, links to every tactic and the patterns, and the safety line. It catches old or mistyped links.
7. **IndexNow ping** after the deploy, for the changed URLs only, using `scripts/seo/indexnow.py`. Google Search Console submission still needs the owner's account.
8. **Social share cards (optional, larger).** One card per tactic, showing the tactic name on the Decoder card design (`scripts/make-decoder-og.js`). Facebook is the top referrer at about 310 visits, and 87% of visitors are on phones. This adds about 367 small images to the deploy and no weight to the pages.

## C. References to other works
1. **"Research behind this" on the matching entries**, using only sources already verified in The Long After's appendix (DOIs in `content/longafter-v2/dois.json`). Examples:
   - Gaslighting: Sweet 2019 and Stern 2007
   - DARVO: Freyd 1997 and Harsey & Freyd 2020
   - Trauma Bonding: Dutton & Painter 1981 and 1993, Carnes 1997
   - Intermittent reinforcement: Ferster & Skinner 1957
   - Coercive control: Stark 2007
   - Economic abuse: Adams 2008 and Postmus 2012
   - Litigation abuse: Miller & Smolter 2011 and Gutowski & Goodman 2023
   - Post-separation abuse: Spearman 2023
   - Stalking: Logan & Walker 2017

   This is new text on the Decoder (sources only, no rewording), so it needs the owner's yes. It is a strong signal for AI answers that cite sources.
2. **A help link on sensitive pages.** The "Safety first" box links to The Long After's *If you're not safe right now* page, which lists helplines by country and tap-to-call numbers. Today the box only says "contact emergency services".
3. **Long After A to Z → Decoder.** Each glossary term that has a Decoder page links to it (65 entries, an estimated 25 to 30 matches). The Long After isn't deployed yet, so this goes out with its deploy at no extra cost.
4. **Topics hub.** Regenerate `hub/topics.html` so each topic lists the Decoder page together with the chapters from all 13 books.

## D. Checked and not recommended
- **Inline source links inside definitions.** They interrupt reading, which is what the owner wanted to avoid. Keep sources in their own section at the end, as in the books.
- **AI-written new text for Decoder entries.** v20's "It can sound like" lines are still awaiting the owner's skim, so don't add more.
- **Any change to tactic names or wording.** That's the owner's rule.

## Order of work (one session)
1. Check live against the repo first (`verify-deployed playbook`).
2. Make the A, B and C changes in `decoder_v20.py`, `decoder_pages.py` and the book builds.
3. Rebuild with `design/build-decoder-v15.py`.
4. Run the checks: `scripts/decoder-verify.js` (109 checks), every old address resolves, axe, speed, and screenshots at 375 and 1440.
5. Version bump to v21, plus the changelog in `sites.json` and the on-page note.
6. Deploy together, on the owner's words: the Decoder, the five books (plus the four with updated links if the owner wants them redeployed), the hub (llms.txt, topics), and The Long After.
7. Ping IndexNow.
