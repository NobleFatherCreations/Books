#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grammar, spelling and formatting checker for the book.

The other two checkers cover claims (continuity) and surface typography
(proofread). This is the third thing a copy editor does: dialect
consistency, real misspellings, agreement errors, and formatting drift.

There is no spell-checker or dictionary in this environment, so the
misspelling check is dictionary-free and works on a property of long
books instead: in 335,000 words a real typo is almost always a hapax
(appears exactly once) that is one edit away from a word the book uses
often. "Chatper" next to 40 uses of "chapter" is a typo; "Sundog" used
once is a name. That catches the class that matters and produces very
few false positives.

    python3 scripts/wook-grammar-check.py
    python3 scripts/wook-grammar-check.py --only dialect,typos
    python3 scripts/wook-grammar-check.py --file library/festival/index.html

Checks:

  dialect     British spellings in a book written in American English,
              decided by counting the book's own usage rather than by
              assumption.
  typos       Hapax legomena within one edit of a frequent word.
  articles    "a" before a vowel sound, "an" before a consonant sound.
  punct       Doubled punctuation, space before punctuation, missing
              space after a sentence ends, spaced-out ellipses.
  caps        Sentences starting lowercase, and proper nouns the book
              capitalises inconsistently.
  compounds   A compound the book hyphenates in some places and not in
              others, where the grammatical role is the same.
  numbers     A figure used where the book's own house style spells the
              number out.

Exit code is 0 when no ERROR-level findings, 1 otherwise.
"""
import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "library/wook/index.html"

FINDINGS = []

# -ise/-ize words where both spellings are real; everything else (promise,
# surprise, exercise, supervise, compromise…) is -ise in every dialect and
# must never be flagged.
ALTERNATING = """
recognis organis apologis realis memoris mobilis metabolis rationalis
hospitalis monetis minimis maximis prioritis categoris summaris emphasis
legitimis normalis specialis utilis criticis characteris standardis
sensitis authoris theoris symbolis moralis capitalis
""".split()

OTHER_DIALECT = {
    "behaviour": "behavior", "behaviours": "behaviors",
    "colour": "color", "colours": "colors", "coloured": "colored",
    "favour": "favor", "favours": "favors", "favourite": "favorite",
    "honour": "honor", "honours": "honors", "labour": "labor",
    "neighbour": "neighbor", "neighbours": "neighbors",
    "defence": "defense", "defences": "defenses",
    "offence": "offense", "offences": "offenses",
    "practising": "practicing", "practised": "practiced",
    "travelling": "traveling", "travelled": "traveled",
    "cancelled": "canceled", "cancelling": "canceling",
    "whilst": "while", "learnt": "learned", "spelt": "spelled",
    "judgement": "judgment", "acknowledgement": "acknowledgment",
    "grey": "gray", "storey": "story", "kerb": "curb",
    "analyse": "analyze", "analysed": "analyzed", "analysing": "analyzing",
}

# Proper nouns whose capitalisation should be consistent wherever they appear.
PROPER = ["Zendo", "DanceSafe", "Narcan", "Signal", "Facebook", "Instagram",
          "Venmo", "Walgreens", "Discord", "Spotify", "Subaru", "Tacoma",
          "Sprinter", "Pelican", "Gatorade", "Costco", "Bunk Police",
          "Wharf Rats", "Good Samaritan", "Fireside", "RAINN"]

VOWEL_SOUND_EXCEPTIONS = {
    # written with a vowel, pronounced with a consonant -> takes "a"
    "a": {"one", "once", "united", "unique", "uniform", "universal", "university",
          "user", "usual", "useful", "euphemism", "european", "ubiquitous", "eulogy"},
    # written with a consonant, pronounced with a vowel -> takes "an"
    "an": {"hour", "honest", "honour", "honor", "heir", "mba", "fbi", "hiv", "llc",
           "nda", "rv", "suv", "x-ray", "icu", "id"},
}


def add(level, check, where, message, context=""):
    FINDINGS.append({"level": level, "check": check, "where": where,
                     "message": message,
                     "context": re.sub(r"\s+", " ", context).strip()[:200]})


class Doc:
    def __init__(self, path):
        raw = path.read_text(errors="surrogateescape")
        self.raw = re.sub(r'(src="data:[^"]{200,}")', 'src="data:..."', raw)
        self.starts = {int(m.group(1)): m.start() for m in
                       re.finditer(r'<div class="chwrap s\d" data-ch="(\d+)">', self.raw)}
        self.ends = {int(m.group(1)): m.start() for m in
                     re.finditer(r'<i class="ch-end" data-ch="(\d+)">', self.raw)}
        self.paras = [(m.start(), m.group(1)) for m in
                      re.finditer(r'<p[^>]*>(.*?)</p>', self.raw, re.S)]
        self.text = strip(self.raw)

    def locate(self, pos):
        for n, s in self.starts.items():
            if s <= pos < self.ends.get(n, s):
                return f"ch{n:02d}"
        return "book"


INLINE = ("span", "mark", "strong", "em", "b", "i", "a", "u", "code", "small",
          "sup", "sub", "abbr", "q", "s")
ENTS = {'&rsquo;': "’", '&lsquo;': "‘", '&rdquo;': '”', '&ldquo;': '“',
        '&mdash;': '—', '&ndash;': '–', '&hellip;': '…', '&nbsp;': ' ',
        '&middot;': '·', '&amp;': '&', '&#8217;': "’", '&quot;': '"',
        '&rarr;': '→', '&larr;': '←'}


def strip(s):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<svg\b.*?</svg>', ' ', s, flags=re.S)
    s = re.sub(r'</?(?:%s)\b[^>]*>' % "|".join(INLINE), '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    for k, v in ENTS.items():
        s = s.replace(k, v)
    return re.sub(r'[ \t]{2,}', ' ', s)


# ---------------------------------------------------------------- checks
def check_dialect(doc):
    """British spellings, judged against the book's own American usage."""
    ise = Counter()
    ize = Counter()
    for m in re.finditer(r'\b([A-Za-z]{3,}?)(is|iz)(e|es|ed|ing|ation|ations)\b',
                         doc.text):
        stem = m.group(1).lower()
        if not any(stem.startswith(a[:-2]) or a.startswith(stem) for a in ALTERNATING):
            continue
        (ise if m.group(2) == "is" else ize)[m.group(0).lower()] += 1

    for w, c in ise.items():
        for m in re.finditer(r'\b' + re.escape(w) + r'\b', doc.text, re.I):
            add("ERROR", "dialect", doc.locate(doc.raw.find(m.group(0))),
                f"British spelling {m.group(0)!r} — this book is American "
                f"({sum(ize.values())} -ize forms vs {sum(ise.values())} -ise)",
                doc.text[max(0, m.start() - 80):m.end() + 60])
            break

    for brit, amer in OTHER_DIALECT.items():
        cb = len(re.findall(r'\b' + brit + r'\b', doc.text, re.I))
        ca = len(re.findall(r'\b' + amer + r'\b', doc.text, re.I))
        if cb and ca >= cb:
            m = re.search(r'\b' + brit + r'\b', doc.text, re.I)
            add("ERROR", "dialect", doc.locate(doc.raw.find(m.group(0))),
                f"{brit!r} ({cb}x) against {amer!r} ({ca}x) — house style is the latter",
                doc.text[max(0, m.start() - 80):m.end() + 60])


