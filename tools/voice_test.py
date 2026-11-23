"""Voice test: render a handful of key script lines with their delivery tags (voice / pause_after) through the real TTS
pipeline, without touching any project. Output: projects/<out>/audio/<scene>.wav + VOICE_TEST.wav (all scenes, 1.2 s apart).

  python tools/voice_test.py            # GTA6 key lines -> projects/gta6-voice-test
"""
import json, os, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from studio import voice, script

R, M, D, T = "benny", "maya", "dana", "tom"
DANA_TTS = {"engine": "qwen_design", "model": "models/Qwen3-TTS-12Hz-1.7B-VoiceDesign", "base_direction": "",
            "design": "A composed woman in her early forties, low-to-mid pitch, efficient and pleasant, neutral American accent; "
                      "a real, busy team manager, natural and conversational, never theatrical."}
TOM_TTS = {"engine": "qwen_custom", "model": "models/Qwen3-TTS-12Hz-1.7B-CustomVoice", "speaker": "Aiden", "base_direction": ""}


def L(spk, text, v, emotion="neutral", pause=None):
    d = {"speaker": spk, "text": text, "voice": v, "emotion": emotion}
    if pause is not None: d["pause_after"] = pause
    return d


SCENES = [
 {"id": "t1_business_plan", "lines": [
   L(R, "I've been looking into taking tomorrow off.", "rationalising"),
   L(M, "You have annual leave.", "distracted"),
   L(R, "Yes... But that's for holidays.", "rationalising", pause=0.6),
   L(M, "And tomorrow?", "curious"),
   L(R, "Is a medical situation.", "deadpan"),
   L(M, "You're not ill.", "dry"),
   L(R, "Not yet... There's still time.", "deadpan", pause=1.2),
   L(M, "You're planning to develop a medical condition.", "curious"),
   L(R, "I'm exploring my options.", "rationalising", pause=0.8),
   L(M, "Let me know what you come down with.", "dry")]},
 {"id": "t2_the_call", "lines": [
   L(R, "Hi, Dana. It's Ryan. Just wanted to let you know I'm feeling a little under the weather.", "fake_ill"),
   L(D, "Oh no. What is it?", "concerned"),
   L(R, "Flu, I think. Headache. Fatigue... Very sudden.", "fake_ill"),
   L(D, "Great. Actually, could you just send the deck over before you log off? I'll take the client through it at two.", "professional"),
   L(R, "Of course.", "formal"),
   L(D, "And the revised budget.", "professional"),
   L(R, "Naturally.", "formal"),
   L(D, "And the client notes. And if you could update the tracker, that'd be amazing.", "professional"),
   L(R, "I'm beginning to regret being such a good employee.", "under_breath"),
   L(D, "Sorry?", "professional"),
   L(R, "Fever. I'm delirious.", "fake_ill")]},
 {"id": "t3_office_and_ending", "lines": [
   L(R, "Interesting.", "deadpan", pause=1.0),
   L(R, "I've accidentally been promoted by the flu.", "under_breath", pause=1.0),
   L(T, "Yeah, nothing from me, mate.", "distracted"),
   L(R, "Thanks, Tom. Get well soon.", "deadpan", pause=1.2),
   L(M, "September. I booked it the day they announced the date.", "dry"),
   L(R, "It wasn't sick leave.", "deadpan"),
   L(M, "No. That's for when you're ill.", "dry", pause=1.0),
   L(R, "I think I'm coming down with something.", "under_breath", pause=0.5),
   L(M, "There's still time.", "deadpan")]},
]


def main(out="projects/gta6-voice-test"):
    sh = script.load_show()
    chars = [{k: c[k] for k in ("id", "name", "look", "voice") if k in c} | ({"tts": c["tts"]} if c.get("tts") else {}) for c in sh["cast"]]
    chars.append({"id": D, "name": "Dana", "look": "", "voice": DANA_TTS["design"], "tts": DANA_TTS})
    chars.append({"id": T, "name": "Tom", "look": "", "voice": "a man in his thirties", "tts": TOM_TTS})
    sc = {"characters": chars, "narrator_voice": sh.get("narrator"), "scenes": json.loads(json.dumps(SCENES))}
    os.makedirs(f"{out}/audio", exist_ok=True)
    voice.narrate(sc, f"{out}/audio")
    parts = []
    for s in SCENES:
        a, sr = sf.read(f"{out}/audio/{s['id']}.wav", dtype="float32")
        parts += [a, np.zeros(int(sr * 1.2), np.float32)]
    sf.write(f"{out}/VOICE_TEST.wav", np.concatenate(parts), sr)
    print("done", f"{out}/VOICE_TEST.wav")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    main(*sys.argv[1:])
