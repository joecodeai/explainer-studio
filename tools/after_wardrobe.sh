#!/usr/bin/env bash
cd "$(dirname "$0")/.."
PYTHONNOUSERSITE=1 .venv/bin/python tools/clean_poses.py > logs/clean_poses.log 2>&1
exec tools/run_chain.sh "Benny millionaire in Japan reel" "Benny millionaire in Japan episode"
