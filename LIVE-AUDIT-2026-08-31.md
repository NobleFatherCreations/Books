# Live audit — every hosted page, 2026-08-31

19 pages: the hub, 12 book projects, 5 craft/business sites, the reaction
map. Supersedes nothing in `AUDIT-2026-08-12.md`; several items from that
audit are confirmed fixed below.

## Method, and what it cannot tell you

Headless Chromium could not reach the live sites through this session's
agent proxy — `ERR_CONNECTION_RESET` on every navigation — while `curl`
through the same proxy worked. So: **`curl` each page to disk, then run the
browser checks against the local copies.** Each page was loaded at 375px
with touch and at 1440px, in normal and reduced motion, scrolled a screen
at a time with 420ms to settle at each stop.

This audits **the bytes the server actually delivered**, which is where
almost everything below lives. It does **not** audit server-side routing,
redirects, or cross-origin asset delivery — anything of that kind was
checked separately with `curl` against the live origins and is marked as
such.

Two corrections I made to my own method before reporting anything, because
both would have produced confident nonsense:

1. **A naive "stuck at `opacity:0`" check reports hundreds of false
   positives on any scroll-reveal page.** The first run claimed 329 stuck
   elements on the children's book. Scrolling one screen at a time, letting
   each settle, and counting only what is *in the viewport* gives 1. A fast
   scroll followed by a single count measures "hasn't been scrolled past
   yet," not "broken."
2. **`data-here` is not a leaked placeholder.** A leak scan flagged
   `data-here=` on loop and scale. It is a real attribute marking which
   project the page is so the nav drawer can highlight it, and it is
   present in the repo's own byte-verified fix files. Do not re-open it.

---

## 1. The finding: 16 of 19 pages load third-party analytics, and six of
them tell the reader they don't

Every page carries
`<script src="https://static.cloudflareinsights.com/beacon.min.js">`.

For loop and scale this is now the **only** difference between what is live
and the repo's verified `fixes/` — 229 bytes appended at the end of each
file. (Which also confirms the original build-comment leak, the thing that
started this whole project, is gone: it was deployed 2026-08-05 and a byte
diff of live against `fixes/` shows nothing else differs.)

Three separate problems, in increasing order of seriousness:

**It breaks the architecture rule.** `CLAUDE.md`: *"no dependencies, no
external requests… Never add a CDN `<script>` or `<link>` tag."*

**It breaks offline capability.** Every one of these books is supposed to
work from a saved file with no network. They still render, but they now
make a request on every open.

**Six pages promise the reader the opposite, in their own body copy:**

| page | what the page says | loads the beacon |
|---|---|---|
| **faith** — The Coercive Control Codex | *"no analytics, no tracking, no external requests… it will not measure you"* | yes |
| **music** — The Listening Room | *"no external requests, no tracking"* | yes |
| **loop** | "No tracking · Nothing stored" + *"no analytics, no tracking"* | yes |
| **scale** | "No tracking · Nothing stored" + *"no analytics, no tracking, nothing stored"* | yes |
| **children** — Playground Protectors | "no tracking" | yes |
| **hub** | "No tracking" | yes |

These are books about coercive control and manipulation, and the Codex is
explicitly designed for readers who may be monitored at home. A
third-party request on page load is a record that a particular device
visited a domestic-abuse resource. That is a different category of problem
from a style-guide violation, and it is why this is first.

### Where it comes from is only half established

- It **is** in the repo source for The Casting — `casting/index.html` and
  every `casting/statues/*/index.html`, added by commit `8625710`
  *"Add Cloudflare Web Analytics site-wide."*
- It is **not** in the repo source for any book. The books have no repo, and
  the verified `fixes/` files do not contain it.

So on the book pages it is either baked into what was deployed, or injected
at the Cloudflare edge for the whole zone. **That distinction decides the
fix** — editing and redeploying 12 sites, versus one toggle in the
Cloudflare dashboard — and I have not confirmed which. Check the zone's
Web Analytics setting first; if it is on there, nothing needs redeploying.

**Not changed.** Removing analytics from a live site is a production write
and this repo's rules require a go-ahead for those. The finding is
documented and nothing was touched.

---

