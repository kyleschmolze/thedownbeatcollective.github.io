#!/usr/bin/env python3
"""Make a mirrored ICS file stable so unchanged feeds produce no diff.

Drops per-fetch volatile properties (DTSTAMP, SEQUENCE) and sorts the
VEVENT blocks, since Google returns events in varying order. Edits in place.
"""
import re
import sys

for path in sys.argv[1:]:
    text = open(path, newline='').read()
    parts = re.split(r'(?=BEGIN:VEVENT)', text)
    head, events = parts[0], parts[1:]
    tail = ''
    if events:
        i = events[-1].rindex('END:VCALENDAR')
        events[-1], tail = events[-1][:i], events[-1][i:]
    volatile = re.compile(r'^(DTSTAMP|SEQUENCE)[:;]')
    cleaned = []
    for ev in events:
        lines = ev.splitlines(keepends=True)
        out, drop = [], False
        for ln in lines:
            if ln[:1] in (' ', '\t'):  # folded continuation
                if not drop:
                    out.append(ln)
                continue
            drop = bool(volatile.match(ln))
            if not drop:
                out.append(ln)
        cleaned.append(''.join(out))
    with open(path, 'w', newline='') as f:
        f.write(head + ''.join(sorted(cleaned)) + tail)
