# Assessment A: design review of the noblefathercreations.com homepage

Source: `hub/catalogue-redesign.html` (180 KB). Evidence: the `audit/` screenshots listed below plus new phone captures `A-start.png`, `A-doors.png`, `A-workshop.png`, `A-seal-open.png` (live site, 390px).

## 1. Design-specificity verdict: partly specific, mostly a template

**Specific to this author:** the brass-on-ink palette, the wax-seal emblem (`.st-hero-seal`, line 373), the fedora-and-orb figure (`desktop-fold.png`), the real book covers, and the "What brings you here?" picker (`A-start.png`).

**Template:** the hero is the stock luxury-dark arrangement. A watermark wordmark sits behind a centred serif headline with one italic accent word ("The collected *works.*"), followed by a four-number stat strip ("3 / 14 / 3 / Free", `phone-fold.png`). Any author, distillery or tattoo studio could use it unchanged. The headline says nothing about manipulation, coercion, light or dark. The tagline, which is the best line on the site, is set as small italic body text. The glow-in-the-dark idea ("Alive in the dark") is never acted out on the page.

## 2. Nielsen heuristics

| # | Heuristic | Score | Evidence |
|---|---|---|---|
| 1 | Visibility of status | 2 | There is a progress bar, but the active nav pill is wrong: it shows MUSIC while Workshop is on screen (`A-workshop.png`) |
| 2 | Match to real world | 2 | Jargon: "NFC craft lines", "Instruments", "Living tools", "Portals" (`phone-fold.png`) |
| 3 | User control | 2 | The fixed audio and seal buttons cover content (`A-doors.png`, a row is cut to "oing to a festival"). No quick exit |
| 4 | Consistency | 1 | The page numbers Workshop "04"; the seal menu numbers it "02" and Instruments "00" (`A-seal-open.png`, `.nf-num`). The hero says 14 books; the menu footer says "twenty-one volumes". Nav "Art" leaves the page for `/portals` while the other items scroll (line 1518) |
| 5 | Error prevention | 3 | Little to get wrong. Rows in Start Here expand in place |
| 6 | Recognition over recall | 2 | The hero tells people to "tap the seal (bottom right)" instead of showing the way in (`folds.jpg`) |
| 7 | Flexibility | 2 | There is a seal index and a /topics page. No search or filter across 22 entries |
| 8 | Aesthetic and minimalist | 1 | 39.6 phone screens, 3,760 words. The Library alone is 13,362px (`metrics.json`) |
| 9 | Error recovery | n/a | No forms or error states |
| 10 | Help and docs | n/a | A catalogue page; Start Here does the help job |

**Total: 15/32 = 47%, Poor.**

## 3. Cognitive load

Failures, 6 of 8 (high load):
- **Single focus:** four nav pills plus a seal and an audio button compete with the hero.
- **Chunking:** 22 `.st-vol` entries sit in one undivided column.
- **Visual hierarchy:** in the first screen the name appears three times (brand lockup, watermark, eyebrow), but there is no call to action.
- **Minimal choices:** see the list below.
- **Progressive disclosure:** every book shows its full blurb, tags and cover at once.
- **One thing at a time.**

Decision points with more than 4 visible options:
- Top nav: 8 items (Start here, Books, Tools, Music, Art, Workshop, Topics, Support), clipped into a horizontal scroll on phone.
- Start Here: 11 situation rows (`.st-help`).
- Library: 22 volumes.
- Seal panel: 7 sections plus the volume list.
- Choices visible above the fold: 20 on phone, 35 on tablet (`metrics.json`).

## 4. Emotional journey (peak-end)

- **Opening:** atmospheric and slow. Nothing in the first screen says "you're safe, start here."
- **Peak:** "What brings you here?" (`A-start.png`). This is the kindest moment on the page and the right one.
- **Valley:** 13,000px of book entries that all look the same (`phone-strips.jpg`, columns 2 to 6).
- **Second valley:** the Workshop arrives around 19,500px down and opens with a blurry, upscaled pendant image (`A-workshop.png`).
- **End:** donation QR codes, then a footer list. Live also adds a dense changelog in the last column. The visit ends on payment and admin, not on reassurance.

