"""Tactic pages (NAV-SPEC 7) and the eight stage chapters (full entries, each headed by a link to its tactic page)."""
from lib import CONFIG, LEVELS, S, STAGE_INFO, clip, dot, esc, inline, plain, src
from frame import article_ld, frame
from pages_combo import LV_ICON


def levels_html(t, cls="levels"):
    lv = "".join('<div class="lv lv-%s"><h3 class="lvn">%s%s</h3>%s</div>' % (
        k, LV_ICON[k], lab, src("<p>%s</p>" % inline(t["examples"].get(key, ""))))
        for key, k, lab in LEVELS if t["examples"].get(key))
    return '<div class="%s">%s</div>' % (cls, lv)


def stage_tactics(cx, stage):
    return [t for t in cx.d["tactics"] if t["stage"] == stage]


def tactic_page(cx, t):
    stage = t["stage"]
    n = cx.stage_no(stage)
    ts = stage_tactics(cx, stage)
    i = ts.index(t)
    uses = cx.der["tactic_uses"].get(t["single_no"], [])
    rows = []
    for u in uses:
        if u["combo_id"] not in cx.live:
            continue
        pos = S("use_pos", pos=u["pos"], of=u["of"]) if u["pos"] else S("use_nopos")
        rows.append('<li><span class="meta">%s</span> %s</li>' % (esc(pos), cx.combo_link(u["combo_id"])))
    uses_html = '<ul class="plain uses">%s</ul>' % "".join(rows) if rows else '<p class="note">%s</p>' % esc(S("uses_none"))
    el = []
    dec = cx.links["tactics"].get(t["standard_id"], {}).get("decoder")
    if dec:
        el.append('<li><a href="%s">%s</a></li>' % (dec, esc(S("decoder_entry"))))
    fr = cx.links["fractal"]
    if fr["chapter"]:
        el.append('<li><a href="%s">%s</a></li>' % (fr["chapter"], esc(S("fractal_chapter", sector=cx.me["name"]))))
    fs = fr["stages"].get(stage, {})
    if fs.get("lens"):
        el.append('<li><a href="%s">%s</a></li>' % (fs["lens"], esc(S("fractal_lens"))))
    if fs.get("frequency"):
        el.append('<li><a href="%s">%s</a></li>' % (fs["frequency"], esc(S("fractal_freq"))))
    el.append('<li><a href="%s#%s">%s</a></li>' % (cx.stage_url(stage), t["anchor"], esc(S("back_stage"))))
    prv, nxt = (ts[i - 1] if i > 0 else None), (ts[i + 1] if i + 1 < len(ts) else None)
    pn = '<nav class="pn" aria-label="%s">%s%s</nav>' % (
        esc(cx.stage_name(stage)),
        '<a href="%s"><small>%s</small><b>%s</b></a>' % (cx.tactic_url(prv["single_no"]), esc(S("prev_stage_t")), esc(prv["name"])) if prv else "<span></span>",
        '<a class="nx" href="%s"><small>%s</small><b>%s</b></a>' % (cx.tactic_url(nxt["single_no"]), esc(S("next_stage_t")), esc(nxt["name"])) if nxt else "<span></span>")
    aka = '<p class="aka ui"><span class="kicker">%s</span> %s</p>' % (esc(S("also_called")), esc(t["also_called"].replace(";", ","))) if t.get("also_called") else ""
    body = f"""
<article class="tactic">
<header class="phead">
  <p class="kicker stage-k">{dot(n)}<a href="{cx.stage_url(stage)}">{esc(S('stage_of', n=n))} · {esc(cx.stage_name(stage))}</a></p>
  <h1>{esc(t['name'])}</h1>
  {src('<p class="def lede">%s</p>' % inline(t['definition']))}
  {aka}
</header>
<section id="levels" class="t-sec"><h2>{esc(S('levels_h'))}</h2>{levels_html(t)}</section>
<section id="patterns" class="t-sec"><h2>{esc(S('uses_h'))}</h2>{uses_html}</section>
<section id="elsewhere" class="t-sec"><h2>{esc(S('elsewhere_h'))}</h2><ul class="plain go">{''.join(el)}</ul></section>
{pn}
</article>"""
    desc = clip("%s: %s How it shows up %s, for a person, an organization and the culture." % (
        t["name"], plain(t["definition"]), cx.ph.get("in_industry", "")))
    O = CONFIG["origin"]
    ld = [article_ld(cx, t["name"], desc, "tactic/" + t["slug"], "DefinedTerm", {
        "termCode": t["standard_id"], "inDefinedTermSet": O + cx.stage_url(stage)})]
    ttl = "%s: a Manipulation Tactic in the %s · %s" % (t["name"], cx.ti, S("site"))
    if len(ttl) > 70:
        ttl = "%s · %s · %s" % (t["name"], cx.short, S("site"))
    return frame(cx, title=ttl, desc=desc, path="tactic/" + t["slug"],
                 crumbs=[(cx.short, cx.u()), (S("tactics_k"), cx.u("tactics")), (cx.stage_name(stage), cx.stage_url(stage)), (t["name"], None)],
                 body=body, ld=ld, og="stage-" + stage.lower(), cls="tactic-page")


