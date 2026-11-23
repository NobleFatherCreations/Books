# The Weighing v5: writing brief (binding for every pass)

Owner, 2026-11-23, verbatim:
- Voice: *"Sharp thinking partner with more than normal humor that's blunt and no filter."*
- Goal: *"I do not want the expansion goal to be a certain amount of words. I want all topics covered and easy for people to understand and remember how to weigh effectively. … identify any missing content related to the book, all ideas are fully discussed, book is optimized for seo and connects to other books to build the web, the content written relatable and helpful … take the original 20,000 start point and branch off into the ideas / missed opportunities … and write a full book. The sections within each chapter shouldn't follow a static flow / audit and design a unique approach to each chapter that ensures usability and retention tricks for people to remember in the moment."*

One agent per source file (`content/scale-v2/NN-*.md`). For each chapter in your file you **(a)** rewrite or write it in the voice, **(b)** build it to its card in `CHAPTER-DESIGN.md` (shape, handle, anchor image, recall moment, worked case, search headings, links), and **(c)** make sure every topic `COVERAGE-MAP.md` assigns to it is fully discussed. A chapter is done when a stressed reader could use it in the moment, and could still say its handle a week later.

## 1. The voice: a sharp thinking partner with no filter

The reader is usually mid-situation: a text they can't read, a partner they can't figure out, a friend saying they're overreacting, or a quiet fear that they're the problem. They want someone smart who tells them the truth fast and makes them laugh while doing it.

- **Blunt.** Say the true thing first, then explain. "Your gut is not a lie detector. It's a pattern detector with a grudge." Cut throat-clearing and hedges ("it may be worth considering"). Where something is uncertain, say so in one plain line, then move on.
- **Funny, more than usual.** Dry, specific, a little savage about the absurd. Targets: the brain's defaults, the internet's diagnosis machine, the 3am investigation, the friend who has never met your partner and has already cast them as a villain, the reader's own detective phase (warmly, never cruelly). Aim for 2 to 4 real laughs per chapter in the ordinary chapters. A laugh must also teach: if you can delete the joke and lose nothing, delete it.
  - **No filter has limits.** Never joke about violence, sexual abuse, self-harm, children being hurt, or real fear. No humour in or next to the three heavy chapters (`this-book-in-the-wrong-hands`, `before-you-test-is-testing-safe`, `when-weighing-stops`), inside any `::: warn` block, or in any safety line anywhere. Never mock the reader. Never punch at a group (gender, culture, neurotype, class, religion).
  - Swearing: none. Bluntness comes from the content, not from swear words.
  - **Pilot note (01-i-a, 2026-11-23):** accurate, well built and safe, and the safety chapter was exactly right. In the ordinary chapters, though, the humour read polite, about one gag per section ("Give it a fortnight and it will catch your dentist love bombing you" was the right register). The owner asked for *more than normal* and *no filter*, so go further: say the uncomfortable true thing out loud ("You don't have a gut feeling. You have a grudge with a search history."), let the reader see themselves mid-spiral and laugh at it, and roast the internet's diagnosis culture freely. Keep every joke attached to the point, and keep all of it out of the safety zones above.
- **Precise.** This is a thinking book. Keep the original's best lines, its distinctions and its intellectual honesty. Plain words over jargon; when a term matters (base rate, false positive), define it once in a sentence a 14-year-old could follow.
- **Talk to them.** Second person, contractions, short sentences, a longer one when it carries something. Concrete over abstract: the "k." text, the read receipt, the half-second pause before "I'm fine", the group chat that has already reached a verdict.
- **"I" sparingly**, for opinion ("I'd bet on the boring explanation"). Never invent anything about the author.
- **No therapist-speak, no preaching:** no "it's important to", "hold space", "you are valid", "journey", "you've got this".
- **Run the `no-ai-slop` rules** (`.claude/skills/no-ai-slop/SKILL.md`): no "it's not X, it's Y" reveals, no "no X, no Y, no Z" lists, no colon reveals, no fake-profound kickers, no trailing -ing clauses, at most 3 dashes per 1,000 words, no rule-of-three padding.

## 2. Build each chapter to its design card (CHAPTER-DESIGN.md)

