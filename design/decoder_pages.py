"""Plain pages for the Pattern Decoder (v16): one per tactic, one per line, an index of every tactic, and a sitemap.

The reader app (index.html) is one page with hash routes, so search engines and AI crawlers see it as a single
address. These pages give every tactic its own address (/playbook/gaslighting) with its full reading in plain HTML,
a descriptive title and description, a canonical link and a Schema.org DefinedTerm. Each one leads into the app.

Called by build-decoder-v15.py, which owns the content. This file only lays it out. Nothing here changes a word of an
entry. All links are absolute (/playbook/...) because the site is proxied at /playbook and relative paths would
resolve against whatever the address bar says (see CLAUDE.md, "This applies to images too").
"""
import base64
import html as _html
import json
import os
import re
import shutil

SITE = "https://noblefathercreations.com/playbook"
ORIGIN = "https://noblefathercreations.com"
BASE = "/playbook"
RESP = [("soft_clarification", "Ask about it gently"), ("firm_boundary", "Set a clear limit"), ("disengagement", "Step back"),
        ("support_seeking", "Get support"), ("workplace_or_professional", "At work, school or with services")]
SCRIPT_H = {"verify": "A check to run before you share or act", "self": "Words to say to yourself", "say": "Words you could use"}


# ---------- text helpers: ports of the app's own, so the plain pages read the same ----------
def esc(s):
    return _html.escape(str(s if s is not None else ""), quote=True)


def curly(s):
    s = re.sub(r'(^|[\s(\u2014-])"', "\\1\u201c", str(s)).replace('"', "\u201d")
    return re.sub(r"(^|[\s(])'", "\\1\u2018", s).replace("'", "\u2019")


def H(s):
    return esc(curly(s))


def sentences(t):
    m = re.findall(r"[^.!?]+(?:[.!?]+[\"\u201d\u2019)]*|$)\s*", str(t or ""))
    return [x.strip() for x in (m or [str(t or "")]) if x.strip()]


def prose(t):
    ss = sentences(t)
    if not ss:
        return ""
    out = "<p><strong>" + H(ss[0]) + "</strong>" + (" " + H(ss[1]) if len(ss) > 1 else "") + "</p>"
    for i in range(2, len(ss), 2):
        out += "<p>" + H(ss[i]) + (" " + H(ss[i + 1]) if i + 1 < len(ss) else "") + "</p>"
    return out


def unq(t):
    t = str(t or "").strip()
    return re.sub(r"\s*[\"\u201d\u2019]$", "", re.sub(r"^[\"\u201c\u2018]\s*", "", t)) if re.match(r"^[\"\u201c\u2018]", t) and re.search(r"[\"\u201d\u2019]$", t) else t


def say_li(t):
    t = str(t or "").strip()
    narrates = re.match(r"^[\"\u201c\u2018]", t) and not re.search(r"[\"\u201d\u2019]$", t)
    return '<li class="nq">' + H(t) + "</li>" if narrates else "<li>" + H(unq(t)) + "</li>"


