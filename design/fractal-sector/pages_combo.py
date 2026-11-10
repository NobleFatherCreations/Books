"""A combo page (NAV-SPEC 6): one document, three reading modes over the same words (no text duplicated)."""
import re

from lib import (CONFIG, S, STATE_NAME, STATE_NOTE, TAG_LABEL, blocks, clip, dot, esc, fam_name, first_sentence, inline,
                 md, slugify, src, svg)
from frame import article_ld, frame

Q, SQ, F = "quick", "seq", "full"
# (source heading, reader heading, modes it shows in). Safety note is always first and in every mode.
COMBO_ORDER = [
    ("Cold Open", "The scene", {F}), ("The Name", None, {F}), ("Definition", "What it is", {Q, F}),
    ("Verbal Breakdown", "The tactics, in order", {Q, SQ, F}), ("Why This Order", "Why this order", {SQ, F}),
    ("LEVELS", "One pattern, three altitudes", {F}),
    ("Observable Indicators", "What you might notice", {F}), ("Recognition Cue Cards", "Spot it", {Q, F}),
    ("False-Positive Check — Specific", "Before you read too much into it", {F}),
    ("Evidence To Preserve — Additions", "What to keep", {F}), ("Chain Breakers", "What breaks the chain", {Q, F}),
    ("Escalation Triggers — Specific", "When to get help, and where", {Q, F}),
    ("Safer Response Language", "Words you could use", {Q, F}), ("Reflection", None, {F}),
]
WAY_OUT = {"Chain Breakers", "Safer Response Language"}
LV_ICON = {
    "ind": '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="5" fill="currentColor"/></svg>',
    "inst": '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="10" cy="10" r="3.5" fill="currentColor"/></svg>',
    "civ": '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="10" cy="10" r="5.5" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="10" cy="10" r="2.2" fill="currentColor"/></svg>',
}


def m_attr(modes):
    return ' data-m="%s"' % " ".join(m for m in (Q, SQ, F) if m in modes)


def chain_item_href(cx, e):
    if e["single_no"]:
        return cx.tactic_url(e["single_no"])
    if e.get("pattern"):
        return e["pattern"]["url"]
    return None


def chain_html(cx, c):
    out = []
    for e in cx.chain(c["combo_id"]):
        if e["single_no"]:
            t = cx.tactics[e["single_no"]]
            n = cx.stage_no(t["stage"])
            out.append('<li>%s<a href="%s">%s</a><span class="ch-s">stage %d</span></li>' % (
                dot(n), cx.tactic_url(t["single_no"]), esc(e["name"]), n))
        elif e.get("pattern"):
            out.append('<li><span class="sd sd-o" aria-hidden="true"></span><a href="%s">%s</a><span class="ch-s">%s</span></li>' % (
                e["pattern"]["url"], esc(e["name"]), esc(S("footer_decoder"))))
        else:
            out.append('<li><span class="sd sd-o" aria-hidden="true"></span>%s</li>' % esc(e["name"]))
    return '<ol class="chain" aria-label="%s">%s</ol>' % (esc(S("chain_label")), "".join(out))


def levels_block(c):
    st = c["review_state"]
    parts = []
    for key, k, lab in [("Individual Level", "ind", "Individual"), ("Institutional Echo", "inst", "Institutional"),
                        ("Civilizational Echo", "civ", "Civilizational")]:
        if c["sections"].get(key):
            parts.append('<div class="lv lv-%s"><h3 class="lvn">%s%s</h3>%s</div>' % (k, LV_ICON[k], lab, src(md(c["sections"][key], st))))
    return '<div class="levels big">%s</div>' % "".join(parts)


def cue_cards(text, st):
    cards = []
    for b in blocks(text):
        lines = b.split("\n")
        m = re.match(r"\*\*(.+?):?\*\*:?\s*$", lines[0])
        if m:
            cards.append('<div class="cue"><h3>%s</h3>%s</div>' % (
                inline(m.group(1).rstrip(":"), st), src("".join("<p>%s</p>" % inline(l, st) for l in lines[1:]))))
        else:
            cards.append(src(md(b, st)))
    return '<div class="cues" data-src>%s</div>' % "".join(cards)


def escalation(text, st):
    out = []
    for b in blocks(text):
        m = re.match(r"\*\*(.+?):\*\*\s*(.*)", b, re.S)
        if m and "→" in m.group(1):
            lvl = m.group(1).split("→")[-1].strip().lower()
            out.append('<div class="esc esc-%s"><p class="esc-h">%s</p><p>%s</p></div>' % (
                slugify(lvl), inline(m.group(1), st), inline(m.group(2), st)))
        else:
            out.append(md(b, st))
    return '<div class="escs" data-src>%s</div>' % "".join(out)


