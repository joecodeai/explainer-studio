"""MiniMax H3 engine: its own ComfyUI (engines/ComfyUI, port 8189, venv .venv-comfy) next to the LTX/Qwen ComfyUI on 8188.

One shot = Ref2VA (character reference pictures) + MiniMaxH3AddGuide pinning our keyframe (or the previous shot's last frames,
for a continuous take) and OUR dialogue audio at frame 0, so the video is generated around the fixed voice track.
"flex" = Pika-H3-Flex 6-step (default), "base" = original H3 14-step.
"""
import json, os, shutil, subprocess, time, uuid
import requests
from . import config as C

DIR = os.path.join(C.ROOT, "engines", "ComfyUI")
URL = os.environ.get("H3_URL", "http://127.0.0.1:8189")
PY = os.path.join(C.ROOT, ".venv-comfy", "bin", "python")
UNET = "minimax_h3_ref2va_pruned_int8_convrot.safetensors"
TE = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
VAE, AVAE = "minimax_h3_video_vae_fp16.safetensors", "minimax_h3_audio_vae_fp32.safetensors"
LORA = "pika_h3_flex_ref2va_v1_bf16.safetensors"
FLEX_SIGMAS = "1.0, 0.972973, 0.923077, 0.8, 0.571429, 0.333333, 0.0"
FILES = [f"diffusion_models/{UNET}", f"text_encoders/{TE}", f"vae/{VAE}", f"vae/{AVAE}", f"loras/{LORA}"]
_proc = None


def available():
    return os.path.exists(PY) and all(os.path.exists(os.path.join(DIR, "models", f)) for f in FILES)


def up():
    try:
        return requests.get(f"{URL}/system_stats", timeout=3).ok
    except requests.RequestException:
        return False


def start():
    global _proc
    if up(): return
    log = open(os.path.join(C.ROOT, "logs", "comfyui_h3.log"), "a")
    _proc = subprocess.Popen([PY, "main.py", "--listen", "127.0.0.1", "--port", URL.rsplit(":", 1)[1], "--disable-auto-launch"],
                             cwd=DIR, stdout=log, stderr=log, start_new_session=True)
    for _ in range(300):
        if up(): return
        time.sleep(2)
    raise RuntimeError("H3 ComfyUI did not start; see logs/comfyui_h3.log")


def free():
    if up():
        requests.post(f"{URL}/free", json={"unload_models": True, "free_memory": True}, timeout=60)


def frames_for(seconds):
    n = max(124, round(seconds * 24))           # trained range starts at ~5 s; shorter shots are rendered at 5 s and trimmed
    return n + (5 - n % 17) % 17                 # H3 needs 17k+5 frames


def _stage(path, root=False):
    """Copy an input into ComfyUI/input (h3/ subfolder, or the root for LoadVideo) and return the name to reference."""
    d = os.path.join(DIR, "input", "" if root else "h3"); os.makedirs(d, exist_ok=True)
    stem, ext = os.path.splitext(os.path.basename(path))
    name = f"{stem}_{uuid.uuid4().hex[:6]}{ext}"
    shutil.copy(path, os.path.join(d, name))
    return name if root else f"h3/{name}"


