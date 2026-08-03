#!/usr/bin/env python3
"""Generate the library index — one page mapping the whole 9-book corpus.

This is VISION.md's Wait But Why move: "nobody currently sees the scale of
this — ~85+ finished chapters across nine books that already cite each
other." Bakes sites.json + chapters.json into one self-contained page at
generation time (same discipline as build-chapter-index.py — no runtime
fetch, file:// pages can't fetch sibling JSON).

Usage: python3 design/build-library-index.py
"""
import base64
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = json.loads((ROOT / "sites.json").read_text())
CHAPTERS = json.loads((ROOT / "chapters.json").read_text())
FRAUNCES = ROOT / "tools" / "fonts" / "fraunces"

chapters_by_slug = {b["slug"]: b for b in CHAPTERS["books"]}


def esc(s):
    return html.escape(s) if isinstance(s, str) else s


def font_face():
    roman = base64.b64encode((FRAUNCES / "Fraunces[SOFT,WONK,opsz,wght].ttf").read_bytes()).decode("ascii")
    italic = base64.b64encode((FRAUNCES / "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf").read_bytes()).decode("ascii")
    return f"""
  @font-face {{ font-family:'Fraunces'; font-style:normal; font-weight:1 999; font-display:swap;
    src:url(data:font/ttf;base64,{roman}) format('truetype-variations'); }}
  @font-face {{ font-family:'Fraunces'; font-style:italic; font-weight:1 999; font-display:swap;
    src:url(data:font/ttf;base64,{italic}) format('truetype-variations'); }}
"""


def book_card(p):
    slug = p["slug"]
    book = chapters_by_slug.get(slug)
    movements = book.get("movements", []) if book else []
    total_chapters = sum(len(mv["chapters"]) for mv in movements)

    if total_chapters:
        mv_rows = "".join(
            f'<div class="mv-row"><span class="mv-num">{esc(mv["movement"])}</span>'
            f'<span class="mv-name">{esc(mv.get("name") or "")}</span>'
            f'<span class="mv-count">{len(mv["chapters"])} ch.</span></div>'
            for mv in movements
        )
        meta = f'<div class="book-count">{total_chapters} chapters &middot; {len(movements)} movements</div>'
        detail = f'<div class="mv-list">{mv_rows}</div>'
    else:
        meta = '<div class="book-count book-count-pending">chapter map not yet catalogued</div>'
        detail = ""

    return f"""
    <a class="book-card reveal" href="{esc(p['url'])}">
      <div class="book-title">{esc(p['title'])}</div>
      <div class="book-tagline">{esc(p.get('tagline') or '')}</div>
      {meta}
      {detail}
    </a>"""



# playbook = a lookup tool ("type what happened"), music = a media page —
# neither is a chapter book, per BOOKS.md's own analysis. Keep them out of
# the "N works" book count and give them their own small section instead.
TOOL_SLUGS = {"playbook", "music"}


def build():
    all_projects = SITES["projects"]
    books = [p for p in all_projects if p["slug"] not in TOOL_SLUGS]
    tools = [p for p in all_projects if p["slug"] in TOOL_SLUGS]
    total_known_chapters = sum(
        len(ch["chapters"])
        for b in CHAPTERS["books"]
        for ch in b.get("movements", [])
    )
    cards = "\n".join(book_card(p) for p in books)
    tool_cards = "\n".join(book_card(p) for p in tools)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Library — Noble Father Creations</title>
<style>
{font_face()}
:root{{
  --bg:#14110d; --ink:#e4dcc8; --ink2:#a89a7d; --gold:#a8813a; --crimson:#8a2432;
  --card:#1b1712; --line:rgba(168,129,58,.22);
  --serif:'Fraunces','Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif;
  --sp-1:8px;--sp-2:16px;--sp-3:24px;--sp-4:32px;--sp-5:48px;--sp-6:64px;--sp-7:96px;
}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--serif);margin:0;
  padding:var(--sp-7) var(--sp-3) var(--sp-7);}}
