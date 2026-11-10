#!/usr/bin/env python3
"""Credibility tag resolution (content/fractal2/TAG-POLICY.md).   python3 design/fractal-sector/resolve.py <sector> <step>

  classify   every review_queue item gets a ledger entry; the mechanical verdicts are filled in, the rest go to
             resolution/todo.jsonl for the model step (research + judgment)
  check      the ledger is complete and safe to apply (exit 1 if not)
  summary    writes resolution/SUMMARY.md

The ledger is the derived layer. The author's files are read, never written.
  content/fractal/<s>/resolution/ledger.json   one entry per queue item, in queue order
  content/fractal/<s>/resolution/facts.json    the sector fact base (written by the research step)
build.py applies the ledger in memory through apply_ledger() below.
"""
import collections
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERDICTS = {"keep-label", "keep-conditional", "keep-cited", "generalize", "soften", "remove", "no-change", "escalate"}
REWRITES = {"generalize", "soften", "remove"}
PROTECTED = {"Safety Note (read first)", "Escalation Triggers — Specific", "Safer Response Language", "Chain Breakers", "Evidence To Preserve — Additions"}
SCENE = {"Cold Open", "The Name"}
CONDITIONAL = re.compile(r"\b[Ww]hether\b.{0,200}\bdepends?\b|\bdepends? on\b.{0,80}\b(terms|agreement|contract|place)\b|\bthe difference lies in\b", re.S)
ROUTING = re.compile(r"question for (a )?qualified|matters? for qualified|qualified (counsel|review|professional|adviser|advisor)|independent (adviser|advisor|attorney|counsel)|second perspective", re.I)
CHECKABLE = re.compile(r"\d|\$|£|€|\bpercent\b|\b(Act|Code|Statute|Directive|Regulation)\b")
TAG = re.compile(r"\[(REQUIRES SUBJECT-MATTER REVIEW|VERIFIED SOURCE NEEDED|HISTORICAL EXAMPLE TO VERIFY|LEGAL CLAIM[^\]]*|COMMON INDUSTRY PATTERN|HYPOTHETICAL COMPOSITE)\]")
# Real organizations a script must never present as acting. Extend per sector in content/fractal/<s>/nav.json → "entities".
ENTITIES = ["Spotify", "Apple Music", "YouTube", "TikTok", "Instagram", "Facebook", "Meta", "Twitter", "Amazon", "SoundCloud", "Bandcamp", "Universal Music", "Sony Music", "Warner Music",
            "Live Nation", "Ticketmaster", "AEG", "Billboard", "Grammy", "Recording Academy", "ASCAP", "BMI", "SESAC", "SAG-AFTRA", "Netflix", "Disney", "Coachella", "Glastonbury"]


def paths(sector):
    base = ROOT / "content/fractal" / sector
    return base, base / "build/review_queue.json", base / "build/sector.json", base / "resolution"


def blocks(text):
    out = []
    for b in re.split(r"\n\s*\n", text):
        lines = [l for l in b.split("\n") if l.strip()]
        if lines and all(re.match(r"\s*(?:[-*]|\d+\.)\s", l) for l in lines):
            out += lines
        elif b.strip():
            out.append(b.strip())
    return out


def context_for(item, combo, used):
    """The block (paragraph or list item) of the script section that holds this queue item."""
    sec = combo["sections"].get(item["section"], "")
    text = item["text"].strip()
    bare = bool(re.fullmatch(r"(\s*\[[^\]]+\]\s*)+", text))
    for i, b in enumerate(blocks(sec)):
        key = (combo["combo_id"], item["section"], i)
        if not bare and text[:60] in b:
            return b
        if bare and ("[%s]" % item["tag"]) in b and key not in used:
            used.add(key)
            return b
    return text


