# Homepage v18: consolidated design review (read-only)

Method: I read each skill and ran it as its own pass. On top of the existing QA shots I made new Playwright measurements at 390, 1024, 1280, 1366 and 1440, with and without reduced motion. My shots are in `scratchpad/rev/`.

Clean results:
- External hosts: only the Cloudflare beacon.
- 0 console errors and 0 overflow.
- No contrast fails under 4.5:1.
- No tap targets under 44px.
- Every image has an alt and width and height.
- No `transition: all`.
- Nothing is stuck at opacity 0.
- taste `copy-lint`: 0 FAIL, 0 WARN.
- taste `consistency.mjs` crashed in undici (`assert(!this.paused)`), so it was not run.

## Changes, by impact

1. **MUST: the hero cover is cut in half at rest.** Raised by polish, audit and overdrive ("polish is the difference").
   - Evidence: at scroll 0, the blank `.book3d .inside` page paints over the left third of the cover, even though `#hero-face` is `matrix(1,0,0,1,0,0)`. See `rev/stage-now.png`, `rev/d-fold.png` and `rev/m-rm-fold.png` (reduced motion too).
   - Ruled out: `translateZ(-8px)`, `transform-style:flat` and turning off the blend mode all leave it broken. `display:none` on `.inside` fixes it (`rev/stage-tests.png`).
   - Change: `.book3d .inside{visibility:hidden}`. Show it only while the face is turned: in the `#hero-face` scroll tween, add `onUpdate: s => inside.style.visibility = s.progress > .02 ? 'visible' : 'hidden'`. Do the same during `swapCover`.
   - Re-check on a real GPU afterwards.

2. **MUST: the first screen cuts off the chips.** Raised by taste §5 "first screen… main button inside it" and refactoring-ui hierarchy.
   - Evidence: the last chip's bottom edge is at 883 on a 390×844 screen, 791 on 1366×768 and 764 on 1280×720.
   - Phone (≤900px): set `.stage{height:224px}`, `.book3d{width:124px}`, `.halo{width:240px}` and `.hero{padding-top:var(--s2)}`.
   - Desktop: change to `--t-h1:clamp(46px,min(6.6vw + 14px,10.5svh + 20px),128px)` and `.hero{padding-top:var(--s6)}`.

3. **MUST: the Portals' charge pill covers the product.** Raised by taste ("the product big, whole") and polish (duplicate state).
   - Evidence: `.charge` sits `bottom:16px` inside `.portal` and covers the bottom of each pendant (Ember square is clipped, `rev/d-portal.png`). "Charging" also appears twice, on the pill and in `.legend .state` (`phone-states.jpg`).
   - Change: move the button out of the figure into the `.legend` row (`position:static; transform:none`), with the name on the left and the button on the right. Delete the `.state` span and keep `aria-live` on the button label.
   - Pressing anywhere on the figure still charges it.

4. **MUST: the Listening Room shows 5 disabled play buttons.** Raised by polish triage #2 (misleading state), refactoring-ui and web-design-guidelines ("every control answers").
   - Evidence: `.play[disabled]{opacity:.4}` on all rows, plus a note saying the songs are being restored.
   - Change: until the songs are back, render the rows without `.play`. Use a 44px track number in Instrument Serif at `--muted` in its place, keep the durations, and keep "All 176 songs" as the action.
   - Put the buttons back in `data.json` when the songs return.

5. **NICE: too many type sizes.** Raised by typeset, refactoring-ui and taste ("one heading scale").
   - Evidence: there are 12, 13, 15, 17, 19, 23, 25 and 27px sizes, plus three one-off clamps (`.threshold h2`, `.workshop h3`, `.card.guide h3`).
   - Change: use small 14, sm 15, body 17, lede 19, h4 23, h4-lg 27 (`.more` 25 becomes 27), then h3, h2 and h1.
   - Set `.bk small, .trk time, .legend, .card .tag` to 14px (they are 13 now). Add one `--t-h3-lg:clamp(32px,2.4vw + 16px,56px)` for the two card heads.

