#!/usr/bin/env bash
cd "$(dirname "$0")/.."; M=ComfyUI/models; F=tools/fetch.sh
$F Comfy-Org/Qwen-Image-2.1 vae/qwen_image_2.1_vae_bf16.safetensors $M/vae/qwen_image_2.1_vae_bf16.safetensors
$F Comfy-Org/Qwen-Image-2.1 text_encoders/qwen3vl_8b_int8_convrot.safetensors $M/text_encoders/qwen3vl_8b_int8_convrot.safetensors
for r in Qwen3-TTS-12Hz-1.7B-VoiceDesign Qwen3-TTS-12Hz-1.7B-Base; do
  for f in $(curl -s https://huggingface.co/api/models/Qwen/$r | python3 -c "import json,sys;print(' '.join(s['rfilename'] for s in json.load(sys.stdin)['siblings']))"); do
    $F Qwen/$r $f models/$r/$f; done; done
for f in vae/ltx-2.5-audio-vae-bf16.safetensors vae/ltx-2.5-video-vae-bf16.safetensors; do $F Lightricks/LTX-2.5 $f $M/vae/$(basename $f); done
$F Lightricks/LTX-2.5 latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors $M/latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors
$F Lightricks/LTX-2.5 text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors $M/text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors
$F Lightricks/LTX-2.5 diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors $M/diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors
$F lmstudio-community/Qwen3.6-35B-A3B-GGUF Qwen3.6-35B-A3B-Q4_K_M.gguf ~/.lmstudio/models/lmstudio-community/Qwen3.6-35B-A3B-GGUF/Qwen3.6-35B-A3B-Q4_K_M.gguf
echo ALLDONE
