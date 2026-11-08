#!/usr/bin/env python3
"""Shared pieces for making each book findable (docs/SEO-AEO-PLAN.md).

The book's own app/page stays exactly as readers know it. This module ADDS:
  * a findability <head> block on the book's index.html (title, description, canonical,
    Open Graph, Twitter card, JSON-LD Book graph) -- every injected tag carries data-seo
    so a rebuild removes and rewrites them (idempotent, no marker comments shipped);
  * one plain HTML page per chapter (<chapter>.html, served by Netlify at /<book>/<chapter>);
  * contents.html, sitemap.xml, og.png and the book's own fonts as files under /<book>/f/.

Rules carried over from the Decoder's plain pages (MEMORY 2026-10-27):
  * every link absolute (/<book>/...) -- relative paths break behind the proxy;
  * pages are x.html, never x/index.html (a trailing-slash redirect escapes the prefix);
  * no word of book text is invented: chapter text is lifted from the book's own HTML/data.
"""
import base64
import datetime as _dt
import html
import io
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[2]
DOMAIN = "https://noblefathercreations.com"
AUTHOR = "Shae Stovell"
LICENSE_URL = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
LICENSE_NAME = "CC BY-NC-ND 4.0"
LICENSE_LINE = ("&copy; 2026 Shae Stovell &middot; Free forever. Share it freely with credit, under "
                f'<a href="{LICENSE_URL}" rel="license">{LICENSE_NAME}</a> (no selling, no edited copies).')
TODAY = _dt.date.today().isoformat()

PERSON = {"@type": "Person", "@id": DOMAIN + "/#shae", "name": AUTHOR, "alternateName": "Dapper Dad", "url": DOMAIN + "/",
          "sameAs": ["https://www.tiktok.com/@noblefathercreatorsource"], "worksFor": {"@id": DOMAIN + "/#org"}}
ORG = {"@type": "Organization", "@id": DOMAIN + "/#org", "name": "Noble Father Creations", "url": DOMAIN + "/",
       "founder": {"@id": DOMAIN + "/#shae"},
       "sameAs": ["https://www.tiktok.com/@noblefathercreatorsource"]}


# ---------------------------------------------------------------- small helpers
def esc(s):
    return html.escape(s or "", quote=True)


def plain(s):
    """Visible text of an HTML fragment, whitespace collapsed."""
    t = BeautifulSoup(s or "", "html.parser").get_text(" ")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def slugify(s, maxlen=70):
    s = plain(s).lower().replace("&", " and ").replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > maxlen:
        s = s[:maxlen].rsplit("-", 1)[0]
    return s or "section"


def clip(s, n=158):
    s = plain(s)
    if len(s) <= n:
        return s
    cut = s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:—–- ")
    return cut + "…"


def first_sentences(text, n=158):
    """Description from the book's own words: whole sentences up to n chars (paragraphs only, never headings)."""
    if "<p" in (text or ""):
        text = " ".join(p.get_text(" ") for p in BeautifulSoup(text, "html.parser").find_all("p")[:6])
    t = plain(text)
    out = ""
    for sent in re.split(r"(?<=[.!?])\s+", t):
        if len(out) + len(sent) + 1 > n:
            break
        out = (out + " " + sent).strip()
    return out if len(out) >= 60 else clip(t, n)


def ld_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="surrogateescape")


def write(p, s):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8", errors="surrogateescape")


# ---------------------------------------------------------------- pieces lifted from the book
def house_parts(book_html):
    """THE HOUSE / Catalogue drawer exactly as the book carries it: (css, html, js)."""
    css = re.search(r'<style id="nf-chrome-css">.*?</style>', book_html, re.S).group(0)
    i = book_html.find('<div id="nf-chrome"')
    m = None
    for mm in re.finditer(r"<script[^>]*>.*?</script>", book_html[i:], re.S):
        if "nf-" in mm.group(0):
            m = mm
            break
    chrome = book_html[i:i + m.start()]
    js = m.group(0)
    chrome = chrome.replace(' class="nf-here"', "").replace('aria-current="page"', "")
    return css, chrome, js


def beacon(book_html):
    m = re.search(r"<script[^>]*cloudflareinsights[^>]*></script>", book_html)
    return m.group(0) if m else ""


