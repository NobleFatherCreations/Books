# Fractal² — credibility tag resolution policy (v1, 2026-11-10)

**Purpose.** Every item in a sector's `review_queue.json` gets a recorded verdict, so the owner never has to verify examples by hand. The author's files are never edited. All changes live in a derived layer and are logged in a ledger. This policy is written so a model starting cold can apply it, and so the same process runs for every future sector.

## 0. What is in the queue (ENT: 1,370 items)

| Kind | Count | What it is | Default handling |
|---|---|---|---|
| `composite` | 191 | A scene or example marked as made up | **Keep the label.** No research. |
| `pattern` | 228 | "Common industry pattern": a general practice, hedged | **Keep the label.** No research, unless the sentence states a number, a law, a date or a named body (then treat as `source`). |
| `legal` | 301 | "Varies by place" | **Keep the label.** Never turn it into a statement of what the law is. |
| `review` | 82 | "Requires subject-matter review" | **Resolve** (section 2). |
| `source` | 17 | "Verified source needed" / "Historical example to verify" | **Resolve** (section 2). |
| `audit` · Claims needing verification | 141 | The author's own note listing what was tagged in that script | Check against the script (section 3). |
| `audit` · Overstatement risks | 141 | The author's own note of lines that may claim too much, usually with a softer wording | Decide per line (section 4). |
| `audit` · Overapplication risks | 141 | The author's own note on how the pattern could be misread onto innocent situations | Check it is covered on the page (section 5). |
| `audit` · Sector accuracy check | 128 | A list of things "a sector insider should verify" | Resolve the terms and practices (section 6). |

## 1. Verdicts (the only allowed values)

| Verdict | Meaning | Reader sees |
|---|---|---|
| `keep-label` | Descriptive label stays as written | Composite / Common pattern / Varies by place |
| `keep-conditional` | The sentence makes no factual claim; it says an outcome *depends on* stated conditions, or sends the reader to a qualified person | Label **Depends on the terms** (or **Ask a qualified person** for health, legal or safety routing) |
| `keep-cited` | The claim was checked and a real source supports it as worded | Label **Source checked**, linked to the page's source list |
| `generalize` | A specific claim could not be supported as worded; replaced by the general statement the sources do support | Reworded sentence, label **Source checked** if cited, otherwise **Common pattern** |
| `soften` | Wording implied intent, certainty or universality the text cannot show; replaced by the softer wording | Reworded sentence, no new label |
| `remove` | The claim is false or cannot be supported in any form, and the section still makes sense without it | Sentence gone; ledger keeps it |
| `surface` | The author's own audit note contains a safety line or an over-reading test that the page lacks; that sentence is added, word for word, to the named section (director's decision only; always high risk) | The added sentence |
| `no-change` | An audit note that needs no change to the page (already handled, or advisory to the author) | Nothing |
| `escalate` | Needs the directing session's judgment (section 8) | Nothing until decided |

There is no "expert reviewed" verdict. Nothing in this process claims a human industry expert has read the page.

## 2. Resolving `review` and `source` items

For each item, read the full sentence in its script (`content/fractal/<s>/source/scripts/…`), not only the queue excerpt. A queue entry whose text is only a bare tag belongs to the sentence or list item it sits on in the script: find it.

1. **Is it conditional or a routing line?** "Whether X is fair or exit-blocking depends on …", "… is a question for qualified counsel", "… are matters for qualified review", "seek a second perspective from an independent adviser". → `keep-conditional`. No research.
2. **Is it a hedged general statement about practice** ("can", "may", "often") with no number, law, date or named body? Research it once at the **topic** level (section 7). If a reliable source describes the practice → `keep-cited` with that fact id. If sources describe something narrower → `generalize`. If nothing reliable describes it → `soften` to an explicitly conditional form ("Where an agreement …, it can …") or `remove`.
3. **Does it state something checkable** (a rule, a chart-methodology change, how a platform works, a category of fraud)? It must be `keep-cited`, `generalize` or `remove`. Never leave it as written without a source.

**Sources that count.** Regulators and courts; statutes; unions, guilds and collecting societies; standards and chart bodies; platform documentation; established trade and national press; academic or industry-body reports; consumer-protection agencies. **Sources that do not count:** forums, anonymous posts, AI-generated text, content farms, marketing pages making claims about themselves, Wikipedia (use it only to find a primary source).

**A citation record must have:** URL, title, publisher, date published if shown, date accessed, and a quote of at most 25 words that supports the claim. The researcher must have fetched the page in this run. **Never fabricate or reconstruct a source.** If the page could not be opened, it is not a source.

