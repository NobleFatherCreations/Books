#!/usr/bin/env python3
"""Make the Bible's guide-count strings derive from the data, not literals.

The page said "Section N of 12" and "Twelve Guides. One Community." as fixed
text. Adding a thirteenth guide made both wrong -- the same class of bug as
the hardcoded 'v6' version badge. The two in the render path now read
FESTIE_DATA.guides.length; the two in static chrome (the meta description and
THE HOUSE drawer row) cannot, so festie-check.py asserts them instead.
"""
import json
import re
import sys

DATA = "content/festie-bible-data.json"
PAGE = "library/festival/index.html"
WORDS = {12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen",
         16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen", 20: "Twenty",
         21: "Twenty-One", 22: "Twenty-Two", 23: "Twenty-Three", 24: "Twenty-Four", 25: "Twenty-Five", 26: "Twenty-Six", 27: "Twenty-Seven", 28: "Twenty-Eight", 29: "Twenty-Nine", 30: "Thirty"}


def main():
    d = json.load(open(DATA, encoding="utf-8"))
    n = len(d["guides"])
    word = WORDS.get(n, str(n))
    s = open(PAGE, encoding="utf-8").read()
    before = s
    notes = []

    # 1. "Section N of 12" in the guide intro
    old = "'<div class=\"fb-section-of\">Section '+g.sectionOf+' of 12</div>'+"
    new = "'<div class=\"fb-section-of\">Section '+g.sectionOf+' of '+FESTIE_DATA.guides.length+'</div>'+"
    if old in s:
        s = s.replace(old, new); notes.append("'Section N of 12' now derives from the data")

    # 2. the table-of-contents heading
    old = "'<div class=\"fb-toc-head\"><h2>Twelve Guides. One Community.</h2>"
    new = ("'<div class=\"fb-toc-head\"><h2>'+GUIDE_COUNT_WORD+' Guides. One Community.</h2>")
    if old in s:
        s = s.replace(old, new)
        # define the word list next to the data so it travels with it
        anchor = "\n(function(){\n\"use strict\";\n"
        decl = ("\nvar GUIDE_COUNT_WORD = ({12:'Twelve',13:'Thirteen',14:'Fourteen',15:'Fifteen',"
                "16:'Sixteen',17:'Seventeen',18:'Eighteen',19:'Nineteen',20:'Twenty'})"
                "[FESTIE_DATA.guides.length] || String(FESTIE_DATA.guides.length);\n")
        s = s.replace(anchor, anchor + decl, 1)
        notes.append("the contents heading now derives from the data")

    # 3 + 4. static chrome that cannot read the data -- corrected in place
    s2 = re.sub(r"(<meta name=\"description\" content=\"[^\"]*?— )\w+( guides, one community)",
                lambda m: m.group(1) + word.lower() + m.group(2), s)
    if s2 != s:
        s = s2; notes.append(f"meta description says {word.lower()} guides")
    s2 = re.sub(r"(<span class=\"nf-desc\">)\w+( guides for the festival world</span>)",
                lambda m: m.group(1) + word + m.group(2), s)
    if s2 != s:
        s = s2; notes.append(f"THE HOUSE drawer row says {word} guides")

    if s != before:
        open(PAGE, "w", encoding="utf-8").write(s)
    for x in notes:
        print("  " + x)
    if not notes:
        print("  (already derived / correct)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