def clip(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    if len(s) <= n:
        return s
    c = s[: n - 1]
    return re.sub(r"[,;:.]$", "", c[: c.rfind(" ")]) + "\u2026"


def ul(items, cls=""):
    items = [i for i in (items or []) if str(i).strip()]
    return '<ul%s>%s</ul>' % (' class="%s"' % cls if cls else "", "".join("<li>" + H(i) + "</li>" for i in items)) if items else ""


def sec(title, body, cls=""):
    return '<section class="blk%s"><h2>%s</h2>%s</section>' % (" " + cls if cls else "", title, body) if body else ""


# ---------- page frame ----------
CSS = """
@font-face{font-family:'Overpass';font-weight:600 800;font-display:swap;src:url(/playbook/f/overpass-var.woff2) format('woff2')}
@font-face{font-family:'Atkinson Next';font-weight:400 700;font-display:swap;src:url(/playbook/f/atkinson-next-var.woff2) format('woff2')}
:root{--bg:#050507;--panel:#0E0E12;--panel-2:#17171D;--rule:#25252D;--rule-hi:#383842;--fg:#F2F0EA;--fg-2:#A8A69E;--fg-3:#8B8982;
--blade:#E5C158;--blade-ink:#050507;--bullet-ink:#050507;--amber:#FF6B5E;--amber-fill:#F04438;--amber-fill-ink:#050507;--exit:#00B864;--exit-ink:#04140B;
--sign:'Overpass',system-ui,sans-serif;--read:'Atkinson Next','Atkinson Hyperlegible',system-ui,sans-serif;color-scheme:dark}
@media (prefers-color-scheme:light){:root{--bg:#FBFAF7;--panel:#F3F1EB;--panel-2:#E8E5DC;--rule:#DAD6CB;--rule-hi:#BDB8AA;--fg:#14161A;--fg-2:#4B5159;--fg-3:#5C636B;
--blade:#6B500F;--blade-ink:#FFFFFF;--bullet-ink:#FFFFFF;--amber:#B42318;--exit:#007A40;--exit-ink:#FFFFFF;color-scheme:light}%DAY%}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1.125rem/1.6 var(--read);overflow-wrap:break-word}
a{color:inherit;text-decoration-color:var(--fg-3);text-underline-offset:.2em}a:hover{text-decoration-color:currentColor}
:focus-visible{outline:3px solid var(--fg);outline-offset:3px}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:16px;min-height:56px;padding:0 16px;padding-top:env(safe-area-inset-top);background:var(--bg);box-shadow:inset 0 -1px 0 var(--rule)}
.brand{font:800 1.0625rem/1 var(--sign);text-decoration:none;margin-right:auto;min-height:44px;display:flex;align-items:center}
.leave{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border:0;background:var(--exit);color:var(--exit-ink);font:700 .9375rem/1 var(--sign);cursor:pointer}
.view{max-width:44rem;margin:0 auto;padding:24px 16px 64px}
.crumbs{font:700 .875rem/1.4 var(--sign);color:var(--fg-2);margin:0 0 24px}.crumbs a{display:inline-block;min-height:44px;line-height:44px}
.sign{display:flex;gap:16px;align-items:flex-start;padding-top:16px;border-top:8px solid var(--lc,var(--fg))}
.bul{flex:none;display:grid;place-items:center;width:48px;height:48px;border-radius:50%;background:var(--lc);color:var(--bullet-ink);font:800 1.375rem/1 var(--sign)}
.bul.sm{width:28px;height:28px;font-size:.9375rem}
h1{font:800 clamp(2rem,1.3rem + 3.2vw,3.25rem)/1.04 var(--sign);letter-spacing:-.025em;margin:0}
h2{font:800 1.375rem/1.2 var(--sign);letter-spacing:-.01em;margin:0 0 12px}
.sub{color:var(--fg-2);margin:8px 0 0;font-size:1.1875rem;line-height:1.5}
.onl{font:700 .9375rem/1.4 var(--sign);color:var(--fg-2);margin:16px 0 32px}
.warn{margin:0 0 32px;background:var(--panel)}.warn h2{display:flex;gap:8px;align-items:center;margin:0;padding:10px 16px;background:var(--amber-fill);color:var(--amber-fill-ink);font-size:1rem}
.warn .body{padding:16px}.warn p{margin:0 0 12px}.warn p:last-child{margin:0}
.answer{background:var(--panel);padding:24px;box-shadow:inset 0 3px 0 var(--lc,var(--fg));margin:0 0 24px}.answer p{margin:0 0 12px}
.says{list-style:none;padding:0;margin:0}.says li{padding:8px 0 8px 32px;position:relative;font-style:italic}
.says li:not(.nq)::before{content:"\\201C";position:absolute;left:0;top:6px;font:800 2rem/1 var(--sign);color:var(--lc,var(--fg-2));font-style:normal}
.k{font:800 1.0625rem/1.2 var(--sign);margin:20px 0 4px}
.also{color:var(--fg-2);font-size:1rem;margin:12px 0 0}
.go{display:block;min-height:72px;padding:16px 20px;margin:0 0 48px;background:var(--blade);color:var(--blade-ink);text-decoration:none;font:800 1.1875rem/1.2 var(--sign)}
.go small{display:block;font:400 .9375rem/1.4 var(--read);margin-top:4px}
.blk{padding:32px 0 0;margin:32px 0 0;box-shadow:inset 0 1px 0 var(--rule)}.blk p{margin:0 0 12px}.blk ul{margin:0;padding-left:1.25em}.blk li{margin:0 0 8px}
.blk h3{font:800 1.0625rem/1.25 var(--sign);margin:20px 0 4px}
blockquote{margin:0;padding:16px 20px;background:var(--panel);font-style:italic;box-shadow:inset 3px 0 0 var(--lc,var(--fg-2))}
.rows{display:grid;gap:0}.row{display:flex;gap:12px;align-items:flex-start;padding:14px 0;text-decoration:none;box-shadow:inset 0 -1px 0 var(--rule);min-height:44px}
.row b{display:block;font:800 1.0625rem/1.25 var(--sign)}.row small{display:block;color:var(--fg-2);font-size:1rem;line-height:1.45;margin-top:2px}
.row .code{flex:none;font:700 .8125rem/28px var(--sign);color:var(--fg-2);min-width:2.75rem}
.pn{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:48px 0 0}.pn a{display:block;padding:16px;background:var(--panel);text-decoration:none;min-height:44px}
.pn small{display:block;color:var(--fg-2);font:700 .8125rem/1.3 var(--sign)}.pn b{font:800 1.0625rem/1.25 var(--sign)}.pn .nx{text-align:right}
.lede{color:var(--fg-2);font-size:1.1875rem;line-height:1.5;margin:16px 0 32px}
.foot{max-width:44rem;margin:0 auto;padding:32px 16px 96px;color:var(--fg-2);font-size:1rem;box-shadow:inset 0 1px 0 var(--rule)}
.foot nav{display:flex;flex-wrap:wrap;gap:0 24px}.foot nav a{min-height:44px;display:inline-flex;align-items:center}
.lines{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));margin:0 0 32px}
.lines a{display:flex;gap:12px;align-items:center;padding:12px;background:var(--panel);text-decoration:none;font:800 1rem/1.25 var(--sign);min-height:56px}
%LINES%
@media print{.top,.go,.foot nav,#nf-chrome{display:none}}
"""

LEAVE_JS = ("<script>document.getElementById('leave').addEventListener('click',function(){document.title='Weather';"
            "document.body.style.visibility='hidden';location.replace(navigator.onLine?'https://www.google.com/search?q=weather':'about:blank')});"
            "addEventListener('keydown',function(e){if(e.key==='Escape'){var n=Date.now();if(n-(window.__esc||0)<600)document.getElementById('leave').click();window.__esc=n}});</script>")


def frame(title, desc, url, ld, body, house, beacon, extra_head=""):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            "<title>%s</title>\n<meta name=\"description\" content=\"%s\">\n<link rel=\"canonical\" href=\"%s\">\n"
            "<meta property=\"og:type\" content=\"article\">\n<meta property=\"og:site_name\" content=\"Noble Father Creations\">\n"
            "<meta property=\"og:title\" content=\"%s\">\n<meta property=\"og:description\" content=\"%s\">\n<meta property=\"og:url\" content=\"%s\">\n"
            "<meta name=\"twitter:card\" content=\"summary\">\n"
            "<meta name=\"theme-color\" content=\"#050507\" media=\"(prefers-color-scheme: dark)\">\n"
            "<meta name=\"theme-color\" content=\"#FBFAF7\" media=\"(prefers-color-scheme: light)\">\n"
            "<link rel=\"icon\" href=\"/playbook/f/icon.webp\">\n%s"
            "<link rel=\"preload\" href=\"/playbook/f/overpass-var.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>\n"
            "<style>%s</style>\n<script type=\"application/ld+json\">%s</script>\n</head>\n<body>\n"
            "<header class=\"top\"><a class=\"brand\" href=\"/playbook\">Pattern Decoder</a>"
            "<button class=\"leave\" id=\"leave\" type=\"button\" aria-label=\"Leave this site now\">"
            "<svg width=\"20\" height=\"20\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" aria-hidden=\"true\"><path d=\"M14 4h5v16h-5M10 8l-4 4 4 4M6 12h10\"/></svg>Leave</button></header>\n"
            "%s\n"
            "<footer class=\"foot\"><p>A reading aid, not a diagnosis, a legal opinion or therapy. If you are in danger, contact emergency services. "
            "Press Escape twice, or the green Leave button, to leave this site quickly.</p>"
            "<nav aria-label=\"More\"><a href=\"/playbook\">Open the Pattern Decoder</a><a href=\"/playbook/tactics\">Every tactic</a>"
            "<a href=\"/playbook#/safety\">Use this safely</a><a href=\"/\">Noble Father Creations</a></nav></footer>\n"
            "%s\n%s\n%s\n</body>\n</html>\n") % (
        esc(title), esc(desc), url, esc(title), esc(desc), url, extra_head, CSS_FINAL, json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"),
        body, house, LEAVE_JS, beacon)


