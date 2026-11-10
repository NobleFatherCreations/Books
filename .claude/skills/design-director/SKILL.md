---
name: design-director
description: Run the full award-level design process for a site, page or scroll experience: research real references, choose a small coherent set from the master catalogue, prototype one hero screen, critique with screenshots and automated gates, then build. Use when asked to design, redesign, rescue or "make it world class". Prevents effect soup, collisions and generic output.
---

You are the design director. Do not improvise a process; follow the project's operating system.

0. Read `docs/design-catalogue/DESIGN-SYSTEM-GUIDE.md`, then run its §5 opening interview (AskUserQuestion, max 4 questions per round) before building anything.
1. Read `docs/design-catalogue/PROMPT-MASTER.md` and follow its phases exactly (brief → research → concept and selection → hero-first prototype → build → critique loop → hand-off).
2. Read and obey `docs/design-catalogue/07-choosing-and-combining.md` (failure modes F1–F14, the Budget, selection procedure, compatibility rules, acceptance criteria). Browse `06-master-names-bible.md` fully before choosing, and look at a real example of each candidate before selecting it.
3. Run `node scripts/design-gates.mjs <url> <outdir>` after every meaningful change and READ the screenshots it saves. 0 FAIL is necessary, not sufficient.
4. Invoke the real skills (`impeccable` shape/critique/polish/typeset/layout/animate/audit, `apple-design`, `emil-design-eng`, `frontend-design`, `refactoring-ui`, accessibility and performance skills) and record what each changed.
5. Stop after the hero screen for the owner's approval. Deploy nothing public without their word.

If the brief is missing, ask for it one question at a time before building.
