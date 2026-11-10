# AI quickstart (read this first; ~2 minutes)

Repo `NobleFatherCreations/Books`, branch `claude/fervent-cori-gu2uzi`. Rules: `CLAUDE.md`. History: end of `MEMORY.md`.
Owner: Shae Stovell ("Dapper Dad"). Plain, direct answers; give exact click-by-click steps when they must do something.

## State (end of 2026-11-09)
- **LIVE + verified (live = repo):**
  - Homepage v17 (deploy 6af1238b): design-skills polish, Start here chooser, all books first, 0.19 MB.
    Also robots.txt (9 sitemaps), root sitemap, llms.txt, /topics, og.png, IndexNow key file.
  - Seven round-1 books, 530 plain chapter pages, findability layer: The Sacred Divide (/faith), Playground Protectors
    (/children), The Sovereign Divine Feminine (/feminine), The Fractal, The Fracture, The Festie Codex (/wook),
    The Festie Bible (/festival).
  - **Pattern Decoder v20** (/playbook, deploy 6af18f94): 335 standard tactics (110 new) + 32 patterns (Gaslighting,
    DARVO, FOG, Trauma Bonding...) kept at their old addresses; 103 old addresses 301 to new names; /playbook/patterns;
    stage + standard number; "Where this comes up in the books" on each tactic; licence + author; design polish.
- **Search:** Google Search Console verified (DNS TXT at SiteGround) + sitemap submitted; Bing Webmaster imported.
  IndexNow: use www.bing.com/indexnow (api.indexnow.org answers SiteVerificationNotCompleted). All URLs pinged.
- **NOT live:** The Weighing (ask first). Round 2 books not started.
- **Owner to check in ~1 week:** Search Console > Pages and Performance; send a screenshot.

## Owner rules learned this round (binding)
- NEVER change names or wording inside the books. The children's book and Festie Bible use their own audience
  language on purpose. Add connectors/links only; ask before touching any book writing. Do NOT run the book
  rebuild loop without a reason the owner agreed to (it regenerates pages; an interrupted run was reverted).
- Only deploy what the owner names in the current conversation.
- New writing lives only in `content/seo/<book>.json` (plain, aka) and needs owner approval.
- The SOVEREIGN framework (Spot, Orient, Validate, Establish the frame, Respond, Enforce, Invest, Ground, Navigate) is
  the core of the Feminine book. Idea pending owner yes: add it as defined terms on Feminine pages.

## Decoder v20: how it is built
`python3 design/build-decoder-v15.py` builds `instruments/playbook/site/` (app + 367 plain pages + sitemap + llms.txt +
`_redirects`). `design/decoder_v20.py` applies the owner's package (`content/decoder-v20/`) on top of v19 data; plain
page templates and CSS in `design/decoder_pages.py`; app in `design/decoder-v15/`. "It can sound like" lines for the
110 new tactics were drafted by AI in `content/decoder-v20/sounds_like.json` (owner may want to skim). Test suite:
`node scripts/decoder-verify.js instruments/playbook/site/index.html` (105/106; the section-tap check is a timing flake
that also misses on v19). Deploy = copy the whole site folder to a staging dir, Netlify MCP deploy-site, siteId in sites.json.

## Short commands
| Owner says | Do |
|---|---|
| "check" | `node scripts/verify-deployed.mjs` (live = repo?), then `python3 scripts/seo/verify_seo.py fracture feminine children wook fractal festival faith` |
| "test homepage" | `python3 scripts/seo/serve.py 8765 &` then `node scripts/verify-hub.mjs http://127.0.0.1:8765/`, `node scripts/seo/a11y.js http://127.0.0.1:8765/`, `node scripts/seo/perf.js http://127.0.0.1:8765/` |
| "test <book>" | serve.py, then `node scripts/seo/shoot.js <outdir> http://127.0.0.1:8765/<book>/<page>` and `node scripts/seo/a11y.js ...`; `python3 scripts/seo/fidelity.py <book> <original>` proves text unchanged |
| "deploy <thing>" | Netlify MCP deploy-site with the siteId in `sites.json`, from a folder holding EVERYTHING that site serves; then `verify-deployed.mjs <slug>`; bump `sites.json` lastDeploy |
| "ping" | `python3 scripts/seo/indexnow.py hub fracture feminine children wook fractal festival faith` (Bing endpoint) |

## Next, if the owner wants
1. Round 2 books (Loop, Weighing, Silence, At Will, Slow Take, Long After, Repair, Root) — same findability layer,
   discreet-mode toggle for safety books (owner decision), no wording changes.
2. SOVEREIGN defined terms on Feminine pages (needs yes + Feminine redeploy).
3. Short /topics summaries (new writing, needs approval). Outreach drafts (owner sends; never auto-send).

## Never
Add external scripts (only the Cloudflare beacon), cookie analytics, Decoder links in the kids' book, living people
named in Fracture titles/summaries; run `playwright install`; auto-send outreach; merge the Sacred Divide v5 branch whole.
