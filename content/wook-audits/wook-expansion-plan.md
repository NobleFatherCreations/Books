# Wook — The Seven-Chapter Expansion

Plan of record for adding seven new chapters to `library/wook/index.html`,
taking the book from 26 chapters to 33. Author-approved 2026-09-15.
Written here rather than held in conversation because the renumbering
this causes touches ~443 numeric cross-references and ~52 word-form
chapter counts, and a half-finished version of this job would be worse
than not starting it.

## Why these seven

They came out of a gap analysis run after the full thirteen-pass review
(`wook-full-review-plan.md`) — topics that are real, common, and
documented in the scene, that the book's existing 26 chapters either
touch only glancingly or address from prevention when the reader needs
response.

## Placement

Every insertion sits adjacent to the chapter it extends, so each new
chapter reads as the natural next question of the one before it.

| New # | Title | Slots after | Why there |
|---|---|---|---|
| 6 | The Group Chat | old 5 (Yes Is A Sober Word) | The on-ramp starts weeks before the gate. Opens SET TWO with "the room starts in your phone." |
| 10 | The Love Of It | old 8 (Vendor Row Bloodsport) | Vendor Row is makers being skimmed; this is the labor side of the same economy. |
| 14 | The Two Festivals | old 11 (The Road) | The Road is the traffic stop. This is who gets stopped, and who gets believed after. |
| 17 | The Container | old 13 (The Free One) | The Free One is a man with a jar. This is the institutional version with a lineage and a price list. |
| 20 | The Next Twelve Hours | old 15 (The RV) | The RV is the geometry trap. This is the chapter that exists because sometimes the trap closes. |
| 26 | He Still Has Your Number | old 20 (The Re-Entry Window) | Re-Entry is the text that arrives Sunday. This is the texts that don't stop. |
| 31 | What To Tell Your Mom | old 24 (Protecting The Magic) | Sits in the ENCORE with the other protection chapters; the one chapter written to be handed to someone else. |

## Old → new chapter map

    1→1   2→2   3→3   4→4   5→5
    [NEW 6 — The Group Chat]
    6→7   7→8   8→9
    [NEW 10 — The Love Of It]
    9→11  10→12  11→13
    [NEW 14 — The Two Festivals]
    12→15  13→16
    [NEW 17 — The Container]
    14→18  15→19
    [NEW 20 — The Next Twelve Hours]
    16→21  17→22  18→23  19→24  20→25
    [NEW 26 — He Still Has Your Number]
    21→27  22→28  23→29  24→30
    [NEW 31 — What To Tell Your Mom]
    25→32  26→33

## Set boundaries after the expansion

- SET ONE — KNOW THE PATTERN: 1–5 (unchanged)
- SET TWO — READ THE ROOM: 6–26 (was 6–20)
- ENCORE — PROTECT THE MAGIC: 27–33 (was 21–26)

## Build order

1. Write all seven chapters as standalone fragments in
   `content/wook-new-chapters/`, each structurally identical to an
   existing chapter (see the component list below). **Done before any
   renumbering touches the live book.**
2. One splice script (`scripts/wook-expansion-pass.py`) that, in a single
   idempotent run: renumbers every existing cross-reference through the
   map above, splices the seven fragments into their slots, rewrites the
   set boundaries, and corrects word-form counts.
3. Appendix reconciliation: A (Master Track Index), B (Recurring Cast),
   F (Counter-Drop Master List), G (Discog), Q (Sixteen Moves — the
   count of moves does **not** change, only chapter attributions), and
   every single-topic appendix's "From Chapter N" line.
4. `chapters.json`, the contents drawer, the front matter's Content
   Disclosure, and the reel doc.
5. Seven new `<symbol id="spec-…">` field-tag icons for the new Field
   Specimens.
6. Content warnings — chapter 20 (assault aftermath) needs a real one,
   placed before the cold open, matching how the front matter already
   handles this.
7. Version bump to v12 with "seven more chapters" stated plainly in both
   `sites.json` and the on-page patch note.
8. Both checkers to zero, Playwright, deploy, verify live bytes.

## Per-chapter component checklist

Every chapter carries, in this order:

- `<div class="chwrap sN" data-ch="N">` wrapper, `ch-poster` with rail /
  part / num / title / and-line / keys / meta / ebars
- THE DROP (cold open, POV badge)
- THE SOUNDBOARD QUOTE (board-q + attr, a named scene voice)
- THE REAL F*CKING SETLIST (thesis + THE TAPERS' SECTION)
- THE WOOK'S SETLIST (roster — skip on a no-predator chapter)
- FIELD SPECIMEN (spec-no / name / cap / joke + SVG symbol)
- Tracks: BEHAVIOR · READ · VIBE CHECK · MIRROR SET · REFRACTIONS ·
  RUNS IN EVERY DIRECTION · SOBER TUESDAY · COUNTER-DROP
- HAVE YOU BEEN THE WOOK? (inter-mirror-big)
- THE WOOK DISCOG (Studio Debut / Live Album / Greatest Hits)
- Tales From … — The Save
- THE FANNY PACK (+ POCKET SCRIPTS, + SAFETY APPENDIX where earned)
- THE SOUNDCHECK (a named drill)
- THE SUNRISE SET (zero slang, the true thing)
- THE KANDI TRADE (the vow, closing on PROTECT THE F*CKING MAGIC)
- THE BRIDGE (points at the next chapter by its **new** number)
- `<i class="ch-end" data-ch="N">`

## Status

| Chapter | Written | Spliced | Notes |
|---|---|---|---|
| 6 The Group Chat | **yes** | | 10,594 words, 5 Tracks, clean. New cast voice: Junie “Firewall” Park (needs an Appendix B entry). New counter-drops: Named Reference Rule, Logged-Channel Rule, Hours Audit, Second Anchor, Asymmetry Check (all five need Appendix F entries). New specimen icon needed: `spec-helpfulone`. |
| 10 The Love Of It | **yes** | | 10,741 words, 5 Tracks, clean. Witness POV (Bird, load-in lead). Reuses Wingnut as the Soundboard voice — his Appendix B line needs a second-appearance update. New counter-drops: Hourly Conversion, Payroll Question, Incident Record, Title-To-Terms Test, Off-Season Test. New specimen icon: `spec-coreteam`. |
| 14 The Two Festivals | **yes** | | 10,856 words, 5 Tracks, clean. Festie POV (Tee, ninth year). Reuses Céline “Patch” Oduya as the Soundboard voice — Appendix B needs a second-appearance update. Contains the book’s disclosure that its own first thirteen chapters carried an unmarked assumption about involving staff/police. New counter-drops: Medical Words, Corroboration Pre-Load, Personal Risk Map, Handoff, Affinity Anchor. New specimen icon: `spec-secondlook`. |
| 17 The Container | **yes** | | 11,287 words, 5 Tracks, clean. Festie POV (Noor, hospital pharmacist). New cast voice: Margarethe “Bell” Ndiaye (needs Appendix B entry). New counter-drops: Pre-State Contract, Lineage Check, Dose Disclosure Rule, Daylight Contact, Separate Integrator. New specimen icon: `spec-facilitator`. Consider a content note — boundary violation during an altered state. |
| 20 The Next Twelve Hours | | | needs content warning |
| 26 He Still Has Your Number | | | |
| 31 What To Tell Your Mom | | | audience is the loved one, not the attendee |
