#!/usr/bin/env python3
"""Convert straight quotes to typographic ones in a book's chapter bodies.

The rest of the library uses typographic apostrophes and quotation marks
throughout (Playground 1146, The Weighing 44, The Repair 79, all with zero
straight ones in prose). Three of the four new books use straight quotes,
which is internally consistent but not the house convention.

Only text nodes are touched -- never markup -- so attribute values and the
JS around the bodies are untouched.  --dry reports only.
"""
import re, sys, pathlib

def smarten(text):
    # apostrophes: contractions, possessives, plural possessives
    text = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\\\\u2019", text)
    text = re.sub(r"(?<=[A-Za-z])'(?![A-Za-z])", "\\\\u2019", text)
    # double quotes: opening after start/space/opening punctuation, else closing
    out, open_q = [], True
    for ch in text:
        if ch == '"':
            out.append("\\\\u201c" if open_q else "\\\\u201d")
            open_q = not open_q
        else:
            if ch in " \n\t([—":
                open_q = True if ch != " " or not out else open_q
            out.append(ch)
    # re-derive open/close by context rather than by toggling alone
    res = "".join(out)
    return res

def smarten_ctx(text):
    def dq(m):
        before = text[:m.start()]
        prev = before[-1] if before else " "
        return "\\\\u201c" if prev in " \n\t([—-" or not before else "\\\\u201d"
    text = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\\\\u2019", text)
    text = re.sub(r"(?<=[A-Za-z])'(?![A-Za-z0-9])", "\\\\u2019", text)
    # an apostrophe opening a text node follows a closing tag: <em>Title</em>'s
    text = re.sub(r"^'(?=[A-Za-z])", "\\\\u2019", text)
    out, i = [], 0
    for m in re.finditer(r'"', text):
        out.append(text[i:m.start()])
        prev = text[m.start()-1] if m.start() else " "
        out.append("\\\\u201c" if prev in " \n\t([" or prev == "" or m.start() == 0 else "\\\\u201d")
        i = m.end()
    out.append(text[i:])
    return "".join(out)

def convert_body(b):
    parts = re.split(r"(<[^>]+>)", b)
    return "".join(p if p.startswith("<") else smarten_ctx(p) for p in parts)

def main():
    path = pathlib.Path(sys.argv[1]); dry = "--dry" in sys.argv
    s = path.read_text(encoding="utf-8")
    head, rest = s.split('<script id="book-js">', 1)
    js, tail = rest.split("</script>", 1)
    before_ap = before_dq = 0
    for b in re.findall(r"BODIES\[\d+\]=`([\s\S]*?)`;", js):
        txt = "".join(p for p in re.split(r"(<[^>]+>)", b) if not p.startswith("<"))
        before_ap += len(re.findall(r"[A-Za-z]'", txt)); before_dq += txt.count('"')
    new = re.sub(r"BODIES\[(\d+)\]=`([\s\S]*?)`;",
                 lambda m: f"BODIES[{m.group(1)}]=`" + convert_body(m.group(2)) + "`;", js)
    after_ap = after_dq = 0
    for b in re.findall(r"BODIES\[\d+\]=`([\s\S]*?)`;", new):
        txt = "".join(p for p in re.split(r"(<[^>]+>)", b) if not p.startswith("<"))
        after_ap += len(re.findall(r"[A-Za-z]'", txt)); after_dq += txt.count('"')
    print(f"{path.parent.name}: apostrophes {before_ap} -> {after_ap}, "
          f"double quotes {before_dq} -> {after_dq}")
    if not dry:
        path.write_text(head + '<script id="book-js">' + new + "</script>" + tail, encoding="utf-8")

main()
