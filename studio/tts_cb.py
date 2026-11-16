"""Chatterbox TTS worker with a "voice director" (runs in .venv-tts, separate from the main venv).

Identity: every line of a character is cloned from that character's ONE reference recording, so the voice never changes.
Emotion only changes delivery (exaggeration / pacing). Each line is recorded in several takes and the best is kept:
  1. same voice   — speaker-embedding similarity to the reference (drops takes that drift)
  2. right words  — ASR word error rate (drops takes with mumbles, skipped or invented words)
  3. right acting — pitch movement that fits the emotion (lively for excited/surprised, controlled for sarcastic, ...)

  .venv-tts/bin/python studio/tts_cb.py jobs.json      # jobs: [{text, ref, emotion, out, takes?}]
"""
import hashlib, json, re, sys

# emotion -> (exaggeration, cfg_weight, target pitch movement in semitones (std), or None = "as lively as possible")
STYLE = {"neutral": (0.5, 0.5, 2.6), "confident": (0.6, 0.45, 3.0), "happy": (0.75, 0.4, None), "excited": (0.95, 0.3, None),
         "surprised": (0.9, 0.35, None), "confused": (0.6, 0.4, 3.4), "worried": (0.65, 0.4, 3.0), "sad": (0.45, 0.5, 2.0),
         "angry": (0.8, 0.35, None), "sarcastic": (0.45, 0.5, 2.4)}


NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
           "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion and point "
           "percent".split())


def _norm(t):
    """Words for the error check; numbers are dropped on both sides (the ASR writes '159,000' where the script says
    'a hundred and fifty-nine thousand')."""
    t = re.sub(r"\ba (?=(hundred|thousand|million|billion|trillion)\b)", "", t.lower().replace("-", " "))
    w = re.sub(r"[^a-z0-9' ]+", " ", t).split()
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


def main(path):
    import numpy as np, torch, soundfile as sf, librosa
    from chatterbox.tts import ChatterboxTTS
    from faster_whisper import WhisperModel
    jobs = json.load(open(path))
    m = ChatterboxTTS.from_pretrained(device="cuda")
    asr = WhisperModel("small.en", device="cuda", compute_type="float16")
    ref_emb = {}
    for j in jobs:
        ex, cfg, target = STYLE.get(j.get("emotion", "neutral"), STYLE["neutral"])
        if j["ref"] not in ref_emb:
            r, rsr = librosa.load(j["ref"], sr=16000)
            ref_emb[j["ref"]] = m.ve.embeds_from_wavs([r], sample_rate=16000)[0]
        takes = []
        base = int(hashlib.md5((j["ref"] + j["text"]).encode()).hexdigest()[:8], 16)
        for k in range(int(j.get("takes", 3))):
            torch.manual_seed(base + 7919 * k)
            w = m.generate(j["text"], audio_prompt_path=j["ref"], exaggeration=ex, cfg_weight=cfg).squeeze(0).cpu().numpy()
            w16 = librosa.resample(w, orig_sr=m.sr, target_sr=16000)
            emb = m.ve.embeds_from_wavs([w16], sample_rate=16000)[0]
            sim = float(np.dot(emb, ref_emb[j["ref"]]) / (np.linalg.norm(emb) * np.linalg.norm(ref_emb[j["ref"]])))
            hyp = " ".join(s.text for s in asr.transcribe(w16, beam_size=3, initial_prompt=None)[0])
            takes.append({"w": w, "sim": sim, "wer": _wer(j["text"], hyp), "pitch": _pitch_std(w, m.sr), "hyp": hyp})
        best_sim = max(t["sim"] for t in takes)
        ok = [t for t in takes if t["wer"] <= 0.1 and t["sim"] >= best_sim - 0.03] or \
             sorted(takes, key=lambda t: (t["wer"], -t["sim"]))[:1]
        pick = max(ok, key=lambda t: t["pitch"]) if target is None else min(ok, key=lambda t: abs(t["pitch"] - target))
        sf.write(j["out"], pick["w"], m.sr)
        print(f"tts {j['out'].rsplit('/', 1)[-1]} [{j.get('emotion')}] " +
              " | ".join(f"sim {t['sim']:.3f} wer {t['wer']:.2f} pitch {t['pitch']:.1f}{' *' if t is pick else ''}" for t in takes), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