**Patterns, never people.** Do not cite a source whose subject is a named individual's dispute if that would put the name on the page. Prefer institutional sources. If only a named-person case supports a claim, `generalize` and cite nothing.

## 3. Audit · Claims needing verification

This note lists what the script tagged and states that no named company or person appears. Check both mechanically:
- every tag the note lists exists in the script → otherwise `escalate`;
- a named-entity scan of the script (capitalized multi-word names, known company, platform, award, chart and union names) finds no real organization or person presented as doing something → otherwise `escalate` with the line.
Verdict `no-change` when both pass.

## 4. Audit · Overstatement risks

Each note quotes one or more lines and usually offers a softer wording. Decide per quoted line:

- **Apply the softer wording (`soften`)** when the line is in an explanatory section (Definition, Verbal Breakdown, Why This Order, Individual Level, Institutional Echo, Civilizational Echo, Observable Indicators, False-Positive Check, Reflection) **and** it states intent, design, certainty or universality as fact ("planted doubt", "it arrived exactly when", "wins go upward, losses go downward"). Use the author's own suggested wording, exactly. If the note names the problem but gives no wording, write the smallest change that removes the implication and mark it `"wording":"derived"` for the director's review.
- **Leave it (`no-change`)** when the line is inside the scene (Cold Open) or The Name: the scene is a labelled composite told from one person's point of view, and the note already says how to read it. Also leave it when the note only says "should be read as…" without identifying a false implication.
- **Never soften** a line in Safety Note, Escalation Triggers, Safer Response Language, Chain Breakers or Evidence To Preserve if the change would make a safety instruction weaker, vaguer or more optional. If such a line is quoted, `escalate`.

## 5. Audit · Overapplication risks

The note says how the pattern could be misread onto ordinary situations. Check that the page's "Before you read too much into it" section (False-Positive Check) states the same distinguishing test in substance. If yes → `no-change`. If the note contains a test the section lacks → `escalate` (the director may surface the note's sentence in the derived layer as a short "Do not over-read this" line; it is the author's own wording).

## 6. Audit · Sector accuracy check

Lists like "(a) how development weekends are structured and priced; (b) whether bundling … is typical". Split each list into its lettered points. For each point:
- If it is about the **scene** (how a fictional detail would typically look) and the page labels the scene as a composite → `no-change`, reason "illustrative detail in a labelled composite".
- If it is about a **term of art or practice that the explanatory sections rely on** (recoupment, cross-collateralization, work-for-hire, controlled composition, approval rights, audit windows, chaperone and work-permit rules for minors, residuals, chart rules) → link it to a topic in the fact base (section 7): `keep-cited` if the page uses the term consistently with the sources, `generalize` or `soften` if not.
- If it is a legal or health question → `keep-conditional`; the page already routes to qualified help. Confirm it does; if not, `escalate`.

## 7. The sector fact base (research once, use everywhere)

Many scripts lean on the same few dozen industry facts. Research by **topic**, not by sentence.

1. Cluster every item that needs research (sections 2 and 6) into topics. Expect roughly 40 to 70 topics for a sector.
2. For each topic write one neutral statement of what reliable sources support, in plain language, with 1 to 3 citation records. Store in `content/fractal/<s>/resolution/facts.json`:
   `{"id":"F012","topic":"cross-collateralization","statement":"…","scope":"general; terms vary by contract and country","sources":[{url,title,publisher,published,accessed,quote}],"confidence":"high|medium","notes":"…"}`
3. If no reliable source can be found for a topic after a real search (at least three distinct queries and two candidate pages opened), record it with `"sources":[]` and `"confidence":"none"`. Items that depend on it become `generalize`, `soften` or `remove`. **Do not guess.**

## 8. Escalate to the directing session when

- a change would touch safety content, a minor-safety line, or anything about self-harm, sexual violence or medical decisions;
- a source contradicts the script's claim (the claim may be false, not just unsupported);
- a named real organization or person is found in a script;
- the only way to keep a sentence is to cite a named individual's case;
- a `soften` would change what a scene says happened;
- you are not sure which verdict applies. Do not pick the convenient one.

## 9. The ledger and the derived layer

`content/fractal/<s>/resolution/ledger.json`: one entry per queue item, in queue order.

```json
{"q": 412, "combo_id": "C093", "section": "Institutional Echo", "kind": "source",
 "verdict": "keep-cited", "fact": "F031",
 "before": "<the exact sentence from the script, tags included>",
 "after": null,
 "reason": "Chart compilers publish rule changes addressing bundling; statement matches F031.",
 "by": "model:sonnet", "checked": "2026-11-10", "risk": "low"}
```

