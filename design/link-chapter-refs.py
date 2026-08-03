#!/usr/bin/env python3
"""Turn in-prose chapter references into real links.

These books constantly say "as in chapter four" or "chapter seventeen of
The Weighing" as plain text. This finds those (only inside var BODIES={...},
never touching JS, attributes, or already-linked text) and wraps just the
number word/digit in an <a> — same-book refs go to #/c/N, cross-book refs
(the "chapter N of <em>Other Book</em>" pattern) go to the other book's URL
via sites.json.

Conservative on purpose: only matches "chapter" + a real number word or
digit (a whitelist, not "any word"), so "this chapter offers..." or "the
chapter reads..." are correctly left alone. Idempotent — running twice
does not double-wrap.

Usage: python3 design/link-chapter-refs.py <path-to-book.html> [--apply]
Without --apply, prints a dry-run report only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NUM_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}
TENS = {"twenty": 20, "thirty": 30, "forty": 40}
for tens_word, base in TENS.items():
    NUM_WORDS[tens_word] = base  # bare "thirty", "forty" (bug: these were missing entirely)
    for ones_word, ones_val in list(NUM_WORDS.items())[:9]:  # one..nine
        NUM_WORDS[f"{tens_word}-{ones_word}"] = base + ones_val

# sort longest-first so "twenty-three" matches before "twenty"
NUM_PATTERN = "|".join(sorted((re.escape(w) for w in NUM_WORDS), key=len, reverse=True))
CHAPTER_RE = re.compile(
    rf"\bChapter\s+(?P<num>\d{{1,2}}|{NUM_PATTERN})\b"
    rf"(?:\s+of\s+<em>(?P<book>[^<]+)</em>)?",
    re.IGNORECASE,
)


def to_int(word):
    return int(word) if word.isdigit() else NUM_WORDS[word.lower()]


def load_book_urls():
    sites = json.loads((ROOT / "sites.json").read_text())
    by_title = {}
    for p in sites["projects"]:
        by_title[p["title"]] = p["url"]
    for extra in sites.get("otherLiveSites", []):
        by_title[extra["title"]] = extra["url"]
    return by_title


def process(path: Path, apply: bool):
    text = path.read_text(encoding="utf-8")
    start = text.find("var BODIES={")
    if start == -1:
        sys.exit(f"no 'var BODIES={{...}}' declaration found in {path}")
    # BODIES is populated as scattered `BODIES[N]=`...`;` assignments, not one
    # object literal — the region runs from the declaration to just after the
    # last such assignment.
    body_assignments = list(re.finditer(r"BODIES\[\d+\]\s*=\s*`.*?`;", text[start:], re.DOTALL))
    if not body_assignments:
        sys.exit(f"no BODIES[N]=`...`; assignments found in {path}")
    end = start + body_assignments[-1].end()

    book_urls = load_book_urls()
    region = text[start:end]
    already_linked = 0
    new_links = 0
    skipped_unknown_book = []

    def repl(m):
        nonlocal already_linked, new_links, skipped_unknown_book
        # Skip if we're inside an unclosed <a>: find the LAST <a  before this
        # match and check whether it already closed before we got here. A
        # fixed-width lookback isn't enough — if an earlier, unrelated link
        # closes within the window (e.g. two refs close together: "...</a>.
        # The claim in <a href=...>"), a naive "does '</a>' appear anywhere
        # in the window" check false-negatives and double-wraps.
        pre = region[max(0, m.start() - 300):m.start()]
        last_open = pre.rfind("<a ")
        if last_open != -1 and "</a>" not in pre[last_open:]:
            already_linked += 1
            return m.group(0)
        n = to_int(m.group("num"))
        book = m.group("book")
        label = f"Chapter {m.group('num')}" + (f" of <em>{book}</em>" if book else "")
        if book:
            url = book_urls.get(book)
            if not url:
                skipped_unknown_book.append(book)
                return m.group(0)
            href = f"{url}#/c/{n}"
        else:
            href = f"#/c/{n}"
        new_links += 1
        if book:
            return f'<a href="{href}">Chapter {m.group("num")}</a> of <em>{book}</em>'
        return f'<a href="{href}">Chapter {m.group("num")}</a>'

    new_region = CHAPTER_RE.sub(repl, region)

    print(f"{path.name}: {new_links} new links, {already_linked} already linked, skipped {len(skipped_unknown_book)} (unknown book: {set(skipped_unknown_book)})")

    if apply and new_links:
        new_text = text[:start] + new_region + text[end:]
        path.write_text(new_text, encoding="utf-8")
        print(f"  -> written")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    process(Path(args.path), args.apply)
