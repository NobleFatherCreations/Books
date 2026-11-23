#!/usr/bin/env python3
"""Check a rewritten chapter file against its committed version (git HEAD).

  python3 scripts/book/rewrite-check.py content/<book>-v2/01-i-a.md [--ref HEAD]
The book comes from the file's folder; its book.json "rewrite" key can set scene_line, honest_line, crisis (link
targets a heavy chapter must keep) and headers (required header keys). Without it, The Long After's rules apply.
Per chapter: same slugs; every link kept; Sources section identical; scene/honest blocks still there with their
opening note lines; fences balanced; the plan keyword still in `short`; heavy chapters keep a crisis link; word change.
Exit 1 on any failure.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENE = "*This example is made up, built from patterns many people describe.*"
HONEST = "*An honest check, just for you. This is about what's in your hands now, not blame for what was done to you.*"
CRISIS = ("ch:when-its-more-than-aftermath", "ch:if-youre-not-safe-right-now", "ch:find-help")


def parse(t):
    out = {}
    for block in re.split(r"^=== ", t, flags=re.M)[1:]:
        slug, rest = block.split("\n", 1)
        head, _, body = rest.partition("\n---\n")
        out[slug.strip()] = (dict(re.findall(r"^(\w+):\s*(.+)$", head, re.M)), body)
    return out


def main():
    f = Path(sys.argv[1]); ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else "HEAD"
    rel = f.resolve().relative_to(ROOT).as_posix()
    old = parse(subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    new = parse(f.read_text(encoding="utf-8"))
    book_dir = f.resolve().parent
    plan = {c["slug"]: c for c in json.loads((book_dir / "plan.json").read_text())["chapters"]}
    cfg = json.loads((book_dir / "book.json").read_text()).get("rewrite", {}) if (book_dir / "book.json").exists() else {}
    scene_line, honest_line = cfg.get("scene_line", SCENE), cfg.get("honest_line", HONEST)
    crisis, headers = tuple(cfg.get("crisis", CRISIS)), cfg.get("headers", ["title", "question", "seo", "short"])
    bad = []
    if set(old) != set(new):
        bad.append(f"chapters differ: {set(old) ^ set(new)}")
    for s in old:
        if s not in new:
            continue
        (oh, ob), (nh, nb) = old[s], new[s]
        lk = lambda b: set(re.findall(r"\]\(([^)]+)\)", b.split("\n## Sources")[0]))
        lost = lk(ob) - lk(nb)
        if lost:
            bad.append(f"{s}: links lost {sorted(lost)}")
        src = lambda b: b.partition("\n## Sources")[2].strip()
        if src(ob) != src(nb):
            bad.append(f"{s}: Sources changed")
        for k in headers:
            if k not in nh:
                bad.append(f"{s}: header {k} missing")
        kw = plan[s].get("keyword", "").lower()
        if kw and kw not in nh.get("short", "").lower() and kw in oh.get("short", "").lower():
            bad.append(f"{s}: keyword '{kw}' dropped from short")
        opens, closes = len(re.findall(r"^::: \w", nb, re.M)), len(re.findall(r"^:::\s*$", nb, re.M))
        if opens != closes:
            bad.append(f"{s}: fences unbalanced ({opens} open, {closes} close)")
        for kind, line in (("scene", scene_line), ("honest", honest_line)):
            o, n = ob.count(f"::: {kind}"), nb.count(f"::: {kind}")
            if n < o:
                bad.append(f"{s}: {kind} blocks {o} -> {n}")
            if line and nb.count(line) < n:
                bad.append(f"{s}: a {kind} block lost its opening note line")
        if plan[s].get("heavy") and not any(c in nb for c in crisis):
            bad.append(f"{s}: heavy chapter lost its crisis link")
        wo, wn = len(ob.split()), len(nb.split())
        print(f"  {s}: {wo} -> {wn} words ({(wn - wo) * 100 // max(wo, 1):+d}%)")
    for b in bad:
        print("FAIL", b)
    print(f"{rel}: {len(bad)} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
