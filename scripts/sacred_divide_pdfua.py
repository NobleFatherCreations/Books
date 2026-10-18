"""PDF/UA repair for Chromium-tagged PDFs: mark untagged graphics/text as Artifact, and give each list item the
Lbl/LBody shape ISO 14289-1 requires. Content that is already inside marked content is left alone."""
import pikepdf
from pikepdf import Name, Operator

TEXT_OK = {'BT', 'ET'}
PATH = {'m', 'l', 'c', 'v', 'y', 'h', 're', 'S', 's', 'f', 'F', 'f*', 'B', 'B*', 'b', 'b*', 'n', 'W', 'W*', 'Do', 'sh'}


def artifact_wrap(page, pdf):
    ins = pikepdf.parse_content_stream(page)
    out, depth, in_text, open_art, changed = [], 0, False, False, 0
    ART = pikepdf.ContentStreamInstruction([Name.Artifact], Operator('BMC'))
    EMC = pikepdf.ContentStreamInstruction([], Operator('EMC'))

    def close():
        nonlocal open_art
        if open_art: out.append(EMC); open_art = False
    for i in ins:
        op = str(i.operator)
        if op in ('BDC', 'BMC'):
            close(); depth += 1; out.append(i); continue
        if op == 'EMC':
            depth -= 1; out.append(i); continue
        top = depth == 0
        if op == 'BT' and top: in_text = True
        if top and (in_text or op in PATH or op == 'BI'):
            if not open_art: out.append(ART); open_art = True; changed += 1
            out.append(i)
            if op == 'ET': in_text = False
            continue
        if op == 'ET': in_text = False
        close(); out.append(i)
    close()
    if changed:
        page.Contents = pdf.make_stream(pikepdf.unparse_content_stream(out))
    return changed


def fix_lists(pdf):
    root = pdf.Root.get('/StructTreeRoot')
    if root is None: return 0
    n = 0

    def kids(e):
        k = e.get('/K')
        if k is None: return []
        return list(k) if isinstance(k, pikepdf.Array) else [k]

    def walk(e):
        nonlocal n
        for c in kids(e):
            if isinstance(c, pikepdf.Dictionary): walk(c)
        if e.get('/S') == '/LI':
            ks = kids(e)
            if any(not (isinstance(c, pikepdf.Dictionary) and c.get('/S') in ('/Lbl', '/LBody')) for c in ks):
                body = pdf.make_indirect(pikepdf.Dictionary(Type=Name.StructElem, S=Name.LBody, P=e, K=pikepdf.Array(ks)))
                for c in ks:
                    if isinstance(c, pikepdf.Dictionary) and '/S' in c and c.get('/S') not in ('/Lbl', '/LBody'): c.P = body
                e.K = pikepdf.Array([body]); n += 1
    walk(root)
    return n


def fill_alts(pdf, alts, page_text=None):
    """Give any Figure that Chromium left without /Alt a label. `alts` is a list of labels or of (label, key) pairs, in document
    order; a key is a snippet of the figure's own title. With `page_text` (one string per page) the label whose key appears on the
    figure's page is used first, which survives Chromium skipping a different figure from one build to the next; otherwise,
    or when no key matches, the next unused label is taken in document order."""
    root = pdf.Root.get('/StructTreeRoot'); n = 0
    pairs = [(a, a) if isinstance(a, str) else (a[0], a[1]) for a in alts]
    used = [False] * len(pairs)
    pageno = {p.objgen: i for i, p in enumerate(pdf.pages)}
    def pick(pg):
        raw = page_text[pg] if page_text and pg is not None and pg < len(page_text) else ''
        lines = [' '.join(l.split()).lower() for l in raw.split('\n')]
        for i, (lab, key) in enumerate(pairs):   # a figure's title starts a line; the same words inside a sentence do not count
            k = ' '.join(key.split()).lower()
            if not used[i] and k and any(l.startswith(k) for l in lines): used[i] = True; return lab
        for i, (lab, key) in enumerate(pairs):
            if not used[i]: used[i] = True; return lab
    def first_pg(e):
        if '/Pg' in e: return pageno.get(e['/Pg'].objgen)
        k = e.get('/K')
        for c in ([] if k is None else (list(k) if isinstance(k, pikepdf.Array) else [k])):
            if isinstance(c, pikepdf.Dictionary):
                r = first_pg(c)
                if r is not None: return r
    def walk(e):
        nonlocal n
        if not isinstance(e, pikepdf.Dictionary): return
        if e.get('/S') == '/Figure' and '/Alt' not in e:
            a = pick(first_pg(e))
            if a: e.Alt = pikepdf.String(a); n += 1
        k = e.get('/K')
        for c in ([] if k is None else (list(k) if isinstance(k, pikepdf.Array) else [k])): walk(c)
    if root is not None: walk(root)
    return n


def run(path, alts=()):
    try:
        import pymupdf
        with pymupdf.open(path) as doc: page_text = [pg.get_text() for pg in doc]
    except Exception:
        page_text = None
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        w = sum(artifact_wrap(p, pdf) for p in pdf.pages)
        li = fix_lists(pdf)
        fa = fill_alts(pdf, alts, page_text)
        pdf.save(path)
    return w, li, fa
