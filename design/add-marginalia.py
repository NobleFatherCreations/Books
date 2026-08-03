#!/usr/bin/env python3
"""Inject the marginalia component (design/marginalia.html's CSS) plus the
specific "see also" cross-reference notes both content-review agents
flagged (.audit-view/loop-content-review.md, scale-content-review.md).

These are added as clearly-marked editorial apparatus (a `.marginnote`,
visually distinct from body prose) — not a change to any chapter's frozen
prose. No existing sentence is edited; every note is new, separate,
side-column content, the same way a publisher's cross-reference or "see
also" note sits beside a text without becoming part of the author's
argument. `.reader` gets `position:relative` added so the notes can anchor
to it (currently missing — the previous measure-fix pass didn't need it).

Usage: python3 design/add-marginalia.py <loop|scale> [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Each book's own accent custom property — Loop defines --glow, Scale does
# not (it uses --bronze/--bronze2 for emphasis/hover instead). Hardcoding
# --glow here previously shipped an invalid var() reference into Scale.
ACCENT_VAR = {"loop": "--glow", "scale": "--bronze2"}

MARGINALIA_CSS_TEMPLATE = """<style id="nfc-marginalia-css">
  .marginnote {{
    float: none; position: absolute; left: 100%; margin-left: 32px; width: 240px;
    font-size: .82rem; line-height: 1.5; color: var(--ink2);
    border-left: 1px solid var(--line); padding-left: 14px;
  }}
  .marginnote a {{ color: var({accent}) }}
  .margin-toggle-label {{ cursor: pointer; border-bottom: 1px dotted var({accent}); color: inherit; }}
  .margin-toggle-input {{ display: none; }}
  @media (max-width: 1199px) {{
    .marginnote {{ position: static; float: none; display: none; width: auto; margin: 10px 0;
      padding: 10px 14px; background: var(--card); border-left: 3px solid var({accent}); border-radius: 4px; }}
    .margin-toggle-input:checked + .marginnote {{ display: block; }}
  }}
