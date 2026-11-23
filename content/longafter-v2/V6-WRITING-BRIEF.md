# The Long After v6: step 2 writing brief (binding for every pass)

Owner's direction, 2026-11-23, verbatim: *"Go ahead with all of step 2 but fix and replace with a unique solution where possible - get down to earth with the reader where you can, make them laugh if appropriate - approach this info like a best friend sending their bestie info that may help."*

One pass per source file (`NN-*.md`). Each chapter gets the voice pass **and** every item in its section of `WORKLIST.md`, in one go. Fix things properly: rewrite the passage instead of bolting on a patch.

## 1. The voice: a best friend who's been through it, texting their bestie

The reader is often reading at 2am, tired, scared or furious, on a phone. Write like their smartest, warmest friend: the one who did the research, has been through it, and talks straight.

- **Talk to them, not at them.** Contractions. Second person. Short sentences, with a longer one when it has to carry something. "Here's what helps" beats "The following strategies may be beneficial."
- **Down to earth.** Name the real, everyday version of the thing: the 11pm message that's "just about the kids", the friend who says "but he was always so nice to me", the dog your ex suddenly can't live without. Use concrete detail over abstraction.
- **Humour where it fits. It's a pressure valve, never a punchline.**
  - Yes: dry, warm lightness about the absurd everyday side, like the 47-message essay at midnight, the ex's sudden passion for the school calendar, the forms that ask for the same thing four times, or yourself rehearsing a reply in the shower for the ninth time.
  - Never: jokes about violence, sexual abuse, self-harm, children being hurt, or the reader's pain; anything mocking the reader; anything in the crisis and safety sections. In the heavy chapters (book.json `chapter_class` crisis = `heavy: true` in plan.json), keep the safety parts plain and steady. A light line elsewhere in the chapter is fine if it helps them breathe.
  - Aim for roughly one light moment per chapter where it fits naturally. Zero is fine. Never force it.
  - Pilot note (01-i-a): the result was clean and accurate but a little reserved. In non-heavy chapters, lean further into friend-talk: the aside a mate would actually say, the knowing "yep, that one", a wry line about the absurd bits. In practical, legal and money chapters especially, warmth and a little wit make dry material bearable.
- **Owner's voice signals** (from `content/about.md`): plain words, raw honesty, short punches ("You're not."), naming the feeling exactly ("checking your own memory like it's lying to you"), no hedged corporate tone, warmth without syrup. Steal the cadence, not the content.
- **"I" is allowed sparingly** for opinion and solidarity ("I won't pretend this part is fun"). Never invent a personal story, experience or fact about the author.
- **Never preachy, never therapist-speak.** No "it's important to", "self-care journey", "hold space", "you've got this", "you are valid". Show it instead.
- **Run the `no-ai-slop` rules** (`.claude/skills/no-ai-slop/SKILL.md`): no binary "it's not X, it's Y" reveals, no "no X, no Y, no Z" lists, no colon reveals, no fake-profound kickers, no trailing -ing clauses, at most 3 dashes per 1,000 words.

## 2. What must not change (hard rules)

