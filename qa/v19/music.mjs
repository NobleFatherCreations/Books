// The Listening Room on the homepage: a featured song plays, the now-playing bar shows, all 176 songs open and play, next works.
import { chromium, devices } from 'playwright';
const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.route('**/api/visits', r => r.fulfill({ contentType: 'application/json', body: '{"visits":880}' }));
await p.goto('http://127.0.0.1:8765/', { waitUntil: 'networkidle' }); await p.waitForTimeout(800);
await p.evaluate(() => document.querySelector('#music').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600);
await p.tap('#music .tracks .trk .play'); await p.waitForTimeout(2500);
const a = await p.evaluate(() => ({ t: +window.__nfAudio.currentTime.toFixed(1), paused: window.__nfAudio.paused, src: window.__nfAudio.src.split('/').slice(-3).join('/'), bar: !document.querySelector('#nowbar').hidden, title: document.querySelector('#np-title').textContent }));
await p.screenshot({ path: 'qa/v19/shots/music-1.png' });
await p.tap('#all-btn'); await p.waitForTimeout(500);
const n = await p.evaluate(() => document.querySelectorAll('#all-songs .trk').length);
const last = await p.$$('#all-songs .trk .play'); await last[last.length - 1].scrollIntoViewIfNeeded(); await last[last.length - 1].tap(); await p.waitForTimeout(2000);
const b2 = await p.evaluate(() => ({ t: +window.__nfAudio.currentTime.toFixed(1), title: document.querySelector('#np-title').textContent }));
await p.screenshot({ path: 'qa/v19/shots/music-2.png' });
await p.tap('#np-next'); await p.waitForTimeout(1500);
const c = await p.evaluate(() => ({ title: document.querySelector('#np-title').textContent, playing: !window.__nfAudio.paused }));
await p.tap('#still-btn'); await p.waitForTimeout(300); const stillPaused = await p.evaluate(() => window.__nfAudio.paused);
await b.close(); console.log(JSON.stringify({ a, songs: n, b2, next: c, stillPaused, errs }));
