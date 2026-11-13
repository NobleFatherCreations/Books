import sys,re,logging; logging.disable(logging.CRITICAL)
import pdfplumber
with pdfplumber.open(sys.argv[1]) as pdf:
    H=float(pdf.pages[0].height); start={}; fill={}
    for i,p in enumerate(pdf.pages):
        t=p.extract_text() or ''
        for m in re.findall(r'zzS(\d\d)',t): start[m]=i
        ch=[c for c in p.chars if c['bottom']<H-50]
        fill[i]=(max(c['bottom'] for c in ch)-52)/(H-52-59) if ch else 0
    ids=sorted(start); n=len(pdf.pages)
    bad=[]
    for k,s in enumerate(ids):
        e=(start[ids[k+1]] if k+1<len(ids) else n)-1
        span=e-start[s]+1; f=fill[e]
        flag='' if f>=0.72 else '  <-- short last page'
        if flag: bad.append(s)
        print(f"S{s}: pages {start[s]+1}-{e+1} span {span} last-fill {f:.2f}{flag}")
    print("pages",n,"short:",bad)
