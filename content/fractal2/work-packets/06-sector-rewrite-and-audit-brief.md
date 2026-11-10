# Brief for the next sectors: the cold open, the rewrite rules, the audit

For an AI preparing or checking another sector's package (Music Festivals, Spiritual Communities, and the rest) so it matches what was done for Entertainment and Music (ENT). Short on purpose. Full detail: `content/fractal2/TAG-POLICY.md` and `work-packets/03-tag-resolution-model-step.md`.

**One fact first.** The ENT cold opens were not rewritten. All 153 are the author's text, unchanged. Part 1 is the standard those scenes already meet, written down so other sectors can be held to it. Parts 2 and 3 are the changes that were actually applied to ENT.

## 1. The visceral cold open

Every combination opens with one scene. It must make the reader feel the sequence in the body before any tactic is named.

- **Second person, present tense, one unbroken scene.** "You're a frontwoman, twenty-six years old, standing in an apartment you could not have imagined two years ago."
- **Start with real warmth.** The first tactic must feel good, and be good. "The happiness is real."
- **One concrete moment for each tactic, in the exact order of the sequence.** No tactic is named inside the scene.
- **Show each step removing the defence against the next.** The gift makes the question feel rude; the signature makes the lawyer "for your own peace of mind".
- **Physical and specific.** Objects, rooms, sounds, what the hands do: "carpet that muffles the sound of your boots". Sector detail by its real name ("cross-collateralization").
- **Other people stay pleasant.** Nobody in the scene is a villain. "She smiles and says of course."
- **One turn line** where the trap closes. In The Debt Prison: "but you've already signed".
- **End on an image or a question, never an explanation.** "You no longer know whether it was a gift, a loan, or a sentence."
- **About 450 to 600 words.** Then the hard cut to the name: "That's the Debt Prison."
- **Always a composite.** No real or recognisable person, company, venue or event. The scene is labelled Composite on the page.
- **Never softened in the audit.** The scene is one person's point of view inside a labelled composite; hedging belongs in the explanatory sections.

## 2. Rules for the other fifteen sections

Order and names are fixed: Cold Open, The Name, Definition, Verbal Breakdown, Why This Order, Individual Level, Institutional Echo, Civilizational Echo, Observable Indicators, Evidence To Preserve, False-Positive Check, Recognition Cue Cards, Chain Breakers, Escalation Triggers, Safer Response Language, Reflection.

- **Definition** ends with who benefits, why it is hard to detect, and: "Intent would require additional evidence; the pattern is what can be observed."
- **Why This Order** names the turning point and what weakens the sequence.
- **Explanatory sections state possibility, not certainty.** "will" becomes "may"; "this functions by" becomes "this can function as"; "is what weakens" becomes "can weaken". No claim of intent, design or "always".
- **Leave the author's figures of speech alone.** "Works like a fence", "the machine needs no author" stay as written.
- **Never weaken a safety instruction.** Safety Note, Evidence To Preserve, Chain Breakers, Escalation Triggers and Safer Response Language are not softened. Urgent level always says: safety first, do not confront.
- **False-Positive Check must name the innocent explanations** and the test that tells the pattern from ordinary practice.
- **Words to use:** "documented across", never "proved". "Intermittent reinforcement", never "Pavlovian". Inherited stress is the author's belief, not settled science. No promised outcomes ("begins to loosen", not "dissolves").
- **Patterns, never people.** No named or identifiable wrongdoer anywhere.

## 3. The audit (credibility tags)

Every tag and audit note gets one verdict, logged in a ledger. The author's files are never edited; changes are applied when pages are built.

| Verdict | When | ENT count |
|---|---|---|
| keep-label | Descriptive label is right as it stands (Composite, Common pattern, Varies by place) | 718 |
| no-change | Note needs no change to the page | 407 |
| keep-conditional | Sentence says an outcome depends on terms, or sends the reader to a qualified person | 23 |
| soften | Explanatory line states intent, certainty or universality as fact | 23 |
| keep-cited | A fetched, real source supports the sentence as worded | 8 |
| surface | A safety or over-reading test sits in the author's audit note but not on the page: add it word for word (owner approves each) | 5 |
| generalize | Specific claim not supported; replaced by what the sources do support | 2 |
| remove | False and unsupportable in any form | 0 |

- Research each term of art once per sector into a fact base, then reuse it on every page.
- A source must be fetched and read. If none is found, the sentence is generalized or softened, never labelled as checked.
- No page claims expert review. Each says: "Not yet reviewed by a working industry professional."
- ENT still has 184 items open; do not copy that state.

## 4. Fixed names and numbers

- The same 335 tactics in every sector, with the same ids. Three examples each: Individual, Institutional, Civilizational.
- Eight stages. Stage 6 is shown as "Extract · Control".
- "Chain Breakers" is the official section name.
- Check tag counts against the script itself, and technique numbers against the published list (both were wrong in places in ENT's inputs).

## 5. Running it for a new sector

```
design/fractal-sector/run.sh <sector>                       # ingest, build, verify
python3 design/fractal-sector/resolve.py <sector> classify  # once only, at the start
# model step: work-packets/03-tag-resolution-model-step.md
python3 design/fractal-sector/resolve.py <sector> check --final
python3 design/fractal-sector/resolve.py <sector> summary
```

Never run `classify` a second time on a sector: it resets pending work. Deploy nothing.

## 6. Before handing back

- Every scene: second person, present tense, tactics in sequence order, no tactic named, one turn line, composite.
- Word count of the author's text on each page matches the source, plus only the changes in the ledger.
- No safety line weakened. No named wrongdoer. No "proved". No page claims expert review.
- Summary of verdicts written, with every `surface` and every rewording listed for the owner.
