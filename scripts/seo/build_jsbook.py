#!/usr/bin/env python3
"""Round 2: one plain, crawlable page per chapter for the seven one-page books whose text lives in JavaScript
(The Long After, The Silence, The Repair, At Will, The Slow Take, The Loop, The Weighing).

Run:  python3 scripts/seo/build_jsbook.py [slug ...]      (no slug = all seven)
Reads library/<slug>/index.html (MOVEMENTS / CH / BODIES, pulled out by jsbook_extract.js in an empty sandbox)
and writes library/<slug>/<chapter>.html, contents.html, sitemap.xml, og.png, f/ (fonts), plus the findability
head on the book's own index.html. Chapter text is the book's own, word for word; the only additions are
connectors (breadcrumbs, prev/next, links to the Pattern Decoder pages a chapter names, related books).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S

HERE = Path(__file__).resolve().parent
DEC = ("playbook", "The Pattern Decoder", "Hundreds of manipulation and control tactics, each with signs and what to do")
ROOT_ = ("shadowroot", "The Root", "A guided practice for coming back to yourself")


def theme(bg, fg, fg2, panel, line, acc, disp="'BookDisplay',Georgia,serif", body="'BookSerif',Georgia,serif"):
    return {"fs": "1.1875rem", "scheme": "dark", "bg": bg, "fg": fg, "fg2": fg2, "panel": panel, "line": line,
            "glow": panel, "acc": acc, "accink": bg, "disp": disp, "body": body}


FRA = "'Fraunces','Iowan Old Style',Palatino,Georgia,serif"
BOOKS = {
    "longafter": dict(
        title="The Long After", sub="What happens once you've left",
        theme=theme("#151220", "#E5E0EC", "#948AA3", "#1B1728", "#332C42", "#E08A6A"),
        index_title="The Long After: Post-Separation Abuse After Leaving",
        genre=["Self-help", "Psychology", "Domestic abuse recovery"],
        about=["Post-separation abuse", "Leaving an abusive relationship", "Co-parenting with an abuser", "Litigation abuse",
               "Financial abuse", "Narcissistic abuse recovery", "Coercive control", "Trauma recovery"],
        keywords=["post-separation abuse", "after leaving an abusive relationship", "narcissist co-parenting",
                  "litigation abuse", "custody abuse", "abuse recovery", "free book"],
        related=[("feminine", "The Sovereign Divine Feminine", "A field guide to coercive control in relationships"), DEC, ROOT_]),
    "silence": dict(
        title="The Silence", sub="For men nobody thought to ask",
        theme=theme("#14171A", "#DEE1E4", "#878E96", "#1B1F23", "#2E343A", "#D65F53"),
        index_title="The Silence: Men in Abusive Relationships (Free Book)",
        genre=["Self-help", "Psychology", "Men's issues"],
        about=["Male victims of domestic abuse", "Abused men", "Coercive control", "Emotional abuse", "Narcissistic abuse",
               "Abusive relationships", "Men's mental health"],
        keywords=["abused men", "male domestic abuse victim", "emotionally abusive wife", "coercive control men",
                  "men in abusive relationships", "narcissistic abuse men", "free book"],
        related=[("feminine", "The Sovereign Divine Feminine", "A field guide to coercive control in relationships"), DEC, ("longafter", "The Long After", "What happens once you've left")]),
    "repair": dict(
        title="The Repair", sub="For the person on the other side of it",
        theme=theme("#161615", "#E5E2DA", "#918D85", "#1D1D1B", "#33322F", "#C29A52"),
        index_title="The Repair: How to Stop Being Controlling (Free Book)",
        genre=["Self-help", "Psychology", "Behaviour change"],
        about=["Stopping abusive behaviour", "Controlling behaviour", "Accountability", "Emotional abuse",
               "Coercive control", "Repairing relationships", "Anger and control"],
        keywords=["how to stop being controlling", "am I the abuser", "how to stop being abusive", "accountability",
                  "change controlling behavior", "emotional abuse", "free book"],
        related=[DEC, ("scale", "The Weighing", "How to be right about people"), ROOT_]),
    "atwill": dict(
        title="At Will", sub="The coercive workplace",
        theme=theme("#12151A", "#DDE2E6", "#828A92", "#181C22", "#2A3038", "#D9A03E"),
        index_title="At Will: Workplace Bullying and Gaslighting (Free Book)",
        genre=["Self-help", "Workplace", "Psychology"],
        about=["Workplace bullying", "Workplace gaslighting", "Toxic boss", "Workplace harassment", "Retaliation",
               "Employee rights", "Coercive control at work"],
        keywords=["workplace bullying", "workplace gaslighting", "toxic boss", "narcissistic boss", "retaliation at work",
                  "hostile work environment", "free book"],
        related=[DEC, ("fracture", "The Fracture", "Who received fifty trillion dollars, and how"), ("scale", "The Weighing", "How to be right about people")]),
    "slowtake": dict(
        title="The Slow Take", sub="Coercion in later life",
        theme=theme("#171510", "#E6DFCB", "#9C927A", "#1E1B14", "#39331F", "#CFA847"),
        index_title="The Slow Take: Elder Abuse and Financial Exploitation",
        genre=["Self-help", "Ageing and family", "Psychology"],
        about=["Elder abuse", "Elder financial abuse", "Financial exploitation", "Undue influence", "Romance scams",
               "Caregiver abuse", "Coercive control"],
        keywords=["elder abuse", "elder financial abuse", "undue influence", "parent being scammed",
                  "financial exploitation of elderly", "romance scam elderly", "free book"],
        related=[DEC, ("fractal", "The Fractal", "One manipulation pattern at every scale"), ROOT_]),
    "loop": dict(
        title="The Loop", sub="The machine that learns you", fonts=["Fraunces"],
        theme=theme("#0E1116", "#E4E8ED", "#8C95A2", "#161B22", "#252D38", "#7FB2E8", FRA, FRA),
        index_title="The Loop: Algorithmic Manipulation and Dark Patterns",
        genre=["Technology", "Psychology", "Media studies"],
        about=["Algorithmic manipulation", "Dark patterns", "Attention economy", "Social media addiction",
               "Persuasive technology", "Surveillance advertising", "Recommendation algorithms"],
        keywords=["algorithmic manipulation", "dark patterns", "social media manipulation", "attention economy",
                  "doomscrolling", "how algorithms manipulate you", "free book"],
        related=[DEC, ("fractal", "The Fractal", "One manipulation pattern at every scale"), ("fracture", "The Fracture", "Who received fifty trillion dollars, and how")]),
    "scale": dict(
        title="The Weighing", sub="How to be right about people", fonts=["Fraunces"],
        theme=theme("#16140F", "#E7DFCE", "#A09683", "#1D1A14", "#3A342A", "#C29A52", FRA, FRA),
        index_title="The Weighing: Is It Manipulation or Ordinary Conflict?",
        genre=["Psychology", "Critical thinking", "Self-help"],
        about=["Discernment", "Manipulation", "Narcissistic abuse", "Evidence", "Cognitive bias", "Healthy conflict",
               "Recognising abuse"],
        keywords=["is it manipulation", "am I being manipulated", "narcissist or not", "healthy conflict vs abuse",
                  "how to judge people", "red flags", "free book"],
        related=[DEC, ("repair", "The Repair", "For the person on the other side of it"), ("longafter", "The Long After", "What happens once you've left")]),
}


def extract(index):
    out = subprocess.run(["node", str(HERE / "jsbook_extract.js"), str(index)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def book_meta(slug, h):
    b = dict(BOOKS[slug])
    desc = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    desc = re.sub(r"\s*Free, offline,.*$", "", desc).strip()
    b.update(slug=slug, version=b.get("version", "v4"), fonts=b.get("fonts", ["BookDisplay", "BookSerif"]),
             description=f"{desc} Free to read, by {S.AUTHOR}.",
             index_desc=S.clip(f"{b['title']}: {b['sub']}. {desc} Free to read online, chapter by chapter.", 158),
             notice_short=("Information and lived-pattern guidance, not legal, medical or therapeutic advice. "
                           "If you are in danger, contact local emergency services."),
             notice_href=f"/{slug}#/limits", unit="chapters",
             contents_eyebrow=f"Free to read · {b['sub']}")
    return b


def decoder_index():
    """(pattern, url, page name): every Decoder name and alias, including one-word names of 8+ letters
    (Hoovering, Gaslighting, Triangulation) that the inline linker skips."""
    import html as _h
    site = S.ROOT / "instruments/playbook/site"
    pages = {}
    for f in sorted(site.glob("*.html")):
        if f.name in ("index.html", "tactics.html") or f.name.startswith("line-"):
            continue
        t = re.search(r"<title>(.*?):", S.read(f))
        if t:
            pages[f"/playbook/{f.stem}"] = _h.unescape(t.group(1)).strip()
    pats = []
    for name, url in S.decoder_terms():
        pats.append((re.compile(r"\b" + re.escape(name) + r"\b", re.I), url))
    for url, full in pages.items():
        for w in re.split(r"\s*/\s*", re.sub(r"\s*\(.*?\)", "", full)):
            if " " not in w and len(w) >= 8:
                pats.append((re.compile(r"\b" + re.escape(w) + r"\b", re.I), url))
    for words, slug in EVERYDAY:
        assert f"/playbook/{slug}" in pages, slug
        pats.append((re.compile(r"\b(?:" + words + r")\b", re.I), f"/playbook/{slug}"))
    return pats, pages


# the everyday words these books use, mapped to the Decoder page that names the same pattern (links only)
EVERYDAY = [
    (r"family court|custody|court orders?|litigation|legal process|solicitors?|lawyers?", "legal-abuse"),
    (r"children as (?:the )?channel|through the children|use the children", "children-as-leverage"),
    (r"money as (?:the )?channel|financial abuse|controlled the money|bank accounts?|joint accounts?|debt in your name", "financial-control"),
    (r"economic dependence|financially dependent|no money of your own", "financial-dependence-by-design"),
    (r"narrative campaign|smear|telling people you|rumou?rs?|reputation", "smear-campaigns"),
    (r"mutual friends|flying monkeys|recruit(?:ed|s)? (?:others|people|friends|family)", "flying-monkeys-proxy-recruitment"),
    (r"tracking|trackers?|location sharing|stalkerware|spyware|surveillance|monitor(?:s|ed|ing) your", "monitoring-surveillance"),
    (r"find my|airtags?|gps", "location-tracking"),
    (r"isolat(?:ed|ion|ing)|cut (?:you )?off from", "isolation"),
    (r"silent treatment|stonewall(?:ing|ed)?|went silent|withdrawal of affection", "withholding-silent-treatment"),
    (r"blame[sd]? you|your fault|blame-shifting", "blame-shifting"),
    (r"guilt", "guilt-tripping"),
    (r"come back|hoover(?:ing|ed)?|promises? to change|if you go back", "hoovering-relief-bait"),
    (r"trauma bond(?:ing|ed)?|bonded to|miss them", "trauma-bonding"),
    (r"threat(?:s|en|ened|ening)?|intimidat(?:e|ion|ing)", "intimidation"),
    (r"minimi[sz](?:e|ed|ing)|it wasn't that bad|overreacting", "minimization"),
    (r"apolog(?:y|ies|ise|ize|ising|izing)", "non-apology-apologies"),
    (r"accountab(?:le|ility)", "accountability-reset"),
    (r"jealous(?:y)?|possessive", "behavior-control"),
    (r"memory|remember(?:ed|ing)? it differently|your own perception", "gaslighting"),
    (r"fawn(?:ing)?|appeas(?:e|ing|ement)|walking on eggshells", "fawning"),
    (r"sleep", "sleep-deprivation"),
    (r"police|protective orders?|reporting it", "legal-administrative-threats"),
    (r"benefits|housing|agencies|systems abuse|false reports?|vexatious", "administrative-escalation"),
    (r"therapy[- ]speak|weaponi[sz]ed therapy|boundaries as a weapon", "weaponized-therapy-speak"),
    (r"retaliat(?:e|ion|ed)|disciplinary|performance review|HR\b", "performance-framework-manipulation"),
    (r"micromanag(?:e|ed|ement|ing)|monitor(?:ing)? (?:your )?(?:work|keystrokes|screen)|productivity tracking", "performance-monitoring"),
    (r"undue influence|power of attorney|new best friend|caregiver|carer", "i-know-best-paternalism-velvet-glove-control"),
    (r"scams?|scammers?|romance scam", "love-bombing"),
    (r"love[- ]bomb(?:ing|ed)?|too good to be true|intense early", "love-bombing"),
    (r"future[- ]fak(?:ing|e)|promised a future", "future-faking"),
    (r"dark patterns?|interface", "dark-patterns-ai-adaptive"),
    (r"algorithms?|recommendation|feed", "algorithmic-manipulation"),
    (r"outrage", "moral-outrage-as-weapon"),
    (r"information control|what you were allowed to know", "information-control"),
    (r"triangulat(?:e|ion|ing)|compar(?:ed|es|ing) you to", "triangulation"),
    (r"control(?:ling)? (?:behaviou?r|partner)|coercive control", "behavior-control"),
    (r"darvo|deny, attack|played the victim", "darvo"),
    (r"gaslight(?:ing|ed)?", "gaslighting"),
]


DEC_PATS = None


def decoder_block(title, body):
    """Up to four Decoder pages this chapter is about: named in its title first, then most-mentioned in its text."""
    global DEC_PATS
    if DEC_PATS is None:
        DEC_PATS = decoder_index()
    pats, pages = DEC_PATS
    text = S.plain(body)
    score = {}
    for rx, url in pats:
        n = len(rx.findall(text)) + 10 * len(rx.findall(title))
        if n:
            score[url] = max(score.get(url, 0), n)
    top = sorted(score, key=lambda u: -score[u])[:4]
    items = "".join(f'<li><a href="{u}">{S.esc(pages[u])}</a></li>' for u in top)
    if not top:
        items = '<li><a href="/playbook">Look up any pattern in the Pattern Decoder</a></li><li><a href="/topics">Every topic, A to Z</a></li>'
    else:
        items += '<li><a href="/playbook">Every pattern in the Pattern Decoder</a></li>'
    return (f'\n<section class="dec" aria-labelledby="dec-h"><h2 id="dec-h">Name the pattern in the Pattern Decoder</h2>'
            f"<ul>{items}</ul></section>"), len(top)


def blocks(frag):
    """The books' styled boxes are <div>s; keep them as separate blocks (pull quote = blockquote, others = paragraph)."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(frag, "html.parser")
    for d in reversed(soup.find_all("div")):
        if d.find(["p", "ul", "ol", "h3", "h4", "div", "table", "blockquote"]):
            if "pull" in (d.get("class") or []):
                d.name = "blockquote"
            else:
                d.unwrap()
        else:
            d.name = "blockquote" if "pull" in (d.get("class") or []) else "p"
    return str(soup)


