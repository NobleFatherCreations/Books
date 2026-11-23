#!/usr/bin/env python3
"""Tell Bing / Yandex / Naver / Seznam (IndexNow) that pages changed. Run ONLY after a deploy is live and verified:
    python3 scripts/seo/indexnow.py <book> [<book> ...]     (submits that book's sitemap URLs)
The key file hub/3b85ef6f77878fe76e9845021f786fce.txt must be live at https://noblefathercreations.com/3b85ef6f77878fe76e9845021f786fce.txt first."""
import json, sys, urllib.request
from xml.etree import ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
KEY = "3b85ef6f77878fe76e9845021f786fce"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
urls = []
if "--live" in sys.argv:          # every sitemap the live robots.txt lists: the true set of what is online
    robots = urllib.request.urlopen("https://noblefathercreations.com/robots.txt", timeout=30).read().decode()
    for sm in [l.split(":", 1)[1].strip() for l in robots.splitlines() if l.lower().startswith("sitemap:")]:
        try: urls += [e.text for e in ET.fromstring(urllib.request.urlopen(sm, timeout=30).read()).iter(NS)]
        except Exception as ex: print("skipped", sm, ex)
for b in [a for a in sys.argv[1:] if not a.startswith("--")]:
    sm = ROOT / ("hub/sitemap.xml" if b == "hub" else "instruments/playbook/site/sitemap.xml" if b == "playbook" else f"library/{b}/sitemap.xml")
    urls += [e.text for e in ET.parse(sm).getroot().iter(NS)]
urls = list(dict.fromkeys(u for u in urls if u and u.startswith("https://noblefathercreations.com")))
body = json.dumps({"host": "noblefathercreations.com", "key": KEY, "keyLocation": f"https://noblefathercreations.com/{KEY}.txt", "urlList": urls[:10000]}).encode()
for ep in ("https://api.indexnow.org/indexnow", "https://www.bing.com/indexnow", "https://yandex.com/indexnow"):   # any one shares with all; three for safety
    req = urllib.request.Request(ep, data=body, headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "noblefathercreations-indexnow/1.0"})
    try: print(len(urls), "urls ->", ep, urllib.request.urlopen(req, timeout=30).status)
    except Exception as ex: print(len(urls), "urls ->", ep, "error", getattr(ex, "code", ex))
