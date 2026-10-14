# bedtime-stories
Daily bedtime stories with moral lessons for 4-year-olds, generated and delivered at 8 PM Belgium time

## How it works
A GitHub Actions workflow (`.github/workflows/daily-story.yml`) runs `scripts/generate_story.py`, a deterministic generator (no AI API, no secrets, no paid services). It writes a short, gentle story (120–220 words) for age 4, with a title and a final `Moral: ...` line, and commits it only if the file is new or changed.

## Run it manually today
Repo → **Actions** → **Daily bedtime story** → **Run workflow**. A manual run always generates today's story (Europe/Brussels date).
Locally: `python3 scripts/generate_story.py` (optionally pass a date, e.g. `2026-10-14`).

## Daily schedule and DST
The story is generated every day at **8:00 PM Europe/Brussels**. GitHub cron uses UTC only, so the workflow triggers at both 18:00 UTC (summer, CEST) and 19:00 UTC (winter, CET); a check step lets only the run that falls at 20:xx Brussels time proceed. This handles daylight saving automatically. Note GitHub may delay scheduled runs by several minutes.

## Where stories appear
`stories/YYYY-MM-DD.md` (Brussels local date).

## Customize
Edit the top of `scripts/generate_story.py`:
- `THEMES`: add or edit themes and morals (rotated by date).
- `SETTINGS`: add characters and places.
- `MIN_WORDS` / `MAX_WORDS`: allowed length; the script fails if a story falls outside it. Adjust the paragraph text in `build_story` to change length.