def breakdown(cx, c, st):
    """Link each tactic name at the start of a numbered item (resolved ids only), and mark items as steps."""
    h = md(c["sections"]["Verbal Breakdown"], st)
    for e in cx.chain(c["combo_id"]):
        href = chain_item_href(cx, e)
        if href:
            nm = esc(e["name"])
            h = h.replace("<li><strong>%s</strong>" % nm, '<li><strong><a href="%s">%s</a></strong>' % (href, nm), 1)
    h = re.sub(r"</ol>\s*<ol>", "", h)   # the scripts put a blank line between items: one list, numbered 1..n
    h = h.replace("<ol>", '<ol class="steps">', 1)
    return h


def combo_page(cx, c):
    d, st = cx.d, c["review_state"]
    cat = cx.cats[c["category_id"]]
    fam = fam_name(cat)
    der = cx.der["combos"][c["combo_id"]]
    Sx = c["sections"]
    toc, parts = [], []
    if c["has_safety_note"]:
        parts.append('<aside class="safety" id="safety" role="note" aria-labelledby="safety-h"%s>'
                     '<p class="safety-h" id="safety-h">%s %s</p>%s</aside>' % (
                         m_attr({Q, SQ, F}), svg("alert"), esc(S("read_first")), src(md(Sx["Safety Note (read first)"], st))))
    for key, head, modes in COMBO_ORDER:
        ma = m_attr(modes)
        if key == "LEVELS":
            parts.append('<section id="levels"%s><h2>%s</h2>%s</section>' % (ma, head, levels_block(c)))
            toc.append(("levels", head, modes))
            continue
        if not Sx.get(key):
            continue
        sid = slugify(head or key)
        if key == "Cold Open":
            inner = src(md(Sx[key], st, first_cls="first"), "scene")
        elif key == "The Name":
            parts.append('<p class="name-line"%s data-src>%s</p>' % (ma, inline(Sx[key], st)))
            continue
        elif key == "Reflection":
            parts.append('<blockquote class="reflect"%s data-src>%s</blockquote>' % (ma, inline(" ".join(blocks(Sx[key])), st)))
            continue
        elif key == "Verbal Breakdown":
            inner = '<div class="stepper-mount"></div>' + src(breakdown(cx, c, st), "breakdown")
        elif key == "Recognition Cue Cards":
            inner = cue_cards(Sx[key], st)
        elif key == "Escalation Triggers — Specific":
            inner = escalation(Sx[key], st)
        else:
            inner = src(md(Sx[key], st))
        cls = ' class="way-out"' if key in WAY_OUT else ""
        parts.append('<section id="%s"%s%s><h2>%s</h2>%s</section>' % (sid, cls, ma, esc(head), inner))
        toc.append((sid, head, modes))
    body_html = "\n".join(parts)

    chain = cx.chain(c["combo_id"])
    tac = "".join('<li>%s</li>' % ('<a href="%s">%s</a>' % (chain_item_href(cx, e), esc(e["name"])) if chain_item_href(cx, e) else esc(e["name"]))
                  for e in chain)
    lives = [k for k in cat["combos"] if k in cx.live]
    sib = [k for k in lives if k != c["combo_id"]][:6]
    cross = [x for x in cx.cross.get(c["combo_id"], []) if x.get("sector") != d["sector"]]
    cross_html = ('<section class="aside-sec"><h2>%s</h2><ul class="plain">%s</ul></section>' % (
        esc(S("other_sectors")), "".join('<li><a href="%s">%s</a></li>' % (esc(x["url"]), esc(x["title"])) for x in cross))) if cross else ""
    shared = [x for x in der["shared"] if x["combo_id"] in cx.live]
    shared_html = ('<section class="aside-sec"><h2>%s</h2><ul class="plain">%s</ul></section>' % (
        esc(S("shares_tactics")), "".join('<li>%s <span class="meta">%s</span></li>' % (
            cx.combo_link(x["combo_id"]), esc(S("shares_n", n=x["n"]))) for x in shared))) if shared else ""
    toc_html = "".join('<li%s><a href="#%s">%s</a></li>' % (m_attr(m), i, esc(h)) for i, h, m in toc)
    i = lives.index(c["combo_id"])
    prv, nxt = (lives[i - 1] if i > 0 else None), (lives[i + 1] if i + 1 < len(lives) else None)
    pn = '<nav class="pn" aria-label="%s">%s%s</nav>' % (
        esc(fam),
        '<a href="%s"><small>%s</small><b>%s</b></a>' % (cx.combo_url(prv), esc(S("prev_family")), esc(cx.combos[prv]["name"])) if prv else "<span></span>",
        '<a class="nx" href="%s"><small>%s</small><b>%s</b></a>' % (cx.combo_url(nxt), esc(S("next_family")), esc(cx.combos[nxt]["name"])) if nxt else "<span></span>")
    modes = "".join('<button type="button" data-mode="%s" aria-pressed="%s">%s</button>' % (m, "true" if m == F else "false", esc(S(k)))
                    for m, k in ((Q, "mode_quick"), (SQ, "mode_seq"), (F, "mode_full")))
    body = f"""
<article class="combo" id="combo" data-mode="full" data-step="{esc(S('step_of', n='{n}', total='{total}'))}" data-prev="{esc(S('prev'))}" data-next="{esc(S('next'))}" data-play="{esc(S('play'))}" data-pause="{esc(S('pause'))}" data-mode-seq="{esc(S('mode_seq'))}">
<header class="phead">
  <p class="kicker"><a href="{cx.u('family-' + cat['slug'])}">{esc(fam)}</a> · {esc(S('tactics_n', n=len(chain)))}</p>
  <h1>{esc(c['name'])}</h1>
  <p class="sub">{esc(cx.ph.get('in_industry', ''))}</p>
  {chain_html(cx, c)}
  <p class="times ui">{esc(S('min_quick', n=der['quick_min']))} · {esc(S('min_full', n=der['full_min']))}</p>
  <p class="state state-{st} ui"><span class="chip">{STATE_NAME[st]}</span> {esc(STATE_NOTE[st])} <a href="#labels">{esc(S('labels_h'))}</a></p>
</header>
<div class="modes" role="group" aria-label="{esc(S('mode_label'))}">{modes}</div>
<p class="print-only print-safety">{esc(S('safety_line'))}<br>{esc(S('print_from', url=CONFIG['origin'] + cx.u(c['slug']), date=cx.date))}</p>
<div class="combo-grid">
<aside class="toc"><details open><summary>{esc(S('on_page'))}</summary><ol>{toc_html}<li><a href="#tactics">{esc(S('tactics_in_it'))}</a></li></ol></details></aside>
<div class="combo-body">
{body_html}
<section id="tactics" class="aside-sec"><h2>{esc(S('tactics_in_it'))}</h2><ol class="plain">{tac}</ol></section>
{cross_html}
{shared_html}
<section class="aside-sec"><h2>{esc(S('more_in', family=fam))}</h2><ul class="plain">{''.join('<li>%s</li>' % cx.combo_link(k) for k in sib)}</ul></section>
<section id="labels" class="aside-sec legend"><h2>{esc(S('labels_h'))}</h2>
<p><span class="tg tg-composite">Composite</span> a made-up example built from common situations; no real person is described.
<span class="tg tg-pattern">Common pattern</span> widely reported in the industry, not a claim about any one company.
<span class="tg tg-legal">Varies by place</span> law and contract practice differ by country and state.
<span class="tg tg-review">{TAG_LABEL[('review', st)][0]}</span> and <span class="tg tg-source">{TAG_LABEL[('source', st)][0]}</span> show where checking stands.
<span class="slot">[X]</span> marks a blank for you to fill in.</p></section>
{pn}
</div></div>
</article>"""
    O = CONFIG["origin"]
    desc = clip("%s: %s" % (c["name"], first_sentence(c["definition"])))
    ld = [article_ld(cx, "%s %s" % (c["name"], cx.ph.get("in_industry", "")), desc, c["slug"], "Article", {
        "articleSection": fam, "wordCount": c["reader_words"],
        "about": [{"@type": "DefinedTerm", "name": e["name"], "url": O + cx.tactic_url(e["single_no"])} for e in chain if e["single_no"]]})]
    ttl = "%s: Signs in the %s and What to Do · %s" % (c["name"], cx.ti, S("site"))
    if len(ttl) > 70:
        ttl = "%s: Signs in the %s · %s" % (c["name"], cx.ti, S("site"))
    return frame(cx, title=ttl, desc=desc, path=c["slug"],
                 crumbs=[(cx.short, cx.u()), (fam, cx.u("family-" + cat["slug"])), (c["name"], None)],
                 body=body, ld=ld, og="family-" + cat["slug"], progress=True, cls="combo-page")
