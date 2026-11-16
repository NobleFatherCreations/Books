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
'uniform float uOrigA,uCoreA,uLogoA,uEmbA,uWords,uReveal,uFront,uTitle,uSpin,uDim,uOrigK,uRingDim;uniform vec2 uOrigP;uniform vec4 uRing;',
'uniform vec3 uLight;uniform vec4 uOrb;uniform float uMotes,uGlint,uStars,uDust,uStreak,uHole,uRingS,uPoolR,uPoolK;',
'in vec2 v;out vec4 o;',
'const float FR[8]=float[8](.207,.296,.38,.462,.547,.624,.713,.829);',
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
'  float rv=smoothstep(uReveal+.012,uReveal-.012,length(p-uOrigP));float hole=max(uTitle,smoothstep(uHole*.82,uHole,length(p-uOrigP)));vec3 sky=col;float px=1./(uUnit*uZoom);vec3 gold=vec3(1.,.80,.42);',
'  if(uEmbA>0.||uLogoA>0.){vec2 pl=p;float rl=length(pl)/3.2;',
'    if(uEmbA>0.){vec4 a=art(tEmb,pl,3.2,uSpin)*uEmbA;col=col*(1.-a.a)+a.rgb;}',
'    if(uLogoA>0.){float wm=smoothstep(uWords+.03,uWords-.03,rl);vec4 a=art(tLogo,pl,3.2,uSpin)*uLogoA*wm;col=col*(1.-a.a)+a.rgb;}}',
'  if(uRing.x>0.){float an=atan(p.x,p.y);float st=.20943951;float idx=floor(an/st+.5);float ii=mod(idx+30.,30.);',
'    if(ii>.5){float ia=idx*st;vec2 pl=rot(ia)*(rot(-ia)*p-vec2(0.,uRing.y));float vis=clamp(uRing.z-ii,0.,1.);float dh=abs(ii-uRing.w);dh=min(dh,30.-dh);float hi=smoothstep(1.15,0.,dh);',
'      vec4 a=art(tOrig,pl,1.,0.)*uRing.x*vis;a.rgb*=mix(uRingDim,1.,hi);col=col*(1.-a.a)+a.rgb;',
'      float e=(length(pl)-.887)/(px*2.5+.025);col+=gold*exp(-e*e)*hi*vis*uRing.x*.8;}}',
'  if(uOrigA>0.){vec4 a=art(tOrig,p-uOrigP,1.,0.)*uOrigA*rv;a.rgb*=uOrigK;col=col*(1.-a.a)+a.rgb;',
'    if(uRing.x>0.){float dh=min(abs(uRing.w),30.-abs(uRing.w));float e=(length(p-uOrigP)-.887)/(px*2.5+.025);col+=gold*exp(-e*e)*smoothstep(1.15,0.,dh)*uRing.x*.8;}}',
'  if(uCoreA>0.){vec4 a=art(tCore,p-uOrigP,.7,0.);a.a=1.;a*=uCoreA*rv*smoothstep(.7,.66,max(abs(p.x-uOrigP.x),abs(p.y-uOrigP.y)));col=col*(1.-a.a)+a.rgb;}',

