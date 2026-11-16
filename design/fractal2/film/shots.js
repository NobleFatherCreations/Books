/* Fractal² film: the timeline. state(t) and draw(t) are pure functions of time.
   Times come from caption anchors (C('slug').t0), so re-timing the captions from a recorded voice moves the picture with it. */
(function () {
'use strict';
var F = window.FILM, D = F.data, E = F.ease, track = F.track, clamp = F.clamp, lerp = F.lerp, sm = F.sm, TAU = Math.PI * 2;
var FRr = [.207, .296, .38, .462, .547, .624, .713, .84];
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
var starsK = track([[0, .5], [2.2, 0], [cwi.t0 + .2, 0], [cwi.t0 + 5, .9, E.out2], [c8.t0, .9], [st[7].t0, .75]]);
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
var wander = track([[T1, 0], [9, 1, E.io], [c2.t0 - 6, 1], [c2.t0 - .5, 0, E.io]]);
var cxfK = track([[T1 - .3, 0], [9, 1, E.io]]);
var push = track([[9, 1], [cme.t0 - 1, 1.42, E.lin], [cme.t0 + 1.4, 1], [c2.t0, 1]]);
var ringY = track([[g1.t0 - .2, 0], [g1.t0 + 4.6, RW, E.film]]);
var ringN = track([[g2.t0 + 1.5, 1], [g2.t0 + 2.1, 2, E.out2], [g3.t0 + .5, 2], [g3.t0 + 1.1, 3, E.out2], [g6.t0, 3], [g6.t0 + g6.say, 6, E.lin], [gk.t0 + .3, 6], [gk.t0 + 6.6, 30, E.io]]);
var ringA = track([[g2.t0 + 1.3, 0], [g2.t0 + 1.6, 1]]);
function ZF() { var d = F.dims(); return (d.PORT ? .84 : .98) / (RW + .9); }
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
var PAIRS = D.tables.pairs, IMP = D.tables.impulses, T4a = t4.t0 + t4.say * .62, T4b = QL[0].t0 - 4.4, T4c = QL[0].t0 - .7, pairT = [];
(function () { var w = [], sum = 0, i, t = T4a; for (i = 0; i < 30; i++) { w.push(i < 3 ? 5.6 : i < 6 ? 2 : 1); sum += w[i]; } for (i = 0; i < 30; i++) { var dd = w[i] / sum * (T4b - T4a); pairT.push([t, dd]); t += dd; } })();
var NAMES = ['the false god', 'the devil', 'the adversary', 'the matrix', 'the machine', 'the system'], nameT0 = nm.t0 + nm.say * .27, nameD = nm.say * .73 / 6;
var T6a = k2.t0 + k2.say + .5, T6b = T6a + 15.2, impT = [];
(function () { var w = [], sum = 0, i, t = T6a + 1.2; for (i = 0; i < 30; i++) { w.push(i < 3 ? 3.4 : i < 7 ? 1.7 : 1); sum += w[i]; } for (i = 0; i < 30; i++) { var dd = w[i] / sum * (T6b - T6a - 1.2); impT.push([t, dd]); t += dd; } })();
var K6 = null, K6key = '';
function cam6(t) {
  var d = F.dims(), key = d.W + 'x' + d.H;
  if (key !== K6key) { var zf = ZF(), R = -TAU; K6key = key;
    K6 = [[i1.t0 - .4, cam45(i1.t0 - .4)[1], 0, 0, R], [i1.t0 + 8.6, .5, 0, 0, R, E.film], [i3.t0 + 4.2, 1.0, 0, 0, R, E.film], [T4a - .4, 1.0, 0, 0, R], [T4a + 2.4, .62, 0, 0, R, E.film], [k2.t0 + k2.say, .62, 0, 0, R], [T6a + 3.4, zf, 0, 0, R, E.film], [T6b + 12, zf * 1.05, 0, 0, R, E.lin]]; }
  return keysAt(K6, t);
}
var dim6 = track([[i1.t0 - .2, 1], [i1.t0 + 5, .3, E.io], [T4a - .4, .34], [T4a + 2, .14, E.io], [QL[0].t0 - .5, .14], [QL[0].t0 + .5, .3], [QL[4].t0 + 4, .12, E.lin], [k2.t0, .12], [T6a + 3, .2, E.io]]);
var ring6 = track([[i1.t0 - .2, 1], [i1.t0 + 5, .25, E.io], [T6a + .5, .25], [T6a + 3, .55, E.io]]);
var NOOSE = [1.9, 1.5, 1.22, .98, .76, .56];
function wrapText(str, maxc) { var w = str.split(' '), lines = [], cur = ''; for (var i = 0; i < w.length; i++) { if (cur && (cur + ' ' + w[i]).length > maxc) { lines.push(cur); cur = w[i]; } else cur = cur ? cur + ' ' + w[i] : w[i]; } if (cur) lines.push(cur); return lines; }
var dimK = track([[0, .78], [1.2, 1, E.io]]);

function dlog(f, t) { var h = 1 / 240; return (Math.log(f(t + h)) - Math.log(f(t - h))) / (2 * h); }

var S0 = { zoom: 1, rot: 0, camx: 0, camy: 0, pt: 0, orig: 0, core: 0, logo: 0, emb: 0, words: 2, reveal: 2, front: 0, title: 0, spin: 0, dim: 1, hole: .108, rings: 1, poolr: 1, poolg: 0,
  patc: 0, lineh: 0, lineha: 0, linev: 0, lineva: 0, ls: 3.2, ring0: 0, lrev: 2, logok: 1, gen: 0, gena: 0, genlit: -9, frontl: 0, frontla: 0, patr: 0, pata: 0, gt: null, origx: 0, origy: 0, origk: 1, ringa: 0, ringr: 10.5, ringn: 0, ringhi: -9, ringdim: 1, motes: 0, cxf: .5, light: 0, lsize: .16, lx: 0, ly: 0, orba: 0, orbr: 0, orb: 0, glint: 0, stars: 0, dust: 0, streak: 0, bloom: .7, rays: 0, ca: 0, vig: .5, grain: .045, expo: 1, fade: 1, ripx: 0, ripy: -1.6, ripr: 0, ripa: 0, poolk: 1 };

function Z0() { var d = F.dims(); return Math.max(.8, d.H * (1 - d.CYF) / (2.84 * d.U) * 1.08); }
var shots = F.shots = { tau: 0, tau0: 20, rip: null };
shots.state = function (t, S) {
  var k; for (k in S0) S[k] = S0[k];
  var rm = F.RM ? .2 : 1;
  if (t < 0) {                             // the entry screen: a living emblem, driven by wall time tau
    var a = shots.tau;
    S.zoom = Z0() * (1 + .012 * Math.sin(a * .21) * rm); S.logo = 1; S.words = 2; S.spin = a * .012 * rm; S.hole = .385; S.rings = 3.2; S.dim = .78;
    S.poolr = 1.7; S.poolg = .93; S.orbr = 1.216; S.orba = a * .19; S.orb = 1; S.glint = 1; S.stars = .5; S.dust = .7; S.pt = a; S.vig = .62; S.bloom = 1; S.rays = 0;
    S.light = 0;
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
      var inPairs = t < T4b; S.lineha = Math.min(1, (t - T4a + .3) / .8) * (inPairs ? 1 : 1 - sm((t - T4b) / .5)); S.lineh = 0;
      S.lineva = inPairs ? 0 : sm((t - T4b - .2) / .5) * (1 - sm((t - T4c) / .5)); S.linev = 0; S._lk = inPairs ? .7 : lerp(.7, .3, sm((t - T4b) / .6));
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
  S.motes = motesK(t);
  S.glint = glintK(t); S.stars = starsK(t); S.dust = dustK(t); S.vig = vigK(t);
  var v = F.env(t, 'voice'), sb = F.env(t, 'sub'), breath = 1 + .05 * Math.sin(TAU * (t >= g4.t0 ? t - lost(t) : t) / 5.2);
  S.light = lightI(t) * breath * (1 + .22 * v); S.lsize = lightS(t) * (1 + .04 * v) * push(t);
  if (S._warm) { S.light *= 1 + .7 * S._warm; S.rays *= 1 + .8 * S._warm; S._warm = 0; }
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
  var wa = wander(t); if (wa > 0) { S.lx = wa * (F.dims().PORT ? .3 : .22) * Math.sin(t * .052 + .6); S.ly = wa * .24 * Math.sin(t * .081 + 2.1); }
  if (!F.dims().PORT) S.cxf = lerp(.5, .31, cxfK(t));
  if (!F.dims().PORT && fo > 0) { S.zoom *= lerp(1, 1.42 / TOURZ, fo / .78); S.camx += .2 * fo; }
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
function section6(t, S, d) {
  var c = F.w2s(0, 0, S), cx = c[0], cy = c[1], U = d.U, mw = Math.min(d.W * .86, d.PORT ? d.W : d.W * .54), i, u, a, sz;
  if (t < T4a) {                               // table 3
    for (i = 7; i >= 0; i--) if (t >= invT[i][0]) break; if (i < 0) return; u = (t - invT[i][0]) / invT[i][1]; if (u > 1.15) return;
    var flip = sm((u - .42) / .16), out = 1 - sm((u - 1) / .15), y3 = cy - U * .47;
    sz = fit(INV[i][0], U * .23, mw);
    if (flip < 1) F.text(INV[i][0], cx, y3, sz, [1, .84, .52, Math.min(1, u / .12)], { fx: function (k, n, o) { o.sy = Math.cos(Math.min(1, flip * 2) * Math.PI / 2); o.dy = (1 - E.out3(Math.min(1, u / .2))) * sz * .25; } });
    if (flip > .5) { sz = fit(INV[i][1], U * .25, mw); F.text(INV[i][1], cx, y3, sz, [GREY[0], GREY[1], GREY[2], out], { fx: function (k, n, o) { o.sy = Math.sin((flip - .5) * Math.PI); } }); }
    F.text('becomes', cx, cy + U * .5, U * .085, [.953, .925, .851, .7 * Math.min(1, u / .2) * out], { track: U * .03 });
    return;
  }
  if (t < T4b) {                               // table 4: gold meets its reflection at the glass
    for (i = 29; i >= 0; i--) if (t >= pairT[i][0]) break; if (i < 0) return; u = (t - pairT[i][0]) / pairT[i][1];
    var ap = (1 - E.out3(Math.min(1, u / .42))) * U * .42, gap = U * .13, turn = sm((u - .52) / .26), en = Math.min(1, u / .16), ex = 1 - sm((u - .86) / .14), g0 = PAIRS[i][0], g1 = PAIRS[i][1];
    sz = Math.min(fit(g0, U * .2, mw), fit(g1, U * .2, mw));
    F.text(g0, cx, cy - gap - ap, sz, [1, .84, .52, en * (1 - turn) * ex], { soft: turn * .8 });
    F.text(g1, cx, cy + gap + ap + sz * .78 * turn, sz, [lerp(.5, .9, turn), lerp(.54, .93, turn), lerp(.64, 1, turn), en * lerp(.55, 1, turn) * ex], { fx: function (k, n, o) { o.sy = lerp(-1, 1, turn); } });
    F.text(('0' + (i + 1)).slice(-2) + ' / 30', cx, cy + U * .78, U * .07, [.953, .925, .851, .55], { track: U * .02 });
    return;
  }
  if (t < T4c + .6) {                          // the whole table, held
    var top = d.H * (d.PORT ? .055 : .08), rowh = (d.H * (d.PORT ? .62 : .84)) / 30, fs = Math.min(rowh * .8, U * .068), half = Math.min(mw / 2, cx - 6) - 8, fade = 1 - sm((t - T4c) / .5);
    for (i = 0; i < 30; i++) { a = sm((t - T4b - .15 - i * .028) / .3) * fade; if (a <= 0) continue; var y4 = top + rowh * (i + .7);
      F.text(PAIRS[i][0], cx - 9, y4, fit(PAIRS[i][0], fs, half), [1, .84, .52, a], { align: 1 }); F.text(PAIRS[i][1], cx + 9, y4, fit(PAIRS[i][1], fs, half), [GREY[0], GREY[1], GREY[2], a], { align: -1 }); }
    return;
  }
  if (t >= nameT0 - .2 && t < nm.t1 + .8) {     // the names: one place, one size, each melting into the next
    for (i = 0; i < 6; i++) { u = (t - nameT0 - i * nameD) / nameD; if (u < -.02 || u > (i === 5 ? 2.2 : 1.02)) continue; a = sm(u / .2) * (i === 5 ? 1 - sm((u - 1.5) / .7) : 1 - sm((u - .82) / .2));
      sz = fit(NAMES[i], U * .3, mw); F.text(NAMES[i], cx, cy - U * .62, sz, [GREY[0], GREY[1], GREY[2], a], { soft: (1 - a) * 1.2 }); }
    return;
  }
  if (t >= T6a + 1 && t < T6b + .8) {           // table 6: what was here first
    for (i = 29; i >= 0; i--) if (t >= impT[i][0]) break; if (i < 0) return; u = (t - impT[i][0]) / impT[i][1]; a = Math.min(1, u / .16) * Math.min(1, (1 - u) / .16); if (i === 29 && u > 1) return;
    var s1 = U * .1, lines = wrapText(IMP[i], d.PORT ? 22 : 26), s2 = Math.min(U * .17, mw / 12), j;
    for (j = 0; j < lines.length; j++) s2 = Math.min(s2, fit(lines[j], s2, Math.min(mw, U * 1.5)));
    F.text(('0' + (i + 1)).slice(-2) + '  ' + SECT[i].name.toUpperCase(), cx, cy - U * .34, s1 * .8, [.72, .76, .84, a * .9], { track: s1 * .22 });
    for (j = 0; j < lines.length; j++) F.text(lines[j], cx, cy + U * .3 + s2 * (.3 + j * 1.12), s2, [1, .86, .56, a]);
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
shots.need = function (t) { return t < 2.5 ? ['logo'] : t < 3.1 ? ['logo', 'orig', 'core'] : t < g1.t0 ? ['orig', 'core'] : t < PK1 - 6 ? ['orig'] : ['orig', 'logo', 'emb']; };
shots.boundary = function (t, dt) {         // true in the gaps between captions: the only place quality may step
  var c = D.caps, i; for (i = 0; i < c.length; i++) if (t >= c[i].t0 - .1 && t <= c[i].t0 + c[i].say + .1) return false; return true;
};
shots.built = T6b + 2;                   // how far the picture is choreographed so far
})();