def export_fonts(book_html, out_dir, families):
    """Write the book's own embedded faces for `families` to out_dir as woff2.
    Returns @font-face CSS pointing at /<book>/f/... (absolute)."""
    from fontTools.ttLib import TTFont
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rel = "/" + out_dir.relative_to(ROOT / "library").as_posix()
    css = []
    for block in re.findall(r"@font-face\s*\{[^}]*\}", book_html):
        fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", block).group(1).strip()
        if fam not in families or "base64," not in block:
            continue
        w = (re.search(r"font-weight:\s*([^;]+)", block) or [0, "400"])[1].strip()
        st = (re.search(r"font-style:\s*([^;]+)", block) or [0, "normal"])[1].strip()
        data = base64.b64decode(re.search(r"base64,([A-Za-z0-9+/=]+)", block).group(1))
        name = f"{slugify(fam)}-{slugify(w)}-{st}.woff2"
        f = TTFont(io.BytesIO(data))
        f.flavor = "woff2"
        buf = io.BytesIO()
        f.save(buf)
        (out_dir / name).write_bytes(buf.getvalue())
        css.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};font-display:swap;"
                   f"src:url({rel}/{name}) format('woff2')}}")
    return "\n".join(css)


# ---------------------------------------------------------------- cleaning book HTML into reading HTML
KEEP = {"h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "blockquote", "em", "strong", "b", "i", "a",
        "table", "thead", "tbody", "tr", "th", "td", "cite", "br", "hr", "dl", "dt", "dd", "figure",
        "figcaption", "sup", "sub", "small", "abbr", "q", "mark"}
DROP = {"script", "style", "svg", "img", "picture", "video", "audio", "source", "button", "input", "select",
        "textarea", "form", "iframe", "canvas", "noscript", "template", "dialog", "label", "object", "embed"}


def clean_fragment(frag, id_map=None, book_slug="", page_ids=None, drop_selectors=()):
    """Book HTML -> plain reading HTML. Keeps text and structure; removes interactive chrome.
    id_map: {element_id: page_slug} so '#x' links resolve to the right chapter page."""
    soup = BeautifulSoup(frag, "html.parser")
    for sel in drop_selectors:
        for el in soup.select(sel):
            el.decompose()
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for el in soup.find_all(list(DROP)):
        el.decompose()
    for el in soup.find_all(attrs={"aria-hidden": "true"}):
        el.decompose()
    for el in soup.find_all(True):
        if el.name not in KEEP:
            el.unwrap()
            continue
        keep = {}
        if el.get("id"):
            keep["id"] = el["id"]
        if el.name == "a" and el.get("href"):
            href = el["href"]
            if href.startswith("#"):
                target = href[1:]
                if page_ids is not None and target in page_ids:
                    keep["href"] = href
                elif id_map and target in id_map:
                    keep["href"] = f"/{book_slug}/{id_map[target]}#{target}"
                else:
                    keep["href"] = f"/{book_slug}#{target}"
            elif href.startswith(("http://", "https://", "mailto:", "tel:", "/")):
                keep["href"] = href
            else:
                el.unwrap()
                continue
        if el.name in ("td", "th") and el.get("colspan"):
            keep["colspan"] = el["colspan"]
        el.attrs = keep
    # drop empty paragraphs/list items left behind by removed widgets
    for el in soup.find_all(["p", "li", "h2", "h3", "h4", "blockquote"]):
        if not el.get_text(strip=True):
            el.decompose()
    return str(soup)


def promote(frag, rules):
    """Turn a book's styled labels into real structure before cleaning.
    rules: [(css selector, 'h2'|'h3'|'h4'|'strong'|'blockquote'|'drop')]."""
    soup = BeautifulSoup(frag, "html.parser")
    for sel, to in rules:
        for el in soup.select(sel):
            if to == "drop":
                el.decompose()
                continue
            txt = " — ".join(x for x in (s.strip() for s in el.stripped_strings) if x)
            if to == "strong":
                new = soup.new_tag("p")
                b = soup.new_tag("strong")
                b.string = el.get_text(" ", strip=True)
                new.append(b)
            elif to == "blockquote":
                new = soup.new_tag("blockquote")
                for ch in list(el.children):
                    new.append(ch.extract())
            else:
                new = soup.new_tag(to)
                new.string = title_case(re.sub(r"^[^\w“\"(]+", "", re.sub(r"\s+", " ", txt)).strip())
                if el.get("id"):
                    new["id"] = el["id"]
            el.replace_with(new)
    return str(soup)


SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}
KEEP_UPPER = {"DARVO", "FOG", "AI", "OS", "NFC", "DV", "HR", "ID", "PLUR", "RV", "DJ", "DJS", "MDMA", "LSD", "DMT", "GHB", "ER", "EMS", "GPS", "SMS", "LGBTQ", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII"}


def title_case(s):
    """'THE HARM LADDER: REPAIR, LIMIT, EXIT' -> 'The Harm Ladder: Repair, Limit, Exit' (only if the source is all caps)."""
    s = re.sub(r"\s+", " ", s).strip()
    letters = [c for c in s if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) / len(letters) < 0.8:
        # already mixed case: only lower the joining words of Title Case ("Bill Of Rights" -> "Bill of Rights")
        ws = s.split(" ")
        return " ".join(w.lower() if i and w in ("And", "Of", "The", "In", "On", "To", "For", "A", "An", "Or", "With", "At", "By")
                        and not ws[i - 1].endswith((":", "—")) else w for i, w in enumerate(ws))
    out = []
    for i, w in enumerate(s.split(" ")):
        core = re.sub(r"[^A-Za-z]", "", w)
        if core in KEEP_UPPER:
            out.append(w)
        elif i and core.lower() in SMALL and not out[-1].endswith((":", "—", "→")):
            out.append(w.lower())
        else:
            out.append(re.sub(r"[A-Za-z][A-Za-z’'*]*", lambda m: m.group(0) if m.group(0) in KEEP_UPPER
                              else m.group(0)[0].upper() + m.group(0)[1:].lower(), w))
    res = " ".join(out).replace("- ", "-") if "SELF- " in s else " ".join(out)
    return re.sub(r"-(And|Or|Of|The|In|To|A|An)-", lambda m: "-" + m.group(1).lower() + "-", res)


def collect_until(start, is_stop):
    """start element + following siblings until one satisfies is_stop (exclusive)."""
    parts, n = [], start.next_sibling
    while n is not None:
        if getattr(n, "name", None) and is_stop(n):
            break
        parts.append(str(n))
        n = n.next_sibling
    return "".join(parts)


def give_heading_ids(frag, prefix=""):
    """Every h2-h4 gets a stable, unique, readable id (AI citations can point at the exact block)."""
    soup = BeautifulSoup(frag, "html.parser")
    seen = set(e["id"] for e in soup.find_all(id=True))
    out = []
    for h in soup.find_all(["h2", "h3", "h4"]):
        first = next(iter(h.strings), None)
        if first is not None and re.match(r"^[^\w“\"(]+", first):
            first.replace_with(re.sub(r"^[^\w“\"(]+", "", first))
        if not h.get("id"):
            base = (prefix + "-" if prefix else "") + slugify(h.get_text(), 50)
            i, cand = 2, base
            while cand in seen:
                cand = f"{base}-{i}"
                i += 1
            h["id"] = cand
            seen.add(cand)
        out.append((h.name, h["id"], h.get_text(" ", strip=True)))
    return str(soup), out


def link_terms(frag, terms, limit=6):
    """Link the first plain-text mention of known Decoder tactic names (internal linking).
    terms: list of (name, url), longest first. Never inside existing links or headings."""
    soup = BeautifulSoup(frag, "html.parser")
    done = 0
    used = set()
    for name, url in terms:
        if done >= limit:
            break
        pat = re.compile(r"\b(" + re.escape(name) + r")\b", re.I)
        for node in soup.find_all(string=pat):
            if node.find_parent(["a", "h1", "h2", "h3", "h4", "cite", "blockquote"]):
                continue
            if url in used:
                break
            m = pat.search(node)
            before, word, after = node[:m.start()], m.group(1), node[m.end():]
            a = soup.new_tag("a", href=url)
            a.string = word
            node.replace_with(before, a, after)
            used.add(url)
            done += 1
            break
    return str(soup)


def decoder_terms():
    """(name, url) for each Decoder tactic page, from its own sitemap + page titles."""
    site = ROOT / "instruments/playbook/site"
    out = []
    for f in sorted(site.glob("*.html")):
        if f.name in ("index.html", "tactics.html") or f.name.startswith("line-"):
            continue
        t = re.search(r"<title>(.*?):", read(f))
        if t:
            name = html.unescape(t.group(1)).strip()
            if len(name) >= 6 and " " in name or len(name) >= 10:
                out.append((name, f"/playbook/{f.stem}"))
    out.sort(key=lambda x: -len(x[0]))
    return out


def fit_title(t, book_title, n=65):
    """'<chapter> · <book>' when it fits; else the chapter name alone; else clipped."""
    t = plain(t)
    if t.endswith(" · " + book_title):
        t = t[: -len(" · " + book_title)]
    full = f"{t} · {book_title}"
    if len(full) <= n:
        return full
    return t if len(t) <= n else clip(t, n)


OG_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>%(fonts)s
html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:%(bg)s;color:%(fg)s}
.c{box-sizing:border-box;width:1200px;height:630px;padding:72px 80px;display:flex;flex-direction:column;justify-content:space-between;
background:radial-gradient(120%% 90%% at 85%% 0%%,%(glow)s 0%%,transparent 60%%),%(bg)s;border-bottom:12px solid %(acc)s}
.k{font:600 24px/1.2 %(disp)s;letter-spacing:.14em;text-transform:uppercase;color:%(acc)s}
h1{font:600 %(size)spx/1.02 %(disp)s;margin:0;letter-spacing:-.01em;max-width:1000px}
p{font:400 34px/1.3 %(body)s;margin:20px 0 0;color:%(fg2)s;max-width:960px}
.f{display:flex;justify-content:space-between;font:600 24px/1.2 %(disp)s;color:%(fg2)s}.f b{color:%(acc)s;font-weight:600}
</style></head><body><div class="c"><div class="k">%(kicker)s</div><div><h1>%(title)s</h1><p>%(sub)s</p></div>
<div class="f"><span>by Shae Stovell &middot; Noble Father Creations</span><b>noblefathercreations.com/%(slug)s</b></div></div></body></html>"""


def make_og(book, out_dir, kicker, sub):
    """1200x630 share card in the book's own colours and display face (rendered by Playwright)."""
    import subprocess, tempfile
    out_dir = Path(out_dir)
    fonts = []
    for f in sorted((out_dir / "f").glob("*.woff2")):
        fam = book["fonts"][0] if f.name.startswith(slugify(book["fonts"][0])) else (book["fonts"][1] if len(book["fonts"]) > 1 and f.name.startswith(slugify(book["fonts"][1])) else None)
        if fam:
            w = "1 999" if "1-999" in f.name else re.search(r"-(\d+)-", f.name).group(1) if re.search(r"-(\d+)-", f.name) else "400"
            st = "italic" if f.name.endswith("italic.woff2") else "normal"
            fonts.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url('{f.as_uri()}')}}")
    th = book["theme"]
    title = book["title"]
    size = 132 if len(title) <= 14 else 108 if len(title) <= 22 else 88
    page = OG_HTML % dict(fonts="\n".join(fonts), bg=th["bg"], fg=th["fg"], fg2=th["fg2"], acc=th["acc"],
                          glow=th.get("glow", th["panel"]), disp=th["disp"], body=th["body"], size=size,
                          kicker=esc(kicker), title=esc(title), sub=esc(sub), slug=book["slug"])
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(page)
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});"
          f"await p.goto('file://{t.name}');await p.waitForTimeout(400);await p.screenshot({{path:'{out_dir / 'og.png'}'}});await b.close();}})();")
    subprocess.run(["node", "-e", js], check=True, cwd=str(ROOT))
    return out_dir / "og.png"


