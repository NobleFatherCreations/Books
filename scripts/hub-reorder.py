#!/usr/bin/env python3
"""Reorder the hub: Art first, every book in one block, in a chosen order.

What the page did before this:

  hero → manifesto → Instruments → Library → Workshop → Music → Maker → Support

which opened the site on three software tools, put the craft between the books
and the music, and shelved the books in the order they happened to be built.
Asked for instead: the art at the top, all the books together underneath it in
a deliberate reading order, and the NFC guide featured at the foot of the page.

  hero → manifesto → Workshop → Library → Instruments → Music
       → The Guide → Maker → Support

Three things move independently and all three have to agree, or the page reads
as three different opinions about the same site:

  1. the sections themselves
  2. the numbers printed on them (00/01/02/03 chapter marks, VOL. I-XIV)
  3. the top navigation, and the Library/Workshop lists in the footer

So this script owns all three. It is idempotent in the sense that it asserts
its way in -- run it twice and the second run fails loudly on a missing anchor
rather than quietly producing a second Guide section.

This is the HUB ONLY. The books' own THE HOUSE drawer is a separate, canonical
order (scripts/nf-catalogue.py) that is append-only by design and is not
touched here -- the hub is an edited shelf, the drawer is an index.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT / "hub/catalogue-redesign.html"

# The shelf order, by the marker comment each card already carries.
# Festival and Codex lead (the festival pair, and the way most people arrive),
# then the two written for a specific reader -- women, then children -- then
# the two that describe the system itself, then the mechanics of coercion,
# then faith, then the four about who else it happens to, then the two about
# afterwards. Anyone can re-cut this list; nothing else here hard-codes it.
ORDER = [
    "10 · The Festie Bible",
    "3 · The Festie Codex",
    "1 · Sovereign Divine Feminine",
    "2 · Playground Protectors",
    "4 · The Fractal",
    "5 · The Fracture",
    "7 · The Loop",
    "8 · The Weighing",
    "6 · The Sacred Divide",
    "12 · The Silence",
    "13 · At Will",
    "15 · The Slow Take",
    "11 · The Long After",
    "14 · The Repair",
]
CLOSER = "9 · Collection closer"

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV"]

SECTION_RE = {
    "instruments": r'  <!-- =+ INSTRUMENTS =+ -->\n  <section class="section workshop-band" id="instruments">.*?\n  </section>\n',
    "library":     r'  <!-- =+ LIBRARY =+ -->\n  <section class="section" id="library">.*?\n  </section>\n',
    "workshop":    r'  <!-- =+ WORKSHOP =+ -->\n  <section class="section workshop-band" id="workshop">.*?\n  </section>\n',
    "music":       r'  <!-- =+ MUSIC =+ -->\n  <section class="section music-band" id="music">.*?\n  </section>\n',
}


def cut(html, name):
    """Lift a whole section out of the page, returning (rest, section)."""
    m = re.search(SECTION_RE[name], html, re.S)
    assert m, f"could not find the {name} section"
    return html[:m.start()] + html[m.end():], m.group(0)


def split_cards(library):
    """The library's cards, keyed by their existing marker comment."""
    body_open = '      <div class="library">\n\n'
    i = library.index(body_open) + len(body_open)
    j = library.index("\n      </div>\n    </div>\n  </section>", i)
    head, tail = library[:i], library[j:]

    cards, marks = {}, [
        (m.start(), m.group(1))
        for m in re.finditer(r"<!-- (\d+ · [^>]*?) -->", library[i:j])
    ]
    for n, (start, label) in enumerate(marks):
        end = marks[n + 1][0] if n + 1 < len(marks) else len(library[i:j])
        cards[label] = library[i:j][start:end].rstrip() + "\n"
    return head, cards, tail


def renumber(card, n):
    """Print the card's new place on it: the numeral and the VOL. code."""
    card, a = re.subn(r'(<span class="st-vol-n">)[^<]*(</span>)',
                      lambda m: m.group(1) + ROMAN[n] + m.group(2), card, count=1)
    card, b = re.subn(r'(<span class="st-vol-code">)VOL\. [^<]*(</span>)',
                      lambda m: m.group(1) + "VOL. " + ROMAN[n] + m.group(2),
                      card, count=1)
    assert a == 1 and b == 1, f"card {n}: numeral {a}, code {b}"
    return card


def reorder_library(library):
    head, cards, tail = split_cards(library)
    missing = [k for k in ORDER + [CLOSER] if k not in cards]
    assert not missing, f"cards not found: {missing}"
    extra = [k for k in cards if k not in ORDER + [CLOSER]]
    assert not extra, f"cards left unplaced: {extra}"

    out = []
    for n, label in enumerate(ORDER):
        card = renumber(cards[label], n)
        # Rewrite the marker comment too, so the source reads in shelf order
        # instead of preserving the build order it no longer has.
        card = card.replace(f"<!-- {label} -->",
                            f"<!-- {n + 1} · {label.split(' · ', 1)[1]} -->", 1)
        out.append(card)
    out.append(cards[CLOSER].replace(f"<!-- {CLOSER} -->",
                                     "<!-- closer · the collection -->", 1))
    return head + "\n".join(out) + tail