.wrap{{max-width:920px;margin:0 auto}}
.kicker{{font:600 .78rem/1 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gold);text-align:center;margin-bottom:var(--sp-2)}}
h1{{font-size:clamp(2.4rem,6vw,4rem);text-align:center;margin:0 0 var(--sp-2);font-weight:600;
  letter-spacing:-.01em}}
h1 em{{color:var(--gold)}}
.sub{{text-align:center;color:var(--ink2);font-style:italic;font-size:1.15rem;
  max-width:56ch;margin:0 auto var(--sp-3)}}
.stats{{display:flex;justify-content:center;gap:var(--sp-5);margin:var(--sp-5) 0 var(--sp-6);
  padding:var(--sp-3) 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.stat{{text-align:center}}
.stat b{{display:block;font-size:1.8rem;color:var(--gold)}}
.stat span{{font:500 .7rem ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;
  color:var(--ink2)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:var(--sp-3)}}
.book-card{{display:block;background:var(--card);border:1px solid var(--line);border-radius:8px;
  padding:var(--sp-3);text-decoration:none;color:inherit;transition:border-color .3s ease,transform .3s ease}}
.book-card:hover{{border-color:var(--gold);transform:translateY(-3px)}}
.book-title{{font-size:1.3rem;font-weight:600;margin-bottom:4px}}
.book-tagline{{font-style:italic;color:var(--ink2);font-size:.92rem;margin-bottom:var(--sp-2)}}
.book-count{{font:600 .72rem ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;
  color:var(--crimson);margin-bottom:var(--sp-1)}}
.book-count-pending{{color:var(--ink2);opacity:.6;text-transform:none;font-style:italic;letter-spacing:0}}
.mv-list{{margin-top:var(--sp-2);border-top:1px solid var(--line);padding-top:var(--sp-1)}}
.mv-row{{display:flex;gap:var(--sp-1);font-size:.8rem;padding:2px 0;color:var(--ink2)}}
.mv-num{{font:600 .75rem ui-monospace,monospace;color:var(--gold);min-width:1.6em}}
.mv-name{{flex:1}}
.mv-count{{font:500 .7rem ui-monospace,monospace;opacity:.7}}
.reveal{{opacity:0;transform:translateY(14px);transition:opacity .6s cubic-bezier(.16,1,.3,1),
  transform .6s cubic-bezier(.16,1,.3,1)}}
.reveal.in{{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){{.reveal{{opacity:1;transform:none;transition:none}}}}
</style>
</head>
<body>
  <div class="wrap">
    <div class="kicker">Noble Father Creations</div>
    <h1>The <em>Library</em></h1>
    <p class="sub">{len(books)} books. One instinct: what matters is usually the thing you can't see yet.</p>
    <div class="stats">
      <div class="stat"><b>{len(books)}</b><span>Books</span></div>
      <div class="stat"><b>{total_known_chapters}+</b><span>Chapters catalogued</span></div>
      <div class="stat"><b>Free</b><span>To read</span></div>
    </div>
    <div class="grid">
{cards}
    </div>
    <div class="kicker" style="margin-top:var(--sp-6)">Living tools</div>
    <div class="grid" style="margin-top:var(--sp-3)">
{tool_cards}
    </div>
  </div>
  <script>
    if ('IntersectionObserver' in window) {{
      var io = new IntersectionObserver(function(es){{
        es.forEach(function(e){{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
      }}, {{rootMargin:'0px 0px -8% 0px', threshold:.1}});
      document.querySelectorAll('.reveal').forEach(function(el){{ io.observe(el); }});
    }} else {{
      document.querySelectorAll('.reveal').forEach(function(el){{ el.classList.add('in'); }});
    }}
  </script>
</body>
</html>
"""
    out = ROOT / "design" / "library-index.html"
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
