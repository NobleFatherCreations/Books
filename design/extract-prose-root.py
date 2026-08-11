"""Extract The Root's real content — a branching guided-practice state
machine whose prompts live in JS `shell(title, subtitle, ...)` calls and
several `const WHO=/ORIGIN=/CONSCIOUSNESS=/THEMES=` option arrays, not
static HTML, so extract-prose.py returns nothing for it. Run from the
repo root. Usage: python3 design/extract-prose-root.py
"""
import re, json, os

PATH = os.path.join(os.path.dirname(__file__), "..", ".audit-view", "noble-father-root.html")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", ".audit-view", "prose")
OUT = os.path.join(OUT_DIR, "root.md")
os.makedirs(OUT_DIR, exist_ok=True)

text = open(PATH, encoding="utf-8").read()

STEP_ORDER = ["callback", "resume", "root", "who", "conscious", "breath", "belief",
              "theme-pick", "origin", "originfollow", "body", "protector", "tally",
              "named", "action", "commitment", "record"]

STEP_TITLES = {
    "callback": "0. Before we begin (returning-visitor check-in)",
    "resume": "0b. Welcome back",
    "root": "1. Where it starts",
    "who": "2. Who / what surfaced",
    "conscious": "3. Was this already on your mind?",
    "breath": "3b. A breath, if this was buried",
    "belief": "4. Naming the belief",
    "theme-pick": "4b. If more than one theme surfaced",
    "origin": "5. Where the belief came from",
    "originfollow": "5b. Following the origin",
    "body": "6. Where you feel it in the body",
    "protector": "7. Naming the protector",
    "tally": "8. What it's cost you / given you",
    "named": "9. Naming it",
    "action": "10. One action",
    "commitment": "11. Commitment / how you'll know",
    "record": "12. Closing record",
}


def find_str_literal(s, start):
    """Find a JS string literal (", ', or `) starting at/after `start`, return (text, end_index)."""
    i = start
    while i < len(s) and s[i] in " \t\n":
        i += 1
    if i >= len(s) or s[i] not in "\"'`":
        return None, start
    quote = s[i]
    j = i + 1
    buf = []
    while j < len(s):
        c = s[j]
        if c == "\\" and j + 1 < len(s):
            buf.append(s[j:j + 2])
            j += 2
            continue
        if c == quote:
            j += 1
            break
        buf.append(c)
        j += 1
    raw = "".join(buf)
    # unescape common JS escapes
    raw = raw.replace("\\n", " ").replace("\\'", "'").replace('\\"', '"').replace("\\`", "`")
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw, j


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\$\{[^}]*\}", "", s)  # drop template interpolations
    s = re.sub(r"\s+", " ", s).strip()
    return s


results = {}
for m in re.finditer(r'if\(id==="([a-z_-]+)"\)\{', text):
    step_id = m.group(1)
    block_start = m.end()
    shell_m = re.search(r"shell\(", text[block_start:block_start + 4000])
    if not shell_m:
        continue
    pos = block_start + shell_m.end()
    title, pos = find_str_literal(text, pos)
    pos += 1  # skip comma
    subtitle, pos = find_str_literal(text, pos)
    # look ahead a bit for a subtext:"..." option
    lookahead = text[pos:pos + 3000]
    subtext = None
    sm = re.search(r'subtext:\s*', lookahead)
    if sm:
        st, _ = find_str_literal(lookahead, sm.end())
        subtext = strip_html(st) if st else None
    results[step_id] = {
        "title": strip_html(title) if title else None,
        "subtitle": strip_html(subtitle) if subtitle else None,
        "subtext": subtext,
    }

out = []
out.append("# The Root — a guided shadow-work practice\n")
out.append("*This is a tool, not a book: an 18-step branching guided practice you move "
            "through once, in sequence (not browsed like chapters). Extracted from the "
            "tool's own JS state machine and prompt strings in "
            "`.audit-view/noble-father-root.html`. Where a step branches based on your "
            "answer, both branches are shown below.*\n")
out.append("---\n")

for step_id in STEP_ORDER:
    r = results.get(step_id)
    if not r:
        continue
    out.append(f"\n## {STEP_TITLES.get(step_id, step_id)}\n")
    if r["title"]:
        out.append(f"**{r['title']}**")
    if r["subtitle"]:
        out.append(r["subtitle"])
    if r["subtext"]:
        out.append(f"*{r['subtext']}*")

out.append("\n\n---\n\n## Branching content the practice draws from\n")
out.append("*These are the actual option sets and follow-up insight text the tool shows "
            "depending on what you answer at each branch point.*\n")


def extract_js_array(varname):
    marker = f"const {varname}=" if f"const {varname}=" in text else f"const {varname} ="
    start = text.find(marker)
    if start == -1:
        return None
    start += len(marker)
    depth = 0
    i = start
    while text[i] in " \t\n":
        i += 1
    open_ch = text[i]
    close_ch = "]" if open_ch == "[" else "}"
    j = i
    depth = 0
    while j < len(text):
        if text[j] == open_ch:
            depth += 1
        elif text[j] == close_ch:
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    return text[i:j]


def fields_from_obj_literal(chunk, field_names):
    found = {}
    for fname in field_names:
        m = re.search(rf"\b{fname}\s*:\s*", chunk)
        if not m:
            continue
        val, _ = find_str_literal(chunk, m.end())
        if val:
            found[fname] = strip_html(val)
    return found


def split_top_level_objects(array_text):
    """Split a [ {...}, {...} ] string into individual {...} chunks (top-level only)."""
    chunks = []
    depth = 0
    start = None
    for i, c in enumerate(array_text):
        if c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(array_text[start:i + 1])
                start = None
    return chunks


for varname, label, fields in [
    ("WHO", "What surfaced", ["label", "insight", "follow"]),
    ("CONSCIOUSNESS", "Was it already conscious", ["label", "insight"]),
    ("ORIGIN", "Where the belief came from", ["label", "follow"]),
    ("THEMES", "Belief themes it can detect", ["ref", "cost"]),
]:
    arr = extract_js_array(varname)
    if not arr:
        continue
    out.append(f"\n### {label}\n")
    for chunk in split_top_level_objects(arr):
        f = fields_from_obj_literal(chunk, fields)
        if not f:
            continue
        line = " — ".join(v for v in f.values() if v)
        out.append(f"- {line}")

full_text = "\n".join(out)
word_count = len(full_text.split())
open(OUT, "w", encoding="utf-8").write(full_text)
print(f"root: {word_count:,} words -> {OUT}")
print(f"steps captured: {sorted(results.keys())}")
