"""Design the new recurring voices (Brayden, Gerald, Inner Voice), make A/B/C takes, and clone real script lines from each take.

  P=.venv/bin/python; export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1
  $P tools/voice_cast_design.py design     # VoiceDesign: 3 reference takes per character -> library/voices/<id>/design_take{A,B,C}.wav
  $P tools/voice_cast_design.py samples    # Base clone: script lines from each take -> VIDEOS/.../VOICE SAMPLES/<Name> - take X.wav
  $P tools/voice_cast_design.py maya       # Maya's locked voice on the tricky lines, at normal speed and +10%
  $P tools/voice_cast_design.py lock <id> <A|B|C>   # chosen take becomes library/voices/<id>/ref_locked.wav (+ .txt)
"""
import json, os, shutil, subprocess, sys
import numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
OUT = "VIDEOS/Is Hustle Culture a Scam/VOICE SAMPLES"
CAST = {
 "brayden": dict(name="Brayden",
   design="A man in his late twenties with a loud, bright, energetic American voice, fast and punchy, smiling as he talks, like a fitness "
          "influencer filming himself on his phone at sunrise. Supremely confident and completely sincere, hyped, never sarcastic, never ironic.",
   ref="Good morning, team! It's four a.m. and I've already crushed three goals. Winners don't sleep in. Winners don't even sleep. Let's go!",
   lines=["Good morning. It's four a.m. Right now, you're asleep. That's why you're broke. I've been up since three. I've already had a cold shower, a hot shower, and an argument with a swan.",
          "Team. Let's talk about sleep. Every night, eight hours, gone. No revenue. No content. I'm not paying you to lie there in the dark.",
          "Kidneys. Two of you, doing the same job. That's a redundancy situation.",
          "Still counts."]),
 "gerald": dict(name="Gerald",
   design="A middle-aged British man with a soft, warm, unhurried voice, extremely polite and reassuring, gentle and calm like a hostage "
          "negotiator or a kindly human resources manager. A quiet smile in the voice. He never raises his voice and never sounds angry.",
   ref="Hello. Please, take a seat. Nobody's in trouble. I just want to have a little chat about your availability. One step at a time. That's completely valid.",
   lines=["Hi, Ryan. I'm Gerald, from People and Culture. Nobody's in trouble. I just want to talk.",
          "Put the weekend down, Ryan. Slowly. Nobody has to get hurt.",
          "Weekend Lite gives you Saturday morning, with occasional emails. Weekend Plus adds Sunday, but the Sunday evening dread is billed separately.",
          "And if you'd rather sleep when you're dead, we've partnered with a lovely cemetery. Staff get ten percent off.",
          "Cancellations are done in person. On a Saturday."]),
 "inner": dict(name="Inner Voice",
   design="A breathy, impish whisper very close to the microphone, mischievous and delighted with itself, intimate and slightly unsettling, "
          "like a little devil on your shoulder whispering a terrible idea into your ear. Soft whispering, not shouting.",
   ref="Psst. Hey. Do it. Nobody's looking. Text your ex. Buy the thing. It'll be fine. Probably.",
   lines=["He's good.", "Text your ex. Sell her a candle.", "Breathwork. Ninety-nine dollars."]),
}
TAKES = "ABC"


def design():
    import torch
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cuda:0", dtype=torch.bfloat16)
    for cid, c in CAST.items():
        d = f"library/voices/{cid}"; os.makedirs(d, exist_ok=True)
        for k, t in enumerate(TAKES):
            torch.manual_seed(2026 + 17 * k)
            w, sr = m.generate_voice_design(text=c["ref"], language="English", instruct=c["design"])
            sf.write(f"{d}/design_take{t}.wav", w[0], sr); print("design", cid, t, flush=True)
        json.dump({"name": c["name"], "design": c["design"], "ref_text": c["ref"]}, open(f"{d}/design.json", "w"), indent=1)


def _clone_lines(m, ref_wav, ref_text, lines, seed=7):
    import torch
    cp = m.create_voice_clone_prompt(ref_audio=ref_wav, ref_text=ref_text); out = []
    for i, ln in enumerate(lines):
        torch.manual_seed(seed + i)
        w, sr = m.generate_voice_clone(text=ln, language="English", voice_clone_prompt=cp)
        out.append((w[0].astype(np.float32), sr))
    return out


def _join(parts, path, gap=0.6, tempo=1.0):
    sr = parts[0][1]; z = np.zeros(int(gap * sr), np.float32)
    y = np.concatenate([np.concatenate([a, z]) for a, _ in parts]); y = y / (np.abs(y).max() + 1e-6) * 0.89
    sf.write(path, y, sr)
    if tempo != 1.0:
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", path, "-af", f"atempo={tempo}", path + ".t.wav"], check=True); os.replace(path + ".t.wav", path)


def samples():
    import torch
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0", dtype=torch.bfloat16)
    os.makedirs(OUT, exist_ok=True)
    takes = sys.argv[2] if len(sys.argv) > 2 else TAKES; ids = sys.argv[3].split(",") if len(sys.argv) > 3 else list(CAST)
    for cid, c in CAST.items():
        if cid not in ids: continue
        for t in takes:
            ref = f"library/voices/{cid}/design_take{t}.wav"
            parts = [(sf.read(ref, dtype="float32")[0], sf.read(ref)[1])] + _clone_lines(m, ref, c["ref"], c["lines"])
            _join(parts, f"{OUT}/{c['name']} - take {t}.wav"); print("sample", cid, t, flush=True)


def maya():
    import torch
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0", dtype=torch.bfloat16)
    lines = ["It was selling you this video.", "He fired a kidney.", "Sorry. The actual science.", "Absolutely not.", "Ryan?",
             "I tried it, actually. Day one, I did yoga. Day two, I journaled. On day three, I woke up at five, looked at the ceiling, and said no out loud. To nobody.",
             "It's the most honest I've ever been.", "Filmed at four in the afternoon. The sunrise is a lamp."]
    ref = "library/voices/maya/ref_lively.wav"; txt = open("library/voices/maya/ref_lively.txt").read().strip()
    parts = _clone_lines(m, ref, txt, lines, seed=11); os.makedirs(OUT, exist_ok=True)
    _join(parts, f"{OUT}/Maya - normal speed.wav", gap=0.8)
    _join(parts, f"{OUT}/Maya - 10 percent faster (last videos).wav", gap=0.8, tempo=1.10)
    print("maya done", flush=True)


def lock(cid, take):
    d = f"library/voices/{cid}"; meta = json.load(open(f"{d}/design.json"))
    shutil.copy(f"{d}/design_take{take}.wav", f"{d}/ref_locked.wav"); open(f"{d}/ref_locked.txt", "w").write(meta["ref_text"])
    print("locked", cid, take)


cmd = sys.argv[1]
{"design": design, "samples": samples, "maya": maya}.get(cmd, lambda: lock(sys.argv[2], sys.argv[3]))()
