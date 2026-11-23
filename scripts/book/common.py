"""Shared loader for the book scripts: python3 scripts/book/<tool>.py --book longafter

Reads content/<book>-v2/book.json (falls back to content/<book>/book.json), the plan and the NN-*.md chapter files.
Read-only: nothing here writes book text.
"""
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(argv=None, desc=""):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("--book", default="longafter")
    ap.add_argument("--stdout", action="store_true", help="print the report instead of writing it")
    a = ap.parse_args(argv)
    for d in (ROOT / f"content/{a.book}-v2", ROOT / f"content/{a.book}"):
        if (d / "book.json").exists():
            break
    else:
        raise SystemExit(f"no book.json for {a.book}")
    cfg = json.loads((d / "book.json").read_text())
    plan = json.loads((d / cfg.get("plan", "plan.json")).read_text())
    text = {}
    for f in sorted(d.glob("[0-9][0-9]-*.md")):
        for block in re.split(r"^=== ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            slug, rest = block.split("\n", 1)
            head, _, body = rest.partition("\n---\n")
            text[slug.strip()] = {"meta": dict(re.findall(r"^(\w+):\s*(.+)$", head, re.M)), "body": body.strip(),
                                  "file": f.name}
    chapters = [dict(c, **text[c["slug"]]) for c in plan["chapters"] if c["slug"] in text]
    return a, d, cfg, plan, chapters


def write(a, d, name, report):
    if a.stdout:
        print(report)
    else:
        (d / name).write_text(report, encoding="utf-8")
        print(f"wrote {d.relative_to(ROOT)}/{name}")


def main_body(body):
    """The chapter text without its Sources section and without ::: block fences."""
    body = re.sub(r"^:::.*\n?", "", body, flags=re.M)
    return re.split(r"^## Sources\s*$", body, flags=re.M)[0].strip()


def plain(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"[*_`>#|]", "", t)
    return re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", t, flags=re.M).strip()


def words(t):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", plain(t))


def syllables(w):
    w = w.lower().strip("'’")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def grade(t):
    """Flesch-Kincaid grade of a stretch of prose."""
    p = plain(t)
    ws = words(p)
    sents = max(1, len(re.findall(r"[.!?]+(?=\s|$)", p)))
    if not ws:
        return 0.0
    return 0.39 * len(ws) / sents + 11.8 * sum(map(syllables, ws)) / len(ws) - 15.59


def blocks(body):
    """Split a body into (kind, text) blocks. Kinds: heading, list, quote, table, label (a **Bold lead.** paragraph), para."""
    out = []
    for b in re.split(r"\n\s*\n", body.strip()):
        b = b.strip()
        if not b:
            continue
        first = b.lstrip()
        if first.startswith("#"):
            kind = "heading"
            head, _, rest = b.partition("\n")
            out.append(("heading", head))
            if rest.strip():
                out.extend(blocks(rest))
            continue
        if re.match(r"(?:[-*]|\d+\.)\s", first):
            kind = "list"
        elif first.startswith(">"):
            kind = "quote"
        elif first.startswith("|"):
            kind = "table"
        elif re.match(r"\*\*[^*]{1,80}[.:?]\*\*", first):
            kind = "label"
        else:
            kind = "para"
        out.append((kind, b))
    return out


def chapter_class(c, cfg):
    rule = cfg.get("chapter_class", {})
    if rule.get("crisis") == "heavy" and c.get("heavy"):
        return "crisis"
    if c["part"] in rule.get("legal_parts", []):
        return "legal"
    return "default"
