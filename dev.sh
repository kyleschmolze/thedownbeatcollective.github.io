#!/usr/bin/env bash
# Local dev for the site (plain static HTML, no build step).
#   ./dev.sh          serve at http://localhost:8000  (PORT=3000 ./dev.sh to change)
#   ./dev.sh sync     refresh the calendar feed mirrors from Google + Luma, same as the GitHub Action
set -euo pipefail
cd "$(dirname "$0")"

if [ "${1:-}" = "sync" ]; then
  fetch() {
    curl -fsSL --retry 3 "$1" -o "$2.tmp"
    grep -q 'BEGIN:VCALENDAR' "$2.tmp"
    mv "$2.tmp" "$2"
    python3 .github/scripts/normalize_ics.py "$2"
  }
  fetch 'https://calendar.google.com/calendar/ical/06093b94873d5bcca7b4acaebde9cd8b7e8f40822f3dce5a3eccfdf84d162930%40group.calendar.google.com/public/basic.ics' calendar/events.ics
  fetch 'https://api.luma.com/ics/get?entity=calendar&id=cal-tmZVAT6bkyIXJMn' calendar/luma.ics
  python3 .github/scripts/luma_images.py
  echo "Synced. Review with: git diff --stat"
  exit 0
fi

PORT="${PORT:-8000}"
echo "Serving on http://localhost:$PORT  (calendar: /calendar/, colors playground: /calendar-colors/)"
exec python3 -m http.server "$PORT"
