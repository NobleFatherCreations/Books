"""Extract readable prose (headings + paragraphs, all markup stripped) from
the books whose content is static HTML. The Fractal and The Root store
their real content in JS data objects instead — use extract-prose-fractal.py
and extract-prose-root.py for those.

Run `python3 design/prep-audit.py` first if .audit-view/*.html is stale.
Usage: python3 design/extract-prose.py [--apply]   (dry-run prints word
counts only; --apply writes the .md files to .audit-view/prose/)
"""
import sys, re
from bs4 import BeautifulSoup, NavigableString

BOOKS = [
    ("sovereign", "The Sovereign Divine Feminine", ".audit-view/noble-father-sovereign.html"),
    ("playground", "Playground Protectors", ".audit-view/noble-father-playground.html"),
    ("festival", "The Festie Codex", ".audit-view/noble-father-festival.html"),
    ("fracture", "All Fracture", ".audit-view/noble-father-fracture.html"),
]

HEADING_TAGS = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}
BLOCK_TEXT_CLASSES_SKIP = {"c-tag"}  # small kicker labels handled inline, not worth their own line


def clean_text(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_book(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    soup = BeautifulSoup(raw, "html.parser")

    for tag in soup.find_all(["script", "style", "svg", "nav"]):
        tag.decompose()
    for tag in soup.find_all(attrs={"aria-hidden": "true"}):
        tag.decompose()

    lines = []
    seen_recent = []

    def emit(line):
        line = clean_text(line)
        if not line:
            return
        # collapse immediate duplicate lines (repeated chrome/labels)
        if seen_recent and seen_recent[-1] == line:
            return
        seen_recent.append(line)
        if len(seen_recent) > 3:
            seen_recent.pop(0)
        lines.append(line)

    body = soup.body or soup
    for el in body.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        # skip if nested inside another already-handled block element of the same walk
        # (find_all already returns all matches in document order; p inside li can double-emit,
        # so skip <p> whose parent is <li> since the <li> itself will be emitted)
        if el.name == "p" and el.find_parent("li"):
            continue
        cls = " ".join(el.get("class") or [])
        if any(c in BLOCK_TEXT_CLASSES_SKIP for c in cls.split()):
            continue
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name in HEADING_TAGS:
            emit(f"\n{HEADING_TAGS[el.name]} {text}\n")
        elif el.name == "li":
            emit(f"- {text}")
        elif el.name == "blockquote":
            emit(f"> {text}")
        else:
            emit(text)

    return "\n".join(lines)


def main():
    apply = "--apply" in sys.argv
    out_dir = ".audit-view/prose"
    import os
    os.makedirs(out_dir, exist_ok=True)

    for slug, title, path in BOOKS:
        text = extract_book(path)
        word_count = len(text.split())
        out_path = f"{out_dir}/{slug}.md"
        header = f"# {title}\n\n*Extracted from `{path}` — {word_count:,} words.*\n\n---\n\n"
        full = header + text + "\n"
        print(f"{slug:12s} {word_count:>7,} words  -> {out_path}")
        if apply:
            open(out_path, "w", encoding="utf-8").write(full)


if __name__ == "__main__":
    main()
