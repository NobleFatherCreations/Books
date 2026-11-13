#!/usr/bin/env python3
"""Turns the invisible qaNN/qzNN (text box corners) and qcNN (checkbox) markers into real, typeable PDF form fields.
Usage: fields.py in.pdf out.pdf"""
import sys, logging, pdfplumber
logging.disable(logging.CRITICAL)
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, ArrayObject, FloatObject, NumberObject, TextStringObject, BooleanObject, StreamObject
src, dst = sys.argv[1:3]
marks = {}
with pdfplumber.open(src) as pdf:
    for pi, pg in enumerate(pdf.pages):
        H = float(pg.height)
        for w in pg.extract_words(keep_blank_chars=False, use_text_flow=False):
            t = w["text"]
            if len(t) == 4 and t[:2] in ("qa", "qz", "qc") and t[2:].isdigit():
                marks[t] = (pi, w["x0"], H - w["top"], w["x1"], H - w["bottom"])
r = PdfReader(src); wtr = PdfWriter(clone_from=r)
fields = ArrayObject()
font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
zadb = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/ZapfDingbats")})
fref, zref = wtr._add_object(font), wtr._add_object(zadb)
def stream(data, bbox, res=None):
    s = StreamObject(); s._data = data.encode()
    s.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Form"),
              NameObject("/BBox"): ArrayObject([FloatObject(v) for v in bbox])})
    if res: s[NameObject("/Resources")] = res
    return wtr._add_object(s)
def add(pi, rect, d):
    d.update({NameObject("/Type"): NameObject("/Annot"), NameObject("/Subtype"): NameObject("/Widget"),
              NameObject("/Rect"): ArrayObject([FloatObject(round(v, 2)) for v in rect]), NameObject("/F"): NumberObject(4),
              NameObject("/P"): wtr.pages[pi].indirect_reference})
    ref = wtr._add_object(d)
    pg = wtr.pages[pi]
    if "/Annots" not in pg: pg[NameObject("/Annots")] = ArrayObject()
    pg["/Annots"].append(ref); fields.append(ref)
nt = nc = 0
for k, (pi, x0, ytop, x1, ybot) in sorted(marks.items()):
    n = k[2:]
    if k.startswith("qa") and "qz" + n in marks:
        _, _, _, zx1, zybot = marks["qz" + n]
        add(pi, [x0 + 2, zybot + 1.5, zx1 - 2, ytop - 1.5], DictionaryObject({
            NameObject("/FT"): NameObject("/Tx"), NameObject("/T"): TextStringObject("note_" + n), NameObject("/Ff"): NumberObject(4096),
            NameObject("/DA"): TextStringObject("/Helv 9 Tf 0.09 0.09 0.11 rg"), NameObject("/V"): TextStringObject("")})); nt += 1
    elif k.startswith("qc"):
        S = 10.2; rect = [x0 - 0.6, ytop - S + 0.6, x0 - 0.6 + S, ytop + 0.6]
        res = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/ZaDb"): zref})})
        on = stream(f"q BT /ZaDb 8.5 Tf 0.54 0.37 0 rg 1.6 2.2 Td (4) Tj ET Q", [0, 0, S, S], res); off = stream("", [0, 0, S, S])
        add(pi, rect, DictionaryObject({
            NameObject("/FT"): NameObject("/Btn"), NameObject("/T"): TextStringObject("check_" + n),
            NameObject("/V"): NameObject("/Off"), NameObject("/AS"): NameObject("/Off"),
            NameObject("/AP"): DictionaryObject({NameObject("/N"): DictionaryObject({NameObject("/Yes"): on, NameObject("/Off"): off})}),
            NameObject("/MK"): DictionaryObject({NameObject("/CA"): TextStringObject("4")})})); nc += 1
wtr._root_object[NameObject("/AcroForm")] = wtr._add_object(DictionaryObject({
    NameObject("/Fields"): fields, NameObject("/NeedAppearances"): BooleanObject(True),
    NameObject("/DA"): TextStringObject("/Helv 9 Tf 0 g"),
    NameObject("/DR"): DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/Helv"): fref, NameObject("/ZaDb"): zref})})}))
wtr.add_metadata({"/Title": "Why I Wrote This", "/Author": "Shae Stovell", "/Subject": "The Fractal: the map and what it is for"})
wtr.write(dst)
links = sum(1 for p in wtr.pages for a in p.get("/Annots", []) if a.get_object().get("/Subtype") == "/Link")
print(f"{dst}: {len(wtr.pages)} pages, {nt} text fields, {nc} checkboxes, {links} links")
