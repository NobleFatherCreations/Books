#!/usr/bin/env python3
"""Builds 'Five machines, one school' in the visual system of the CRE top-10 combos PDF. Five combinations: the owner's three Education scripts
(content_edu.py: breakdowns verbatim, stories expanded) then The Paper Child and The Calling Trap (content.py).
Every section starts on a new page; fit.mjs scales each section's type so it fills 1-2 whole pages.
Usage: python3 build.py -> composites.html ; node fit.mjs composites.html out.pdf"""
import re, html, pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from content import COMBOS as OLD
import content_edu as E

COVER = E.COVER
COMBOS = E.EDU + OLD
for i, c in enumerate(COMBOS, 1): c["n"] = i

def md(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t
def P(lst, cls=""): return "".join(f'<p{" class=%s" % cls if cls else ""}>{md(x)}</p>' for x in lst)

SEC = [0]
def sec(kind, inner, fit=True):
    SEC[0] += 1
    return f'<section class="sec {kind}{" fit" if fit else ""}" data-id="{SEC[0]:02d}"><span class="mk">zzS{SEC[0]:02d}</span><div class="in">{inner}</div></section>'

out = []
out.append(sec("cover", f'''<div class="eb">{md(COVER["eyebrow"])}</div><h1>{md(COVER["title"])}</h1>
<p class="lede">{md(COVER["lede"])}</p><p class="lede2">{md(COVER["body"])}</p>
<ol class="toc">{"".join(f'<li><span class="bdg">{c["n"]}</span><b>{md(c["name"])}</b><i>{md(c["tagline"])}</i></li>' for c in COMBOS)}</ol>
<div class="note">{md(COVER["note"])}</div>''', fit=False))

for c in COMBOS:
    chain = " <span class='ar'>→</span> ".join(f"<span>{md(t)}</span>" for t in c["chain"])
    out.append(sec("title", f'''<div class="hd"><span class="bdg big">{c["n"]}</span><h2>{md(c["name"])}</h2></div>
<div class="meta">{md(c["meta"])}</div><p class="tag">{md(c["tagline"])}</p>
<p class="why"><b>Why it matters here.</b> {md(c["why"])}</p>
<div class="chain">{chain}</div>
<blockquote>{md(c["quote"])}</blockquote>
<p class="small">The story comes first, with no labels. Every tactic in the chain above happens in it, in that order. The architecture follows.</p>'''))
    for label, paras in c["scenes"]:
        out.append(sec("scene", f'<div class="sl"><span>{md(label)}</span></div><div class="story">{P(paras)}</div>'))
    out.append(sec("scene cost", f'<div class="sl"><span>What it cost</span></div><div class="story">{P(c["cost"])}</div>'))
    cards = "".join(f'''<div class="tc"><div class="tch"><span class="num">{k}</span><b>{md(n)}</b></div><p class="tq">{md(q)}</p><p>{md(t)}</p></div>'''
                    for k, (n, q, t) in enumerate(c["tactics"], 1))
    out.append(sec("cut", f'''<div class="hardcut"><span>HARD CUT</span></div><h3 class="named">{md(c["named"])}</h3>
<p class="def">{md(c["definition"])}</p><div class="cards">{cards}</div>'''))
    out.append(sec("text", f'<div class="kk">Why this order</div><h3>Why the sequence works</h3>{P(c["order"])}'))
    out.append(sec("text", f'<div class="kk">Why the system produces this order</div><h3>Nobody designed it. Here is where it comes from.</h3>{P(c["system"])}'))
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
# every tactic appears, in order, in its story's beat map
for c in COMBOS: assert [b[0] for b in c["beats"]] == c["chain"], c["name"]
(HERE / "composites.html").write_text(doc)
print("wrote composites.html, sections:", SEC[0], "; owner lines checked:", len(E.USED), "+", sum(len(v) for v in E.KEYQ.values()), "key lines; all present")