6. **NICE: the paper grain sits above everything.** Raised by audit and web-design-guidelines (focus visible, overlays).
   - Evidence: `body::before` is `position:fixed; z-index:60`, which is above the header (20), the sheet (40), the skip link (50) and every focus ring. It also lays a 5% veil over all text.
   - Change: `body{isolation:isolate}` and `body::before{z-index:-1}`. The grain then stays on the paper sections only, and the Workshop's night stays clean.

7. **NICE: spacing off the 8px grid.** Raised by refactoring-ui and polish (DESIGN-STATE sets an 8px grid).
   - Change each one-off to the nearest grid value:

   | Selector | Now | Change to |
   |---|---|---|
   | `.btn` padding | 22 | 24 |
   | `.chip` padding | 18 / 14 | 16 |
   | `.ribbon` padding | 14 / 10 | 16 / 8 |
   | `.ribbon span` padding-right | 72 | 64 |
   | `.btn`, `.charge` gap | 10 | 8 |
   | `.menu-btn` padding | 14 | 16 |
   | `.spines` gap | 6 | 8 |
   | `.skip` padding | 12px 16px | 8px 16px |

8. **NICE: the ribbon looks like navigation but does nothing.** Raised by refactoring-ui (affordance) and web-design-guidelines.
   - Evidence: `.ribbon-track span` holds 14 titles at 27px italic that are not links. With the header, that is 104px of chrome on the phone.
   - Change: make each title an `<a href="/slug">` with `min-height:44px`.
   - Or demote it instead: 19px, `color:var(--muted)`, `display:none` at ≤900px.

9. **NICE: Free tools is sparse at 1440.** Raised by taste ("nothing sparse") and bolder.
   - Evidence: two cards end at y=730 and are followed by about 300px of empty ground (`rev/d-tools.png`).
   - Change: `.tool{grid-template-columns:200px 1fr; padding:var(--s6)}`, `.tool img{width:200px}`, `.tool h3{font-size:clamp(32px,2.4vw + 16px,44px)}` and `.sec#tools{padding-block:var(--s12)}`.

10. **NICE: a ghost of the spines stays in the open door.** Raised by polish.
    - Evidence: on open, `.spines i` go to opacity .35 and leave a faded thumbnail stuck at the top of the open panel on the phone (`phone-states.jpg` panel 3).
    - Change: tween to `opacity:0, height:0` (or `@media(max-width:900px){.door[data-open] .spines{display:none}}`).

11. **NICE: touch details missing.** Raised by web-design-guidelines.
    - Add `a,button,.chip{touch-action:manipulation}` and `html{-webkit-tap-highlight-color:transparent}`. The `:active` scales already give press feedback.

12. **NICE: the selected chip leaves no trace after scrolling.** Raised by delight (make the next step obvious).
    - When the answer panel opens, the hero chip stays filled, but the panel head gives no way back.
    - Add a "Change answer" text button (44px) next to `#result-title` that focuses the chips.

## False positives / rejected

- **Detector: Instrument Serif "overused".** The font is about to change.
- **Detector: dark-glow on `.glowline` and the knob.** The glow is literal (the strontium).
- **web-design-guidelines: "animate transform/opacity only" on `.result` and `.door-body` `grid-template-rows`.** These run once, on tap, on small blocks, and the design gates showed 0 dropped frames.
- **taste §6: the paper grain counts as an "effect ground outside tech".** It is a 5% static print texture, not an effect, and it is on-brand for "The Press". Only its stacking order is wrong (#6).
- **taste: "no row half empty" on the 2-book shelves.** These are shelves in a catalogue, and the empty space reads as shelf space, not a broken grid.
- **taste copy-lint INFO: two-fragment heading, "isn't", "quiet", one triad.** The heading is the line that carries the Workshop, and the others are literal. All are INFO only.
- **web-design-guidelines: Title Case for headings and buttons.** The brief chose sentence case.
- **web-design-guidelines: preload and preconnect fonts.** The fonts are inlined, and LCP is 0.5s.
- **overdrive: add WebGL or a bigger effect.** It forbids competing big moments, and the hero book plus the Portals charge already fill that role.
- **"Leave now" goes to google.com.** That is a navigation, not a third-party request.
