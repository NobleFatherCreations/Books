# Work packet 03 — Tag resolution, the model step (ENT)

**For:** a research model starting cold (web search and fetch required). **Repo:** `/home/user/Books`. Do not commit, push or deploy. Do not edit anything under `content/fractal/ent/source/`.

## Goal

Give every pending item in `content/fractal/ent/resolution/ledger.json` a verdict under `content/fractal2/TAG-POLICY.md`, backed where needed by a real, fetched source in `content/fractal/ent/resolution/facts.json`. When you finish, `python3 design/fractal-sector/resolve.py ent check --final` must pass.

## Read first

1. `content/fractal2/TAG-POLICY.md` (the rules; follow them exactly, including "never fabricate a source").
2. `design/fractal-sector/resolve.py` (the ledger format; `check` tells you what is still wrong).
3. `content/fractal/ent/resolution/todo.jsonl`: 504 items, one JSON object per line, each with `q` (its index in the ledger), `task`, `combo_id`, `section`, `before` (the text concerned). Tasks: `research` (84), `overstatement` (141), `confirm-covered` (141), `sector-accuracy` (128), `confirm-note` (10).
4. The script for any item you are unsure about: `content/fractal/ent/source/scripts/ENT_<combo_id>_*.md`, or the parsed sections in `content/fractal/ent/build/sector.json` (`combos[].sections`).

## How to work (in this order)

**A. Topics first (policy §7).** Read all `research` and `sector-accuracy` items. Cluster them into 40 to 70 topics (examples: recoupment and cross-collateralization; approval rights over name and image; "commercially satisfactory" delivery standards; work-for-hire and session releases; NDAs and confidentiality in settlements; minors' earnings, work permits and chaperones; royalty audit rights and objection windows; chart rules on bundles and bulk purchases; payola and promotional incentives; streaming manipulation and purchased streams; impersonation of scouts and A&R; long-running online investment fraud; merch fees taken by venues; touring crew hours and fatigue; residuals and union claim procedures; platform metadata and genre fields; data migration between services; reward and notification design in apps). Write the topic list to `content/fractal/ent/resolution/topics.json` before researching: `[{"id":"F001","topic":"…","items":[q,…]}]`.

**B. Research each topic.** At least three distinct searches and two pages actually opened per topic. Prefer regulators, courts, unions and guilds, collecting societies, chart and standards bodies, platform documentation, consumer-protection agencies, and established trade or national press. Write `facts.json` entries exactly as in policy §7. Quotes are at most 25 words and must appear on the page you fetched. If nothing reliable is found, record the topic with `"sources": []` and `"confidence": "none"`. Do not cite a page about a named individual's dispute.

**C. Decide verdicts and write them into `ledger.json`** (edit the entry whose `q` matches; set `verdict`, `fact`, `after` when rewording, `reason`, `risk`, and `"by": "model"`). Keep `before` exactly as it is in the script; for an `overstatement` rewrite, set `before` to the exact sentence or phrase in the script section that changes, set `patch_section` to that section's name, and `after` to the replacement. Several rewrites from one audit note go in `"patches": [{"section","before","after"}]`.
- `research`: policy §2. 
- `sector-accuracy`: policy §6. One verdict per audit item; in `reason`, give one line per lettered point (which are scene details, which map to which fact id).
- `overstatement`: policy §4. Use the author's own suggested softer wording, exactly. Rewrites only in explanatory sections; never in the scene (Cold Open, The Name); never in a protected section.
- `confirm-covered`: policy §5. Compare the note with `false_positive_check` in the todo item. `no-change` when the same distinguishing test is there in substance; otherwise `escalate` with the missing sentence quoted.
- `confirm-note`: read the audit note. If it says no such claim is made or none is needed → `no-change`. If it says a tag was applied that is not in the script → `escalate`.

**D. Run** `python3 design/fractal-sector/resolve.py ent check --final` and fix what it reports, then `python3 design/fractal-sector/resolve.py ent summary`.

Work in batches of about 40 ledger entries and save `ledger.json` and `facts.json` after each batch, so nothing is lost if you are interrupted. If you are interrupted and resumed, continue from the entries still `"by": "pending"`.

## Done when

- `check --final` passes with 0 problems.
- `facts.json` has every topic, each with complete citation records or an honest `"confidence": "none"`.
- Your final message reports: counts by verdict; every `escalate` with its q number and why; every `remove`; every topic with no source; the ten changes you consider riskiest; and anything in the policy you had to interpret.

## Escalate (verdict `escalate`, do not guess) when

Policy §8 applies; a source contradicts a script; a real organization or person turns up in a script; you are unsure between two verdicts.
