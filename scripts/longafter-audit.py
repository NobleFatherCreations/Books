#!/usr/bin/env python3
"""Content audit for The Long After, 2nd edition (content/longafter-v2/*.md against plan.json).

Run:  python3 scripts/longafter-audit.py [part-id ...]        (no ids = every written chapter)
Exit code 1 if any chapter FAILS. Checks, per chapter:
  structure   the header fields title / question / seo / short are present; the slug is in plan.json
  search      the target phrase is in the browser title or chapter title, in the short answer, and in the body
  links       every [x](ch:slug) points to a planned chapter; /playbook/ pages exist; /feminine/ pages and anchors exist;
              the plan's required Decoder and Feminine links are present; at least 3 links to other chapters
  questions   at least one heading phrased as the reader's question (ends with "?"), chapters only
  sources     a "## Sources" section with at least one item, chapters only
  voice       banned filler words; "rather than" at most 2; dashes at most 3 per 1,000 words; average sentence at most
              17 words, none over 40; reading ease (Flesch) at least 55
  timelines   no prescribed feelings or deadlines ("by now you should", "you will feel", "within 6 months you")
  safety      heavy chapters link to a crisis route; no method-level self-harm wording anywhere
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content/longafter-v2"
PLAN = json.loads((SRC / "plan.json").read_text())
CH = {c["slug"]: c for c in PLAN["chapters"]}

BANNED = [r"\bgenuine(ly)?\b", r"\bactual(ly)?\b", r"\bspecific(ally)?\b", r"\breally\b", r"\bit'?s important\b",
          r"\bit is important to\b", r"\bworth noting\b", r"\bdelve", r"\bjourney\b", r"\bempower", r"\bnavigat",
          r"\btapestry\b", r"\bin today'?s\b", r"\bat the end of the day\b", r"\brest assured\b", r"\bgame[- ]changer\b",
          r"\bunlock", r"\bholistic\b", r"(?<!as )\bleverage\b(?! (over|against))", r"\bseamless", r"\brobust\b", r"\bcrucial\b",
          r"\bembark", r"\bfoster(ing)?\b(?! (care|home|scheme|programme|program|carer))", r"\butilis|\butiliz", r"\bmoreover\b",
          r"\bfurthermore\b", r"\bin conclusion\b", r"\bit'?s not (just )?about\b", r"\bnot only\b", r"\bwarrior\b",
          r"\byou'?ve got this\b", r"\bhealing (journey|process)\b", r"\bspace to\b", r"\bhold space\b", r"\bdocumented pattern\b"]
PRESCRIBE = [r"\bby now you\b", r"\byou should (feel|be over|have moved on)\b", r"\byou will feel\b",
             r"\bwithin (a|one|two|three|six|\d+) (weeks?|months?|years?),? you('ll| will| should)\b", r"\bshould be over (it|this)\b"]
METHOD = [r"\blethal\b", r"\bdose of\b", r"\bmilligrams?\b", r"\bhang(ing)? yourself\b", r"\bcut yourself\b",
          r"\boverdose on\b", r"\bhow to (kill|end your life)\b"]
CRISIS = ("ch:when-its-more-than-aftermath", "ch:if-youre-not-safe-right-now", "ch:find-help")
STOP = {"a", "an", "the", "to", "of", "in", "on", "my", "i", "is", "it", "and", "or", "for", "with", "after", "from",
        "your", "you", "do", "does", "how", "what", "when", "why", "can", "an", "me", "be", "if", "at", "vs"}


def parse():
    out = {}
    for f in sorted(SRC.glob("[0-9][0-9]-*.md")):
        for block in re.split(r"^=== ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            slug, rest = block.split("\n", 1)
            head, _, body = rest.partition("\n---\n")
            meta = dict(re.findall(r"^(\w+):\s*(.+)$", head, re.M))
            out[slug.strip()] = {"meta": meta, "body": body.strip(), "file": f.name}
    return out


def words(t):
    return re.findall(r"[A-Za-z’'][A-Za-z’'-]*", t)


def syllables(w):
    w = w.lower().strip("’'")
    v = re.findall(r"[aeiouy]+", w)
    n = len(v) - (1 if w.endswith("e") and len(v) > 1 and not w.endswith("le") else 0)
    return max(1, n)


def prose(body):
    """The reading text only: no links targets, no sources list, no headings markup."""
    b = body.split("\n## Sources")[0].split("\n## Research and books")[0]   # citation lists are not prose
    b = "\n".join(l for l in b.split("\n") if not l.lstrip().startswith("|"))   # tables are reference lists, not prose
    b = re.sub(r"\]\([^)]*\)", "]", b)
    b = re.sub(r"[#>*_`\[\]]", " ", b)
    return b


FEM_CACHE = {}


def fem_ok(target):
    page, _, anchor = target.partition("#")
    f = ROOT / "library/feminine" / f"{page}.html"
    if not f.exists():
        return False
    if page not in FEM_CACHE:
        FEM_CACHE[page] = f.read_text(encoding="utf-8")
    return not anchor or anchor == "top" or f'id="{anchor}"' in FEM_CACHE[page]


def audit(slug, ch):
    m, body = ch["meta"], ch["body"]
    fails, warns = [], []
    plan = CH.get(slug)
    if not plan:
        return ["not in plan.json"], [], 0
    is_chapter = plan["part"] not in ("start", "tools")
    for k in ("title", "question", "seo", "short"):
        if k not in m:
            fails.append(f"missing header field '{k}'")
    text = prose(body)
    W = words(text)
    nw = len(W)
    # search phrase
    kw = [t for t in re.findall(r"[a-z0-9']+", plan["keyword"].lower()) if t not in STOP]
    def has(s):
        s = s.lower().replace("’", "'")
        return all(re.search(r"\b" + re.escape(t), s) for t in kw)
    if not (has(m.get("seo", "")) or has(m.get("title", ""))):
        fails.append(f"search phrase '{plan['keyword']}' not in title or browser title")
    if not has(m.get("short", "")):
        fails.append(f"search phrase '{plan['keyword']}' not in the short answer")
    if not has(text):
        warns.append(f"search phrase '{plan['keyword']}' not in the body")
    if len(m.get("seo", "")) > 65:
        warns.append(f"browser title {len(m['seo'])} characters (Google shows about 60)")
    sl = len(m.get("short", ""))
    if not 90 <= sl <= 420:
        warns.append(f"short answer {sl} characters (aim 120 to 320)")
    # links
    links = re.findall(r"\]\(([^)]+)\)", body)
    internal = [l for l in links if l.startswith("ch:")]
    for l in internal:
        if l[3:].split("#")[0] not in CH:
            fails.append(f"link to unknown chapter {l}")
    for l in links:
        if l.startswith("/playbook/") and not (ROOT / "instruments/playbook/site" / (l[10:].split("#")[0] + ".html")).exists():
            fails.append(f"Decoder page missing: {l}")
        if l.startswith("/feminine/") and not fem_ok(l[10:]):
            fails.append(f"Feminine page or anchor missing: {l}")
    for d in plan["decoder"]:
        if f"/playbook/{d}" not in links:
            fails.append(f"required Decoder link missing: /playbook/{d}")
    for fm in plan["feminine"]:
        if not any(l == f"/feminine/{fm}" or l.startswith(f"/feminine/{fm.split('#')[0]}") for l in links):
            fails.append(f"required Feminine link missing: /feminine/{fm}")
    if is_chapter and len(set(internal)) < 3:
        fails.append(f"only {len(set(internal))} links to other chapters (want 3+)")
    # questions + sources
    heads = re.findall(r"^## (.+)$", body, re.M)
    if is_chapter and not any(h.strip().endswith("?") for h in heads):
        fails.append("no heading phrased as the reader's question")
    if is_chapter:
        src = body.split("\n## Sources", 1)
        if len(src) < 2 or not re.search(r"^- ", src[1], re.M):
            fails.append("no Sources section")
    # voice
    low = text.lower().replace("’", "'")
    for p in BANNED:
        n = len(re.findall(p, low))
        if n:
            fails.append(f"filler '{p.strip(chr(92)+'b')}' x{n}")
    rt = len(re.findall(r"\brather than\b", low))
    if rt > 2:
        fails.append(f"'rather than' x{rt}")
    dashes = len(re.findall(r"[—–]", body.split("\n## Sources")[0].split("\n## Research and books")[0]))
    if nw and dashes * 1000 / nw > 3:
        fails.append(f"{dashes} dashes ({dashes * 1000 / nw:.1f} per 1,000 words; limit 3)")
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(words(s)) > 2]
    if sents:
        L = [len(words(s)) for s in sents]
        avg = sum(L) / len(L)
        if avg > 17:
            fails.append(f"average sentence {avg:.1f} words (limit 17)")
        long_ = [s.strip()[:60] for s in sents if len(words(s)) > 40]
        if long_:
            fails.append(f"{len(long_)} sentence(s) over 40 words: '{long_[0]}...'")
        fk = 206.835 - 1.015 * (nw / len(sents)) - 84.6 * (sum(syllables(w) for w in W) / max(1, nw))
        if fk < 55 and plan["part"] != "tools":   # checklists, directories and the glossary are reference lists
            fails.append(f"reading ease {fk:.0f} (want 55+)")
    for p in PRESCRIBE:
        if re.search(p, low):
            fails.append(f"prescribes a feeling or timeline: '{p}'")
    for p in METHOD:
        if re.search(p, low):
            fails.append(f"method-level wording: '{p}'")
    if plan["heavy"] and slug != "when-its-more-than-aftermath" and not any(c in body for c in CRISIS):
        fails.append("heavy chapter without a link to a crisis route")
    if is_chapter and nw < 350:
        warns.append(f"only {nw} words: is the information complete?")
    return fails, warns, nw


def main():
    want = set(sys.argv[1:])
    chs = parse()
    order = [c["slug"] for c in PLAN["chapters"] if not want or c["part"] in want]
    total, bad, written = 0, 0, 0
    for slug in order:
        if slug not in chs:
            continue
        written += 1
        f, w, n = audit(slug, chs[slug])
        total += n
        flag = "FAIL" if f else ("warn" if w else " ok ")
        bad += bool(f)
        print(f"{flag} {CH[slug]['part']:>5}.{CH[slug]['n']:<2} {slug:52} {n:>5} w")
        for x in f:
            print(f"        FAIL {x}")
        for x in w:
            print(f"        warn {x}")
    extra = [s for s in chs if s not in CH]
    for s in extra:
        print(f"FAIL  {s}: written but not in plan.json"); bad += 1
    missing = [s for s in order if s not in chs]
    print(f"\n{written} written, {len(missing)} still to write, {total:,} words; {bad} failing")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