# ---------------------------------------------------------------- page frame
PAGE_CSS = """
:root{color-scheme:%(scheme)s;--bg:%(bg)s;--fg:%(fg)s;--fg2:%(fg2)s;--panel:%(panel)s;--line:%(line)s;--acc:%(acc)s;--acc-ink:%(accink)s;
--disp:%(disp)s;--body:%(body)s}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;text-size-adjust:100%%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1.125rem/1.7 var(--body);overflow-x:hidden}
a{color:var(--acc);text-underline-offset:.18em;text-decoration-thickness:1px;transition:color .2s ease}
a:hover{color:var(--fg)}
a:focus-visible,button:focus-visible{outline:2px solid var(--acc);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:9;background:var(--panel);padding:8px 16px}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;max-width:42rem;margin:0 auto;padding:16px 16px 0}
.bar .bk{font:600 1rem/1.3 var(--disp);color:var(--fg);text-decoration:none;min-height:44px;display:inline-flex;align-items:center;min-width:0}
.bar .open{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border-radius:999px;background:var(--acc);color:var(--acc-ink);
text-decoration:none;font:600 .9375rem/1 var(--disp);transition:opacity .2s ease;white-space:nowrap;flex:none}.bar .open:hover{opacity:.88}
main{max-width:42rem;margin:0 auto;padding:24px 16px 48px}
.crumbs{font-size:.9375rem;color:var(--fg2);margin:0 0 32px}.crumbs ol{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0 8px}
.crumbs li+li::before{content:"›";margin-right:8px;color:var(--fg2)}.crumbs a{color:var(--fg2)}
.eyebrow{font:600 .875rem/1.4 var(--disp);letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:0 0 8px}
h1{font:600 clamp(2.25rem,1.4rem + 3.6vw,3.5rem)/1.08 var(--disp);letter-spacing:-.01em;margin:0 0 16px;text-wrap:balance}
.lede{font-size:1.25rem;line-height:1.55;color:var(--fg2);margin:0 0 24px}
.notice{font-size:.9375rem;line-height:1.5;color:var(--fg2);border-left:2px solid var(--acc);padding:4px 0 4px 16px;margin:0 0 40px}
article h2{font:600 1.75rem/1.2 var(--disp);margin:56px 0 16px;scroll-margin-top:24px;text-wrap:balance}
article h3{font:600 1.3125rem/1.3 var(--disp);margin:40px 0 8px;scroll-margin-top:24px}
article h4{font:600 1.125rem/1.35 var(--disp);margin:32px 0 8px}
article p{margin:0 0 20px}article ul,article ol{margin:0 0 20px;padding-left:1.4em}article li{margin:0 0 8px}
article blockquote{margin:24px 0;padding:16px 24px;background:var(--panel);border-radius:8px;font-style:italic}
article table{border-collapse:collapse;width:100%%;margin:0 0 24px;font-size:1rem;display:block;overflow-x:auto}
article th,article td{text-align:left;padding:8px;border-bottom:1px solid var(--line);vertical-align:top}
article hr{border:0;border-top:1px solid var(--line);margin:40px 0}
.srcs{margin:56px 0 0;padding:32px 0 0;border-top:1px solid var(--line)}.srcs h2{margin-top:0}
.srcs ol{font-size:1rem;line-height:1.55;padding-left:1.6em}.srcs li{margin:0 0 12px}.srcs cite{font-style:normal}
.toc{margin:0 0 40px;padding:16px 24px;background:var(--panel);border-radius:8px;font-size:1rem}
.toc h2{font:600 .875rem/1.4 var(--disp);letter-spacing:.08em;text-transform:uppercase;margin:0 0 8px;color:var(--fg2)}
.toc ol{margin:0;padding-left:1.2em}.toc li{margin:4px 0}
.pn{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:64px 0 0}
.pn a{display:block;padding:16px;background:var(--panel);border-radius:8px;text-decoration:none;color:var(--fg);min-height:44px;transition:background-color .2s ease}
.pn a:hover{background:var(--line)}.pn small{display:block;color:var(--fg2);font-size:.875rem}.pn b{font:600 1.0625rem/1.3 var(--disp)}.pn .nx{text-align:right;grid-column:2}
.list{list-style:none;margin:0;padding:0}.list li{border-bottom:1px solid var(--line)}
.list a{display:block;padding:16px 0;text-decoration:none;color:var(--fg);min-height:44px}
.list b{display:block;font:600 1.125rem/1.3 var(--disp)}.list small{display:block;color:var(--fg2);font-size:1rem;line-height:1.5;margin-top:4px}
.mv{font:600 .875rem/1.4 var(--disp);letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:48px 0 8px}
.rel{margin:64px 0 0;padding:32px 0 0;border-top:1px solid var(--line)}.rel h2{font:600 1.25rem/1.3 var(--disp);margin:0 0 8px}
.foot{max-width:42rem;margin:0 auto;padding:32px 16px 112px;color:var(--fg2);font-size:.9375rem;line-height:1.6;border-top:1px solid var(--line)}
.foot p{margin:0 0 12px}.foot nav{display:flex;flex-wrap:wrap;gap:0 24px}.foot nav a{min-height:44px;display:inline-flex;align-items:center}
@media (max-width:480px){.pn{grid-template-columns:1fr}.pn .nx{grid-column:1}.bar .bk{font-size:.9375rem}.bar .open{padding:0 14px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
@media print{.bar,.pn,.foot nav,#nf-chrome{display:none}}
"""