def chapters(slug, data):
    mv_of = {}
    for m in data["MOVEMENTS"]:
        for n in m["c"]:
            mv_of[int(n)] = f"{m['r']}. {m['t']}"
    nums = sorted(int(k) for k in data["CH"])
    slugs, seen = {}, set()
    for n in nums:
        s = S.slugify(data["CH"][str(n)]["t"], 60)
        while s in seen or s in ("contents", "index", "sitemap", "f", "og"):
            s += f"-{n}"
        seen.add(s)
        slugs[n] = s
    terms = S.decoder_terms()
    chs = []
    for n in nums:
        c = data["CH"][str(n)]
        body = data["BODIES"].get(str(n), "")
        # in-book chapter links (#/c/12) become links to that chapter's own page; other routes go to the book
        body = re.sub(r'href="#/c/(\d+)"', lambda m: f'href="/{slug}/{slugs.get(int(m.group(1)), "contents")}"', body)
        body = re.sub(r'href="#/([a-z]+)"', lambda m: f'href="/{slug}#/{m.group(1)}"', body)
        body = S.clean_fragment(blocks(body), None, slug)
        body = re.sub(r"<(/?)h3\b", r"<\1h2", body)
        body = re.sub(r"<(/?)h4\b", r"<\1h3", body)
        body, heads = S.give_heading_ids(body)
        body = S.link_terms(body, terms, limit=5)
        title = S.plain(c["t"])
        block, _ = decoder_block(title, body)
        body += block
        chs.append({"n": n, "slug": slugs[n], "title": title, "eyebrow": f"Chapter {n}", "movement": mv_of.get(n),
                    "lede": c.get("d"), "blurb": c.get("d"), "html": body, "heads": heads,
                    "desc": S.clip(f"{c.get('d', '')} " + S.first_sentences(body, 200), 158),
                    "seo_title": f"{title} · {BOOKS[slug]['title']}"})
    return chs


