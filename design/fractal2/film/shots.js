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
var T1 = 3.3;                              // end of launch: black, one light

/* ---------- tracks ---------- */
var revKeys = [[c2.t0 - .2, .06], [c2.t0 + 3.2, .118, E.film], [c8.t0, .118]], zKeys = [[0, .8], [.35, .8], [3.0, 11, F.bez(.6, 0, .25, 1)], [T1, 11], [T1 + .01, 3.5], [c8.t0, 3.5]];
st.forEach(function (c, i) {
  revKeys.push([c.t0 - .05, i ? FRr[i - 1] : .118]); revKeys.push([c.t0 + 1.05, FRr[i], E.film]);
  var zt = Math.min(3.5, .92 / (FRr[i] + .05) * (i < 7 ? 1 : .98)); zKeys.push([c.t0 - .05, zKeys[zKeys.length - 1][1]]); zKeys.push([c.t0 + 1.25, Math.max(1, zt), E.weight]);
});
revKeys.push([c30.t0, .84]); revKeys.push([c30.t0 + 1.2, .92, E.io]);
zKeys.push([c30.t0 - .3, 1]); zKeys.push([c30.t0 + 2.2, 1.9, E.film]); zKeys.push([cth.t0 - 1.6, 1.9]); zKeys.push([cth.t0 + .6, 1, E.film]); zKeys.push([crm.t0 - .2, 1]); zKeys.push([crm.t1 + 1.5, .34, E.film]);
var zoom = track(zKeys, true), reveal = track(revKeys);
var artLogo = track([[0, 1], [1.6, 1], [2.7, 0, E.in2]]);
var spinV = track([[0, 0], [2.6, 5.2, E.in3]]);                         // extra turn during the dive
var orbR = track([[0, 1.216], [.3, 1.216], [2.3, 0, E.in2]]), orbI = track([[0, 1], [2.0, 1.5], [2.6, 0]]);
var orbA = track([[0, 0], [2.6, 11, E.in2]]);
var lightI = track([[1.3, 0], [2.9, .85, E.out3], [cme.t0 - .6, .85], [cme.t0 + 1.4, .34, E.io], [cwi.t0 - .2, .34], [cwi.t0 + 1.6, 1.25, E.weight], [c2.t0, 1.0, E.io], [c8.t0, .9], [st[7].t0 + 1.3, .55, E.io], [c30.t0 + 8, .5]]);
var lightS = track([[1.3, .03], [3.2, .16, E.out3], [cq.t0 - .3, .16], [cq.t0 + 1.2, .2, E.io], [cme.t0 - .6, .2], [cme.t0 + 1.4, .085, E.io], [cwi.t0 - .2, .085], [cwi.t0 + 1.6, .2, E.weight], [c2.t0 + 3, .15, E.io], [st[7].t0 + 1.3, .085, E.io]]);
var starsK = track([[0, .5], [2.2, 0], [cwi.t0 + .2, 0], [cwi.t0 + 5, .9, E.out2], [c8.t0, .9], [st[7].t0, .75]]);
var dustK = track([[0, .7], [2.4, 0], [cwi.t0 + .5, 0], [cwi.t0 + 6, .7, E.io]]);
var origA = track([[c2.t0 - .3, 0], [c2.t0, 1]]);
var frontK = track([[c2.t0 - .2, 0], [c2.t0 + .4, 1, E.out2], [st[7].t0 + 1.2, 1], [c30.t0 + 1.4, 0]]);
var glintK = track([[0, 1], [2.4, 1], [2.7, 0], [c2.t0, 0], [c8.t0, .5, E.io], [c30.t0, .5], [c30.t0 + .6, 1.2], [cth.t0, 1.2], [crm.t1 + 2, .6]]);
var sweepA = track([[c30.t0, 1.2], [cth.t0 - .3, 1.2 + TAU * 1.5, F.bez(.3, 0, .3, 1)]]);
var sweepR = track([[c30.t0, .16], [cth.t0 - .3, .8, E.lin]]);
var sweepI = track([[c30.t0 - .2, 0], [c30.t0 + .5, 1.3], [cth.t0 - .8, 1.3], [cth.t0, 0]]);
var raysK = track([[0, 0], [2.4, 0], [3.4, .55], [cme.t0 + 1.4, .2, E.io], [cwi.t0 + 1.6, .9, E.out2], [c2.t0 + 2, .5, E.io], [st[7].t0, .3]]);
var poolG = track([[0, .93], [1.2, 0, E.out2]]);
var rip = track([[0, 0], [1.5, 3.4, E.outExpo]]), ripA = track([[0, .05], [1.5, 0, E.out2]]);
var vigK = track([[0, .62], [3, .5], [c2.t0, .5], [st[7].t0, .42]]);
var motesK = track([[3, 0], [7, -.8, E.io], [cme.t0, -.8], [cme.t0 + 1.5, -.25, E.io], [cwi.t0, -.25], [cwi.t0 + .4, 0], [cwi.t0 + 1.4, 1, E.out2], [c2.t0 + 4, .7], [st[0].t0, .25, E.io], [c30.t0, .25]]);
var follow = track([[c30.t0 - .3, 0], [c30.t0 + 2.2, .78, E.film], [cth.t0 - 1.6, .78], [cth.t0 + .6, 0, E.film]]);
var wander = track([[T1, 0], [9, 1, E.io], [c2.t0 - 6, 1], [c2.t0 - .5, 0, E.io]]);
var cxfK = track([[T1 - .3, 0], [9, 1, E.io]]);
var dimK = track([[0, .78], [1.2, 1, E.io]]);

