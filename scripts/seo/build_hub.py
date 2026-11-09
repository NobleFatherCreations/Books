#!/usr/bin/env python3
"""Homepage v17 (owner, 2026-11-08): small enough for Google to read, simpler to navigate, same look.

1. Media out of the HTML (21 MB -> ~0.2 MB): the song, the intro video (recompressed), every picture (WebP at
   display size), every font (subset WOFF2) become files on the hub site itself (/media/, /f/). Still self-hosted:
   no outside requests are added.
2. The intro video plays in the hero background instead of locking the page; no door gate, no tour, no autoplay sound
   (the music button plays on tap).
3. Order: Start here -> every book -> tools -> music -> workshop -> guide -> manifesto -> maker -> support.
   The Art portal opens the portal pendants (/portals) directly.
4. "Start here": plain situations that open to a short list of books that may help (native <details>, no JavaScript).
5. Card facts brought up to date with the books.

Idempotent: run again any time; media steps only act on data: URIs still present.
Run: python3 scripts/seo/build_hub.py
"""
import base64
import hashlib
import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S
from PIL import Image

HUB = S.ROOT / "hub"
SRC = HUB / "catalogue-redesign.html"
MEDIA = HUB / "media"
FONTS = HUB / "f"


# ---------------------------------------------------------------- 1. media out of the HTML
def _img(data, max_w, name_hint):
    im = Image.open(io.BytesIO(data))
    im.load()
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    keep_alpha = im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode in ("RGBA", "LA")
    im = im.convert("RGBA" if keep_alpha else "RGB")
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=74, method=6)
    out = buf.getvalue()
    name = f"{name_hint}-{hashlib.md5(out).hexdigest()[:10]}.webp"
    (MEDIA / name).write_bytes(out)
    return f"/media/{name}", im.width, im.height


def extract_media(h):
    MEDIA.mkdir(exist_ok=True)
    FONTS.mkdir(exist_ok=True)
    report = []

    # the song: stays full quality, downloads only when someone presses play
    def audio(m):
        data = base64.b64decode(m.group(1))
        (MEDIA / "now-playing.mp3").write_bytes(data)
        report.append(("audio", len(data), 0))
        return "/media/now-playing.mp3"
    h = re.sub(r"data:audio/mpeg;base64,([A-Za-z0-9+/=]+)", audio, h)

    # the intro: recompressed for the web (no audio track; same picture)
    def video(m):
        data = base64.b64decode(m.group(1))
        with tempfile.TemporaryDirectory() as t:
            src, dst = Path(t) / "in.mp4", MEDIA / "intro.mp4"
            src.write_bytes(data)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-an", "-vf", "scale=540:-2",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(dst)], check=True)
        report.append(("video", len(data), dst.stat().st_size))
        return "/media/intro.mp4"
    h = re.sub(r"data:video/mp4;base64,([A-Za-z0-9+/=]+)", video, h)

    # pictures in <img src>: WebP at twice their display size, with real dimensions (no layout shift)
    src_h = h
    def img_tag(m):
        tag = m.group(0)
        before = src_h[max(0, m.start() - 200):m.start()]
        mm = re.search(r'src="data:image/(?:jpeg|jpg|png|webp|gif);base64,([A-Za-z0-9+/=]+)"', tag)
        if not mm:
            return tag
        cls = (re.search(r'class="([^"]*)"', tag) or [0, ""])[1]
        ctx = cls + " " + " ".join(re.findall(r'class="([^"]*)"', before)[-2:])
        max_w = (600 if "book-face" in ctx or "st-book" in ctx else 900 if "portrait" in ctx else
                 720 if any(k in ctx for k in ("card", "tile", "vol", "pg-", "product", "thumb")) else 1400)
        cls = cls or ("cover" if "book" in ctx else "img")
        data = base64.b64decode(mm.group(1))
        url, w, hh = _img(data, max_w, S.slugify(cls.split()[0] if cls else "img", 30) or "img")
        report.append(("img", len(data), (MEDIA / url.split("/")[-1]).stat().st_size))
        tag = tag.replace(mm.group(0), f'src="{url}"')
        if " width=" not in tag:
            tag = tag.replace("<img", f'<img width="{w}" height="{hh}"', 1)
        if "loading=" not in tag:
            tag = tag.replace("<img", '<img loading="lazy" decoding="async"', 1)
        return tag
    h = re.sub(r"<img\b[^>]*>", img_tag, h)

    # video posters and CSS backgrounds
    def attr_or_css(m):
        data = base64.b64decode(m.group(2))
        url, *_ = _img(data, 1600, "bg")
        report.append(("bg", len(data), (MEDIA / url.split("/")[-1]).stat().st_size))
        return m.group(1) + url
    h = re.sub(r'(poster=")data:image/[a-z+]+;base64,([A-Za-z0-9+/=]+)', attr_or_css, h)
    h = re.sub(r"""(url\(["']?)data:image/(?:jpeg|jpg|png|webp|gif);base64,([A-Za-z0-9+/=]+)""", attr_or_css, h)

    # fonts: subset WOFF2 files
    from fontTools.ttLib import TTFont
    from fontTools import subset as _subset
    chars = S._book_chars(h)
    def font(m):
        block = m.group(0)
        mm = re.search(r"url\(['\"]?data:font/[a-z0-9]+;base64,([A-Za-z0-9+/=]+)['\"]?\)(\s*format\([^)]*\))?", block)
        if not mm:
            return block
        fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", block).group(1).strip()
        w = (re.search(r"font-weight:\s*([^;]+)", block) or [0, "400"])[1].strip()
        st = (re.search(r"font-style:\s*([^;]+)", block) or [0, "normal"])[1].strip()
        data = base64.b64decode(mm.group(1))
        f = TTFont(io.BytesIO(data))
        opts = _subset.Options(); opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
        sub = _subset.Subsetter(opts); sub.populate(unicodes=chars); sub.subset(f)
        f.flavor = "woff2"
        buf = io.BytesIO(); f.save(buf)
        name = f"{S.slugify(fam)}-{S.slugify(w)}-{st}.woff2"
        (FONTS / name).write_bytes(buf.getvalue())
        report.append(("font", len(data), len(buf.getvalue())))
        new = block.replace(mm.group(0), f"url(/f/{name}) format('woff2')")
        if "font-display" not in new:
            new = new.replace("}", ";font-display:swap}", 1) if new.rstrip().endswith("}") else new
        return new
    h = re.sub(r"@font-face\s*\{[^}]*\}", font, h)
    return h, report


