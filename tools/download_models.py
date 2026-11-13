"""Download all non-gated models into ComfyUI/models + model folders. Resumable."""
import os, shutil, sys
from huggingface_hub import hf_hub_download, snapshot_download
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CM = os.path.join(R, "ComfyUI", "models")
def get(repo, f, sub):
    d = os.path.join(CM, sub); os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, os.path.basename(f))
    if os.path.exists(dst): print("have", dst, flush=True); return
    p = hf_hub_download(repo, f, local_dir=os.path.join(R, ".dl", repo.replace("/", "__")))
    shutil.move(p, dst); print("got", dst, flush=True)
which = sys.argv[1] if len(sys.argv) > 1 else "free"
if which == "free":
    for f, sub in [("diffusion_models/qwen_image_2.1_turbo_int8_convrot.safetensors", "diffusion_models"),
                   ("text_encoders/qwen3vl_8b_int8_convrot.safetensors", "text_encoders"),
                   ("vae/qwen_image_2.1_vae_bf16.safetensors", "vae")]:
        get("Comfy-Org/Qwen-Image-2.1", f, sub)
    for r in ["Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", "Qwen/Qwen3-TTS-12Hz-1.7B-Base"]:
        print(snapshot_download(r, local_dir=os.path.join(R, "models", r.split("/")[1])), flush=True)
    d = os.path.expanduser("~/.lmstudio/models/lmstudio-community/Qwen3.6-35B-A3B-GGUF")
    print(hf_hub_download("lmstudio-community/Qwen3.6-35B-A3B-GGUF", "Qwen3.6-35B-A3B-Q4_K_M.gguf", local_dir=d), flush=True)
elif which == "ltx":
    for f, sub in [("vae/ltx-2.5-audio-vae-bf16.safetensors", "vae"), ("vae/ltx-2.5-video-vae-bf16.safetensors", "vae"),
                   ("latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors", "latent_upscale_models"),
                   ("text_encoders/gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors", "text_encoders"),
                   ("diffusion_models/ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors", "diffusion_models")]:
        get("Lightricks/LTX-2.5", f, sub)
print("DONE", which)
