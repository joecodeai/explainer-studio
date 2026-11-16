#!/usr/bin/env bash
# Produce several projects one after another (GPU stays busy): tools/run_chain.sh "topic 1" "topic 2" ...
cd "$(dirname "$0")/.."
for t in "$@"; do
  slug=$(echo "$t" | tr 'A-Z' 'a-z' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g' | cut -c1-50)
  echo "[$(date +%H:%M)] start $t"
  PYTHONNOUSERSITE=1 .venv/bin/python make_video.py "$t" --approve > "logs/${slug}.log" 2>&1
  echo "[$(date +%H:%M)] end $t (exit $?)"
done