def classify(sector):
    base, qf, sf, rdir = paths(sector)
    queue = json.loads(qf.read_text())
    data = json.loads(sf.read_text())
    combos = {c["combo_id"]: c for c in data["combos"]}
    rdir.mkdir(exist_ok=True)
    old = {}
    lf = rdir / "ledger.json"
    if lf.exists():                                        # keep decisions already made by the model or the director
        old = {e["q"]: e for e in json.loads(lf.read_text()) if e.get("by", "rule") != "rule"}
    today = datetime.date.today().isoformat()
    ledger, todo, used = [], [], set()
    for q, it in enumerate(queue):
        c = combos[it["combo_id"]]
        e = {"q": q, "combo_id": it["combo_id"], "section": it["section"], "kind": it["kind"], "tag": it["tag"],
             "verdict": None, "fact": None, "before": None, "after": None, "reason": "", "by": "rule", "checked": today, "risk": "low"}
        if q in old:
            ledger.append(old[q]); continue
        kind, text = it["kind"], it["text"]
        if kind in ("composite", "legal"):
            e.update(verdict="keep-label", reason="descriptive label")
        elif kind == "pattern":
            ctx = context_for(it, c, used)
            if CHECKABLE.search(TAG.sub("", ctx)):
                e.update(before=ctx, reason="common-pattern line states something checkable (number, law or date)"); todo.append(dict(e, task="research"))
            else:
                e.update(verdict="keep-label", reason="hedged general practice; descriptive label")
        elif kind in ("review", "source"):
            ctx = context_for(it, c, used)
            e["before"] = ctx
            body = TAG.sub("", ctx)
            if kind == "review" and (CONDITIONAL.search(body) or ROUTING.search(body)):
                e.update(verdict="keep-conditional", reason="routes to qualified help" if ROUTING.search(body) else "outcome stated as depending on the terms; no factual claim",
                         label="Ask a qualified person" if ROUTING.search(body) else "Depends on the terms")
            else:
                todo.append(dict(e, task="research"))
        elif it["tag"] == "Claims needing verification":
            script = "\n".join(c["sections"].values())
            named = [n for n in ENTITIES if re.search(r"\b%s\b(?!-)" % re.escape(n), script)]
            listed = set(TAG.findall(text))
            # every scene carries the site's own Composite label, so a composite tag named only in the note needs nothing
            missing = [t for t in listed if ("[%s]" % t) not in script and t != "HYPOTHETICAL COMPOSITE"]
            if named:
                e.update(verdict="escalate", risk="high", reason="real organization named in script: %s" % named)
            elif missing:
                e["before"] = text
                todo.append(dict(e, task="confirm-note", absent_tags=missing))
            else:
                e.update(verdict="no-change", reason="every tag the note lists is in the script; no real organization named (scan of %d names)" % len(ENTITIES))
        elif it["tag"] == "Overapplication risks":
            fp = c["sections"].get("False-Positive Check — Specific", "")
            e["before"] = text
            if len(fp.split()) >= 40:
                todo.append(dict(e, task="confirm-covered", false_positive_check=fp))
            else:
                e.update(verdict="escalate", risk="medium", reason="False-Positive Check section missing or very short")
        else:                                              # Overstatement risks, Sector accuracy check
            e["before"] = text
            todo.append(dict(e, task="overstatement" if it["tag"] == "Overstatement risks" else "sector-accuracy"))
        if e["verdict"] is None:
            e["by"] = "pending"
        ledger.append(e)
    lf.write_text(json.dumps(ledger, indent=1, ensure_ascii=False))
    (rdir / "todo.jsonl").write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in todo))
    cnt = collections.Counter(e["verdict"] or "pending" for e in ledger)
    print("%s: %d queue items -> %s" % (sector, len(ledger), dict(cnt)))
    print("todo by task:", dict(collections.Counter(t["task"] for t in todo)))


def load(sector):
    base, qf, sf, rdir = paths(sector)
    lf, ff = rdir / "ledger.json", rdir / "facts.json"
    ledger = json.loads(lf.read_text()) if lf.exists() else []
    facts = {f["id"]: f for f in json.loads(ff.read_text())} if ff.exists() else {}
    return ledger, facts


def patches_of(e):
    """A ledger entry may carry one rewrite (before/after) or several ("patches": [{section, before, after}])."""
    if e.get("patches"):
        return [(p.get("section", e["section"]), p["before"], p["after"]) for p in e["patches"]]
    if e.get("verdict") in REWRITES and e.get("after") is not None and e.get("before"):
        return [(e.get("patch_section", e["section"]), e["before"], e["after"])]
    return []


def check(sector, strict=True):
    base, qf, sf, rdir = paths(sector)
    queue = json.loads(qf.read_text())
    data = json.loads(sf.read_text())
    combos = {c["combo_id"]: c for c in data["combos"]}
    ledger, facts = load(sector)
    bad = []
    if len(ledger) != len(queue):
        bad.append("ledger has %d entries, queue has %d" % (len(ledger), len(queue)))
    for e in ledger:
        v = e.get("verdict")
        if v is None:
            if strict:
                bad.append("q%d: no verdict" % e["q"])
            continue
        if v not in VERDICTS:
            bad.append("q%d: unknown verdict %s" % (e["q"], v))
        if v == "keep-cited" or (v == "generalize" and e.get("fact")):
            f = facts.get(e.get("fact"))
            ok = f and f.get("sources") and all(s.get("url") and s.get("title") and s.get("publisher") and s.get("accessed") and s.get("quote") for s in f["sources"])
            if not ok:
                bad.append("q%d: %s without a complete citation (fact %s)" % (e["q"], v, e.get("fact")))
        for sec, before, after in patches_of(e):
            if sec in PROTECTED and not e.get("escalated"):
                bad.append("q%d: rewrite in protected section %s without escalation" % (e["q"], sec))
            if before not in combos[e["combo_id"]]["sections"].get(sec, ""):
                bad.append("q%d: 'before' text not found in %s / %s" % (e["q"], e["combo_id"], sec))
        if v in REWRITES and not patches_of(e):
            bad.append("q%d: %s with nothing to apply" % (e["q"], v))
    for fid, f in facts.items():
        for s in f.get("sources", []):
            if len(s.get("quote", "").split()) > 25:
                bad.append("%s: quote longer than 25 words" % fid)
    print("ledger check: %d entries, %d problems" % (len(ledger), len(bad)))
    for b in bad[:40]:
        print("  -", b)
    return not bad