# ---------------------------------------------------------------- 2-5. structure
START_HERE = [
    ("Manipulated by one person", [
        ("A partner or ex", [("feminine", "The Sovereign Divine Feminine", "Name the tactics, with counter-moves and safety planning"),
                             ("longafter", "The Long After", "What happens once you've left"),
                             ("silence", "The Silence", "For men nobody thought to ask")]),
        ("Family", [("feminine", "The Sovereign Divine Feminine", "Family scripts, guilt and obligation"),
                    ("playbook", "The Pattern Decoder", "Look up what they keep doing, by name")]),
        ("A friend, boss or anyone", [("playbook", "The Pattern Decoder", "310 tactics, each with signs and what to do"),
                                      ("scale", "The Weighing", "How to be right about people")]),
    ]),
    ("At work", [(None, [("atwill", "At Will", "The coercive workplace"),
                         ("playbook", "The Pattern Decoder", "Name the move your manager is making")])]),
    ("In a group, faith or community", [(None, [("faith", "The Sacred Divide", "How power works inside 34 faiths, every claim sourced"),
                                                ("wook", "The Festie Codex", "Coercive crews and high-control scenes"),
                                                ("fractal", "The Fractal", "The same pattern in every institution")])]),
    ("Protecting my kids", [(None, [("children", "Playground Protectors", "A free picture book for kids 5 and up"),
                                    ("feminine", "The Sovereign Divine Feminine", "The motherhood chapters, for you")])]),
    ("Going to a festival", [(None, [("festival", "The Festie Bible", "21 guides, one for every corner of the scene"),
                                     ("wook", "The Festie Codex", "Harm reduction, consent and what to do after")])]),
    ("Money, power and the world", [(None, [("fracture", "The Fracture", "Who received $50 trillion, 195 sources"),
                                            ("fractal", "The Fractal", "One manipulation pattern, every scale"),
                                            ("loop", "The Loop", "The machine that learns you")])]),
    ("An ageing parent, or later life", [(None, [("slowtake", "The Slow Take", "Coercion in later life")])]),
    ("I hurt someone and want to repair it", [(None, [("repair", "The Repair", "For the person on the other side of it")])]),
    ("Healing, and coming back to myself", [(None, [("shadowroot", "The Root", "A shadow-work practice"),
                                                   ("music", "The Listening Room", "Free music to sit with")])]),
]

