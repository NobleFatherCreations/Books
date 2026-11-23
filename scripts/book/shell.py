#!/usr/bin/env python3
"""The shared book shell: everything a v2 book page needs that is not the book's own skin.

Moved word for word out of scripts/seo/build_longafter_v2.py (The Long After v6, 2026-11-23), so every book renders
the same `:::` blocks, Copy buttons, real checkboxes, Just the steps toggle, progress bar, On this page menu, share
line, discreet mode, Leave (button and Escape twice), rail and dock, print rules and old #/c/N forwarding.
Each book keeps its own skin (palette, fonts, cover, part names) in its builder. Plain functions, no framework.

Use:  import shell as SH; SH.BASE = "/scale"; html = SH.md(body)
"""
import html
import importlib.util as _iu
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/seo"))
import seo_common as S  # noqa: E402

BASE = ""   # the book's path on the site, e.g. "/longafter"; set by the builder before rendering

_spec = _iu.spec_from_file_location("nf_catalogue", ROOT / "scripts/nf-catalogue.py")
CAT = _iu.module_from_spec(_spec); _spec.loader.exec_module(CAT)


def parse(src):
    out = {}
    for f in sorted(Path(src).glob("[0-9][0-9]-*.md")):
        for block in re.split(r"^=== ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            slug, rest = block.split("\n", 1)
            head, _, body = rest.partition("\n---\n")
            out[slug.strip()] = {"meta": dict(re.findall(r"^(\w+):\s*(.+)$", head, re.M)), "body": body.strip()}
    return out



# ---------------------------------------------------------------- Markdown (the small subset the book uses)
def href(target):
    if target.startswith("ch:"):
        slug, _, frag = target[3:].partition("#")
        return f"{BASE}/{slug}" + (f"#{frag}" if frag else "")
    return target


def inline(t):
    t = html.escape(smart(t), quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(href(m.group(2)))}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def smart(t):
    t = re.sub(r'(^|[\s(\[>*_])"', "\\1\u201c", t)
    t = t.replace('"', "\u201d")
    t = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", t)
    t = re.sub(r"(^|[\s(\[>])'", "\\1\u2018", t)
    t = t.replace("'", "\u2019")
    return t




LONG_TEL = re.compile(r"(?<![\w-])(1-800-\d{3}-\d{4}|0\d{2,3}(?: \d{2,4}){2,3}|01 \d{3} \d{4}|1800 \d{3} \d{3}|13 11 14|116 123)(?![\w-])")
SHORT_TEL = re.compile(r"(?<![\w.,-])(911|999|000|112|988|211)(?![\w-])")
SMS = re.compile(r"text START to (88788)")


def telify(h):
    """Tap-to-call on the crisis pages: numbers in text (never inside a tag or an existing link) become tel:/sms: links."""
    out, in_a = [], 0
    for part in re.split(r"(<[^>]+>)", h):
        if part.startswith("<"):
            in_a += 1 if re.match(r"<a[\s>]", part) else (-1 if part.startswith("</a") else 0)
            out.append(part); continue
        if in_a:
            out.append(part); continue
        part = SMS.sub(lambda m: f'text START to <a class="tel" href="sms:{m.group(1)}?body=START">{m.group(1)}</a>', part)
        bits = re.split(r"(<a [^>]+>.*?</a>)", part)
        for i, b in enumerate(bits):
            if b.startswith("<a "):
                continue
            b = LONG_TEL.sub(lambda m: f'<a class="tel" href="tel:{re.sub(r"[^0-9]", "", m.group(1))}">{m.group(1)}</a>', b)
            segs = re.split(r"(<a [^>]+>.*?</a>)", b)
            bits[i] = "".join(x if x.startswith("<a ") else SHORT_TEL.sub(lambda m: f'<a class="tel" href="tel:{m.group(1)}">{m.group(1)}</a>', x) for x in segs)
        out.append("".join(bits))
    return "".join(out)




def md(body):
    lines = body.split("\n")
    out, i, used, stack = [], 0, set(), []
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if ln.startswith(":::"):   # block fences (BOOK-PIPELINE-V2 section 3): "::: kind [arg]" opens, ":::" closes
            kind, _, arg = ln[3:].strip().partition(" ")
            if kind:
                extra = f' data-arg="{html.escape(arg)}"' if arg else ""
                out.append(f'<div class="blk blk-{html.escape(kind)}"{extra}>'); stack.append(kind)
            else:
                out.append("</div>"); stack and stack.pop()
            i += 1; continue
        if stack and stack[-1] == "decoder" and ln.startswith("**"):   # one element per voice; Copy on the reply
            voices = []
            while i < len(lines) and lines[i].startswith("**"):
                lab, _, rest = inline(lines[i].strip()).partition("</strong>")
                k = "say" if "They say" in lab else "why" if "What it" in lab else "reply"
                lab = lab.replace("<strong>", "<strong class=\"dv-l\">") + "</strong>"
                if k == "reply":   # Copy sits beside the label, so it shows as soon as the reply does (never under the dock)
                    lab = f'<span class="dv-h">{lab} <button class="dv-copy" type="button" data-js>Copy</button></span>'
                voices.append(f'<p class="dv dv-{k}">{lab} <span class="dv-t">{rest.strip()}</span></p>')
                i += 1
            out.append('<div class="dv-p">' + "".join(voices) + "</div>"); continue
        if ln.startswith("## "):
            text = ln[3:].strip()
            hid = S.slugify(text, 60)
            while hid in used:
                hid += "-2"
            used.add(hid)
            out.append(f'<h2 id="{hid}">{inline(text)}</h2>'); i += 1; continue
        if ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:].strip())}</h3>"); i += 1; continue
        if ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i][1:].lstrip()); i += 1
            paras, cur = [], []
            for b in block:
                if b.strip():
                    cur.append(b)
                else:
                    if cur: paras.append(" ".join(cur)); cur = []
            if cur: paras.append(" ".join(cur))
            cls = "say" if any("**Say" in p for p in paras) else "pull"
            out.append(f'<blockquote class="{cls}">' + "".join(f"<p>{inline(p)}</p>" for p in paras) + "</blockquote>")
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body_rows = rows[0], [r for r in rows[1:] if not set("".join(r)) <= set("-: ")]
            t = '<div class="tbl"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body_rows)
            out.append(t + "</tbody></table></div>"); continue
        if re.match(r"^\s*- ", ln) or ln.startswith("☐"):
            items = []
            while i < len(lines) and (re.match(r"^\s*- ", lines[i]) or lines[i].startswith("☐")):
                items.append(lines[i]); i += 1
            if stack and stack[-1] == "sort":   # "- item || answer": the answer stays behind a tap (recall before reveal)
                items = [re.sub(r"^\s*- ", "", x).split(" || ", 1) for x in items]
                out.append('<ul class="sort">' + "".join(
                    f'<li><details><summary>{inline(q[0])}</summary><p>{inline(q[1])}</p></details></li>' if len(q) == 2
                    else f"<li>{inline(q[0])}</li>" for q in items) + "</ul>"); continue
            lis = "".join(f'<li class="check"><label><input type="checkbox"><span>{inline(x[1:].lstrip())}</span></label></li>' if x.startswith("☐") else f"<li>{inline(re.sub(r'^\s*- ', '', x))}</li>" for x in items)
            out.append(f'<ul{" class=\"checks\"" if items[0].startswith("☐") else ""}>{lis}</ul>'); continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(## |### |>|\||\s*- |\d+\. |☐|:::)", lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)




def split_sources(body):
    main, _, src = body.partition("\n## Sources")
    return main.strip(), src.strip()


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()




# Lucide paths (tools/lucide-icons-lucide), drawn as CSS masks so they take the part's accent.
ICONS = {
    "lamp": '<path d="M12 12v6"/><path d="M4.077 10.615A1 1 0 0 0 5 12h14a1 1 0 0 0 .923-1.385l-3.077-7.384A2 2 0 0 0 15 2H9a2 2 0 0 0-1.846 1.23Z"/><path d="M8 20a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1z"/>',
    "door": '<path d="M11 20H2"/><path d="M11 4.562v16.157a1 1 0 0 0 1.242.97L19 20V5.562a2 2 0 0 0-1.515-1.94l-4-1A2 2 0 0 0 11 4.561z"/><path d="M11 4H8a2 2 0 0 0-2 2v14"/><path d="M14 12h.01"/><path d="M22 20h-3"/>',
    "msg": '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/><path d="M8 12h.01"/><path d="M12 12h.01"/><path d="M16 12h.01"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/>',
    "scale": '<path d="M12 3v18"/><path d="m19 8 3 8a5 5 0 0 1-6 0zV7"/><path d="M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1"/><path d="m5 8 3 8a5 5 0 0 1-6 0zV7"/><path d="M7 21h10"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4"/><path d="M12 16h.01"/>',
    "moon": '<path d="M18 5h4"/><path d="M20 3v4"/><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/>',
    "printer": '<path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 9V3a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v6"/><rect x="6" y="14" width="12" height="8" rx="1"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "signpost": '<path d="M12 13v8"/><path d="M12 3v3"/><path d="M2.354 10.354a1.207 1.207 0 0 1 0-1.708l2.06-2.06A2 2 0 0 1 5.828 6h12.344a2 2 0 0 1 1.414.586l2.06 2.06a1.207 1.207 0 0 1 0 1.708l-2.06 2.06a2 2 0 0 1-1.414.586H5.828a2 2 0 0 1-1.414-.586z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
}


def ico(name, stroke="black"):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{stroke}' stroke-width='1.75' "
           f"stroke-linecap='round' stroke-linejoin='round'>{ICONS[name].replace(chr(34), chr(39))}</svg>")
    return 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'


