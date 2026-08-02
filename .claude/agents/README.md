# Project subagents

These are real Claude Code subagent definitions, copied in from two
inspected collections (wshobson/agents and contains-studio/agents — no
telemetry, no daemons, no hooks in either). Because they live in
`.claude/agents/` **inside this repo**, they're available automatically in
any future session that opens this repo — no install step, no plugin
marketplace, nothing that depends on this container's home directory
surviving between sessions (see `MEMORY.md` for why that distinction
matters here).

## How to use them

In conversation, just describe the task — Claude Code matches it to the
right agent automatically (each has a `description` explaining when to use
it). Or name one directly: "use the ui-designer agent to review this page."

## What's here, by the three review categories asked for

**Design / UX**
- `ui-designer.md` — visual design, layout, component styling
- `ux-researcher.md` — usability, information architecture, user flow
- `brand-guardian.md` — visual identity consistency across pages/projects
- `visual-storyteller.md` — narrative/visual cohesion, imagery choices

**Writing / copy**
- `content-creator.md` — general content across formats
- `content-marketer.md` — marketing copy, campaigns, positioning

**Code / technical**
- `code-reviewer.md` — code quality, bugs, maintainability
- `security-auditor.md` — security review
- `architect-review.md` — structural/architectural review
- `frontend-developer.md` — implementation review for HTML/CSS/JS
- `mobile-developer.md` — mobile experience specifically (your books are
  primarily read on phones per the review package's own notes)
- `test-writer-fixer.md` — test coverage and fixes

**Impeccable's support crew** (design skill, see below) — used automatically
by the `impeccable` skill, not usually invoked directly:
- `impeccable-finish-reviewer.md`, `impeccable-documenter.md`,
  `impeccable-manual-edit-applier.md`, `impeccable-asset-producer.md`

## Not brought in

The full collections have far more than this (203 in wshobson/agents alone —
backend, data, ML, infra, etc.) — not relevant to a self-contained static
book/gallery project, so left out to avoid clutter. Say the word if a
specific one from either collection would help and I'll add it.