CSS_FINAL = ""


def bullet(l, cls=""):
    return '<span class="bul%s" aria-hidden="true">%s</span>' % (" " + cls if cls else "", l["letter"])


def code(l, n):
    return "%s %02d" % (l["letter"], n)


def term_set():
    return {"@type": "DefinedTermSet", "@id": SITE + "#set", "name": "Pattern Decoder", "url": SITE,
            "description": "A free guide to manipulation and control tactics in plain words.",
            "publisher": {"@type": "Organization", "name": "Noble Father Creations", "url": ORIGIN}}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                                            for i, (n, u) in enumerate(items)]}


# ---------- the three kinds of page ----------
def tactic_page(e, l, si, by, line_of, house, beacon):
    f, n, s = e["f"], e["n"], e["s"]
    url = SITE + "/" + s
    title = n + ": Signs, Examples and What to Do \u00b7 Pattern Decoder"
    desc = clip("What is " + n + "? " + f["short_definition"], 160)
    order = l["order"]
    prev = by[order[si - 1]] if si > 0 else None
    nxt = by[order[si + 1]] if si + 1 < len(order) else None
    says = f.get("what_it_sounds_like") or []
    rel = [by[r] for r in e["rel"] if r in by]
    resp = "".join("<h3>%s</h3><p>%s</p>" % (h, H(f["response_options"][k]))
                   for k, h in RESP if (f.get("response_options") or {}).get(k))
    script = re.sub(r"^Verification script[^:]*:\s*", "", str(f.get("boundary_script") or ""), flags=re.I)
    other = (f.get("this_may_not_be_it_when") or []) + (f.get("less_concerning_if") or [])
    body = (
        '<main class="view" data-g="%s"><article aria-labelledby="h">' % l["k"] +
        '<nav class="crumbs" aria-label="You are here"><a href="/playbook">Pattern Decoder</a> \u203a <a href="/playbook/line-%s">%s</a></nav>' % (l["k"], esc(l["label"])) +
        '<header><div class="sign">%s<div><h1 id="h">%s</h1>%s</div></div>' % (bullet(l), H(n), '<p class="sub">%s</p>' % H(e["sub"]) if e["sub"] else "") +
        '<p class="onl">Station %d of %d on the %s line. Code %s</p></header>' % (si + 1, len(order), esc(l["label"]), code(l, si + 1)) +
        ('<section class="warn" role="note" aria-labelledby="w"><h2 id="w"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3 2 20h20z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/></svg>Safety first</h2><div class="body">%s</div></section>' % prose(f["safety_note"]) if e["sens"] else "") +
        '<section class="answer" aria-label="In short"><h2>What is %s?</h2>%s%s%s</section>' % (
            H(n), prose(f["plain_language_summary"]),
            ('<h3 class="k">It can sound like</h3><ul class="says">%s</ul>' % "".join(say_li(x) for x in says[:3])) if says else "",
            ('<p class="also">Also called %s</p>' % ", ".join(H(a) for a in e["abs"])) if e["abs"] else "") +
        '<a class="go" href="/playbook#/entry/%s">Check it step by step in the guide<small>Tick what fits, compare look-alikes and save it, all on your own device.</small></a>' % s +
        sec("Signs it might be this", ul(f.get("this_may_be_it_when"))) +
        sec("Signs it is probably something else", ul(other)) +
        sec("Questions to ask yourself", ul(f.get("discernment_questions"))) +
        sec("What it is", prose(f.get("expanded_definition"))) +
        sec("Why it matters", prose(f.get("why_this_matters"))) +
        sec("How it shows up", ul(f.get("what_it_is"))) +
        sec("What you can do",
            ('<p>Read the safety note at the top first. If speaking up could make things worse, skip the wording below and talk to someone you trust or a local support service.</p>' if e["sens"]
             else "<p>Pick what fits. You do not owe anyone a confrontation.</p>") +
            ("<h3>%s</h3><blockquote>%s</blockquote>" % (SCRIPT_H[e["kind"]], H(script)) if script else "") + resp) +
        sec("Using this label fairly", ul(f.get("misuse_warning"))) +
        sec("How it differs from look-alikes",
            prose(f.get("how_to_distinguish_from_related")) +
            ('<div class="rows">%s</div>' % "".join(
                '<a class="row" href="/playbook/%s" data-g="%s">%s<span><b>%s</b><small>%s</small></span></a>' % (
                    r["s"], r["g"], bullet(line_of[r["g"]], "sm"), H(r["n"]), H(clip(r["f"]["short_definition"], 120))) for r in rel[:8]) if rel else "")) +
        '<nav class="pn" aria-label="Along the %s line">%s%s</nav>' % (
            esc(l["label"]),
            '<a href="/playbook/%s"><small>Previous station</small><b>%s</b></a>' % (prev["s"], H(prev["n"])) if prev else "<span></span>",
            '<a class="nx" href="/playbook/%s"><small>Next station</small><b>%s</b></a>' % (nxt["s"], H(nxt["n"])) if nxt else "") +
        "</article></main>")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "DefinedTerm", "@id": url + "#term", "name": n, "url": url, "termCode": code(l, si + 1).replace(" ", ""),
         "description": f["short_definition"], **({"alternateName": e["abs"]} if e["abs"] else {}), "inDefinedTermSet": {"@id": SITE + "#set"}},
        term_set(),
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": SITE + "#set"}, "about": {"@id": url + "#term"},
         "breadcrumb": crumbs_ld([("Noble Father Creations", ORIGIN), ("Pattern Decoder", SITE), (l["label"], SITE + "/line-" + l["k"]), (n, url)])}]}
    return frame(title, desc, url, ld, body, house, beacon)