def edits1(w):
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    out = set()
    for a, b in splits:
        if b:
            out.add(a + b[1:])
            if len(b) > 1:
                out.add(a + b[1] + b[0] + b[2:])
            for c in letters:
                out.add(a + c + b[1:])
        for c in letters:
            out.add(a + c + b)
    return out


def check_typos(doc):
    """A hapax one edit away from a word the book uses often."""
    words = [w.lower() for w in re.findall(r"\b[A-Za-z][A-Za-z’'-]{3,}\b", doc.text)]
    freq = Counter(words)
    common = {w for w, c in freq.items() if c >= 6}
    for w, c in freq.items():
        if c != 1 or len(w) < 5 or "’" in w or "-" in w:
            continue
        near = sorted(edits1(w) & common)
        if not near:
            continue
        m = re.search(r'\b' + re.escape(w) + r'\b', doc.text, re.I)
        add("ERROR", "typos", doc.locate(doc.raw.lower().find(w)),
            f"{w!r} appears once and is one edit from {near[0]!r} "
            f"({freq[near[0]]}x)",
            doc.text[max(0, m.start() - 90):m.end() + 70] if m else "")


def check_articles(doc):
    for m in re.finditer(r'\b(a|an)\s+([A-Za-z][A-Za-z-]*)', doc.text):
        art, word = m.group(1).lower(), m.group(2).lower()
        vowel = word[0] in "aeiou"
        if word in VOWEL_SOUND_EXCEPTIONS["a"]:
            want = "a"
        elif word in VOWEL_SOUND_EXCEPTIONS["an"]:
            want = "an"
        else:
            want = "an" if vowel else "a"
        if art != want:
            add("ERROR", "articles", doc.locate(doc.raw.find(m.group(0))),
                f"{art!r} before {m.group(2)!r} — should be {want!r}",
                doc.text[max(0, m.start() - 80):m.end() + 60])


