# Homepage redesign: Stage 2, information architecture (draft for owner check-in, 2026-11-21)

## Owner inputs (2026-11-21)
- Keep the books separate from the artwork.
- Music must actually play (finding: every Listening Room track returns 404; the mp3s were never uploaded to noblemusic; the files are recoverable from the owner's Drive folder "MP3 music". Direct download tested: byte-identical).
- Someone looking for one book must not be put off by The Sacred Divide (religion) or The Fractal (the pattern everywhere).
- Shop: showcase The Portals. The Press (seals) and The Casting are not ready.
- The NFC guide is easy to find, but the trip there passes other parts of the site.

## Mental model
Visitors arrive with a situation, not a title. Two separate audiences: readers (often hurting, on a phone, late) and art buyers (came for the pendants). Readers think "what's happening to me"; buyers think "show me the thing".

## Structure: one page, two worlds, a hard threshold between them
```
noblefathercreations.com
│
├─ THE STUDY (light: the reading world)
│   1. Opening: one question, "What's happening?", with 4 situation doors + "Just browsing"
│   2. Start-here result: 1 book + 1 tool for that situation (in place, no page change)
│   3. The Library, by situation (4 shelves, max 4 books each)
│        Someone close to me ...... The Sovereign Divine Feminine · The Long After · The Silence · The Repair
│        Work, money & family ..... At Will · The Slow Take · Playground Protectors
│        Screens & judgement ...... The Loop · The Weighing
│        Festivals ................ The Festie Codex · The Festie Bible
│   4. The bigger picture (opt-in door, closed by default, after the shelves)
│        "For when you want to see how it all connects": The Fractal · The Fracture · The Sacred Divide
│   5. Tools: The Pattern Decoder · The Root
│   6. The Listening Room: in-page player (6 featured songs, play right here) + "All 176 songs"
│
├─ THRESHOLD: "Cross into the Workshop" (light turns to dark; the tagline acted out)
│
├─ THE WORKSHOP (dark: the glowing art world)
│   7. The Portals: full showcase (glow reveal, details, how to get one)
│   8. In the making: The Press · The Casting (small "coming soon" plates)
│   9. How to Program NFC Tags: the guide (end of the Workshop, so a nav jump scrolls past the Portals on the way)
│
└─ Shared end: the maker (short) · support (donate) · footer (full index)
```

## Navigation
- Top bar, 5 items max: **Books · Tools · Music · Art · NFC guide**, plus the seal menu. Every item scrolls on this page (no item leaves the page), so a jump to the NFC guide travels down past the Library, the Music and the Portals. Reduced motion jumps instead.
- Active-section marker, fixed: one numbering system, generated from one list.
- Quick exit: a small "Leave" control, always reachable (pending owner yes).
- Seal menu: the same five groups, plus every book by shelf.

## Labels
- "Art" (not "Workshop" and "Art" as two things). The section heading can still say The Workshop.
- Drop "NFC craft lines", "living tools", "instruments" from visible copy; say "free tools" and "art".
- Shelf names are situations in the reader's words, never categories like "Systemic".

## URLs and anchors (hard rule 1)
Existing anchors (#start-here, #library, #instruments, #music, #workshop, #guide, #support) keep working. New anchors are added; none is removed without a redirect alias in the page.

## Open questions for the owner
1. Grouping above: right shelves?
2. Music: may I restore the 176 songs to the music site (download from your Drive, then redeploy the Listening Room; needs your go-ahead)?
3. Quick exit: yes/no.
4. A real buy path for the Portals: where do pendants sell today (link, DM, form)?