def renumber_chapter(section, num, name=None):
    """The big 00/01/02 mark at the head of a section."""
    section, n = re.subn(r'(<span class="st-chapter-num" aria-hidden="true">)\d+(</span>)',
                         lambda m: m.group(1) + num + m.group(2), section, count=1)
    assert n == 1, f"no chapter number in {name or 'section'}"
    return section


def main():
    html = HUB.read_text(errors="surrogateescape")

    html, instruments = cut(html, "instruments")
    html, library = cut(html, "library")
    html, workshop = cut(html, "workshop")
    html, music = cut(html, "music")

    library = reorder_library(library)

    # Art leads, so it takes 00 and everything below it shifts down one.
    workshop = renumber_chapter(workshop, "00", "workshop")
    library = renumber_chapter(library, "01", "library")
    instruments = renumber_chapter(instruments, "02", "instruments")
    music, n = re.subn(r'(<span class="st-kicker-n">)\d+(</span>)',
                       lambda m: m.group(1) + "03" + m.group(2), music, count=1)
    assert n == 1, "no kicker number in music"

    # Put them back, in the new order, where the first one used to start.
    assert JACKET.exists(), (
        f"{JACKET} missing — run scripts/covers/compose-guide-jacket.py first")
    guide = GUIDE_SECTION.replace("{jacket}", JACKET.read_text().strip())

    anchor = "  <!-- ===================== MAKER ===================== -->"
    assert html.count(anchor) == 1
    html = html.replace(
        anchor, workshop + "\n" + library + "\n" + instruments + "\n" + music
        + "\n" + guide + "\n" + anchor, 1)

    html = retop_nav(html)
    html = restats(html)
    html = redoors(html)
    html = refoot(html)
    html = reupdates(html)

    HUB.write_text(html, errors="surrogateescape")
    print(f"hub reordered: {len(html):,} bytes")
    for label in ORDER:
        print("   ", label.split(" · ", 1)[1])


# ---------------------------------------------------------------- navigation

OLD_NAV = """      <a href="#instruments">The Instruments</a>
      <a href="#library">The Library</a>
      <a href="#workshop">The Workshop</a>
      <a href="#music">The Music</a>
      <a href="#maker">The Maker</a>
      <a href="#support">Support</a>"""

NEW_NAV = """      <a href="#workshop">The Workshop</a>
      <a href="#library">The Library</a>
      <a href="#instruments">The Instruments</a>
      <a href="#music">The Music</a>
      <a href="#guide">The Guide</a>
      <a href="#maker">The Maker</a>
      <a href="#support">Support</a>"""


def retop_nav(html):
    assert html.count(OLD_NAV) == 1, "top nav not found in the expected shape"
    return html.replace(OLD_NAV, NEW_NAV, 1)


# The footer's Library list was still the nine books that existed before the
# 2026-09-01 round -- longafter, silence, atwill, repair and slowtake were
# added to the shelf and to the drawer but never to the footer, so the page
# has been quietly under-listing itself by five titles. Rebuilt whole, in
# shelf order, rather than patched, so the two can't drift again.
FOOT_LIBRARY = [
    ("festival",  "The Festie Bible"),
    ("wook",      "The Festie Codex"),
    ("feminine",  "The Sovereign Divine Feminine"),
    ("children",  "Playground Protectors"),
    ("fractal",   "The Fractal"),
    ("fracture",  "The Fracture"),
    ("loop",      "The Loop"),
    ("scale",     "The Weighing"),
    ("faith",     "The Sacred Divide"),
    ("silence",   "The Silence"),
    ("atwill",    "At Will"),
    ("slowtake",  "The Slow Take"),
    ("longafter", "The Long After"),
    ("repair",    "The Repair"),
]

GUIDE_FOOT_ROW = ('<li><a href="/nfc/" target="_blank" rel="noopener">'
                  "How to Program NFC Tags &mdash; the guide</a></li>")


def foot_list(html, heading, rows):
    """Replace one footer column's <ul> contents outright."""
    m = re.search(r'<h3[^>]*>\s*' + heading + r'\s*</h3>\s*<ul[^>]*>(.*?)</ul>',
                  html, re.S)
    assert m, f"footer list for {heading!r} not found"
    body = "\n          " + "\n          ".join(rows) + "\n        "
    return html[:m.start(1)] + body + html[m.end(1):]


