"""Qwen-Image-2.1 (ComfyUI): text-to-image, multi-reference edit, background removal."""
import os, random
from . import comfy, workflows as W


def _common(api, prompt, w, h, seed):
    W.set_input(api, "TextEncodeQwenImage21", "prompt", prompt)
    for k in W.find(api, "EmptyLatentImage"):
        api[k]["inputs"].update(width=int(w) // 16 * 16, height=int(h) // 16 * 16)
    for k in W.find(api, "RandomNoise"): api[k]["inputs"]["noise_seed"] = seed
    for k in W.find(api, "KSampler"): api[k]["inputs"]["seed"] = seed


def t2i(prompt, out_dir, name, w=1024, h=1024, seed=None):
    api = W.load("qwen_t2i")
    _common(api, prompt, w, h, seed if seed is not None else random.randint(0, 2**31))
    return comfy.run(W.prune(api), out_dir, name)[0]


def edit(prompt, refs, out_dir, name, w=1024, h=1024, seed=None, fixed_size=False):
    """refs: list of local image paths (<=10) — identity/style references."""
    api = W.load("qwen_edit")
    names = [comfy.upload(p) for p in refs]
    enc = W.find(api, "TextEncodeQwenImage21")[0]
    load = W.find(api, "LoadImage")[0]
    api[load]["inputs"]["image"] = names[0]
    inputs = api[enc]["inputs"]
    for k in [k for k in inputs if k.startswith("images.")]: del inputs[k]
    for i, n in enumerate(names):
        nid = load if i == 0 else f"ref{i}"
        if i: api[nid] = {"class_type": "LoadImage", "inputs": {"image": n}, "_meta": {"title": "ref"}}
        inputs[f"images.image_{i + 1}"] = [nid, 0]
    _common(api, prompt, w, h, seed if seed is not None else random.randint(0, 2**31))
    if fixed_size:   # use EmptyLatentImage (w x h) instead of the reference image's size
        for k in W.find(api, "ComfySwitchNode"):
            if api[k]["inputs"].get("on_true") and isinstance(api[k]["inputs"]["on_true"], list) and \
               api[api[k]["inputs"]["on_true"][0]]["class_type"] == "EmptyLatentImage":
                api[k]["inputs"]["switch"] = True
    return comfy.run(W.prune(api), out_dir, name)[0]


def has_alpha(path, frac=0.08):
    from PIL import Image
    import numpy as np
    im = Image.open(path)
    if im.mode != "RGBA": return False
    a = np.asarray(im.split()[-1])
    return (a < 10).mean() > frac


def remove_bg(path, out_dir, name, seed=1):
    """Qwen-Image-2.1 background removal -> RGBA."""
    api = W.load("qwen_bgremove")
    W.set_input(api, "UNETLoader", "unet_name", "qwen_image_2.1_turbo_int8_convrot.safetensors")
    W.set_input(api, "LoadImage", "image", comfy.upload(path))
    W.set_input(api, "TextEncodeQwenImage21", "prompt", "Remove the background completely and output the subject on a transparent background. Keep the subject exactly unchanged.")
    for k in W.find(api, "KSampler"): api[k]["inputs"].update(seed=seed, steps=8)
    return comfy.run(W.prune(api), out_dir, name)[0]
