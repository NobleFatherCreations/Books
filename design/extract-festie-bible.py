#!/usr/bin/env python3
"""
Parse the 183-page Festie Bible OCR output (+ pypdf fallback) into
structured JSON: content/festie-bible-data.json.

Two independent extractions are combined, each used where it's strongest:
- OCR (tesseract against the 300dpi page render) is ground truth for
  scenario-page prose. The source PDF's font has broken ToUnicode mappings
  for several ligatures (fr/fo/fe/fa/kn...), which silently drops letters
  from the PDF's own text stream ("before" -> "be re"); OCR reproduces the
  rendered page correctly and doesn't have this defect.
- pypdf's text stream is used for the intro/check pages instead, because
  those pages have a real authoring bug (two overlapping text layers at
  the same position for each acronym-check description) that OCR faithfully
  renders as garbled overlapping text -- pypdf's extraction happens to keep
  only one clean layer there.
"""
import json, re, sys
from pathlib import Path
from pypdf import PdfReader

OCR_DIR = Path("/tmp/claude-0/-home-user-Wookbook/29d6f5a7-291c-50fb-9d74-8e56b2b57a42/scratchpad/festie-ocr/text")
MST_DIR = Path("/tmp/claude-0/-home-user-Wookbook/29d6f5a7-291c-50fb-9d74-8e56b2b57a42/scratchpad/festie-ocr/mst-text")
PDF_FILES = [
    "/root/.claude/uploads/29d6f5a7-291c-50fb-9d74-8e56b2b57a42/91adc303-Festie1.pdf",
    "/root/.claude/uploads/29d6f5a7-291c-50fb-9d74-8e56b2b57a42/c558fd55-Fesitie2.pdf",
    "/root/.claude/uploads/29d6f5a7-291c-50fb-9d74-8e56b2b57a42/b6bfaacc-Festie3.pdf",
]
OCR_PREFIXES = ["f1", "f2", "f3"]

GUIDE_META = [
    ("grove","fb-g-grove","WOMEN ATTENDEES","G.R.O.V.E.","Women Attendees Edition",1),
    ("bass","fb-g-bass","MEN ATTENDEES","B.A.S.S.","Men Attendees Edition",2),
    ("rave","fb-g-rave","FIRST-TIMERS","R.A.V.E.","First-Timers Edition",3),
    ("pride","fb-g-pride","LGBTQ+ ATTENDEES","P.R.I.D.E.","LGBTQ+ Attendees Edition",4),
    ("create","fb-g-create","LIVE PAINTERS & ARTISTS","C.R.E.A.T.E.","Live Painters & Artists Edition",5),
    ("sound","fb-g-sound","MUSICIANS & TOURING","S.O.U.N.D.","Musicians & Touring Edition",6),
    ("market","fb-g-market","VENDORS & MARKET ARTISTS","M.A.R.K.E.T.","Vendors & Market Artists Edition",7),
    ("hold","fb-g-hold","STAFF & VOLUNTEERS","H.O.L.D.","Staff & Volunteers Edition",8),
    ("care","fb-g-care","HARM REDUCTION","C.A.R.E.","Harm Reduction Edition",9),
    ("lead","fb-g-lead","CAMP LEADS & ORGANIZERS","L.E.A.D.","Camp Leads & Organizers Edition",10),
    ("event","fb-g-event","PROMOTERS ACCOUNTABILITY","E.V.E.N.T.","Promoters Accountability Edition",11),
    ("safe","fb-g-safe","HEALTH & SAFETY","S.A.F.E.","Health & Safety Edition",12),
]
SECTIONS = ["CAPTURE","CONDITION","CONTROL","TOOLS","SUPPORT"]

def load_all_pages():
    pages = []
    n = 1
    for pdf_path, prefix in zip(PDF_FILES, OCR_PREFIXES):
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages, start=1):
            pypdf_text = page.extract_text() or ""
            stem = f"{prefix}-{i:02d}"
            ocr_path = OCR_DIR / f"{stem}.txt"
            ocr_text = ocr_path.read_text() if ocr_path.exists() else ""
            pages.append({"n": n, "ocr": ocr_text.strip(), "pypdf": pypdf_text.strip(), "stem": stem})
            n += 1
    return pages

