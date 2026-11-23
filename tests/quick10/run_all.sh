#!/usr/bin/env bash
# 10-second comparison: same moment (Ryan's opening + Maya's silent eyebrow), three pipelines, timed.
R=/home/mundax/Documents/REL/ExplainerStudio; cd $R; T=tests/acting_scene; Q=tests/quick10
PY=$R/.venv/bin/python
for s in benny maya; do ffmpeg -v error -y -i $T/track_$s.wav -t 10.3 $Q/track_$s.wav; done
ffmpeg -v error -y -i $T/mix.wav -t 10.3 $Q/mix.wav
$PY - <<'P'
import json
R="/home/mundax/Documents/REL/ExplainerStudio"; T="tests/acting_scene"; Q="tests/quick10"
inp=json.load(open(f"{T}/longcat_input_v2.json"))
inp["segment_prompts"]=inp["segment_prompts"][:3]; inp["prompt"]=inp["segment_prompts"][0]
inp["cond_audio"]={"person1":f"{R}/{Q}/track_benny.wav","person2":f"{R}/{Q}/track_maya.wav"}
json.dump(inp,open(f"{Q}/lc_input.json","w"),indent=1)
json.dump([{"input_json":f"{R}/{Q}/lc_input.json","num_segments":3,"out":f"{R}/{Q}/longcat480.mp4","seed":42,"clean_audio":True,"segment_text_guidance":{"2":3.0}}],open(f"{Q}/jobs.json","w"))
tl=json.load(open(f"{T}/timeline.json")); tl["timeline"]=[e for e in tl["timeline"] if e["start"]<10.3]; tl["duration"]=10.3
json.dump(tl,open(f"{Q}/timeline.json","w"))
P
$PY -c "import sys;sys.path.insert(0,'.');from studio import llm, comfy;llm.unload();comfy.free()" 2>/dev/null
t0=$(date +%s); tools/longcat_batch.sh $R/$Q/jobs.json 480p > $Q/longcat.log 2>&1; echo "longcat480 $(( $(date +%s)-t0 ))s" >> $Q/times.txt
t0=$(date +%s); PYTHONNOUSERSITE=1 $PY $Q/run_ltx.py 1280 704 > $Q/ltx704.log 2>&1; echo "ltx1280x704 $(( $(date +%s)-t0 ))s" >> $Q/times.txt
t0=$(date +%s); PYTHONNOUSERSITE=1 $PY $Q/run_ltx.py 1920 1088 > $Q/ltx1088.log 2>&1; echo "ltx1920x1088 $(( $(date +%s)-t0 ))s" >> $Q/times.txt
echo ALLDONE >> $Q/times.txt
