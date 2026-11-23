#!/usr/bin/env bash
# LongCat-Video-Avatar 1.6 multi-person render of the acting test (one continuous take, both characters, own audio each).
set -e
R=/home/mundax/Documents/REL/ExplainerStudio
cd $R/engines/LongCat-Video
NSEG=$($R/.venv/bin/python -c "import json; print(len(json.load(open('$R/tests/acting_scene/longcat_input.json'))['segment_prompts']))")
export LONGCAT_TE_OFFLOAD=1 PYTHONPATH=$R/engines/shims:$PYTHONPATH PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
$R/.venv-longcat/bin/torchrun --nproc_per_node=1 run_demo_avatar_multi_audio_to_video.py --context_parallel_size=1 \
  --checkpoint_dir=./weights/LongCat-Video-Avatar-1.6 --input_json=$R/tests/acting_scene/longcat_input.json \
  --output_dir=$R/tests/acting_scene/longcat_out --resolution 720p --num_segments $NSEG \
  --use_distill --model_type avatar-v1.6 --use_int8
