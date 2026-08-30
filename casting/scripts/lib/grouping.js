/* =====================================================================
   grouping.js — decides which photographs belong to the same statue.

   Preferred convention (fully automatic):
       NFC-0001_front.jpg
       NFC-0001_back.jpg     → one piece, id NFC-0001, two angles

   Also understood:
       dragon-01_left.png, dragon-01-2.jpg, IMG_4821.jpeg

   When filenames carry no usable grouping signal at all the files are
   chunked sequentially instead and every resulting piece is flagged
   needsReview, so nothing is silently mis-grouped.
   ===================================================================== */

import path from 'node:path';
import { slugify } from './util.js';

export const IMAGE_EXT = new Set([
  '.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif', '.avif',
]);

/* Words that name a camera angle rather than a piece. */
const ANGLE_WORDS = [
  'front', 'back', 'rear', 'left', 'right', 'side', 'top', 'bottom',
  'base', 'detail', 'close', 'closeup', 'macro', 'angle', 'three-quarter',
  'threequarter', 'quarter', 'profile', 'full', 'main', 'hero', 'lit', 'glow',
  'dark', 'night', 'day',
];

const ANGLE_RE = new RegExp(
  `^(?<group>.+?)[\\s._-]+(?<angle>(?:${ANGLE_WORDS.join('|')})(?:[\\s._-]*\\d+)?)$`, 'i');

/* Trailing counter: "dragon-01-2" → group "dragon-01", angle "2".
   Requires a separator so "NFC-0001" itself is never split. */
const NUMBER_RE = /^(?<group>.+?)[\s._-]+(?<angle>\d{1,2})$/;

/* A filename that is already a piece id, e.g. NFC-0007. */
const ID_RE = /^([A-Za-z]{2,6})[\s._-]?(\d{2,6})$/;

/**
 * Parse one filename into a grouping decision.
 * `confident` is false when the name gave us nothing to group on.
 */
export function parseName(filename) {
  const base = path.basename(filename, path.extname(filename)).trim();

  let m = base.match(ANGLE_RE);
  if (m) {
    return {
      group: m.groups.group.trim(),
      angle: slugify(m.groups.angle),
      confident: true,
    };
  }

  m = base.match(NUMBER_RE);
  if (m) {
    /* "IMG_4821" is a camera counter, not an angle — four or more digits
       after a bare prefix means the whole name identifies one photo. */
    if (m.groups.angle.length <= 2) {
      return {
        group: m.groups.group.trim(),
        angle: `view-${m.groups.angle}`,
        confident: true,
      };
    }
  }

  /* A bare name carries no angle signal at all. It still becomes its own
     piece, but the caller is told the grouping was a guess. */
  return { group: base, angle: 'main', confident: false };
}

/**
 * Does this basename name an existing piece, e.g. "NFC-0001"?
 *
 * Only the collection's own id prefix counts. Camera filenames such as
 * IMG_4821 or DSC_0093 look structurally identical, so matching on shape
 * alone would turn every camera dump into a bogus id.
 */
export function looksLikeId(name, prefix) {
  const m = String(name).match(ID_RE);
  if (!m) return null;
  if (!prefix || m[1].toUpperCase() !== String(prefix).toUpperCase()) return null;
  return `${m[1].toUpperCase()}-${m[2]}`;
}

/**
 * Group a list of files into pieces.
 *
 * @param {{abs:string, rel:string, folder:string}[]} files
 * @param {{groupSize:number}} opts  chunk size for the sequential fallback
 * @returns {{key:string, folder:string, files:object[], needsReview:boolean}[]}
 */
export function groupFiles(files, { groupSize = 1 } = {}) {
  /* Files are grouped within their folder, so two different themes can
     both contain a "front.jpg" without colliding. */
  const byFolder = new Map();
  for (const f of files) {
    if (!byFolder.has(f.folder)) byFolder.set(f.folder, []);
    byFolder.get(f.folder).push(f);
  }

  const groups = [];

  for (const [folder, folderFiles] of byFolder) {
    const parsed = folderFiles.map(f => ({ ...f, ...parseName(f.rel) }));

    /* Provisional grouping by the parsed prefix. */
    const buckets = new Map();
    for (const p of parsed) {
      const key = p.group.toLowerCase();
      if (!buckets.has(key)) buckets.set(key, []);
      buckets.get(key).push(p);
    }

    /* Is the naming actually telling us anything? It is if some names
       carried an explicit angle word, or if any prefix collected more
       than one photo. Otherwise every file looks unrelated and we fall
       back to sequential chunks. */
    const anyConfident = parsed.some(p => p.confident);
    const anyMultiFile = [...buckets.values()].some(b => b.length > 1);
    const usable = anyConfident || anyMultiFile;

    if (usable) {
      for (const [key, items] of buckets) {
        items.sort((a, b) => a.rel.localeCompare(b.rel, undefined, { numeric: true }));
        groups.push({
          key: items[0].group,
          folder,
          files: items,
          /* A lone photo whose name gave no signal still gets its own
             piece, but is flagged so it can be checked by eye. */
          needsReview: items.length === 1 && !items[0].confident,
        });
      }
    } else {
      const sorted = [...parsed].sort(
        (a, b) => a.rel.localeCompare(b.rel, undefined, { numeric: true }));
      const size = Math.max(1, groupSize);
      for (let i = 0; i < sorted.length; i += size) {
        const chunk = sorted.slice(i, i + size);
        groups.push({
          key: chunk[0].group,
          folder,
          files: chunk.map((c, j) => ({ ...c, angle: j === 0 ? 'main' : `view-${j + 1}` })),
          needsReview: true,
        });
      }
    }
  }

  /* Stable order: folder first, then natural filename order. */
  groups.sort((a, b) =>
    a.folder.localeCompare(b.folder) ||
    a.key.localeCompare(b.key, undefined, { numeric: true }));

  return groups;
}

/* Angles render in a sensible order rather than alphabetically. */
const ANGLE_ORDER = ['main', 'hero', 'front', 'three-quarter', 'profile', 'side',
  'left', 'right', 'back', 'rear', 'top', 'bottom', 'base', 'detail', 'closeup'];

export function sortAngles(angles) {
  return [...angles].sort((a, b) => {
    const ai = ANGLE_ORDER.indexOf(a.label ?? a);
    const bi = ANGLE_ORDER.indexOf(b.label ?? b);
    if (ai !== -1 || bi !== -1) return (ai === -1 ? 99 : ai) - (bi === -1 ? 99 : bi);
    return String(a.label ?? a).localeCompare(String(b.label ?? b), undefined, { numeric: true });
  });
}
