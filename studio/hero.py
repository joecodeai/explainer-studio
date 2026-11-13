"""Cinematic hero shots: Qwen-Image keyframe in the channel style -> LTX-2.5 (distilled, int8) image-to-video."""
import os, random
from . import comfy, config as C, imagegen, workflows as W

NEG = "blurry, distorted faces, extra limbs, text, letters, words, writing, captions, subtitles, signs with writing, watermark, logo, photorealistic, live action, 3d render, jitter, flicker"


def clean_prompt(prompt):
    """Drop requested on-screen wording (quoted text, 'labelled/saying X') - image models garble text."""
    import re
    p = re.sub(r"[\"“”][^\"“”]{2,60}[\"“”]", "", prompt)
    p = re.sub(r"\b(labell?ed|saying|reading|titled|that says|with the words?)\b[^,.;]*", "", p, flags=re.I)
    return re.sub(r"\s{2,}", " ", p).strip()


def keyframe(prompt, out_dir, name):
    prompt = clean_prompt(prompt)
    return imagegen.t2i(f"{C.ART_STYLE}. Cinematic wide shot: {prompt}. Detailed background, dramatic lighting. "
                        "Absolutely NO text, letters, numbers or writing anywhere: every paper, screen, sign and document is blank.",
                        out_dir, name, 1280, 720)


def i2v(image, prompt, out_dir, name, seconds=5, fps=24, w=1280, h=704, seed=None):
    api = W.load("ltx_i2v")
    seed = seed if seed is not None else random.randint(0, 2**31)
    n = lambda title_id: f"398:{title_id}"
    api[n(364)]["inputs"]["text"] = (f"{clean_prompt(prompt)} Clean modern editorial illustration style like a serious news documentary, muted navy and warm grey palette, subtle realistic motion, "
                                     f"camera slowly pushes in. Matching ambient sound effects, no music, no speech.")
    api[n(373)]["inputs"]["text"] = NEG
    api[n(362)]["inputs"]["value"] = int(seconds)
    api[n(361)]["inputs"]["value"] = int(fps)
    api[n(372)]["inputs"]["value"] = int(w)
    api[n(360)]["inputs"]["value"] = int(h)
    api[n(366)]["inputs"]["batch_size"] = 1
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(339)]["inputs"]["noise_seed"] = seed
    api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    return comfy.run(W.prune(api), out_dir, name, timeout=1800)[0]


def make(prompt, out_dir, name, seconds=5):
    kf = keyframe(prompt, out_dir, name + "_kf")
    return i2v(kf, prompt, out_dir, name, seconds=seconds)
