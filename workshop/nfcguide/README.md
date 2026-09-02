# How to Program NFC Tags — Noble Father Creations

A complete, deploy-ready static site teaching anyone how to program NFC tags with the
free **NFC Tools** app by wakdev, on iPhone and Android.

**139 recipes.** One searchable, filterable, deep-linkable index. Zero dependencies,
zero build step, zero network requests, zero trackers, zero cookies.

---

## Deploy to Netlify

### Drag and drop (fastest)

1. Zip the contents of this folder so that **`index.html` sits at the root of the zip**,
   not inside a wrapper directory. From inside `nfc-guide/`:
   ```sh
   zip -r ../nfc-guide.zip . -x '.*' -x '__MACOSX/*'
   ```
2. Go to <https://app.netlify.com/drop> and drag the zip in.
3. Done. Netlify serves it immediately.

### From Git (better — redeploys on every push)

1. In Netlify: **Add new site → Import an existing project**, pick this repo.
2. **Base directory:** `nfc-guide`
3. **Build command:** leave empty
4. **Publish directory:** `nfc-guide`
5. Deploy.

`netlify.toml` already sets the security headers (CSP, nosniff, referrer policy,
permissions policy), long-cache for `/assets/*`, and the catch-all 404.

### After the first deploy

Nothing. Every placeholder the first draft shipped with is filled in and
verified: `og:url`/`og:image`, `robots.txt`, `sitemap.xml`, the three cards at
the foot of section J, the House tab, and the footer links. A
`grep -rn "REPLACE" .` returns no hits, and that is the state to keep it in --
this site is proxied at a real address and a `#REPLACE-` anchor is a dead link
in production.

Where they point now:

| Was | Now |
|---|---|
| `og:url` / `og:image` / sitemap / robots | `https://noblefathercreations.com/nfc/` |
| `#REPLACE-shop` | `/portals` |
| `#REPLACE-custom` | `mailto:dapperdadnfc@gmail.com` |
| `#REPLACE-library` | `/#library` |
| `#REPLACE-house` | the hub, plus the real catalogue drawer (below) |
| `#REPLACE-instagram` | replaced with the email -- **no Instagram URL exists in the repo.** If there is one, put it back as a footer row |

---

## The file layout

```
nfcguide/
├── index.html                 ← the whole site. CSS, JS, SVG, fonts, the
│                                seal, the icons and all 16 screenshots are
│                                inlined. 139 recipes. Nothing else is needed
│                                to render the page.
├── 404.html
├── netlify.toml
├── robots.txt
├── sitemap.xml
├── README.md
├── SCREENSHOT_SHOTLIST.md
└── assets/                    ← still deployed, but index.html asks for
    │                            none of it
    ├── logo-seal.png          ← the source the inliner reads
    ├── apple-touch-icon.png
    ├── favicon.png
    ├── og-image.jpg           ← share card; og:image needs a real fetchable
    │                            URL, so this one has to exist as a file
    ├── wordmark.jpg           ← spare
    ├── fonts/                 ← the OFL licences, which must ship with the
    │                            embedded fonts, and charset.txt
    └── screens/               ← the screenshot sources the inliner reads
```

**`index.html` has no relative references at all, and that is load-bearing.**
It is served through the main domain at `/nfc`, and a relative path there
resolves against whatever the address bar says — with or without a trailing
slash, two different answers. As a directory this page broke at `/nfc`, where
`assets/screens/x.png` resolved to `/assets/screens/x.png`, a prefix The
Casting owns on that domain: the page loaded and looked almost right, with
every screenshot silently gone.

Netlify can't fix that in `_redirects` — it strips a trailing slash from a
rule's source, so `/nfc → /nfc/` matches `/nfc/` too and loops; and it prefers
a real file to a rewrite, so a redirect page at `nfc.html` captured `/nfc/`
and broke the working form instead. Both were tried. Inlining is what works,
and it is also what every book on the site already does.

So: **edit `index.html` directly** for anything textual, but if you change the
seal, an icon or a screenshot, edit the file in `assets/` and re-run the
inliner from the repo root:

```sh
python3 scripts/nfcguide-inline.py
```

It is not idempotent — it asserts on the original markup and will refuse to
run against an already-inlined file. Restore `index.html` from git first.

## Adding a recipe (under a minute)

Find `var RECIPES = [` near the top of the `<script>` block and add one object.
**Only five fields are required** — `norm()` fills in everything else:

```js
{id:"my-new-thing", title:"My New Thing", blurb:"One line on what it does.",
 cat:"Social & Profiles", template:"https://example.com/YOUR_THING"},
```

That alone gives you a card in the index, a working search entry, a detail view, a
`#/r/my-new-thing` deep link, a copy-to-clipboard value, an automatic byte estimate,
a will-it-fit meter, and a print sheet.

