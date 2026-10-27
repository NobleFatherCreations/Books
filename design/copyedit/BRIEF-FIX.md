# Fix brief: repeated phrasing in Pattern Decoder entries

A repeated-wording checker rejects these passages. Each item in the worklist has `why`, which names the exact phrase or pattern that
is repeated across other entries (for example 'the pattern shows x15', 'ends the same way as 2 other entries', 'opens ... like 7 other
entries', 'sentence may be cut off'). Rewrite ONLY that passage so the flagged phrase or ending or opening is gone, using wording that
belongs to this tactic. Keep it as plain as it is now (about a 6th-grade level, short sentences, everyday words).

Rules: keep the meaning, facts, numbers, named terms, hedging words (can, may, often) and any negation (not, never, no). Add no new
facts. Never change words inside quotation marks. No em dashes or en dashes. No 'not just X, but Y' frames. Do not use any of these
as replacements, because they are also repeated elsewhere: 'the pattern shows', 'pattern shows when', 'can feel like', 'to feel like',
'feels like', 'people describe feeling', 'people describe dread', 'tend to'. Vary the opening: start from this tactic's own subject.
For a 'cut off' warning, make sure the passage ends in a complete sentence that does not finish on a word like 'before', 'be', 'and',
'the', 'to'. Keep length within roughly 80% to 120% of the current length (word limits are enforced: expanded_definition 40-110 words,
repair_check and boundary_respect_check 20-60, how_to_distinguish_from_related 30-105, safety_note 25-95, list items 45 or fewer).

Input: a worklist JSON (entries with `items`: id, field, why, text). Output: ONE JSON object {"<id>": "<new text>"} for every item,
ids copied exactly. Valid JSON, UTF-8. Reply with one line: how many items you rewrote.
