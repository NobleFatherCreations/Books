/* Fractal² film engine. One clock; every frame is a pure function of time.
   Built into film.html by build.py. Data arrives in window.FILM_DATA. Timeline in shots.js (FILM.shots). */
(function () {
'use strict';
var D = window.FILM_DATA, F = window.FILM = { data: D };
var d = document, $ = function (i) { return d.getElementById(i); };
var TAU = Math.PI * 2;
function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
function lerp(a, b, t) { return a + (b - a) * t; }
function sm(t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); }
F.clamp = clamp; F.lerp = lerp; F.sm = sm;

/* ---------- easing: all closed form, so seek(t) is exact ---------- */
function bez(x1, y1, x2, y2) {            // css-style cubic-bezier, solved by bisection
  return function (x) {
    if (x <= 0) return 0; if (x >= 1) return 1;
    var lo = 0, hi = 1, t = x, i, cx;
    for (i = 0; i < 22; i++) { cx = 3 * (1 - t) * (1 - t) * t * x1 + 3 * (1 - t) * t * t * x2 + t * t * t; if (cx < x) lo = t; else hi = t; t = (lo + hi) / 2; }
    return 3 * (1 - t) * (1 - t) * t * y1 + 3 * (1 - t) * t * t * y2 + t * t * t;
  };
}
function spring(zeta, w) {                 // damped harmonic step response, normalised to land exactly on 1
  function s(u) {
    if (zeta >= 1) return 1 - Math.exp(-w * u) * (1 + w * u);
    var wd = w * Math.sqrt(1 - zeta * zeta);
    return 1 - Math.exp(-zeta * w * u) * (Math.cos(wd * u) + zeta * w / wd * Math.sin(wd * u));
  }
  var e = s(1);
  return function (u) { return u <= 0 ? 0 : u >= 1 ? 1 : s(u) / e; };
}
var E = F.ease = {
  lin: function (t) { return clamp(t, 0, 1); },
  io: sm,
  in2: function (t) { t = clamp(t, 0, 1); return t * t; },
  out2: function (t) { t = clamp(t, 0, 1); return 1 - (1 - t) * (1 - t); },
  in3: function (t) { t = clamp(t, 0, 1); return t * t * t; },
  out3: function (t) { t = clamp(t, 0, 1); return 1 - Math.pow(1 - t, 3); },
  io3: function (t) { t = clamp(t, 0, 1); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; },
  io5: function (t) { t = clamp(t, 0, 1); return t < .5 ? 16 * t * t * t * t * t : 1 - Math.pow(-2 * t + 2, 5) / 2; },
  outExpo: function (t) { t = clamp(t, 0, 1); return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t); },
  inExpo: function (t) { t = clamp(t, 0, 1); return t <= 0 ? 0 : Math.pow(2, 10 * t - 10); },
  ioExpo: function (t) { t = clamp(t, 0, 1); return t <= 0 ? 0 : t >= 1 ? 1 : t < .5 ? Math.pow(2, 20 * t - 10) / 2 : (2 - Math.pow(2, -20 * t + 10)) / 2; },
  weight: spring(.62, 9),                  // arrives with mass: slight overshoot, settles
  settle: spring(1, 8),                    // critically damped: no bounce
  film: bez(.22, .0, .12, 1),              // slow in, long glide out
  cut: bez(.7, 0, .2, 1)
};
F.bez = bez; F.spring = spring;

/* ---------- tracks: [[time, value, easeIntoThisKey], ...]; value holds before first and after last ---------- */
function track(keys, log) {
  return function (t) {
    var n = keys.length, i;
    if (t <= keys[0][0]) return keys[0][1];
    if (t >= keys[n - 1][0]) return keys[n - 1][1];
    for (i = 1; i < n; i++) if (t < keys[i][0]) break;
    var a = keys[i - 1], b = keys[i], u = (t - a[0]) / (b[0] - a[0]), e = (b[2] || E.io)(u);
    return log ? Math.exp(lerp(Math.log(a[1]), Math.log(b[1]), e)) : lerp(a[1], b[1], e);
  };
}
F.track = track;

/* ---------- layout: one stable box, pixels only ---------- */
var cv = $('gl'), W = 0, H = 0, DPR = 1, U = 1, CYF = .4, PORT = true;
var tier = 0, TIERS = [
  { name: 'full', dpr: 2, rays: 28, bloom: 3, dust: 1, part: 1, hdr: 1 },
  { name: 'reduced', dpr: 1.5, rays: 12, bloom: 2, dust: 0, part: .5, hdr: 1 },
  { name: 'low', dpr: 1, rays: 0, bloom: 1, dust: 0, part: .25, hdr: 0 }
];
function layout() {
  var box = $('stage').getBoundingClientRect();
  var w = Math.round(box.width), h = Math.round(box.height);
  var dpr = Math.min(window.devicePixelRatio || 1, TIERS[tier].dpr);
  if (w === W && h === H && dpr === DPR) return false;
  W = w; H = h; DPR = dpr; PORT = H > W * 1.05;
  CYF = PORT ? .40 : .5;
  U = PORT ? Math.min(W * .5, H * .34) : Math.min(W * .3, H * .44);
  cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR);
  cv.style.width = W + 'px'; cv.style.height = H + 'px';
  d.documentElement.style.setProperty('--u', U + 'px');
  if (gl) targets();
  return true;
}
F.dims = function () { return { W: W, H: H, DPR: DPR, U: U, CYF: CYF, PORT: PORT, CXF: (F.S && F.S.cxf) || .5 }; };

/* ---------- WebGL2 ---------- */
var gl = null, P = {}, TX = {}, RT = {}, quad, HDR = false, alloc = 0, peakAlloc = 0, ctxLost = 0;
var VS = '#version 300 es\nin vec2 a;out vec2 v;void main(){v=a*.5+.5;gl_Position=vec4(a,0.,1.);}';
var COMMON = '#version 300 es\nprecision highp float;\n' +
  'float h21(vec2 p){vec3 p3=fract(vec3(p.xyx)*.1031);p3+=dot(p3,p3.yzx+33.33);return fract((p3.x+p3.y)*p3.z);}\n' +
  'float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h21(i),h21(i+vec2(1,0)),f.x),mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x),f.y);}\n' +
  'mat2 rot(float a){float c=cos(a),s=sin(a);return mat2(c,-s,s,c);}\n';
