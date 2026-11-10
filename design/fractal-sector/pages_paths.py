"""Reader paths, "What are you noticing?" and the living map (content/fractal2/NAV-SPEC.md sections 8 to 10).

Everything here is a view over the author's data. Indicators, tests and phrases are shown in the author's exact words
and always link back to the pattern they came from. Reader input never leaves the page and is never stored.
"""
import json
import math
import re

from frame import article_ld, frame
from lib import HERE, STAGE_INFO, S, clip, dot, esc, fam_name, plain, svg
from pages_index import H, safety_box, standards_html


# ---------- pulling parts out of a script (author's words, tags stripped) ----------
def indicators(c):
    return [plain(re.sub(r"^\s*[-*]\s+", "", l)) for l in c["sections"].get("Observable Indicators", "").split("\n") if re.match(r"\s*[-*]\s+\S", l)]


def cue_tests(c):
    """-> [(title, ask, concern)] from Recognition Cue Cards."""
    out = []
    for b in re.split(r"\n\s*\n", c["sections"].get("Recognition Cue Cards", "")):
        lines = [l.strip() for l in b.strip().split("\n") if l.strip()]
        m = lines and re.match(r"\*\*(?:SPOT IT\s*[—-]\s*)?(.+?):?\*\*:?$", lines[0])
        if not m:
            continue
        ask = next((plain(re.sub(r"^Ask:\s*", "", l)) for l in lines[1:] if l.startswith("Ask:")), "")
        con = next((plain(re.sub(r"^Concern rises if:\s*", "", l)) for l in lines[1:] if l.startswith("Concern rises if:")), "")
        if ask:
            out.append((plain(m.group(1)), ask, con))
    return out


def phrases(c):
    return [plain(re.sub(r"^\s*[-*]\s+", "", l)) for l in c["sections"].get("Safer Response Language", "").split("\n") if re.match(r"\s*[-*]\s+\S", l)]


def order_key(cx, k):
    return (cx.rank.get(k, 99), re.sub(r"^the\s+", "", cx.combos[k]["name"].lower()))


def page_js(name):
    return "<script>%s</script>" % (HERE / name).read_text()


# ---------- what are you noticing? ----------
def notice_page(cx):
    data, n_ind = [], 0
    for k in sorted(cx.live, key=lambda k: order_key(cx, k)):
        c = cx.combos[k]
        ind = indicators(c)
        n_ind += len(ind)
        data.append({"n": c["name"], "u": cx.combo_url(k), "f": fam_name(cx.cats[c["category_id"]]), "s": cx.der["combos"][k]["settings"], "i": ind,
                     "sf": 1 if c["has_safety_note"] else 0})
    chips = "".join('<button type="button" class="chip" data-set="%s" aria-pressed="false">%s</button>' % (s["key"], esc(s["label"])) for s in cx.der["settings"])
    fallback = "".join('<li><a class="door" href="%s?setting=%s"><span>%s</span><span class="meta num">%s</span></a></li>' % (
        cx.u("patterns"), s["key"], esc(s["label"]), esc(S("patterns_n", n=s["n"]))) for s in cx.der["settings"])
    body = f"""<header class="phead"><p class="kicker">{esc(S('notice_k'))}</p><h1>{esc(S('notice_h'))}</h1>
<p class="lede">{esc(S('notice_lede2'))}</p><p class="ui meta">{esc(S('notice_private'))}</p></header>
{safety_box()}
<div id="nt" class="nt" data-strings='{esc(json.dumps({k: S(k) for k in ("nt_none", "nt_more", "nt_match", "nt_signs", "nt_pick", "nt_quick", "nt_full", "nt_shown", "nt_safety")}))}' hidden>
  <section class="nt-step" aria-labelledby="nt1"><h2 id="nt1"><span class="num">1</span> {esc(S('nt_step1'))}</h2>
    <div class="chips" role="group" aria-label="{esc(S('nt_step1'))}">{chips}</div>
    <label class="filter"><span>{esc(S('nt_word'))}</span><input id="nt-q" type="search" autocomplete="off" spellcheck="false" placeholder="{esc(S('nt_word_ph'))}"></label>
  </section>
  <section class="nt-step" aria-labelledby="nt2"><h2 id="nt2"><span class="num">2</span> {esc(S('nt_step2'))}</h2>
    <p class="ui meta" id="nt-count" aria-live="polite"></p>
    <ul class="nt-list" id="nt-list"></ul>
    <p><button type="button" class="btn" id="nt-more" hidden>{esc(S('nt_more'))}</button> <button type="button" class="btn" id="nt-clear" hidden>{esc(S('nt_clear'))}</button></p>
  </section>
  <section class="nt-step" aria-labelledby="nt3"><h2 id="nt3"><span class="num">3</span> {esc(S('nt_step3'))}</h2>
    <p class="nt-caveat">{esc(S('nt_caveat'))}</p>
    <ol class="nt-res" id="nt-res" aria-live="polite"></ol>
  </section>
</div>
<section id="nt-fallback"><h2>{esc(S('nt_fallback_h'))}</h2><ul class="doors">{fallback}</ul></section>
<p class="ui"><a class="go-link" href="{cx.u('in-it-now')}">{esc(S('door_in_it_now'))}</a></p>
<script type="application/json" id="nt-data">{json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')}</script>
{page_js('notice.js')}"""
    desc = clip("Tick the signs you recognise, in the author's own words, and see which manipulation patterns %s share them. Private: nothing is stored or sent." % cx.ph.get("in_industry", ""))
    return frame(cx, title="What Are You Noticing? · %s · %s" % (cx.short, S("site")), desc=desc, path="notice",
                 crumbs=H(cx) + [(S("notice_k"), None)], body=body, ld=[article_ld(cx, S("notice_k"), desc, "notice")], cls="notice")