def head_tags(book, title, desc, url, image, image_alt, og_type="article"):
    return (f'<title>{esc(title)}</title>\n'
            f'<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<meta name="author" content="{AUTHOR}">\n'
            f'<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">\n'
            f'<meta property="og:type" content="{og_type}">\n'
            f'<meta property="og:site_name" content="Noble Father Creations">\n'
            f'<meta property="og:locale" content="en_US">\n'
            f'<meta property="og:title" content="{esc(title)}">\n'
            f'<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{image}">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{esc(image_alt)}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{esc(title)}">\n'
            f'<meta name="twitter:description" content="{esc(desc)}">\n'
            f'<meta name="twitter:image" content="{image}">\n'
            f'<meta name="twitter:image:alt" content="{esc(image_alt)}">\n'
            f'<link rel="license" href="{LICENSE_URL}">\n'
            f'<link rel="sitemap" type="application/xml" href="/{book["slug"]}/sitemap.xml">\n')


def book_node(book, chapters=None):
    url = f"{DOMAIN}/{book['slug']}"
    node = {"@type": "Book", "@id": url + "#book", "name": book["title"], "url": url,
            "author": {"@id": PERSON["@id"]}, "publisher": {"@id": ORG["@id"]},
            "copyrightHolder": {"@id": PERSON["@id"]}, "copyrightYear": 2026,
            "inLanguage": "en", "bookFormat": "https://schema.org/EBook", "isAccessibleForFree": True,
            "license": LICENSE_URL, "image": f"{url}/og.png", "description": book["description"],
            "version": book.get("version", ""), "dateModified": TODAY,
            "genre": book.get("genre", []), "keywords": ", ".join(book.get("keywords", [])),
            "about": [{"@type": "Thing", "name": a} for a in book.get("about", [])],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": url}}
    if book.get("alternateName"):
        node["alternateName"] = book["alternateName"]
    if book.get("audience"):
        node["audience"] = book["audience"]
    if book.get("typicalAgeRange"):
        node["typicalAgeRange"] = book["typicalAgeRange"]
    if chapters:
        node["hasPart"] = [{"@type": "Chapter", "@id": f"{url}/{c['slug']}#chapter", "name": c["title"],
                            "position": i + 1, "url": f"{url}/{c['slug']}"} for i, c in enumerate(chapters)]
    return {k: v for k, v in node.items() if v not in ("", [], None)}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def frame(book, parts, *, title, desc, url, ld, body, image_alt):
    css_vars = dict(book["theme"])
    css = PAGE_CSS % css_vars
    house_css, house_html, house_js = parts["house"]
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            + head_tags(book, title, desc, url, f"{DOMAIN}/{book['slug']}/og.png", image_alt)
            + f'<meta name="theme-color" content="{book["theme"]["bg"]}">\n'
            + f"<style>{parts['fonts']}\n{css}</style>\n{house_css}\n"
            + f'<script type="application/ld+json">{ld_json(ld)}</script>\n</head>\n<body>\n'
            + '<a class="skip" href="#text">Skip to the text</a>\n'
            + f'<header class="bar"><a class="bk" href="/{book["slug"]}/contents">{esc(book["title"])}</a>'
            + f'<a class="open" href="/{book["slug"]}">Open the full book</a></header>\n'
            + body
            + f'\n<footer class="foot"><p>{LICENSE_LINE}</p>'
            + f'<p>{book["notice_short"]} <a href="{book["notice_href"]}">Read the full notice</a>.</p>'
            + f'<nav aria-label="More"><a href="/{book["slug"]}/contents">Every chapter</a>'
            + f'<a href="/{book["slug"]}">The full book</a><a href="/">Noble Father Creations</a></nav></footer>\n'
            + house_html + "\n" + house_js + "\n" + parts["beacon"] + "\n</body>\n</html>\n")


