# Wook in Sheep's Clothing — Teleprompter Reading Plan

How to read the whole book on camera, chapter by chapter, without either
reading a 10,000-word chapter in one unbroken take or inventing a chunking
scheme the book doesn't already have. **The book already ships in
video-sized modules** — this plan just names them and puts them in a
filming order. Nothing here changes the book; it's a reading plan for it.

## The short version

Every chapter breaks into the same sequence of module types, because every
chapter is built from the same sequence of module types. Cold opens are
their own video, same as your instinct said — everything else in a chapter
follows as its own short run of additional videos, in this fixed order:

1. **THE DROP (Cold Open)** — the chapter's own video already. Full
   narrative scene, one POV, no framework language, nothing explained.
   ~1,500–2,500 words per chapter. This is the one piece of the book you
   already have a promo plan for — see `content/wook-audits/wook-cold-opens-reel-order.md`,
   the existing 33-cold-open reel order with cut points and a season
   structure. Use that doc for the promotional cut; use THE DROP as
   extracted here for the full, unabridged read.
2. **The Setup** — the soundboard quote, the chapter's real thesis ("what
   this chapter is actually about"), and the roster of Tracks in play.
   Short, punchy, works as the "here's what you're about to learn" video
   right after the cold open.
3. **One video per Track** — the chapter's core teaching units. Each Track
   is a single manipulation pattern with a fixed 7–8 beat structure: the
   behavior, the read, a counter-drop (the actual script to run), a vibe
   check, a mirror set (turn it on yourself), refractions (how it lands
   differently by identity/experience), how it runs in other directions,
   and the Sober Tuesday version (the plain, day-after truth). A chapter
   has anywhere from 0 (a few chapters run a different shape entirely —
   see below) to 12 Tracks. Each is a complete, self-contained ~900–1,100
   word unit — this is the book's equivalent of a Festie Bible scenario,
   and it gets the same treatment: its own video, full text, no cuts.
4. **The Mirror + The Discog** — a direct self-reflection ("have you done
   this?") followed by the Wook Discog, a four-stage character composite
   (Studio Debut → Live Album → Greatest Hits → sometimes a fourth stage)
   showing the same pattern at increasing severity. Works as a single
   "now turn it around" video.
5. **Tales From [Place] — The Save** — a full second narrative, same
   scenario as the cold open, but this time the counter-drop actually gets
   run and it works. The book's answer to "okay but what do I actually
   do" told as a story instead of a list. Its own video — it's the payoff
   beat, don't fold it into anything else.
6. **The Fanny Pack** — the chapter's own recap, structured as short named
   call-outs (one line per Track) plus, in most chapters, a block of
   pocket scripts (exact lines to say) and a Safety Appendix (legal/safety
   specifics — constructive possession, your rights at a gate, the
   dump-it-now protocol, that kind of thing). This is the single video
   someone re-watches before their next festival instead of the whole
   chapter — treat it as the chapter's highlight reel.
7. **The Soundcheck** — a short, named practical drill (3–4 steps, a few
   minutes). The most naturally "demonstrate this on camera" video in the
   whole chapter.
8. **The Sunrise Set + The Kandi Trade** — the closer. Sunrise Set is the
   chapter's thesis stripped of all slang, delivered straight. Kandi
   Trade is a vow, one line per commitment, read like a pledge. These are
   short and both closing-beat, so they're one video, not two, ending on
   the vow. The Bridge (a one-line tease into next chapter) is included as
   an optional stinger to read over the outro card — it's 40–90 words, not
   a video on its own.

**Five chapters (20, 27, 31, 32, 33) don't use Tracks at all** — they're
built differently on purpose (an emergency/response chapter, a resource
chapter, closing chapters). Those still produce the same 7 non-Track
videos (Drop, Setup, Mirror+Discog, Tales, Fanny Pack, Soundcheck,
Sunrise+Kandi); there's just no Track run in the middle. The generator
handles this automatically — nothing to chop differently by hand.

## Why this order, not some other one

The book already uses this order internally, chapter after chapter,
33 times without deviation. That consistency is the whole argument for
using it as the video plan instead of inventing a new one: a viewer who
watches chapter 3's Track videos already knows what a Fanny Pack video
from chapter 9 is going to be, without being told again. Matching the
book's own rhythm means the audience only has to learn the format once,
in chapter 1, and every chapter after that plays by the same rules.

It also happens to sort correctly by attention span. The cold open is the
hook (no context needed, pure scene). The setup is the trailer (what's
coming, why it matters). The Tracks are the meal (the actual teaching,
one idea per video). The Mirror+Discog and the Tales are the gut-check and
the payoff. The Fanny Pack, Soundcheck, and closer are the "if you only
watch three things" set — which is also, not coincidentally, the natural
place to point someone who found the channel through a single Track video
and wants the rest of the chapter without starting from the cold open.

## What this produces

33 files, one per chapter, in `content/wook-teleprompter/`, each internally
divided into `## 🎬 VIDEO N — <name>` sections in the order above, every
section carrying its own spoken-word count and an estimated read time at
150 words per minute (the same rate and disclosure style used for the
Festie Bible teleprompter scripts). See `00-INDEX.md` for the full
33-chapter manifest — chapter, Track count, video count, total words, file.

Read straight through, a chapter runs long (most land in the 6,000–13,000
spoken-word range — 40 minutes to over an hour at a natural pace). That's
expected and not a problem: nobody is meant to film "Chapter 12" as one
video. They're meant to film its 7–19 pieces as 7–19 separate uploads,
same logic as the Festie Bible's per-scenario posts, and let a viewer who
only wants the Borrowed Mule Track watch four minutes instead of an hour.

## Regenerating

Source of truth is `library/wook/index.html` — never hand-edit the output
files. Re-run `python3 scripts/wook-teleprompter-build.py` (or pass one or
more chapter numbers, e.g. `... 12 13`, to rebuild just those) any time the
live book changes, so these stay in sync with what's actually shipped.

## Natural next step, not done yet

This round produces one file per chapter, sectioned into videos — the
"give me a teleprompter MD... for each chapter" ask. It does **not** yet
split every Track/Tales/etc. into its own individually-postable file the
way the Festie Bible's 270 posts work, or add `[INSERT IMAGE HERE]`
markers, or a title-card image set. Both are straightforward follow-ups
using the same pipeline this used, if/when wanted.
