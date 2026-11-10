# Fractal² — design rebuild prompt (paste this as the first message of a new session on this repo)

You are rebuilding the **look and motion** of two things that are already written and working: the scroll intro at `/fractal2` and the Entertainment & Music site at `/fractal2/entertainment`. The words, data, safety lines and page structure are finished. The design is not. The owner looked at the live intro on an iPhone and called it generic and broken. Their screenshots show it: figures drawn over paragraphs, a ring label ("Replace") printed on top of body text, headings clipped under the header, a 2,700 counter colliding with text, large empty beige areas, thin specks standing in for illustration, and a body-text-first layout that reads like a default blog template.

You are the designer. Not a coordinator. **Do not delegate design or visual choreography to other models.** Delegate only mechanical work (re-running builds, file moves).

## 0. Rules you must follow before touching anything

1. Read, in this order: `CLAUDE.md`, `MEMORY.md`, `docs/AI-QUICKSTART.md`, `content/fractal2/STATUS.md`, `content/fractal2/DESIGN-SPEC.md`, `design/fractal2/tokens.css`. Then the owner's own words in `content/fractal2/owner-source/` (E, F, G). They win every conflict.
2. **Do not change words.** `content/fractal2/intro-final.md` (Part VI is the owner's account, locked by a test), `design/fractal-sector/strings.json`, the ledger, safety notes, and every published book are untouched. You may change what the words sit on, how they enter, and what surrounds them. Do not change the tag/label results.
3. Keep the architecture rules in `CLAUDE.md`: no external requests except the one Cloudflare beacon, fonts self-hosted, icons inline SVG, no storage, works offline, reduced-motion and no-JavaScript versions, light and dark.
4. Nothing is deployed until the owner says "deploy" in that conversation. Preview only.
5. Commit and push after each phase to the branch you are given.

## 1. Use the tools. This is the part that was skipped before.

Before designing, **actually invoke** these with the Skill tool and apply what they return. Name each one in your phase notes with one sentence on what it changed:
- `impeccable` — run `shape` before building, `critique` after every round, then `polish`, `typeset`, `layout`, `animate`, `colorize`, `bolder`, `audit` as the critique calls for them.
- `apple-design` and `emil-design-eng` — for the scroll choreography, spring and easing values, and the feel of touch.
- `frontend-design`, `refactoring-ui` — hierarchy, spacing, depth.
- `better-accessibility`, `web-perf` — last.
Use `ToolSearch` to find MCP tools. Use Playwright (it is pre-installed; never run `playwright install`). Use the Figma, Canva or image tools only for mood boards or storyboards if they help. They are never the source of truth. If a tool is unavailable, say so in your notes and carry on; do not silently skip it.

## 2. The standard (what "world class" means here)

Reference quality: press.stripe.com, Apple product pages, the best Pudding / NYT / Pitchfork scrollytelling, Locomotive-style kinetic type. Concretely:
- **A distinct visual identity, not a template.** Choose a real display typeface with character (self-hosted, subset, `font-display` handled) paired with one reading face. A dramatic scale: huge display type for the big moments, a calm measure (60–70 characters) for reading. No default serif-on-cream look. A restrained palette with one memorable accent, designed for both dark and light, with real contrast.
- **The page is the figure; text is the caption, not the other way round.** Each of the 20 figures gets a full-bleed or full-height stage that is composed, large and beautiful: layered depth, considered colour, motion with weight and easing, typographic figures where words are the graphic. The ring with 30 techniques, the three nested rings, the 2,700 grid, the chain of generations and the three overlapping circles each need to be an image people screenshot.
- **Text and figure never collide.** On a phone, the figure owns the screen during its moment, then yields to the text; they do not overlap. Captions ("What the figure shows") sit in their own safe zone. Headings never sit under the header.
- **Motion has intent.** Scroll-linked reveals, staged entrances, parallax or depth where it earns its place, spring physics on touch, and a distinct transition between acts. All of it off or simplified under `prefers-reduced-motion`. 60 fps on a mid phone; no layout shift.
- **The open and the handoff are an experience.** The first screen is a title moment worth the owner's name. The end of the scroll leads into the Entertainment & Music site with a deliberate transition, not a link list. The Entertainment site gets the same identity: real home page, stage rings as navigation, pattern pages with typographic hierarchy, the interactive map as a hero. Same fonts, same accent, same motion language as the intro.
- **Reuse the engine, rebuild the skin.** `design/fractal2/intro.js` and `design/fractal-sector/` already produce correct structure and data. Rebuild the presentation layer (`tokens.css`, `intro.css`, figure drawing and choreography, sector templates and CSS). Keep what works. Keep the narration player and the 31 + 27 existing checks passing.

## 3. Process (follow it; do not jump to "done")

**Phase A — Direction, before any code.** Write `content/fractal2/DESIGN-DIRECTION-v2.md`: the concept in one paragraph, the type pair and why, the palette (dark and light) with contrast ratios, the motion principles with actual duration and easing values, and a one-paragraph storyboard for each of the 20 figures that says what is on screen, what moves, and where the text sits on a 390 × 844 phone and on a 1440 × 900 desktop. Run `impeccable shape` first. Build **one hero figure and the title screen** to the full standard and review it before scaling to the rest. That is the bar.

**Phase B — Build the intro.** Figure by figure. After **every** figure or meaningful change, take real screenshots and **read them as images** (Read tool on the PNG). Describe what you actually see. If you did not look at it, it is not verified.

**Phase C — Rebuild the Entertainment site skin** the same way, then the handoff between the two.

**Phase D — Critique loop, minimum three rounds.** Each round: screenshots of every figure and 10 representative site pages at 390 × 844 (touch, `deviceScaleFactor` 3) and 1440 × 900, light and dark, plus reduced motion; run `impeccable critique` and `audit`; list defects in your own words from what you saw; fix; repeat. Stop only when a round finds no overlap, clipping, dead space, weak hierarchy or generic-looking screen.

## 4. Hard failure conditions (any one means not done)

- Any screenshot where a figure overlaps readable text, a label overlaps body text, or anything sits under the header.
- A figure area that is mostly empty background or reads as thin dots or specks without a composed focal point.
- A screen that could belong to any blog. Test: cover the logo; would a stranger know whose it is?
- Fonts that fall back to system faces on first paint.
- Anything that works only after a hover.
- You describe a screenshot you did not read.

Headless checks (overflow, console errors, opacity) are necessary, not sufficient. They passed on the version the owner just rejected. The visual review in section 3 is the real gate.

## 5. Real-device honesty

Chromium emulation is not iOS Safari. The previous version passed every automated check and still failed on an iPhone. So: keep `-webkit-` prefixes and safe-area insets (`env(safe-area-inset-*)`), use `100svh` / `dvh` not `100vh`, avoid `position: sticky` and `backdrop-filter` patterns that break in iOS Safari, test with `scroll-behavior` and rubber-banding in mind, and avoid WebGL features iOS lacks. Write `content/fractal2/PHONE-CHECK.md`: a 10-step checklist the owner can run on their phone in five minutes (what to scroll to, what should be happening), and ask for a private preview deploy to run it on.

## 6. Deliver

- Branch pushed, with a short `DESIGN-NOTES.md`: what changed, which skills and tools were used and what each changed, before/after screenshots at `library/fractal2/review/v2/`.
- `verify_intro.mjs` and `verify.mjs ent` still pass; add visual checks that fail on text/figure overlap (bounding-box intersection tests between figure stage and text blocks at 390 and 1440).
- A plain-language summary for the owner, with the five screens you are proudest of and the two you are least sure about.
- Ask the owner for "deploy" before publishing anything, and say what it will replace.
