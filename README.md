# Tri & Half Rotation

A 16-week rotating training plan for Olympic-distance triathlon and half-marathon training, built around a fixed Tuesday bike commute (33km each way) and lunchtime-only weekday runs. Generated as three single-file web apps so it's usable straight from a phone browser.

## What's here

- **`gen_plan.py`** — the source of truth. Defines all 16 weeks (4 phases of 4 weeks: Foundation, Build, Specific/Peak, Recovery + Half-Marathon Focus) as structured data and writes `plan_data.json`.
- **`gen_html.py`** — reads `plan_data.json` and generates `dist/index.html`, the Claude-hosted app. Syncs checkbox/effort-rating state across devices via a `db` capability that only exists inside Claude.
- **`gen_html_standalone.py`** — the same app, but fully self-contained: state is saved to `localStorage`, so it works fully offline with no account and no dependency on anything external, from a single file. Never syncs between devices.
- **`gen_html_supabase.py`** — the same app again, syncing through your own [Supabase](https://supabase.com) project instead: a simple email/password sign-in, real-time sync across every device, no Claude dependency. This is what `docs/index.html` (GitHub Pages) runs.
- **`plan_data.json`** — generated. Don't edit by hand; edit `gen_plan.py` and rerun the build.
- **`dist/`** — generated build output (all three apps). Also don't edit by hand.
- **`docs/index.html`** — generated. A copy of the Supabase-synced build, at the path GitHub Pages serves by default. Also don't edit by hand.
- **`build.sh`** — regenerates everything from source.

## Building

```
./build.sh
```

Requires Python 3 (standard library only, no dependencies). Regenerates `plan_data.json`, all three apps in `dist/`, and the `docs/index.html` copy GitHub Pages serves.

## Using the apps

- **`dist/tri-half-synced.html`** (= `docs/index.html`) — syncs across devices via your own Supabase project. No Claude dependency. This is the one to actually use day-to-day; see "Supabase setup" below.
- **`dist/tri-half-rotation-plan.html`** — a no-account, fully offline fallback. Open directly in any browser. Progress is stored per-device only (checking things off on your phone won't show up on desktop) — keep this around for when you genuinely have no connectivity, not as your daily driver.
- **`dist/index.html`** — meant to be hosted as a Claude Artifact (not on GitHub Pages — it depends on a Claude-only `db` capability to sync) so progress syncs across every device you open it from, if you'd rather stay inside Claude for this.

## Supabase setup

The synced build needs one table in your Supabase project, with row-level security so you can only ever read/write your own data:

```sql
create table training_state (
  user_id uuid primary key references auth.users(id) on delete cascade,
  data jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table training_state enable row level security;

create policy "Users can manage their own data"
  on training_state
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

Run that once in the Supabase SQL Editor. Also worth turning off "Confirm email" under Authentication → Settings, so signing in on a new device doesn't require clicking a confirmation link each time — there's only one real user of this app, so that check is pure friction.

The project URL and anon public key are baked into `gen_html_supabase.py` as constants (`SUPABASE_URL`, `SUPABASE_ANON_KEY`). The anon key is meant to be public — Supabase designs it to be safe in client-side code, since the row-level security policy above is what actually restricts access, not secrecy of the key. If you ever rotate the project or start a new one, update those two constants and rerun `build.sh`.

The first time you open the synced app on a new device, use "Create an account" with an email + password (any email works, it doesn't need to be verified once email confirmation is off) — after that it stays signed in on that device/browser until you explicitly sign out.

There's a "Forgot password?" link on the sign-in screen: it emails a reset link (Supabase's default template, no extra setup needed for the email itself), and opening that link drops you into a "set a new password" screen right there in the app. One thing this **does** need: once you know the app's real URL (your GitHub Pages URL, once that's live), add it in Supabase under **Authentication → URL Configuration → Redirect URLs**. Without that, Supabase will send the reset email but reject the link when clicked, since it only allows redirecting back to URLs you've explicitly approved. If you ever open the app from a different URL (a different Pages URL, a custom domain, testing the file locally), add that one too.

## Turning on GitHub Pages

After pushing this repo to GitHub:

1. On GitHub, go to the repo's **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Branch: `main`, folder: **`/docs`**. Save.
4. GitHub gives you a URL (usually `https://<username>.github.io/<repo-name>/`) within a minute or two. Open that on your phone and use "Add to Home Screen" for an app-like icon.

This serves the Supabase-synced build (`docs/index.html`), so it works with no Claude dependency and syncs across every device you sign in on. Whenever you push a change that reruns `build.sh` first, Pages picks up the new `docs/index.html` automatically.

## Design constraints this plan is built around

- Weekday runs are lunchtime-only, capped at one 30-minute and one 45-minute session.
- Tuesday is a fixed 66km round-trip bike commute (33km each way) — steady on the way out, progressive RPE-based intervals on the way home (no power meter).
- No lunchtime pool access, so swimming is evening-only (Thursday and Sunday).
- Saturday is parkrun + an extra distance add-on — the main lever for long-run volume.
- S&C sits on Saturday evening, well after parkrun, rather than stacked onto Tuesday's commute — Tuesday, Thursday and Saturday are the week's three harder days, and each has a full rest or easy day on both sides of it (Mon rest → Tue hard bike → Wed easy run → Thu hard run + eve swim → Fri rest → Sat parkrun + eve S&C → Sun easy bike + eve swim).
- Every session with real internal structure (warm-up/main set/cool-down, commute legs, race legs) renders as a small table (set / work / effort / recovery) rather than prose.

## Feedback and rotation

The app includes a per-session effort (RPE 1-10) rating, a block-review summary at the end of each 16-week cycle, and event/calendar back-planning: enter an upcoming race date and the app back-fills the calendar and tells you when to restart the rotation so the block lands correctly.