def line_page(l, by, house, beacon):
    url = SITE + "/line-" + l["k"]
    title = "%s: %d Tactics \u00b7 Pattern Decoder" % (l["label"], len(l["order"]))
    desc = clip(l["blurb"], 160)
    rows = "".join('<a class="row" href="/playbook/%s"><span class="code">%s</span><span><b>%s</b><small>%s</small></span></a>' % (
        by[n]["s"], code(l, i + 1), H(n), H(clip(by[n]["f"]["short_definition"], 140))) for i, n in enumerate(l["order"]))
    body = ('<main class="view" data-g="%s"><nav class="crumbs" aria-label="You are here"><a href="/playbook">Pattern Decoder</a> \u203a <a href="/playbook/tactics">Every tactic</a></nav>'
            '<div class="sign">%s<h1>%s</h1></div><p class="lede">%s %d tactics on this line, in the order the guide walks them.</p>'
            '<a class="go" href="/playbook#/line/%s">Open this line in the guide<small>See it on the map, with look-alikes on other lines.</small></a>'
            '<div class="rows">%s</div></main>') % (l["k"], bullet(l), esc(l["label"]), H(l["blurb"]), len(l["order"]), l["k"], rows)
    ld = {"@context": "https://schema.org", "@graph": [
        term_set(),
        {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "#set"},
         "breadcrumb": crumbs_ld([("Noble Father Creations", ORIGIN), ("Pattern Decoder", SITE), (l["label"], url)]),
         "mainEntity": {"@type": "ItemList", "numberOfItems": len(l["order"]), "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": SITE + "/" + by[n]["s"], "name": n} for i, n in enumerate(l["order"])]}}]}
    return frame(title, desc, url, ld, body, house, beacon)


