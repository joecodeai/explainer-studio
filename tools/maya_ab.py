"""Maya voice A/B: the same lines, four ways, each paired with Ryan's approved test lines.
  A  current voice (Chatterbox, her reference) with natural default settings
  B  current voice cloned by Qwen3-TTS Base (same identity, other engine)
  C  Qwen3 CustomVoice preset 'Serena' + per-line acting direction (the engine that fixed Ryan)
  D  Qwen3 CustomVoice preset 'Vivian' + per-line acting direction
Output: projects/gta6-voice-test/maya_ab/MAYA_<X>.wav
"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf, librosa
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT); os.chdir(ROOT)
from studio import voice

OUT = "projects/gta6-voice-test/maya_ab"
LINES = "projects/gta6-voice-test/audio/lines"
BASE = ("A woman in her late twenties, smooth, mellow and natural, relaxed conversational pace, like a real actress in an understated "
        "workplace sitcom; she is dry and quietly amused, never performs a joke, never an announcer.")
DIR = {"distracted": "Half-engaged, still reading her book, casual and low-key.",
       "curious": "Genuinely curious, a pinch of disbelief, processing what she heard, not mocking.",
       "dry": "Dry and matter-of-fact, treating something absurd as ordinary, a faint warmth underneath.",
       "deadpan": "Completely flat and indifferent, no smile in the voice, calm and quiet."}
# (ryan line key or None, maya text, maya style)
SEQ = [("266dd3e75f", "You have annual leave.", "distracted"),
       ("f82a331f3c", "And tomorrow?", "curious"),
       ("7a05f276c3", "You're not ill.", "dry"),
       ("8e6d0aa3c4", "You're planning to develop a medical condition.", "curious"),
       ("6e027995ee", "Let me know what you come down with.", "dry"),
       (None, "September. I booked it the day they announced the date.", "dry"),
       ("d86634d7c5", "No. That's for when you're ill.", "dry"),
       ("ddc5065b77", "There's still time.", "deadpan")]


def post(w, sr, f):
    raw = f + ".raw.wav"; sf.write(raw, voice._trim(np.asarray(w, np.float32), sr), sr); voice._clean(raw, f); os.remove(raw)


def main():
    os.makedirs(OUT, exist_ok=True)
    texts = [m for _, m, _ in SEQ]
    # A: Chatterbox, her reference, natural defaults (neutral style = exaggeration 0.5, cfg 0.5)
    jobs = [{"text": t, "ref": "library/voices/maya/reference.wav", "emotion": "neutral", "out": f"{OUT}/A_{i}.cb.wav"} for i, t in enumerate(texts)]
    jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(jobs, jf); jf.close()
    subprocess.run([".venv-tts/bin/python", "studio/tts_cb.py", jf.name], check=True)
    for i in range(len(texts)):
        w, sr = sf.read(f"{OUT}/A_{i}.cb.wav", dtype="float32"); post(w, sr, f"{OUT}/A_{i}.wav")
    import torch
    from qwen_tts import Qwen3TTSModel
    # B: Qwen Base clone of her reference
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0", dtype=torch.bfloat16)
    prompt = m.create_voice_clone_prompt(ref_audio="library/voices/maya/reference.wav", ref_text=open("library/voices/maya/reference.txt").read())
    torch.manual_seed(7)
    wavs, sr = m.generate_voice_clone(text=texts, language=["English"] * len(texts), voice_clone_prompt=prompt * len(texts))
    for i, w in enumerate(wavs): post(w, sr, f"{OUT}/B_{i}.wav")
    del m; torch.cuda.empty_cache()
    # C / D: CustomVoice presets with acting direction
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0", dtype=torch.bfloat16)
    for X, spk in (("C", "Serena"), ("D", "Vivian")):
        for i, (_, t, st) in enumerate(SEQ):
            torch.manual_seed(11 + i)
            w, sr = m.generate_custom_voice(text=t, language="English", speaker=spk, instruct=BASE + " " + DIR[st])
            post(w[0], sr, f"{OUT}/{X}_{i}.wav")
    del m; torch.cuda.empty_cache()
    # assemble: Ryan line, gap, Maya line ...
    for X in "ABCD":
        parts = []
        for i, (rk, _, _) in enumerate(SEQ):
            if rk:
                a, sr = sf.read(f"{LINES}/{rk}.wav", dtype="float32"); parts += [a, np.zeros(int(sr * 0.3), np.float32)]
            a, sr = sf.read(f"{OUT}/{X}_{i}.wav", dtype="float32"); parts += [a, np.zeros(int(sr * 0.6), np.float32)]
        sf.write(f"{OUT}/MAYA_{X}.wav", np.concatenate(parts), 48000)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/MAYA_{X}.wav", "-c:a", "libmp3lame", "-b:a", "160k", f"{OUT}/MAYA_{X}.mp3"], check=True)
        print("made", X)


if __name__ == "__main__":
    main()
