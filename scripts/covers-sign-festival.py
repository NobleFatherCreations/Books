import cv2, numpy as np
SIG='tools/brand/signature-shae-stovell.png'
im=cv2.imread('content/covers/original/06-festival.jpg'); h,w=im.shape[:2]
X0,X1,Y0,Y1=105,545,514+130,514+262
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(np.float32)
bg=cv2.medianBlur(g.astype(np.uint8),41).astype(np.float32)
d=g-bg; m=np.zeros((h,w),np.uint8); m[Y0:Y1,X0:X1]=(d[Y0:Y1,X0:X1]>14).astype(np.uint8)*255
ty,tx=np.where(m>0); lum=g[ty,tx]; core=(lum>=np.percentile(lum,35))&(lum<=np.percentile(lum,80))
color=np.median(im[ty[core],tx[core]],axis=0)
color=np.array([88.,168.,226.])  # warm gold matching the title lettering
mm=cv2.dilate(m,np.ones((5,5),np.uint8),iterations=2)
clean=cv2.inpaint(im,mm,9,cv2.INPAINT_TELEA)
sig=cv2.imread(SIG,cv2.IMREAD_GRAYSCALE); a=255-sig; ys,xs=np.where(a>40); a=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
sw=400; sh=int(sw*a.shape[0]/a.shape[1])
aa=cv2.resize(a,(sw,sh),interpolation=cv2.INTER_AREA); aa=cv2.dilate(aa,np.ones((2,2),np.uint8)).astype(np.float32)/255
aa=np.clip(aa*1.35,0,1)
cx,cy=(X0+X1)//2,(Y0+Y1)//2; ox,oy=cx-sw//2,cy-int(sh*.5)
roi=clean[oy:oy+sh,ox:ox+sw].astype(np.float32)
roi=roi*(1-aa[...,None])+color[None,None,:]*aa[...,None]
clean[oy:oy+sh,ox:ox+sw]=np.clip(roi,0,255).astype(np.uint8)
cv2.imwrite('content/covers/signed/06-festival.jpg',clean,[cv2.IMWRITE_JPEG_QUALITY,93]); print(color)
