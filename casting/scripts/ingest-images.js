#!/usr/bin/env node
/* =====================================================================
   ingest-images.js — turn a folder of raw photographs into gallery data.

   USAGE
     npm run ingest                     process everything in incoming/
     npm run ingest:dry                 show the plan, write nothing
     node scripts/ingest-images.js --set form=jar
     node scripts/ingest-images.js --replace        overwrite existing masters
     node scripts/ingest-images.js --no-folder-facets

   WHAT IT DOES
     1. Walks incoming/ (including subfolders) for photographs.
     2. Reads the folder path as facet values. `Pets/Cats/Incense Burners`
        files a piece as subject=pets/cats AND form=incense-burner —
        folders are matched by slug or by human label, and an unrecognised
        folder is registered as a new subject rather than dropped.
     3. Writes one high-quality WebP master per photo to
        assets/images/statues/{id}/, and samples the photo's dominant
        colour so each tile can be painted from the work itself.
     4. Appends new pieces to data/statues.json and extends
        data/facets.json with anything new.

   SAFETY
     · Every source photo is recorded in data/.ingest-manifest.json by
       content hash, so re-running skips what is already in — even after
       renaming — and duplicates within one batch collapse to one piece.
     · A photo that cannot be read is reported and skipped; the rest of
       the batch still lands. Progress is flushed to disk every 25 pieces
       and again on exit, so a crash never discards completed work.
     · An existing master is never silently overwritten (Netlify serves
       them immutable), unless --replace is passed.
     · HEIC/HEIF is detected and reported: this sharp build cannot decode
       it. Shoot JPEG — on iPhone, Settings > Camera > Formats > "Most
       Compatible".
   ===================================================================== */

import { readdir, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

import {
  PATHS, ROOT, say, readJSON, writeJSON, hashFile,
  slugify, titleCase, today, parseArgs,
} from './lib/util.js';
import { IMAGE_EXT, groupFiles, looksLikeId, sortAngles } from './lib/grouping.js';
import { findSegment, ensureValue, primaryAxis } from './lib/facets.js';
import { findSubject, planCrop, toneCurve } from './lib/reframe.js';

const args = parseArgs();

const CONFIG = {
  /* One high-quality master per photo is committed; every size the site
     shows is derived from it on request by Netlify's Image CDN. 2560px
     covers a full-screen view on a 1440p display and 2x zoom on a phone,
     which is as far as detail on a resin surface is worth carrying. */
  masterQuality: Number(args['quality'] || 84),

  /* Fixed widths written as real files. 600 covers a grid card at 2x,
     1200 a phone full-view at 3x, 2000 a desktop full-view at 2x. */
  sizes: (args.sizes ? String(args.sizes).split(',').map(Number) : [600, 1200, 2000])
    .filter(n => n > 0).sort((a, b) => a - b),
  idPrefix: args['id-prefix'] || 'NFC',
  idPad: 4,
  groupSize: Number(args['group-size'] || 1),
  dryRun: args['dry-run'] === true || args.n === true,
  /* Subfolder path → facet values. On by default; this is what makes
     sorting by theme a matter of dragging folders around in Drive. */
  folderFacets: args['no-folder-facets'] !== true,

  /* --set subject=pets/cats --set form=jar  forces values for the run. */
  forcedFacets: (() => {
    const raw = args.set;
    const list = Array.isArray(raw) ? raw : raw ? [raw] : [];
    const out = {};
    for (const pair of list) {
      const [k, v] = String(pair).split('=');
      if (k && v) out[k.trim()] = v.trim().toLowerCase();
    }
    return out;
  })(),

  /* Overwriting a committed master is refused unless asked for. */
  replace: args.replace === true,
  /* Auto-centre the piece and apply the tone curve. */
  reframe: args['no-reframe'] !== true,
  tone: args['no-tone'] !== true,

  /* One photograph per statue is the collection's convention, so by
     default every file is its own piece and no grouping is attempted.
     This matters: under prefix grouping, dragon-1.jpg and dragon-2.jpg
     would be read as two angles of one statue rather than two statues.
     Pass --group to photograph pieces from several sides instead. */
  onePerFile: args.group !== true,
};

let sharp;
try {
  ({ default: sharp } = await import('sharp'));
} catch {
  say.err('sharp is not installed. Run:  npm install');
  process.exit(1);
}

/* ------------------------------------------------------------------ */
/*  Discover source photographs                                        */
/* ------------------------------------------------------------------ */

async function walk(dir, base = dir) {
  if (!existsSync(dir)) return [];
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...await walk(abs, base));
    } else if (IMAGE_EXT.has(path.extname(entry.name).toLowerCase())) {
      const rel = path.relative(base, abs);
      out.push({ abs, rel, folder: path.dirname(rel) === '.' ? '' : path.dirname(rel) });
    }
  }
  return out;
}