# ---------------------------------------------------------------- chapter + contents pages
def chapter_page(book, parts, chs, i, related):
    c = chs[i]
    url = f"{DOMAIN}/{book['slug']}/{c['slug']}"
    burl = f"{DOMAIN}/{book['slug']}"
    title = fit_title(c.get("seo_title") or plain(c["title"]), book["title"])
    desc = c.get("desc") or first_sentences(c.get("lede") or c["html"])
    crumbs = [("Noble Father Creations", DOMAIN + "/"), (book["title"], burl), (plain(c["title"]), url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": burl + "#book"}, "breadcrumb": {"@id": url + "#crumbs"},
         "primaryImageOfPage": f"{burl}/og.png", "dateModified": TODAY, "author": {"@id": PERSON["@id"]},
         "isAccessibleForFree": True, "license": LICENSE_URL, "mainEntity": {"@id": url + "#chapter"}},
        {"@type": "Chapter", "@id": url + "#chapter", "name": plain(c["title"]), "position": i + 1, "url": url,
         "isPartOf": {"@id": burl + "#book"}, "author": {"@id": PERSON["@id"]}, "license": LICENSE_URL,
         "isAccessibleForFree": True, "inLanguage": "en", "description": desc,
         **({"citation": c["citations"]} if c.get("citations") else {})},
        dict(crumbs_ld(crumbs), **{"@id": url + "#crumbs"}),
        book_node(book), PERSON, ORG]}
    toc = ""
    if len(c.get("heads", [])) >= 4:
        toc = ('<nav class="toc" aria-labelledby="toc-h"><h2 id="toc-h">On this page</h2><ol>'
               + "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for lvl, hid, t in c["heads"] if lvl == "h2" or len([x for x in c["heads"] if x[0] == "h2"]) < 3 and lvl == "h3")
               + "</ol></nav>")
    pn = '<nav class="pn" aria-label="Chapters">'
    if i > 0:
        p = chs[i - 1]
        pn += f'<a href="/{book["slug"]}/{p["slug"]}" rel="prev"><small>Previous</small><b>{esc(plain(p["title"]))}</b></a>'
    if i < len(chs) - 1:
        n = chs[i + 1]
        pn += f'<a class="nx" href="/{book["slug"]}/{n["slug"]}" rel="next"><small>Next</small><b>{esc(plain(n["title"]))}</b></a>'
    pn += "</nav>"
    rel = ""
    if related:
        rel = ('<aside class="rel" aria-labelledby="rel-h"><h2 id="rel-h">Keep reading in the library</h2><ul class="list">'
               + "".join(f'<li><a href="/{s}"><b>{esc(t)}</b><small>{esc(d)}</small></a></li>' for s, t, d in related)
               + "</ul></aside>")
    body = (f'<main id="text"><nav class="crumbs" aria-label="Breadcrumb"><ol>'
            + "".join(f'<li><a href="{u.replace(DOMAIN, "") or "/"}">{esc(n)}</a></li>' for n, u in crumbs[:-1])
            + f'<li aria-current="page">{esc(plain(c["title"]))}</li></ol></nav>\n'
            + (f'<p class="eyebrow">{esc(c["eyebrow"])}</p>' if c.get("eyebrow") else "")
            + f'<h1 id="top">{esc(plain(c["title"]))}</h1>\n'
            + (f'<p class="lede">{esc(plain(c["lede"]))}</p>' if c.get("lede") else "")
            + f'<p class="notice">{book["notice_short"]} <a href="{book["notice_href"]}">Full notice</a>.</p>\n'
            + toc + f'<article>\n{c["html"]}\n</article>\n'
            + (f'<section class="srcs" aria-labelledby="src-h"><h2 id="src-h">Sources for this chapter</h2>{c["sources_html"]}</section>' if c.get("sources_html") else "")
            + pn + rel + "</main>")
    return frame(book, parts, title=title, desc=desc, url=url, ld=ld, body=body,
                 image_alt=f"{book['title']} by {AUTHOR}, free to read")