1. **Facts.** Don't add a fact, number, law, study, service or phone number that isn't already in the chapter or its Sources, unless you are certain and it's general (for example "laws differ between countries"). When in doubt, point to [Where to find the right body](ch:where-to-find-the-right-body) or [Find help](ch:find-help) instead of stating a rule.
2. **Header fields** (`title`, `question`, `seo`, `short`): keep them. You may tighten `short` into the new voice, but it must still contain the chapter's `keyword` from plan.json, read well quoted alone, and stay 40-60 words.
3. **Every link stays** (`ch:` links, `/playbook/` links, `/feminine/` links, sister-book links). You may rephrase the link text and move the link.
4. **`## Sources` stays exactly as it is**, at the end.
5. **Safety:** heavy chapters keep at least one link to `ch:if-youre-not-safe-right-now`, `ch:when-its-more-than-aftermath` or `ch:find-help`. Never write method-level self-harm detail. Never prescribe feelings or deadlines ("by now you should", "you will feel", "within six months you'll").
6. **Honest checks** (`::: honest`) keep their exact opening line (*An honest check, just for you. This is about what's in your hands now, not blame for what was done to you.*) and the four rules in `TONE-AUDIT.md`: about the present, a blame-free opener, private questions with no verdicts, a gentle next step. No humour inside them.
7. **Composite examples** (`::: scene`) keep their opening note line exactly (*This example is made up, built from patterns many people describe.*). You may rewrite the story in the new voice. Never describe a real person or case.
8. **Blocks:** keep the `:::` fences around what they wrap. Opening line `::: kind`, closing line `:::` alone, a blank line before and after. New blocks use the same syntax: `scene`, `honest`, `decoder`, `action`, `bridge`.
9. **No Root or Listening Room links** (owner left that question open). Don't change the composite-example wording rule (also left open).
10. **Length:** each chapter within about 15% of its current word count, unless the worklist adds something.

## 3. The worklist items, and how to do each one

- **Split paragraphs over 60 words.** Find the natural break. Don't just cut in half.
- **Break unanchored runs over 350 words** with a question heading, a short list or a block.
- **Reading grade over the limit:** shorter sentences, everyday words. Legal terms that must stay get a plain gloss the first time.
- **"Say where this applies":** name the place ("in England and Wales", "in most US states", "in Australia") **only if the chapter or its Sources already support it**. Otherwise make it honest and general ("the rules depend on where you live") and point to [Where to find the right body](ch:where-to-find-the-right-body).
- **Handoff line:** the chapter's last line points to the chapter that naturally comes next for this reader, as a `ch:` link, written like a friend ("When you've got a minute, [the money chapter](ch:money-as-the-channel) is the next fire to put out."). Put it after the closing action block, as the final paragraph before Sources.
- **Closing `::: action`:** one physical step, three minutes or less, concrete ("Open your notes app and write the next three dates that worry you"). Never a reflection prompt. Keep the section's heading inside the block.
- **Change the opening shape:** open with the reader's question, or with a myth they may believe ("Everyone says leaving is the end of it. If only."), then move on.
- **Concept HOME:** one full, plain, 40-60 word definition straight under a question heading. It should be quotable alone (this is what search engines and AI assistants lift).
- **Concept explained elsewhere:** cut to one line plus a link to its home chapter.
- **Decoder link text:** use the Decoder's name; add the everyday word in brackets if it reads better: [Hoovering / Relief Bait](/playbook/hoovering-relief-bait) (getting pulled back in).
- **`::: decoder` block** (dialogue decoder), using this exact shape:

  ```
  ::: decoder
  **They say:** "I just think the kids deserve to see their parents get along."
  **What it's doing:** Making your boundary sound like the problem. See [Name](/playbook/slug).
  **A reply you could send:** "I agree the children come first. Handovers stay at school, as agreed."
  :::
  ```
  The reply must be calm and court-safe: something you'd be happy for a judge to read.
- **`::: bridge book:slug`:** one or two friendly sentences on who it's for, with the link inside: `::: bridge atwill:a-bad-job-versus-a-coercive-one` then the text with [At Will](/atwill/a-bad-job-versus-a-coercive-one), then `:::`. Use `/book` for `index`.
- **Weaponization check (every script, checklist and boundary):** ask whether the abuser could use this page against the reader. If so, add a one-line counter-note ("If they ever quote this back at you, ..."), and soften any script that could read as uncooperative in court.

## 4. Checks before you hand back (all must pass)

```
python3 scripts/longafter-audit.py <part-id>          # 0 failing (voice, links, safety, Flesch, sentence length)
python3 scripts/longafter-ai-audit.py | head -3       # no new hard hits for your chapters
python3 scripts/book/readability.py --stdout | grep -A3 "^## Totals"   # your chapters improved
```
Don't build, deploy, commit or push. `longafter-ai-audit.py` rewrites AI-AUDIT.md/.json: put them back with `git checkout` after running it. Also run `python3 scripts/book/rewrite-check.py content/longafter-v2/<file>` (must show 0 problems). Don't touch files other than your assigned `NN-*.md`.

Report back: the chapters done, worklist items done or skipped (with why), facts you were unsure of, and three short before-and-after samples (one with a light moment, one structural fix, one handoff line).

## 5. How to run a pass (for the worker)

1. Read fully: this brief; your chapters' sections of `WORKLIST.md` (chapters are `=== slug` blocks; ignore a "HOME of" item if the definition already sits under a question heading, and an opening-shape item if the neighbours already open differently); `.claude/skills/no-ai-slop/SKILL.md`; `content/about.md` lines 1-60; `TONE-AUDIT.md`; `plan.json` (keywords, which chapters are heavy); and skim the previous file already rewritten, for tone continuity.
2. Rewrite each chapter top to bottom: the voice pass plus every applicable worklist item, including the weaponization check.
3. Run until clean: `python3 scripts/longafter-audit.py <part>` (0 failing), `python3 scripts/book/rewrite-check.py content/longafter-v2/<file>.md` (0 problems), `python3 scripts/book/readability.py --stdout | sed -n 1,20p`, `python3 scripts/longafter-ai-audit.py | head -5`, then `git checkout content/longafter-v2/AI-AUDIT.md content/longafter-v2/AI-AUDIT.json`.
4. Edit only your file, and don't build, commit, push or deploy.
5. Report in under 350 words: the chapters done; worklist items done or skipped, with why; facts you were unsure of; the check results; three short before-and-after samples (a light moment, a structural fix, a handoff).