def patch_index(book, h):
    h = S.inject_index(book, h, CHS[book["slug"]])
    # one plain link to the chapter-by-chapter edition, so crawlers (and readers) can reach every chapter page
    mark = "<!-- nf-contents-link -->"
    h = re.sub(re.escape(mark) + r".*?" + re.escape(mark) + r"\n?", "", h, flags=re.S)
    # the page's one heading in the HTML itself (the cover's visible heading is drawn by the script); same words
    link = (f'{mark}<h1 style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">'
            f'{S.esc(book["title"])}: {S.esc(book["sub"])}</h1>\n<p class="nf-contents-link" style="text-align:center;margin:32px auto;padding:0 16px;font-size:16px">'
            f'<a href="/{book["slug"]}/contents" style="color:inherit">Read {S.esc(book["title"])} chapter by chapter</a>'
            f' &middot; <a href="/playbook" style="color:inherit">The Pattern Decoder</a></p>{mark}\n')
    ver = ('<span class="ver">v4 &middot; 21 November 2026 &mdash; Every chapter now also has its own page, so a search '
           'or an AI assistant can point you straight to it, with links to the matching patterns in the Pattern Decoder.</span>')
    first = '<span class="ver">v3 &middot;'
    if first in h and ver not in h:
        h = h.replace(first, ver + first, 1)
    h = cover(book, h)
    # owner 2026-11-21: remove the "no analytics" line (the anonymous Cloudflare visit count is on every page)
    for old, new in (("No account, no analytics, nothing stored", "No account, nothing stored"),
                     ("no stored reading position, no analytics. It does", "no stored reading position. It does"),
                     ("no accounts, no analytics, nothing stored", "no accounts, nothing stored")):
        h = h.replace(old, new)
    assert "no analytics" not in h.lower(), book["slug"]
    i = h.find('<script id="book-js">')
    return h[:i] + link + h[i:]


