# Monthly plan import format (`plan_YYYY-MM.json`)

Imported on the app's **Schedule** tab (Import plan). Saved inside the existing Supabase `training_state` JSONB blob as `settings.datedPlan`; no table changes. Sample: `examples/plan_sample.json`.

## File

```json
{
  "schema": 1,
  "plan_id": "2026-10-15_to_2026-11-30",
  "title": "Oct 15 – Nov 30",
  "generated": "2026-10-15",
  "range": { "from": "2026-10-15", "to": "2026-11-30" },
  "sessions": [ ... ]
}
```

| Field | Required | Notes |
|---|---|---|
| `schema` | yes | Must be `1` |
| `plan_id`, `title`, `generated` | no | Labels only (shown in the import log) |
| `range` | no | `from`/`to` (YYYY-MM-DD). Defaults to the first/last session date. Every session must fall inside it |
| `sessions` | yes | Non-empty list |

## Session

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Unique, stable across re-exports. Convention: `YYYY-MM-DD_<discipline>_<slug>`, e.g. `2026-11-03_run_easy-strides`. Ticks and effort ratings are keyed on this |
| `date` | yes | Real calendar date, `YYYY-MM-DD` |
| `discipline` | yes | `run`, `bike`, `swim`, `sc`, `brick` or `rest` |
| `title` | yes | Short name |
| `slot` | no | Label shown on the card and used for ordering: `Morning`/`AM`, `Day`, `Lunch`, `PM`/`Afternoon`, `Evening` |
| `order` | no | Number; overrides slot ordering within a day |
| `detail` | no | One or two sentences |
| `duration` | no | Display text, e.g. `45 min` |
| `table` | no | Rows of `{ "set", "work", "effort", "recovery" }` (all text; missing = `–`). Same shape the 16-week plan uses |
| `optional` | no | `true` = not counted in weekly progress |
| `tag` | no | `"race"` highlights the title |

All text is shown as plain text (no markup).

## Import rules

- Merge by `id`: new ids are added, changed ones updated, identical ones untouched.
- Existing sessions dated inside the file's range but missing from the file are **removed**. Sessions outside the range are never touched.
- Ticks and ratings follow the `id`, so changing a session's date, title or table keeps them. Removing a session discards its tick/rating (the preview warns first).
- Any validation error rejects the whole file; nothing is saved.
- Re-importing an identical file reports "Nothing to change".

## Rules for the PT session when exporting

- Keep `id`s identical when a session carries over between regenerated versions of the same month.
- Monthly files should cover their own date range; the first file runs 15 Oct to 30 Nov 2026, later ones start on the 1st.
- One session per training activity; use `slot` for AM/PM splits (e.g. a commute is two sessions).
