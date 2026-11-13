#!/usr/bin/env python3
"""Builds "Why I Wrote This" as HTML. Usage: build.py master|foil  -> why-<edition>.html
Render with render.mjs, then add fill-in fields with fields.py."""
import sys, html, textwrap, pathlib
from data import FAM, TECH, SECT, STAGE, STAGE_COL

ED = sys.argv[1] if len(sys.argv) > 1 else "master"
HERE = pathlib.Path(__file__).parent
E = html.escape
INK, INK2, INK3, LINE, PAPER2, GOLD, WASH = "#16171B", "#45443F", "#6B6860", "#D6CDBD", "#F6F1E7", "#8A5E00", "#F6EBD0"
SANS = "Hanken Grotesk, sans-serif"
_f = [0]

def fld(h=9, cls=""):
    _f[0] += 1; n = _f[0]
    return f'<div class="fld {cls}" style="height:{h}mm"><i class="ta">qa{n:02d}</i><i class="tz">qz{n:02d}</i></div>'
def cb():
    _f[0] += 1
    return f'<span class="cb"><i>qc{_f[0]:02d}</i></span>'

# ---------- SVG helpers ----------
def tx(x, y, s, size=10, w=400, fill=INK, anchor="middle", ls=0, style=""):
    size=round(size*1.07,2)
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {style}>{E(s)}</text>'
def wrapt(x, y, s, n, size=9, w=400, fill=INK2, anchor="middle", lh=None):
    lh = lh or size * 1.28
    return "".join(tx(x, y + i * lh, l, size, w, fill, anchor) for i, l in enumerate(textwrap.wrap(s, n)))