OLD_HERO_JS = ('<script>(function(){var c=document.querySelector(".st-colophon");if(c)c.classList.add("nf-cl-in");'
               'var v=document.querySelector(".st-hero-video");if(v&&matchMedia("(prefers-reduced-motion: reduce)").matches){v.removeAttribute("autoplay");v.pause();}})();</script>')
# runs after parsing: the colophon list sits below this script, so querying it immediately found nothing
HERO_JS = ('<script>addEventListener("DOMContentLoaded",function(){var c=document.querySelector(".st-colophon");if(c)c.classList.add("nf-cl-in");'
           'var v=document.querySelector(".st-hero-video");if(v&&matchMedia("(prefers-reduced-motion: reduce)").matches){v.removeAttribute("autoplay");v.pause();}});</script>')

# phone-nav polish (design review 2026-11-09): active pill, condensed header, edge fades, music state, one-open accordions
NAV_JS = """<script id="v17-js">(function(){
var nav=document.querySelector('.masthead .topnav'),mh=document.querySelector('.masthead'),rm=matchMedia('(prefers-reduced-motion: reduce)');
var a=document.getElementById('npAudio'),m=document.getElementById('npToggle');
if(a&&m){var sync=function(){var on=!a.paused;m.dataset.playing=on;m.removeAttribute('aria-pressed');m.setAttribute('aria-label',on?'Pause background music':'Play background music')};
a.addEventListener('play',sync);a.addEventListener('pause',sync);m.addEventListener('click',function(){setTimeout(sync,0)});sync();}
document.querySelectorAll('.st-start details').forEach(function(d){d.addEventListener('toggle',function(){if(!d.open)return;
var t=d.firstElementChild.getBoundingClientRect().top;if(t<mh.offsetHeight)d.scrollIntoView({block:'start',behavior:rm.matches?'auto':'smooth'})})});
if(!nav||!('IntersectionObserver' in window))return;var links={};
nav.querySelectorAll('a[href^="#"]').forEach(function(l){links[l.getAttribute('href').slice(1)]=l});
function edges(){nav.dataset.start=nav.scrollLeft<4;nav.dataset.end=nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-4}
function setActive(id){for(var k in links)links[k].removeAttribute('aria-current');var l=links[id];if(!l)return;l.setAttribute('aria-current','location');
if(nav.scrollWidth>nav.clientWidth){var x=l.getBoundingClientRect().left-nav.getBoundingClientRect().left+nav.scrollLeft;
nav.scrollTo({left:x-(nav.clientWidth-l.offsetWidth)/2,behavior:rm.matches?'auto':'smooth'})}}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)setActive(e.target.id)})},{rootMargin:'-45% 0px -50% 0px'});
document.querySelectorAll('main section[id], .st-hero').forEach(function(s){io.observe(s)});
var hero=document.querySelector('.st-hero');if(hero)new IntersectionObserver(function(es){mh.classList.toggle('is-condensed',!es[0].isIntersecting)},{rootMargin:'-120px 0px 0px 0px'}).observe(hero);
nav.addEventListener('scroll',edges,{passive:true});addEventListener('resize',edges);edges();})();</script>"""

