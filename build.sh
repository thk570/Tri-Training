#!/usr/bin/env bash
# Regenerates plan_data.json and all three HTML apps from source.
# Run this after editing gen_plan.py, gen_html.py, gen_html_standalone.py,
# or gen_html_supabase.py.
set -euo pipefail
cd "$(dirname "$0")"

python3 gen_plan.py
python3 gen_html.py
python3 gen_html_standalone.py
python3 gen_html_supabase.py

mkdir -p dist docs
mv index.html dist/index.html
mv tri-half-rotation-plan.html dist/tri-half-rotation-plan.html
mv tri-half-synced.html dist/tri-half-synced.html

# docs/ is what GitHub Pages serves (Settings -> Pages -> Deploy from branch
# -> /docs). It's the Supabase-synced build, not dist/index.html or
# dist/tri-half-rotation-plan.html: dist/index.html depends on window.claude's
# db capability, which only exists inside Claude — on GitHub Pages it would
# silently fail to save anything at all. dist/tri-half-rotation-plan.html
# works anywhere but never syncs between devices (localStorage only) — keep
# it around as a no-account offline fallback, but it's not what phones should
# be pointed at day to day.
cp dist/tri-half-synced.html docs/index.html
touch docs/.nojekyll

echo "Built dist/index.html (hosted via Claude, cross-device sync), dist/tri-half-rotation-plan.html (standalone, offline-only fallback), dist/tri-half-synced.html (Supabase-synced), and docs/index.html (= tri-half-synced.html, served by GitHub Pages)."