var FS_SCENE = COMMON + [
'uniform vec2 uRes,uCtr,uCam,uLS;uniform float uUnit,uZoom,uRot,uT,uPT;',
'uniform sampler2D tOrig,tCore,tLogo,tEmb;',
'uniform float uOrigA,uCoreA,uLogoA,uEmbA,uWords,uReveal,uFront,uTitle,uSpin,uDim,uOrigK,uRingDim;uniform vec2 uOrigP;uniform vec4 uRing;uniform float uRingL,uRing0,uLRev,uLogoK,uLH;uniform vec4 uGen;uniform vec2 uFrontL,uPat,uLineH,uLineV;uniform float uPatC;uniform vec3 uMk[10];uniform float uMkR,uMkL;uniform float uThN,uThA;uniform vec2 uTh[8];uniform vec4 uTrA[6],uTrB[6];',
'uniform vec3 uLight;uniform vec4 uOrb;uniform float uMotes,uGlint,uStars,uDust,uStreak,uHole,uRingS,uPoolR,uPoolK;',
'uniform sampler2D tP0,tP1,tP2;uniform vec4 uPA0,uPA1,uPA2,uPB0,uPB1,uSeam,uSeam2,uEmbD;uniform vec2 uBd[8];uniform float uDisF;uniform vec3 uPL;',
'uniform sampler2D tH0,tH1,tW;uniform vec4 uHa[2],uHb[2],uHc[2],uHd[2],uWin,uWin2,uWin3,uWin4,uWB[30],uWQ[30];uniform vec3 uHL;float hcov=0.;',
'in vec2 v;out vec4 o;',
'const float FR[8]=float[8](.207,.296,.38,.462,.547,.624,.713,.829);',
/* plates: the owner's images, lit by the film's one light and moved by its camera. g0 = centre.xy, half-size, angle; g1 = gain, lit, aspect (w/h), space (0 screen, 1 world) */
'const float OB[10]=float[10](0.,.118,.207,.296,.38,.462,.547,.624,.713,.84);const float PB[10]=float[10](0.,.157,.232,.322,.404,.488,.572,.645,.755,.86);',
'float remap(float r){if(r>=.84)return .86+(r-.84)*.957;for(int i=1;i<10;i++){if(r<OB[i])return mix(PB[i-1],PB[i],(r-OB[i-1])/(OB[i]-OB[i-1]));}return r;}',  // owner map radius -> twin plate radius, band for band
'int bandOf(float r){int b=0;for(int i=1;i<10;i++)if(r>=PB[i])b=i;return b;}',
'float litK(vec2 q){vec2 dv=q-uLS;float dl=length(dv)/max(uLight.y*3.,.25);return min(uLight.z,1.6)/(1.+dl*dl);}',
'vec2 pD(vec2 q,vec2 p,vec4 g0,vec4 g1){return rot(-g0.w)*((g1.w>.5?p:q)-g0.xy)/g0.z;}',
'vec4 pS(sampler2D t,vec2 d,float asp,float disc,float lod){vec2 uv=vec2(d.x/asp,d.y-disc*.026)*.5+.5;',
'  float m=disc>.5?smoothstep(.905,.885,length(d)):smoothstep(0.,.03,uv.x)*smoothstep(0.,.03,1.-uv.x)*smoothstep(0.,.03,uv.y)*smoothstep(0.,.03,1.-uv.y);',
'  return vec4(textureLod(t,clamp(uv,0.,1.),lod).rgb,m);}',
'vec3 pLit(vec3 c,vec2 q,vec4 g1){return c*g1.x*(1.+g1.y*litK(q));}',
'void pairL(vec2 q,vec2 p,inout vec3 col){float pm=uPA2.x;vec2 d=pD(q,p,uPA0,uPA1);float rr=length(d);if(pm==6.)d*=remap(rr)/max(rr,1e-5);',   // the twins: seam split (3; 6 registered to the map, drawn over it) or band-by-band dissolve (5)
'    vec4 a=pS(tP0,d,1.,1.,uPL.x),b=pS(tP1,d,1.,1.,uPL.y);float k,sd=dot(gl_FragCoord.xy,uSeam.xy)-uSeam.z;',
'    if(pm==5.){int bi=bandOf(length(d));float lo=PB[bi],hi=bi>=9?.905:PB[bi+1];float loc=clamp(uDisF-max(float(bi)-1.,0.),0.,1.);k=loc>=1.?1.:loc<=0.?0.:smoothstep(.01,-.01,length(d)-mix(lo,hi,loc));}',
'    else k=smoothstep(-1.,1.,sd);',
'    vec3 c=mix(pLit(a.rgb,q,uPA1),pLit(b.rgb,q,uPB1)*mix(1.,smoothstep(.98,.12,rr),uPB1.w),k);col=col*(1.-uPA2.y*a.a)+c*a.a;hcov=max(hcov,uPA2.y*a.a);',
'    if(pm!=5.&&uSeam.w>0.){float sc=sd/uSeam2.x,sg=sd/uSeam2.y;col+=(vec3(1.,.965,.886)*exp(-sc*sc)*.85+vec3(1.,.92,.75)*exp(-sg*sg*.5)*.4)*uSeam.w*smoothstep(1.,.86,rr);}}',
'void hero(sampler2D t,vec4 A,vec4 B,vec4 Cc,vec4 Dd,float lod,vec2 q,inout vec3 col){',     // a hero plate: screen-space, whole, at full strength. A = centre (device px, y up), half-size, angle; B = strength, aspect, mask (0 rect, 1 disc, 2 twin disc), brightness; Cc = reveal radius, grade, under, lit; Dd = map px per world unit (registration), band morph, pulse, registration blend
'  vec2 f=gl_FragCoord.xy-A.xy;vec2 d=rot(-A.w)*f/A.z;float rr=length(d),rm=-1.;',
'  if(Dd.x>0.){rm=length(f)/Dd.x;float rp=remap(rm);d=mix(d,d*rp/max(rr,1e-5),Dd.w);rr=length(d);}',
'  if(B.z>.5&&rr>.95)return;if(B.z<.5&&(abs(d.x)>B.y*1.02||abs(d.y)>1.02))return;',
'  vec2 uv=vec2(d.x/B.y,d.y-(B.z>1.5?.026:0.))*.5+.5;',
'  float m=B.z>.5?smoothstep(.905,.885,rr):smoothstep(0.,.006,uv.x)*smoothstep(0.,.006,1.-uv.x)*smoothstep(0.,.006,uv.y)*smoothstep(0.,.006,1.-uv.y);',
'  if(Cc.x<1.5)m*=smoothstep(Cc.x+.025,Cc.x-.025,rr);',
'  if(Dd.y>-.5){float x=rm>=0.?rm:rr;int bi=0;for(int i=1;i<10;i++){if(x>=(rm>=0.?OB[i]:PB[i]))bi=i;}float lo=rm>=0.?OB[bi]:PB[bi],hi=bi>=9?1.2:(rm>=0.?OB[bi+1]:PB[bi+1]);float loc=clamp(Dd.y-float(bi),0.,1.);m*=loc>=1.?0.:loc<=0.?1.:smoothstep(-.008,.008,x-mix(lo,hi,loc));}',   // bands go from the centre out, showing what is under (the owner's map)
'  if(m<=0.)return;vec3 c=textureLod(t,clamp(uv,0.,1.),lod).rgb;',
'  c*=mix(1.,mix(1.08,.84,smoothstep(0.,.9,rr)),Cc.y)*B.w*Dd.z*max(1.,B.x)*(1.+Cc.w*litK(q));',
'  float a=min(1.,B.x)*m;col=mix(col,c,a);hcov=max(hcov,a);}',
'float wsd(vec2 o){float hw=uWin.z,tp=uWin.w-hw;if(o.y>tp)return length(o-vec2(0.,tp))-hw;return max(abs(o.x)-hw,-uWin.w-o.y);}',   // the window opening: an arch on a rectangle (device px from its centre)
'vec4 art(sampler2D t,vec2 p,float hs,float spin){',
'  float r=length(p)/hs;if(spin!=0.){float b=0.;for(int i=0;i<8;i++)b+=step(FR[i],r);float dir=mod(b,2.)<.5?1.:-1.;p=rot(spin*dir*(.55+.09*b))*p;}',
'  vec2 uv=p/(2.*hs)+.5;vec2 e=smoothstep(vec2(0.),vec2(.004),uv)*smoothstep(vec2(0.),vec2(.004),1.-uv);',
'  return texture(t,clamp(uv,0.,1.))*e.x*e.y;}',
'float stars(vec2 sp,float dens,float seed,vec2 vel){',
'  vec2 g=sp*dens,id=floor(g),f=fract(g)-.5;float n=h21(id+seed);if(n<.80)return 0.;',
'  vec2 off=(vec2(h21(id+seed+1.3),h21(id+seed+2.7))-.5)*.7;vec2 dd=f-off;',
'  float sl=length(vel);if(sl>.001){vec2 dir=vel/sl;float al=dot(dd,dir);dd-=dir*clamp(al,-sl,sl);}',
'  float size=mix(.018,.05,h21(id+9.1));float tw=.62+.38*sin(uPT*(.5+2.*h21(id+4.4))+6.283*n);',
'  return smoothstep(size,0.,length(dd))*tw*(n-.80)/.20;}',
'void main(){',
'  vec2 q=(gl_FragCoord.xy-uCtr)/uUnit;',           // screen units, origin at the map centre
'  vec2 p=rot(-uRot)*q/uZoom+uCam;float r=length(p);',
'  float lz=log(uZoom);',
'  vec3 col=vec3(.0196,.0275,.051);',
'  vec2 sq=rot(-uRot)*q;',
'  if(uDust>0.){vec2 dp=sq*exp(-.18*lz)*1.3+uCam*.2;float n=vn(dp+vec2(uPT*.011,0.))*.55+vn(dp*2.3-vec2(0.,uPT*.017))*.3+vn(dp*5.1+3.7)*.15;',
'    n=smoothstep(.38,.9,n);col+=mix(vec3(.018,.032,.085),vec3(.085,.055,.02),vn(dp*.7+9.))*n*uDust;}',
'  if(uStars>0.){vec2 vel=normalize(sq+1e-5)*uStreak;float s=stars(sq*exp(.10*lz)+uCam*.1,7.,1.,vel*.6)*.55+stars(sq*exp(.22*lz)+uCam*.25,13.,5.,vel)*.8+stars(sq*exp(.40*lz)+uCam*.5,23.,9.,vel*1.6);',
'    col+=vec3(.82,.88,1.)*s*uStars;}',
'  if(uHb[0].x>0.&&uHc[0].z>.5)hero(tH0,uHa[0],uHb[0],uHc[0],uHd[0],uHL.x,q,col);if(uHb[1].x>0.&&uHc[1].z>.5)hero(tH1,uHa[1],uHb[1],uHc[1],uHd[1],uHL.y,q,col);',
'  float pm=uPA2.x;',
'  if(pm==1.){vec2 d=pD(q,p,uPA0,uPA1);vec4 a=pS(tP0,d,uPA1.z,0.,uPL.x);if(uPA2.w>0.)a.a*=smoothstep(1.,1.-uPA2.w,length(d));vec3 c=pLit(a.rgb,q,uPA1)*a.a;',      // one plate; uPA2.z > 0 adds a second, nearer copy (depth)
'    if(uPA2.z>0.){vec4 b=pS(tP0,pD(q,p,uPB0,uPA1),uPA1.z,0.,max(uPL.x-.5,0.));c+=pLit(b.rgb,q,uPA1)*b.a*uPA2.z;}',
'    col=col*(1.-uPA2.y*a.a)+c;}',
'  else if(pm==5.)pairL(q,p,col);',
'  float rv=smoothstep(uReveal+.012,uReveal-.012,length(p-uOrigP));float hole=max(uTitle,smoothstep(uHole*.82,uHole,length(p-uOrigP)));vec3 sky=col;float px=1./(uUnit*uZoom);vec3 gold=vec3(1.,.80,.42);',
'  if(uEmbA>0.||uLogoA>0.){vec2 pl=p;float rl=length(pl)/uLH;',
'    float lm=smoothstep(uLRev+.025,uLRev-.025,rl);',
'    float ed=uEmbD.z>0.?mix(uEmbD.z,1.,smoothstep(uEmbD.w*.8,uEmbD.w*1.15,length((q-uEmbD.xy)*vec2(1.,1.6)))):1.;',   // entry: the word rings behind the title sit at 55%
'    if(uEmbA>0.){vec4 a=art(tEmb,pl,uLH,uSpin)*uEmbA*lm;a.rgb*=uLogoK*ed;col=col*(1.-a.a)+a.rgb;}',
'    if(uLogoA>0.){float wm=smoothstep(uWords+.03,uWords-.03,rl);vec4 a=art(tLogo,pl,uLH,uSpin)*uLogoA*wm*lm;a.rgb*=uLogoK*ed;col=col*(1.-a.a)+a.rgb;}if(uFrontL.y>0.){float dF=(rl-uFrontL.x)*uLH/(px*2.6);col+=gold*(exp(-dF*dF)*1.1+exp(-dF*dF/70.)*.22)*uFrontL.y;}}',
'  if(uRing.x>0.){float an=atan(p.x,p.y);float st=.20943951;float idx=floor(an/st+.5);float ii=mod(idx+30.,30.);',
'    if(ii>.5||uRing0>.5){float ia=idx*st;vec2 pl=rot(ia)*(rot(-ia)*p-vec2(0.,uRing.y));float vis=clamp(uRing.z-ii,0.,1.);float dh=abs(ii-uRing.w);dh=min(dh,30.-dh);float hi=uRing.w<-50.?1.:uRing.w<-5.?0.:smoothstep(1.15,0.,dh);hi=max(hi,clamp(uRingL-ii,0.,1.));',
'      vec4 a=art(tOrig,pl,1.,0.)*uRing.x*vis;a.rgb*=mix(uRingDim,1.,hi);col=col*(1.-a.a)+a.rgb;',
'      float e=(length(pl)-.887)/(px*2.5+.025);col+=gold*exp(-e*e)*hi*vis*uRing.x*.8;}}',
'  if(uGen.y>0.){vec2 gd=vec2(-.545,.838);for(int k=6;k>=1;k--){float fk=float(k);float sc=pow(.72,fk);vec2 gc=gd*(1.-sc)/.28*1.55;float vis=clamp(uGen.x-(fk-1.),0.,1.);if(vis>0.){float hi=smoothstep(.9,0.,abs(fk-uGen.z));vec4 a=art(tOrig,p-gc,sc,0.)*uGen.y*vis;a.rgb*=.5*pow(.9,fk)+hi*.9;col=col*(1.-a.a)+a.rgb;float e=(length(p-gc)-.887*sc)/(px*2.5+.02*sc);col+=gold*exp(-e*e)*hi*vis*uGen.y*.9;}}}',
'  if(uOrigA>0.){vec4 a=art(tOrig,p-uOrigP,1.,0.)*uOrigA*rv;a.rgb*=uOrigK;col=col*(1.-a.a)+a.rgb;',
'    if(uRing.x>0.){float dh=min(abs(uRing.w),30.-abs(uRing.w));float e=(length(p-uOrigP)-.887)/(px*2.5+.025);col+=gold*exp(-e*e)*(uRing.w<-5.?0.:smoothstep(1.15,0.,dh))*uRing.x*.8;}}',
'  if(uCoreA>0.){vec4 a=art(tCore,p-uOrigP,.7,0.);a.a=1.;a*=uCoreA*rv*smoothstep(.7,.66,max(abs(p.x-uOrigP.x),abs(p.y-uOrigP.y)));col=col*(1.-a.a)+a.rgb;}',

'  col=mix(mix(sky,vec3(.012,.014,.022),min(1.,uOrigA+uLogoA+uEmbA)),col,hole);',
'  if(pm==6.||pm==3.)pairL(q,p,col);',
'  if(pm==4.){vec2 d=rot(-uPA0.w)*(p-uOrigP);',            // table 3: a ring of the map turns over (the twin plate's band, registered band for band), gold to pewter
'    for(int i=0;i<8;i++){vec2 bd=uBd[i];if(bd.x<=0.)continue;float s=abs(cos(3.14159*clamp(bd.y,0.,1.)));vec2 ds=vec2(d.x/max(s,.03),d.y);float rs=length(ds);',
'      float inb=smoothstep(OB[i+1]-.004,OB[i+1]+.004,rs)*smoothstep(OB[i+2]+.004,OB[i+2]-.004,rs)*step(.03,s);if(inb<=0.)continue;',
'      vec2 dt=ds*remap(rs)/max(rs,1e-5);vec3 f=pS(tP0,dt,1.,1.,uPL.x).rgb,g=pS(tP1,dt,1.,1.,uPL.y).rgb;vec3 gd=mix(f,g*vec3(1.,.8,.48),.35);float lu=dot(f,vec3(.299,.587,.114));',
'      vec3 c=bd.y<.5?gd:mix(f,vec3(lu),.8)*.85*uPA2.z;col=mix(col,pLit(c,q,uPA1)*(.75+.25*s),inb*bd.x);}}',
'  if(uPoolK>0.)col*=mix(1.-uPoolK,1.,smoothstep(uPoolR*.35,uPoolR,length(q)));',
'  col*=uDim;',
'  if(uHb[0].x>0.&&uHc[0].z<.5)hero(tH0,uHa[0],uHb[0],uHc[0],uHd[0],uHL.x,q,col);if(uHb[1].x>0.&&uHc[1].z<.5)hero(tH1,uHa[1],uHb[1],uHc[1],uHd[1],uHL.y,q,col);',
'  if(uPat.y>0.){float dP=(r-uPat.x)/(px*2.4+uPat.x*.004);col+=mix(gold,vec3(.6,.65,.76),uPatC)*(exp(-dP*dP)*1.+exp(-dP*dP/50.)*.2)*uPat.y;}',
'  if(uLineH.y>0.){float dL=(q.y-uLineH.x)*uUnit/1.3;col+=vec3(.8,.86,1.)*(exp(-dL*dL)*.9+exp(-dL*dL/90.)*.12)*uLineH.y*smoothstep(1.9,.5,abs(q.x));}',
'  if(uLineV.y>0.){float dL=(q.x-uLineV.x)*uUnit/1.3;col+=vec3(.8,.86,1.)*(exp(-dL*dL)*.7+exp(-dL*dL/90.)*.08)*uLineV.y*smoothstep(2.6,1.2,abs(q.y+.4));}',
'  if(uFront>0.){float dF=(r-uReveal)/(px*2.2);col+=gold*(exp(-dF*dF)*.85+exp(-dF*dF/60.)*.16)*uFront;}',
'  if(uGlint>0.){vec2 L=uOrb.y*vec2(cos(uOrb.x),sin(uOrb.x));float g=0.;',
'    for(int i=0;i<8;i++){float dd=(r-FR[i]*uRingS)/(px*1.6);g+=exp(-dd*dd)+exp(-dd*dd/40.)*.22;}',
'    float dl=length(p-L);col+=gold*g*uGlint*(uOrb.z/(1.+dl*dl*46.)+uLight.z*.05/(1.+r*r*9.));',
'    float od=dl/(uOrb.w*px*6.);col+=vec3(1.,.93,.78)*uOrb.z*uGlint*(exp(-od*od)*1.5+.28/(1.+od*od*.9));}',
'  if(uThA>0.){float dmin=1e9;float nd=0.;for(int i=0;i<8;i++){float fi=float(i);if(fi<=uThN){float dn=length(p-uTh[i])/(px*4.5);nd+=exp(-dn*dn);}if(i<7&&fi<uThN){vec2 ta=uTh[i],tb=mix(ta,uTh[i+1],clamp(uThN-fi,0.,1.));vec2 pa=p-ta,ba=tb-ta;float hh=clamp(dot(pa,ba)/max(dot(ba,ba),1e-6),0.,1.);dmin=min(dmin,length(pa-ba*hh));}}float dt=dmin/(px*1.7);col+=gold*(exp(-dt*dt)*1.5+exp(-dt*dt/60.)*.22+nd*1.6)*uThA;}',
'  for(int i=0;i<10;i++){if(uMk[i].z>0.){float dm;vec2 mq=q-uMk[i].xy;float od=mod(float(i),2.);',
'    if(uMkL>0.){vec2 tg=normalize(vec2(-uMk[i].y,uMk[i].x)+1e-5);float al=dot(mq,tg);float ll=uMkR*(od<.5?1.:1.55);vec2 sp=mq-tg*clamp(al,-ll,ll);',
'      dm=od<.5?abs(length(sp)-uMkR*.62)/(.006+uMkR*.07):max(length(sp)-uMkR*.05,0.)/(.006+uMkR*.07);}',
'    else dm=uMkR>0.?abs(length(mq)-uMkR)/.011:length(mq)/.03;',
'    col+=vec3(1.,.9,.72)*uMk[i].z*(exp(-dm*dm)*1.7+.22/(1.+dm*dm*.8))*(uMkL>0.?.62:1.);}}',
'  for(int i=0;i<6;i++){vec4 A=uTrA[i];if(A.w>0.){vec4 B=uTrB[i];vec2 dc=q-A.xy;float da=abs(length(dc)-A.z)*uUnit;float an=(atan(dc.y,dc.x)+1.5707963+B.w)/6.2831853;float u=B.y>0.?fract(an+1.):fract(1.-an);',
'    float on=step(u,B.x)*smoothstep(0.,.004,B.x);float hd=exp(-(B.x-u)*B.z);col+=vec3(1.,.82,.52)*on*A.w*(.55+hd*1.2)*(exp(-da*da/1.4)*.55+exp(-da*da/40.)*.09);}}',
'  if(uLight.z>0.){vec2 dv=q-uLS;float dl=length(dv)/uLight.y;float an=atan(dv.y,dv.x);',
'    float cor=vn(vec2(an*2.2+uPT*.07,dl*.9-uPT*.22))*.6+vn(vec2(an*5.+3.-uPT*.05,dl*2.1-uPT*.4))*.4;',
'    float spk=pow(abs(cos(an*3.+uPT*.03)),90.)*.5+pow(abs(cos(an*2.-uPT*.021+.7)),140.)*.35;',
'    col+=vec3(1.,.97,.9)*uLight.z*exp(-dl*dl*7.)*2.6+vec3(1.,.82,.5)*uLight.z*(.55/pow(1.+dl*dl*1.2,1.7))*(.62+.76*cor)+vec3(1.,.9,.7)*uLight.z*spk/(1.+dl*dl*.5)*.5;',
'    if(uMotes!=0.){float lr=log(length(dv)+1e-4);vec2 mp=vec2(an*2.86,lr*3.2+uPT*.085*sign(uMotes));float m=0.;',
'      for(int i=0;i<2;i++){vec2 g=mp*(i==0?vec2(3.,2.):vec2(5.,3.1))+float(i)*7.3,id=floor(g),f=fract(g)-.5;id.x=mod(id.x,i==0?18.:29.);float n=h21(id+float(i)*3.1);',
'        if(n>.55){vec2 off=(vec2(h21(id+1.7),h21(id+5.3))-.5)*.6;float dd=length((f-off)*vec2(1.,.55));m+=smoothstep(.07,0.,dd)*(n-.55)*2.2*(.5+.5*sin(uPT*(1.+3.*n)+n*40.));}}',
'      col+=vec3(1.,.86,.6)*m*abs(uMotes)*smoothstep(.0,.25,length(dv))*smoothstep(2.6,.5,length(dv))*.9;}}',
'  float wm=0.;',
'  if(uWin2.x>0.){vec2 o=gl_FragCoord.xy-uWin.xy;float g=uWin3.w,so=wsd(o),inb=0.,jl=0.,gw=0.,sh=0.,hl=9.,bid=-1.,lift=0.;vec2 tp=o;',     // the window: one basalt wall, an arched opening, thirty blocks in courses
'    if(so>0.)inb=1.;',
'    else{float best=1e9,top=0.;vec2 bt=o;',
'      for(int i=0;i<30;i++){vec4 Q=uWQ[i],B=uWB[i];vec2 c=(B.xy+B.zw)*.5,hz=(B.zw-B.xy)*.5-g*.5;',
'        vec2 e0=abs(o-c)-hz;float rs=length(max(e0,0.))+min(max(e0.x,e0.y),0.);float ho=Q.x<=0.?1.:clamp(-Q.z/(2.*hz.y),0.,1.);if(ho>0.)gw+=ho*exp(-max(rs,0.)/uWin4.x);',
'        if(Q.x<=0.)continue;vec2 lo=(o-c-Q.yz)/Q.w;vec2 e=abs(lo)-hz;float sd=length(max(e,0.))+min(max(e.x,e.y),0.);',
'        if(Q.w>1.0005){sh=max(sh,exp(-max(sd*Q.w,0.)/(g*7.))*.65*Q.x);if(sd<0.&&wsd(c+lo)<0.&&top<.5){top=1.;lift=1.;bt=c+lo;inb=Q.x;hl=-sd;bid=float(i);}}',
'        else if(sd<best){best=sd;if(top<.5){bt=c+lo;bid=float(i);}}}',
'      if(top<.5){if(best<0.&&wsd(bt)<0.){inb=1.;hl=-best;}else{bid=-1.;if(best<g*1.2)jl=1.-smoothstep(g*.15,g*1.2,best);}}else sh=0.;',
'      if(so>-g*.8)jl=max(jl,1.-smoothstep(0.,g*.8,-so));tp=bt;}',
'    vec3 wc=vec3(1.,.906,.722);vec3 st=textureLod(tW,clamp((tp+uWin.xy-uWin3.xy)/(2.*uWin3.z)+.5,0.,1.),uHL.z).rgb;st=mix(st,vec3(dot(st,vec3(.3,.59,.11))),.55)*vec3(1.06,1.,.9)*uWin2.y*(bid>=0.?.82+.36*h21(vec2(bid,4.7)):1.);',
'    st*=.62+.38*smoothstep(0.,g*1.4,hl);st+=wc*exp(-hl/(g*2.2))*.06*uWin2.z;',          // a cut edge, catching the light from the joints
'    if(so>0.)st+=wc*exp(-so/uWin2.w)*.10*(.4+.6*uWin2.z);',                               // the reveal round the opening, lit from inside
'    st+=wc*min(gw,1.4)*uWin4.y*(so>0.?.5:1.)*(1.-.8*lift);st*=1.-sh;',
'    vec3 jc=st*.2+wc*.42*uWin2.z;',
'    float k=uWin2.x;col=mix(col,st,inb*k);col=mix(col,jc,jl*k*(1.-inb));col=mix(col,col*(1.-sh),k*(1.-inb)*(1.-jl));wm=max(inb,jl)*k;}',
'  o=vec4(col,1.-max(wm*.96,hcov*.9));}'].join('\n');
var FS_BRIGHT = COMMON + 'uniform sampler2D t;uniform vec2 px;uniform float thr;in vec2 v;out vec4 o;void main(){vec4 s4=(texture(t,v+px*vec2(-.5,-.5))+texture(t,v+px*vec2(.5,-.5))+texture(t,v+px*vec2(-.5,.5))+texture(t,v+px*vec2(.5,.5)))*.25;vec3 c=s4.rgb*s4.a;float l=max(c.r,max(c.g,c.b));o=vec4(c*smoothstep(thr,thr+.35,l),1.);}';
var FS_DOWN = COMMON + 'uniform sampler2D t;uniform vec2 px;in vec2 v;out vec4 o;void main(){o=(texture(t,v+px*vec2(-1,-1))+texture(t,v+px*vec2(1,-1))+texture(t,v+px*vec2(-1,1))+texture(t,v+px*vec2(1,1)))*.25;}';
var FS_UP = COMMON + 'uniform sampler2D t,b;uniform vec2 px;in vec2 v;out vec4 o;void main(){vec4 s=(texture(t,v+px*vec2(-1,-1))+texture(t,v+px*vec2(1,-1))+texture(t,v+px*vec2(-1,1))+texture(t,v+px*vec2(1,1))+texture(t,v+px*vec2(0,1.5))+texture(t,v+px*vec2(0,-1.5))+texture(t,v+px*vec2(1.5,0))+texture(t,v+px*vec2(-1.5,0)))*.125;o=s+texture(b,v);}';
var FS_FIN = COMMON + [
'uniform sampler2D tS,tB;uniform vec2 uRes,uLUV,uRipC;uniform float uT,uBloom,uRays,uCA,uVig,uGrain,uExpo,uRipR,uRipA,uAsp,uFade;uniform int uN;uniform vec4 uGl,uLim;uniform float uGlX,uGlD,uLimD;',
'in vec2 v;out vec4 o;',
'void main(){vec2 uv=v;',
'  if(uRipA>0.){vec2 dv=(uv-uRipC)*vec2(uAsp,1.);float dl=length(dv);float k=(dl-uRipR)/.05;uv+=normalize(dv+1e-5)/vec2(uAsp,1.)*exp(-k*k)*k*uRipA;}',
'  vec2 dc=uv-.5;vec3 c;float gk=0.;vec3 gy=vec3(0.);',
'  if(uGl.z>0.){float s=(uv.y-uGl.x)/uGl.y;float ex=smoothstep(uGl.w,uGl.w*.55,abs(uv.x-uGlX));if(abs(s)<1.&&ex>0.){',
'    float al=asin(clamp(s,-.999,.999));vec3 n=uGlD>0.?vec3(1.47,1.5,1.55):vec3(1.5);vec3 be=asin(clamp(vec3(s)/n,-1.,1.));vec3 de=min(2.*(vec3(al)-be)*sign(s),vec3(1.15));',
'    gk=uGl.z*ex*smoothstep(1.,.86,abs(s));gy=-sign(s)*tan(de)*uGl.y*.62*gk;}}',
'  if(gk>0.){c=vec3(texture(tS,uv+vec2(0.,gy.r)).r,texture(tS,uv+vec2(0.,gy.g)).g,texture(tS,uv+vec2(0.,gy.b)).b);',
'    float s2=(uv.y-uGl.x)/uGl.y;uv.y+=gy.g;c*=1.-.1*gk;c+=vec3(.75,.82,1.)*gk*(pow(abs(s2),9.)*.32+exp(-pow((s2+.62)*7.,2.))*.05);}',
'  else if(uCA>0.){c=vec3(texture(tS,uv+dc*uCA).r,texture(tS,uv).g,texture(tS,uv-dc*uCA).b);}else c=texture(tS,uv).rgb;',
'  float msk=texture(tS,uv).a;',
'  vec3 b=texture(tB,uv).rgb;c+=b*uBloom*msk;',
'  if(uN>0&&uRays>0.){vec3 a=vec3(0.);vec2 st=(uv-uLUV)/float(uN)*.82;vec2 pp=uv;float w=1.;float j=h21(gl_FragCoord.xy+fract(uT)*61.);pp-=st*j;',
'    for(int i=0;i<uN;i++){pp-=st;a+=texture(tB,pp).rgb*w;w*=.94;}c+=a/float(uN)*uRays*2.2*(.2+.8*msk);}',
'  c*=uExpo;c=mix(c,.72+.28*(1.-exp(-(c-.72)/.28)),step(.72,c));',
'  float vg=1.-uVig*smoothstep(.25,1.05,length(dc*vec2(uAsp>1.?1.:uAsp*1.4,uAsp>1.?1./uAsp*1.4:1.))*1.25);c*=vg;',
'  if(uLim.w>0.){float mk=smoothstep(uLim.x,uLim.y,uLimD>0.?uv.x:1.-v.y)*uLim.w;float m=max(c.r,max(c.g,c.b)),cl=uLim.z,kn=cl*.55;',
'    float m2=m<kn?m:kn+(cl-kn)*(1.-exp(-(m-kn)/(cl-kn)));c=mix(c,c*m2/max(m,1e-4),mk);}',
'  float fr=floor(uT*24.);float g=h21(gl_FragCoord.xy*.71+fr*17.3)-.5;c+=g*uGrain*(.4+.6*(1.-dot(c,vec3(.333))));',
'  c*=uFade;',
'  float dth=(h21(gl_FragCoord.xy+3.1)+h21(gl_FragCoord.xy+7.7)-1.)/255.;',
'  o=vec4(max(c+dth,0.),1.);}'].join('\n');
var VS_TXT = '#version 300 es\nin vec2 a;in vec4 iR;in vec4 iU;in vec4 iC;in vec2 iX;uniform vec2 uRes;out vec2 v;out vec4 c;out float soft;void main(){vec2 q=a*.5+.5;vec2 lp=(q-.5)*iR.zw;float cs=cos(iX.y),sn=sin(iX.y);lp=vec2(lp.x*cs-lp.y*sn,lp.x*sn+lp.y*cs);vec2 p=iR.xy+lp;v=mix(iU.xy,iU.zw,q);c=iC;soft=iX.x;gl_Position=vec4(p/uRes*2.-1.,0.,1.);gl_Position.y=-gl_Position.y;}';
var FS_TXT = '#version 300 es\nprecision highp float;uniform sampler2D t;uniform float uRange,uLR,uLB;uniform vec2 uLP;in vec2 v;in vec4 c;in float soft;out vec4 o;float med(vec3 s){return max(min(s.r,s.g),min(max(s.r,s.g),s.b));}float h(vec2 p){vec3 q=fract(vec3(p.xyx)*.1031);q+=dot(q,q.yzx+33.33);return fract((q.x+q.y)*q.z);}void main(){float sf=max(soft,0.),dis=max(-soft,0.);vec3 s=texture(t,v).rgb;float sd=med(s)-.5;vec2 ts=vec2(textureSize(t,0));float spr=max(.5*dot(vec2(uRange)/ts,1./fwidth(v)),1.);float a=clamp(sd*spr/(1.+sf*spr*.9)+.5,0.,1.);a*=1./(1.+sf*1.4);vec3 col=c.rgb;if(dis>0.){float n=h(floor(gl_FragCoord.xy/2.))*.7+h(floor(gl_FragCoord.xy/7.))*.3;float e=n-dis;a*=smoothstep(0.,.06,e);col+=vec3(1.,.85,.6)*smoothstep(.12,0.,e)*.8;}col*=1.+uLB*smoothstep(1.4,0.,length(gl_FragCoord.xy-uLP)/uLR);o=vec4(col*c.a*a,c.a*a);}';

