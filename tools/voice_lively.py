"""Livelier locked voice: same identity, quicker amused delivery.

The locked clone copies the pacing of its ONE reference recording. Maya's reference was a slow dramatic documentary line, so every
line came out slow and flat. This makes a new reference in her voice with a brisk, amused read, then compares old vs new on the
same lines.

  P=.venv/bin/python; export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1
  $P tools/voice_lively.py takes        # 8 lively VoiceDesign takes of REF (Maya's design text) -> projects/voice-lively/ref_takes/
  .venv-tts/bin/python tools/voice_lively.py score   # similarity to the locked voice + pace; best -> library/voices/maya/ref_lively.wav
  $P tools/voice_lively.py compare      # same test lines: A = old lock (sped up), B = lively lock -> projects/voice-lively/COMPARE.wav
"""
import json, os, re, sys
import numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
OUT = "projects/voice-lively"; os.makedirs(f"{OUT}/ref_takes", exist_ok=True)
LOCK = "library/voices/maya/ref_locked.wav"
REF = ("Okay, so here's the thing. In 1858, London had a smell problem. Not a little one. A national-news, give-it-a-name, "
       "politicians-running-out-of-meetings kind of problem. And honestly? They had it coming.")
DIRECTION = ("Brisk, quick conversational pace, about three words per second. Playful and amused, a smile in the voice, like telling a "
             "friend a ridiculous true story. Natural energy and rhythm, crisp consonants, light emphasis on the punchlines. "
             "Never slow, never dramatic, never announcer-like.")
LINES = ["Then the smell reached the one building that mattered.",
         "They soaked the curtains in chemicals. The curtains lost.",
         "Nothing speeds up a government like a problem it can smell from its own desk.",
         "So they beat cholera by accident. Wrong theory. Right sewer."]


def takes():
    import torch
    from qwen_tts import Qwen3TTSModel
    sh = json.load(open("library/show.json")); t = [c for c in sh["cast"] if c["id"] == "maya"][0]["tts"]["previous"]
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cuda:0", dtype=torch.bfloat16)
    for k in range(8):
        torch.manual_seed(1000 + k)
        w, sr = m.generate_voice_design(text=REF, language="English", instruct=t["design"] + " " + DIRECTION)
        sf.write(f"{OUT}/ref_takes/t{k}.wav", w[0], sr); print("take", k, flush=True)


def score():
    import torch, librosa
    from chatterbox.models.voice_encoder import VoiceEncoder
    from huggingface_hub import hf_hub_download
    ve = VoiceEncoder(); ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cpu")); ve = ve.to("cuda").eval()
    emb = lambda w: (lambda e: e / np.linalg.norm(e))(ve.embeds_from_wavs([w], sample_rate=16000)[0])
    r = emb(librosa.load(LOCK, sr=16000)[0]); n = len(re.split(r"[\s-]+", REF)); best = None
    for k in range(8):
        f = f"{OUT}/ref_takes/t{k}.wav"; w = librosa.load(f, sr=16000)[0]
        sim = float(emb(w) @ r); wps = n / (len(w) / 16000)
        print(f"t{k} sim={sim:.3f} pace={wps:.2f} w/s")
        if best is None or sim > best[1]: best = (k, sim, wps)       # voice match first; pace is fixed by tempo afterwards
    print("BEST", best)
    import shutil
    shutil.copy(f"{OUT}/ref_takes/t{best[0]}.wav", "library/voices/maya/ref_lively.wav")
    open("library/voices/maya/ref_lively.txt", "w").write(REF)


def compare():
    import torch, subprocess
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0", dtype=torch.bfloat16)
    parts = []
    for name, ref, txt, tempo in (("A_old_sped", LOCK, open("library/voices/maya/ref_locked.txt").read().strip(), 1.12),
                                  ("B_lively", "library/voices/maya/ref_lively.wav", REF, 1.0),
                                  ("C_lively_sped", "library/voices/maya/ref_lively.wav", REF, 1.1)):
        cp = m.create_voice_clone_prompt(ref_audio=ref, ref_text=txt)
        for i, line in enumerate(LINES):
            torch.manual_seed(7 + i)
            w, sr = m.generate_voice_clone(text=line, language="English", voice_clone_prompt=cp)
            f = f"{OUT}/{name}_{i}.wav"; sf.write(f, w[0], sr)
            if tempo != 1.0:
                subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f, "-af", f"atempo={tempo}", f + ".t.wav"], check=True); os.replace(f + ".t.wav", f)
            a, sr2 = sf.read(f, dtype="float32"); parts.append(np.concatenate([a, np.zeros(int(0.35 * sr2), np.float32)]))
        parts.append(np.zeros(int(1.2 * sr2), np.float32))
    sf.write(f"{OUT}/COMPARE.wav", np.concatenate(parts), sr2); print("COMPARE", f"{OUT}/COMPARE.wav")


{"takes": takes, "score": score, "compare": compare}[sys.argv[1]]()