Optional fields, all shorthand:

| Key | Default | What it does |
|---|---|---|
| `rec` | `"URL / URI"` | the exact record type as NFC Tools names it |
| `plat` | `["android","ios"]` | `["android"]` for Android-only, etc. |
| `diff` | `1` | 1 easy · 2 medium · 3 advanced |
| `bytes` | estimated from `template` | override the byte estimate |
| `get` | — | array: where to find the real value |
| `tips` | — | array of tips |
| `got` | — | array of gotchas |
| `tag` | `"NTAG213 is plenty."` | tag recommendation |
| `scr` | the URL write flow | array of screen names |
| `ios` | — | a note about how iPhone differs |
| `verify` | `false` | flags the "verify on your device" badge |

`cat` must be one of the strings in `CATS` — add a new one there and a filter chip
appears automatically. The `139` counts in the prose are read from the array length,
so they update themselves.

---

## Swapping the logo

The mark is `assets/logo-seal.png` — a transparent PNG so it sits on any ground. It is
used in the top bar, the hero, the footer, the 404 page and the print header.

To swap it, replace that file (keep the name, keep it square, transparent background).
If you have an SVG, save it as `assets/logo-seal.png`'s replacement and update the four
`<img src="assets/logo-seal.png">` references — a plain find-and-replace.

In light mode the mark is inverted by a CSS filter (`.hero .sealwrap img`). If your
replacement is already dark-on-transparent, delete that filter rule.

---

## Typography

| Family | Weight | Role |
|---|---|---|
| **Fraunces** | 700 / 900 | The wordmark and every heading |
| **Hanken Grotesk** | 400 / 600 / 700 | Body copy, UI chrome, labels |
| **Space Mono** | 400 | Section letters, counts, the catalogue rows |

All three are SIL Open Font License 1.1, and all three are the Noble Father
house faces -- the same pairing the hub, every book and both craft sites use.
They are **subset to the glyphs this page actually uses** (65KB of font data
total, against ~600KB for the full variable files the books inline) and
base64-inlined into `index.html`. Re-cut them with
`python3 scripts/nfcguide-fonts.py` from the repo root.

That is deliberate, not laziness: browsers block same-origin font *files* loaded over
`file://`, so an external `.woff2` would silently fail whenever the page is opened
straight from disk — and offline-from-the-filesystem is a requirement here. Data URIs
always work, cost zero network requests, and eliminate any flash of unstyled text.

Reference copies, both licences, and re-subsetting instructions are in
`assets/fonts/README.md`. **If you add a recipe using a character outside basic Latin
and the listed punctuation, the fonts need re-subsetting** — the instructions are there.

Only three weights ship. If you need another, add the `@font-face` rather than relying
on the browser to synthesise it (faux-bold on a Didone looks bad).

---

## Navigation

One `SECTIONS` array near the bottom of the script drives **three** views of the same
map, so they can never disagree:

- the **lettered rail** (A–J) — fixed at the left edge on screens ≥1420px, mirroring the
  printed guide's section tabs, with the section name on hover
- the **drawer** — the same list, opened by the burger on screens ≤760px
- the **top-bar links**

A single `IntersectionObserver` scrollspy marks the current section with
`aria-current="true"` in all three at once. Add a row to `SECTIONS` and every one
of them picks it up.

Also: a reading-progress hairline under the top bar, a back-to-top button after one
viewport of scroll, prev/next recipe buttons inside every detail sheet, and `/` to
jump to search.

**THE HOUSE catalogue drawer** is separate from all of that. The wax seal in the
bottom-right corner opens the same twenty-volume drawer every Noble Father page
carries, generated from `scripts/nf-catalogue.py` and installed by
`scripts/nfcguide-chrome.py` -- never hand-edited here. Note the deliberate
asymmetry: this guide links out to all twenty, but is **not** listed in their
drawers. Only the hub features it.

---

## Motion

All of it is opt-in and fails safe. Content is **visible by default**; the script adds
`.js-motion` to `<html>` only when `prefers-reduced-motion` is *not* set, and only then
do the reveal rules apply. If the script never runs, nothing is ever hidden.

- sections and grids fade up on scroll (grids stagger their children, capped at 320ms)
- the hero seal sits in three slowly expanding rings — the radio field, made visible
- the detail sheet rises on mobile and scales in on desktop
- cards lift on hover; arrows nudge forward

Anything already scrolled past is shown instantly with no delay, so scrolling back up
never re-animates old content. A 2.5s failsafe reveals everything if the observer never
reports.

To strip the motion entirely, delete the `motion()` IIFE — the CSS is inert without the
`.js-motion` class.

---

## Adding real screenshots

**Sixteen real captures ship**, covering the whole write flow and every common
record type. The remaining ten screens render as hand-drawn SVG diagrams.