def refoot(html):
    rows = [f'<li><a href="/{slug}" target="_blank" rel="noopener">{title}</a></li>'
            for slug, title in FOOT_LIBRARY]
    html = foot_list(html, "The Library", rows)

    # The guide belongs in the Workshop column -- it is the manual for what
    # the Workshop sells -- ahead of the TikTok row, which stays last.
    m = re.search(r'<h3[^>]*>\s*The Workshop\s*</h3>\s*<ul[^>]*>(.*?)</ul>',
                  html, re.S)
    assert m, "footer Workshop list not found"
    craft = re.findall(r"<li>.*?</li>", m.group(1), re.S)
    assert craft and "tiktok" in craft[-1].lower(), "unexpected Workshop list shape"
    assert not any("/nfc/" in r for r in craft), "guide already in the footer"
    return foot_list(html, "The Workshop", craft[:-1] + [GUIDE_FOOT_ROW] + craft[-1:])


# The four counters under the hero link straight into the sections, so their
# order is part of the navigation and has to move with it.
OLD_STATS = """      <li><a href="#instruments"><b data-nf-count>3</b><span>living tools</span></a></li>
      <li><a href="#library"><b data-nf-count>14</b><span>interactive books</span></a></li>
      <li><a href="#workshop"><b data-nf-count>3</b><span>NFC craft lines</span></a></li>"""

NEW_STATS = """      <li><a href="#workshop"><b data-nf-count>3</b><span>NFC craft lines</span></a></li>
      <li><a href="#library"><b data-nf-count>14</b><span>interactive books</span></a></li>
      <li><a href="#instruments"><b data-nf-count>3</b><span>living tools</span></a></li>"""


def restats(html):
    assert html.count(OLD_STATS) == 1, "hero counters not in the expected shape"
    return html.replace(OLD_STATS, NEW_STATS, 1)


# ------------------------------------------------------------- the three doors

# The words on two of the three gates are swapped, and have been live that
# way: the door to #workshop -- resin, wax seals, castings -- is labelled
# "Tools", and the door to #instruments -- Pattern Decoder, The Root, the
# Listening Room -- is labelled "Art / The Lab", which is not a section name
# anywhere on the site. Putting the art first is the moment to fix it, since
# a reader told the art is at the top would otherwise be sent to the software.
DOORS = [
    ("#workshop",    "--gate-silver", "Art",   "The Workshop"),
    ("#library",     "--gate-gold",   "Book",  "The Library"),
    ("#instruments", "--gate-white",  "Tools", "The Instruments"),
]

DOOR = ('<a class="st-portal" href="{href}" style="--pg-img:var({img})">'
        '<span class="pg-img" aria-hidden="true"></span>'
        '<span class="pg-shine" aria-hidden="true"></span>'
        '<span class="pg-scrim" aria-hidden="true"></span>'
        '<span class="pg-label"><b>{word}</b><span>{name}</span></span></a>')

TOUR_BODIES = {
    "The Workshop": "Hand-made objects with a living core: wax seals, resin "
                    "portals and cast pieces you can tap with a phone.",
    "The Library": "Fourteen field guides, free to read on any phone. No app, "
                   "no account, no sign-up.",
    "The Instruments": "Living apps and music — the pieces built to be returned "
                       "to, not just read once.",
}


def redoors(html):
    m = re.search(r'(<div class="st-portals">\n)(.*?)(\n    </div>)', html, re.S)
    assert m, "the three gates were not found in the expected shape"
    assert len(re.findall(r"<a class=\"st-portal\"", m.group(2))) == 3
    rows = "\n".join(
        "      " + DOOR.format(href=h, img=i, word=w, name=n)
        for h, i, w, n in DOORS)
    html = html[:m.start(2)] + rows + html[m.end(2):]

    # The walkthrough points at these by position, so its copy moves with them.
    for n, (_, _, word, name) in enumerate(DOORS, start=1):
        pat = (r"(\{ sel:'\.st-portals \.st-portal:nth-child\(%d\)'[^}]*?title:')"
               r"[^']*('[^}]*?body:')[^']*(')" % n)
        html, k = re.subn(pat, lambda mm: (mm.group(1) + f"{word} — {name}"
                                           + mm.group(2) + TOUR_BODIES[name]
                                           + mm.group(3)), html, count=1)
        assert k == 1, f"tour step {n} not found"
    return html


# ------------------------------------------------------------- patch notes

