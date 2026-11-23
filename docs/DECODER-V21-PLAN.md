# Pattern Decoder v21: revised plan (2026-11-23, nothing built)

This revises the 2026-11-22 proposal after the owner shared an outside review. It keeps what holds up and corrects what the review got wrong against our own data. It adds two big wins the review missed, both found by checking the built pages against the source data.

## What the outside review got right (kept)
- Approve everything, including C1 (sources) and the share cards.
- Redeploy the four books whose links now point straight at the current pages.
- Name the AI file `llms-full.txt`.
- Titles: drop the brand suffix first and keep the search phrase.
- Links sideways between tactics, not only up to patterns.
- A short answer plus key signs at the top of each page.
- A methodology page and a real clinical reviewer as the main trust signals.
- A visible "last updated" on each page.
- New tactics wait for v22.

## What it got wrong (checked against the repo)
| Claim | What is actually true |
|---|---|
| "Add a Quick Exit button" | Every Decoder page already has a Leave button and "press Escape twice". The Long After's help page has its own Leave button. Nothing to add. |
| "Build a guided triage flow, a compare tool, a save feature, printable cards" | The app already has a two-question helper (`#/help`), Compare look-alikes, opt-in Save, and a one-page printable station card. The real gap is that none of these exist as crawlable pages. |
| "A private local pattern log" | This conflicts with the privacy stance. Saving is already opt-in and limited to one scrambled entry. Don't widen it. |
| FAQPage schema "feeds featured snippets" | Since 2023, Google shows FAQ rich results only for government and health sites. Add it anyway because it's cheap and AI tools read it, but expect no visible change in Google. |
| "Swap primary titles to the more searched name" | This breaks the owner's rule: never change names. More searched names go into "Also called" and search only. |
| The 335-tactic researcher map | Several entries are wrong or would mislead if shown as "research": |

Problems in that researcher map:
- **Forced Teaming** is Gavin de Becker's term (*The Gift of Fear*), not Joe Navarro's.
- **Pacing and Leading** is cited to NLP, which has no research support. Showing it under "Research behind this" would lend false credibility.
- **Legal abuse** is cited to "Elizabeth Topliffe". I could not identify this source.
- **Kafka trapping** comes from a blog post, not research.
- **Idealize, devalue, discard** is attributed to Kernberg and Kohut. That's a stretch: the cycle is a popular term, not their construct.
- Most lines name a famous theorist rather than a specific work that discusses the tactic.

The verification rules in C1 below exist because of these problems.

Problems in the alias list:
- **"Parental Alienation" as another name for Children as Leverage.** This is dangerous. The Long After explains how that label is used against people reporting abuse.
- **"Benevolent sexism" for Concern Trolling** is a different concept.
- **"Bystander effect" for Diffusion of Responsibility** is a related idea, not the same thing.
- **"Emotional incest" for Parentification** is a separate concept.
- **"Schrödinger's Douchebag"** is slang and doesn't belong.

So every alias gets a check: same thing, not just related. Related concepts become links, not aliases.

## Two big wins the review missed

### 1. The crawlable pages hide 9 of the 21 fields
Search engines and AI tools see only the plain pages, because the app is JavaScript. Those pages leave out nine fields that the app shows:
- what it is not
- innocent or ordinary possibilities
- common false positives
- more concerning if
- signs of a pattern over time
- repair check
- boundary respect check
- psychological mechanism
- possible impact on the person

Showing them adds no new writing. It's the fairest and deepest material we have, and it's exactly the "restraint" the review calls our main trust signal.

How to show them:
- **Shown openly**, because they're about reading the situation fairly: what it is not, innocent possibilities, false positives, more concerning if, pattern over time.
- **In open-on-tap sections**, to keep pages readable on a phone: mechanism, impact, repair check, boundary respect check.

