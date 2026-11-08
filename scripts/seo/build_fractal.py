#!/usr/bin/env python3
"""The Fractal: one plain page per chapter, rendered from the book's own DATA object exactly the way
the book's own renderer lays it out (essays: h/stage/tech/table/p blocks; sectors: narrative, then the
thirty techniques grouped by stage, each at individual / institutional / civilizational scale).

Sectors the book itself marks "in production" (no techniques yet) get no page.
Also adds the book's first Editorial & Legal Notice (it had none; see docs/LEGAL-AUDIT-2026-11-08.md).

Run: python3 scripts/seo/build_fractal.py   (reads/writes library/fractal/)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S

OUT = S.ROOT / "library/fractal"
CONTACT = "dapperdadnfc@gmail.com"
BOOK = {
    "slug": "fractal", "title": "The Fractal", "version": "v4",
    "fonts": ["Fraunces", "Spectral"],
    "theme": {"scheme": "dark", "bg": "#0A0B11", "fg": "#E7E5EE", "fg2": "#A9AAC0", "panel": "#141625",
              "line": "#1F2236", "glow": "#2a1d3d", "acc": "#E5A93C", "accink": "#0A0B11",
              "disp": "'Fraunces',Georgia,serif", "body": "'Spectral',Georgia,serif"},
    "description": ("A free book on one manipulation cycle that runs at every scale: thirty techniques, from love "
                    "bombing to learned helplessness, traced through religion, politics, healthcare, housing and 22 more "
                    "parts of life, in a person, an institution and a civilization."),
    "index_title": "The Fractal: How One Manipulation Pattern Runs the World (Free)",
    "index_desc": ("A free book tracing one manipulation cycle and its thirty techniques through religion, politics, "
                   "healthcare, housing and more, at every scale."),
    "genre": ["Psychology", "Sociology", "Social criticism"],
    "about": ["Psychological manipulation", "Coercive control", "Institutional abuse", "Love bombing",
              "Trauma bonding", "Learned helplessness", "Propaganda", "Systems thinking"],
    "keywords": ["manipulation tactics in institutions", "love bombing in religion", "narcissistic abuse cycle society",
                 "institutional gaslighting", "learned helplessness", "free book"],
    "notice_short": ("Educational commentary on patterns, not accusations against any person or organization; the "
                     "author's interpretation, not legal, medical, psychological or financial advice."),
    "notice_href": "/fractal#notice",
    "unit": "chapters",
}
RELATED = [("fracture", "The Fracture", "The who: where roughly $50 trillion went, with 195 public-record sources"),
           ("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("feminine", "The Sovereign Divine Feminine", "A field guide to manipulation tactics and counter-moves")]

NOTICE_HTML = f"""<section class="fx-notice" id="notice" style="max-width:40rem;margin:64px auto;padding:24px;border:1px solid rgba(150,160,200,.16);border-radius:12px;font-size:.9375rem;line-height:1.6;color:#A9AAC0">
<h2 style="font:600 1.25rem/1.3 'Fraunces',Georgia,serif;color:#E7E5EE;margin:0 0 12px">Editorial &amp; Legal Notice</h2>
<p style="margin:0 0 12px"><b>What this is.</b> The Fractal is educational commentary and analysis. It describes how one pattern of manipulation can show up in a person, an institution and a society. Its examples illustrate patterns; they are not accusations that any particular person, organization or institution has done any particular thing.</p>
<p style="margin:0 0 12px"><b>Opinion and interpretation.</b> The framings, comparisons and conclusions are the author&rsquo;s perspective. Where the book refers to real events, it draws on what has been publicly reported.</p>
<p style="margin:0 0 12px"><b>Not advice.</b> Nothing here is legal, medical, psychological, financial or religious advice, or a diagnosis of anyone. If you are in danger, contact emergency services.</p>
<p style="margin:0 0 12px"><b>Corrections.</b> If you find a factual error, write to <a href="mailto:{CONTACT}" style="color:#E5A93C">{CONTACT}</a> and it will be reviewed and corrected.</p>
<p style="margin:0">{S.LICENSE_LINE} <a href="/fractal/contents" style="color:#E5A93C">Read it chapter by chapter</a>.</p>
{{CHAPTER_LINKS}}
</section>"""


def load_data(h):
    m = re.search(r"const DATA\s*=\s*", h)
    data, _ = json.JSONDecoder().raw_decode(h, m.end())
    return data


def render_closing(ch, stages, terms):
    out = []
    for b in ch["blocks"]:
        t = b["t"]
        if t == "h":
            out.append(f"<h2>{S.esc(b['x'])}</h2>")
        elif t == "stage":
            gl = f" — {S.esc(b['gloss'])}" if b.get("gloss") else ""
            out.append(f"<h2>Stage: {S.esc(b['name'])}{gl}</h2>")
        elif t == "tech":
            out.append(f"<h3>{int(b['n']):02d} · {S.esc(b['name'])}</h3>")
        elif t == "table":
            th = "".join(f"<th>{S.esc(x)}</th>" for x in b["head"])
            rows = "".join("<tr>" + "".join(f"<td>{S.esc(c)}</td>" for c in r) + "</tr>" for r in b["rows"])
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>")
        else:
            out.append(f"<p>{b['x']}</p>")       # the book renders paragraph blocks as HTML; same here
    return "\n".join(out)


def render_sector(sec, data):
    stages = {s["key"]: s for s in data["stages"]}
    out = [f"<p><strong>Controls</strong> {S.esc(sec['controls'])}</p>",
           f"<p><strong>Captured</strong> <em>{S.esc(sec['impulse'])}</em></p>",
           "<h2>The Narrative — from the inside</h2>"]
    out += [f"<p>{S.esc(p.strip())}</p>" for p in re.split(r"\n\s*\n", sec["narrative"]) if p.strip()]
    by_stage = {}
    for t in sec["techs"]:
        by_stage.setdefault(data["techStage"][str(t["num"])], []).append(t)
    seen = set()
    for s in data["stages"]:
        sk = s["key"]
        if sk in seen or sk not in by_stage:
            continue
        seen.add(sk)
        out.append(f"<h2>Stage {s['n']}: {S.esc(s['name'])}</h2><p><em>{S.esc(s['fn'])}</em></p>")
        for t in by_stage[sk]:
            ess = data["essence"].get(str(t["num"]), "")
            out.append(f"<h3>{int(t['num']):02d} · {S.esc(t['name'])}</h3>")
            if ess:
                out.append(f"<p><em>{S.esc(ess)}</em></p>")
            out.append(f"<p><strong>Individual.</strong> {S.esc(t['ind'])}</p>"
                       f"<p><strong>Institutional.</strong> {S.esc(t['inst'])}</p>"
                       f"<p><strong>Civilizational.</strong> {S.esc(t['civ'])}</p>")
    return "\n".join(out)


def build(h):
    data = load_data(h)
    closings = {c["slug"]: c for c in data["closings"]}
    terms = S.decoder_terms()
    order = []
    for slug in ("intro", "origin", "spiritual"):
        c = closings[slug]
        order.append(dict(kind="closing", src=c, title=c["title"], eyebrow=c.get("kicker", ""), lede=c.get("sub"),
                          movement="Before the thirty", slug=S.slugify(c["title"], 48)))
    n = 0
    for sec in data["sectors"]:
        if sec["slug"] == "surveillance":
            continue          # the book exchanges this one out
        n += 1
        if not sec.get("techs"):
            continue          # the book marks it "in production"
        name = S.title_case(sec["full"])
        order.append(dict(kind="sector", src=sec, title=name, eyebrow=f"Sector {n} of 30",
                          lede=f"How the pattern captures {sec['impulse'][0].lower() + sec['impulse'][1:]}.",
                          movement="The thirty sectors", slug=S.slugify(sec["short"], 48)))
    m = closings["mirror"]
    order.append(dict(kind="closing", src=m, title=m["title"], eyebrow=m.get("kicker", ""), lede=m.get("sub"),
                      movement="The thirty sectors", slug="the-mirror"))
    for slug in ("body", "chain", "frequency", "epilogue"):
        c = closings[slug]
        order.append(dict(kind="closing", src=c, title=c["title"], eyebrow=c.get("kicker", ""), lede=c.get("sub"),
                          movement="After the thirty", slug=S.slugify(c["title"], 48)))
    for c in order:
        body = render_closing(c["src"], data["stages"], terms) if c["kind"] == "closing" else render_sector(c["src"], data)
        body, heads = S.give_heading_ids(body)
        body = S.link_terms(body, terms, limit=6)
        c["html"], c["heads"] = body, heads
        if c["kind"] == "sector":
            cand = f"Manipulation in {c['src']['short']}: 30 Techniques"
            c["seo_title"] = S.fit_title(cand if len(cand) <= 65 else f"Manipulation in {c['src']['short']}", "The Fractal")
            c["desc"] = S.clip(f"How love bombing, gaslighting and 28 more manipulation techniques run through "
                               f"{c['src']['short'].lower()}, in a person, an institution and a society. Free, from The Fractal.", 158)
        else:
            c["seo_title"] = c["title"]
            c["desc"] = S.clip(f"{c['title']}, from The Fractal (free): {c['lede'] or S.first_sentences(body, 120)}", 158)
        del c["src"]
    return order


def patch_index(h, chs):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace("no cookies, no personal data, nothing that leaves this domain",
                  "anonymous visit counts through Cloudflare: no cookies, no personal data")
    h = re.sub(r'\n?<section class="fx-notice" id="notice".*?</section>', "", h, flags=re.S)
    entry = ('<p class="ch-p"><b>v4 &middot; November 8, 2026.</b> Every essay and every finished sector now also has its own '
             'page, so a search or an AI assistant can send someone straight to it (<a href="/fractal/contents">see them all</a>). '
             'Added an editorial and legal notice with a corrections address, and the free licence (credit required, no selling).</p>')
    anchor = '<h3 class="ch-h">Updates</h3>\n'
    assert anchor in h, "fractal: updates heading not found"
    if "v4 &middot; November 8, 2026" not in h:
        h = h.replace(anchor, anchor + "          " + entry + "\n", 1)
    i = h.find('<div id="nf-chrome"')
    links = "".join(f'<li><a href="/{BOOK["slug"]}/{c["slug"]}" style="color:inherit">{S.esc(c["title"])}</a></li>'
                    for c in chs if (BOOK["slug"] != "festival" or c["eyebrow"].startswith("Guide for")))
    block = (f'<h3 style="font-size:1rem;margin:16px 0 8px;color:inherit">Every {"guide" if BOOK["slug"] == "festival" else "chapter"}</h3>'
             f'<ul style="margin:0;padding-left:1.2em;columns:16rem;column-gap:24px">{links}</ul>')
    h = h[:i] + NOTICE_HTML.replace("{CHAPTER_LINKS}", block) + "\n" + h[i:]
    return h


def main():
    src = OUT / "index.html"
    h = S.read(src)
    for f in OUT.glob("*.html"):
        if f.name != "index.html":
            f.unlink()
    chs = build(h)
    S.write_book(BOOK, h, chs, OUT, RELATED)
    S.write(src, patch_index(h, chs))
    S.make_og(BOOK, OUT, "Free to read · 30 techniques · 26 sectors", "One pattern. Every scale. Once you see it, you see it everywhere.")
    print(f"fractal: {len(chs)} pages")
    for c in chs:
        print(f"  {c['movement'][:20]:20} /fractal/{c['slug']:34} {len(S.plain(c['html']).split()):>6}w {len(c['heads']):>3}h  {c['seo_title'][:62]}")


if __name__ == "__main__":
    main()
