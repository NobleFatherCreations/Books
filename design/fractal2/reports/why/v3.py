#!/usr/bin/env python3
"""Edition 3 of "Why I Wrote This".

Reuses every edition-2 section from final-master.html (found by its kicker number), drops the old
movement dividers, reorders into eight movements, adds the owner's three education combination scripts
verbatim (from docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md) plus The Paper Child and The Calling
Trap as interludes, and adds the new sections from v3_content.py.

Usage: python3 v3.py            -> v3-master.html  (then: node render.mjs v3-master.html out.pdf; python3 fields.py out.pdf final.pdf)
Fails loudly if the origin passage or any line of the owner's scripts is not reproduced exactly.
"""
import re, html, pathlib, sys
HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import v3_content as C

src = (HERE / "final-master.html").read_text()
head, body = src.split("<body>", 1)
body = body.rsplit("</body>", 1)[0]
cover = re.search(r'<section class="cover">.*?</section>', body, re.S).group(0)
hook = re.search(r'<section class="hook pb">.*?</section>', body, re.S).group(0).replace("and how it stops.", "and where it breaks.")
qs = re.search(r'<section class="pb" id="qs">.*?(?=<div class="sec" id="s1">)', body, re.S).group(0)
machine = re.search(r'<figure class="fig">.*?</figure>', qs, re.S).group(0)

# ---- edition-2 sections, keyed by their old kicker number
rest = body[body.index('<div class="sec" id="s1">'):]
rest = re.sub(r'<div class="part[^"]*">.*?</div>\s*', "", rest, flags=re.S)
rest = re.sub(r"</section>\s*$", "", rest.strip())
OLD, cur = {}, None
for c in re.split(r'(?=<div class="sec)', rest):
    m = re.search(r'<div class="kick">(\d+) · ', c[:400])
    if m: cur = int(m.group(1))
    if cur is None: continue
    OLD[cur] = OLD.get(cur, "") + c
assert sorted(OLD) == list(range(1, 24)), sorted(OLD)
# edition-2 cross-references -> edition-3 numbers (only inside reused edition-2 text)
MAP = {1: 2, 2: 4, 3: 5, 4: 14, 5: 6, 6: 8, 7: 7, 8: 13, 9: 9, 10: 11, 11: 16, 12: 12, 13: 17, 14: 18, 15: 19,
       16: 23, 17: 25, 18: 26, 19: "R1", 20: "R2", 21: "R3", 22: "R5", 23: 27}
OLDREF = re.compile(r"(Sections? )((?:\d+(?:, | and | to |, and )?)+)")
def remap(m):
    return m.group(1) + re.sub(r"\d+", lambda n: str(MAP.get(int(n.group()), n.group())), m.group(2))
OLD = {k: OLDREF.sub(remap, v) for k, v in OLD.items()}

def kick(chunk, n, label):
    """Replace the first kicker with the new number and label."""
    return re.sub(r'<div class="kick">[^<]*</div>', f'<div class="kick">{n} · {label}</div>', chunk, count=1)

# ---- edition 1 (the first 21-page build): nothing is dropped. Sections v2 left out go back into the story; v1's own
# versions of the tables go into an appendix at the back.
V1 = (HERE.parent / "why-i-wrote-this.html").read_text()
V1 = V1[V1.index("<body"):]
v1s = {}
for c in re.split(r'(?=<div class="sec)', V1)[1:]:
    t = re.search(r"<h2[^>]*>(.*?)</h2>", c, re.S)
    if t: v1s[re.sub(r"<[^>]+>", "", t.group(1))] = re.sub(r"</section>.*$", "", c, flags=re.S).replace('class="sec pb"', 'class="sec"')
def v1(title): return v1s[title]

# ---- split the old "five combinations" section into its parts
c11 = OLD[11]
combo_starts = [m.start() for m in re.finditer(r'<div class="combo">', c11)]
connect_at = c11.index("<h3>How the five connect")
combos_v2 = [c11[a:b] for a, b in zip(combo_starts, combo_starts[1:] + [connect_at])]
intro11 = c11[:combo_starts[0]]
connect = c11[connect_at:]
chains = [re.search(r'<figure class="fig chain">.*?</figure>', c, re.S).group(0) for c in combos_v2]

# ---- the owner's scripts, verbatim
VERB = (ROOT / "docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md").read_text().split("\n")
def lines(a, b):  # 1-based inclusive line numbers in OWNER-MESSAGES-VERBATIM.md
    return [l for l in VERB[a - 1:b] if l.strip()]