# ---------- in it now ----------
def in_it_now_page(cx):
    stages = cx.d["stages"]
    by_stage = {s: [] for s in stages}
    for k in cx.live:
        seen = {}
        for e in cx.chain(k):
            if e.get("single_no"):
                st = cx.tactics[e["single_no"]]["stage"]
                seen[st] = seen.get(st, 0) + 1
        for st, n in seen.items():
            by_stage[st].append((cx.rank.get(k, 99), -n, cx.combos[k]["name"], k))
    rows = []
    for i, s in enumerate(stages):
        nxt = stages[i + 1] if i + 1 < len(stages) else None
        pats = "".join("<li>%s</li>" % cx.combo_link(k, None, "#quick") for _, _, _, k in sorted(by_stage[s])[:8])
        nxt_html = ('<p class="nx-h">%s</p><p><b>%s.</b> %s <a href="%s">%s</a></p>' % (
            esc(S("inn_next")), esc(cx.stage_name(nxt)), esc(STAGE_INFO[nxt]), cx.stage_url(nxt), esc(S("inn_read_stage")))) if nxt else '<p class="nx-h">%s</p><p>%s</p>' % (esc(S("inn_next")), esc(S("inn_after_replace")))
        rows.append(f"""<li style="--c:var(--s{i + 1})"><details><summary><span class="num">{i + 1:02d}</span> <b>{esc(cx.stage_name(s))}</b><small>{esc(STAGE_INFO[s])}</small></summary>
<div class="st-open">{nxt_html}<p class="nx-h">{esc(S('inn_live_here'))}</p><ul class="plain">{pats}</ul></div></details></li>""")
    ten = "".join('<li><b>%s</b> <span class="ui"><a href="%s#words-you-could-use">%s</a> · <a href="%s#when-to-get-help-and-where">%s</a> · <a href="%s#quick">%s</a></span></li>' % (
        esc(t["name"]), cx.combo_url(t["combo_id"]), esc(S("inn_words")), cx.combo_url(t["combo_id"]), esc(S("inn_help")), cx.combo_url(t["combo_id"]), esc(S("quick_link")))
        for t in cx.d["top10"] if t["combo_id"] in cx.live)
    body = f"""<header class="phead"><p class="kicker">{esc(S('inn_k'))}</p><h1>{esc(S('inn_h'))}</h1></header>
{safety_box(True)}
<p class="ui">{esc(S('inn_leave'))}</p>
<div class="prose-ui">{standards_html(cx, ['Escalation Tiers For This Sector'], 'h2')}</div>
<section><h2>{esc(S('inn_stages'))}</h2><p>{esc(S('inn_stages_d2'))}</p><ol class="stage-strip open">{''.join(rows)}</ol></section>
<section><h2>{esc(S('inn_ten'))}</h2><ol class="plain big-list">{ten}</ol></section>
<p class="ui"><a class="go-link" href="{cx.u('notice')}">{esc(S('door_notice'))}</a></p>"""
    desc = clip("If you are inside a manipulative situation %s now: safety first, what tends to come next, words you could use and when to get help." % cx.ph.get("in_industry", ""))
    return frame(cx, title="If You Are in It Now · %s · %s" % (cx.short, S("site")), desc=desc, path="in-it-now",
                 crumbs=H(cx) + [(S("inn_k"), None)], body=body, ld=[article_ld(cx, S("inn_k"), desc, "in-it-now")], cls="path")


