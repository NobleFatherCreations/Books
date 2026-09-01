# The five new books — what's done, what's left

Updated 2026-09-01: **all five are live.**

Every "done" line below was verified by opening the page and looking at
it, not by a passing check. That distinction is the
whole reason this file exists: `qa.js` and the Playwright verifier both
reported clean on a build where four of five cover marks rendered as a
stray black dot, and again on a build where a quoting bug broke the entire
script. Structure checks cannot see a page that renders nothing.

## Done

| | Long After | Silence | At Will | Repair | Slow Take |
|---|---|---|---|---|---|
| Own body typeface, self-hosted | Newsreader | Source Serif 4 | Spectral | Crimson Text | Hanken Grotesk |
| Own display face for headings | Instrument Serif | Young Serif | Bricolage | Anton | Outfit |
| Own cover art, author + seal | horizon at dusk | gapped ring | clock face | mended ledger | thread |
| Own card language | rounded, filled | hairline rule | squared, ruled edge | ledger rule | rounded, filled |
| Section mark on every heading | ✓ | ✓ | ✓ | ✓ | ✓ |
| A−/A+ reader text scaling | ✓ | ✓ | ✓ | ✓ | ✓ |
| Quick exit (Esc + Leave) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `#/help` routing page | ✓ | ✓ | ✓ | ✓ | ✓ |
| Scroll-verified, both themes, 390 + 1200px | ✓ | ✓ | ✓ | ✓ | ✓ |
| Zero external requests | ✓ | ✓ | ✓ | ✓ | ✓ |
| THE HOUSE catalogue drawer | ✓ | ✓ | ✓ | ✓ | ✓ |
| Live on noblefathercreations.com | ✓ | ✓ | ✓ | ✓ | ✓ |

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

**`playbook` (Pattern Decoder) has no source in any repo.** Confirmed
absent, not a lookup failure. If it needs editing it has to be recovered
from the live site first.

**Synonym cycling** is the one no-ai-slop category still unautomated —
detecting it needs semantic judgment a keyword scan can't provide, and a
script returning a false "0" would be worse than no script. Flagged for a
manual read rather than faked.

**This repo is behind live for the older projects.** Found while deploying:
eight live sites carry Cloudflare Web Analytics added 2026-08-15 that
exists nowhere here, the Listening Room is live at v4 against v2 in the
repo, the Portals carry CSS fixes the repo lacks, and the reaction map's
live file is a different build entirely. This round worked around it by
patching the live HTML rather than overwriting it
(`scripts/nf-patch-live.py`), but the repo copies are still stale. Someone
should decide deliberately whether to pull live back into the repo. See
`MEMORY.md` under 2026-09-01.

## Shipped 2026-09-01

**Cover art.** Each book has real generated cover art (Artlist), composited
locally with **Shae Stovell** as author and a small NF wax-seal watermark
in the site's own seal colours. Two crops per book: the wide banner inside
the book, and a portrait jacket for the hub's shelf, which uses a 1:1.42
book face that would have cropped the banner to its middle third.

**THE HOUSE nav, generated not pasted.** All five carry the catalogue
drawer, built by `scripts/nf-install-chrome.py` from
`scripts/nf-catalogue.py` — the generator the previous entry asked for.
The same generator repaired the existing pages, where the nav had drifted
to 11/12/13/15/21 rows with two different volume counts.

**Live.** All five at `noblefathercreations.com/longafter|silence|atwill|
repair|slowtake`, each on its own Netlify site proxied at a clean path.
`sites.json` carries their URLs and site IDs.

One adaptation worth knowing about: the drawer's Escape handler runs in the
capture phase and stops the event. These books bind Escape to an emergency
exit that blanks the page, so without that, closing the catalogue would
also have triggered it. Both behaviours are verified in a browser.