def stage_page(cx, stage):
    d, i = cx.d, cx.stage_no(stage)
    ts = stage_tactics(cx, stage)
    chips = "".join('<li><a href="#%s">%s</a></li>' % (t["anchor"], esc(t["name"])) for t in ts)
    arts = []
    for t in ts:
        seen = [k for k in t["combos"] if k in cx.live]
        seen_html = ('<p class="seen ui"><span class="kicker">%s</span> %s</p>' % (esc(S("seen_in")), ", ".join(cx.combo_link(k) for k in seen))) if seen else ""
        aka = '<p class="aka ui"><span class="kicker">%s</span> %s</p>' % (esc(S("also_called")), esc(t["also_called"].replace(";", ","))) if t.get("also_called") else ""
        arts.append(f"""<article class="tac" id="{t['anchor']}">
  <p class="tno num">{dot(i)}{i}.{int(t['standard_id'].split('-')[-1])}</p>
  <h2><a href="{cx.tactic_url(t['single_no'])}">{esc(t['name'])}</a></h2>
  {src('<p class="def">%s</p>' % inline(t['definition']))}
  {aka}
  {levels_html(t)}
  {seen_html}
</article>""")
    prv = d["stages"][i - 2] if i > 1 else None
    nxt = d["stages"][i] if i < 8 else None
    pn = '<nav class="pn" aria-label="%s">%s%s</nav>' % (
        esc(S("home_stages_h")),
        '<a href="%s"><small>%s</small><b>%s</b></a>' % (cx.stage_url(prv), esc(S("prev_stage")), esc(cx.stage_name(prv))) if prv else "<span></span>",
        '<a class="nx" href="%s"><small>%s</small><b>%s</b></a>' % (cx.stage_url(nxt), esc(S("next_stage")), esc(cx.stage_name(nxt))) if nxt else "<span></span>")
    note = '<p class="note ui">%s</p>' % esc(S("stage_extract_note")) if stage == "CONTROL" else ""
    body = f"""
<header class="phead stage-head" style="--c:var(--s{i})">
  <p class="kicker">{dot(i)}{esc(S('stage_of', n=i))}</p>
  <h1>{esc(cx.stage_name(stage))}</h1>
  <p class="lede">{esc(STAGE_INFO[stage])} {esc(S('tactics_n', n=len(ts)))}, each shown in a person's life, inside an organization, and in the culture around it.</p>
  {note}
  <nav aria-label="{esc(S('tactics_n', n=len(ts)))}"><ul class="chips">{chips}</ul></nav>
</header>
<div class="tacs">{''.join(arts)}</div>
{pn}"""
    nm = cx.stage_name(stage)
    desc = clip("The %s stage of manipulation %s: %d tactics including %s, with examples for a person, an organization and the culture." % (
        nm, cx.ph.get("in_industry", ""), len(ts), ", ".join(t["name"] for t in ts[:3])))
    O = CONFIG["origin"]
    ld = [article_ld(cx, "%s: stage %d of 8" % (nm, i), desc, "stage-" + stage.lower(), "CollectionPage", {
        "hasPart": {"@type": "DefinedTermSet", "name": nm, "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": t["name"], "description": plain(t["definition"]), "termCode": t["standard_id"],
             "url": O + cx.tactic_url(t["single_no"])} for t in ts]}})]
    return frame(cx, title="%s Tactics in the %s (Stage %d of 8) · %s" % (nm, cx.ti, i, S("site")), desc=desc,
                 path="stage-" + stage.lower(),
                 crumbs=[(cx.short, cx.u()), (S("tactics_k"), cx.u("tactics")), (S("stage_of", n=i) + ": " + nm, None)],
                 body=body, ld=ld, og="stage-" + stage.lower(), cls="stage")
