#!/usr/bin/env python3
"""Generate a self-contained chapter-index page for one book from chapters.json
+ sites.json. Usage: python3 design/build-chapter-index.py <book-slug>
Data is inlined at generation time — the shipped page makes no requests,
fetches no JSON, loads no external font/CSS. Regenerate whenever
chapters.json changes; don't hand-edit the output.
"""
import json
import pathlib
import sys
import html

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIPPET = (ROOT / "design" / "snippets.html").read_text()
CHAPTERS = json.loads((ROOT / "chapters.json").read_text())
SITES = json.loads((ROOT / "sites.json").read_text())


def esc(s):
    return html.escape(s) if isinstance(s, str) else s


def house_nav_html():
    rows = []
    for p in SITES["projects"]:
        title = esc(p.get("title") or p["slug"])
        url = esc(p["url"])
        tagline = esc(p.get("tagline") or "")
        rows.append(
            f'    <a data-nh="{esc(p["slug"])}" href="{url}"><b>{title}</b><i>{tagline}</i></a>'
        )
    return "\n".join(rows)


def build(slug):
    book = next((b for b in CHAPTERS["books"] if b["slug"] == slug), None)
    if not book:
        sys.exit(f"no book with slug '{slug}' in chapters.json")

    movements_html = []
    for mv in book["movements"]:
        name = f'MOVEMENT {mv["movement"]}' + (f' — {esc(mv["name"])}' if mv.get("name") else "")
        cards = []
        for ch in mv["chapters"]:
            blurb = esc(ch.get("blurb")) or "<em>blurb pending</em>"
            readmin = f'{ch["readMin"]} min' if ch.get("readMin") else ""
            cards.append(f"""
      <a class="nfc-card nfc-reveal" href="#ch{ch['n']}">
        <span class="nfc-card-n">{ch['n']:02d}</span>
        <span class="nfc-card-title">{esc(ch['title'])}</span>
        <span class="nfc-card-blurb">{blurb}</span>
        <span class="nfc-card-meta">{readmin}</span>
      </a>""")
        movements_html.append(f"""
    <section class="nfc-movement nfc-reveal">
      <h2>{name}</h2>
      <div class="nfc-cards">{"".join(cards)}</div>
    </section>""")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(book['title'])} — Contents</title>
{SNIPPET}
<style>
  body{{background:var(--nfc-bg);color:var(--nfc-ink);margin:0;padding:0 var(--sp-3) var(--sp-8);
    max-width:70ch;margin-inline:auto;line-height:1.6}}
  h1{{font-size:2.4rem;margin:var(--sp-6) 0 var(--sp-2);letter-spacing:-.01em}}
  .nfc-tagline{{color:var(--nfc-gold);font:600 .8rem/1 ui-monospace,monospace;
    letter-spacing:.08em;text-transform:uppercase;margin-bottom:var(--sp-5)}}
  .nfc-movement{{margin-top:var(--sp-6)}}
  .nfc-movement h2{{font:600 .85rem/1 ui-monospace,monospace;letter-spacing:.1em;
    text-transform:uppercase;color:var(--nfc-crimson);border-bottom:1px solid rgba(168,129,58,.3);
    padding-bottom:var(--sp-2)}}
  .nfc-cards{{display:flex;flex-direction:column;gap:var(--sp-2);margin-top:var(--sp-3)}}
  .nfc-card{{display:grid;grid-template-columns:auto 1fr auto;gap:var(--sp-1) var(--sp-2);
    align-items:baseline;padding:var(--sp-2);border-radius:6px;text-decoration:none;color:inherit;
    border:1px solid rgba(168,129,58,.15);transition:border-color .25s ease,transform .25s ease}}
  .nfc-card:hover{{border-color:var(--nfc-gold);transform:translateX(4px)}}
  .nfc-card-n{{font:600 1.1rem ui-monospace,monospace;color:var(--nfc-gold);grid-row:1 / 3}}
  .nfc-card-title{{font-size:1.15rem}}
  .nfc-card-blurb{{grid-column:2;font-size:.92rem;opacity:.7}}
  .nfc-card-meta{{font:500 .75rem ui-monospace,monospace;opacity:.55;white-space:nowrap}}
</style>
</head>
<body>
  <h1>{esc(book['title'])}</h1>
  <div class="nfc-tagline">Contents</div>
  {"".join(movements_html)}
  <nav aria-label="The House" style="margin-top:var(--sp-8);padding-top:var(--sp-4);
    border-top:1px solid rgba(168,129,58,.25);font-size:.85rem;opacity:.85">
{house_nav_html()}
  </nav>
</body>
</html>
"""
    out = ROOT / "design" / f"chapter-index-{slug}.html"
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "fracture")
