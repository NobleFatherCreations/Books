# Design pass — the four new books

*Run 2026-08-30.* The rule in `CLAUDE.md` is the one that shaped this:
**never apply a design pattern uniformly across all the books — check each
book's own content and stance first.** These four arrived on one template
with four palettes swapped in. The palettes were good and are unchanged.
Everything else came from reading each book's own brief.

## What was wrong before the pass

**They rendered in whatever serif the reader's OS happened to have.** All
four declared `'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book
Antiqua', Georgia, serif` and shipped no `@font-face` at all. On a Mac that
is Iowan Old Style. On Windows it is Georgia. On Android it is whatever the
system serif is. The typography the author was designing against was not
the typography most readers were getting, and self-hosting is a house rule
besides.

**Four books, one layout.** Same masthead, same hero shape, same pill row,
same card grid. The only differences were colour and the logo mark.

**Two regressions I introduced earlier in this session.** The quick-exit
note went in as a full-width monospace paragraph directly above the
buttons and became the loudest block on the contents screen — on mobile it
ran to eight lines. And adding a help button took the button row to six or
seven equal-weight buttons wrapping onto three lines.

## Typefaces, self-hosted

Variable fonts are instanced before subsetting — optical size pinned,
weight kept as a range — then subset to the characters that book actually
renders. On Newsreader that is 76 KB → 21 KB for identical glyphs, because
on a small subset the unused variation machinery is most of the file. Each
family is declared once with a weight range, which is structurally
incapable of the bug `MEMORY.md` records (one family inlined three times at
discrete weights with byte-identical blobs).

| book | face | why | cost |
|---|---|---|---|
| The Long After | Newsreader | Warm and literary with a real italic, for the most patient voice in the library. | 62 KB |
| The Silence | Source Serif 4 | Plain and sturdy. The brief asks for *less* literary, on purpose. | 55 KB |
| At Will | Spectral | A screen serif with a documentary edge, for a book about contracts and records. | 55 KB |
| The Repair | Crimson Text | A sober book serif with no warmth anywhere that could read as absolution. | 65 KB |

IBM Plex Mono throughout for labels and numerals — the one shared element,
because it is the library's UI voice rather than a book's own.

## The four identities

Each is derived from the book's own brief, quoted in the CSS beside the
rules it produced.

**The Long After — time passing.** The book covers years and is read
slowly, re-read, "often opened at 2am." So it gets the loosest leading and
the most air of the four, a hero that breathes across two lines with the
italic intact, and movement breaks drawn as a horizon: a rule that fades
out at both ends rather than stopping. It keeps the card grid — this is the
one book where a soft, held container is right.

**The Silence — plainness as the design.** Its brief is explicit: less
literary on purpose, "a friend giving him a straight answer," never
"brave." So the ornament comes off rather than going on. No italic in the
hero. No cards — chapters are a plain ruled list. Tighter measure. The
restraint is the identity, and it is the only one of the four where the
design argument is subtraction.

**At Will — the file.** Contracts, records, grievances, process, and a
method of "teach the category, route the specifics." So: a rule under the
masthead like a form header, movement titles underscored in full ink,
chapters as filed rows with the number in the margin. Orderly rather than
cold — the reader is in a car park before a shift — because order is the
thing this book is actually handing over.

**The Repair — the ledger.** Chapter 2 writes the design brief itself:
*"That is a record, not an identity."* So the page is a ledger. Hairline
rules, numerals in their own column, every radius squared off, nothing
raised off the surface, and the accent reserved for danger. The book's
brief forbids warmth that could be mistaken for absolution, and that
applies to the design as much as the prose.

## Also fixed

- The exit note is now one dimmed monospace line below the buttons, where
  a footnote belongs, and it brightens on hover.
- Two buttons per book — start reading, or get help now, which are the only
  two decisions the reader actually has on this screen. The other four
  routes became a quiet line of text links under them.
- Read time moved out of its own line into a right-hand column on the three
  list-style books, which is what a table column is for and takes about a
  third off the height of every row. It drops back under the title below
  560px.

## Verified

Playwright at 375px with touch and at 1440px, in normal and reduced motion,
across every route, plus dark mode and the mobile contents screen read
directly rather than assumed. Zero console errors, zero horizontal
overflow, nothing stuck at `opacity:0`. Still no external requests of any
kind: every face is embedded base64, and each book's own `qa.js` fails the
build on an external URL.