/* One photo per statue: no grouping, no guessing, nothing to review.
   The filename identifies the piece and that is the whole convention. */
function oneGroupPerFile(files) {
  return [...files]
    .sort((a, b) => a.rel.localeCompare(b.rel, undefined, { numeric: true }))
    .map(f => ({
      key: path.basename(f.rel, path.extname(f.rel)).trim(),
      folder: f.folder,
      files: [{ ...f, angle: 'main' }],
      needsReview: false,
    }));
}

/* ------------------------------------------------------------------ */
/*  Folder path → facet values                                         */
/* ------------------------------------------------------------------ */

/**
 * Turn `incoming/Pets/Cats/Incense Burners` into
 * `{ subject: "pets/cats", form: "incense-burner" }`.
 *
 * Each folder segment is matched against every declared axis. A segment
 * that matches a hierarchical axis extends that axis's path; one that
 * matches a flat axis sets it. Segments matching nothing extend the
 * primary axis and are registered, so a subject invented at the camera
 * still lands somewhere findable rather than being dropped.
 */
function resolveFacets(facets, folder) {
  const out = { ...CONFIG.forcedFacets };
  if (!CONFIG.folderFacets || !folder) return out;

  const primary = primaryAxis(facets);

  for (const raw of folder.split(path.sep).filter(Boolean)) {
    if (!slugify(raw)) continue;

    let placed = false;

    /* Flat axes first. "Incense Burners" is a Type, and must be read as
       one even while we are partway down the Subject tree — otherwise it
       would be mistaken for a new subject nested under Pets/Cats. */
    for (const axis of facets) {
      if (axis.hierarchical || out[axis.key]) continue;
      const hit = findSegment(axis, raw);
      if (hit) { out[axis.key] = hit.path; placed = true; break; }
    }
    if (placed) continue;

    /* Then hierarchical axes, descending from wherever we already are. */
    for (const axis of facets) {
      if (!axis.hierarchical) continue;
      const under = out[axis.key] || null;
      const hit = findSegment(axis, raw, under) || findSegment(axis, raw, null);
      if (hit) { out[axis.key] = hit.path; placed = true; break; }
    }
    if (placed) continue;

    /* Genuinely unknown: nest under the primary axis and declare it, so a
       subject invented at the camera is still findable on the site. */
    if (primary) {
      const under = out[primary.key]
        ? `${out[primary.key]}/${slugify(raw)}` : slugify(raw);
      ensureValue(primary, under, { label: titleCase(raw) });
      out[primary.key] = under;
      say.ok(`New ${primary.key}: ${under}`);
    }
  }

  return out;
}

/* ------------------------------------------------------------------ */
/*  Ids                                                                */
/* ------------------------------------------------------------------ */

