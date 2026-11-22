"""The frame on every page (NAV-SPEC 3): top bar (mark, sector switcher, search, Leave), breadcrumbs, footer,
search dialog, THE HOUSE drawer and the beacon, exactly as the previous frame() included them."""
import json

from lib import CONFIG, HERE, ROOT, S, esc, svg

_CSS = {}


def css(cx):
    if cx.root not in _CSS:
        tokens = CONFIG["tokens"].read_text().replace("/F/", cx.root + "/_a/f/")
        _CSS[cx.root] = tokens + "\n" + (HERE / "sector.css").read_text()
    return _CSS[cx.root]


def switcher(cx):
    rows = []
    for s in cx.reg["sectors"]:
        cur = s.get("id") and s["id"].upper() == cx.d["sector"]
        n = '<span class="num">%02d</span>' % s["n"]
        if s.get("built") and s.get("slug"):
            rows.append('<li%s>%s<a href="%s/%s"%s>%s</a><span class="st">%s</span></li>' % (
                ' class="cur"' if cur else "", n, cx.root, s["slug"], ' aria-current="true"' if cur else "",
                esc(s.get("title") or s["name"]), esc(S("switcher_built"))))
        else:
            ch = s.get("fractal_chapter")
            ok = ch and (ROOT / "library" / (ch.strip("/") + ".html")).exists()
            rows.append('<li>%s<span class="nm">%s</span><span class="st">%s%s</span></li>' % (
                n, esc(s["name"]), esc(S("switcher_unbuilt")),
                ' · <a href="%s">%s</a>' % (ch, esc(S("switcher_fractal"))) if ok else ""))
    return f"""<details class="sw" id="sw">
  <summary aria-label="{esc(S('switcher_label'))}: {esc(cx.short)}">{svg('grid', 16)}<span class="sw-l">{esc(cx.short)}</span><span class="sw-s">{esc(S('switcher_label'))}</span></summary>
  <div class="sw-panel"><p class="kicker">{esc(S('switcher_title'))}</p><ol class="sw-list">{''.join(rows)}</ol></div>
</details>"""


def search_dialog():
    return f"""<dialog class="sd-dlg" id="search" aria-labelledby="search-h">
  <form method="dialog" class="sd-head"><h2 id="search-h" class="vh">{esc(S('search_label'))}</h2>
    <label class="sd-field">{svg('search')}<span class="vh">{esc(S('search_label'))}</span>
      <input id="sq" type="search" autocomplete="off" spellcheck="false" placeholder="{esc(S('search_placeholder'))}" aria-controls="sr" aria-describedby="sp"></label>
    <button class="icon-btn" value="close" aria-label="{esc(S('close'))}">{svg('x')}</button></form>
  <p class="sd-note" id="sp">{esc(S('search_private'))}</p>
  <div id="sr" class="sd-res" aria-live="polite" data-p="{esc(S('search_patterns'))}" data-t="{esc(S('search_tactics'))}" data-empty="{esc(S('search_empty'))}" data-loading="{esc(S('search_loading'))}"></div>
</dialog>"""


def frame(cx, *, title, desc, path, crumbs, body, ld, og="home", progress=False, cls=""):
    O = CONFIG["origin"]
    url = O + cx.u(path)
    crumbs = [(S("site"), cx.root)] + crumbs
    crumb_html = '<span aria-hidden="true">/</span>'.join(
        '<a href="%s">%s</a>' % (u, esc(n)) if u else '<span aria-current="page">%s</span>' % esc(n) for n, u in crumbs)
    ld_all = {"@context": "https://schema.org", "@graph": ld + [{
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": O + (u or cx.u(path))}
            for i, (n, u) in enumerate(crumbs)]}]}
    f = cx.root + "/_a/f/"
    paths = [("notice", "door_notice"), ("in-it-now", "door_in_it_now"), ("worried-about-someone", "door_worried"),
             ("before-you-sign", "door_sign"), ("patterns", "browse_patterns"), ("tactics", "browse_tactics"),
             ("method", "method_link"), ("take-it-with-you", "take_link"), ("a-z", "az_h")]
    foot_links = "".join('<li><a href="%s">%s</a></li>' % (cx.u(p), esc(S(k))) for p, k in paths)
    chap = cx.links["fractal"]["chapter"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="{esc(S('site'))} · {esc(S('publisher'))}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{O}{cx.u('og/' + og + '.png')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{f}newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{f}hanken.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#0B0C0F" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#F5F0E6" media="(prefers-color-scheme: light)">
<script>document.documentElement.className+=' js'</script>
<style>{css(cx)}</style>
<script type="application/ld+json">{json.dumps(ld_all, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>
<body class="{cls}" data-search="{cx.root}/_a/d/{cx.sector}-search.json">
<a class="skip" href="#main">{esc(S('skip'))}</a>
{'<div class="progress" aria-hidden="true"><span></span></div>' if progress else ''}
<header class="top">
  <a class="mark" href="{cx.root}">{esc(S('site'))}</a>
  {switcher(cx)}
  <a class="sbtn" id="sbtn" href="{cx.u('a-z')}" aria-label="{esc(S('search_label'))}">{svg('search')}<span>{esc(S('search'))}</span></a>
  <button class="leave" id="leave" type="button" aria-label="{esc(S('leave_label'))}">{svg('leave')}<span>{esc(S('leave'))}</span></button>
</header>
<nav class="crumbs" aria-label="{esc(S('crumbs_label'))}">{crumb_html}</nav>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="foot-in">
  <nav aria-label="{esc(S('footer_paths'))}"><ul class="foot-links">{foot_links}</ul></nav>
  <ul class="foot-links foot-out">{f'<li><a href="{chap}">{esc(S("footer_fractal"))}</a></li>' if chap else ''}<li><a href="/playbook">{esc(S('footer_decoder'))}</a></li><li><a href="{cx.root}">{esc(S('site'))}</a></li></ul>
  <p class="foot-safety">{esc(S('footer_safety'))}</p>
  <p class="fine">{esc(S('footer_line', author=S('author'), publisher=S('publisher')))} · {esc(S('footer_version', version=cx.version, date=cx.date))} · <a href="{cx.u()}#updates">{esc(S('footer_updates'))}</a></p>
  </div>
</footer>
{search_dialog()}
<script>{(HERE / 'site.js').read_text()}</script>
{cx.house}
{cx.beacon}
</body>
</html>
"""


def article_ld(cx, name, desc, path, kind="Article", extra=None):
    O = CONFIG["origin"]
    o = {"@type": kind, "headline": name, "name": name, "description": desc, "url": O + cx.u(path),
         "inLanguage": "en", "dateModified": cx.date,
         "author": {"@type": "Person", "name": S("author")},
         "publisher": {"@type": "Organization", "name": S("publisher"), "url": O},
         "isPartOf": {"@type": "CollectionPage", "name": "%s: %s" % (S("site"), cx.title), "url": O + cx.u()}}
    o.update(extra or {})
    return o
