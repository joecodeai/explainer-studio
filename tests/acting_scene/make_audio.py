"""Voice the acting test, then build one track per character on a shared timeline (silence while the other speaks)."""
import sys, os, json, subprocess
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import numpy as np, soundfile as sf
from studio import voice, pace, config as C
T = sys.argv[1]; benny_ref = sys.argv[2]
sc = json.load(open(f"{T}/scene.json"))["beats"]
REF = {"benny": benny_ref, "maya": f"{C.VOICE_LIB}/maya/reference.wav"}
show = json.load(open(f"{C.LIBRARY}/show.json")); tts = {c["id"]: c.get("tts", {}) for c in show["cast"]}
profiles = {k: {"name": k, "tts": v} for k, v in tts.items()}
todo, idx, files = {}, [], {}
for i, b in enumerate(sc):
    if b.get("silent"): continue
    f = f"{T}/line{i}.wav"; files[i] = f; idx.append(i)
    todo.setdefault(b["spk"], []).append(({"text": b["text"], "emotion": b["emotion"], "direction": b.get("direction")}, f))
voice._chatterbox(todo, profiles)          # routes Benny to Ryan (qwen_custom), Maya to her Chatterbox reference
voice._pace_lines(list(files.values()), {files[i]: sc[i]["text"] for i in idx})
voice._match_tempo([(files[i], sc[i]["text"], sc[i]["emotion"]) for i in idx])
SR = 16000; import librosa
t = 0.3; tracks = {"benny": [], "maya": []}; timeline = []
segs = []
for i, b in enumerate(sc):
    if b.get("silent"):
        timeline.append({"i": i, "spk": b["spk"], "start": round(t, 2), "end": round(t + b["silent"], 2), "silent": True}); t += b["silent"]; continue
    a, _ = librosa.load(files[i], sr=SR); d = len(a) / SR
    segs.append((b["spk"], t, a)); timeline.append({"i": i, "spk": b["spk"], "start": round(t, 2), "end": round(t + d, 2), "text": b["text"]})
    nxt = next((x for x in sc[i + 1:] if not x.get("silent")), None)
    g = (pace.gap_between({"speaker": b["spk"], "text": b["text"], "pause_after": b.get("pause_after")}, {"speaker": nxt["spk"], "text": nxt["text"]})
         if nxt and not sc[i + 1].get("silent") else 0.15) if i + 1 < len(sc) else 0.8
    t += d + g
total = t + 0.4
for spk in tracks:
    tr = np.zeros(int(total * SR), np.float32)
    for s, st, a in segs:
        if s == spk: tr[int(st * SR):int(st * SR) + len(a)] = a
    sf.write(f"{T}/track_{spk}.wav", tr, SR)
mix = sf.read(f"{T}/track_benny.wav")[0] + sf.read(f"{T}/track_maya.wav")[0]
sf.write(f"{T}/mix.wav", mix, SR)
json.dump({"duration": round(total, 2), "timeline": timeline}, open(f"{T}/timeline.json", "w"), indent=1)
print("TOTAL", round(total, 2)); [print(x) for x in timeline]
