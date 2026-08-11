#!/usr/bin/env node
/* =====================================================================
   build-pages.js — generate a real, crawlable page for every piece.

       npm run pages           build them all
       npm run pages -- --force  rebuild social cards that already exist

   WHY THIS EXISTS
     Facebook, TikTok, Pinterest, iMessage and every other link-preview
     crawler reads the raw HTML a URL returns. None of them run
     JavaScript. A gallery that renders client-side therefore previews
     identically no matter which piece is shared — one thousand statues,
     one preview card — which for a business whose funnel is social is
     the most expensive thing the site could get wrong.

     So each piece gets a real file at statues/<id>/index.html carrying
     its own <title>, og:image and visible content, plus a 1200x630
     social card rendered from its photograph.

   WHY NOT A FRAMEWORK
     This runs on the same machine, in the same command, as the ingest.
     Netlify's build command stays empty, so nothing can fail at deploy
     time because nothing runs at deploy time. If this script breaks it
     breaks here, before the push, where it can be read and fixed.
   ===================================================================== */

import { mkdir, writeFile, rm, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

import { PATHS, ROOT, say, readJSON, parseArgs } from './lib/util.js';
import { primaryAxis, findValue, trailFor, labelFor } from './lib/facets.js';

const args = parseArgs();
const FORCE = args.force === true;

let sharp;
try { ({ default: sharp } = await import('sharp')); }
catch { say.err('sharp is not installed. Run: npm install'); process.exit(1); }

const OUT = path.join(ROOT, 'statues');
const CARDS = path.join(ROOT, 'assets/images/social');

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

/* ------------------------------------------------------------------ */
/*  Social card: 1200x630, the format every platform crops toward      */
/* ------------------------------------------------------------------ */

/**
 * A 3:4 portrait photo cannot fill a 1.91:1 landscape card without being
 * destroyed, so the card is built the way broadcast does it: the photo
 * blurred and darkened as a full-bleed ground, with the undistorted
 * photograph standing on top of it.
 */
async function buildCard(masterAbs, outAbs) {
  const W = 1200, H = 630;

  const backdrop = await sharp(masterAbs, { failOn: 'none' })
    .rotate()
    .resize(W, H, { fit: 'cover', position: 'centre' })
    .blur(28)
    .modulate({ brightness: 0.45, saturation: 1.1 })
    .composite([{
      /* A flat scrim over the blur. Without it a pale piece on a pale
         backdrop has no edge, and the card reads as a smear. */
      input: { create: { width: W, height: H, channels: 4,
                         background: { r: 10, g: 10, b: 12, alpha: 0.42 } } },
      blend: 'over',
    }])
    .toBuffer();

  /* Leave a margin so the piece never touches the card edge, and so
     platform-specific crops still land inside the photograph. */
  const inner = await sharp(masterAbs, { failOn: 'none' })
    .rotate()
    .resize({ height: H - 56, fit: 'inside', withoutEnlargement: false })
    .toBuffer();

  await sharp(backdrop)
    .composite([{ input: inner, gravity: 'centre' }])
    .jpeg({ quality: 82, mozjpeg: true })   // JPEG: crawlers handle it universally
    .toFile(outAbs);
}

/* ------------------------------------------------------------------ */
/*  Page                                                               */
/* ------------------------------------------------------------------ */

function facetTrail(facets, piece) {
  const out = [];
  for (const axis of facets) {
    const v = piece.facets?.[axis.key];
    if (!v) continue;
    out.push({ axis, path: v, labels: trailFor(axis, v) });
  }
  return out;
}

function pageHTML({ site, piece, facets, cardURL, master }) {
  const title = piece.title || `Piece ${piece.id}`;
  const trail = facetTrail(facets, piece);

  const descr = piece.description
    || [title, ...trail.map(t => t.labels.join(' › '))].filter(Boolean).join(' · ')
       + ` — hand-poured eco-resin, hand-painted finish. ${site.name}.`;

  const url = `${site.url}/statues/${piece.id}/`;
  const img = `${site.url}${cardURL}`;
  const photo = `${site.url}${master}`;

  const crumbs = trail.map(t =>
    `<a href="/statues/?${t.axis.key}=${encodeURIComponent(t.path)}">${esc(t.labels.join(' › '))}</a>`
  ).join('<span class="sep">·</span>');

  const jsonld = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: title,
    sku: piece.id,
    image: [photo],
    description: descr,
    brand: { '@type': 'Brand', name: site.name },
    url,
    ...(piece.tags?.length ? { keywords: piece.tags.join(', ') } : {}),
  };

  /* Open Graph tags go immediately after <meta charset>: Facebook parses
     only roughly the first 60 KB of a document, so they must precede the
     stylesheets and everything else. */
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="${esc(site.name)}" />
<meta property="og:title" content="${esc(title)}" />
<meta property="og:description" content="${esc(descr)}" />
<meta property="og:url" content="${esc(url)}" />
<meta property="og:image" content="${esc(img)}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="${esc(title)}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${esc(title)}" />
<meta name="twitter:description" content="${esc(descr)}" />
<meta name="twitter:image" content="${esc(img)}" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>${esc(title)} — ${esc(site.name)}</title>
<meta name="description" content="${esc(descr)}" />
<link rel="canonical" href="${esc(url)}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,400&family=Jost:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/assets/css/theme.css" />
<link rel="stylesheet" href="/assets/css/piece.css" />
<script type="application/ld+json">${JSON.stringify(jsonld)}</script>
</head>
<body>

<div class="topbar">
  <a class="menu-btn" href="/statues/" aria-label="Back to the collection">‹</a>
  <span class="tb-mark">Noble <b>Father</b> Creations</span>
</div>

<main class="piece-page">
  <figure class="pp-figure" style="--tile-bg:${esc(piece.angles[0].bg || '#101015')}">
    <img src="${esc(master)}" alt="${esc(title)}"
         ${piece.angles[0].width ? `width="${piece.angles[0].width}"` : ''}
         ${piece.angles[0].height ? `height="${piece.angles[0].height}"` : ''}
         fetchpriority="high" decoding="async" />
  </figure>

  <div class="pp-body">
    <p class="pp-id">${esc(piece.id)}</p>
    <h1>${esc(title)}</h1>
    ${crumbs ? `<nav class="pp-crumbs">${crumbs}</nav>` : ''}
    ${piece.description ? `<p class="pp-desc">${esc(piece.description)}</p>` : ''}
    ${piece.tags?.length
      ? `<ul class="pp-tags">${piece.tags.map(t => `<li>${esc(t)}</li>`).join('')}</ul>`
      : ''}

    <div class="links">
      <a class="btn g" href="mailto:${esc(site.email)}?subject=${
        encodeURIComponent(`Enquiry — ${piece.id}${piece.title ? ` (${piece.title})` : ''}`)
      }&body=${encodeURIComponent(`I'm interested in this piece:\n${url}\n\n`)}">Enquire about this piece</a>
      <a class="btn o" href="/statues/">See the whole collection</a>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <div class="mk">${esc(site.name)}</div>
    <div class="hd">${esc(site.tagline)}</div>
  </div>
