// Paginates books.json into 1080x1920 TikTok slides and screenshots each one.
// Usage: node render.mjs <deckDir>   (expects <deckDir>/build/books.json)
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'fs';
import path from 'path';

const deck = path.resolve(process.argv[2] || '.');
const build = path.join(deck, 'build');
const out = path.join(build, 'slides');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
const books = JSON.parse(fs.readFileSync(path.join(build, 'books.json'), 'utf8'));
const fonts = path.resolve(deck, '../../tools/fonts');
const f = (p) => 'file://' + path.join(fonts, p);

const CSS = `
@font-face{font-family:IS;src:url('${f('instrumentserif/InstrumentSerif-Regular.ttf')}')}
@font-face{font-family:IS;font-style:italic;src:url('${f('instrumentserif/InstrumentSerif-Italic.ttf')}')}
@font-face{font-family:HG;font-weight:100 900;src:url('${f('hankengrotesk/HankenGrotesk[wght].ttf')}')}
@font-face{font-family:HG;font-style:italic;font-weight:100 900;src:url('${f('hankengrotesk/HankenGrotesk-Italic[wght].ttf')}')}
:root{--bg:#0f0d0b;--ink:#f1e9d8;--dim:#b9ad97;--gold:#d4ad62;--line:rgba(212,173,98,.28)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:HG,sans-serif;color:var(--ink)}
.slide{width:1080px;height:1920px;position:relative;overflow:hidden;background:var(--bg)}
.bgart{position:absolute;inset:-80px;background-size:cover;background-position:center;filter:blur(60px) saturate(1.1);opacity:.22}
.veil{position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 0%,rgba(15,13,11,.35),rgba(15,13,11,.92) 70%)}
/* TikTok safe area: top 170, bottom 480 (caption+UI), left 72, right 168 */
.safe{position:absolute;left:72px;top:170px;width:840px;height:1270px;display:flex;flex-direction:column}
.head{display:flex;gap:24px;align-items:center;padding-bottom:26px;border-bottom:1px solid var(--line)}
.thumb{width:66px;height:99px;object-fit:cover;border-radius:4px;box-shadow:0 6px 18px rgba(0,0,0,.6);flex:none}
.hk{font:600 22px/1.2 HG;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
.ht{font:48px/1.05 IS;color:var(--ink);margin-top:6px}
.bar{height:4px;background:rgba(255,255,255,.1);border-radius:2px;margin-top:22px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--gold)}
.h2{font:84px/1 IS;color:var(--ink);margin:46px 0 30px}
.h2 em{color:var(--gold)}
.h2 small{display:block;font:600 22px/1 HG;letter-spacing:.2em;text-transform:uppercase;color:var(--dim);margin-bottom:16px}
.body{flex:1;overflow:hidden;min-height:0}
.body p{font:400 40px/1.42 HG;margin-bottom:28px;color:var(--ink)}
.body p strong{color:var(--gold);font-weight:700}
.body p em,.it em{font-family:HG;font-style:italic}
.ac{display:flex;align-items:baseline;gap:34px;padding:2px 0;border-bottom:1px solid var(--line)}.ac b{font:80px/1 IS;color:var(--gold);width:70px;text-align:center}.ac span{font:500 42px/1.2 HG}
.it{padding:18px 0 18px 26px;border-left:4px solid var(--gold);margin-bottom:18px}
.it b{display:block;font:700 37px/1.2 HG;color:var(--gold)}
.it span{display:block;font:400 33px/1.38 HG;color:var(--ink);margin-top:6px}
.it.solo b{color:var(--ink)}
.bl{display:flex;gap:22px;font:400 40px/1.35 HG;margin-bottom:28px}
.bl:before{content:"";flex:none;width:14px;height:14px;margin-top:17px;background:var(--gold);transform:rotate(45deg)}
.foot{gap:24px;padding-top:22px;border-top:1px solid var(--line);font:600 24px/1.2 HG;letter-spacing:.06em;color:var(--dim);display:flex;justify-content:space-between}
.foot b{color:var(--gold);font-weight:600}
/* cover */
.cov{position:absolute;left:0;width:1080px;object-fit:contain;box-shadow:0 30px 80px rgba(0,0,0,.7)}
/* title cards */
.card{position:absolute;left:72px;width:840px;top:170px;height:1270px;display:flex;flex-direction:column;justify-content:center}
.card .k{font:600 26px/1.3 HG;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
.card h1{font:150px/.95 IS;margin:30px 0}
.card h1 em{color:var(--gold)}
.card p{font:400 44px/1.4 HG;color:var(--dim)}
.chips{display:flex;flex-wrap:wrap;gap:14px;margin-top:40px}
.chips span{border:1.5px solid var(--gold);color:var(--gold);font:700 24px/1 HG;letter-spacing:.14em;text-transform:uppercase;padding:14px 18px;border-radius:4px}
`;

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>');
const splitSentences = (p) => p.split(/(?<=[.?!…]["”)]?)\s+(?=["“(*A-Z0-9$])/);

function units(sec) {
  if (sec.p) return sec.p.flatMap((para, pi) => splitSentences(para).map((s) => ({ k: 'p', pi, s })));
  if (sec.items) return sec.items.map(([n, d]) => ({ k: 'i', n, d }));
  if (sec.acro) return sec.acro.map(([n, d]) => ({ k: 'a', n, d }));
  return sec.bullets.map((s) => ({ k: 'b', s }));
}
function unitsHtml(us) {
  let h = '', curP = null, buf = [];
  const flush = () => { if (buf.length) h += `<p>${buf.map(md).join(' ')}</p>`; buf = []; };
  for (const u of us) {
    if (u.k === 'p') { if (curP !== u.pi) { flush(); curP = u.pi; } buf.push(u.s); continue; }
    flush(); curP = null;
    if (u.k === 'a') { h += `<div class="ac"><b>${esc(u.n)}</b><span>${esc(u.d)}</span></div>`; continue; }
    if (u.k === 'i') h += `<div class="it${u.d ? '' : ' solo'}"><b>${md(u.n)}</b>${u.d ? `<span>${md(u.d)}</span>` : ''}</div>`;
    else h += `<div class="bl"><div>${md(u.s)}</div></div>`;
  }
  flush();
  return h;
}
const bg = (b) => `<div class="bgart" style="background-image:url('${b.coverUrl}')"></div><div class="veil"></div>`;
const head = (b, n, of) => `<div class="head"><img class="thumb" src="${b.coverUrl}"><div style="flex:1"><div class="hk">${esc(b.kicker)} · ${n} / ${of}</div><div class="ht">${esc(b.title)}</div><div class="bar"><i style="width:${(n / of) * 100}%"></i></div></div></div>`;
const foot = (b) => `<div class="foot"><span>Free to read</span><b>${esc(b.url)}</b></div>`;
const heading = (h, cont) => { const words = h.split(' '); const last = words.pop(); return `<div class="h2">${cont ? '<small>Continued</small>' : ''}${esc(words.join(' '))} <em>${esc(last)}</em></div>`; };
function textSlide(b, h, cont, us, n, of) {
  return `<div class="slide">${bg(b)}<div class="safe">${head(b, n, of)}${heading(h, cont)}<div class="body">${unitsHtml(us)}</div>${foot(b)}</div></div>`;
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const mpage = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const tmpM = path.join(build, '_measure.html');
fs.writeFileSync(tmpM, `<!doctype html><meta charset="utf-8"><style>${CSS}</style><div id="m"></div>`);
await mpage.goto('file://' + tmpM);
await mpage.evaluate(() => document.fonts.ready);
const fits = async (html) => mpage.evaluate((html) => {
  const m = document.getElementById('m'); m.innerHTML = html;
  const b = m.querySelector('.body'); return b.scrollHeight <= b.clientHeight + 1;
}, html);

const manifest = [];
let idx = 0;
const shoot = async (html, meta) => {
  const tmp = path.join(build, '_slide.html');
  fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><style>${CSS}</style>${html}`);
  await page.goto('file://' + tmp);
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
  const file = `${String(++idx).padStart(3, '0')}-${meta.slug}-${meta.kind}.png`;
  await page.locator('.slide').screenshot({ path: path.join(out, file) });
  manifest.push({ file, ...meta });
};

// Intro
const brand = books.brandUrl;
await shoot(`<div class="slide"><div class="bgart" style="background-image:url('${brand}');opacity:.35"></div><div class="veil"></div>
 <div class="card"><div class="k">Noble Father Creations · Shae Stovell</div><h1>Words for the things we <em>can't name</em></h1>
 <p>A library of free field guides. Fifteen books and one guided practice, each written for the person who needs it most.</p>
 <div class="chips"><span>Free</span><span>No accounts</span><span>No paywalls</span></div></div></div>`, { slug: 'intro', kind: 'title', words: 30 });

for (const b of books.books) {
  // 1) plan pages (dry-run packing)
  const pages = [];
  for (const sec of b.sections) {
    const us = units(sec); let start = 0, cont = false;
    while (start < us.length) {
      let end = start + 1;
      while (end < us.length && await fits(textSlide(b, sec.h, cont, us.slice(start, end + 1), 1, 9))) end++;
      if (!(await fits(textSlide(b, sec.h, cont, us.slice(start, end), 1, 9)))) console.warn('OVERFLOW', b.slug, sec.h, start);
      pages.push({ h: sec.h, cont, us: us.slice(start, end) });
      start = end; cont = true;
    }
  }
  // 2) cover (full-size image)
  const ar = b.coverH / b.coverW, ch = Math.min(1920, Math.round(1080 * ar)), top = Math.round((1920 - ch) / 2);
  await shoot(`<div class="slide"><div class="bgart" style="background-image:url('${b.coverUrl}');opacity:.55"></div>
   <img class="cov" style="top:${top}px;height:${ch}px" src="${b.coverUrl}"></div>`, { slug: b.slug, kind: 'cover', words: 0 });
  // 3) title card
  await shoot(`<div class="slide">${bg(b)}<div class="card"><div class="k">${esc(b.kicker)}</div><h1 style="font-size:${b.title.length > 20 ? 120 : 150}px">${esc(b.title)}</h1>
   <p>${esc(b.sub)}</p><div class="chips">${b.chips.map((c) => `<span>${esc(c)}</span>`).join('')}</div>
   <p style="margin-top:50px;font-size:30px;color:var(--gold)">Read it free · ${esc(b.url)}</p></div></div>`, { slug: b.slug, kind: 'title', words: 12 + b.sub.split(' ').length });
  // 4) info pages
  for (let i = 0; i < pages.length; i++) {
    const p = pages[i];
    const words = p.us.map((u) => (u.s || `${u.n} ${u.d}`)).join(' ').split(/\s+/).length;
    await shoot(textSlide(b, p.h, p.cont, p.us, i + 1, pages.length), { slug: b.slug, kind: 'info', words });
  }
  console.log(b.slug, pages.length, 'info slides');
}

// Outro
await shoot(`<div class="slide"><div class="bgart" style="background-image:url('${brand}');opacity:.35"></div><div class="veil"></div>
 <div class="card"><div class="k">All of it, free</div><h1>Find the one you <em>need.</em></h1>
 <p>Every book and the Root are free to read, with no account and nothing tracked.</p>
 <p style="margin-top:50px;font:400 64px/1.1 IS;color:var(--gold)">noblefathercreations.com</p></div></div>`, { slug: 'outro', kind: 'title', words: 25 });

fs.writeFileSync(path.join(build, 'manifest.json'), JSON.stringify(manifest, null, 1));
await browser.close();
console.log('slides:', manifest.length);