</style>
"""

NOTES = {
    "loop": {
        "reader_rule": ".reader{padding:24px 0 40px;max-width:65ch;margin-left:auto;margin-right:auto}",
        "reader_rule_new": ".reader{padding:24px 0 40px;max-width:65ch;margin-left:auto;margin-right:auto;position:relative}",
        "insertions": [
            (
                "id-mn-loop-1",
                '<strong>It cannot refuse you</strong> &mdash; and the capacity to be refused',
                'See also: <a href="https://noblefathercreations.com/feminine">The Sovereign Divine Feminine</a>, which addresses this same one-directional relational asymmetry directly.',
            ),
            (
                "id-mn-loop-2",
                '<li><strong>Inferred segment.</strong> Whatever category the model has placed you in, which you cannot see.</li>',
                'See also: <a href="#/c/16">Chapter sixteen</a>, which this chapter’s inference mechanism depends on directly.',
            ),
            (
                "id-mn-loop-3",
                'The comfortable assumption underneath most criticism of these systems is that you have preferences',
                'See also: <a href="#/c/4">Chapter four</a>, which first raised and answered this same objection about revealed preference.',
            ),
            (
                "id-mn-loop-4",
                'The relationship is real in one direction and the direction matters.',
                'See also: <a href="https://noblefathercreations.com/feminine">The Sovereign Divine Feminine</a>, which addresses this same one-directional relational asymmetry directly.',
            ),
            (
                "id-mn-loop-5",
                'The <b>magnitude</b> of their effect on actual political outcomes is genuinely uncertain',
                '<a href="#/limits">Appendix C</a> sorts every major claim in this book as well-evidenced, contested, or this book&rsquo;s own inference &mdash; including this one.',
            ),
            (
                "id-mn-loop-6",
                'The honest position: the strong version of the filter bubble is not well supported.',
                '<a href="#/limits">Appendix C</a> sorts every major claim in this book as well-evidenced, contested, or this book&rsquo;s own inference &mdash; this chapter&rsquo;s own text places this one in the contested category.',
            ),
            (
                "id-mn-loop-7",
                'The mechanism is not persuasion. It is <b>the steady relocation of what counts as moderate</b>, achieved by moving the surrounding material rather than by arguing with you.',
                '<a href="#/limits">Appendix C</a> sorts every major claim in this book as well-evidenced, contested, or this book&rsquo;s own inference &mdash; including this one.',
            ),
            (
                "id-mn-loop-8",
                'Books about new technology have a bad record, and this one owes you its own uncertainty rather than a confident finish.',
                'Companion piece: <a href="#/limits">Appendix C</a> covers this same ground &mdash; chapter by chapter, with what would falsify the book&rsquo;s own thesis.',
            ),
        ],
    },
    "scale": {
        "reader_rule": ".reader{padding:24px 0 40px;max-width:65ch;margin-left:auto;margin-right:auto}",
        "reader_rule_new": ".reader{padding:24px 0 40px;max-width:65ch;margin-left:auto;margin-right:auto;position:relative}",
        "insertions": [
            (
                "id-mn-scale-1",
                "BODIES[9]=`\n<p>",
                "Related to <a href=\"#/c/8\">Chapter eight</a>, but distinct: that was grief mistaken for analysis; this is memory rewriting itself after a revelation.",
            ),
            (
                "id-mn-scale-2",
                "Before probing anyone, answer these. Honestly, and quickly &mdash; this is not an exercise in fairness.</p>",
                "Worth running first: <a href=\"#/c/10\">Chapter ten</a>&rsquo;s pre-flight check. That one asks whether <em>you</em> are fit to judge right now &mdash; a different question from whether testing is safe, and this movement needs both answered.",
            ),
            (
                "id-mn-scale-3",
                "You do not need to prove intent to be entitled to a boundary.",
                "See also: <a href=\"https://noblefathercreations.com/loop\">The Loop</a>, which links to this exact sentence as its own foundation for separating intent from impact.",
            ),
            (
                "id-mn-scale-4",
                "<h3>The vocabulary of the middle</h3>",
                "See also: <a href=\"https://noblefathercreations.com/loop\">The Loop</a>, which cites this vocabulary by name.",
            ),
            (
                "id-mn-scale-5",
                "That is the whole thesis of the Fractal, arriving here as self-defence.",
                "See also: <a href=\"https://noblefathercreations.com/loop\">The Loop</a>, which cites this chapter twice as the foundation for its own argument about certainty.",
            ),
        ],
    },
}


def make_pair(note_id, note_html):
    n = note_id.replace("id-mn-", "")
    return (
        f'<label for="{note_id}" class="margin-toggle-label">*</label>'
        f'<input type="checkbox" id="{note_id}" class="margin-toggle-input">'
        f'<span class="marginnote">{note_html}</span>'
    )


def process(book, apply):
    cfg = NOTES[book]
    path = ROOT / "fixes" / f"{book}.html"
    text = path.read_text(encoding="utf-8")
    orig_len = len(text)

    if cfg["reader_rule_new"] not in text:
        count = text.count(cfg["reader_rule"])
        assert count == 1, f".reader rule: expected 1 match, got {count}"
        text = text.replace(cfg["reader_rule"], cfg["reader_rule_new"])
        added_css = True
    else:
        added_css = False

    if 'id="nfc-marginalia-css"' not in text:
        head_end = text.find("</head>")
        css = MARGINALIA_CSS_TEMPLATE.format(accent=ACCENT_VAR[book])
        text = text[:head_end] + css + text[head_end:]
        added_style = True
    else:
        added_style = False

    applied, skipped = 0, 0
    for note_id, anchor, note_text in cfg["insertions"]:
        if f'id="{note_id}"' in text:
            skipped += 1
            continue
        count = text.count(anchor)
        if count != 1:
            print(f"  WARN [{note_id}]: expected 1 anchor match, got {count} — skipping", file=sys.stderr)
            continue
        text = text.replace(anchor, anchor + make_pair(note_id, note_text), 1)
        applied += 1

    print(f"{book}: reader-position-fix={'new' if added_css else 'already present'}, "
          f"style-block={'new' if added_style else 'already present'}, "
          f"{applied} note(s) applied, {skipped} already present "
          f"({orig_len} -> {len(text)} bytes)")

    if apply:
        path.write_text(text, encoding="utf-8")
        print("  -> written")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("book", choices=list(NOTES))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    process(args.book, args.apply)