function dlog(f, t) { var h = 1 / 240; return (Math.log(f(t + h)) - Math.log(f(t - h))) / (2 * h); }

var S0 = { zoom: 1, rot: 0, camx: 0, camy: 0, pt: 0, orig: 0, core: 0, logo: 0, emb: 0, words: 2, reveal: 2, front: 0, title: 0, spin: 0, dim: 1, hole: .108, rings: 1, poolr: 1, poolg: 0,
  motes: 0, cxf: .5, light: 0, lsize: .16, lx: 0, ly: 0, orba: 0, orbr: 0, orb: 0, glint: 0, stars: 0, dust: 0, streak: 0, bloom: .7, rays: 0, ca: 0, vig: .5, grain: .045, expo: 1, fade: 1, ripx: 0, ripy: -1.6, ripr: 0, ripa: 0, poolk: 1 };

function Z0() { var d = F.dims(); return Math.max(.8, d.H * (1 - d.CYF) / (2.84 * d.U) * 1.08); }
var shots = F.shots = { tau: 0, tau0: 20, rip: null };
shots.state = function (t, S) {
  var k; for (k in S0) S[k] = S0[k];
  var rm = F.RM ? .2 : 1;
  if (t < 0) {                             // the entry screen: a living emblem, driven by wall time tau
    var a = shots.tau;
    S.zoom = Z0() * (1 + .012 * Math.sin(a * .21) * rm); S.logo = 1; S.words = 2; S.spin = a * .012 * rm; S.hole = .345; S.rings = 3.2; S.dim = .78;
    S.poolr = 1.7; S.poolg = .93; S.orbr = 1.216; S.orba = a * .19; S.orb = 1; S.glint = 1; S.stars = .5; S.dust = .7; S.pt = a; S.vig = .62; S.bloom = 1; S.rays = 0;
    S.light = 0;
    return S;
  }
  var a0 = shots.tau0, z = zoom(t), vz = dlog(zoom, t);
  if (t < T1) z *= Z0() / .8;
  S.zoom = z; S.pt = a0 + t;
  if (t < T1) {                            // launch: the ring ripples out, the light spirals in, the camera falls into the centre
    S.logo = artLogo(t); S.words = 2; S.hole = .345; S.rings = 3.2; S.spin = a0 * .012 * rm + spinV(t) * .05; S.dim = dimK(t);
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
  S.motes = motesK(t);
  S.glint = glintK(t); S.stars = starsK(t); S.dust = dustK(t); S.vig = vigK(t);
  var v = F.env(t, 'voice'), sb = F.env(t, 'sub'), breath = 1 + .05 * Math.sin(TAU * t / 5.2);
  S.light = lightI(t) * breath * (1 + .22 * v); S.lsize = lightS(t) * (1 + .04 * v);
  S.rays = raysK(t) * (1 + .3 * v);
  S.zoom *= 1 + .003 * sb * rm;            // sub-bass camera impulse, capped well under 0.6%
  S.glint *= 1 + .35 * sb;
  var sp = Math.abs(vz);
  S.ca = Math.min(.0055, sp * .0016); S.streak = Math.min(.45, sp * .12);
  S.camx = .004 * Math.sin(t * .31) + .003 * Math.sin(t * .13 + 2) ; S.camy = .004 * Math.sin(t * .23 + 1);   // handheld drift, reproducible
  S.camx /= S.zoom; S.camy /= S.zoom;
  var fo = follow(t); if (fo > 0) { S.camx += Math.cos(S.orba) * S.orbr * fo; S.camy += Math.sin(S.orba) * S.orbr * fo; }
  var wa = wander(t); if (wa > 0) { S.lx = wa * (F.dims().PORT ? .3 : .22) * Math.sin(t * .052 + .6); S.ly = wa * .24 * Math.sin(t * .081 + 2.1); }
  if (!F.dims().PORT) S.cxf = lerp(.5, .31, cxfK(t));
  return S;
};

/* ---------- GPU text for this frame ---------- */
var CREAM = [.953, .925, .851, 1];
shots.draw = function (t, S) {
  var d = F.dims(), ts = Math.min(d.W * .205, d.H * .2), cy = d.H * d.CYF + ts * .3;
  var tw = F.measure('Fractal', ts, ts * .012), s2 = ts * .5, w2 = F.measure('2', s2), x0 = d.W / 2 - (tw + w2 * 1.05) / 2;
  function title(fx) { F.text('Fractal', x0, cy, ts, CREAM, { track: ts * .012, align: -1, fx: fx }); F.text('2', x0 + tw + w2 * .08, cy - ts * .36, s2, CREAM, { align: -1, fx: fx ? function (i, n, o, gx, gy) { fx(7, 8, o, tw / 2 + gx, gy); } : null }); }
  if (t < 0) { title(null); return; }
  if (t < 2.4) {                           // the title breaks into points that become the stars
    var u = t / 2.2;
    title(function (i, n, o, gx) {
      var del = .05 + .35 * h1(i + 3), k = clamp((u - del * .5) / (1 - del * .5), 0, 1), e = E.io3(k);
      var ang = Math.atan2(-.35 - h1(i * 7.1) * .8, (gx - tw / 2) / ts + (h1(i * 3.3) - .5) * .6), dist = (.6 + h1(i + 11) * 1.6) * ts * 1.7;
      o.dx = Math.cos(ang) * dist * e; o.dy = Math.sin(ang) * dist * e; o.s = 1 - .4 * E.out2(k); o.a = 1 - sm((k - .35) / .5); o.soft = k * .5;
    });
  }
};
shots.need = function (t) { return t < 2.5 ? ['logo'] : t < 3.1 ? ['logo', 'orig', 'core'] : ['orig', 'core']; };
shots.boundary = function (t, dt) {         // true in the gaps between captions: the only place quality may step
  var c = D.caps, i; for (i = 0; i < c.length; i++) if (t >= c[i].t0 - .1 && t <= c[i].t0 + c[i].say + .1) return false; return true;
};
shots.built = crm.t1 + 3;                   // how far the picture is choreographed so far
})();