'  col=mix(mix(sky,vec3(.012,.014,.022),min(1.,uOrigA+uLogoA+uEmbA)),col,hole);',
'  if(uPoolK>0.)col*=mix(1.-uPoolK,1.,smoothstep(uPoolR*.35,uPoolR,length(q)));',
'  col*=uDim;',
'  if(uFront>0.){float dF=(r-uReveal)/(px*2.2);col+=gold*(exp(-dF*dF)*.85+exp(-dF*dF/60.)*.16)*uFront;}',
'  if(uGlint>0.){vec2 L=uOrb.y*vec2(cos(uOrb.x),sin(uOrb.x));float g=0.;',
'    for(int i=0;i<8;i++){float dd=(r-FR[i]*uRingS)/(px*1.6);g+=exp(-dd*dd)+exp(-dd*dd/40.)*.22;}',
'    float dl=length(p-L);col+=gold*g*uGlint*(uOrb.z/(1.+dl*dl*46.)+uLight.z*.05/(1.+r*r*9.));',
'    float od=dl/(uOrb.w*px*6.);col+=vec3(1.,.93,.78)*uOrb.z*uGlint*(exp(-od*od)*1.5+.28/(1.+od*od*.9));}',
'  if(uLight.z>0.){vec2 dv=q-uLS;float dl=length(dv)/uLight.y;float an=atan(dv.y,dv.x);',
'    float cor=vn(vec2(an*2.2+uPT*.07,dl*.9-uPT*.22))*.6+vn(vec2(an*5.+3.-uPT*.05,dl*2.1-uPT*.4))*.4;',
'    float spk=pow(abs(cos(an*3.+uPT*.03)),90.)*.5+pow(abs(cos(an*2.-uPT*.021+.7)),140.)*.35;',
'    col+=vec3(1.,.97,.9)*uLight.z*exp(-dl*dl*7.)*2.6+vec3(1.,.82,.5)*uLight.z*(.55/pow(1.+dl*dl*1.2,1.7))*(.62+.76*cor)+vec3(1.,.9,.7)*uLight.z*spk/(1.+dl*dl*.5)*.5;',
'    if(uMotes!=0.){float lr=log(length(dv)+1e-4);vec2 mp=vec2(an*2.86,lr*3.2+uPT*.085*sign(uMotes));float m=0.;',
'      for(int i=0;i<2;i++){vec2 g=mp*(i==0?vec2(3.,2.):vec2(5.,3.1))+float(i)*7.3,id=floor(g),f=fract(g)-.5;id.x=mod(id.x,i==0?18.:29.);float n=h21(id+float(i)*3.1);',
'        if(n>.55){vec2 off=(vec2(h21(id+1.7),h21(id+5.3))-.5)*.6;float dd=length((f-off)*vec2(1.,.55));m+=smoothstep(.07,0.,dd)*(n-.55)*2.2*(.5+.5*sin(uPT*(1.+3.*n)+n*40.));}}',
'      col+=vec3(1.,.86,.6)*m*abs(uMotes)*smoothstep(.0,.25,length(dv))*smoothstep(2.6,.5,length(dv))*.9;}}',
'  o=vec4(col,1.);}'].join('\n');
var FS_BRIGHT = COMMON + 'uniform sampler2D t;uniform vec2 px;uniform float thr;in vec2 v;out vec4 o;void main(){vec3 c=(texture(t,v+px*vec2(-.5,-.5)).rgb+texture(t,v+px*vec2(.5,-.5)).rgb+texture(t,v+px*vec2(-.5,.5)).rgb+texture(t,v+px*vec2(.5,.5)).rgb)*.25;float l=max(c.r,max(c.g,c.b));o=vec4(c*smoothstep(thr,thr+.35,l),1.);}';
var FS_DOWN = COMMON + 'uniform sampler2D t;uniform vec2 px;in vec2 v;out vec4 o;void main(){o=(texture(t,v+px*vec2(-1,-1))+texture(t,v+px*vec2(1,-1))+texture(t,v+px*vec2(-1,1))+texture(t,v+px*vec2(1,1)))*.25;}';
var FS_UP = COMMON + 'uniform sampler2D t,b;uniform vec2 px;in vec2 v;out vec4 o;void main(){vec4 s=(texture(t,v+px*vec2(-1,-1))+texture(t,v+px*vec2(1,-1))+texture(t,v+px*vec2(-1,1))+texture(t,v+px*vec2(1,1))+texture(t,v+px*vec2(0,1.5))+texture(t,v+px*vec2(0,-1.5))+texture(t,v+px*vec2(1.5,0))+texture(t,v+px*vec2(-1.5,0)))*.125;o=s+texture(b,v);}';
var FS_FIN = COMMON + [
'uniform sampler2D tS,tB;uniform vec2 uRes,uLUV,uRipC;uniform float uT,uBloom,uRays,uCA,uVig,uGrain,uExpo,uRipR,uRipA,uAsp,uFade;uniform int uN;',
'in vec2 v;out vec4 o;',
'void main(){vec2 uv=v;',
'  if(uRipA>0.){vec2 dv=(uv-uRipC)*vec2(uAsp,1.);float dl=length(dv);float k=(dl-uRipR)/.05;uv+=normalize(dv+1e-5)/vec2(uAsp,1.)*exp(-k*k)*k*uRipA;}',
'  vec2 dc=uv-.5;vec3 c;',
'  if(uCA>0.){c=vec3(texture(tS,uv+dc*uCA).r,texture(tS,uv).g,texture(tS,uv-dc*uCA).b);}else c=texture(tS,uv).rgb;',
'  vec3 b=texture(tB,uv).rgb;c+=b*uBloom;',
'  if(uN>0&&uRays>0.){vec3 a=vec3(0.);vec2 st=(uv-uLUV)/float(uN)*.82;vec2 pp=uv;float w=1.;float j=h21(gl_FragCoord.xy+fract(uT)*61.);pp-=st*j;',
'    for(int i=0;i<uN;i++){pp-=st;a+=texture(tB,pp).rgb*w;w*=.94;}c+=a/float(uN)*uRays*2.2;}',
'  c*=uExpo;c=mix(c,.72+.28*(1.-exp(-(c-.72)/.28)),step(.72,c));',
'  float vg=1.-uVig*smoothstep(.25,1.05,length(dc*vec2(uAsp>1.?1.:uAsp*1.4,uAsp>1.?1./uAsp*1.4:1.))*1.25);c*=vg;',
'  float fr=floor(uT*24.);float g=h21(gl_FragCoord.xy*.71+fr*17.3)-.5;c+=g*uGrain*(.4+.6*(1.-dot(c,vec3(.333))));',
'  c*=uFade;',
'  float dth=(h21(gl_FragCoord.xy+3.1)+h21(gl_FragCoord.xy+7.7)-1.)/255.;',
'  o=vec4(max(c+dth,0.),1.);}'].join('\n');
var VS_TXT = '#version 300 es\nin vec2 a;in vec4 iR;in vec4 iU;in vec4 iC;in vec2 iX;uniform vec2 uRes;out vec2 v;out vec4 c;out float soft;void main(){vec2 q=a*.5+.5;vec2 lp=(q-.5)*iR.zw;float cs=cos(iX.y),sn=sin(iX.y);lp=vec2(lp.x*cs-lp.y*sn,lp.x*sn+lp.y*cs);vec2 p=iR.xy+lp;v=mix(iU.xy,iU.zw,q);c=iC;soft=iX.x;gl_Position=vec4(p/uRes*2.-1.,0.,1.);gl_Position.y=-gl_Position.y;}';
var FS_TXT = '#version 300 es\nprecision highp float;uniform sampler2D t;uniform float uRange;in vec2 v;in vec4 c;in float soft;out vec4 o;float med(vec3 s){return max(min(s.r,s.g),min(max(s.r,s.g),s.b));}void main(){vec3 s=texture(t,v).rgb;float sd=med(s)-.5;vec2 ts=vec2(textureSize(t,0));float spr=max(.5*dot(vec2(uRange)/ts,1./fwidth(v)),1.);float a=clamp(sd*spr/(1.+soft*spr*.9)+.5,0.,1.);a*=1./(1.+soft*1.4);o=vec4(c.rgb*c.a*a,c.a*a);}';

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
  var k; for (k in TX) if (k !== 'font' && need.indexOf(k) < 0) { gl.deleteTexture(TX[k]); delete TX[k]; txBytes -= IMG[k].bytes; account(); }
  for (var i = 0; i < need.length; i++) { k = need[i]; if (!TX[k]) { if (IMG[k] && IMG[k].ok) upload(k); else if (!IMG[k]) load(k); } }
}
var blank = null;
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
var fxo = { dx: 0, dy: 0, a: 1, s: 1, soft: 0 };
function text(str, x, y, size, col, opt) {
  opt = opt || {};
  var sp = shape(str), k = size / FONT.size, tr = opt.track || 0, n = sp.g.length, i, g, gx, gy, w, h, o;
  var tw = sp.w * k + tr * (str.length - 1), al = opt.align == null ? 0 : opt.align;
  var x0 = x - (al === 0 ? tw / 2 : al > 0 ? tw : 0), rot = opt.rot || 0, cs = Math.cos(rot), sn = Math.sin(rot), a = TXT.data, q;
  for (i = 0; i < n; i++) {
    if (TXT.n >= TXT.max) return tw;
    g = sp.g[i]; w = g[4] * k; h = g[5] * k;
    gx = x0 + g[0] * k + tr * g[6] + w / 2 - x; gy = (g[1] - FONT.base) * k + h / 2;
    fxo.dx = 0; fxo.dy = 0; fxo.a = 1; fxo.s = 1; fxo.soft = 0; if (opt.fx) opt.fx(i, n, fxo, gx, gy);
    if (fxo.a <= .003) continue;
    q = TXT.n * 14;
    a[q] = (x + gx * cs - gy * sn + fxo.dx) * DPR; a[q + 1] = (y + gx * sn + gy * cs + fxo.dy) * DPR; a[q + 2] = w * fxo.s * DPR; a[q + 3] = h * fxo.s * DPR;
    a[q + 4] = g[2] / FONT.w; a[q + 5] = g[3] / FONT.h; a[q + 6] = (g[2] + g[4]) / FONT.w; a[q + 7] = (g[3] + g[5]) / FONT.h;
    a[q + 8] = col[0]; a[q + 9] = col[1]; a[q + 10] = col[2]; a[q + 11] = col[3] * fxo.a;
    a[q + 12] = (opt.soft || 0) + fxo.soft; a[q + 13] = rot;
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
function drawText() {
  if (!TXT.n || !TX.font) return;
  gl.useProgram(P.txt.p); gl.uniform2f(P.txt.u.uRes, cv.width, cv.height); gl.uniform1f(P.txt.u.uRange, FONT.range);
  gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, TX.font); gl.uniform1i(P.txt.u.t, 0);
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
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
var S = F.S = {};                           // the frame state, filled by shots.js
function render(t) {
  S = F.S = F.shots.state(t, S);            // pure: t -> state
  TXT.n = 0; F.shots.draw(t, S);            // pure: pushes text for this frame
  captions(t);
  if (!gl) return fallback2d(S);
  keep(F.shots.need(t));
  var T = TIERS[tier], u, i, cx = cv.width * S.cxf, cy = cv.height * (1 - CYF), unit = U * DPR;
  pass(P.scene, RT.scene); u = P.scene.u;
  gl.uniform2f(u.uRes, cv.width, cv.height); gl.uniform2f(u.uCtr, cx, cy); gl.uniform1f(u.uUnit, unit);
  gl.uniform1f(u.uZoom, S.zoom); gl.uniform1f(u.uRot, S.rot); gl.uniform2f(u.uCam, S.camx, S.camy);
  gl.uniform1f(u.uT, t); gl.uniform1f(u.uPT, S.pt);
  gl.uniform2f(u.uOrigP, S.origx, S.origy); gl.uniform1f(u.uOrigK, S.origk); gl.uniform4f(u.uRing, S.ringa, S.ringr, S.ringn, S.ringhi); gl.uniform1f(u.uRingDim, S.ringdim);
  gl.uniform1f(u.uOrigA, S.orig); gl.uniform1f(u.uCoreA, S.core); gl.uniform1f(u.uLogoA, S.logo); gl.uniform1f(u.uEmbA, S.emb);
  gl.uniform1f(u.uWords, S.words); gl.uniform1f(u.uReveal, S.reveal); gl.uniform1f(u.uFront, S.front); gl.uniform1f(u.uTitle, S.title);
  gl.uniform1f(u.uSpin, S.spin); gl.uniform1f(u.uDim, S.dim);
  gl.uniform3f(u.uLight, 0, S.lsize, S.light); gl.uniform2f(u.uLS, S.lx, S.ly);
  gl.uniform4f(u.uOrb, S.orba, S.orbr, S.orb, 1); gl.uniform1f(u.uGlint, S.glint);
  gl.uniform1f(u.uMotes, S.motes); gl.uniform1f(u.uHole, S.hole); gl.uniform1f(u.uRingS, S.rings); gl.uniform1f(u.uPoolR, S.poolr); gl.uniform1f(u.uPoolK, S.poolg);
  gl.uniform1f(u.uStars, S.stars); gl.uniform1f(u.uDust, T.dust ? S.dust : 0); gl.uniform1f(u.uStreak, S.streak);
  bind(0, 'orig'); gl.uniform1i(u.tOrig, 0); bind(1, 'core'); gl.uniform1i(u.tCore, 1); bind(2, 'logo'); gl.uniform1i(u.tLogo, 2); bind(3, 'emb'); gl.uniform1i(u.tEmb, 3);
  fs();
  drawText();
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
  gl.uniform2f(u.uRes, cv.width, cv.height); gl.uniform1f(u.uT, t); gl.uniform1f(u.uAsp, cv.width / cv.height);
  gl.uniform2f(u.uLUV, S.cxf + S.lx * unit / cv.width, (cy + S.ly * unit) / cv.height);
  gl.uniform1f(u.uBloom, S.bloom); gl.uniform1f(u.uRays, S.rays); gl.uniform1i(u.uN, T.rays);
  gl.uniform1f(u.uCA, S.ca); gl.uniform1f(u.uVig, S.vig); gl.uniform1f(u.uGrain, S.grain); gl.uniform1f(u.uExpo, S.expo); gl.uniform1f(u.uFade, S.fade);
  gl.uniform2f(u.uRipC, S.cxf + S.ripx * unit / cv.width, (cy + S.ripy * unit) / cv.height); gl.uniform1f(u.uRipR, S.ripr * unit / cv.height); gl.uniform1f(u.uRipA, S.ripa);
  fs();
}
/* plain 2D picture for browsers with no WebGL2: art, camera and light only */
var c2 = null;
function fallback2d(S) {
  if (!c2) { c2 = cv.getContext('2d'); if (!c2) return; }
  var cx = W * S.cxf * DPR, cy = H * CYF * DPR, k = U * DPR * S.zoom;
  c2.setTransform(1, 0, 0, 1, 0, 0); c2.fillStyle = '#05070d'; c2.fillRect(0, 0, cv.width, cv.height);
  function put(key, hs, al) { var m = IMG[key]; if (!m || !m.ok || al <= .01) return; c2.globalAlpha = al * S.dim * S.fade; c2.save(); c2.translate(cx - S.camx * k, cy + S.camy * k); c2.rotate(-S.rot); c2.drawImage(m.el, -hs * k, -hs * k, 2 * hs * k, 2 * hs * k); c2.restore(); }
  put('emb', 3.2, S.emb); put('logo', 3.2, S.logo); put('orig', 1, S.orig * (S.reveal >= 1 ? 1 : 0));
  if (S.light > 0) { c2.globalAlpha = Math.min(1, S.light) * S.fade; var lx = cx + S.lx * U * DPR, ly = cy - S.ly * U * DPR, r = S.lsize * U * DPR * 2.4, g = c2.createRadialGradient(lx, ly, 0, lx, ly, r); g.addColorStop(0, 'rgba(255,246,226,1)'); g.addColorStop(.18, 'rgba(255,214,140,.55)'); g.addColorStop(1, 'rgba(255,200,120,0)'); c2.fillStyle = g; c2.fillRect(lx - r, ly - r, 2 * r, 2 * r); }
  c2.globalAlpha = 1;
}

/* ---------- captions: real text, transforms and opacity only ---------- */
var CAPS = D.caps, capEl = [$('capA'), $('capB')], capCur = [-1, -1], pool = $('pool');
function capBuild(el, c) {
  var h = '', i, g = c.g;
  for (i = 0; i < g.length; i++) h += '<span class="g">' + g[i] + '</span>' + (i < g.length - 1 ? ' ' : '');
  el.innerHTML = h; el.className = 'cap' + (c.big ? ' big' : '') + (c.long ? ' long' : '');
  el._g = el.querySelectorAll('.g');
}
function captions(t) {
  var i, c, slot, shown = [false, false], best = 0;
  for (i = 0; i < CAPS.length; i++) {
    c = CAPS[i]; if (t < c.t0 - .05 || t > c.t1 + c.out) continue;
    slot = i % 2; shown[slot] = true;
    var el = capEl[slot]; if (capCur[slot] !== i) { capBuild(el, c); capCur[slot] = i; }
    var age = t - c.t0, left = c.t1 + c.out - t, o = 1, y = 0, sc = 1, n = el._g.length, k, gi, ge;
    if (left < c.out) { var e = 1 - left / c.out; e = E.in2(e); o = 1 - e; y = -34 * e; sc = 1 - .05 * e; }
    el.style.opacity = o.toFixed(3);
    el.style.transform = 'translate3d(-50%,' + (Math.round(y * DPR) / DPR) + 'px,0) scale(' + sc.toFixed(4) + ')';
    var per = Math.min(.5, Math.max(.16, (c.t1 - c.t0) * .5 / n));
    for (k = 0; k < n; k++) { gi = clamp((age - k * per) / .7, 0, 1); ge = E.out3(gi); var s = el._g[k].style; s.opacity = ge.toFixed(3); s.transform = 'translate3d(0,' + (Math.round((1 - ge) * 16 * DPR) / DPR) + 'px,0)'; }
    best = Math.max(best, o * clamp(age / .5, 0, 1));
  }
  for (slot = 0; slot < 2; slot++) if (!shown[slot] && capCur[slot] !== -1) { capEl[slot].style.opacity = 0; capCur[slot] = -1; }
  pool.style.opacity = (best * (S.poolk == null ? 1 : S.poolk)).toFixed(3);
}

/* ---------- clock ---------- */
var mode = 'entry', t = 0, playing = false, lastNow = 0, tau = 0, raf = 0, dirty = true, audio = null;
F.dur = D.dur;
function now() { return performance.now() / 1000; }
function frame() {
  raf = 0; var n = now(), dt = Math.min(.5, n - lastNow); lastNow = n;
  if (mode === 'entry') { tau += dt * (RM ? .25 : 1); F.shots.tau = tau; render(-1); gov(dt); }
  else {
    if (playing) {
      if (audio && !audio.paused) { var at = audio.currentTime; t += dt; var dr = at - t; drift = dr; if (Math.abs(dr) > .04) t = at; else t += dr * .1; }
      else t += dt;
      if (t >= F.dur) { t = F.dur; playing = false; ended(); }
      gov(dt);
    }
    render(t); progress();
  }
  if (mode === 'entry' || playing || dirty) { dirty = false; go(); }
}
function go() { if (!raf && !F.capture && !d.hidden) raf = requestAnimationFrame(frame); }
var drift = 0;
F.seek = function (x) { mode = x < 0 ? 'entry' : 'film'; if (x < 0) { tau = -x; F.shots.tau = tau; render(-1); } else { t = clamp(x, 0, F.dur); if (audio) try { audio.currentTime = t; } catch (e) {} render(t); progress(); } d.documentElement.setAttribute('data-mode', mode); return F.S; };
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
  if (audio) { if (on) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); } else audio.pause(); }
  if (on) { wakeOn(); lastNow = now(); go(); } else wakeOff();
  var b = $('pp'); if (b) { b.setAttribute('aria-label', on ? 'Pause' : 'Play'); b.setAttribute('aria-pressed', on ? 'true' : 'false'); }
}
function begin() {
  if (mode !== 'entry') return;
  F.shots.tau0 = tau; mode = 'film'; t = 0; d.documentElement.setAttribute('data-mode', 'film');
  if (audio) { try { audio.currentTime = 0; } catch (e) {} }
  if (navigator.vibrate) try { navigator.vibrate(12); } catch (e) {}
  setPlaying(true); showUI();
}
function ended() { d.documentElement.classList.add('ended'); wakeOff(); }
function progress() { var p = $('bar'); if (p) p.style.transform = 'scaleX(' + (t / F.dur).toFixed(5) + ')'; }
var uiT = 0;
function showUI() { d.documentElement.classList.add('ui'); clearTimeout(uiT); uiT = setTimeout(function () { if (playing) d.documentElement.classList.remove('ui'); }, 2500); }
F.begin = begin; F.play = function () { setPlaying(true); }; F.pause = function () { setPlaying(false); };
F.state = function () {
  var n = Math.min(ft.length, 600), s = 0, i, a = ft.slice(-n).sort(function (x, y) { return x - y; }); for (i = 0; i < a.length; i++) s += a[i];
  return { mode: mode, t: +F.time().toFixed(3), playing: playing, tier: TIERS[tier].name, dpr: DPR, w: W, h: H, gl: !!gl, hdr: HDR && !!TIERS[tier].hdr,
    fps: n ? +(n / s).toFixed(1) : 0, p95: n ? +(a[Math.floor(n * .95)] * 1000).toFixed(1) : 0, drops: drops, allocMB: +(alloc / 1048576).toFixed(1), peakMB: +(peakAlloc / 1048576).toFixed(1),
    drift: +(drift * 1000).toFixed(1), ctxLost: ctxLost, tiers: tierLog, glyphs: TXT.n, caps: capCur.slice(), ready: ready };
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
  var need = D.first, left = need.length, ring = $('ring');
  function one() { left--; if (ring) ring.style.strokeDashoffset = (ring.getTotalLength ? 283 * left / need.length : 0).toFixed(1); if (left <= 0) { var fin = function () { ready = true; d.documentElement.classList.add('ready'); dirty = true; if (F.capture) render(F.time() < 0 ? -1 : t); go(); }; if (d.fonts && d.fonts.ready) Promise.all([d.fonts.load('1em Voice'), d.fonts.load('1em "Source Serif"'), d.fonts.ready]).then(fin, fin); else fin(); } }
  need.forEach(function (k) { load(k, one); });
  setTimeout(function () { D.later.forEach(function (k) { load(k); }); }, 1500);
  if (D.audio) { audio = new Audio(); audio.preload = 'auto'; audio.src = D.audio; }
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
