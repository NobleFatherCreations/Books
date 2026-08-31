# The cover marks — visual comparison against Playground Protectors and Wook

Requested twice and not done before this pass: look at the two named
reference books, then give the 5 new books an equivalent stand-out
identity. Screenshotted both live for the first time here.

## What the references actually are

**Playground Protectors** — a full illustrated RPG box-cover: real
character art, a "Friendship Meter" progress bar rendered as game UI, a
physical-book framing device (border, drop shadow), hand-lettered display
type, sparkle decoration, "28 missions · 4 worlds."

**Wook** — *"The PLURth Angels Guide to Spotting a Wook in Sheep's
Clothing"* (the literal source of "sheep's clothing" as a reference point)
— a single full-bleed painted illustration, a psychedelic festival scene,
gradient display lettering, the tagline "PROTECT THE FUCKING MAGIC."

Neither is a typographic system. Both are bespoke cover *illustration*,
and the two are nothing alike except in ambition — a cartoon RPG cover and
a painted festival poster share no visual language at all. What they
share is that each book has an unmistakable, specific visual object at its
front door.

The 5 new books did not have that. They had five palettes and five
typefaces on one shared card-grid page. Distinguishable side by side,
but not a "moment" the way either reference is.

## What was built instead, and why not literal parity

Full painted character illustration or a psychedelic poster would be wrong
for these five specifically — their own briefs call for restraint (*"never
alarmist," "no warmth that could read as absolution," "steady, warm,
unhurried"*) for books about domestic abuse, workplace coercion, and elder
exploitation. That's a real reason, but it's a judgment that should follow
from looking at the references, not a reason to skip looking — which is
what happened the first time.

So: each book now gets a bespoke inline-SVG cover mark, a real visual
concept specific to that book rather than a font swap, in a register that
fits serious nonfiction rather than illustrated fiction:

- **The Long After** — a horizon at dusk, the sun still low rather than
  set. *"Leaving was the middle, not the end."*
- **The Silence** — a single unbroken ring with one narrow gap. The
  brief's own instruction was subtraction; this is the smallest visual
  event that still reads as deliberate.
- **At Will** — a clock face, one hour marked off-schedule, a dashed line
  underneath like a payslip stub. The working file.
- **The Repair** — four ledger rules, one visibly mended with a stitch.
  Chapter 2's own words: *"a record, not an identity."*
- **The Slow Take** — a tangled thread resolving into one straight line
  between two points. A record built entry by entry, out of confusion.

Each uses that book's own CSS custom properties, so it inherits the
palette exactly and works in both themes without a second declaration.

**This is a real escalation, not parity with the references.** Two hand-
painted covers are a different scale of production than five geometric
marks built in code. Naming that gap rather than presenting five SVGs as
equivalent to bespoke illustration.

## A bug the comparison caught

The first version of all five marks referenced generic token names —
`var(--plum)`, `var(--coral)`, `var(--brass)` — copied from *The Long
After*'s palette without checking that the other four books use entirely
different token names (`--steel`/`--signal` for *The Silence*, `--blue`/
`--amber` for *At Will*, `--iron`/`--brass`/`--wax` for *The Repair*,
`--green`/`--gold` for *The Slow Take*). An unresolved CSS variable in an
SVG paint attribute doesn't error — `stroke` silently falls back to its
inherited value (`none`) and `fill` falls back to its initial value
(`black`). Four of five marks rendered as a stray black dot or nothing at
all, and `qa.js` and the Playwright pass both reported clean, because
neither checks whether a custom property actually resolves to a color.
Only caught by opening the screenshot and looking.
