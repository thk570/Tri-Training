import json

WEEKS = json.load(open("plan_data.json"))

NUTRITION = [
    {"name": "Rice Energy Bars", "recipe": "2 cups cooked white rice (~400g), 3 tbsp honey (~60g), 1/4 tsp salt, optional banana", "use": "During rides, pre-run", "pros": "Highly digestible, compact", "cons": "Prep needed", "carbs": "~22g per bar (makes 4)"},
    {"name": "Banana Oat Balls", "recipe": "2 bananas (~240g), 1 cup oats (~80g), 1 tbsp honey, salt", "use": "Pre-training", "pros": "Balanced energy", "cons": "Can bloat", "carbs": "~25g per ball (makes ~4)"},
    {"name": "Salted Potatoes", "recipe": "300g potatoes, 1/2 tsp salt", "use": "Long rides", "pros": "Sustained carbs", "cons": "Bulky", "carbs": "~50g per portion"},
    {"name": "Jam Sandwich", "recipe": "2 slices white bread (~70g), 2 tbsp jam (~40g)", "use": "Bike fuel", "pros": "Cheap", "cons": "Low nutrients", "carbs": "~45g per sandwich"},
    {"name": "Quick Honey Gel", "recipe": "1 tbsp honey, salt, water", "use": "Quick energy", "pros": "Fast", "cons": "Short lasting", "carbs": "~17g per serving"},
    {"name": "Rice Water Drink", "recipe": "500ml rice water, 1 tbsp honey", "use": "Sensitive gut", "pros": "Very gentle", "cons": "Low density", "carbs": "~15-20g per bottle"},
    {"name": "Mixed Carb Drink", "recipe": "500ml water, 1 tbsp sugar, 1 tbsp honey, salt", "use": "Hard sessions", "pros": "High delivery", "cons": "GI risk", "carbs": "~30-32g per bottle"},
    {"name": "Honey Drink", "recipe": "500ml water, 1 tbsp honey, salt, lemon", "use": "General", "pros": "Fast absorption", "cons": "Lower carbs", "carbs": "~17g per bottle"},
    {"name": "Isotonic Mix", "recipe": "500ml water, 25g sugar/honey, salt", "use": "Long sessions", "pros": "Balanced fuel", "cons": "Needs correct mix", "carbs": "~25g per bottle"},
    {"name": "Diluted Juice", "recipe": "200ml juice, 300ml water, salt", "use": "Mid sessions", "pros": "Good absorption", "cons": "Acidic", "carbs": "~18-22g per bottle"},
]

DAY_ORDER = ["Mon", "Tue_am", "Tue_pm", "Tue_eve", "Wed", "Thu_lunch", "Thu_eve", "Fri", "Sat", "Sat_eve", "Sun", "Sun_eve"]
DAY_LABELS = {
    "Mon": ("Mon", "Lunch"), "Tue_am": ("Tue", "AM"), "Tue_pm": ("Tue", "PM"), "Tue_eve": ("Tue", "Evening"),
    "Wed": ("Wed", "Lunch"), "Thu_lunch": ("Thu", "Lunch"), "Thu_eve": ("Thu", "Evening"),
    "Fri": ("Fri", "Lunch"), "Sat": ("Sat", "Morning"), "Sat_eve": ("Sat", "Evening"),
    "Sun": ("Sun", "Day"), "Sun_eve": ("Sun", "Evening"),
}

PHASE_NAMES = {1: "Foundation", 2: "Build", 3: "Specific / Peak", 4: "Half-Marathon Focus"}
PHASE_WEEKS = {1: (1,4), 2: (5,8), 3: (9,12), 4: (13,16)}

payload = {
    "weeks": WEEKS,
    "dayOrder": DAY_ORDER,
    "dayLabels": DAY_LABELS,
    "phaseNames": PHASE_NAMES,
    "phaseWeeks": PHASE_WEEKS,
    "nutrition": NUTRITION,
}

DATA_JSON = json.dumps(payload)

# Supabase project this build syncs through. The anon key is meant to be
# public — it's safe to ship in client-side code — access is controlled by
# the row-level security policy on the training_state table, not by keeping
# this key secret. Never put the service_role key here.
SUPABASE_URL = "https://wdbmghwhgpgsvqgryywn.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkYm1naHdoZ3Bnc3ZxZ3J5eXduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk1NTg2MDEsImV4cCI6MjEwNTEzNDYwMX0.VSRz8mKzRbsEuttSwF5br_oq5kl2hHiYL2qg7ZoZ8oE"

html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tri &amp; Half Rotation</title>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#EEF1EC; --surface:#FFFFFF; --surface-2:#E3E8E0; --raised:#FFFFFF;
  --ink:#1C2420; --ink-dim:#5B655D; --ink-faint:#8A9189;
  --line:#D2D9CE; --line-strong:#B7C0B1;
  --accent:#0E7C86; --accent-ink:#FFFFFF; --accent-soft:#DCEEEF;
  --run:#C24E23; --run-soft:#F6E2D8;
  --bike:#B07A0C; --bike-soft:#F3E6C9;
  --swim:#0E7C86; --swim-soft:#D9EDEE;
  --sc:#6B4E9E; --sc-soft:#E7E0F4;
  --rest:#8A9189; --rest-soft:#E7EAE4;
  --race:#B0281F; --race-soft:#F6DAD6;
  --shadow: 0 1px 2px rgba(28,36,32,.06), 0 8px 24px -12px rgba(28,36,32,.18);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#131917; --surface:#1B2320; --surface-2:#222B27; --raised:#1F2926;
    --ink:#ECEFEA; --ink-dim:#9FAB9F; --ink-faint:#6E7A70;
    --line:#2B3531; --line-strong:#3A4640;
    --accent:#49CBD6; --accent-ink:#0B1614; --accent-soft:#1B3A3C;
    --run:#EC8759; --run-soft:#3A2A20;
    --bike:#E4B94E; --bike-soft:#3A3018;
    --swim:#49CBD6; --swim-soft:#173537;
    --sc:#B39AF0; --sc-soft:#2E2647;
    --rest:#8A9891; --rest-soft:#232B27;
    --race:#F0776A; --race-soft:#3C201C;
    --shadow: 0 1px 2px rgba(0,0,0,.3), 0 12px 28px -14px rgba(0,0,0,.55);
  }
}
:root[data-theme="dark"]{
  --bg:#131917; --surface:#1B2320; --surface-2:#222B27; --raised:#1F2926;
  --ink:#ECEFEA; --ink-dim:#9FAB9F; --ink-faint:#6E7A70;
  --line:#2B3531; --line-strong:#3A4640;
  --accent:#49CBD6; --accent-ink:#0B1614; --accent-soft:#1B3A3C;
  --run:#EC8759; --run-soft:#3A2A20;
  --bike:#E4B94E; --bike-soft:#3A3018;
  --swim:#49CBD6; --swim-soft:#173537;
  --sc:#B39AF0; --sc-soft:#2E2647;
  --rest:#8A9891; --rest-soft:#232B27;
  --race:#F0776A; --race-soft:#3C201C;
  --shadow: 0 1px 2px rgba(0,0,0,.3), 0 12px 28px -14px rgba(0,0,0,.55);
}
*{box-sizing:border-box;}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Source Sans 3",-apple-system,BlinkMacSystemFont,sans-serif;
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3,.display{ font-family:"Big Shoulders Display",system-ui,sans-serif; font-weight:800; letter-spacing:.01em; text-wrap:balance; }
.mono{ font-family:"IBM Plex Mono", ui-monospace, monospace; font-variant-numeric:tabular-nums; }
a{color:inherit;}
button{font:inherit;}

