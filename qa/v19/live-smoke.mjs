// smoke test on the real domain (phone): doors after the montage, seal Catalogue, a song plays, beacon sent, no errors
import { chromium, devices } from 'playwright';
const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
const errs = [], hosts = new Set(); p.on('pageerror', e => errs.push(String(e))); p.on('request', r => hosts.add(new URL(r.url()).host));
await p.goto('https://noblefathercreations.com/', { waitUntil: 'networkidle' }); await p.waitForTimeout(5000);
const doors = await p.$$eval('.door-t', a => a.map(x => [x.textContent.trim(), getComputedStyle(x).opacity]));
await p.screenshot({ path: 'qa/v19/shots/live-phone.png' });
await p.tap('.nf-seal'); await p.waitForTimeout(600); const cat = await p.$$eval('#nf-panel a', a => a.length); await p.keyboard.press('Escape');
await p.evaluate(() => document.querySelector('#music').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500);
await p.tap('#music .tracks .trk .play'); await p.waitForTimeout(4000);
const t = await p.evaluate(() => +window.__nfAudio.currentTime.toFixed(1));
const visible = await p.evaluate(() => { const e = document.getElementById('nf-visits'); return e ? !e.hidden : null; });
await b.close(); console.log(JSON.stringify({ doors, catalogueLinks: cat, songSeconds: t, hosts: [...hosts], counterShown: visible, errs }));
