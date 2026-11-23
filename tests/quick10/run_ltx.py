"""Same acting test rendered with the current LTX conversation staging (per-line chained two-shot + stabiliser) for comparison."""
import sys, os, json, subprocess, shutil
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import numpy as np, soundfile as sf
from studio import talk, comfy, stabilize, pipeline as PL
T = "tests/acting_scene"; Q = "tests/quick10"; W_, H_ = int(sys.argv[1]), int(sys.argv[2]); O = f"{Q}/ltx{H_}"; os.makedirs(O, exist_ok=True)
sc = json.load(open(f"{T}/scene.json"))["beats"]; tl = json.load(open(f"{Q}/timeline.json"))
mix, sr = sf.read(f"{Q}/mix.wav", dtype="float32")
from PIL import Image
ref = f"{O}/ref.png"; Image.open(f"{T}/cond.png").convert("RGB").resize((W_, H_)).save(ref)
STY = ("Polished 2D anime-style animated series, warm colours, attractive expressive faces, consistent faces and clothes, natural hands with five fingers, hands mostly relaxed.")
start, outs = ref, []
ev = tl["timeline"]
for n, (b, e) in enumerate(zip(sc[:len(ev)], ev)):
    a = e["start"] if n else 0.0; z = ev[n + 1]["start"] if n + 1 < len(ev) else tl["duration"]
    aud, secs = talk.cut_audio(f"{Q}/mix.wav", a, z, f"{O}/aud{n}.wav", pad=0.0)
    who = "Nobody speaks; mouths closed." if b.get("silent") else "Only the speaking person's lips move, in exact sync with the speech; the listener's mouth stays closed."
    prompt = (f"Two people having a conversation in a cosy Japanese ramen shop, medium two-shot from mid-thigh up, they look at each other. "
              f"{b['act']}; {b['react']}. {who} Natural, subtle acting, expressions change gradually and stay. Static locked-off camera, no zoom. {STY}")
    raw = talk.clip(start, aud, prompt, f"{T}/ltx", f"shot{n}", secs, seed=777 + n, neg=talk.NEG_SCENE, w=W_, h=H_)
    shutil.copy(raw, f"{O}/shot{n}.mp4"); talk.fix_doubled(f"{O}/shot{n}.mp4")
    st, last = stabilize.stabilize(f"{O}/shot{n}.mp4", ref, f"{O}/stab{n}.mp4", tuple(int(v * W_ / 1280) for v in (45, 24, 1190, 669)))
    start = last; outs.append((st, z - a)); print("shot", n, flush=True)
comfy.free()
lst = open(f"{O}/list.txt", "w")
for n, (v, d) in enumerate(outs):
    o = f"{O}/cut{n}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-t", f"{d:.3f}", "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "25", o], check=True)
    lst.write(f"file '{os.path.abspath(o)}'\n")
lst.close()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{O}/list.txt", "-i", f"{Q}/mix.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-shortest", f"{Q}/ltx{W_}x{H_}.mp4"], check=True)
print("DONE", flush=True)
