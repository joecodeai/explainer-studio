"""Talking shots: LTX-2.5 image+audio -> video. The character's REAL voice line is encoded into the audio latent and frozen
(noise mask 0), so the model animates head, hands, body and lips to match the speech. Replaces cut-out mouth flaps."""
import os, random, subprocess
from . import comfy, config as C, workflows as W

NEG_SCENE = ("blurry, distorted face, extra limbs, extra fingers, extra hands, deformed hands, fused fingers, text, letters, captions, "
             "subtitles, watermark, logo, photorealistic, live action, 3d render, jitter, flicker, morphing, exaggerated expressions, "
             "camera shake, zoom in, zoom out, push in, dolly, camera movement, pan, frantic hand waving, both people talking at once")
NEG = ("blurry, distorted face, extra limbs, extra fingers, text, letters, captions, subtitles, watermark, logo, photorealistic, "
       "live action, 3d render, jitter, flicker, morphing, cartoon, childish, exaggerated expressions, camera shake")


def clip(image, audio, prompt, out_dir, name, seconds, fps=24, w=1280, h=704, seed=None, neg=None):
    """image: composed still (character in the scene); audio: wav of exactly this line. Returns mp4 path (video only is used)."""
    api = W.load("ltx_i2v")
    seed = seed if seed is not None else random.randint(0, 2**31)
    n = lambda i: f"398:{i}"
    api[n(364)]["inputs"]["text"] = prompt          # our prompt as-is (bypasses the LLM prompt-rewrite switch)
    api[n(373)]["inputs"]["text"] = neg or NEG
    api[n(362)]["inputs"]["value"] = max(1, int(-(-seconds // 1)))   # whole seconds, rounded up
    api[n(361)]["inputs"]["value"] = int(fps)
    api[n(372)]["inputs"]["value"] = int(w)
    api[n(360)]["inputs"]["value"] = int(h)
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(357)]["inputs"]["strength"] = 1.0           # keep the first frame = our still (identity, framing)
    api[n(339)]["inputs"]["noise_seed"] = seed
    api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    # audio conditioning: LoadAudio -> trim -> encode -> noise mask 0 (frozen) -> replaces the empty audio latent
    api["900"] = {"class_type": "LoadAudio", "inputs": {"audio": comfy.upload(audio)}}
    api["901"] = {"class_type": "TrimAudioDuration", "inputs": {"audio": ["900", 0], "start_index": 0.0, "duration": float(api[n(362)]["inputs"]["value"])}}
    api["902"] = {"class_type": "LTXVAudioVAEEncode", "inputs": {"audio": ["901", 0], "audio_vae": [n(386), 0]}}
    api["903"] = {"class_type": "SolidMask", "inputs": {"value": 0.0, "width": int(w), "height": int(h)}}
    api["904"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["902", 0], "mask": ["903", 0]}}
    api[n(377)]["inputs"]["audio_latent"] = ["904", 0]
    api.pop(n(366), None)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    return comfy.run(W.prune(api), out_dir, name, timeout=1800)[0]


def cut_audio(src, start, end, out, pad=0.15):
    """Line audio (with a little air) padded with silence to a whole number of seconds."""
    dur = end - start + 2 * pad
    whole = -(-dur // 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, start - pad):.3f}", "-t", f"{dur:.3f}", "-i", src,
                    "-af", f"apad=whole_dur={whole}", "-ac", "1", "-ar", "48000", out], check=True)
    return out, whole


def fix_doubled(path, fps=24):
    """LTX sometimes returns short clips at an effective 12 fps (every frame shown twice -> visible stutter).
    Detect that pattern and rebuild the clip: keep only the frames that change, then motion-interpolate back to 24 fps.
    Returns True if the clip was repaired in place."""
    import cv2, numpy as np, shutil, tempfile
    cap = cv2.VideoCapture(path); prev = None; d = []
    while True:
        ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(f, (320, 176)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None: d.append(float(np.abs(g - prev).mean()))
        prev = g
    cap.release()
    d = np.array(d)
    if len(d) < 12: return False
    big = np.median(d[d >= np.percentile(d, 60)])
    still = d < 0.12 * big                      # near-duplicate frames
    alt = np.mean(still[1:] != still[:-1])      # how often "duplicate / new" alternates
    if big < 0.5 or still.mean() < 0.3 or alt < 0.55: return False
    n = len(d) + 1
    tmp = tempfile.mkdtemp()
    out = os.path.join(tmp, "fixed.mp4")
    keep = [0] + [i + 1 for i in range(len(d)) if not still[i]]   # frame i+1 is new when diff i is large
    sel = "+".join(f"eq(n\\,{k})" for k in keep)
    rate = fps * len(keep) / n                                      # effective source rate (~12 fps)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf",
                    f"select='{sel}',setpts=N/({rate:.4f})/TB,"
                    f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop=24,trim=end_frame={n},setpts=N/{fps}/TB",
                    "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps), out], check=True)
    shutil.move(out, path); shutil.rmtree(tmp, ignore_errors=True)
    return True
