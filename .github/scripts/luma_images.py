#!/usr/bin/env python3
"""Map upcoming Luma event URLs to their cover images (og:image).

Reads calendar/luma.ics, writes calendar/luma-images.json. Only URLs not
already in the JSON are fetched; entries for events no longer upcoming
are dropped.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

ICS = 'calendar/luma.ics'
OUT = 'calendar/luma-images.json'

text = re.sub(r'\r?\n[ \t]', '', open(ICS, encoding='utf-8').read())
cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y%m%d')

urls = set()
for block in text.split('BEGIN:VEVENT')[1:]:
    start = re.search(r'^DTSTART[^:\n]*:(\d{8})', block, re.M)
    url = re.search(r'https://(?:luma\.com|lu\.ma)/[A-Za-z0-9_-]+', block)
    if start and url and start.group(1) >= cutoff:
        urls.add(url.group(0))

try:
    known = json.load(open(OUT))
except (OSError, ValueError):
    known = {}

result = {}
for url in sorted(urls):
    if url in known:
        result[url] = known[url]
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'replace')
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', page)
        if m:
            result[url] = html.unescape(m.group(1))
    except Exception as e:  # one bad page shouldn't sink the run
        print('skip %s: %s' % (url, e), file=sys.stderr)

with open(OUT, 'w') as f:
    json.dump(result, f, indent=2, sort_keys=True)
    f.write('\n')
print('%d/%d events have images' % (len(result), len(urls)))
