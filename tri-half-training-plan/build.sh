#!/usr/bin/env bash
# Regenerates plan_data.json and both HTML apps from source.
# Run this after editing gen_plan.py, gen_html.py, or gen_html_standalone.py.
set -euo pipefail
cd "$(dirname "$0")"

python3 gen_plan.py
python3 gen_html.py
python3 gen_html_standalone.py

mkdir -p dist docs
mv index.html dist/index.html
mv tri-half-rotation-plan.html dist/tri-half-rotation-plan.html

# docs/ is what GitHub Pages serves (Settings -> Pages -> Deploy from branch
# -> /docs). It's the standalone build, not dist/index.html: the hosted
# build depends on window.claude's db capability, which only exists inside
# Claude — on GitHub Pages it would silently fail to save anything at all.
# The standalone build uses localStorage instead, so it works anywhere.
cp dist/tri-half-rotation-plan.html docs/index.html
touch docs/.nojekyll

echo "Built dist/index.html (hosted, cross-device sync), dist/tri-half-rotation-plan.html (standalone, this device only), and docs/index.html (same standalone build, served by GitHub Pages)."
