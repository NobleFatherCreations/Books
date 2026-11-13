"""Sector home, start, patterns, tactics, families, method, take-it-with-you, a-z and the packet-02 stubs."""
import collections
import re

from lib import (CONFIG, S, STAGE_INFO, STATE_NAME, TAG_LABEL, V1_DATE, clip, dot, esc, fam_name, first_sentence, md,
                 plain, slugify, src, svg)
from frame import ring, article_ld, frame

SCORES = [("likelihood", "score_likelihood"), ("harm", "score_harm"), ("hidden", "score_hidden"), ("recognition", "score_recognition")]


def H(cx):
    return [(cx.short, cx.u())]


def score_bars(t):
    return '<dl class="scores">%s</dl>' % "".join(
        '<div><dt>%s</dt><dd><span class="bar" aria-hidden="true"><span style="width:%d%%"></span></span><span class="num">%d<span class="vh"> out of 5</span><span aria-hidden="true">/5</span></span></dd></div>' % (
            esc(S(k)), t["scores"][s] * 20, t["scores"][s]) for s, k in SCORES)


def top_row(cx, t, rich=False):
    cid = t["combo_id"]
    extra = ""
    if rich:
        tests = "".join('<li><b>%s</b> %s</li>' % (esc(x["test"]), esc(x["cue"])) for x in t.get("spot_it", []))
        extra = '<ul class="plain tests ui">%s</ul>' % tests if tests else ""
    links = ""
    if cid in cx.live:
        links = '<p class="go-links ui"><a href="%s#quick">%s</a><a href="%s">%s</a></p>' % (
            cx.combo_url(cid), esc(S("quick_link")), cx.combo_url(cid), esc(S("full_link")))
    return ('<li class="top-row"><span class="rk num">%02d</span><div class="top-b"><h3>%s</h3><p>%s</p>%s%s%s</div></li>' % (
        t["rank"], cx.combo_link(cid, t["name"]), esc(plain(t["why_it_ranks"])), score_bars(t), extra, links))


def stage_band(cx):
    rows = []
    mx = max(sum(t["stage"] == s for t in cx.d["tactics"]) for s in cx.d["stages"])
    for i, s in enumerate(cx.d["stages"]):
        n = sum(t["stage"] == s for t in cx.d["tactics"])
        rows.append('<li style="--g:%d;--w:%d%%;--c:var(--s%d)"><a href="%s"><span class="sb-rule" aria-hidden="true"></span>'
                    '<span class="num sb-n">%02d</span><b>%s</b><span class="sb-c num">%s</span></a></li>' % (
                        n, round(n / mx * 100), i + 1, cx.stage_url(s), i + 1, esc(cx.stage_name(s)), esc(S("tactics_n", n=n))))
    return '<ol class="stage-band">%s</ol>' % "".join(rows)


def updates(cx):
    dates = {"v3": cx.date, "v2": "2026-11-10", "v1": V1_DATE}
    return ('<section class="updates" id="updates"><h2>%s</h2><p><span class="badge num">%s — %s</span></p><ul class="plain">%s</ul></section>' % (
        esc(S("updates_h")), cx.version, cx.date,
        "".join('<li><span class="num meta">%s · %s</span> %s</li>' % (v, dates[v], esc(S(k))) for v, k in [("v3", "updates_v3"), ("v2", "updates_v2"), ("v1", "updates_v1")])))


