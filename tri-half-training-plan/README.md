# Tri & Half Rotation

A 16-week rotating training plan for Olympic-distance triathlon and half-marathon training, built around a fixed Tuesday bike commute (33km each way) and lunchtime-only weekday runs. Generated as two single-file web apps so it's usable straight from a phone browser.

## What's here

- **`gen_plan.py`** — the source of truth. Defines all 16 weeks (4 phases of 4 weeks: Foundation, Build, Specific/Peak, Recovery + Half-Marathon Focus) as structured data and writes `plan_data.json`.
- **`gen_html.py`** — reads `plan_data.json` and generates `dist/index.html`, the hosted app. Syncs checkbox/effort-rating state across devices via a `db` capability.
- **`gen_html_standalone.py`** — the same app, but self-contained: state is saved to `localStorage` instead, so it works fully offline with no account, from a single file.
- **`plan_data.json`** — generated. Don't edit by hand; edit `gen_plan.py` and rerun the build.
- **`dist/`** — generated build output (both HTML apps). Also don't edit by hand.
- **`docs/index.html`** — generated. A copy of the standalone app, at the path GitHub Pages serves by default. Also don't edit by hand.
- **`build.sh`** — regenerates everything from source.

## Building

```
./build.sh
```

Requires Python 3 (standard library only, no dependencies). Regenerates `plan_data.json`, both apps in `dist/`, and the `docs/index.html` copy GitHub Pages serves.

## Using the apps

- **`dist/tri-half-rotation-plan.html`** — open directly in any browser, or add it to your phone's home screen for app-like access. Fully offline, no login. Progress is stored per-device (checking things off on your phone won't show up on desktop).
- **`dist/index.html`** — meant to be hosted as a Claude Artifact (not on GitHub Pages — it depends on a Claude-only `db` capability to sync) so progress syncs across every device you open it from.

## Turning on GitHub Pages

After pushing this repo to GitHub:

1. On GitHub, go to the repo's **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Branch: `main`, folder: **`/docs`**. Save.
4. GitHub gives you a URL (usually `https://<username>.github.io/<repo-name>/`) within a minute or two. Open that on your phone and use "Add to Home Screen" for an app-like icon.

This serves the standalone build (`docs/index.html`), so it works with no login and no dependency on Claude — but progress only saves on the device/browser you're using, it won't sync between your phone and desktop. Whenever you push a change that reruns `build.sh` first, Pages picks up the new `docs/index.html` automatically.

## Design constraints this plan is built around

- Weekday runs are lunchtime-only, capped at one 30-minute and one 45-minute session.
- Tuesday is a fixed 66km round-trip bike commute (33km each way) — steady on the way out, progressive RPE-based intervals on the way home (no power meter).
- No lunchtime pool access, so swimming is evening-only (Thursday and Sunday).
- Saturday is parkrun + an extra distance add-on — the main lever for long-run volume.
- S&C sits on Saturday evening, well after parkrun, rather than stacked onto Tuesday's commute — Tuesday, Thursday and Saturday are the week's three harder days, and each has a full rest or easy day on both sides of it (Mon rest → Tue hard bike → Wed easy run → Thu hard run + eve swim → Fri rest → Sat parkrun + eve S&C → Sun easy bike + eve swim).
- Every session with real internal structure (warm-up/main set/cool-down, commute legs, race legs) renders as a small table (set / work / effort / recovery) rather than prose.

## Feedback and rotation

The app includes a per-session effort (RPE 1-10) rating, a block-review summary at the end of each 16-week cycle, and event/calendar back-planning: enter an upcoming race date and the app back-fills the calendar and tells you when to restart the rotation so the block lands correctly.
