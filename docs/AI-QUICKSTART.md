# AI quickstart (read this first; ~1 minute)

Repo `NobleFatherCreations/Books`, branch `claude/fervent-cori-gu2uzi`. Rules: `CLAUDE.md`. History: end of `MEMORY.md`.

## State (2026-11-09)
- LIVE + verified: homepage v17 (deploy 6af1238b), robots.txt, sitemaps, llms.txt, /topics, IndexNow key;
  seven round-1 books (The Sacred Divide, Playground Protectors, Sovereign Divine Feminine, The Fractal, The Fracture,
  The Festie Codex, The Festie Bible) with 530 plain chapter pages.
- NOT live: The Weighing (pending on purpose; ask before deploying). Round 2 books not started.
- Parked: The Pattern Decoder (owner has their own update coming).
- Owner-only: Search Console + Bing verification by DNS, sitemap submission (`docs/OFFSITE-PLAN.md`).

## Short commands (what each phrase means)
| Owner says | Do |
|---|---|
| "check" | `node scripts/verify-deployed.mjs` (live = repo?) then `python3 scripts/seo/verify_seo.py fracture feminine children wook fractal festival faith` |
| "rebuild" | `for b in fracture feminine children wook fractal festival faith; do python3 scripts/seo/build_$b.py; done; python3 scripts/seo/build_hub.py; python3 scripts/seo/build_site.py` |
| "test homepage" | `python3 scripts/seo/serve.py 8765 &` then `node scripts/verify-hub.mjs http://127.0.0.1:8765/`, `node scripts/seo/a11y.js http://127.0.0.1:8765/`, `node scripts/seo/perf.js http://127.0.0.1:8765/` |
| "deploy <book>" | Netlify MCP deploy-site with the siteId in `sites.json`, run from a folder holding EVERYTHING that site serves (a deploy replaces the whole site); then `verify-deployed.mjs <book>`; then bump `sites.json` lastDeploy |
| "ping" | `python3 scripts/seo/indexnow.py hub fracture feminine children wook fractal festival faith` (only after a verified deploy) |

## Never
- Deploy anything the owner didn't name in this conversation. Never merge the Sacred Divide v5 branch whole.
- Change the books' own text. New words live only in `content/seo/<book>.json` (`plain`, `aka`).
- Add external scripts (only the Cloudflare beacon is allowed), analytics with cookies, or Decoder links on the kids' book.
- Name living people in Fracture titles/summaries. Run `playwright install`.
- Send outreach automatically (drafts only; owner sends).