function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) + '\n' + src.split('\n').slice(0, 4).join('\n')); return s; }
function prog(vs, fs, attribs) {
  var p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
  if (attribs) attribs.forEach(function (n, i) { gl.bindAttribLocation(p, i, n); }); else gl.bindAttribLocation(p, 0, 'a');
  gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
  var u = {}, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS), i, inf;
  for (i = 0; i < n; i++) { inf = gl.getActiveUniform(p, i); u[inf.name.replace('[0]', '')] = gl.getUniformLocation(p, inf.name); }
  return { p: p, u: u };
}
function mkRT(w, h, hdr) {
  var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
  gl.texImage2D(gl.TEXTURE_2D, 0, hdr ? gl.RGBA16F : gl.RGBA8, w, h, 0, gl.RGBA, hdr ? gl.HALF_FLOAT : gl.UNSIGNED_BYTE, null);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  var f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
  return { t: t, f: f, w: w, h: h, bytes: w * h * (hdr ? 8 : 4) };
}
function freeRT(r) { if (r) { gl.deleteTexture(r.t); gl.deleteFramebuffer(r.f); } }
var rtBytes = 0, txBytes = 0;
function targets() {
  var k; for (k in RT) { if (Array.isArray(RT[k])) RT[k].forEach(freeRT); else freeRT(RT[k]); }
  var hdr = HDR && TIERS[tier].hdr, w = cv.width, h = cv.height, i;
  RT.scene = mkRT(w, h, hdr); RT.down = []; RT.up = [];
  var n = TIERS[tier].bloom;
  for (i = 0; i <= n; i++) RT.down.push(mkRT(Math.max(2, w >> (i + 1)), Math.max(2, h >> (i + 1)), hdr));
  for (i = 0; i < n; i++) RT.up.push(mkRT(RT.down[i].w, RT.down[i].h, hdr));
  rtBytes = RT.scene.bytes; RT.down.concat(RT.up).forEach(function (r) { rtBytes += r.bytes; });
  account();
}
function account() { alloc = rtBytes + txBytes + cv.width * cv.height * 4; if (alloc > peakAlloc) peakAlloc = alloc; }
function initGL() {
  gl = cv.getContext('webgl2', { alpha: false, antialias: false, depth: false, stencil: false, powerPreference: 'high-performance', preserveDrawingBuffer: !!F.capture });
  if (!gl) return false;
  HDR = !!(gl.getExtension('EXT_color_buffer_float') || gl.getExtension('EXT_color_buffer_half_float'));
  gl.getExtension('OES_texture_float_linear'); gl.getExtension('OES_texture_half_float_linear');
  P.scene = prog(VS, FS_SCENE); P.bright = prog(VS, FS_BRIGHT); P.down = prog(VS, FS_DOWN); P.up = prog(VS, FS_UP); P.fin = prog(VS, FS_FIN);
  P.txt = prog(VS_TXT, FS_TXT, ['a', 'iR', 'iU', 'iC', 'iX']);
  quad = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  TXT.buf = gl.createBuffer();
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  if (IMG.font && IMG.font.ok) upload('font');
  targets();
  return true;
}
/* ---------- textures: loaded on demand, counted ---------- */
var IMG = {};
function upload(k) {
  var m = IMG[k], t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, k !== 'font'); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, k !== 'font');
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, m.el);
  if (k === 'font') { gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); }
  else { gl.generateMipmap(gl.TEXTURE_2D); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    var an = gl.getExtension('EXT_texture_filter_anisotropic'); if (an) gl.texParameterf(gl.TEXTURE_2D, an.TEXTURE_MAX_ANISOTROPY_EXT, 4); }
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  TX[k] = t; m.bytes = m.el.naturalWidth * m.el.naturalHeight * 4 * (k === 'font' ? 1 : 1.34); txBytes += m.bytes; account();
}
function load(k, cb) {
  if (IMG[k]) { if (cb) { if (IMG[k].ok) cb(); else IMG[k].cbs.push(cb); } return; }
  var e = new Image(), m = IMG[k] = { el: e, ok: false, cbs: cb ? [cb] : [] };
  e.decoding = 'async';
  e.onload = function () { m.ok = true; if (gl && k === 'font') upload(k); m.cbs.forEach(function (f) { f(); }); m.cbs = []; dirty = true; };
  e.onerror = function () { m.err = true; m.cbs.forEach(function (f) { f(); }); };
  e.src = D.assets[k][(Math.min(screen.width, screen.height) < 700 || tier > 0) && D.assets[k][1] ? 1 : 0];
}
F.load = load; F.loaded = function (k) { return IMG[k] && IMG[k].ok; };
function keep(need) {
  var k; for (k in TX) if (k !== 'font' && need.indexOf(k) < 0) { gl.deleteTexture(TX[k]); delete TX[k]; txBytes -= IMG[k].bytes; account(); if (k.charAt(0) === 'p' && !F.capture) delete IMG[k]; }   // plates are released after their scene
  for (var i = 0; i < need.length; i++) { k = need[i]; if (!TX[k]) { if (IMG[k] && IMG[k].ok) upload(k); else if (!IMG[k]) load(k); } }
}
var blank = null;
function plod(k) {                            // mip level for a plate (texels per pixel): explicit, because derivatives are undefined inside the shader's loops
  var m = IMG[k]; if (!m || !m.ok) return 0; var hs = S.pA0[2] * (S.pA1[3] > .5 ? S.zoom : 1) * U * DPR; return Math.max(0, Math.log2(m.el.naturalWidth / Math.max(1, 2 * hs)));
}
function bind(unit, k) {
  gl.activeTexture(gl.TEXTURE0 + unit);
  if (TX[k]) gl.bindTexture(gl.TEXTURE_2D, TX[k]);
  else { if (!blank) { blank = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, blank); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); } gl.bindTexture(gl.TEXTURE_2D, blank); }
}