SCRIPTS = {
    "trauma": lines(1033, 1083),
    "normal": lines(1085, 1135),
    "shame": lines(1137, 1176),
}
CUE = re.compile(r"^\[(.+)\]$")
def script_html(key, chain):
    L = SCRIPTS[key]
    out, i = [], 0
    eyebrow = []
    while i < len(L) and (L[i].isupper() and not L[i].startswith('"')):   # COMBO 21: ... / SPOKEN SCRIPT
        eyebrow.append(L[i]); i += 1
    if i < len(L) and CUE.match(L[i]) and "COLD OPEN" in L[i].upper():  # the cold open has no heading, by request
        eyebrow.append(CUE.match(L[i]).group(1)); i += 1
    out.append('<section class="interlude pb">')
    if eyebrow: out.append('<p class="ieb">' + " · ".join(html.escape(e) for e in eyebrow) + "</p>")
    out.append('<div class="cold">')
    cut = False
    chain_done = False
    for l in L[i:]:
        m = CUE.match(l.strip())
        if m:
            label = m.group(1)
            if label.upper() == "HARD CUT":
                out.append('</div><div class="hardcut"><span>' + html.escape(label) + "</span></div><div class=\"bd\">")
                cut = True
                continue
            if cut and not chain_done and "WHY THIS ORDER" in label.upper():
                out.append(chain); chain_done = True
            out.append('<p class="cue">' + html.escape(label) + "</p>")
            continue
        if not cut and (l.startswith("That's called") or l.startswith('"That\'s the')):
            pass
        cls = ""
        if re.match(r"^(That's called|\"That's the) ", l): cls = ' class="named"'
        elif l.strip() in ("CHAIN BREAKERS.", "Here's your question:") or l.startswith("Now the question"): cls = ' class="turn"'
        out.append(f"<p{cls}>" + html.escape(l) + "</p>")
    if not chain_done: out.append(chain)
    out.append("</div></section>")
    return "\n".join(out)

def v2_interlude(block):
    """The Paper Child / The Calling Trap: scene first with no heading, then the full breakdown from edition 2."""
    name = re.search(r'<h3 class="cname">(.*?)</h3>', block, re.S).group(1)
    scene = re.search(r'<div class="scene">.*?</div>', block, re.S).group(0)
    rest_ = block.replace(scene, "").replace(re.search(r'<h3 class="cname">.*?</h3>', block, re.S).group(0), "")
    rest_ = re.sub(r'<div class="ckick">.*?</div>', "", rest_, count=1)
    scene_p = re.sub(r'</?div[^>]*>', "", scene)
    return ('<section class="interlude pb"><div class="cold">' + scene_p + '</div>'
            '<div class="hardcut"><span>HARD CUT</span></div><div class="bd">'
            f'<h3 class="cname named-h">{name}</h3>' + rest_ + "</div></section>")

# ---- assemble
P = C.parts()
N = {}  # section number -> anchor title, for the contents page
def sec(n, label, chunk, title):
    N[n] = title
    return f'<a id="sec{n}"></a>' + kick(chunk, n, label)

