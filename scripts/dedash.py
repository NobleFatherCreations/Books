#!/usr/bin/env python3
"""Reduce em-dash density in a book's chapter bodies.

The no-ai-slop rule: an em dash earns its place when it clearly beats a
comma, period, colon or parentheses. As a default rhythm crutch it is the
loudest AI tell in prose, and these books run 7-15 per 1,000 words.

Each dash is judged with the full surrounding body as context, so a
term/gloss dash in a definition list and the closing half of a
parenthetical are both recognised for what they are. Anything it cannot
classify keeps its dash, so what survives is the set worth a human's
attention.

Never deletes or reorders text.   --dry reports only.
"""
import re, sys, pathlib
from collections import defaultdict

D = "\\u2014"
FINITE = {"is","are","was","were","has","have","had","does","do","did","will","would",
 "can","could","should","may","might","must","means","meant","happens","happened",
 "comes","came","goes","went","gets","got","takes","took","makes","made","tells","told",
 "says","said","costs","works","worked","stops","stopped","starts","started","leaves",
 "left","holds","held","counts","reads","looks","feels","felt","becomes","became",
 "stays","stayed","ends","ended","matters","mattered","applies","exists","existed",
 "needs","needed","changes","changed","tends","tended","seems","seemed","remains",
 "remained","carries","carried","produces","requires","depends","varies","belongs",
 "involves","reflects","isn","aren","wasn","weren","hasn","haven","hadn","doesn",
 "didn","don","won","wouldn","couldn","shouldn","tend","seem","remain","apply","exist",
 "covered","covers","explained","explains","described","describes","showed","shows",
 "noted","notes","listed","lists","set","put","gave","gives","give","told","meant",
 "asked","asks","calls","called","treats","treated","names","named","says","stated",
 "states","offers","offered","allows","allowed","prevents","prevented","stops","stop",
 "helps","helped","works","work","looked","felt","knew","knows","know","think","thought",
 "want","wants","wanted","went","become","came","happen","happens","include","includes"}
CONJ = {"and","but","or","so","yet","nor","which","because","not","though","although"}

def txt(s):
    return re.sub(r"<[^>]+>", " ", s).replace("\\u2019","’").replace("\\u201c",'"').replace("\\u201d",'"')

SUBJ = {"it","they","he","she","you","we","i","that","this","there","these","those",
 "nobody","nothing","everyone","someone","most","some","one","both","none","each"}
# A segment opening with one of these is a trailing modifier, never a new sentence.
MODIFIER = {"including","particularly","especially","such","meaning","drawn","based",
 "given","leaving","giving","making","taking","covered","applied","used","seen","often",
 "usually","sometimes","typically","generally","mostly","largely","partly","rather",
 "whether","unless","until","before","after","while","since","despite","without","with",
 "for","from","in","on","at","by","to","as","like","plus","and","but","or","not","no"}

def starts_clause(seg):
    """A subject pronoun or demonstrative followed closely by a finite verb.

    Deliberately narrow. A looser test turns trailing modifiers and noun
    phrases into sentence fragments, which is worse than leaving the dash.
    """
    t = txt(seg).strip()
    w = [x.lower() for x in re.findall(r"[A-Za-z’']+", t)]
    if len(w) < 3 or w[0] in MODIFIER or w[0] not in SUBJ:
        return False
    if re.match(r"^[A-Za-z’']+['’](s|re|ll|ve|d)\b", t, re.I):
        return True
    return any(x.rstrip("’'t") in FINITE for x in w[1:5])

