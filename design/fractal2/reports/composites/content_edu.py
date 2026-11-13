"""The owner's three Education combination scripts, expanded. Breakdown, why-this-order, institutional and civilizational echoes,
recognition cues, chain breakers and questions are read straight from docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md (lines 1033-1176)
and recorded in USED so build.py can fail if any line is missing. The cold-open stories, cost pages, 'why the system produces this order'
sections and beat maps are new writing, in edu.txt."""
import re, pathlib
HERE = pathlib.Path(__file__).parent
VERB = (HERE.parents[3] / "docs/handoff-2026-11-13/OWNER-MESSAGES-VERBATIM.md").read_text().split("\n")
def nb(a, b): return [l.strip() for l in VERB[a - 1:b] if l.strip()]
TB = nb(1033, 1083)
ALL = nb(1085, 1176)
NO, SH = ALL[:51], ALL[51:]
USED = []

def clean(l):
    """Multi-paragraph quotes in the owner's script open every paragraph with a quote mark and close only the last: drop the stray ones."""
    s = l
    if s.startswith('"'): s = s[1:]
    if s.endswith('"') and s.count('"') % 2 == 1: s = s[:-1]
    return s
def G(lst, a, b=None):
    out = [clean(x) for x in lst[a - 1:(b or a)]]
    USED.extend(out); return out
def tests(lines):
    out = []
    for l in lines:
        m = re.match(r'^(The [^.]+?(?:Test|Reflex|Scan|Audit))\. (.*)$', l, re.S)
        assert m, l[:60]
        out.append((m.group(1), m.group(2)))
    return out