def mask(name):
    return f"-webkit-mask:{ico(name)} center/contain no-repeat;mask:{ico(name)} center/contain no-repeat;"




SHELL_CSS = f"""/* checklists: real checkboxes, ticks live in memory only (nothing stored, reset on reload) */
ul.checks label{{display:flex;align-items:flex-start;gap:12px;min-height:44px;padding:10px 0;cursor:pointer}}
ul.checks input{{appearance:none;-webkit-appearance:none;flex:none;width:22px;height:22px;margin:.2em 0 0;border:2px solid var(--acc);border-radius:5px;background:transparent;cursor:pointer;display:grid;place-content:center}}
ul.checks input:checked{{background:var(--acc) {ico('check', '#1c1322')} center/16px no-repeat}}
/* shell */
[hidden]{{display:none!important}}
html:not(.js) [data-js]{{display:none!important}}
button{{font-family:var(--sans)}}
details:not([open])>:not(summary){{display:none}}
/* compact chapter header: byline on one line where it fits, then one row of controls (44px tall) */
.by{{font-size:.9rem;line-height:1.45;color:#f1e9ee;margin:10px 0 0}}
.sky:has(.hrow){{padding-bottom:44px}}
.hrow{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0 0}}.hrow .tools,.hrow .otp{{margin:0}}.otp[open]{{flex-basis:100%;order:2}}.by a{{color:#fff;display:inline-block;padding:10px 0;margin:-10px 0}}
.tools{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:12px 0 0}}
.mode{{display:inline-flex;padding:3px;border-radius:999px;background:rgba(10,8,16,.55);border:1px solid rgba(255,255,255,.14)}}
.mode button,.disc{{min-height:44px;padding:0 14px;border-radius:999px;border:0;background:none;color:#f1e9ee;font:600 1rem/1 var(--sans);cursor:pointer}}
.mode button[aria-pressed=true]{{background:var(--acc);color:#1c1322}}
.disc{{border:1px solid rgba(255,255,255,.22);background:rgba(10,8,16,.4)}}.disc[aria-pressed=true]{{background:#f1e9ee;color:#1c1322}}
.otp{{margin:12px 0 0;background:rgba(10,8,16,.55);border:1px solid rgba(255,255,255,.14);border-radius:12px;font-size:1rem}}
.otp summary{{cursor:pointer;min-height:44px;display:flex;align-items:center;padding:0 14px;font-weight:600;color:#fff}}
.otp summary::before{{content:"▸";margin-right:10px;transition:transform .2s var(--ease-out)}}.otp[open] summary::before{{transform:rotate(90deg)}}
.otp ol{{margin:0;padding:0 14px 8px;list-style:none}}.otp a{{display:block;padding:10px 0;color:#f1e9ee;border-top:1px solid rgba(255,255,255,.1);text-decoration:none}}
.prog{{position:fixed;top:0;left:0;right:0;height:3px;z-index:9600;pointer-events:none}}.prog i{{display:block;height:100%;background:var(--acc);transform:scaleX(0);transform-origin:0 50%}}
.end{{max-width:44rem;margin:40px auto 0;padding-top:20px;border-top:1px solid var(--line);font-size:1rem;color:var(--fg2)}}
.end p{{margin:0 0 8px}}.end a{{display:inline-block;padding:10px 0;margin:-10px 0}}
.share button{{min-height:44px;padding:0 4px;border:0;background:none;color:var(--acc);font:600 1rem/1 var(--sans);text-decoration:underline;text-underline-offset:.2em;cursor:pointer}}
footer .disc{{color:var(--fg2);margin-top:8px}}
.rail,.dock .leave{{font-family:var(--sans)}}
.rail{{display:none}}
.dock{{position:fixed;left:0;right:0;bottom:0;z-index:8999;display:grid;grid-template-columns:auto auto 1fr;align-items:end;gap:8px;padding:8px 12px calc(8px + env(safe-area-inset-bottom));
background:var(--night);border-top:1px solid var(--line)}}
.dock a,.dock button{{display:flex;align-items:center;justify-content:center;min-height:48px;padding:0 12px;border-radius:12px;border:1px solid var(--line);background:var(--panel);
color:var(--fg);font:600 .95rem/1.1 var(--sans);white-space:nowrap;text-decoration:none;text-align:center;cursor:pointer}}
.dock button[aria-pressed=true]{{background:var(--acc);color:#1c1322;border-color:var(--acc)}}
.dock [data-mode-toggle]{{min-width:8.4em}}.dock .leave{{min-height:56px;background:#7a2730;border-color:#a33a45;color:#fff;font-size:1.1rem}}
body:has(.dock) footer{{padding-bottom:120px}}
@media (max-width:1099px){{.tools .mode{{display:none}}}}
@media (min-width:1100px){{.dock{{display:none}}.otp{{display:none}}
.rail{{display:flex;flex-direction:column;gap:6px;position:fixed;z-index:50;top:84px;right:calc(50% + 22rem + 24px);width:min(240px,calc(50vw - 22rem - 40px));max-height:calc(100vh - 100px);overflow:auto;
padding:14px;background:rgba(17,14,25,.94);border:1px solid var(--line);border-radius:14px;font-size:.95rem;line-height:1.35}}
.rail p{{margin:0}}.rail .r-loc a{{color:var(--acc);display:inline;padding:0;margin:0}}.rail .r-t{{font:400 1.2rem/1.2 var(--disp);color:#fff;margin:4px 0 6px}}
.rail ol{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}}.rail ol a{{display:block;padding:9px 0;color:var(--fg2);text-decoration:none;border-bottom:1px solid var(--line)}}
.rail ol a:hover{{color:#fff}}
.rail .leave{{position:sticky;bottom:0;flex:none;box-shadow:0 -12px 12px rgba(17,14,25,.94);margin-top:10px;min-height:52px;border-radius:12px;background:#7a2730;border:1px solid #a33a45;color:#fff;font:600 1.1rem/1 var(--sans);cursor:pointer}}}}
"""


