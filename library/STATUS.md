# The five new books — what's done, what's left

Updated 2026-08-31. Every "done" line below was verified by opening the
page and looking at it, not by a passing check. That distinction is the
whole reason this file exists: `qa.js` and the Playwright verifier both
reported clean on a build where four of five cover marks rendered as a
stray black dot, and again on a build where a quoting bug broke the entire
script. Structure checks cannot see a page that renders nothing.

## Done

| | Long After | Silence | At Will | Repair | Slow Take |
|---|---|---|---|---|---|
| Own body typeface, self-hosted | Newsreader | Source Serif 4 | Spectral | Crimson Text | Hanken Grotesk |
| Own display face for headings | Instrument Serif | Young Serif | Bricolage | Anton | Outfit |
| Own cover mark | horizon at dusk | gapped ring | clock face | mended ledger | thread |
| Own card language | rounded, filled | hairline rule | squared, ruled edge | ledger rule | rounded, filled |
| Section mark on every heading | ✓ | ✓ | ✓ | ✓ | ✓ |
| A−/A+ reader text scaling | ✓ | ✓ | ✓ | ✓ | ✓ |
| Quick exit (Esc + Leave) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `#/help` routing page | ✓ | ✓ | ✓ | ✓ | ✓ |
| Scroll-verified, both themes, 390 + 1200px | ✓ | ✓ | ✓ | ✓ | ✓ |
| Zero external requests | ✓ | ✓ | ✓ | ✓ | ✓ |

Prose passes: psychologist audit (`PSYCHOLOGIST-AUDIT.md`), em-dash and
typography pass (`PROOFREAD-NOTES.md`), the full 21-category no-ai-slop
audit including the judgment categories a script cannot reach.

## Deliberately not done, with the reason

**No progress bar, completion tracker, or collectible.** Wook has both — a
fill-bar and 26 beads, one per chapter — and it is the most obvious thing
to copy. All five of these books say in their own text: *"Nothing here
keeps score or knows you were here."* Adding one would make each book
contradict itself the same way the analytics beacon contradicts *faith*.

**No topic icons on headings.** Both reference books pair every header with
an emoji. On chapters about assault, drugging, and elder exploitation, a
topic-guessed glyph risks a tasteless mismatch, so each book repeats its
own motif instead. Same visual job, no risk.

**Text scaling writes to no browser storage**, so it resets on a full page
reload. That is the correct trade against the "nothing stored" vow. It does
survive chapter navigation, which is the case that matters, because the
router re-renders without reloading.

## Left to do

**Illustrated cover art.** The references have real painted/illustrated
covers. These five have hand-built SVG marks. Generating actual
illustration is possible — ElevenLabs, Artlist and Gamma image generation
are all connected and working — but it spends the account's credits, so it
is a decision rather than something to do unasked. Everything else is in
place to receive it: drop a base64 image into the cover slot and the layout
holds.

**No HOUSE nav tab on any of the five.** They cannot deploy without one,
and it has to come from a generator reading `sites.json`, not another
hand-paste — hand-pasting that component is the documented root cause of
the three-nav-generations mess in `docs/AUDIT-2026-08-12.md`.

**Not deployed.** All five are repo-only. `sites.json` carries no `url` for
them.

**`playbook` (Pattern Decoder) has no source in any repo.** Confirmed
absent, not a lookup failure. If it needs editing it has to be recovered
from the live site first.

**Synonym cycling** is the one no-ai-slop category still unautomated —
detecting it needs semantic judgment a keyword scan can't provide, and a
script returning a false "0" would be worse than no script. Flagged for a
manual read rather than faked.
