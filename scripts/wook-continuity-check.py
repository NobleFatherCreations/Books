#!/usr/bin/env python3
"""Continuity checker for Wook in Sheep's Clothing.

The 2026-09-10 cold-open audit was done by reading. That found real defects
but only inside THE DROP and "Tales From ... The Save" -- and the worst
class of bug (a self-reference that was correct in an earlier draft and
silently went wrong when the book grew) turned out to live mostly in the
OTHER sections: Tracks, the Fanny Pack, the Bridges, the Confession, the
appendices.

This checks the whole book, every section, mechanically.

    python3 scripts/wook-continuity-check.py            # human report
    python3 scripts/wook-continuity-check.py --json     # machine-readable
    python3 scripts/wook-continuity-check.py --only counts,callbacks

Checks, roughly in descending order of how much a reader would notice:

  counts      Claims about how many chapters the book has, or how many the
              reader has read so far. Verified against real position.
  callbacks   "Chapter N" cross-references. Flags out-of-range targets, and
              verifies "X appears in Chapters A, B, C" style roster claims
              against where the name actually appears.
  bridges     The end-of-chapter Bridge must tease chapter N+1. Sixteen of
              twenty-five pointed backwards before 2026-09-10.
  scenes      "<Name> from the <place>" claims, verified by checking the
              name and the place actually co-occur in one chapter.
  names       First names doing duty for unrelated characters in different
              chapters. Judgment required, so these are reported, not failed.
  orphans     Proper nouns that appear in the back half of a narrative
              section having never appeared earlier in it -- the "bandana
              guys" shape, where someone exits a scene they never entered.
  enumerated  "the sixteen moves", "seven Tracks", "twelve levers" and
              friends, checked against what is actually enumerated nearby.
  structure   Poster metadata (TRACKS, MIN READ) vs. real content, and the
              standard component set per chapter.
  placeholder Unfilled template text left in the manuscript.

Exit code is 0 when no ERROR-level findings, 1 otherwise, so it can gate a
deploy.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

TOTAL_CHAPTERS = 26

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "twenty-one": 21, "twenty-two": 22, "twenty-three": 23,
    "twenty-four": 24, "twenty-five": 25, "twenty-six": 26,
}

# Scene keywords that identify a chapter, for verifying "<Name> from the <X>"
SCENE_WORDS = ["yurt", "bus", "warehouse", "hot springs", "vendor row", "gate line",
               "bass stage", "row 14", "lot", "booth", "rail", "campfire",
               "apartment", "backyard", "gorge", "rest stop", "water station"]

# Words that get capitalised mid-sentence without being characters.
NOT_NAMES = {
    "The", "A", "An", "And", "But", "Not", "This", "That", "There", "Here",
    "It", "He", "She", "They", "You", "We", "I", "If", "When", "What", "Who",
    "Why", "How", "His", "Her", "Their", "Your", "My", "Our", "Its", "By",
    "For", "From", "With", "Without", "In", "On", "At", "To", "Of", "As",
    "So", "Then", "Now", "Every", "Some", "Most", "All", "No", "Yes", "Do",
    "Does", "Did", "Is", "Are", "Was", "Were", "Be", "Been", "Has", "Have",
    "Had", "Will", "Would", "Can", "Could", "Should", "May", "Might", "Must",
    "Chapter", "Chapters", "Track", "Tracks", "Appendix", "Wook", "Wooks",
    "Festie", "Festies", "PLUR", "Sunday", "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "January", "February", "March", "April",
    "June", "July", "August", "September", "October", "November", "December",
    "Step", "Source", "Green", "Yellow", "Red", "One", "Two", "Three", "Four",
    "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Both", "Each", "Just",
    "Only", "Even", "Still", "Also", "Because", "Before", "After", "Until",
    "While", "Where", "Which", "Whose", "Nobody", "Somebody", "Everyone",
    # The Wook Discog uses these as recurring section headings, not people.
    "Album", "Debut", "Compilation", "Studio", "Live", "Greatest", "Hits",
    "Neither", "Either", "Both", "Anyone", "Nothing", "Something",
    "Everything", "Anything", "Let", "Say",
    "Ask", "Run", "Watch", "Look", "Find", "Keep", "Make", "Take", "Give",
    "Go", "Get", "Put", "Call", "Tell", "Know", "Think", "Feel", "Want",
    "Need", "Like", "Love", "Live", "Leave", "Stay", "Stop", "Start",
}

FINDINGS = []

# Findings that are correct as written. A substring of the context, with the
# reason it is not a bug. Keep this short -- every entry is a check the tool
# will never make again, so an entry that is wrong hides a real defect later.
ALLOWLIST = [
    ("has been describing for nine chapters",
     "'nine chapters' here is the book's own motif -- the number of chapters "
     "the fifteen-minute briefing prevents, stated repeatedly in ch21 -- not a "
     "claim about the reader's position in the book."),
]


def allowed(context, message):
    for needle, _reason in ALLOWLIST:
        if needle in context or needle in message:
            return True
    return False


def add(level, check, chapter, message, context=""):
    ctx = context.strip()[:300]
    if allowed(ctx, message):
        return
    FINDINGS.append({
        "level": level, "check": check, "chapter": chapter,
        "message": message, "context": ctx,
    })


def strip(s):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'</p>\s*<p[^>]*>', '\n', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    for k, v in {'&rsquo;': "’", '&lsquo;': "‘", '&rdquo;': '”', '&ldquo;': '“',
                 '&mdash;': '—', '&ndash;': '–', '&amp;': '&', '&#8217;': "’",
                 '&middot;': '·', '&hellip;': '…', '&nbsp;': ' '}.items():
        s = s.replace(k, v)
    return re.sub(r'[ \t]{2,}', ' ', s)


class Book:
    def __init__(self, path):
        raw = path.read_text(errors="surrogateescape")
        # Strip the giant base64 payloads so nothing downstream chokes on them.
        self.raw = re.sub(r'(src="data:[^"]{200,}")', 'src="data:..."', raw)
        self.starts = {int(m.group(1)): m.start() for m in
                       re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', self.raw)}
        self.ends = {int(m.group(1)): m.start() for m in
                     re.finditer(r'<i class="ch-end" data-ch="(\d+)">', self.raw)}
        self.n = len(self.starts)
        self.html = {n: self.raw[self.starts[n]:self.ends[n]] for n in self.starts}
        self.text = {n: strip(h) for n, h in self.html.items()}
        first = min(self.starts.values()) if self.starts else len(self.raw)
        last = max(self.ends.values()) if self.ends else 0
        self.front = strip(self.raw[:first])
        self.back = strip(self.raw[last:])

    def locate(self, pos):
        for n in self.starts:
            if self.starts[n] <= pos < self.ends[n]:
                return n
        return None

    def section(self, n, cls):
        m = re.search(r'<section class="panel[^"]*\b%s\b[^"]*">(.*?)</section>' % cls,
                      self.html[n], re.S)
        return strip(m.group(1)) if m else None


# ----------------------------------------------------------------------
# checks
# ----------------------------------------------------------------------
def check_counts(book):
    """Claims about the book's length, or how far the reader has come.

    Only cumulative claims are checkable. "The next fifteen chapters" and
    "prevents nine chapters" are relative or rhetorical and are left alone;
    "we have spent X chapters together" and "the book has X chapters" are
    assertions about position, and those are exactly the ones that went
    stale when the Encore grew.
    """
    CUMULATIVE = re.compile(
        r'(in all|book has|have spent|just read|carried it through|'
        r'sitting inside for|reading about[^.]{0,40}for|accumulates across|'
        r'entire book has been|been about[^.]{0,30}for|chapters before this|'
        r'after|across the full|'
        # perfect-tense "has/have been ... for N chapters" -- a cumulative
        # claim. Bare "for N chapters" is not: "you pick it up for two
        # chapters and put it down" describes reading habit, not position.
        r'(?:has|have|had)\s+been\b[^.]{0,60}?for)\s*$', re.I)

    pat = re.compile(r'\b(' + '|'.join(NUMBER_WORDS) + r')[- ]chapters?\b', re.I)
    for m in pat.finditer(book.raw):
        claimed = NUMBER_WORDS[m.group(1).lower()]
        ch = book.locate(m.start())
        lead = strip(book.raw[max(0, m.start() - 60):m.start()])
        if not CUMULATIVE.search(lead):
            continue
        ctx = strip(book.raw[max(0, m.start() - 130):m.end() + 90])
        # Inside chapter N, a cumulative claim should be N-1 (what precedes)
        # or TOTAL (the whole book). Allow TOTAL-1 for "everything but this one".
        ok = {TOTAL_CHAPTERS, TOTAL_CHAPTERS - 1}
        if ch:
            ok |= {ch - 1, ch, TOTAL_CHAPTERS - ch}
        if claimed not in ok:
            add("ERROR", "counts", ch,
                f"cumulative claim of {claimed} chapters; book has {TOTAL_CHAPTERS}"
                + (f" and {ch - 1} precede this one" if ch else ""), ctx)


def check_callbacks(book):
    """Cross-references to other chapters."""
    # Out-of-range targets.
    for m in re.finditer(r'\bChapter\s+(\d{1,2})\b', book.raw):
        target = int(m.group(1))
        if target > TOTAL_CHAPTERS or target < 1:
            add("ERROR", "callbacks", book.locate(m.start()),
                f"references Chapter {target}, which does not exist",
                strip(book.raw[max(0, m.start() - 120):m.end() + 90]))

    # "<Name> appears in Chapters A, B and C" -- verify against reality.
    roster = re.compile(
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+appears?\s+in\s+Chapters?\s+'
        r'([\d,\sand]+)', re.I)
    for m in roster.finditer(book.raw):
        name = m.group(1).strip()
        claimed = sorted({int(x) for x in re.findall(r'\d+', m.group(2))})
        if not claimed:
            continue
        actual = sorted(n for n in book.text
                        if re.search(r'\b' + re.escape(name) + r'\b', book.text[n]))
        # The sentence making the claim sits in a chapter; ignore that one.
        here = book.locate(m.start())
        actual = [a for a in actual if a != here]
        missing = [c for c in claimed if c not in actual]
        if missing:
            add("ERROR", "callbacks", here,
                f"claims {name} appears in Chapters {claimed}; not found in {missing}. "
                f"Actual: {actual}",
                strip(book.raw[max(0, m.start() - 60):m.end() + 60]))


def check_bridges(book):
    """The Bridge at the end of chapter N must point the reader at N+1.

    This is the book's own signposting, so a stale number here sends people
    backwards into a chapter they already read. Sixteen of twenty-five were
    wrong before the 2026-09-10 pass, all of them pointing at the arrangement
    the book had before three chapters were inserted.
    """
    for n in sorted(book.html):
        m = re.search(r'<section class="panel pp-black prose bridge">(.*?)</section>',
                      book.html[n], re.S)
        if not m:
            if n != max(book.html):  # the last chapter has nothing to tease
                add("WARN", "bridges", n, "has no Bridge")
            continue
        text = strip(m.group(1))
        cited = {int(x) for x in re.findall(r'Chapter\s+(\d+)', text)}
        if not cited:
            add("INFO", "bridges", n, "Bridge names no chapter", text[:120])
        elif n + 1 not in cited:
            add("ERROR", "bridges", n,
                f"Bridge points at {sorted(cited)}; the next chapter is {n + 1}",
                text[:200])


def check_scenes(book):
    """'<Name> from the <place>' -- does that person appear in that scene?"""
    pat = re.compile(r'\b([A-Z][a-z]{2,})\s+from\s+the\s+([a-z0-9 ]{3,18}?)(?=[,.;]|\s+and\b)')
    for m in pat.finditer(book.raw):
        name, place = m.group(1), m.group(2).strip()
        if name in NOT_NAMES or place not in SCENE_WORDS:
            continue
        here = book.locate(m.start())
        hits = [n for n in book.text
                if re.search(r'\b' + re.escape(name) + r'\b', book.text[n])
                and re.search(re.escape(place), book.text[n], re.I)
                and n != here]
        if not hits:
            elsewhere = [n for n in book.text
                         if re.search(r'\b' + re.escape(name) + r'\b', book.text[n])
                         and n != here]
            add("ERROR", "scenes", here,
                f"'{name} from the {place}' -- no chapter contains both. "
                f"{name} appears in {elsewhere or 'no other chapter'}",
                strip(book.raw[max(0, m.start() - 80):m.end() + 80]))


def check_names(book):
    """One first name doing duty for unrelated characters."""
    seen = defaultdict(set)
    for n, txt in book.text.items():
        for name in set(re.findall(r'\b([A-Z][a-z]{2,})\b', txt)):
            if name in NOT_NAMES:
                continue
            # A capitalised word is a *person* if it speaks, or is introduced
            # with an age. "The Sunk Cost Swamp is..." passes a bare is/was
            # test; "Marcus says" and "Priya is twenty" do not fire for
            # archetype names or sentence-initial nouns.
            if re.search(r'\b%s\s+(says|said|texts|texted|asks|asked|replies|'
                         r'replied|nods|nodded|laughs|laughed)\b' % re.escape(name), txt) \
               or re.search(r'\b%s\s+is\s+(twenty|thirty|forty|fifty|sixty|seventeen|'
                            r'eighteen|nineteen|\d\d)\b' % re.escape(name), txt):
                seen[name].add(n)
    for name, chapters in sorted(seen.items()):
        if len(chapters) >= 3:
            add("WARN", "names", None,
                f"'{name}' is used as a character in {len(chapters)} chapters: "
                f"{sorted(chapters)} -- intentional recurring cast, or a collision?")


def check_orphans(book):
    """A named person who exits a scene they were never shown entering."""
    for n in book.text:
        for cls in ("comp-drop", "inter-tales"):
            sec = book.section(n, cls)
            if not sec or len(sec) < 800:
                continue
            split = int(len(sec) * 0.6)
            head, tail = sec[:split], sec[split:]
            for name in set(re.findall(r'\b([A-Z][a-z]{2,})\b', tail)):
                if name in NOT_NAMES:
                    continue
                # Must act like a person, not be a capitalised abstraction.
                if not re.search(r'\b%s\s+(says|said|is|was|walks|walked|gets|got|'
                                 r'leaves|left|takes|took|comes|came|texts|texted)\b'
                                 % re.escape(name), tail):
                    continue
                # A real character recurs; a sentence-initial noun usually
                # does not. Require two mentions, at least one of them not
                # at the start of a sentence.
                spots = list(re.finditer(r'\b' + re.escape(name) + r'\b', tail))
                if len(spots) < 2:
                    continue
                if not any(re.search(r'[a-z,;]\s+$', tail[max(0, s.start() - 12):s.start()])
                           for s in spots):
                    continue
                if re.search(r'\b' + re.escape(name) + r'\b', head):
                    continue
                ctx = re.search(r'.{0,90}\b%s\b.{0,90}' % re.escape(name), tail, re.S)
                add("WARN", "orphans", n,
                    f"'{name}' acts in the back of the {cls.replace('comp-', '').replace('inter-', '')} "
                    f"but never appears in the front of it",
                    ctx.group(0) if ctx else "")


def check_enumerated(book):
    """'the sixteen moves' / 'seven Tracks' vs. what is actually enumerated."""
    # Track claims are checkable exactly.
    for n in book.text:
        actual = len(re.findall(r'<span class="gate-tag track-tag">TRACK', book.html[n]))
        for m in re.finditer(r'\b(' + '|'.join(NUMBER_WORDS) + r')\s+Tracks?\b',
                             book.text[n], re.I):
            claimed = NUMBER_WORDS[m.group(1).lower()]
            if claimed != actual:
                add("ERROR", "enumerated", n,
                    f"claims {claimed} Tracks; chapter has {actual}",
                    m.group(0))
    # Other enumerations are reported for eyeballing, not auto-failed.
    for m in re.finditer(r'\b(' + '|'.join(NUMBER_WORDS) + r')\s+'
                         r'(moves|levers|bugs|pillars|questions|confessions|'
                         r'principles|steps|domains|fronts)\b', book.raw, re.I):
        word, thing = m.group(1).lower(), m.group(2).lower()
        add("INFO", "enumerated", book.locate(m.start()),
            f"claims {NUMBER_WORDS[word]} {thing} -- verify the list still has that many",
            strip(book.raw[max(0, m.start() - 90):m.end() + 70]))


def check_structure(book):
    """Poster metadata vs. real content, and the standard component set."""
    if book.n != TOTAL_CHAPTERS:
        add("ERROR", "structure", None,
            f"found {book.n} chapters, expected {TOTAL_CHAPTERS}")

    for n in book.text:
        m = re.search(r'poster-meta">([^<]*)', book.html[n])
        if m:
            claim = strip(m.group(1))
            tm = re.search(r'(\d+)\s*TRACKS?', claim)
            if tm:
                actual = len(re.findall(r'<span class="gate-tag track-tag">TRACK',
                                        book.html[n]))
                if int(tm.group(1)) != actual:
                    add("ERROR", "structure", n,
                        f"poster says {tm.group(1)} TRACKS, chapter has {actual}")
            rm = re.search(r'~?(\d+)\s*MIN READ', claim)
            if rm:
                words = len(book.text[n].split())
                est = words / 235.0  # silent reading pace
                if not (0.55 * est <= int(rm.group(1)) <= 1.9 * est):
                    add("WARN", "structure", n,
                        f"poster says ~{rm.group(1)} min read; {words:,} words "
                        f"is about {est:.0f} min")

        for cls, label in [("comp-drop", "cold open"),
                           ("inter-tales", "Tales From ... The Save"),
                           ("comp-fanny", "Fanny Pack"),
                           ("comp-kandi", "Kandi Trade")]:
            if cls not in book.html[n]:
                add("WARN", "structure", n, f"missing its {label}")


def check_placeholder(book):
    """Template text nobody filled in."""
    pat = re.compile(r'\[(?:your|Your|In Vellum|Author|AUTHOR|Year|TODO|TK|REPLACE)'
                     r'[^\]]{0,120}\]')
    for m in pat.finditer(book.raw):
        add("ERROR", "placeholder", book.locate(m.start()),
            "unfilled placeholder still in the manuscript", m.group(0))


CHECKS = {
    "counts": check_counts,
    "callbacks": check_callbacks,
    "bridges": check_bridges,
    "scenes": check_scenes,
    "names": check_names,
    "orphans": check_orphans,
    "enumerated": check_enumerated,
    "structure": check_structure,
    "placeholder": check_placeholder,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", help="comma-separated check names")
    ap.add_argument("--level", default="INFO", choices=["ERROR", "WARN", "INFO"])
    ap.add_argument("--file", default=str(WOOK))
    args = ap.parse_args()

    book = Book(Path(args.file))
    names = args.only.split(",") if args.only else list(CHECKS)
    for nm in names:
        nm = nm.strip()
        if nm not in CHECKS:
            print(f"unknown check: {nm}. known: {', '.join(CHECKS)}", file=sys.stderr)
            return 2
        CHECKS[nm](book)

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    keep = [f for f in FINDINGS if order[f["level"]] <= order[args.level]]
    keep.sort(key=lambda f: (order[f["level"]], f["chapter"] or 0, f["check"]))

    if args.json:
        print(json.dumps({"file": args.file, "chapters": book.n,
                          "findings": keep}, indent=2))
        return 1 if any(f["level"] == "ERROR" for f in keep) else 0

    print(f"Wook continuity check — {book.n} chapters, {len(keep)} findings\n")
    counts = defaultdict(int)
    for f in keep:
        counts[f["level"]] += 1
    print("  " + "   ".join(f"{k}: {counts[k]}" for k in ("ERROR", "WARN", "INFO")
                            if counts[k]) + "\n")

    last = None
    for f in keep:
        if f["level"] != last:
            print(f"\n{'=' * 70}\n{f['level']}\n{'=' * 70}")
            last = f["level"]
        where = f"ch{f['chapter']:02d}" if f["chapter"] else "book"
        print(f"\n[{where}] ({f['check']}) {f['message']}")
        if f["context"]:
            print(f"       … {f['context']} …")

    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
