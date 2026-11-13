#!/usr/bin/env bash
cd "$(dirname "$0")/.."; M=ComfyUI/models; F=tools/fetch.sh
$F Comfy-Org/stable-audio-3 text_encoders/t5gemma_b_b_ul2.safetensors $M/text_encoders/t5gemma_b_b_ul2.safetensors
$F Comfy-Org/stable-audio-3 checkpoints/stable_audio_3_medium.safetensors $M/checkpoints/stable_audio_3_medium.safetensors
$F Comfy-Org/ace_step_1.5_ComfyUI_files checkpoints/ace_step_1.5_turbo_aio.safetensors $M/checkpoints/ace_step_1.5_turbo_aio.safetensors
echo AUDIODONE
