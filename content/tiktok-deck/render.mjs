// TikTok book deck v3 renderer: books.json -> 1080x1920 PNG slides.
// Design: gold-on-black editorial "field guide poster". Brand bar (logo +
// wordmark) on every slide, one big serif headline, one proof block, and the
// site link set large as a signed footer. TikTok safe area: x 72..912,
// y 150..1440 (bottom 480 px is caption/UI).
// Usage: node render.mjs <deckDir>
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'fs';
import path from 'path';

const deck = path.resolve(process.argv[2] || '.');
const build = path.join(deck, 'build');
const out = path.join(build, 'slides');
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
const data = JSON.parse(fs.readFileSync(path.join(build, 'books.json'), 'utf8'));
const root = path.resolve(deck, '../..');
const f = (p) => 'file://' + path.join(root, 'tools/fonts', p);
const LOGO = 'file://' + path.join(root, 'design/brand/logo-noble-father.png');

const CSS = `
@font-face{font-family:IS;src:url('${f('instrumentserif/InstrumentSerif-Regular.ttf')}')}
@font-face{font-family:IS;font-style:italic;src:url('${f('instrumentserif/InstrumentSerif-Italic.ttf')}')}
@font-face{font-family:HG;font-weight:100 900;src:url('${f('hankengrotesk/HankenGrotesk[wght].ttf')}')}
@font-face{font-family:HG;font-style:italic;font-weight:100 900;src:url('${f('hankengrotesk/HankenGrotesk-Italic[wght].ttf')}')}
:root{--bg:#0b0a08;--ink:#f3ecdc;--dim:#b8ad98;--gold:#e0b55e;--gold2:#f4d58a;--line:rgba(224,181,94,.32)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:HG,sans-serif;color:var(--ink)}
.slide{width:1080px;height:1920px;position:relative;overflow:hidden;background:var(--bg)}
.glow{position:absolute;left:-200px;right:-200px;top:-300px;height:1300px;background-size:cover;background-position:center;filter:blur(90px) saturate(1.35);opacity:.5}
.veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,10,8,.25) 0%,rgba(11,10,8,.82) 38%,var(--bg) 62%)}
.frame{position:absolute;inset:28px;border:1px solid rgba(224,181,94,.18);border-radius:6px;pointer-events:none}
.safe{position:absolute;left:72px;top:150px;width:840px;height:1290px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:26px;height:150px;flex:none}
.brand .mk{width:150px;height:150px;border-radius:50%;flex:none;background:#000 url('${LOGO}') center 8%/118% auto no-repeat;box-shadow:0 0 0 3px var(--gold),0 0 0 9px rgba(224,181,94,.18),0 12px 30px rgba(0,0,0,.7)}
.brand .wm{font:700 27px/1 HG;letter-spacing:.3em;color:var(--gold)}
.brand .bt{font:italic 44px/1.1 IS;color:var(--ink);margin-top:12px}
.lab{display:flex;align-items:center;gap:18px;font:700 28px/1 HG;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-top:40px;flex:none}
.lab:before{content:"";width:48px;height:2px;background:var(--gold)}
.hl{font:100px/1 IS;letter-spacing:-.005em;color:var(--ink);margin:18px 0 28px;flex:none}
.hl em{color:var(--gold2)}
.body{flex:1;min-height:0;overflow:hidden}
.body p{font:400 46px/1.42 HG;margin-bottom:28px;color:var(--ink)}
.body p strong{color:var(--gold2);font-weight:700}
.body p em{font-style:italic}
.bl{display:flex;gap:24px;font:500 44px/1.3 HG;padding:16px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.bl:last-child{border-bottom:0}
.bl:before{content:"";flex:none;width:13px;height:13px;margin-top:17px;background:var(--gold);transform:rotate(45deg)}
.it{padding:8px 0 8px 28px;border-left:4px solid var(--gold);margin-bottom:12px}
.it b{display:block;font:700 41px/1.2 HG;color:var(--gold2)}
.it span{display:block;font:400 37px/1.36 HG;color:var(--ink);margin-top:6px}
.ac{display:flex;align-items:baseline;gap:34px;padding:2px 0;border-bottom:1px solid var(--line)}
.ac b{font:70px/1 IS;color:var(--gold2);width:70px;text-align:center}
.ac span{font:500 40px/1.2 HG}
.card{border:1.5px solid var(--line);border-radius:18px;background:linear-gradient(180deg,rgba(224,181,94,.09),rgba(255,255,255,.02));padding:26px 32px;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.card .ct{font:700 24px/1.3 HG;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);padding-bottom:22px;border-bottom:1px solid var(--line)}
.card .cr{padding:10px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.card .cr:last-child{border-bottom:0;padding-bottom:4px}
.card .cr b{display:block;font:700 25px/1 HG;letter-spacing:.16em;text-transform:uppercase;color:var(--gold2);margin-bottom:8px}
.card .cr span{display:block;font:400 34px/1.34 HG}
.stats .st{display:flex;align-items:baseline;gap:30px;padding:10px 0 18px;border-bottom:1px solid var(--line)}
.stats .st b{font:170px/1 IS;color:var(--gold2);min-width:380px}
.stats .st span{font:500 38px/1.25 HG;color:var(--ink)}
.foot{flex:none;padding-top:20px;border-top:1px solid var(--line)}
.foot .fl{font:700 25px/1 HG;letter-spacing:.3em;color:var(--dim);text-transform:uppercase}
.foot .fu{font:68px/1.2 IS;color:var(--gold2);margin-top:12px;white-space:nowrap}
.cbrand{position:absolute;left:72px;top:150px}
.cov{position:absolute;left:0;width:1080px;object-fit:contain;box-shadow:0 30px 80px rgba(0,0,0,.7)}
.hook{flex:1;display:flex;flex-direction:column;align-items:flex-start;justify-content:center}
.hook .hc{height:430px;border-radius:6px;box-shadow:0 40px 90px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.08)}
.hook h1{font:120px/.95 IS;margin-top:44px}
.hook .sb{font:400 40px/1.35 HG;color:var(--dim);margin-top:22px}
.nums{display:flex;gap:40px;margin-top:40px;flex-wrap:wrap}
.nums div{display:flex;flex-direction:column}
.nums b{font:84px/1 IS;color:var(--gold2)}
.nums span{font:600 25px/1.2 HG;letter-spacing:.16em;text-transform:uppercase;color:var(--dim);margin-top:8px}
.tc{flex:1;display:flex;flex-direction:column;justify-content:center}
.tc .k{font:700 27px/1 HG;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
.tc h1{font:118px/.95 IS;margin:24px 0 30px}
.tc h1 em{color:var(--gold2)}
.tc p{font:400 44px/1.4 HG;color:var(--ink)}
.tc .bl{font-size:42px}
.grid{display:grid;grid-template-columns:repeat(8,1fr);gap:12px;margin-top:50px}
.grid img{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:3px;box-shadow:0 6px 16px rgba(0,0,0,.6)}
.don{margin-top:40px;border:1.5px solid var(--gold);border-radius:14px;padding:28px 34px;background:rgba(224,181,94,.07)}
.don .dk{font:700 21px/1 HG;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin-bottom:16px}
.dr{display:flex;justify-content:space-between;align-items:baseline;padding:8px 0;font:500 38px/1.2 HG}
.dr b{font:400 60px/1 IS;color:var(--gold2)}
.big{font:74px/1.05 IS;color:var(--gold2);margin-top:40px}
`;

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>');
const hmd = (s) => esc(s).replace(/\*(.+?)\*/g, '<em>$1</em>');
const brandBar = (sub) => `<div class="brand"><div class="mk"></div><div><div class="wm">NOBLE FATHER CREATIONS</div><div class="bt">${esc(sub)}</div></div></div>`;
const foot = (url, label = 'Read it free') => `<div class="foot"><div class="fl">${esc(label)}</div><div class="fu">${esc(url)}</div></div>`;
const shell = (glowUrl, inner) => `<div class="slide"><div class="glow" style="background-image:url('${glowUrl}')"></div><div class="veil"></div><div class="frame"></div><div class="safe">${inner}</div></div>`;