def js(chapters, routes, base):
    return f"""<script>
(function(){{var O={json.dumps(chapters)},R={json.dumps(routes)},h=location.hash,m;
if((m=h.match(/^#\\/c\\/(\\d+)/))&&O[m[1]])location.replace('{base}/'+O[m[1]]);
else if((m=h.match(/^#\\/(\\w+)/))&&R[m[1]])location.replace('{base}/'+R[m[1]]);
var D=document,H=D.documentElement,$$=function(q){{return D.querySelectorAll(q)}};
function leave(){{try{{document.title='New Tab';document.body.innerHTML='';}}catch(e){{}}location.replace('about:blank');}}
D.addEventListener('click',function(e){{var t=e.target.closest&&e.target.closest('[data-leave]');if(t){{e.preventDefault();leave();}}}});
addEventListener('beforeprint',function(){{$$('details').forEach(function(d){{d.open=true}})}});
var esc=0;D.addEventListener('keydown',function(e){{if(e.key!=='Escape'||D.querySelector('.nf-open,[data-nf-open]'))return;
var n=Date.now();if(n-esc<1500)leave();else esc=n;}});
/* nothing below stores anything: every setting lives in memory and resets on reload */
function steps(on){{H.classList.toggle('steps',on);$$('[data-mode]').forEach(function(b){{b.setAttribute('aria-pressed',String((b.dataset.mode==='steps')===on))}});
$$('[data-mode-toggle]').forEach(function(b){{b.setAttribute('aria-pressed',String(on));b.textContent=on?'Full read':'Just the steps'}});}}
$$('[data-mode]').forEach(function(b){{b.onclick=function(){{steps(b.dataset.mode==='steps')}}}});
$$('[data-mode-toggle]').forEach(function(b){{b.onclick=function(){{steps(!H.classList.contains('steps'))}}}});
var title0=D.title,disc=false,fav=null;$$('[data-discreet]').forEach(function(b){{b.onclick=function(){{disc=!disc;D.title=disc?'Reading':title0;
if(disc){{fav=D.createElement('link');fav.rel='icon';fav.href='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 16 16%22%3E%3Crect width=%2216%22 height=%2216%22 rx=%223%22 fill=%22%23888%22/%3E%3C/svg%3E';D.head.appendChild(fav)}}
else if(fav){{D.head.removeChild(fav);fav=null}}$$('[data-discreet]').forEach(function(x){{x.setAttribute('aria-pressed',String(disc))}});}}}});
function flash(b,t,t0){{b.textContent=t;clearTimeout(b._t);b._t=setTimeout(function(){{b.textContent=t0}},2000)}}
$$('.dv-copy').forEach(function(b){{if(!navigator.clipboard){{b.hidden=true;return}}b.onclick=function(){{
var x=b.closest('.dv').querySelector('.dv-t').textContent.trim(),q=x.match(/\\u201c[^\\u201d]+\\u201d/g);if(q)x=q.map(function(s){{return s.slice(1,-1)}}).join(' ');
navigator.clipboard.writeText(x).then(function(){{flash(b,'Copied','Copy')}})}}}});
$$('[data-share]').forEach(function(b){{b.onclick=function(){{var u=location.href.split('#')[0];
if(navigator.share)navigator.share({{title:D.title,url:u}}).catch(function(){{}});
else if(navigator.clipboard)navigator.clipboard.writeText(u).then(function(){{flash(b,'Link copied','Share this page')}});}}}});
var bar=D.querySelector('.prog i');if(bar){{var f=0;addEventListener('scroll',function(){{if(f)return;f=requestAnimationFrame(function(){{f=0;
var d=H.scrollHeight-innerHeight;bar.style.transform='scaleX('+(d>0?Math.min(1,scrollY/d):0)+')'}})}},{{passive:true}});}}
}})();
</script>"""


def house(slug):
    src = S.read(ROOT / "library/silence/index.html")
    css, chrome, js = S.house_parts(CAT.retoc(src, slug))
    return css, chrome, js, S.beacon(src)