/* ---------- GPU text (MSDF) ---------- */
var TXT = { n: 0, max: 6000, data: null, buf: null, cache: {} };
TXT.data = new Float32Array(TXT.max * 14);
var FONT = D.font;
function shape(str) {                       // glyph positions in font units, cached
  var c = TXT.cache[str]; if (c) return c;
  var x = 0, g = [], i, ch, prev = 0, id, k;
  for (i = 0; i < str.length; i++) {
    id = str.charCodeAt(i); ch = FONT.c[id]; if (!ch) { ch = FONT.c[63]; id = 63; }
    k = FONT.k[prev + ',' + id]; if (k) x += k;
    if (ch[2] > 0) g.push([x + ch[4], ch[5], ch[0], ch[1], ch[2], ch[3], i]);
    x += ch[6]; prev = id;
  }
  return (TXT.cache[str] = { g: g, w: x });
}
/* text(str, x, y, sizePx, [r,g,b,a], opt): x,y in CSS px (screen). opt: align -1|0|1, soft, rot, track (px), fx(i,n,o) per glyph */
var fxo = { dx: 0, dy: 0, a: 1, s: 1, sy: 1, soft: 0 };
function text(str, x, y, size, col, opt) {
  opt = opt || {};
  if (F.rec && !opt.shadow) F.rec.push({ s: str, x: x, y: y, size: size, a: col[3], al: opt.align == null ? 0 : opt.align, w: F.measure(str, size, opt.track), rot: opt.rot || 0, soft: opt.soft || 0, small: opt.small || 0 });
  var sp = shape(str), k = size / FONT.size, tr = opt.track || 0, n = sp.g.length, i, g, gx, gy, w, h, o;
  var tw = sp.w * k + tr * (str.length - 1), al = opt.align == null ? 0 : opt.align;
  var x0 = x - (al === 0 ? tw / 2 : al > 0 ? tw : 0), rot = opt.rot || 0, cs = Math.cos(rot), sn = Math.sin(rot), a = TXT.data, q;
  for (i = 0; i < n; i++) {
    if (TXT.n >= TXT.max) return tw;
    g = sp.g[i]; w = g[4] * k; h = g[5] * k;
    gx = x0 + g[0] * k + tr * g[6] + w / 2 - x; gy = (g[1] - FONT.base) * k + h / 2;
    fxo.dx = 0; fxo.dy = 0; fxo.a = 1; fxo.s = 1; fxo.sy = 1; fxo.soft = 0; if (opt.fx) opt.fx(i, n, fxo, gx, gy, g[6]);
    if (fxo.a <= .003) continue;
    q = TXT.n * 14;
    gy *= fxo.sy; a[q] = (x + gx * cs - gy * sn + fxo.dx) * DPR; a[q + 1] = (y + gx * sn + gy * cs + fxo.dy) * DPR; a[q + 2] = w * fxo.s * DPR; a[q + 3] = h * fxo.s * fxo.sy * DPR;
    a[q + 4] = g[2] / FONT.w; a[q + 5] = g[3] / FONT.h; a[q + 6] = (g[2] + g[4]) / FONT.w; a[q + 7] = (g[3] + g[5]) / FONT.h;
    a[q + 8] = col[0]; a[q + 9] = col[1]; a[q + 10] = col[2]; a[q + 11] = col[3] * fxo.a;
    a[q + 12] = fxo.soft < 0 ? fxo.soft : (opt.soft || 0) + fxo.soft; a[q + 13] = rot;
    TXT.n++;
  }
  return tw;
}
F.text = text; F.measure = function (str, size, track) { return shape(str).w * size / FONT.size + (track || 0) * (str.length - 1); };
function w2s(wx, wy, S) {                   // world point -> CSS px, with the frame's camera
  var x = (wx - S.camx) * S.zoom, y = (wy - S.camy) * S.zoom, c = Math.cos(S.rot), s = Math.sin(S.rot);
  return [W * (S.cxf || .5) + (x * c - y * s) * U, H * CYF - (x * s + y * c) * U];
}
F.w2s = w2s;
/* in-picture words move like the captions (spec 4.11): per word, fade 520 ms, focus 720 ms (soft edge as the blur), rise 0.30 em with a small settle;
   60 ms between words, 140 ms between rows. exit 560 ms: soft and up, toward the light. kind 'copy' = the grey counterfeit (from above, flat curve, no settle).
   dust > 0: the word dissolves to dust instead (0..1). Reduced motion: opacity only. */