function nextIdFactory(existingIds) {
  const taken = new Set(existingIds.map(s => s.toUpperCase()));
  const re = new RegExp(`^${CONFIG.idPrefix}-(\\d+)$`, 'i');
  let highest = 0;

  const noteHighest = id => {
    const m = String(id).toUpperCase().match(re);
    if (m) highest = Math.max(highest, parseInt(m[1], 10));
  };
  existingIds.forEach(noteHighest);

  return {
    /* Reserve an id a filename has already claimed, so the sequential
       allocator can never hand the same id to a second piece. */
    claim(id) {
      taken.add(String(id).toUpperCase());
      noteHighest(id);
    },
    next() {
      let candidate;
      do {
        highest += 1;
        candidate = `${CONFIG.idPrefix}-${String(highest).padStart(CONFIG.idPad, '0')}`;
      } while (taken.has(candidate.toUpperCase()));
      taken.add(candidate.toUpperCase());
      return candidate;
    },
  };
}

/* ------------------------------------------------------------------ */
/*  Image processing                                                   */
/* ------------------------------------------------------------------ */

const relURL = p => '/' + path.relative(ROOT, p).split(path.sep).join('/');

/**
 * Write the image files for one photograph.
 *
 * Real files at fixed widths, not transform URLs. The site then depends on
 * nothing but a static file server, so the whole thing can be moved to any
 * host — Netlify, Cloudflare Pages, GitHub Pages, S3, a plain server — by
 * copying the folder. A CDN-transform URL would tie it to one provider.
 */
async function renderDerivatives(srcAbs, outDir, angleLabel) {
  const stem = slugify(angleLabel) || 'view';
  const widths = CONFIG.sizes;
  const largest = widths[widths.length - 1];

  const fileFor = w => path.join(outDir, `${stem}-${w}.webp`);
  const describe = () => ({
    master: relURL(fileFor(largest)),
    sizes: widths.map(w => ({ w, src: relURL(fileFor(w)) })),
  });

  if (CONFIG.dryRun) return { paths: describe(), width: null, height: null, bg: null };

  /* Never silently replace an image already on disk: it is served with a
     long cache life, so the old bytes would stay pinned at the same URL
     and the change would appear not to have worked. */
  if (existsSync(fileFor(largest)) && !CONFIG.replace) {
    throw new Error(
      `${path.relative(ROOT, fileFor(largest))} already exists — pass --replace to overwrite`);
  }

  await mkdir(outDir, { recursive: true });

  /* Locate the piece and re-frame it, so every statue ends up at a
     comparable scale in the grid rather than floating at whatever size it
     happened to be shot. */
  let region = null;
  if (CONFIG.reframe) {
    try {
      const subject = await findSubject(sharp, srcAbs);
      if (subject) region = planCrop(subject, subject.srcW, subject.srcH);
    } catch { /* framing is an enhancement; never fail an ingest for it */ }
  }

  let pipeline = sharp(srcAbs, { failOn: 'none' }).rotate();
  if (region) pipeline = pipeline.extract(region);
  if (CONFIG.tone) pipeline = await toneCurve(pipeline, sharp, srcAbs);

  /* Render the largest once, then derive the smaller widths from that
     buffer rather than re-decoding a 12-megapixel original each time. */
  const bigBuf = await pipeline
    .resize({ width: largest, withoutEnlargement: true })
    .webp({ quality: CONFIG.masterQuality })
    .toBuffer();
  await writeFile(fileFor(largest), bigBuf);

  for (const w of widths.slice(0, -1)) {
    await sharp(bigBuf)
      .resize({ width: w, withoutEnlargement: true })
      .webp({ quality: w <= 600 ? 80 : 82 })
      .toFile(fileFor(w));
  }

  const outMeta = await sharp(bigBuf).metadata();

  /* The photo's own dominant colour, darkened toward the site ground.
     Tiles are painted with it, so a piece whose framing differs from the
     3:4 house standard letterboxes into a colour drawn from itself
     rather than sitting on a hard black rectangle. */
  let bg = null;
  try {
    const { dominant } = await sharp(bigBuf).stats();
    if (dominant) {
      bg = '#' + [dominant.r, dominant.g, dominant.b]
        .map(n => Math.round(n * 0.42).toString(16).padStart(2, '0')).join('');
    }
  } catch { /* colour is a nicety; never fail an ingest over it */ }

  return {
    paths: describe(),
    width: outMeta.width,
    height: outMeta.height,
    bg,
  };
}

