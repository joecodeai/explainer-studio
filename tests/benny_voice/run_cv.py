"""Benny test script with Qwen3-TTS CustomVoice presets (fixed identity) + per-line acting directions."""
import sys, os, json
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import numpy as np, soundfile as sf, torch
from qwen_tts import Qwen3TTSModel
from studio import voice
T = sys.argv[1]
DIR = {"storytelling / overconfident": "Relaxed and very sure of himself, explaining it like an obvious fact, with a little extra punch on 'Thousands!'",
       "noticing / curious pause": "Stops short, a beat of silence, then wary and slightly defensive, half-laughing",
       "confusion": "Slow and genuinely confused, the pitch rising on 'cent', trailing off",
       "embarrassment / hesitant": "Quietly embarrassed, hesitant, slowing down as he realises, a small awkward laugh at the end",
       "nervous laugh / defensive": "Recovering with a nervous laugh, trying to sound confident again, playful",
       "whisper / conspiratorial": "Whispering, conspiratorial, leaning in, a little guilty",
       "excited / quick": "Suddenly excited and fast, words tumbling out, amazed",
       "serious explanation / slower": "Calm and clear, a bit proud that he finally understands, steady pace",
       "playful teasing": "Smug and playful, teasing, with a grin in the voice"}
lines = json.load(open(f"{T}/script.json"))["lines"]
m = Qwen3TTSModel.from_pretrained("/home/mundax/Documents/REL/ExplainerStudio/models/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0", dtype=torch.bfloat16)
for spk in ("Aiden", "Ryan"):
    k = f"C_{spk}"; os.makedirs(f"{T}/{k}", exist_ok=True); files = []
    for i, l in enumerate(lines):
        w, sr = m.generate_custom_voice(text=l["text"], language="English", speaker=spk, instruct=DIR[l["profile"]])
        f = f"{T}/{k}/line{i}.wav"; sf.write(f + ".r.wav", voice._trim(w[0], sr), sr); voice._clean(f + ".r.wav", f); os.remove(f + ".r.wav"); files.append(f)
    voice._pace_lines(files, {f: l["text"] for f, l in zip(files, lines)})
    out = []
    for f in files:
        a, sr = sf.read(f, dtype="float32"); out += [a, np.zeros(int(sr * 0.6), np.float32)]
    sf.write(f"{T}/BENNY_{k}.wav", np.concatenate(out), sr); print("done", k, flush=True)
