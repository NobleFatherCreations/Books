# Review: the "13 Gates Matrix / SovereignPlaybookEngine" plan (2026-10-27)

The owner pasted a plan from another chat (React + Tailwind + Framer Motion component, `tacticsMatrix.json`,
React Helmet SEO, robots.txt, three MCP servers) and asked for it to be checked against the real Decoder,
built, and analysed. This is the result. Nothing from the plan was built or deployed.

## State of the real product at the time of review

- Live `/playbook` is **v15 "Wayfinding"** (the metro-at-night redesign), deployed 2026-10-27 10:42 UTC from
  `claude/friendly-albattani-j667ry`. This branch was 50 commits behind it, so `verify-deployed` reported
  drift. Live was right (that branch builds on ours, and its file matches live byte for byte), so this
  branch was fast-forwarded. Wookbook was fast-forwarded the same way.
- `python3 design/build-decoder-v15.py`: pre-compile gate passes (310/310 entries read back byte for byte);
  the output is **byte-identical to `instruments/playbook/index.html` and to live**.
- `node scripts/decoder-verify.js`: **108/108 checks pass**, axe-core has no serious or critical violations
  (64 scans, WCAG 2.2 AA), and there is no sideways scroll at 320px. Phone at 4x CPU: LCP 600 ms, longest
  task 129 ms (v14 was 836 ms). The one first-run failure was axe-core not being installed
  (`npm i --no-save axe-core`).

## What the paste gets right (and v15 already does)

| Paste idea | v15 today |
|---|---|
| 10 categorical lines | 10 lettered lines (T G C L W B P S O M); the line names in the paste are the real ones |
| Station-based wayfinding | Every tactic is a station, with code plates (`G 01`) and search by code |
| Quick exit | Green **Leave** button in the top bar on every screen, destination set in Settings, no referrer sent, history unwound |
| "Type what happened" search | Everyday-words engine with stemming, synonyms and fuzzy fallback, which shows why each result matched. "they blamed me" finds Blame-Shifting; "they told everyone I was lying" finds Smear Campaign |
| Thumb-zone controls | Four doors on a bottom sign bar, safe-area insets, a step dock, and the bar steps aside when the keyboard is up |
| Swipe between tactics | Route swipe strip with a one-time tip; Previous/Next arrows |
| Zero layout shift on change | Fixed station layout; the verify suite checks every one of the 310 at 390px and 1440px |
| Bottom-sheet over map | The network map station sheet, with a grab handle |

## Where it is misaligned (blockers first)

1. **The content is invented.** Of the 12 sample tactics, only DARVO and Love Bombing exist. "Controlled
   Leakage", "Manufactured Urgency", "The Guilt Sanction", "Time Auditing", "Micro-Financial Throttling",
   "Bureaucratic Weaponization", "Reality Reconstruction", "Echo-Chamber Manufacturing" and "Digital Footprint
   Hijacking" are not entries. Their nearest real neighbours are Strategic Leaking, Urgency Manufacturing,
   Smear Campaign and others. The station numbers (3.12, 4.15) do not exist. The count is 310, not 320, and
   there are no "20 volumes". Line II ("Put-downs that wear you down", 27 tactics) is missing, and so the
   default index lands on the wrong line.
2. **The "exit" copy is unsafe.** It says "Disconnect immediately", "Run an absolute security reset. Change all
   root passwords", "Establish a fully detached, private account immediately" and "their exposure is permanent".
   For stalkerware and financial control, abrupt changes can tip off the controlling person and escalate risk.
   The real entries put a safety note *before* the answer on 105 sensitive entries, and the frozen safety
   framing ("a reading aid, never a diagnosis or a verdict") rules out imperatives like these.
3. **It deletes about 95% of each entry.** Two fields (definition, exit) replace the 5-part model and 40
   fields, including `what_it_is_not`, `common_false_positives` and `safety_note`. Those fields are what stop a
   reader mislabelling an ordinary conflict.
4. **The SEO section would undo a safety feature.** The page has carried `noindex` and a neutral tab title
   ("Pattern Decoder") since v8, so a monitored browser's history or tabs do not reveal what was read. Helmet
   would write "Line III | Gaslighting Deconstruction" into the title on every view. It is also broken:
   - The canonical URL is malformed (`https://noblefathercreations.com{currentLine.id}`).
   - `Sitemap:` points at the home page, not an XML file.
   - Client-side Helmet writes nothing into static HTML, so the "bots read it without JS" claim is false.
   - Hash routes (`#/entry/slug`) are never crawled as separate URLs.
   Changing discoverability is an owner decision about safety, not a build step.
5. **It breaks the frozen architecture.** React, Tailwind, Framer Motion and npm packages are frameworks.
   There is no `src/`, `package.json` or bundler in this project. The Decoder is one offline HTML file built by
   `design/build-decoder-v15.py` from `design/decoder-v15/` and `content/`.
6. **The code does not do what its comments say.**
   - Search returns the first substring hit on every keystroke ("a" jumps somewhere), and the exit text is
     not searched.
   - There is no swipe handler at all; "Layers" just cycles lines.
   - `h-screen` (100vh) is the exact mobile-browser-bar bug it claims to fix; it needs `100dvh` plus
     safe-area insets.
   - `AnimatePresence` cards of different heights do shift the layout.
   - `select-none` blocks copying a script.
   - The text is too small and too faint: 9px labels, `white/20` placeholders, and disabled buttons at
     `opacity-5`.
   - `silvergray: #9A9A1A` is olive, not grey.
   - The grain SVG data URL is malformed.
   - Other code errors: `useMemo` is not imported in one version, `itemprop` should be `itemProp`, there is a
     `idDefinedTermSet` typo, and `|| tacticsData` falls back to the whole array.
   - Quick exit uses `location.href`, so Back returns to the page; it needs `location.replace`. v15's Leave
     already handles this.
7. **"13 Gates of Perception / Matrix" appears nowhere** in any repo. It is a new name, and a naming
   decision for the owner.
8. **The analytics idea conflicts with the product's promise.** "Track which tactics are searched most" breaks
   the page's own promise that "Nothing you type leaves your device". The Metricool MCP measures social
   accounts, not on-site search, so it could not do this anyway.

## Decisions for the owner (nothing here was acted on)

1. Keep `noindex` and neutral titles (the current safety stance), or make the Decoder discoverable? If it should
   be discoverable, the safe way is a separate static, indexable "about" page per line that links into the
   private reader. Changing the reader's own title would remove that protection.
2. Adopt the name "13 Gates", or keep "Pattern Decoder"?
3. Open questions already on file from v15: Vivid or Quiet colours by default; a clinical review of the medical
   symptom lists and safeguarding notes.

## MCP servers asked for

- **Sequential Thinking:** inspected first. It is the official `modelcontextprotocol/servers` package, runs over
  stdio, has four ordinary dependencies, and has no telemetry or daemon. It was added to `.mcp.json`, pinned to
  2.0.0, and answered an MCP handshake. Project MCP servers start with a session, so it is live from the next
  session. The package asks for Node 24; Node 22 here gives a warning but works.
- **Filesystem:** not added. Claude Code already reads and writes files directly.
- **Metricool:** already connected at account level. See item 8 for why it does not fit this use.