START_CSS = """
.st-start{padding:72px 0 24px}.st-start .wrap{max-width:860px}
.st-start h2{font-family:var(--display);font-weight:500;font-size:clamp(28px,4vw,40px);line-height:1.15;margin:8px 0 8px;color:var(--bone)}
.st-start .st-start-lede{color:var(--bone-dim,#BCB1A0);margin:0 0 24px;max-width:56ch}
.st-start details{border:1px solid var(--line);border-radius:14px;margin:0 0 10px;background:rgba(27,21,34,.55);transition:border-color .25s ease}
.st-start details[open]{border-color:rgba(201,163,91,.55)}
.st-start summary{list-style:none;cursor:pointer;padding:16px 20px;min-height:52px;display:flex;align-items:center;justify-content:space-between;gap:16px;
font-family:var(--display);font-size:20px;color:var(--bone)}
.st-start summary::-webkit-details-marker{display:none}
.st-start summary::after{content:"+";color:var(--brass);font-size:24px;line-height:1;transition:transform .25s ease}
.st-start details[open]>summary::after{transform:rotate(45deg)}
.st-start summary:focus-visible{outline:2px solid var(--brass);outline-offset:2px;border-radius:12px}
.st-start .st-help{padding:0 20px 18px}
.st-start .st-help-k{font-family:var(--mono,ui-monospace,monospace);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);margin:0 0 8px}
.st-start .st-help ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.st-start .st-help a{display:block;padding:12px 14px;border-radius:10px;background:rgba(20,16,25,.8);border:1px solid var(--line);transition:border-color .2s ease,transform .2s ease}
.st-start .st-help a:hover,.st-start .st-help a:focus-visible{border-color:var(--brass);transform:translateY(-1px)}
.st-start .st-help a b{display:block;font-family:var(--display);font-weight:500;color:var(--bone);font-size:18px}
.st-start .st-help a span{display:block;color:var(--bone-dim,#BCB1A0);font-size:15px;margin-top:2px}
.st-start details details{margin:10px 20px 0;background:transparent}
.st-start details details summary{font-size:17px;padding:12px 16px;min-height:44px}
.st-start .st-start-art{display:inline-flex;align-items:center;gap:10px;margin:24px 0 0;padding:14px 22px;border-radius:999px;border:1px solid var(--brass);
color:var(--bone);font-family:var(--display);font-size:18px;transition:background-color .25s ease}
.st-start .st-start-art:hover{background:rgba(201,163,91,.14)}
.st-lib-art{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin:-8px 0 28px;padding:16px 20px;border:1px solid var(--line);border-radius:14px;
background:rgba(27,21,34,.55)}
.st-lib-art p{margin:0;color:var(--bone-dim,#BCB1A0)}
.st-lib-art a{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;border-radius:999px;background:var(--brass);color:#141019;font-family:var(--display);font-size:17px;
transition:filter .2s ease}.st-lib-art a:hover{filter:brightness(1.08)}
.st-hero-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.2;mix-blend-mode:screen;pointer-events:none;
-webkit-mask-image:linear-gradient(180deg,#000 0%,rgba(0,0,0,.35) 45%,#000 100%);mask-image:linear-gradient(180deg,#000 0%,rgba(0,0,0,.35) 45%,#000 100%)}
@media (min-width:900px){.st-hero-video{left:auto;right:0;width:46%;opacity:.55;-webkit-mask-image:none;mask-image:none;-webkit-mask-image:linear-gradient(90deg,transparent,#000 30%);mask-image:linear-gradient(90deg,transparent,#000 30%)}}
@media (prefers-reduced-motion:reduce){.st-hero-video{display:none}}
/* phones: the menu stays reachable as one swipeable row under the brand */
@media (max-width:899px){
.masthead .bar{flex-wrap:wrap;row-gap:6px;padding-bottom:8px}
.masthead .topnav{display:flex!important;width:100%;gap:4px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;
-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
.masthead .topnav::-webkit-scrollbar{display:none}
.masthead .topnav a{flex:none;min-height:44px;display:inline-flex;align-items:center;padding:0 12px;border:1px solid var(--line);border-radius:999px;font-size:.66rem}
}

/* ---- design review 2026-11-09 ---- */
:root{--mast-h:68px}@media (max-width:899px){:root{--mast-h:112px}}
main section[id]{scroll-margin-top:var(--mast-h)}
@media (prefers-reduced-motion:no-preference){@supports (animation-timeline:view()){
.st-hero-plate,.st-hero-glow,.st-hero-beam,.st-hero-motes,.st-hero-inner{animation-timeline:scroll(root);animation-range:0 100vh}}}
.st-colophon a{min-height:44px;justify-content:center}
.masthead .topnav a{transition:color .2s ease,border-color .2s ease,background-color .2s ease,transform .12s ease-out;-webkit-tap-highlight-color:transparent}
.masthead .topnav a[aria-current]{color:var(--brass-bright);border-color:rgba(201,163,91,.6);background:rgba(201,163,91,.12)}
@media (hover:none){.masthead .topnav a:hover:not([aria-current]){color:var(--bone-dim)}}
.masthead .topnav a:active{transform:scale(.96)}
.masthead .topnav a:focus-visible{outline-offset:-3px}
.st-start summary,.st-start .st-help a,.st-lib-art a{-webkit-tap-highlight-color:transparent}
.st-start summary{transition:background-color .15s ease}.st-start summary:active{background:rgba(201,163,91,.08)}
.st-start .st-help a:active,.st-lib-art a:active{transform:scale(.98);transition-duration:.1s}
.st-start details{scroll-margin-top:calc(var(--mast-h) + 8px)}
.st-start details details{margin:0 20px;border:0;border-top:1px solid var(--line);border-radius:0;background:transparent}
.st-start details details[open]{border-color:var(--line)}
.st-start details details summary{padding:12px 0}
.st-start details details .st-help{padding:0 0 16px}
@supports (interpolate-size:allow-keywords){.st-start{interpolate-size:allow-keywords}
.st-start details::details-content{block-size:0;overflow:clip;opacity:0;transition:block-size .25s cubic-bezier(.23,1,.32,1),opacity .2s ease,content-visibility .25s allow-discrete}
.st-start details[open]::details-content{block-size:auto;opacity:1}}
.nf-mute.nf-mute[data-playing="false"] .nf-mute-on-icon{display:none}.nf-mute.nf-mute[data-playing="false"] .nf-mute-off-icon{display:block}
.nf-mute.nf-mute[data-playing="true"] .nf-mute-on-icon{display:block}.nf-mute.nf-mute[data-playing="true"] .nf-mute-off-icon{display:none}
.nf-seal.nf-seal{right:calc(18px + env(safe-area-inset-right));bottom:calc(18px + env(safe-area-inset-bottom))}
.nf-mute.nf-mute{left:calc(18px + env(safe-area-inset-left));bottom:calc(18px + env(safe-area-inset-bottom))}
.masthead .bar{padding-left:max(var(--gutter,20px),env(safe-area-inset-left));padding-right:max(var(--gutter,20px),env(safe-area-inset-right))}
.footer{padding-bottom:calc(88px + env(safe-area-inset-bottom))}
@media (max-width:899px){
.masthead .topnav a{font-size:.75rem;letter-spacing:.08em;padding:0 14px}
.masthead .topnav a[href="#start-here"]{background:var(--brass);border-color:var(--brass);color:#141019}
.masthead .topnav{--l:0px;--r:32px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 var(--l),#000 calc(100% - var(--r)),transparent);mask-image:linear-gradient(90deg,transparent,#000 var(--l),#000 calc(100% - var(--r)),transparent)}
.masthead .topnav[data-start=false]{--l:24px}.masthead .topnav[data-end=true]{--r:0px}
.masthead{transition:background-color .25s ease}
.masthead .bar{transition:padding .25s cubic-bezier(.23,1,.32,1)}
.masthead .nm>span{display:block;max-height:16px;overflow:hidden;transition:opacity .2s ease,max-height .25s cubic-bezier(.23,1,.32,1)}
.masthead.is-condensed{background:rgba(14,10,20,.86)}
.masthead.is-condensed .bar{padding-top:8px}
.masthead.is-condensed .nm>span{opacity:0;max-height:0}}
@media (prefers-reduced-motion:reduce){
.masthead,.masthead .bar,.masthead .nm>span{transition:none}
.masthead .topnav a{transition:color .2s ease,border-color .2s ease,background-color .2s ease}
.masthead .topnav a:active,.st-start .st-help a:active,.st-lib-art a:active{transform:none}
.st-start details::details-content{transition:opacity .15s ease}}
"""