MST_FOOTER_CUT = re.compile(
    r"(DanceSafe|Dance\s*Safe|Zendo|RAINN|Crisis\s*Text|MAPS\.?org|Test\s*Kits|TikTok|"
    r"dapperdadnfc|\d{3,4}[\s-]?\d{3}[\s-]?\d{4}|741741|HOME[>→]|NOBLE FATHER)",
    re.I,
)

def load_mst(stem):
    out = {}
    for col in ("move", "say", "truth"):
        p = MST_DIR / f"{stem}-{col}.txt"
        raw = p.read_text() if p.exists() else ""
        lines = [l for l in raw.split("\n") if l.strip()]
        if lines:
            lines = lines[1:]  # drop the column header word
        kept = []
        for l in lines:
            m = MST_FOOTER_CUT.search(l)
            if m:
                if m.start() > 15:
                    kept.append(l[:m.start()])
                break
            kept.append(l)
        joined = clean(" ".join(kept)).rstrip(" ;:|*").strip()
        joined = re.sub(r'([.!?"])\s+[a-zA-Z]{1,2}$', r"\1", joined)  # trailing 1-2 letter noise
        out[col] = joined
    return out

CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f﻿]")

def clean(text):
    if not text:
        return ""
    text = CTRL_RE.sub("", text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("≠", "≠").replace("®", "").replace("¢", "").replace("«", "")
    text = re.sub(r"\bJs\b", "Is", text)
    text = re.sub(r"(?<=\s)\|(?=\s)", "I", text)
    text = re.sub(r"\s*\n\s*", " ", text)          # collapse newlines to spaces
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def clean_block(text):
    """Like clean() but preserves line breaks (for lists)."""
    if not text:
        return ""
    text = CTRL_RE.sub("", text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\bJs\b", "Is", text)
    text = re.sub(r"(?<=\s)\|(?=\s)", "I", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

FOOTER_CUT = re.compile(r"(DanceSafe|Dance Safe)", re.I)

def strip_footer(text):
    m = FOOTER_CUT.search(text)
    return text[:m.start()] if m else text

def classify(raw, known_sections=None):
    t = raw.upper()
    if "SECTION" in t and "OF 12" in t:
        return "divider"
    if "SENTENCES" in t and "GUIDE" in t:
        return "intro"
    if "SCENE" in t and re.search(r"DEALING\s*WITH", t):
        return "scenario"
    if known_sections and "SCENE" in t and any(re.search(rf"\b{re.escape(s)}\b", t) for s in known_sections):
        return "scenario"
    return "other"

# Ordered scenario labels: (key, regex, "before"|"after" -- whether the
# *content* for this field sits before or after the label match)
SCENARIO_LABELS = [
    ("who_label",   re.compile(r"WHO\s*YOU.?RE\s*DEALING\s*WITH", re.I)),
    ("scene_label", re.compile(r"\bTHE\s*SCENE\b", re.I)),
    ("tells_label", re.compile(r"SPOT\s*IT\s*[—\-]?\s*THE\W{0,3}TELLS", re.I)),
    ("happening_label", re.compile(r"WHAT.?S\s*ACTUALLY\s*HAPPENING", re.I)),
    ("check_label", re.compile(r'[A-Z](\.[A-Z]){2,}\.?\s*[—\-]\s*"?[A-Z]"?\s*CHECK:?', re.I)),
    ("dark_label",  re.compile(r"DARK\s*REALITY\s*[—\-]?\s*[A-Z ,'&]{0,60}", re.I)),
    ("move_label",  re.compile(r"(?:^|\n)\s*(?:⚡\s*)?THE\s*MOVE\s*(?:\n|$)", re.I)),
    ("say_label",   re.compile(r"(?:^|\n)\s*SAY\s*THIS\s*(?:\n|$)", re.I)),
    ("truth_label", re.compile(r"(?:^|\n)\s*THE\s*TRUTH\s*(?:\n|$)", re.I)),
]

def segment(text):
    """Find each label's span in order; return dict of key -> text following
    that label up to the next found label (or end of text)."""
    matches = []
    for key, rx in SCENARIO_LABELS:
        m = rx.search(text)
        if m:
            matches.append((m.start(), m.end(), key))
    matches.sort()
    out = {}
    for i, (start, end, key) in enumerate(matches):
        nxt = matches[i+1][0] if i+1 < len(matches) else len(text)
        out[key] = text[end:nxt]
    # header = everything before the first label match (hook/archetype/clinical)
    header = text[:matches[0][0]] if matches else text
    return header, out

def extract_header(header_text):
    hlines = [clean(l) for l in header_text.split("\n") if clean(l)]
    start_i = None
    for i, l in enumerate(hlines):
        if l.startswith('"') or l.startswith("'"):
            start_i = i
            break
    if start_i is None:
        # some guides' hooks aren't quoted -- fall back to the first
        # substantially-uppercase line (a real title), not a stray glyph
        for i, l in enumerate(hlines):
            if "—" in l or "-" in l or "PAGE" in l.upper():
                continue  # eyebrow/section badge fragments, not the real title
            letters = [c for c in l if c.isalpha()]
            if len(letters) >= 8 and sum(1 for c in letters if c.isupper()) / len(letters) > 0.8:
                start_i = i
                break
    if start_i is None:
        return "", "", ""
    hook = hlines[start_i].strip('"\' ')
    archetype = hlines[start_i+1] if start_i+1 < len(hlines) else ""
    clinical = ""
    if start_i+2 < len(hlines) and hlines[start_i+2].lower().startswith("clinical"):
        clinical = re.sub(r"^clinical:?\s*", "", hlines[start_i+2], flags=re.I)
    return hook, archetype, clinical

def parse_scenario(raw, section_hint, mst, pypdf_raw=""):
    text = strip_footer(raw)
    header, seg = segment(text)

    hook, archetype, clinical = extract_header(header)
    if len(hook) < 4 and pypdf_raw:
        pheader, _ = segment(strip_footer(pypdf_raw))
        hook2, arch2, clin2 = extract_header(pheader)
        if len(hook2) >= 4:
            hook, archetype, clinical = hook2, arch2, clin2

    check_m = SCENARIO_LABELS[4][1].search(text)
    check_label_text = clean(check_m.group(0)) if check_m else ""
    check_content = clean(seg.get("check_label", ""))
    check_content = re.sub(r"\.\s*\b[A-Z]{1,3}\b\s*$", ".", check_content)  # trailing OCR-noise token
    check_full = (check_label_text + " " + check_content).strip()

    dark_m = SCENARIO_LABELS[5][1].search(text)
    dark_title = ""
    if dark_m:
        dm2 = re.search(r"[—\-]\s*([A-Z][A-Z ,'&]{2,50})", dark_m.group(0))
        if dm2:
            candidate = dm2.group(1).strip()
            # only usable if it has real word-gaps; the label-collision bug
            # glues these into one run on many pages, which we can't recover
            if " " in candidate:
                dark_title = candidate.title()

    tells_raw = seg.get("tells_label", "")
    tells = []
    for l in tells_raw.split("\n"):
        l = clean(l)
        if len(l) > 3:
            tells.append(l)

    return {
        "section": section_hint,
        "hook": hook,
        "archetype": archetype,
        "clinical": clinical,
        "who": clean(seg.get("who_label", "")),
        "scene": clean(seg.get("scene_label", "")),
        "tells": tells,
        "happening": clean(seg.get("happening_label", "")),
        "check": check_full,
        "darkTitle": dark_title,
        "dark": re.sub(r"[\s;:|*]+$", "", clean(re.split(r"THE\s*MOVE", seg.get("dark_label", ""), flags=re.I)[0])),
        "move": mst.get("move", ""),
        "say": mst.get("say", "").strip('"\' '),
        "truth": mst.get("truth", ""),
    }

def detect_section(raw, known_sections):
    head = raw[:250].upper()
    for s in known_sections:
        if re.search(rf"\b{re.escape(s)}\b", head):
            return s
    up = raw.upper()
    for s in known_sections:
        if re.search(rf"\b{re.escape(s)}\b", up):
            return s
    return known_sections[0] if known_sections else "CAPTURE"

ROW_NAME_RE = re.compile(r"[A-Z][a-zA-Z']{2,}(?:\s[A-Z][a-zA-Z']{2,}){0,2}\??")

def split_rows(block, n_expected):
    """Split a block of 'Name Name? Sentence... Name Name? Sentence...' into
    (name, desc) pairs by finding Title-Case-name-immediately-followed-by-a
    capitalized-sentence-start boundaries."""
    starts = [m.start() for m in re.finditer(
        r"(?:(?<=^)|(?<=[\s)\]]))([A-Z][a-zA-Z']{2,}(?:\s[A-Z][a-zA-Z']{2,}){0,2}\??)(?=\s+[A-Z][a-z])",
        block)]
    if not starts:
        return []
    rows = []
    for i, s in enumerate(starts):
        end = starts[i+1] if i+1 < len(starts) else len(block)
        chunk = block[s:end].strip()
        m = re.match(r"([A-Z][a-zA-Z']{2,}(?:\s[A-Z][a-zA-Z']{2,}){0,2}\??)\s+(.*)", chunk, re.S)
        if m:
            rows.append((m.group(1).strip(), clean(m.group(2))))
    return rows

def is_garbled(s):
    if not s or len(s) < 8:
        return True
    words = s.split()
    if not words:
        return True
    bad = sum(1 for w in words if len(w) > 3 and sum(c.isalpha() for c in w) / max(len(w),1) < 0.7)
    weird_case = sum(1 for w in words if re.search(r"[a-z][A-Z]|[A-Z]{2,}[a-z]", w) and not w.isupper())
    return (bad + weird_case) > max(1, len(words) // 4)

def letter_anchored_rows(block, letters):
    """Split '<caption>.G Gut Check desc... R Rapid Pace? desc...' into rows
    using the known acronym letters (in order) as row-start anchors -- far
    more reliable than guessing name/sentence boundaries generically, since
    duplicate letters (B.A.S.S. has two S rows) make generic parsing ambiguous."""
    block = re.sub(r"^[^.]*\.\s*", "", block, count=1)  # drop leading caption sentence
    positions = []
    search_from = 0
    for L in letters:
        m = re.search(rf"(?:^|(?<=[\s)\]]))\(?{re.escape(L)}\)?\s+(?=[A-Z][a-z])", block[search_from:])
        if not m:
            positions.append(None)
            continue
        pos = search_from + m.start()
        positions.append(pos)
        search_from = search_from + m.end()
    rows = []
    real = [p for p in positions if p is not None] + [len(block)]
    for i, pos in enumerate(positions):
        if pos is None:
            rows.append(("", ""))
            continue
        end = min([p for p in real if p > pos], default=len(block))
        chunk = block[pos:end].strip()
        m = re.match(r"\(?[A-Z]\)?\s+([A-Z][a-zA-Z']*(?:\s[A-Z][a-zA-Z']*){0,2}\??)\s+(.*)", chunk, re.S)
        if m:
            rows.append((m.group(1).strip(), clean(m.group(2))))
        else:
            rows.append(("", ""))
    return rows

def parse_check_panel(pypdf_text, ocr_text, letters):
    n = len(letters)
    def block_of(text):
        u = text.upper()
        s = u.find("CHECK")
        e = u.find("WHAT")
        if e == -1:
            e = u.find("GUIDE")
        if s == -1:
            return ""
        body = text[s:e if e != -1 else len(text)]
        return re.sub(r"^CHECK", "", body, flags=re.I).strip()

    pp_rows = letter_anchored_rows(clean_block(block_of(pypdf_text)), letters)
    ocr_rows = letter_anchored_rows(clean_block(block_of(ocr_text)), letters)

    checks = []
    for i in range(n):
        cands = []
        if i < len(pp_rows) and pp_rows[i][0]: cands.append(pp_rows[i])
        if i < len(ocr_rows) and ocr_rows[i][0]: cands.append(ocr_rows[i])
        best = None
        for name, desc in cands:
            if not is_garbled(desc):
                best = (name, desc); break
        if not best and cands:
            best = max(cands, key=lambda c: len(c[1]))
        if best and best[0] and best[1]:
            name, desc = best
            desc = desc.rstrip('.')
            if not desc.endswith("..."):
                desc += "..."
            checks.append({"letter": letters[i], "name": name, "desc": desc})
    return checks

def parse_intro(pypdf_text, ocr_text, acronym):
    letters = [c for c in acronym if c.isalpha()]
    checks = parse_check_panel(pypdf_text, ocr_text, letters)

    src = pypdf_text if len(pypdf_text) > len(ocr_text) * 0.7 else ocr_text
    body = strip_footer(src)
    u = body.upper()
    ostart = u.find("GUIDE")
    oend = u.find("SENTENCES")
    outline = []
    if ostart != -1 and oend != -1:
        oblock = body[ostart:oend]
        for l in oblock.split("\n"):
            l = clean(l)
            m = re.match(r"^([A-Z][A-Z &]{2,24}?)\s*[—\-]\s*\.?(.{5,})$", l)
            if m:
                key = re.sub(r"\s+", " ", m.group(1)).strip()
                outline.append({"key": key, "desc": m.group(2).strip()})

    lines = [clean(l) for l in body.split("\n") if clean(l)]
    sentences = []
    for l in lines:
        if l.startswith('"') and l.strip('"').strip():
            sentences.append(l.strip('"').strip())

    intro_line = ""
    for l in lines:
        if "field guide" in l.lower():
            intro_line = l
            break
    return checks, outline, sentences, intro_line

def parse_divider(text):
    m = re.search(r"(\d+)\s*pages", text, re.I)
    return int(m.group(1)) if m else None

def main():
    pages = load_all_pages()
    print(f"Loaded {len(pages)} pages", file=sys.stderr)

    mission_src = pages[1]["pypdf"] or pages[1]["ocr"]
    mission = clean(mission_src)
    mission = re.sub(r"^.*?Digital Experiences\W*", "", mission).strip()
    mission = re.sub(r'^\W*dapper dad\W*', '', mission, flags=re.I).strip()
    mission = re.sub(r"(With love for the community.{0,60}Noble Father Creations)\b.*$", r"\1", mission, flags=re.I|re.S)

    cursor = 3
    guides = []
    for slug, cls, role, acro, edition, section_of in GUIDE_META:
        divider_pg = pages[cursor]
        declared_pages = parse_divider(divider_pg["pypdf"]) or parse_divider(divider_pg["ocr"])
        cursor += 1

        intro_pg = pages[cursor]
        checks, outline, sentences, intro_line = parse_intro(intro_pg["pypdf"], intro_pg["ocr"], acro)
        known_sections = [o["key"] for o in outline] or SECTIONS
        cursor += 1

        scenarios = []
        pages_consumed = 2
        limit = declared_pages or 30
        while pages_consumed < limit:
            if cursor >= len(pages):
                break
            pg = pages[cursor]
            raw = pg["ocr"] if len(pg["ocr"]) >= 40 else pg["pypdf"]
            cls_type = classify(raw, known_sections)
            if cls_type == "divider":
                break
            if cls_type == "scenario":
                section_hint = detect_section(raw, known_sections)
                mst = load_mst(pg["stem"])
                sc = parse_scenario(raw, section_hint, mst, pg["pypdf"])
                if sc["hook"] and (sc["who"] or sc["scene"]):
                    scenarios.append(sc)
            cursor += 1
            pages_consumed += 1

        guides.append({
            "slug": slug, "acronymClass": cls, "role": role, "acronym": acro,
            "edition": edition, "sectionOf": section_of,
            "pages": declared_pages or (len(scenarios) + 2),
            "intro": intro_line,
            "checks": checks, "outline": outline, "sentences": sentences,
            "scenarios": scenarios,
        })
        print(f"{acro}: {len(scenarios)} scenarios, {len(checks)} checks (declared {declared_pages} pages)", file=sys.stderr)

    data = {
        "mission": mission,
        "updated": "2026-08-10",
        "changelog": [
            "Launched The Festie Bible as its own door on the hub: 12 field guides rebuilt from the original 183-page collection.",
            "Fixed the systemic label-collision and near-invisible interior brand mark from the source document.",
        ],
        "guides": guides,
    }
    out = Path("/home/user/Wookbook/content/festie-bible-data.json")
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    total_sc = sum(len(g["scenarios"]) for g in guides)
    print(f"TOTAL scenarios: {total_sc}", file=sys.stderr)
    print(f"Wrote {out}", file=sys.stderr)

if __name__ == "__main__":
    main()
