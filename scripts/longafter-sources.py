#!/usr/bin/env python3
"""Build the "Every source in this book" appendix (chapter all-sources) from every chapter's Sources list.

  - collects every source line, de-duplicates, notes which chapters cite it
  - groups: research and books / laws and official guidance / services, organisations and tools
  - links: research articles get a DOI from Crossref (cached in content/longafter-v2/dois.json; only accepted when the
    title matches closely and the year agrees); services get their own website where the line names a domain or a
    known organisation; UK laws link to a legislation.gov.uk title search
Rewrites the "=== all-sources" block in content/longafter-v2/12-tools.md. Run before building.
Usage: python3 scripts/longafter-sources.py [--no-lookup]
"""
import re, glob, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "content/longafter-v2"
CACHE = D / "dois.json"
cache = json.load(open(CACHE)) if CACHE.exists() else {}
LOOKUP = "--no-lookup" not in sys.argv
plan = json.load(open(D / "plan.json")); TITLE = {c["slug"]: c["title"] for c in plan["chapters"]}

KNOWN = {  # organisation name fragment -> website (well-established official sites only)
    "National Domestic Violence Hotline": "https://www.thehotline.org", "National Domestic Abuse Helpline": "https://www.nationaldahelpline.org.uk",
    "Samaritans": "https://www.samaritans.org", "988 Suicide and Crisis Lifeline": "https://988lifeline.org", "1800RESPECT": "https://www.1800respect.org.au",
    "Women's Aid Ireland": "https://www.womensaid.ie", "Men's Aid Ireland": "https://www.mensaid.ie", "ShelterSafe": "https://www.sheltersafe.ca",
    "Relay UK": "https://www.relayuk.bt.com", "National Relay Service": "https://www.accesshub.gov.au", "Rape Crisis England": "https://rapecrisis.org.uk",
    "RAINN": "https://rainn.org", "StopNCII": "https://stopncii.org", "Take It Down": "https://takeitdown.ncmec.org", "Federal Trade Commission": "https://www.ftc.gov",
    "Surviving Economic Abuse": "https://survivingeconomicabuse.org", "NICE": "https://www.nice.org.uk", "Hourglass": "https://wearehourglass.org",
    "SignHealth": "https://signhealth.org.uk", "love is respect": "https://www.loveisrespect.org", "Reunite International": "https://www.reunite.org",
    "Children's Passport Issuance Alert Program": "https://travel.state.gov/CPIAP", "Galop": "https://galop.org.uk", "Men's Advice Line": "https://mensadviceline.org.uk",
    "Cafcass": "https://www.cafcass.gov.uk", "SafeLives": "https://safelives.org.uk", "Suzy Lamplugh Trust": "https://www.suzylamplugh.org",
    "Women's Refuge NZ": "https://womensrefuge.org.nz", "Shelter England": "https://england.shelter.org.uk", "Electoral Commission": "https://www.electoralcommission.org.uk",
    "National Association of Child Contact Centres": "https://naccc.org.uk", "Fair Work Ombudsman": "https://www.fairwork.gov.au", "Employment New Zealand": "https://www.employment.govt.nz",
    "Childline": "https://www.childline.org.uk", "eSafety Commissioner": "https://www.esafety.gov.au", "Cyber Civil Rights Initiative": "https://cybercivilrights.org",
}
DOMAIN = re.compile(r"\b((?:[a-z0-9-]+\.)+(?:org|org\.uk|gov\.uk|gov|co\.uk|ca|ie|org\.au|gov\.au|nz|org\.nz|govt\.nz|com|uk))\b")


def kind(line):
    if re.search(r"\(\d{4}[a-z]?\)", line) or re.search(r"\*[^*]+\*.*(Press|Books|Publishing|Putnam|Viking|Routledge)", line):
        return "research"
    if re.search(r"\b(Act|Code|Practice Direction|Rules|U\.S\.C\.|C\.F\.R\.|Convention|Order|Regulations|guidance|guideline|Directive)\b", line):
        return "law"
    return "service"


