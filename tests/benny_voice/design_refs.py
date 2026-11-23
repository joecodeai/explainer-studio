"""Design new candidate Benny reference recordings (VoiceDesign), conversational rather than announcer-like."""
import sys, os, json
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio")
import torch, soundfile as sf
from qwen_tts import Qwen3TTSModel
from studio import config as C, voice
OUT = sys.argv[1]
REF = ("Ha, okay, okay, so, listen. I had this whole plan, right? And honestly? It was a good plan. Mostly. "
       "Well... it was a plan. Anyway, the point is, I'm fine. Totally fine. Why are you looking at me like that?")
INSTR = {
 "B1": "A 25-year-old American man with a warm, relaxed, charismatic voice, playful and a little cheeky, natural conversational delivery "
       "with a genuine laugh at the start and small natural hesitations, like a likeable sitcom actor improvising; natural mid-low male pitch, "
       "light casual General American accent; not an announcer, not exaggerated, not cartoonish.",
 "B2": "A friendly, confident young man in his mid-twenties, easygoing and expressive, slightly husky warm voice with a smile in it, "
       "relaxed rhythm that speeds up when excited and slows down when unsure, casual neutral American accent, talks like he's chatting with "
       "his best friend; genuine, spontaneous, never theatrical.",
}
m = Qwen3TTSModel.from_pretrained(C.TTS_DESIGN, device_map="cuda:0", dtype=torch.bfloat16)
for k, ins in INSTR.items():
    best = None
    for t in range(6):
        w, sr = m.generate_voice_design(text=REF, language="English", instruct=ins)
        f0 = voice.pitch(w[0], sr); print(k, t, round(f0), flush=True)
        if 100 <= f0 <= 150: best = w[0]; break
        best = best if best is not None else w[0]
    sf.write(f"{OUT}/ref_{k}.wav", best, sr); open(f"{OUT}/ref_{k}.txt", "w").write(REF)
print("DONE")