old1 = C.fix_why(OLD[1])
parts_html = [
    cover, hook,
    script_html("trauma", chains[0]),
    "@@CONTENTS@@",
    C.trust(),
    P[1],
    sec(1, "Where it comes from", C.origin(), "Why I can draw this"),
    sec(2, "Why", old1, "Why these books exist"),
    sec(3, "Three works", C.three_works(), "Three works, four verbs"),
    script_html("normal", chains[1]),
    P[2],
    sec(4, "The cycle", OLD[2], "Eight stages, and the garden and the gate"),
    sec(5, "Originals and inversions", OLD[3], "The thirty techniques, and what each one copies"),
    sec(6, "The sectors", OLD[5], "Thirty sectors, and our relationship to each need"),
    sec(7, "The fractal", OLD[7], "Three levels, and how the pattern passes on"),
    script_html("shame", chains[2]),
    P[3],
    sec(8, "The body of work", C.numbers_plus(OLD[6]), "What I built, in numbers"),
    sec(9, "The step into Fractal²", C.ladder_plus(OLD[9]), "From the map to the life"),
    sec(10, "One move, five works", C.one_tactic(), "One tactic through every work"),
    v2_interlude(combos_v2[3]),
    P[4],
    sec(11, "The combinations", C.order_plus(OLD[10]) + C.v1_body(v1("Why the order matters, and how combinations help people")), "Why the order matters"),
    sec(12, "Connections", OLD[12], "What the whole map shows that no single chapter says"),
    P[5],
    sec(13, "The frequency", C.frequency_plus(OLD[8]), "Why the pattern feels familiar, and what interrupts it"),
    sec(14, "What was there first", OLD[4], "The thirty original impulses"),
    sec("14b", "Turned inward", v1("The cage and the intent: accountability without shame"), "The cage and the intent: accountability without shame"),
    sec(15, "Your life, sector by sector", C.sector_cards(), "Your life, sector by sector"),
    v2_interlude(combos_v2[4]),
    P[6],
    sec(16, "Machines feed machines", C.machines(intro11, connect), "Five machines, one school"),
    sec(17, "The positive blueprint", OLD[13], "What a clean system looks like"),
    sec(18, "The war map", C.war_map_plus(OLD[14]), "How this turns into real change"),
    sec("18b", "Three fractals of change", v1("The three fractals of making change"), "The three fractals of making change"),
    sec(19, "Children and schools", OLD[15], "Where the pattern starts, and where it's easiest to stop"),
    P[7],
    sec(20, "Who it is for", C.need(), "Who this is for, in numbers"),
    sec(21, "How it helps", C.mechanisms(), "How it helps, and how sure I can be"),
    sec(22, "Precedent", C.precedents(), "This is how work like this has always started"),
    sec("22b", "What I hope this does", v1("What I hope this does"), "What I hope this does"),
    sec(23, "The horizon", C.horizon_plus(OLD[16]), "What this can become"),
    sec(24, "What it is worth", C.worth(), "What these three works do for people"),
    sec(25, "The best case", OLD[17], "The world that saw it"),
    P[8],
    sec(26, "The ask", C.ask_plus(OLD[18]), "I've mapped it. I can't carry it alone."),
    sec(27, "One more thing", C.levers(OLD[23]), "You may have noticed"),
    P["ref"],
    sec("R1", "Tools", OLD[19], "Trace it, interrupt it, audit your own system"),
    sec("R2", "Reading it whatever you believe", C.lenses_plus(OLD[20]), "Three lenses, one shape"),
    sec("R3", "Honest limits", C.limits_plus(OLD[21]), "What this is and is not"),
    sec("R4", "One possible program", C.laws(), "The laws list from the war map"),
    sec("R5", "From the series", C.slides_plus(OLD[22]), "The thirty inversions, and the whole map"),
    C.first_edition_note(),
    sec("R6", "From the first edition", v1("The eight stages, and what each one counterfeits"), "The eight stages, and what each one counterfeits (first edition)"),
    sec("R7", "From the first edition", v1("Thirty techniques, and the real needs they imitate"), "Thirty techniques, and the real needs they imitate (first edition)"),
    sec("R8", "From the first edition", v1("Thirty sectors: our relationship with every need"), "Thirty sectors: our relationship with every need (first edition)"),
    sec("R9", "From the first edition", v1("One pattern at three levels"), "One pattern at three levels (first edition)"),
    sec("R10", "From the first edition", v1("What this means for children and schools"), "What this means for children and schools (first edition)"),
    sec("R11", "From the first edition", v1("What this is and is not"), "What this is and is not (first edition)"),
    sec("R12", "From the first edition", v1("Three lenses, one shape"), "Three lenses, one shape (first edition)"),
    sec("R13", "From the first edition", v1("Why these books exist"), "Why these books exist (first edition)"),
    sec("R14", "From the first edition", v1("What I built, in numbers"), "What I built, in numbers (first edition)"),
]
doc = "\n".join(parts_html)

machine2 = (machine.replace("Sections 5, 8", "Sections 13 to 15").replace(">Section 5<", ">Sections 6, 15<")
            .replace(">Section 2<", ">Section 4<").replace("real. Section 3", "real. Section 5")
            .replace("live through. Section 10", "live through. Sections 11, 16").replace("fractal.  Section 7", "fractal.  Section 7"))
doc = doc.replace("@@CONTENTS@@", C.contents(N, machine2))

css = (HERE / "v3.css").read_text()
head = head.replace("</style>", css + "</style>")
head = re.sub(r"<title>.*?</title>", "<title>Why I Wrote This</title>", head)
out = head + "<body>" + doc + "</body></html>"

# ---- fidelity tests (fail the build)
plain = html.unescape(re.sub(r"<[^>]+>", " ", out))
plain = re.sub(r"\s+", " ", plain)
ORIGIN = (ROOT / "content/fractal2/intro-final.md").read_text().split("\n")[274:279]
for l in ORIGIN:
    if l.strip() and not l.startswith("<!--"):
        assert re.sub(r"\s+", " ", l.strip()) in plain, "ORIGIN PASSAGE CHANGED: " + l[:60]
for k, L in SCRIPTS.items():
    for l in L:
        t = CUE.match(l.strip()).group(1) if CUE.match(l.strip()) else l
        assert re.sub(r"\s+", " ", t.strip()) in plain, f"SCRIPT {k} LINE MISSING: {l[:70]}"
assert "@@" not in out
(HERE / "v3-master.html").write_text(out)
print("wrote v3-master.html", len(out), "bytes; sections:", len(N), "; fidelity tests passed")
