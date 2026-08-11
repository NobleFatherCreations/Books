/* =====================================================================
   images.js — where the site gets its image URLs.

   Every size is a REAL FILE written at ingest time, referenced by a plain
   path. Nothing here depends on a CDN, an image-transform service or a
   particular host, which means the whole site is portable: copy the
   folder to Netlify, Cloudflare Pages, GitHub Pages, S3 or any plain web
   server and it works unchanged.

   An earlier version pointed at Netlify's /.netlify/images transform
   endpoint. That is a nicer pipeline in one respect — sizes retunable
   without re-processing — but it silently ties the site to one provider,
   and every photograph 404s the moment it is hosted anywhere else.
   ===================================================================== */

/* Widths the ingest writes. Kept only as a fallback for entries that
   predate the `sizes` array. */
const FALLBACK_WIDTHS = [600, 1200, 2000];

/** The largest rendition — used as a last-resort src. */
export function masterURL(angle) {
  if (!angle) return '';
  if (angle.master) return angle.master;
  const s = angle.sizes;
  return s?.length ? s[s.length - 1].src : '';
}

/** Grid card: the smallest rendition is already 2x for a ~300px tile. */
export function cardImage(angle) {
  const sizes = angle?.sizes;
  const src = sizes?.length ? sizes[0].src : masterURL(angle);
  return { src, fallback: masterURL(angle) };
}

/**
 * Full view: hand the browser every rendition and let it choose using the
 * viewport and pixel density, so a phone never downloads the 2000px file.
 */
export function detailImage(angle) {
  const sizes = angle?.sizes;
  const master = masterURL(angle);

  if (!sizes?.length) {
    return { src: master, srcset: '', sizes: '100vw', fallback: master };
  }

  return {
    src: sizes[sizes.length - 1].src,
    srcset: sizes.map(s => `${s.src} ${s.w}w`).join(', '),
    sizes: '100vw',
    fallback: master,
  };
}

/** Widths available for an angle, largest last. */
export function widthsFor(angle) {
  return angle?.sizes?.map(s => s.w) ?? FALLBACK_WIDTHS;
}
