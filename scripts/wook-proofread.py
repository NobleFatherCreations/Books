#!/usr/bin/env python3
"""Mechanical proofreader for Wook in Sheep's Clothing.

The continuity checker (scripts/wook-continuity-check.py) verifies claims --
chapter counts, cross-references, rosters. It says nothing about the surface
of the prose. This is the other half: the defects a copy editor catches by
looking rather than by cross-checking.

    python3 scripts/wook-proofread.py                 # human report
    python3 scripts/wook-proofread.py --json          # machine-readable
    python3 scripts/wook-proofread.py --only quotes,glyphs

Checks:

  quotes      Doubled quotation marks (&ldquo;"..."&rdquo; renders as ""x""),
              straight quotes and apostrophes in a book set entirely in
              curly ones, and paragraphs whose curly quotes do not close.
  glyphs      Mojibake, replacement characters, and orphaned variation
              selectors -- the bare U+FE0F left behind when an emoji is
              stripped out of a heading.
  doubled     A word repeated back to back, and a sentence repeated back to
              back. Both survive rewriting passes because they read fine.
  spacing     Space before punctuation, runs of spaces inside a sentence,
              and a missing space after sentence-ending punctuation.
  chips       Pocket Script chips longer than the pill shape can hold. The
              tone audit's finding 4: reference material wearing the shape
              of a memorize-this line.
  labels      Every nav/drawer label checked against the heading of the
              section it points at. Catches a title that was rewritten in
              one place only.
  markup      Structural inconsistency between sibling sections -- a heading
              class that differs from its 25 siblings, an empty paragraph.
  placeholder Bracketed template text and build instructions.
  duplicates  Two components wearing the same name. The "Tales From ... The
              Save" headers are supposed to name distinct places, and four
              pairs had collided; Track titles and element ids must be
              unique outright.
  typography  House style, measured off the book rather than assumed: a
              hyphen standing in for an em dash, a time written in a format
              the other 360 are not, a straight ellipsis, a numeric range
              hyphenated where the book uses an en dash.
  sequence    A run of numbered headings inside one section that skips a
              number. Appendix A's index went 20, 22 with nothing saying
              why chapter 21 was absent.
  titlecase   A title-casing script's fingerprints on a mixed-case label:
              It's rendered "It'S", RV rendered "Rv". Invisible on the
              rail, which uppercases, and plainly wrong in the Setlist and
              the nav drawer, which do not.

Exit code is 0 when no ERROR-level findings, 1 otherwise.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"

FINDINGS = []

# (needle, reason) -- suppresses a known-good finding so the report stays
# readable. Same contract as the continuity checker's allowlist.
ALLOWLIST = [
    ("Slang current as of 2014",
     "Field Specimen kicker; the fragment style is deliberate."),
    ("Not like a nod nod",
     "ch1's doubled 'nod nod' is the sentence's joke, not a typo."),
    ("Tyler Smithson of [address]",
     "The book fills scripts in with bracketed slots -- [name], [specific "
     "thing], [location] -- more than fifty times. This is that device, not "
     "an unfilled template."),
    ("Please please be careful with what you take",
     "ch31's drafted text message from a parent. The doubling is the voice -- "
     "it is what the sentence is doing, and it gets deleted in the next line."),
    ("SPECIMEN SPECIMEN",
     "The decorative marquee band, not a sentence."),
    ("Row 14 at a festival at 10:54 pm from a stranger",
     "Lowercase 'pm' inside a text message a character typed. People text "
     "that way; the narration around it does not."),
    ("competitors - general",
     "A folder name a character made up, not prose."),
    ("Jess says: “…Okonkwo?”",
     "The ellipsis opens the line because she is trailing into it."),
]


def allowed(context, message):
    return any(n in context or n in message for n, _ in ALLOWLIST)


def add(level, check, where, message, context=""):
    ctx = re.sub(r"\s+", " ", context).strip()[:220]
    if allowed(ctx, message):
        return
    FINDINGS.append({"level": level, "check": check, "where": where,
                     "message": message, "context": ctx})


ENTITIES = {'&rsquo;': "’", '&lsquo;': "‘", '&rdquo;': '”', '&ldquo;': '“',
            '&mdash;': '—', '&ndash;': '–', '&hellip;': '…', '&nbsp;': ' ',
            '&middot;': '·', '&amp;': '&', '&#8217;': "’", '&quot;': '"'}


def unescape(s):
    for k, v in ENTITIES.items():
        s = s.replace(k, v)
    return s


INLINE = ("span", "mark", "strong", "em", "b", "i", "a", "u", "code",
          "small", "sup", "sub", "abbr", "q", "s")


def strip_tags(s):
    """Drop markup the way a browser renders it.

    Inline tags close up -- <mark>Wook</mark>. is "Wook." not "Wook ." --
    or every highlighted word in the book reads as a spacing error.
    """
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'</?(?:%s)\b[^>]*>' % "|".join(INLINE), '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'[ \t]{2,}', ' ', unescape(s))


class Book:
    def __init__(self, path):
        raw = path.read_text(errors="surrogateescape")
        self.raw = re.sub(r'(src="data:[^"]{200,}")', 'src="data:..."', raw)
        self.starts = {int(m.group(1)): m.start() for m in
                       re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', self.raw)}
        self.ends = {int(m.group(1)): m.start() for m in
                     re.finditer(r'<i class="ch-end" data-ch="(\d+)">', self.raw)}
        # Paragraph-level units: the real unit a copy editor reads.
        self.paras = [(m.start(), m.group(1)) for m in
                      re.finditer(r'<p[^>]*>(.*?)</p>', self.raw, re.S)]

    def locate(self, pos):
        for n, s in self.starts.items():
            if s <= pos < self.ends.get(n, s):
                return f"ch{n:02d}"
        return "book"


# ----------------------------------------------------------------------
# checks
# ----------------------------------------------------------------------
def check_quotes(book):
    """Doubled, straight, and unclosed quotation marks."""
    for m in re.finditer(r'&ldquo;\s*[“"]|[”"]\s*&rdquo;', book.raw):
        add("ERROR", "quotes", book.locate(m.start()),
            "quotation mark doubled -- entity and literal both present",
            book.raw[max(0, m.start() - 90):m.start() + 90])

    # Only same-direction doubles. ." followed by "X is two adjacent
    # quotations, which this book does constantly and correctly.
    for m in re.finditer(r'“\s*“|”\s*”', book.raw):
        add("ERROR", "quotes", book.locate(m.start()),
            "two curly quotation marks facing the same way, back to back",
            book.raw[max(0, m.start() - 90):m.start() + 90])

    for pos, para in book.paras:
        text = strip_tags(para)
        if not text:
            continue
        # Straight marks in a manuscript typeset entirely in curly ones.
        if '"' in text:
            add("WARN", "quotes", book.locate(pos),
                "straight double quote in running prose", text)
        for m in re.finditer(r"(?<=[A-Za-z])'(?=[A-Za-z]|\s|$)", text):
            add("WARN", "quotes", book.locate(pos),
                "straight apostrophe in running prose", text)
            break
        for m in re.finditer(r'(?:^|[\s(—])”(?=[^\s,.;:!?])', text):
            add("ERROR", "quotes", book.locate(pos),
                "closing quotation mark used to open a quotation", text)
            break
        if text.count('“') != text.count('”'):
            add("WARN", "quotes", book.locate(pos),
                f"unbalanced curly quotes ({text.count('“')} open, "
                f"{text.count('”')} close)", text)


def check_glyphs(book):
    """Mojibake, replacement characters, orphaned variation selectors."""
    for m in re.finditer(r'â€|Ã|Â[^\w\s]|�', book.raw):
        add("ERROR", "glyphs", book.locate(m.start()),
            "mojibake or replacement character",
            book.raw[max(0, m.start() - 80):m.start() + 80])

    # A bare U+FE0F with no emoji in front of it is the scar an emoji leaves
    # when it is deleted character by character.
    for m in re.finditer(r'(^|[>\s])️', book.raw):
        add("ERROR", "glyphs", book.locate(m.start()),
            "orphaned variation selector -- an emoji was stripped here",
            book.raw[max(0, m.start() - 60):m.start() + 90])


def check_doubled(book):
    """A word or a sentence repeated back to back."""
    skip = {"had", "that", "no", "very", "sooner", "long", "ha", "yeah", "one",
            "blah", "so", "night", "again", "more", "specimen"}
    for pos, para in book.paras:
        text = strip_tags(para)
        for m in re.finditer(r'\b([A-Za-z]{2,})\s+\1\b', text, re.I):
            if m.group(1).lower() in skip:
                continue
            add("ERROR", "doubled", book.locate(pos),
                f"word repeated: {m.group(1)} {m.group(1)}", text)
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 25]
        for a, b in zip(sents, sents[1:]):
            if a == b:
                add("WARN", "doubled", book.locate(pos),
                    "sentence repeated back to back", a)


def check_spacing(book):
    for pos, para in book.paras:
        text = strip_tags(para)
        if re.search(r'[A-Za-z”’]\s+[,.;:!?](\s|$)', text):
            add("WARN", "spacing", book.locate(pos), "space before punctuation", text)
        if re.search(r'[a-z]{2}[.!?][A-Z][a-z]', text):
            add("WARN", "spacing", book.locate(pos),
                "missing space after sentence-ending punctuation", text)


def check_chips(book):
    """Pocket Script chips too long for the pill shape they render as."""
    for m in re.finditer(r'<span class="chip">(.*?)</span>', book.raw, re.S):
        words = strip_tags(m.group(1)).split()
        # Fifteen is the audit's rule of thumb; the six scripts that land at
        # sixteen or seventeen are real scripts, so the line sits at 18.
        if len(words) > 17:
            add("WARN", "chips", book.locate(m.start()),
                f"pocket-script chip is {len(words)} words -- reference "
                f"material in a memorize-this shape",
                " ".join(words))


def check_labels(book):
    """Every drawer label against the heading it points at."""
    heads = {m.group(1): strip_tags(m.group(2)).strip()
             for m in re.finditer(r'id="([A-Za-z0-9_-]+)"[^>]*>\s*<h2[^>]*>(.*?)</h2>',
                                  book.raw, re.S)}
    # Appendix rows only: the Setlist's own rows are deliberately worded
    # differently from the headings they point at ("The Full Setlist").
    for m in re.finditer(r'<a class="dr-row" href="#(ap[A-Z])"[^>]*>(.*?)</a>',
                         book.raw, re.S):
        target, label = m.group(1), strip_tags(m.group(2)).strip()
        head = heads.get(target)
        if not head:
            continue
        # Drawer rows carry a letter chip then the title; the heading carries
        # an emoji, "APPENDIX X —", then the same title.
        tail = head.split("—")[-1].strip().lower()
        short = re.sub(r'^[A-Z]\s*', '', label).strip().lower()
        if tail and short and tail != short:
            add("ERROR", "labels", "book",
                f"nav label and heading disagree for #{target}",
                f"nav: {short!r} vs heading: {tail!r}")


def check_markup(book):
    """Sibling sections that stopped matching each other."""
    classes = {}
    for m in re.finditer(r'id="(ap[A-Z])"[^>]*>\s*<h2 class="([^"]+)"', book.raw):
        classes.setdefault(m.group(2), []).append(m.group(1))
    if len(classes) > 1:
        main = max(classes, key=lambda c: len(classes[c]))
        for cls, ids in classes.items():
            if cls == main:
                continue
            add("WARN", "markup", "book",
                f"appendix heading class {cls!r} differs from the {len(classes[main])} "
                f"siblings using {main!r}", ", ".join(ids))

    for m in re.finditer(r'<p[^>]*>\s*</p>', book.raw):
        add("WARN", "markup", book.locate(m.start()), "empty paragraph",
            book.raw[max(0, m.start() - 70):m.start() + 40])


def check_placeholder(book):
    pat = re.compile(r'\[(?:your|add|insert|author|imprint|website|contact|in vellum|'
                     r'tk|todo)[^\]]{0,80}\]|#REPLACE|data-here|Lorem ipsum|'
                     r'\[Title (?:One|Two|Three|Four|Five)\]|'
                     r'\[[^\]]{0,80}(?:list .{0,20} here|delete this element|'
                     r'one-line description)[^\]]{0,40}\]', re.I)
    for m in pat.finditer(book.raw):
        add("ERROR", "placeholder", book.locate(m.start()),
            "template or build-instruction text still in the manuscript",
            book.raw[max(0, m.start() - 80):m.start() + 120])


def check_duplicates(book):
    """Two components wearing the same name."""
    saves = {}
    for m in re.finditer(r'<p class="comp-title">(Tales From[^<]*)</p>', book.raw):
        saves.setdefault(strip_tags(m.group(1)).strip(), []).append(book.locate(m.start()))
    for name, where in saves.items():
        if len(where) > 1:
            add("ERROR", "duplicates", "book",
                f"{len(where)} chapters share one Save title", f"{name} — {where}")

    tracks = {}
    for m in re.finditer(r'<h3 class="track-title">(.*?)</h3>', book.raw, re.S):
        tracks.setdefault(strip_tags(m.group(1)).strip(), []).append(book.locate(m.start()))
    for name, where in tracks.items():
        if len(where) > 1:
            add("ERROR", "duplicates", "book",
                f"{len(where)} Tracks share one title", f"{name} — {where}")

    ids = {}
    for m in re.finditer(r'\sid="([^"]+)"', book.raw):
        ids.setdefault(m.group(1), 0)
        ids[m.group(1)] += 1
    for name, n in ids.items():
        if n > 1:
            add("ERROR", "duplicates", "book", f"element id used {n} times", name)


def check_typography(book):
    """House style, measured off the book rather than assumed."""
    text = strip_tags(book.raw)

    for m in re.finditer(r'\S\s-\s\S', text):
        add("WARN", "typography", "book", "hyphen standing in for an em dash",
            text[max(0, m.start() - 90):m.start() + 90])

    # 360-odd times are written "9:14 a.m." or "nine-forty-seven p.m."
    for m in re.finditer(r'\b\d{1,2}:\d{2}\s?[ap]m\b|\b\d{1,2}:\d{2}\s?[AP]\.?M\.?', text):
        add("WARN", "typography", "book",
            "time in a format the rest of the book does not use",
            text[max(0, m.start() - 90):m.start() + 60])

    if '...' in text:
        i = text.find('...')
        add("WARN", "typography", "book", "three periods where the book uses an ellipsis",
            text[max(0, i - 80):i + 80])

    for m in re.finditer(r'(?<![\d-])\b(\d{1,3})-(\d{1,3})\b(?!-)', text):
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo < hi <= 120:   # a range, not a phone number or a model year
            add("WARN", "typography", "book",
                "numeric range hyphenated where the book uses an en dash",
                text[max(0, m.start() - 70):m.start() + 70])


def check_sequence(book):
    """A run of numbered headings that skips a number."""
    for sec in re.finditer(r'<section[^>]*id="(ap[A-Z])"[^>]*>(.*?)</section>',
                           book.raw, re.S):
        nums = [int(x) for x in re.findall(r'<h[1-6][^>]*>Chapter (\d+)</h[1-6]>', sec.group(2))]
        if len(nums) < 3:
            continue
        missing = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
        if missing:
            add("ERROR", "sequence", "book",
                f"#{sec.group(1)} indexes chapters {min(nums)}-{max(nums)} "
                f"but skips {', '.join(map(str, missing))}",
                "an index that silently omits a chapter reads as an omission")


def check_titlecase(book):
    """Title-casing artifacts in mixed-case labels."""
    for m in re.finditer(r'<a class="(?:dr-row|sl-row)[^"]*" href="#ch\d+"[^>]*>(.*?)</a>',
                         book.raw, re.S):
        label = strip_tags(m.group(1)).strip()
        label = re.sub(r'^\d+\s*', '', label)
        if label.isupper():
            continue
        for bad in re.finditer(r'[a-z]’[A-Z]', label):
            add("ERROR", "titlecase", "book",
                "apostrophe-S capitalised inside a mixed-case label", label)
        # An initialism that a title-caser lowercased: The Rv, The Dj.
        for word in label.split():
            if (len(word) == 2 and word[0].isupper() and word[1].islower()
                    and word.upper() in {"RV", "DJ", "ID", "TV", "AM", "PM"}):
                add("ERROR", "titlecase", "book",
                    f"initialism title-cased to {word!r} in a nav label", label)


def check_headings(book):
    """Heading levels that skip a rung."""
    seq = [(m.start(), int(m.group(1))) for m in re.finditer(r'<h([1-6])\b', book.raw)]
    for (_, a), (pos, b) in zip(seq, seq[1:]):
        if b > a + 1:
            add("WARN", "headings", book.locate(pos),
                f"heading jumps from h{a} to h{b}",
                strip_tags(book.raw[pos:pos + 90]))


CHECKS = {
    "quotes": check_quotes,
    "glyphs": check_glyphs,
    "doubled": check_doubled,
    "spacing": check_spacing,
    "chips": check_chips,
    "labels": check_labels,
    "markup": check_markup,
    "placeholder": check_placeholder,
    "duplicates": check_duplicates,
    "typography": check_typography,
    "sequence": check_sequence,
    "titlecase": check_titlecase,
    "headings": check_headings,
}

ORDER = ["ERROR", "WARN", "INFO"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--file", default=str(WOOK))
    args = ap.parse_args()

    book = Book(Path(args.file))
    names = [n.strip() for n in args.only.split(",") if n.strip()] or list(CHECKS)
    for name in names:
        CHECKS[name](book)

    if args.json:
        print(json.dumps(FINDINGS, ensure_ascii=False, indent=2))
    else:
        counts = {lvl: sum(1 for f in FINDINGS if f["level"] == lvl) for lvl in ORDER}
        print(f"Wook proofread — {len(FINDINGS)} findings\n")
        print("  " + "   ".join(f"{lvl}: {counts[lvl]}" for lvl in ORDER if counts[lvl]))
        for lvl in ORDER:
            rows = [f for f in FINDINGS if f["level"] == lvl]
            if not rows:
                continue
            print("\n" + "=" * 70 + f"\n{lvl}\n" + "=" * 70 + "\n")
            for f in rows:
                print(f"[{f['where']}] ({f['check']}) {f['message']}")
                if f["context"]:
                    print(f"       … {f['context']} …")
                print()
    return 1 if any(f["level"] == "ERROR" for f in FINDINGS) else 0


if __name__ == "__main__":
    sys.exit(main())
