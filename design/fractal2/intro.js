/* Fractal² intro: the stage.
   One field of points. Point 0 is "you" (the signal). Points 1..2700 are the 2,700 examples of The Fractal
   (30 sectors x 30 techniques x 3 levels). The rest bring one sector to 1,005 (335 tactics x 3 levels) and
   thirty sectors to 30,150. Every figure on the page is a formation of these same points.
   Motion is a critically damped chase toward a target that the scroll position sets, so it can be interrupted
   at any moment and never plays "at" the reader. No libraries. No storage. No network except same-site audio. */
(function () {
  'use strict';
  var D = window.F2, doc = document, root = doc.documentElement, cv = doc.getElementById('stage'), LB = doc.getElementById('labels');
  if (!cv || !D) return;
  var rmq = matchMedia('(prefers-reduced-motion: reduce)'), RM = rmq.matches;
  var lightq = matchMedia('(prefers-color-scheme: light)');
  var TAU = Math.PI * 2, NS = 30, NCORE = 2700, PER = 1005, N = 1 + NS * PER;
  function H(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  function clamp(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function ss(x) { x = clamp(x); return x * x * (3 - 2 * x); }

  /* ---------- who each point is ---------- */
  var TC = D.techCounts, SCN = D.stageCounts, techStage = [], tacStage = [], bandFirst = [], g, k, a;
  for (g = 0; g < 8; g++) for (k = 0; k < TC[g]; k++) techStage.push(g);
  for (g = 0, a = 0; g < 8; g++) { bandFirst.push(a); for (k = 0; k < SCN[g]; k++) tacStage.push(g); a += SCN[g]; }
  var NT = tacStage.length, coreM = [], restM = [], isCore = {};
  for (k = 0; k < 30; k++) { var m0 = Math.floor((k + .5) * NT / 30); coreM.push(m0); isCore[m0] = 1; }
  for (k = 0; k < NT; k++) if (!isCore[k]) restM.push(k);
  var pS = new Uint8Array(N), pM = new Uint16Array(N), pL = new Uint8Array(N), pK = new Int8Array(N), pC = new Uint8Array(N);
  (function () {
    for (var i = 1; i < N; i++) {
      var j = i - 1, s, q;
      if (j < NCORE) { s = j % 30; q = (j / 30) | 0; pK[i] = (q / 3) | 0; pC[i] = q; pM[i] = coreM[(q / 3) | 0]; pL[i] = q % 3; }
      else { var e = j - NCORE; s = e % 30; q = (e / 30) | 0; pK[i] = -1; pC[i] = 0; pM[i] = restM[((q / 3) | 0) % restM.length]; pL[i] = q % 3; }
      pS[i] = s;
    }
  })();

  /* ---------- palette (from the page's own tokens) ---------- */
  var PAL = [], LIGHT = false;
  function hex(v) { v = v.trim(); if (v.charAt(0) !== '#') return [.9, .9, .88]; if (v.length === 4) v = '#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3]; return [parseInt(v.substr(1, 2), 16) / 255, parseInt(v.substr(3, 2), 16) / 255, parseInt(v.substr(5, 2), 16) / 255]; }
  function readPalette() {
    var cs = getComputedStyle(root), names = ['--ink', '--s1', '--s2', '--s3', '--s4', '--s5', '--s6', '--s7', '--s8', '--gold', '--ink-3', '--warn'];
    PAL = names.map(function (n) { return hex(cs.getPropertyValue(n)); });
    LIGHT = lightq.matches;
    if (!LIGHT) PAL[10] = [.48, .56, .7];
  }
  var INK = 0, GOLD = 9, COLD = 10, WARN = 11;

  /* ---------- layout ---------- */
  var L = { w: 1, h: 1, P: true, cx: 0, cy: 0, u: 100, dpr: 1 }, stableH = 0;
  function measure() {
    var w = root.clientWidth, h = window.innerHeight;
    if (!stableH || Math.abs(h - stableH) > 140 || w !== L.w) stableH = h;
    L.w = w; L.h = stableH; L.P = w < 960 || w / stableH < 1;
    L.dpr = Math.min(window.devicePixelRatio || 1, 2);
  }
  function centre(hold) {       /* where the stage sits: beside the text on wide screens, behind it on narrow ones */
    if (L.P) return { cx: L.w * .5, cy: L.h * .36, u: Math.min(L.w * .44, L.h * .25) };
    var side = { cx: L.w * .71, cy: L.h * .52, u: Math.min(L.w * .25, L.h * .38) }, mid = { cx: L.w * .56, cy: L.h * .5, u: Math.min(L.w * .3, L.h * .4) };
    return { cx: side.cx + (mid.cx - side.cx) * hold, cy: side.cy + (mid.cy - side.cy) * hold, u: side.u + (mid.u - side.u) * hold };
  }

  /* ---------- formations ---------- */
  function mk(n, fn) {
    var d = new Float32Array(n * 6), o = {};
    for (var i = 0; i < n; i++) { o.x = 0; o.y = 0; o.s = 2; o.a = 0; o.c = INK; o.d = 0; fn(i, o); var b = i * 6; d[b] = o.x; d[b + 1] = o.y; d[b + 2] = o.s; d[b + 3] = o.a; d[b + 4] = o.c; d[b + 5] = o.d; }
    return { n: n, d: d };
  }
  function you(o, x, y, s, a, c) { o.x = x || 0; o.y = y || 0; o.s = s || 9; o.a = a === undefined ? 1 : a; o.c = c === undefined ? GOLD : c; }
  var GAP = .09, arc0 = [], arcSpan = [];
  (function () { var acc = 0; for (var g = 0; g < 8; g++) { arcSpan.push(TC[g] / 30 * (TAU - 8 * GAP)); arc0.push(acc + GAP / 2); acc += arcSpan[g] + GAP; } })();
  function ringPos(i, R, o, ox, oy) {
    var kk = pK[i], g = techStage[kk], first = 0, j; for (j = 0; j < g; j++) first += TC[j];
    var f = ((kk - first) + (pL[i] + H(i, 1)) / 3) / TC[g], th = -Math.PI / 2 + arc0[g] + f * arcSpan[g], r = R * (1 + (H(i, 2) - .5) * .085);
    o.x = (ox || 0) + Math.cos(th) * r; o.y = (oy || 0) + Math.sin(th) * r; return g;
  }
  function gridPos(i, o) {
    var s = pS[i], kk = pK[i], l = pL[i];
    if (L.P) { var col = s % 15, row = (s / 15) | 0; o.x = -.96 + (col + .5) / 15 * 1.92 + (l - 1) * .026; o.y = (row ? .06 : -.94) + kk / 29 * .84; }
    else { o.x = -1 + (s + .5) / 30 * 2 + (l - 1) * .015; o.y = -.62 + kk / 29 * 1.24; }
  }
  var ROWS = [], rowAcc = 0; for (g = 0; g < 8; g++) { ROWS.push(rowAcc + g * .5); rowAcc += Math.ceil(SCN[g] / 30); }
  var ROWT = rowAcc + 3.5;
  function panelPos(i, cx, cy, W, Hh, o) {
    var m = pM[i], gg = tacStage[m], t = m - bandFirst[gg], r = ROWS[gg] + ((t / 30) | 0), c = t % 30;
    o.x = cx - W / 2 + (c + .5 + (pL[i] - 1) * .28) / 30 * W; o.y = cy - Hh / 2 + (r + .5) / ROWT * Hh; return gg;
  }
  function tile(s) {
    var cols = L.P ? 5 : 6, rows = L.P ? 6 : 5, y0 = L.P ? -1.22 : -.9, y1 = L.P ? 1.32 : .9, c = s % cols, r = (s / cols) | 0;
    return { x: -1 + (c + .5) * 2 / cols, y: y0 + (r + .5) * (y1 - y0) / rows, W: 2 / cols * .8, H: (y1 - y0) / rows * .74 };
  }
  var LV = [.3, .58, .86];
  function levelPos(i, o, scale) { var th = H(i, 3) * TAU, r = (LV[pL[i]] + (H(i, 4) - .5) * .05) * (scale || 1); o.x = Math.cos(th) * r; o.y = Math.sin(th) * r; }
  var ENT = 11;
  var debt = (function () { for (var i = 0; i < D.combos.length; i++) if (D.combos[i][0] === 'The Debt Prison') return D.combos[i][1]; return [6, 6, 2, 2, 2, 6]; })();
  var beads = []; D.combos.forEach(function (c, ci) { c[1].forEach(function (st, t) { beads.push([ci, t, st, c[1].length]); }); });
  var ROSTER = ['The Debt Prison', 'The Golden Cage', 'The Trauma Bond Engine', 'The Gaslighting Machine', 'The Phantom Equity', 'The Memory Hole', 'The Halo Shield', 'The Confidentiality Cage', 'The Frog in Boiling Water', 'Learned Silence', 'Walking on Eggshells', 'Social Death', 'The Room',
    'The Loyalty Trap', 'The Burnout Machine', 'The Erased Contributor', 'The NDA Silencer', 'The Paper Cage', 'The Scapegoat Machine', 'The Long Con', 'The Wall', 'The Gratitude Prison', 'The Identity Lock', 'The Captured Referee'];

  var S = {};
  S.signal = { n: 1, gain: 1, keys: function () { return [mk(1, function (i, o) { you(o, 0, 0, 11, 1); })]; } };
  S.room = { n: 261, amb: .05, gain: .85, keys: function () { return [mk(261, function (i, o) { if (!i) return you(o, .18, -.06, 8, .95); o.x = (H(i, 5) * 2 - 1) * 1.12; o.y = (H(i, 6) * 2 - 1) * (L.P ? 1.45 : 1); o.s = 1.6 + H(i, 7) * 1.6; o.a = .14 + H(i, 8) * .3; })]; } };
  S.cycle = { n: 2701, sp: 7 / 8, amb: .006,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 6, .5); ringPos(i, .84, o); o.s = 1.9; o.a = .2; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 6, .5); var gg = ringPos(i, .84, o); o.s = 2.1; o.a = .9; o.c = 1 + gg; o.d = gg / 7; })];
    },
    labels: function () {
      var out = D.stages.map(function (nm, gi) { return { h: nm, c: 'mid', x: 0, y: -.02, a: gi / 8, b: gi === 7 ? 9 : (gi + 1) / 8 }; });
      out.push({ h: '', c: 'dim', x: 0, y: .2, a: 0, b: 9, f: function (p, el) { var t = Math.min(8, Math.floor(p * 8) + 1) + ' of 8'; if (el.textContent !== t) el.textContent = t; } });
      return out;
    } };
  S.levels = { n: 2701, sp: 2 / 3, stops: [0, .75, 1], amb: .008,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 7, .9); levelPos(i, o); o.s = 1.8; o.a = .16; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 7, .9); levelPos(i, o); o.s = 2; o.a = .8; o.d = pL[i] / 2; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 7, .9); var inn = H(i, 9) < .15; levelPos(i, o, inn ? .2 : 1); o.s = inn ? 1.5 : 2; o.a = inn ? .95 : .6; o.c = inn ? GOLD : INK; o.d = H(i, 10); })];
    },
    labels: function () {
      return [{ h: 'one life', x: 0, y: -LV[0] - .08, a: .02 }, { h: 'an institution', x: 0, y: -LV[1] - .08, a: .27 }, { h: 'a civilization', x: 0, y: -LV[2] - .08, a: .52 },
        { h: 'the pattern, inside the person', c: 'gold', x: 0, y: .44, a: .86 }];
    } };
  S.count = { n: 2701, sp: .72,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); o.x = H(i, 11) * 2 - 1; o.y = (H(i, 12) * 2 - 1) * .9; o.s = 1.8; o.a = .14; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); gridPos(i, o); o.s = 1.9; o.a = .88; o.c = 1 + techStage[pK[i]]; o.d = pS[i] / 29; })];
    },
    labels: function () {
      return [{ h: '0', c: 'big', x: 0, y: L.P ? -1.2 : -.87, a: .03, f: function (p, el) { var t = Math.round(2700 * ss(p * 1.08)).toLocaleString('en-US'); if (el.firstChild.nodeValue !== t) el.firstChild.nodeValue = t; } },
        { h: 'examples · 30 sectors × 30 techniques × 3 levels', c: 'cap', x: 0, y: L.P ? 1.08 : .8, a: .5 }];
    } };
  function gateXY(i, o) {
    var s = pS[i], th = -Math.PI / 2 + s * TAU / 30, R = .8, f = (pC[i] + .5) / 90, w = .05, hh = .085, u, v;
    if (f < .3) { u = -w; v = -hh + f / .3 * 1.4 * hh; } else if (f > .7) { u = w; v = -hh + (1 - f) / .3 * 1.4 * hh; } else { var ph = Math.PI * (f - .3) / .4; u = -w * Math.cos(ph); v = .4 * hh + w * Math.sin(ph); }
    var c = Math.cos(th), sn = Math.sin(th); o.x = c * (R + v) - sn * u; o.y = sn * (R + v) + c * u;
  }
  S.gates = { n: 2701, sp: 29 / 30,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 9, 1); gateXY(i, o); o.s = 1.6; o.a = .28; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 9, 1); gateXY(i, o); o.s = 1.7; o.a = .62; o.d = pS[i] / 29; })];
    },
    post: function (p) { var act = Math.min(29, Math.floor(p * 30)); if (p <= 0 || p >= 1) return; for (var i = 1; i < 2701; i++) if (pS[i] === act) { tA[i] = 1; tS[i] = 2.6; tC[i * 3] = PAL[GOLD][0]; tC[i * 3 + 1] = PAL[GOLD][1]; tC[i * 3 + 2] = PAL[GOLD][2]; } },
    labels: function () {
      return [{ h: '<span class="nmx"></span><span class="sub"></span>', c: 'mid', x: 0, y: .3, a: .001, b: 9, f: function (p, el) {
        var act = Math.min(29, Math.floor(p * 30)), s = D.sectors[act];
        if (el._a !== act) { el._a = act; el.firstChild.textContent = s[0]; el.lastChild.textContent = 'your relationship with ' + s[1]; }
      } }, { h: '', c: 'dim', x: 0, y: -.26, a: .001, b: 9, f: function (p, el) { var t = ('0' + Math.min(30, Math.floor(p * 30) + 1)).slice(-2) + ' / 30'; if (el.textContent !== t) el.textContent = t; } }];
    } };
  var OA = [[-.5, -.36], [.5, -.36], [0, .5]], OC = [[-.2, -.12], [.2, -.12], [0, .21]];
  function circ(i, cs, r, o) { var gq = pL[i], th = H(i, 13) * TAU, rr = r * (1 + (H(i, 14) - .5) * .07); o.x = cs[gq][0] + Math.cos(th) * rr; o.y = cs[gq][1] + Math.sin(th) * rr; }
  function originFinal(i, o) { if (!i) return you(o, 0, 0, 5, 0); if (H(i, 15) < .24) { var gg = ringPos(i, .13, o, 0, 0); o.c = 1 + gg; o.a = 1; o.s = 1.7; } else { circ(i, OC, .42, o); o.a = .5; o.s = 1.8; } o.d = H(i, 16); }
  S.origin = { n: 2701, sp: 2 / 3, stops: [0, .75, 1], tail: 1,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); circ(i, OA, .4, o); o.s = 1.8; o.a = .18; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); circ(i, OA, .4, o); o.s = 2; o.a = .85; o.d = pL[i] / 2; }),
        mk(2701, originFinal)];
    },
    labels: function () {
      return [{ h: 'a real need', x: -.5, y: L.P ? -.86 : -.84, a: .02, b: .78 }, { h: 'a difference in power', x: .5, y: L.P ? -.86 : -.84, a: .27, b: .78 }, { h: 'a gatekeeper', x: 0, y: .98, a: .52, b: .78 },
        { h: 'it installs itself', c: 'gold', x: 0, y: .7, a: .9 }];
    } };
  S.drivers = { n: 2701, amb: .01, keys: function () { return [mk(2701, originFinal)]; } };
  S.mirror = { n: 2701, sp: .4,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 7, 1); var gg = ringPos(i, .84, o); o.c = 1 + gg; o.a = .5; o.s = 1.9; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 8, 1); var gg = ringPos(i, .24, o); o.c = 1 + gg; o.a = .95; o.s = 1.6; o.d = H(i, 17); })];
    } };
  function linkPos(gq, i, o, dx, dy) {
    var th = H(i, 18) * TAU, rr = 1 + (H(i, 19) - .5) * .16;
    if (L.P) { o.x = Math.cos(th) * .17 * rr + (dx || 0); o.y = -.78 + gq * .52 + Math.sin(th) * .33 * rr + (dy || 0); }
    else { o.x = -.69 + gq * .46 + Math.cos(th) * .3 * rr + (dx || 0); o.y = Math.sin(th) * .15 * rr + (dy || 0); }
  }
  S.chain = { n: 2701, sp: .75,
    keys: function () {
      function yo(o) { if (L.P) you(o, 0, .78, 8, 1); else you(o, .69, 0, 8, 1); }
      return [mk(2701, function (i, o) { if (!i) { yo(o); o.a = .4; return; } linkPos((i - 1) % 4, i, o); o.s = 1.8; o.a = .14; }),
        mk(2701, function (i, o) { if (!i) return yo(o); var gq = (i - 1) % 4; linkPos(gq, i, o); o.s = 2; o.a = gq === 3 ? .95 : .6; o.c = gq === 3 ? GOLD : INK; o.d = gq / 3; })];
    },
    labels: function () {
      return ['great-grandmother', 'grandmother', 'mother', 'you'].map(function (t, gq) { return L.P ? { h: t, c: gq === 3 ? 'gold' : '', x: .6, y: -.78 + gq * .52, a: .05 + gq * .22 } : { h: t, c: gq === 3 ? 'gold' : '', x: -.69 + gq * .46, y: .3, a: .05 + gq * .22 }; });
    } };
  function tilesKey(alpha, col, gold) {
    return mk(N, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var t = tile(pS[i]), gg = panelPos(i, t.x, t.y, t.W, t.H, o); o.s = 1.35; o.a = alpha; o.c = gold ? GOLD : col ? 1 + gg : INK; o.d = gold ? H(i, 20) : pS[i] / 29 * .6 + H(i, 20) * .35; });
  }
  S.zoom = { n: N, sp: .5, stops: [0, .42, 1],
    keys: function () {
      var bigW = 1.9, bigH = L.P ? 2.05 : 1.5, bigY = L.P ? .05 : 0;
      return [mk(N, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var core = pK[i] >= 0; if (core) { gridPos(i, o); o.a = .85; o.c = 1 + techStage[pK[i]]; } else { gridPos(i, o); o.y = (H(i, 21) * 2 - 1) * .6; o.a = 0; } o.s = 1.9; }),
        mk(N, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); if (pS[i] === ENT) { var gg = panelPos(i, 0, bigY, bigW, bigH, o); o.a = .92; o.s = 2.1; o.c = 1 + gg; o.d = H(i, 22) * .9; } else if (pK[i] >= 0) { gridPos(i, o); o.a = .07; o.s = 1.6; } else { var t = tile(pS[i]); o.x = t.x; o.y = t.y; o.a = 0; } }),
        tilesKey(.82, 1)];
    },
    labels: function () {
      var y = L.P ? 1.5 : -.92;
      return [{ h: '30<span class="sub">techniques, the backbone</span>', c: 'big', x: 0, y: y, a: 0, b: .1 },
        { h: '335<span class="sub">tactics in one sector, each at three levels</span>', c: 'big gold', x: 0, y: y, a: .14, b: .5 },
        { h: '30,000+<span class="sub">examples when all thirty sectors are mapped</span>', c: 'big', x: 0, y: L.P ? 1.56 : -.985, a: .66, b: 9 }];
    } };
  S.altitudes = { n: 2701, sp: 2 / 3,
    keys: function () {
      function base(a2) { return function (i, o) { if (!i) return you(o, 0, 0, 6, .7); if (i <= 3) { o.x = 0; o.y = -LV[i - 1]; o.s = 9; o.a = a2; o.c = GOLD; o.d = (i - 1) / 2; return; } levelPos(i, o); o.s = 1.8; o.a = .26; }; }
      return [mk(2701, base(0)), mk(2701, base(1))];
    },
    labels: function () { return [{ h: 'in one life', x: .34, y: -LV[0], a: .05 }, { h: 'inside an institution', x: .42, y: -LV[1], a: .38 }, { h: 'across a culture', x: .38, y: -LV[2], a: .7 }]; } };
  S.names = { n: N, sp: .82, keys: function () { return [tilesKey(.2, 0), tilesKey(.8, 0, 1)]; } };
  S.witness = { n: 1, gain: 1, keys: function () { return [mk(1, function (i, o) { you(o, 0, 0, 8, .9); })]; } };
  S.threshold = { n: 1, gain: 1, keys: function () { return [mk(1, function (i, o) { you(o, 0, 0, 6, .55, COLD); })]; } };
  function beadPos(b, o) {
    var bd = beads[b], cols = L.P ? 9 : 17, rows = L.P ? 17 : 9, y0 = L.P ? -1.25 : -.9, y1 = L.P ? 1.4 : .9, ci = bd[0], c = ci % cols, r = (ci / cols) | 0;
    var ch = (y1 - y0) / rows, sp = Math.min(.034, ch * .78 / bd[3]);
    o.x = -1 + (c + .5) * 2 / cols + Math.sin(bd[1] * .9 + ci) * .008; o.y = y0 + (r + .5) * ch + (bd[1] - (bd[3] - 1) / 2) * sp;
  }
  S.roster = { n: 1 + beads.length, sp: .7,
    keys: function () {
      var nb = 1 + beads.length;
      return [mk(nb, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); beadPos(i - 1, o); o.a = 0; o.s = 2.4; }),
        mk(nb, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var bd = beads[i - 1]; beadPos(i - 1, o); o.a = bd[2] ? .7 : .4; o.s = 2.6; o.c = bd[2] ? bd[2] : INK; o.d = H(bd[0], 23); })];
    },
    labels: function () {
      var list = ROSTER.slice(0, L.P ? 13 : 24), n = list.length;
      return list.map(function (t, i2) {
        var x, y; if (L.P) { x = (i2 % 2 ? .06 : -.06); y = -1.18 + i2 * .205; } else { x = [-.74, 0, .74][i2 % 3]; y = -.8 + ((i2 / 3) | 0) * .23; }
        return { h: t, c: 'nm', x: x, y: y, a: .06 + i2 / n * .8 };
      });
    } };
  var DOORS = ['your guard', 'your way out', 'your worth', 'your certainty', 'your witnesses'];
  function doorPos(i, R, open, o) {
    var gq = (i - 1) % 5, f = (((i - 1) / 5) | 0) / 299, span = TAU / 5 - .16, th0 = -Math.PI / 2 + gq * TAU / 5, th = th0 + (f - .5) * span;
    var x = Math.cos(th) * R, y = Math.sin(th) * R, isDoor = Math.abs(f - .5) < .24;
    if (open && isDoor) { var hth = th0 + (.26 - .5) * span, hx = Math.cos(hth) * R, hy = Math.sin(hth) * R, vx = x - hx, vy = y - hy, ca = Math.cos(-1.25), sa = Math.sin(-1.25); x = hx + vx * ca - vy * sa; y = hy + vx * sa + vy * ca; }
    o.x = x; o.y = y; return gq;
  }
  S.multiply = { n: 1501, sp: 4 / 5, stops: [0, 5 / 6, 1],
    keys: function () {
      var R = L.P ? .52 : .62;
      return [mk(1501, function (i, o) { if (!i) return you(o, 0, 0, 9, 1); doorPos(i, R, 1, o); o.s = 2; o.a = .45; }),
        mk(1501, function (i, o) { if (!i) return you(o, 0, 0, 9, 1); var gq = doorPos(i, R, 0, o); o.s = 2.2; o.a = .9; o.c = COLD; o.d = gq / 4; }),
        mk(1501, function (i, o) { if (!i) return you(o, 0, 0, 6, .5); doorPos(i, R * .7, 0, o); o.s = 2.4; o.a = 1; o.c = WARN; o.d = H(i, 25) * .5; })];
    },
    labels: function () {
      var R = L.P ? .8 : .92;
      return DOORS.map(function (t, gq) { var th = -Math.PI / 2 + gq * TAU / 5; return { h: t, x: Math.cos(th) * R, y: Math.sin(th) * R, a: 0, b: 9, f: function (p, el) { var sh = p > (gq + .7) / 6; if (el._s !== sh) { el._s = sh; el.classList.toggle('shut', sh); } } }; });
    } };
  var NL = 6, LPTS = 200, NMASS = 3906, SEQN = 1 + NL * LPTS + NMASS;
  function seqLink(i, o, shiftAxis) {
    var gq = ((i - 1) / LPTS) | 0, th = H(i, 26) * TAU, rr = 1 + (H(i, 27) - .5) * .18, sh = shiftAxis || 0;
    if (L.P) { o.x = -.66 + Math.cos(th) * .12 * rr; o.y = -1.02 + gq * .42 + Math.sin(th) * .26 * rr + sh * (Math.sin(th) < 0 ? -1 : 1); }
    else { o.x = -.8 + gq * .32 + Math.cos(th) * .2 * rr + sh * (Math.cos(th) < 0 ? -1 : 1); o.y = .66 + Math.sin(th) * .1 * rr; }
    return gq;
  }
  function massPos(i, o, k2) {
    var e = i - 1 - NL * LPTS, lv = Math.floor(Math.log(e / 62 + 1) / Math.LN2), R = .1 * Math.pow(1.45, lv) * (L.P ? 1 : 1.12) * (k2 || 1), r = R * Math.sqrt(H(i, 28)), th = H(i, 29) * TAU;
    o.x = (L.P ? .3 : 0) + Math.cos(th) * r; o.y = (L.P ? 0 : -.2) + Math.sin(th) * r; return lv;
  }
  function seqYou(o, a2, s2) { you(o, L.P ? .3 : 0, L.P ? 0 : -.2, s2 || 9, a2); }
  function seqKeyB() { return mk(SEQN, function (i, o) { if (!i) return seqYou(o, .5, 7); if (i <= NL * LPTS) { var gq = seqLink(i, o); o.a = .9; o.s = 2.1; o.c = debt[gq] || INK; o.d = gq / 5; } else { var lv = massPos(i, o); o.a = .55; o.s = 2; o.c = WARN; o.d = lv / 5; } }); }
  S.sequence = { n: SEQN, sp: 5 / 6,
    keys: function () {
      return [mk(SEQN, function (i, o) { if (!i) return seqYou(o, 1); if (i <= NL * LPTS) { seqLink(i, o); o.a = .1; o.s = 1.8; } else { massPos(i, o, .1); o.a = 0; o.s = 1.6; o.c = WARN; } }), seqKeyB()];
    },
    labels: function () {
      var out = []; for (var gq = 0; gq < 6; gq++) out.push(L.P ? { h: String(gq + 1), c: 'dim', x: -.93, y: -1.02 + gq * .42, a: gq / 6 + .01 } : { h: String(gq + 1), c: 'dim', x: -.8 + gq * .32, y: .88, a: gq / 6 + .01 });
      return out;
    } };
  S['break'] = { n: SEQN, sp: .45, stops: [0, .4, 1],
    keys: function () {
      return [seqKeyB(),
        mk(SEQN, function (i, o) { if (!i) return seqYou(o, .6, 8); if (i <= NL * LPTS) { var gq = ((i - 1) / LPTS) | 0; seqLink(i, o, gq === 3 ? .07 : 0); o.a = .9; o.s = gq === 3 ? 2.5 : 2.1; o.c = gq === 3 ? GOLD : (debt[gq] || INK); o.d = H(i, 30) * .4; } else { massPos(i, o); o.a = .55; o.s = 2; o.c = WARN; } }),
        mk(SEQN, function (i, o) { if (!i) return seqYou(o, 1, 12); if (i <= NL * LPTS) { var gq = ((i - 1) / LPTS) | 0; seqLink(i, o, gq === 3 ? .13 : 0); if (gq > 3) { if (L.P) o.y += .2 + (gq - 3) * .1; else o.x += .12 + (gq - 3) * .06; o.y += L.P ? 0 : .14; o.a = .22; } else if (gq < 3) { o.a = .35; } else { o.a = .95; o.c = GOLD; } o.s = 2; if (gq !== 3) o.c = INK; o.d = H(i, 30); } else { massPos(i, o, 3.4); o.y -= .25; o.a = 0; o.s = 1.4; o.c = WARN; o.d = H(i, 31); } })];
    },
    labels: function () { return [L.P ? { h: 'break one', c: 'gold', x: -.2, y: -1.02 + 3 * .42, a: .12 } : { h: 'break one', c: 'gold', x: -.8 + 3 * .32, y: .4, a: .12 }]; } };
  function barPos(i, o) { var gq = (i - 1) % 8; o.x = (H(i, 32) * 2 - 1) * .94; o.y = (L.P ? -1.02 : -.75) + gq * (L.P ? .3 : .215) + (H(i, 33) - .5) * .03; return gq; }
  S.inversion = { n: 2401, sp: 7 / 8,
    keys: function () {
      return [mk(2401, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var gq = barPos(i, o); o.c = 1 + gq; o.a = .55; o.s = 1.8; }),
        mk(2401, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var gq = barPos(i, o); o.c = GOLD; o.a = .95; o.s = 2.1; o.d = gq / 7; })];
    },
    labels: function () {
      return D.stages.map(function (t, gq) { return { h: t, c: 'nm', x: 0, y: (L.P ? -1.02 : -.75) + gq * (L.P ? .3 : .215) - (L.P ? .1 : .085), a: 0, b: 9, f: function (p, el) { var done = p > (gq + .55) / 8; if (el._s !== done) { el._s = done; el.textContent = done ? D.originals[gq] : t; el.classList.toggle('gold', done); } } }; });
    } };
  S.frequency = { n: 1201, fast: 1, gain: 1,
    keys: function () { return [mk(1201, function (i, o) { if (!i) return you(o, 0, 0, 12, 1); var r = (((i - 1) % 6) + 1) / 6 * 1.05, th = H(i, 34) * TAU; o.x = Math.cos(th) * r; o.y = Math.sin(th) * r; o.c = GOLD; o.s = 2.4; o.a = .5 * (1 - r / 1.3); })]; },
    tick: function (t) { if (RM) return; for (var i = 1; i < 1201; i++) { var f = (((i - 1) % 6) / 6 + t * .055) % 1, r = .06 + f * 1.1, th = H(i, 34) * TAU; tX[i] = Math.cos(th) * r; tY[i] = Math.sin(th) * r; tA[i] = Math.sin(Math.PI * f) * .85; } } };
  var STRATA = ['the sectors', 'the techniques', 'the mirror', 'the body', 'the chain'], DROP = 4.25;
  S.descent = { n: 2701, sp: 0, linear: 1,
    keys: function () {
      function at(off) { return function (i, o) { if (!i) return you(o, 0, DROP - off, 12, 1); var b = (i - 1) % 5; o.x = (H(i, 35) * 2 - 1); o.y = -.45 + b * .85 + (H(i, 36) - .5) * .24 - off; o.s = 2.1; o.a = .8 - b * .08; o.c = b === 0 ? 1 + techStage[pK[i]] : INK; }; }
      return [mk(2701, at(0)), mk(2701, at(DROP))];
    },
    labels: function () { return STRATA.map(function (t, b) { return { h: t, x: 0, y: 0, a: 0, b: 9, yf: function (p) { return -.45 + b * .85 - .2 - p * DROP; } }; }); } };
  S.ground = { n: 301, gain: 1, fast: 1,
    keys: function () { return [mk(301, function (i, o) { if (!i) return you(o, 0, 0, 13, 1); var th = H(i, 37) * TAU; o.x = Math.cos(th) * .32; o.y = Math.sin(th) * .32; o.c = GOLD; o.s = 1.6; o.a = .16; })]; },
    tick: function (t) { if (RM) return; var r = .32 + Math.sin(t * .8) * .035; for (var i = 1; i < 301; i++) { var th = H(i, 37) * TAU; tX[i] = Math.cos(th) * r; tY[i] = Math.sin(th) * r; } } };
  function lightPos(i, o) { var th = H(i, 38) * TAU, r = Math.sqrt(H(i, 39)) * 1.3; o.x = Math.cos(th) * r; o.y = Math.sin(th) * r * (L.P ? 1.25 : .8); return r / 1.3; }
  S.horizon = { n: 2701, sp: .82, amb: .01,
    keys: function () {
      return [mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 12, 1); lightPos(i, o); o.a = 0; o.c = GOLD; }),
        mk(2701, function (i, o) { if (!i) return you(o, 0, 0, 10, 1); var r = lightPos(i, o); o.a = .3 + H(i, 40) * .65; o.s = 1.6 + H(i, 41) * 2.6; o.c = GOLD; o.d = r; })];
    } };
  S.atlas = { n: N, sp: .5,
    keys: function () {
      function k(lit) { return mk(N, function (i, o) { if (!i) return you(o, 0, 0, 5, 0); var s = pS[i], t = tile(s); if (s === ENT) { var gg = panelPos(i, t.x, t.y, t.W, t.H, o); o.a = lit ? .92 : .2; o.c = lit ? 1 + gg : INK; o.s = 1.4; o.d = H(i, 42); return; }
        if (pK[i] < 0) { o.x = t.x; o.y = t.y; o.a = 0; return; }
        var f = (pC[i] + H(i, 43)) / 90 * 4, e = f | 0, q = f - e, hw = t.W / 2, hh = t.H / 2; o.x = t.x + (e === 0 ? -hw + q * t.W : e === 1 ? hw : e === 2 ? hw - q * t.W : -hw); o.y = t.y + (e === 0 ? -hh : e === 1 ? -hh + q * t.H : e === 2 ? hh : hh - q * t.H); o.a = .3; o.s = 1.4; }); }
      return [k(0), k(1)];
    },
    labels: function () {
      var t = tile(ENT), out = [{ h: 'Entertainment &amp; Music', c: 'gold tiny', x: t.x, y: t.y - t.H / 2 - .05, a: .3 }, { h: '1 of 30 mapped at full resolution', c: 'cap', x: 0, y: L.P ? 1.5 : .985, a: .6 }];
      if (!L.P) D.sectors.forEach(function (s, i2) { if (i2 !== ENT) { var tt = tile(i2); out.push({ h: s[0], c: 'dim tiny', x: tt.x, y: tt.y, a: .1 }); } });
      return out;
    } };
  var NDOOR = 1401;
  function doorKey(open) {
    return mk(NDOOR, function (i, o) {
      if (!i) return you(o, 0, .3, 9, 1);
      var x0 = -.27, x1 = .27, y0 = -.82, y1 = .46;
      if (i <= 500) { var f = (i - 1) / 500 * 3, e = f | 0, q = f - e; o.x = e === 0 ? x0 : e === 1 ? x0 + q * (x1 - x0) : x1; o.y = e === 0 ? y1 - q * (y1 - y0) : e === 1 ? y0 : y0 + q * (y1 - y0); o.s = 2; o.a = open ? .95 : .5; o.c = open ? GOLD : INK; o.d = H(i, 44) * .3; }
      else if (i <= 800) { o.x = x0 + H(i, 45) * (x1 - x0); o.y = y0 + H(i, 46) * (y1 - y0); o.s = 2; o.a = open ? .5 : 0; o.c = GOLD; o.d = H(i, 47) * .5; }
      else { var d = H(i, 48), yy = y1 + d * (L.P ? .95 : .5), hw = .27 + d * (L.P ? .75 : .9); o.x = (H(i, 49) * 2 - 1) * hw; o.y = yy; o.s = 2.2; o.a = open ? .9 * (1 - d * .7) : 0; o.c = GOLD; o.d = .25 + d * .7; }
    });
  }
  S.door = { n: NDOOR, sp: .6, keys: function () { return [doorKey(0), doorKey(1)]; } };
  S.enter = { n: NDOOR, keys: function () { return [doorKey(1)]; } };

  /* ---------- simulation ---------- */
  var cur = new Float32Array(N * 7), tX = new Float32Array(N), tY = new Float32Array(N), tS = new Float32Array(N), tA = new Float32Array(N), tC = new Float32Array(N * 3), rate = new Float32Array(N);
  for (var ii = 0; ii < N; ii++) rate[ii] = .65 + H(ii, 50) * .8;
  var scene = null, sceneName = '', keyP = null, activeN = 1, holdN = 0, holdUntil = 0, lastP = -1, dirty = true;
  function setScene(name, now) {
    if (name === sceneName || !S[name]) return;
    var sc = S[name];
    if (!sc._k || sc._P !== L.P) { sc._k = sc.keys(); sc._P = L.P; }
    holdN = Math.max(activeN, holdN); holdUntil = now + 2600;
    scene = sc; sceneName = name; activeN = Math.max(sc.n, holdN); lastP = -1; dirty = true;
    buildLabels(sc);
    for (var nm in S) if (S[nm] !== sc && S[nm]._k && S[nm].n > 6000) S[nm]._k = null;     /* keep memory flat on phones */
  }
  function targets(p) {
    var ks = scene._k, st = scene.stops || [0, 1], seg = 0, t = 0, A, B;
    if (ks.length === 1) { A = B = ks[0]; }
    else { for (seg = 0; seg < ks.length - 2; seg++) if (p <= st[seg + 1]) break; A = ks[seg]; B = ks[seg + 1]; t = clamp((p - st[seg]) / (st[seg + 1] - st[seg])); }
    var sp = scene.sp === undefined ? .6 : scene.sp, lin = scene.linear, n = scene.n, ad = A.d, bd = B.d, i, b, e, te, ca, cb, pa, pb;
    for (i = 0; i < n; i++) {
      b = i * 6;
      te = sp >= 1 ? t : clamp((t - bd[b + 5] * sp) / (1 - sp)); e = lin ? te : te * te * (3 - 2 * te);
      tX[i] = ad[b] + (bd[b] - ad[b]) * e; tY[i] = ad[b + 1] + (bd[b + 1] - ad[b + 1]) * e; tS[i] = ad[b + 2] + (bd[b + 2] - ad[b + 2]) * e; tA[i] = ad[b + 3] + (bd[b + 3] - ad[b + 3]) * e;
      ca = ad[b + 4] | 0; cb = bd[b + 4] | 0; pa = PAL[ca]; pb = PAL[cb];
      tC[i * 3] = pa[0] + (pb[0] - pa[0]) * e; tC[i * 3 + 1] = pa[1] + (pb[1] - pa[1]) * e; tC[i * 3 + 2] = pa[2] + (pb[2] - pa[2]) * e;
    }
    for (i = n; i < activeN; i++) tA[i] = 0;
    if (scene.post) scene.post(p);
  }
  function simulate(dt, snap) {
    var lam = snap ? 1e3 : 5.2, i, b, k2, kp, fast = scene.fast;
    for (i = 0; i < activeN; i++) {
      b = i * 7; k2 = lam * dt * rate[i]; if (k2 > 1) k2 = 1; kp = fast && !snap ? Math.min(1, k2 * 4) : k2;
      if (cur[b + 6] < .004 && tA[i] > 0) { cur[b] = cur[b] + (tX[i] - cur[b]) * .85; cur[b + 1] = cur[b + 1] + (tY[i] - cur[b + 1]) * .85; }   /* invisible points do not fly across the stage */
      cur[b] += (tX[i] - cur[b]) * kp; cur[b + 1] += (tY[i] - cur[b + 1]) * kp; cur[b + 2] += (tS[i] - cur[b + 2]) * k2;
      cur[b + 3] += (tC[i * 3] - cur[b + 3]) * k2; cur[b + 4] += (tC[i * 3 + 1] - cur[b + 4]) * k2; cur[b + 5] += (tC[i * 3 + 2] - cur[b + 5]) * k2; cur[b + 6] += (tA[i] - cur[b + 6]) * k2;
    }
  }

  /* ---------- drawing ---------- */
  var gl = null, ctx2 = null, prog, buf, ibuf, U = {};
  function initGL() {
    try { gl = cv.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: false, powerPreference: 'low-power' }); } catch (e) { gl = null; }
    if (!gl) { ctx2 = cv.getContext('2d'); return; }
    var vs = 'attribute vec2 a_p;attribute float a_s;attribute vec4 a_c;attribute float a_i;uniform vec2 u_res,u_c;uniform float u_u,u_t,u_amb,u_gain,u_px;varying vec4 v_c;' +
      'void main(){float ph=a_i*12.9898;vec2 dr=vec2(sin(u_t*.31+ph),cos(u_t*.27+ph*1.7))*u_amb;vec2 px=u_c+(a_p+dr)*u_u;vec2 cl=px/u_res*2.-1.;gl_Position=vec4(cl.x,-cl.y,0.,1.);' +
      'float s=a_s;if(a_i<.5)s*=1.+.2*sin(u_t*1.7);gl_PointSize=max(1.5,s*u_px);v_c=vec4(a_c.rgb,a_c.a*(a_i<.5?max(u_gain,.85):u_gain));}';
    var fs = 'precision mediump float;varying vec4 v_c;void main(){vec2 q=gl_PointCoord-.5;float d=length(q)*2.;float a=smoothstep(1.,.25,d)*v_c.a;gl_FragColor=vec4(v_c.rgb*a,a);}';
    function sh(t, src) { var s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s); return s; }
    prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { gl = null; ctx2 = cv.getContext('2d'); return; }
    gl.useProgram(prog);
    buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, cur.byteLength, gl.DYNAMIC_DRAW);
    var ap = gl.getAttribLocation(prog, 'a_p'), as = gl.getAttribLocation(prog, 'a_s'), ac = gl.getAttribLocation(prog, 'a_c'), ai = gl.getAttribLocation(prog, 'a_i');
    gl.enableVertexAttribArray(ap); gl.vertexAttribPointer(ap, 2, gl.FLOAT, false, 28, 0);
    gl.enableVertexAttribArray(as); gl.vertexAttribPointer(as, 1, gl.FLOAT, false, 28, 8);
    gl.enableVertexAttribArray(ac); gl.vertexAttribPointer(ac, 4, gl.FLOAT, false, 28, 12);
    var idx = new Float32Array(N); for (var i = 0; i < N; i++) idx[i] = i;
    ibuf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, ibuf); gl.bufferData(gl.ARRAY_BUFFER, idx, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(ai); gl.vertexAttribPointer(ai, 1, gl.FLOAT, false, 0, 0);
    ['u_res', 'u_c', 'u_u', 'u_t', 'u_amb', 'u_gain', 'u_px'].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
    gl.enable(gl.BLEND); gl.disable(gl.DEPTH_TEST);
    cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); gl = null; ctx2 = null; });
    cv.addEventListener('webglcontextrestored', function () { initGL(); resize(); });
  }
  function resize() {
    measure();
    var w = Math.round(L.w * L.dpr), h = Math.round(cv.clientHeight * L.dpr);
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
    if (gl) gl.viewport(0, 0, w, h);
    readPalette(); layoutDOM();
    for (var nm in S) if (S[nm]._P !== L.P) S[nm]._k = null;
    if (scene) { scene._k = scene._k || scene.keys(); scene._P = L.P; buildLabels(scene); }
    dirty = true;
  }
  var C = { cx: 0, cy: 0, u: 100 }, gain = 1, ambNow = 0, holdAmt = 0, focusAmt = 0;
  function draw(time) {
    var px = L.dpr * Math.max(.85, Math.min(1.7, Math.sqrt(C.u / 190)));
    if (gl) {
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      if (LIGHT) gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); else gl.blendFunc(gl.ONE, gl.ONE);
      gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferSubData(gl.ARRAY_BUFFER, 0, cur.subarray(0, activeN * 7));
      gl.uniform2f(U.u_res, cv.width, cv.height); gl.uniform2f(U.u_c, C.cx * L.dpr, C.cy * L.dpr); gl.uniform1f(U.u_u, C.u * L.dpr);
      gl.uniform1f(U.u_t, RM ? 0 : time); gl.uniform1f(U.u_amb, RM ? 0 : ambNow); gl.uniform1f(U.u_gain, gain * (LIGHT ? 1.15 : 1)); gl.uniform1f(U.u_px, px);
      gl.drawArrays(gl.POINTS, 0, activeN);
    } else if (ctx2) {
      ctx2.setTransform(1, 0, 0, 1, 0, 0); ctx2.clearRect(0, 0, cv.width, cv.height);
      var step = activeN > 6000 ? 5 : 1;
      for (var i = 0; i < activeN; i += step) { var b = i * 7, al = cur[b + 6] * gain; if (al < .02) continue; var s = Math.max(1.5, cur[b + 2] * px * .7);
        ctx2.fillStyle = 'rgba(' + (cur[b + 3] * 255 | 0) + ',' + (cur[b + 4] * 255 | 0) + ',' + (cur[b + 5] * 255 | 0) + ',' + al.toFixed(3) + ')';
        ctx2.fillRect((C.cx + cur[b] * C.u) * L.dpr - s / 2, (C.cy + cur[b + 1] * C.u) * L.dpr - s / 2, s, s); }
    }
  }

  /* ---------- labels ---------- */
  var labels = [];
  function buildLabels(sc) {
    LB.textContent = ''; labels = [];
    if (!sc.labels) return;
    sc.labels().forEach(function (sp) { var el = doc.createElement('div'); el.className = 'lb ' + (sp.c || ''); el.innerHTML = sp.h; LB.appendChild(el); labels.push({ el: el, sp: sp, on: false, x: NaN, y: NaN }); });
  }
  function updateLabels(p, inFig) {
    for (var i = 0; i < labels.length; i++) {
      var lb = labels[i], sp = lb.sp, on = (inFig || (!L.P && p >= 1 && sp.b === undefined)) && p >= sp.a && p < (sp.b === undefined ? 9 : sp.b);
      if (RM) on = inFig && (sp.b === undefined || sp.b > 1);
      var yy = sp.yf ? sp.yf(p) : sp.y, x = Math.round(C.cx + sp.x * C.u), y = Math.round(C.cy + yy * C.u);
      if (sp.yf && (yy < -1.35 || yy > 1.5)) on = false;
      if (sp.f) sp.f(p, lb.el);
      if (x !== lb.x || y !== lb.y) { lb.x = x; lb.y = y; lb.el.style.transform = 'translate(' + x + 'px,' + y + 'px) translate(-50%,-50%)'; }
      if (on !== lb.on) { lb.on = on; lb.el.classList.toggle('on', on); }
    }
  }

  /* ---------- the page: scenes, figures, steps ---------- */
  var scenes = [], figs = {}, prog_el = doc.getElementById('prog'), docH = 1;
  function layoutDOM() {
    var sy = window.scrollY;
    scenes = [].map.call(doc.querySelectorAll('[data-scene]'), function (el) { return { name: el.getAttribute('data-scene'), top: el.getBoundingClientRect().top + sy }; });
    figs = {};
    [].forEach.call(doc.querySelectorAll('.fig'), function (el) {
      var r = el.getBoundingClientRect(), st = [].slice.call(el.querySelectorAll('.step'));
      var f = { el: el, top: r.top + sy, h: r.height, steps: st, tops: st.map(function (s) { return s.getBoundingClientRect().top + sy; }), on: -2 };
      if (st.length > 1) f.span = (f.tops[st.length - 1] - f.tops[0]) / (st.length - 1); else if (st.length === 1) f.span = st[0].getBoundingClientRect().height;
      figs[el.getAttribute('data-fig')] = f;
    });
    docH = Math.max(1, doc.documentElement.scrollHeight - window.innerHeight);
  }
  function readScroll() {
    var sy = window.scrollY, vh = L.h, mid = sy + vh * .55, idx = 0, i;
    for (i = 0; i < scenes.length; i++) if (scenes[i].top <= mid) idx = i; else break;
    var name = scenes.length ? scenes[idx].name : 'signal', f = figs[name], p = 0, inFig = false, isHold = false;
    if (f) {
      if (f.steps.length) {
        var y = sy + vh * (L.P ? .78 : .46), n = f.steps.length, tailW = (S[name] && S[name].tail) || 0;
        var ps = (y - f.tops[0]) / (n * f.span), tailH = Math.max(1, f.top + f.h - (f.tops[0] + n * f.span) - vh * .25), pt = (y - f.tops[0] - n * f.span) / tailH;
        p = (clamp(ps) * n + clamp(pt) * tailW) / (n + tailW);
        inFig = sy + vh * (L.P ? .55 : .9) > f.tops[0] && sy + vh * .3 < f.top + f.h;
        var on = inFig ? Math.min(n - 1, Math.floor(clamp(ps) * n + 1e-6)) : -1;
        if (ps >= 1 && tailW) on = n - 1;
        if (on !== f.on) { for (i = 0; i < n; i++) f.steps[i].classList.toggle('on', i === on); f.on = on; }
      } else {
        p = clamp((sy + vh * .5 - f.top) / Math.max(1, f.h - vh * .4)); isHold = true;
        inFig = sy + vh * .72 > f.top && sy + vh * .82 < f.top + f.h;
      }
      if (RM) p = sy + vh * .9 > f.top ? 1 : 0;
    }
    return { name: name, p: p, inFig: inFig, hold: inFig && isHold, sy: sy };
  }

  var last = 0, started = false, cost = { n: 0, sum: 0, max: 0 };
  function frame(now) {
    requestAnimationFrame(frame);
    var t0 = performance.now();
    var t = now / 1000, dt = Math.min(.05, t - last || .016); last = t;
    var st = readScroll();
    if (st.name !== sceneName) setScene(st.name, now);
    if (!scene) return;
    if (holdN && now > holdUntil) { holdN = 0; activeN = scene.n; }
    if (st.p !== lastP || dirty || scene.tick) { targets(st.p); if (scene.tick) scene.tick(t, st.p); lastP = st.p; dirty = false; }
    simulate(dt, RM || !started);
    started = true;
    var k = RM ? 1 : Math.min(1, dt * 4.5);
    focusAmt += ((st.inFig ? 1 : 0) - focusAmt) * k; holdAmt += ((st.hold ? 1 : 0) - holdAmt) * k;
    var c = centre(ss(holdAmt)); C.cx += (c.cx - C.cx) * (RM ? 1 : Math.min(1, dt * 6)); C.cy += (c.cy - C.cy) * (RM ? 1 : Math.min(1, dt * 6)); C.u += (c.u - C.u) * (RM ? 1 : Math.min(1, dt * 6));
    var flow = scene.gain !== undefined ? scene.gain : (L.P ? .2 : .72);
    gain += ((flow + (1 - flow) * focusAmt) - gain) * k;
    ambNow += (((scene.amb === undefined ? .004 : scene.amb)) - ambNow) * k;
    draw(t); updateLabels(st.p, st.inFig);
    if (prog_el) prog_el.style.transform = 'scaleX(' + clamp(st.sy / docH).toFixed(4) + ')';
    var c1 = performance.now() - t0; cost.n++; cost.sum += c1; if (c1 > cost.max) cost.max = c1;
  }

  function boot() {
    initGL(); measure(); var c0 = centre(0); C.cx = c0.cx; C.cy = c0.cy; C.u = c0.u;
    if (RM) root.classList.add('rm');
    root.classList.add('live');
    resize();
    addEventListener('resize', resize);
    if (window.ResizeObserver) new ResizeObserver(function () { layoutDOM(); }).observe(doc.getElementById('main'));
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(layoutDOM);
    var onq = function () { RM = rmq.matches; root.classList.toggle('rm', RM); layoutDOM(); dirty = true; };
    if (rmq.addEventListener) { rmq.addEventListener('change', onq); lightq.addEventListener('change', function () { readPalette(); dirty = true; }); }
    requestAnimationFrame(frame);
  }
  try { boot(); } catch (e) { root.classList.remove('live'); cv.style.display = 'none'; LB.style.display = 'none'; if (window.console) console.error(e); }
  window.F2stage = { state: function () { return { scene: sceneName, p: lastP, activeN: activeN, gl: !!gl, gain: gain }; }, cost: function (reset) { var o = { n: cost.n, avg: cost.n ? cost.sum / cost.n : 0, max: cost.max }; if (reset) cost = { n: 0, sum: 0, max: 0 }; return o; } };

  /* ---------- contents, quick exit ---------- */
  var tocB = doc.getElementById('toc-b'), toc = doc.getElementById('toc');
  function tocSet(open) { toc.hidden = !open; tocB.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  if (tocB && toc) {
    tocB.addEventListener('click', function () { tocSet(toc.hidden); if (!toc.hidden) { var a = toc.querySelector('a'); if (a) a.focus(); } });
    toc.addEventListener('click', function (e) { if (e.target.closest('a')) tocSet(false); });
    doc.addEventListener('click', function (e) { if (!toc.hidden && !e.target.closest('#toc,#toc-b')) tocSet(false); });
    if ('IntersectionObserver' in window) {
      var links = {}; [].forEach.call(toc.querySelectorAll('a[href^="#"]'), function (a) { links[a.getAttribute('href').slice(1)] = a; });
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { for (var id in links) links[id].removeAttribute('aria-current'); if (links[e.target.id]) links[e.target.id].setAttribute('aria-current', 'true'); } }); }, { rootMargin: '-30% 0px -60% 0px' });
      Object.keys(links).forEach(function (id) { var el = doc.getElementById(id); if (el) io.observe(el); });
    }
  }
  var lv = doc.getElementById('leave'), escAt = 0;
  if (lv) lv.addEventListener('click', function () { doc.title = 'Weather'; doc.body.style.visibility = 'hidden'; location.replace(navigator.onLine ? 'https://www.google.com/search?q=weather' : 'about:blank'); });
  addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (toc && !toc.hidden) { tocSet(false); tocB.focus(); return; }
    if (doc.querySelector('#nf-chrome.nf-open')) return;
    var n = Date.now(); if (n - escAt < 600 && lv) lv.click(); escAt = n;
  });

  /* ---------- narration: started by the reader, follows the voice, can be interrupted by any scroll ---------- */
  var pl = doc.getElementById('player'), au = doc.getElementById('pl-audio'), listen = doc.getElementById('listen');
  if (pl && au && listen) {
    var cap = doc.getElementById('pl-cap'), play = doc.getElementById('pl-play'), seek = doc.getElementById('pl-seek'), tm = doc.getElementById('pl-time'), rateB = doc.getElementById('pl-rate'), mute = doc.getElementById('pl-mute'), follow = doc.getElementById('pl-follow'), closeB = doc.getElementById('pl-close');
    var units = [], loaded = false, failed = false, curU = -1, following = true, autoScroll = 0, rates = [1, 1.25, 1.5, .85], ri = 0;
    var fmt = function (s) { s = Math.max(0, s | 0); return ((s / 60) | 0) + ':' + ('0' + s % 60).slice(-2); };
    function load() {
      if (loaded || failed) return; loaded = true;
      fetch(au.getAttribute('data-sync')).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
        units = j.units || []; au.src = au.getAttribute('data-src'); au.load();
        if (j.note) cap.textContent = j.note;
      }).catch(function () { failed = true; cap.textContent = 'The narration is being recorded and is not here yet. The text on the page is complete.'; play.disabled = true; seek.disabled = true; });
    }
    function open(o) { pl.hidden = !o; doc.body.classList.toggle('pl-open', o); listen.setAttribute('aria-expanded', o ? 'true' : 'false'); if (o) { load(); play.focus(); } else { au.pause(); listen.focus(); } }
    listen.addEventListener('click', function () { open(pl.hidden); });
    closeB.addEventListener('click', function () { open(false); });
    play.addEventListener('click', function () { if (au.paused) { var pr = au.play(); if (pr && pr.catch) pr.catch(function () {}); } else au.pause(); });
    au.addEventListener('play', function () { pl.classList.add('playing'); play.setAttribute('aria-label', 'Pause narration'); });
    au.addEventListener('pause', function () { pl.classList.remove('playing'); play.setAttribute('aria-label', 'Play narration'); });
    au.addEventListener('error', function () { if (au.src) { failed = true; cap.textContent = 'The narration could not be loaded. The text on the page is complete.'; play.disabled = true; } });
    rateB.addEventListener('click', function () { ri = (ri + 1) % rates.length; au.playbackRate = rates[ri]; rateB.textContent = rates[ri] + '×'; rateB.setAttribute('aria-label', 'Playback speed, ' + rates[ri] + ' times'); });
    mute.addEventListener('click', function () { au.muted = !au.muted; mute.setAttribute('aria-pressed', au.muted ? 'true' : 'false'); });
    function setFollow(v) { following = v; follow.setAttribute('aria-pressed', v ? 'true' : 'false'); }
    follow.addEventListener('click', function () { setFollow(!following); if (following) show(curU, true); });
    seek.addEventListener('input', function () { if (au.duration) au.currentTime = seek.value / 1000 * au.duration; });
    ['wheel', 'touchmove', 'keydown'].forEach(function (ev) { addEventListener(ev, function (e) { if (ev === 'keydown' && !/^(Arrow|Page|Home|End| )/.test(e.key)) return; if (!au.paused && following && Date.now() > autoScroll) setFollow(false); }, { passive: true }); });
    function show(i, force) {
      if (i < 0 || !units[i]) return;
      var el = doc.querySelector('[data-n="' + units[i].n + '"]'); if (!el) return;
      var txt = el.textContent.replace(/\s+/g, ' ').trim(); cap.textContent = txt.length > 220 ? txt.slice(0, 217).replace(/\s\S*$/, '') + '…' : txt;
      var prev = doc.querySelector('.nq-on'); if (prev) prev.classList.remove('nq-on'); el.classList.add('nq-on');
      if (following || force) { var r = el.getBoundingClientRect(), target = window.scrollY + r.top - L.h * (el.closest('.step') && L.P ? .6 : .38); autoScroll = Date.now() + 1200; window.scrollTo({ top: target, behavior: RM ? 'auto' : 'smooth' }); }
    }
    au.addEventListener('timeupdate', function () {
      var t = au.currentTime, i = curU < 0 ? 0 : curU;
      if (units.length) { if (units[i] && units[i].t > t) i = 0; while (i + 1 < units.length && units[i + 1].t <= t) i++; if (i !== curU) { curU = i; show(i); } }
      if (au.duration) { seek.value = Math.round(t / au.duration * 1000); tm.textContent = fmt(t) + ' / ' + fmt(au.duration); }
    });
  }
})();