COVER_FILE = {"longafter": "03", "silence": "10", "repair": "11", "atwill": "12", "slowtake": "13", "loop": "14", "scale": "15"}


def cover(book, h):
    """Owner 2026-11-21: the new signed cover art (content/covers/signed/) replaces the old cover strip on the book page.
    Written as /<book>/cover.webp (absolute path, a separate file instead of base64 inside the page)."""
    from PIL import Image
    slug = book["slug"]
    src = S.ROOT / "content/covers/signed" / f"{COVER_FILE[slug]}-{slug}.jpg"
    im = Image.open(src).convert("RGB")
    w = 720
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(S.ROOT / "library" / slug / "cover.webp", "WEBP", quality=80, method=6)
    tag = (f'<img class="cover-mark nf-cover" src="/{slug}/cover.webp" width="{w}" height="{im.height}" '
           f'alt="{book["title"]} by Shae Stovell, book cover" decoding="async" fetchpriority="high">')
    h = re.sub(r'<img class="cover-mark[^"]*"[^>]*>', tag, h, count=1)
    if "nf-cover" not in h:      # The Loop and The Weighing had no cover on the page: put it at the top of the hero
        anchor = "'<section class=\"hero\"><div class=\"wrap\">'+"
        assert anchor in h, slug
        h = h.replace(anchor, anchor + "\n   '" + tag + "'+", 1)
    css = ('<style id="nf-cover-css">.nf-cover{display:block;width:min(64vw,300px);max-width:300px;height:auto;aspect-ratio:'
           f'{w}/{im.height};margin:8px auto 24px;border-radius:4px;box-shadow:0 18px 40px rgba(0,0,0,.28),0 2px 6px rgba(0,0,0,.18);filter:none}}</style>')
    h = re.sub(r'<style id="nf-cover-css">.*?</style>\n?', "", h, flags=re.S)
    return h.replace("</head>", css + "\n</head>", 1)


