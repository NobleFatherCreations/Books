# Copy-edit brief: Pattern Decoder entries

You are a careful human editor. The Pattern Decoder is a free guide to manipulation and control tactics. Its reader may be hurting, tired,
scared, on a phone, with limited reading ability, or new to every idea in it. Some readers are teenagers, some have learning
difficulties, some are reading in a second language, some are in crisis. Every sentence must be understood on a first read by any of them.

## What you receive
A worklist JSON: a list of entries. Each has `entry` (tactic name), `about` (its one-line definition, for context only), and `items`.
Each item has an `id`, the `field` it belongs to, `why` (what is wrong with it) and `text` (the current wording).

## What you return
Write ONE file (path given in your task): a JSON object `{ "<id>": "<new text>", ... }` with one key per item you change.
Copy each `id` exactly. If an item is already fine, leave it out (do not return it unchanged). Valid JSON, UTF-8, no comments.
Also write a second file (path given) `flags`: a JSON list of `{ "id": ..., "concern": ... }` for any sentence that states something
that looks factually wrong, unverifiable, overclaimed, or that you are not sure is true (a statistic, a named study or person, a law, a
clinical or medical claim, a date). Do NOT silently change the facts in those; keep the claim as written, and flag it. An empty list is fine.

## How to write
- Aim for about a 6th-grade reading level. Sentences under 20 words where you can. One idea per sentence.
- Everyday words. Say "use" not "utilize", "help" not "facilitate", "make worse" not "exacerbate". If a technical word is needed
  (it names the tactic), keep it but make the sentence around it plain, and explain it in a few everyday words the first time.
- Active voice, concrete verbs. Say who does what: "They tell you that it never happened."
- Sound like a kind, direct person talking, not a report. Vary sentence length and shape. No stacked fragments, no lectures.
- Keep the SAME meaning, the same hedging ("can", "may", "often", "tends to", "does not always mean") and the same facts. Never add a
  fact, example, statistic or claim that is not in the original. Never make a sentence stronger or more certain than it was.
- Keep every number, every named framework or term (DARVO, MICE, etc.), and every quoted phrase exactly as written.
- Keep the item's role. A list item stays one item (you may use two or three short sentences inside it). A question stays a question.
  Keep the same grammatical person ("you", "they", "someone").
- Keep a similar length. Splitting a long sentence usually makes it a little longer; that is fine. Do not pad, do not cut content.

## Never
- No em dashes or en dashes, and no " -- ". Use a full stop, a comma, or "and"/"but".
- No "not just X, but Y" / "not only X but Y" / "it is not X, it is Y" contrasts. State the point directly.
- No AI-flavoured words: delve, foster, leverage, utilize, facilitate, empower, robust, nuanced, intricate, multifaceted, navigate (as a
  metaphor), landscape, journey, realm, tapestry, pivotal, crucial, holistic, resonate, myriad, plethora, moreover, furthermore,
  ultimately, essentially, fundamentally, underscore.
- No throat-clearing ("It's important to note", "It's worth noting", "Here's the thing"), no "This highlights...", no closing
  summary lines that restate the point, no moralising.
- No diagnosing or labelling people (never narcissist, abuser, toxic, etc.). Describe what happens, not what a person is.
- If the entry's safety tone is cautious (leaving, danger, threats, children, money), keep it exactly as cautious. Never write
  anything that tells the reader to announce they are leaving, give an ultimatum, or name a consequence to the other person.
- Never explain how to do a harmful thing. Do not add steps, tools or wording a manipulator could use.

## Examples
Before: "Gaslighting is a pattern of contradicting a person's memory or perception, often about things that clearly happened, so that they begin to defer to the other person's version of events."
After:  "Gaslighting is when someone keeps contradicting what you remember or saw, even about things that clearly happened. Over time you start to go along with their version instead."

Before: "The denial arrives with a comment about you: your memory, your stability, or your habit of exaggerating."
After:  "The denial comes with a comment about you, like your memory, your mood, or a habit of exaggerating."

Before: "It is not just a disagreement, it is a way of making you doubt yourself."
After:  "It is a way of making you doubt yourself, which is different from an ordinary disagreement."

After you write the files, reply with ONE line: how many items you changed and how many flags. Nothing else.

## SECOND PASS (sentence length)
These items were already edited once, but each still has a sentence over 24 words (or a leftover dash, stiff word, or "not just" frame).
Rewrite so that EVERY sentence is 20 words or fewer, wherever the meaning allows. Split long sentences into two or three short ones.
Replace any remaining hard word with an everyday word. Keep everything else the same (meaning, hedges, negations, numbers, quotes,
named terms, safety tone). Do not use 'can feel like', 'to feel like', 'feels like', 'can seem like', 'may seem', 'tend to', 'the pattern
shows', 'pattern shows when', 'people describe feeling', 'people describe dread'. Keep list items at 45 words or fewer, short_definition
and core_meaning one sentence of 10-30 words that does not end on 'before', 'be', 'and', 'the', 'to'. Vary how items open. Return only
items you change.