def contents_page(book, parts, chs):
    url = f"{DOMAIN}/{book['slug']}/contents"
    burl = f"{DOMAIN}/{book['slug']}"
    title = book.get("contents_title") or f"{book['title']}: Every Chapter, Free to Read"
    desc = clip(f"All {len(chs)} {book.get('unit', 'chapters')} of {book['title']} by {AUTHOR}, free to read online. {book['description']}")
    crumbs = [("Noble Father Creations", DOMAIN + "/"), (book["title"], burl), ("Contents", url)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": burl + "#book"}, "dateModified": TODAY, "breadcrumb": {"@id": url + "#crumbs"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(chs), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{burl}/{c['slug']}", "name": plain(c["title"])} for i, c in enumerate(chs)]}},
        dict(crumbs_ld(crumbs), **{"@id": url + "#crumbs"}), book_node(book, chs), PERSON, ORG]}
    rows, last_mv = "", None
    for c in chs:
        if c.get("movement") and c["movement"] != last_mv:
            if rows:
                rows += "</ul>"
            rows += f'<h2 class="mv" id="{slugify(c["movement"], 60)}">{esc(c["movement"])}</h2><ul class="list">'
            last_mv = c["movement"]
        elif not rows:
            rows = '<ul class="list">'
        rows += (f'<li><a href="/{book["slug"]}/{c["slug"]}"><b>{esc((c.get("eyebrow") + " · ") if c.get("eyebrow") and not c.get("movement") else "")}{esc(plain(c["title"]))}</b>'
                 f'<small>{esc(clip(c.get("lede") or c.get("desc") or c["html"], 170))}</small></a></li>')
    rows += "</ul>"
    body = (f'<main id="text"><nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Noble Father Creations</a></li>'
            f'<li><a href="/{book["slug"]}">{esc(book["title"])}</a></li><li aria-current="page">Contents</li></ol></nav>'
            f'<p class="eyebrow">Free to read · {len(chs)} {book.get("unit", "chapters")}</p><h1 id="top">{esc(book["title"])}</h1>'
            f'<p class="lede">{esc(book["description"])}</p>'
            f'<p class="notice">{book["notice_short"]} <a href="{book["notice_href"]}">Full notice</a>.</p>{rows}</main>')
    return frame(book, parts, title=title, desc=desc, url=url, ld=ld, body=body,
                 image_alt=f"{book['title']} by {AUTHOR}, free to read")


