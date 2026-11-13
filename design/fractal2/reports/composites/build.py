#!/usr/bin/env python3
"""Builds 'Five machines, one school' in the visual system of the CRE top-10 combos PDF.
Per combination: cold intro page ('Composite chain #N', no name, no tactics) -> story scenes -> cost -> the name and chain
(title page) -> tactic cards -> why this order -> why the system produces it -> 'on purpose' page -> institution/society ->
recognition + chain breakers -> where each tactic happened + the question.
The owner's three Education scripts keep their breakdowns verbatim (content_edu.py); Paper Child + Calling Trap come from content.py with
their stories from edu.txt. The build fails if an owner line is missing or a tactic is not found, in order, in its story.
Usage: python3 build.py -> composites.html (+ audit-data.json); node fit.mjs composites.html out.pdf"""
import re, html, json, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from content import COMBOS as OLD
import content_edu as E

COVER = E.COVER
KEY = {"The Paper Child": "paper", "The Calling Trap": "calling"}
for c in OLD:
    n = E.NEW[KEY[c["name"]]]
    c["scenes"], c["cost"], c["beats"] = n["scenes"], n["cost"], n["beats"]
    c["intro"], c["purpose"], c["anchors"], c["key"] = n["intro"], n["purpose"], n["anchors"], KEY[c["name"]]
    c["named"] = f"That's called {c['name']}."
COMBOS = E.EDU + OLD
for i, c in enumerate(COMBOS, 1): c["n"] = i

