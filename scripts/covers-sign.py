# Swap the printed author name for the signature (no AI, no credits): inpaint the name, overlay tools/brand/signature-shae-stovell.png in the lettering colour.
# Run from the repo root: python3 scripts/covers-sign.py [slug ...]
import cv2, numpy as np, os, sys
SIG='tools/brand/signature-shae-stovell.png'
# band-local display boxes read off name-bands.jpg (x0,x1,y0,y1); dark=text darker than background
BOX={'decoder':(215,540,52,92),'feminine':(212,545,73,113),'longafter':(148,608,75,122),
 'children':(222,538,90,135,'dark'),'silence':(185,572,80,107),'repair':(200,555,102,130),
 'atwill':(175,580,97,127),'slowtake':(175,580,83,113),'loop':(128,628,67,118),
 'scale':(165,590,74,117),'root':(230,525,87,120)}
FILES={s:f for f in os.listdir('content/covers/original') for s in BOX if f[3:-4]==s}
sig=cv2.imread(SIG,cv2.IMREAD_GRAYSCALE)
a=255-sig; ys,xs=np.where(a>40); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]
def run(slug, out):
    b=BOX[slug]; dark=len(b)>4
    im=cv2.imread('content/covers/original/'+FILES[slug]); h,w=im.shape[:2]
    s=1.06*w/800; top=0.86*h
    x0,x1=int(b[0]*s),int(b[1]*s); y0,y1=int(top+b[2]*s),int(top+b[3]*s)
    px,py=int((x1-x0)*.06),int((y1-y0)*.35)
    X0,X1,Y0,Y1=max(0,x0-px),min(w,x1+px),max(0,y0-py),min(h,y1+py)
    g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg=cv2.medianBlur(g.astype(np.uint8),(int(w*.05)|1)).astype(np.float32)
    d=(bg-g) if dark else (g-bg)
    m=np.zeros((h,w),np.uint8); m[Y0:Y1,X0:X1]=(d[Y0:Y1,X0:X1]>22).astype(np.uint8)*255
    ty,tx=np.where(m>0)
    tb=(tx.min(),ty.min(),tx.max(),ty.max())
    color=np.median(im[ty,tx],axis=0)
    if not dark:  # use the bright core of the letters for the colour
        lum=g[ty,tx]; core=lum>=np.percentile(lum,70); color=np.median(im[ty[core],tx[core]],axis=0)
    mm=cv2.dilate(m,np.ones((int(3+w/400),)*2,np.uint8),iterations=2)
    clean=cv2.inpaint(im,mm,int(6+w/300),cv2.INPAINT_TELEA)
    tw,th=tb[2]-tb[0],tb[3]-tb[1]
    sw=int(tw*0.95); sh=int(sw*a.shape[0]/a.shape[1])
    lim=int(th*(4.4 if th<60*w/1696 else 3.2))
    if sh>lim: sh=lim; sw=int(sh*a.shape[1]/a.shape[0])
    aa=cv2.resize(a,(sw,sh),interpolation=cv2.INTER_AREA)
    t=max(1,round(sw/650))
    if t>1: aa=cv2.dilate(aa,np.ones((t,t),np.uint8))
    aa=aa.astype(np.float32)/255
    aa=np.clip(aa*1.35,0,1)
    cx,cy=(tb[0]+tb[2])//2,(tb[1]+tb[3])//2
    ox=cx-sw//2; oy=min(h-sh-int(h*.012), cy-int(sh*0.55))
    roi=clean[oy:oy+sh, ox:ox+sw].astype(np.float32)
    # faint dark halo for legibility on busy art (not for the white children's cover)
    if not dark:
        halo=cv2.GaussianBlur(aa,(0,0),sw/120)[...,None]*0.45
        roi=roi*(1-halo)
    roi=roi*(1-aa[...,None])+color[None,None,:]*aa[...,None]
    clean[oy:oy+sh, ox:ox+sw]=np.clip(roi,0,255).astype(np.uint8)
    cv2.imwrite(out,clean,[cv2.IMWRITE_JPEG_QUALITY,93])
    return tb,color
for slug in (sys.argv[1:] or BOX):
    tb,c=run(slug,f'content/covers/signed/{FILES[slug]}'); print(slug,tb,c.astype(int))
