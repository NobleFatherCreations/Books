# History: what happened (2026-11-22 to 2026-11-23)

Newest last. Full detail is in `MEMORY.md` (search the date) and `git log`.

## 2026-11-22: The Long After, second edition
- **Written** in `content/longafter-v2/`. It started at 13 Markdown files, 96 pages and 47.6k words, all passing the audit.
- **Built** by `scripts/seo/build_longafter_v2.py` into `library/longafter/`.
  - The book is now static multi-page, with no JS app.
  - `/longafter/all` is the offline one-page edition.
- **Polish round:**
  - keyword research (Ubersuggest, Windsor Search Console)
  - 15 new sections
  - no-ai-slop and copy-editing passes
  - schema citations
  - on-page SEO script
  - tap-to-call numbers on the safety pages
  - one-command pipeline `bash scripts/longafter-pipeline.sh`
- **Owner's order: double the book.**
  - Two expansion passes took it from 55,682 to about 107,000 words.
  - Each chapter got a worked example and a "one thing to do" section.
  - 17 honest checks were added.
  - A to Z with 65 entries.
  - Sources appendix: 263 sources, 104 linked.
- **Audits passed:** voice, AI-writing v2, tone, steelman 2, facts, completeness.
- **Process map and retrospective:** `docs/LONGAFTER-PROCESS-MAP.md`.

## 2026-11-23: Decoder v21 and the deploy round
- **Decoder v21 plan** revised after the owner's outside review (`docs/DECODER-V21-PLAN.md`). Built:
  - back-links from 5 more books
  - all 21 fields shown on plain pages
  - verified research sources (69 sources)
  - vetted aliases
  - content-hash lastmod
  - full llms.txt and llms-full.txt
  - a 404 page
  - per-tactic share cards
  - the About page
  - reviewer checklist `docs/DECODER-REVIEW-CHECKLIST.md`
- **Deployed:**

| Site | Deploy ID | Note |
|---|---|---|
| Decoder v21 | 6b03b699 | |
| The Long After v5 | 6b03b6d1 | |
| Feminine | 6b03b6de | direct Decoder links |
| Festie Codex | 6b03b71f | direct Decoder links |
| Fractal | 6b03b736 | direct Decoder links |
| Fracture | 6b03b742 | direct Decoder links |
| Playground Protectors | 6b03b6ea | menu count only. **Beyond the owner's ask;** he OK'd it afterwards. |

- **The owner stopped the deploy** before The Sacred Divide, Festie Bible, Silence and the rest. See 02, incident 1.
- **Homepage deployed** (6b03b97d, byte-identical).

## 2026-11-23: indexing everywhere
- **IndexNow** `--live`: 1,412 URLs sent to api.indexnow.org, Bing and Yandex.
- **Wayback Machine:** 42 key pages saved.
- **Google Search Console:** already verified. The owner submitted all 16 sitemaps, read with Success.
- **Bing Webmaster:** the owner imported the site. All 16 sitemaps in, 4.2K URLs received.
- **Tracker** `docs/SUBMISSIONS.md`. **Paste-ready packets** `docs/SUBMISSION-PACKETS.md`.
- **Four Gmail drafts** for the owner to review and send: NNEDV Safety Net, ICSA, Center for Institutional Courage, DomesticShelters.org.
- **Decoder dataset export** for Zenodo: `content/decoder-v21/export/`.

## 2026-11-23: share cards on brand
- **Brand master:** `design/brand/noble-father-header.png`, the owner's lettering plus the hatted figure holding the NFC chip, with the lapis gem and the geometry circle.
- **Card design:** the whole header as background (`card-bg-1200x630.jpg`), lettering faded on the left under a veil in each card's colour, figure in full colour on the right.
- **Where the template lives:** `seo_common.make_og` (books and hub), `scripts/make-decoder-og.js`, `scripts/make-decoder-cards.js` (367 Decoder cards), `build_longafter_v2.py --og`.
- **Deployed with the new cards:**

| Site | Deploy ID |
|---|---|
| Playbook | 6b03cf36 |
| The Long After | 6b03cf48 |
| Hub | 6b03cdef |

## 2026-11-23: "Who made this" (the owner's bio)
- **Plan:** `docs/ORIGIN-STORY-PLAN.md`.
- **Bio:** `content/about.md`, version 5 plus additions. The owner's raw voice:
  - hooks for empaths and people in it
  - **no helplines** (the owner's order)
- **Three-reader steelman:** `docs/ABOUT-STEELMAN.md` (brand-trust psychologist, distrustful reader in the thick of it, DV advocate).
- **Added at the owner's request:**
  - "This won't read like any psychology book you've seen"
  - a pride passage and "people I'll never meet"
  - closing "My only ask" (share it on), plus "bonus points if you tell me how it helped you 🌹"
- **Wordmark** extracted from the header: `design/brand/wordmark-white.png` and `wordmark-dark.png`. Use these. Never imitate the lettering with a font.
- **Not built yet:** the `/about` page, the colophon lines, the schema, and the feedback box. See 03 and 06.
