# The Downbeat Collective

Static site for [thedownbeatcollective.com](https://thedownbeatcollective.com), hosted on GitHub Pages from `main`. Plain HTML/CSS/JS, no build step.

## Run it locally

You need Python 3 (already on macOS). From the repo root:

```sh
./dev.sh
```

Then open http://localhost:8000. Use `PORT=3000 ./dev.sh` for another port. A server is required (opening the files directly won't work) because the calendar pages `fetch()` local files.

## Layout

| Path | What it is |
|---|---|
| `index.html`, `subscribe.html` | Home page and Luma subscribe instructions |
| `css/`, `img/` | Styles and images |
| `calendar/` | `/calendar`: events as cards, from the Google Calendar + Luma feeds |
| `calendar-colors/` | `/calendar-colors`: unlisted copy with a brand color + heading font playground |

## Calendar data

Google and Luma don't allow browsers to read their feeds directly, so a GitHub Action (`.github/workflows/sync-calendar.yml`) mirrors them every 30 minutes into `calendar/events.ics`, `calendar/luma.ics`, and `calendar/luma-images.json`. The pages read those files. Don't edit them by hand.

To pull fresh data locally (then `git diff` to see what changed):

```sh
./dev.sh sync
```

## Deploying

Push to `main`. GitHub Pages redeploys on its own, usually within a minute or two. The sync Action also commits to `main`, so `git pull --rebase` before you push.
