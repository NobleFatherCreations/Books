#!/usr/bin/env python3
"""Regenerate design/snippets.html from the vendored Newsreader font.
Run this if the font changes or the CSS/JS below is edited.
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "tools" / "fonts" / "newsreader"
OUT = pathlib.Path(__file__).resolve().parent / "snippets.html"

roman = base64.b64encode((FONT_DIR / "Newsreader[opsz,wght].ttf").read_bytes()).decode("ascii")
italic = base64.b64encode((FONT_DIR / "Newsreader-Italic[opsz,wght].ttf").read_bytes()).decode("ascii")

TEMPLATE = """<!-- ============================================================
  NOBLE FATHER CREATIONS — shared design snippet
  Self-contained: no external requests. Paste this whole block once,
  right before </head> (font+tokens) is fine anywhere in <head>; the
  <script> at the end can go right before </body>.
  Source: design/snippets.html in the Wookbook repo — regenerate via
  design/build-snippets.py if the font or tokens change.
============================================================ -->
<style id="nfc-design-tokens">
  /* ---- self-hosted serif, embedded, zero network requests ---- */
  @font-face {{
    font-family:'Newsreader';
    src:url(data:font/ttf;base64,{roman}) format('truetype-variations');
    font-weight:200 800; font-style:normal; font-display:swap;
  }}
  @font-face {{
    font-family:'Newsreader';
    src:url(data:font/ttf;base64,{italic}) format('truetype-variations');
    font-weight:200 800; font-style:italic; font-display:swap;
  }}

  /* ---- 8px spacing scale ---- */
  :root {{
    --sp-1:8px; --sp-2:16px; --sp-3:24px; --sp-4:32px; --sp-5:48px;
    --sp-6:64px; --sp-7:96px; --sp-8:128px;
    /* palette tokens — dark + gold + crimson, override per-project if needed */
    --nfc-bg:#14110d; --nfc-ink:#e4dcc8; --nfc-gold:#a8813a; --nfc-crimson:#8a2432;
    --nfc-serif:'Newsreader', 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif;
  }}

  body {{ font-family:var(--nfc-serif); }}

  /* ---- reading-progress bar ---- */
  #nfc-progress {{
    position:fixed; top:0; left:0; height:3px; width:0%;
    background:linear-gradient(90deg,var(--nfc-gold),var(--nfc-crimson));
    z-index:999; transition:width .1s linear;
  }}

  /* ---- scroll fade-ins (native IntersectionObserver, class toggled by JS below) ---- */
  .nfc-reveal {{ opacity:0; transform:translateY(16px);
    transition:opacity .7s cubic-bezier(.16,1,.3,1), transform .7s cubic-bezier(.16,1,.3,1); }}
  .nfc-reveal.nfc-in {{ opacity:1; transform:none; }}
  @media (prefers-reduced-motion:reduce) {{
    .nfc-reveal {{ opacity:1; transform:none; transition:none; }}
  }}
</style>
<div id="nfc-progress" aria-hidden="true"></div>
<script id="nfc-design-js">
(function(){{
  /* reading-progress bar */
  var bar = document.getElementById('nfc-progress');
  function updateProgress(){{
    var h = document.documentElement;
    var scrolled = h.scrollTop || document.body.scrollTop;
    var height = (h.scrollHeight || document.body.scrollHeight) - h.clientHeight;
    var pct = height > 0 ? (scrolled / height) * 100 : 0;
    bar.style.width = pct + '%';
  }}
  addEventListener('scroll', updateProgress, {{passive:true}});
  addEventListener('resize', updateProgress);
  updateProgress();

  /* scroll fade-ins */
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function(entries){{
      entries.forEach(function(en){{
        if (en.isIntersecting) {{ en.target.classList.add('nfc-in'); io.unobserve(en.target); }}
      }});
    }}, {{rootMargin:'0px 0px -10% 0px', threshold:.12}});
    function wire(){{
      document.querySelectorAll('.nfc-reveal:not([data-nfc-seen])').forEach(function(el){{
        el.setAttribute('data-nfc-seen','1'); io.observe(el);
      }});
    }}
    wire();
    if (window.MutationObserver) new MutationObserver(wire).observe(document.body,{{childList:true,subtree:true}});
  }} else {{
    document.querySelectorAll('.nfc-reveal').forEach(function(el){{ el.classList.add('nfc-in'); }});
  }}
}})();
</script>
"""

OUT.write_text(TEMPLATE.format(roman=roman, italic=italic))
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")