function bodyHtml(sec) {
  if (sec.p) return sec.p.map((p) => `<p>${md(p)}</p>`).join('');
  if (sec.bullets) return sec.bullets.map((s) => `<div class="bl"><div>${md(s)}</div></div>`).join('');
  if (sec.items) return sec.items.map(([n, d]) => `<div class="it"><b>${md(n)}</b>${d ? `<span>${md(d)}</span>` : ''}</div>`).join('');
  if (sec.acro) return sec.acro.map(([l, w]) => `<div class="ac"><b>${esc(l)}</b><span>${esc(w)}</span></div>`).join('');
  if (sec.card) return `<div class="card"><div class="ct">${esc(sec.card.title)}</div>${sec.card.rows.map(([l, t]) => `<div class="cr"><b>${esc(l)}</b><span>${md(t)}</span></div>`).join('')}</div>`;
  if (sec.stats) return `<div class="stats">${sec.stats.map(([n, l]) => `<div class="st"><b>${esc(n)}</b><span>${esc(l)}</span></div>`).join('')}</div>`;
  return '';
}
const words = (sec) => JSON.stringify([sec.t, sec.p, sec.bullets, sec.items, sec.acro, sec.card, sec.stats]).replace(/[^\w\s$%']/g, ' ').split(/\s+/).filter(Boolean).length;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const manifest = [];
let idx = 0, problems = 0;
async function shoot(html, meta) {
  const tmp = path.join(build, '_slide.html');
  fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><style>${CSS}</style>${html}`);
  await page.goto('file://' + tmp);
  const r = await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.decode().catch(() => {})));
    for (const u of document.querySelectorAll('.fu')) { let s = 68; while (u.scrollWidth > u.clientWidth && s > 36) { s -= 2; u.style.fontSize = s + 'px'; } }
    const b = document.querySelector('.body');
    const over = b ? b.scrollHeight - b.clientHeight : 0;
    const safe = document.querySelector('.safe');
    const sOver = safe ? safe.scrollHeight - safe.clientHeight : 0;
    const broken = [...document.images].filter((i) => !i.naturalWidth).length;
    const fill = b ? Math.round(100 * [...b.children].reduce((a, c) => a + c.getBoundingClientRect().height, 0) / b.clientHeight) : null;
    return { over, sOver, broken, fill };
  });
  if (r.over > 1 || r.sOver > 4 || r.broken) { problems++; console.warn('PROBLEM', meta.slug, meta.kind, meta.h || '', JSON.stringify(r)); }
  const file = `${String(++idx).padStart(3, '0')}-${meta.slug}-${meta.kind}.png`;
  await page.locator('.slide').screenshot({ path: path.join(out, file) });
  manifest.push({ file, ...meta, fill: r.fill });
}

async function card(c, slug) {
  const body = (c.p ? `<p>${esc(c.p)}</p>` : '')
    + (c.bullets ? `<div>${c.bullets.map((s) => `<div class="bl"><div>${esc(s)}</div></div>`).join('')}</div>` : '')
    + (c.big ? `<div class="big">${esc(c.big)}</div>` : '')
    + (c.donate ? `<div class="don"><div class="dk">Support the work · optional</div>${data.donate.map(([a, b]) => `<div class="dr"><span>${esc(a)}</span><b>${esc(b)}</b></div>`).join('')}</div>` : '')
    + (c.grid ? `<div class="grid">${data.books.map((b) => `<img src="${b.coverUrl}">`).join('')}</div>` : '');
  const n = [c.h, c.p || '', ...(c.bullets || [])].join(' ').split(/\s+/).length + (c.donate ? 6 : 0);
  await shoot(shell(data.brandUrl, `${brandBar('Books by Shae Stovell')}<div class="tc"><div class="k">${esc(c.k)}</div><h1 style="font-size:${c.h.length > 36 ? 100 : 118}px">${hmd(c.h)}</h1>${body}</div>${c.big ? '' : foot('noblefathercreations.com', 'Free to read')}`), { slug, kind: 'card', words: n });
}

for (const c of data.intro) await card(c, 'intro');

for (const b of data.books) {
  // full cover below the brand bar, kept inside the area TikTok leaves clear
  const maxH = 1250, maxW = 1000; let ch = maxH, cw = Math.round(maxH * b.coverW / b.coverH);
  if (cw > maxW) { cw = maxW; ch = Math.round(maxW * b.coverH / b.coverW); }
  const top = 300 + Math.round((maxH - ch) / 2), left = Math.round((1080 - cw) / 2);
  await shoot(`<div class="slide"><div class="glow" style="background-image:url('${b.coverUrl}');opacity:.7;top:-200px;height:2300px"></div><div class="veil" style="background:rgba(11,10,8,.35)"></div>
    <div class="cbrand">${brandBar('Books by Shae Stovell')}</div>
    <img class="cov" style="top:${top}px;left:${left}px;width:${cw}px;height:${ch}px;border-radius:6px" src="${b.coverUrl}"></div>`, { slug: b.slug, kind: 'cover', words: 0 });
  const nums = b.chips.map((c) => { const m = c.match(/^([$0-9][0-9,.\-]*[A-Z%]*)\s+(.*)$/); return m ? `<div><b>${esc(m[1])}</b><span>${esc(m[2])}</span></div>` : `<div><b>✦</b><span>${esc(c)}</span></div>`; }).join('');
  await shoot(shell(b.coverUrl, `${brandBar(b.kicker)}<div class="hook"><img class="hc" src="${b.coverUrl}"><h1 style="font-size:${b.title.length > 22 ? 96 : 120}px">${esc(b.title)}</h1><div class="sb">${esc(b.sub)}</div><div class="nums">${nums}</div></div>${foot(b.url)}`),
    { slug: b.slug, kind: 'title', words: 10 + b.sub.split(' ').length });
  for (const sec of b.sections) {
    await shoot(shell(b.coverUrl, `${brandBar(b.title)}<div class="lab">${esc(sec.h)}</div><div class="hl">${hmd(sec.t)}</div><div class="body">${bodyHtml(sec)}</div>${foot(b.url)}`),
      { slug: b.slug, kind: 'info', h: sec.h, words: words(sec) + (sec.card ? 4 : 0) });
  }
  console.log(b.slug, b.sections.length + 2, 'slides');
}
for (const c of data.outro) await card(c, 'outro');

fs.writeFileSync(path.join(build, 'manifest.json'), JSON.stringify(manifest, null, 1));
await browser.close();
console.log('slides:', manifest.length, 'problems:', problems);
