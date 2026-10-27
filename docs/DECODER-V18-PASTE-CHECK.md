# The pasted "v18 13 Gates Matrix" spec, checked line by line against live v17 (2026-10-27)

The owner pasted a v18 directive (an HTML/CSS template, a robots.txt, and three "master prompts"). This file records
what it asks for, what v17 already does, what was adopted in v18, and what was refused, with the reason. A reviewer can
use it to check that nothing was dropped.

## Already live in v17 (nothing to do)

| Asks for | Where it already is |
|---|---|
| No React, Tailwind, Framer or npm; keep the Python single-file build | That is the architecture: `design/build-decoder-v15.py` |
| Remove `noindex`; descriptive titles | v16. `<Tactic>: Signs, Examples and What to Do · Pattern Decoder` (the owner chose to keep this format on 2026-10-27) |
| JSON-LD `DefinedTerm` per tactic | v16. On each of the 310 plain pages, and in the app per route via `seo()` |
| robots.txt inviting AI crawlers, plus a sitemap | v16. Root `robots.txt` names 11 AI agents; two real sitemaps (the pasted `Sitemap: https://noblefathercreations.com` is not a sitemap) |
| Matte void #050507, obsidian #0E0E12, champagne #E5C158 | v17 tokens |
| Plain-language "shunting" search ("they blamed me" gives Blame-Shifting) | The v14/v15 search engine; measured on live |
| Safety note before the answer on the 105 sensitive entries | Built into the station page and the plain pages, and checked by the suite |
| A quick-exit button that replaces the page | The green Leave button (top right, every page, Escape twice), which also unwinds history, sends no referrer and clears memory |
| Thumb-zone controls | A bottom sign bar of four doors on phones, plus a step dock; see v18 below for station prev/next |
| Run the build, the regression suite and axe-core | Done every round |

## Refused, with reasons

| Pasted item | Why it was not used |
|---|---|
| `maximum-scale=1.0, user-scalable=no` | Blocks pinch zoom. It fails WCAG 1.4.4 and harms low-vision readers, the core audience. |
| `* { user-select: none }` | Readers could not copy the "Words you could use" scripts or quotes to keep. |
| `body { height:100vh; overflow:hidden }` and an absolutely positioned card | Entries run to many screens of text. Locking the page would cut content off, and `100vh` is the mobile browser-bar bug the spec says it fixes. |
| 9–11px labels, `font-weight:300` body at 14–15px, `rgba(255,255,255,.25)` labels | Below legibility and contrast minimums (the v17 floor is 13px for labels and 18px body, AA everywhere). |
| Labels tracked to 0.2–0.4em in capitals | Hard to read for stressed readers; v15 limits tracked capitals to two places. |
| `--silvergray: #9A9A1A` | This is olive, not grey (probably a typo for #9A9A9A). v17 uses #A8A69E. |
| Crimson "Quick Exit" pill | Red now means danger. A red exit would blur the safety signal, and the owner kept the green Leave. |
| Font `Inter` / `SF Pro Display` | Neither is embedded, so they would fall back unpredictably or need an outside request. v17 embeds Overpass and Atkinson Next. |
| 24–28px card radii, `box-shadow: 0 40px 80px` drop shadows | These break the v15 shape language (square signs, round stations) and its no-drop-shadow rule. The look stays matte and flat by design. |
| Grain overlay SVG | The data URL in the paste is malformed and would draw nothing. See v18 for a working, static, opt-out texture. |
| Canonical `https://noblefathercreations.com{line_id}&tactic={tactic_id}` | Not a valid URL (missing path and `?`). Live canonicals point at real pages, `/playbook/<slug>`. |
| `"name": "The 13 Gates of Perception - Line {roman}"`, "Pattern Decoder Matrix" | The owner kept the name "Pattern Decoder". Lines are lettered (T, G, C…), not Roman-numbered. |
| `{tactic_exit}` "Sovereign Exit Blueprint" | No such field exists in the content. The real "What you can do" step (script, five response options, safety caveat) is already shown. Inventing exit advice for a safety guide is refused. |
| A one-card PREV / [MATRIX] / NEXT deck as the whole interface | It would drop search results, the guide, compare, the map and the four steps, and turn 1,700-word entries into a scroll-locked card. See v18 for the parts adopted. |
| `max-w: 500px` | Not a CSS property (a Tailwind leftover), so the browser ignores it. |
| Sequential Thinking before coding | Configured in `Books/.mcp.json`, but it only loads in a session started inside `Books/`, and this session did not start there. Planning was done in-context. |

## Adopted in v18 (what shipped)

- **Thumb zone:** while reading a station on a phone, the step dock alone holds the bottom edge; scrolling up brings back
  the doors and Back to top. This is the paste's "thumb-arc controls", without replacing the four doors.
- **Calmer chrome:** the dock and Back to top are obsidian with gold accents, so gold marks only what to press.
- **Less clutter before reading:** Save · Listen · Text size · More (Share, Print).
- **"Background mutes":** the map behind the station sheet blurs (off under reduced transparency).
- **Compare on phones:** one labelled column; a stray quote mark fixed.
- **Day theme:** true champagne gold with dark ink.

Not adopted after review:
- static grain (the critique found the page already decorative enough);
- the single-card PREV / MATRIX / NEXT deck (it would drop the steps, search results and compare);
- gold "you are here" code plates (the critique found the plate already says little to readers; making it louder would
  not help).