CHS = {}

# The Loop and The Weighing still carry the older drawer; their new chapter pages use the current shared menu
import importlib.util as _iu
def _load(name, path):
    spec = _iu.spec_from_file_location(name, path); m = _iu.module_from_spec(spec); spec.loader.exec_module(m); return m
CAT = _load("nf_catalogue", S.ROOT / "scripts/nf-catalogue.py")          # the one list of every book and project (21)
NH = _load("nh_drawer", S.ROOT / "scripts/nh-drawer-catalogue.py")       # the older drawer on The Loop / The Weighing
_house = S.house_parts
_here = {}
S.house_parts = lambda h: _house(h if 'id="nf-chrome-css"' in h else
                                 CAT.retoc(S.read(S.ROOT / "library/longafter/index.html"), _here["slug"]))


def main(slugs):
    for slug in slugs:
        out = S.ROOT / "library" / slug
        src = out / "index.html"
        h = S.read(src)
        _here["slug"] = slug
        # every page lists every other book and project (scripts/nf-catalogue.py), this one marked as "here"
        h = CAT.retoc(h, slug) if 'class="nf-toc"' in h else NH.retoc(h, "scale" if slug == "scale" else slug)
        book = book_meta(slug, h)
        chs = chapters(slug, extract(src))
        CHS[slug] = chs
        names = S.write_book(book, h, chs, out, book["related"])
        S.write(src, patch_index(book, h))
        S.make_og(book, out, f"Free to read · {len(chs)} chapters", book["sub"] + ".")
        words = sum(len(S.plain(c["html"]).split()) for c in chs)
        dec = sum(c["html"].count('href="/playbook/') for c in chs)
        print(f"{slug}: {len(names)} chapter pages + contents + sitemap · {words} words · {dec} Decoder links")


if __name__ == "__main__":
    main(sys.argv[1:] or list(BOOKS))