### 2. The combo data already supports sideways links
The 109 combos (the build's `recipes`) list which tactics happen together and in what order. A data-driven "Often used together" block, and a "What often comes next" block where the combo has an order, needs no new writing and no guessing.

## v21: one build, one deploy

### A. Back-links
1. Add longafter, silence, atwill, repair and slowtake to `BOOKS`. That's about 394 new links.
2. Show one row per book with its best chapter, and the rest under "More from this book". The JSON-LD citation list is uncapped.
3. Point the 121 old-address links in the books straight at the current pages (connector links only). Redeploy fractal, feminine, wook, festival and fracture with them.

### B. Findability, using only text we already have
1. **Show the 9 hidden fields** on the plain pages (win 1).
2. **Answer box at the top:** the existing two-sentence summary, the top 3 "Signs it might be this" and the "It can sound like" lines, within the first screen.
3. **Up and sideways links:**
   - "Part of these patterns" on each tactic
   - "Often used together" and "What often comes next", built from the combos
4. **Titles in tiers:**
   - "<Tactic>: Signs, Examples and What to Do" when it fits in 60 characters
   - otherwise "<Tactic>: Signs and What to Do"
   - otherwise "<Tactic>"

   The brand suffix is dropped first, since Google shows the site name anyway.
5. **Real dates:**
   - the sitemap `lastmod` only changes when a page's content changes (content hash stored in `design/`)
   - a visible "Last updated" date on every page
   - `dateModified` in the structured data
6. **AI files at `/playbook/`:**
   - `llms.txt` lists all 367 entries, each with its one-line definition
   - `llms-full.txt` holds each entry's answer, signs both ways and safety note
   - the count in the hub's llms.txt is fixed

   No per-page `.md` copies: the pages already wrap the entry in `<article>`, and llms-full.txt covers it.
7. **Structured data:**
   - `DefinedTerm`, already in place, gains `isPartOf` its patterns and `subjectOf` the book chapters
   - `FAQPage` built from the "What is X?" answer, the signs and what you can do
8. **A 404 page** with search, every tactic, the patterns and the safety line.
9. **Share cards:**
   - one 1200×630 card per entry, made by the existing `scripts/make-decoder-og.js` (Playwright, already here)
   - each card shows the name, the line colour, the code and a definition of up to 120 characters
   - cards are regenerated only when their entry changes, and checked at 300px wide
   - a "Save this card" link on each page
10. **IndexNow** after the deploy, for changed URLs only.

### C. References to other works
1. **"Research behind this", in its own section at the end.** It shows only:
   - (a) sources already verified in The Long After (40 DOIs), and
   - (b) further sources verified the same way: the work exists (Crossref or a publisher ISBN record), its year and authors match, and it actually discusses this concept.

   Each source gets one of three labels: **Research**, **Where the name comes from**, or **Popular book**. Entries where nothing is found say so plainly, like the existing Pocketing note ("no peer-reviewed research was found"). NLP and blog-only origins never appear as research. The build reports how many entries are cited and which were left uncited.
2. **"Also called" additions.** A vetted list from the review's alias table, each checked as the same thing (for example "thought-terminating cliché", "reactive abuse", "tu quoque", "constructive dismissal", "floodlighting"). These feed search, `alternateName` and the "Also called" line. The owner skims the list before the build.
3. **The "Safety first" box** links to The Long After's *If you're not safe right now* page (helplines by country, tap to call).
4. **The Long After's A to Z** links to Decoder pages (about 25 to 30 terms).
5. **The Topics page** is rebuilt so each topic shows the Decoder page alongside chapters from all 13 books.

### D. Trust page
1. **`/playbook/about-this-guide`.** It covers:
   - how entries are built
   - why every entry carries innocent possibilities, false positives and a misuse warning
   - how sources are chosen and labelled
   - versions and the licence
   - "a reading aid, not a diagnosis"

   It needs two owner answers: how the entries were made (this is the open AI-use disclosure decision) and whether a reviewer is named. No review badge until a review has actually happened.
2. **A reviewer checklist** (`docs/DECODER-REVIEW-CHECKLIST.md`) for a licensed psychologist, about 30 minutes. It starts with the items already flagged as needing clinical sign-off:
   - the medical symptom lists (Clinical Tone Policing, Medical Gaslighting, False Conclusion from Normal Labs)
   - the safeguarding notes (The Exception Script, Stalking)
   - the 10 child-related entries without a help route
   - then the pages with a "Safety first" box

### Checks, then deploy on the owner's words
1. Run `verify-deployed playbook` first, to make sure live matches the repo.
2. Run `decoder-verify.js` (109 checks), check every old address, then axe, speed, and screenshots at 375 and 1440 (including a long page with the new sections and the 404).
3. Version v21, with the `sites.json` changelog and the on-page note.
4. Deploy together: the Decoder, the 5 back-linked books, the 5 books with updated links, the hub (llms.txt, topics) and The Long After.
5. Ping IndexNow.

## v22, after v21 is live
- **New tactics.** First compare the 45 suggestions against the existing 335 entries and their aliases; many are already there (Confirmshaming, Roach Motel, Tu quoque or Whataboutism, Fait accompli or Moving in Silence). Only the real gaps get entries, and their wording needs the owner's approval.
- **Comparison pages** for the most confused pairs, built from each entry's existing "How it differs from look-alikes" text: Gaslighting or lying, Stonewalling or silent treatment, Boundary or ultimatum, Trauma bond or codependency, DARVO or defensiveness.
- **Arena hubs** (relationships, work, groups and faith, courts, online), built from the existing `w` tags and lines.
- **"How it feels" entry pages** ("I feel like I'm walking on eggshells"). These need new writing, so they go to the owner.

## After deploy (owner's accounts and decisions)
- **Google Search Console and Bing Webmaster Tools:** verify the site and submit both sitemaps.
- **Clinical review**, using the checklist. The reviewer's views are their own, never their employer's.
- **Dataset with a DOI** (Zenodo or OSF). The licence is CC BY-NC-ND, so the owner decides whether to release the dataset under that licence or a looser one.
- **Outreach** to VAWnet, NNEDV Safety Net, the state coalition and ICSA. I draft, the owner sends (CLAUDE.md: never auto-send).
