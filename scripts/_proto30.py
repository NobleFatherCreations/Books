import importlib.util,re,sys,os
spec=importlib.util.spec_from_file_location('cs','/home/user/Books/scripts/counterfeit-slides.py'); cs=importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)
RELIG=cs.RELIG
canon=cs.canon_techniques(); rel=cs.religions(canon)
def clean(x):
    x=re.sub(r'\s*\[\d+\](?:\[\d+\])*','',x); x=re.sub(r'\s*\[[A-Z][A-Z /\-]+(?::[^\]]*)?\]','',x)
    return re.sub(r'\s+',' ',re.sub(r'\*\*|\*','',x)).strip()
r=[x for x in rel if x['id']=='hare-krishna'][0]
t=open(f'{RELIG}/hare-krishna.md').read()
heads=[(m.start(),int(m.group(1))) for m in re.finditer(r'^#### (\d+) · ',t,re.M)][:30]
lines=[]
for k,(pos,n) in enumerate(heads):
    end=heads[k+1][0] if k+1<30 else pos+6000
    m=re.search(r'\*\*How it shows here\*\*\s*\n\s*\n((?:- .+\n?)+)',t[pos:end]); b=clean(re.findall(r'^- (.+)$',m.group(1),re.M)[0])
    lines.append(b if len(b)<=110 else b[:107].rsplit(' ',1)[0]+'…')
print(sum(len(x) for x in lines)/30)
CSS30="""
.box30 { position:absolute; left:80px; top:130px; width:900px; height:1470px; overflow:hidden; display:flex; flex-direction:column; }
.r30 { display:flex; gap:calc(14px*var(--s)); align-items:flex-start; border-top:1px solid var(--rule); padding:calc(9px*var(--s)) 0; font-size:calc(22px*var(--s)); line-height:1.25; }
.r30 .dot { flex:none; border-radius:50%; margin-top:calc(6px*var(--s)); width:calc(15px*var(--s)); height:calc(15px*var(--s)); }
.r30 b { font-weight:700; color:var(--text); } .r30 span.t { color:#D9D1BE; }
"""
rows=''.join(f'<div class="r30"><span class="dot" style="background:{cs.GCOL[g]}"></span><div><b>{cs.e(canon[i])}.</b> <span class="t">{cs.e(lines[i])}</span></div></div>' for i,g in enumerate(r['grades']))
inner=f'<div class="kick" style="font-size:calc(24px*var(--s))">{cs.e(r["family"])}</div><h2 style="font-size:calc(54px*var(--s));margin-top:6px">{cs.e(r["title"])}</h2><div class="a" style="font-size:calc(24px*var(--s));margin:8px 0 12px">How each of the 30 techniques shows up here</div>{rows}'
html=f'<!doctype html><meta charset="utf-8"><style>{cs.CSS}{CSS30}</style><div class="box30 box">{inner}</div>'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox']); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.set_content(html); pg.wait_for_timeout(150)
    s=pg.evaluate("() => { const b=document.querySelector('.box30'); let s=1,n=0; while(b.scrollHeight>b.clientHeight+1&&s>0.5&&n<60){s-=0.02;document.documentElement.style.setProperty('--s',s.toFixed(2));n++} return s }")
    print('scale',s); pg.screenshot(path='/tmp/claude-0/-home-user/72e21852-6952-5a8e-8604-2110f224b19a/scratchpad/proto30.png'); b.close()
