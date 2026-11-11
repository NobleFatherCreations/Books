# STORY-SYSTEM: how a Fractal² intro script is drafted, attacked, chosen and checked

Why it exists (owner, 2026-11-11): "develop a system that can audit and steelman different ways and how you came up with the final one" before rewriting. The earlier drafts told the cycle but did not make the danger felt, narrated the combinations as an example instead of the antagonist, and read like a list. This system makes the choice inspectable.

## The protocol (every rewrite follows it, in order)
1. **Brief and constraints.** Write the owner's words verbatim (what to include, what to cut, voice, scope). Add the guardrails from the earlier independent audit of draft 4 (`content/fractal2/owner-source/G-...`): no "proved"; no outcome promises; one safety line near the combinations; patterns never people; hedge contested claims; spiritual layer offered as one person's sight; American spelling; one call to action; counts consistent (30 techniques, 335 tactics, 203 combinations, 153 in the first sector, 2,700 examples, 30 sectors).
2. **Generate at least four candidate frames** from different sources (a prior prompt set, a literary form, a design idea, a first-principles idea). Each is one paragraph: voice, spine, what the reader feels at the end.
3. **Steelman each** (the strongest honest case for it: what it does best, who it serves, what it makes the reader understand).
4. **Attack each** with named failure modes: S1 fact-list (informs, does not move), S2 overclaim, S3 vague menace (frightens without teaching), S4 trauma exploitation (vivid for its own sake), S5 pacing (cannot be told one or two sentences at a time), S6 scope blur (reader cannot tell how big or how important the work is), S7 voice mismatch (owner would not say it), S8 spiritual overreach (states belief as fact).
5. **Score** 0-2 on a fixed rubric: voice, antagonist clarity, healing key, scope and size, spiritual and psychological weaving (hedged), safety, scene-ability (one or two sentences, paced), truthfulness to the audit. Totals decide; ties go to the frame that serves the reader in danger.
6. **Blend on purpose.** A winning frame may borrow one strength from a loser; record each borrowed part and why.
7. **Write** as scenes (`<!--scene H ...-->` + 1-2 sentences). Camera moves are written beside the words so story and image are one script.
8. **Mechanical audit:** `node scripts/story-lint.mjs <file>` (length, sentences per scene, banned patterns, required beats, number consistency). Must PASS.
9. **Fresh-reader test:** an agent that has seen only the text summarizes in five bullets what the work is, how big it is, what the danger is, what the key is, and lists any claim that reads as overreach or unsupported. If its summary misses the scope or the antagonist, revise.
10. **Record** the decision in `STORY-DECISION.md` (candidates, steelman, attack, scores, blend, lint output, reader-test result).