def index_page(lines, by, count, house, beacon):
    url = SITE + "/tactics"
    title = "All %d Manipulation and Control Tactics, A to Z by Group \u00b7 Pattern Decoder" % count
    desc = "Every one of the %d tactics in the Pattern Decoder, grouped into ten lines, each with its own plain-words page." % count
    body = ('<main class="view"><nav class="crumbs" aria-label="You are here"><a href="/playbook">Pattern Decoder</a></nav>'
            '<h1>Every tactic</h1><p class="lede">%d manipulation and control tactics in ten groups. Each has its own page in plain words: '
            'what it is, what it can sound like, how to tell if it fits, and what you can do.</p>'
            '<a class="go" href="/playbook#/help">Not sure what to look for?<small>Answer two short questions in the guide instead.</small></a>'
            '<nav class="lines" aria-label="Lines">%s</nav>%s</main>') % (
        count,
        "".join('<a href="#%s" data-g="%s">%s%s</a>' % (l["k"], l["k"], bullet(l, "sm"), esc(l["label"])) for l in lines),
        "".join('<section class="blk" id="%s" data-g="%s"><h2><a href="/playbook/line-%s">%s</a></h2><div class="rows">%s</div></section>' % (
            l["k"], l["k"], l["k"], esc(l["label"]),
            "".join('<a class="row" href="/playbook/%s"><span class="code">%s</span><span><b>%s</b></span></a>' % (by[n]["s"], code(l, i + 1), H(n))
                    for i, n in enumerate(l["order"]))) for l in lines))
    ld = {"@context": "https://schema.org", "@graph": [term_set(), {
        "@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE + "#set"},
        "hasPart": [{"@type": "CollectionPage", "url": SITE + "/line-" + l["k"], "name": l["label"]} for l in lines]}]}
    return frame(title, desc, url, ld, body, house, beacon)