.wrap{ max-width:760px; margin:0 auto; padding:0 18px 64px; }

/* Top bar */
.topbar{
  position:sticky; top:0; z-index:20; background:var(--bg);
  border-bottom:1px solid var(--line);
  padding-top: max(14px, env(safe-area-inset-top));
}
.topbar-inner{ max-width:760px; margin:0 auto; padding:0 18px 12px; display:flex; align-items:baseline; justify-content:space-between; gap:10px; flex-wrap:wrap; }
.brand{ display:flex; flex-direction:column; gap:1px; }
.brand .kicker{ font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-faint); font-weight:600; }
.brand h1{ margin:0; font-size:26px; line-height:1; color:var(--ink); }
.tabs{ display:flex; gap:4px; background:var(--surface-2); padding:3px; border-radius:10px; flex-wrap:wrap; }
.tab-btn{ border:none; background:transparent; color:var(--ink-dim); padding:7px 12px; border-radius:8px; font-weight:600; font-size:13px; cursor:pointer; }
.tab-btn.active{ background:var(--surface); color:var(--ink); box-shadow:var(--shadow); }
.tab-btn:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }

/* Week rail */
.rail-section{ padding:14px 0 4px; }
.rail{ display:flex; gap:7px; overflow-x:auto; padding:2px 0 10px; scrollbar-width:thin; }
.rail::-webkit-scrollbar{ height:5px; }
.rail::-webkit-scrollbar-thumb{ background:var(--line-strong); border-radius:4px; }
.pill{
  flex:0 0 auto; width:46px; height:52px; border-radius:12px; border:1px solid var(--line);
  background:var(--surface); display:flex; flex-direction:column; align-items:center; justify-content:center;
  cursor:pointer; gap:2px; position:relative;
}
.pill .pn{ font-family:"Big Shoulders Display"; font-weight:800; font-size:19px; line-height:1; }
.pill .pl{ font-size:9px; text-transform:uppercase; letter-spacing:.06em; color:var(--ink-faint); font-weight:600; }
.pill.active{ background:var(--accent); border-color:var(--accent); }
.pill.active .pn, .pill.active .pl{ color:var(--accent-ink); }
.pill.race::after{ content:"🏁"; position:absolute; top:-7px; right:-4px; font-size:12px; }
.pill:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
.phase-strip{ display:flex; gap:6px; margin-top:2px; }
.phase-chip{ flex:1; text-align:center; font-size:10px; padding:5px 4px; border-radius:7px; font-weight:600; letter-spacing:.02em; color:var(--ink-faint); background:var(--surface-2); }
.phase-chip.on{ color:var(--accent-ink); }

/* Week header */
.week-head{ padding:18px 0 6px; }
.week-head .wk-phase{ font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--accent); font-weight:700; }
.week-head h2{ margin:2px 0 2px; font-size:30px; }
.week-head .wk-dates{ font-size:12.5px; color:var(--ink-faint); margin-bottom:8px; }
.week-head p{ margin:0 0 12px; color:var(--ink-dim); font-size:14.5px; line-height:1.5; max-width:60ch; }
.progress-row{ display:flex; align-items:center; gap:10px; margin-bottom:4px; }
.progress-track{ flex:1; height:7px; border-radius:5px; background:var(--surface-2); overflow:hidden; }
.progress-fill{ height:100%; background:var(--accent); border-radius:5px; transition:width .25s ease; }
.progress-label{ font-size:12px; color:var(--ink-dim); white-space:nowrap; }

/* Day cards */
.day-list{ display:flex; flex-direction:column; gap:10px; margin-top:14px; }
.day-card{
  display:flex; gap:12px; background:var(--surface); border:1px solid var(--line); border-radius:14px;
  padding:13px 14px; box-shadow:var(--shadow); position:relative; overflow:hidden;
}
.day-card::before{ content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--bar-color,var(--ink-faint)); }
.day-card.done{ opacity:.62; }
.day-card.optional{ border-style:dashed; box-shadow:none; }
.day-meta{ flex:0 0 54px; display:flex; flex-direction:column; align-items:flex-start; gap:2px; padding-left:6px; }
.day-meta .dname{ font-family:"Big Shoulders Display"; font-weight:700; font-size:16px; line-height:1.1; }
.day-meta .dwhen{ font-size:10px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.05em; }
.day-body{ flex:1; min-width:0; padding-left:6px; }
.day-toprow{ display:flex; align-items:flex-start; justify-content:space-between; gap:10px; }
.badge{ display:inline-flex; align-items:center; gap:5px; font-size:10.5px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; padding:3px 8px; border-radius:99px; color:var(--badge-fg); background:var(--badge-bg); margin-bottom:5px; }
.day-title{ margin:0 0 3px; font-size:16.5px; font-weight:700; line-height:1.25; }
.day-title.race{ color:var(--race); }
.day-detail{ margin:0; font-size:13.5px; color:var(--ink-dim); line-height:1.45; }
.day-dur{ font-size:12px; color:var(--ink-faint); flex:0 0 auto; padding-top:1px; }

/* Session structure table */
.session-table{ width:100%; margin-top:8px; border-collapse:collapse; font-size:11.5px; }
.session-table th{ text-align:left; font-size:9.5px; text-transform:uppercase; letter-spacing:.05em; color:var(--ink-faint); font-weight:700; padding:0 8px 4px 0; border-bottom:1px solid var(--line); }
.session-table td{ padding:4px 8px 4px 0; color:var(--ink-dim); border-bottom:1px solid var(--line); white-space:normal; }
.session-table tr:last-child td{ border-bottom:none; }
.session-table td:first-child, .session-table th:first-child{ color:var(--ink); font-weight:600; white-space:nowrap; padding-right:6px; }
.session-table td:nth-child(2){ color:var(--ink); font-weight:600; white-space:nowrap; }
.check{
  appearance:none; -webkit-appearance:none; width:24px; height:24px; border-radius:7px; border:2px solid var(--line-strong);
  background:var(--surface); cursor:pointer; flex:0 0 auto; display:grid; place-items:center; margin-top:1px;
}
.check:checked{ background:var(--accent); border-color:var(--accent); }
.check:checked::after{ content:"✓"; color:var(--accent-ink); font-size:14px; font-weight:800; }
.check:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
.opt-tag{ font-size:10.5px; color:var(--ink-faint); font-style:italic; }

/* Effort (RPE) picker */
.rpe-row{ display:flex; align-items:center; gap:7px; margin-top:10px; flex-wrap:wrap; }
.rpe-label{ font-size:10px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.06em; font-weight:700; flex:0 0 auto; }
.rpe-pills{ display:flex; gap:3px; flex-wrap:wrap; }
.rpe-pill{
  width:21px; height:21px; border-radius:5px; border:1px solid var(--line-strong); background:var(--bg);
  font-size:10px; font-weight:700; color:var(--ink-faint); cursor:pointer; display:grid; place-items:center;
  font-family:"IBM Plex Mono", monospace; padding:0;
}
.rpe-pill.active{ background:var(--accent); border-color:var(--accent); color:var(--accent-ink); }
.rpe-pill:focus-visible{ outline:2px solid var(--accent); outline-offset:1px; }

/* legend */
.legend{ display:flex; flex-wrap:wrap; gap:10px 16px; margin:18px 0 4px; font-size:12px; color:var(--ink-dim); }
.legend span{ display:inline-flex; align-items:center; gap:5px; }
.legend i{ width:9px; height:9px; border-radius:3px; background:var(--dot); display:inline-block; }