# The page's own updates block had stopped at v9 while sites.json ran on to
# v12 -- three shipped rounds a reader had no way to see. CLAUDE.md says these
# two are updated together, every time; this backfills the three that were
# missed and adds this round.
UPDATES = [
    ("v13", "2026-09-02", [
        "Added <strong>How to Program NFC Tags</strong> at the foot of the page — the "
        "complete free guide to putting anything you want on the chip inside your "
        "piece, with 139 recipes for iPhone and Android.",
        "Reorganised the page: the Workshop now opens it, all fourteen books sit "
        "together underneath in a proper reading order, and the tools and music "
        "follow. The menu at the top matches.",
        "The footer's book list was still showing nine titles out of fourteen. "
        "All fourteen are listed now.",
    ]),
    ("v12", "2026-09-01", [
        "Swapped the five new books' cover watermark to the author's own logo on the "
        "shelf jackets.",
    ]),
    ("v11", "2026-09-01", [
        "Added five new books to the Library — The Long After, The Silence, At Will, "
        "The Repair and The Slow Take — each with its own cover art.",
        "Corrected the book count in the header and the opening tour. The Catalogue "
        "now lists all twenty volumes on every page.",
    ]),
    ("v10", "2026-08-12", [
        "Fixed The Casting loading as unstyled text with no photos when opened from "
        "this site.",
        "Settled on one name for The Fracture, which had been appearing under three.",
        "New cover art for The Festie Codex.",
    ]),
]


def reupdates(html):
    anchor = '<section id="updates">\n      '
    i = html.index(anchor) + len(anchor)
    first = html.index('<p class="updates-version">', i - len(anchor))
    assert html[first:first + 60].find("v9") != -1, \
        "on-page updates no longer start at v9 — check before backfilling"

    blocks = []
    for n, (ver, date, lines) in enumerate(UPDATES):
        style = "" if n == 0 else ' style="margin-top:16px"'
        items = "".join(f"\n        <li>{l}</li>" for l in lines)
        blocks.append(f'<p class="updates-version"{style}>{ver} &mdash; {date}</p>\n'
                      f"      <ul>{items}\n      </ul>")
    # The old v9 block keeps its own margin-top, so give it one.
    tail = html[first:].replace('<p class="updates-version">v9',
                                '<p class="updates-version" style="margin-top:16px">v9', 1)
    return html[:first] + "\n      ".join(blocks) + "\n      " + tail


# ------------------------------------------------------------- the new section

JACKET = ROOT / "scripts/covers/_work/nfcguide-jacket.b64"

GUIDE_SECTION = """  <!-- ===================== THE GUIDE ===================== -->
  <section class="section workshop-band" id="guide">
    <div class="wrap">
      <div class="st-chapter reveal"><span class="st-chapter-num" aria-hidden="true">04</span><div class="st-chapter-body"><p class="st-chapter-name">The Guide</p><h2 class="st-chapter-title">How to program <em>your own chip</em></h2><span class="st-chapter-rule" aria-hidden="true"></span><p class="st-chapter-note">Free &middot; nothing to install but the app that writes tags &middot; works offline, on any phone</p></div></div>

      <div class="workshop">

        <!-- How to Program NFC Tags -->
        <article class="st-vol reveal" style="--glow:#c9a35b"><div class="st-vol-plate"><div class="st-book"><div class="st-book-face"><img src="data:image/jpeg;base64,{jacket}" alt="How to Program NFC Tags &mdash; the Dapper Dad figure holding a near-field signal" loading="lazy" /></div><span class="st-book-spine" aria-hidden="true"></span><span class="st-book-edge" aria-hidden="true"></span><span class="st-book-gloss" aria-hidden="true"></span></div><span class="st-shelf" aria-hidden="true"></span><span class="st-pool" aria-hidden="true"></span></div><div class="st-vol-entry"><div class="st-vol-rule"><span class="st-vol-n">01</span><span class="st-vol-code">THE GUIDE</span></div><span class="st-vol-category">Manual</span><h3 class="st-vol-title">How to Program NFC Tags</h3><p class="st-vol-sub">139 recipes, searchable, for iPhone and Android</p><p class="st-vol-hook">Five steps. Thirty seconds. Then it&#8217;s yours to change forever.</p><p class="st-vol-desc">Every piece from the Workshop has a chip sealed inside it, and this is the whole manual for putting anything you want on that chip &mdash; a song, a Wi-Fi password, a tribute, a business card, a treasure hunt &mdash; and rewriting it whenever you change your mind. A hundred and thirty-nine recipes, each with the exact record type and a value template you can copy straight into the app, plus how to choose the right tag and twelve real failure modes with what actually fixes each one. Written for people who have never programmed anything.</p><ul class="st-vol-tags"><li>139 recipes</li><li>iPhone &amp; Android</li><li>Works offline</li></ul><a class="st-vol-open" href="/nfc/" target="_blank" rel="noopener">Open the guide<span class="st-arr" aria-hidden="true">&#8594;</span></a></div><a class="stretch" tabindex="-1" href="/nfc/" target="_blank" rel="noopener" aria-label="Open How to Program NFC Tags"></a></article>

      </div>
    </div>
  </section>
"""


if __name__ == "__main__":
    sys.exit(main())
