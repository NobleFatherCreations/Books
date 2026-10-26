#!/usr/bin/env python3
"""Sentence-level copy-edit pass over the 310 Pattern Decoder entries.

  --extract OUTDIR [--per N]   write worklist-NN.json (items that need a plainer, more human wording)
  --apply FILE...              apply reply files ({id: new text}) to every copy of the text, with guards
  --report                     reading-level and pattern counts for the whole book

An id is  "<entry name>|<field>|<index or ->|<sub key or ->".  Edits go to content/playbook-data.json (what the build
reads), to the accepted batch files in content/codex-final/ (what the validator reads), and to the compendium copy.
An edit is refused unless the old text matches exactly where it is written and the new text passes the guards:
same numbers, same capitalised terms, same hedging words, no dashes, none of the banned words, a sane length.
"""
import argparse, collections, glob, json, os, re, statistics, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "content", "playbook-data.json")
FINAL = os.path.join(ROOT, "content", "codex-final")
SKIP = {"name", "tier", "tier_key", "branch", "category", "detectability_note", "aftermath_state", "forensic_only", "absorbs",
        "codex_maturity", "detection_notes", "human_review_flags", "related_tactics", "safety_sensitive", "what_it_sounds_like", "risk_flagged"}
VOC = re.compile(r"\b(delve|tapestry|crucial|landscape|journey|realm|testament|underscore[sd]?|pivotal|foster(?:s|ed|ing)?|robust|nuanced|intricate|multifaceted|navigat(?:e|es|ed|ing)|leverag(?:e|es|ed|ing)|holistic|empower(?:s|ed|ing)?|resonat(?:e|es|ed|ing)|myriad|plethora|moreover|furthermore|utiliz(?:e|es|ed|ing)|facilitat(?:e|es|ed|ing)|ultimately|essentially|fundamentally)\b", re.I)
HEDGE = ["can", "may", "might", "tends to", "tend to", "often", "usually", "sometimes", "could", "can be", "does not", "doesn't", "not"]


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(n, 1)


def sents(t): return [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]


def fk(t):
    s, w = sents(t), re.findall(r"[A-Za-z’']+", t)
    if not s or not w: return 0
    return 0.39 * len(w) / len(s) + 11.8 * sum(map(syl, w)) / len(w) - 15.59


def items(e):
    """Yield (field, index, sub, text) for every editable string of an entry."""
    for k, v in e.items():
        if k in SKIP: continue
        if isinstance(v, str): yield k, "-", "-", v
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, str): yield k, str(i), "-", x
        elif isinstance(v, dict):
            for kk, x in v.items():
                if isinstance(x, str): yield k, "-", kk, x


def reasons(t):
    why = []
    for s in sents(t):
        if len(s.split()) > 24: why.append("long sentence")
        if "—" in s or " -- " in s: why.append("dash")
        if re.search(r"\bnot just\b|\bnot only\b", s, re.I): why.append("not-just frame")
        if VOC.search(s): why.append("AI-flavoured word")
    if len(t.split()) >= 18 and fk(t) > 10.5: why.append("dense")
    return sorted(set(why))


def entries(): return json.load(open(DATA, encoding="utf-8"))["codex_completed"]


