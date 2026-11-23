# START HERE: new chat, 2026-11-23 handoff

Paste the **opening prompt** below as the first message of the new chat. Everything it points to is in this folder or the repo.

**Repo:** `NobleFatherCreations/Books`. **Branch:** `claude/modest-keller-vgex1c`, or the new session's own branch. Commit and push there only. No PR unless asked.

---

## Opening prompt (copy and paste)

> Read `docs/handoff-2026-11-23/00-START-HERE.md` and follow it exactly. Then read, in this order:
> 1. `CLAUDE.md`
> 2. the last 40 lines of `MEMORY.md`
> 3. `docs/handoff-2026-11-23/02-PROBLEMS-AND-FIXES.md`
> 4. `docs/handoff-2026-11-23/03-STILL-TO-DO.md`
> 5. `docs/handoff-2026-11-23/04-LONGAFTER-FINISH-ORDER.md`
>
> Load the skills listed in section A of 00-START-HERE before any work. Then ask me the questions in 04 section 0, all in one message. Do not deploy anything unless I name the site in this chat.

---

## A. Skills and tools to load at the start (before touching anything)

Load each skill when its step starts. Read it in full the first time it's used. The new session's skill list is the source of truth: if a name below isn't listed, skip it and say so.

| When | Skill or tool | Why |
|---|---|---|
| Session start | `mcp__sequential-thinking__sequentialthinking` | Plan multi-step work before doing it (CLAUDE.md) |
| Writing passes | `no-ai-slop`, `copy-editing` | Every insert and rewrite. The owner's voice, not AI cadence. |
| Meso, rhythm and readability passes | `cognitive-design` | 2am overwhelm, chunking, anchors |
| Structure and links | `information-architecture`, `site-architecture` | Chapter arc, cross-book bridges, the About page placement |
| Findability | `seo-audit`, `ai-seo`, `schema` | GEO definitions, Person/Organization schema, llms.txt |
| Design phase only (after the content freeze) | `design-director` (the binding process), `impeccable`, `frontend-design`, `emil-design-eng`, `refactoring-ui`, `apple-design` | `docs/design-catalogue/13-html-books-playbook.md` is binding |
| Checks | `better-accessibility`, `web-accessibility`, `web-perf`, `webapp-testing`, `ux-heuristics` | axe, keyboard, reduced motion, phone-first |
| Code | `ponytail` | Simplest script that works. No new dependencies. |
| Facts | WebSearch (standard), `scripts/longafter-sources.py` | Every new claim gets a source or a "where this applies" |
| Deploy (only on the owner's words) | Netlify MCP `netlify-deploy-services-updater` (deploy-site) | See section C |

## B. Rules that caused trouble before (binding)
1. **"Deploy X" means only X.** If a change touches shared parts (the seal menu, the drawer, counts, cards), **list every affected site and ask about each one by name.** Never treat a sweep's site list as approved. See 02, incident 1.
2. **Never run a full book rebuild (`scripts/seo/build_<book>.py`) just to fix links.** It rewrites menus, fonts and share images, and an interrupted run deletes pages. Use the targeted sweeps (`scripts/decoder-relink.py`, `scripts/nf-catalogue-sweep.py`). See 02, incident 2.
3. **Never change the owner's wording inside a book** without asking. Add links and connectors only.
4. **No helplines in the owner's bio** (`content/about.md`). It's his story, not a resource page.
5. **No outside requests** except the Cloudflare beacon. Nothing stored on the reader's device. No tracking.
6. **Outreach is never sent automatically.** Drafts only. The owner presses Send.
7. **Never ask the owner to paste a key or password in chat.** Use the credential form or Netlify environment variables, which the owner sets himself.
8. **One background agent at a time.**
9. **Never run `playwright install`.**
10. **The owner's voice:** raw, first person, passionate, plain. Don't make it read "like it's supposed to be".

## C. Deploy recipe (only after the owner names the site)
1. Stage a copy of the site folder. Leave out `*.md`, `qa.js`, and `sectors/` for The Fractal.
2. Call the Netlify MCP deploy-site tool with that site's `siteId` from `sites.json`. Run the returned one-shot `npx … --proxy-path …` command from the staging folder.
3. Check that the live md5 matches the repo md5 for the key pages.
4. Run `python3 scripts/visit-counter.py --all` after any rebuild, so the beacon is back on every page.
5. Run IndexNow (`python3 scripts/seo/indexnow.py --live`). Record `lastDeploy` in `sites.json`. Write a MEMORY.md line.

**Homepage staging:**
- `hub/catalogue-redesign.html` becomes `index.html`.
- `hub/catalogue-redesign._redirects` becomes `_redirects`.
- Also copy: the IndexNow key txt, llms.txt, og.png, robots.txt, sitemap.xml, topics.html, netlify.toml, `f/`, `media/`, `netlify/`.
- Hub site ID: `58596923-a3a6-4f9e-9e9f-e934a1920aed`.

## D. Files in this pack
| File | What |
|---|---|
| 00-START-HERE.md | This page: the opening prompt, skills, rules, deploy recipe |
| 01-HISTORY.md | What happened, in order, with deploy IDs |
| 02-PROBLEMS-AND-FIXES.md | Every incident: what went wrong, why, the fix, the rule it created |
| 03-STILL-TO-DO.md | Open work and the owner's pending decisions |
| 04-LONGAFTER-FINISH-ORDER.md | The optimal order to finish The Long After, with every new idea folded in |
| 05-NEXT-BOOK-PLAN.md | The recommended next book (The Silence) and its full outline plan |
| 06-ABOUT-THE-AUTHOR-EVERYWHERE.md | How "Who made this" shows up on every page of every book |
| reference/ | Copies of the key docs: the Long After handoff, Book Pipeline v2, the process map, the origin story plan, the bio, the steelman, the submissions files |
