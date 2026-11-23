#!/usr/bin/env bash
# Resumable download of the LongCat-Video-Avatar 1.6 weights (retries stalled transfers).
cd "$(dirname "$0")/../engines/LongCat-Video"
export HF_HUB_DOWNLOAD_TIMEOUT=60 HF_HUB_ETAG_TIMEOUT=60
PY=/home/mundax/Documents/REL/ExplainerStudio/.venv/bin/python
for i in 1 2 3 4 5 6; do
  timeout 1800 $PY -c "
from huggingface_hub import snapshot_download
snapshot_download('meituan-longcat/LongCat-Video-Avatar-1.6', local_dir='weights/LongCat-Video-Avatar-1.6',
  allow_patterns=['base_model_int8/*','loraA/*','loraB/*','vocal_separator/*','scheduler/*','*.json','whisper-large-v3/*.json','whisper-large-v3/*.txt','whisper-large-v3/*.safetensors','whisper-large-v3/*.model','whisper-large-v3/*tokenizer*','whisper-large-v3/*vocab*','whisper-large-v3/*merges*'])
print('AVATAR done', flush=True)
snapshot_download('meituan-longcat/LongCat-Video', local_dir='weights/LongCat-Video', allow_patterns=['tokenizer/*','text_encoder/*','vae/*','scheduler/*','*.json'])
print('BASE done', flush=True)
" && break
  echo "retry $i"
done
