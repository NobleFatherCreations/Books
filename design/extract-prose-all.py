"""Regenerate the full-prose extraction for all 6 books (Sovereign,
Playground, Festie Codex, All Fracture, The Fractal, The Root) and
concatenate them into one delivery file.

Run this after ANY commit that changes a book's actual words, so the
extracted-prose deliverable never goes stale. Assumes .audit-view/*.html
is current — run `python3 design/prep-audit.py` first if unsure.

Usage: python3 design/extract-prose-all.py
"""
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

subprocess.run([sys.executable, "design/extract-prose.py", "--apply"], check=True)
subprocess.run([sys.executable, "design/extract-prose-fractal.py"], check=True)
subprocess.run([sys.executable, "design/extract-prose-root.py"], check=True)

PROSE_DIR = ".audit-view/prose"
OUT = ".audit-view/prose/ALL-BOOKS.md"
ORDER = ["sovereign", "playground", "festival", "fracture", "fractal", "root"]

parts = [
    "# Noble Father Creations — Extracted Book Prose\n",
    "Actual chapter/content text, stripped of all HTML/CSS/JS/images — "
    "regenerated from this repo's own source files. If a book's words "
    "changed since this was last generated, run "
    "`python3 design/extract-prose-all.py` again before treating this as "
    "current.\n",
    "---\n",
]
for slug in ORDER:
    path = f"{PROSE_DIR}/{slug}.md"
    if os.path.exists(path):
        parts.append(open(path, encoding="utf-8").read())
        parts.append("\n---\n")
    else:
        parts.append(f"\n*[{slug} not found — extraction may have failed, check the individual script's output above]*\n---\n")

full = "\n".join(parts)
open(OUT, "w", encoding="utf-8").write(full)
print(f"\nWrote {len(full.split()):,} words -> {OUT}")
