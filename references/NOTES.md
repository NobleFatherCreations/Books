# references/NOTES.md — what the captured benchmark screenshots show

Captured 2026-11-10 with `scripts/capture-references.mjs` (headless Chromium in a cloud container: **no GPU**, so heavy WebGL sites can look wrong; phone 390 px and desktop 1440 px; hero + two scroll positions; cookie banners rejected where a reject button existed). Notes below describe **only what was visible in the phone screenshots I read**; they are observations, not endorsements. Desktop shots were captured but not yet reviewed. Screenshots are for private study, not republishing. Compare new work **only within the matching set**.

Capture caveats: Calm captured blank; Raycast desktop timed out; Active Theory showed "your browser is not supported" (no GPU); some sites were caught mid-preloader or mid-animation (Lusion and Persepolis showed a "100" loading counter; Stripe Press showed stacked image strips mid-transition); Quanta's consent banner partly reappeared.

## reading-first (benchmark for HTML books)
| Site | Observed | Steal | Avoid / caution |
|---|---|---|---|
| **Aeon** | Red wordmark; centred "Essays" heading with one-line description; text-only tabs (Latest / Popular); large photographic cards with category tag, serif title, standfirst, author | Restraint: plain tabs, one image per card, clear hierarchy | Heavy photography is not available to every book |
| **Ciechanowski** | Solid blue header with big sans name; date line; very readable body text with generous space; explorable moon figure with a slider (dark figure) | Figures that you manipulate inside a calm text column | Full custom explorables are costly |
| **Gwern** | Very dense small-caps/mono text, a right-edge toolbar of reading controls (theme etc.), inline two-column table of contents, pull quote, link popups | Reading-control toolbar idea; sidenote/popup grammar | Density overwhelms a vulnerable reader |
| **The Marginalian** | Yellow banner with logo; title set as yellow highlighter strips; single column; quoted passages with attributions; book-cover image | Warmth from a single accent; marker-highlight title; single-column reading | Yellow-on-yellow contrast needs checking |
| **Practical Typography** | Plain black text on white; grouped contents list with generous line spacing; no decoration | Perfect plain hierarchy; proof that type alone can carry a book site | Austere for emotional subjects |
| **Quanta** | Article page with serif headline, small caps category label, caption credit; illustration-led | Headline/caption/credit grammar | — |
| **Standard Ebooks** | Dark blue header with seal; "Browse Ebooks" centred; utilitarian form controls; book-cover grid (second screen) | Book-as-object covers in a grid; consistent cover system | Utilitarian chrome |
| **Stripe Press** | Dark page of stacked image strips naming each book ("Nomad Letters", "Built to Grow", "Poor Charlie's Almanack"), caught mid-transition; "Ideas for progress" | Each book gets its own bold visual identity; the title moment | Mid-animation capture: view the live site before judging |
| **The Pudding** | Brush-script wordmark; search and filter; issue-numbered cards (#228) in bold colours with data figures | Numbered issues; each story a distinct colour world | Loud: not for sensitive content |
| **Tufte CSS** | Serif text with generous margins, italic subtitle, link underlines; clean paragraphs | Margin grammar for sidenotes; typographic calm | Minimal navigation |
| **Wait But Why** | Hand-drawn banner; grey menu bar; colourful illustrated thumbnails; blue links; older-web layout | Illustration as voice | Dated chrome |
| **Works in Progress** | Cream page, dropdown topic nav, bold red illustrated card with serif title and outlined "Read now" button, newsletter prompt | Bold illustrated cover cards on a calm cream ground | Consent/newsletter prompts add clutter |

## care-public-service (overrides spectacle for safety, care, crisis content)
| Site | Observed | Steal | Avoid / caution |
|---|---|---|---|
| **GOV.UK** | Strong blue header; large bold plain-language headline; prominent search; list of popular tasks with arrow icons; cookie choice recorded with a hide button | Plain language, one clear search, task list | Colour is institutional, not warm |
| **GOV.UK Design System** | Same system; "Design your service using GOV.UK styles, components and patterns"; clear primary action button | Tested components; clarity | — |
| **NHS** | Strong blue; clear headline over photo; large stacked cards with arrow affordances | Large tappable cards with clear arrows | — |
| **The Hotline (domestic violence)** | A "Security Alert" modal on arrival: internet use can be monitored; **click the red X top-right or press Escape twice to leave immediately**; emergency line shown; red exit button top-right | **Quick-exit pattern with explicit Esc-twice**, safety message first, emergency instruction | Modal on arrival interrupts reading: keep it short and dismissible |
| **Women's Aid** | Magenta brand; vertical yellow **"EXIT SITE" tab fixed to the right edge**; large mixed-weight headline; "Get Help / Donate / Accessibility" strip | Persistent edge exit tab always visible | Strong brand colour is noticeable on a shared screen |
| **Chayn** | Warm peach page; soft rounded type; a pink **"Leave this site" pill button** under the nav; hopeful illustration; plain supportive copy | Warm trauma-informed tone with a visible leave button | — |
| **Headspace** | Bright orange promo page with smiling sun illustration and discount tag | Friendly illustration | Promotional pressure ("don't miss out") is the opposite of care; the capture is a promo state |
| **Calm** | Captured blank | — | Re-capture manually |

## tools-product (for lookup instruments such as the Pattern Decoder)
| Site | Observed | Steal | Avoid / caution |
|---|---|---|---|
| **Arc** | Dark page, large rainbow logo, serif headline "A farewell to Arc", note that Arc is being sunset on 22 December 2026 | A single confident message screen | State-specific (farewell page) |
| **Framer** | Black; white sans headline; glowing blue UI object in a video; logo ticker | Dark craft with one glowing focal object | Glow overuse |
| **Linear** | Dark; light-weight large headline; product screenshot as proof | Product screenshot as hero; restraint | — |
| **Notion** | White; hand-drawn avatars; large sans headline with a green "Ship" chip; solid blue CTA | Friendly illustration; chip device in headline | — |
| **Raycast** | Dark with red diagonal 3D ribbons; short headline "Your shortcut to everything." | One bold graphic with minimal text | — |
| **Stripe** | White; diagonal multicolour gradient; headline with grey second clause; indigo CTA; logo row | Gradient as brand signature; two-tone headline | — |
| **Vercel** | White; black triangle with soft shadow; centred "Agentic Infrastructure"; monospaced subline; black pill CTA | Monospaced support line; black/white discipline | Sparse for dense content |

## showcase-story (craft, not structure: award winners score low on accessibility; see `09-award-winners-data.md`)
Observed in the second-position phone screenshots: **Igloo Inc** shows a 3D igloo on icy terrain; **Lando Norris** a dark olive page with a portrait, lime accent and a kinetic stripe of type; **Lusion** a black screen with a big "L" and a "100" loading counter; **Mana Yerba Mate** a cream page with tilted green label shapes and playful copy; **Messenger (abeto)** a teal field with a tiny planet; **Noomo** a lilac gradient with a 3D jellyfish passing through the word "IMMERSIVE"; **Pangram Pangram** type-specimen product cards; **Persepolis Reimagined** a slate screen with an ornate ring and a "100" loading counter; **Bruno Simon** a purple grid with a glowing ring; **Active Theory** "browser not supported" over a 3D logo (no GPU). Preloaders as part of the design, per-product colour worlds and a single focal 3D object recur: see the patterns in `09`.

## Next steps
- Review the desktop screenshots and the third scroll position per site; add notes.
- Re-capture Calm and Raycast desktop; capture the GOV.UK "Exit this page" component page.
- Add sites as discovered; keep one line of "steal / avoid" per site.

## scale-zoom-story (captured 2026-11-11 for the Fractal² intro; `references/shots/scale-zoom-story/`)
Read: **Apple AirPods Pro** (concentric-ring hero, one idea per screen, huge calm headline, minimal chrome), **Stripe Press** (dark stack of spines navigated by scroll; each book its own identity), **NASA Webb** (dark hero, giant left title, small labelled facts), **NASA Eyes** (card list, flat ground for text), **The Pudding** (each story its own colour world, loud), **BBC News** (irrelevant news chrome, kept as a contrast). Blocked or empty: neal.fun deep-sea and size-of-space (Cloudflare check), Eames Powers of Ten (Cloudflare check), Scale of the Universe (language picker only). Steal: one subject per screen; titles and labelled facts as the only chrome; a physical stack you move through. Avoid: card grids and loud colour worlds for this subject.
