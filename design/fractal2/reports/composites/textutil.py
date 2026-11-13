"""Shared text helpers: Title Case for headings and labels, and typographic (curly) quotes for display."""
import re
SMALL = {"a", "an", "the", "and", "but", "or", "nor", "for", "yet", "so", "as", "at", "by", "in", "of", "on", "to", "up", "per", "via", "vs"}

def _cap(w):
    m = re.search(r"[A-Za-z\u00c0-\u024f]", w)
    if not m: return w
    i = m.start()
    return w[:i] + w[i].upper() + w[i + 1:]

def titlecase(s):
    words = s.split(" ")
    out = []
    for k, w in enumerate(words):
        bare = re.sub(r"^[^A-Za-z]+|[^A-Za-z]+$", "", w).lower()
        first = k == 0 or re.search(r"[:.!?]$", words[k - 1] or "")
        last = k == len(words) - 1
        if w.isupper() and len(w) > 1:                       # FOG, NOT PREPARED
            out.append(w)
        elif "-" in w and not w.startswith("-"):
            out.append("-".join(_cap(p) for p in w.split("-")))
        elif bare in SMALL and not first and not last:
            out.append(w)
        else:
            out.append(_cap(w))
    return " ".join(out)

def smart(t):
    """Straight quotes to curly. Applied to display text only; the words are unchanged."""
    t = t.replace("\u2019", "'")
    t = re.sub(r"(?<![\w\u2019])'(?=Cause\b|cause\b|til\b|em\b)", "\u2019", t)           # 'Cause, 'til: an apostrophe, not an opening quote
    t = re.sub(r'(^|[\s(\[\u2014\u2018{*])"', "\\1\u201c", t)
    t = t.replace('"', "\u201d")
    t = re.sub(r"(^|[\s(\[\u2014\u201c{*])'", "\\1\u2018", t)
    t = t.replace("'", "\u2019")
    return t

def capfirst(s):
    return _cap(s) if s else s