def home(cx):
    d = cx.d
    nt, npat = len(d["tactics"]), len(cx.live)
    doors = [("notice", "door_notice"), ("in-it-now", "door_in_it_now"), ("start", "door_start"),
             ("worried-about-someone", "door_worried"), ("before-you-sign", "door_sign"), ("method", "door_method")]
    doors_html = "".join('<li><a class="door" href="%s"><span>%s</span>%s</a></li>' % (cx.u(p), esc(S(k)), svg("arrow", 18)) for p, k in doors)
    top = "".join(top_row(cx, t) for t in d["top10"])
    browse = [("patterns", "browse_patterns", S("browse_patterns_d", n=npat)), ("tactics", "browse_tactics", S("browse_tactics_d", n=nt)),
              ("map", "browse_map", S("browse_map_d"))]
    browse_html = "".join('<li><a class="card" href="%s"><span class="num card-n">%02d</span><b>%s</b><small>%s</small></a></li>' % (
        cx.u(p), i + 1, esc(S(k)), esc(dd)) for i, (p, k, dd) in enumerate(browse))
    line = cx.ph.get("cover_line", "").format(tactics=nt, patterns=npat)
    from pages_paths import map_layout          # the same layout as the map page, drawn small as the cover figure
    pos, _arcs, cpos, _fl = map_layout(cx)
    mini = ''.join('<circle class="mt s%d" cx="%.0f" cy="%.0f" r="5"/>' % (cx.stage_no(t["stage"]), pos[t["single_no"]][0], pos[t["single_no"]][1]) for t in d["tactics"]) + \
           ''.join('<circle class="mc" cx="%.0f" cy="%.0f" r="6"/>' % cpos[k] for k in cpos)
    body = f"""
<section class="cover">
  <div class="cover-t">
  <p class="kicker">{esc(S('site'))} · Sector {cx.me['n']:02d} of {len(cx.reg['sectors'])}</p>
  <h1 class="display">{esc(cx.title)}</h1>
  <p class="lede">{esc(line)}</p>
  <dl class="figures">
    <div><dt>tactics</dt><dd class="num">{nt}</dd></div>
    <div><dt>patterns</dt><dd class="num">{npat}</dd></div>
    <div><dt>levels</dt><dd class="num">3</dd></div>
  </dl>
  </div>
  {ring(cx, big=True)}
</section>
<section class="band" aria-labelledby="doors-h">
  <h2 id="doors-h">{esc(S('home_doors_h'))}</h2>
  <ul class="doors">{doors_html}</ul>
</section>
<section class="band" id="start" aria-labelledby="start-h">
  <p class="kicker">{esc(S('home_start_k'))}</p><h2 id="start-h">{esc(S('home_start_h'))}</h2>
  <ol class="top10">{top}</ol>
  <p class="note ui">{esc(S('scores_note'))} {esc(d.get('top10_method', ''))}</p>
</section>
<section class="band" aria-labelledby="browse-h">
  <h2 id="browse-h">{esc(S('home_browse_h'))}</h2>
  <ul class="cards three">{browse_html}</ul>
</section>
<section class="band" id="stages" aria-labelledby="stages-h">
  <h2 id="stages-h">{esc(S('home_stages_h'))}</h2>
  {stage_band(cx)}
</section>
<section class="band" aria-labelledby="more-h">
  <h2 id="more-h">{esc(S('home_more_h'))}</h2>
  <ul class="cards two">
    <li><a class="card" href="{cx.u('take-it-with-you')}"><b>{esc(S('take_link'))}</b><small>{esc(S('take_link_d'))}</small></a></li>
    <li><a class="card" href="{cx.u('method')}"><b>{esc(S('method_link'))}</b><small>{esc(S('method_link_d'))}</small></a></li>
  </ul>
</section>
{updates(cx)}"""
    desc = clip("How manipulation and control work %s: %d tactics and %d patterns, with signs, what to keep and what to do." % (cx.ph.get("in_industry", ""), nt, npat))
    O = CONFIG["origin"]
    ld = [article_ld(cx, "%s: %s" % (S("site"), cx.title), desc, "", "CollectionPage", {
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": t["rank"], "url": O + cx.combo_url(t["combo_id"]), "name": t["name"]}
            for t in d["top10"] if t["combo_id"] in cx.live]}})]
    return frame(cx, title="Manipulation in the %s: Tactics, Patterns, What to Do · %s" % (cx.ti, S("site")),
                 desc=desc, path="", crumbs=[(cx.short, None)], body=body, ld=ld, og="home", cls="home")


def start_page(cx):
    top = "".join(top_row(cx, t, rich=True) for t in cx.d["top10"])
    body = f"""<header class="phead"><p class="kicker">{esc(S('start_k'))}</p><h1>{esc(S('start_h'))}</h1>
<p class="lede">{esc(S('start_lede'))}</p></header>
<ol class="top10 rich">{top}</ol>
<p class="note ui">{esc(S('scores_note'))} {esc(cx.d.get('top10_method', ''))}</p>"""
    desc = clip("The ten manipulation patterns most likely to cost people money, credit, years or safety %s, with how to spot each." % cx.ph.get("in_industry", ""))
    return frame(cx, title="The Ten Patterns That Matter Most in the %s · %s" % (cx.ti, S("site")), desc=desc, path="start",
                 crumbs=H(cx) + [(S("start_k"), None)], body=body, ld=[article_ld(cx, S("start_k"), desc, "start", "CollectionPage")], cls="start")


