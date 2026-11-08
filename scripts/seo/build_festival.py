#!/usr/bin/env python3
"""The Festie Bible: one plain page per guide (21) and per scenario (270), rendered from the book's own
FESTIE_DATA with the book's own section labels (same order as its renderScenario()); plus the findability
head, a static notice + licence the app's footer lacked, and the v11 entry in the book's own changelog.

Run: python3 scripts/seo/build_festival.py   (reads/writes library/festival/)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_common as S

OUT = S.ROOT / "library/festival"
CONTACT = "dapperdadnfc@gmail.com"
BOOK = {
    "slug": "festival", "title": "The Festie Bible", "version": "v11",
    "fonts": ["Fraunces", "Hanken Grotesk"],
    "theme": {"scheme": "dark", "bg": "#141019", "fg": "#ECE4D6", "fg2": "#BCB1A0", "panel": "#1B1522",
              "line": "#2C2236", "glow": "#3a2028", "acc": "#E8C879", "accink": "#141019",
              "disp": "'Fraunces',Georgia,serif", "body": "'Hanken Grotesk',system-ui,sans-serif"},
    "description": ("Twenty-one free field guides to psychological safety at festivals, one for each corner of the scene: "
                    "women, men, first-timers, sober, LGBTQ+, BIPOC, disabled, artists, vendors, crew, harm reduction and "
                    "more. 270 real-feeling scenarios with the tells, what is happening, and what to say."),
    "index_title": "The Festie Bible: 21 Free Festival Safety Guides",
    "index_desc": ("Twenty-one free festival safety guides: women, first-timers, sober, LGBTQ+, artists, vendors, crew and "
                   "more. 270 scenarios, the tells, and what to say."),
    "genre": ["Harm reduction", "Self-help", "Psychology"],
    "about": ["Festival safety", "Love bombing", "Coercive control", "Consent", "Harm reduction",
              "Sober festival", "Workplace exploitation in events", "Predatory behavior"],
    "keywords": ["festival safety tips", "festival love bombing", "first festival guide", "sober at a festival",
                 "festival vendor exploitation", "free festival guide"],
    "notice_short": ("Field guides for awareness and harm reduction, not medical, legal or mental-health advice. "
                     "Scenarios are illustrative. In immediate danger, contact emergency services; in crisis, call or text 988."),
    "notice_href": "/festival#notice",
    "unit": "guides and scenarios",
}
RELATED = [("wook", "The Festie Codex", "The full field manual: 33 chapters on spotting Wooks in sheep's clothing"),
           ("playbook", "The Pattern Decoder", "310 manipulation and control tactics, each with signs and what to do"),
           ("feminine", "The Sovereign Divine Feminine", "A field guide to manipulation tactics and counter-moves")]

NOTICE_HTML = f"""<section id="notice" style="max-width:44rem;margin:48px auto 120px;padding:24px;border:1px solid rgba(201,163,91,.16);border-radius:12px;color:#BCB1A0;font:400 15px/1.6 'Hanken Grotesk',system-ui,sans-serif">
<h2 style="font:600 20px/1.3 'Fraunces',Georgia,serif;color:#ECE4D6;margin:0 0 12px">About these guides</h2>
<p style="margin:0 0 12px">Twenty-one field guides for awareness and harm reduction, written by festies, for festies. They are not medical, legal or mental-health advice, and they diagnose no one. Scenarios are illustrative, not accounts of real, identifiable people. In immediate danger, contact emergency services; in crisis, call or text 988.</p>
<p style="margin:0 0 12px">Every guide and scenario also has its own page: <a href="/festival/contents" style="color:#E8C879">read them guide by guide</a>. Corrections and feedback: <a href="mailto:{CONTACT}" style="color:#E8C879">{CONTACT}</a>.</p>
<p style="margin:0">{S.LICENSE_LINE}</p>
</section>"""


def data_of(h):
    m = re.search(r"FESTIE_DATA\s*=\s*", h)
    d, _ = json.JSONDecoder().raw_decode(h, m.end())
    return d


def hook_title(hk):
    return S.title_case(hk.strip('"'))


def build(h):
    d = data_of(h)
    terms = S.decoder_terms()
    order = []
    for g in d["guides"]:
        gslug = S.slugify(g["role"], 40)
        role_tc = S.title_case(g["role"])
        mv = f"{g['acronym']} · {g['edition']}"
        checks = "".join(f"<li><strong>{S.esc(c['letter'])} — {S.esc(c['name'])}.</strong> {S.esc(c['desc'])}</li>" for c in g["checks"])
        outline = "".join(f"<li><strong>{S.esc(o['key'].title())}.</strong> {S.esc(o['desc'])}</li>" for o in g["outline"])
        sentences = "".join(f"<li>{S.esc(s)}</li>" for s in g.get("sentences", []))
        sc_list = "".join(f'<li class="nav"><a href="/festival/{g["slug"]}-{S.slugify(hook_title(s["hook"]), 44)}">{S.esc(hook_title(s["hook"]))}</a> — '
                          f'{S.esc(s["archetype"])}</li>' for s in g["scenarios"])
        body = (f"<p>{S.esc(g['intro'])}</p>"
                f"<h2>The {S.esc(g['acronym'])} check</h2><ul>{checks}</ul>"
                f"<h2>How the guide is built</h2><ul>{outline}</ul>"
                + (f"<h2>Sentences to carry</h2><ul>{sentences}</ul>" if sentences else "")
                + f"<h2>The {len(g['scenarios'])} scenarios</h2><ol>{sc_list}</ol>")
        order.append(dict(slug=gslug, title=f"{g['acronym']}: {g['edition']}", eyebrow=f"Guide for {role_tc.lower()}",
                          lede=g["intro"], movement=mv, html=body,
                          seo_title=S.fit_title(f"Festival Safety Guide for {role_tc}", "The Festie Bible"),
                          desc=S.clip(f"A free festival safety guide for {g['role'].lower()}: {g['intro']} "
                                      f"{len(g['scenarios'])} scenarios with the tells and what to say.", 158)))
        for i, s in enumerate(g["scenarios"]):
            hk = hook_title(s["hook"])
            tells = "".join(f"<li>{S.esc(t)}</li>" for t in s["tells"])
            dark = (f"<h2>Dark Reality{' — ' + S.esc(s['darkTitle']) if s.get('darkTitle') else ''}</h2><p>{S.esc(s['dark'])}</p>"
                    if s.get("dark") else "")
            body = ((f"<p><strong>Clinical:</strong> {S.esc(s['clinical'])}</p>" if s.get("clinical") else "")
                    + (f"<h2>Who You’re Dealing With</h2><p>{S.esc(s['who'])}</p>" if s.get("who") else "")
                    + (f"<h2>The Scene</h2><p>{S.esc(s['scene'])}</p>" if s.get("scene") else "")
                    + (f"<h2>Spot It — The Tells</h2><ul>{tells}</ul>" if tells else "")
                    + (f"<h2>What’s Actually Happening</h2><p>{S.esc(s['happening'])}</p>" if s.get("happening") else "")
                    + (f"<blockquote><p>{s['check']}</p></blockquote>" if s.get("check") else "")
                    + dark
                    + f"<h2>The Move</h2><p>{S.esc(s['move'])}</p>"
                    + f"<h2>Say This</h2><blockquote><p>“{S.esc(s['say'])}”</p></blockquote>"
                    + f"<h2>The Truth</h2><p>{S.esc(s['truth'])}</p>"
                    + f'<p class="nav"><a href="/festival/{gslug}">Back to the {S.esc(g["acronym"])} guide</a> · '
                      f'<a href="/festival#/{g["slug"]}/{i + 1}">Open this scenario in the book</a></p>')
            body = S.link_terms(body, terms, limit=4)
            clinical = (s.get("clinical") or "").split("/")[0].strip()
            seo = f"“{hk}”: {clinical}" if clinical else hk
            order.append(dict(slug=f"{g['slug']}-{S.slugify(hk, 44)}", title=hk,
                              eyebrow=f"{g['acronym']} · {S.title_case(s['section'])} · {i + 1} of {len(g['scenarios'])}",
                              lede=s["archetype"], movement=mv, html=body,
                              seo_title=S.fit_title(seo, "Festie Bible"),
                              desc=S.clip(f"{s['archetype']} ({clinical or s['section'].title()}), for {g['role'].lower()} "
                                          f"at festivals: {S.first_sentences(s['who'], 100)}", 158)))
    for c in order:
        c["html"], c["heads"] = S.give_heading_ids(c["html"])
    slugs = [c["slug"] for c in order]
    assert len(slugs) == len(set(slugs)), "duplicate festival page slugs"
    return order, d


def patch_index(h, chs, d):
    h = S.inject_index(BOOK, h, chs)
    h = h.replace('<meta name="copyright" content="Copyright © 2026 Shae Stovell. All rights reserved.">',
                  '<meta name="copyright" content="© 2026 Shae Stovell. Free to share with credit under CC BY-NC-ND 4.0.">')
    h = h.replace("'<div class=\"fb-disclaimer\">For educational purposes only • Noble Father Creations • In immediate danger? Contact emergency services.</div>'",
                  "'<div class=\"fb-disclaimer\">For educational purposes only; not medical, legal or mental-health advice • Noble Father Creations • In immediate danger? Contact emergency services.</div>'")
    h = h.replace("'<div class=\"fb-disclaimer\">Copyright © 2026 Shae Stovell. All rights reserved. The Festie Bible and Noble Father Creations are works of Shae Stovell.</div>'",
                  "'<div class=\"fb-disclaimer\">" + S.LICENSE_LINE.replace("'", "\\'") + " The Festie Bible and Noble Father Creations are works of Shae Stovell.</div>'")
    if "All rights reserved" in h:
        raise SystemExit("festival: an 'All rights reserved' line was not replaced")
    # the book's own changelog lives in its data: version + newest entry
    if data_of(h)["version"] != "v11":
        entry = {"version": "v11", "date": "2026-11-08",
                 "summary": ("Every guide and all 270 scenarios now also have their own pages, so a search or an AI "
                             "assistant can send someone straight to the one they need. Added a not-advice line, a "
                             "corrections address and the free licence (credit required, no selling).")}
        old_head = f'"updated":"{d["updated"]}","changelog":['
        assert h.count(old_head) == 1, "festival: changelog head not unique"
        h = h.replace(old_head, '"updated":"2026-11-08","changelog":[' + json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + ",", 1)
        old_ver = f'"version":"{d["version"]}"}}'
        assert h.count(old_ver) == 1, "festival: version key not unique"
        h = h.replace(old_ver, '"version":"v11"}', 1)
    h = re.sub(r'\n?<section id="notice" style=.*?</section>', "", h, flags=re.S)
    h = re.sub(r'\n?<h1 class="sr-title"[^>]*>.*?</h1>', "", h, flags=re.S)
    h = re.sub(r"(<body[^>]*>)", r'\1\n<h1 class="sr-title" style="position:absolute;width:1px;height:1px;overflow:hidden;'
               r'clip:rect(0 0 0 0);white-space:nowrap">The Festie Bible: Twenty-One Field Guides to Psychological Safety '
               r'in the Festival World</h1>', h, count=1)
    i = h.find('<div id="nf-chrome"')
    h = h[:i] + NOTICE_HTML + "\n" + h[i:]
    return h


def main():
    src = OUT / "index.html"
    h = S.read(src)
    for f in OUT.glob("*.html"):
        if f.name != "index.html":
            f.unlink()
    chs, d = build(h)
    S.write_book(BOOK, h, chs, OUT, RELATED)
    S.write(src, patch_index(h, chs, d))
    S.make_og(BOOK, OUT, "Free · 21 guides · 270 scenarios", "Know the pattern. Trust your body. Protect the magic.")
    print(f"festival: {len(chs)} pages")
    for c in chs[:4] + chs[21:24]:
        print(f"  /festival/{c['slug']:44} {len(S.plain(c['html']).split()):>5}w  {c['seo_title']}")


if __name__ == "__main__":
    main()