def check_punct(doc):
    pats = [
        (r'[,;:]{2,}', "doubled punctuation"),
        (r'\s+[,;:.!?](?![’”"\)])', "space before punctuation"),
        (r'[a-z]{2}\.[A-Z][a-z]', "missing space after a sentence ends"),
        (r'\.\s\.\s\.', "spaced-out ellipsis — the book uses …"),
        (r'\?\!|\!\?', "?! — the book does not use this"),
        (r'--', "double hyphen where an em dash belongs"),
    ]
    for pos, para in doc.paras:
        t = strip(para)
        for rx, msg in pats:
            for m in re.finditer(rx, t):
                add("ERROR", "punct", doc.locate(pos), msg,
                    t[max(0, m.start() - 80):m.end() + 60])


def check_caps(doc):
    for name in PROPER:
        variants = Counter()
        for m in re.finditer(r'\b' + re.escape(name) + r'\b', doc.text, re.I):
            variants[m.group(0)] += 1
        if len(variants) > 1:
            good, n = variants.most_common(1)[0]
            for v, c in variants.items():
                if v == good:
                    continue
                m = re.search(r'\b' + re.escape(v) + r'\b', doc.text)
                add("ERROR", "caps", doc.locate(doc.raw.find(v)),
                    f"{v!r} ({c}x) against {good!r} ({n}x)",
                    doc.text[max(0, m.start() - 70):m.end() + 60] if m else "")


def check_compounds(doc):
    """A compound hyphenated in some places and open in others."""
    hy = Counter(m.group(0).lower() for m in
                 re.finditer(r'\b[a-z]{3,}-[a-z]{3,}\b', doc.text))
    for comp, c in hy.items():
        if c < 4:
            continue
        a, b = comp.split("-")
        # only compare where the open form is followed by a noun-ish word,
        # i.e. the same attributive role the hyphen marks
        open_uses = len(re.findall(r'\b' + a + r' ' + b + r'\b(?= [a-z])', doc.text))
        if open_uses >= 3 and c >= 4:
            add("WARN", "compounds", "book",
                f"{comp!r} hyphenated {c}x but open {open_uses}x in the same role",
                "")


def check_numbers(doc):
    """The book spells small numbers out; a bare figure stands out."""
    for pos, para in doc.paras:
        t = strip(para)
        for m in re.finditer(r'(?<![\d:$%.\-–])\b([2-9])\b(?![\d:%.\-–])', t):
            ctx = t[max(0, m.start() - 60):m.end() + 50]
            if re.search(r'\b(a\.m|p\.m|percent|dollars?|Step|Question|TRACK|'
                         r'PROTOCOL|Protocol|Track|Chapter|WAY|row|Row)\b', ctx):
                continue
            add("WARN", "numbers", doc.locate(pos),
                f"bare figure {m.group(1)!r} where the book spells numbers out", ctx)


CHECKS = {"dialect": check_dialect, "typos": check_typos, "articles": check_articles,
          "punct": check_punct, "caps": check_caps, "compounds": check_compounds,
          "numbers": check_numbers}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(DEFAULT))
    ap.add_argument("--only", default="")
    ap.add_argument("--level", default="ALL")
    args = ap.parse_args()

    doc = Doc(Path(args.file))
    names = [n.strip() for n in args.only.split(",") if n.strip()] or list(CHECKS)
    for n in names:
        CHECKS[n](doc)

    shown = [f for f in FINDINGS if args.level == "ALL" or f["level"] == args.level]
    counts = Counter(f["level"] for f in shown)
    print(f"Grammar check — {Path(args.file).name}, {len(shown)} findings")
    print("  " + "  ".join(f"{k}: {v}" for k, v in counts.items()) + "\n")
    by = defaultdict(list)
    for f in shown:
        by[f["check"]].append(f)
    for check in sorted(by):
        print("=" * 70)
        print(check.upper(), f"({len(by[check])})")
        print("=" * 70)
        for f in by[check][:60]:
            print(f"\n[{f['where']}] {f['message']}")
            if f["context"]:
                print(f"       … {f['context']}")
        print()
    sys.exit(1 if counts.get("ERROR") else 0)


if __name__ == "__main__":
    main()
