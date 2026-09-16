"""Generates plan_data.json: the 16-week rotation, as a list of week dicts.

Each week has a "days" dict keyed by slot (Mon, Tue_am, Tue_pm, Tue_eve, Wed,
Thu_lunch, Thu_eve, Fri, Sat, Sat_eve, Sun, Sun_eve). Each day is built with
day(): a discipline, title, short framing "detail", a duration, and an
optional "table" — the session's structure (warm-up/main-set/cool-down, or
commute/race legs) as rows for the UI to render as a small table. Rest and
S&C days have no table; every run/bike/swim session with real structure does.
"""

import json

# UI colour coding by discipline: run=coral, bike=amber, swim=teal, sc=violet, rest=neutral.
RUN, BIKE, SWIM, SC, REST = "run", "bike", "swim", "sc", "rest"

SC_ROTATION = [
    ("Lower-body strength", "3 rounds: goblet squat x12, single-leg RDL x8/side, calf raises x15, glute bridge x12"),
    ("Core + mobility", "Plank x3x45s, side plank x2/side, dead bug x10/side, hip flexor + thoracic mobility flow"),
    ("Upper + posture", "Press-ups x3x10, band pull-aparts x15, row x12, Copenhagen plank x30s/side"),
    ("Full-body circuit", "3 rounds: squat jump x8, press-up x10, RDL x10, plank x40s, easy 5min spin cooldown"),
]

def sc(week_idx):
    """S&C rotates through 4 short circuits, one per week, on a 4-week cycle.

    Lives on Saturday, well after parkrun (morning session, evening S&C) —
    not on Tuesday, which already carries two commute rides. Any time
    Saturday works, so it doesn't need to be an evening-only commitment.
    """
    name, detail = SC_ROTATION[week_idx % 4]
    return {"discipline": "sc", "title": f"S&C — {name}",
            "detail": f"{detail}. Any time today works — straight after parkrun, or later if that fits better.",
            "duration": "20-25 min"}

def R(set_, work, effort, recovery="–"):
    """One row of a session table: SET | WORK | EFFORT | RECOVERY."""
    return {"set": set_, "work": work, "effort": effort, "recovery": recovery}

def day(disc, title, detail, dur, tag=None, table=None):
    d = {"discipline": disc, "title": title, "detail": detail, "duration": dur}
    if tag: d["tag"] = tag
    if table: d["table"] = table
    return d

def commute_out(effort="steady, controlled", detail="Save the legs for the interval work on the way home.", dur="~70-90 min"):
    return day(BIKE, "Commute out — steady", detail, dur, table=[R("1", "33 km", effort)])

def commute_home(title, rows, detail, dur="~75-95 min"):
    return day(BIKE, f"Commute home — {title}", detail, dur, table=rows)

WEEKS = []

def add_week(n, phase, label, mon, tue_am, tue_pm, wed_swim, thu_lunch, thu_swim, fri, sat, sun, sun_eve, note=""):
    # Two slots are swapped on display, so the week's hard days each get a
    # genuine buffer on both sides instead of stacking:
    #  - Mon <-> Thu_lunch: the quality run (passed in as `mon`) lands on
    #    Thursday, and the rest slot (passed in as `thu_lunch`) lands on
    #    Monday — so the hard run no longer sits the day before Tuesday's
    #    hard commute.
    #  - Wed <-> Fri: the easy run (passed in as `fri`) lands on Wednesday,
    #    and the rest slot (passed in as `wed_swim`) lands on Friday — so
    #    Thursday's hard run is followed by a full rest day, not another
    #    running session, before Saturday's parkrun.
    # Net effect: Mon rest, Tue hard bike (no evening add-on — it's already a
    # 66km day), Wed easy run, Thu hard run + eve swim, Fri rest, Sat hard
    # parkrun + eve S&C (hours apart, not stacked), Sun easy bike + eve swim.
    # S&C lives on Saturday rather than Tuesday so the week's single heaviest
    # day (two commute rides) doesn't also carry a third session.
    WEEKS.append({
        "n": n, "phase": phase, "label": label, "note": note,
        "days": {
            "Mon": thu_lunch, "Tue_am": tue_am, "Tue_pm": tue_pm,
            "Wed": fri, "Thu_lunch": mon, "Thu_eve": thu_swim,
            "Fri": wed_swim, "Sat": sat, "Sat_eve": sc(n - 1),
            "Sun": sun, "Sun_eve": sun_eve,
        },
    })

