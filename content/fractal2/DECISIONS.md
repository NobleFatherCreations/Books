# Fractal² — decisions log

Newest first. Each entry: what was decided, why, and how to change it.

## 2026-11-10

**D14. Stale agent discipline.** A sector-build worker (Opus) hit the 5-hour usage limit twice. Per CLAUDE.md, nothing else was dispatched in parallel; the directing session continued the remaining work itself and resumes workers one at a time after the reset.

**D13. THE HOUSE drawer is excluded from this project's accessibility scan.** axe reports one issue inside the shared drawer button (its visible "NF" differs from its label). It is a site-wide component used on every page and is not edited here. Listed for the owner under "next".

**D12. Heavy formations are built ahead of time in idle slices.** The 30,000-point figures are prepared one at a time while the reader is still at the top, so reaching them never causes a slow frame. Change: `HEAVY` in `design/fractal2/intro.js`.

**D11. Narration placeholder is a silent timing track**, not a synthetic voice. Reason: the owner chose to decide about a voice clone after recording, and nothing synthetic should speak as the owner. The Listen button leads the reader down the page at reading pace until the real recording exists. Change: record, then run `design/fractal2/sync_audio.py`.

**D10. The narration script is generated from the page text.** One source of truth (`intro-final.md`). Spoken wording that differs from the page lives in `narration-edits.json`. Change the text, rebuild, and the script, captions and timings follow.

**D9. Same-site shared files are allowed for fonts, audio and data** (search index, later the map). Every page still reads completely on its own; these files only add features. They are fetched by absolute path from `/fractal2/_a/`. This is the one place the "self-contained page" rule is read as "no third-party requests and no relative paths" instead of "one file". Without it, each of 500+ pages would carry about 300 KB of fonts and the search index. Owner may overrule; the build can inline fonts instead (`build.py`, `frame.py`).

**D8. Every scene on the sector site carries the Composite label**, whether or not the script tagged it inline. Reason: hard rule "label every scenario as a composite".

**D7. Tag resolution states.** A new state `sources_checked` (checked against published sources by a model, logged in a ledger) is distinct from `expert_reviewed` (a named human). The site never claims expert review that did not happen. See TAG-POLICY.md.

**D6. Stage 6 is shown as "Extract · Control".** The Fractal says Extract; the expanded tactic book says Control. One stage, both names, one explanatory line on the stage chapter. Owner to confirm the line.

**D5. One Netlify site for all of Fractal²** (intro and every sector), publish folder `library/fractal2/site/`, pages nested under `fractal2/` so the same files work on the site's own address and behind the main domain. See ARCHITECTURE.md.

**D4. Combo reading modes are views over one document**, never copies, so the author's word count still matches exactly.

**D3. The intro's visual idea: one field of light.** Every point on the page is one mapped example: 2,700 for The Fractal, growing to more than 30,000. Each figure is a formation of the same points, so nothing is decoration. Point zero is "you": the page begins and ends on that single light.

**D2. Name and line.** *Fractal²* — "The closer you look, the more there is." The ² is explained in the text as The Fractal turned on itself, the fractal of The Fractal (the owner asked for something clever that carries the scope as a larger fractal of the series). Alternatives are in the session notes; easy to change in `intro-final.md` line 1–3.

**D1. Intro structure.** The descent shape from the story blueprint, with the combinations at the bottom of the descent and the frequency as the answer. Eleven parts. The owner's account (Part VI) holds only what the owner wrote. "Weapons" is not used as a frame; "the sequence" is.

## 2026-11-09 (owner)

- Name: "come up with something clever…" → D2.
- What's coming: say this is a lifetime of work; all of it, every sector → Part X.
- Policy list: not included; describe a future and "first people need to see what is in the way" → Part X.
- Voice clone: decide after recording. No word cap on the intro.
- No need to stop for approval mid-build, provided the script and design stay easy to adjust.
