#!/usr/bin/env bash
# Resumable download of MiniMax-H3 (Comfy-Org ComfyUI-format files) into engines/ComfyUI/models.
cd "$(dirname "$0")/../engines" && mkdir -p ComfyUI/models
export HF_HUB_DOWNLOAD_TIMEOUT=60 HF_HUB_ETAG_TIMEOUT=60
PY=/home/mundax/Documents/REL/ExplainerStudio/.venv/bin/python
for i in 1 2 3 4 5 6 7 8; do
  timeout 3600 $PY -c "
from huggingface_hub import snapshot_download
snapshot_download('Comfy-Org/MiniMax-H3', local_dir='ComfyUI/models', allow_patterns=[
  'diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors',
  'text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors',
  'vae/minimax_h3_video_vae_fp16.safetensors', 'vae/minimax_h3_audio_vae_fp32.safetensors',
  'loras/pika_h3_flex_ref2va_v1_bf16.safetensors'])
print('H3 DOWNLOAD DONE', flush=True)
" && break
  echo "retry $i"
done