## 5. Strengths

1. The situation-led entry. The 11 `.st-help` rows use plain, human labels ("I hurt someone and want to repair it") and follow the reader's state, not the catalogue's structure.
2. The seal index panel (`A-seal-open.png`) is a well-crafted, on-brand way to browse, with generous tap rows.
3. A coherent material palette (brass `#C9A35B`, wax `#B23A33`) and real, distinct book covers.

## 6. Priority issues

**[P1] There is no front door in the first screen.**
The hero spends a full phone screen on brand and stats, and the only instruction points to an icon. A hurting reader gets no first step.
Fix: replace the stat strip and the watermark with one plain sentence about what this place is for, plus two or three large doors ("I think I'm being manipulated", "Browse the books", "The glowing pendants"). Put the Start Here picker inside the first screen.
Command: `/impeccable distill`, `/impeccable clarify`

**[P1] The Library takes 40% of the page as one column.**
22 entries at roughly 600px each mean scroll fatigue, and the shop is buried. Everything after the Library is effectively invisible on phone.
Fix: make the Library a compact cover grid or shelf with short hooks, and move blurbs to the book pages. Target under 12 phone screens in total.
Command: `/impeccable layout`, `/impeccable distill`

**[P1] Numbering and counts contradict each other.**
00–04 in the menu, 01–05 on the page, Roman numerals for the books, and 14 against 21 volumes. This undercuts trust on a site whose whole argument is pattern clarity.
Fix: use one numbering system, generate every count from `sites.json`, and say "books" in one place only.
Command: `/impeccable polish`

**[P2] Fixed controls cover content and too many targets are small.**
`.nf-seal` and the mute button cover rows (`A-doors.png`). 47 targets are under 44px on phone (`metrics.json`). There is no skip link.
Fix: keep one fixed control, reserve a safe area for it, enforce a minimum 44px target, and add a skip link.
Command: `/impeccable harden`, `/impeccable adapt`

**[P2] The hero is generic.**
Fix: build the moment around the tagline. For example, a light/dark reveal on scroll or tap that shows the pattern hidden in the page, which is literally what the pendants and the books do.
Command: `/impeccable bolder`, `/impeccable overdrive`

## 7. Persona red flags

**Distressed reader on a phone at 1am:**
- Must read past a stat strip about "NFC craft lines" before seeing any help.
- No quick-exit button and no crisis line.
- The ambient audio control and slow parallax add stimulation.
- Eleven choices to sort through while exhausted.
- The 22-book wall forces comparison when they need one book.

**Craft buyer who came for the pendants:**
- Nav "Art" and "Workshop" look like two different things.
- On phone the Workshop sits behind about 19,500px of books.
- The pendant image is soft and low-resolution (`A-workshop.png`).
- No price, availability or "how to get one" on the homepage. The words "price" and "$50" appear once each in the whole source.

**Keyboard and screen-reader user:**
- No skip link (checked by query).
- 139 interactive elements, so 22 "Open the book" links read as duplicates out of context.

## 8. Minor observations

- Four font families: Hanken Grotesk, Fraunces, Space Mono, and Arial as a visible fallback (`metrics.json`).
- Mono labels at 9.5–10.5px with .3em tracking in `#8A8071` (lines 399, 433, 451, 541) are borderline AA and hard to read on phone.
- Blank band above the sticky header after an anchor jump (`A-workshop.png`).
- The top nav clips mid-word ("T…") with no scroll cue (`A-workshop.png`).
- The ghost watermark is cropped on phone ("OBLE FATHE", `phone-fold.png`) and reads as a mistake.

## 9. Questions for the redesign

1. What if the first screen were a single question ("What's happening to you?") and the catalogue came second?
2. Should the books and the shop share one scroll at all, or does the pendant buyer deserve a separate glowing room behind a light-to-dark switch?
3. If the tagline is the brand, what would it look like for the page itself to be "worn in the light, alive in the dark", with a hidden layer the reader uncovers?
