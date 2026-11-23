"""Voice consistency: speaker similarity (Resemble voice encoder, same as tts_pick) of every line of one speaker in a voice
test against a reference recording. Runs in .venv-tts.

  .venv-tts/bin/python tools/voice_consistency.py projects/batbomb-voice-test maya library/voices/maya/ref_locked.wav
"""
import hashlib, json, os, sys
import numpy as np, librosa

proj, spk, ref = sys.argv[1:4]
tag = sys.argv[4] if len(sys.argv) > 4 else ""
import torch
from chatterbox.models.voice_encoder import VoiceEncoder
from huggingface_hub import hf_hub_download
ve = VoiceEncoder(); ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cpu")); ve = ve.to("cuda").eval()
emb = lambda w: (lambda e: e / np.linalg.norm(e))(ve.embeds_from_wavs([w], sample_rate=16000)[0])
r = emb(librosa.load(ref, sr=16000)[0])
key = lambda text: hashlib.md5((f"{spk}|{text}" + (f"|{tag}" if tag else "")).encode()).hexdigest()[:10]
sims = []
for s in json.load(open(os.path.join(proj, "lines.json"))):
    for i, ln in enumerate(s["lines"]):
        if ln["speaker"] != spk: continue
        f = os.path.join(proj, "audio", "lines", key(ln["text"]) + ".wav")
        if not os.path.exists(f): print("missing", s["id"], i); continue
        v = float(emb(librosa.load(f, sr=16000)[0]) @ r); sims.append(v)
        print(f"{s['id']}#{i:<2} {ln['voice']:<10} sim={v:.3f}  {ln['text'][:50]}")
a = np.array(sims)
print(json.dumps({"lines": len(a), "mean": round(float(a.mean()), 3), "min": round(float(a.min()), 3), "std": round(float(a.std()), 3)}))