def start_here_html():
    def books(lst):
        return "<ul>" + "".join(f'<li><a href="/{s}"><b>{S.esc(t)}</b><span>{S.esc(d)}</span></a></li>' for s, t, d in lst) + "</ul>"
    out = []
    for i, (situation, branches) in enumerate(START_HERE):
        inner = ""
        if len(branches) == 1 and branches[0][0] is None:
            inner = f'<div class="st-help"><p class="st-help-k">These may help</p>{books(branches[0][1])}</div>'
        else:
            inner = "".join(f'<details name="st-sub-{i}"><summary>{S.esc(sub)}</summary><div class="st-help"><p class="st-help-k">These may help</p>'
                            f'{books(lst)}</div></details>' for sub, lst in branches) + '<div style="height:14px"></div>'
        out.append(f"<details name=\"st-top\"><summary>{S.esc(situation)}</summary>{inner}</details>")
    return ('<section class="st-start" id="start-here" aria-labelledby="start-h"><div class="wrap">'
            '<p class="st-kicker">Start here</p><h2 id="start-h">What brings you here?</h2>'
            '<p class="st-start-lede">Pick what fits. A few free books open up that may help, and you can narrow it down from there.</p>'
            + "".join(out) +
            '<a class="st-start-art" href="/portals">Here for the art? Open the portal pendants <span aria-hidden="true">&#8594;</span></a>'
            '</div></section>')


