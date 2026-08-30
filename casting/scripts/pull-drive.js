#!/usr/bin/env node
/* =====================================================================
   pull-drive.js — sync photographs from a Google Drive folder into
   incoming/, ready for `npm run ingest`.

       npm run pull                 sync, then show what would be ingested
       npm run pull -- --ingest     sync and ingest in one go
       npm run pull -- --dry-run    list what would come down

   WHY rclone RATHER THAN THE DRIVE API
     Bulk-downloading hundreds of large photos needs resumable transfers,
     retry on flaky connections, and change detection so a second run only
     fetches what is new. rclone does all of that and is a single binary.
     Writing it against the raw Drive API would mean an OAuth flow, a GCP
     project, pagination, and hand-rolled retry logic — considerably more
     to set up and to keep working.

   ONE-TIME SETUP
     1. Install rclone:  https://rclone.org/downloads/
                         macOS:  brew install rclone
                         Windows: winget install Rclone.Rclone
     2. Connect Drive:   rclone config
                         n) new remote
                         name> gdrive
                         Storage> drive
                         ...accept the defaults, and it opens a browser
                         so you can grant access.
     3. Point this script at your folder — either edit DEFAULTS below, or:
                         npm run pull -- --folder "Statue Photos"

   The folder is read but never written to. Nothing in Drive is modified
   or deleted, so the originals stay exactly as you left them.
   ===================================================================== */

import { spawn } from 'node:child_process';
import { readdir, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

import { PATHS, ROOT, say, parseArgs } from './lib/util.js';
import { IMAGE_EXT } from './lib/grouping.js';

const args = parseArgs();

const DEFAULTS = {
  /* The rclone remote name you chose during `rclone config`. */
  remote: 'gdrive',
  /* Folder inside Drive holding the photographs. Subfolders are kept,
     and the ingest script turns each one into a category. */
  folder: 'Statue Photos',
};

const CONFIG = {
  remote: args.remote || process.env.NFC_DRIVE_REMOTE || DEFAULTS.remote,
  folder: args.folder || process.env.NFC_DRIVE_FOLDER || DEFAULTS.folder,
  dryRun: args['dry-run'] === true,
  thenIngest: args.ingest === true,
};

function run(cmd, argv, { capture = false } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, argv, {
      stdio: capture ? ['ignore', 'pipe', 'pipe'] : 'inherit',
      cwd: ROOT,
    });
    let out = '', err = '';
    if (capture) {
      child.stdout.on('data', d => { out += d; });
      child.stderr.on('data', d => { err += d; });
    }
    child.on('error', reject);
    child.on('close', code => code === 0
      ? resolve(out)
      : reject(new Error(`${cmd} exited ${code}${err ? `\n${err.trim()}` : ''}`)));
  });
}

async function haveRclone() {
  try { await run('rclone', ['version'], { capture: true }); return true; }
  catch { return false; }
}

async function remoteExists(remote) {
  try {
    const out = await run('rclone', ['listremotes'], { capture: true });
    return out.split('\n').map(s => s.trim()).includes(`${remote}:`);
  } catch { return false; }
}

async function countImages(dir) {
  if (!existsSync(dir)) return 0;
  let n = 0;
  for (const e of await readdir(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue;
    if (e.isDirectory()) n += await countImages(path.join(dir, e.name));
    else if (IMAGE_EXT.has(path.extname(e.name).toLowerCase())) n++;
  }
  return n;
}

async function main() {
  say.head('Pulling photographs from Google Drive');

  if (!await haveRclone()) {
    say.err('rclone is not installed.');
    say.info('Install it, then run `rclone config` once to connect Drive:');
    say.dim('  macOS    brew install rclone');
    say.dim('  Windows  winget install Rclone.Rclone');
    say.dim('  Linux    curl https://rclone.org/install.sh | sudo bash');
    say.info('Setup instructions are at the top of scripts/pull-drive.js');
    process.exit(1);
  }

  if (!await remoteExists(CONFIG.remote)) {
    say.err(`rclone has no remote named "${CONFIG.remote}".`);
    say.info('Run `rclone config` to create one, or pass --remote <name>.');
    say.dim('Existing remotes: ' +
      ((await run('rclone', ['listremotes'], { capture: true })).trim() || 'none'));
    process.exit(1);
  }

  const source = `${CONFIG.remote}:${CONFIG.folder}`;
  say.info(`Source      ${source}`);
  say.info(`Destination ${path.relative(ROOT, PATHS.incoming)}/`);

  await mkdir(PATHS.incoming, { recursive: true });
  const before = await countImages(PATHS.incoming);

  /* Only photographs come down; Drive's own sidecar files and any stray
     documents are left behind. --ignore-existing keeps a second run cheap. */
  const filters = [];
  for (const ext of IMAGE_EXT) {
    filters.push('--include', `*${ext}`, '--include', `*${ext.toUpperCase()}`);
  }

  const rcloneArgs = [
    CONFIG.dryRun ? 'copy' : 'copy',
    source,
    PATHS.incoming,
    ...filters,
    '--ignore-existing',
    '--transfers', '8',
    '--retries', '5',
    '--low-level-retries', '10',
    '--progress',
    '--stats-one-line',
  ];
  if (CONFIG.dryRun) rcloneArgs.push('--dry-run');

  say.step(`rclone ${rcloneArgs.slice(0, 3).join(' ')} …`);
  try {
    await run('rclone', rcloneArgs);
  } catch (err) {
    say.err(err.message);
    say.info('If the folder name is wrong, list what is there with:');
    say.dim(`  rclone lsd ${CONFIG.remote}:`);
    process.exit(1);
  }

  if (CONFIG.dryRun) { say.warn('Dry run — nothing downloaded'); return; }

  const after = await countImages(PATHS.incoming);
  const added = after - before;

  say.head('Sync complete');
  say.ok(`${added} new photograph${added === 1 ? '' : 's'} downloaded`);
  say.info(`${after} total waiting in incoming/`);

  if (!added) {
    say.dim('Nothing new in Drive since the last pull.');
    return;
  }

  if (CONFIG.thenIngest) {
    say.head('Ingesting');
    await run(process.execPath, [path.join(ROOT, 'scripts/ingest-images.js')]);
  } else {
    say.info('Next:  npm run ingest');
  }
}

main().catch(err => { say.err(err.stack || err.message); process.exit(1); });