def md(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t
def P(lst, cls=""):
    return "".join('<p class="brk">· · ·</p>' if x.strip() == "---" else f'<p{" class=%s" % cls if cls else ""}>{md(x)}</p>' for x in lst)

SEC = [0]
def sec(kind, inner, fit=True):
    SEC[0] += 1
    return f'<section class="sec {kind}{" fit" if fit else ""}" data-id="{SEC[0]:02d}"><span class="mk">zzS{SEC[0]:02d}</span><div class="in">{inner}</div></section>'

LEAD = ("Nobody orchestrated what you just read. A budget, a funnel, a schedule or a form did it, and the people inside were doing their jobs. "
        "Here is the same chain with a person steering it on purpose, against someone close to them. The tactics are the same and so is their order. "
        "Only the chooser has changed.")
OWN = "Nobody designed what you just read, and that doesn't make it any less real."

out = []
out.append(sec("cover", f'''<div class="eb">{md(COVER["eyebrow"])}</div><h1>{md(COVER["title"])}</h1>
<p class="lede">{md(COVER["lede"])}</p><p class="lede2">{md(COVER["body"])}</p>
<ol class="toc">{"".join(f'<li><span class="bdg">{c["n"]}</span><b>Composite chain {c["n"]}</b><i>{md(c["intro"].split(" Where")[0].replace("A point in a life: ", ""))}</i></li>' for c in COMBOS)}</ol>
<div class="note">{md(COVER["note"])}</div>''', fit=False))

audit = []
for c in COMBOS:
    # 1. the cold intro: no name, no tactics
    stage, where = c["intro"].split(" Where it happens: ")
    out.append(sec("intro", f'''<div class="ik">Composite chain</div><div class="inum">{c["n"]}</div>
<p class="idesc">This example will show you the architecture of a sequence of tactics that happens at one point in a life, and that can affect you for the rest of it.</p>
<p class="idesc2">You won't be told what it's called, or what's inside it. Read the story first. When it ends, we'll take it apart in the order it happened.</p>
<div class="isetting"><span>{md(stage.replace("A point in a life: ", "A point in a life: "))}</span><span>Where it happens: {md(where)}</span></div>''', fit=False))
    # 2. the story, then what it cost
    for label, paras in c["scenes"]:
        out.append(sec("scene", f'<div class="sl"><span>{md(label)}</span></div><div class="story">{P(paras)}</div>'))
    out.append(sec("scene cost", f'<div class="sl"><span>What it cost</span></div><div class="story">{P(c["cost"])}</div>'))
    # 3. the name and what is in it
    chain = " <span class='ar'>→</span> ".join(f"<span>{md(t)}</span>" for t in c["chain"])
    out.append(sec("title", f'''<div class="hardcut"><span>HARD CUT</span></div>
<div class="hd"><span class="bdg big">{c["n"]}</span><span class="hdt">Composite chain {c["n"]}</span></div>
<h2 class="nm">{md(c["named"])}</h2>
<div class="meta">{md(c["meta"])}</div><p class="tag">{md(c["tagline"])}</p>
<p class="why"><b>Why it matters here.</b> {md(c["why"])}</p>
<div class="kk2">What it has in it, in order</div><div class="chain">{chain}</div>'''))
    cards = "".join(f'''<div class="tc"><div class="tch"><span class="num">{k}</span><b>{md(n)}</b></div><p class="tq">{md(q)}</p><p>{md(t)}</p></div>'''
                    for k, (n, q, t) in enumerate(c["tactics"], 1))
    out.append(sec("cut", f'''<div class="kk">The chain, tactic by tactic</div><p class="def">{md(c["definition"])}</p><div class="cards">{cards}</div>'''))
    out.append(sec("text", f'<div class="kk">Why this order</div><h3>Why the sequence works</h3>{P(c["order"])}'))
    out.append(sec("text", f'<div class="kk">Why the system produces this order</div><h3>Nobody designed it. Here is where it comes from.</h3>{P(c["system"])}'))
    # 4. the same chain, on purpose
    out.append(sec("text purpose", f'<div class="kk">On purpose</div><h3>The same chain, with a person steering it</h3><p class="leadp">{md(LEAD)}</p>{P(c["purpose"])}'))
    out.append(sec("text", f'''<div class="kk">The same machine, larger</div><h3>In an institution</h3>{P(c["institution"])}
<h3>Across a society</h3>{P(c["civilization"])}'''))
    if c.get("raw"):
        spots = "".join(f'<div class="spot"><b>Spot it — {md(n)}.</b> {md(t)}</div>' for n, t in c["spot_raw"])
        steps = "".join(f'<p><b>{md(m.group(1))}</b> {md(m.group(2))}</p>' if (m := re.match(r"^(Step \w+:) (.*)$", s, re.S)) else f"<p>{md(s)}</p>" for s in c["steps"])
        bi = f'<p>{md(c["breaker_intro"])}</p>' if c.get("breaker_intro") else ""
        out.append(sec("text", f'''<div class="kk">Recognition and chain breakers</div><h3>How to know if you're inside it</h3><p>{md(c["spot_intro"])}</p>{spots}
<h3>{md(c["breaker_label"])}</h3>{bi}{steps}'''))
    else:
        spots = "".join(f'<div class="spot"><b>Spot it — {md(n)}:</b> Ask: {md(a)} Concern rises if: {md(r)}</div>' for n, a, r in c["spot"])
        out.append(sec("text", f'<div class="kk">Recognition</div><h3>How to know if you\'re inside it</h3><p>From any seat at the table. Most good practitioners already do some of these. That\'s why they work.</p>{spots}'))
        out.append(sec("text", f'<div class="kk">Chain breakers</div><h3>How to start breaking it</h3><ul class="br">{"".join(f"<li>{md(b)}</li>" for b in c["breakers"])}</ul><div class="say"><b>Say:</b><br>{"<br>".join(md(s) for s in c["say"])}</div>'))
    rows = "".join(f'<tr><td class="n">{k}</td><td><b>{md(t)}</b></td><td>{md(w)}</td><td>{md(m)}</td></tr>' for k, (t, w, m) in enumerate(c["beats"], 1))
    qh = c.get("qlabel", "Here's your question:") if c.get("raw") else "Here's your question"
    qhead = f'<div class="qhead">{md(qh)}</div>' if qh else ""
    out.append(sec("text", f'''<div class="kk">The architecture under the story</div><h3>Where each tactic happened</h3>
<table class="beats"><tr><th></th><th>Tactic</th><th>Scene</th><th>The moment</th></tr>{rows}</table>
{qhead}<blockquote class="q">{md(c["question"])}</blockquote>'''))

    # ---- order audit: every tactic's anchor phrase must sit in the story, in chain order
    story = "\n".join(p for _, ps in c["scenes"] for p in ps if p.strip() != "---")
    pos, last = [], -1
    assert [a[0] for a in c["anchors"]] == c["chain"], f'{c["name"]}: anchors do not follow the chain'
    for (tactic, phrase) in c["anchors"]:
        i = story.find(phrase)
        assert i >= 0, f'{c["name"]}: no story line for {tactic}: {phrase!r}'
        assert i > last, f'{c["name"]}: {tactic} appears out of order'
        last = i
        scene = next(l for l, ps in c["scenes"] if phrase in " ".join(ps))
        pos.append({"tactic": tactic, "scene": scene, "phrase": phrase, "pos": i})
    words = sum(len(p.split()) for _, ps in c["scenes"] for p in ps if p.strip() != "---")
    audit.append({"n": c["n"], "name": c["name"], "words": words, "scenes": len(c["scenes"]), "tactics": pos})

CSS = (HERE / "style.css").read_text()
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Five machines, one school</title><style>{CSS}</style></head>
<body>{"".join(out)}</body></html>'''

# ---- fidelity tests: the owner's lines, word for word
def norm(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).replace('"', "").replace("“", "").replace("”", "").strip()
plain = norm(doc)
miss = [l for l in E.USED if norm(l) not in plain]
assert not miss, f"OWNER SCRIPT LINES MISSING ({len(miss)}): {miss[0][:80]}"
for k, qs in E.KEYQ.items():
    for q in qs: assert norm(q) in plain, f"{k}: key line missing from the expanded story: {q[:70]}"
for c in COMBOS: assert [b[0] for b in c["beats"]] == c["chain"], c["name"]
# the cold intro must not give the game away: no combination name and no tactic before the story ends
for c in COMBOS:
    intro = next(s for s in out if s.count(f'class="inum">{c["n"]}<') == 1)
    low = html.unescape(re.sub(r"<[^>]+>", " ", intro)).lower()
    assert c["name"].lower() not in low and not any(t.lower() in low for t in c["chain"]), f'{c["name"]}: intro page names the chain'
(HERE / "composites.html").write_text(doc)
(HERE / "audit-data.json").write_text(json.dumps(audit, indent=1))
print("wrote composites.html, sections:", SEC[0], "; owner lines:", len(E.USED), "+", sum(len(v) for v in E.KEYQ.values()), "key lines present;",
      "story words:", [a["words"] for a in audit], "; every tactic found in order")
