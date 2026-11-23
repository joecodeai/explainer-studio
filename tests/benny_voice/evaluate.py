import sys, os, json, glob, numpy as np, librosa
sys.path.insert(0, "/home/mundax/Documents/REL/ExplainerStudio/studio")
from chatterbox.models.voice_encoder import VoiceEncoder
from faster_whisper import WhisperModel
import tts_cb as TC
T = sys.argv[1]; lines = json.load(open(f"{T}/script.json"))["lines"]
ve = VoiceEncoder().to("cuda").eval()
from chatterbox.tts import ChatterboxTTS
asr = WhisperModel("small.en", device="cuda", compute_type="float16")
ve_sd = None
try:
    from huggingface_hub import hf_hub_download
    import torch
    ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cuda"))
except Exception as e: print("ve load", e)
res = {}
for d in sorted(glob.glob(f"{T}/*/line0.wav")):
    k = os.path.basename(os.path.dirname(d)); embs, wers, pit, rates = [], [], [], []
    for i, l in enumerate(lines):
        w, sr = librosa.load(f"{T}/{k}/line{i}.wav", sr=16000)
        e = ve.embeds_from_wavs([w], sample_rate=16000)[0]; embs.append(e / np.linalg.norm(e))
        hyp = " ".join(s.text for s in asr.transcribe(w, beam_size=3)[0]); wers.append(TC._wer(l["text"], hyp))
        pit.append(TC._pitch_std(w, 16000)); rates.append(len(l["text"].split()) / (len(w) / 16000))
    E = np.array(embs); c = E.mean(0); c /= np.linalg.norm(c)
    res[k] = {"identity_consistency(min sim to centroid)": round(float((E @ c).min()), 3), "mean_sim": round(float((E @ c).mean()), 3),
              "word_error": round(float(np.mean(wers)), 3), "pitch_movement_mean": round(float(np.mean(pit)), 2),
              "pitch_movement_spread_across_emotions": round(float(np.std(pit)), 2), "pace_spread_words_per_s": round(float(np.std(rates)), 2)}
    print(k, res[k], flush=True)
json.dump(res, open(f"{T}/metrics.json", "w"), indent=1)