def pattern_row(cx, c):
    cat = cx.cats[c["category_id"]]
    der = cx.der["combos"][c["combo_id"]]
    chain = cx.chain(c["combo_id"])
    dots = "".join(dot(cx.stage_no(cx.tactics[e["single_no"]]["stage"])) if e["single_no"] else '<span class="sd sd-o" aria-hidden="true"></span>' for e in chain)
    fd = first_sentence(c["definition"])
    q = (c["name"] + " " + plain(c["definition"])).lower()
    return ('<li class="prow" data-fit="%s" data-fam="%s" data-set="%s" data-safety="%d" data-n="%d" data-rank="%d" data-name="%s" data-q="%s">'
            '<a class="prow-a" href="%s"><span class="prow-h"><b>%s</b>%s</span><span class="prow-f ui">%s</span><span class="prow-d">%s</span>'
            '<span class="prow-c ui"><span class="dots">%s</span>%s</span></a></li>') % (
        c["tier"], cat["slug"], " ".join(der["settings"]), c["has_safety_note"], len(chain), cx.rank.get(c["combo_id"], 99),
        esc(re.sub(r"^the\s+", "", c["name"].lower())), esc(q), cx.combo_url(c["combo_id"]), esc(c["name"]),
        ('<span class="smark ui">%s%s</span>' % (svg("alert", 14), esc(S("safety_mark")))) if c["has_safety_note"] else "",
        esc(fam_name(cat)), esc(clip(fd, 200)), dots, esc(S("tactics_n", n=len(chain))))


def patterns_page(cx):
    cs = sorted((cx.combos[k] for k in cx.live), key=lambda c: re.sub(r"^the\s+", "", c["name"].lower()))
    rows = "".join(pattern_row(cx, c) for c in cs)
    fams = "".join('<option value="%s">%s</option>' % (c["slug"], esc(fam_name(c))) for c in cx.d["categories"])
    sets = "".join('<option value="%s">%s (%d)</option>' % (s["key"], esc(s["label"]), s["n"]) for s in cx.der["settings"])
    n = len(cs)
    nsafe = sum(c["has_safety_note"] for c in cs)
    body = f"""<header class="phead"><p class="kicker">{esc(S('patterns_k'))}</p><h1>{esc(S('patterns_h'))}</h1>
<p class="lede">{esc(S('patterns_lede'))}</p></header>
<div class="pbar">
<details class="filters" id="filters"><summary class="btn">{svg('sliders', 16)}<span>{esc(S('filters'))}</span></summary>
<form id="pf" class="pf ui" role="search" onsubmit="return false">
  <label class="pf-q"><span>{esc(S('f_q'))}</span><input type="search" name="q" autocomplete="off"></label>
  <fieldset class="seg-f"><legend>{esc(S('f_fit'))}</legend>
    <label><input type="radio" name="fit" value="" checked><span>{esc(S('f_fit_all'))}</span></label>
    <label><input type="radio" name="fit" value="A"><span>{esc(S('f_fit_a'))}</span></label>
    <label><input type="radio" name="fit" value="B"><span>{esc(S('f_fit_b'))}</span></label>
    <p class="hint">{esc(S('f_fit_note'))}</p></fieldset>
  <label><span>{esc(S('f_family'))}</span><select name="family"><option value="">{esc(S('f_any'))}</option>{fams}</select></label>
  <label><span>{esc(S('f_setting'))}</span><select name="setting"><option value="">{esc(S('f_any'))}</option>{sets}</select></label>
  <label><span>{esc(S('f_n'))}</span><select name="n"><option value="">{esc(S('f_n_any'))}</option><option value="short">{esc(S('f_n_short'))}</option><option value="mid">{esc(S('f_n_mid'))}</option><option value="long">{esc(S('f_n_long'))}</option></select></label>
  <label><span>{esc(S('f_sort'))}</span><select name="sort"><option value="az">{esc(S('sort_az'))}</option><option value="family">{esc(S('sort_family'))}</option><option value="most">{esc(S('sort_most'))}</option><option value="ten">{esc(S('sort_ten'))}</option></select></label>
  <label class="pf-c"><input type="checkbox" name="safety" value="1"><span>{esc(S('f_safety'))} ({nsafe})</span></label>
  <button type="button" class="btn ghost" id="pf-reset">{esc(S('f_reset'))}</button>
</form></details>
<p class="count ui num" id="count" aria-live="polite">{esc(S('count', n=n, total=n))}</p>
</div>
<ul class="plist" id="plist" data-total="{n}" data-tpl="{esc(S('count', n='{n}', total='{total}'))}">{rows}</ul>
<p class="note" id="pnone" hidden>{esc(S('none_match'))}</p>"""
    desc = clip("All %d manipulation patterns %s: filter by setting, family, fit and safety note." % (n, cx.ph.get("in_industry", "")))
    return frame(cx, title="All %d Manipulation Patterns in the %s · %s" % (n, cx.ti, S("site")), desc=desc, path="patterns",
                 crumbs=H(cx) + [(S("patterns_k"), None)], body=body, ld=[article_ld(cx, S("patterns_h"), desc, "patterns", "CollectionPage")], cls="patterns")


