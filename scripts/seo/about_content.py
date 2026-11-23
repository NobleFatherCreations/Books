#!/usr/bin/env python3
"""The owner's bio ("Who made this") from content/about.md, as HTML, for the homepage section and /about.

Edit content/about.md, never the output. Only the part after "## Full page" is published.
Placeholders in the Markdown:
  [tell me how it helped you]           -> a link to CONTACT (Instagram direct message)
  [the Noble Father Creations wordmark] -> the wordmark image
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "content/about.md"
INSTAGRAM = "https://www.instagram.com/dapperdad_nfc/"
THREADS = "https://www.threads.net/@dapperdad_nfc"
TIKTOK = "https://www.tiktok.com/@noblefathercreatorsource"
CONTACT = "https://ig.me/m/dapperdad_nfc"          # opens an Instagram direct message to the owner
SOCIAL = [("Instagram", INSTAGRAM, "@dapperdad_nfc"), ("Threads", THREADS, "@dapperdad_nfc"), ("TikTok", TIKTOK, "@noblefathercreatorsource")]
WORDMARK = '<img class="ab-wordmark" src="/media/v18/wordmark.webp" width="{w}" height="{h}" alt="Noble Father Creations" loading="lazy" decoding="async">'


def _inline(s):
    s = html.escape(s, quote=False)
    s = s.replace("[tell me how it helped you]", f'<a href="{CONTACT}" rel="noopener" target="_blank">tell me how it helped you</a>')
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def blocks():
    """(title, html_body) of the full page. title is the page's '# ' heading (plain text)."""
    md = SRC.read_text()
    md = md.split("## Full page", 1)[1]
    title, out, para, lst = None, [], [], []

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + "<br>".join(_inline(x) for x in para) + "</p>")
        if lst:
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in lst) + "</ul>")
        para, lst = [], []

    for line in md.splitlines():
        t = line.strip()
        if not t:
            flush(); continue
        if t.startswith("# "):
            flush(); title = t[2:].strip(); continue
        if t.startswith("## "):
            flush(); out.append(f"<h3>{_inline(t[3:])}</h3>"); continue
        if t == "---":
            flush(); out.append('<hr class="ab-rule">'); continue
        if t.startswith("- "):
            if para: flush()
            lst.append(t[2:]); continue
        if t == "[the Noble Father Creations wordmark]":
            flush(); out.append("{WORDMARK}"); continue
        para.append(t)
    flush()
    return title, "\n".join(out)


def plain_summary():
    """One plain paragraph about the author, for schema descriptions and llms.txt."""
    return ("Shae Stovell is a father of four and the founder of Noble Father Creations. After someone used his trust and "
            "loyalty against him, he wrote his way through it, and the writing became fourteen free books and the Pattern "
            "Decoder (335 manipulation and control tactics in plain words), built every day for almost two years. "
            "He is not a therapist or lawyer; where research exists he names it, and where he speaks from his own life or "
            "faith he says so. Everything is free: no sign-up, no ads, no tracking.")


if __name__ == "__main__":
    t, b = blocks()
    print(t); print(len(b), "chars")