- **Shape:** the card names the chapter's structure (a dial, a drill, a fill-in form, a myth-buster). Build that shape. Don't fall back on intro, three headed sections, summary. Neighbouring chapters must feel different.
- **Handle:** one `::: handle` block with the line to remember, placed where the idea lands. You may sharpen the card's wording; keep it under 12 words and sayable aloud.
- **Anchor image:** use the card's image (or a better one, if you note why) and keep it through the chapter. Don't stack metaphors.
- **Recall moment:** after the middle, ask the reader to produce the idea before showing it again, with the answer in a `::: sort` (`- prompt || answer`) or a `::: check`.
- **Worked case:** at least one `::: scene` per chapter. Its first line is exactly `*LABEL*` (the owner picks the label wording later). Made-up people, everyday detail, under about 220 words, and it must show the chapter's tool being used. **Across your file, at least one case ends "yes, it really was manipulation"**: the book teaches accuracy, not doubt.
- **Search headings:** use the card's reader-language headings as `##` headings where they fit ("## Am I overreacting?"). These are what people type; they're also what search engines and AI assistants lift. The first paragraph under a question heading answers it directly in 40 to 60 words.
- **Closing step:** every chapter ends with something to do, in a `::: try <label>` block (the label is reader text, such as "Try it tonight"), unless its card says otherwise (the heavy chapters end with help, not homework). It should be one concrete action, ideally under five minutes.
- **Handoff:** the last paragraph links onward to the chapter this reader needs next (`ch:` link), in the voice.
- **Links (the web):**
  - `ch:` links inside the book wherever another chapter carries the idea.
  - The card's sister-book bridges as `::: bridge` blocks: one or two sentences saying who it's for, with the link (`/repair/what-an-apology-is-for`, `/longafter/dating-when-youre-ready-and-when-youre-not`, `/atwill/a-bad-job-versus-a-coercive-one` and so on). Only use addresses listed in the card or in COVERAGE-MAP section 8, or that you have checked exist in `library/<book>/`.
  - Pattern Decoder links in text where a tactic is named: `[Gaslighting](/playbook/<slug>)`. Check the slug exists in `instruments/playbook/site/<slug>.html`. Use the Decoder's name, with the everyday word in brackets if it reads better.

## 3. What must not change (hard rules)

1. **The floor.** Chapter 2's rules outrank everything: you do not owe anyone certainty before you protect yourself; using calibration to make someone doubt an accusation about you is itself evidence; in danger, stop weighing and act. No chapter may weaken them. Every doubt tool (base rates, three explanations, boring explanations, difference, the mirror) carries a one-line reminder or link that it doesn't apply to someone in danger (`ch:when-weighing-stops`).
2. **Weaponisation check** on every script, test and checklist: could a manipulative person quote this page to make the reader doubt themselves, or use the test as a cover? If so, add the counter line ("If someone hands you this chapter to prove you're overreacting, reread chapter 2.").
3. **Existing text:** keep every existing link (`ch:`, `/playbook/`, `/loop` and others). You may rephrase link text and move links. Keep each existing chapter's best lines and all its distinctions. You may restructure freely to fit the card. Don't drop an idea; if you merge one, say where in your report.
4. **Facts and sources.** The original book cites almost nothing; the new chapters need research. Rules:
   - State a research finding only if you are confident of it **and** can name the source precisely (authors, year, title, journal or publisher). Use WebSearch or WebFetch to confirm it.
   - Every chapter that states a finding ends with `## Sources` as a `- ` list: Author(s) (year). *Title*. Journal or publisher. DOI or URL if you found one.
   - Name models as models (the BITE model is Steven Hassan's model, not settled science). No invented numbers. No clinical claims beyond what a source says.
   - When unsure, write it as general ("researchers who study deception mostly agree…") or leave it out, and list it in your report.
5. **Headers:** every chapter has `title`, `question` (the reader's question, in their words), `seo` (a 50 to 60 character page title with the main search phrase near the front), and `short` (40 to 60 words, readable quoted alone, answering the question). Don't change the `title` of an existing chapter. New chapters keep the title in plan.json unless you have a clearly better one (say so in your report).
6. **Blocks:** palette only (CHAPTER-DESIGN.md): `handle`, `scene`, `try`, `warn [danger]`, `tree`, `sort`, `myth`, `script`, `check`, `compare`, `pull`, `aside`, `gradient`, `bridge`. Opening line `::: kind [label]`, closing line `:::` alone, a blank line before and after. Existing `::: warn` blocks stay warn blocks with their labels.
7. **Safety:** the heavy chapters keep at least one link to `ch:when-weighing-stops`, `ch:before-you-test-is-testing-safe` or `ch:this-book-in-the-wrong-hands`. No diagnosis of anyone. No deadlines or prescribed feelings. Where help services matter, say "the domestic abuse service where you live" and link `/longafter/find-help` rather than naming a number you haven't checked.
8. **No length cap and no padding.** Write until the chapter does its job and covers its topics, then stop. A typical ordinary chapter lands between 1,000 and 1,800 words; a tool page can be 400. Never repeat an idea that another chapter owns: one line and a link.
9. Don't touch files other than your assigned `NN-*.md`. Don't build, commit, push or deploy.

## 4. Checks before you hand back

```
python3 scripts/book/rewrite-check.py content/scale-v2/<file>.md           # 0 problems
python3 scripts/book/readability.py --book scale --stdout | sed -n 1,16p   # 0 paragraphs over 90 words in your chapters; grade within limits
grep -c '^::: ' content/scale-v2/<file>.md; grep -c '^:::$' content/scale-v2/<file>.md   # equal
```
Check every `/playbook/<slug>` and sister-book link you added exists on disk (`ls instruments/playbook/site/<slug>.html`, `ls library/<book>/<slug>.html`).

## 5. Report back (under 400 words)

For each chapter: the words, the shape used, the handle, and whether its case ends "yes, it was". Then:
- Topics from COVERAGE-MAP you covered, merged or skipped, and why.
- Every research claim you added, with its source and how you confirmed it, plus anything you were unsure of.
- New links added (internal, sister books, Decoder).
- Your proposed `keyword` (main search phrase) and two alternates per chapter.
- Three samples, before and after: a laugh, a structural change, a handle.