def apply_ledger(data, sector):
    """Called by build.py. Rewrites section text in memory; returns ({combo_id: word delta}, per-combo resolution info)."""
    ledger, facts = load(sector)
    combos = {c["combo_id"]: c for c in data["combos"]}
    delta, info = collections.Counter(), {}
    wc = lambda s: len(re.findall(r"\S+", re.sub(r"\[[^\[\]\n]{1,120}\]", " ", s)))
    for e in ledger:
        c = combos.get(e["combo_id"])
        if not c or not e.get("verdict"):
            continue
        d = info.setdefault(e["combo_id"], {"cited": 0, "reworded": 0, "removed": 0, "conditional": 0, "pending": 0, "facts": [], "labels": {}})
        v = e["verdict"]
        for sec, before, after in patches_of(e):
            txt = c["sections"].get(sec, "")
            if before in txt:
                c["sections"][sec] = txt.replace(before, after, 1)
                delta[e["combo_id"]] += wc(after) - wc(before)
        if v == "keep-cited":
            d["cited"] += 1
        elif v in ("generalize", "soften"):
            d["reworded"] += 1
        elif v == "remove":
            d["removed"] += 1
        elif v == "keep-conditional":
            d["conditional"] += 1
        if e.get("fact") and e["fact"] in facts and e["fact"] not in d["facts"]:
            d["facts"].append(e["fact"])
        if e["kind"] in ("review", "source") and e.get("before"):
            lab = {"keep-conditional": e.get("label", "Depends on the terms"), "keep-cited": "Source checked"}.get(v)
            if v == "generalize" and e.get("fact"):
                lab = "Source checked"
            d["labels"][(e["section"], (e.get("after") if v in REWRITES else e["before"]) or "")[:2] + ("",)] = lab
    for e in ledger:
        if not e.get("verdict") and e["combo_id"] in combos:
            info.setdefault(e["combo_id"], {"cited": 0, "reworded": 0, "removed": 0, "conditional": 0, "pending": 0, "facts": [], "labels": {}})["pending"] += 1
    return dict(delta), info, facts


def summary(sector):
    base, qf, sf, rdir = paths(sector)
    ledger, facts = load(sector)
    cnt = collections.Counter(e.get("verdict") or "pending" for e in ledger)
    out = ["# %s — tag resolution summary" % sector.upper(), "", "Generated %s by `design/fractal-sector/resolve.py`. Policy: `content/fractal2/TAG-POLICY.md`." % datetime.date.today().isoformat(), "",
           "| Verdict | Items |", "|---|---|"] + ["| %s | %d |" % (k, v) for k, v in sorted(cnt.items(), key=lambda x: -x[1])] + ["", "Total: %d queue items. Fact base: %d topics, %d with at least one source, %d with none." % (
               len(ledger), len(facts), sum(1 for f in facts.values() if f.get("sources")), sum(1 for f in facts.values() if not f.get("sources"))), ""]
    for title, pick in [("High-risk changes (owner approves each)", lambda e: e.get("risk") == "high"), ("Removals", lambda e: e.get("verdict") == "remove"),
                        ("Rewordings (medium risk)", lambda e: e.get("verdict") in ("generalize", "soften") and e.get("risk") != "high")]:
        rows = [e for e in ledger if pick(e)]
        out += ["## %s (%d)" % (title, len(rows)), ""]
        for e in rows[:400]:
            out += ["- **%s · %s** (%s, q%d): %s" % (e["combo_id"], e["section"], e["verdict"], e["q"], e.get("reason", ""))]
            for sec, b, a in patches_of(e):
                out += ["  - before: %s" % b.replace("\n", " ")[:400], "  - after: %s" % (a.replace("\n", " ")[:400] or "(removed)")]
        out.append("")
    out += ["## Topics with no reliable source", ""] + ["- %s: %s" % (f["id"], f["topic"]) for f in facts.values() if not f.get("sources")] + [""]
    (rdir / "SUMMARY.md").write_text("\n".join(out))
    print("wrote", rdir / "SUMMARY.md")


if __name__ == "__main__":
    a = sys.argv[1:]
    sector, step = (a[0] if a else "ent"), (a[1] if len(a) > 1 else "classify")
    if step == "classify":
        classify(sector)
    elif step == "check":
        sys.exit(0 if check(sector, strict="--final" in a) else 1)
    elif step == "summary":
        summary(sector)