# ---------- worried about someone ----------
def worried_page(cx):
    pick = [k for k in cx.live if cx.combos[k]["has_safety_note"] or k in cx.rank]
    order = [s for s in cx.der["settings"]]
    order.sort(key=lambda s: 0 if s["key"] == cx.nav.get("young_setting", "young") else 1)
    groups = []
    for s in order:
        ks = sorted([k for k in pick if s["key"] in cx.der["combos"][k]["settings"]], key=lambda k: order_key(cx, k))
        if not ks:
            continue
        items = "".join('<li><p class="w-n">%s</p><ul>%s</ul></li>' % (cx.combo_link(k), "".join("<li>%s</li>" % esc(x) for x in indicators(cx.combos[k])[:3])) for k in ks)
        groups.append('<details class="w-g"><summary><b>%s</b> <span class="meta num">%s</span></summary><ul class="w-list">%s</ul></details>' % (
            esc(s["label"]), esc(S("patterns_n", n=len(ks))), items))
    body = f"""<header class="phead"><p class="kicker">{esc(S('worried_k'))}</p><h1>{esc(S('worried_h'))}</h1>
<p class="lede">{esc(S('worried_lede'))}</p></header>
{safety_box()}
<section><h2>{esc(S('worried_see_h'))}</h2><p>{esc(S('worried_see_d'))}</p>{''.join(groups)}</section>
<div class="prose-ui">{standards_html(cx, ['Universal Benign Explanations', 'Concern Strengthens When', 'Concern Weakens When'], 'h2')}</div>
<section><h2>{esc(S('worried_do_h'))}</h2><ul class="plain big-list"><li>{esc(S('worried_do_1'))}</li><li>{esc(S('worried_do_2'))}</li><li>{esc(S('worried_do_3'))}</li></ul></section>"""
    desc = clip("Worried about someone %s? Signs you can see from outside, the ordinary explanations to rule out first, and what makes concern grow." % cx.ph.get("in_industry", ""))
    return frame(cx, title="If You Are Worried About Someone · %s · %s" % (cx.short, S("site")), desc=desc, path="worried-about-someone",
                 crumbs=H(cx) + [(S("worried_k"), None)], body=body, ld=[article_ld(cx, S("worried_k"), desc, "worried-about-someone")], cls="path")


# ---------- before you sign ----------
def sign_page(cx):
    ks = sorted([k for k in cx.live if {"signing", "money"} & set(cx.der["combos"][k]["settings"])], key=lambda k: order_key(cx, k))
    cards = []
    for k in ks:
        c = cx.combos[k]
        tests = "".join('<li><b>%s.</b> %s%s</li>' % (esc(t), esc(a), (' <span class="meta">%s %s</span>' % (esc(S("sign_concern")), esc(cn))) if cn else "") for t, a, cn in cue_tests(c)[:2])
        ph = phrases(c)
        cards.append(f"""<li class="s-card"><h3>{('<span class="num rk-s">%02d</span> ' % cx.rank[k]) if k in cx.rank else ''}{cx.combo_link(k, None, '#quick')}</h3>
<p class="meta ui">{esc(fam_name(cx.cats[c['category_id']]))}</p>
{'<ul class="s-tests">' + tests + '</ul>' if tests else ''}
{'<p class="s-say"><span class="meta ui">%s</span> %s</p>' % (esc(S('sign_say')), esc(ph[0])) if ph else ''}</li>""")
    body = f"""<header class="phead"><p class="kicker">{esc(S('sign_k'))}</p><h1>{esc(S('sign_h'))}</h1>
<p class="lede">{esc(S('sign_lede'))}</p></header>
{safety_box()}
<section><h2>{esc(S('patterns_n', n=len(ks)))}</h2><p class="ui meta">{esc(S('sign_note'))}</p><ol class="s-cards">{''.join(cards)}</ol></section>
<div class="prose-ui">{standards_html(cx, ['Universal Evidence To Preserve'], 'h2')}</div>"""
    desc = clip("About to sign something %s? The patterns that live in contracts and money, two tests for each, words you could use, and what to keep." % cx.ph.get("in_industry", ""))
    return frame(cx, title="Before You Sign · %s · %s" % (cx.short, S("site")), desc=desc, path="before-you-sign",
                 crumbs=H(cx) + [(S("sign_k"), None)], body=body, ld=[article_ld(cx, S("sign_k"), desc, "before-you-sign")], cls="path")


