# Ghostwriter prompt: the emotional spine of Fractal²

Reusable brief for any writer (human or AI) revising the narration in `content/fractal2/intro-v8.md`.

## Final audit of the emotional power struggle (2026-11-11)

The struggle the film stages is **powerlessness against reclaimed sight**. The reader begins as someone being quietly diminished (laughter they cannot join, a verdict they pass on themselves: "it must be me"). The antagonist is not a villain but a shape that works in order. The turn is not rescue; it is *naming*. Power returns when the sequence becomes visible and a first step becomes possible.

| Beat | What the viewer feels | Finding |
|---|---|---|
| Room, pew, phone at 2 a.m. | Recognition, shame | Strong. The body leads. |
| "But what if it is not you?" | Relief, permission | Strongest hinge in the film. |
| Shape, scale, 2,700 | Awe, vertigo | Strong. Scope shown, not stated. |
| Danger, combinations | Dread with a handle | Strong. The key sits inside the threat. |
| Safety note | Being held | Good. Keep early and quiet. |
| Old words | Depth, reverence | Good, hedged as one person's sight. |
| Work, descent, spark | Return, belief | Good. |
| **Missing: the narrator's stake** | Why this person? Why should I trust the guide? | **Weakness found.** Until now the author was an invisible cartographer. Facts were tested; the human reason for the work was absent. A viewer in pain needs to know the guide has walked it. |

Fix applied: the author's lens now enters (a) at the hinge ("I know that question, because I asked it of myself first") and (b) in a section, "Why I carry it", before the work is described. It states only what the author has said: a lifetime of noticing patterns, that this noticing saved the author's life, a healing and a spiritual journey, and a wish for it to reach people everywhere. It invents no events.

## The prompt

You are a ghostwriter. You are writing in the first person for one author, in their voice, for a cinematic scroll film. Each caption is one to three short sentences shown large, one at a time, with silence between.

**The author's lens (use only this; invent nothing about their life).** This body of work comes from a lifetime of honing pattern recognition. That noticing saved the author's life. It is both a healing journey and a spiritual journey. The goal is to share it worldwide so that people who are where the author once was can see the shape of what is happening to them. Facts about the project (30 techniques, 335 tactics, 203 combinations, 2,700 examples, 30 sectors) are tested and stay exactly as written; the author's meaning is *lens*, offered as one person's sight, never as proof.

**Psychology to use.**
1. Start in the body, then the mind, then the world (a hand closing in the chest, then the verdict, then the system).
2. Give relief before information: permission ("it is not you") must land before any list.
3. One image per caption. Concrete nouns (a pew, a phone glow at two in the morning), never abstractions stacked on abstractions.
4. Let the antagonist be a shape and an order, never a person. Patterns, never people.
5. Withhold. A pause is a sentence. Place silence after the hardest line, not before.
6. Vulnerability by understatement: say the true thing plainly once ("It saved my life") and move on. No pleading, no sermon.
7. Agency in the last beat: the viewer is given a first place to start, not a promise of an outcome.

**Rules.** American spelling. No em dashes. No "proved". No outcome promises (no "will heal", "cure", "guarantee"). Keep the safety line (call emergency services first). Offer the spiritual layer as one person's sight. Do not shame the faithful. One call to action only.

**Process.** Read the script. Mark where the viewer's emotion flattens. Write three candidate lines for each flat beat in different registers (plain, lyrical, severe). Choose the plainest that still lands. Read it aloud at the pace of narration. Run `node scripts/story-lint.mjs content/fractal2/intro-v8.md` and fix every failure.
