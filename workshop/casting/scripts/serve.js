#!/usr/bin/env node
/* =====================================================================
   serve.js — zero-dependency local preview.

       npm run serve        then open http://localhost:8080/statues

   Mirrors the two Netlify redirects so /statues and /statues/NFC-0001
   behave locally exactly as they do once deployed.
   ===================================================================== */

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { ROOT } from './lib/util.js';

const PORT = Number(process.argv[2] || process.env.PORT || 8080);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};

async function resolve(urlPath) {
  const clean = decodeURIComponent(urlPath.split('?')[0]);

  /* Block traversal above the repo root. */
  const abs = path.join(ROOT, path.normalize(clean).replace(/^(\.\.[/\\])+/, ''));
  if (!abs.startsWith(ROOT)) return null;

  try {
    const info = await stat(abs);
    if (info.isDirectory()) {
      const index = path.join(abs, 'index.html');
      await stat(index);
      return index;
    }
    return abs;
  } catch { /* fall through to the redirects */ }

  /* /statues and /statues/:id both serve the gallery. */
  if (/^\/statues(\/[^/]*)?\/?$/.test(clean)) {
    return path.join(ROOT, 'statues/index.html');
  }
  return null;
}

/* Emulate Netlify's Image CDN locally so the preview behaves like the
   deployed site instead of silently falling back to full-size masters.
   Supports the parameters the gallery actually sends: w, q, fm, fit. */
/* Resizing a 2560px master costs real CPU, and a grid of cards fires many
   at once. Cache by full request key so the preview stays responsive. */
const tCache = new Map();

async function transform(req, res, url) {
  const params = url.searchParams;
  const src = params.get('url');
  if (!src) { res.writeHead(400).end('missing url'); return; }

  const abs = path.join(ROOT, decodeURIComponent(src).replace(/^\//, ''));
  if (!abs.startsWith(ROOT)) { res.writeHead(403).end('forbidden'); return; }

  let sharp;
  try {
    ({ default: sharp } = await import('sharp'));
  } catch {
    /* No sharp available — redirect to the original so the page still works. */
    res.writeHead(302, { location: src }).end();
    return;
  }

  const width = Number(params.get('w')) || null;
  const quality = Number(params.get('q')) || 82;

  /* Netlify negotiates the format from Accept when none is forced. */
  const accept = req.headers.accept || '';
  const fm = params.get('fm')
    || (accept.includes('image/avif') ? 'avif'
      : accept.includes('image/webp') ? 'webp' : 'jpeg');

  const key = `${abs}|${width}|${quality}|${fm}`;

  try {
    let body = tCache.get(key);
    if (!body) {
      let pipe = sharp(abs, { failOn: 'none' }).rotate();
      if (width) pipe = pipe.resize({ width, withoutEnlargement: true });
      pipe = fm === 'avif' ? pipe.avif({ quality })
        : fm === 'webp' ? pipe.webp({ quality })
        : fm === 'png' ? pipe.png()
        : pipe.jpeg({ quality, mozjpeg: true });

      body = await pipe.toBuffer();
      if (tCache.size > 400) tCache.clear();
      tCache.set(key, body);
    }

    res.writeHead(200, {
      'content-type': `image/${fm === 'jpeg' ? 'jpeg' : fm}`,
      'cache-control': 'public, max-age=60',
      'x-transform': `local-emulation w=${width || 'auto'} fm=${fm}`,
    });
    res.end(body);
  } catch (err) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end(`image transform failed: ${err.message}`);
  }
}

createServer(async (req, res) => {
  const url = new URL(req.url || '/', 'http://localhost');
  if (url.pathname === '/.netlify/images') return transform(req, res, url);

  const file = await resolve(req.url || '/');
  if (!file) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    return res.end('404 — not found');
  }
  try {
    const body = await readFile(file);
    res.writeHead(200, {
      'content-type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'cache-control': 'no-cache',
    });
    res.end(body);
  } catch (err) {
    res.writeHead(500, { 'content-type': 'text/plain' });
    res.end(`500 — ${err.message}`);
  }
}).listen(PORT, () => {
  console.log(`\n  Noble Father Creations — local preview`);
  console.log(`  http://localhost:${PORT}/statues\n`);
});
