# Homepage final sweep (v19, 2026-11-21)

Tested on iPhone 13, then 1440x900. Evidence: `qa/v19/final/` (scripts, `phone.json`, `desktop.json`, `shots/`).

**Verdict:** every function works and every hard rule passes. Nothing blocks the ship.

## 1. SEO
- **Head:** title is 74 characters (Google shows ~60). Description is 184 characters (cut at ~155). Canonical, og:* (`og.png` is 1200x630) and twitter:card/image are present. No twitter:title or description, but Twitter falls back to og. No noindex anywhere.
- **JSON-LD:** the 1 block parses (WebSite, CollectionPage, Person, Organization).
- **Headings:** the only H1 is "Noble Father Creations", brand only. No heading near the top carries a topic word.
- **Links:** 79 unique hrefs: 13 to /playbook, 8 to /topics, all 200, every anchor present. The 6 local failures (/portals, /press, /resin, /nfc/) are proxied in `_redirects`, so not real 404s.
- **Alt text:** covers and logos use `alt=""`, which is correct because their titles sit next to them. Portals and signature have alt text.
- **robots, sitemap, llms.txt:** robots allows everything; all 8 local sitemaps it names exist. sitemap.xml has 24 URLs, but every lastmod is the build date. Tactic count disagrees: "310" in llms.txt and once on the page, "335" three times; 380 playbook pages ship.

**Top 5 SEO fixes still open**
1. Put the search terms in the H1 and first screen ("Free books on manipulation, narcissistic abuse and gaslighting"); move the brand to the eyebrow. Today the first phone screen reads brand, pendant tagline, four doors (`phone-montage-5000.png`).
2. Add a block of one-sentence definitions (gaslighting, love bombing, trauma bonding, DARVO), each linking to its `/playbook/<slug>` page.
3. A song title with "Fuck" is inline on the homepage. It risks SafeSearch filtering for exactly these readers. Keep the full song list on /music.
4. Use one tactic count across the page, llms.txt and JSON-LD.
5. Use real per-URL lastmod dates; cut the title to ~60 characters and the description to ~155.

## 2. Functions: all pass on phone and desktop
- **Montage:** four doors at full opacity after 3,967 ms (`phone-montage-*.png`); 263 ms with reduced motion. Each door lands its section at top 80px.
- **Chips:** "Someone close to me" gives 3 picks: /feminine, /silence, /playbook (`phone-chips.png`).
- **Door:** a 200 ms tap does not open it; a 950 ms hold does; Enter opens it at once (aria-expanded true, inert removed). Shows 3 books (`phone-door-open.png`).
- **Portal:** hold, then release, gives is-glowing, "Glowing" and a status message (`phone-portal-glow.png`).
- **Catalogue (seal):** 29 links, all 16 books (`phone-catalogue.png`). Escape closes it, focus returns to the seal, the URL stays local.
- **Music:**
  - Nothing plays before a tap.
  - The featured song plays (t=2.38 s).
  - "Show all 176 songs" builds 176 rows; row 61 plays.
  - The now-playing bar's pause and next work.
- **Still:** pauses audio, 0 GSAP tweens left, but the seal's `nf-sealidle` 7 s loop keeps running (`still.mjs`).
- **Leave now:** tap and Esc twice both go to google.com/search?q=weather.
- **Hard rules:**
  - 0 console errors.
  - Only third-party requests: the beacon and the Leave page.
  - No horizontal overflow (scrollWidth = 390 / 1440).
  - Nothing stuck invisible.
  - No target under 44px.
  - 49 keyboard tab stops, all with a visible focus ring.

## 3. Design
Contact sheets: `contact-phone-a.png`, `contact-phone-b.png`, `contact-desktop.png`. Opened-state shots: `phone-states.png`.

| | Score |
|---|---|
| First impression | 4 |
| Hierarchy | 3 |
| Composition and rhythm | 4 |
| Phone ergonomics | 3 |
| Finish | 4 |
| Effect cohesion | 4 |

**Defects, most severe first**
1. **Bottom-right corner covers content.** On phone the seal covers text (`phone-states.png`); on desktop the now-playing bar covers the NFC door (`desktop-frame-00.png`). Fix: bottom padding equal to the bar height plus safe area; dock the seal into the bar while music plays.
2. **About 4 s of artwork with no text and no sign this is a place for help.** Fix: show the H1 and lede at first paint, cap the montage at ~1.5 s, skip it on any tap or scroll.
3. **The hero speaks for the Portals, not the books.** Its tagline is the Workshop's line and repeats at #art. Fix: hero line about the books; keep the tagline for the Workshop.
4. **Duplicate brand.** The header reads "Noble Father" directly above the "Noble Father Creations" H1. Fix: hide the header brand while the H1 is on screen.
5. **Still misses the seal animation.** Fix: `.is-still .nf-seal::after{animation:none}`.
6. **Catalogue duplicates.** The Portals and The Listening Room appear twice, and there is no Topics A to Z entry. Fix: remove the duplicates, add /topics.
7. **Opened song list is very long.** The phone page reaches 25,931px. Fix: 6 songs per shelf, then a "More" link to /music.
