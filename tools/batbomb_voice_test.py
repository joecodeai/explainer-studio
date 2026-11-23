"""Bat-bomb film voice test: key narration lines (Maya) and Ryan's cutaways, pulled verbatim from
scripts/BATBOMB_STAGE2_NARRATION.md by section, voiced through the real TTS pipeline with their tags.
Output: projects/batbomb-voice-test/audio/<scene>.wav + VOICE_TEST.wav. Cached per line: delete a line's wav to redo it.

  PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1 .venv/bin/python tools/batbomb_voice_test.py
"""
import json, os, re, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from studio import voice, script

SRC = "scripts/BATBOMB_STAGE2_NARRATION.md"
SPK = {"MAYA": "maya", "RYAN": "benny"}
# (test scene id, section number, line indexes within that section to voice; None = all)
PICK = [("v1_hook", "1", None),
        ("v2_dentist", "2", [3, 4, 5]),
        ("v3_letter", "3", [1, 3, 4, 5]),
        ("v4_team", "4", [0, 1, 6, 7]),
        ("v5_party", "5", [1, 2, 3, 9]),
        ("v6_rancher", "6", [1, 4, 5, 7]),
        ("v7_fire", "7", [2, 3, 6, 7, 8]),
        ("v8_payoff", "8", [5, 6, 7, 8, 9]),
        ("v9_end", "9", [0, 3])]


def sections():
    t = open(SRC).read().split("## Line-by-line fact check")[0]
    out, cur = {}, None
    for line in t.splitlines():
        m = re.match(r"## (\d)", line)
        if m: cur = m.group(1); out[cur] = []
        m = re.match(r"(MAYA|RYAN) \[(\w+)\]: (.*)", line)
        if m and cur: out[cur].append({"speaker": SPK[m.group(1)], "voice": m.group(2), "text": m.group(3).strip(), "emotion": "neutral"})
    return out


def main(out="projects/batbomb-voice-test"):
    sec = sections()
    scenes = []
    for sid, num, idx in PICK:
        lines = sec[num] if idx is None else [sec[num][i] for i in idx]
        scenes.append({"id": sid, "lines": lines})
    sh = script.load_show()
    chars = [{k: c[k] for k in ("id", "name", "look", "voice") if k in c} | ({"tts": c["tts"]} if c.get("tts") else {}) for c in sh["cast"]]
    sc = {"characters": chars, "narrator_voice": sh.get("narrator"), "scenes": json.loads(json.dumps(scenes))}
    os.makedirs(f"{out}/audio", exist_ok=True)
    json.dump(scenes, open(f"{out}/lines.json", "w"), indent=1)
    voice.narrate(sc, f"{out}/audio")
    parts = []
    for s in scenes:
        a, sr = sf.read(f"{out}/audio/{s['id']}.wav", dtype="float32")
        parts += [a, np.zeros(int(sr * 1.5), np.float32)]
    sf.write(f"{out}/VOICE_TEST.wav", np.concatenate(parts), sr)
    print("done", f"{out}/VOICE_TEST.wav")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    main(*sys.argv[1:])