/* collapsibles */
details.panel{ margin-top:22px; border:1px solid var(--line); border-radius:14px; background:var(--surface); overflow:hidden; }
details.panel summary{ cursor:pointer; padding:14px 16px; font-weight:700; font-size:15px; list-style:none; display:flex; align-items:center; justify-content:space-between; }
details.panel summary::-webkit-details-marker{ display:none; }
details.panel summary::after{ content:"+"; font-size:20px; color:var(--ink-faint); font-weight:400; }
details.panel[open] summary::after{ content:"–"; }
.panel-body{ padding:0 16px 16px; color:var(--ink-dim); font-size:14px; line-height:1.6; }
.panel-body h4{ margin:14px 0 4px; color:var(--ink); font-size:13.5px; }
.panel-body p{ margin:0 0 8px; }
.phase-overview{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:6px; }
@media (max-width:480px){ .phase-overview{ grid-template-columns:1fr; } }
.phase-card{ border:1px solid var(--line); border-radius:10px; padding:10px 12px; background:var(--surface-2); }
.phase-card .pf-name{ font-weight:700; color:var(--ink); font-size:13.5px; }
.phase-card .pf-weeks{ font-size:11px; color:var(--ink-faint); margin-bottom:4px; }

/* nutrition tab */
.nut-list{ display:flex; flex-direction:column; gap:10px; margin-top:16px; }
.nut-card{ border:1px solid var(--line); border-radius:12px; background:var(--surface); padding:12px 14px; box-shadow:var(--shadow); }
.nut-card h3{ margin:0 0 4px; font-size:16px; }
.nut-card .nut-recipe{ font-size:13px; color:var(--ink-dim); margin:0 0 8px; line-height:1.5; }
.nut-row{ display:flex; flex-wrap:wrap; gap:6px 14px; font-size:12px; }
.nut-row span b{ color:var(--ink-dim); font-weight:600; }
.nut-carbs{ font-size:12px; }
.intro-note{ margin:16px 0 0; padding:12px 14px; border:1px solid var(--line); border-radius:12px; background:var(--surface-2); font-size:13px; color:var(--ink-dim); line-height:1.55; }

/* coach tab */
.coach-card{ border:1px solid var(--line); border-radius:14px; background:var(--surface); padding:16px; box-shadow:var(--shadow); margin-top:16px; }
.coach-card h3{ margin:0 0 4px; font-size:19px; }
.coach-card .sub{ font-size:13px; color:var(--ink-dim); margin:0 0 14px; line-height:1.5; }
.toggle-row{ display:flex; align-items:center; justify-content:space-between; gap:10px; padding:2px 0 12px; }
.toggle-row .tlabel{ font-size:14px; font-weight:600; }
.switch{ position:relative; width:42px; height:24px; flex:0 0 auto; display:inline-block; }
.switch input{ opacity:0; width:100%; height:100%; margin:0; position:absolute; inset:0; cursor:pointer; z-index:1; }
.switch .track{ position:absolute; inset:0; background:var(--surface-2); border-radius:99px; border:1px solid var(--line-strong); transition:background .15s, border-color .15s; }
.switch .thumb{ position:absolute; top:1px; left:1px; width:18px; height:18px; border-radius:50%; background:var(--ink-faint); transition:transform .15s, background .15s; }
.switch input:checked ~ .track{ background:var(--accent); border-color:var(--accent); }
.switch input:checked ~ .track .thumb{ transform:translateX(18px); background:var(--accent-ink); }
.field-row{ display:flex; flex-direction:column; gap:6px; margin-bottom:12px; }
.field-row:last-child{ margin-bottom:0; }
.field-row label{ font-size:12px; font-weight:600; color:var(--ink-dim); }
.field-row input[type=date], .field-row select{
  font:inherit; padding:9px 10px; border-radius:9px; border:1px solid var(--line-strong); background:var(--bg); color:var(--ink); font-size:14px;
}
.event-banner{ padding:12px 14px; border-radius:12px; background:var(--accent-soft); color:var(--ink); font-size:13.5px; line-height:1.5; border:1px solid var(--accent); margin-top:16px; }
.review-stats{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:4px 0 18px; }
@media (max-width:480px){ .review-stats{ grid-template-columns:1fr; } }
.stat-tile{ border:1px solid var(--line); border-radius:10px; padding:10px 12px; background:var(--surface-2); }
.stat-tile .stat-num{ font-family:"Big Shoulders Display"; font-weight:800; font-size:28px; line-height:1; }
.stat-tile .stat-label{ font-size:11px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:.04em; margin-top:3px; }
.phase-bars{ display:flex; flex-direction:column; gap:9px; margin:0 0 16px; }
.phase-bar-row{ display:flex; align-items:center; gap:10px; font-size:12.5px; }
.phase-bar-row .pbr-name{ flex:0 0 100px; color:var(--ink-dim); font-weight:600; }
.phase-bar-track{ flex:1; height:8px; border-radius:5px; background:var(--surface-2); overflow:hidden; display:block; }
.phase-bar-fill{ height:100%; background:var(--accent); border-radius:5px; display:block; }
.phase-bar-rpe{ flex:0 0 46px; text-align:right; color:var(--ink-faint); }
.recommend-box{ padding:14px; border-radius:12px; background:var(--surface-2); border-left:4px solid var(--accent); font-size:13.5px; line-height:1.6; color:var(--ink); }
.recommend-box b{ color:var(--ink); }

footer{ margin-top:30px; padding-top:14px; border-top:1px solid var(--line); font-size:11.5px; color:var(--ink-faint); }
.footer-signout{ background:none; border:none; color:var(--ink-faint); text-decoration:underline; cursor:pointer; font-size:11.5px; padding:0; font-family:inherit; }

/* Auth gate */
#authGate{
  position:fixed; inset:0; z-index:100; background:var(--bg);
  align-items:center; justify-content:center; padding:24px;
}
/* #authGate's own display:flex would otherwise outrank the browser's
   default [hidden]{display:none} rule (an ID selector beats an attribute
   selector), so setting authGateEl.hidden = true in JS would silently do
   nothing and the overlay would stay on screen forever. Scoping display:flex
   to the *not*-hidden state avoids that fight entirely. */
#authGate:not([hidden]){ display:flex; }
.auth-card{
  width:100%; max-width:360px; background:var(--surface); border:1px solid var(--line);
  border-radius:16px; padding:28px 24px; box-shadow:var(--shadow);
}
.auth-card h1{ font-family:"Big Shoulders Display"; font-size:26px; margin:0 0 4px; }
.auth-card p.sub{ margin:0 0 20px; color:var(--ink-dim); font-size:13px; line-height:1.5; }
.auth-field{ margin-bottom:12px; }
.auth-field label{ display:block; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--ink-faint); font-weight:700; margin-bottom:5px; }
.auth-field input{
  width:100%; box-sizing:border-box; padding:10px 12px; border-radius:9px; border:1px solid var(--line-strong);
  background:var(--bg); color:var(--ink); font-size:14.5px; font-family:inherit;
}
.auth-field input:focus{ outline:2px solid var(--accent); outline-offset:1px; }
.link-btn{
  background:none; border:none; padding:0; margin:-6px 0 4px; color:var(--accent); font-size:12.5px;
  text-decoration:underline; cursor:pointer; font-family:inherit; display:block;
}
.auth-actions{ display:flex; flex-direction:column; gap:8px; margin-top:18px; }
.auth-btn{
  padding:11px; border-radius:9px; border:none; font-size:14px; font-weight:700; cursor:pointer; font-family:inherit;
}
.auth-btn.primary{ background:var(--accent); color:var(--accent-ink); }
.auth-btn.secondary{ background:transparent; color:var(--ink-dim); border:1px solid var(--line-strong); }
.auth-msg{ margin:12px 0 0; font-size:12.5px; line-height:1.5; min-height:1em; }
.auth-msg.error{ color:var(--race); }
.auth-msg.info{ color:var(--ink-dim); }
</style>

