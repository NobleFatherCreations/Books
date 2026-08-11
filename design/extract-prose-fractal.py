"""Extract The Fractal's real content — it lives in a JS `const DATA = {...}`
object (which happens to be valid JSON) rather than static HTML, so
extract-prose.py returns nothing for it. Run from the repo root.
Usage: python3 design/extract-prose-fractal.py
"""
import json, os

PATH = os.path.join(os.path.dirname(__file__), "..", ".audit-view", "noble-father-fractal.html")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", ".audit-view", "prose")
OUT = os.path.join(OUT_DIR, "fractal.md")
os.makedirs(OUT_DIR, exist_ok=True)

text = open(PATH, encoding="utf-8").read()
i = text.find("const DATA = ") + len("const DATA = ")
data, _ = json.JSONDecoder().raw_decode(text, i)

out = []
out.append("# The Fractal\n")
out.append("*Extracted from the book's own JS data object (`const DATA`) in "
            "`.audit-view/noble-father-fractal.html` — this is an interactive "
            "technique-decoder/constellation-map tool, not a linear chapter book, "
            "so content is organized here by its real sections: framing chapters, "
            "the 8 cycle stages, and the 30 sectors.*\n")
out.append("---\n")


def block_text(blocks):
    lines = []
    for b in blocks:
        t = b.get("t")
        x = b.get("x", "")
        if t == "h":
            lines.append(f"\n### {x}\n")
        elif t == "p":
            lines.append(x)
        elif t == "q":
            lines.append(f"> {x}")
        else:
            lines.append(x)
    return "\n\n".join(l for l in lines if l)


out.append("## Framing chapters\n")
for c in data["closings"]:
    out.append(f"\n## {c.get('kicker','')} — {c.get('title','')}\n")
    if c.get("sub"):
        out.append(f"*{c['sub']}*\n")
    out.append(block_text(c.get("blocks", [])))

out.append("\n\n---\n\n## The eight cycle stages\n")
for s in data["stages"]:
    out.append(f"\n### {s['n']}. {s['name']} — {s['fn']}\n")
    out.append(f"**What it looks like:** {s['gloss']}\n")
    out.append(f"**What it actually is:** {s['truth']}\n")
    out.append(f"**What it sounds like:** {s['sound']}\n")

out.append("\n\n---\n\n## The thirty sectors\n")
for sec in data["sectors"]:
    n = sec["num"]
    name = sec.get("full") or sec.get("short")
    out.append(f"\n### Sector {n}: {name}\n")
    if sec.get("controls"):
        out.append(f"*Controls: {sec['controls']}*\n")
    tech_name = data["techNames"][n - 1] if n - 1 < len(data["techNames"]) else None
    essence = data["essence"].get(str(n))
    if tech_name:
        out.append(f"**Technique: {tech_name}**")
        if essence:
            out.append(f" — {essence}")
        out.append("\n")
    out.append(sec.get("narrative", ""))

full_text = "\n".join(out)
word_count = len(full_text.split())
open(OUT, "w", encoding="utf-8").write(full_text)
print(f"fractal: {word_count:,} words -> {OUT}")