# ---------- the living map ----------
def map_layout(cx):
    """Positions in a 1000 x 1000 box. Tactics on a ring in eight stage arcs; combos inside, clustered by family."""
    stages, tactics = cx.d["stages"], cx.d["tactics"]
    gap, total = 0.05, len(tactics)
    span_all = 2 * math.pi - gap * len(stages)
    pos, arcs, a = {}, [], -math.pi / 2
    for s in stages:
        ts = [t for t in tactics if t["stage"] == s]
        span = span_all * len(ts) / total
        for j, t in enumerate(ts):
            th = a + gap / 2 + (j + 0.5) / len(ts) * span
            r = 452 if j % 2 else 432                       # two lanes so 335 dots do not touch
            pos[t["single_no"]] = (500 + r * math.cos(th), 500 + r * math.sin(th))
        mid = a + gap / 2 + span / 2
        arcs.append((s, a + gap / 2, a + gap / 2 + span, mid))
        a += span + gap
    cpos, fam_lab = {}, []
    cats = cx.d["categories"]
    for i, cat in enumerate(cats):
        th = -math.pi / 2 + i * 2 * math.pi / len(cats)
        cx0, cy0 = 500 + 250 * math.cos(th), 500 + 250 * math.sin(th)
        ks = [k for k in cat["combos"] if k in cx.live]
        for j, k in enumerate(ks):
            rr, an = 13.5 * math.sqrt(j + 0.6), j * 2.39996
            cpos[k] = (cx0 + rr * math.cos(an), cy0 + rr * math.sin(an))
        fam_lab.append((fam_name(cat), 500 + 250 * math.cos(th), 500 + 250 * math.sin(th), len(ks)))
    return pos, arcs, cpos, fam_lab