def graph(keyframe, refs, audio, prompt, size=(864, 480), seconds=5.0, seed=7, mode="flex", guide_clip=None, steps=14, anchor_audio=True):
    w, h = size
    g = {
        "unet": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": TE, "type": "minimax", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "avae": {"class_type": "VAELoader", "inputs": {"vae_name": AVAE}},
        "kf": {"class_type": "LoadImage", "inputs": {"image": _stage(keyframe)}},
        "aud": {"class_type": "LoadAudio", "inputs": {"audio": _stage(audio)}},
        "r2v": {"class_type": "MiniMaxH3ReferenceToVideo", "inputs": {
            "clip": ["clip", 0], "vae": ["vae", 0], "audio_vae": ["avae", 0], "prompt": prompt,
            "width": w, "height": h, "length": frames_for(seconds), "ref_image_size": "match"}},
        "guide": {"class_type": "MiniMaxH3AddGuide", "inputs": {
            "positive": ["r2v", 0], "vae": ["vae", 0], "audio_vae": ["avae", 0], "latent": ["r2v", 1],
            "image": ["kf", 0], "frame_idx": 0}},
        "noise": {"class_type": "RandomNoise", "inputs": {"noise_seed": int(seed)}},
        "dec": {"class_type": "VAEDecode", "inputs": {"samples": ["samp", 0], "vae": ["vae", 0]}},
        "adec": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["samp", 0], "vae": ["avae", 0]}},
        "mk": {"class_type": "CreateVideo", "inputs": {"images": ["dec", 0], "audio": ["adec", 0], "fps": 24.0}},
        "save": {"class_type": "SaveVideo", "inputs": {"video": ["mk", 0], "filename_prefix": "h3/shot", "format": "mp4", "format.codec": "h264"}},
    }
    if guide_clip:          # continuous take: the previous shot's last frames (5 = smallest valid clip) anchored at frame 0
        g["gclip"] = {"class_type": "LoadVideo", "inputs": {"file": _stage(guide_clip, root=True)}}
        g["gparts"] = {"class_type": "GetVideoComponents", "inputs": {"video": ["gclip", 0]}}
        g["guide"]["inputs"]["image"] = ["gparts", 0]
    if anchor_audio:
        g["guide"]["inputs"]["audio"] = ["aud", 0]
    for i, r in enumerate([keyframe] + list(refs)):        # <Picture 1> = the keyframe, then the identity references
        g[f"ref{i}"] = {"class_type": "LoadImage", "inputs": {"image": _stage(r)}}
        g["r2v"]["inputs"][f"ref_images.ref_image_{i}"] = [f"ref{i}", 0]
    model = ["unet", 0]
    if mode == "flex":
        g["lora"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": model, "lora_name": LORA, "strength_model": 1.0}}
        model = ["lora", 0]
        g["ksel"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "lcm"}}
        g["sig"] = {"class_type": "ManualSigmas", "inputs": {"sigmas": FLEX_SIGMAS}}
    else:
        g["ksel"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}}
        g["sig"] = {"class_type": "BasicScheduler", "inputs": {"model": model, "scheduler": "simple", "steps": steps, "denoise": 1.0}}
    g["guider"] = {"class_type": "BasicGuider", "inputs": {"model": model, "conditioning": ["guide", 0]}}
    g["samp"] = {"class_type": "SamplerCustomAdvanced", "inputs": {
        "noise": ["noise", 0], "guider": ["guider", 0], "sampler": ["ksel", 0], "sigmas": ["sig", 0], "latent_image": ["r2v", 1]}}
    return g


def render(out, timeout=3600, **kw):
    """Render one shot to `out` (mp4 with H3's own decode of the audio). Returns {"comfy_s": seconds}."""
    start()
    r = requests.post(f"{URL}/prompt", json={"prompt": graph(**kw), "client_id": "h3"})
    if r.status_code != 200:
        raise RuntimeError(f"H3 graph rejected: {r.text[:2000]}")
    pid = r.json()["prompt_id"]; t0 = time.time()
    while time.time() - t0 < timeout:
        h = requests.get(f"{URL}/history/{pid}").json().get(pid)       # appears once the job has finished (ok or error)
        if h:
            st = h["status"]
            if st.get("status_str") != "success":
                raise RuntimeError(f"H3 render failed: {json.dumps(st.get('messages', []))[:2000]}")
            v = h["outputs"]["save"]["images"][0]
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            shutil.copy(os.path.join(DIR, "output", v.get("subfolder", ""), v["filename"]), out)
            m = {x[0]: x[1].get("timestamp") for x in st.get("messages", [])}
            return {"comfy_s": round((m.get("execution_success", 0) - m.get("execution_start", 0)) / 1000, 1)}
        time.sleep(2)
    raise TimeoutError("H3 render timed out")