**Drop a PNG into `assets/screens/` with the right filename, re-run
`python3 scripts/nfcguide-inline.py`, and it replaces the drawing.** Delete it,
re-run, and the drawing comes back. The lookup the page uses is built from
whatever is in that folder at the time — a name with no capture falls through
to its hand-drawn SVG, and never requests a file that isn't there.

See `SCREENSHOT_SHOTLIST.md` for every filename, what should be on screen, capture
instructions, and which five to take first.

---

## What's in the box

| Section | |
|---|---|
| **A** | What's actually inside your piece |
| **B** | iPhone vs Android — where the antenna is |
| **C** | Get the app |
| **D** | The Universal Write — the five steps every recipe shares |
| **E** | Ten ideas to get you started |
| **F** | The index — 139 searchable recipes |
| **G** | Choose your tag — capacity, form factors, on-metal |
| **H** | Locked vs unlocked |
| **I** | Troubleshooting — 12 failure modes |
| **J** | Made by Noble Father Creations |

Plus: `#/r/<id>` deep links with a working back button, a copy-link button per recipe,
`@media print` one-page instruction sheets, `HowTo` and `FAQPage` structured data, full
Open Graph and Twitter cards, a session-only light/dark toggle, and `/` to focus search.

---

## Verify these before you publish

### Store links

Both are marked with an HTML comment near them in `index.html`. Store listings move —
confirm both still resolve to **NFC Tools by wakdev**:

- iOS — <https://apps.apple.com/app/nfc-tools/id1252962749>
- Android — <https://play.google.com/store/apps/details?id=com.wakdev.wdnfc>

### Recipes flagged "verify on your device"

These 15 recipes carry a visible **verify** badge because platform behaviour has changed
between OS versions and we would rather flag that than state it as fact. Each is worth
testing on a spare tag before you rely on it:

- **SMS with a Message Ready** (`#/r/sms`) — pre-filled SMS body behaviour differs across iOS versions.
- **Signal** (`#/r/signal`) — Signal contact-link format has changed between app versions.
- **Google Review Link** (`#/r/google-review`) — Google has changed the review short-link format more than once.
- **Bluetooth Pairing** (`#/r/bluetooth-pairing`) — Android-only, and support varies widely by phone and device.
- **Smart Home Scene** (`#/r/smart-home-scene`) — every smart-home platform does this differently, and they change.
- **Custom URL Scheme** (`#/r/custom-url-scheme`) — app URL schemes are largely undocumented and can vanish in an update.
- **Toggle a Device Setting** (`#/r/toggle-setting`) — newer Android restricts what an app may toggle without a prompt.
- **Start a Timer** (`#/r/start-timer`) — system-action support varies by Android version.
- **Set an Alarm** (`#/r/set-alarm`) — system-action support varies by Android version.
- **Bedtime Routine** (`#/r/bedtime-routine`) — depends entirely on Tasker / Shortcuts being set up.
- **Work Mode Routine** (`#/r/work-mode`) — depends entirely on Tasker / Shortcuts being set up.
- **Raw GPS Coordinates** (`#/r/gps-coordinates`) — some phones handle the raw geo: record inconsistently.
- **Add to Calendar** (`#/r/calendar-event`) — .ics links open, download, or do nothing depending on the phone.
- **Password-Protect a Tag** (`#/r/password-protect`) — password support varies by chip type.
- **MIME Type Record** (`#/r/mime-record`) — only an app registered for that MIME type responds.

### Deliberate honesty

Byte counts are **estimates**, and the site says so. NDEF overhead varies by record type
and by chip. They are accurate enough to answer "will this fit", which is the only
question they claim to answer.

---

## Constraints this site holds to

- One `index.html`. All CSS, JS, SVG, fonts **and images** inline — zero
  relative references, so it renders correctly at any path it is served from.
- Vanilla JS, ES2019. No framework, no bundler, no npm, no CDN, no hosted fonts.
- Works fully offline, including opened directly from `file://`.
- No network requests of any kind. No analytics, no trackers, no cookies.
- `localStorage` is not used at all — the theme toggle is session-only.
- Minimum tap target 44px; no font size below 12.4px.
- Semantic landmarks, ordered headings, `:focus-visible` rings, a focus-trapped dialog,
  a skip link, alt text on every image, titles on every SVG.
- Respects `prefers-reduced-motion` and `prefers-color-scheme`.
- No horizontal overflow at 320px through 1920px.
- Motion is opt-in and fails visible; `prefers-reduced-motion` disables all of it.

---

## Credits

Noble Father Creations · NFC Digital Experiences · Dapper Dad
Made by Shae. Programmed by you.

NFC Tools is made by wakdev and is not affiliated with Noble Father Creations.
