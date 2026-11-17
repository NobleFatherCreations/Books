/* Fractal² film: the timeline. state(t) and draw(t) are pure functions of time.
   Times come from caption anchors (C('slug').t0), so re-timing the captions from a recorded voice moves the picture with it. */
(function () {
'use strict';
var F = window.FILM, D = F.data, E = F.ease, track = F.track, clamp = F.clamp, lerp = F.lerp, sm = F.sm, TAU = Math.PI * 2;
var FRr = [.207, .296, .38, .462, .547, .624, .713, .84];
F.COL = .595;                                  // left edge of the caption column on wide screens (template: left 78%, width 37vw)
function C(slug) { var i = D.capId[slug]; if (i == null) throw new Error('no caption ' + slug); return D.caps[i]; }
function h1(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

/* placeholder envelopes until the baked audio track exists: same shape the real ones will have */
function voice(t) {
  var c = D.caps, i, v = 0;
  for (i = 0; i < c.length; i++) if (t >= c[i].t0 && t <= c[i].t0 + c[i].say) { var u = (t - c[i].t0), e = Math.min(1, u / .12) * Math.min(1, (c[i].t0 + c[i].say - t) / .25); v = e * (.55 + .45 * Math.sin(t * 9.1) * Math.sin(t * 5.3 + 1)); break; }
  return Math.max(0, v);
}
function sub(t) { if (t < 25.6) return 0; var ph = (t % 1.6) / 1.6; return Math.exp(-ph * 7) * clamp((t - 25.6) / 12, 0, 1); }
F.env = D.env ? function (t, ch) { var a = D.env[ch], i = clamp(Math.round(t * D.env.fps), 0, a.length - 1); return a[i] / 255; } : function (t, ch) { return ch === 'voice' ? voice(t) : ch === 'sub' ? sub(t) : .3; };

/* ---------- section anchors ---------- */
var c1 = C('it-started-with-a'), cdr = C('a-different-room-a'), cq = C('why-do-i-keep'), cme = C('it-must-be-me'), cwi = C('what-if-it-isnt'),
  c2 = C('i-wrote-it-down'), c8 = C('it-came-in-eight'), st = ['idealize', 'hook', 'devalue', 'confuse', 'isolate', 'extract', 'discard', 'replace'].map(C),
  c30 = C('thirty-techniques-carried-a'), cth = C('i-thought-i-had'), crm = C('i-had-only-found');
var T1 = 3.3, TOURZ = 1.9;
/* section 3: thirty rooms in a circle around the light */
var RW = 10.5, SECT = D.sectors, g1 = C('so-i-went-looking'), g2 = C('i-opened-a-second'), g3 = C('a-third-and-it'), g6 = C('religion-politics-media-education'), gk = C('i-kept-walking-until'),
  gm = C('from-the-moment-you'), g27 = C('two-thousand-seven-hundred'), gl1 = C('i-looked-for-a'), gs = C('i-am-still-looking'), SIX = ['Religion', 'Politics', 'Media', 'Education', 'Medicine', 'Money'];
var relT = []; (function () { var t = gm.t0 + .2, span = g27.t0 - .5 - t, w = [], i, sum = 0; for (i = 0; i < 30; i++) { w.push(i < 4 ? 2.6 : i < 8 ? 1.5 : 1); sum += w[i]; } for (i = 0; i < 30; i++) { var dd = w[i] / sum * span; relT.push([t, dd]); t += dd; } })();                              // end of launch: black, one light

/* section 1: the light walks the same loop, lap after lap (a different room, a different face, the same ending).
   Every lap passes through one point P. At "It must be me" it stops there; "I turned the question around" is one lap the other way;
   at "What if it isn't me?" every lap it ever walked lights at once, and the road opens back to the centre. */
var LAPV = [0, .09, -.07, .12, -.04, .05], LAPT = [0, .14, -.1, .2, -.16, .06], LAPS = [], ROAD0 = C('that-was-the-moment').t0 + .3, ROAD1 = c2.t0 - .5;
(function () { var e = [9.6, cq.t0 + .8, cdr.t0 + 3.6, 44.2, 57.0, cme.t0], i; for (i = 0; i < 5; i++) LAPS.push([e[i], e[i + 1], 1]); LAPS.push([cme.t0 + 4.3, cwi.t0, -1]); })();
function lapR() { return F.dims().PORT ? .55 : .5; }
function lapGeo(k) { var R = lapR(), r = R * (1 + LAPV[k]), ta = LAPT[k]; return [r * Math.sin(ta), -R + r * Math.cos(ta), r, ta]; }
function lapF(u) { u = clamp(u, 0, 1); return u - .35 * Math.sin(TAU * u) / TAU; }
function lapPos(k, f) { var g = lapGeo(k), th = -Math.PI / 2 - g[3] + LAPS[k][2] * TAU * f; return [g[0] + g[2] * Math.cos(th), g[1] + g[2] * Math.sin(th)]; }
function path1(t) {                           // where the one light is in section 1 (screen units from the picture centre)
  var R = lapR(), k;
  if (t < LAPS[0][0]) { var u = E.io((t - 3.6) / (LAPS[0][0] - 3.6)); return [0, -R * u]; }
  for (k = 0; k < 6; k++) if (t < LAPS[k][1]) return t < LAPS[k][0] ? [0, -R] : lapPos(k, lapF((t - LAPS[k][0]) / (LAPS[k][1] - LAPS[k][0])));
  var v = E.film((t - ROAD0) / (ROAD1 - ROAD0)); return [0, -R * (1 - v)];
}
function trail1(t, S) {
  var A = S.tra = shots._tra || (shots._tra = new Float32Array(24)), B = S.trb = shots._trb || (shots._trb = new Float32Array(24)), k;
  var see = sm((t - cwi.t0 - .1) / .5), dimm = 1 - .75 * sm((t - cme.t0 - .2) / 1.4) * (1 - sm((t - cme.t0 - 4.3) / 2)), gone = 1 - sm((t - ROAD0 - 1.2) / 4);
  for (k = 0; k < 6; k++) {
    var L = LAPS[k], g = lapGeo(k), f = t <= L[0] ? 0 : lapF((t - L[0]) / (L[1] - L[0])), age = Math.max(0, t - L[1]);
    var base = (k === 5 ? .36 : .3) * (1 - .35 * sm(age / 30)) * (k < 5 ? dimm : 1);
    A[k * 4] = g[0]; A[k * 4 + 1] = g[1]; A[k * 4 + 2] = g[2]; A[k * 4 + 3] = f > 0 ? lerp(base, .62 + .5 * Math.exp(-Math.max(0, t - cwi.t0 - .6) * 1.2), see) * gone : 0;
    B[k * 4] = f; B[k * 4 + 1] = L[2]; B[k * 4 + 2] = t < L[1] ? 9 : 400; B[k * 4 + 3] = g[3];
  }
}
/* ---------- tracks ---------- */
var revKeys = [[c2.t0 - .2, .06], [c2.t0 + 3.2, .118, E.film], [c8.t0, .118]], zKeys = [[0, .8], [.35, .8], [3.0, 11, F.bez(.6, 0, .25, 1)], [T1, 11], [T1 + .01, 2.2], [cme.t0, 3.3, E.lin], [cwi.t0 + 2, 3.0, E.io], [c2.t0, 3.5, E.io], [c8.t0, 3.5]];
st.forEach(function (c, i) {
  revKeys.push([c.t0 - .05, i ? FRr[i - 1] : .118]); revKeys.push([c.t0 + 1.05, FRr[i], E.film]);
  var zt = Math.min(3.5, .92 / (FRr[i] + .05) * (i < 7 ? 1 : .98)); zKeys.push([c.t0 - .05, zKeys[zKeys.length - 1][1]]); zKeys.push([c.t0 + 1.25, Math.max(1, zt), E.weight]);
});
revKeys.push([c30.t0, .84]); revKeys.push([c30.t0 + 1.2, .92, E.io]);
zKeys.push([c30.t0 - .3, 1]); zKeys.push([c30.t0 + 2.2, TOURZ, E.film]); zKeys.push([cth.t0 - 1.6, TOURZ]); zKeys.push([cth.t0 + .6, 1, E.film]); zKeys.push([crm.t0 - .2, 1]); zKeys.push([crm.t1 + 1.5, .34, E.film]);
var zoom = track(zKeys, true), reveal = track(revKeys);
var artLogo = track([[0, 1], [1.6, 1], [2.7, 0, E.in2]]);
var spinV = track([[0, 0], [2.6, 5.2, E.in3]]);                         // extra turn during the dive
var orbR = track([[0, 1.216], [.3, 1.216], [2.3, 0, E.in2]]), orbI = track([[0, 1], [2.0, 1.5], [2.6, 0]]);
var orbA = track([[0, 0], [2.6, 11, E.in2]]);
var lightI = track([[1.3, 0], [2.9, .85, E.out3], [cme.t0 - .6, .85], [cme.t0 + 1.4, .34, E.io], [cwi.t0 - .2, .34], [cwi.t0 + 1.6, 1.25, E.weight], [c2.t0, 1.0, E.io], [c8.t0, .9], [st[7].t0 + 1.3, .55, E.io], [c30.t0 + 8, .5], [g1.t0, .5], [g1.t0 + 4, .8, E.io]]);
var lightS = track([[1.3, .03], [3.2, .16, E.out3], [cq.t0 - .3, .16], [cq.t0 + 1.2, .2, E.io], [cme.t0 - .6, .2], [cme.t0 + 1.4, .085, E.io], [cwi.t0 - .2, .085], [cwi.t0 + 1.6, .2, E.weight], [c2.t0 + 3, .15, E.io], [st[7].t0 + 1.3, .085, E.io], [g1.t0, .085], [g1.t0 + 4, .11, E.io]]);
var starsK = track([[0, .5], [2.2, 0], [5.5, 0], [16, .38, E.io], [cme.t0, .42], [cme.t0 + 1.4, .2, E.io], [cwi.t0 + .2, .24], [cwi.t0 + 5, .9, E.out2], [c8.t0, .9], [st[7].t0, .75]]);
var dustK = track([[0, .7], [2.4, 0], [cwi.t0 + .5, 0], [cwi.t0 + 6, .7, E.io]]);
var origA = track([[c2.t0 - .3, 0], [c2.t0, 1]]);
var frontK = track([[c2.t0 - .2, 0], [c2.t0 + .4, 1, E.out2], [st[7].t0 + 1.2, 1], [c30.t0 + 1.4, 0]]);
var glintK = track([[0, 1], [2.4, 1], [2.7, 0], [c2.t0, 0], [c8.t0, .5, E.io], [c30.t0, .5], [c30.t0 + .6, 1.2], [cth.t0, 1.2], [crm.t1 + 2, .6]]);
var sweepA = track([[c30.t0, 1.2], [cth.t0 - .3, 1.2 + TAU * 1.5, F.bez(.3, 0, .3, 1)]]);
var sweepU = track([[c30.t0, 0], [cth.t0 - .3, 1, E.lin]]);
function sweepR(t) { var u = sweepU(t) * 7.999, k = Math.floor(u), f = sm((u - k - .72) / .28); return lerp(FRr[k], FRr[Math.min(7, k + 1)], f); }
var sweepI = track([[c30.t0 - .2, 0], [c30.t0 + .5, .8], [cth.t0 - .8, .8], [cth.t0, 0]]);
var raysK = track([[0, 0], [2.4, 0], [3.4, .55], [cme.t0 + 1.4, .2, E.io], [cwi.t0 + 1.6, .9, E.out2], [c2.t0 + 2, .5, E.io], [st[7].t0, .3]]);
var poolG = track([[0, .93], [1.2, 0, E.out2]]);
var rip = track([[0, 0], [1.5, 3.4, E.outExpo]]), ripA = track([[0, .05], [1.5, 0, E.out2]]);
var vigK = track([[0, .62], [3, .5], [c2.t0, .5], [st[7].t0, .42]]);
var motesK = track([[3, 0], [7, -.8, E.io], [cme.t0, -.8], [cme.t0 + 1.5, -.25, E.io], [cwi.t0, -.25], [cwi.t0 + .4, 0], [cwi.t0 + 1.4, 1, E.out2], [c2.t0 + 4, .7], [st[0].t0, .25, E.io], [c30.t0, .25]]);
var follow = track([[c30.t0 - .3, 0], [c30.t0 + 2.2, .78, E.film], [cth.t0 - 1.6, .78], [cth.t0 + .6, 0, E.film]]);
var cxfK = track([[T1 - .3, 0], [9, 1, E.io]]);
var push = track([[9, 1], [cme.t0 - 1, 1.42, E.lin], [cme.t0 + 1.4, 1], [c2.t0, 1]]);
var ringY = track([[g1.t0 - .2, 0], [g1.t0 + 4.6, RW, E.film]]);
var ringN = track([[g2.t0 + 1.5, 1], [g2.t0 + 2.1, 2, E.out2], [g3.t0 + .5, 2], [g3.t0 + 1.1, 3, E.out2], [g6.t0, 3], [g6.t0 + g6.say, 6, E.lin], [gk.t0 + .3, 6], [gk.t0 + 6.6, 30, E.io]]);
var ringA = track([[g2.t0 + 1.3, 0], [g2.t0 + 1.6, 1]]);
function ZF() { var d = F.dims(); return (d.PORT ? .97 : .9) / (RW + .9); }
function cam3(t) {                            // camera: stay with the first room, pan with each door, then show the whole circle
  var zf = ZF(), a = [[g1.t0 - .2, .34, 0, 0], [g1.t0 + 4.6, .25, 0, 6.4], [g2.t0 + 1.2, .25, 0, 6.4], [g2.t0 + 3, .23, 1.2, 6.6], [g3.t0 + .4, .23, 1.2, 6.6], [g3.t0 + 2.2, .2, 2.4, 6.4], [g6.t0, .2, 2.4, 6.4], [g6.t0 + g6.say + .6, .125, 4.6, 5.2], [gk.t0 + .4, .125, 4.6, 5.2], [gk.t0 + 6.8, zf, 0, 0], [gs.t1 + 9, zf * 1.06, 0, 0]], i;
  if (t <= a[0][0]) return a[0]; for (i = 1; i < a.length; i++) if (t < a[i][0]) break; if (i >= a.length) return a[a.length - 1];
  var u = E.film((t - a[i - 1][0]) / (a[i][0] - a[i - 1][0])); return [0, Math.exp(lerp(Math.log(a[i - 1][1]), Math.log(a[i][1]), u)), lerp(a[i - 1][2], a[i][2], u), lerp(a[i - 1][3], a[i][3], u)];
}
function hi3(t) {
  if (t >= gl1.t0) { var u = (t - gl1.t0) / (gs.t1 - gl1.t0); return (u < .62 ? E.io(u / .62) * 30 : 30 + (u - .62) / .38 * 9) % 30; }
  if (t >= g27.t0 - .5) return -9;
  if (t >= relT[0][0]) { for (var i = 29; i >= 0; i--) if (t >= relT[i][0]) return i + sm((t - relT[i][0] - relT[i][1] + .25) / .25) * (i < 29 ? 1 : 0); }
  if (t >= gk.t0 + .3) return ringN(t) - 1;
  if (t >= g6.t0) return Math.min(5, Math.floor((t - g6.t0) / g6.say * 6));
  if (t >= g3.t0 + .5) return 2; if (t >= g2.t0 + 1.5) return 1; return 0;
}
/* sections 4 and 5: the full stop, the mirror, the great pull-back, three nested scales */
var g4 = C('then-the-map-turned'), m1 = C('i-found-the-cycle'), m2 = D.caps[D.capId['i-found-the-cycle'] + 1], m3 = D.caps[D.capId['i-found-the-cycle'] + 2], m4 = C('handed-down-not-out'), m5 = C('i-came-to-believe'),
  m6 = C('the-enemy-i-had'), m7 = C('and-it-had-never'), m8 = C('it-had-been-handed'), a1 = C('that-is-when-i'), a2 = C('it-was-never-only'), a5 = C('the-pattern-wears-a'), a6 = C('it-wears-the-sky'),
  n1 = C('the-person-is-inside'), n2 = C('the-institution-is-inside'), n3 = C('the-civilization-is-inside'), n4 = C('and-the-pattern-is'), n5 = C('that-is-the-fractal');
var STOP = g4.t0 + 3.4, PK1 = D.marks.PEAK1, PATR = 13.4, LS5 = 8.2, LR5 = 7.27;
function lost(t) {                            // time the particles and the camera's breath lose to the full stop (closed form)
  var A = STOP - .6, B = STOP, Cc = STOP + 1.4, Dd = STOP + 3.4;
  if (t <= A) return 0; if (t <= B) return (t - A) * (t - A) / (2 * (B - A)); if (t <= Cc) return .3 + (t - B);
  if (t <= Dd) return 1.7 + (t - Cc) - (t - Cc) * (t - Cc) / (2 * (Dd - Cc)); return 2.7;
}
function keysAt(K, t) {
  var i; if (t <= K[0][0]) return K[0]; for (i = 1; i < K.length; i++) if (t < K[i][0]) break; if (i >= K.length) return K[K.length - 1];
  var a = K[i - 1], b = K[i], u = (b[5] || E.film)((t - a[0]) / (b[0] - a[0]));
  return [0, Math.exp(lerp(Math.log(a[1]), Math.log(b[1]), u)), lerp(a[2], b[2], u), lerp(a[3], b[3], u), lerp(a[4], b[4], u)];
}
var K45 = null, K45key = '';
function cam45(t) {
  var d = F.dims(), key = d.W + 'x' + d.H;
  if (key !== K45key) {
    var zf = ZF(), z0 = cam3(g4.t0)[1], zP = d.PORT ? .62 : .6, zI = d.PORT ? .112 : .125, zPat = zf * .8, e = a5.t0, R = -TAU;
    K45 = [[g4.t0, z0, 0, 0, 0], [STOP, z0 * 1.04, 0, 0, 0, E.in2], [STOP + 1.3, z0 * 1.037, 0, 0, 0, E.settle], [m1.t0 + 9.5, .55, 0, 0, 0, E.film], [m2.t1, .8, 0, 0, 0, E.lin],
      [m3.t0 + 5.6, .3, -1.5, 2.3, 0, E.film], [m6.t0, .27, -1.7, 2.6, 0, E.lin], [m6.t0 + 6.4, zf * 1.25, 0, 0, 0, E.film], [a1.t0, zf * 1.3, 0, 0, 0, E.lin],
      [PK1 - .12, 2.4, 0, 0, 0, E.in3], [PK1 + 9.4, zf, 0, 0, R, F.spring(.66, 7.5)], [e - .1, zf * 1.02, 0, 0, R, E.lin],
      [e + 1.5, zP, 0, 0, R, E.film], [e + 2.7, zP, 0, 0, R], [e + 4.3, zI, 0, 0, R, E.film], [a6.t0 - .1, zI, 0, 0, R], [a6.t0 + 1.9, zf, 0, 0, R, E.film], [n1.t0 - .1, zf, 0, 0, R],
      [n1.t0 + 1.5, zI, 0, 0, R, E.film], [n2.t0 - .1, zI, 0, 0, R], [n2.t0 + 1.6, zf, 0, 0, R, E.film], [n3.t0 - .1, zf, 0, 0, R], [n3.t0 + 1.7, zPat, 0, 0, R, E.film], [n4.t0 + .2, zPat, 0, 0, R],
      [n4.t0 + 3.85, 70, 0, 0, R, E.inExpo], [n4.t0 + 3.86, zf * 2.6, 0, 0, R, E.lin], [n5.t0 + 3.4, zf, 0, 0, R, E.out3], [n5.t1 + 8, zf * 1.05, 0, 0, R, E.lin]];
    K45key = key;
  }
  return keysAt(K45, t);
}
var rev4 = track([[STOP + 1.39, 2], [STOP + 1.4, .1], [m1.t0 + 9, .92, E.film], [m7.t0, .92], [m7.t0 + 3, .1, E.io], [PK1 + 3.4, .1], [PK1 + 7, .92, E.out2]]);
var front4 = track([[STOP + 1.4, 0], [STOP + 2, .7], [m1.t0 + 9, .7], [m1.t0 + 10.5, 0], [m7.t0, 0], [m7.t0 + .3, .6], [m7.t0 + 3, 0], [PK1 + 3.4, 0], [PK1 + 3.8, .8], [PK1 + 7.6, 0]]);
var genN = track([[m3.t0 + .4, 0], [m3.t0 + 5.6, 6, E.lin]]), genA = track([[m3.t0 + .3, 0], [m3.t0 + .6, 1], [a1.t0 - 3, 1], [a1.t0, 0, E.io]]);
function genLit(t) { var u = (t - m4.t0 - .2) / 4.6; if (u > 0 && u < 1) return lerp(6.8, -.6, E.io(u)); u = (t - m8.t0 - .1) / 3.2; if (u > 0 && u < 1) return lerp(6.8, -.6, E.io(u)); return -9; }
var ringDim4 = track([[g4.t0, .32], [STOP - .05, .32], [STOP, 1.7], [STOP + 2.6, 1, E.out2], [m6.t0, 1], [m6.t0 + .1, .4], [a1.t0, .4], [PK1 + 4, .4], [PK1 + 8, 1, E.io]]);
var lrev5 = track([[PK1 - .1, 0], [PK1 + 4.6, 1.06, E.out2]]), frontl5 = track([[PK1 - .1, 0], [PK1, 1], [PK1 + 4.5, 1], [PK1 + 5.4, 0]]);
var logoA5 = track([[PK1 - .2, 0], [PK1, 1]]);
var pat5 = track([[n3.t0 + .4, 0], [n3.t0 + 1.8, 1, E.out2], [n4.t0 + 1.2, 1], [n4.t0 + 2.6, 0], [n5.t0 + 1.2, 0], [n5.t0 + 3.2, .8, E.io]]);
var glare = track([[n4.t0 + .6, 0], [n4.t0 + 3.85, 1, E.in3], [n5.t0 + .4, .9], [n5.t0 + 3.4, 0, E.out2]]);
/* section 6: the inversion. tables 3 to 6 and the names */
var i1 = C('i-will-tell-you'), i3 = C('every-stage-is-a'), e1 = C('election-becomes-idealize-covenant'), e2 = C('truth-becomes-confuse-community'), e3 = C('i-will-never-leave'), e4 = C('and-the-one-who'),
  t4 = C('every-technique-is-a'), QL = ['you-are-loved-and', 'you-are-safe-and', 'you-belong-and-then', 'you-are-whole-and', 'come-home-and-then'].map(C), nm = C('people-have-given-it'), u1 = C('use-the-word-that'),
  b1 = C('it-is-not-a'), b2 = C('it-is-a-pattern'), k1 = C('a-counterfeit-always-comes'), k2 = C('which-means-something-real');
var INV = [['Election', 'Idealize'], ['Covenant', 'Hook'], ['Inherent worth', 'Devalue'], ['Truth', 'Confuse'], ['Community', 'Isolate'], ['Abundance', 'Extract'], ['“I will never leave you”', 'Discard'], ['The one who cannot be replaced', 'Replace']];
var invT = []; (function () { var i; for (i = 0; i < 3; i++) invT.push([e1.t0 + (e1.say + .5) * i / 3, (e1.say + .5) / 3]); for (i = 0; i < 3; i++) invT.push([e2.t0 + (e2.say + .5) * i / 3, (e2.say + .5) / 3]); invT.push([e3.t0, e3.say + .6]); invT.push([e4.t0, e4.say + 1]); })();
var PAIRS = D.tables.pairs, IMP = D.tables.impulses, T4a = t4.t0 + t4.say * .62, T4b = QL[0].t0 - .9, T4c = QL[0].t0 - .7, pairT = [];
(function () { var w = [], sum = 0, i, t = T4a; for (i = 0; i < 30; i++) { w.push(i < 3 ? 3.4 : i < 6 ? 1.8 : 1); sum += w[i]; } for (i = 0; i < 30; i++) { var dd = w[i] / sum * (T4b - T4a); pairT.push([t, dd]); t += dd; } })();
var NAMES = ['the false god', 'the devil', 'the adversary', 'the matrix', 'the machine', 'the system'], nameT0 = nm.t0 + nm.say * .27, nameD = nm.say * .73 / 6;
var T6a = k2.t0 + k2.say + .5, T6b = T6a + 15.2, impT = [];
(function () { var w = [], sum = 0, i, t = T6a + 1.2; for (i = 0; i < 30; i++) { w.push(i < 3 ? 3.4 : i < 7 ? 1.7 : 1); sum += w[i]; } for (i = 0; i < 30; i++) { var dd = w[i] / sum * (T6b - T6a - 1.2); impT.push([t, dd]); t += dd; } })();
var K6 = null, K6key = '';
function cam6(t) {
  var d = F.dims(), key = d.W + 'x' + d.H;
  if (key !== K6key) { var zf = ZF(), R = -TAU; K6key = key;
    K6 = [[i1.t0 - .4, cam45(i1.t0 - .4)[1], 0, 0, R], [i1.t0 + 8.6, .5, 0, 0, R, E.film], [i3.t0 + 4.2, d.PORT ? 1.0 : .76, 0, 0, R, E.film], [T4a - .4, d.PORT ? 1.0 : .76, 0, 0, R], [T4a + 2.4, .62, 0, 0, R, E.film], [k2.t0 + k2.say, .62, 0, 0, R], [T6a + 3.4, zf, 0, 0, R, E.film], [T6b + 12, zf * 1.05, 0, 0, R, E.lin]]; }
  return keysAt(K6, t);
}
var dim6 = track([[i1.t0 - .2, 1], [i1.t0 + 5, .3, E.io], [T4a - .4, .34], [T4a + 2, .14, E.io], [QL[0].t0 - .5, .14], [QL[0].t0 + .5, .3], [QL[4].t0 + 4, .12, E.lin], [k2.t0, .12], [T6a + 3, .2, E.io]]);
var ring6 = track([[i1.t0 - .2, 1], [i1.t0 + 5, .25, E.io], [T6a + .5, .25], [T6a + 3, .55, E.io]]);
var NOOSE = [1.9, 1.5, 1.22, .98, .76, .56];
function wrapText(str, maxc) { var w = str.split(' '), lines = [], cur = ''; for (var i = 0; i < w.length; i++) { if (cur && (cur + ' ' + w[i]).length > maxc) { lines.push(cur); cur = w[i]; } else cur = cur ? cur + ' ' + w[i] : w[i]; } if (cur) lines.push(cur); return lines; }
/* sections 7 and 8: the fall, the dark, the light at the bottom, the markers */
var f1 = C('so-i-stopped-trying'), d1 = C('down-through-the-sectors'), d2 = C('down-through-the-tactics'), d3 = C('down-through-the-mirror'), d4 = C('all-the-way-down'), sh1 = C('i-shed-it-one'), sh3 = C('some-of-it-i'),
  bt = C('and-at-the-bottom'), nb = C('not-above-me-not'), im = C('in-me-where-it'), tr0 = C('every-tradition-i-know'), TRC = ['the-christian-calls-it', 'the-buddhist-calls-it', 'the-muslim-speaks-of', 'the-jew-speaks-of', 'many-indigenous-peoples-call', 'the-taoist-says-that', 'the-mystic-calls-it'].map(C),
  sk1 = C('a-pattern-observed-traced'), sk2 = C('it-only-needs-your');
var PK2 = D.marks.PEAK2, FALL1 = d4.t0 + 3.2, LITE = bt.t0 + bt.say - 1.2;
var depth = track([[PK2 - .1, 0], [d1.t0, 1.6, E.in2], [d1.t0 + d1.say * .5, 9.4, E.io], [d1.t0 + d1.say + .5, 19.4, E.io], [d2.t1 + .4, 29.4, E.io], [d3.t0 + d3.say + .6, 49, E.io], [FALL1, 56, E.out2]]);
var LAY = [], TERMS = ['THE NARROW GATE', 'WAKING UP', 'THE LIFTING OF THE VEILS', 'THOU ART THAT', 'GATHERING THE SPARKS', 'THE REMEMBERING', 'THE WAY', 'THE DAWN', 'A PATTERN, OBSERVED'], mkT = [];
(function () { var i, src = [SECT.map(function (x) { return x.name; }), PAIRS.map(function (x) { return x[1]; }), D.tactics.filter(function (x, j) { return j % 3 === 0; })], k;
  for (k = 0; k < 3; k++) for (i = 0; i < src[k].length; i++) LAY.push([src[k][i], k * 10 + 2.2 + 7.2 * h1(i * 3.7 + k * 91.3), TAU * h1(i * 9.1 + k * 17.7), .34 + .95 * h1(i * 5.3 + k * 7.1), k]);
  mkT.push(TRC[0].t0 + .7, TRC[1].t0 + .7, TRC[2].t0 + .7, TRC[2].t0 + TRC[2].say * .62, TRC[3].t0 + .7, TRC[4].t0 + .7, TRC[5].t0 + .7, TRC[6].t0 + .7, sk1.t0 + .4); })();
var fallDim = track([[f1.t0, 1], [PK2 + 1.5, 0, E.in2]]);
var light78 = track([[f1.t0, 1], [PK2 + 2, .55, E.io], [d4.t0, .2, E.lin], [FALL1 - .6, 0, E.io], [LITE, 0], [LITE + 4.2, 1.15, E.out3], [im.t0 + 3, 1.3, E.io]]);
var lsize78 = track([[f1.t0, 1], [PK2 + 2, .6, E.io], [FALL1, .3], [LITE, .25], [LITE + 4.2, 1.7, E.out3], [im.t0 + 3, 2.0, E.io], [tr0.t0 + 6, 1.55, E.io]]);
var stars78 = track([[f1.t0, .75], [PK2 + .4, 1.2], [d3.t0, .9], [FALL1 - 1, 0, E.io], [im.t0, 0], [tr0.t0 + 8, .55, E.io]]);
/* sections 9, 10, 11 */
var YR = [0, 1, 2, 3].map(function (n) { return Cn('if-you-call-it', n); }), wd = C('the-words-are-different'), ds = C('the-destination-is-the'), w1 = C('notice-what-i-did'), w4 = C('i-descended-down-through'), w6 = C('i-only-moved-what'), w7 = C('one-block-at-a'),
  mof = C('my-original-frequency'), pq = C('pulsing-quietly-and-waiting'), x1 = C('i-came-back-up'), x2 = C('the-first-fractal-helped'), x3 = C('this-one-completes-the'), x4 = C('every-technique-is-opened'), x5 = C('and-now-it-holds'),
  x6 = C('no-one-is-undone'), x7 = C('the-moves-arrive-in'), x8 = C('two-hundred-and-three'), x9 = C('like-the-debt-prison'), x10 = C('together-they-are-the'), y1 = C('here-is-what-i'), y2 = C('a-chain-is-built'),
  MB = [Cn('maybe-it-was-a', 0), Cn('maybe-it-was-a', 1), C('maybe-it-was-the')], y3 = C('and-then-it-dissolves'), y4 = C('it-becomes-the-perfectionism'), y5 = C('it-made-me-who'), y6 = C('but-this-is-also'), y7 = C('when-one-of-them'),
  y8 = C('we-win-back-everything'), y9 = C('the-heaviest-chain-once'), z1 = C('my-healing-journey-meant'), z2 = C('it-will-take-me'), z3 = C('i-am-giving-it'), z4 = Cn('it-started-with-a', 1), z5 = C('now-the-map-is');
var PK3 = D.marks.PEAK3, pulseT = [YR[0].t0 + YR[0].say * .78, YR[1].t0 + YR[1].say * .78, YR[2].t0 + YR[2].say * .42, YR[2].t0 + YR[2].say * .58, YR[2].t0 + YR[2].say * .74, YR[2].t0 + YR[2].say * .92, YR[3].t0 + YR[3].say * .86, ds.t0 + ds.say * .7];
var BORD = []; (function () { var a = [], i, j, t; for (i = 0; i < 30; i++) a.push(i); for (i = 29; i > 0; i--) { j = Math.floor(h1(i * 12.9) * (i + 1)); t = a[i]; a[i] = a[j]; a[j] = t; } BORD = a; })();
var bkOn = w1.t0 + .3, bkGo = w6.t0 + .5;
/* the thirty blocks: each its own size and angle, a little out of line, the way things are stacked by hand */
var BLKW = [], BLKP = []; (function () { for (var i = 0; i < 30; i++) { var c = i % 5, r = Math.floor(i / 5), c3 = i % 3, r3 = Math.floor(i / 3), jx = (h1(i * 8.3) - .5), jy = (h1(i * 3.9) - .5), ang = (h1(i * 6.1 + 2) - .5) * .09, sg = h1(i * 1.9) > .5 ? 1 : -1;
  BLKW.push([(c - 2) * .36 + jx * .035, (r - 2.5) * .3 + jy * .028, .18 * (.8 + .3 * h1(i * 2.3 + .4)), .15 * (.7 + .36 * h1(i * 5.7 + 1.1)), ang, sg]);
  BLKP.push([(c3 - 1) * .64 + jx * .04, (r3 - 4.5) * .262 + jy * .02, .3 * (.86 + .14 * h1(i * 2.3 + .4)), .108 * (.8 + .26 * h1(i * 5.7 + 1.1)), ang * .7, sg]); } })();   // portrait: a tall window, three across and ten high
function blockAt(i, pz) {                     // where block i is when it is pz of the way into place (1 = resting against the window)
  var b = (F.dims().PORT ? BLKP : BLKW)[i], l = 1 - pz, sc = 1 + .32 * l;
  return [b[0] + b[5] * l * .09, b[1] + Math.pow(l, 1.4) * .5, b[2] * sc, b[3] * sc, b[4] + b[5] * l * .32];
}
function blocks(S, bk) {
  var P = S.bkp = shots._bkp || (shots._bkp = new Float32Array(120)), Q = S.bkq = shots._bkq || (shots._bkq = new Float32Array(60)), i;
  for (i = 0; i < 30; i++) { var g = blockAt(i, bk[i]); P[i * 4] = S.lx + g[0]; P[i * 4 + 1] = S.ly + g[1]; P[i * 4 + 2] = g[2]; P[i * 4 + 3] = g[3]; Q[i * 2] = bk[i]; Q[i * 2 + 1] = g[4]; }
}
function bkLeave(n) { return n < 3 ? w4.t0 + .8 + n * 1.5 : bkGo + (n - 3) / 26 * (PK3 - .15 - bkGo); }   // when the n-th block lifts
var THR = function (seed) { var o = [], j, a0 = TAU * h1(seed * 3.3), st = (h1(seed * 7.1) - .5) * 1.5; for (j = 0; j < 8; j++) { var r = (j ? (FRr[j - 1] + FRr[j]) / 2 : .16) * LS5 / 1.0, an = a0 + j * st + (h1(seed * 1.7 + j * 5.3) - .5) * .7; o.push(Math.cos(an) * r, Math.sin(an) * r); } return o; };
var K11 = null, K11key = '';
function cam11(t) {
  var d = F.dims(), key = d.W + 'x' + d.H;
  if (key !== K11key) { var zf = ZF(), zI = d.PORT ? .112 : .125, R = -TAU; K11key = key;
    var zN = zI * (d.PORT ? .84 : .7), yN = d.PORT ? -1.1 : -2.3;          // the names need the sky above the map: the map steps back and down
    K11 = [[x1.t0 - 1, 1.15, 0, 0, R], [x3.t0, 1.0, 0, 0, R, E.lin], [x3.t0 + 6, zI, 0, 0, R, E.film], [x4.t0 + .5, zI, 0, 0, R], [x4.t0 + 4.5, .5, 2.9, 2.5, R, E.film], [x5.t0 - .5, .5, 1.6, 3.5, R, E.lin], [x5.t0 + 3.5, zI, 0, 0, R, E.film],
      [x8.t0 + 1, zI, 0, 0, R], [x9.t0 - .3, zN, 0, yN, R, E.film], [x10.t0 + .4, zN, 0, yN, R], [x10.t0 + 4.5, zI, 0, 0, R, E.film],
      [y1.t0 - .3, zI * 1.04, 0, 0, R, E.lin], [y1.t0 + 6, 1.0, 0, 0, R, E.film], [z1.t0, 1.0, 0, 0, R], [z2.t0 - .3, 1.3, 0, 0, R, E.lin],
      [z2.t0 + 7, zf, 0, 0, R, E.film], [z4.t0, zf * 1.04, 0, 0, R, E.lin], [z5.t0 + 2.5, zf * (d.PORT ? 1.34 : 1.05), 0, d.PORT ? .9 : 0, R, E.film], [F.dur + 20, zf * (d.PORT ? 1.42 : 1.08), 0, d.PORT ? 1 : 0, R, E.lin]]; }
  return keysAt(K11, t);
}
var dimK = track([[0, .78], [1.2, 1, E.io]]);

function dlog(f, t) { var h = 1 / 240; return (Math.log(f(t + h)) - Math.log(f(t - h))) / (2 * h); }

var MK0 = new Float32Array(30), BKP0 = new Float32Array(120), BKQ0 = new Float32Array(60), TH0 = new Float32Array(16), TRA0 = new Float32Array(24), TRB0 = new Float32Array(24), LIM0 = [0, 0, 0, 0];
function Cn(slug, n) { var k = 0; for (var i = 0; i < D.caps.length; i++) if (D.caps[i].slug === slug && k++ === n) return D.caps[i]; throw new Error('no caption ' + slug + ' #' + n); }
var S0 = { zoom: 1, rot: 0, camx: 0, camy: 0, pt: 0, orig: 0, core: 0, logo: 0, emb: 0, words: 2, reveal: 2, front: 0, title: 0, spin: 0, dim: 1, hole: .108, rings: 1, poolr: 1, poolg: 0,
  mkr: 0, mkl: 0, glass: 0, glw: 0, bka: 0, thn: 0, tha: 0, patc: 0, lineh: 0, lineha: 0, linev: 0, lineva: 0, ls: 3.2, ring0: 0, lrev: 2, logok: 1, gen: 0, gena: 0, genlit: -9, frontl: 0, frontla: 0, patr: 0, pata: 0, gt: null, origx: 0, origy: 0, origk: 1, ringa: 0, ringr: 10.5, ringn: 0, ringhi: -9, ringdim: 1, motes: 0, cxf: .5, light: 0, lsize: .16, lx: 0, ly: 0, orba: 0, orbr: 0, orb: 0, glint: 0, stars: 0, dust: 0, streak: 0, bloom: .7, rays: 0, ca: 0, vig: .5, grain: .045, expo: 1, fade: 1, ringl: 0, ripx: 0, ripy: -1.6, ripr: 0, ripa: 0, poolk: 1 };

function Z0() { var d = F.dims(); return Math.max(.8, d.H * (1 - d.CYF) / (2.84 * d.U) * 1.08); }
var shots = F.shots = { tau: 0, tau0: 20, rip: null };
shots.state = function (t, S) {
  var k; for (k in S0) S[k] = S0[k]; S.mk = MK0; S.bkp = BKP0; S.bkq = BKQ0; S.th = TH0; S.tra = TRA0; S.trb = TRB0; S.lim = LIM0;
  var rm = F.RM ? .2 : 1;
  if (t < 0) {                             // the entry screen: a living emblem, driven by wall time tau
    var a = shots.tau;
    S.zoom = Z0() * (1 + .012 * Math.sin(a * .21) * rm); S.logo = 1; S.words = 2; S.spin = a * .012 * rm; S.hole = .385; S.rings = 3.2; S.dim = .78;
    S.poolr = 1.7; S.poolg = .93; S.orbr = 1.216; S.orba = a * .19; S.orb = 1; S.glint = 1; S.stars = .5; S.dust = .7; S.pt = a; S.vig = .62; S.bloom = 1; S.rays = 0;
    S.light = 0; plates(t, S);
    return S;
  }
  var a0 = shots.tau0, z = zoom(t), vz = dlog(zoom, t);
  if (t < T1) z *= Z0() / .8;
  S.zoom = z; S.pt = a0 + t;
  if (t < T1) {                            // launch: the ring ripples out, the light spirals in, the camera falls into the centre
    S.logo = artLogo(t); S.words = 2; S.hole = .385; S.rings = 3.2; S.spin = a0 * .012 * rm + spinV(t) * .05; S.dim = dimK(t);
    S.poolr = 1.7; S.poolg = poolG(t); S.orbr = orbR(t); S.orba = a0 * .19 + orbA(t); S.orb = orbI(t);
    if (shots.rip) { S.ripx = shots.rip[0]; S.ripy = shots.rip[1]; }
    S.ripr = rip(t); S.ripa = ripA(t);
  } else {
    S.orig = origA(t); S.reveal = reveal(t); S.front = frontK(t); S.core = S.orig * sm((z - 1.9) / .7); S.title = 0;
    if (t >= c30.t0 - .2) { S.orba = sweepA(t); S.orbr = sweepR(t); S.orb = sweepI(t); }
  }
  if (t > T1 && t < c2.t0 - .4) {            // "A different room. A different face. The same ending.": the same ring, three times
    for (var k = 0; k < 3; k++) { var u = (t - (cdr.t0 + .25 + k * 1.45)) / 1.9; if (u > 0 && u < 1) { S.reveal = lerp(.035, .5, E.out2(u)); S.front = .5 * Math.pow(1 - u, 1.6); } }
  }
  if (t >= g1.t0 - .2) {                     // the first map becomes one room among thirty
    var c3 = cam3(t); S.zoom = c3[1]; S.origy = ringY(t); S.ringa = ringA(t); S.ringr = RW; S.ringn = ringN(t); S.ringhi = hi3(t);
    S.ringdim = t >= gl1.t0 ? lerp(1, .32, sm((t - gl1.t0) / 1.5)) : t >= relT[0][0] && t < g27.t0 - .5 ? .55 : 1; S.origk = S.ringhi > -1 && Math.min(S.ringhi, 30 - S.ringhi) < 1.15 ? 1 : S.ringdim;
    if (t >= g27.t0 - .5 && t < gl1.t0) { var pu = Math.exp(-Math.max(0, t - g27.t0) * 1.4); S.ringdim = 1 + .5 * pu; S.origk = S.ringdim; }
    S._c3 = c3;
  }
  if (t >= g4.t0) {                          // sections 4 and 5
    var c4 = cam45(t), L = lost(t), f;
    S._c3 = [0, c4[1], c4[2], c4[3]]; S.zoom = c4[1]; S.rot = c4[4]; S.pt = a0 + t - L; S.gt = t - L;
    S.ringa = 1; S.ringn = 30; S.ringdim = ringDim4(t); S.ringhi = t < STOP ? hi3(t) : t < STOP + 2.4 ? -99 : -9;
    if (t < STOP + 1.4) { S.origy = RW; S.origk = t < STOP ? (Math.min(S.ringhi, 30 - S.ringhi) < 1.15 ? 1 : S.ringdim) : S.ringdim; }
    else { S.origy = 0; S.ring0 = 1; S.origk = 1; S.reveal = rev4(t); S.front = front4(t); }
    S.gen = genN(t); S.gena = genA(t); S.genlit = genLit(t);
    S._lk = t < PK1 - 5 ? lerp(1, .62, sm((t - STOP - 1.4) / 4)) : 1;
    if (t >= m2.t0 && t < m3.t0 + .5) {       // "in my body": a heartbeat travels the rings
      for (var hb = 0; hb < 8; hb++) for (var q2 = 0; q2 < 2; q2++) { var hu = (t - (m2.t0 + .5 + hb * 1.12 + q2 * .3)) / .95; if (hu > 0 && hu < 1) { S.patr = lerp(.12, .95, E.out2(hu)); S.pata = Math.pow(1 - hu, 2) * (q2 ? .45 : .8); } }
    }
    if (t >= PK1 - .2) {
      S.logo = logoA5(t); S.emb = S.logo; S.ls = LS5; S.lrev = lrev5(t); S.frontl = S.lrev; S.frontla = frontl5(t); S.hole = S.reveal > .1 && S.reveal < 1.5 ? Math.max(.108, .95 - (S.reveal - .1) * 3) : .95; S._lk = t > PK1 + 4 ? lerp(1, .55, sm((t - PK1 - 4) / 3)) : 1;
      var e5 = a5.t0;                         // table 2: three nested scales, lit in turn
      if (t >= e5 && t < n4.t0) {
        f = t < e5 + 2.9 ? 0 : t < a6.t0 ? 1 : t < n1.t0 ? 2 : t < n2.t0 ? 3 : t < n3.t0 ? 4 : 5;
        var want = [[1, .3, .3], [1, 1, .3], [.6, .6, 1.25], [1, 1, .3], [.55, 1, 1.2], [.6, .7, 1]][f], bl = sm((t - [e5, e5 + 2.9, a6.t0, n1.t0, n2.t0, n3.t0][f]) / .9);
        var prev = f ? [[1, .3, .3], [1, 1, .3], [.6, .6, 1.25], [1, 1, .3], [.55, 1, 1.2]][f - 1] : [1, 1, 1];
        S.origk = lerp(prev[0], want[0], bl); S.logok = lerp(prev[1], want[1], bl); S.ringdim = lerp(prev[2], want[2], bl);
      }
      if (pat5(t) > 0) { S.patr = PATR; S.pata = pat5(t); }
      var gl5 = glare(t); if (gl5 > 0) { S._glare = gl5; }
    }
  }
  if (t >= i1.t0 - .4) {                     // section 6
    var c6 = cam6(t), k6;
    S._c3 = [0, c6[1], c6[2], c6[3]]; S.zoom = c6[1]; S.rot = c6[4]; S.ls = LS5; S.logo = 1; S.emb = 1; S.lrev = 2; S.frontla = 0; S.hole = .108; S.reveal = .92; S.front = 0; S.ring0 = 1; S.origy = 0;
    S.origk = dim6(t); S.logok = Math.min(1, dim6(t) * .8); S.ringdim = ring6(t); S.ringhi = -9; S.pata = 0; S._lk = .7;
    if (t < i1.t0 + 6) { S.patr = PATR; S.pata = lerp(.8, 0, sm((t - i1.t0) / 5)); }
    if (t >= invT[0][0] - .2 && t < T4a) {     // table 3: each ring shows its original, then turns over
      for (k6 = 7; k6 >= 0; k6--) if (t >= invT[k6][0]) break; if (k6 >= 0) { var u6 = (t - invT[k6][0]) / invT[k6][1]; if (u6 < 1.15) { S.patr = FRr[k6]; S.pata = u6 < .5 ? Math.min(1, u6 / .12) : lerp(1, .35, sm((u6 - .5) / .2)) * (1 - sm((u6 - 1) / .15)); S.patc = sm((u6 - .46) / .1); } }
    }
    if (t >= T4a - .3 && t < T4c + .6) {       // table 4: the mirror
      var inPairs = t < T4b; S.lineha = Math.min(1, (t - T4a + .3) / .8) * (inPairs ? 1 : 1 - sm((t - T4b) / .5)); S.lineh = 0; S.glass = S.lineha; S.glw = F.dims().PORT ? .085 : .075;   // the glass: a real lens of thickness glw
      S.lineva = 0; S.linev = 0; S._lk = inPairs ? .7 : lerp(.7, .3, sm((t - T4b) / .6));
    }
    for (k6 = 0; k6 < 5; k6++) {               // table 5: the promise, and then the noose
      var q6 = QL[k6]; if (t >= q6.t0 - .1) { var uq = (t - q6.t0) / (q6.say + .6), cut = .5; S.patc = 1; S.patr = lerp(NOOSE[k6], NOOSE[k6 + 1], E.weight((uq - cut) / .3)); S.pata = .85; if (uq > 0 && uq < cut) S._warm = Math.sin(Math.PI * uq / cut); S._lk = .7 * lerp(1, .78, k6 / 4) * (uq > cut ? 1 - .1 * sm((uq - cut) / .2) : 1); }
    }
    if (t >= nm.t0 - .2) { S.patc = 1; S.patr = NOOSE[5]; S.pata = .85 * (1 - sm((t - k1.t0 - .4) / 2)); }
    if (t >= b2.t0 && t < T6a + 2) {           // "a chair that was never its own": the light stands apart from the ring
      S._lo = (F.dims().PORT ? .46 : .5) * sm((t - b2.t0 - .3) / 2.6) * (1 - sm((t - k2.t0 - .2) / 2.4));
    }
    if (t >= T6a) {                            // table 6: the thirty originals, room by room
      for (k6 = 29; k6 >= 0; k6--) if (t >= impT[k6][0]) break; S.ringhi = t < T6b && k6 >= 0 ? k6 : -9; if (t >= T6b) S.ringdim = lerp(.55, 1.15, sm((t - T6b) / 1.5));
      S._lk = .75; S._warm = (S._warm || 0) + .35 * sm((t - T6a) / 3);
    }
  }
  if (t >= f1.t0) {                          // sections 7 and 8
    var zf7 = ZF(), R7 = -TAU, z7 = t < PK2 - .3 ? Math.exp(lerp(Math.log(cam6(f1.t0)[1]), Math.log(zf7 * 1.5), E.in2((t - f1.t0) / (PK2 - .3 - f1.t0)))) : Math.exp(lerp(Math.log(zf7 * 1.5), Math.log(9), E.in3(Math.min(1, (t - PK2 + .3) / 2.2))));
    S._c3 = [0, z7, 0, 0]; S.zoom = z7; S.rot = R7; var fd = fallDim(t); S.origk = .2 * fd; S.logok = .16 * fd; S.ringdim = 1.15 * fd; S.ringa = fd > 0 ? 1 : 0; S.orig = fd > 0 ? 1 : 0; S.logo = S.emb = fd > 0 ? 1 : 0; S.ringhi = -9;
    S.pata = 0; S._lk = lsize78(t); S._li = light78(t); S._st = stars78(t); S.lineha = 0; S.lineva = 0;
    if (t >= PK2 && t < FALL1) {               // the shaft: rings pass outward as the camera falls
      var dz = depth(t), ph = (dz * .55) % 1; S.patr = .05 * Math.exp(4.6 * ph) / z7; S.pata = Math.sin(Math.PI * ph) * .5 * (1 - sm((t - d4.t0) / 3)); S.patc = sm((dz - 18) / 20); S._fall = 1;
    }
    if (t >= tr0.t0) {                          // the markers left by those who walked it before
      var mk = S.mk = shots._mk || (shots._mk = new Float32Array(30)), pr = F.dims().PORT, rr = pr ? .7 : .62, all = sm((t - sk2.t0) / 1.2);
      for (var m7 = 0; m7 < 9; m7++) { var an7 = TAU * (m7 / 9) , on = sm((t - mkT[m7]) / .9); mk[m7 * 3] = S.lx * 0 + Math.sin(an7) * rr; mk[m7 * 3 + 1] = Math.cos(an7) * rr; mk[m7 * 3 + 2] = on * (.55 + .5 * all + .12 * Math.sin(t * 1.3 + m7)); }
    }
  }
  if (t >= YR[0].t0 - .5) {                  // section 9: you're right
    var pr9 = F.dims().PORT, rr9 = (pr9 ? .7 : .62) * (1 - E.io((t - wd.t0) / (ds.t1 - wd.t0 + 1))), mk9 = S.mk = shots._mk || (shots._mk = new Float32Array(30)), pl = 0, pi9;
    for (pi9 = 0; pi9 < pulseT.length; pi9++) { var up = (t - pulseT[pi9]) / 1.5; if (up > 0 && up < 1) { S.patr = lerp(.1, 2.4, E.out2(up)) / S.zoom; S.pata = Math.pow(1 - up, 1.6) * .8; S.patc = 0; pl = Math.max(pl, Math.pow(1 - up, 2)); } }
    for (var m9 = 0; m9 < 9; m9++) { var a9 = TAU * (m9 / 9); mk9[m9 * 3] = Math.sin(a9) * rr9; mk9[m9 * 3 + 1] = Math.cos(a9) * rr9; mk9[m9 * 3 + 2] = t < ds.t1 + 1 ? (.9 + .6 * pl) * (rr9 > .02 ? 1 : 0) : 0; }
    S._warm = (S._warm || 0) + .5 * pl + .5 * sm((t - wd.t0) / 8); S._lk = lsize78(t) * (1 + .12 * pl + .25 * sm((t - wd.t0) / 8));
  }
  if (t >= bkOn) {                            // section 10: the window
    var bk = S.bk = shots._bk || (shots._bk = new Float32Array(30)), nb10;
    for (nb10 = 0; nb10 < 30; nb10++) { var on10 = sm((t - bkOn - h1(nb10 * 4.1) * 2.2) / 1.1), off10 = sm((t - bkLeave(nb10)) / .9); bk[BORD[nb10]] = on10 * (1 - off10); }
    blocks(S, bk);
    var capK = sm((t - bkOn + 1.6) / 1.4) * (1 - sm((t - x1.t0 + 2.6) / 1.5));          // the light may spread under the words: the finish pass caps it there instead of a dark pool
    S.lim = shots._lim || (shots._lim = [0, 0, 0, 0]); S.lim[0] = F.dims().PORT ? .68 : .4; S.lim[1] = F.dims().PORT ? .735 : .585; S.lim[2] = .34; S.lim[3] = capK; S.poolk = 1 - capK;
    S.bka = t < PK3 + 2 ? 1 : 0; var open = sm((t - bkGo) / (PK3 - bkGo)), fl = sm((t - PK3 + .2) / 1.6) * (1 - sm((t - mof.t1 - 1) / 5));
    S._li = 2.3 + 1.2 * open; S._st = .3; S._lk = 5.5 + 1.5 * open + 1.6 * fl * fl; S._warm = .4 * open + .9 * fl; S.expo = 1 + .08 * fl; S.bloom = .8 + .5 * open; S._rays = .9 + 1.4 * open;
    if (t >= PK3 + 2) { var cal = sm((t - PK3 - 2) / 7); S._li = lerp(2.4, 1.4, cal); S._lk = lerp(6.6, 2.1, cal); S._rays = .9; }
  }
  if (t >= x1.t0 - 1) {                       // section 11: the map, the chains, the giving
    var c11 = cam11(t), th, lk = shots._mk || (shots._mk = new Float32Array(30)), j11;
    S._c3 = [0, c11[1], c11[2], c11[3]]; S.zoom = c11[1]; S.rot = c11[4]; S.bka = 0; S.ls = LS5; S.ring0 = 1; S.origy = 0; S.hole = .108; S.expo = 1; S.bloom = .7;
    S.orig = 1; S.reveal = lerp(.1, .92, E.film((t - x1.t0) / 5.5)); S.front = t < x1.t0 + 6 ? .7 * sm((t - x1.t0) / .5) * (1 - sm((t - x1.t0 - 5) / 1)) : 0;
    S.logo = S.emb = t >= x3.t0 - .2 ? 1 : 0; S.lrev = lerp(0, 1.06, E.out2((t - x3.t0) / 5.5)); S.frontl = S.lrev; S.frontla = t >= x3.t0 && t < x3.t0 + 6.4 ? sm((t - x3.t0) / .4) * (1 - sm((t - x3.t0 - 5.4) / 1)) : 0;
    var fin = sm((t - z2.t0) / 5), inner = sm((t - y1.t0) / 5) * (1 - fin), md = lerp(1, 0, sm(inner * 1.6));
    S.origk = md; S.logok = md; S.ringa = sm((t - z2.t0 - 2.6) / 2.4);                       // the thirty arrive once the camera is far enough out to hold them S.ringn = 30; S.ringdim = 1.1; S.ringhi = t >= z3.t0 && t < z4.t0 ? ((t - z3.t0) / (z4.t0 - z3.t0)) * 30 : -9; S.ringl = t >= z3.t0 ? 30 * clamp((t - z3.t0) / (z4.t0 - z3.t0), 0, 1) : 0;
    if (t >= z2.t0) { S.ringdim = lerp(.5, 1.1, sm((t - z2.t0) / 4)) + .25 * sm((t - z4.t0) / 3); S.rot = c11[4] - .006 * Math.max(0, t - z2.t0 - 2) * Math.max(0, t - z2.t0 - 2) / (1 + .25 * Math.max(0, t - z2.t0 - 2)); } S._li = lerp(1.2, 1.5, inner); S._st = lerp(.6, .35, inner); S._lk = lerp(.75, 1.5, inner) * lerp(1, .55, fin); S._rays = .5;
    S.mk = lk; for (j11 = 0; j11 < 30; j11++) lk[j11] = 0;
    if (t >= x6.t0 - .2 && t < y1.t0 + 2) {     // the combinations: threads through the rings
      var seed = 1, prog = 7, al = 1;
      if (t < x7.t0) { prog = 0; al = sm((t - x6.t0) / .6); }
      else if (t < x8.t0) prog = 7 * E.io((t - x7.t0) / (x7.say + .4));
      else if (t < x9.t0) { var q8 = (t - x8.t0) / .22; seed = 10 + Math.floor(q8); al = .35 + .65 * Math.sin(Math.PI * (q8 % 1)); }
      else if (t < x10.t0) { var q9 = Math.min(2.999, (t - x9.t0) / ((x9.say + 1) / 3)); seed = 1 + Math.floor(q9); prog = 7 * E.out2(Math.min(1, (q9 % 1) / .45)); al = 1 - sm(((q9 % 1) - .86) / .14); }
      else { var q10 = (t - x10.t0) / 1.3; seed = 40 + Math.floor(q10); prog = 7; al = Math.sin(Math.PI * (q10 % 1)) * (1 - sm((t - y1.t0) / 2)); }
      th = S.th = shots._th || (shots._th = new Float32Array(16)); var nodes = THR(seed); for (j11 = 0; j11 < 16; j11++) th[j11] = nodes[j11]; S.thn = prog; S.tha = al; shots._seed = seed;
    }
    if (t >= y2.t0 && t < z1.t0) {              // the chain: nine links around the light
      var born = function (n) { return n < 3 ? MB[0].t0 + n * 3 : n < 6 ? MB[1].t0 + (n - 3) * 3.2 : MB[2].t0 + (n - 6) * 2.9; }, sink = E.io((t - y3.t0) / 4.5), back = E.out2((t - y6.t0 - .5) / 3), brk = sm((t - y7.t0 - 1.2) / 1.2), burst = E.out3((t - y9.t0 - 2.2) / 2.4);
      var tight = sm((t - y4.t0) / 40), pr11 = F.dims().PORT, R0 = pr11 ? .74 : .46, beat = .5 + .5 * Math.sin(t * 1.9);
      var base0 = t < y4.t0 ? R0 * (1 - sink * .55) : t < y6.t0 ? R0 * lerp(.45, .34, tight) : R0 * lerp(.34, 1, back); S.mkl = 1; S.mkr = base0 * TAU / 10 * .36;
      for (j11 = 0; j11 < 10; j11++) { var ang = TAU * j11 / 10 + t * .05, base = t < y4.t0 ? R0 * (1 - sink * .55) : t < y6.t0 ? R0 * lerp(.45, .34, tight) * (1 - .05 * beat * tight) : R0 * lerp(.34, 1, back), rad = base + (j11 === 4 ? brk * 2.6 : 0) + (t >= y9.t0 + 2.2 ? burst * 3 : 0),
          on = t < y3.t0 ? sm((t - born(j11)) / 1.2) : t < y6.t0 ? lerp(1, .42 + .12 * beat, sink) : (j11 === 4 ? 1 - brk : 1) * (1 - sm((burst - .5) / .5));
        lk[j11 * 3] = Math.sin(ang) * rad; lk[j11 * 3 + 1] = Math.cos(ang) * rad; lk[j11 * 3 + 2] = on * (t < y6.t0 ? .8 : 1); }
      if (t >= y4.t0 && t < y7.t0 + 1.2) { S._lk *= lerp(1, .6, tight); S._li *= lerp(1, .68, tight); }
      if (t >= y7.t0 + 1.2) { var gain = sm((t - y7.t0 - 1.2) / 3) * .4 + sm((t - y8.t0) / 12) * .35 + sm((t - y9.t0 - 2) / 3) * .5; S._lk *= .62 + gain * 1.1; S._li *= .7 + gain * .7; S._warm = gain * .8; }
    }
    if (t >= z4.t0) S._warm = .35 * sm((t - z4.t0) / 2) + .3 * sm((t - z5.t0) / 3);
  }
  S.motes = motesK(t);
  S.glint = glintK(t); S.stars = starsK(t); S.dust = dustK(t); S.vig = vigK(t);
  var v = F.env(t, 'voice'), sb = F.env(t, 'sub'), breath = 1 + .05 * Math.sin(TAU * (t >= g4.t0 ? t - lost(t) : t) / 5.2);
  S.light = lightI(t) * breath * (1 + .22 * v); S.lsize = lightS(t) * (1 + .04 * v) * push(t);
  if (S._warm) { S.light *= 1 + .7 * S._warm; S.rays *= 1 + .8 * S._warm; S._warm = 0; }
  if (S._li != null) { S.light = (.5 + .05 * Math.sin(t * 1.2)) * S._li * (1 + .22 * v); S.stars = S._st; S.dust = Math.min(S.dust, S._st); S.motes = t > LITE ? -.7 * sm((t - LITE) / 4) : 0; S.glint = 0; S._li = null; if (S._rays) { S.rays = S._rays * (1 + .3 * v); S._rays = 0; } if (S._fall) { S.streak = .3 * (1 - sm((t - d4.t0) / 3)); S.ca = .003; S._fall = 0; } }
  if (S._lk) { S.lsize *= S._lk; S.light *= lerp(1, .8, 1 - S._lk > 0 ? 1 : 0); S._lk = 0; }
  if (S._glare) { S.light *= 1 + 1.1 * S._glare; S.lsize *= 1 + 4.2 * S._glare * S._glare; S.expo = 1 + .3 * S._glare; S.bloom = .7 + .5 * S._glare; S._glare = 0; }
  if (t >= g4.t0) { var h4 = 1 / 120, vz4 = (Math.log(cam45(t + h4)[1]) - Math.log(cam45(t - h4)[1])) / (2 * h4); if (Math.abs(vz4) < 40) vz = vz4; else vz = 0; }
  S.rays = raysK(t) * (1 + .3 * v);
  S.zoom *= 1 + .003 * sb * rm;            // sub-bass camera impulse, capped well under 0.6%
  S.glint *= 1 + .35 * sb;
  var sp = Math.abs(vz);
  S.ca = Math.min(.0055, sp * .0016); S.streak = Math.min(.45, sp * .12);
  var tl = t >= g4.t0 ? t - lost(t) : t;
  S.camx = .004 * Math.sin(tl * .31) + .003 * Math.sin(tl * .13 + 2) ; S.camy = .004 * Math.sin(tl * .23 + 1);   // handheld drift, reproducible
  S.camx /= S.zoom; S.camy /= S.zoom;
  if (S._c3) { S.camx += S._c3[2]; S.camy += S._c3[3]; S.lx = -S.camx * S.zoom; S.ly = -S.camy * S.zoom; S._c3 = null; }
  if (S._lo) { S.lx += S._lo; S.ly += S._lo * .18; S._lo = 0; }
  var fo = follow(t); if (fo > 0) { S.camx += Math.cos(S.orba) * S.orbr * fo; S.camy += Math.sin(S.orba) * S.orbr * fo; }
  if (t >= T1 && t < c2.t0) { var p1 = path1(t), pk = .9 * sm((t - 5) / 6) * (1 - sm((t - ROAD0) / (ROAD1 - ROAD0))); S.lx = p1[0]; S.ly = p1[1]; trail1(t, S); S.camx += p1[0] * pk / S.zoom; S.camy += p1[1] * pk / S.zoom; }   // the camera leans after the light: near stars slide, far ones barely move
  if (!F.dims().PORT) S.cxf = lerp(.5, .31, cxfK(t));
  if (!F.dims().PORT && fo > 0) { S.zoom *= lerp(1, 1.42 / TOURZ, fo / .78); S.camx += .2 * fo; }
  plates(t, S);
  return S;
};

/* ---------- GPU text for this frame ---------- */
var CREAM = [.953, .925, .851, 1];
shots.draw = function (t, S) {
  var d = F.dims(), ts = Math.min(d.W * .205, d.H * .2), cy = d.H * d.CYF + ts * .3;
  var tw = F.measure('Fractal', ts, ts * .012), s2 = ts * .5, w2 = F.measure('2', s2), x0 = d.W / 2 - (tw + w2 * 1.05) / 2;
  function title(fx) { F.text('Fractal', x0, cy, ts, CREAM, { track: ts * .012, align: -1, fx: fx }); F.text('2', x0 + tw + w2 * .08, cy - ts * .36, s2, CREAM, { align: -1, fx: fx ? function (i, n, o, gx, gy) { fx(7, 8, o, tw / 2 + gx, gy); } : null }); }
  if (t < 0) { title(null); return; }
  if (t >= g6.t0 - .1 && t < gs.t1 + 2) section3(t, S, d);
  if (t >= a5.t0 && t < n4.t0 + 1.5) section5(t, S, d);
  if (t >= invT[0][0] - .2 && t < T6b + 1) section6(t, S, d);
  if (t >= PK2 && t < bt.t0) section7(t, S, d);
  if (t >= tr0.t0 && t < ds.t1 + 1) section8(t, S, d);
  if (t >= bkOn && t < x1.t0 - 1) section10(t, S, d);
  if (t >= x9.t0 && t < x10.t0) section11(t, S, d);
  if (t < 2.4) {                           // the title breaks into points that become the stars
    var u = t / 2.2;
    title(function (i, n, o, gx) {
      var del = .05 + .35 * h1(i + 3), k = clamp((u - del * .5) / (1 - del * .5), 0, 1), e = E.io3(k);
      var ang = Math.atan2(-.35 - h1(i * 7.1) * .8, (gx - tw / 2) / ts + (h1(i * 3.3) - .5) * .6), dist = (.6 + h1(i + 11) * 1.6) * ts * 1.7;
      o.dx = Math.cos(ang) * dist * e; o.dy = Math.sin(ang) * dist * e; o.s = 1 - .4 * E.out2(k); o.a = 1 - sm((k - .35) / .5); o.soft = k * .5;
    });
  }
};
var GOLD = [1, .84, .52, 1];
function fit(str, size, maxw) { var w = F.measure(str, size); return w > maxw ? size * maxw / w : size; }
function section3(t, S, d) {
  var c = F.w2s(0, 0, S), cx = c[0], cy = c[1], R = RW * S.zoom * d.U, mw = Math.min(d.W * .8, Math.max(R * 1.45, d.U * .9)), i, u, a;
  if (t < g6.t0 + g6.say + .5) {              // the six names, one with each door
    i = Math.min(5, Math.floor((t - g6.t0) / g6.say * 6)); if (i < 0) return; u = (t - g6.t0) / g6.say * 6 - i; a = Math.min(1, u / .18) * (i < 5 ? Math.min(1, (1 - u) / .2) : Math.max(0, 1 - (t - g6.t0 - g6.say) / .5));
    var p6 = F.w2s(RW * Math.sin(i * .20943951), RW * Math.cos(i * .20943951), S), sz = fit(SIX[i], d.U * .26, d.W * .6);
    F.text(SIX[i], clamp(p6[0], d.W * .32, d.W * .68), p6[1] + S.zoom * d.U * 1.25 + sz * .9, sz, [GOLD[0], GOLD[1], GOLD[2], a], { fx: function (k, n, o) { o.dy = (1 - E.out3(Math.min(1, u / .3))) * sz * .25; } });
    return;
  }
  if (t >= relT[0][0] && t < g27.t0 - .5) {    // table 1: "Your relationship with ..." for all thirty
    for (i = 29; i >= 0; i--) if (t >= relT[i][0]) break; u = (t - relT[i][0]) / relT[i][1]; a = Math.min(1, u / .16) * Math.min(1, (1 - u) / .16);
    var s1 = d.U * .105, s2 = fit(SECT[i].relationship, d.U * .25, mw), nm = ('0' + (i + 1)).slice(-2) + '  ' + SECT[i].name.toUpperCase();
    F.text(nm, cx, cy - d.U * .36, s1 * .82, [GOLD[0], GOLD[1], GOLD[2], a * .9], { track: s1 * .22 });
    F.text('Your relationship with', cx, cy - d.U * .2, s1 * 1.25, [.953, .925, .851, a * .85]);
    F.text(SECT[i].relationship, cx, cy + d.U * .3 + s2 * .3, s2, [1, 1, 1, a], { fx: function (k, n, o) { o.dy = (1 - E.out3(Math.min(1, u / .25))) * s2 * .2; } });
    return;
  }
  if (t >= g27.t0 - .2 && t < gl1.t0 - .2) {   // the count
    u = clamp((t - g27.t0 + .2) / 2.2, 0, 1); var n = Math.round(2700 * E.out3(u)), str = n >= 1000 ? Math.floor(n / 1000) + ',' + ('00' + (n % 1000)).slice(-3) : '' + n;
    a = Math.min(1, (t - g27.t0 + .2) / .3) * Math.min(1, (gl1.t0 - .2 - t) / .6); var s3 = d.U * .46;
    F.text(str, cx, cy + d.U * .34 + s3 * .3, s3, [GOLD[0], GOLD[1], GOLD[2], a]);
    F.text('examples', cx, cy + d.U * .34 + s3 * .3 + d.U * .17, d.U * .11, [.953, .925, .851, a * .8], { track: d.U * .02 });
  }
}
var GREY = [.72, .76, .84, 1];
function section7(t, S, d) {
  var cx = d.W * S.cxf, cy = d.H * d.CYF, U = d.U, i, L, dz, s, a, sz, zc;
  if (t < FALL1) {                             // words rush past in depth: sectors, techniques, tactics
    zc = depth(t); var cols = [[1, .86, .56], [.8, .84, .95], [.62, .66, .76]];
    var boxes = [];
    for (i = 0; i < LAY.length; i++) { L = LAY[i]; dz = L[1] - zc; if (dz < .1 || dz > 6.5) continue; s = 1 / dz; a = sm((6.5 - dz) / 2.2) * sm((dz - .1) / .22) * (L[4] === 2 ? .8 : 1);
      sz = Math.min(U * .085 * s * 1.35, U * .9); var rx = Math.cos(L[2]) * L[3] * s * U * (d.PORT ? .8 : 1.25), ry = Math.sin(L[2]) * L[3] * s * U * 1.1;
      if (Math.abs(rx) > d.W || Math.abs(ry) > d.H) continue;
      var bw = F.measure(L[0], sz) / 2, bx0 = cx + rx - bw, bx1 = cx + rx + bw, by0 = cy + ry - sz, by1 = cy + ry + sz * .3, hit = false, bj;
      if (d.PORT ? by1 > d.H * .7 : bx1 > d.W * .57) continue;
      if (a > .35) { for (bj = 0; bj < boxes.length; bj++) if (bx0 < boxes[bj][1] && bx1 > boxes[bj][0] && by0 < boxes[bj][3] && by1 > boxes[bj][2]) { hit = true; break; } if (hit) continue; boxes.push([bx0, bx1, by0, by1]); }
      F.text(L[0], cx + rx, cy + ry, sz, [cols[L[4]][0], cols[L[4]][1], cols[L[4]][2], a], { soft: Math.max(0, s - 1.6) * .5 + Math.max(0, .3 - s) * 1.2 }); }
    return;
  }
  if (t >= sh1.t0 - .3) {                      // shedding: the inversions lift off, one at a time; the last come away in pieces
    for (i = 0; i < 30; i++) { var t0 = sh1.t0 + i * (bt.t0 - 2.4 - sh1.t0) / 30, u = (t - t0) / 2.6; if (u <= 0 || u >= 1) continue;
      var word = PAIRS[i][1], px = cx + (h1(i * 7.7) - .5) * U * (d.PORT ? .9 : 1.3), py = cy + U * .5 - E.out2(u) * U * 1.25, pieces = t0 >= sh3.t0 - .6 ? 1 : 0; a = Math.min(1, u / .2) * (1 - sm((u - .5) / .5));
      F.text(word, px, py, fit(word, U * .15, d.W * .8), [.93, .88, .78, a * .8], { soft: u * .9, fx: pieces ? function (k, n, o) { var e = E.out2(u); o.dx = (h1(k * 3.1 + i) - .5) * U * .9 * e; o.dy = (h1(k * 5.9 + i) - .2) * U * .5 * e; } : null }); }
  }
}
function section10(t, S, d) {
  var U = d.U, i, bk = S.bk, P = S.bkp, sz = Math.max(d.PORT ? 13 : 12, U * .05);
  for (i = 0; i < 30; i++) { var pz = bk[i]; if (pz < .03) continue; var g = blockAt(i, pz), bx = d.W * S.cxf + P[i * 4] * U, by = d.H * d.CYF - P[i * 4 + 1] * U, rot = g[4], lines = wrapText(PAIRS[i][1], d.PORT ? 16 : 13), j, s = sz * (1 + .32 * (1 - pz)), cs = Math.cos(rot), sn = Math.sin(rot);
    for (j = 0; j < lines.length; j++) s = Math.max(12, Math.min(s, fit(lines[j], s, g[2] * 2 * U * (d.PORT ? .9 : .86))));
    for (j = 0; j < lines.length; j++) { var oy = s * (.35 + (j - (lines.length - 1) / 2) * 1.15); F.text(lines[j], bx - oy * sn, by + oy * cs, s, [.96, .93, .86, Math.pow(pz, 1.5)], { rot: rot, soft: (1 - pz) * 1.5 }); } }
}
var TNAME = ['', 'The Debt Prison', 'The Golden Cage', 'The Trauma Bond Engine'];
function section11(t, S, d) {
  var q9 = Math.min(2.999, (t - x9.t0) / ((x9.say + 1) / 3)), k = 1 + Math.floor(q9), f = q9 % 1, a = sm(f / .25) * (1 - sm((f - .82) / .18)), c = F.w2s(0, LR5 * 1.0, S), sz = fit(TNAME[k], d.U * .2, d.W * .86);
  F.text(TNAME[k], c[0], Math.max(sz * 1.1, c[1] - sz * .75), sz, [1, .88, .6, a]);
  if (F.rec) F.rec[F.rec.length - 1].mapTop = c[1];                     // for the gate: the name must sit above the map's outer words
}
function section8(t, S, d) {
  var cx = d.W * S.cxf, cy = d.H * d.CYF, U = d.U, rr = d.PORT ? .7 : .62, i, j, a, sz = Math.max(12, U * .064);
  for (i = 0; i < 9; i++) { a = sm((t - mkT[i] - .3) / .8); if (a <= 0) continue; var an = TAU * (i / 9), mx = cx + Math.sin(an) * rr * U, my = cy - Math.cos(an) * rr * U, sd = Math.sin(an), cs = Math.cos(an), lines = wrapText(TERMS[i], 13), n = lines.length;
    var wm = 0; for (j = 0; j < n; j++) wm = Math.max(wm, F.measure(lines[j], sz, sz * .12));
    var RX = d.PORT ? d.W - 16 : d.W * F.COL - 24, al = sd > .2 ? -1 : sd < -.2 ? 1 : 0, room = al < 0 ? RX - (mx + sz) : al > 0 ? mx - sz - 16 : 1e9, top = cs > -.3;
    if (room < wm) al = 2;                      // no room beside the marker: the label sits above it (or below, in the lower half), never over it
    if (F.rec) F.rec.push({ s: '', dot: 1, x: mx, y: my, size: 14, a: a, al: 0, w: 14, rot: 0, soft: 0 });
    for (j = 0; j < n; j++) { var w = F.measure(lines[j], sz, sz * .12), lx, ly;
      if (al === 2) { lx = clamp(mx, 16 + wm / 2, RX - wm / 2); ly = top ? my - sz * 1.15 - (n - 1 - j) * sz * 1.2 : my + sz * 1.9 + j * sz * 1.2; }
      else { lx = al < 0 ? Math.min(mx + sz, RX - w) : al > 0 ? Math.max(mx - sz, 16 + w) : mx; ly = (al ? my + sz * .35 + (cs < -.3 ? sz * 1.1 : cs > .3 ? -sz * .9 : 0) : my - sz * 1.2 - (n - 1) * sz * 1.2) + j * sz * 1.2 - (al ? (n - 1) * sz * .6 : 0); }
      F.text(lines[j], lx, ly, sz, [1, .88, .62, a * .95], { align: al === 2 ? 0 : al, track: sz * .12 }); } }
}
function section6(t, S, d) {
  var c = F.w2s(0, 0, S), cx = c[0], cy = c[1], U = d.U, mw = Math.min(d.W * .86, d.PORT ? d.W : d.W * .54), i, u, a, sz;
  if (t < T4a) {                               // table 3
    for (i = 7; i >= 0; i--) if (t >= invT[i][0]) break; if (i < 0) return; u = (t - invT[i][0]) / invT[i][1]; if (u > 1.15) return;
    var flip = sm((u - .34) / .16), out = 1 - sm((u - 1) / .15), topm = cy - .887 * S.zoom * U, lh = Math.min(U * .26, (topm - 14) / 3.1), y3 = topm - lh * 2.25, en3 = Math.min(1, u / .12) * out;
    sz = Math.min(fit(INV[i][0], lh * .82, mw), lh * .82);
    F.text(INV[i][0], cx, y3, sz, [1, .84, .52, en3 * lerp(1, .86, flip)], { fx: function (k, n, o) { o.dy = (1 - E.out3(Math.min(1, u / .2))) * sz * .25; } });
    F.text('becomes', cx, y3 + lh * .82, lh * .4, [.953, .925, .851, .8 * flip * out], { track: lh * .1 });
    sz = Math.min(fit(INV[i][1], lh * .9, mw), lh * .9);
    if (flip > 0) F.text(INV[i][1], cx, y3 + lh * 1.85, sz, [.86, .89, .96, flip * out], { fx: function (k, n, o) { o.sy = Math.sin(flip * Math.PI / 2); } });
    return;
  }
  if (t < T4b) {                               // table 4: gold meets its reflection at the glass
    for (i = 29; i >= 0; i--) if (t >= pairT[i][0]) break; if (i < 0) return; u = (t - pairT[i][0]) / pairT[i][1];
    var ap = (1 - E.out3(Math.min(1, u / .42))) * U * .42, gap = U * .035, turn = sm((u - .52) / .26), en = Math.min(1, u / .16), ex = 1 - sm((u - .86) / .14), g0 = PAIRS[i][0], g1 = PAIRS[i][1];
    if (!section6.sz || section6.key !== d.W) { section6.sz = U * .2; for (var pi = 0; pi < 30; pi++) section6.sz = Math.min(section6.sz, fit(PAIRS[pi][0], U * .2, mw), fit(PAIRS[pi][1], U * .2, mw)); section6.key = d.W; }
    sz = section6.sz;
    F.text(g0, cx, cy - gap - ap, sz, [1, .84, .52, en * (1 - turn) * ex], { soft: turn * .8 });
    F.text(g1, cx, cy + gap + ap + sz * .78 * turn, sz, [lerp(.5, .9, turn), lerp(.54, .93, turn), lerp(.64, 1, turn), en * lerp(.55, 1, turn) * ex], { fx: function (k, n, o) { o.sy = lerp(-1, 1, turn); } });
    F.text(('0' + (i + 1)).slice(-2) + ' / 30', cx, cy + U * .78, U * .075, [.953, .925, .851, .72], { track: U * .02 });
    return;
  }
  if (t >= nameT0 - .2 && t < nm.t1 + .8) {     // the names: one place, one size, each melting into the next
    for (i = 0; i < 6; i++) { u = (t - nameT0 - i * nameD) / nameD; if (u < -.02 || u > (i === 5 ? 2.2 : 1.02)) continue; a = sm(u / .2) * (i === 5 ? 1 - sm((u - 1.5) / .7) : 1 - sm((u - .82) / .2));
      sz = fit(NAMES[i], U * .3, mw); F.text(NAMES[i], cx, cy - U * .62, sz, [GREY[0], GREY[1], GREY[2], a], { soft: (1 - a) * 1.2 }); }
    return;
  }
  if (t >= T6a + 1 && t < T6b + .8) {           // table 6: what was here first
    for (i = 29; i >= 0; i--) if (t >= impT[i][0]) break; if (i < 0) return; u = (t - impT[i][0]) / impT[i][1]; a = Math.min(1, u / .16) * Math.min(1, (1 - u) / .16); if (i === 29 && u > 1) return;
    // the words take the caption's place (no caption speaks here): the right-hand column on wide screens, under the ring on phones
    var s1 = U * .1, lines = wrapText(IMP[i], d.PORT ? 24 : 22), cw = d.PORT ? d.W - 40 : d.W * .37 - 24, s2 = d.PORT ? Math.min(32, d.W * .085) : Math.min(U * .17, d.W * .034), j, tx = d.PORT ? d.W / 2 : d.W * F.COL, ty, al6 = d.PORT ? 0 : -1;
    for (j = 0; j < lines.length; j++) s2 = Math.min(s2, fit(lines[j], s2, cw));
    ty = d.PORT ? d.H * .76 - (lines.length - 1) * s2 * .56 : d.H * .5 - (lines.length - 1) * s2 * .56;
    var kk = Math.max(12, s1 * .8);
    F.text(('0' + (i + 1)).slice(-2) + '  ' + SECT[i].name.toUpperCase(), tx, ty - s2 * 1.25, kk, [.75, .79, .87, a * .95], { track: kk * .28, align: al6 });
    for (j = 0; j < lines.length; j++) F.text(lines[j], tx, ty + s2 * (.3 + j * 1.12), s2, [1, .86, .56, a], { align: al6 });
  }
}
function section5(t, S, d) {
  var e = a5.t0, items = [[e + .5, e + 2.9, 'a human face', .887, 0], [e + 3.1, a6.t0 - .1, 'a logo', LR5, 0], [a6.t0 + .4, n1.t0 - .1, 'the sky', RW + .9, 0],
    [n1.t0 + .3, n2.t0 - .2, 'PERSON', .887, 1], [n1.t0 + 1.2, n3.t0 - .2, 'INSTITUTION', LR5, 1], [n2.t0 + 1.2, n3.t0 - .2, 'CIVILIZATION', RW + .9, 1], [n3.t0 + .2, n4.t0 + .3, 'CIVILIZATION', RW - 1.5, 2], [n3.t0 + 1.4, n4.t0 + .3, 'PATTERN', PATR, 1]], i, it, a, p, sz;
  for (i = 0; i < items.length; i++) {
    it = items[i]; if (t < it[0] || t > it[1] + .5) continue; a = Math.min(1, (t - it[0]) / .45) * Math.min(1, Math.max(0, (it[1] + .5 - t) / .5));
    p = F.w2s(0, it[3], S); if (it[3] * S.zoom * d.U < d.U * .16) continue;
    if (it[4]) { sz = d.U * .078; F.text(it[2], p[0], it[4] === 2 ? p[1] + sz * 1.5 : Math.max(sz * 1.6, p[1] - sz * .7), sz, [1, .84, .52, a], { track: sz * .34 }); }
    else { sz = d.U * .2; F.text(it[2], p[0], Math.max(sz * 1.3, p[1] - sz * .55), sz, [1, .93, .78, a], { fx: function (k, n, o) { o.dy = (1 - E.out3(Math.min(1, (t - it[0]) / .5))) * sz * .2; } }); }
  }
}
/* ---------- plates: the owner's images, lit by the one light, moved by the camera (engine: uPA*, uSeam, uBd, uDisF, uBkT) ---------- */
var PL = { A0: new Float32Array(4), A1: new Float32Array(4), A2: new Float32Array(4), B0: new Float32Array(4), B1: new Float32Array(4), seam: new Float32Array(4), seam2: new Float32Array(4), bd: new Float32Array(16), embd: new Float32Array(4) };
function v4(a, x, y, z, w) { a[0] = x; a[1] = y; a[2] = z; a[3] = w; }
function win(t, a, b, c, dd) { return sm((t - a) / (b - a)) * (1 - sm((t - c) / (dd - c))); }     // fade in a..b, out c..d
function scr(d, S) { return [(.5 - (S.cxf || .5)) * d.W / d.U, (d.CYF - .5) * d.H / d.U]; }              // screen centre, in screen units from the picture centre
function cover(d, asp, k) { return Math.max(d.H / (2 * d.U), d.W / (2 * d.U * asp)) * k; }
var DUST = [4, 10, 92, 99], MIR = [STOP + 1.2, STOP + 3.2, m2.t0 + .5, m2.t0 + 3], RINGS = [m3.t0 - .5, m3.t0 + 2.5, a1.t0 - 3, a1.t0 + .5], CITY = [PK1 - 1.5, PK1 + 4, i1.t0 - 1, i1.t0 + 2.5],
  SHAFT = [PK2 - .4, PK2 + 1.2, FALL1 - 2.4, FALL1 + 1], SKY = [tr0.t0 - 1, tr0.t0 + 6, YR[0].t0 - 1, YR[0].t0 + 2.5], FREQ = [YR[0].t0 - 1, YR[0].t0 + 3, ds.t1 - 1, ds.t1 + 3],
  SEAM4 = [g4.t0 - .3, g4.t0 + 1.2, STOP + 1.0, STOP + 1.45], BAND = [invT[0][0] - .2, T4a - .3], SEAM6 = [T4a - .3, T4c + .6], DIS = [bkOn - .5, bkOn + 2, PK3 + 2.5, PK3 + 7];
shots.PLATES = { DUST: DUST, MIR: MIR, RINGS: RINGS, CITY: CITY, SHAFT: SHAFT, SKY: SKY, FREQ: FREQ, SEAM4: SEAM4, BAND: BAND, SEAM6: SEAM6, DIS: DIS };
function plates(t, S) {
  var k; for (k in PL) PL[k].fill(0);
  S.pA0 = PL.A0; S.pA1 = PL.A1; S.pA2 = PL.A2; S.pB0 = PL.B0; S.pB1 = PL.B1; S.seam = PL.seam; S.seam2 = PL.seam2; S.bd = PL.bd; S.embd = PL.embd; S.pm = 0; S.pa = S.pb = S.pc = null; S.bkt = 0; S.disf = 0;
  var d = F.dims(), sc = scr(d, S), a, h, z;
  if (t < 0) {                                  // entry: the word rings behind the title sit at 55%, so the title reads cleanly
    var ts = Math.min(d.W * .205, d.H * .2), tw = F.measure('Fractal', ts, ts * .012) + F.measure('2', ts * .5) * 1.05;
    v4(PL.embd, 0, (ts * .3 - ts * .32) / -d.U, .55, tw * .65 / d.U); return;
  }
  if (t < DUST[3]) {                            // section 1: dust in the dark, two depths, sliding against the walking light
    a = win(t, DUST[0], DUST[1], DUST[2], DUST[3]); if (a <= 0) return; h = cover(d, 1, 1.25); var cx = S.camx * S.zoom, cy = S.camy * S.zoom;
    S.pm = 1; S.pa = 'p:dust'; v4(PL.A0, sc[0] - cx * .35 + .004 * t, sc[1] - cy * .35, h, .004 * t); v4(PL.A1, .42 * a, 1.4, 1, 0); v4(PL.A2, 1, 0, .55, 0);
    v4(PL.B0, sc[0] - cx * .9 - .009 * t, sc[1] - cy * .9 + .003 * t, h * .75, -.006 * t + 1.7); return;
  }
  if (t >= SEAM4[0] && t < SEAM4[3]) {          // section 4: the map turns around; its light face looks back. The twins, split by a seam of light
    a = win(t, SEAM4[0], SEAM4[1], SEAM4[2], SEAM4[3]); h = RW * S.zoom * (d.PORT ? .58 : .6);
    S.pm = 3; S.pa = 'p:fractal-8'; S.pb = 'p:frequency-8'; v4(PL.A0, S.lx, S.ly, h, 0); v4(PL.A1, .95 * a, .9, 1, 0); v4(PL.A2, 3, a, 0, 0); v4(PL.B1, .52 * a, .35, 1, .3);
    var ux = d.W * S.cxf + S.lx * d.U, sw = E.io3((t - g4.t0 - .4) / (STOP - g4.t0 - .4)), xs = ux + h * d.U * lerp(1.02, 0, sw);
    v4(PL.seam, 1, 0, xs * d.DPR, a * sm((t - g4.t0 - .3) / .5)); v4(PL.seam2, 1.5 * d.DPR * .5 + .5, Math.max(1.5, 5 / 1024 * 2 * h * d.U * d.DPR), 0, 0); return;
  }
  if (t >= MIR[0] && t < MIR[3]) {              // "the way I spoke to myself": a tarnished mirror behind the map, its sheen follows the light
    a = win(t, MIR[0], MIR[1], MIR[2], MIR[3]); h = cover(d, 1, 1.4) * (1 + .04 * Math.sin(t * .11)); z = Math.pow(S.zoom / .55, .25);
    S.pm = 1; S.pa = 'p:mirror'; v4(PL.A0, sc[0] + .06 * Math.sin(t * .07) - S.camx * S.zoom * .3, sc[1] + .04 * Math.cos(t * .05), h * z, -.05 + .012 * (t - MIR[0])); v4(PL.A1, .9 * a, 1.6, 1, 0); return;
  }
  if (t >= RINGS[0] && t < RINGS[3]) {          // the generations: growth rings, the newest map at their centre
    a = win(t, RINGS[0], RINGS[1], RINGS[2], RINGS[3]);
    S.pm = 1; S.pa = 'p:rings'; v4(PL.A0, S.camx * .2, S.camy * .2, 5.6, .018 * (t - RINGS[0])); v4(PL.A1, .5 * a, 1.1, 1, 1); return;
  }
  if (t >= CITY[0] && t < CITY[3]) {            // section 5: the far larger map the first one becomes the hub of; it moves at 0.6 of the camera
    a = win(t, CITY[0], CITY[1], CITY[2], CITY[3]); var zf = ZF(); h = 16 * zf * Math.pow(S.zoom / zf, .6);
    S.pm = 1; S.pa = 'p:city'; v4(PL.A0, -S.camx * Math.pow(S.zoom, .6), -S.camy * Math.pow(S.zoom, .6), h, S.rot); v4(PL.A1, .38 * a, 1.1, 1, 0); return;
  }
  if (t >= BAND[0] && t < BAND[1]) {            // table 3: each ring shows its gold original, then turns over to the grey stage (the twin plate, drained)
    S.pm = 4; S.pa = 'p:fractal-8'; S.pb = 'p:frequency-8'; v4(PL.A1, 1.7, .9, 1, 1); v4(PL.A2, 4, 0, 1.25, 0); var off = 1 - sm((t - BAND[1] + .6) / .6);
    for (k = 0; k < 8; k++) { var u = (t - invT[k][0]) / invT[k][1]; if (u <= 0) continue; PL.bd[k * 2] = Math.min(1, u / .12) * (u < 1 ? .92 : lerp(.92, .45, sm((u - 1) / .15))) * off; PL.bd[k * 2 + 1] = (t - (invT[k][0] + .42 * invT[k][1])) / .6 + .5; }
    return;
  }
  if (t >= SEAM6[0] && t < SEAM6[1]) {          // table 4: the mirror. Light above the glass (where the original stands), dark below (the counterfeit); the rings cross unbroken
    a = S.lineha; S.pm = 6; S.pa = 'p:fractal-8'; S.pb = 'p:frequency-8'; v4(PL.A0, S.origx, S.origy, 1, 0); v4(PL.A1, .62 * a, .8, 1, 1); v4(PL.A2, 6, a * .9, 0, 0); v4(PL.B1, .34 * a, .5, 1, .4);
    v4(PL.seam, 0, 1, (1 - d.CYF) * d.H * d.DPR + S.lineh * d.U * d.DPR, .35 * a); v4(PL.seam2, 1.5 * d.DPR * .5 + .5, 5 / 1024 * 2 * S.zoom * d.U * d.DPR, 0, 0); return;
  }
  if (t >= SHAFT[0] && t < SHAFT[3]) {          // section 7: the shaft, falling; the walls pass upward. x0.87 to match the original plate
    a = win(t, SHAFT[0], SHAFT[1], SHAFT[2], SHAFT[3]); var dz = clamp(depth(t) / 56, 0, 1); h = cover(d, .558, 1.12) * (1 + .55 * dz);
    S.pm = 1; S.pa = 'p:shaft'; v4(PL.A0, sc[0], sc[1] + h * (.04 + .1 * dz) - .05 * h, h, .05 * dz); v4(PL.A1, .87 * .78 * a, .5, .558, 0); return;
  }
  if (t >= SKY[0] && t < SKY[3]) {              // section 8: the sky behind the markers; one of its rings carries them
    a = win(t, SKY[0], SKY[1], SKY[2], SKY[3]); var rr = d.PORT ? .7 : .62;
    S.pm = 1; S.pa = 'p:sky'; v4(PL.A0, -S.camx * S.zoom * .4, -S.camy * S.zoom * .4, rr / .56, .006 * (t - SKY[0])); v4(PL.A1, .55 * a, .9, 1, 0); return;
  }
  if (t >= FREQ[0] && t < FREQ[3]) {            // section 9: the light holds; a faint Frequency layer turns behind it and answers each "you're right"
    a = win(t, FREQ[0], FREQ[1], FREQ[2], FREQ[3]); var pl = 0, pi; for (pi = 0; pi < pulseT.length; pi++) { var up = (t - pulseT[pi]) / 1.5; if (up > 0 && up < 1) pl = Math.max(pl, Math.pow(1 - up, 2)); }
    S.pm = 1; S.pa = 'p:frequency'; v4(PL.A0, S.lx, S.ly, d.PORT ? 1.12 : 1.35, .0087 * (t - FREQ[0])); v4(PL.A1, .15 * a * (1 + .04 * pl), .25, 1, 0); return;
  }
  if (t >= DIS[0] && t < DIS[3]) {              // section 10: as the blocks lift, the dark twin turns to the light one, band by band from the centre out
    a = win(t, DIS[0], DIS[1], DIS[2], DIS[3]); var lifted = 0; for (k = 0; k < 30; k++) lifted += sm((t - bkLeave(k)) / .9);
    S.pm = 5; S.pa = 'p:fractal-8'; S.pb = 'p:frequency-8'; v4(PL.A0, S.lx, S.ly, d.PORT ? 1.02 : .98, -.004 * (t - DIS[0])); v4(PL.A1, .9 * a, .8, 1, 0); v4(PL.A2, 5, a, 0, 0); v4(PL.B1, (.45 + .2 * sm((t - PK3 + 1) / 2)) * a, .4, 1, .85);
    S.disf = lifted / 30 * 9.02;
    if (t < PK3 + 2.2) { S.pc = 'p:basalt'; S.bkt = .5; }
  }
}
shots.need = function (t) {
  var n = t >= f1.t0 + 12 && t < x1.t0 - 3 ? [] : t < 2.5 ? ['logo'] : t < 3.1 ? ['logo', 'orig', 'core'] : t < g1.t0 ? ['orig', 'core'] : t < PK1 - 6 ? ['orig'] : ['orig', 'logo', 'emb'];
  function w(r, k) { if (t >= r[0] - .5 && t < r[r.length - 1] + .5) for (var i = 1; i < arguments.length; i++) n.push(arguments[i]); }
  w(DUST, 'p:dust'); w(SEAM4, 'p:fractal-8', 'p:frequency-8'); w(MIR, 'p:mirror'); w(RINGS, 'p:rings'); w(CITY, 'p:city'); w(BAND, 'p:fractal-8', 'p:frequency-8'); w(SEAM6, 'p:fractal-8', 'p:frequency-8');
  w(SHAFT, 'p:shaft'); w(SKY, 'p:sky'); w(FREQ, 'p:frequency'); w(DIS, 'p:fractal-8', 'p:frequency-8', 'p:basalt');
  return n.filter(function (k, i) { return n.indexOf(k) === i; });
};
shots.boundary = function (t, dt) {         // true in the gaps between captions: the only place quality may step
  var c = D.caps, i; for (i = 0; i < c.length; i++) if (t >= c[i].t0 - .1 && t <= c[i].t0 + c[i].say + .1) return false; return true;
};
shots.built = D.dur;
shots.endAt = z5.t0 + 3.4;               // "Enter the map" arrives under the last line and stays to the end                   // how far the picture is choreographed so far
})();