</head>
<body>

<div id="authGate">
  <div class="auth-card">
    <h1>Tri &amp; Half Plan</h1>
    <p class="sub" id="authSub">Sign in to sync your training log across devices.</p>
    <form id="authForm">
      <div class="auth-field" id="authEmailField">
        <label for="authEmail">Email</label>
        <input id="authEmail" type="email" autocomplete="email" required>
      </div>
      <div class="auth-field" id="authPasswordField">
        <label for="authPassword" id="authPasswordLabel">Password</label>
        <input id="authPassword" type="password" autocomplete="current-password" required minlength="6">
      </div>
      <button type="button" class="link-btn" id="forgotBtn">Forgot password?</button>
      <div class="auth-actions">
        <button type="submit" class="auth-btn primary" id="authSubmitBtn">Sign in</button>
        <button type="button" class="auth-btn secondary" id="authToggleBtn">First time here? Create an account</button>
        <button type="button" class="auth-btn secondary" id="authBackBtn" hidden>Back to sign in</button>
      </div>
      <p class="auth-msg" id="authMsg"></p>
    </form>
  </div>
</div>

<div class="topbar">
  <div class="topbar-inner">
    <div class="brand">
      <span class="kicker">16-week rotation</span>
      <h1>Tri &amp; Half Plan</h1>
    </div>
    <div class="tabs" role="tablist">
      <button class="tab-btn active" data-tab="plan" role="tab" aria-selected="true">Plan</button>
      <button class="tab-btn" data-tab="fuel" role="tab" aria-selected="false">Fuelling</button>
      <button class="tab-btn" data-tab="coach" role="tab" aria-selected="false">Coach</button>
    </div>
  </div>
</div>