def map_page(cx):
    T = cx.tactics
    pos, arcs, cpos, fam_lab = map_layout(cx)
    tl = lambda no: '<a href="%s">%s</a>' % (cx.tactic_url(no), esc(T[no]["name"]))
    top = "".join('<tr><td>%s</td><td>%s%s</td><td class="num">%d</td></tr>' % (
        tl(x["single_no"]), dot(cx.stage_no(T[x["single_no"]]["stage"])), esc(cx.stage_name(T[x["single_no"]]["stage"])), x["n"])
        for x in cx.der["map"]["top_tactics"])
    pairs = "".join('<tr><td>%s <span class="meta">%s</span> %s</td><td class="num">%d</td><td>%s</td></tr>' % (
        tl(p["a"]), esc(S("map_then")), tl(p["b"]), len(p["combos"]), ", ".join(cx.combo_link(k) for k in p["combos"]))
        for p in cx.der["map"]["pairs"])
    tnos = [t["single_no"] for t in cx.d["tactics"]]
    tix = {no: i for i, no in enumerate(tnos)}
    cks = sorted(cx.live, key=lambda k: (cx.combos[k]["category_id"], re.sub(r"^the\s+", "", cx.combos[k]["name"].lower())))
    data = {"t": [[T[no]["name"], cx.tactic_url(no), cx.stage_no(T[no]["stage"]), round(pos[no][0], 1), round(pos[no][1], 1)] for no in tnos],
            "c": [[cx.combos[k]["name"], cx.combo_url(k), fam_name(cx.cats[cx.combos[k]["category_id"]]), round(cpos[k][0], 1), round(cpos[k][1], 1),
                   [tix.get(e.get("single_no"), -1) for e in cx.chain(k)], [e["name"] for e in cx.chain(k)]] for k in cks],
            "stages": [cx.stage_name(s) for s in cx.d["stages"]]}
    dots_t = "".join('<circle class="mt s%d" cx="%.1f" cy="%.1f" r="4.2"/>' % (cx.stage_no(T[no]["stage"]), pos[no][0], pos[no][1]) for no in tnos)
    dots_c = "".join('<circle class="mc" cx="%.1f" cy="%.1f" r="5.2"/>' % cpos[k] for k in cks)
    arc_l = "".join('<text class="ml s%d" x="%.1f" y="%.1f" text-anchor="middle">%d</text>' % (
        i + 1, 500 + 487 * math.cos(mid), 500 + 487 * math.sin(mid) + 7, i + 1) for i, (s, a0, a1, mid) in enumerate(arcs))
    opt_c, cur = [], None
    for i, k in enumerate(cks):
        f = fam_name(cx.cats[cx.combos[k]["category_id"]])
        if f != cur:
            opt_c.append(("</optgroup>" if cur else "") + '<optgroup label="%s">' % esc(f)); cur = f
        opt_c.append('<option value="%d">%s</option>' % (i, esc(cx.combos[k]["name"])))
    opt_c.append("</optgroup>")
    opt_t = "".join('<optgroup label="%s">%s</optgroup>' % (esc("%d. %s" % (cx.stage_no(s), cx.stage_name(s))),
                    "".join('<option value="%d">%s</option>' % (tix[t["single_no"]], esc(t["name"])) for t in cx.d["tactics"] if t["stage"] == s)) for s in cx.d["stages"])
    legend = "".join('<li>%s<span class="num">%d</span> %s</li>' % (dot(i + 1), i + 1, esc(cx.stage_name(s))) for i, s in enumerate(cx.d["stages"]))
    body = f"""<header class="phead"><p class="kicker">{esc(S('map_k'))}</p><h1>{esc(S('map_h'))}</h1>
<p class="lede">{esc(S('map_lede2'))}</p></header>
<div id="map-stage" class="mapw">
  <div class="map-ctl" hidden id="map-ctl">
    <label class="filter"><span>{esc(S('map_pick_c'))}</span><select id="map-c"><option value="">{esc(S('map_choose'))}</option>{''.join(opt_c)}</select></label>
    <label class="filter"><span>{esc(S('map_pick_t'))}</span><select id="map-t"><option value="">{esc(S('map_choose'))}</option>{opt_t}</select></label>
  </div>
  <div class="map-grid">
    <figure class="map-fig">
      <svg id="map" viewBox="0 0 1000 1000" role="img" aria-labelledby="map-title map-desc" tabindex="-1">
        <title id="map-title">{esc(S('map_h'))}</title>
        <desc id="map-desc">{esc(S('map_desc', t=len(tnos), c=len(cks)))}</desc>
        <g class="g-t">{dots_t}</g><g class="g-c">{dots_c}</g><g class="g-l" aria-hidden="true">{arc_l}</g>
        <g id="map-path" aria-hidden="true"></g>
      </svg>
      <figcaption class="ui meta">{esc(S('map_caption'))}</figcaption>
    </figure>
    <div class="map-side">
      <div class="map-panel" id="map-panel" aria-live="polite"><p class="ui">{esc(S('map_hint'))}</p></div>
      <ol class="map-legend ui" aria-label="{esc(S('map_legend'))}">{legend}</ol>
    </div>
  </div>
</div>
<section><h2>{esc(S('map_top'))}</h2><div class="tbl"><table><thead><tr><th scope="col">Tactic</th><th scope="col">Stage</th><th scope="col">Patterns</th></tr></thead><tbody>{top}</tbody></table></div></section>
<section><h2>{esc(S('map_pairs'))}</h2><div class="tbl"><table><thead><tr><th scope="col">Pair, in order</th><th scope="col">Patterns</th><th scope="col">Where</th></tr></thead><tbody>{pairs}</tbody></table></div></section>
<script type="application/json" id="map-data">{json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')}</script>
<script type="application/json" id="map-str">{json.dumps({k: S(k) for k in ("map_step", "map_uses", "map_not_on", "map_open", "map_prev", "map_next", "map_clear", "map_seq", "map_stage", "map_none_uses")})}</script>
{page_js('map.js')}"""
    desc = clip("An interactive map of %d tactics and %d patterns %s: pick a pattern to see its sequence drawn in order, or a tactic to see every pattern that uses it." % (len(tnos), len(cks), cx.ph.get("in_industry", "")))
    return frame(cx, title="The Map: How Sequences Recur · %s · %s" % (cx.short, S("site")), desc=desc, path="map",
                 crumbs=H(cx) + [(S("map_k"), None)], body=body, ld=[article_ld(cx, S("map_h"), desc, "map", "CollectionPage")], cls="map")
