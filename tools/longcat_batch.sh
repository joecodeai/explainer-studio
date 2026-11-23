#!/usr/bin/env bash
# Render a batch of LongCat-Video-Avatar 1.6 two-person scenes with the models loaded once:  tools/longcat_batch.sh jobs.json [480p|720p]
R=/home/mundax/Documents/REL/ExplainerStudio
cd $R/engines/LongCat-Video
export LONGCAT_TE_OFFLOAD=1 PYTHONPATH=$R/engines/shims:$PYTHONPATH PYTORCH_ALLOC_CONF=expandable_segments:True
exec $R/.venv-longcat/bin/torchrun --nproc_per_node=1 run_batch_multi.py --context_parallel_size=1 --jobs "$1" \
  --checkpoint_dir=./weights/LongCat-Video-Avatar-1.6 --resolution "${2:-480p}" \
  --use_distill --model_type avatar-v1.6 --use_int8 --mix_steps 0 --lora_path loraB/lora.safetensors --lora_multiplier 1.0