## 2. Confirmed fixed since 2026-08-12

- **The Casting through the hub proxy works.** Every real asset and data
  path returns 200 both on its own origin and through
  `noblefathercreations.com/resin` — `/data/statues.json`,
  `/data/facets.json`, `/data/site.json`, `/assets/css/theme.css`,
  `/assets/js/facets.js`, `/assets/js/gallery.js`. The scoped `_redirects`
  rewrites are doing their job.
  *(I first reported a 404 here. It was on filenames I had guessed —
  `pieces.json`, `index.json`, `app.js` — none of which exist. Checked
  against the real file list before reporting.)*
- **The build-instruction leak is gone** from loop, scale and faith.

## 3. Still open from 2026-08-12

- **Three nav generations still ship simultaneously.** The old `nh-*` side
  tab is still live on **loop, scale and playbook**; the rest carry the
  current `nf-seal` coin. The root cause in that audit stands: the nav is
  hand-pasted per page instead of generated from `sites.json`, which
  `CLAUDE.md` already forbids.
- **The old "All Fracture" name is still live** on three sites the rename
  never reached: `noble-nfc-tour`, `nfchq`, and the reaction map.

---

## 4. New: three visible build notes shipped on noble-nfc-tour

`noble-nfc-tour.netlify.app` shows this to readers, three times, in three
different sections:

> **Full section text arriving in the next pass — placeholder so the scroll
> stays whole in the meantime.**

Under *The living tools*, *The music*, and *The art portfolios*. This is
the exact class `CLAUDE.md` forbids — and it is worse than the leak that
started this project, because that one was an HTML comment and this is
visible body text on the page.

**Not the same thing, and left alone:** `noblenfcseals` says *"Catalogued ·
full photography coming soon"* on individual pieces. That is honest
reader-facing status on a catalogue, not a build note. It stays.

## 5. New: three sites make external font requests

`nfchq` and `noble-nfc-tour` load Cormorant Garamond and Albert Sans from
`fonts.googleapis.com`; The Casting loads Fraunces the same way; the
reaction map does too. Same architecture rule as the beacon, lower stakes
— these are craft/business pages, not books read by monitored people — but
the fix is the same one already tooled for in this repo
(`scripts/embed-fonts.py`, and `tools/fonts/` has all four families
vendored already).

## 6. Structural checks — all 19 pages clean

Every page has a `lang` attribute, a viewport meta, and a non-empty
`<title>`. No dead in-page anchors. No horizontal overflow at 375px or
1440px. No text rendered the same colour as its background.

## Per-page summary

| page | beacon | old nav | old name | placeholders | ext. fonts |
|---|---|---|---|---|---|
| hub | ● | | | | |
| loop | ● | ● | | | |
| scale | ● | ● | | | |
| playbook | ● | ● | | | |
| faith | ● | | | | |
| fracture | ● | | | | |
| fractal | ● | | | | |
| feminine | ● | | | | |
| children | ● | | | | |
| shadowroot | ● | | | | |
| wook | ● | | | | |
| music | ● | | | | |
| festival | ● | | | | |
| nfcportals | ● | | | | |
| noblenfcseals | ● | | | | |
| noble-nfc-tour | | | ● | ● | ● |
| nfchq | | | ● | | ● |
| The Casting | ● | | | | ● |
| reaction map | | | ● | | ● |

## What I would do first

1. **Check the Cloudflare zone's Web Analytics setting.** If the beacon is
   injected at the edge, one toggle fixes 16 pages and nothing needs
   redeploying. If it is not, this is a 12-site redeploy and worth
   scheduling deliberately. Either way, `faith` and `music` should stop
   claiming "no external requests" until it is off — the claim being false
   is worse than the request.
2. **Pull the three build notes off noble-nfc-tour.** Small, isolated, and
   it is the rule this project was started to enforce.
3. **The nav generator.** Three generations still shipping simultaneously
   is the 2026-08-12 root cause, unfixed, and it is also what blocks the
   five new books from deploying — they have no HOUSE tab and hand-pasting
   one is what created this problem in the first place.

**Nothing on any live site was changed.** Every item above is a production
write; this repo's rules require a go-ahead for those.