def tactics_page(cx):
    secs = []
    for i, s in enumerate(cx.d["stages"]):
        ts = [t for t in cx.d["tactics"] if t["stage"] == s]
        lis = "".join('<li><a href="%s">%s</a></li>' % (cx.tactic_url(t["single_no"]), esc(t["name"])) for t in ts)
        secs.append(f"""<section class="t-stage" id="{s.lower()}" style="--c:var(--s{i + 1})">
<h2><a href="{cx.stage_url(s)}"><span class="num">{i + 1:02d}</span> {esc(cx.stage_name(s))}</a></h2>
<p class="ui meta">{dot(i + 1)}{esc(S('stage_of', n=i + 1))} · {esc(S('tactics_n', n=len(ts)))}</p>
<p>{esc(STAGE_INFO[s])}</p><ul class="cols">{lis}</ul></section>""")
    body = f"""<header class="phead"><p class="kicker">{esc(S('tactics_k'))}</p><h1>{esc(S('tactics_h'))}</h1>
<p class="lede">{esc(S('tactics_lede'))}</p>{ring(cx)}</header>{''.join(secs)}"""
    desc = clip("All %d manipulation tactics %s, in eight stages from first approach to replacement." % (len(cx.d["tactics"]), cx.ph.get("in_industry", "")))
    return frame(cx, title="All %d Manipulation Tactics in the %s, by Stage · %s" % (len(cx.d["tactics"]), cx.ti, S("site")), desc=desc,
                 path="tactics", crumbs=H(cx) + [(S("tactics_k"), None)], body=body, ld=[article_ld(cx, S("tactics_h"), desc, "tactics", "CollectionPage")], cls="tactics")


def family_page(cx, cat, idx):
    nm = fam_name(cat)
    cats = cx.d["categories"]
    cards = []
    for k in cat["combos"]:
        if k not in cx.live:
            continue
        c = cx.combos[k]
        cards.append('<li><a class="card" href="%s"><span class="num card-n">%02d</span><b>%s</b><small>%s</small><span class="meta ui">%s%s</span></a></li>' % (
            cx.combo_url(k), len(cards) + 1, esc(c["name"]), esc(clip(first_sentence(c["definition"]), 190)), esc(S("tactics_n", n=len(c["tactics"]))),
            " · " + esc(S("safety_mark")) if c["has_safety_note"] else ""))
    prv, nxt = (cats[idx - 1] if idx > 0 else None), (cats[idx + 1] if idx + 1 < len(cats) else None)
    pn = '<nav class="pn" aria-label="Families">%s%s</nav>' % (
        '<a href="%s"><small>%s</small><b>%s</b></a>' % (cx.u("family-" + prv["slug"]), esc(S("prev_fam")), esc(fam_name(prv))) if prv else "<span></span>",
        '<a class="nx" href="%s"><small>%s</small><b>%s</b></a>' % (cx.u("family-" + nxt["slug"]), esc(S("next_fam")), esc(fam_name(nxt))) if nxt else "<span></span>")
    body = f"""<header class="phead"><p class="kicker num">{esc(S('family_of', n=idx + 1, total=len(cats)))} · {esc(S('patterns_n', n=len(cards)))}</p>
<h1>{esc(nm)}</h1></header>
{src(md(cat['intro_md'], first_cls='first'), 'intro')}
<ul class="cards">{''.join(cards)}</ul>
{pn}"""
    desc = clip("%s %s: %d patterns, each with a scene, signs, what to keep and what to do." % (nm, cx.ph.get("in_industry", ""), len(cards)))
    O = CONFIG["origin"]
    ld = [article_ld(cx, nm, desc, "family-" + cat["slug"], "CollectionPage", {
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "url": O + cx.combo_url(k), "name": cx.combos[k]["name"]}
            for n, k in enumerate(k for k in cat["combos"] if k in cx.live)]}})]
    return frame(cx, title="%s in the %s · %s" % (nm, cx.ti, S("site")), desc=desc, path="family-" + cat["slug"],
                 crumbs=H(cx) + [(S("patterns_k"), cx.u("patterns")), (nm, None)], body=body, ld=ld, og="family-" + cat["slug"], cls="family")


