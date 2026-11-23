#!/usr/bin/env python3
"""Move a one-page JS book (MOVEMENTS / CH / BODIES in library/<slug>/index.html) into the v2 source format:
content/<slug>-v2/plan.json, NN-<part>.md (=== slug / header / --- / body), old_routes.json.

Run:  python3 scripts/book/jsbook-to-v2.py scale [--extra /tmp/scale-extra.json]
--extra is a JSON of rendered views {"card": html, "limits": html} (JS-drawn appendices), saved by a browser.
Text is moved word for word. Book-specific boxes become ::: blocks:
  pull, try <label>, warn <label> (warn danger <label> when it carries the danger mark), gradient, compare <label>,
  aside (a margin note; it sits before the paragraph it belonged to).
Chapter links #/c/N become (ch:<slug>); #/card and #/limits become (ch:field-card) and (ch:limits).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/seo"))
import seo_common as S  # noqa: E402

ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii"]


def slug_of(t):
    return S.slugify(t, 60)  # same rule as build_jsbook.py, so every live chapter address stays


class Conv:
    def __init__(self, slugs):
        self.slugs = slugs  # n(str) -> slug

    def link(self, h):
        m = re.match(r"#/c/(\d+)$", h or "")
        if m:
            return "ch:" + self.slugs[m.group(1)]
        if h in ("#/card",):
            return "ch:field-card"
        if h in ("#/limits",):
            return "ch:limits"
        if h in ("#/", "#"):
            return "ch:contents"
        return h

    def inline(self, node):
        out = []
        for c in node.children:
            if isinstance(c, NavigableString):
                out.append(re.sub(r"\s+", " ", str(c)))
            elif c.name in ("em", "i"):
                t = self.inline(c).strip()
                out.append(f"*{t}*" if t else "")
            elif c.name in ("b", "strong"):
                t = self.inline(c).strip()
                out.append(f"**{t}**" if t else "")
            elif c.name == "a":
                out.append(f"[{self.inline(c).strip()}]({self.link(c.get('href'))})")
            elif c.name == "br":
                out.append("\n")
            elif c.name in ("label", "input"):
                continue  # margin-note toggle (the "*" button): presentation only
            elif c.name == "span" and "marginnote" in (c.get("class") or []):
                continue  # pulled out as an aside block by para()
            elif c.name == "span" and "k" in (c.get("class") or []):
                continue  # block label, read by box()
            elif c.name == "svg":
                continue
            else:
                out.append(self.inline(c))
        return "".join(out)

    def para(self, p):
        notes = [n for n in p.find_all("span", class_="marginnote")]
        pre = [f"::: aside\n{self.inline(n).strip()}\n:::\n" for n in notes]
        return "".join(pre) + self.inline(p).strip()

    def lst(self, el):
        ordered = el.name == "ol"
        rows = []
        for i, li in enumerate(el.find_all("li", recursive=False), 1):
            rows.append(f"{i}. " if ordered else "- ")
            rows[-1] += self.inline(li).strip()
        return "\n".join(rows)

    def table(self, t):
        rows = []
        for tr in t.find_all("tr"):
            cells = [self.inline(c).strip().replace("|", "\\|") for c in tr.find_all(["th", "td"])]
            rows.append("| " + " | ".join(cells) + " |")
            if tr.find("th") and len(rows) == 1:
                rows.append("|" + "---|" * len(cells))
        return "\n".join(rows)

    def box(self, d, kind):
        k = d.find("span", class_="k")
        label = re.sub(r"\s+", " ", k.get_text()).strip() if k else ""
        if kind == "warn" and d.find("svg", class_="danger-mark"):
            label = ("danger " + label).strip()
        head = f"::: {kind}" + (f" {label}" if label else "")
        return head + "\n" + self.blocks(d) + "\n:::"

    INLINE = {"em", "i", "b", "strong", "a", "br"}

    def blocks(self, root):
        out, buf = [], []

        def flush():
            if buf:
                frag = BeautifulSoup("".join(str(x) for x in buf), "html.parser")
                for line in self.inline(frag).split("\n"):
                    if line.strip():
                        out.append(line.strip())
                buf.clear()

        for el in list(root.children):
            if isinstance(el, NavigableString) or el.name in self.INLINE:
                buf.append(el)
                continue
            if el.name in ("label", "input", "svg") or (el.name == "span" and "k" in (el.get("class") or [])):
                continue
            if el.name == "span" and "marginnote" in (el.get("class") or []):
                out.append(f"::: aside\n{self.inline(el).strip()}\n:::")
                continue
            flush()
            cls = el.get("class") or []
            if el.name == "p":
                out.append(self.para(el))
            elif el.name in ("h3", "h2"):
                out.append("## " + self.inline(el).strip())
            elif el.name == "h4":
                out.append("### " + self.inline(el).strip())
            elif el.name in ("ul", "ol"):
                out.append(self.lst(el))
            elif el.name == "table":
                out.append(self.table(el))
            elif el.name == "span" and "k" in cls:
                continue
            elif el.name == "span" and "marginnote" in cls:
                out.append(f"::: aside\n{self.inline(el).strip()}\n:::")
            elif el.name in ("label", "input", "svg"):
                continue
            elif el.name == "div" and "pull" in cls:
                parts = [s.strip() for s in self.inline(el).split("\n") if s.strip()]
                out.append("::: pull\n" + "\n\n".join(parts) + "\n:::")
                for n in el.find_all("span", class_="marginnote"):
                    out.append(f"::: aside\n{self.inline(n).strip()}\n:::")
            elif el.name == "div" and "grad" in cls:
                out.append("::: gradient\n" + "\n".join("- " + s.get_text().strip() for s in el.find_all("span")) + "\n:::")
            elif el.name == "div" and ("try" in cls or "warn" in cls or "cmp-table" in cls):
                kind = "try" if "try" in cls else "warn" if "warn" in cls else "compare"
                out.append(self.box(el, kind))
            elif el.name in ("div", "section", "article", "main"):
                inner = self.blocks(el)
                if inner:
                    out.append(inner)
            else:
                t = self.inline(el).strip()
                if t:
                    out.append(t)
        flush()
        return "\n\n".join(x for x in out if x.strip())

    def convert(self, html):
        return self.blocks(BeautifulSoup(html, "html.parser"))


def page_decoder(path):
    if not path.exists():
        return []
    seen = []
    for h in re.findall(r'href="/playbook/([a-z0-9-]+)"', path.read_text()):
        if h not in seen:
            seen.append(h)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book")
    ap.add_argument("--extra", help="JSON of rendered JS views: {card, limits}")
    ap.add_argument("--out")
    a = ap.parse_args()
    lib = ROOT / "library" / a.book
    src = Path(a.out) if a.out else ROOT / "content" / f"{a.book}-v2"
    src.mkdir(parents=True, exist_ok=True)
    data = json.loads(subprocess.check_output(["node", str(ROOT / "scripts/seo/jsbook_extract.js"), str(lib / "index.html")]))
    CH, B, MV = data["CH"], data["BODIES"], data["MOVEMENTS"]
    slugs = {n: slug_of(c["t"]) for n, c in CH.items()}
    conv = Conv(slugs)
    parts, chapters, routes = [], [], {"chapters": {}, "card": "field-card", "limits": "limits"}
    for pi, m in enumerate(MV):
        pid = ROMAN[pi]
        parts.append({"id": pid, "title": m["t"], "blurb": m["b"], "chapters": [slugs[str(n)] for n in m["c"]]})
        lines = []
        for n in m["c"]:
            c, s = CH[str(n)], slugs[str(n)]
            routes["chapters"][str(n)] = s
            chapters.append({"slug": s, "part": pid, "n": n, "title": c["t"], "minutes": c.get("m"), "keyword": "",
                             "keywords2": [], "decoder": page_decoder(lib / f"{s}.html"), "heavy": False})
            lines += [f"=== {s}", f"title: {c['t']}", f"short: {c['d']}", "---", conv.convert(B[str(n)]), ""]
        (src / f"{pi + 1:02d}-{pid}.md").write_text("\n".join(lines))
    if a.extra:
        ex = json.loads(Path(a.extra).read_text())
        lines = []
        apx = []
        for key, slug, title in (("card", "field-card", "The field card"), ("limits", "limits", "The limits of this instrument")):
            soup = BeautifulSoup(ex[key], "html.parser")
            body = soup.find("article") or soup.find("main") or soup
            for nav in body.find_all(["nav"]) + body.find_all(class_=["crumb", "pager"]):
                nav.decompose()
            lede = body.find(class_=re.compile("lede|dek|sub"))
            short = lede.get_text(" ", strip=True) if lede else ""
            h1 = body.find("h1")
            if h1:
                title = h1.get_text(" ", strip=True)
                h1.decompose()
            if lede:
                lede.decompose()
            lines += [f"=== {slug}", f"title: {title}", f"short: {short}", "---", conv.convert(str(body)), ""]
            apx.append(slug)
            chapters.append({"slug": slug, "part": "appendix", "n": None, "title": title, "keyword": "", "keywords2": [],
                             "decoder": [], "heavy": False})
        parts.append({"id": "appendix", "title": "Appendices", "blurb": "", "chapters": apx})
        (src / f"{len(MV) + 1:02d}-appendix.md").write_text("\n".join(lines))
    (src / "plan.json").write_text(json.dumps({"parts": parts, "chapters": chapters}, indent=1, ensure_ascii=False) + "\n")
    (src / "old_routes.json").write_text(json.dumps(routes, indent=1) + "\n")
    print(f"{len(chapters)} pages, {len(parts)} parts -> {src.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