# Recurring session shapes, reused across weeks.
def strides(n=4, target="strides — fast but relaxed"):
    return R(f"{n}x", "20 sec", target, "walk/jog back")

def easy_run(mins, strides_n=4):
    rows = [R("1", f"{mins} min", "easy")]
    if strides_n:
        rows.append(strides(strides_n))
    return rows

# ================= PHASE 1: FOUNDATION (Weeks 1-4) =================

add_week(1, 1, "Foundation — Week 1",
    day(RUN, "Easy aerobic + strides", "Easy continuous run, finished with strides to open the legs up.", "45 min",
        table=easy_run(30)),
    commute_out(),
    commute_home("intervals",
        [R("4x", "4 min", "RPE 7/10 — a couple of words, not a sentence", "3 min easy")],
        "No power meter needed — go by feel. First one back, see how it feels."),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest / easy walk", "Lunchtime off — walk if you like, or just eat properly.", "—"),
    day(SWIM, "Technique + aerobic", "Drills into a steady aerobic set.", "45 min",
        table=[R("1", "500 m", "warm-up drills (catch-up, single-arm, fist)"), R("10x", "100 m", "steady", "15 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun + extra", "Parkrun eases you in, then extend it.", "~45 min total",
        table=[R("1", "5 km", "parkrun, easy-moderate"), R("1", "15 min", "easy jog")]),
    day(BIKE, "Ride — easy", "Kept short — the commute is doing the heavy lifting this week.", "45-60 min",
        table=[R("1", "45-60 min", "easy, flat if possible")]),
    day(SWIM, "Continuous swim", "Starting where you're already comfortable.", "35 min",
        table=[R("1", "1500 m", "continuous, easy pace")]),
    note="Week 1 is about finding the rhythm of the new week structure. Your Tuesday commute (66km round trip) is already a serious aerobic session on its own — everything else is built around recovering from it, not adding to it."
)

add_week(2, 1, "Foundation — Week 2",
    day(RUN, "Tempo intro", "Building toward tempo work.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("1", "15 min", "moderately hard, controlled"), R("1", "5 min", "easy cool-down")]),
    commute_out(),
    commute_home("intervals", [R("5x", "4 min", "RPE 7/10 — hard-but-sustainable, short phrases only", "3 min easy")],
        "Same shape as Week 1, one more rep."),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest / mobility snack", "5-10min hips/ankles mobility if you fancy it — otherwise rest.", "—"),
    day(SWIM, "Technique + pull", "Pull work to isolate the arms, then drill.", "45 min",
        table=[R("1", "500 m", "warm-up"), R("8x", "100 m", "pull (buoy)", "15 sec"), R("6x", "50 m", "drill"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun race effort", "First real effort test of the block.", "~50 min total",
        table=[R("1", "5 km", "race effort"), R("1", "15-20 min", "easy jog")]),
    day(BIKE, "Ride — steady", "Steady, with the option to open up on any rolling terrain.", "60 min",
        table=[R("1", "60 min", "steady, 1-2 rolling efforts if terrain allows")]),
    day(SWIM, "Continuous swim", "Easy-steady pace.", "35 min", table=[R("1", "1600 m", "continuous, easy-steady")]),
    note="First real test: Saturday's parkrun at race effort. See where the fitness sits."
)

add_week(3, 1, "Foundation — Week 3",
    day(RUN, "Intervals", "The hardest run of the block so far.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("5x", "3 min", "5k effort", "90 sec jog"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady, controlled", "Save the legs — today's effort is on the way home."),
    commute_home("intervals — hardest yet", [R("6x", "4 min", "RPE 7-8/10", "2-3 min easy")],
        "Hardest interval day of this block."),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest / mobility", "Nothing today — save it for Tuesday's commute and Thursday's intervals.", "—"),
    day(SWIM, "Build set", "Each rep builds through the effort spectrum.", "45 min",
        table=[R("1", "500 m", "warm-up"), R("10x", "100 m", "build: easy → moderate → strong", "15 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun hard + extra", "Hardest parkrun effort of the block.", "~45 min total",
        table=[R("1", "5 km", "hard effort"), R("1", "15 min", "easy jog")]),
    day(BIKE, "Ride — steady", "Steady, with two efforts built in partway through.", "70 min",
        table=[R("1", "70 min total", "steady ride"), R("2x", "10 min", "moderate effort, within it", "easy between")]),
    day(SWIM, "Continuous swim", "Steady pace.", "40 min", table=[R("1", "1800 m", "continuous, steady")]),
    note="Peak load of the block — this is the hardest week before the reset."
)

add_week(4, 1, "Foundation — Week 4 (Recovery)",
    day(RUN, "Easy shakeout", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    commute_out("easy, no structure", "Easy both ways this week — the commute becomes your recovery ride."),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Full recovery this week."),
    day(REST, "Rest", "Full rest, or gentle stretch if you're restless.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Easy technique", "Deload week — nothing structured.", "30 min",
        table=[R("1", "1000 m", "easy, drills + long loose strokes")]),
    day(RUN, "Very easy", "No strides this week.", "20 min", table=[R("1", "20 min", "easy, no strides")]),
    day(RUN, "Parkrun — easy", "Run it purely on feel.", "~25 min", table=[R("1", "5 km", "easy/moderate, by feel")]),
    day(BIKE, "Off / easy spin", "The commute is your bike volume this week.", "0-30 min",
        table=[R("1", "0-30 min", "optional easy spin")]),
    day(SWIM, "Easy continuous swim", "Deload week.", "25 min", table=[R("1", "1000 m", "relaxed, technique only")]),
    note="Deload week — absorb the last 3 weeks. Resist the urge to push; this is what makes Week 5 possible."
)

# ================= PHASE 2: BUILD (Weeks 5-8) =================

add_week(5, 2, "Build — Week 5",
    day(RUN, "Tempo", "Comfortably hard, not a race effort.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("1", "20 min", "tempo, comfortably hard"), R("1", "5 min", "easy cool-down")]),
    commute_out(),
    commute_home("intervals", [R("4x", "6 min", "RPE 7/10 — a short sentence, not a conversation", "3 min easy")],
        "Longer reps than last block."),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest — Tuesday's two 33km legs and Thursday's tempo are where the load sits this week.", "—"),
    day(SWIM, "Threshold intro", "Building through the set, sharper on the last three.", "50 min",
        table=[R("1", "500 m", "warm-up"), R("8x", "150 m", "steady, building to mod-hard on the last 3", "20 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun + extra", "First proper long run of the block.", "~55 min total",
        table=[R("1", "5 km", "moderate-hard"), R("1", "25 min", "easy")]),
    day(BIKE, "Ride — steady", "Rolling terrain if you can find it.", "60 min", table=[R("1", "60 min", "steady, rolling terrain if available")]),
    day(SWIM, "Continuous swim", "Strong finish.", "40 min",
        table=[R("1", "1700 m", "continuous, steady"), R("1", "200 m", "strong finish")]),
    note="From here the Tuesday commute carries a bit more intent on the way out — think 'controlled effort', not all-out."
)

add_week(6, 2, "Build — Week 6",
    day(RUN, "Intervals", "Classic 5k-pace reps.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("6x", "800 m", "5k pace", "2 min jog"), R("1", "5 min", "easy cool-down")]),
    commute_out(),
    commute_home("intervals", [R("5x", "6 min", "RPE 7-8/10", "3 min easy")], "One more rep than last week."),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Threshold", "Even effort throughout.", "50 min",
        table=[R("1", "500 m", "warm-up"), R("8x", "150 m", "moderately hard", "20 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun race effort + extra", "Genuine race effort.", "~60 min total",
        table=[R("1", "5 km", "race effort"), R("1", "30 min", "easy")]),
    day(BIKE, "Ride w/ efforts", "Three efforts within a steady ride.", "65 min",
        table=[R("1", "65 min total", "steady ride"), R("3x", "8 min", "moderate effort, within it", "easy between")]),
    day(SWIM, "Continuous swim", "Aim to negative-split.", "45 min",
        table=[R("1", "2000 m", "continuous, negative-split the second half")]),
    note=""
)

add_week(7, 2, "Build — Week 7",
    day(RUN, "Tempo", "Biggest tempo block yet.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("1", "25 min", "tempo"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady, controlled", "The biggest interval session of the block is on the way home — save something for it.", "~65-85 min"),
    commute_home("intervals — biggest yet", [R("3x", "10 min", "RPE 7-8/10, sustained", "4 min easy")],
        "Longest intervals of the block — arrive home properly emptied.", "~70-90 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest — this is the biggest week of the block.", "—"),
    day(SWIM, "Threshold", "Longer reps at a strong, steady effort.", "50 min",
        table=[R("1", "500 m", "warm-up"), R("6x", "300 m", "steady-strong", "30 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun hard + extra", "Longest run so far (~9-10k total).", "~65 min total",
        table=[R("1", "5 km", "hard"), R("1", "35 min", "easy")]),
    day(BIKE, "Ride — steady", "Hillier route if you have one.", "75 min", table=[R("1", "75 min", "steady, hillier route if available")]),
    day(SWIM, "Continuous swim", "Biggest swim of the block.", "45 min", table=[R("1", "2200 m", "continuous, steady")]),
    note="Biggest week of the block. Sleep and food matter more than the sessions themselves this week."
)

add_week(8, 2, "Build — Week 8 (Recovery)",
    day(RUN, "Easy shakeout", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    commute_out("easy, no structure", "No structure, just get there.", "~75-95 min"),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Full recovery.", "~75-95 min"),
    day(REST, "Rest", "Full rest.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Easy technique", "Deload week.", "30 min", table=[R("1", "1000 m", "easy, drills + loose long strokes")]),
    day(RUN, "Very easy", "No strides this week.", "20 min", table=[R("1", "20 min", "easy, no strides")]),
    day(RUN, "Parkrun — easy", "No extra after.", "~25 min", table=[R("1", "5 km", "easy/moderate")]),
    day(BIKE, "Off / easy spin", "Optional, otherwise rest.", "0-30 min", table=[R("1", "0-30 min", "optional easy spin")]),
    day(SWIM, "Easy continuous swim", "Deload week.", "30 min", table=[R("1", "1200 m", "relaxed, technique only")]),
    note="Second deload — you've now built a genuine base. From here the training gets triathlon- and half-marathon-specific."
)

# ================= PHASE 3: SPECIFIC / PEAK (Weeks 9-12) =================
# Builds to the Olympic-distance triathlon at the end of Week 12.

add_week(9, 3, "Specific — Week 9",
    day(RUN, "Race-pace intervals", "10k-pace reps.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("5x", "1 km", "10k pace", "2 min jog"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady, controlled", "Steady, controlled effort.", "~70-90 min"),
    commute_home("race-pace intervals", [R("4x", "8 min", "RPE 7-8/10 — target Oly-tri bike effort", "3 min easy")],
        "Sustained rather than short bursts.", "~75-95 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Race-pace set", "Target Oly-tri pace throughout.", "50 min",
        table=[R("1", "500 m", "warm-up"), R("10x", "100 m", "target Oly-tri pace", "15 sec"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun + extra", "Finishing at half-marathon effort.", "~60 min total",
        table=[R("1", "5 km", "moderate"), R("1", "20 min", "easy"), R("1", "10 min", "half-marathon effort")]),
    day(BIKE, "Long ride + brick", "Race-effort intervals, then straight into a run.", "75 + 10 opt",
        table=[R("1", "75 min total", "steady ride"), R("3x", "10 min", "Oly-tri bike effort, within it", "easy between"), R("1", "10 min", "optional run off the bike")]),
    day(SWIM, "Continuous + sighting", "Practising sighting without breaking rhythm.", "45 min",
        table=[R("1", "2000 m", "continuous, sighting drill every 4th length")]),
    note="Bricks begin on Sunday, not Tuesday — Tuesday's two 33km legs are plenty; the transition practice belongs on the day with more recovery either side of it."
)

add_week(10, 3, "Specific — Week 10",
    day(RUN, "Tempo @ HM effort", "Longest sustained effort of the block.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("1", "30 min", "half-marathon effort"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady, controlled", "Steady, controlled effort.", "~70-90 min"),
    commute_home("race simulation", [R("2x", "15 min", "RPE 7/10 — sustained Oly-tri pacing", "5 min easy")],
        "Dress-rehearsal effort for race day.", "~80-100 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Race simulation", "One continuous effort at race pace.", "45 min",
        table=[R("1", "1500 m", "continuous @ target Oly-tri pace"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun race effort + extra", "~11-12k total, longest run to date.", "~65 min total",
        table=[R("1", "5 km", "race effort"), R("1", "35 min", "easy")]),
    day(BIKE, "Oly-tri distance + brick", "The full Olympic bike leg, then straight into a run.", "~90-100 min + 15",
        table=[R("1", "~40 km", "goal Oly-tri race effort"), R("1", "15 min", "run off the bike")]),
    day(SWIM, "Continuous swim", "Past Olympic swim distance, building toward 70.3.", "45 min",
        table=[R("1", "2200 m", "continuous, aerobic pace")]),
    note="Sunday's ride now covers the full Olympic-distance bike leg with a run straight off it — a genuine dress rehearsal."
)

add_week(11, 3, "Specific — Week 11 (mini taper)",
    day(RUN, "Sharpen", "Full recovery between reps — sharpness, not fatigue.", "40 min",
        table=[R("1", "10 min", "easy warm-up"), R("4x", "1 km", "10k pace", "full recovery"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady, controlled, easing off", "Save the legs for race week.", "~70-90 min"),
    commute_home("easy intervals", [R("3x", "5 min", "RPE 6-7/10", "full easy recovery")],
        "Legs light and ready, not emptied, for race week.", "~75-90 min"),
    day(REST, "Rest", "Full rest — save the legs for race week.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Easy + fast finish", "Practise your warm-up routine.", "30 min",
        table=[R("1", "500 m", "easy"), R("6x", "50 m", "fast"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "25 min", table=easy_run(20)),
    day(RUN, "Parkrun @ effort + short brick", "Keep the legs light.", "~35 min total",
        table=[R("1", "5 km", "moderate effort"), R("1", "10 min", "easy")]),
    day(BIKE, "Short brick ride", "Short and easy — just the transition feel.", "40 + 10 min",
        table=[R("1", "40 min", "easy-steady"), R("1", "10 min", "run off the bike, easy")]),
    day(SWIM, "Easy + race-pace pickups", "Legs light for race week.", "30 min",
        table=[R("1", "1200 m", "relaxed"), R("4x", "50 m", "race pace")]),
    note="Load comes down, sharpness goes up. Trust the fitness — the work is banked."
)

add_week(12, 3, "RACE WEEK — Olympic Triathlon",
    day(RUN, "Easy + strides", "Nothing hard.", "20 min", table=easy_run(20, strides_n=3)),
    commute_out("easy spin", "Legs stay fresh — this is not the week to test anything new.", "~75-95 min"),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Race is Saturday.", "~75-95 min"),
    day(REST, "Rest", "Full rest — race is tomorrow, everything's ready.", "—"),
    day(REST, "Rest", "Full rest — lay out kit, check the bike.", "—"),
    day(REST, "Rest / travel", "Travel to race venue if needed, feet up otherwise.", "—"),
    day(RUN, "Shakeout", "Legs moving, nothing more.", "10 min", table=[R("1", "10 min", "very easy"), strides(3)]),
    day(RUN, "🏁 OLYMPIC TRIATHLON — RACE DAY", "Trust your pacing, enjoy it.", "Race day", tag="race",
        table=[R("1", "1.5 km", "swim"), R("1", "40 km", "bike"), R("1", "10 km", "run")]),
    day(REST, "Recovery", "Full rest — today is for recovering, not training.", "—"),
    day(REST, "Rest", "Full rest the day after racing — skip the pool this week.", "—"),
    note="This is the goal race of the first half of the plan. Everything since Week 1 has been building to today."
)

# ================= PHASE 4: RECOVERY + HALF-MARATHON FOCUS (Weeks 13-16) =================

add_week(13, 4, "Recovery — Week 13",
    day(RUN, "Easy shakeout", "Walk breaks welcome.", "20 min", table=[R("1", "20 min", "easy, walk breaks welcome")]),
    commute_out("easy spin", "Legs still absorbing race effort.", "~75-95 min"),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Full recovery this week.", "~75-95 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(SWIM, "Easy recovery swim", "No effort, technique only.", "30 min", table=[R("1", "1000 m", "easy, technique only, no effort")]),
    day(RUN, "Very easy", "Just moving.", "20 min", table=[R("1", "20 min", "easy")]),
    day(RUN, "Parkrun — easy", "Purely social/recovery effort.", "~28 min", table=[R("1", "5 km", "easy, social/recovery")]),
    day(BIKE, "Off / easy spin", "Optional, otherwise rest.", "0-30 min", table=[R("1", "0-30 min", "optional easy spin")]),
    day(SWIM, "Easy continuous swim", "Easing back in post-race.", "30 min", table=[R("1", "1200 m", "relaxed")]),
    note="Post-race reset. The next 3 weeks pivot the emphasis toward running, aiming at the half marathon in Week 16."
)

add_week(14, 4, "Half-Marathon Build — Week 14",
    day(RUN, "Tempo @ HM pace", "Goal half-marathon pace.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("1", "30 min", "goal half-marathon pace"), R("1", "5 min", "easy cool-down")]),
    commute_out("steady", "The bike now shifts to maintenance, not a build focus.", "~70-90 min"),
    commute_home("easy intervals", [R("3x", "5 min", "RPE 6-7/10", "3 min easy")],
        "Just enough to keep some snap in the legs while running takes priority.", "~75-90 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest / easy", "Rest, or a very easy 20min jog if legs feel good.", "—"),
    day(SWIM, "Maintenance swim", "Even effort throughout.", "40 min",
        table=[R("1", "500 m", "warm-up"), R("8x", "100 m", "steady"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(30)),
    day(RUN, "Parkrun + extra @ HM pace", "Finishing at goal half-marathon pace.", "~60 min total",
        table=[R("1", "5 km", "moderate"), R("1", "30 min", "goal half-marathon pace")]),
    day(BIKE, "Ride — maintenance", "Just keeping the aerobic engine ticking.", "50 min", table=[R("1", "50 min", "easy-steady")]),
    day(SWIM, "Continuous swim", "Maintenance while running takes priority.", "40 min",
        table=[R("1", "2000 m", "continuous, steady")]),
    note="Running takes priority; swim and bike drop to maintenance volume — the Tuesday commute alone comfortably covers that — so the legs can absorb run-specific load."
)

add_week(15, 4, "Half-Marathon Peak — Week 15",
    day(RUN, "Intervals", "10k-pace reps, protecting Saturday's long run.", "45 min",
        table=[R("1", "10 min", "easy warm-up"), R("5x", "1 km", "10k pace", "90 sec"), R("1", "5 min", "easy cool-down")]),
    commute_out("easy-steady", "Protect the legs for Saturday's big long run — nothing hard today.", "~75-95 min"),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Legs are for Saturday.", "~75-95 min"),
    day(REST, "Rest / optional mobility", "Save the legs for tomorrow's parkrun — a short stretch if you fancy it, otherwise switch off completely.", "—"),
    day(REST, "Rest", "Full rest — this is the week of the big long run.", "—"),
    day(SWIM, "Maintenance swim", "Even effort throughout.", "35 min",
        table=[R("1", "500 m", "warm-up"), R("6x", "150 m", "steady"), R("1", "200 m", "easy cool-down")]),
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "30 min", table=easy_run(25)),
    day(RUN, "Parkrun + long extra", "Peak long run of the block, ~15-16k total.", "~70 min total",
        table=[R("1", "5 km", "moderate"), R("1", "45-50 min", "half-marathon pace")]),
    day(BIKE, "Off", "Rest, or a very easy spin.", "0-30 min", table=[R("1", "0-30 min", "optional very easy spin")]),
    day(SWIM, "Easy recovery swim", "Protecting the legs after Saturday.", "30 min", table=[R("1", "1400 m", "relaxed technique")]),
    note="This is the biggest running week of the whole plan — everything after this is taper."
)

add_week(16, 4, "RACE WEEK — Half Marathon",
    day(RUN, "Easy + strides", "Easy run, strides to finish.", "20 min", table=easy_run(20, strides_n=3)),
    commute_out("easy spin", "Legs fresh for race day.", "~75-95 min"),
    commute_home("easy", [R("1", "33 km", "easy spin, no intervals")], "Race is Saturday.", "~75-95 min"),
    day(REST, "Rest", "Full rest — race is tomorrow, everything's ready.", "—"),
    day(REST, "Rest", "Full rest.", "—"),
    day(REST, "Rest", "Full rest — lay out race kit.", "—"),
    day(RUN, "Shakeout", "Sharp, not tired.", "15 min", table=[R("1", "15 min", "very easy"), strides(3, "strides @ goal pace")]),
    day(RUN, "🏁 HALF MARATHON — RACE DAY", "All the work is banked — run your own race.", "Race day", tag="race",
        table=[R("1", "21.1 km", "goal pace")]),
    day(REST, "Recovery", "Full rest and celebrate — then see the rotation notes for what's next.", "—"),
    day(REST, "Rest", "Full rest and recovery after the half marathon — celebrate instead.", "—"),
    note="Sixteen weeks, done. See the 'What's next' panel for how to loop this rotation or step up toward a 70.3 / marathon."
)

with open("plan_data.json", "w") as f:
    json.dump(WEEKS, f, indent=1)

print("weeks:", len(WEEKS))
