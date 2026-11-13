# Prompt: build one full system memory of the whole repo

Purpose: stop things being missed. One run creates a layered memory that any new chat can read in minutes: a short map, a per-section digest, and a machine-readable index, each claim tied to a file path. Paste the block below into a new Claude Code session in the Books repo (branch `claude/optimistic-clarke-86s6bg`). Expect it to take several turns; it is built to be resumable.

Recommended models: **Sonnet for passes 1-2** (reading and digesting, the bulk of the tokens), **the strongest model only for pass 3** (synthesis and the cross-links), Sonnet again for 4-5. Per `CLAUDE.md`, dispatch at most one helper agent at a time, and none unless you want speed.

```
You are building the SYSTEM MEMORY for this repository: one layered, verified, resumable record of everything in it, so no future session misses anything. Work on branch claude/optimistic-clarke-86s6bg. Do not deploy anything. Do not change any live-site source file; you write only under docs/memory/ and the files named in pass 5.

FIRST REPLY (before any work): restate this task in three lines; list every skill and MCP server you will use (expected: none except Bash/Read/Grep/Write; ask before using anything else) and your token plan; list the sections you will cover and the ones you will skip on purpose, with the reason. Wait for my "go" only if something in the scope is ambiguous; otherwise continue.

RULES
1. Evidence only. Every statement in the memory carries a file path (and line or heading when you can). If you did not open it or grep it, write "UNVERIFIED". Never invent a version, URL, count, owner decision, or quote. Unknown is a valid answer; write "UNKNOWN: <what would settle it>".
2. Read cheaply. Use `git ls-files`, `ls`, `wc`, `head -40`, headings (`grep -n '^#'`), and targeted greps. Do not read whole large files. Never read inside `tools/`, `references/`, `exports/`, `logs/`, `node_modules/` beyond one `ls` and a one-line purpose from its README.
3. Registry versus repo. `sites.json` is the project registry. For every project, compare registry fields (version, repoPath, URL, changelog) with the repo (does the path exist, does the on-page version match). Record every mismatch; do not fix it.
4. Owner decisions are sacred. Anything marked locked, approved, declined, "never", or "binding" in CLAUDE.md, MEMORY.md, BOOKS.md, docs/, or content/*/DECISIONS.md goes into a DECISIONS table verbatim with its source.
5. Failures count. Read content/fractal2/design/FAILURE-LOG.md and content/fractal2/design/REGRESSIONS.md. Every recurring failure becomes a rule in the memory's "Do not" section, with its check if one exists.
6. Be resumable. Write a progress file docs/memory/_progress.json after each section (section, status, files read, date). If it exists, continue from it; do not redo finished sections.

PASS 0: MAP (about 10 minutes of work)
- `git ls-files | cut -d/ -f1-2 | sort | uniq -c | sort -rn` and `git log --oneline | wc -l`, `git branch -r`.
- Write docs/memory/00-map.md: every top-level directory and second-level directory with file count, one-line purpose (from README/CLAUDE.md/BOOKS.md), and whether it is a SOURCE (hand-edited), GENERATED (output of a script), VENDORED (copied from elsewhere), or LIVE (deployed byte-for-byte). For each GENERATED directory, name the generating script. For each LIVE directory, name the live URL and Netlify site id from sites.json.

PASS 1: SECTION DIGESTS (one file each, docs/memory/NN-<section>.md, 250-450 words, this exact schema)
Sections, in this order: library/ (one digest per book directory, grouped, with the book's design stance from BOOKS.md), workshop/, instruments/ (playbook, shadowroot, music), hub/, other/, content/, design/, scripts/, docs/, brand/, .claude/ (skills, agents, settings), root files (CLAUDE.md, MEMORY.md, BOOKS.md, sites.json, chapters.json, Makefile-like files).
Schema for each digest:
  WHAT IT IS (2 lines) · SOURCE OF TRUTH (path) · BUILD (exact command) · OUTPUT (path) · DEPLOY (exact method, site id, who may approve) · LIVE URL + version (from sites.json) · STATE (done / in progress / not started) · LOCKED DECISIONS (with source) · OPEN ITEMS (with source) · KNOWN DEFECTS (with source) · DO NOT (rules that apply here) · KEY FILES (max 8, each with one line) · UNVERIFIED (what you could not confirm).
For the Fractal family (library/fractal, library/fractal2, design/fractal2, design/fractal-sector, content/fractal2, instruments/playbook, library/children), make one digest each plus a combined FRACTAL index that reconciles: Fractal (30x30x3, 26 of 30 sectors published), Pattern Decoder (310 entries), Fractal² (300+ tactics, 150+ combinations per sector; finished sectors), Playground Protectors, Sacred Divide, the intro site, the explainer PDFs.

PASS 2: CROSS-LINKS (docs/memory/90-links.md)
- Dependency graph as a table: script -> reads -> writes -> deployed as. Find every place one section's output is another's input (e.g. content/*.json feeding site generators, shared CSS, shared fonts, the hub redirects feeding every project URL).
- Duplicates: files that exist in two places (repo vs library/_undeployed vs live), and which copy is canonical.
- The hub: noblefathercreations.com proxy rules (hub/catalogue-redesign._redirects) mapped to each project's Netlify site.
- Mismatches from rule 3.
- Other repos and branches: list remote branches with what is unique on each (git rev-list --count, merge-base). Do not push or merge anything.

PASS 3: SYNTHESIS (strongest model; docs/SYSTEM-MEMORY.md, at most 3,000 words)
Sections: 1) What this system is, in 10 lines. 2) The map: one table of every project (name, kind, source path, live URL, version, state, next action). 3) How things connect (from pass 2, as a short diagram in text). 4) Locked decisions (table). 5) Open items ranked by owner impact. 6) Known defects. 7) DO NOT (every recurring failure as a rule). 8) Cheap-start guide: for each common task ("work on the intro site", "edit a book", "rebuild the PDFs", "deploy the hub") the three files to read and the one command to run. 9) What is not in this memory and why. Also write docs/memory/system-memory.json (same facts, machine-readable: projects[], decisions[], openItems[], defects[], links[], with a "source" field on every item and "verified": true/false).

PASS 4: VERIFY
- Pick 25 claims at random from SYSTEM-MEMORY.md (at least 5 numbers, 5 URLs or versions, 5 decisions, 5 build commands, 5 file paths). Re-check each against the files. Write the result in docs/memory/_verification.md as a table: claim, source, result, fix. Fix every wrong claim in the memory (not in the source files). If more than 3 of 25 fail, repeat pass 1 for the sections they came from.
- Run a coverage check: every top-level directory from pass 0 appears in a digest or in "What is not in this memory." List gaps.

PASS 5: WIRE IT IN AND KEEP IT FRESH
- Add one line to CLAUDE.md after the existing digest pointer: "Whole-repo memory: docs/SYSTEM-MEMORY.md (read first); per-section digests in docs/memory/."
- Add a MEMORY.md entry with the date, the commit, and the verification score.
- Write scripts/memory-check.py: exits non-zero if (a) any project in sites.json is missing from system-memory.json, (b) a registry version differs from the memory, (c) a path named in the memory no longer exists, (d) docs/memory/_progress.json is older than the newest commit touching a covered section. Run it and report.
- Stamp every digest with `source_commit: <git rev-parse --short HEAD>` and `last_verified: <date>`.

FINAL REPLY: a table with one row per section: covered / skipped, files read, claims verified, claims marked UNVERIFIED, and what you need from me. List every mismatch and every decision you found that conflicts with another. Commit with a clear message and push to claude/optimistic-clarke-86s6bg only.
```

## How to keep it from going stale

- Run `python3 scripts/memory-check.py` at the start of any session (it is cheap). If it fails, re-run only the passes for the sections it names.
- After any real piece of work (a deploy, a new sector, a book revision), update that section's digest and the matching line in `system-memory.json`. One paragraph is enough.
- Re-run pass 4 monthly, or after any large merge.