def crawl_links(lines, count):
    """Links for crawlers that do not run scripts, placed in the app's <noscript>."""
    return ('<nav aria-label="Every tactic" style="max-width:44rem;margin:0 auto;padding:24px 16px">'
            '<p><a href="/playbook/tactics">All %d tactics, each on its own page</a></p><ul>%s</ul></nav>') % (
        count, "".join('<li><a href="/playbook/line-%s">%s</a></li>' % (l["k"], esc(l["label"])) for l in lines))


def ld_set(count):
    return json.dumps({"@context": "https://schema.org", "@graph": [
        {**term_set(), "description": "A free guide to %d manipulation and control tactics in plain words." % count},
        {"@type": "WebApplication", "name": "Pattern Decoder", "url": SITE, "applicationCategory": "ReferenceApplication",
         "operatingSystem": "Any", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "publisher": {"@type": "Organization", "name": "Noble Father Creations", "url": ORIGIN}}]},
        ensure_ascii=False).replace("</", "<\\/")


def write_site(out_dir, app_html, entries, lines, house, beacon, logo_data_uri, font_dir, date):
    """Write the publish directory: the app as index.html, the plain pages beside it, fonts, icon and sitemap."""
    global CSS_FINAL
    line_of = {l["k"]: l for l in lines}
    by = {e["n"]: e for e in entries}
    day = "".join(":root [data-g=%s]{--lc:%s}" % (l["k"], l["d"]) for l in lines)
    CSS_FINAL = re.sub(r"\s*\n\s*", "", CSS.replace("%DAY%", day).replace(
        "%LINES%", "".join("[data-g=%s]{--lc:%s}" % (l["k"], l["c"]) for l in lines)))
    if os.path.isdir(out_dir):
        for name in os.listdir(out_dir):        # generated output only; stale pages from renamed tactics must not linger
            p = os.path.join(out_dir, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(os.path.join(out_dir, "f"), exist_ok=True)
    for fn in ("overpass-var.woff2", "atkinson-next-var.woff2"):
        shutil.copyfile(os.path.join(font_dir, fn), os.path.join(out_dir, "f", fn))
    open(os.path.join(out_dir, "f", "icon.webp"), "wb").write(base64.b64decode(logo_data_uri.split(",", 1)[1]))
    pages = {"index.html": app_html,
             "tactics.html": index_page(lines, by, len(entries), house, beacon)}
    for l in lines:
        pages["line-%s.html" % l["k"]] = line_page(l, by, house, beacon)
        for si, n in enumerate(l["order"]):
            e = by[n]
            pages[e["s"] + ".html"] = tactic_page(e, l, si, by, line_of, house, beacon)
    for name, text in pages.items():
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    urls = [SITE, SITE + "/tactics"] + [SITE + "/line-" + l["k"] for l in lines] + [SITE + "/" + by[n]["s"] for l in lines for n in l["order"]]
    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                 "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, date) for u in urls) + "</urlset>\n")
    return pages, urls
