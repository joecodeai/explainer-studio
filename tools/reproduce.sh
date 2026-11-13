#!/usr/bin/env bash
# re-produce finished projects with the current pipeline (cached stages reused; renders redo on renderer changes)
cd "$(dirname "$0")/.."
for p in "$@"; do
  T=$(cat "projects/$p/TOPIC")
  echo "=== $p $(date +%H:%M)"
  ./make_video "$T" --approve > "logs/redo_${p:0:20}.log" 2>&1 || echo "FAILED $p"
  tail -2 "projects/$p/production.log"
done
