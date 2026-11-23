"""Chatterbox TTS worker with a "voice director" (runs in .venv-tts, separate from the main venv).

Identity: every line of a character is cloned from that character's ONE reference recording, so the voice never changes.
Emotion only changes delivery (exaggeration / pacing). Each line is recorded in several takes and the best is kept:
  1. same voice   — speaker-embedding similarity to the reference (drops takes that drift)
  2. right words  — ASR word error rate (drops takes with mumbles, skipped or invented words)
  3. right acting — pitch movement that fits the emotion (lively for excited/surprised, controlled for sarcastic, ...)

  .venv-tts/bin/python studio/tts_cb.py jobs.json      # jobs: [{text, ref, emotion, out, takes?}]
"""
import hashlib, json, re, sys

# word check: the larger model catches near-misses small.en lets through (e.g. "flu" heard as "blue")
ASR_MODEL = "distil-large-v3"

# emotion -> (exaggeration, cfg_weight, target pitch movement in semitones (std), or None = "as lively as possible")
STYLE = {"neutral": (0.5, 0.5, 2.6), "confident": (0.6, 0.45, 3.0), "happy": (0.75, 0.4, None), "excited": (0.95, 0.3, None),
         "surprised": (0.9, 0.35, None), "confused": (0.6, 0.4, 3.4), "worried": (0.65, 0.4, 3.0), "sad": (0.45, 0.5, 2.0),
         "angry": (0.8, 0.35, None), "sarcastic": (0.45, 0.5, 2.4),
         # performance styles (script field "voice"): understated sitcom delivery, flatter pitch, no performed punchlines
         "deadpan": (0.3, 0.55, 1.6), "dry": (0.38, 0.5, 2.0), "amused": (0.5, 0.45, 2.5), "curious": (0.5, 0.45, 3.0),
         "awkward": (0.5, 0.45, 2.8), "professional": (0.42, 0.5, 2.2), "concerned": (0.5, 0.45, 2.6), "tired": (0.32, 0.55, 1.7),
         "distracted": (0.35, 0.5, 1.9)}


NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
           "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion and point "
           "percent".split())


def _norm(t):
    """Words for the error check; numbers are dropped on both sides (the ASR writes '159,000' where the script says
    'a hundred and fifty-nine thousand')."""
    t = re.sub(r"\ba (?=(hundred|thousand|million|billion|trillion)\b)", "", t.lower().replace("-", " "))
    w = re.sub(r"[^a-z0-9 ]+", " ", t.replace("'", "")).split()      # "it's" == "its"
    return [x for x in w if x not in NUMW and not re.search(r"\d", x)]


def _wer(ref, hyp):
    r, h = _norm(ref), _norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(1, len(r))


def _pitch_std(w, sr):
    import librosa, numpy as np
    f0 = librosa.yin(w, fmin=70, fmax=400, sr=sr, frame_length=1024)
    e = librosa.feature.rms(y=w, frame_length=1024, hop_length=256)[0][:len(f0)]
    f0 = f0[: len(e)][e > 0.25 * e.max()]                      # voiced, not breath
    if len(f0) < 5: return 0.0
    st = 12 * np.log2(f0 / np.median(f0))
    return float(np.std(np.clip(st, -12, 12)))


RATE = (1.8, 4.6)          # raw-take words/second (pauses excluded), before the pipeline evens tempo (up to -13%): only clearly rushed/dragging takes lose


def _rate(text, w16):
    import numpy as np, librosa
    e = librosa.feature.rms(y=w16, frame_length=400, hop_length=160)[0]
    quiet = e < 0.05 * np.percentile(e, 95)
    pause = run = 0
    for q in list(quiet) + [False]:
        if q: run += 1
        else:
            if run >= 12: pause += run
            run = 0
    return len(text.split()) / max(0.3, len(e) * 0.01 - pause * 0.01)


def main(path):
    import numpy as np, torch, soundfile as sf, librosa
    from chatterbox.tts import ChatterboxTTS
    from faster_whisper import WhisperModel
    jobs = json.load(open(path))
    m = ChatterboxTTS.from_pretrained(device="cuda")
    asr = WhisperModel(ASR_MODEL, device="cuda", compute_type="float16")
    ref_emb = {}
    for j in jobs:
        ex, cfg, target = STYLE.get(j.get("emotion", "neutral"), STYLE["neutral"])
        if j["ref"] not in ref_emb:
            r, rsr = librosa.load(j["ref"], sr=16000)
            ref_emb[j["ref"]] = m.ve.embeds_from_wavs([r], sample_rate=16000)[0]
        takes = []
        base = int(hashlib.md5((j["ref"] + j["text"]).encode()).hexdigest()[:8], 16)
        n = int(j.get("takes", 3)); plan = [(k, cfg) for k in range(n)]
        while plan:
            k, c = plan.pop(0)
            torch.manual_seed(base + 7919 * k)
            w = m.generate(j["text"], audio_prompt_path=j["ref"], exaggeration=ex, cfg_weight=c).squeeze(0).cpu().numpy()
            w16 = librosa.resample(w, orig_sr=m.sr, target_sr=16000)
            emb = m.ve.embeds_from_wavs([w16], sample_rate=16000)[0]
            sim = float(np.dot(emb, ref_emb[j["ref"]]) / (np.linalg.norm(emb) * np.linalg.norm(ref_emb[j["ref"]])))
            hyp = " ".join(s.text for s in asr.transcribe(w16, beam_size=3, language="en", initial_prompt=None)[0])
            rate = _rate(j["text"], w16)
            takes.append({"w": w, "sim": sim, "wer": _wer(j["text"], hyp), "pitch": _pitch_std(w, m.sr), "hyp": hyp, "rate": rate,
                          "rate_off": max(0.0, RATE[0] - rate, rate - RATE[1])})
            if not plan and k < n and all(t["rate_off"] >= 0.15 for t in takes):
                # every take rushed (or dragged): 3 more takes with pacing pushed the other way (lower cfg_weight = slower in Chatterbox)
                c2 = max(0.15, cfg - 0.2) if all(t["rate"] > RATE[1] for t in takes) else min(0.8, cfg + 0.2)
                plan = [(n + i, c2) for i in range(3)]
        best_sim = max(t["sim"] for t in takes)
        ok = [t for t in takes if t["wer"] <= 0.1 and t["sim"] >= best_sim - 0.03] or \
             sorted(takes, key=lambda t: (t["wer"], -t["sim"]))[:1]
        ok = [t for t in ok if t["rate_off"] < 0.15] or sorted(ok, key=lambda t: t["rate_off"])[:1]   # natural speaking speed first
        pick = max(ok, key=lambda t: t["pitch"]) if target is None else min(ok, key=lambda t: abs(t["pitch"] - target))
        sf.write(j["out"], pick["w"], m.sr)
        if pick["rate"] > RATE[1]:      # still rushed: slow the whole line evenly (pitch kept) - never insert a pause mid-sentence
            import subprocess, os
            k = max(0.78, (RATE[1] * 0.92) / pick["rate"]); tmp = j["out"] + ".t.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", j["out"], "-af", f"atempo={k:.3f}", tmp], check=True); os.replace(tmp, j["out"])
            print(f"   slowed x{k:.2f} (rate {pick['rate']:.1f})", flush=True)
        print(f"tts {j['out'].rsplit('/', 1)[-1]} [{j.get('emotion')}] " +
              " | ".join(f"sim {t['sim']:.3f} wer {t['wer']:.2f} pitch {t['pitch']:.1f} rate {t['rate']:.1f}{' *' if t is pick else ''}" for t in takes), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