- `after` is set only for `generalize`, `soften`, `remove` (empty string for remove). `before` must match the script text exactly, or the patch is refused at build time.
- `risk`: `low` (label-only), `medium` (rewording in an explanatory section), `high` (a removal, anything the reader might act on, anything escalated and then decided). The owner approves all `high` and a sample of `medium`, once, as a batch.
- The build applies `after` in memory when rendering. Source files stay byte-identical. The word-count check becomes: page words == source reader words + the ledger's recorded delta for that combo, exactly.
- `content/fractal/<s>/resolution/SUMMARY.md` is generated: counts by verdict, every `high`, every removal, every topic with no source.

## 10. What the reader sees after resolution

- Combo banner, replacing "Unreviewed draft": **"The claims on this page were checked on <date>."** followed by the counts for that page ("3 points have a source, 1 was reworded, the scene is a composite") and: **"Not yet reviewed by a working industry professional."** Both sentences always appear together.
- In the text: `Composite`, `Common pattern`, `Varies by place` unchanged; `Depends on the terms`; `Ask a qualified person`; `Source checked` (links to "Sources for this page" at the foot, which lists the fact statements and their sources).
- `method` page: the sector totals from `SUMMARY.md`, and the full fact base as a readable list.
- A combo's `review_state` gains the value `sources_checked`. `expert_reviewed` stays reserved for a named human reviewer.

## 11. Automation for every future sector

`design/fractal-sector/resolve.py <sector>`:
1. `classify`: applies sections 0, 2.1, 3, 5 mechanically; writes the items that need a model to `resolution/todo.jsonl`, grouped by topic candidates.
2. (model step, from a work packet) research topics → `facts.json`; decide verdicts → `ledger.json`.
3. `check`: every queue item has exactly one ledger entry; every `before` matches the script; every `keep-cited` has a fact with at least one complete citation record; no entry touches a protected section without `"escalated": true`; URLs respond.
4. `apply` is part of the normal build. `summary` writes `SUMMARY.md`.

## 12. Worked examples (from ENT)

1. *C018, Institutional Echo:* "[REQUIRES SUBJECT-MATTER REVIEW] Whether a recoupment structure is a fair way to fund a record or a structure that keeps a balance from ever clearing depends on written terms, the rate and scope of recoupable items, how statements are presented and whether the artist has independent advice." → `keep-conditional`. Label: Depends on the terms.
2. *C063, Institutional Echo:* "Whether a transfer, rating change or access change amounts to unlawful retaliation is a question for qualified counsel [REQUIRES SUBJECT-MATTER REVIEW]." → `keep-conditional`. Label: Ask a qualified person.
3. *C022, Institutional Echo:* "Where delivery clauses use terms such as 'commercially satisfactory' without defining the standard or the decision-maker, the artist's compliance cannot be tested [COMMON INDUSTRY PATTERN] [REQUIRES SUBJECT-MATTER REVIEW]." → topic "delivery standards in recording agreements". If a reliable source describes "commercially satisfactory" delivery clauses → `keep-cited`. If sources only describe "technically satisfactory" versus "commercially satisfactory" as a negotiated distinction → `generalize` to that.
4. *C093, Institutional Echo:* "Chart methodology is periodically revised, in part to address practices that distorted results [HISTORICAL EXAMPLE TO VERIFY]." → must be `keep-cited` (a chart compiler's own published rule change is the ideal source) or `generalize`/`remove`. Cite the compiler's announcement, not a story about a named artist.
5. *C174, Institutional Echo:* "Long-running online investment frauds that combine a friendly relationship with a fake trading or investment interface have been widely reported in general terms [VERIFIED SOURCE NEEDED]." → `keep-cited` from a consumer-protection or law-enforcement advisory.
6. *C030, False-Positive Check:* "A reasonable number of rounds is standard practice [REQUIRES SUBJECT-MATTER REVIEW]." → states a norm as fact. If no source → `soften` to "A reasonable number of revision rounds is an ordinary part of the work." (`"wording":"derived"`, risk medium).
7. *C033, Overstatement:* "'Planted doubt' implies intent; softer: 'may produce doubt.'" → the phrase is in Verbal Breakdown → `soften` using the author's wording.
8. *C003, Overstatement:* "'He made a room feel like weather' is a characterization, not evidence of intent; softer: 'the atmosphere around him was unpredictable.'" → the line is in the Cold Open (the composite scene) → `no-change`.
9. *C051, Chain Breakers:* "Seek a second perspective from a trusted peer or an independent adviser … [REQUIRES SUBJECT-MATTER REVIEW]." → safety-adjacent advice that routes to help → `keep-conditional`; do not weaken.
