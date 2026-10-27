#!/usr/bin/env python3
"""Write hub/sitemap.xml from the hub's own routing rules, so the sitemap lists exactly the paths the domain serves.

Every exact `/slug  https://...  200` rule in hub/catalogue-redesign._redirects is a page on noblefathercreations.com;
the NFC guide is served from the hub's /nfc rules and is added by hand below. The Pattern Decoder's 322 pages have
their own sitemap (/playbook/sitemap.xml, written by design/build-decoder-v15.py); hub/robots.txt names both.

    python3 scripts/build-root-sitemap.py
"""
import datetime
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ORIGIN = "https://noblefathercreations.com"

rules = open(os.path.join(ROOT, "hub", "catalogue-redesign._redirects"), encoding="utf-8").read()
paths = ["/"] + re.findall(r"^(/[a-z0-9-]+)\s+https://\S+\s+200\s*$", rules, re.M) + ["/nfc"]
today = datetime.date.today().isoformat()
with open(os.path.join(ROOT, "hub", "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             + "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (ORIGIN + (p if p != "/" else "/"), today)
                       for p in dict.fromkeys(paths))
             + "</urlset>\n")
print("hub/sitemap.xml:", len(dict.fromkeys(paths)), "addresses")