/* ------------------------------------------------------------------ */
/*  Main                                                               */
/* ------------------------------------------------------------------ */

async function main() {
  say.head('Noble Father Creations — image ingest');
  if (CONFIG.dryRun) say.warn('DRY RUN — no files will be written');

  const statues = await readJSON(PATHS.statues, []);
  const facets = await readJSON(PATHS.facets, []);
  const manifest = await readJSON(PATHS.manifest, { images: {} });
  manifest.images ||= {};

  const files = await walk(PATHS.incoming);
  if (!files.length) {
    say.warn(`No images found in ${path.relative(ROOT, PATHS.incoming)}/`);
    say.dim('Drop your photos there (subfolders become facets) and run again.');
    return;
  }
  say.info(`Found ${files.length} image${files.length === 1 ? '' : 's'} in incoming/`);

  /* iPhones shoot HEIC by default and this sharp build cannot decode it —
     libvips ships without the HEVC licence. Catch it here with an
     instruction rather than letting sharp throw on the first file. */
  const heic = files.filter(f => /\.hei[cf]$/i.test(f.rel));
  if (heic.length) {
    say.err(`${heic.length} HEIC/HEIF photo(s) found — this format cannot be read.`);
    say.info('On iPhone: Settings › Camera › Formats › "Most Compatible" shoots JPEG.');
    say.info('To convert what you already have, on a Mac:');
    say.dim('  sips -s format jpeg incoming/**/*.heic --out incoming/');
    say.warn('Skipping those files and continuing with the rest.');
  }
  const usable = files.filter(f => !/\.hei[cf]$/i.test(f.rel));
  if (!usable.length) return;

  /* Skip anything already ingested — this is what makes reruns safe. */
  const seen = new Set(Object.keys(manifest.images));
  const fresh = [];
  let skipped = 0;
  for (const f of usable) {
    const hash = await hashFile(f.abs);
    /* `seen` grows as we go, so two byte-identical photos in the SAME
       batch collapse to one piece rather than becoming duplicates. */
    if (seen.has(hash)) { skipped++; continue; }
    seen.add(hash);
    fresh.push({ ...f, hash });
  }
  if (skipped) say.dim(`${skipped} already ingested or duplicated — skipping`);
  if (!fresh.length) {
    say.ok('Everything in incoming/ is already in the collection. Nothing to do.');
    return;
  }

  const groups = CONFIG.onePerFile ? oneGroupPerFile(fresh)
    : groupFiles(fresh, { groupSize: CONFIG.groupSize });

  say.info(CONFIG.onePerFile
    ? `${groups.length} piece${groups.length === 1 ? '' : 's'} — one photo each`
    : `Grouped into ${groups.length} piece${groups.length === 1 ? '' : 's'}`);

  const byId = new Map(statues.map(s => [String(s.id).toUpperCase(), s]));
  const ids = nextIdFactory(statues.map(s => s.id));

  /* Resolve ids in a pass of their own. Every id claimed by a filename is
     reserved up front, so a later sequentially-numbered piece can never be
     handed an id that a NFC-0001_front.jpg in this same batch already owns. */
  for (const group of groups) {
    group.explicitId = looksLikeId(group.key, CONFIG.idPrefix);
    if (group.explicitId) ids.claim(group.explicitId);
  }
  for (const group of groups) {
    group.id = group.explicitId || ids.next();
    /* A filename that names its own piece is not a guess, whatever the
       angle parser concluded. */
    if (group.explicitId) group.needsReview = false;
  }

  let created = 0, extended = 0, flagged = 0;
  const failures = [];
  const touched = new Map();   // axis key → Set of paths introduced

  /* Progress is written to disk as we go. A 500-photo run that dies on
     photo 400 must not discard 400 photos of work, so the three JSON
     files are flushed periodically and again in `finally`. */
  const flush = async () => {
    if (CONFIG.dryRun) return;
    await writeJSON(PATHS.statues, statues);
    await writeJSON(PATHS.facets, facets);
    await writeJSON(PATHS.manifest, manifest);
  };

  try {
    for (const [n, group] of groups.entries()) {
      const id = group.id;
      const existing = byId.get(id.toUpperCase());
      const outDir = path.join(PATHS.images, id);

      /* Facet values come from the folder path: incoming/Pets/Cats/x.jpg
         files the piece at subject = "pets/cats". --set overrides. */
      const assigned = resolveFacets(facets, group.folder);

      const angles = [];
      let broke = false;

      for (const file of group.files) {
        const label = file.angle || 'main';
        try {
          const r = await renderDerivatives(file.abs, outDir, label);
          angles.push({ label, ...r.paths, width: r.width, height: r.height, bg: r.bg });
          manifest.images[file.hash] = {
            id, angle: label,
            source: file.rel.split(path.sep).join('/'),
            ingested: today(),
          };
        } catch (err) {
          /* One unreadable photo must never abort the batch. */
          broke = true;
          failures.push({ file: file.rel, reason: err.message.split('\n')[0] });
          say.err(`${file.rel} — ${err.message.split('\n')[0]}`);
        }
      }

      if (!angles.length) { if (broke) continue; }

      if (existing) {
        const have = new Set((existing.angles || []).map(a => a.label));
        const added = angles.filter(a => !have.has(a.label));
        existing.angles = sortAngles([...(existing.angles || []), ...added]);
        if (added.length) extended++;
        existing.facets = { ...assigned, ...(existing.facets || {}) };
        say.step(`${id} — added ${added.length} angle${added.length === 1 ? '' : 's'}`);
      } else {
        const entry = {
          id,
          title: null,
          facets: assigned,
          tags: [],
          angles: sortAngles(angles),
          dateAdded: today(),
          description: null,
        };
        if (group.needsReview) { entry.needsReview = true; flagged++; }
        statues.push(entry);
        byId.set(id.toUpperCase(), entry);
        created++;

        const shown = Object.entries(assigned).map(([k, v]) => `${k}=${v}`).join('  ');
        say.step(`${id} — ${shown || 'unfiled'}${group.needsReview ? '  ·  NEEDS REVIEW' : ''}`);
      }

      for (const [k, v] of Object.entries(assigned)) {
        if (!touched.has(k)) touched.set(k, new Set());
        touched.get(k).add(v);
      }

      /* Flush every 25 pieces so a crash costs at most 25 photos. */
      if ((n + 1) % 25 === 0) await flush();
    }
  } finally {
    await flush();
  }

  if (CONFIG.dryRun) {
    say.head('Dry run complete — nothing written');
    say.info(`Would create ${created} piece(s), extend ${extended}, flag ${flagged}`);
    return;
  }

  say.head('Done');
  say.ok(`${created} new piece${created === 1 ? '' : 's'}`);
  if (extended) say.ok(`${extended} existing piece(s) gained new angles`);
  for (const [key, paths] of touched) {
    say.dim(`${key}: ${[...paths].join(', ')}`);
  }
  if (flagged) say.warn(`${flagged} piece(s) flagged for review`);
  if (failures.length) {
    say.warn(`${failures.length} photo(s) could not be read and were skipped:`);
    for (const f of failures.slice(0, 10)) say.dim(`  ${f.file} — ${f.reason}`);
    if (failures.length > 10) say.dim(`  …and ${failures.length - 10} more`);
    say.info('Everything else was saved. Fix those files and run again.');
  }
  say.info(`Collection now holds ${statues.length} piece(s)`);
  say.dim('Next: file pieces with  npm run assign -- --help');
}

main().catch(err => { say.err(err.stack || err.message); process.exit(1); });
