"""Split each book's extracted prose (.audit-view/prose/*.md) into smaller
chunks at natural ## section boundaries, so external tools with tighter
file/context limits (a chat UI, a smaller-context model) can actually read
a whole chunk instead of silently truncating mid-book.

Usage: python3 design/chunk-prose.py [--words N] [--out DIR]
Default target: ~8000 words per chunk (never splits a section in half).
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_DIR = os.path.join(ROOT, ".audit-view", "prose")
OUT_DIR = os.path.join(ROOT, ".audit-view", "prose-chunks")

TARGET_WORDS = 8000
BOOKS = ["sovereign", "playground", "festival", "fracture", "fractal", "root"]


def split_sections(text):
    """Split on lines starting with '## ' (keeps the heading with its body)."""
    lines = text.split("\n")
    sections = []
    current = []
    for line in lines:
        if line.startswith("## ") and current:
            sections.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current))
    return sections


def chunk_book(slug, target_words):
    path = os.path.join(IN_DIR, f"{slug}.md")
    if not os.path.exists(path):
        print(f"{slug}: no prose file found, skipping")
        return
    text = open(path, encoding="utf-8").read()

    # first "section" (before the first ##) is the title + intro note
    header_end = text.find("\n## ")
    if header_end == -1:
        preamble = text
        sections = []
    else:
        preamble = text[:header_end]
        sections = split_sections(text[header_end + 1:])

    title_line = preamble.split("\n", 1)[0].lstrip("# ").strip()

    chunks = []
    current_sections = []
    current_words = 0
    for sec in sections:
        w = len(sec.split())
        if current_sections and current_words + w > target_words:
            chunks.append(current_sections)
            current_sections = []
            current_words = 0
        current_sections.append(sec)
        current_words += w

    if current_sections:
        chunks.append(current_sections)

    if not chunks:
        chunks = [[]]

    total = len(chunks)
    out_paths = []
    for i, secs in enumerate(chunks, start=1):
        body = "\n\n".join(secs)
        out = f"# {title_line} — part {i} of {total}\n\n" + preamble.split("\n", 1)[-1].strip() + "\n\n---\n\n" + body
        out_name = f"{slug}-part{i:02d}-of-{total:02d}.md"
        out_path = os.path.join(OUT_DIR, out_name)
        open(out_path, "w", encoding="utf-8").write(out)
        out_paths.append((out_name, len(body.split())))

    print(f"{slug}: {total} chunk(s)")
    for name, wc in out_paths:
        print(f"  {name}  ({wc:,} words)")


def main():
    target = TARGET_WORDS
    if "--words" in sys.argv:
        target = int(sys.argv[sys.argv.index("--words") + 1])
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug in BOOKS:
        chunk_book(slug, target)


if __name__ == "__main__":
    main()
