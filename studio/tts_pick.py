"""Voice director for engines that make takes in the main venv (Qwen3-TTS CustomVoice): runs in .venv-tts.
jobs: [{text, emotion, takes: [wav...], anchor: wav, out: wav}] -> picks the take that keeps the voice identity (similarity to the
character's anchor recording), says every word (ASR), and has pitch movement that fits the emotion."""
import json, sys, numpy as np, librosa, soundfile as sf
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tts_cb as TC


def main(path):
    import torch
    from chatterbox.models.voice_encoder import VoiceEncoder
    from huggingface_hub import hf_hub_download
    from faster_whisper import WhisperModel
    ve = VoiceEncoder(); ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cpu")); ve = ve.to("cuda").eval()
    asr = WhisperModel(TC.ASR_MODEL, device="cuda", compute_type="float16")
    emb = lambda w: (lambda e: e / np.linalg.norm(e))(ve.embeds_from_wavs([w], sample_rate=16000)[0])
    anchors = {}
    for j in json.load(open(path)):
        if j["anchor"] not in anchors: anchors[j["anchor"]] = emb(librosa.load(j["anchor"], sr=16000)[0])
        target = TC.STYLE.get(j.get("emotion", "neutral"), TC.STYLE["neutral"])[2]
        rows = []
        for f in j["takes"]:
            w, sr = librosa.load(f, sr=None); w16 = librosa.resample(w, orig_sr=sr, target_sr=16000)
            hyp = " ".join(s.text for s in asr.transcribe(w16, beam_size=3, language="en")[0])
            e = librosa.feature.rms(y=w16, frame_length=400, hop_length=160)[0]
            quiet = e < 0.05 * np.percentile(e, 95)                 # pauses = quiet runs of >= 0.12 s; everything else is speech
            pause = 0; run = 0
            for qv in list(quiet) + [False]:
                if qv: run += 1
                else:
                    if run >= 12: pause += run
                    run = 0
            speech = max(0.3, len(e) * 0.01 - pause * 0.01)
            rate = len(j["text"].split()) / speech
            lo, hi = j.get("rate", [0, 99])
            rows.append({"f": f, "w": w, "sr": sr, "sim": float(emb(w16) @ anchors[j["anchor"]]), "wer": TC._wer(j["text"], hyp),
                         "pitch": TC._pitch_std(w, sr), "rate": rate, "rate_off": max(0.0, lo - rate, rate - hi)})
        best = max(r["sim"] for r in rows)
        ok = [r for r in rows if r["wer"] <= 0.1 and r["sim"] >= best - 0.04] or sorted(rows, key=lambda r: (r["wer"], -r["sim"]))[:1]
        inrange = [r for r in ok if r["rate_off"] < 0.15]
        ok = inrange or sorted(ok, key=lambda r: r["rate_off"])[:1]                     # natural speaking speed first
        pick = max(ok, key=lambda r: r["pitch"]) if target is None else min(ok, key=lambda r: abs(r["pitch"] - target))
        sf.write(j["out"], pick["w"], pick["sr"])
        lo, hi = j.get("rate", [0, 99])
        if pick["rate"] > hi * 1.03:                 # rushed: slow the whole line evenly (never add a pause mid-sentence)
            import subprocess, os
            k = max(0.78, hi / pick["rate"]); tmp = j["out"] + ".t.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", j["out"], "-af", f"atempo={k:.3f}", tmp], check=True); os.replace(tmp, j["out"])
            print(f"   slowed x{k:.2f} (rate {pick['rate']:.1f} -> {pick['rate'] * k:.1f})", flush=True)
        elif pick["rate"] < lo * 0.97:                 # a little slow: tighten up to 15% (WSOLA, pitch preserved, voice unchanged)
            import subprocess, os
            k = min(1.15, lo / pick["rate"]); tmp = j["out"] + ".t.wav"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", j["out"], "-af", f"atempo={k:.3f}", tmp], check=True); os.replace(tmp, j["out"])
            print(f"   tightened x{k:.2f} (rate {pick['rate']:.1f} -> {pick['rate'] * k:.1f})", flush=True)
        print(f"pick {j['out'].rsplit('/', 1)[-1]} [{j.get('emotion')}] " + " | ".join(
            f"sim {r['sim']:.3f} wer {r['wer']:.2f} pitch {r['pitch']:.1f} rate {r['rate']:.1f}{' *' if r is pick else ''}" for r in rows), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
