#!/usr/bin/env bash
# fetch.sh REPO FILE DEST — resumable HF download that restarts on stalls
repo=$1; file=$2; dest=$3; tok=$(cat ~/.cache/huggingface/token 2>/dev/null)
mkdir -p "$(dirname "$dest")"; [ -f "$dest" ] && { echo "have $dest"; exit 0; }
for i in $(seq 1 200); do
  curl -sL -C - --speed-limit 300000 --speed-time 45 -H "Authorization: Bearer $tok" \
    -o "$dest.part" "https://huggingface.co/$repo/resolve/main/$file" && { mv "$dest.part" "$dest"; echo "got $dest"; exit 0; }
  sleep 3
done; echo "FAILED $dest"; exit 1