def standards_html(cx, keys=None, h="h3"):
    St = cx.d["standards"]
    return "".join('<section id="%s" class="std-s"><%s>%s</%s>%s</section>' % (slugify(k), h, esc(k), h, src(md(St[k])))
                   for k in (keys or St) if k in St)


def method_page(cx):
    d = cx.d
    tags = collections.Counter()
    for c in d["combos"]:
        for k, v in c["tag_counts"].items():
            tags[k] += v
    from lib import TAG_KIND
    kinds = collections.Counter()
    for k, v in tags.items():
        kinds[TAG_KIND[k]] += v
    states = collections.Counter(c["review_state"] for c in d["combos"])
    lab = [("composite", TAG_LABEL["composite"]), ("pattern", TAG_LABEL["pattern"]), ("legal", TAG_LABEL["legal"]),
           ("review", TAG_LABEL[("review", "unreviewed")]), ("source", TAG_LABEL[("source", "unreviewed")])]
    lab_html = "".join('<li><span class="tg tg-%s">%s</span> %s <span class="meta num">%s</span></li>' % (
        k, esc(l), esc(e), esc("%d in the text" % kinds.get(k, 0))) for k, (l, e) in lab)
    st_html = ", ".join("%s: %d" % (STATE_NAME[k], states.get(k, 0)) for k in STATE_NAME)
    tot = collections.Counter()
    for info in cx.res.values():
        for k2 in ("cited", "reworded", "removed", "conditional", "pending", "resolved"):
            tot[k2] += info.get(k2, 0)
        tot["added"] += info.get("added", 0)
    done_pages = sum(1 for k2 in cx.live if cx.res.get(k2) and cx.res[k2]["resolved"] and not cx.res[k2]["pending"])
    facts = [f for f in cx.facts.values() if f.get("sources")]
    fact_html = "".join('<li><p><b>%s.</b> %s</p><p class="ui meta">%s</p></li>' % (esc(f["topic"][:1].upper() + f["topic"][1:]), esc(f["statement"]), " · ".join(
        '<a href="%s" rel="noopener">%s</a> (%s)' % (esc(x["url"]), esc(x["title"]), esc(x["publisher"])) for x in f["sources"])) for f in facts)
    checking_html = ('<section id="checking"><h2>%s</h2><p>%s</p><p class="ui">%s</p>%s</section>' % (
        esc(S("method_check_h")), esc(S("method_check")),
        esc(S("method_check_n", resolved=tot["resolved"], pending=tot["pending"], cited=tot["cited"], reworded=tot["reworded"], removed=tot["removed"], added=tot["added"], pages=done_pages, total=len(cx.live))),
        ('<h3>%s</h3><ul class="plain sources">%s</ul>' % (esc(S("method_facts_h")), fact_html)) if facts else "")) if cx.res else ""
    body = f"""<header class="phead"><p class="kicker">{esc(S('method_k'))}</p><h1>{esc(S('method_h'))}</h1>
<p class="lede">{esc(S('method_lede'))}</p></header>
<div class="prose-ui">
<section id="what"><h2>{esc(S('method_is_h'))}</h2><p>{esc(S('method_is'))}</p><p>{esc(S('method_isnot'))}</p></section>
<section id="how"><h2>{esc(S('method_how_h'))}</h2><p>{esc(S('method_how', tactics=len(d['tactics']), patterns=len(cx.live)))}</p></section>
<section id="fit"><h2>{esc(S('method_fit_h'))}</h2><p><b>{esc(S('f_fit_a'))}</b> ({sum(c['tier'] == 'A' for c in d['combos'])}) and <b>{esc(S('f_fit_b'))}</b> ({sum(c['tier'] == 'B' for c in d['combos'])}). {esc(S('f_fit_note'))}</p></section>
<section id="labels"><h2>{esc(S('labels_h'))}</h2><p>{esc(S('method_labels'))}</p><ul class="plain legend-list ui">{lab_html}</ul>
<p class="ui meta">{esc(S('method_states'))} {esc(st_html)}.</p></section>
{checking_html}
<section id="standards"><h2>{esc(S('method_std_h'))}</h2><p>{esc(S('method_std'))}</p>{standards_html(cx)}</section>
<section id="cite"><h2>{esc(S('method_cite_h'))}</h2><p class="cite ui">{esc(S('author'))}. {cx.date[:4]}. <i>{esc(cx.title)}</i>. {esc(S('site'))}, {esc(S('publisher'))}. {CONFIG['origin']}{cx.u()}</p></section>
<section id="licence"><h2>{esc(S('method_licence_h'))}</h2><p>{esc(S('method_licence'))}</p></section>
<section id="corrections"><h2>{esc(S('method_contact_h'))}</h2><p>{esc(S('method_contact'))}</p></section>
</div>"""
    desc = clip("What this map of manipulation %s is and is not, how it was written, what the labels mean, and the sector standards." % cx.ph.get("in_industry", ""))
    return frame(cx, title="Method, Labels and Standards · %s · %s" % (cx.short, S("site")), desc=desc, path="method",
                 crumbs=H(cx) + [(S("method_k"), None)], body=body, ld=[article_ld(cx, S("method_h"), desc, "method")], cls="method")


