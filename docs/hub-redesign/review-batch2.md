# Homepage v18: motion, UX and accessibility review

I tested with Playwright at 1440, 375, 375 with reduced motion, 640x400 (200% zoom) and 320. The test scripts are in `qa/mrev/` (t1–t4).

## Issues, ordered by impact

**1. MUST. The hero book jumps to a nearly side-on angle after the first scroll, and mouse tilt fights the scroll.** Skills: gsap-core, gsap-scrolltrigger, review-animations.
- Evidence, from `home.js:151,169`: the scrubbed `to()` takes its start value from the `from()` entrance, which is rotateY −60.
- Measured: the book rests at −29.8°. At 300px of scroll it is at −49.8°, so it turns away from the reader before turning back. Back at the top it rests at −60.
- The mouse `quickTo` (`:164`) sets −30.1°. The next 2px of scroll then snaps it to −49.7°.
- This only happens when motion is on. With reduced motion it is correct.
- Fix: split the book into three wrapper layers.
  - `.book-in`, used only for the entrance and float: `gsap.from('.book-in',{y:40,autoAlpha:0,duration:1.2,ease:'power3.out',delay:.1})`. The float moves to this layer too.
  - `.book-tilt`, used only for the mouse: `quickTo('.book-tilt','rotationY')` with `tx((k-.5)*10)`.
  - `.book3d`, used only for scroll: `gsap.fromTo('.book3d',{rotateY:-30,rotateX:7,rotateZ:-3},{rotateY:-8,rotateX:2,rotateZ:0,ease:'none',immediateRender:false,scrollTrigger:{…}})`.
  - Give both wrappers `transform-style:preserve-3d`.

**2. MUST. Nobody sees the new cover turn after tapping a chip.** Skills: review-animations, ux-heuristics, gsap-timeline.
- Evidence, from `home.js:60`: the panel scrolls into view 140ms after the tap, but the turn takes 700ms.
- Measured scroll: 938px on desktop and 743px on phone. By 400ms the book is off-screen (desktop bottom edge −156, phone −461).
- The swap timeline and the scrubbed `#hero-face` tween animate the same rotateY, so the face ends at the scroll value (−42°).
- `--ar` changes at tap time (`:39`), so the book resizes before it turns.
- Fix:
  - Wrap the sheen and image in `.leaf` and turn `.leaf`, not `#hero-face`.
  - Set `--ar` inside `.add()` at the midpoint.
  - Before starting a new turn, end the previous one: `flipTl&&flipTl.progress(1).kill()`.
  - Do the scroll in the timeline's `onComplete` with `scrollBy({top:r.top-innerHeight*.45,behavior})`, so part of the book stays in view.

**3. MUST. Shelf books appear, blink out and then animate in again.** Skills: review-animations, gsap-scrolltrigger.
- Evidence, from `home.js:156`: the batch `from()` only runs once a book reaches 88% of the viewport, after it has already been drawn.
- Measured opacity: 1.00 → 0.20 → 1.00, on both phone and desktop.
- Tab also landed on books at opacity 0–0.57.
- Fix, in the motion branch:
  - `gsap.set('.shelf .bk',{opacity:0,y:28,rotate:-1.5})`.
  - Then `batch(...,{start:'top 92%',once:true,onEnter:els=>gsap.to(els,{opacity:1,y:0,rotate:0,duration:.6,stagger:.08,ease:'power3.out',overwrite:true})})`.
  - Add a `focusin` handler that calls `gsap.to(bk,{opacity:1,y:0,rotate:0,duration:.2})`.
  - Use opacity, not autoAlpha, so the books stay in the tab order.

**4. MUST. "Change answer" can be focused while the answer panel is collapsed to zero height.** Skills: better-accessibility, web-accessibility.
- Evidence: the Tab order runs chips → "Change answer" → books, with `#result` closed.
- Fix:
  - Add `inert` to `<section class="result">`.
  - Set `result.inert=false` before writing the new HTML, and `true` when the panel closes.
  - Move `aria-live` off the whole section to a `.vh` status that says "Three suggestions for …". At the moment every link gets read out.

**5. MUST. The charge buttons fail Label in Name (WCAG 2.5.3) and misuse ARIA.**
- Evidence: the visible text is "Hold to charge", but the `aria-label` is "Charge Clockwork with light…".
- `aria-pressed` is used on a button that is not a toggle.
- There is an `aria-live` region inside the named button.
- `say()` (`:83`) does nothing.
- Fix:
  - Remove the `aria-label` and `aria-pressed`. Use `<span class="label">Hold to charge</span><span class="vh"> Clockwork</span>` inside the button.
  - Add a sibling `<span class="vh" role="status">`.
  - Wire `say()` to the status, and announce only "Clockwork is glowing".

