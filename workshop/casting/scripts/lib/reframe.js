/* =====================================================================
   reframe.js — put every piece at the same apparent size, and give each
   photograph a gentle, consistent tone.

   The pieces are shot on black velvet, which means two things can be
   relied on: the backdrop is dark and almost completely desaturated,
   while the work itself is hand-painted and therefore is not. Detecting
   on saturation separates them cleanly where an edge-detect or a plain
   trim() does not — the velvet has folds and a visible horizon, so it is
   nowhere near uniform enough for sharp's own trim to find anything.

   Scattered bright specks in the velvet still pass a saturation test, so
   the mask is reduced to its largest connected component. That is the
   piece; everything else is noise.
   ===================================================================== */

const ANALYSIS_WIDTH = 180;   // detection raster; small is plenty and fast

export const REFRAME = {
  /* Share of the output's shorter dimension the piece should occupy.
     0.72 leaves a margin that reads as deliberate rather than cramped. */
  targetFill: 0.72,
  /* Objects sit on a surface, so a little more room above than below
     looks natural — 0.47 places the subject centre just above middle. */
  verticalAnchor: 0.47,
  aspect: 3 / 4,              // width / height, matching iPhone vertical
  minSaturation: 0.34,
  minBrightness: 55,
  /* If the piece is this small or this large a share of frame, the
     detection is probably wrong and the original framing is kept. */
  minPlausible: 0.005,
  maxPlausible: 0.80,
};

/**
 * Dimensions the photograph actually has once EXIF rotation is applied.
 *
 * sharp's metadata() reports the stored dimensions, NOT the displayed
 * ones — an iPhone portrait shot is stored 4032x3024 with orientation 6.
 * Scaling a detection box by the stored size puts the crop in the wrong
 * place entirely, so every consumer needs the rotated size.
 */
export function displaySize(meta) {
  const swapped = meta.orientation >= 5 && meta.orientation <= 8;
  return swapped
    ? { width: meta.height, height: meta.width }
    : { width: meta.width, height: meta.height };
}

/**
 * Locate the piece within a photograph.
 * @returns {{x,y,w,h,fill,srcW,srcH}|null} in displayed pixels, or null
 */
export async function findSubject(sharp, srcAbs) {
  const { data, info } = await sharp(srcAbs, { failOn: 'none' })
    .rotate()
    .resize({ width: ANALYSIS_WIDTH })
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const W = info.width, H = info.height;
  const on = new Uint8Array(W * H);

  for (let p = 0, i = 0; p < W * H; p++, i += 3) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    const sat = mx === 0 ? 0 : (mx - mn) / mx;
    on[p] = (sat > REFRAME.minSaturation && mx > REFRAME.minBrightness) ? 1 : 0;
  }

  /* Largest connected component, iterative flood fill. */
  const seen = new Uint8Array(W * H);
  let best = null;
  const stack = [];

  for (let p0 = 0; p0 < W * H; p0++) {
    if (!on[p0] || seen[p0]) continue;
    stack.length = 0;
    stack.push(p0);
    seen[p0] = 1;
    let n = 0, minX = W, minY = H, maxX = 0, maxY = 0;

    while (stack.length) {
      const c = stack.pop();
      n++;
      const x = c % W, y = (c / W) | 0;
      if (x < minX) minX = x;
      if (x > maxX) maxX = x;
      if (y < minY) minY = y;
      if (y > maxY) maxY = y;
      if (x > 0     && on[c - 1] && !seen[c - 1]) { seen[c - 1] = 1; stack.push(c - 1); }
      if (x < W - 1 && on[c + 1] && !seen[c + 1]) { seen[c + 1] = 1; stack.push(c + 1); }
      if (y > 0     && on[c - W] && !seen[c - W]) { seen[c - W] = 1; stack.push(c - W); }
      if (y < H - 1 && on[c + W] && !seen[c + W]) { seen[c + W] = 1; stack.push(c + W); }
    }
    if (!best || n > best.n) best = { n, minX, minY, maxX, maxY };
  }

  if (!best) return null;

  const fill = best.n / (W * H);
  if (fill < REFRAME.minPlausible || fill > REFRAME.maxPlausible) return null;

  const meta = await sharp(srcAbs, { failOn: 'none' }).metadata();
  const { width: srcW, height: srcH } = displaySize(meta);
  const sx = srcW / W, sy = srcH / H;

  return {
    x: Math.round(best.minX * sx),
    y: Math.round(best.minY * sy),
    w: Math.round((best.maxX - best.minX + 1) * sx),
    h: Math.round((best.maxY - best.minY + 1) * sy),
    fill, srcW, srcH,
  };
}

/**
 * Work out the 3:4 crop that centres the piece at a consistent scale.
 * Returns a region clamped to the source, plus how much padding is needed
 * on each side when the ideal crop runs off the edge.
 */
export function planCrop(subject, srcW, srcH) {
  const { targetFill, verticalAnchor, aspect } = REFRAME;

  /* Size the frame so the piece's longest dimension lands on target. */
  const byH = subject.h / targetFill;
  const byW = subject.w / targetFill / aspect;
  let outH = Math.max(byH, byW);
  let outW = outH * aspect;

  /* Never ask for more than the source can give in both directions. */
  const cap = Math.min(srcW / aspect, srcH);
  if (outH > cap) { outH = cap; outW = outH * aspect; }

  const cx = subject.x + subject.w / 2;
  const cy = subject.y + subject.h / 2;

  let left = Math.round(cx - outW / 2);
  let top = Math.round(cy - outH * verticalAnchor);

  left = Math.max(0, Math.min(left, srcW - Math.round(outW)));
  top = Math.max(0, Math.min(top, srcH - Math.round(outH)));

  return {
    left, top,
    width: Math.min(Math.round(outW), srcW - left),
    height: Math.min(Math.round(outH), srcH - top),
  };
}

/**
 * Gentle, adaptive tone. These photographs are shot dark on velvet, so
 * the aim is to lift the piece without ever letting the backdrop turn
 * grey — a flat brightness bump would wash the velvet out and destroy
 * the sense of the object sitting in its own pool of light.
 */
export async function toneCurve(pipeline, sharp, srcAbs) {
  const stats = await sharp(srcAbs, { failOn: 'none' }).rotate().stats();
  const chans = stats.channels.slice(0, 3);
  const mean = chans.reduce((a, c) => a + c.mean, 0) / 3 / 255;

  /* Darker frames get more lift, bright ones almost none. */
  const brightness = Math.min(1.16, Math.max(1.0, 1 + (0.34 - mean) * 0.55));
  /* Hand-painted work benefits from a touch of saturation; too much and
     the resin reads as plastic. */
  const saturation = 1.07;

  return pipeline
    .modulate({ brightness, saturation })
    /* A mild S-curve: deepen the black point so the velvet stays velvet,
       without clipping detail out of the piece itself. */
    .linear(1.06, -6)
    .sharpen({ sigma: 0.7, m1: 0.4, m2: 0.25 });
}