def box(x, y, w, h, fill=PAPER2, stroke=LINE, r=4, sw=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def arrow(x1, y1, x2, y2, col=INK3, sw=1.4, dash=""):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" {d} marker-end="url(#ah{col[1:]})"/>'
def svg(w, h, body, cols=()):
    defs = "".join(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
                   for c in set(cols) | {INK3, GOLD})
    return f'<svg viewBox="0 0 {w} {h}" width="100%" font-family="{SANS}" role="img"><defs>{defs}</defs>{body}</svg>'

def d_machine():
    b = ""
    # frequency ground
    b += box(10, 300, 660, 46, WASH, GOLD, 4, 1.5)
    b += tx(24, 319, "THE ORIGINAL FREQUENCY", 10, 700, GOLD, "start", 1.5)
    b += tx(24, 335, "30 needs you were born with. The ground under everything. Buried, never destroyed.", 9.5, 400, INK2, "start")
    b += tx(656, 327, "Sections 6, 8", 8.5, 600, GOLD, "end")
    # sectors
    b += box(10, 236, 660, 54)
    b += tx(24, 255, "30 SECTORS", 10, 700, INK, "start", 1.5)
    b += tx(24, 271, "A system built around each need: school, clinic, church, bank, feed. Each puts a gate between you and the need.", 9.5, 400, INK2, "start")
    b += tx(656, 263, "Section 6", 8.5, 600, INK3, "end")
    # cycle
    b += box(10, 120, 660, 106)
    b += tx(24, 139, "THE 8-STAGE CYCLE  ·  what happens at every gate", 10, 700, INK, "start", 1.5)
    for i, s in enumerate(STAGE):
        x = 24 + i * 80
        b += box(x, 150, 72, 30, "#fff", STAGE_COL[i], 3, 1.5)
        b += tx(x + 36, 162, str(i + 1), 7.5, 700, STAGE_COL[i]) + tx(x + 36, 174, s[0], 9.5, 650)
        if i < 7: b += arrow(x + 72, 165, x + 80, 165, INK3, 1)
    b += f'<path d="M632 180 Q632 204 600 204 L92 204 Q60 204 60 184" fill="none" stroke="{INK3}" stroke-width="1" stroke-dasharray="3 3" marker-end="url(#ah{INK3[1:]})"/>'
    b += tx(346, 217, "then it restarts on the next person", 8.5, 400, INK3)
    b += tx(656, 139, "Section 4", 8.5, 600, INK3, "end")
    # techniques + combos
    b += box(10, 56, 325, 54) + tx(24, 75, "30 TECHNIQUES", 10, 700, INK, "start", 1.5)
    b += tx(24, 91, "The moves that power each stage. Each one is", 9.5, 400, INK2, "start") + tx(24, 103, "a copy of something real. Section 5", 9.5, 400, INK2, "start")
    b += box(345, 56, 325, 54) + tx(359, 75, "COMBINATIONS", 10, 700, INK, "start", 1.5)
    b += tx(359, 91, "Techniques chained in a set order. This is what", 9.5, 400, INK2, "start") + tx(359, 103, "people actually live through. Section 9", 9.5, 400, INK2, "start")
    b += arrow(172, 110, 172, 120) + arrow(507, 110, 507, 120)
    # levels
    b += box(10, 8, 660, 38, "#fff", INK, 4, 1.2)
    b += tx(24, 31, "3 LEVELS", 10, 700, INK, "start", 1.5)
    b += tx(96, 31, "The same machine runs in a person, in an institution, and across a civilization. That repetition is the fractal.  Section 7", 9.5, 400, INK2, "start")
    return svg(680, 352, b)

def d_gate():
    b = ""
    cols = [("1 · THE NEED", "A real human impulse you were born with", WASH, GOLD),
            ("2 · THE SYSTEM", "Built around the need, to serve it", PAPER2, LINE),
            ("3 · THE GATE", "A condition is added. A gatekeeper stands between you and the need", "#fff", "#D4502F"),
            ("4 · THE INVERSION", "The copy looks like the original. Warmth becomes a hook", PAPER2, LINE),
            ("5 · THE YIELD", "Money, labour, attention, data, compliance, identity", PAPER2, LINE)]
    for i, (t, s, f, st) in enumerate(cols):
        x = 8 + i * 135
        b += box(x, 44, 122, 86, f, st, 4, 1.6 if i in (0, 2) else 1)
        b += tx(x + 61, 62, t, 8.6, 700, INK, "middle", .8) + wrapt(x + 61, 79, s, 22, 9)
        if i < 4: b += arrow(x + 122, 87, x + 135, 87, INK3, 1.4)
    b += tx(8, 22, "THE CAPTURED PATH", 9, 700, "#D4502F", "start", 1.5)
    b += tx(8, 34, "“You belong here, as long as you comply.”", 9.5, 400, INK2, "start", 0, 'font-style="italic"')
    # example row
    ex = ["The child who asks why", "School", "The grade and the ranking", "Worth = the score", "Compliance, then tuition"]
    for i, s in enumerate(ex):
        b += wrapt(8 + i * 135 + 61, 146, s, 24, 8.6, 600, INK3)
    b += tx(8 + 61, 170, "", 8)
    # direct path
    b += f'<path d="M69 176 Q69 214 130 214 L560 214" fill="none" stroke="{GOLD}" stroke-width="2" marker-end="url(#ah{GOLD[1:]})"/>'
    b += box(566, 192, 106, 44, WASH, GOLD, 4, 1.6) + tx(619, 210, "THE NEED, MET", 8.6, 700, GOLD, "middle", .8) + tx(619, 224, "freely, no condition", 9, 400, INK2)
    b += tx(330, 206, "THE ORIGINAL PATH  ·  “You belong.” Full stop.", 9, 700, GOLD, "middle", 1.2)
    b += tx(330, 230, "A question asked and welcomed. A library. A neighbour's help. A hand held.", 9, 400, INK2)
    return svg(680, 240, b, ["#D4502F"])

def d_ring():
    import math
    b = ""; cx, cy, r = 150, 150, 104
    for i, s in enumerate(STAGE):
        a = math.radians(-90 + i * 45); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        a2 = math.radians(-90 + (i + 1) * 45 - 14); a1 = math.radians(-90 + i * 45 + 14)
        b += f'<path d="M{cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f} A{r} {r} 0 0 1 {cx + r * math.cos(a2):.1f} {cy + r * math.sin(a2):.1f}" fill="none" stroke="{INK3}" stroke-width="1.2" marker-end="url(#ah{INK3[1:]})"/>'
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="25" fill="#fff" stroke="{STAGE_COL[i]}" stroke-width="2"/>'
        b += tx(round(x, 1), round(y - 3, 1), str(i + 1), 8, 700, STAGE_COL[i]) + tx(round(x, 1), round(y + 9, 1), s[0], 8.6, 650)
    b += tx(cx, cy - 8, "ONE CYCLE", 9, 700, INK, "middle", 1.5) + tx(cx, cy + 6, "every sector,", 9, 400, INK2) + tx(cx, cy + 18, "every scale", 9, 400, INK2)
    y = 26
    for k, (n, d, c, st) in FAM.items():
        b += f'<rect x="318" y="{y - 9}" width="11" height="11" rx="2" fill="{c}"/>'
        b += tx(336, y, n.upper(), 9, 700, INK, "start", 1) + tx(336, y + 13, f"{st}  ·  {d}", 9, 400, INK2, "start")
        for j, l in enumerate(textwrap.wrap(", ".join(t[0] for t in TECH if t[1] == k), 78)):
            b += tx(336, y + 25 + j * 10.5, l, 7.9, 400, INK3, "start")
        y += 60
    return svg(680, 300, b)

def d_life():
    rows = [("Birth", "Healthcare, Child welfare", "measured and processed in the first minutes"),
            ("0–5", "Family", "the template for love is set, with or without conditions"),
            ("5–12", "Education", "curiosity is graded; worth becomes a letter"),
            ("Teens", "Beauty, Media, Technology, Entertainment, Food, Religion", "body, attention and belonging are claimed"),
            ("Adult", "Finance, Corporate, Housing, Dating, Insurance, Legal", "survival, labour, rest and intimacy are claimed"),
            ("Aging", "Pharmaceuticals, Healthcare, Death", "chemistry, decline and completion are claimed")]
    b = f'<line x1="70" y1="20" x2="70" y2="{20 + len(rows) * 38 - 12}" stroke="{GOLD}" stroke-width="2"/>'
    for i, (a, s, d) in enumerate(rows):
        y = 26 + i * 38
        b += f'<circle cx="70" cy="{y}" r="5" fill="{GOLD}"/>' + tx(58, y + 3.5, a, 9.5, 700, INK, "end")
        b += tx(86, y - 1, s, 9.8, 650, INK, "start") + tx(86, y + 12, d, 9, 400, INK2, "start")
    return svg(680, 20 + len(rows) * 38, b)

def d_levels():
    b = ""; names = [("PERSON", "The pattern wearing a face", "A partner, parent, coach, boss. And the voice in your own head."),
                     ("INSTITUTION", "The pattern wearing a logo", "Policies, billing codes, grading, fine print. It runs even when the staff are kind."),
                     ("CIVILIZATION", "The pattern wearing the sky", "Economy, law, media, “just how things are.” The water the fish can't see.")]
    for i, (n, s, d) in enumerate(names):
        x = 12 + i * 226
        b += box(x, 46, 204, 100, WASH if i == 0 else PAPER2, GOLD if i == 0 else LINE, 4, 1.4)
        b += tx(x + 102, 65, n, 10, 700, INK, "middle", 1.5) + tx(x + 102, 80, s, 9.5, 600, GOLD) + wrapt(x + 102, 97, d, 36, 9)
    R = "#D4502F"
    b += tx(340, 12, "INSTALLED FROM THE OUTSIDE IN", 9, 700, R, "middle", 1.5)
    b += arrow(456, 24, 228, 24, R, 2) + tx(340, 38, "civilization shapes the institution, which shapes the family, which shapes the child", 8.6, 400, INK2)
    b += tx(340, 162, "UNINSTALLED FROM THE INSIDE OUT", 9, 700, GOLD, "middle", 1.5)
    b += arrow(228, 173, 456, 173, GOLD, 2) + tx(340, 190, "one person stops running it, the next generation doesn't receive it, the institution loses its supply", 8.6, 400, INK2)
    ch = [("Nervous system", "A child borrows the caregiver's calm, or their alarm"), ("Attachment", "How we bond is learned in the first years"),
          ("Biology", "Stress can shape the body across generations (my belief; the science is young)"), ("Family story", "“We don't talk about that.”")]
    b += tx(12, 216, "THE FOUR CHANNELS IT TRAVELS THROUGH  (from “The Chain”)", 9, 700, INK, "start", 1.2)
    for i, (n, d) in enumerate(ch):
        x = 12 + i * 167
        b += box(x, 224, 158, 58, "#fff", LINE) + tx(x + 79, 241, n, 9.5, 700) + wrapt(x + 79, 254, d, 30, 8.4)
    b += tx(340, 300, "The same four channels carry the repair: a calm adult, a steady bond, a body allowed to settle, a truer story.", 9.2, 600, GOLD)
    return svg(680, 306, b, [R])

def d_chain(title, steps, conv, cuts, note):
    n = len(steps); w = (664 - (n - 1) * 8) / n; b = ""
    BY, BH = 38, 98; mid = BY + BH / 2
    b += tx(8, 14, title.upper(), 9.5, 700, INK, "start", 1.4)
    for i, (t, d, fam) in enumerate(steps):
        x = 8 + i * (w + 8); c = FAM[fam][2]
        b += box(round(x, 1), BY, round(w, 1), BH, "#fff", c, 4, 1.6)
        b += tx(round(x + 8, 1), BY + 13, str(i + 1), 8, 700, c, "start")
        tl = textwrap.wrap(t, max(9, int(w / 5.9)))
        b += wrapt(round(x + w / 2, 1), BY + 27, t, max(9, int(w / 5.9)), 9, 700, INK, "middle", 11.5)
        b += wrapt(round(x + w / 2, 1), BY + 29 + 11.5 * len(tl), d, max(11, int(w / 4.9)), 8, 400, INK2, "middle", 10)
        if i < n - 1: b += arrow(round(x + w, 1), mid, round(x + w + 8, 1), mid, INK3, 1.2)
    yb = BY + BH; xl = 8 + (n - 1) * (w + 8) + w / 2
    b += f'<path d="M{xl:.1f} {yb} Q{xl:.1f} {yb + 18} 600 {yb + 18} L80 {yb + 18} Q{8 + w / 2:.1f} {yb + 18} {8 + w / 2:.1f} {yb + 4}" fill="none" stroke="{INK3}" stroke-dasharray="3 3" marker-end="url(#ah{INK3[1:]})"/>'
    b += tx(340, yb + 21, "the loop repeats, tighter each time", 8.2, 400, INK3, "middle", 0, 'paint-order="stroke" stroke="#fff" stroke-width="5"')
    for (after, label) in cuts:
        x = 8 + after * (w + 8) - 4
        b += f'<line x1="{x:.1f}" y1="{BY - 8}" x2="{x:.1f}" y2="{yb + 6}" stroke="{GOLD}" stroke-width="2.4"/>'
        b += f'<circle cx="{x:.1f}" cy="{BY - 8}" r="5.5" fill="{GOLD}"/>' + tx(round(x, 1), BY - 5, "✕", 7, 700, "#fff")
    y = yb + 40
    b += tx(8, y, "CHAIN BREAKERS", 8.6, 700, GOLD, "start", 1.4)
    b += tx(118, y, "  ·  ".join(l for _, l in cuts), 9, 600, INK, "start")
    b += tx(8, y + 15, "TURNING POINT", 8.6, 700, "#D4502F", "start", 1.4) + tx(118, y + 15, conv, 9, 400, INK2, "start")
    b += tx(8, y + 30, note, 8.4, 400, INK3, "start", 0, 'font-style="italic"')
    return svg(680, y + 38, b)

def d_loops():
    import math
    b = ""; cx, cy, r = 176, 152, 112
    nodes = [("School", "worth = score"), ("Work", "worth = output"), ("Finance", "debt as leash"), ("Housing", "rest is rented"),
             ("Health cover", "tied to the job"), ("Body", "exhaustion"), ("Family", "pattern repeats")]
    n = len(nodes)
    for i, (t, d) in enumerate(nodes):
        a = math.radians(-90 + i * 360 / n); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        a1 = math.radians(-90 + i * 360 / n + 20); a2 = math.radians(-90 + (i + 1) * 360 / n - 20)
        b += f'<path d="M{cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f} A{r} {r} 0 0 1 {cx + r * math.cos(a2):.1f} {cy + r * math.sin(a2):.1f}" fill="none" stroke="#D4502F" stroke-width="1.5" marker-end="url(#ahD4502F)"/>'
        b += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="44" ry="22" fill="#fff" stroke="{INK}" stroke-width="1.1"/>'
        b += tx(round(x, 1), round(y - 1, 1), t, 9.6, 700) + tx(round(x, 1), round(y + 10, 1), d, 7.8, 400, INK2)
    b += tx(cx, cy - 6, "THE", 8.6, 700, "#D4502F", "middle", 1.4) + tx(cx, cy + 6, "DEPENDENCY", 8.6, 700, "#D4502F", "middle", 1.4) + tx(cx, cy + 18, "LOOP", 8.6, 700, "#D4502F", "middle", 1.4)
    b += tx(176, 298, "Each capture makes the next one harder to refuse.", 9, 600, INK2)
    # repair loop
    x0 = 384
    b += tx(x0, 22, "THE REPAIR LOOP", 9, 700, "#0F8F84", "start", 1.4)
    b += tx(x0, 36, "The cycle sells the cure for its own harm.", 9.2, 400, INK2, "start")
    rr = [("First-order sectors", "school, work, finance, food, media", PAPER2, LINE), ("The cost lands in the body", "stress, loneliness, exhaustion, fear", "#fff", "#D4502F"),
          ("Repair sectors", "wellness, therapy, pharma, insurance, self-help", PAPER2, LINE), ("Symptom managed, cause untouched", "you return to the same conditions", "#fff", "#0F8F84")]
    for i, (t, d, f, st) in enumerate(rr):
        y = 48 + i * 56
        b += box(x0, y, 296, 40, f, st, 4, 1.3) + tx(x0 + 148, y + 17, t, 9.6, 700) + tx(x0 + 148, y + 30, d, 8.6, 400, INK2)
        if i < 3: b += arrow(x0 + 148, y + 40, x0 + 148, y + 56, INK3, 1.3)
    b += f'<path d="M{x0 + 296} 236 Q{x0 + 312} 236 {x0 + 312} 200 L{x0 + 312} 90 Q{x0 + 312} 68 {x0 + 298} 68" fill="none" stroke="{INK3}" stroke-dasharray="3 3" marker-end="url(#ah{INK3[1:]})"/>'
    b += tx(x0 + 148, 280, "The break: ask of any remedy, “does this return me", 9, 600, INK2) + tx(x0 + 148, 292, "to myself, or to the thing that hurt me?”", 9, 600, INK2)
    return svg(712, 304, b, ["#D4502F", "#0F8F84"])

def d_change():
    st = [("NAME", "A word for each move", "The Fractal · Pattern Decoder"), ("RECOGNIZE", "See it while it's happening", "30 sectors · 3 levels"),
          ("PAUSE", "The gap between the move and your response", "The Body · The Frequency"), ("CHOOSE", "The original instead of the copy", "30 practices · chain breakers"),
          ("TRANSMIT", "Children and peers receive a new signal", "The Chain · Playground Protectors"), ("REDESIGN", "Build systems the pattern can't enter", "War Map · self-audit rubric")]
    b = ""
    for i, (t, d, src) in enumerate(st):
        x = 6 + i * 113
        b += box(x, 22, 104, 96, WASH if i == 2 else "#fff", GOLD, 4, 1.8 if i == 2 else 1.2)
        b += tx(x + 52, 40, t, 9.6, 700, GOLD, "middle", 1.3) + wrapt(x + 52, 56, d, 19, 8.8, 500, INK)
        b += wrapt(x + 52, 98, src, 22, 7.4, 400, INK3, "middle", 9)
        if i < 5: b += arrow(x + 104, 70, x + 113, 70, INK3, 1.3)
    b += tx(6, 12, "INNER", 8.4, 700, INK3, "start", 1.4) + tx(345, 12, "BETWEEN PEOPLE", 8.4, 700, INK3, "middle", 1.4) + tx(676, 12, "STRUCTURAL", 8.4, 700, INK3, "end", 1.4)
    b += f'<line x1="50" y1="9" x2="270" y2="9" stroke="{LINE}"/><line x1="420" y1="9" x2="600" y2="9" stroke="{LINE}"/>'
    b += tx(340, 136, "Every step depends on the one before it. Nothing structural holds unless enough people can first name what they're looking at.", 9, 600, INK2)
    return svg(682, 142, b)

def d_states():
    rows = [("SAFE AND SOCIAL", "The body opens: warmth, eye contact, belonging", "Seduction", "sed", "Signals of safety are copied. The body bonds before the mind can evaluate."),
            ("ALARM", "Fight or flight: racing, scanning, bracing", "Destabilization · Isolation", "des", "Contradiction and threat keep the body busy surviving, so it can't step back and see."),
            ("SHUTDOWN", "Collapse: numb, flat, “what's the point”", "Extraction · Disposal", "ext", "Effort stops being tried. Taking meets no resistance. The body calls it peace.")]
    b = ""
    for i, (s, d, f, k, why) in enumerate(rows):
        y = 6 + i * 58; c = FAM[k][2]
        b += box(6, y, 190, 50, "#fff", c, 4, 1.8) + tx(101, y + 20, s, 9.6, 700, c, "middle", 1.3) + wrapt(101, y + 34, d, 40, 8.4)
        b += arrow(196, y + 25, 222, y + 25, INK3, 1.3)
        b += box(224, y, 150, 50) + tx(299, y + 22, "ridden by", 8, 400, INK3) + tx(299, y + 36, f, 9.4, 700)
        b += wrapt(388, y + 20, why, 56, 9, 400, INK2, "start", 12)
    return svg(680, 180, b)

# ---------- content ----------
def stage_table():
    r = "".join(f'<tr><td><b style="color:{STAGE_COL[i]}">{i + 1}. {s[0]}</b></td><td>{E(s[1])}<br><span class="q">{E(s[3])}</span></td><td>{E(s[2])}</td><td class="ps">{E(s[4])}</td><td class="sp">{E(s[5])}</td></tr>' for i, s in enumerate(STAGE))
    return f'<table class="small"><tr><th>Stage</th><th>What it looks and sounds like</th><th>What it actually is</th><th class="ps">The real need it copies</th><th class="sp">The spiritual principle it inverts</th></tr>{r}</table>'

def tech_table(keys):
    out = '<table class="small tech"><tr><th>The inversion (technique)</th><th class="ps">The original it copies</th><th class="sp">The sacred faculty</th><th>How the copy works</th><th>The practice that restores the original</th></tr>'
    for k in keys:
        n, d, c, st = FAM[k]
        out += f'<tr><td colspan="5" class="fam" style="border-left:4px solid {c}"><b style="color:{c}">{n}</b> · {d} · stages: {st}</td></tr>'
        for t in TECH:
            if t[1] == k:
                out += f'<tr><td><b>{E(t[0])}</b></td><td class="ps"><b>{E(t[2])}</b></td><td class="sp">{E(t[3])}</td><td>{E(t[4])}</td><td>{E(t[5])}</td></tr>'
    return out + "</table>"

def sect_table(a, b):
    out = '<table class="small sect"><tr><th>#</th><th>Sector</th><th>Our relationship with…</th><th class="ps">The original impulse</th><th>The gate that was installed</th><th>One way to reclaim it</th></tr>'
    for i, s in enumerate(SECT[a:b], a + 1):
        out += f'<tr><td class="n">{i}</td><td><b>{E(s[0])}</b></td><td>{E(s[1])}</td><td class="ps">{E(s[2])}</td><td>{E(s[4])}</td><td>{E(s[5])}</td></tr>'
    return out + "</table>"

def matrix():
    rows = [("Warmth, praise or promises arriving faster than you know the person or place", "Love bombing", "Idealize", "Genuine welcome", "“I'll take a few days.” Watch what happens to the warmth when you slow down."),
            ("“After all we've done for you…” when you hesitate or say no", "Weaponized generosity", "Hook", "Clean giving", "Ask yourself: was I ever free not to repay this? Thank them, and still decide freely."),
            ("The reward is always one more step away", "Future faking · Moving the goalposts", "Hook · Confuse", "Arrival", "Write down what was promised and what was delivered. Set your own finish line."),
            ("Approval that used to be free now depends on performance", "Devaluation", "Devalue", "Inherent worth", "Separate the feedback about the work from the verdict on the person."),
            ("You leave a conversation doubting what you clearly remember", "Gaslighting", "Confuse", "Self-trust", "Write it down the same day. Check it with one outside person."),
            ("You raise a concern and end up apologizing", "DARVO · Projection", "Confuse", "Holding the naming", "Return once to the original point: “I'd like to go back to what I raised.”"),
            ("“That's just how it is here.” Everyone has stopped noticing", "Normalization", "Confuse", "Recalibration", "Ask what a newcomer would think. Ask what you thought on day one."),
            ("You're hearing about someone through someone else", "Triangulation · Flying monkeys", "Isolate", "Direct relationship", "Go to the person directly. Answer the source, not the messenger."),
            ("Outside friends, activities or opinions are quietly discouraged", "Isolation", "Isolate", "Genuine connection", "Protect one relationship and one activity that sit fully outside."),
            ("Your concern gets no reply at all", "Silent treatment", "Isolate", "Responsive presence", "State it once in writing, with a date. Don't chase."),
            ("Cold, then suddenly kind, then cold again, and you live for the kind days", "Intermittent reinforcement · Trauma bonding", "Extract", "Steady presence · Safe attachment", "Name the swing. Spend time with someone who is the same every day."),
            ("“It's for your own good.” Decisions are made about you, without you", "Benevolent control · Infantilization", "Extract", "Self-governance", "Ask who it protects. Ask for a say, and for the reasons in writing."),
            ("You've stopped trying because trying made it worse", "Learned helplessness", "Extract", "One completed action", "Choose one small thing and finish it today."),
            ("“Decide now.” There is suddenly no time to think", "Manufactured crisis", "Discard", "Deliberate response", "“If I wait a day, who is harmed?” Real emergencies survive that question."),
            ("“We followed the process.” Harm, and nobody responsible", "Plausible deniability", "Replace", "Witnessing", "Dates, names, copies. Ask who made the decision and how to appeal it.")]
    out = '<table class="small mx"><tr><th>What you notice (behaviour)</th><th>Likely technique</th><th>Stage</th><th class="ps">The original need underneath</th><th>First chain breaker</th></tr>'
    for a, b, c, d, e in rows:
        out += f'<tr><td>{E(a)}</td><td><b>{E(b)}</b></td><td>{E(c)}</td><td class="ps">{E(d)}</td><td>{E(e)}</td></tr>'
    return out + "</table>"

def rubric():
    rows = [("Idealize", "Do we promise more at the door than we deliver inside?", "Recruitment, enrolment and welcome material match the daily reality. Nobody is rushed to commit."),
            ("Hook", "Is leaving made costly, shameful or confusing?", "A clear, penalty-free way to leave, change course or opt out, explained at the start."),
            ("Devalue", "Is a person's worth tied to a single measure?", "Feedback is about the work, not the person. No public ranking of people. More than one way to succeed."),
            ("Confuse", "Do the rules change, or contradict what we say?", "Rules are written, stable and applied the same way. People are told the reasons. Questions are welcome."),
            ("Isolate", "Do we discourage outside voices or comparison?", "Families, advocates and second opinions are invited in. People can compare notes without penalty."),
            ("Extract", "Do we take more than we return, from those least able to refuse?", "We know what we ask of people (time, money, data, effort) and can show what they get back."),
            ("Discard", "What happens to people who stop being useful or easy?", "Nobody leaves without a conversation, a reason and a next step. Exclusion is the last resort, with a way back."),
            ("Replace", "When harm happens, can anyone be found responsible?", "A named person answers complaints. Outcomes are recorded and reviewed. We look for patterns, not just cases.")]
    out = '<table class="small rb"><tr><th>#</th><th>Stage it guards against</th><th>The question</th><th>What a clean design looks like</th><th>Yes</th><th>Partly</th><th>No</th></tr>'
    for i, (s, q, c) in enumerate(rows):
        out += f'<tr><td class="n">{i + 1}</td><td><b style="color:{STAGE_COL[i]}">{s}</b></td><td><b>{E(q)}</b></td><td>{E(c)}</td><td>{cb()}</td><td>{cb()}</td><td>{cb()}</td></tr>'
    return out + "</table>"

CH1 = d_chain("The Trauma Bond Engine  ·  harm and warmth from the same source",
    [("Intermittent reinforcement", "warm, then silent, then warm", "des"), ("Trauma bonding", "relief and pain from one source", "ext"), ("Relief bait", "the full apology, just before a request", "sed"),
     ("Push-pull", "close, then distant", "des"), ("Fear, obligation, guilt", "the decision is loaded", "iso"), ("Hoovering", "“we miss you”", "sed"), ("Conditional love", "your answer = your loyalty", "ext")],
    "warmth and a demand arrive in the same week, and you are asked to decide while attached.",
    [(1, "Slow the clock"), (3, "Move it to writing"), (5, "Ask an outside person first"), (6, "Decide the terms before the feelings")],
    "Sequence from my Fractal² combination of the same name. Unpredictable kindness has to come first, or there is no bond to pull on.")
CH2 = d_chain("The Compliance Engine  ·  obedience built from small, reasonable steps",
    [("Behaviour control", "daily choices move into other hands", "ext"), ("Trivial demands", "small, checkable rules", "ext"), ("Relief for obeying", "comply and the coldness lifts", "des"), ("Intermittent reward", "same act, different response", "des"),
     ("Conditional love", "belonging is the prize", "ext"), ("Group pressure", "everyone else complies", "iso"), ("Punished boundaries", "stories of who pushed back", "iso"), ("Finished decisions", "resistance seems pointless", "dis")],
    "the day you agree before you have thought. After that, the enforcement is inside you.",
    [(1, "Ask for the rule and its scope in writing"), (3, "Keep your own dated record"), (5, "Independent advice"), (6, "One peer who says it out loud")],
    "Sequence from my Fractal² combination of the same name.")
CH3 = d_chain("Curiosity to Compliance  ·  a school-based chain",
    [("Love bombing", "gold star: “you're special”", "sed"), ("Devaluation", "the star is withheld", "des"), ("Moving the goalposts", "the bar rises each time", "des"), ("Normalization", "stop asking the odd questions", "des"),
     ("Identity erosion", "“I'm a C student”", "ext"), ("Learned helplessness", "“why try?”", "ext"), ("Future faking", "“it will pay off later”", "sed")],
    "the child stops raising a hand unless sure of the wanted answer. Curiosity has become risk.",
    [(1, "Praise the question, not only the answer"), (2, "Separate worth from the score"), (4, "Name strengths no test measures"), (5, "One adult who stays curious with them")],
    "I drew this chain from the Education chapter of The Fractal. It describes a pattern in a system, not the intent of any teacher.")

def body():
    foil = ED == "foil"
    P = []
    a = P.append
    a(f'''<section class="cover"><img src="../../art/fractal-original-1600.webp" alt="">
<div class="t"><div class="k">The Fractal · the map and what it is for</div><h1>Why I Wrote This</h1>
<p>One pattern, running in every part of life. What it is, how to see it whatever you believe, and what it can become once people share the map.</p>
<div class="m">Shae Stovell · Noble Father Creations · November 2026{"<br>Personal edition for Von “Foil” Saunders" if foil else ""}</div></div></section>''')
    if foil:
        a('''<section class="letter pb"><div class="kick">A personal note</div><h2>Foil,</h2>
<p class="lede">I'm putting this in your hands first because you spend your working life where this pattern is installed earliest, and where it is easiest to interrupt: with children, inside a school system.</p>
<p>You know I've been writing for a long time. What you may not know is how big it became. I started with one question: why does the cycle people describe after a manipulative relationship keep showing up in places that have nothing to do with romance? I followed it through thirty parts of life. Then I mapped it at full resolution. Then I mapped the sequences people actually live through, and how each one breaks. Along the way I wrote a book for my daughter, so she would have the words before she needed them.</p>
<p>This document is the short version of all of it. I wrote it so that someone with your training could see the whole architecture in one sitting and judge it properly.</p>
<p><strong>What I hope you see.</strong> First, that the core is not exotic. It is coercive control, attachment, conditioning and co-regulation, arranged into one map that an ordinary parent or teenager can use. Second, that the map is strict about its own limits: it marks what is documented, what is my synthesis and what is my faith, and it says plainly that it replaces no clinician. Third, that the most useful part may be the least dramatic one: a shared, plain vocabulary that lets a child, a parent, a teacher and a psychologist describe the same thing in the same words.</p>
<p><strong>What I'd like from you</strong> is on the last page, kept separate so the rest can travel without it. In short: your honest read, and if it earns it, a few introductions.</p>
<p>Where you think I'm wrong, I want to hear that most. You'll notice I say in several places that some of this is belief and not settled science. I'd rather you sharpen it than be polite about it.</p>
<p>Start with the map on the next page, then Sections 8, 11 and 14. Those are the ones closest to your work.</p>
<p class="sig">With respect and thanks,<br>Shae</p></section>''')

    # ---- quick start
    a(f'''<section class="pb" id="qs"><div class="kick">Quick start · how to read this map</div><h2>One machine, five parts</h2>
<p class="lede">Everything I've written describes one machine. Read this page and you can find your way through the rest.</p>
<figure class="fig">{d_machine()}</figure>
<p>Read it from the bottom up. <strong>You were born with needs.</strong> A system grew around each one. At the door of each system the same eight-stage cycle runs, powered by the same thirty moves, usually chained into combinations. And it runs the same way in a person, an institution and a whole society. Underneath all of it, the original needs are still there. That last part is the reason I wrote any of this.</p>
<div class="three">
<div><b>If you're a general reader</b><p class="small">Sections <a href="#s1">1</a>, <a href="#s4">4</a> and <a href="#s8">8</a>, then use the <a href="#s13">tools in 13</a> on one real situation from your own life. About 25 minutes.</p></div>
<div><b>If you're a parent</b><p class="small">Sections <a href="#s4">4</a>, <a href="#s7">7</a> (how it passes between generations), <a href="#s9">9</a> (the school chain) and <a href="#s14">14</a>. Then the practices in the sector table.</p></div>
<div><b>If you're an educator or clinician</b><p class="small">Sections <a href="#s3">3</a>, <a href="#s8">8</a>, <a href="#s9">9</a>, the <a href="#rubric">self-audit rubric in 13</a>, <a href="#s14">14</a> and the <a href="#s16">limits in 16</a>.</p></div>
</div>
<p class="small">The tables are meant to be scanned, not read line by line. Blue columns show the original need. Purple columns show my spiritual reading, which you can skip without losing the structure. The worksheets in Section 13 can be typed into on a screen or printed.</p></section>''')

    toc = [("s1","Why these books exist"),("s2","What I built, in numbers"),("s3","Three lenses, one shape"),("s4","The cycle: eight stages, and the garden and the gate"),
           ("s5","Originals and inversions: the thirty techniques"),("s6","The thirty sectors and our relationship to each need"),("s7","The fractal: three levels, and how it passes on"),
           ("s8","The frequency: why it feels familiar, and what interrupts it"),("s9","The combinations: why order matters"),("s10","What the whole map shows that no chapter says"),
           ("s11","What a clean system looks like"),("s12","The war map: how this turns into real change"),("s13","Tools: trace it, interrupt it, audit your own system"),
           ("s14","Children and schools"),("s15","What this can become"),("s16","What this is and is not")]
    a('<section class="pb"><div class="kick">Contents</div><table class="toc">' + "".join(f'<tr><td class="n">{i + 1}</td><td><a href="#{k}">{t}</a></td></tr>' for i, (k, t) in enumerate(toc)) + '</table>')

    a('''<div class="sec" id="s1"><div class="kick">1 · Why</div><h2>Why these books exist</h2>
<p class="lede">I started with one thing: the cycle people describe when they leave a manipulative relationship. Idealize, hook, devalue, confuse, isolate, extract, discard, replace. Then I kept finding it in places that had nothing to do with romance.</p>
<p>I found it in schools, hospitals, workplaces, churches, housing, food, media, borders and prisons. The same eight stages, the same moves, in the same order. I wrote one sector at a time, thirty of them. By the end I wasn't looking at thirty problems. I was looking at one pattern in thirty costumes.</p>
<p>The core idea fits in a sentence: <strong>every human need was meant to be met, and a pattern has learned to stand between people and their needs, copy the real thing, and charge for access.</strong> The original says “you are loved.” The copy says “you are loved, when you perform.” My whole body of work lives in that added condition.</p>
<p>I wrote it for three reasons.</p>
<ol><li><strong>To give people words for what happened to them.</strong> Most people who've been through coercive control can't name it. They only know something was taken. Naming each move turns “something is wrong with me” into “something was done to me.” That shift is where healing starts.</li>
<li><strong>To show that the personal and the institutional are one pattern.</strong> When someone sees that their school, their employer and their family ran the same cycle, they stop blaming themselves for being “too sensitive” in each place separately.</li>
<li><strong>To hand people tools, not only a diagnosis.</strong> Every move has a practice that restores the original. Every combination has chain breakers: specific first steps for taking it apart.</li></ol>
<div class="pull">The pattern is not hidden. It is everywhere, which is why it can't be seen. A pattern that has been seen can't pretend to be the sky anymore.</div>
<p>One thing I want to be clear about from the start. The pattern does not need bad people. It needs structures that sit between a person and a need, with a power gap and a gatekeeper. Kind, skilled people work inside those structures every day and the cycle runs through their hands anyway. So this is not a book of villains. It is a book about a design, and designs can be changed.</p></div>''')

    a('''<div class="sec" id="s2"><div class="kick">2 · The body of work</div><h2>What I built, in numbers</h2>
<div class="nums"><div><b>8</b><span>stages in one repeating cycle</span></div><div><b>30</b><span>techniques that power it</span></div><div><b>3</b><span>levels: person, institution, civilization</span></div><div><b>30</b><span>sectors of life, birth to death</span></div><div><b>2,700</b><span>worked examples in The Fractal (30 × 30 × 3)</span></div></div>
<div class="nums"><div><b>335</b><span>specific tactics mapped in the first full Fractal² sector</span></div><div><b>153</b><span>combinations written for that sector</span></div><div><b>34</b><span>religious traditions compared in The Sacred Divide</span></div><div><b>28</b><span>missions in my children's book, Playground Protectors</span></div><div><b>1</b><span>pattern underneath all of it</span></div></div>
<table><tr><th>Work</th><th>What it is</th><th>The question it answers</th></tr>
<tr><td><b>The Fractal</b></td><td>30 sectors, each walked through all 30 techniques at 3 levels. Then four closing chapters: The Mirror (the pattern in yourself), The Body (in the nervous system), The Chain (across generations) and The Frequency (what survived).</td><td><em>Where</em> does it run? Everywhere, and the repetition is the evidence.</td></tr>
<tr><td><b>Fractal²</b></td><td>Each sector at full resolution: 300+ named tactics, so a reader can find the exact thing that was done to them.</td><td><em>What exactly</em> happens?</td></tr>
<tr><td><b>The Combinations</b></td><td>100+ per sector. How single moves chain into the compound patterns people live through, why the order matters, and how each one breaks.</td><td><em>How</em> does it work on a person, and <em>how do you get out?</em></td></tr>
<tr><td><b>The Sacred Divide</b></td><td>34 traditions, each examined through the same 27 sections.</td><td>How have the world's traditions named the counterfeit?</td></tr>
<tr><td><b>The Pattern Decoder</b></td><td>310 tactics in plain words, each with “Is this it?” and “What you can do,” written for someone who is hurting and unsure.</td><td>What is this, and what do I do today?</td></tr>
<tr><td><b>Playground Protectors</b></td><td>A children's book: 28 missions that teach kids to spot, name and handle “tricky” behaviour, with words to say and a clear rule for when to tell a trusted adult.</td><td>How do we give children the words <em>before</em> they need them?</td></tr></table>
<p class="small">Everything is free to read. That is deliberate: a map of how access gets gated should not have a gate on it.</p></div>''')

    a('''<div class="sec" id="s3"><div class="kick">3 · Reading it whatever you believe</div><h2>Three lenses, one shape</h2>
<p class="lede">My own lens is spiritual. I see this pattern as a counterfeit of something sacred. But the map doesn't depend on my faith. Swap “divine design” for “basic human need” and every chart here still holds.</p>
<div class="lens2"><div class="sp"><b>Spiritual reading</b><p>The “false god” is not a being. It is the pattern itself. It cannot create. It can only copy. It wears the face of the real thing and puts a gatekeeper between people and what they were made for.</p></div>
<div class="ps"><b>Psychological reading</b><p>It is the coercive-control cycle that clinicians describe in abusive relationships: idealization, intermittent reward, devaluation, confusion, isolation, dependency. The same mechanics appear in groups and organizations.</p></div>
<div class="cv"><b>Civilizational reading</b><p>No villain is required. Wherever there is a real need, a power gap and a gatekeeper, the same incentives produce the same cycle: warmth to recruit, conditions to retain, extraction, replacement.</p></div></div>
<p>All three agree on four things. The need is real and is not a weakness. The harm comes from the condition added to the need. The pattern runs best when nobody names it. And seeing it clearly is the first step out.</p>
<h3>How the traditions name it</h3>
<p>Many traditions have a name for something that copies or hides what is real. They disagree about what lies underneath: God, a true self, or no fixed self at all. I don't claim they say the same thing. What they share is narrower: <strong>something obscures the real, and freedom begins with seeing it.</strong></p>
<table class="small"><tr><th>Tradition</th><th>Its word or image</th><th>What it points to</th><th>How it names the way through</th></tr>
<tr><td><b>Christianity</b></td><td>The counterfeit; “an angel of light”</td><td>Deception that looks like the good it replaces</td><td>The narrow gate; the kingdom within</td></tr>
<tr><td><b>Islam</b></td><td><em>Nafs</em> (the commanding self); <em>ghafla</em> (heedlessness)</td><td>Forgetting what is real; appetite steering the person</td><td>Lifting the veils; remembrance</td></tr>
<tr><td><b>Buddhism</b></td><td><em>Avidyā</em> (not-seeing)</td><td>Suffering held in place by misperception</td><td>Clear seeing; waking up</td></tr>
<tr><td><b>Hinduism (Vedanta)</b></td><td><em>Māyā</em></td><td>Appearance taken for reality</td><td><em>Tat tvam asi</em>: recognizing what you already are</td></tr>
<tr><td><b>Judaism (Kabbalah)</b></td><td>The broken vessels</td><td>Sparks of light trapped in the shards</td><td><em>Tikkun olam</em>: gathering the sparks, repairing the world</td></tr>
<tr><td><b>Indigenous teaching</b></td><td><em>Wetiko</em>; the forgotten original instructions</td><td>A sickness of consuming others that spreads</td><td>Remembering; returning to right relationship</td></tr>
<tr><td><b>Secular</b></td><td>Conditioning; incentive structures</td><td>Learned patterns that run without anyone choosing them</td><td>Observation, naming, redesign</td></tr></table>
<p class="small">My invitation is the one I give in the series: whatever tradition you carry, or don't, bring it with you. If what I describe is real, your own framework will recognize it.</p></div>''')

    a(f'''<div class="sec" id="s4"><div class="kick">4 · The cycle</div><h2>Eight stages, and the garden and the gate</h2>
<p class="lede">Each stage is the exact reverse of a real need being met. That precision is why it's so hard to see: it looks like the real thing until the condition appears.</p>
{stage_table()}
<h3>The garden and the gate</h3>
<p>This is the picture I keep coming back to. Every sector began as a garden: a place where a need was meant to be met freely. Then a gate was installed. In the old story an angel with a flaming sword guards the way back. Today the sword is an ordinary object: a billing department, a ranking, a mortgage, a login.</p>
<figure class="fig">{d_gate()}<figcaption>The need on the left is real in both paths. What differs is the condition. The top path adds one and takes a yield. The bottom path meets the need and asks nothing back.</figcaption></figure>
<div class="box keep"><h4>The same cycle in the oldest story</h4><p>Read the Garden of Eden, as history or as myth, and all eight stages are there. The serpent promises (“you will be like God”), hooks with a future (“your eyes will be opened”), and the first result is shame (“they knew they were naked”). Blame splits the relationships three ways, labour becomes extraction, they are expelled, and the way back is guarded. One detail matters most: the serpent's first words are “Did God really say…?” <strong>Confusion came first. A person who trusts their own perception cannot be idealized.</strong> The compass has to be broken before the journey can be redirected.</p></div>
<h3>The cycle as a checklist</h3>
<table class="small">{"".join(f'<tr><td><b style="color:{STAGE_COL[i]}">{s[0]}</b></td><td>{E(s[6])}</td></tr>' for i, s in enumerate(STAGE))}</table>
<p class="small">If you can tell which stage you're in, the cycle can no longer run unnoticed. Running unnoticed is the only way it works.</p></div>''')

    a(f'''<div class="sec" id="s5"><div class="kick">5 · Originals and inversions</div><h2>The thirty techniques, and what each one copies</h2>
<p class="lede">If the eight stages are what the pattern <em>is</em>, the thirty techniques are what it <em>does</em>. None of them is an invention. Each is a copy of something good, run backwards.</p>
<figure class="fig">{d_ring()}<figcaption>Five families of technique power the eight stages. Colours match the tables that follow.</figcaption></figure>
<p>Read each row left to right: the move, the real thing it imitates, the sacred faculty I see behind it, how the copy differs from the original, and the practice that brings the original back. The originals come from the closing chapter of <em>The Fractal</em>, “The Frequency.”</p>
{tech_table(["sed", "des"])}</div>
<div class="sec">{tech_table(["iso", "ext", "dis"])}
<div class="box keep"><h4>How to tell the original from the copy</h4><p>Across all thirty, the copy differs from the original in the same four ways. The copy is <strong>fast</strong> where the original is patient. It is <strong>conditional</strong> where the original is free. It <strong>keeps a ledger</strong> where the original lets go. And it <strong>needs you not to check</strong>, where the original is comfortable being examined. Those four tests work on a person, a program or a policy.</p></div>
<h3>The same techniques, turned inward</h3>
<p>The hardest chapter I wrote is “The Mirror.” It runs all thirty techniques on the self: self-gaslighting (“it wasn't that bad”), self-devaluation, moving your own goalposts, discarding the parts of you that didn't fit. These are habits learned from the systems around us, now running without anyone else in the room. The inner critic is a committee of old voices (a parent, a teacher, an ex, a culture) that was never elected and always votes against your freedom. Each inward technique ends with an honest version: what to do instead.</p></div>''')

    a(f'''<div class="sec" id="s6"><div class="kick">6 · The sectors</div><h2>Thirty sectors, and our relationship to each need</h2>
<p class="lede">Every sector of society began with a real human impulse. Each now stands between people and that impulse. Read the third column straight down and you see the scope: no part of life is left out.</p>
{sect_table(0, 15)}</div>
<div class="sec">{sect_table(15, 30)}
<p class="small">Original impulses are from “The Frequency.” The gates are from “The Spiritual Lens,” where I call each one a flaming sword. The practices are deliberately small. None of them asks anyone to abandon a doctor, a school or a job.</p>
<h3>A life inside the cycle</h3>
<p>The sectors don't wait for us to choose them. They meet us in order.</p>
<figure class="fig">{d_life()}<figcaption>From “The Pattern.” There is no age at which a person stands outside the cycle. That is why the earliest years matter most.</figcaption></figure>
<div class="box keep"><h4>One ordinary day</h4><p>The alarm is on the device that tracked your sleep (technology). The feed has already chosen what you see (media). Breakfast was engineered to taste like food (food). The mirror tightens your chest (beauty). You drive the car you're paying off (finance), covered by insurance you can't legally drive without. Your health cover is tied to the job, so you can't leave the job (corporate plus healthcare). Your child was graded today (education). You lie down in the house the bank owns (housing). Nothing dramatic happened. That is the point. The cycle didn't pause for a single hour, and none of it felt like a cycle.</p></div>
<p><strong>The thirty are not thirty things.</strong> They are one thing, a human being alive, seen through thirty windows. When I group the original impulses, they fall into six roots:</p>
<table class="small"><tr><th>Root need</th><th>Original impulses that belong to it</th><th>Sectors built on top</th></tr>
<tr><td><b>A body at home</b></td><td>To heal, eat, rest, move, be whole, decide what enters you, finish life in peace</td><td>Healthcare, Food, Housing, Sports, Beauty, Pharmaceuticals, Aging and death</td></tr>
<tr><td><b>A mind that knows</b></td><td>To ask why, to understand, to witness the truth, to own your inner world</td><td>Education, Science, Media, Mental health</td></tr>
<tr><td><b>A bond that holds</b></td><td>To be loved without earning it, to be known, to be held and chosen as a child</td><td>Family, Dating, Child welfare</td></tr>
<tr><td><b>A place among others</b></td><td>To decide together, to be treated fairly, to help, to protect, to belong where you stand</td><td>Politics, Legal system, Nonprofits, Military, Immigration, Incarceration</td></tr>
<tr><td><b>Work and provision</b></td><td>To make, to exchange, to have enough, to extend your reach with tools, to feel safe</td><td>Corporate, Finance, Technology, Insurance, Transportation</td></tr>
<tr><td><b>Meaning and expression</b></td><td>To touch the sacred, to express and be seen, to heal the wound, to be private, to belong to the earth</td><td>Religion, Entertainment, Wellness, Surveillance, Energy and environment</td></tr></table></div>''')

    a(f'''<div class="sec" id="s7"><div class="kick">7 · The fractal</div><h2>Three levels, and how the pattern passes on</h2>
<p class="lede">A fractal is a shape that repeats at every scale. This pattern does. That is why it's hard to see, and why changing it at one scale changes it at the others.</p>
<figure class="fig">{d_levels()}</figure>
<p>The levels nest. The person is inside the institution. The institution is inside the civilization. And the civilization's pattern is inside the person, as habits, expectations and an inner voice. The second level explains something that puzzles people: why good staff inside a system still produce harm. The design was there before they arrived.</p>
<p><strong>The pattern is the same for everyone. The pressure is not.</strong> The same technique lands harder on some bodies than others, by race, class, sex, disability, age and status. The people it presses hardest are usually the people least believed when they describe it. That disbelief is the cycle too. I ask every reader to carry one question through the whole map: <em>on whom does this land hardest, and whose account of it is most doubted?</em></p>
<h3>Why the direction can reverse</h3>
<p>The pattern came in from the outside. A civilization shaped its institutions, the institutions shaped families, families shaped children, and children grew an inner voice that carried it on. Each link is a relationship. So each link can carry something else. When one adult catches the old response and chooses differently, a child receives a signal that was never in the family line before. That child grows up needing less from the systems that feed on unmet need. This is slow, and it is real. It is the mechanism I trust most in everything I've written.</p></div>''')

    a(f'''<div class="sec" id="s8"><div class="kick">8 · The frequency</div><h2>Why the pattern feels familiar, and what interrupts it</h2>
<p class="lede">People often ask me why they walked into the same situation three times. My answer: the body recognized it. Familiar and safe feel the same from the inside, and the pattern was built on that.</p>
<h3>What I mean by frequency</h3>
<p>Before the cycle there was something else. Before love bombing there was love. Before gaslighting there was knowing. Before isolation there was belonging. I call that original signal the frequency. It is not a mood or a peak experience. <strong>It is the ground, not the high.</strong> It feels like an ordinary Tuesday morning when, for a few minutes before the phone, you feel okay. Not fixed. Not triumphant. Present. The cycle can't sell you that, which is why it has to keep you from noticing it.</p>
<p>The cycle can capture an impulse. It can't kill it. School can punish the question until a child asks silently, but the child still wonders. The impulses are overgrown, like a forest trail nobody has walked for years. The trail is still there, and it clears one step at a time.</p>
<h3>Why it feels like home</h3>
<p>Here is the mechanism as I understand it. I present the body science as my reading of it, not as settled fact.</p>
<ul><li><strong>The body responds to the signal, not the intent.</strong> Warmth, eye contact and welcome are real signs of safety. The body can't tell whether they are sincere or strategic. It opens first. The mind evaluates later, if at all. So a bond can form before any judgment has been made.</li>
<li><strong>We are tuned by the people who raised us.</strong> A baby can't calm itself. It borrows an adult's nervous system and builds its own on that template. Whatever rhythm filled the first home (steady, or hot and cold) becomes the rhythm the body reads as normal. I call that tuning.</li>
<li><strong>So the familiar pulls.</strong> A person raised on unpredictable warmth will find steady kindness flat and intermittent kindness magnetic. That isn't weakness or bad judgment. It's resonance: the new situation is playing the note the body was tuned to.</li>
<li><strong>Each technique rides a body state.</strong> That is the part I only saw once I wrote “The Body.”</li></ul>
<figure class="fig">{d_states()}<figcaption>The five families map onto three body states. This is my synthesis from “The Body.” The state labels follow common trauma-informed language; researchers still debate the underlying theory.</figcaption></figure>
<h3>What interrupts it: state before story</h3>
<p>If the technique works on the body before the mind, then insight alone is too late. The interruption has to start in the body too. Every one of my thirty practices does the same two things. It <strong>adds time</strong> (slow down, sleep on it, write it down) and it <strong>adds a witness</strong> (your own record, your own body, one outside person). Time and a witness are exactly what every technique removes.</p>
<div class="three"><div><b>1 · Notice</b><p class="small">The stomach tightens, the breath shortens, the chest opens too fast. The body reports before the mind does.</p></div>
<div><b>2 · Pause</b><p class="small">Feet on the floor. One slow breath. “I'll come back to this.” The pause is the gap between the move and your response. It didn't exist before you could name the move.</p></div>
<div><b>3 · Choose</b><p class="small">The original instead of the copy: plain speech, a direct conversation, rest, a third option. Not perfectly. More often this year than last.</p></div></div>
<div class="pull">The pause is where a person is free. Not free from the cycle, which is still running. Free inside it, in the moment between the technique and the response.</div>
<p>Settled states spread the same way alarmed ones do. A calm adult steadies a child. A teacher who isn't bracing steadies a room. That is why I say the repair travels through the same channels as the harm, and why one regulated person in a family or classroom matters more than it looks.</p>
<h3>Signals worth listening to</h3>
<table class="small"><tr><th>What the body does</th><th>What it may be telling you</th><th>What gets lost if it is only labelled</th></tr>
<tr><td>A gut feeling that something is off</td><td>Early detection of a mismatch between words and behaviour</td><td>The information in the unease</td></tr>
<tr><td>Tiredness that sleep doesn't fix</td><td>More is being taken than returned</td><td>The question “what is draining me?”</td></tr>
<tr><td>Loneliness in a full room</td><td>The belonging on offer is conditional</td><td>The search for the real thing</td></tr>
<tr><td>Anger at “that's just how it works”</td><td>A sense of fairness doing its job</td><td>The energy needed to change something</td></tr>
<tr><td>Restlessness in a compliant setting</td><td>A need for movement, meaning or a say</td><td>What the setting could do differently</td></tr></table>
<p class="small">I hold these as questions, not diagnoses. A signal can come from the situation, from the body, or from both. Anxiety, depression and attention differences are real and treatable, and nothing here is a reason to refuse or stop care. My point is narrower: ask what the signal is about <em>as well as</em> how to ease it.</p></div>''')

    a(f'''<div class="sec" id="s9"><div class="kick">9 · The combinations</div><h2>Why the order matters</h2>
<p class="lede">Nobody meets one technique at a time. People live inside compound patterns: several moves, in a set order. I believe the combinations are the most useful thing I've made, because the order is what makes a pattern breakable.</p>
<p>Single techniques are like single chemicals. Combinations are the compounds people actually encounter: <em>The Trauma Bond Engine, The Golden Cage, The Burnout Machine, The Care Trap, The Compliance Engine, Golden Handcuffs.</em> When someone hears the name and the sequence, the usual reaction is “that is exactly what happened to me.”</p>
<p>Order matters because each step prepares the ground for the next. Start with harm and no kindness, and a person simply leaves. A trauma bond only forms when unpredictable kindness comes <em>first</em>. If you know the order, you know which link you're standing on, and you can cut the chain there.</p>
<figure class="fig chain">{CH1}</figure><figure class="fig chain">{CH2}</figure><figure class="fig chain">{CH3}</figure>
<p class="small">Gold bars mark where a chain breaker cuts the sequence. The earlier the cut, the less it costs.</p>
<h3>The six parts of every combination I write</h3>
<div class="chainx"><div><i>1</i><b>A story</b>One vivid, composite scene.</div><div><i>2</i><b>The mechanics</b>Which moves, in what order, and why that order works.</div><div><i>3</i><b>Institutional echo</b>The same sequence run by an organization.</div><div><i>4</i><b>Civilizational echo</b>The same sequence across a society.</div><div><i>5</i><b>Recognition cues</b>How to tell if you're inside it now, and what else it could be.</div><div><i>6</i><b>Chain breakers</b>First steps, and when to get qualified help.</div></div>
<table><tr><th>For</th><th>What a combination gives them</th></tr>
<tr><td><b>A survivor</b></td><td>The difference between a label and a plan. Not “you were trauma bonded,” but which moves built the bond, in what order, how to test whether you're still in it, and where to cut.</td></tr>
<tr><td><b>A helper</b></td><td>Precise, shared language for something the person can only describe as a feeling.</td></tr>
<tr><td><b>People in different fields</b></td><td>A teacher and a nurse can both say “that's the Burnout Machine” and understand each other at once.</td></tr>
<tr><td><b>Anyone designing an institution</b></td><td>A checklist: does our structure allow this sequence to run? If so, where do we cut it?</td></tr>
<tr><td><b>Young people</b></td><td>Recognition before capture. Spotting the first two links is enough to step around the rest.</td></tr></table></div>''')

    a(f'''<div class="sec" id="s10"><div class="kick">10 · Connections</div><h2>What the whole map shows that no single chapter says</h2>
<p class="lede">I wrote the sectors one at a time. Only when I laid all thirty next to the techniques, the body chapter and the combinations did these links appear. They change how I think the work should be used.</p>
<figure class="fig">{d_loops()}<figcaption>Left: sectors hand a person on to each other. Right: the sectors that treat the damage depend on the sectors that cause it.</figcaption></figure>
<ol class="disc">
<li><strong>Sectors prime each other.</strong> Capture in one makes the next harder to refuse. A child who learns at school that worth equals a score arrives at work ready to accept that worth equals output. Health cover tied to a job turns a workplace problem into a medical risk. Debt taken for education narrows every later choice about housing and work. The cycle isn't thirty parallel loops. It is a relay.</li>
<li><strong>Some sectors guard the others.</strong> Four of the thirty decide what counts as true, normal, sane and proven: Media, Education, Mental health and Science. When those are captured, a person loses the tools to recognize capture anywhere else. This is the Garden insight at scale: perception goes first. It also tells me where the map is most needed.</li>
<li><strong>The cycle sells the cure for itself.</strong> Wellness, therapy, pharmaceuticals, insurance and much of self-help treat stress, loneliness and exhaustion that other sectors produce. Much of that help is good and some of it saves lives. But a remedy that returns a person to the same conditions, unchanged, completes a loop. The test I now use: <em>does this help return me to myself, or to the thing that hurt me?</em></li>
<li><strong>Every technique removes the same two things: time and a witness.</strong> Speed stops evaluation. Isolation stops comparison. That is why every practice in the map does the reverse. It also means the simplest institutional safeguard is cheap: a cooling-off period and an outside voice.</li>
<li><strong>Technique families ride body states</strong> (Section 8). This explains why explaining a pattern to someone in alarm or shutdown rarely works, and why safety has to come before insight. For anyone teaching this material, it sets the order: settle first, name second.</li>
<li><strong>The earliest sectors set the template for all the rest.</strong> Family and Education come first in a life. They install the expectations (conditional approval, ranked worth, don't question) that every later sector relies on. If I had to choose one place for this work to land, it would be there.</li>
<li><strong>The same thirty moves describe the inner critic.</strong> “The Mirror” isn't a separate topic. The voice in a person's head uses the institution's techniques word for word. So work on self-talk and work on systems are the same work at two scales.</li>
<li><strong>A gap in my own map.</strong> I have documented capture far more thoroughly than its opposite. A map that only shows what's wrong can leave people bleak, or suspicious of everything. The next section is my start on fixing that.</li></ol></div>''')

    a('''<div class="sec" id="s11"><div class="kick">11 · The positive blueprint</div><h2>What a clean system looks like</h2>
<p class="lede">The opposite of a captured sector isn't “no system.” It's a system that meets the need without adding a condition. These exist. They are ordinary, and most of us have used one.</p>
<table><tr><th>Need</th><th>A clean example</th><th>Why it stays clean</th></tr>
<tr><td><b>Curiosity</b></td><td><b>The public library.</b> Walk in, ask anything, take it home, owe nothing. Also: curiosity-led classrooms where children follow real questions and are assessed on what they can show.</td><td>No ranking of people. No cost to leave. The question is welcome whoever asks it.</td></tr>
<tr><td><b>Provision</b></td><td><b>Mutual aid and member-owned finance.</b> Neighbours pooling help in a crisis. Credit unions owned by the people who use them.</td><td>The people who give are the people who receive. There's no outside party to extract for.</td></tr>
<tr><td><b>Fairness after harm</b></td><td><b>Restorative practice.</b> The person harmed and the person responsible meet with support, and agree on what repair looks like. Many schools now use it in place of automatic exclusion.</td><td>It asks “what was harmed and what would repair it?” in place of “what rule was broken and what's the penalty?”</td></tr>
<tr><td><b>A peaceful ending</b></td><td><b>Hospice care at home.</b> Comfort, family and the person's own wishes come first.</td><td>Success is measured by the person's experience, not by activity billed.</td></tr>
<tr><td><b>Shared knowledge</b></td><td><b>Open-source software and open encyclopedias.</b> Built by many, free to all, checkable by anyone.</td><td>Nothing is hidden, so nothing depends on you not looking.</td></tr></table>
<h3>What they have in common</h3>
<p>Set these beside the eight stages and the pattern of their design is plain. I use it as a short test of any program, school or service.</p>
<div class="cols"><div><ul><li><strong>The door opens both ways.</strong> Leaving is easy and carries no shame.</li><li><strong>No condition on the need.</strong> Help doesn't depend on performance or loyalty.</li><li><strong>Nothing depends on confusion.</strong> Rules are plain and stable.</li><li><strong>Outside voices are welcome.</strong> Second opinions, families, advocates.</li></ul></div>
<div><ul><li><strong>Exchange is visible.</strong> You can see what you give and what you get.</li><li><strong>Worth isn't on the table.</strong> The work is assessed. The person isn't.</li><li><strong>Someone answers.</strong> A named person is responsible when things go wrong.</li><li><strong>It can be examined.</strong> It gets better, not defensive, when questioned.</li></ul></div></div>
<p class="small">No real system is perfectly clean, and many captured ones contain clean rooms: the teacher who protects questions, the doctor who listens for the whole appointment. Those rooms are evidence that the design, not the people, is what needs to change.</p></div>''')

    a(f'''<div class="sec" id="s12"><div class="kick">12 · The war map</div><h2>How this turns into real change</h2>
<p class="lede">I called the plan a war map, but the principle is the opposite of fighting. You don't beat the pattern on its own terms. You run the original: you meet needs without conditions, and you build things the pattern can't enter.</p>
<p>Reform often fails for a reason the map makes obvious. It replaces the person inside the structure and leaves the structure. The new leader inherits the old incentives. And individual healing alone isn't enough either: a person who heals from one relationship walks back into the same cycle in a different building. So the work has to move on three fronts at once, and my content is built to feed each one.</p>
<figure class="fig">{d_change()}<figcaption>The path from one person's recognition to a redesigned system, and which part of my work serves each step.</figcaption></figure>
<div class="three">
<div><b>Front 1 · Inner</b><p>What one person does.</p><p class="small">Spot the stage in real time. Learn the practice for each technique. Reclaim each sector's original impulse in small daily acts. Break the chain with your own children. <em>My content's job here: vocabulary, recognition, practices.</em></p></div>
<div><b>Front 2 · Building</b><p>What we make together.</p><p class="small">Clean versions of each sector (Section 11): member-owned, open, leavable. Networks across fields, so the teacher, the nurse and the parent compare notes. Money and attention moved toward what serves. <em>My content's job: a shared language and a design test.</em></p></div>
<div><b>Front 3 · Structural</b><p>What changes for everyone.</p><p class="small">Change what we measure, the stories we repeat and the rules that reward capture. Restore what was once held in common. Keep the memory alive between generations. <em>My content's job: a public record that makes the pattern arguable in plain terms.</em></p></div></div>
<h3>What each piece of the work does</h3>
<table class="small"><tr><th>Piece</th><th>What it does for a reader</th><th>The change it makes possible</th></tr>
<tr><td><b>The 8 stages</b></td><td>Lets you locate yourself: “I'm at stage three.”</td><td>The cycle can't run unnoticed.</td></tr>
<tr><td><b>The 30 techniques, with originals</b></td><td>Names the move and shows the real thing it copied.</td><td>Grief with direction: you know what to rebuild, not only what was done.</td></tr>
<tr><td><b>The 30 sectors at 3 levels</b></td><td>Shows the same move at home, at work and in policy.</td><td>Self-blame drops. People in different fields find common cause.</td></tr>
<tr><td><b>The combinations</b></td><td>Shows the sequence and where to cut it.</td><td>Earlier exits. Safer institutions, designed against whole sequences.</td></tr>
<tr><td><b>The Mirror and the intent levels</b></td><td>Shows the pattern in yourself without shame.</td><td>People stop passing it on. Accountability without a villain.</td></tr>
<tr><td><b>The Body and The Frequency</b></td><td>Teaches the pause, and what to return to.</td><td>Change that holds under stress, not only in calm moments.</td></tr>
<tr><td><b>Playground Protectors</b></td><td>Gives children the words early, and a clear “tell a grown-up” rule.</td><td>Prevention. The next generation meets the cycle already able to see it.</td></tr></table>
<h3>Change what we measure and the stories we tell</h3>
<div class="cols"><div><table class="small"><tr><th>We measure</th><th>We could measure</th></tr>
<tr><td>Test scores</td><td>Curiosity kept; what a child can make and explain</td></tr><tr><td>Attendance</td><td>Belonging: does each child have one trusted adult?</td></tr>
<tr><td>Engagement</td><td>Quality of attention; time well spent</td></tr><tr><td>Activity billed</td><td>Health restored; people who no longer need us</td></tr><tr><td>GDP</td><td>Wellbeing; security of the median household</td></tr></table></div>
<div><table class="small"><tr><th>The story that keeps it running</th><th>The replacement</th></tr>
<tr><td>“You need to be fixed.”</td><td>You arrived complete.</td></tr><tr><td>“That's just how it works.”</td><td>It works the way it was designed.</td></tr>
<tr><td>“School prepares you for work.”</td><td>Education grows the whole person.</td></tr><tr><td>“Rest is earned.”</td><td>Rest is a need, like breathing.</td></tr><tr><td>“You're only one person.”</td><td>Every change began with one who saw it.</td></tr></table></div></div>
<h3>Practise what can't be sold</h3>
<p>The pattern can only capture what can be turned into money or data. So some of the strongest acts are the plainest: sitting in silence, walking with no destination, listening without replying, grieving without a deadline, playing without keeping score, resting without producing, loving without performing. They create no revenue. They are what people were built for, and they keep the trail clear.</p>
<p class="small">My full War Map also lists specific legal and policy reforms. I've left them out here because the framework doesn't depend on any one political program, and people of different politics can use the same map.</p></div>''')

    # ---- tools
    ws = "".join(f'<div class="wsb"><b>{t}</b><span>{d}</span>{fld(17)}</div>' for t, d in
                 [("1 · Behaviour", "What happened? Facts only, as a camera would record it."), ("2 · Body", "What did you feel in your body, and when?"), ("3 · Technique", "Which move is closest? Use the matrix above or Section 5."),
                  ("4 · Stage", "Where in the eight stages is this?"), ("5 · Original need", "What real need of yours was being used?"), ("6 · Chain breaker", "One small step that adds time or a witness.")])
    prompts = ["Where in my life does warmth come with a condition I've never said out loud?", "Which of the thirty needs do I pay for most, and what would it look like met freely?",
               "Which technique do I run on myself most often? Whose voice does it sound like?", "Which technique have I run on someone else this month? What was I afraid of?",
               "What is one thing my body has been telling me that I keep overriding?", "Which one practice from the tables will I try this week, and who will I tell?"]
    a(f'''<div class="sec pb" id="s13"><div class="kick">13 · Tools</div><h2>Trace it, interrupt it, audit your own system</h2>
<p class="lede">This section is for use. Take one real situation and walk it across the page. You can type into the boxes on a screen, or print them.</p>
<h3>The pattern-interrupt matrix</h3>
<p class="small">Find the row closest to what you're seeing. Read across: behaviour, technique, stage, the need underneath, and a first step. One row is a hint, not a verdict. A pattern is several rows, repeating, with one side gaining.</p>
{matrix()}</div>
<div class="sec pb"><h3>Trace one situation</h3>
<p class="small">Behaviour → body → technique → stage → original need → chain breaker.</p>
<div class="ws">{ws}</div>
<div class="box plain keep"><h4>Before you read too much into it</h4><p>Three checks stop this tool from becoming a way to label people. <strong>Is it a pattern?</strong> Once is an event. <strong>Who gains?</strong> If no one benefits from your confusion, look for a plainer explanation: tiredness, a misunderstanding, a bad day. <strong>What happens when you name it calmly?</strong> A clean relationship or system gets curious. A captured one gets defensive or punishes the question. And if anyone is in danger, skip the worksheet and contact emergency services or a qualified professional.</p></div>
<h3>Six questions to sit with</h3>
<div class="pr">{"".join(f'<div><p>{i + 1}. {E(p)}</p>{fld(11)}</div>' for i, p in enumerate(prompts))}</div></div>
<div class="sec pb" id="rubric"><h3>Is our system running the pattern? An eight-point self-audit</h3>
<p>This is for school leaders, clinicians and anyone who runs a program. It isn't an accusation. Most structures drift toward the cycle without anyone choosing it, because the incentives pull that way. The rubric has one question per stage. It's meant to be used <em>before</em> harm happens, ideally with a parent, a student or a client in the room.</p>
{rubric()}
<div class="cols"><div><p class="small"><b>Reading your answers.</b> Any “No” is a place where the cycle can enter. Start with stages 4 and 5, Confuse and Isolate. If rules are clear and outside voices are welcome, most other problems become visible early and get fixed.</p></div>
<div><p class="small"><b>The one change we will make first:</b></p>{fld(16)}</div></div></div>''')

    a(f'''<div class="sec" id="s14"><div class="kick">14 · Children and schools</div><h2>Where the pattern starts, and where it's easiest to stop</h2>
<p class="lede">The pattern is installed earliest in childhood. That is also where it is cheapest to interrupt. A child who can name a move at eight is far harder to capture at eighteen.</p>
<p>In my Education chapter the original impulse is <em>the child who asked why</em>. The risk I describe isn't teachers. It's a design in which curiosity is graded, worth becomes a number, belonging depends on fitting in, and a child's resistance is treated as the problem and not as information. One line from that chapter: <em>the system sets the bar, denies the ladder, and blames the child.</em> The school chain in Section 9 shows the sequence.</p>
<h3>Why this matters developmentally</h3>
<ul><li><strong>Children build their inner voice from the voices around them.</strong> How adults respond to mistakes becomes how the child talks to themselves for decades.</li>
<li><strong>Children borrow regulation from adults.</strong> A settled adult is the intervention. A child in alarm can't take in a lesson about anything.</li>
<li><strong>Peer groups run the same moves.</strong> The instant best friend, the freeze-out, the rumour, hot-and-cold friendship, “everyone's doing it.” Children meet all of them by age ten, with no words for any of it.</li>
<li><strong>Without words, children conclude they are the problem.</strong> That conclusion is the real injury. A name for the move puts the problem back outside the child.</li></ul>
<h3>What I believe helps</h3>
<table class="small"><tr><th>Principle</th><th>In practice</th></tr>
<tr><td><b>Give the vocabulary early, in plain words</b></td><td>Describe the behaviour, never the child: “that's the hot-and-cold game,” not “she's toxic.” No clinical labels for children.</td></tr>
<tr><td><b>Validate perception</b></td><td>“Something felt wrong? Tell me about it.” A child who is believed keeps their compass.</td></tr>
<tr><td><b>Teach the pause as a skill</b></td><td>Feet on the floor, one breath, “I'll think about it.” It can be practised like any other skill.</td></tr>
<tr><td><b>Sort by safety, simply</b></td><td>Green and yellow: things you can handle with your own words. Red: tell a trusted adult now. Telling is the bravest move, not tattling.</td></tr>
<tr><td><b>Teach both sides</b></td><td>Every child will use these moves as well as receive them. Teaching “I did the freeze-out, and I can repair it” prevents the vocabulary from becoming a weapon.</td></tr>
<tr><td><b>Protect unstructured time</b></td><td>Boredom and free play are where a child's own impulses surface.</td></tr>
<tr><td><b>Model the catch</b></td><td>An adult who says “I snapped at you because I was stressed, and that wasn't fair” teaches the whole map in one sentence.</td></tr></table>
<h3>Playground Protectors</h3>
<p>I wrote this book for my daughter, so she'd have the words before she needed them. It has 28 missions in four worlds. Each one shows a scene, how it feels, words a child can say out loud, a traffic light for how serious it is, and when to get help. The moves have child-sized names: the Memory Mixer-Upper, the Guilt Gripper, the Super-Fast Best Friend, the Silent Freeze-Out, the Hot-and-Cold Game. It also covers the mean voice in your own head, and it ends with missions on repair, kindness and being a good friend. It was written for a child and an adult to read together.</p>
<div class="box plain keep"><h4>Where I'd value professional guidance</h4><p>I'm not a clinician. Three questions matter most to me. How should this be paced by age, so it informs without frightening? How do we keep the words from becoming labels children throw at each other? And how do we make sure that a child who recognizes something serious is connected at once to safe, qualified help, in line with a school's safeguarding duties?</p></div></div>''')

    a('''<div class="sec" id="s15"><div class="kick">15 · The horizon</div><h2>What this can become</h2>
<p class="lede">A pattern that runs everywhere can only survive while it stays unnamed. Once people share a map for seeing it, in daily life and in large systems alike, repetition gives way to choice. That is the whole of my ambition, and I think it is achievable.</p>
<p>We've done this before with other invisible things. People once had no concept of germs, and washing hands seemed pointless. They had no word for sexual harassment, so it couldn't be reported. They couldn't read, so they couldn't check what they were told. In each case the change wasn't a new moral. It was a shared, teachable way of seeing something that had always been there. I think pattern literacy is the next one of these: the ordinary ability to recognize when warmth has a hook in it.</p>
<h3>Five levels of change</h3>
<table><tr><th>Level</th><th>What changes</th></tr>
<tr><td><b>1. A person</b></td><td>Gets a map of what was done and tools to begin undoing it. “Something is wrong with me” becomes “something was taken from me, and it is still mine.”</td></tr>
<tr><td><b>2. A relationship</b></td><td>Recognition becomes a life skill. A parent at a school meeting, a patient in a clinic, a worker told “we're a family here” can see the move as it happens, and can name their own.</td></tr>
<tr><td><b>3. A shared language</b></td><td>Education reformers, health advocates, labour organizers, people recovering from religious harm and justice workers discover they're describing one cycle in different buildings. Common words make common cause.</td></tr>
<tr><td><b>4. Institutional design</b></td><td>The question changes from “how do we reform this?” to “which stages does our structure allow, and how do we design them out?” That is prevention.</td></tr>
<tr><td><b>5. A culture that can see itself</b></td><td>Normalization is one of the cycle's main engines. A society that can name its own patterns gains the option of choosing differently.</td></tr></table>
<h3>What a global standard for pattern literacy would look like</h3>
<div class="cols"><div><ul>
<li><strong>In homes:</strong> families with words for the hot-and-cold game and the guilt trip, used about behaviour and never about a person's worth.</li>
<li><strong>In primary schools:</strong> the moves taught alongside reading, as a friendship and safety skill, with a clear route to a trusted adult.</li>
<li><strong>In secondary schools:</strong> the eight stages and the combinations, applied to relationships, online life, advertising and recruitment.</li></ul></div>
<div><ul><li><strong>In clinics and counselling:</strong> a plain, shared vocabulary that complements professional frameworks and helps people describe what happened.</li>
<li><strong>In workplaces and institutions:</strong> the eight-point audit as routine as a safety check.</li>
<li><strong>In public life:</strong> journalists, voters and consumers able to say “that's a manufactured crisis” and be understood.</li></ul></div></div>
<h3>Why it has to be free, visual and shared</h3>
<p><strong>Free</strong>, because a map of gatekeeping can't have a gatekeeper. <strong>Visual</strong>, because a person in distress can read a chart long before they can read a chapter. <strong>Shared</strong>, because isolation is how the cycle protects itself, and a common vocabulary ends isolation faster than any single insight. When a child, a parent, a teacher and a psychologist can describe the same thing in the same words, private confusion becomes collective discernment.</p>
<h3>What it needs next</h3>
<ul><li><strong>Review by people with clinical and educational training,</strong> to test the claims, mark what is over-stated and tighten the language.</li>
<li><strong>Age-banded versions,</strong> built with educators, that fit real classrooms and safeguarding rules.</li>
<li><strong>Evidence.</strong> Small, honest studies: does learning the vocabulary help young people spot and step around these patterns? Does the audit change anything in a school?</li>
<li><strong>More of the positive blueprint:</strong> a clean-system chapter for every sector.</li></ul>
<div class="pull">Your hunger for belonging is not neediness; it's homesickness. Your hunger for rest is not laziness; it's memory. Your hunger for love without conditions is not naivety; it's recognition.</div>
<p>The original was never destroyed, only buried: the child's curiosity that survived school, the love that survived the manipulator, the knowing that survived the gaslighting. Everything I've written points at one moment, when a person sees the pattern and says: <em>that is not me. That is the pattern, and I don't have to run it.</em> Multiply that moment by enough people and the systems built on unmet need lose their supply. Nothing has to be torn down. People simply stop feeding it, and start building what should have been there.</p></div>''')

    a('''<div class="sec" id="s16"><div class="kick">16 · Honest limits</div><h2>What this is and is not</h2>
<p class="lede">I want any reader, and especially a professional, to know exactly where the evidence ends and my own lens begins.</p>
<table><tr><th>Kind of statement</th><th>What it covers</th></tr>
<tr><td><span class="tag f">Documented</span></td><td>The cycle and most individual techniques are described in clinical and research writing on coercive control, attachment and conditioning. The sector chapters draw on public sources a reader can check.</td></tr>
<tr><td><span class="tag j">My synthesis</span></td><td>That one cycle runs across all thirty sectors at three levels. The originals-and-inversions mapping. The sequencing logic of the combinations. The links in Section 10 and the body-state mapping in Section 8. These are my contributions and should be tested, not assumed.</td></tr>
<tr><td><span class="tag l">My faith lens</span></td><td>The “false god,” the counterfeit of the divine, the garden and the gate. In the series I say openly that this part is revelation and not research. It is offered, never required.</td></tr></table>
<h3>What it is not</h3>
<ul><li><strong>Not a diagnostic tool or a replacement for care.</strong> It helps people find words. It doesn't replace a qualified professional, and nobody should stop treatment or medication because of it.</li>
<li><strong>Not a way to label people.</strong> The techniques describe behaviour and design. Most harm happens without intent, and every one of us runs these moves at times.</li>
<li><strong>Not a call to walk away from everything.</strong> Seeing is not leaving. Sometimes seeing means staying, but staying differently.</li>
<li><strong>Not a claim that every institution is bad.</strong> The same needs are met well in many places, and the people inside captured systems are often the ones holding them together.</li>
<li><strong>Some of it is belief.</strong> That the body is a reliable signal, that stress is passed down biologically, and the body-state model are views I hold. The research on each is active and contested, and I've tried to mark them wherever they appear.</li>
<li><strong>The pattern lands unequally.</strong> I describe one cycle, but it does not press on everyone with the same weight, and the map should never be used to flatten that.</li></ul>
<h3>In one paragraph</h3>
<p>I wrote these books because I kept seeing one pattern take the deepest human needs (to belong, to be safe, to be loved, to rest, to know what is true) and hand them back with conditions attached. I mapped it across thirty sectors, then at full resolution, then as the sequences people actually live through, because naming the exact sequence is what lets a person recognize it, heal from it, and stop passing it on. Whether you read it as a spiritual counterfeit, a psychological cycle or the predictable result of power and incentives, the shape is the same. And underneath it, in every person, the original is still there. My hope is that seeing both becomes common knowledge, and stays free.</p>
<p class="sig">The pattern that was installed in me, I now see. The pattern I carried, I now name. The pattern I passed on, I now interrupt. Not because I am guilty. Because I am awake.</p>
<p class="small" style="margin-top:2em">The Fractal, Fractal², The Sacred Divide, the Pattern Decoder and Playground Protectors are free to read at noblefathercreations.com. Educational commentary on patterns, not accusations against any person or organization, and not legal, medical, psychological or financial advice.</p></div>''')
    if foil:
        a('''</section><section class="letter pb" id="asks"><div class="kick">For Foil · where I'd value your help</div><h2>Three asks</h2>
<p class="lede">None of these is urgent, and any one of them would matter. Say no to whatever doesn't fit.</p>
<div class="ask"><i>1</i><div><h3>Introduce me to people in your field who would review the work</h3>
<p>I'm looking for psychologists, school counsellors, teachers and researchers willing to read some part of it and tell me what holds and what doesn't. Any combination helps: a full review, a single chapter, an hour of blunt comments, or a short written reaction I could quote with permission. Critical reviews are as useful to me as kind ones.</p>
<p class="small"><b>Easiest version:</b> forward the public edition of this document to two or three people with one line from you.</p></div></div>
<div class="ask"><i>2</i><div><h3>Advise me on framing this for young people</h3>
<p>I want the material for children and teenagers to be age-appropriate and non-pathologizing: about behaviour and never about labelling a child, paced so it informs without frightening, and wired into proper safeguarding. You know where the lines are. I'd value your judgment on what to change, what to cut, and what should only ever be delivered with a trained adult present.</p>
<p class="small"><b>Easiest version:</b> read Section 14 and mark anything that would worry you in a school.</p></div></div>
<div class="ask"><i>3</i><div><h3>Help me bring Playground Protectors into schools</h3>
<p>The book is finished and free. What I don't know is the route in: who decides, what a school or district needs to see first, how it would sit beside existing social-emotional or anti-bullying programs, and what a small, honest pilot would look like. If you know someone who could tell me, or would look at it with a counsellor's eye yourself, that would move it further than anything I can do alone.</p>
<p class="small"><b>Easiest version:</b> tell me the first person I should talk to, and what they would ask me.</p></div></div>
<div class="box plain"><h4>What I can offer in return</h4><p>Everything is free and will stay free. I'll adapt, cut or re-word anything a reviewer shows me is wrong or unsafe. I'll credit help however people prefer, or not at all. And I can provide any part of the work in whatever form is easiest to review: a single chapter, the children's book, one sector, or this summary.</p></div>
<p>Mostly, I want eyes on it from people who know this field. You're the first person I thought of.</p>
<p class="sig">Thank you, Foil.<br>Shae</p>''')
    a("</section>")
    return "\n".join(P)

CSS = (HERE / "base.css").read_text() + (HERE / "extra.css").read_text()
foot = "Why I Wrote This · The Fractal · Shae Stovell"
doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Why I Wrote This</title><style>{CSS}\n@page{{@bottom-left{{content:"{foot}"}}}}</style></head><body>{body()}</body></html>'
(HERE / f"why-{ED}.html").write_text(doc)
print(ED, "fields:", _f[0], "bytes:", len(doc))