**6. MUST. Pressing a glowing pendant again snaps it to day, and a quick tap leaves its state stuck.**
- Evidence, from `home.js:100`: `v.g=0` makes the night layer go from 1 to 0 in one frame.
- A 30ms tap takes the early return at `:86`, which leaves `is-glowing` and `aria-pressed="true"` set permanently. Measured 8s later.
- Fix:
  - Replace the snap with `gsap.to(v,{g:0,duration:.25,ease:'power2.out',onUpdate:paint})`.
  - In the early return, run `fig.classList.remove('is-glowing')` and fade the glow out the same way.

**7. MUST. "Just looking" after an answer lands in the middle of the library.** Skill: ux-heuristics.
- Evidence: `#library` ends up with its top at −333px on desktop and −586px on phone. The panel's 0.5s collapse runs during the scroll.
- Fix: if the panel is open, set `result.style.transition='none'`, remove `data-open`, force a layout with `result.offsetHeight`, scroll, then restore the transition in the next frame.

**8. MUST. Reopening the phone menu within 320ms leaves it invisible but still counted as open.**
- Evidence: measured `hidden:true` together with `data-open`. Both Esc presses then went to `closeSheet`, so double-Esc no longer left the site.
- Fix: `let hideT;` then `clearTimeout(hideT)` in `openSheet`, and `hideT=setTimeout(…,320)` in `closeSheet`.

**9. MUST. Opening the door on a phone jumps the content up 148px.**
- Evidence: `home.css:213` hides the spines instantly with `display:none`. Measured door height 396 → 248 in one frame, and the button moves from y 571 to 423.
- Fix: delete that rule. The spines already tip back in GSAP at −14° and 0.35 opacity.

**10. NICE. The glow fades the wrong way.**
- Evidence, from `home.js:93`: with `power2.in`, the night layer is still at 0.92 after 3s, then drops off at the end.
- Strontium fades fast first and then trails off.
- Fix: use `ease:'power1.out'` (g ≈ .57 at 3s, ≈ .29 at 5s).

**11. NICE. Holding a key does not charge a pendant.**
- Evidence: holding Space for 800ms leaves charge at 0, then it jumps straight to full.
- Fix: on `keydown` for Space or Enter with `!e.repeat`, call `charge()`. On `keyup`, call `glow()`. Keep the `detail===0` path as a fallback.

**12. NICE. The chip borders are too faint (WCAG 1.4.11).**
- Evidence: `#4a3d2e` on ink measures 1.78:1.
- Fix: `#7a6850`, which measures 3.5 on ink and 3.28 on ink-2.

**13. NICE. The music copy tells readers to "Press play and keep reading", but there are no play buttons.** Skills: ux-heuristics, cognitive-design.
- Fix: until the songs are restored, cut that sentence. The numbers 1–5 sit where buttons would be, so make them clearly decorative.

**14. NICE. The mouse listener is never cleaned up when the motion setting changes.** Skill: gsap-core.
- Evidence: the `pointermove` listener added at `:165` survives `mm` revert.
- Fix: `return () => hero.removeEventListener('pointermove', onMove)`.

**15. NICE. A scrubbed text-shadow repaints the 132px headline on every frame, and one CSS rule does nothing.**
- Evidence: `:171` scrubs `textShadow`. `.portal.is-glowing .charge` (`home.css:267`) never matches, because the button sits outside `.portal`.
- Fix: put the shadow on `.glowline::after` and scrub only its opacity. Delete the dead rule.

## Checked and working
- Esc twice reached `google.com/search?q=weather` on desktop and phone.
- Esc closes the menu and returns focus to the Menu button. Tab is trapped inside the open menu.
- The door's `aria-expanded` and `inert` are correct, and focus stays on its button.
- No overflow at 200% zoom or at 320px.
- Under reduced motion: no float, no entrance, the cover changes instantly, the glow is instant and stays lit, and no scroll moves are smooth.
- No console errors.

## False positives rejected
- **Scrolling across a pendant on a phone triggers a charge:** a simulated touch scroll ended at charge 0, because `pointercancel` arrives before the 60ms threshold.
- **The book entrance delays the hero image paint (LCP):** the h1 is the largest paint, and the local LCP is 0.5s.
- **Animating panel height, the backdrop blur and the grain cause jank:** the design gates measured p95 16.7ms with 0 dropped frames at 4x CPU throttle.
- **`power2.in` on the first half of the cover turn breaks the "never ease-in" rule:** that is the correct easing for a turn's out-going half.
- **The ribbon and book still move with scroll under reduced motion:** the brief allows scroll-linked motion.
- **Text contrast:** muted text is 7.3–8.3:1, brass 11.5:1, Leave 6.96:1 and the glow line at 0.82 opacity about 9:1.
- **Focus ends on `body` after a menu link:** the hash navigation moves the next Tab to the target, so this is harmless.
