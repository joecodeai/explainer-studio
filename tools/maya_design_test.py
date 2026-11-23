"""Maya on Ryan's engine family: Qwen3-TTS VoiceDesign (voice from a description) + the same kind of per-line acting
direction Ryan gets. Several takes per line; studio/tts_pick.py keeps the take closest to Maya's current voice (reference.wav)
that says every word at a natural pace. Writes MAYA_H.mp3 / MAYA_I.mp3 (two voice descriptions).
"""
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "tools")); os.chdir(ROOT)
import maya_ab as M

DESC = {
    "H": "A woman in her late twenties with a smooth, mellow, natural voice, mid-low pitch, neutral American accent, easy warmth and a quiet "
         "sense of humour; a real actress in an understated workplace sitcom, conversational, never an announcer.",
    "I": "A woman in her late twenties with a low, warm, slightly husky voice, relaxed and unhurried, neutral American accent, dry and quietly "
         "amused; a real actress in an understated workplace sitcom, natural and conversational, never theatrical.",
}
DIR = {"distracted": "She is half-engaged, still reading her book, casual and low-key.",
       "curious": "She is genuinely curious with a pinch of disbelief, processing what she heard, not mocking.",
       "dry": "She is dry and matter-of-fact, treating something absurd as ordinary, a faint warmth underneath.",
       "deadpan": "Completely flat and indifferent, no smile in the voice, calm and quiet."}
TAKES = 5


def main():
    import torch
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained("models/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cuda:0", dtype=torch.bfloat16)
    jobs = []
    for X, desc in DESC.items():
        for i, (_, t, st) in enumerate(M.SEQ):
            takes = []
            for k in range(TAKES):
                torch.manual_seed(1000 * i + k)
                w, sr = m.generate_voice_design(text=t, language="English", instruct=desc + " " + DIR[st])
                f = f"{M.OUT}/{X}_{i}.take{k}.wav"; sf.write(f, w[0], sr); takes.append(os.path.abspath(f))
            jobs.append({"text": t, "emotion": st, "takes": takes, "anchor": os.path.abspath("library/voices/maya/reference.wav"),
                         "out": os.path.abspath(f"{M.OUT}/{X}_{i}.pick.wav"), "rate": [2.3, 3.4]})
    del m; torch.cuda.empty_cache()
    jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(jobs, jf); jf.close()
    subprocess.run([".venv-tts/bin/python", "studio/tts_pick.py", jf.name], check=True)
    for X in DESC:
        parts = []
        for i, (rk, _, _) in enumerate(M.SEQ):
            w, sr = sf.read(f"{M.OUT}/{X}_{i}.pick.wav", dtype="float32"); M.post(w, sr, f"{M.OUT}/{X}_{i}.wav")
            if rk:
                a, _ = sf.read(f"{M.LINES}/{rk}.wav", dtype="float32"); parts += [a, np.zeros(int(48000 * 0.3), np.float32)]
            a, _ = sf.read(f"{M.OUT}/{X}_{i}.wav", dtype="float32"); parts += [a, np.zeros(int(48000 * 0.6), np.float32)]
        sf.write(f"{M.OUT}/MAYA_{X}.wav", np.concatenate(parts), 48000)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{M.OUT}/MAYA_{X}.wav", "-c:a", "libmp3lame", "-b:a", "160k", f"{M.OUT}/MAYA_{X}.mp3"], check=True)
        print("made", X)


if __name__ == "__main__":
    main()