def convert(body, stats):
    idxs = [m.start() for m in re.finditer(re.escape(D), body)]
    if not idxs:
        return body
    out, pos = "", 0
    keep = set()          # reached later, emitted as-is
    for k, i in enumerate(idxs):
        if i < pos:       # already consumed by a pair rewrite
            continue
        if i in keep:
            out += body[pos:i] + D; pos = i + len(D); continue
        before, after = body[:i], body[i + len(D):]
        # text of the segment this dash governs
        seg_raw = re.split(re.escape(D) + r"|[.!?](?=\s|<|$)|</?(?:p|li|h3|div|ul|ol)\b",
                           after, maxsplit=1)
        seg = txt(seg_raw[0]).strip()
        words = re.findall(r"[A-Za-z’']+", seg)
        first = words[0].lower() if words else ""

        # -- a term/gloss dash in a definition list: correct as it stands ----
        if re.search(r"</(strong|b|em|i)>\s*$", before) or \
           re.search(r"<li>\s*[^<>]{0,70}$", before) or \
           re.search(r"(\\u201d|”|&rdquo;)\s*$", before) or \
           re.search(r"(</p>|</li>|</h3>)\s*$", before) or not after.strip():
            stats["kept: definition gloss"] += 1
            # a pair opened by a kept dash keeps its closing dash as well
            close = next((j for j in idxs if j > i), None)
            if close is not None and not re.search(r"</?(p|li|h3|div|ul|ol)>", body[i:close]) \
               and not re.search(r"[.!?](\s|<)", txt(body[i + len(D):close])):
                keep.add(close)
            out += body[pos:i] + D; pos = i + len(D); continue

        # -- matched pair inside the same block: one parenthetical ----------
        nxt = next((j for j in idxs if j > i), None)
        if nxt is not None and not re.search(r"</?(p|li|h3|div|ul|ol)>", body[i:nxt]) \
           and not re.search(r"[.!?]\s", txt(body[i + len(D):nxt])):
            inner = body[i + len(D):nxt]
            tail = body[nxt + len(D):]
            if txt(inner).strip() and txt(tail).strip() and "," not in txt(inner) \
               and len(txt(inner).split()) <= 14:
                stats["pair -> commas"] += 1
                out += body[pos:i].rstrip() + ", " + inner.strip() + ", "
                pos = nxt + len(D)
                while pos < len(body) and body[pos] == " ":
                    pos += 1
                continue
            stats["pair kept (has commas)"] += 1
            out += body[pos:i] + D; pos = i + len(D)
            keep.add(nxt); continue

        # what this dash hangs off: back to the last sentence or block boundary
        LEAD = re.split(r"[.!?](?=\s|<)|</?(?:p|li|h3|div|ul|ol)\b", txt(before))[-1].strip()
        if not words:
            stats["kept: nothing follows"] += 1
            out += body[pos:i] + D; pos = i + len(D); continue

        pre = body[pos:i].rstrip()
        lead = LEAD
        bare = re.sub(r"[“\"‘'][^”\"’']{0,160}[”\"’']", " ", lead)
        lead_is_clause = bool(re.search(r"\b(" + "|".join(sorted(FINITE)) + r")\b", bare, re.I)) \
                         and not re.match(r"^(not|no)\b", bare.strip(), re.I)
        contrastive = bool(re.match(r"^(not|no)\b", txt(lead).strip(), re.I))
        if contrastive:
            # "Not X - Y" is a contrast; a comma reads as a list and loses it
            stats["-> colon (contrast)"] += 1; rep = ": "
        elif first in CONJ:
            stats["-> comma (conjunction)"] += 1; rep = ", "
        elif starts_clause(seg) and len(words) >= 4 and lead_is_clause:
            stats["-> full stop (clause)"] += 1; rep = ". """
        elif starts_clause(seg) and len(words) >= 4:
            # a gloss hanging off a noun phrase: colon, never a full stop
            stats["-> colon (gloss)"] += 1; rep = ": "
        elif seg.count(",") >= 2 and len(words) >= 5:
            stats["-> colon (series)"] += 1; rep = ": "
        elif "," not in seg and len(words) <= 10 and not any(
                x.lower().rstrip("’'t") in FINITE for x in words[:8]):
            stats["-> comma (appositive)"] += 1; rep = ", "
        elif lead_is_clause or any(
                x.lower().rstrip("’'t") in FINITE
                for x in re.findall(r"[A-Za-z’']+", seg)[:8]):
            # a complete clause, then its expansion: a colon is the plain
            # punctuation for this and reads as prose rather than as rhythm
            stats["-> colon (expansion)"] += 1; rep = ": "
        else:
            stats["-> comma (fallback)"] += 1; rep = ", "
        out += pre + rep
        pos = i + len(D)
        while pos < len(body) and body[pos] == " ":
            pos += 1

    out += body[pos:]
    out = re.sub(r"([.!?]\s+)([a-z])", lambda m: m.group(1)+m.group(2).upper(), out)
    out = re.sub(r"([.!?]\s*<[^>]+>\s*)([a-z])", lambda m: m.group(1)+m.group(2).upper(), out)
    out = re.sub(r",\s*,", ",", out)
    out = re.sub(r"[ ]+([,.;:])", r"\1", out)
    return out

def main():
    path = pathlib.Path(sys.argv[1]); dry = "--dry" in sys.argv
    s = path.read_text(encoding="utf-8")
    head, rest = s.split('<script id="book-js">', 1)
    js, tail = rest.split("</script>", 1)
    stats = defaultdict(int)
    was = sum(b.count(D) for b in re.findall(r"BODIES\[\d+\]=`([\s\S]*?)`;", js))
    new = re.sub(r"BODIES\[(\d+)\]=`([\s\S]*?)`;",
                 lambda m: f"BODIES[{m.group(1)}]=`" + convert(m.group(2), stats) + "`;", js)
    bodies = re.findall(r"BODIES\[\d+\]=`([\s\S]*?)`;", new)
    now = sum(b.count(D) for b in bodies); words = sum(len(b.split()) for b in bodies)
    print(f"{path.parent.name}: {was} -> {now} em dashes  ({now/words*1000:.2f} per 1k words)")
    for k in sorted(stats): print(f"    {k:26} {stats[k]}")
    if not dry:
        path.write_text(head + '<script id="book-js">' + new + "</script>" + tail, encoding="utf-8")

main()
