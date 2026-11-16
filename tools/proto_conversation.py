import sys, os, json, subprocess, shutil
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import numpy as np, soundfile as sf
from PIL import Image, ImageOps
from studio import talk, comfy, voice, pace, stabilize, config as C
D = sys.argv[1]; R = C.ROOT; L = C.CHAR_LIB
lines = json.load(open(f"{D}/lines.json"))
# 1) voices: one reference per character, best of 3 takes
jobs = [{"text": l["text"], "ref": f"{C.VOICE_LIB}/{l['spk']}/reference.wav", "emotion": l["emotion"], "out": f"{D}/raw{i}.wav", "takes": 3} for i, l in enumerate(lines)]
json.dump(jobs, open(f"{D}/jobs.json", "w"))
subprocess.run([f"{R}/.venv-tts/bin/python", f"{R}/studio/tts_cb.py", f"{D}/jobs.json"], check=True)
files = []
for i, l in enumerate(lines):
    w, sr = sf.read(f"{D}/raw{i}.wav", dtype="float32"); f = f"{D}/line{i}.wav"
    sf.write(f + ".r.wav", voice._trim(w, sr), sr); voice._clean(f + ".r.wav", f); os.remove(f + ".r.wav"); files.append(f)
voice._pace_lines(files, {f: l["text"] for f, l in zip(files, lines)})
# per-line audio incl. the gap/beat after it (so the shot covers the listener's reaction)
dl = [{"speaker": l["spk"], "text": l["text"], "pause_after": l.get("pause_after")} for l in lines]
for i, f in enumerate(files):
    a, sr = sf.read(f, dtype="float32")
    g = pace.gap_between(dl[i], dl[i + 1]) if i + 1 < len(dl) else 0.6
    a = np.concatenate([np.zeros(int(sr * 0.05), np.float32), a, np.random.default_rng(i).normal(0, 2e-4, int(sr * g)).astype(np.float32)])
    sf.write(f"{D}/seg{i}.wav", a, sr)
# 2) reference still 1280x704: Benny left facing right, Maya right (mirrored) facing left
W, H = 1280, 704
B = Image.open(os.path.join(C.BG_LIB, "coffee_shop_d7de30.png")).convert("RGB").resize((W, H))
def put(img, x, hpx, top, mirror=False):
    ch = Image.open(img).convert("RGBA")
    if mirror: ch = ImageOps.mirror(ch)
    ch = ch.resize((int(ch.width * hpx / ch.height), hpx)); bb = ch.getbbox()
    B.paste(ch, (int(W * x - ch.width / 2), int(top) - bb[1]), ch)
put(f"{L}/benny/poses/side_talk.png", 0.385, 800, 66)
put(f"{L}/maya/poses/side_listen.png", 0.615, 775, 82, mirror=True)
ref = f"{D}/ref.png"; B.save(ref)
crop = (83, 20, 1114, 627)                       # final medium two-shot window (heads with headroom, knees at the bottom)
STYLE = ("Polished 2D animated-series illustration style, warm friendly colours, attractive expressive faces, consistent faces and "
         "clothes, correct anatomy, natural hands with five fingers, hands mostly relaxed or holding the phone")
start, outs = ref, []
for i, l in enumerate(lines):
    secs = sf.info(f"{D}/seg{i}.wav").duration
    aud, whole = talk.cut_audio(f"{D}/seg{i}.wav", 0, secs, f"{D}/aud{i}.wav", pad=0.0)
    prompt = (f"Two friends having a conversation in a cosy coffee shop, medium two-shot, they look at each other. {l['act']}; "
              f"{l['react']}. Only the speaking person's lips move, in exact sync with the speech; the listener's mouth stays closed. "
              f"Natural, subtle acting: blinking, small head movements, expressions change gradually and stay. Static locked-off camera, "
              f"no zoom. {STYLE}.")
    raw = talk.clip(start, aud, prompt, f"{D}/work", f"shot{i}", whole, seed=4242 + i, neg=talk.NEG_SCENE)
    shutil.copy(raw, f"{D}/shot{i}.mp4"); talk.fix_doubled(f"{D}/shot{i}.mp4")
    st, last = stabilize.stabilize(f"{D}/shot{i}.mp4", ref, f"{D}/stab{i}.mp4", crop)
    start = last; outs.append((st, f"{D}/seg{i}.wav", secs, l["cam"])); print("shot", i, "ok", flush=True)
comfy.free()
# 3) edit: wide = the steady two-shot; cu_* = closer framing on that character from the SAME take (same acting)
X = {"cu_benny": 0.36, "cu_maya": 0.64}
lst = open(f"{D}/list.txt", "w")
for i, (v, a, secs, cam) in enumerate(outs):
    vf = "scale=1920:1080"
    if cam in X:
        cw, chh = int(1920 / 1.45), int(1080 / 1.45); cx = int(1920 * X[cam] - cw / 2); cx = max(0, min(1920 - cw, cx))
        vf = f"crop={cw}:{chh}:{cx}:40,scale=1920:1080"
    o = f"{D}/cut{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", a, "-map", "0:v", "-map", "1:a", "-vf", vf, "-t", f"{secs:.3f}",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "24", "-c:a", "aac", "-ar", "48000", o], check=True)
    lst.write(f"file '{o}'\n")
lst.close()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{D}/list.txt", "-c", "copy", f"{D}/PROTOTYPE_v2.mp4"], check=True)
print("DONE", flush=True)