<div class="wrap">

  <section id="tab-plan">
    <div class="rail-section">
      <div class="rail" id="rail"></div>
    </div>

    <div class="week-head">
      <div class="wk-phase" id="wkPhase"></div>
      <h2 id="wkLabel"></h2>
      <div class="wk-dates mono" id="wkDates"></div>
      <p id="wkNote"></p>
      <div class="progress-row">
        <div class="progress-track"><div class="progress-fill" id="wkFill"></div></div>
        <div class="progress-label mono" id="wkFillLabel">0/10</div>
      </div>
    </div>

    <div class="day-list" id="dayList"></div>

    <div class="legend" id="legend"></div>

    <details class="panel">
      <summary>The four phases</summary>
      <div class="panel-body">
        <p>Three build weeks, one deload, on repeat — the classic 3:1 loading pattern — with the whole plan aimed at an Olympic-distance triathlon at the end of Week 12 and a half marathon at the end of Week 16.</p>
        <div class="phase-overview" id="phaseOverview"></div>
      </div>
    </details>

    <details class="panel">
      <summary>How the constraints shape the week</summary>
      <div class="panel-body">
        <p>Every week follows the same skeleton, so the routine becomes automatic rather than something to plan each Sunday:</p>
        <p><b>Lunchtimes (Mon–Fri):</b> only two carry a session at all — Monday (45min, the week's main quality run) and Friday (30min, easy). Tue, Wed, Thu stay free, since swimming isn't an option at lunch.</p>
        <p><b>Swimming</b> now sits on Thursday evening and Sunday evening — two sessions a week, split by purpose rather than just repeated: Thursday carries technique and race-pace work (progressing with the phase you're in), Sunday evening is a longer continuous aerobic swim, building from the 1.5k you're already comfortable with toward open-water distance for the tri. Sunday's swim comes after that day's ride, so it's kept easy — the point is time in the water, not effort.</p>
        <p><b>Tuesday:</b> your 33km-each-way commute is fixed and is, on its own, the week's biggest single training stimulus — roughly 2.5 hours of riding across the day. This follows the habit you already had before this plan: steady out in the morning (nothing to protect, but no reason to arrive at work gassed either), then the structured interval work on the way home, where emptying the tank is followed only by recovery, not a workday. No power meter, so every interval is RPE/feel-based — described as effort-out-of-10 and how much you can talk through it, progressing from 4x4min to 3x10min-style sets across the block. S&amp;C follows in the evening once you're home — one fixed 20–25 minute slot, always the same night, rotating through four short circuits so it never gets stale. A fixed slot beats a floating one when a routine hasn't stuck before, and it's short enough to survive a big riding day.</p>
        <p><b>Saturday:</b> parkrun plus extra is the long-run engine — the "extra" after parkrun grows steadily from 15 minutes in Week 1 to a 45–50 minute half-marathon-pace finish by Week 15.</p>
        <p><b>Sunday:</b> the long ride, building toward the full Olympic bike distance by Week 10, then easing to maintenance once the run takes priority for the half marathon.</p>
      </div>
    </details>

    <details class="panel">
      <summary>What's next — extending the rotation</summary>
      <div class="panel-body">
        <p>This 16-week block is built as a repeatable rotation, not a one-off. After Week 16:</p>
        <h4>Loop it again</h4>
        <p>Start back at Week 1 for your next Olympic tri / half-marathon pair — Weeks 1–4 will feel easy given the fitness you're carrying, so feel free to compress the Foundation phase to 2–3 weeks on a repeat cycle. Check the Coach tab first — your effort ratings from this block shape exactly how to adjust the next one.</p>
        <h4>Step up to a 70.3</h4>
        <p>The base is already pointed that way, and your commute is doing more of the work than you might expect: two 33km legs every Tuesday is around 66km of riding before Sunday's ride even starts. For a 70.3-build repeat, use the occasional free Sunday you mentioned to push that ride out toward 2.5–3 hours (Week 10's ~40k Olympic-distance ride is the template — just keep extending it), and let the Sunday-evening swim keep growing past 2.2k toward continuous 3k+, since that's now your dedicated endurance swim slot. Keep the weekday structure identical; only the Saturday parkrun-extra and the occasional long Sunday ride and swim need to keep progressing past where this block caps them.</p>
        <h4>Step up to a marathon</h4>
        <p>Saturday's parkrun-plus-extra already reaches a 15–16k long run by Week 15. For a marathon repeat, let that keep climbing in 1–2k increments each build week toward 29–32k at peak, and add a second easy run in the free Thursday lunch slot — you're still holding to two <i>quality</i> lunchtime runs (Monday, Friday), this is a third easy one purely for volume. Give yourself a proper 3-week taper into race day rather than the 1-week taper used here for the half.</p>
        <h4>Keep it sustainable</h4>
        <p>The S&amp;C and Saturday-evening mobility slots are marked optional for a reason — missing one is not a failed week. The plan is designed to survive you skipping them without anything else needing to change.</p>
      </div>
    </details>

  </section>

  <section id="tab-fuel" hidden>
    <div class="intro-note">Simple, low-cost fuelling options built around real food — useful for anything from a long Sunday ride to race-day nutrition. Carb figures are approximate; test anything new in training, never on race day.</div>
    <div class="nut-list" id="nutList"></div>
  </section>

  <section id="tab-coach" hidden>
    <div id="eventBanner"></div>

    <div class="coach-card">
      <h3>Next event</h3>
      <p class="sub">Tell me if this block is building toward a real race and I'll back-fill calendar dates onto every week, and let you know when it's time to start the next rotation.</p>
      <div class="toggle-row">
        <span class="tlabel">I have a target event</span>
        <label class="switch">
          <input type="checkbox" id="eventToggle">
          <span class="track"><span class="thumb"></span></span>
        </label>
      </div>
      <div id="eventFields" hidden>
        <div class="field-row">
          <label for="eventDate">Event date</label>
          <input type="date" id="eventDate">
        </div>
        <div class="field-row">
          <label for="eventType">Which race is this?</label>
          <select id="eventType">
            <option value="hm">End of Week 16 — Half Marathon</option>
            <option value="oly">End of Week 12 — Olympic Triathlon</option>
            <option value="custom">Other date — align to Week 16</option>
          </select>
        </div>
      </div>
      <div class="field-row" id="manualStartRow">
        <label for="manualStart">No event? Set a plan start date instead (optional)</label>
        <input type="date" id="manualStart">
      </div>
    </div>

    <div class="coach-card">
      <h3>Block review</h3>
      <p class="sub">Rate each session's effort out of 10 as you go, on the Plan tab — this fills in from those ratings, and it's what shapes the recommendation for your next 16-week block.</p>
      <div class="review-stats" id="reviewStats"></div>
      <div class="phase-bars" id="phaseBars"></div>
      <div class="recommend-box" id="recommendBox"></div>
    </div>
  </section>

  <footer>Built for Theo · rotate continuously · tap a session to check it off — synced across your devices via Supabase. <button type="button" class="footer-signout" id="signOutBtn">Sign out</button></footer>
</div>

<script id="plan-data" type="application/json">__DATA_JSON__</script>
<script>
(function(){
  const DATA = JSON.parse(document.getElementById('plan-data').textContent);
  const { weeks, dayOrder, dayLabels, phaseNames, phaseWeeks, nutrition } = DATA;

  const DISC_LABEL = { run:"Run", bike:"Bike", swim:"Swim", sc:"S&C", rest:"Rest" };

  let currentWeek = 1;
  let checks = {}; // { "w{n}": { dayKey: {done, rpe} } }
  let settings = { eventEnabled:false, eventDate:null, eventType:'hm', manualStart:null };

  // ---------- Supabase: auth + sync ----------
  // Every checkbox tick and effort rating lives in one row per signed-in
  // user (table: training_state, one JSONB column holding {checks,
  // settings}). A realtime subscription pushes updates from other devices
  // in place of a page reload.
  const authGateEl = document.getElementById('authGate');
  const authFormEl = document.getElementById('authForm');
  const authEmailFieldEl = document.getElementById('authEmailField');
  const authEmailEl = document.getElementById('authEmail');
  const authPasswordFieldEl = document.getElementById('authPasswordField');
  const authPasswordEl = document.getElementById('authPassword');
  const authPasswordLabelEl = document.getElementById('authPasswordLabel');
  const authSubmitBtnEl = document.getElementById('authSubmitBtn');
  const authToggleBtnEl = document.getElementById('authToggleBtn');
  const authBackBtnEl = document.getElementById('authBackBtn');
  const forgotBtnEl = document.getElementById('forgotBtn');
  const authMsgEl = document.getElementById('authMsg');
  const authSubEl = document.getElementById('authSub');
  const signOutBtnEl = document.getElementById('signOutBtn');
  let authMode = 'signin'; // 'signin' | 'signup' | 'forgot' | 'reset'

  function setAuthMsg(text, kind){
    authMsgEl.textContent = text || '';
    authMsgEl.className = 'auth-msg' + (kind ? ' ' + kind : '');
  }

  const AUTH_COPY = {
    signin:  { submit: 'Sign in', sub: 'Sign in to sync your training log across devices.' },
    signup:  { submit: 'Create account', sub: 'One account, used on every device — phone and desktop stay in sync.' },
    forgot:  { submit: 'Send reset link', sub: "Enter your email and we'll send a link to reset your password." },
    reset:   { submit: 'Set new password', sub: 'Choose a new password for your account.' },
  };

  function applyAuthMode(){
    const copy = AUTH_COPY[authMode];
    authSubmitBtnEl.textContent = copy.submit;
    authSubEl.textContent = copy.sub;
    authEmailFieldEl.hidden = authMode === 'reset';
    authEmailEl.required = authMode !== 'reset';
    authPasswordFieldEl.hidden = authMode === 'forgot';
    authPasswordEl.required = authMode !== 'forgot';
    authPasswordEl.autocomplete = authMode === 'reset' ? 'new-password' : (authMode === 'signup' ? 'new-password' : 'current-password');
    authPasswordLabelEl.textContent = authMode === 'reset' ? 'New password' : 'Password';
    forgotBtnEl.hidden = authMode !== 'signin';
    authToggleBtnEl.hidden = authMode === 'forgot' || authMode === 'reset';
    authToggleBtnEl.textContent = authMode === 'signin' ? "First time here? Create an account" : 'Already have an account? Sign in';
    authBackBtnEl.hidden = authMode !== 'forgot';
    setAuthMsg('');
  }

  // The Supabase library loads from a CDN — if that failed (offline, an
  // ad/script blocker, the CDN having a bad moment), fail loudly with a
  // message the user can act on, rather than a silently broken page.
  let sb = null;
  let currentUser = null;
  let realtimeChannel = null;
  let saveTimer = null;
  try {
    sb = supabase.createClient('__SUPABASE_URL__', '__SUPABASE_ANON_KEY__');
  } catch (e) {
    setAuthMsg("Couldn't load the sync library — check your internet connection and reload the page.", 'error');
    authSubmitBtnEl.disabled = true;
    authToggleBtnEl.disabled = true;
    forgotBtnEl.disabled = true;
  }

  authToggleBtnEl.addEventListener('click', () => {
    authMode = authMode === 'signin' ? 'signup' : 'signin';
    applyAuthMode();
  });

  forgotBtnEl.addEventListener('click', () => {
    authMode = 'forgot';
    applyAuthMode();
  });

  authBackBtnEl.addEventListener('click', () => {
    authMode = 'signin';
    applyAuthMode();
  });

  authFormEl.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!sb) return;
    const email = authEmailEl.value.trim();
    const password = authPasswordEl.value;
    authSubmitBtnEl.disabled = true;
    setAuthMsg('Working on it…', 'info');
    try {
      if (authMode === 'signin') {
        const { data, error } = await sb.auth.signInWithPassword({ email, password });
        console.log('[auth] signInWithPassword result', { hasSession: !!data?.session, hasUser: !!data?.user, error });
        if (error) throw error;
        // onAuthStateChange picks up the new session and starts the app.
      } else if (authMode === 'signup') {
        const { data, error } = await sb.auth.signUp({ email, password });
        if (error) throw error;
        if (!data.session) {
          setAuthMsg('Account created — check your email to confirm, then sign in.', 'info');
          authSubmitBtnEl.disabled = false;
          return;
        }
        // onAuthStateChange picks up the new session and starts the app.
      } else if (authMode === 'forgot') {
        const { error } = await sb.auth.resetPasswordForEmail(email, {
          redirectTo: window.location.origin + window.location.pathname,
        });
        if (error) throw error;
        setAuthMsg('Check your email for a reset link.', 'info');
        authSubmitBtnEl.disabled = false;
        return;
      } else if (authMode === 'reset') {
        const { error } = await sb.auth.updateUser({ password });
        if (error) throw error;
        // The recovery session Supabase gave us is now a normal signed-in
        // session — go straight into the app rather than asking to sign in again.
        authMode = 'signin';
        applyAuthMode();
        setAuthMsg('Password updated.', 'info');
        const { data: { session } } = await sb.auth.getSession();
        if (session) await enterApp(session);
        return;
      }
    } catch (err) {
      setAuthMsg(err.message || 'Something went wrong — try again.', 'error');
      authSubmitBtnEl.disabled = false;
    }
  });

  signOutBtnEl.addEventListener('click', async () => {
    if (!sb) return;
    if (realtimeChannel) { sb.removeChannel(realtimeChannel); realtimeChannel = null; }
    await sb.auth.signOut();
  });

  async function loadRemoteState(userId){
    const { data, error } = await sb.from('training_state').select('data').eq('user_id', userId).maybeSingle();
    if (error) throw error;
    if (data && data.data) {
      checks = data.data.checks || {};
      settings = Object.assign(settings, data.data.settings || {});
    } else {
      // First sign-in on this account — seed the row so later writes have something to upsert onto.
      await sb.from('training_state').upsert({ user_id: userId, data: { checks, settings } });
    }
  }

  function subscribeRemoteState(userId){
    // Defensive: if a previous (e.g. racing) call already opened a channel,
    // tear it down before opening another — a channel can only be
    // subscribed to once, and re-using the same topic name throws.
    if (realtimeChannel) { sb.removeChannel(realtimeChannel); realtimeChannel = null; }
    realtimeChannel = sb.channel('training_state:' + userId)
      .on('postgres_changes', { event: '*', schema: 'public', table: 'training_state', filter: 'user_id=eq.' + userId },
        (payload) => {
          if (!payload.new || !payload.new.data) return;
          checks = payload.new.data.checks || {};
          settings = Object.assign(settings, payload.new.data.settings || {});
          renderWeek(); renderCoach(); buildRail();
        })
      .subscribe();
  }

  function saveRemoteState(){
    if (!currentUser) return;
    clearTimeout(saveTimer);
    // Small debounce: rapid taps (e.g. changing an RPE rating) collapse into one write.
    saveTimer = setTimeout(async () => {
      try {
        await sb.from('training_state').upsert({ user_id: currentUser.id, data: { checks, settings }, updated_at: new Date().toISOString() });
      } catch (e) { /* offline — the next successful save carries the latest state anyway */ }
    }, 400);
  }

  const railEl = document.getElementById('rail');
  const dayListEl = document.getElementById('dayList');
  const wkPhaseEl = document.getElementById('wkPhase');
  const wkLabelEl = document.getElementById('wkLabel');
  const wkDatesEl = document.getElementById('wkDates');
  const wkNoteEl = document.getElementById('wkNote');
  const wkFillEl = document.getElementById('wkFill');
  const wkFillLabelEl = document.getElementById('wkFillLabel');
  const legendEl = document.getElementById('legend');
  const phaseOverviewEl = document.getElementById('phaseOverview');
  const nutListEl = document.getElementById('nutList');
  const eventBannerEl = document.getElementById('eventBanner');
  const eventToggleEl = document.getElementById('eventToggle');
  const eventFieldsEl = document.getElementById('eventFields');
  const eventDateEl = document.getElementById('eventDate');
  const eventTypeEl = document.getElementById('eventType');
  const manualStartEl = document.getElementById('manualStart');
  const reviewStatsEl = document.getElementById('reviewStats');
  const phaseBarsEl = document.getElementById('phaseBars');
  const recommendBoxEl = document.getElementById('recommendBox');

  function weekByN(n){ return weeks.find(w => w.n === n); }

  function normalizeEntry(v){
    if (v && typeof v === 'object') return { done: !!v.done, rpe: (typeof v.rpe === 'number' ? v.rpe : null) };
    return { done: !!v, rpe: null };
  }

  function ensureWeekChecks(n){
    const key = 'w' + n;
    if (!checks[key]) checks[key] = {};
    return checks[key];
  }

  function getEntry(n, dayKey){
    const wc = checks['w' + n] || {};
    return normalizeEntry(wc[dayKey]);
  }

  // ---------- date / event helpers ----------
  function weeksToEventFor(type){ return type === 'oly' ? 12 : 16; }
  function parseDate(s){ if (!s) return null; const d = new Date(s + 'T00:00:00'); return isNaN(d.getTime()) ? null : d; }
  function addDays(d, n){ const r = new Date(d); r.setDate(r.getDate() + n); return r; }
  function fmtDate(d){ return d.toLocaleDateString(undefined, { day:'numeric', month:'short' }); }

  function computeStartDate(){
    if (settings.eventEnabled && settings.eventDate) {
      const evt = parseDate(settings.eventDate);
      if (evt) return addDays(evt, -(weeksToEventFor(settings.eventType) - 1) * 7);
    }
    if (settings.manualStart) {
      const d = parseDate(settings.manualStart);
      if (d) return d;
    }
    return null;
  }

  function weekDateRange(n){
    const start = computeStartDate();
    if (!start) return null;
    const ws = addDays(start, (n - 1) * 7);
    return { start: ws, end: addDays(ws, 6) };
  }

  function buildRail(){
    railEl.innerHTML = '';
    weeks.forEach(w => {
      const btn = document.createElement('button');
      btn.className = 'pill' + (w.n === currentWeek ? ' active' : '') + (w.label.indexOf('RACE') === 0 ? ' race' : '');
      btn.innerHTML = '<span class="pn">' + w.n + '</span><span class="pl">Wk</span>';
      const range = weekDateRange(w.n);
      btn.setAttribute('aria-label', 'Week ' + w.n + (range ? (', ' + fmtDate(range.start) + ' to ' + fmtDate(range.end)) : ''));
      if (range) btn.title = fmtDate(range.start) + ' – ' + fmtDate(range.end);
      btn.addEventListener('click', () => selectWeek(w.n));
      railEl.appendChild(btn);
    });
  }

  function buildLegend(){
    legendEl.innerHTML = '';
    Object.keys(DISC_LABEL).forEach(k => {
      const span = document.createElement('span');
      span.innerHTML = '<i style="--dot:var(--' + k + ')"></i>' + DISC_LABEL[k];
      legendEl.appendChild(span);
    });
  }

  function buildPhaseOverview(){
    phaseOverviewEl.innerHTML = '';
    Object.keys(phaseNames).forEach(p => {
      const rng = phaseWeeks[p];
      const card = document.createElement('div');
      card.className = 'phase-card';
      card.innerHTML = '<div class="pf-name">' + phaseNames[p] + '</div><div class="pf-weeks">Weeks ' + rng[0] + '–' + rng[1] + '</div>';
      phaseOverviewEl.appendChild(card);
    });
  }

  function buildSessionTable(rows){
    const table = document.createElement('table');
    table.className = 'session-table mono';
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Set</th><th>Work</th><th>Effort</th><th>Recovery</th></tr>';
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    rows.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + r.set + '</td><td>' + r.work + '</td><td>' + r.effort + '</td><td>' + r.recovery + '</td>';
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function renderWeek(){
    const w = weekByN(currentWeek);
    wkPhaseEl.textContent = phaseNames[w.phase] + ' · Phase ' + w.phase + ' of 4';
    wkLabelEl.textContent = w.label;
    const range = weekDateRange(currentWeek);
    wkDatesEl.textContent = range ? (fmtDate(range.start) + ' – ' + fmtDate(range.end)) : '';
    wkNoteEl.textContent = w.note || '';

    dayListEl.innerHTML = '';
    let doneCount = 0, total = 0;

    dayOrder.forEach(key => {
      const d = w.days[key];
      if (!d) return;
      const [dname, dwhen] = dayLabels[key];
      const isOptional = !!d.optional;
      const entry = getEntry(currentWeek, key);
      const isDone = entry.done;
      if (!isOptional) { total++; if (isDone) doneCount++; }

      const card = document.createElement('div');
      card.className = 'day-card' + (isDone ? ' done' : '') + (isOptional ? ' optional' : '');
      card.style.setProperty('--bar-color', 'var(--' + d.discipline + ')');

      const meta = document.createElement('div');
      meta.className = 'day-meta';
      meta.innerHTML = '<span class="dname">' + dname + '</span><span class="dwhen">' + dwhen + '</span>';

      const body = document.createElement('div');
      body.className = 'day-body';
      const top = document.createElement('div');
      top.className = 'day-toprow';
      const left = document.createElement('div');
      left.style.minWidth = '0';
      const badge = document.createElement('span');
      badge.className = 'badge';
      badge.style.setProperty('--badge-bg', 'var(--' + d.discipline + '-soft)');
      badge.style.setProperty('--badge-fg', 'var(--' + d.discipline + ')');
      badge.textContent = DISC_LABEL[d.discipline] + (isOptional ? ' · optional' : '');
      const title = document.createElement('p');
      title.className = 'day-title' + (d.tag === 'race' ? ' race' : '');
      title.textContent = d.title;
      const detail = document.createElement('p');
      detail.className = 'day-detail';
      detail.textContent = d.detail;
      left.appendChild(badge); left.appendChild(title); left.appendChild(detail);
      if (d.table && d.table.length) left.appendChild(buildSessionTable(d.table));

      const right = document.createElement('div');
      right.style.cssText = 'display:flex;flex-direction:column;align-items:flex-end;gap:8px;';
      const dur = document.createElement('div');
      dur.className = 'day-dur mono';
      dur.textContent = d.duration;
      const cb = document.createElement('input');
      cb.type = 'checkbox'; cb.className = 'check';
      cb.checked = isDone;
      cb.id = 'chk-' + currentWeek + '-' + key;
      cb.addEventListener('change', () => toggleDay(key, cb.checked));
      right.appendChild(dur); right.appendChild(cb);

      top.appendChild(left); top.appendChild(right);
      body.appendChild(top);

      if (d.discipline !== 'rest') {
        const rpeRow = document.createElement('div');
        rpeRow.className = 'rpe-row';
        const label = document.createElement('span');
        label.className = 'rpe-label';
        label.textContent = 'Effort';
        const pills = document.createElement('div');
        pills.className = 'rpe-pills';
        for (let i = 1; i <= 10; i++) {
          const b = document.createElement('button');
          b.type = 'button';
          b.className = 'rpe-pill' + (entry.rpe === i ? ' active' : '');
          b.textContent = String(i);
          b.setAttribute('aria-label', 'Effort ' + i + ' out of 10');
          b.addEventListener('click', () => setRpe(key, entry.rpe === i ? null : i));
          pills.appendChild(b);
        }
        rpeRow.appendChild(label);
        rpeRow.appendChild(pills);
        body.appendChild(rpeRow);
      }

      card.appendChild(meta); card.appendChild(body);
      dayListEl.appendChild(card);
    });

    wkFillEl.style.width = (total ? (doneCount/total*100) : 0) + '%';
    wkFillLabelEl.textContent = doneCount + '/' + total;

    [...railEl.children].forEach((el, i) => el.classList.toggle('active', weeks[i].n === currentWeek));
  }

  function selectWeek(n){
    currentWeek = n;
    renderWeek();
  }

  function persistWeek(n){
    saveRemoteState();
  }

  function toggleDay(dayKey, val){
    const wc = ensureWeekChecks(currentWeek);
    const entry = normalizeEntry(wc[dayKey]);
    entry.done = val;
    wc[dayKey] = entry;
    renderWeek();
    renderCoach();
    persistWeek(currentWeek);
  }

  function setRpe(dayKey, val){
    const wc = ensureWeekChecks(currentWeek);
    const entry = normalizeEntry(wc[dayKey]);
    entry.rpe = val;
    wc[dayKey] = entry;
    renderWeek();
    renderCoach();
    persistWeek(currentWeek);
  }

  // ---------- settings persistence ----------
  function persistSettings(){
    saveRemoteState();
  }

  // ---------- block review ----------
  function computeReview(){
    let total = 0, done = 0, rpeSum = 0, rpeCount = 0;
    const phases = {1:{total:0,done:0,rpeSum:0,rpeCount:0},2:{total:0,done:0,rpeSum:0,rpeCount:0},3:{total:0,done:0,rpeSum:0,rpeCount:0},4:{total:0,done:0,rpeSum:0,rpeCount:0}};
    weeks.forEach(w => {
      dayOrder.forEach(key => {
        const d = w.days[key];
        if (!d || d.optional || d.discipline === 'rest') return;
        const entry = getEntry(w.n, key);
        total++; phases[w.phase].total++;
        if (entry.done) { done++; phases[w.phase].done++; }
        if (typeof entry.rpe === 'number') {
          rpeSum += entry.rpe; rpeCount++;
          phases[w.phase].rpeSum += entry.rpe; phases[w.phase].rpeCount++;
        }
      });
    });
    return { completion: total ? done/total : 0, avgRpe: rpeCount ? rpeSum/rpeCount : null, rpeCount, phases };
  }

  function recommendationHTML(review){
    if (review.rpeCount < 6) {
      return `Not enough effort ratings yet — rate a handful of sessions on the Plan tab (tap a number 1–10 under any session) and a real recommendation will appear here, built from how this block actually felt.`;
    }
    const c = review.completion, r = review.avgRpe;
    if (c < 0.6) {
      return `<b>Adherence was the limiter, not fitness.</b> Only ${Math.round(c*100)}% of sessions were completed this block. Before changing intensity next time, simplify: lock in just the fixed anchors — the Tuesday commute, Thursday and Sunday swims, and Saturday parkrun — as the non-negotiable minimum, and treat everything else as a bonus.`;
    }
    if (r >= 8) {
      return `<b>This block ran hot</b> — average effort was ${r.toFixed(1)}/10. Next rotation: keep Foundation at the full 4 weeks rather than compressing it, and cap the top end a little short of where this block peaked (Saturday's long run and Sunday's ride/swim) rather than pushing further.`;
    }
    if (r <= 6.5 && c >= 0.85) {
      return `<b>You had headroom</b> — ${Math.round(c*100)}% completed at an average effort of ${r.toFixed(1)}/10. Next rotation: compress Foundation to 2–3 weeks, bring Week 10's Olympic-distance ride forward a couple of weeks, and grow the Sunday swim distance faster — you're ready to push the 70.3 base harder.`;
    }
    return `<b>This load suited you well</b> — ${Math.round(c*100)}% completed at an average effort of ${r.toFixed(1)}/10. Repeat the block close to as-is: a small nudge to Saturday's peak long run and the Sunday swim distance is enough progression for next time.`;
  }

  function renderCoach(){
    eventToggleEl.checked = settings.eventEnabled;
    eventFieldsEl.hidden = !settings.eventEnabled;
    eventDateEl.value = settings.eventDate || '';
    eventTypeEl.value = settings.eventType || 'hm';
    manualStartEl.value = settings.manualStart || '';

    eventBannerEl.innerHTML = '';
    if (settings.eventEnabled && settings.eventDate) {
      const wk = weeksToEventFor(settings.eventType);
      const raceRange = weekDateRange(wk);
      const w1 = weekDateRange(1);
      const banner = document.createElement('div');
      banner.className = 'event-banner';
      if (raceRange) {
        const today = new Date();
        const passed = today > addDays(raceRange.end, 1);
        if (passed) {
          banner.innerHTML = `<b>This block's race has passed</b> (${fmtDate(raceRange.start)}). Time to set your next event above and start a new rotation — the Block review below will help shape it.`;
        } else {
          banner.innerHTML = `Week 1 begins <b>${fmtDate(w1.start)}</b>, with race day landing on <b>${fmtDate(raceRange.start)}</b>. Calendar dates are now shown against every week on the Plan tab.`;
        }
        eventBannerEl.appendChild(banner);
      }
    } else {
      const w16 = weekByN(16);
      const relevantKeys = dayOrder.filter(k => w16.days[k] && !w16.days[k].optional);
      const doneCount = relevantKeys.filter(k => getEntry(16, k).done).length;
      if (relevantKeys.length && doneCount === relevantKeys.length) {
        const banner = document.createElement('div');
        banner.className = 'event-banner';
        banner.innerHTML = `<b>Week 16 is complete</b> — you've finished the rotation. Set your next event above, or just start back at Week 1 when you're ready.`;
        eventBannerEl.appendChild(banner);
      }
    }

    const review = computeReview();
    reviewStatsEl.innerHTML =
      '<div class="stat-tile"><div class="stat-num mono">' + Math.round(review.completion * 100) + '%</div><div class="stat-label">Sessions completed</div></div>' +
      '<div class="stat-tile"><div class="stat-num mono">' + (review.avgRpe != null ? review.avgRpe.toFixed(1) : '–') + '</div><div class="stat-label">Avg effort (' + review.rpeCount + ' rated)</div></div>';

    phaseBarsEl.innerHTML = '';
    Object.keys(phaseNames).forEach(p => {
      const ph = review.phases[p];
      const pct = ph.total ? Math.round(ph.done / ph.total * 100) : 0;
      const row = document.createElement('div');
      row.className = 'phase-bar-row';
      row.innerHTML =
        '<span class="pbr-name">' + phaseNames[p] + '</span>' +
        '<span class="phase-bar-track"><span class="phase-bar-fill" style="width:' + pct + '%"></span></span>' +
        '<span class="phase-bar-rpe mono">' + (ph.rpeCount ? (ph.rpeSum / ph.rpeCount).toFixed(1) : '–') + '</span>';
      phaseBarsEl.appendChild(row);
    });

    recommendBoxEl.innerHTML = recommendationHTML(review);
  }

  function buildNutrition(){
    nutListEl.innerHTML = '';
    nutrition.forEach(item => {
      const card = document.createElement('div');
      card.className = 'nut-card';
      card.innerHTML =
        '<h3>' + item.name + '</h3>' +
        '<p class="nut-recipe">' + item.recipe + '</p>' +
        '<div class="nut-row">' +
          '<span><b>Best for:</b> ' + item.use + '</span>' +
          '<span><b>Pros:</b> ' + item.pros + '</span>' +
          '<span><b>Cons:</b> ' + item.cons + '</span>' +
        '</div>' +
        '<div class="nut-carbs mono">' + item.carbs + '</div>';
      nutListEl.appendChild(card);
    });
  }

  // tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
      btn.classList.add('active'); btn.setAttribute('aria-selected','true');
      const tab = btn.dataset.tab;
      document.getElementById('tab-plan').hidden = tab !== 'plan';
      document.getElementById('tab-fuel').hidden = tab !== 'fuel';
      document.getElementById('tab-coach').hidden = tab !== 'coach';
      if (tab === 'coach') renderCoach();
    });
  });

  // coach form wiring
  eventToggleEl.addEventListener('change', () => {
    settings.eventEnabled = eventToggleEl.checked;
    persistSettings(); renderCoach(); renderWeek(); buildRail();
  });
  eventDateEl.addEventListener('change', () => {
    settings.eventDate = eventDateEl.value || null;
    persistSettings(); renderCoach(); renderWeek(); buildRail();
  });
  eventTypeEl.addEventListener('change', () => {
    settings.eventType = eventTypeEl.value;
    persistSettings(); renderCoach(); renderWeek(); buildRail();
  });
  manualStartEl.addEventListener('change', () => {
    settings.manualStart = manualStartEl.value || null;
    persistSettings(); renderCoach(); renderWeek(); buildRail();
  });

  buildLegend();
  buildNutrition();

  function startApp(){
    buildRail();
    buildPhaseOverview();
    renderWeek();
    renderCoach();
  }

  // ---------- auth bootstrap ----------
  let appStarted = false;

  async function enterApp(session){
    console.log('[auth] enterApp called', { userId: session.user && session.user.id, appStarted });
    currentUser = session.user;
    authGateEl.hidden = true;
    authSubmitBtnEl.disabled = false;
    // Set this *before* the awaits below, not after. onAuthStateChange can
    // fire this function twice in quick succession (e.g. INITIAL_SESSION
    // followed almost immediately by SIGNED_IN/TOKEN_REFRESHED) — without
    // setting the guard synchronously up front, both calls can race past
    // this check while the first is still awaiting loadRemoteState(),
    // and both then try to open a realtime subscription on the same
    // channel, which throws.
    if (appStarted) return;
    appStarted = true;
    try {
      await loadRemoteState(currentUser.id);
    } catch (e) {
      console.error('[auth] loadRemoteState failed', e);
      setAuthMsg('Signed in, but could not load your data — check your connection and reload.', 'error');
    }
    subscribeRemoteState(currentUser.id);
    startApp();
    console.log('[auth] enterApp finished, app started');
  }

  if (sb) sb.auth.onAuthStateChange(async (event, session) => {
    console.log('[auth] onAuthStateChange', event, { hasSession: !!session, hasUser: !!(session && session.user) });
    // A password-reset link lands here as PASSWORD_RECOVERY with a valid
    // (temporary) session — show the "set a new password" form instead of
    // dropping straight into the app on someone else's half-finished login.
    if (event === 'PASSWORD_RECOVERY') {
      authMode = 'reset';
      applyAuthMode();
      authGateEl.hidden = false;
      return;
    }
    if (session && session.user) {
      await enterApp(session);
    } else {
      console.log('[auth] no session on this event — showing sign-in form', { event });
      currentUser = null;
      appStarted = false;
      if (realtimeChannel) { sb.removeChannel(realtimeChannel); realtimeChannel = null; }
      authGateEl.hidden = false;
      authEmailEl.value = ''; authPasswordEl.value = '';
      if (authMode !== 'reset') setAuthMsg('');
    }
  });

})();
</script>
</body>
</html>
"""

html = html.replace("__DATA_JSON__", DATA_JSON)
html = html.replace("__SUPABASE_URL__", SUPABASE_URL)
html = html.replace("__SUPABASE_ANON_KEY__", SUPABASE_ANON_KEY)

with open("tri-half-synced.html", "w") as f:
    f.write(html)

print("written", len(html), "bytes")
