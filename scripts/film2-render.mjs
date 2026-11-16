#!/usr/bin/env node
// Render the film to MP4, frame by frame, from its clock. node scripts/film2-render.mjs <url> <out.mp4> [--from=0 --to=60 --fps=24 --vp=390x844x2 --entry=5 --crop=WxH]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'child_process';
const [url, out] = process.argv.slice(2); const arg = (k, d) => { const a = process.argv.find(a => a.startsWith('--' + k + '=')); return a ? a.split('=')[1] : d; };
const from = +arg('from', 0), to = +arg('to', 60), fps = +arg('fps', 24), entry = +arg('entry', 0); const [w, h, dpr] = arg('vp', '390x844x2').split('x').map(Number);
const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
await p.goto(url + '?capture'); await p.waitForFunction(() => window.FILM && FILM.state().ready, null, { timeout: 120000 }); await p.mouse.move(2, 2);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '25', '-pix_fmt', 'yuv420p', '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const times = []; for (let i = 0; i < entry * fps; i++) times.push(-(20 + i / fps)); for (let i = 0; i <= (to - from) * fps; i++) times.push(from + i / fps);
let n = 0; const t0 = Date.now();
for (const t of times) {
  await p.evaluate(t => { FILM.seek(t); return new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }, t);
  const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (++n % 240 === 0) console.log(n + '/' + times.length, ((Date.now() - t0) / 1000 | 0) + 's');
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('wrote', out, n, 'frames');
