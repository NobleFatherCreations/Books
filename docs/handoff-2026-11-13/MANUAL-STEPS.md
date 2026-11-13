# Things I could not do from here: step by step

I can write to this repo. I cannot write to your Claude.ai account, your GitHub settings, other repos you haven't given me push access to, your phone, or anything that publishes. Each item below says what to do, in order, and what to tell me afterward.

## A. Put your working rules into Claude.ai memory (2 minutes)
1. Open `docs/handoff-2026-11-13/CLAUDE-MEMORY-PASTE.md` and copy the text between the two `---` lines.
2. On claude.ai go to **Settings, then Capabilities, then Memory** (the name can vary by plan; look for "Memory" or "Manage memory").
3. Choose **Add** or **Edit**, paste the text, and save.
4. Start a new chat and ask: "What are my rules for working with you?" If it recites them, it worked.
If you don't see a Memory setting, use step B instead.

## B. Make a Claude.ai Project that already knows the Fractal (5 minutes)
1. claude.ai, then **Projects**, then **Create project**. Name it "The Fractal."
2. In **Project instructions**, paste the same block from step A.
3. In **Project knowledge**, add these four files from the zip: `START-HERE.md`, `FRACTAL-DIGEST.md`, `FAILURE-LOG.md`, `STEELMAN.md`. (About 20 pages in total; cheap to load.)
4. Do not add the PDFs or the 245,000-word book. They cost far more than they help.
5. Start every Fractal chat inside this project.

## C. Make GitHub show the right branch (3 minutes; I can't change repo settings)
Right now the default branch is stale (`claude/wookbook-castings-consolidate-4zyo0d`). The canonical branch is `claude/optimistic-clarke-86s6bg`.
1. github.com, then the **Books** repo, then **Settings**, then **Branches**.
2. Next to "Default branch," click the switch icon, choose `claude/optimistic-clarke-86s6bg`, and confirm.
3. Tell me, and I'll update `CLAUDE.md` and the registry notes to say so.
Do **not** delete or force-push any branch before you've checked it. If you want the old branches brought up to date, say "fast-forward the strict-ancestor branches" and I'll list the exact commands and the old commit ids first.

## D. Give other repos the same memory (needs your yes)
Wookbook, Castings and Fantasy are separate repos. To add a pointer note to each:
1. Tell me "add the pointer note to Wookbook" (or Castings, or Fantasy).
2. I'll request push access for that one repo. Approve the prompt that appears.
3. I'll add one short file plus a line in its CLAUDE.md saying where the canonical memory lives. I won't change anything else.
If you'd rather do it yourself: copy `docs/FRACTAL-DIGEST.md` into each repo and add one line to its CLAUDE.md: "Canonical project memory is in NobleFatherCreations/Books, branch claude/optimistic-clarke-86s6bg."

## E. Notion memory (optional)
I can save a short version of the digest and the failure log to your Notion memory, but I only do that when you choose it. If you want it, say "save to Notion memory." Note that it only helps chats that have the Notion connector on; the repo version is the reliable one.

## F. Check the intro on a real iPhone (10 minutes; no tool can do this)
Open https://fractal-entertainment.netlify.app/fractal2 on your phone in Safari, then:
1. Scroll all the way to the end. Did the page crash or reload? (Yes or no.)
2. Scroll back up. Does it let you? Do the zoom and rotation move smoothly with no jumps?
3. Are the words readable at the moment they pass the fractal, and does any line appear twice?
4. Does the last button take you somewhere sensible?
Send me the four answers. That closes the biggest open item on the intro.

## G. Two facts in the school-psychologist composites need a source
1. Search "NASP recommended ratio school psychologist student" and open the National Association of School Psychologists page. Note the ratio they recommend (it has been about 1 to 500 at the school level) and the date.
2. Search "disproportionality special education emotional disturbance IDEA" and look for a government or research page (the U.S. Department of Education publishes annual data).
3. Send me the two links and numbers. I'll cite them in the PDF, or soften the sentences if you can't find them.

## H. Decisions only you can make (answer any of these in one line)
- Fix the swapped definitions (Spiritual Bypassing and Financial Control) on all 26 sector pages? A one-line data fix and rebuild; deploying is a separate yes.
- Say "26 of 30 sectors published" in the book, or finish the four missing sectors first?
- The prayer: in the PDF body, or left to the series?
- The laws list from the War Map: in the reference section, or left out?
- The Paper Child and Calling Trap: in the public PDF, or in Foil's copy only?
- Deploy the Entertainment v3 sector site? (Built and verified; not live.)
- Connect Google Drive so I can read your combo book? (claude.ai, Settings, Connectors, Google Drive, Connect; then tell me.)

## I. If a new chat still seems to miss things
1. Make sure it is in the Books repo on branch `claude/optimistic-clarke-86s6bg`.
2. Say: "Read `CLAUDE.md`, then `docs/FRACTAL-DIGEST.md`, then `content/fractal2/design/FAILURE-LOG.md`, then restate my request in two lines before doing anything."
3. If it skips a file you named, say: "You didn't open <file>. Open it and show me the first line."
4. For the bigger fix, run the prompt in `docs/SYSTEM-MEMORY-PROMPT.md`.