def take_page(cx):
    from lib import ROOT
    rows = []
    for x in cx.downloads:
        p = ROOT / "library/fractal2/site" / x.get("file", "").lstrip("/")
        if x.get("file") and p.exists():
            rows.append('<li><a href="/%s">%s</a> <span class="meta">%s</span> %s</li>' % (esc(x["file"].lstrip("/")), esc(x["title"]), esc(x.get("size", "")), esc(x.get("note", ""))))
    dl = '<ul class="plain">%s</ul>' % "".join(rows) if rows else '<p>%s</p>' % esc(S("take_pdf_soon"))
    body = f"""<header class="phead"><p class="kicker">{esc(S('take_k'))}</p><h1>{esc(S('take_h'))}</h1>
<p class="lede">{esc(S('take_lede'))}</p></header>
<div class="prose-ui">
<section id="print"><h2>{esc(S('take_print_h'))}</h2><p>{esc(S('take_print'))}</p><ol class="ui"><li>{esc(S('take_step1'))}</li><li>{esc(S('take_step2'))}</li><li>{esc(S('take_step3'))}</li></ol></section>
<section id="pdf"><h2>{esc(S('take_pdf_h'))}</h2>{dl}<p class="note ui">{esc(S('take_labels_note', date=cx.date))}</p></section>
<section id="share"><h2>{esc(S('take_share_h'))}</h2><p>{esc(S('take_share'))}</p></section>
</div>"""
    desc = clip("Print any pattern %s as a clean hand-out, quick-read sections first. PDF editions are being prepared." % cx.ph.get("in_industry", ""))
    return frame(cx, title="Take It With You: Print and Share · %s · %s" % (cx.short, S("site")), desc=desc, path="take-it-with-you",
                 crumbs=H(cx) + [(S("take_k"), None)], body=body, ld=[article_ld(cx, S("take_h"), desc, "take-it-with-you")], cls="take")


def az_page(cx):
    rows = [(c["name"], cx.combo_url(c["combo_id"]), "Pattern", fam_name(cx.cats[c["category_id"]])) for c in cx.d["combos"] if c["combo_id"] in cx.live]
    rows += [(t["name"], cx.tactic_url(t["single_no"]), "Tactic", cx.stage_name(t["stage"])) for t in cx.d["tactics"]]
    rows.sort(key=lambda r: re.sub(r"^(the|a)\s+", "", r[0].lower().strip('"“')))
    lis = "".join('<li data-k="%s"><a href="%s">%s</a><span class="ui meta">%s · %s</span></li>' % (esc(r[0].lower()), r[1], esc(r[0]), r[2], esc(r[3])) for r in rows)
    body = f"""<header class="phead"><p class="kicker num">{esc(S('az_k', n=len(rows)))}</p><h1>{esc(S('az_h'))}</h1>
<label class="filter ui"><span>{esc(S('az_filter'))}</span><input id="q" type="search" autocomplete="off" placeholder="{esc(S('az_placeholder'))}"></label></header>
<ul class="az" id="az">{lis}</ul><p id="none" class="note" hidden>{esc(S('az_none'))}</p>"""
    desc = clip("Every manipulation tactic and pattern %s, A to Z." % cx.ph.get("in_industry", ""))
    return frame(cx, title="Tactics and Patterns, A to Z · %s · %s" % (cx.short, S("site")), desc=desc, path="a-z",
                 crumbs=H(cx) + [(S("az_h"), None)], body=body, ld=[article_ld(cx, S("az_h"), desc, "a-z", "CollectionPage")], cls="az-page")


