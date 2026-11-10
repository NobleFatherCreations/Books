#!/usr/bin/env python3
"""Vendor an npm library into the repo as LOCAL files (no CDN, no runtime network), recording licence, size and checksum.
Refuses to run without the owner's approval string, because CLAUDE.md forbids adding dependencies without an explicit yes.

  python3 scripts/vendor-lib.py <npm-package> --approved-by "owner, 2026-11-10: use for <project>" [--version X] [--dest vendor] [--files dist/x.min.js,dist/y.js]

Writes <dest>/<package>/<version>/ (chosen files + LICENSE) and appends to <dest>/MANIFEST.json.
Then reference the local file from the page (inline or relative file). Never reference a CDN."""
import argparse, json, hashlib, os, subprocess, sys, tarfile, tempfile, shutil, datetime
ap = argparse.ArgumentParser()
ap.add_argument('pkg'); ap.add_argument('--approved-by', default=''); ap.add_argument('--version', default='')
ap.add_argument('--dest', default='vendor'); ap.add_argument('--files', default='')
a = ap.parse_args()
if len(a.approved_by.strip()) < 12:
    sys.exit('Refusing: pass --approved-by "<who said yes, when, for what>" (CLAUDE.md: no new dependency without an explicit yes).')
spec = a.pkg + ('@' + a.version if a.version else '')
meta = json.loads(subprocess.check_output(['npm', 'view', spec, 'name', 'version', 'license', 'dist.unpackedSize', '--json'], text=True))
tmp = tempfile.mkdtemp()
tgz = subprocess.check_output(['npm', 'pack', spec, '--pack-destination', tmp], text=True, cwd=tmp).strip().splitlines()[-1]
with tarfile.open(os.path.join(tmp, tgz)) as t:
    t.extractall(tmp, filter='data')
root = os.path.join(tmp, 'package')
out = os.path.join(a.dest, meta['name'].replace('/', '_'), meta['version']); os.makedirs(out, exist_ok=True)
want = [f for f in a.files.split(',') if f] or []
if not want:   # auto-pick: minified browser builds under dist/ or build/
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.relpath(os.path.join(dp, f), root)
            if f.endswith('.min.js') or (f.endswith('.mjs') and ('dist' in p or 'build' in p) and 'min' in f):
                want.append(p)
    want = sorted(want)[:6]
sizes = {}
if not want:
    cands = [os.path.relpath(os.path.join(dp, f), root) for dp, _, fs in os.walk(root) for f in fs if f.endswith(('.js', '.mjs', '.css')) and ('dist' in dp or 'build' in dp or 'lib' in dp)]
    print('No minified build auto-detected. Candidate files (pass with --files):', *sorted(cands)[:20], sep='\n  ')
for rel in want:
    src = os.path.join(root, rel)
    if os.path.exists(src):
        dst = os.path.join(out, os.path.basename(rel)); shutil.copy(src, dst)
        sizes[os.path.basename(rel)] = {'bytes': os.path.getsize(dst), 'sha256': hashlib.sha256(open(dst, 'rb').read()).hexdigest()}
for lic in ('LICENSE', 'LICENSE.md', 'LICENSE.txt', 'license'):
    if os.path.exists(os.path.join(root, lic)):
        shutil.copy(os.path.join(root, lic), os.path.join(out, 'LICENSE')); break
mp = os.path.join(a.dest, 'MANIFEST.json'); man = json.load(open(mp)) if os.path.exists(mp) else []
man.append({'name': meta['name'], 'version': meta['version'], 'license': meta['license'], 'files': sizes, 'approvedBy': a.approved_by, 'date': datetime.date.today().isoformat()})
json.dump(man, open(mp, 'w'), indent=1)
shutil.rmtree(tmp)
print(json.dumps(man[-1], indent=1)); print('NOTE: read the licence; GSAP-style "no charge" licences have conditions.')