</footer>

</body>
</html>
`;
}

/* ------------------------------------------------------------------ */

async function main() {
  say.head('Building per-piece pages');

  const site = await readJSON(PATHS.site, null);
  if (!site?.url) { say.err('data/site.json needs a "url".'); process.exit(1); }

  const statues = await readJSON(PATHS.statues, []);
  const facets = await readJSON(PATHS.facets, []);

  if (!statues.length) {
    say.warn('No pieces yet — run npm run ingest first.');
    return;
  }

  await mkdir(CARDS, { recursive: true });

  /* Remove pages for pieces that no longer exist, so a deleted piece
     does not linger as a live URL. */
  const live = new Set(statues.map(s => s.id));
  if (existsSync(OUT)) {
    for (const e of await readdir(OUT, { withFileTypes: true })) {
      if (e.isDirectory() && /^[A-Z]+-\d+$/i.test(e.name) && !live.has(e.name)) {
        await rm(path.join(OUT, e.name), { recursive: true, force: true });
        say.dim(`removed stale page ${e.name}`);
      }
    }
  }

  let pages = 0, cards = 0, failed = 0;

  for (const piece of statues) {
    const angle = piece.angles?.[0];
    if (!angle?.master) { say.warn(`${piece.id} has no image — skipped`); continue; }

    const masterAbs = path.join(ROOT, angle.master.replace(/^\//, ''));
    const cardRel = `/assets/images/social/${piece.id}.jpg`;
    const cardAbs = path.join(ROOT, cardRel.replace(/^\//, ''));

    try {
      if (FORCE || !existsSync(cardAbs)) {
        if (!existsSync(masterAbs)) throw new Error(`master missing: ${angle.master}`);
        await buildCard(masterAbs, cardAbs);
        cards++;
      }

      const dir = path.join(OUT, piece.id);
      await mkdir(dir, { recursive: true });
      await writeFile(
        path.join(dir, 'index.html'),
        pageHTML({ site, piece, facets, cardURL: cardRel, master: angle.master }),
        'utf8');
      pages++;
    } catch (err) {
      failed++;
      say.err(`${piece.id} — ${err.message}`);
    }
  }

  /* sitemap.xml — without it Google has no way to discover the pieces,
     since the gallery index builds its links in the browser. */
  const urls = [
    `${site.url}/`,
    `${site.url}/statues/`,
    ...statues.map(s => `${site.url}/statues/${s.id}/`),
  ];
  await writeFile(path.join(ROOT, 'sitemap.xml'),
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    urls.map(u => `  <url><loc>${esc(u)}</loc></url>`).join('\n') +
    `\n</urlset>\n`, 'utf8');

  await writeFile(path.join(ROOT, 'robots.txt'),
    `User-agent: *\nAllow: /\n\nSitemap: ${site.url}/sitemap.xml\n`, 'utf8');

  say.head('Done');
  say.ok(`${pages} page(s), ${cards} new social card(s)`);
  if (failed) say.warn(`${failed} piece(s) failed`);
  say.info(`sitemap.xml lists ${urls.length} URL(s)`);
}

main().catch(err => { say.err(err.stack || err.message); process.exit(1); });