F.wordFx = function (str, age, sz, o) {
  o = o || {}; var row = o.row || 0, left = o.left == null ? 9 : o.left, copy = o.kind === 'copy', dust = o.dust || 0, CVc = F.curves;
  return function (i, n, fx, gx, gy, ci) {
    var w = 0; for (var j = 0; j < ci; j++) if (str.charCodeAt(j) === 32) w++;
    var u = age - row * .14 - w * .06, e = left < .56 ? CVc.out(1 - left / .56) : 0;
    if (RM) { fx.a = clamp(u / .4, 0, 1) * clamp(left / .3, 0, 1); return; }
    if (copy) { var cp = CVc.copy(u / .42); fx.a = cp; fx.soft = 1 - cp; fx.dy = -.30 * sz * (1 - cp); }
    else { var f9 = CVc.focus(u / .9); fx.a = CVc.fade(u / .52); fx.soft = 1 - CVc.focus(u / .72); fx.dy = .30 * sz * (1 - f9); fx.s = 1 + .035 * (1 - f9); }
    if (e > 0) { fx.a *= 1 - e; fx.soft += .6 * e; fx.dy -= .14 * sz * e; }
    if (dust > 0) { fx.soft = -Math.max(.001, dust); }
  };
};
function drawText() {
  if (!TXT.n || !TX.font) return;
  gl.useProgram(P.txt.p); gl.uniform2f(P.txt.u.uRes, cv.width, cv.height); gl.uniform1f(P.txt.u.uRange, FONT.range);
  gl.uniform2f(P.txt.u.uLP, (W * S.cxf + S.lx * U) * DPR, (H * (1 - CYF) + S.ly * U) * DPR); gl.uniform1f(P.txt.u.uLR, Math.max(.3, S.lsize * 3) * U * DPR); gl.uniform1f(P.txt.u.uLB, tier < 2 ? .12 * Math.min(1, S.light) : 0);   // words nearest the one light are a little brighter
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, TX.font); gl.uniform1i(P.txt.u.t, 0);
  gl.enable(gl.BLEND); gl.blendFuncSeparate(gl.ONE, gl.ONE_MINUS_SRC_ALPHA, gl.ZERO, gl.ONE);
  gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); gl.vertexAttribDivisor(0, 0);
  gl.bindBuffer(gl.ARRAY_BUFFER, TXT.buf); gl.bufferData(gl.ARRAY_BUFFER, TXT.data.subarray(0, TXT.n * 14), gl.DYNAMIC_DRAW);
  var st = 56, i, offs = [0, 16, 32, 48], sz = [4, 4, 4, 2];
  for (i = 0; i < 4; i++) { gl.enableVertexAttribArray(i + 1); gl.vertexAttribPointer(i + 1, sz[i], gl.FLOAT, false, st, offs[i]); gl.vertexAttribDivisor(i + 1, 1); }
  gl.drawArraysInstanced(gl.TRIANGLE_STRIP, 0, 4, TXT.n);
  for (i = 0; i < 4; i++) { gl.vertexAttribDivisor(i + 1, 0); gl.disableVertexAttribArray(i + 1); }
  gl.disable(gl.BLEND);
}

