#!/usr/bin/env python3
"""Tell Bing / Yandex / Naver / Seznam (IndexNow) that pages changed. Run ONLY after a deploy is live and verified:
    python3 scripts/seo/indexnow.py <book> [<book> ...]     (submits that book's sitemap URLs)
The key file hub/3b85ef6f77878fe76e9845021f786fce.txt must be live at https://noblefathercreations.com/3b85ef6f77878fe76e9845021f786fce.txt first."""
import json, sys, urllib.request
from xml.etree import ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
KEY = "3b85ef6f77878fe76e9845021f786fce"
urls = []
for b in sys.argv[1:]:
    sm = ROOT / ("hub/sitemap.xml" if b == "hub" else f"library/{b}/sitemap.xml")
    urls += [e.text for e in ET.parse(sm).getroot().iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
body = json.dumps({"host": "noblefathercreations.com", "key": KEY, "keyLocation": f"https://noblefathercreations.com/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
print(len(urls), "urls ->", urllib.request.urlopen(req, timeout=30).status)