def sitemap(book, chs, extra=()):
    base = f"{DOMAIN}/{book['slug']}"
    urls = [base, base + "/contents"] + [f"{base}/{c['slug']}" for c in chs] + [f"{base}/{e}" for e in extra]
    body = "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


# ---------------------------------------------------------------- the book's own index.html
SEO_TAG = re.compile(r'[ \t]*<(?:meta|link)\b[^>]*\bdata-seo\b[^>]*>\n?|[ \t]*<script type="application/ld\+json" data-seo>.*?</script>\n?', re.S)


def inject_index(book, index_html, chs):
    """Add the findability head block to the book's own page. Idempotent."""
    h = SEO_TAG.sub("", index_html)
    url = f"{DOMAIN}/{book['slug']}"
    title, desc = book["index_title"], book["index_desc"]
    # replace the page's existing <title> and description (exactly one each)
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", h, count=1, flags=re.S)
    if re.search(r'<meta\s+name="description"[^>]*>', h):
        h = re.sub(r'<meta\s+name="description"[^>]*>', f'<meta name="description" content="{esc(desc)}">', h, count=1)
    else:
        h = h.replace("</title>", f'</title>\n<meta name="description" content="{esc(desc)}">', 1)
    # strip any older og/twitter/canonical tags so there is exactly one of each
    h = re.sub(r'[ \t]*<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>\n?', "", h)
    h = re.sub(r'[ \t]*<link\s+rel="canonical"[^>]*>\n?', "", h)
    tags = head_tags(book, title, desc, url, url + "/og.png", f"{book['title']} by {AUTHOR}, free to read", "book")
    tags = "\n".join(t for t in tags.split("\n") if t and not t.startswith(("<title>", '<meta name="description"')))
    tags = re.sub(r"<(meta|link)\b", r"<\1 data-seo", tags)
    ld = {"@context": "https://schema.org", "@graph": [
        dict(book_node(book, chs), **{"mainEntityOfPage": url}),
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
         "about": {"@id": url + "#book"}, "dateModified": TODAY, "isAccessibleForFree": True, "license": LICENSE_URL},
        PERSON, ORG]}
    block = tags + f'\n<script type="application/ld+json" data-seo>{ld_json(ld)}</script>\n'
    h = re.sub(r"(</title>\n<meta name=\"description\"[^>]*>\n?)", lambda m: m.group(1).rstrip("\n") + "\n" + block, h, count=1)
    if block not in h:
        h = h.replace("</head>", block + "</head>", 1)
    return h


def write_book(book, index_html, chs, out_dir, related=None, extra_pages=()):
    """Write chapter pages, contents, sitemap; returns list of written page names."""
    out_dir = Path(out_dir)
    parts = {"house": house_parts(index_html), "beacon": beacon(index_html),
             "fonts": export_fonts(index_html, out_dir / "f", book["fonts"])}
    names = []
    for i, c in enumerate(chs):
        write(out_dir / f"{c['slug']}.html", chapter_page(book, parts, chs, i, related or []))
        names.append(c["slug"])
    write(out_dir / "contents.html", contents_page(book, parts, chs))
    write(out_dir / "sitemap.xml", sitemap(book, chs, extra_pages))
    return names