/* ---------- one frame ---------- */
function pass(p, rt) {
  gl.bindFramebuffer(gl.FRAMEBUFFER, rt ? rt.f : null); gl.viewport(0, 0, rt ? rt.w : cv.width, rt ? rt.h : cv.height);
  gl.useProgram(p.p); gl.bindBuffer(gl.ARRAY_BUFFER, quad); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
}
function fs() { gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); }
var S = F.S = {}; F.opt = {};                // F.opt: test switches for the gate only (notext, norefr)                           // the frame state, filled by shots.js
function render(t) {
  S = F.S = F.shots.state(t, S);            // pure: t -> state
  TXT.n = 0; F.rec = F.capture ? [] : null; F.shots.draw(t, S);            // pure: pushes text for this frame
  captions(t); endState(t);
  if (!gl) return fallback2d(S);
  keep(F.shots.need(t)); if (t >= 0) F.shots.need(t + 8).forEach(function (k) { load(k); });     // fetch the next scene's plates ahead of time
  var T = TIERS[tier], u, i, cx = cv.width * S.cxf, cy = cv.height * (1 - CYF), unit = U * DPR;
  pass(P.scene, RT.scene); u = P.scene.u;
  gl.uniform2f(u.uRes, cv.width, cv.height); gl.uniform2f(u.uCtr, cx, cy); gl.uniform1f(u.uUnit, unit);
  gl.uniform1f(u.uZoom, S.zoom); gl.uniform1f(u.uRot, S.rot); gl.uniform2f(u.uCam, S.camx, S.camy);
  gl.uniform1f(u.uT, t); gl.uniform1f(u.uPT, S.pt);
  gl.uniform2f(u.uOrigP, S.origx, S.origy); gl.uniform1f(u.uOrigK, S.origk); gl.uniform4f(u.uRing, S.ringa, S.ringr, S.ringn, S.ringhi); gl.uniform1f(u.uRingDim, S.ringdim);
  gl.uniform1f(u.uLH, S.ls); gl.uniform1f(u.uRing0, S.ring0); gl.uniform1f(u.uRingL, S.ringl || 0); gl.uniform1f(u.uLRev, S.lrev); gl.uniform1f(u.uLogoK, S.logok); gl.uniform4f(u.uGen, S.gen, S.gena, S.genlit, 0); gl.uniform2f(u.uFrontL, S.frontl, S.frontla); gl.uniform2f(u.uPat, S.patr, S.pata); gl.uniform1f(u.uPatC, S.patc); gl.uniform3fv(u.uMk, S.mk); gl.uniform1f(u.uMkR, S.mkr); gl.uniform1f(u.uMkL, S.mkl); gl.uniform4fv(u.uTrA, S.tra); gl.uniform4fv(u.uTrB, S.trb); gl.uniform2fv(u.uTh, S.th); gl.uniform1f(u.uThN, S.thn); gl.uniform1f(u.uThA, S.tha); gl.uniform2f(u.uLineH, S.lineh, S.lineha); gl.uniform2f(u.uLineV, S.linev, S.lineva);
  gl.uniform1f(u.uOrigA, S.orig); gl.uniform1f(u.uCoreA, S.core); gl.uniform1f(u.uLogoA, S.logo); gl.uniform1f(u.uEmbA, S.emb);
  gl.uniform1f(u.uWords, S.words); gl.uniform1f(u.uReveal, S.reveal); gl.uniform1f(u.uFront, S.front); gl.uniform1f(u.uTitle, S.title);
  gl.uniform1f(u.uSpin, S.spin); gl.uniform1f(u.uDim, S.dim);
  gl.uniform3f(u.uLight, 0, S.lsize, S.light); gl.uniform2f(u.uLS, S.lx, S.ly);
  gl.uniform4f(u.uOrb, S.orba, S.orbr, S.orb, 1); gl.uniform1f(u.uGlint, S.glint);
  gl.uniform1f(u.uMotes, S.motes); gl.uniform1f(u.uHole, S.hole); gl.uniform1f(u.uRingS, S.rings); gl.uniform1f(u.uPoolR, S.poolr); gl.uniform1f(u.uPoolK, S.poolg);
  gl.uniform1f(u.uStars, S.stars); gl.uniform1f(u.uDust, T.dust ? S.dust : 0); gl.uniform1f(u.uStreak, S.streak);
  bind(0, 'orig'); gl.uniform1i(u.tOrig, 0); bind(1, 'core'); gl.uniform1i(u.tCore, 1); bind(2, 'logo'); gl.uniform1i(u.tLogo, 2); bind(3, 'emb'); gl.uniform1i(u.tEmb, 3);
  var pm = (S.pa && TX[S.pa] && !F.opt.noplate) ? S.pm : 0; if ((pm === 3 || pm === 5 || pm === 6 || pm === 4) && !TX[S.pb]) pm = 0;     // a plate draws only once its texture is on the GPU
  gl.uniform4f(u.uPA2, pm, S.pA2[1], S.pA2[2], S.pA2[3]); gl.uniform4fv(u.uPA0, S.pA0); gl.uniform4fv(u.uPA1, S.pA1); gl.uniform4fv(u.uPB0, S.pB0); gl.uniform4fv(u.uPB1, S.pB1);
  gl.uniform4fv(u.uSeam, S.seam); gl.uniform4fv(u.uSeam2, S.seam2); gl.uniform2fv(u.uBd, S.bd); gl.uniform1f(u.uDisF, S.disf); gl.uniform4fv(u.uEmbD, S.embd); gl.uniform3f(u.uPL, plod(S.pa), plod(S.pb), S.pc && IMG[S.pc] && IMG[S.pc].ok ? Math.max(0, Math.log2(IMG[S.pc].el.naturalWidth * 1.25 / (U * DPR))) : 0);
  bind(4, S.pa); gl.uniform1i(u.tP0, 4); bind(5, S.pb); gl.uniform1i(u.tP1, 5); bind(6, S.pc); gl.uniform1i(u.tP2, 6);
  heroU(u);
  fs();
  if (!F.opt.notext) drawText();
  // bloom
  var n = T.bloom, src = RT.scene;
  pass(P.bright, RT.down[0]); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, src.t); gl.uniform1i(P.bright.u.t, 0);
  gl.uniform2f(P.bright.u.px, 1 / src.w, 1 / src.h); gl.uniform1f(P.bright.u.thr, (HDR && T.hdr) ? .92 : .8); fs();
  for (i = 1; i <= n; i++) { pass(P.down, RT.down[i]); gl.bindTexture(gl.TEXTURE_2D, RT.down[i - 1].t); gl.uniform1i(P.down.u.t, 0); gl.uniform2f(P.down.u.px, 1 / RT.down[i - 1].w, 1 / RT.down[i - 1].h); fs(); }
  var last = RT.down[n];
  for (i = n - 1; i >= 0; i--) {
    pass(P.up, RT.up[i]); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, last.t); gl.uniform1i(P.up.u.t, 0);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, RT.down[i].t); gl.uniform1i(P.up.u.b, 1); gl.uniform2f(P.up.u.px, 1 / last.w, 1 / last.h); fs(); last = RT.up[i];
  }
  pass(P.fin, null); u = P.fin.u;
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, RT.scene.t); gl.uniform1i(u.tS, 0);
  gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, last.t); gl.uniform1i(u.tB, 1);
  gl.uniform2f(u.uRes, cv.width, cv.height); gl.uniform1f(u.uT, S.gt == null ? t : S.gt); gl.uniform1f(u.uAsp, cv.width / cv.height);
  gl.uniform2f(u.uLUV, S.cxf + S.lx * unit / cv.width, (cy + S.ly * unit) / cv.height);
  gl.uniform1f(u.uBloom, S.bloom); gl.uniform1f(u.uRays, S.rays); gl.uniform1i(u.uN, T.rays);
  gl.uniform4f(u.uGl, (cy + S.lineh * unit) / cv.height, S.glw * unit / cv.height, F.opt.norefr ? 0 : S.glass, 1.25 * unit / cv.width); gl.uniform1f(u.uGlX, S.cxf); gl.uniform1f(u.uGlD, tier < 2 ? 1 : 0);
  gl.uniform4fv(u.uLim, S.lim); gl.uniform1f(u.uLimD, PORT ? 0 : 1);
  gl.uniform1f(u.uCA, S.ca); gl.uniform1f(u.uVig, S.vig); gl.uniform1f(u.uGrain, S.grain); gl.uniform1f(u.uExpo, S.expo); gl.uniform1f(u.uFade, S.fade);
  gl.uniform2f(u.uRipC, S.cxf + S.ripx * unit / cv.width, (cy + S.ripy * unit) / cv.height); gl.uniform1f(u.uRipR, S.ripr * unit / cv.height); gl.uniform1f(u.uRipA, S.ripa);
  fs();
}
/* hero plates (shots.js heroes(): CSS px, y down) and the window, to device px for the scene shader */
var HU = { a: new Float32Array(8), b: new Float32Array(8), c: new Float32Array(8), d: new Float32Array(8), l: [0, 0, 0], wb: new Float32Array(120), wq: new Float32Array(120) };
function heroOn(h) { return !!(h && h.a > 0 && TX[h.k] && !F.opt.noplate); }
function heroU(u) {
  var i, h, o, lw = 0;
  for (i = 0; i < 2; i++) { h = S.hero && S.hero[i]; o = i * 4;
    if (!heroOn(h)) { HU.b[o] = 0; HU.l[i] = 0; continue; }
    HU.a[o] = h.x * DPR; HU.a[o + 1] = (H - h.y) * DPR; HU.a[o + 2] = h.r * DPR; HU.a[o + 3] = h.ang;
    HU.b[o] = h.a; HU.b[o + 1] = h.asp; HU.b[o + 2] = h.disc; HU.b[o + 3] = h.dark;
    HU.c[o] = h.rev; HU.c[o + 1] = h.grade; HU.c[o + 2] = h.under; HU.c[o + 3] = h.lit;
    HU.d[o] = h.reg * DPR; HU.d[o + 1] = h.morph; HU.d[o + 2] = h.pulse; HU.d[o + 3] = h.regk;
    var m = IMG[h.k]; HU.l[i] = m && m.ok ? Math.max(0, Math.log2(m.el.naturalWidth / Math.max(1, 2 * h.r * DPR * h.asp))) : 0; }
  gl.uniform4fv(u.uHa, HU.a); gl.uniform4fv(u.uHb, HU.b); gl.uniform4fv(u.uHc, HU.c); gl.uniform4fv(u.uHd, HU.d);
  bind(7, S.hero && S.hero[0] && S.hero[0].k); gl.uniform1i(u.tH0, 7); bind(8, S.hero && S.hero[1] && S.hero[1].k); gl.uniform1i(u.tH1, 8);
  var w = S.win, wk = w && TX['p:basalt'] && !F.opt.noplate;
  if (wk) { var m2 = IMG['p:basalt']; lw = Math.max(0, Math.log2(m2.el.naturalWidth / Math.max(1, 2 * w.th * DPR)));
    gl.uniform4f(u.uWin, w.x * DPR, (H - w.y) * DPR, w.hw * DPR, w.hh * DPR); gl.uniform4f(u.uWin2, w.a, w.gain, w.joint, w.reveal * DPR);
    gl.uniform4f(u.uWin3, w.tx * DPR, (H - w.ty) * DPR, w.th * DPR, w.gap * DPR); gl.uniform4f(u.uWin4, w.glow * DPR, w.shaft, 0, 0);
    for (i = 0; i < 120; i++) { HU.wb[i] = w.b[i] * DPR; HU.wq[i] = (i & 3) === 1 || (i & 3) === 2 ? w.q[i] * DPR : w.q[i]; }
    gl.uniform4fv(u.uWB, HU.wb); gl.uniform4fv(u.uWQ, HU.wq); } else gl.uniform4f(u.uWin2, 0, 0, 0, 0);
  bind(9, 'p:basalt'); gl.uniform1i(u.tW, 9);
  gl.uniform3f(u.uHL, HU.l[0], HU.l[1], lw);
}
/* plain 2D picture for browsers with no WebGL2: art, camera, plates and light only */
var c2 = null;
function plate2d(S, cx, cy) {
  var pm = S.pm, A = IMG[S.pa], B = IMG[S.pb]; if (!pm || !A || !A.ok) return;
  var g0 = S.pA0, g1 = S.pA1, disc = pm >= 3, x, y, hs, ang, uu = U * DPR;
  if (g1[3] > .5) { var w = w2s(g0[0], g0[1], S); x = w[0] * DPR; y = w[1] * DPR; hs = g0[2] * S.zoom * uu; ang = -S.rot - g0[3]; }
  else { x = cx + g0[0] * uu; y = cy - g0[1] * uu; hs = g0[2] * uu; ang = -g0[3]; }
  var asp = disc ? 1 : g1[2], al = Math.min(1, g1[0] * (1 + g1[1] * .5)) * S.fade;
  function img(m, a, clip) { c2.save(); c2.translate(x, y); c2.rotate(ang); c2.globalAlpha = a; if (clip) clip(); else if (disc || S.pA2[3] > 0) { c2.beginPath(); c2.arc(0, 0, hs * (disc ? .9 : .92), 0, TAU); c2.clip(); }
    c2.drawImage(m.el, -hs * asp, -hs * (1 + (disc ? .026 : 0)), 2 * hs * asp, 2 * hs); c2.restore(); }
  c2.globalCompositeOperation = S.pA2[1] > .5 ? 'source-over' : 'lighter';
  if (pm === 1) img(A, al);
  else if (pm === 4) { for (var i = 0; i < 8; i++) if (S.bd[i * 2] > 0) { var r0 = [.118, .207, .296, .38, .462, .547, .624, .713, .84]; img(A, Math.min(1, S.bd[i * 2]) * S.fade, function () { c2.beginPath(); c2.arc(0, 0, r0[i + 1] * hs, 0, TAU); c2.arc(0, 0, r0[i] * hs, 0, TAU, true); c2.clip(); }); } }
  else { img(A, al); if (B && B.ok) {
      if (pm === 5) { var rr = Math.min(.9, S.disf / 9 * .905) * hs; if (rr > 0) img(B, Math.min(1, S.pB1[0] * (1 + S.pB1[1] * .5)) * S.fade, function () { c2.beginPath(); c2.arc(0, 0, rr, 0, TAU); c2.clip(); }); }
      else { var n = S.seam; c2.save(); c2.setTransform(1, 0, 0, 1, 0, 0); c2.beginPath(); var L = 1e5, ox = n[0] * n[2], oy = n[1] * n[2], tx = -n[1], ty = n[0];    // the light side of the seam (device px, y up in GL: flip)
        var Y = function (v) { return cv.height - v; }; c2.moveTo(ox + tx * L, Y(oy + ty * L)); c2.lineTo(ox - tx * L, Y(oy - ty * L)); c2.lineTo(ox - tx * L + n[0] * L, Y(oy - ty * L + n[1] * L)); c2.lineTo(ox + tx * L + n[0] * L, Y(oy + ty * L + n[1] * L)); c2.closePath(); c2.clip();
        c2.translate(x, y); c2.rotate(ang); c2.beginPath(); c2.arc(0, 0, hs * .9, 0, TAU); c2.clip(); c2.globalAlpha = Math.min(1, S.pB1[0] * (1 + S.pB1[1] * .5)) * S.fade; c2.drawImage(B.el, -hs, -hs * 1.026, 2 * hs, 2 * hs); c2.restore(); } } }
  c2.globalCompositeOperation = 'source-over'; c2.globalAlpha = 1;
}
function hero2d(under) {
  for (var i = 0; i < 2; i++) { var h = S.hero && S.hero[i], m = h && IMG[h.k]; if (!h || !(h.a > 0) || !m || !m.ok || (h.under ? 1 : 0) !== under) continue;
    var x = h.x * DPR, y = h.y * DPR, r = h.r * DPR, rv = Math.min(h.rev, .905);
    if (h.morph > -.5) rv = Math.min(rv, .905 * (1 - clamp(h.morph / 9, 0, 1)));
    c2.save(); c2.translate(x, y); c2.rotate(-h.ang); c2.globalAlpha = Math.min(1, h.a) * Math.min(1, h.dark) * S.fade;
    if (h.disc) { c2.beginPath(); c2.arc(0, 0, r * rv, 0, TAU); c2.clip(); }
    c2.drawImage(m.el, -r * h.asp, -r * (1 + (h.disc > 1.5 ? .026 : 0)), 2 * r * h.asp, 2 * r); c2.restore(); }
  c2.globalAlpha = 1;
}
function fallback2d(S) {
  if (!c2) { c2 = cv.getContext('2d'); if (!c2) return; }
  var cx = W * S.cxf * DPR, cy = H * CYF * DPR, k = U * DPR * S.zoom;
  c2.setTransform(1, 0, 0, 1, 0, 0); c2.fillStyle = '#05070d'; c2.fillRect(0, 0, cv.width, cv.height);
  function put(key, hs, al) { var m = IMG[key]; if (!m || !m.ok || al <= .01) return; c2.globalAlpha = al * S.dim * S.fade; c2.save(); c2.translate(cx - S.camx * k, cy + S.camy * k); c2.rotate(-S.rot); c2.drawImage(m.el, -hs * k, -hs * k, 2 * hs * k, 2 * hs * k); c2.restore(); }
  if (!F.opt.noplate) { hero2d(1); plate2d(S, cx, cy); }
  put('emb', S.ls, S.emb); put('logo', S.ls, S.logo); put('orig', 1, S.orig * (S.reveal >= 1 ? 1 : 0));
  if (!F.opt.noplate) hero2d(0);
  var i2, A = S.tra, B = S.trb, ux = W * S.cxf * DPR, uy = H * CYF * DPR, uu = U * DPR;
  c2.lineWidth = 1.2 * DPR; c2.strokeStyle = 'rgb(255,209,133)';
  for (i2 = 0; i2 < 6; i2++) if (A[i2 * 4 + 3] > 0 && B[i2 * 4] > 0) { var st2 = Math.PI / 2 + B[i2 * 4 + 3], sw = TAU * B[i2 * 4] * B[i2 * 4 + 1]; c2.globalAlpha = Math.min(1, A[i2 * 4 + 3] * .9) * S.fade; c2.beginPath(); c2.arc(ux + A[i2 * 4] * uu, uy - A[i2 * 4 + 1] * uu, A[i2 * 4 + 2] * uu, st2, st2 - sw, sw > 0); c2.stroke(); }
  if (S.glass > 0) { var gy2 = uy - S.lineh * uu, gw = S.glw * uu, gg = c2.createLinearGradient(0, gy2 - gw, 0, gy2 + gw); gg.addColorStop(0, 'rgba(190,210,255,0)'); gg.addColorStop(.5, 'rgba(205,220,255,.55)'); gg.addColorStop(1, 'rgba(190,210,255,0)'); c2.globalAlpha = S.glass * S.fade; c2.fillStyle = gg; c2.fillRect(ux - 1.25 * uu, gy2 - gw, 2.5 * uu, 2 * gw); }
  if (S.light > 0) { c2.globalAlpha = Math.min(1, S.light) * S.fade; var lx = cx + S.lx * U * DPR, ly = cy - S.ly * U * DPR, r = S.lsize * U * DPR * 2.4, g = c2.createRadialGradient(lx, ly, 0, lx, ly, r); g.addColorStop(0, 'rgba(255,246,226,1)'); g.addColorStop(.18, 'rgba(255,214,140,.55)'); g.addColorStop(1, 'rgba(255,200,120,0)'); c2.fillStyle = g; c2.fillRect(lx - r, ly - r, 2 * r, 2 * r); }
  c2.globalAlpha = 1;
}