def extract(outdir, per):
    os.makedirs(outdir, exist_ok=True)
    ents = entries(); n = 0; work = []
    for e in ents:
        its = []
        for f, i, sub, t in items(e):
            r = reasons(t)
            if r: its.append({"id": "|".join([e["name"], f, i, sub]), "field": f, "why": r, "text": t})
        if its: work.append({"entry": e["name"], "about": e.get("short_definition", ""), "items": its})
    for b in range(0, len(work), per):
        chunk = work[b:b + per]; n += 1
        json.dump(chunk, open(os.path.join(outdir, "worklist-%02d.json" % n), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%d entries, %d items, %d worklists of up to %d entries" % (len(work), sum(len(w["items"]) for w in work), n, per))


def caps(t):
    """Capitalised terms that are not at the start of a sentence: names, acronyms, frameworks."""
    out = set()
    for s in sents(t):
        words = re.findall(r"[A-Za-z][A-Za-z’'\-]*", s)
        for w in words[1:]:
            if w[0].isupper() and w not in ("I", "I'm", "I’m", "I'll", "I’ll", "I've", "I’ve", "I'd", "I’d"): out.add(w)
    return out


def check(old, new):
    bad = []
    if not new or not new.strip(): return ["empty"]
    if new == old: return ["unchanged"]
    if "—" in new or " -- " in new or "–" in new: bad.append("dash")
    m = VOC.search(new)
    if m and m.group(0).lower() not in old.lower(): bad.append("banned word: " + m.group(0))
    if re.search(r"\bnot (?:just|only)\b", new, re.I) and not re.search(r"\bnot (?:just|only)\b", old, re.I): bad.append("new not-just frame")
    if sorted(re.findall(r"\d[\d,.%]*", old)) != sorted(re.findall(r"\d[\d,.%]*", new)): bad.append("numbers changed")
    miss = caps(old) - caps(new) - set(re.findall(r"[A-Za-z][A-Za-z’'\-]*", new))
    if miss: bad.append("terms lost: " + ", ".join(sorted(miss)))
    ow, nw = len(old.split()), len(new.split())
    if nw < ow * 0.45 or nw > ow * 1.35 + 4: bad.append("length %d -> %d" % (ow, nw))
    for q in re.findall(r"[“\"]([^”\"]{6,})[”\"]", old):
        if q not in new: bad.append("quoted words changed")
    if old.rstrip()[-1:] in ".?!" and new.rstrip()[-1:] not in ".?!”\"": bad.append("lost final punctuation")
    if "?" in old.rstrip()[-2:] and "?" not in new: bad.append("question became a statement")
    lo = " " + old.lower() + " "; ln = " " + new.lower() + " "
    for h in ("can", "may", "might", "could", "tends to", "tend to"):
        if (" " + h + " ") in lo and (" " + h + " ") not in ln and not any((" " + x + " ") in ln for x in ("can", "may", "might", "could", "tends to", "tend to", "often", "usually", "sometimes", "likely")):
            bad.append("hedge lost: " + h); break
    lo_n = re.sub(r"\bnot (?:just|only)\b", "", lo)
    for neg in (" not ", " never ", " no ", "n't", "n’t"):
        if neg in lo_n and neg not in ln and not any(x in ln for x in (" not ", " never ", " no ", "n't", "n’t", " without ", " nothing ", " none ", " neither ", " nor ")):
            bad.append("a negation was lost"); break
    return bad


def enc(t, ascii_):
    return json.dumps(t, ensure_ascii=ascii_)


def apply(files):
    """Check every proposed edit against the parsed book, then change the raw text of each file in place, so nothing but
    the edited strings differs (these files are formatted unevenly; re-serialising would rewrite thousands of lines)."""
    base = {x["name"]: x for x in json.load(open(DATA, encoding="utf-8"))["codex_completed"]}
    accepted = {}; refused = 0; log = []
    for fn in files:
        for id_, new in json.load(open(fn, encoding="utf-8")).items():
            name, f, i, sub = id_.split("|")
            rec = base.get(name); old = None
            if rec:
                for ff, ii, ss, t in items(rec):
                    if (ff, ii, ss) == (f, i, sub): old = t
            if old is None: refused += 1; log.append((id_, "no such item")); continue
            new = new.strip(); bad = check(old, new)
            if bad: refused += 1; log.append((id_, "; ".join(bad))); continue
            accepted[old] = new
    paths = [DATA] + sorted(glob.glob(os.path.join(FINAL, "batch-*.json")) + glob.glob(os.path.join(FINAL, "merged-*.json"))) + [os.path.join(FINAL, "exemplars.json")]
    raws = {p: open(p, encoding="utf-8").read() for p in paths}; hits = collections.Counter()
    for old, new in accepted.items():
        for p in paths:
            for ascii_ in (False, True):
                o, n = enc(old, ascii_), enc(new, ascii_)
                c = raws[p].count(o)
                if c:
                    raws[p] = raws[p].replace(o, n); hits[old] += c
    for old in accepted:
        if hits[old] == 0: log.append((old[:50], "not found in any file")); refused += 1
        elif hits[old] > 4: log.append((old[:50], "text appears %d times" % hits[old]))
    for p in paths: json.loads(raws[p])
    return raws, len([o for o in accepted if hits[o]]), refused, log


def write(raws):
    for p, raw in raws.items():
        if open(p, encoding="utf-8").read() != raw:
            with open(p, "w", encoding="utf-8") as fh: fh.write(raw)


def report():
    ents = entries(); g = []; c = collections.Counter()
    for e in ents:
        blob = " ".join(t for _, _, _, t in items(e)); g.append(fk(blob))
        for _, _, _, t in items(e):
            for r in reasons(t): c[r] += 1
    print("entries %d  mean grade %.2f  median %.2f  above 8: %d  above 7: %d" % (len(g), statistics.mean(g), statistics.median(g), sum(x > 8 for x in g), sum(x > 7 for x in g)))
    print(dict(c))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract"); ap.add_argument("--per", type=int, default=25)
    ap.add_argument("--apply", nargs="+"); ap.add_argument("--report", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    if a.extract: extract(a.extract, a.per)
    if a.report: report()
    if a.apply:
        raws, done, refused, log = apply(a.apply)
        if not a.dry: write(raws)
        print("applied %d, refused %d%s" % (done, refused, " (dry run, nothing written)" if a.dry else ""))
        for id_, why in log[:400]: print("  REFUSED", id_, "::", why)