# ---------- packet-02 stubs: complete static pages from existing data only ----------
def safety_box(big=False):
    return '<aside class="safety%s" role="note"><p class="safety-h">%s %s</p><p>%s</p></aside>' % (
        " big" if big else "", svg("alert"), esc(S("read_first")), esc(S("safety_line")))


def notice_page(cx):
    lis = "".join('<li><a class="door" href="%s?setting=%s"><span>%s</span><span class="meta num">%s</span></a></li>' % (
        cx.u("patterns"), s["key"], esc(s["label"]), esc(S("patterns_n", n=s["n"]))) for s in cx.der["settings"])
    body = f"""<header class="phead"><p class="kicker">{esc(S('notice_k'))}</p><h1>{esc(S('notice_h'))}</h1>
<p class="lede">{esc(S('notice_lede'))}</p><p class="ui meta">{esc(S('notice_private'))}</p></header>
{safety_box()}<ul class="doors">{lis}</ul><p class="ui"><a class="go-link" href="{cx.u('in-it-now')}">{esc(S('door_in_it_now'))}</a></p>"""
    desc = clip("Start from the part of the work where something feels off, and find the manipulation patterns %s that live there." % cx.ph.get("in_industry", ""))
    return frame(cx, title="What Are You Noticing? · %s · %s" % (cx.short, S("site")), desc=desc, path="notice",
                 crumbs=H(cx) + [(S("notice_k"), None)], body=body, ld=[article_ld(cx, S("notice_k"), desc, "notice")], cls="notice")


def in_it_now_page(cx):
    strip = "".join('<li style="--c:var(--s%d)"><a href="%s"><span class="num">%02d</span> <b>%s</b><small>%s</small></a></li>' % (
        i + 1, cx.stage_url(s), i + 1, esc(cx.stage_name(s)), esc(STAGE_INFO[s])) for i, s in enumerate(cx.d["stages"]))
    ten = "".join('<li>%s</li>' % cx.combo_link(t["combo_id"], t["name"], "#quick") for t in cx.d["top10"])
    body = f"""<header class="phead"><p class="kicker">{esc(S('inn_k'))}</p><h1>{esc(S('inn_h'))}</h1></header>
{safety_box(True)}
<p class="ui">{esc(S('inn_leave'))}</p>
<div class="prose-ui">{standards_html(cx, ['Escalation Tiers For This Sector'], 'h2')}</div>
<section><h2>{esc(S('inn_stages'))}</h2><p>{esc(S('inn_stages_d'))}</p><ol class="stage-strip">{strip}</ol></section>
<section><h2>{esc(S('inn_ten'))}</h2><ol class="plain big-list">{ten}</ol></section>"""
    desc = clip("If you are inside a manipulative situation %s now: safety first, when to get help, and the ten patterns at two minutes each." % cx.ph.get("in_industry", ""))
    return frame(cx, title="If You Are in It Now · %s · %s" % (cx.short, S("site")), desc=desc, path="in-it-now",
                 crumbs=H(cx) + [(S("inn_k"), None)], body=body, ld=[article_ld(cx, S("inn_k"), desc, "in-it-now")], cls="path")


