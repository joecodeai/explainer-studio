#!/usr/bin/env bash
# H3 bake-off: start ComfyUI, render the yen scene as 4 beat shots, then speed variants. Results -> results.jsonl
set -u
ES=/home/mundax/Documents/REL/ExplainerStudio
B=$ES/tests/h3_bakeoff; IN=$B/in; OUT=$B/out; mkdir -p $OUT
PY=$ES/.venv/bin/python
cd $ES/engines/ComfyUI
if ! curl -sf http://127.0.0.1:8188/system_stats >/dev/null; then
  setsid nohup $ES/.venv-comfy/bin/python main.py --listen 127.0.0.1 --port 8188 --disable-auto-launch \
    > $ES/logs/comfyui.log 2>&1 < /dev/null &
  until curl -sf http://127.0.0.1:8188/system_stats >/dev/null; do sleep 2; done
fi
echo "comfy ready $(date +%T)"
shot() {  # id mode size seed tag [extra args]
  local id=$1 mode=$2 size=$3 seed=$4 tag=$5; shift 5
  local sec kf
  sec=$(python3 -c "import json;print(json.load(open('$IN/$id.json'))['seconds'])")
  kf=$(python3 -c "import json;print(json.load(open('$IN/$id.json'))['keyframe'])")
  echo "start $id $tag $(date +%T)"
  $PY $ES/tools/h3_run.py --keyframe $kf --ref $kf --ref $IN/ref_ryan.png --ref $IN/ref_maya.png \
    --audio $IN/$id.wav --prompt-file $IN/$id.txt --seconds $sec --mode $mode --size $size --seed $seed \
    --out $OUT/${id}_$tag.mp4 "$@" 2>&1 | tail -3 | tee -a $B/results.jsonl
}
# Round 1: the scene, Flex 6-step 864x480 (T1 lip-sync, T2 identity, T4 two speakers, T3 speed)
for id in b1 b2 b3 b4; do shot $id flex 864x480 7 flex480; done
echo "ROUND1 DONE $(date +%T)"
# Round 2: speed/quality variants on the two-speaker shot
shot b2 base 864x480 7 base480
shot b2 flex 1344x768 7 flex768
echo "BAKEOFF DONE $(date +%T)"
