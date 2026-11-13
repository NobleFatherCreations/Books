# Package check (steelman of this package)

Question asked of the package: could a new chat, with only this zip, understand what happened, see what was asked and failed, rebuild the PDFs, and continue? Each requirement below was tested by file existence when the zip was built.

| What a new chat needs | File | Result |
|---|---|---|
| What the thread was and what was asked | `START-HERE.md` | present |
| Every owner message and pasted script, verbatim (23 genuine messages) | `OWNER-MESSAGES-VERBATIM.md` | present |
| Earlier-session context summary | `CONTEXT-SUMMARY-EARLIER-SESSION.md` | present |
| Every failure (intro site and PDF work) + pre-flight | `FAILURE-LOG.md` | present |
| Steelman of the PDF | `STEELMAN.md` | present |
| Spec for the final revision + execution prompt | `BLUEPRINT.md` | present |
| New-content draft | `NEW-CONTENT-FOR-REVIEW.md` | present |
| 2-minute project digest | `FRACTAL-DIGEST.md` | present |
| Instructions for what an AI can't do | `MANUAL-STEPS.md` | present |
| Claude.ai memory paste | `CLAUDE-MEMORY-PASTE.md` | present |
| Whole-repo memory prompt | `SYSTEM-MEMORY-PROMPT.md` | present |
| Machine-readable state | `thread-state-2026-11-13.json` | present |
| Master PDF | `pdfs/Why-I-Wrote-This.pdf` | present |
| Foil PDF | `pdfs/Why-I-Wrote-This-for-Foil.pdf` | present |
| Book 1 audit PDF | `pdfs/The-Fractal-Book-1-Audit.pdf` | present |
| Value-and-Impact PDF (to weave in) | `pdfs/Fractal2-Value-and-Impact.pdf` | present |
| Value-and-Impact source HTML | `rebuild/design/fractal2/reports/value-and-impact.html` | present |
| Audit source | `rebuild/design/fractal2/reports/fractal1-audit.body.html` | present |
| Build code: sections | `rebuild/design/fractal2/reports/why/build.py` | present |
| Build code: final weave | `rebuild/design/fractal2/reports/why/final.py` | present |
| Data tables | `rebuild/design/fractal2/reports/why/data.py` | present |
| Form fields | `rebuild/design/fractal2/reports/why/fields.py` | present |
| Renderer | `rebuild/design/fractal2/reports/why/render.mjs` | present |
| Styles | `rebuild/design/fractal2/reports/why/base.css` | present |
| Fonts | `rebuild/design/fractal2/fonts/newsreader.woff2` | present |
| Cover art | `rebuild/design/fractal2/art/fractal-original-1600.webp` | present |
| Series slides used in PDF | `rebuild/design/fractal2/reports/why/slide-003.jpg` | present |
| Artifact index (combo files) | `reference/artifact-index-2026-11-13.html` | present |

## What is still NOT in the package, and why

| Gap | Why | Where it is instead |
|---|---|---|
| The Fractal's own text (245,383 words) | Too large; reading it is what the digest exists to avoid | `content/prose/fractal.md`, `library/fractal/` in the repo; grep, don't read |
| The Pattern Decoder data (310 entries) | Large, and in the repo | `content/playbook-data.json` |
| Fractal² Entertainment and Corporate pages and combo scripts | Large, in the repo; the combo book (39 MB) is in the owner's Google Drive | `library/fractal2/site/fractal2/entertainment/`; Drive: `ENT_combo_book.pdf` |
| Intro-site source and deploy tooling | Separate project; documented, not bundled | `design/fractal2/redesign/v9/`, `scripts/film-*.sh`, `docs/FABLE-HANDOFF.md` sections 0a-0e |
| The assistant's full working transcript | 50 MB; not useful to read | Owner messages are verbatim; decisions are in START-HERE and the JSON |
| Output of the data checks in blueprint Part F | Not run yet | Blueprint Part F; to be run by the builder |
| Verified sources for the school-psychologist ratio and referral disparity | Not yet sourced | MANUAL-STEPS section G |
| Owner's answers on the pending decisions (prayer, laws list, Paper Child in public edition, fix swapped definitions, deploy v3) | Not given | MANUAL-STEPS section H; defaults listed in START-HERE section 8 |

## A defect found by this check

The first version of the owner-messages file claimed 47 owner messages but contained injected skill documents, sub-agent hand-backs and system notes. It was rebuilt with only the 23 messages the owner actually wrote.

## Verdict
**All required files present.** The gaps above are known and deliberate or waiting on the owner. A new chat that reads START-HERE, the digest, the failure log, the steelman and the blueprint has what it needs; the zip contains no secrets or credentials.