/* ---------- captions: real text; transform, opacity and filter only. The Focus Pull (FILM-MOTION-AND-PLATES.md section 4):
   every caption comes into focus phrase by phrase and leaves by going out of focus, drifting a few pixels toward the one light.
   capState(i, t) is pure: the same time always gives the same styles. ---------- */
var CAPS = D.caps, capEl = [$('capA'), $('capB')], capCur = [-1, -1], pool = $('pool');
var CV = F.curves = { focus: bez(.16, 1, .3, 1), fade: bez(.33, 0, .2, 1), out: bez(.5, 0, .75, 0), copy: bez(.45, 0, .55, 1), sweep: bez(.45, 0, .55, 1) };
var capM = null, emCache = {};
function capClass(c) { return 'cap' + (c.big ? ' big' : '') + (c.long ? ' long' : ''); }
function emOf(c) {                            // the caption's font size in px, for this layout (read once, cached)
  var key = capClass(c) + W + 'x' + H; if (emCache[key]) return emCache[key];
  if (!capM) { capM = d.createElement('p'); capM.id = 'capM'; capM.setAttribute('aria-hidden', 'true'); capM.style.visibility = 'hidden'; capM.textContent = 'M'; $('stage').appendChild(capM); }
  capM.className = capClass(c); return (emCache[key] = parseFloat(getComputedStyle(capM).fontSize) || 40);
}
function capBuild(el, c) {
  var h = '', i, g = c.g, sp = '';
  for (i = 0; i < g.length; i++) { var cl = c.qn ? (i < c.qn ? ' q' : ' x') : ''; h += '<span class="g' + cl + '">' + g[i] + '</span>' + (i < g.length - 1 ? ' ' : ''); sp += '<span class="h">' + g[i] + '</span>' + (i < g.length - 1 ? ' ' : ''); }
  if (c.v === 'P') h += '<span class="lp" aria-hidden="true">' + sp + '</span>';     // the PEAK light pass: a lit copy under a moving mask
  el.innerHTML = h; el.className = capClass(c);
  el._g = el.querySelectorAll('.g'); el._lp = el.querySelector('.lp'); el._key = '';
}
function capGeo(el) {                         // caption centre and width, in CSS px (layout only, no transforms); cached per layout
  var k = W + 'x' + H; if (el._key !== k) { el._key = k; el._cx = el.offsetLeft; el._cy = el.offsetTop; el._w = el.offsetWidth; } return el;
}
function exitDir(S, cx, cy) {                 // unit vector toward the film light, never downward; straight up when there is no light
  if (!(S.light > .01)) return [0, -1];
  var lx = W * S.cxf + S.lx * U - cx, ly = H * CYF - S.ly * U - cy; if (ly > 0) ly = 0; var l = Math.sqrt(lx * lx + ly * ly);
  return l < 1 ? [0, -1] : [lx / l, ly / l];
}
function capState(i, t, em, dir) {
  var c = CAPS[i], n = c.g.length, v = c.v, R = { v: v, o: 1, b: 0, x: 0, y: 0, s: 1, br: 1, g: [], lp: -1 }, k, u, e, lowT = tier === 2;
  if (RM) {                                   // reduced motion: a plain fade, nothing moves
    var pv = CAPS[i - 1], lead = clamp(c.t0 - (pv ? pv.t1 + .32 : -1), 0, .3);   // starts up to 0.3 s early (never before the last caption is gone) so the plain fade costs no reading time
    R.o = clamp((t - c.t0 + lead) / .4, 0, 1) * (1 - clamp((t - c.t1) / .3, 0, 1));
    for (k = 0; k < n; k++) R.g.push({ o: 1, b: 0, y: 0, sx: 1 }); return R;
  }
  if (v === 'S') {                            // the STOP line: everything stops; only the words appear
    R.o = clamp((t - c.t0) / .9, 0, 1) * (1 - CV.out((t - c.t1) / c.out));
    for (k = 0; k < n; k++) R.g.push({ o: 1, b: 0, y: 0, sx: 1 }); return R;
  }
  var stag = clamp(.55 * c.say / n, .12, .42) * (v === 'P' ? 1.3 : v === 'F' ? 1.5 : 1), qn = v === 'Q' ? c.qn : n, gs = 0;
  if (v === 'Q' && qn < n) gs = c.t0 + (qn - 1) * stag + capReady(em, 'O') + .22;   // the grey copy arrives after the gold original reads
  for (k = 0; k < n; k++) {
    var G = { o: 1, b: 0, y: 0, sx: 1 };
    if (k >= qn) { u = (t - gs - (k - qn) * stag) / .42; var cp = CV.copy(u); G.o = cp; G.b = .10 * em * (1 - cp); G.y = -.30 * em * (1 - cp); }
    else {
      u = t - c.t0 - k * stag;
      if (v === 'W') { G.o = CV.fade(u / .3); G.b = .12 * em * (1 - CV.focus(u / .38)); G.y = .18 * em * (1 - CV.focus(u / .48)); }
      else if (v === 'F') { G.o = CV.fade(u / .8); G.b = .22 * em * (1 - CV.focus(u / 1.15)); G.y = .30 * em * (1 - CV.focus(u / 1.3)); }
      else { var f9 = CV.focus(u / .9); G.o = CV.fade(u / .52); G.b = .16 * em * (1 - CV.focus(u / .72)); G.y = .30 * em * (1 - f9); G.sx = 1 + .035 * (1 - f9); }
    }
    if (v === 'Q' && k >= qn && t > c.t1 - .12) G.o *= 1 - CV.out((t - c.t1 + .12) / c.out);   // the copy leaves first; the original is the last thing seen
    R.g.push(G);
  }
  e = CV.out((t - c.t1) / c.out);
  if (v === 'W') R.o = 1 - e;
  else if (e > 0) {
    R.o = 1 - e; R.s = 1 - .015 * e; var dd = .14 * em * e; R.x = dir[0] * dd; R.y = dir[1] * dd;
    if (v === 'F' && c.out > 1) { R.b = .30 * em * e; R.br = 1 + .35 * e; } else R.b = .10 * em * e;   // the last question exits into the light
  }
  if (v === 'P' && !lowT && D.marks[c.pk] != null) { u = (t - D.marks[c.pk] + .45) / .9; if (u > 0 && u < 1) R.lp = CV.sweep(u); }
  var cap = lowT ? 0 : tier === 1 ? 4 : 6, nb = 0;           // filter budget: at most six blurred spans (four on the reduced tier, none on low)
  for (k = 0; k < n; k++) { var gg = R.g[k]; if (gg.b > .124) { if (nb < cap) nb++; else gg.b = 0; } }
  if (lowT) { R.b = 0; R.br = 1; }
  return R;
}
var readyC = {};
function capReady(em, v) {                    // seconds from a group's start until it reads (blur at or under 1.5 px, opacity at or above 0.9)
  var key = v + em; if (readyC[key] != null) return readyC[key];
  for (var s = 0; s < 3; s += .005) { var b = v === 'F' ? .22 * em * (1 - CV.focus(s / 1.15)) : .16 * em * (1 - CV.focus(s / .72)), o = v === 'F' ? CV.fade(s / .8) : CV.fade(s / .52); if (b <= 1.5 && o >= .9) break; }
  return (readyC[key] = s);
}
function px(v) { return Math.round(v * DPR) / DPR; }
function blurCss(b, br) { b = Math.round(b * 4) / 4; return (b > 0 ? 'blur(' + b + 'px)' : '') + (br > 1.001 ? (b > 0 ? ' ' : '') + 'brightness(' + br.toFixed(3) + ')' : '') || 'none'; }
function poolAt(t) {                          // the dark ground: before the words, held between captions closer than 1.2 s, gone with the last word
  var i, c, best = 0;
  for (i = 0; i < CAPS.length; i++) { c = CAPS[i]; if (t < c.t0 - .75) break; var nx = CAPS[i + 1], end = c.t1 + c.out;
    if (t < c.t0) best = Math.max(best, sm((t - c.t0 + (RM ? .75 : .45)) / .38));
    else if (t <= c.t1) best = 1;
    else if (nx && nx.t0 - end < 1.2 && t < nx.t0) best = 1;
    else if (t < end) best = Math.max(best, 1 - (c.v === 'S' ? CV.out((t - c.t1) / c.out) : CV.out((t - c.t1) / c.out))); }
  return best;
}
F.plate = function () {
  var hs = (S.hero || []).filter(function (h) { return h && h.a > 0; }), r = { pm: S.pm || 0, pa: S.pa, pb: S.pb, pc: S.pc, gpu: gl ? !!(S.pa && TX[S.pa]) && (!S.pb || !!TX[S.pb]) : !!(S.pa && IMG[S.pa] && IMG[S.pa].ok), heroes: hs.map(function (h) { return h.k; }), win: !!S.win };
  if (hs.length || S.win) { var ks = hs.map(function (h) { return h.k; }); if (S.win) ks.push('p:basalt');
    var on = ks.every(function (k) { return gl ? !!TX[k] : !!(IMG[k] && IMG[k].ok); });
    if (!r.pm) { r.pm = 7; r.pa = ks[0]; r.pb = ks[1] || null; r.gpu = on; } else { r.gpu = r.gpu && on; r.pb = r.pb || ks[0]; } }
  return r; };
F.heroGeo = function () { return { hero: (S.hero || []).map(function (h) { return h ? { k: h.k, x: h.x, y: h.y, r: h.r, ang: h.ang, a: h.a, asp: h.asp, disc: h.disc, dark: h.dark, rev: h.rev, morph: h.morph, reg: h.reg, regk: h.regk, under: h.under } : null; }), win: S.win ? { x: S.win.x, y: S.win.y, hw: S.win.hw, hh: S.win.hh, a: S.win.a, b: Array.from(S.win.b), q: Array.from(S.win.q), labels: S.win.labels || [] } : null }; };
F.capState = function (i, t) {               // for the gate: the pure caption state at any time
  var S2 = F.shots.state(t, {}), el = capEl[i % 2], c = CAPS[i];
  if (capCur[i % 2] !== i) { capBuild(el, c); capCur[i % 2] = i; }
  capGeo(el); var R = capState(i, t, emOf(c), exitDir(S2, el._cx, el._cy)); R.em = emOf(c); R.ready = capReady(emOf(c), c.v === 'F' ? 'F' : 'O'); return R;
};
function captions(t) {
  var i, c, slot, shown = [false, false];
  for (i = 0; i < CAPS.length; i++) {
    c = CAPS[i]; if (t < c.t0 - (RM ? .3 : .05) || t > c.t1 + c.out) continue;
    slot = i % 2; shown[slot] = true;
    var el = capEl[slot]; if (capCur[slot] !== i) { capBuild(el, c); capCur[slot] = i; }
    capGeo(el); var R = capState(i, t, emOf(c), exitDir(S, el._cx, el._cy)), k, st = el.style;
    st.opacity = R.o.toFixed(3);
    st.transform = 'translate3d(calc(-50% + ' + px(R.x) + 'px),' + px(R.y) + 'px,0)' + (R.s !== 1 ? ' scale(' + R.s.toFixed(4) + ')' : '');
    st.filter = blurCss(R.b, R.br);
    for (k = 0; k < el._g.length; k++) { var G = R.g[k], s = el._g[k].style; s.opacity = G.o.toFixed(3);
      s.transform = G.y || G.sx !== 1 ? 'translate3d(0,' + px(G.y) + 'px,0)' + (G.sx !== 1 ? ' scaleX(' + G.sx.toFixed(4) + ')' : '') : 'none'; s.filter = blurCss(G.b, 1); }
    if (el._lp) { var lp = el._lp.style; if (R.lp >= 0) { var w = el._w, toL = (W * S.cxf + S.lx * U) < el._cx, pos = toL ? lerp(w, -.4 * w, R.lp) : lerp(-.4 * w, w, R.lp); lp.opacity = '1'; lp.webkitMaskPosition = lp.maskPosition = px(pos) + 'px 0'; } else lp.opacity = '0'; }
  }
  for (slot = 0; slot < 2; slot++) if (!shown[slot] && capCur[slot] !== -1) { capEl[slot].innerHTML = ''; capEl[slot].removeAttribute('style'); capEl[slot].style.opacity = 0; capCur[slot] = -1; }   // emptied, so the page never depends on what was seen before
  pool.style.opacity = (poolAt(t) * (S.poolk == null ? 1 : S.poolk)).toFixed(3);
}

