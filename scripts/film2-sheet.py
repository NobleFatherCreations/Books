#!/usr/bin/env python3
"""Fractal² film: contact sheet (each hero hold next to its plate) and the seen-marks check. python3 -I scripts/film2-sheet.py sheet.json out.jpg platesdir CONTACT-SEEN.json [--mark]
--mark writes the current frames' hashes as seen: only after a person has looked at out.jpg."""
import sys,json,os
from PIL import Image,ImageDraw
import numpy as np
S=json.load(open(sys.argv[1])); out=sys.argv[2]; PL=sys.argv[3]; seen=json.load(open(sys.argv[4])) if os.path.exists(sys.argv[4]) else {}
def ah(f):
    a=np.asarray(Image.open(f).convert('L').resize((16,16),Image.BILINEAR)).astype(float); return ''.join('1' if v else '0' for v in (a>a.mean()).ravel())
rows=[]; res={'missing':[],'hashes':{}}
for e in S:
    k=e['hero']+'|'+e['prof']; h=ah(e['f']); res['hashes'][k]=h
    if k not in seen or sum(x!=y for x,y in zip(seen[k],h))>24: res['missing'].append(k)
    fr=Image.open(e['f']).convert('RGB'); th=360; fr=fr.resize((int(fr.width*th/fr.height),th))
    pls=[Image.open(os.path.join(PL,p+'-m.webp')).convert('RGB').resize((th,th) if p!='shaft' else (int(th*.558),th)) for p in e['plates']]
    w=sum(p.width for p in pls)+fr.width+30; row=Image.new('RGB',(w,th+26),(24,24,28)); x=0
    for p in pls: row.paste(p,(x,26)); x+=p.width
    row.paste(fr,(x+30,26)); ImageDraw.Draw(row).text((4,6),'%s  (%s, %.1f s)   plate | frame'%(e['hero'],e['prof'],e['t']),fill=(240,220,160)); rows.append(row)
W=max(r.width for r in rows); H=sum(r.height for r in rows); sh=Image.new('RGB',(W,H),(24,24,28)); y=0
for r in rows: sh.paste(r,(0,y)); y+=r.height
sh.save(out,quality=86)
if '--mark' in sys.argv: json.dump(res['hashes'],open(sys.argv[4],'w'),indent=1); res['missing']=[]
print(json.dumps(res))