def doi_for(line):
    if line in cache:
        return cache[line]
    m = re.search(r"\((\d{4})\)\.?\s*(.+?)(?:\.\s*\*|\*)", line)
    if not m or not LOOKUP:
        return None
    year, title = m.group(1), m.group(2).strip(' ."')
    q = urllib.parse.quote(line[:300])
    try:
        req = urllib.request.Request(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3",
                                     headers={"User-Agent": "longafter-sources/1.0 (book reference check)"})
        items = json.load(urllib.request.urlopen(req, timeout=20))["message"]["items"]
    except Exception:
        return None
    tw = set(re.findall(r"[a-z]{4,}", title.lower()))
    best = None
    for it in items:
        t = " ".join(it.get("title", [""]))
        iw = set(re.findall(r"[a-z]{4,}", t.lower()))
        overlap = len(tw & iw) / max(1, len(tw))
        y = str((it.get("issued", {}).get("date-parts") or [[None]])[0][0])
        if overlap >= 0.7 and y.isdigit() and abs(int(y) - int(year)) <= 1:
            best = "https://doi.org/" + it["DOI"]; break
    cache[line] = best
    time.sleep(0.4)
    return best


def link_for(line, k):
    if k == "research":
        return doi_for(line)
    for name, url in KNOWN.items():
        if name.lower() in line.lower():
            return url
    m = DOMAIN.search(line)
    if m and "." in m.group(1) and not m.group(1).endswith((".md",)):
        return "https://" + m.group(1)
    if k == "law":
        m = re.match(r"([A-Z][A-Za-z()' ,-]+? Act \d{4})", line)
        if m and not any(x in line for x in ("U.S.", "Ireland", "New Zealand", "Canada", "Australia", "Scotland) Act")):
            return "https://www.legislation.gov.uk/search?title=" + urllib.parse.quote(m.group(1))
    return None


src = {}
for f in sorted(glob.glob(str(D / "[0-9]*.md"))):
    for blk in re.split(r"^=== ", open(f).read(), flags=re.M)[1:]:
        slug = blk.split("\n", 1)[0].strip()
        if slug == "all-sources" or "\n## Sources\n" not in blk:
            continue
        for l in blk.split("\n## Sources\n", 1)[1].splitlines():
            if l.startswith("- "):
                src.setdefault(l[2:].strip(), []).append(slug)

groups = {"research": [], "law": [], "service": []}
for line, chs in sorted(src.items(), key=lambda x: x[0].lower()):
    k = kind(line)
    url = link_for(line, k)
    shown = line.rstrip(".")
    where = ", ".join(f"[{TITLE[c]}](ch:{c})" for c in dict.fromkeys(chs) if c in TITLE)
    url = url.replace("(", "%28").replace(")", "%29") if url else url   # brackets would end the Markdown link early
    item = f"- {shown}." + (f" [Link]({url})" if url else "") + f" Cited in: {where}."
    groups[k].append(item)
json.dump(cache, open(CACHE, "w"), indent=1, ensure_ascii=False)

n_link = sum(1 for g in groups.values() for i in g if "[Link](" in i)
body = f"""=== all-sources
title: Every source in this book
question: Where does the information in this book come from?
seo: Domestic Abuse Research Sources: Every Reference
short: This page lists every source this guide cites as domestic abuse research sources, {len(src)} in all: research studies and books, laws and official guidance, and the services and organisations named in the chapters. Each one shows which chapters use it, with a link where one could be confirmed.
---
Every chapter of this book ends with its own list of sources. This page brings them together, so you, an advocate or a researcher can see the whole base the book stands on. It's here for checking, not for reading straight through, and it doubles as a list of domestic abuse research sources for anyone studying the subject.

## How are the sources chosen?
The book uses published research where it exists, the laws and official guidance that apply, and the national services that people can call. Where research is thin or disputed, the chapter says so. [What this book might have wrong](ch:what-this-book-might-have-wrong) explains the weak spots, and [For professionals](ch:for-professionals) explains how to cite the book.

## How do the links work?
Research articles link to their DOI, a permanent address for the article, where one could be matched with confidence. Services link to their own websites. Laws in the UK link to a search on the official legislation site. {n_link} of {len(src)} sources have a link. Laws, helpline numbers and services change, so check the current position where you live. The [A to Z](ch:a-to-z) explains the terms.

## Research and books
{chr(10).join(groups['research'])}

## Laws, courts and official guidance
{chr(10).join(groups['law'])}

## Services, organisations and tools
{chr(10).join(groups['service'])}
"""
p = D / "12-tools.md"; s = open(p).read()
if "=== all-sources\n" in s:
    st = s.index("=== all-sources\n"); en = s.find("\n=== ", st + 4); en = len(s) if en < 0 else en + 1
    s = s[:st] + body.rstrip("\n") + "\n" + ("\n" if en < len(s) else "") + s[en:]
else:
    s = s.rstrip("\n") + "\n\n" + body
open(p, "w").write(s)
print(f"{len(src)} sources: research {len(groups['research'])}, law {len(groups['law'])}, services {len(groups['service'])}; {n_link} linked")