/* ---------- the end: "Enter the map" is part of the picture, a function of time like everything else ---------- */
var door = null;
function endState(t) {
  if (!door) door = d.querySelector('#end .door'); var e = mode === 'film' && t >= 0 && F.shots.endAt != null ? sm((t - F.shots.endAt) / 1.2) : 0;
  d.documentElement.classList.toggle('ended', e > 0);
  if (door) { door.style.opacity = e.toFixed(3); door.style.transform = 'translate3d(0,' + (Math.round((1 - E.out3(e)) * 12 * DPR) / DPR) + 'px,0)'; }
}
/* ---------- clock ---------- */
var mode = 'entry', t = 0, playing = false, lastNow = 0, tau = 0, raf = 0, dirty = true, audio = null, snd = true, resync = false, lastSync = 0;
F.dur = D.dur;
function now() { return performance.now() / 1000; }
function frame() {
  raf = 0; var n = now(), dt = Math.min(.5, n - lastNow); lastNow = n;
  if (mode === 'entry') { tau += dt * (RM ? .25 : 1); F.shots.tau = tau; render(-1); gov(dt); }
  else {
    if (playing) {
      if (audio && snd && !audio.paused && audio.readyState >= 3) {        // the clock follows the score when sound is on
        var at = audio.currentTime; t += dt; var dr = at - t; drift = dr;
        if (resync || Math.abs(dr) > 1) { if (Math.abs(dr) > .25 && n - lastSync > 1) { try { audio.currentTime = t; } catch (e) {} lastSync = n; } resync = false; }   // a seek the score did not take: the picture leads, the score is sent after it
        else if (Math.abs(dr) > .04) t = at; else t += dr * .1; }
      else { t += dt; if (audio && snd && playing) resync = true; }        // still loading or stalled: the picture runs on, and the score catches up to it
      if (t >= F.dur) { t = F.dur; playing = false; ended(); }
      gov(dt);
    }
    render(t); progress();
  }
  if (mode === 'entry' || playing || dirty) { dirty = false; go(); }
}
function go() { if (!raf && !F.capture && !d.hidden) raf = requestAnimationFrame(frame); }
var drift = 0;
F.seek = function (x) { mode = x < 0 ? 'entry' : 'film'; d.documentElement.setAttribute('data-mode', mode); if (x < 0) { tau = -x; F.shots.tau = tau; render(-1); } else { t = clamp(x, 0, F.dur); if (audio) try { audio.currentTime = t; } catch (e) {} render(t); progress(); } d.documentElement.setAttribute('data-mode', mode); return F.S; };
F.time = function () { return mode === 'entry' ? -tau : t; };

/* ---------- governor: frame-time window, steps between shots ---------- */
var ft = [], drops = 0, tierLog = [], pend = 0, lastStep = 0, slow = 0;
function gov(dt) {
  ft.push(dt); if (ft.length > 1800) ft.shift();
  if (dt > .034) drops++;
  if (F.capture || ft.length < 120) return;
  var n = Math.min(ft.length, 600), s = 0, i; for (i = ft.length - n; i < ft.length; i++) s += ft[i]; var avg = s / n;
  var tnow = now();
  if (avg > .0215 && tier < 2 && tnow - lastStep > 12) pend = 1;
  else if (avg < .0172 && tier > 0 && tnow - lastStep > 45 && slow === 0) pend = -1; else if (avg <= .0215 && pend > 0) pend = 0;
  if (pend && (mode === 'entry' || F.shots.boundary(t, dt))) { setTier(tier + pend, avg); if (pend > 0) slow++; pend = 0; }
}
function setTier(n, avg) {
  n = clamp(n, 0, 2); if (n === tier) return; tier = n; lastStep = now(); ft = [];
  tierLog.push({ at: +F.time().toFixed(1), tier: TIERS[n].name, avg: avg ? +(avg * 1000).toFixed(1) : 0 });
  layout(); if (gl) targets(); dirty = true;
}
F.setTier = setTier; F.tier = function () { return TIERS[tier].name; };

/* ---------- controls ---------- */
var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
var wake = null;
function wakeOn() { if (navigator.wakeLock) navigator.wakeLock.request('screen').then(function (w) { wake = w; }).catch(function () {}); }
function wakeOff() { if (wake) { try { wake.release(); } catch (e) {} wake = null; } }
function setPlaying(on) {
  playing = on; d.documentElement.classList.toggle('paused', !on && mode === 'film');
  if (audio) { if (on && snd) { if (Math.abs(audio.currentTime - t) > .1) try { audio.currentTime = t; } catch (e) {} var p = audio.play(); if (p && p.catch) p.catch(function () {}); } else audio.pause(); }
  if (on) { wakeOn(); lastNow = now(); go(); } else wakeOff();
  var b = $('pp'); if (b) { b.setAttribute('aria-label', on ? 'Pause' : 'Play'); b.setAttribute('aria-pressed', on ? 'true' : 'false'); }
}
function begin() {
  if (mode !== 'entry') return;
  F.shots.tau0 = tau; mode = 'film'; t = 0; d.documentElement.setAttribute('data-mode', 'film');
  if (audio && snd) { audio.preload = 'auto'; try { audio.currentTime = 0; } catch (e) {} }
  if (navigator.vibrate) try { navigator.vibrate(12); } catch (e) {}
  setPlaying(true); showUI();
}
function ended() { endState(t); wakeOff(); }
function progress() { var p = $('bar'); if (p) p.style.transform = 'scaleX(' + (t / F.dur).toFixed(5) + ')'; }
var uiT = 0;
function showUI() { d.documentElement.classList.add('ui'); clearTimeout(uiT); uiT = setTimeout(function () { if (playing) d.documentElement.classList.remove('ui'); }, 2500); }
F.begin = begin; F.play = function () { setPlaying(true); }; F.pause = function () { setPlaying(false); };
F.state = function () {
  var n = Math.min(ft.length, 600), s = 0, i, a = ft.slice(-n).sort(function (x, y) { return x - y; }); for (i = 0; i < a.length; i++) s += a[i];
  return { mode: mode, t: +F.time().toFixed(3), playing: playing, tier: TIERS[tier].name, dpr: DPR, w: W, h: H, gl: !!gl, hdr: HDR && !!TIERS[tier].hdr,
    fps: n ? +(n / s).toFixed(1) : 0, p95: n ? +(a[Math.floor(n * .95)] * 1000).toFixed(1) : 0, drops: drops, allocMB: +(alloc / 1048576).toFixed(1), peakMB: +(peakAlloc / 1048576).toFixed(1),
    drift: +(drift * 1000).toFixed(1), sound: !!(audio && snd), audioT: audio ? +audio.currentTime.toFixed(3) : null, audioDur: audio && isFinite(audio.duration) ? audio.duration : null, ctxLost: ctxLost, tiers: tierLog, glyphs: TXT.n, caps: capCur.slice(), ready: ready };
};

/* ---------- boot ---------- */
var ready = false;
function boot() {
  F.capture = /[?&]capture/.test(location.search); if (F.capture) d.documentElement.classList.add('capture');
  var q = /[?&]tier=(\d)/.exec(location.search); if (q) tier = +q[1];
  layout();
  try { if (!/[?&]nogl/.test(location.search)) initGL(); } catch (e) { console.error('gl', e); gl = null; }
  if (!gl) d.documentElement.classList.add('nogl');
  cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); ctxLost++; gl = null; TX = {}; RT = {}; });
  cv.addEventListener('webglcontextrestored', function () { tier = Math.min(2, tier + 1); try { initGL(); layout(); targets(); } catch (e) { gl = null; } dirty = true; go(); });
  var need = D.first.slice(), left, ring = $('ring');
  if (F.capture) for (var pk in D.assets) if (pk.charAt(0) === 'p' && pk.charAt(1) === ':') need.push(pk);   // exact frames: every plate in memory first, so seek(t) never waits for a download
  left = need.length;
  function one() { left--; if (ring) ring.style.strokeDashoffset = (ring.getTotalLength ? 283 * left / need.length : 0).toFixed(1); if (left <= 0) { var fin = function () { ready = true; d.documentElement.classList.add('ready'); dirty = true; if (F.capture) render(F.time() < 0 ? -1 : t); go(); }; if (d.fonts && d.fonts.ready) Promise.all([d.fonts.load('1em Voice'), d.fonts.load('1em "Source Serif"'), d.fonts.ready]).then(fin, fin); else fin(); } }
  need.forEach(function (k) { load(k, one); });
  setTimeout(function () { D.later.forEach(function (k) { load(k); }); }, 1500);
  if (D.audio && !F.capture) { audio = new Audio(); audio.preload = 'metadata'; audio.src = D.audio.src; }      // never in ?capture: frames there are a function of the clock alone
  var sb = $('snd');
  function sndSet(on) { snd = on; d.documentElement.classList.toggle('mute', !on); [sb, $('snd2')].forEach(function (b) { if (b) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.querySelector('.l').textContent = on ? 'Sound on' : 'Sound off'; } });
    if (audio) { if (on && playing) { try { audio.currentTime = t; } catch (e) {} var p = audio.play(); if (p && p.catch) p.catch(function () {}); } else if (!on) audio.pause(); } }
  if (!audio) { if (sb) sb.hidden = true; if ($('snd2')) $('snd2').hidden = true; snd = false; }
  else { sb.addEventListener('click', function (e) { e.stopPropagation(); sndSet(!snd); }); $('snd2').addEventListener('click', function (e) { e.stopPropagation(); sndSet(!snd); showUI(); }); sndSet(true); }
  $('begin').addEventListener('click', function () { if (ready) begin(); });
  $('pp').addEventListener('click', function (e) { e.stopPropagation(); setPlaying(!playing); showUI(); });
  $('stage').addEventListener('click', function (e) { if (mode !== 'film' || (e.target.closest && e.target.closest('button,a'))) return; if (d.documentElement.classList.contains('ui') || !playing) { setPlaying(!playing); } showUI(); });
  $('replay').addEventListener('click', function (e) { e.stopPropagation(); d.documentElement.classList.remove('ended'); F.seek(0); setPlaying(true); });
  d.addEventListener('keydown', function (e) {
    if (mode !== 'film') return;
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); setPlaying(!playing); showUI(); }
    else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { var ch = D.chapters, i, cur = 0; for (i = 0; i < ch.length; i++) if (ch[i].t <= t + .01) cur = i; var to = e.key === 'ArrowRight' ? ch[Math.min(ch.length - 1, cur + 1)].t : ch[Math.max(0, t - ch[cur].t > 2 ? cur : cur - 1)].t; F.seek(to); showUI(); go(); }
  });
  d.addEventListener('visibilitychange', function () { if (d.hidden) { if (playing) { setPlaying(false); F._auto = true; } } else { lastNow = now(); if (F._auto) { F._auto = false; setPlaying(true); } go(); } });
  var rz = 0; addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { if (layout()) { dirty = true; go(); if (F.capture) render(F.time() < 0 ? -1 : t); } }, 120); });
  if (/[?&]hud/.test(location.search)) { var hud = $('hud'); hud.hidden = false; setInterval(function () { var s = F.state(); hud.textContent = 't ' + s.t + '  ' + s.fps + ' fps  p95 ' + s.p95 + ' ms\ntier ' + s.tier + '  dpr ' + s.dpr + '  hdr ' + (s.hdr ? 1 : 0) + '\ngpu ' + s.allocMB + ' MB (peak ' + s.peakMB + ')\ndrift ' + s.drift + ' ms  drops ' + s.drops + '  lost ' + s.ctxLost + '\n' + s.tiers.map(function (x) { return x.at + 's>' + x.tier; }).join(' '); }, 500); }
  d.documentElement.setAttribute('data-mode', 'entry');
  lastNow = now(); F.shots.tau = 0; render(-1); go();
  F.booted = true;
}
F.RM = RM;
F.boot = boot;
})();