FACTS = [
    ("<li>12 guides</li><li>149 scenarios</li>", "<li>21 guides</li><li>270 scenarios</li>"),
    ("Twelve field guides for every corner of the festival world", "Twenty-one field guides for every corner of the festival world"),
    ("<li>26 chapters</li><li>Harm reduction</li>", "<li>33 chapters</li><li>Harm reduction</li>"),
    ("<li>25 traditions</li><li>750 entries</li>", "<li>34 traditions</li><li>Every claim sourced</li>"),
    ('<h3 class="st-vol-title">The Music</h3>', '<h3 class="st-vol-title">The Listening Room</h3>'),
]


def restructure(h):
    # intro overlay -> hero background video
    h = re.sub(r'<div[^>]*id="heroIntro"[^>]*>.*?</div>\s*<script>\s*\(function\(\)\{\s*var overlay = document\.getElementById\(\'heroIntro\'\);.*?</script>',
               HERO_JS,
               h, count=1, flags=re.S)
    if 'class="st-hero-video"' not in h:
        h = h.replace('<span class="st-hero-glow"></span>',
                      '<video class="st-hero-video" autoplay muted loop playsinline preload="metadata" aria-hidden="true" tabindex="-1" '
                      'poster="/media/intro-poster.webp"><source src="/media/intro.mp4" type="video/mp4"></video>'
                      '<span class="st-hero-glow"></span>', 1)
    # no gate, no tour, no autoplaying sound (the music button plays on tap)
    h = h.replace("var chosen = false;\n  try { chosen = sessionStorage.getItem('nfDoorChosen') === '1'; } catch(_){}", "var chosen = true;")
    h = re.sub(r"var chosen = false;\s*try \{ chosen = sessionStorage\.getItem\('nfDoorChosen'\) === '1'; \} catch\(_\)\{\}", "var chosen = true;", h)
    h = re.sub(r'(<audio[^>]*id="npAudio"[^>]*?)\s+preload="[^"]*"', r"\1", h)
    h = re.sub(r'(<audio)([^>]*id="npAudio")', r'\1 preload="none"\2', h, count=1) if 'preload="none"' not in re.search(r'<audio[^>]*id="npAudio"[^>]*>', h).group(0) else h
    h = h.replace('<p class="st-portals-note">Three ways in &mdash; or tap the seal (bottom right) anytime to browse everything.</p>',
                  '<p class="st-portals-note">Jump straight in &mdash; or tap the seal (bottom right) anytime to browse everything.</p>')
    # the Art portal opens the portal pendants directly
    h = h.replace('<a class="st-portal" href="#workshop" style="--pg-img:var(--gate-silver)">',
                  '<a class="st-portal" href="/portals" style="--pg-img:var(--gate-silver)">')
    h = h.replace('<span class="pg-label"><b>Art</b><span>The Workshop</span></span>',
                  '<span class="pg-label"><b>Art</b><span>Portal pendants</span></span>')
    # menu in the new order
    h = re.sub(r'<nav class="topnav" aria-label="Sections">.*?</nav>',
               '<nav class="topnav" aria-label="Sections"> <a href="#start-here">Start here</a> <a href="#library">Books</a> '
               '<a href="#instruments">Tools</a> <a href="#music">Music</a> <a href="/portals">Art</a> <a href="#workshop">Workshop</a> '
               '<a href="/topics">Topics</a> <a href="#support">Support</a> </nav>', h, count=1, flags=re.S)
    # sections: cut each by id, put back in the new order after the hero block
    ids = ["manifesto", "workshop", "guide", "library", "instruments", "music", "maker", "support"]
    blocks = {}
    for i in ids:
        m = re.search(r'\s*<!-- =+ [A-Z ]+ =+ -->\s*<section[^>]*\bid="%s"[^>]*>.*?</section>' % i, h, re.S) or \
            re.search(r'\s*<section[^>]*\bid="%s"[^>]*>.*?</section>' % i, h, re.S)
        blocks[i] = m.group(0)
        h = h.replace(m.group(0), "", 1)
    h = re.sub(r'\s*<section class="st-start" id="start-here".*?</section>', "", h, flags=re.S)
    order = ["library", "instruments", "music", "workshop", "guide", "manifesto", "maker", "support"]
    new = "\n" + start_here_html() + "".join("\n" + blocks[i] for i in order)
    h = h.replace("</main>", new + "\n</main>", 1)
    # chapter numbers follow the new order
    num = {"library": "01", "instruments": "02", "music": "03", "workshop": "04", "guide": "05", "support": "06"}
    for sid, n in num.items():
        h = re.sub(r'(<section[^>]*\bid="%s"[^>]*>.*?<span class="st-chapter-num" aria-hidden="true">)[^<]*' % sid, r"\g<1>" + n, h, count=1, flags=re.S)
    # one clear art button at the top of the library
    if 'class="st-lib-art"' not in h:
        h = re.sub(r'(<section[^>]*\bid="library"[^>]*>.*?</div></div>)',
                   r'\1<div class="st-lib-art"><p>Every book below is free to read. Here for the art instead?</p>'
                   r'<a href="/portals">Open the portal pendants <span aria-hidden="true">&#8594;</span></a></div>', h, count=1, flags=re.S)
    if 'id="nfTutorial" inert' not in h:
        h = h.replace('id="nfTutorial"', 'id="nfTutorial" inert', 1)   # the tour never opens now; keep it out of the tab order
    v17 = ('<p class="updates-version">v17 &mdash; 2026-11-08</p>\n      <ul>\n        <li>The homepage now opens straight away: '
           'the intro plays in the background instead of making you wait, and the page is over 100 times smaller, so it '
           'loads fast on any phone.</li>\n        <li>New <a href="#start-here">Start here</a>: pick what brings you here and see '
           'the books that may help.</li>\n        <li>All the books come first, the Art door opens the portal pendants, and the '
           'menu now works on phones too. Music plays when you press the music button.</li>\n      </ul>\n      ')
    h = re.sub(r'<p class="updates-version">v17 &mdash; 2026-11-08</p>.*?</ul>\n      ', "", h, count=1, flags=re.S)
    m = re.search(r'<p class="updates-version">v1[56] &mdash;', h)
    if m:
        h = h[:m.start()] + v17 + h[m.start():]
    for a, b in FACTS:
        h = h.replace(a, b)
    h = h.replace(OLD_HERO_JS, HERO_JS)
    h = re.sub(r'<script id="v17-js">.*?</script>\n?', "", h, flags=re.S)
    h = h.replace("</body>", NAV_JS + "\n</body>", 1)
    h = re.sub(r'<style id="v17-css">.*?</style>\n?', "", h, flags=re.S)
    h = h.replace("</head>", f"<style id=\"v17-css\">{START_CSS}</style>\n</head>", 1)
    return h


def main():
    h = S.read(SRC)
    before = len(h.encode())
    h, report = extract_media(h)
    # the intro's poster frame
    if not (MEDIA / "intro-poster.webp").exists() and (MEDIA / "intro.mp4").exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(MEDIA / "intro.mp4"), "-frames:v", "1", "-q:v", "70",
                        str(MEDIA / "intro-poster.webp")], check=True)
    h = restructure(h)
    S.write(SRC, h)
    after = len(h.encode())
    print(f"homepage HTML {before/1e6:.2f} MB -> {after/1e6:.2f} MB")
    tot = {}
    for kind, a, b in report:
        x = tot.setdefault(kind, [0, 0, 0]); x[0] += 1; x[1] += a; x[2] += b
    for k, (n, a, b) in tot.items():
        print(f"  {k:5} x{n:<3} {a/1e6:6.2f} MB embedded -> {b/1e6:6.2f} MB as files" + (" (loads only on play)" if k == "audio" else ""))


if __name__ == "__main__":
    main()