# ---------------------------------------------------------------- prose file
TXT = (HERE / "edu.txt").read_text()
blocks = re.split(r"(?m)^@@ ", TXT)[1:]
NEW = {}; cur = None
def paras(body): return [" ".join(p.split("\n")).strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
for b in blocks:
    head, _, body = b.partition("\n")
    kind, _, arg = head.partition(" ")
    if kind == "combo":
        cur = NEW[arg] = {"scenes": [], "key": arg}
        for line in body.strip().split("\n"):
            k, _, v = line.partition(": "); cur[k] = v.strip()
        if "chain" in cur: cur["chain"] = [x.strip() for x in cur["chain"].split("|")]
        cur["carries"] = [x.strip() for x in cur["carries"].split("|")]
    elif kind == "scene": cur["scenes"].append((arg.strip(), paras(body)))
    elif kind in ("cost", "system", "purpose"): cur[kind] = paras(body)
    elif kind in ("anchors", "purpose_anchors"): cur[kind] = [[x.strip() for x in l.split("|")] for l in body.strip().split("\n") if l.strip()]
    elif kind in ("tactic_moments", "beats"):
        cur[kind] = [[x.strip() for x in l.split("|")] for l in body.strip().split("\n") if l.strip()]

def assemble(key, **o):
    c = NEW[key]
    tq = {n: q for n, q in c["tactic_moments"]}
    names = c["chain"]
    assert len(o["tactic_lines"]) == len(names), key
    return {
        "key": key, "stage": c["stage"], "where": c["where"], "installs": c["installs"], "carries": c["carries"],
        "purpose": c["purpose"], "purpose_anchors": c["purpose_anchors"], "anchors": c["anchors"], "name": c["name"], "tagline": c["tagline"], "meta": c["meta"], "why": c["why"], "chain": names,
        "scenes": c["scenes"], "cost": c["cost"], "named": o["named"], "definition": o["definition"],
        "tactics": [(n, tq[n], t) for n, t in zip(names, o["tactic_lines"])],
        "order": o["order"], "system": c["system"], "institution": o["inst"], "civilization": o["civ"],
        "raw": True, "spot_intro": o["spot_intro"], "spot_raw": tests(o["tests"]),
        "breaker_label": o.get("breaker_label", "How to start breaking it"), "breaker_intro": o.get("breaker_intro"), "steps": o["steps"],
        "qlabel": o.get("qlabel"), "question": o["question"], "beats": c["beats"],
    }

EDU = [
    assemble("trauma",
        named=G(TB, 9)[0], definition=G(TB, 11)[0], tactic_lines=G(TB, 12, 18), order=G(TB, 20, 25),
        inst=G(TB, 27, 34), civ=G(TB, 36, 40), spot_intro=G(TB, 42)[0], tests=G(TB, 43, 45),
        breaker_intro=G(TB, 46)[0], steps=G(TB, 47, 49), qlabel=G(TB, 50)[0], question=G(TB, 51)[0]),
    assemble("normal",
        named=G(NO, 15)[0], definition=G(NO, 17)[0], tactic_lines=G(NO, 18, 24), order=G(NO, 26, 30),
        inst=G(NO, 32, 35), civ=G(NO, 37, 41), spot_intro=G(NO, 43)[0], tests=G(NO, 44, 45),
        breaker_intro=G(NO, 46)[0], steps=G(NO, 47, 49), qlabel=G(NO, 50)[0], question=G(NO, 51)[0]),
]
_named_full = G(SH, 11)[0]
_n, _d = _named_full.split(". ", 1)
USED.remove(_named_full); USED.extend([_n + ".", _d])   # shown on two pages: the name, then the definition
EDU.append(assemble("shame",
    named=_n + ".", definition=_d, tactic_lines=G(SH, 14, 19), order=G(SH, 21, 26),
    inst=G(SH, 28), civ=G(SH, 30), spot_intro=G(SH, 32)[0], tests=G(SH, 33, 35),
    breaker_label="Chain breakers", breaker_intro=None, steps=G(SH, 37, 39), qlabel=None, question=G(SH, 40)[0]))

# lines of the owner's cold opens that the expanded stories must still contain, word for word
KEYQ = {
 "trauma": ["He pushed you when no one else did.", "He believed in you.", "don't have the mental toughness to play at the next level.",
            "He's hard on you because he sees something in you.",
            "Hey — I was tough yesterday because I refuse to let you waste what you have. I don't do that for players I don't believe in. You know that, right?",
            "And just like that — the pain turns into proof of love.", "He made me who I am.", "You're not wrong. That's the problem."],
 "normal": ["We know. There's a waitlist for the free lunch program. We're doing what we can.", "You were devastated. You bought the kid breakfast the next morning.",
            "By the end of year two, you were buying three kids breakfast every morning. You didn't report it anymore. You just handled it. It was just... how things were.",
            "Yeah. It's always been like that. You get used to it.", "Welcome to teaching.",
            "You now teach six straight periods with no break. You eat lunch in four minutes between classes. You haven't used the bathroom during school hours in weeks.",
            "You didn't laugh. But you didn't push back either.", "You haven't changed your values. You still believe class sizes should be smaller, kids shouldn't be hungry, and teachers deserve a break.",
            "You didn't accept these conditions. You were trained to absorb them. One degree at a time, until the water was boiling and you'd stopped noticing the heat."],
 "shame": ["Let's see who came prepared today.", "NOT PREPARED", "This is the third time.", "I'm very disappointed. I expected more from you.",
           "The board gave him the word, and the word gave him permission.", "Let's see if we can keep this going.",
           "The punishment was public. The correction is invisible. The shame stays on the wall."],
}

COVER = {
    "eyebrow": "Combinations · for people who work in schools",
    "title": "Five machines, one school",
    "lede": ("Five stories from inside the same school world: a travel-basketball gym, a middle-school classroom, a sixth-grade whiteboard, "
             "a special-education meeting and a district office. In each one the people are good at what they do, and every sentence anyone says is true. "
             "And in each one a real person still pays a real cost."),
    "body": ("Three of these are the combination scripts I wrote for the Education series. I've kept their breakdowns word for word and expanded their opening scenes into full stories. "
             "The other two I wrote for the people who work in schools, because the pattern runs through their hands too. "
             "Each story shows its tactics in order, then the architecture underneath: why that order works, why the system produces it, "
             "how the same machine runs in an institution and across a society, how to recognise it, and how to start breaking it."),
    "note": "Composites and scripts. They describe a design, not anyone's intent, and not every school or every year.",
}
