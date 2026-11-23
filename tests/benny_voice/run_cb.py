"""Render the Benny test script with Chatterbox for each reference (A = current, B1, B2), pace, assemble."""
import sys, os, json, subprocess
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import numpy as np, soundfile as sf
from studio import voice, config as C
T = sys.argv[1]
EMO = {"storytelling / overconfident": "confident", "noticing / curious pause": "confused", "confusion": "confused",
       "embarrassment / hesitant": "sad", "nervous laugh / defensive": "happy", "whisper / conspiratorial": "neutral",
       "excited / quick": "excited", "serious explanation / slower": "neutral", "playful teasing": "happy"}
lines = json.load(open(f"{T}/script.json"))["lines"]
refs = {"A_current": f"{C.VOICE_LIB}/benny/reference.wav", "B1_new": f"{T}/ref_B1.wav", "B2_new": f"{T}/ref_B2.wav"}
for k, ref in refs.items():
    os.makedirs(f"{T}/{k}", exist_ok=True)
    jobs = [{"text": l["text"], "ref": ref, "emotion": EMO[l["profile"]], "out": f"{T}/{k}/raw{i}.wav", "takes": 3} for i, l in enumerate(lines)]
    json.dump(jobs, open(f"{T}/{k}/jobs.json", "w"))
    subprocess.run([f"{C.ROOT}/.venv-tts/bin/python", f"{C.ROOT}/studio/tts_cb.py", f"{T}/{k}/jobs.json"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    files = []
    for i in range(len(lines)):
        w, sr = sf.read(f"{T}/{k}/raw{i}.wav", dtype="float32"); f = f"{T}/{k}/line{i}.wav"
        sf.write(f + ".r.wav", voice._trim(w, sr), sr); voice._clean(f + ".r.wav", f); os.remove(f + ".r.wav"); files.append(f)
    voice._pace_lines(files, {f: l["text"] for f, l in zip(files, lines)})
    out = []
    for f in files:
        a, sr = sf.read(f, dtype="float32"); out += [a, np.zeros(int(sr * 0.6), np.float32)]
    sf.write(f"{T}/BENNY_{k}.wav", np.concatenate(out), sr); print("done", k, flush=True)
