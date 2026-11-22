# AI-writing audit v2: what changed compared with the first no-AI-slop pass (2026-11-22)

**Sources combined** (rules read and folded into `scripts/longafter-ai-audit.py`; nothing installed): yotamgutman/ai-free-writing-checklist, blader/humanizer, solanabr/writer-style-skill (validator thresholds), danielrosehill/My-Tone-Of-Voice (stylometric profile method), zoharbabin/brand-voice (rules only; its install hook was not used), houtini-ai/ai-detect (light ONNX model run once in a scratch environment), youcontent360 20-point checklist. Anthropic's brand-guidelines skill covers Anthropic's own colours and fonts, so it doesn't apply to this book's voice.

| Check | First pass caught it? | Before v2 | After v2 | What was done |
|---|---|---|---|---|
| AI vocabulary (about 90 words across the lists) | partly (about 30 words) | 20 hits | 20 hits | All legitimate uses: Decoder page names (children used as leverage), literal "quietly", pet fostering. Kept |
| Stiff spelled-out forms ("it is", "do not") | no | 154 (detector) | 118 | 33 converted where a contraction is natural; 3 bad conversions undone, including one quotation from the Feminine book that must stay word for word. The rest are clause-final or emphatic |
| Writing about the page ("this chapter covers…") | no | 26 | 13 | Generic ones rewritten to speak to the reader; reassuring ones kept ("This chapter is short and plain on purpose") because they tell the reader they're in the right place |
| Three sentences in a row with the same opening | no | 44 | 29 | Worked examples rewritten (the "She… She… She…" runs). Deliberate repetition in openings kept ("The first Christmas. The first birthday.") |
| Heading restated in the first sentence | no | 13 | 11 | 2 real ones fixed; the rest are the *Where are you right now?* page, where the heading is the reader's situation and the line under it is the answer |
| Short pull quotes that read like sayings | partly (16 rewritten earlier) | 33 | 32 | 3 more rewritten; the rest are practical lines |
| Sentences over 30 words | no (limit was 40) | 45 | 37 | 8 heavy prose sentences split; the rest are colon lists or quoted speech |
| Bold labels on list items | no | 780 | 780 | Measured: only 35 labels repeat their own text, mostly country names a reader scans for. Kept on purpose for scanning on a phone |
| Lists of three | no | 64 | 64 | Reviewed; most are real three-part lists (where, when, who). Not changed |
| Sentence-length spread (machine-even text) | no | median 6.7, 0 machine-even pages | same | Within the human band for a terse writer |
| Detector model score | no | median 77% of sentences flagged | 77% | Not a target: the model flags plain instructional writing. Highest scores are the help-number and police pages; lowest are the warmest pages |
| youcontent360 facts and sources | yes (phase 6) | n/a | n/a | Done earlier: verified numbers and laws, 263 sources listed |
| AI-use disclosure | no | n/a | n/a | **Owner decision**: the checklist recommends saying how a piece was made when readers might wonder. Not changed without the owner |