def worried_page(cx):
    groups = []
    for cat in cx.d["categories"]:
        ks = [k for k in cat["combos"] if k in cx.live and cx.combos[k]["has_safety_note"]]
        if ks:
            groups.append('<section class="g"><h3>%s</h3><ul class="plain">%s</ul></section>' % (esc(fam_name(cat)), "".join('<li>%s</li>' % cx.combo_link(k) for k in ks)))
    body = f"""<header class="phead"><p class="kicker">{esc(S('worried_k'))}</p><h1>{esc(S('worried_h'))}</h1>
<p class="lede">{esc(S('worried_lede'))}</p></header>
{safety_box()}
<div class="prose-ui">{standards_html(cx, ['Universal Benign Explanations', 'Concern Strengthens When'], 'h2')}</div>
<section><h2>{esc(S('worried_safety_h'))}</h2><div class="groups">{''.join(groups)}</div></section>"""
    desc = clip("Worried about someone %s? The ordinary explanations to rule out first, the signs that make concern grow, and the patterns with a safety note." % cx.ph.get("in_industry", ""))
    return frame(cx, title="If You Are Worried About Someone · %s · %s" % (cx.short, S("site")), desc=desc, path="worried-about-someone",
                 crumbs=H(cx) + [(S("worried_k"), None)], body=body, ld=[article_ld(cx, S("worried_k"), desc, "worried-about-someone")], cls="path")


def sign_page(cx):
    ks = [k for k in cx.live if {"signing", "money"} & set(cx.der["combos"][k]["settings"])]
    ks.sort(key=lambda k: (cx.rank.get(k, 99), re.sub(r"^the\s+", "", cx.combos[k]["name"].lower())))
    lis = "".join('<li>%s%s <span class="meta ui">%s</span></li>' % (
        ('<span class="num rk-s">%02d</span> ' % cx.rank[k]) if k in cx.rank else "", cx.combo_link(k, None, "#quick"),
        esc(fam_name(cx.cats[cx.combos[k]["category_id"]]))) for k in ks)
    body = f"""<header class="phead"><p class="kicker">{esc(S('sign_k'))}</p><h1>{esc(S('sign_h'))}</h1>
<p class="lede">{esc(S('sign_lede'))}</p></header>
<section><h2>{esc(S('patterns_n', n=len(ks)))}</h2><ol class="plain big-list">{lis}</ol></section>
<div class="prose-ui">{standards_html(cx, ['Universal Evidence To Preserve'], 'h2')}</div>"""
    desc = clip("About to sign something %s? The manipulation patterns that live in contracts and money, ten that matter most first, and what to keep." % cx.ph.get("in_industry", ""))
    return frame(cx, title="Before You Sign · %s · %s" % (cx.short, S("site")), desc=desc, path="before-you-sign",
                 crumbs=H(cx) + [(S("sign_k"), None)], body=body, ld=[article_ld(cx, S("sign_k"), desc, "before-you-sign")], cls="path")


def map_page(cx):
    T = cx.tactics
    tl = lambda no: '<a href="%s">%s</a>' % (cx.tactic_url(no), esc(T[no]["name"]))
    top = "".join('<tr><td>%s</td><td>%s%s</td><td class="num">%d</td></tr>' % (
        tl(x["single_no"]), dot(cx.stage_no(T[x["single_no"]]["stage"])), esc(cx.stage_name(T[x["single_no"]]["stage"])), x["n"])
        for x in cx.der["map"]["top_tactics"])
    pairs = "".join('<tr><td>%s <span class="meta">%s</span> %s</td><td class="num">%d</td><td>%s</td></tr>' % (
        tl(p["a"]), esc(S("map_then")), tl(p["b"]), len(p["combos"]), ", ".join(cx.combo_link(k) for k in p["combos"]))
        for p in cx.der["map"]["pairs"])
    body = f"""<header class="phead"><p class="kicker">{esc(S('map_k'))}</p><h1>{esc(S('map_h'))}</h1>
<p class="lede">{esc(S('map_lede'))}</p></header>
<div id="map-stage"></div>
<section><h2>{esc(S('map_top'))}</h2><div class="tbl"><table><thead><tr><th scope="col">Tactic</th><th scope="col">Stage</th><th scope="col">Patterns</th></tr></thead><tbody>{top}</tbody></table></div></section>
<section><h2>{esc(S('map_pairs'))}</h2><div class="tbl"><table><thead><tr><th scope="col">Pair, in order</th><th scope="col">Patterns</th><th scope="col">Where</th></tr></thead><tbody>{pairs}</tbody></table></div></section>"""
    desc = clip("Which manipulation tactics recur most often %s, and which pairs most often follow each other." % cx.ph.get("in_industry", ""))
    return frame(cx, title="The Map: How Sequences Recur · %s · %s" % (cx.short, S("site")), desc=desc, path="map",
                 crumbs=H(cx) + [(S("map_k"), None)], body=body, ld=[article_ld(cx, S("map_h"), desc, "map", "CollectionPage")], cls="map")
