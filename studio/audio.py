"""Sound: SFX (Stable Audio 3) and music beds (ACE-Step 1.5), both cached in the library; final mix with ducking."""
import hashlib, json, os, random, subprocess
import soundfile as sf
from . import config as C, comfy, workflows as W

MOODS = {
    "tense": ("dark tense cinematic underscore, low pulsing synth bass, ticking percussion, suspense, instrumental", 96, "D minor"),
    "upbeat": ("playful upbeat explainer background music, pizzicato strings, light marimba, claps, cheerful, instrumental", 118, "C major"),
    "sad": ("soft melancholic piano with warm strings, slow and gentle, instrumental", 72, "A minor"),
    "epic": ("epic orchestral build, big drums, brass hits, heroic, instrumental", 110, "E minor"),
    "comedic": ("quirky comedic background music, bassoon, pizzicato, wood blocks, cartoonish, instrumental", 124, "F major"),
    "mysterious": ("mysterious ambient underscore, airy pads, music box, curious, instrumental", 90, "B minor"),
}


def _key(*parts):
    return hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:10]


def _save_fmt(api):
    for k in W.find(api, "SaveAudioAdvanced"):
        api[k]["inputs"]["format"] = "flac"


def sfx(prompt, seconds=2.5):
    d = os.path.join(C.SOUND_LIB, "sfx"); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, f"{_key(prompt.lower().strip(), seconds)}.flac")
    if os.path.exists(out): return out
    api = W.load("sa3_sfx")
    pos = [k for k, v in api.items() if v["class_type"] == "CLIPTextEncode" and isinstance(v["inputs"].get("text"), list)][0]
    api[pos]["inputs"]["text"] = f"{prompt}, cartoon sound effect, clean, isolated, no music"
    for k in W.find(api, "EmptyLatentAudio"): api[k]["inputs"]["seconds"] = float(seconds)
    for k in W.find(api, "KSampler"): api[k]["inputs"]["seed"] = random.randint(0, 2**31)
    _save_fmt(api)
    p = comfy.run(W.prune(api), d, "tmp")[0]
    os.replace(p, out); json.dump({"prompt": prompt, "seconds": seconds}, open(out + ".json", "w"))
    return out


def music(mood, seconds):
    d = os.path.join(C.SOUND_LIB, "music"); os.makedirs(d, exist_ok=True)
    seconds = int(min(240, max(30, seconds)))
    tags, bpm, key = MOODS.get(mood, MOODS["upbeat"])
    out = os.path.join(d, f"{mood}_{seconds}_{_key(tags, seconds)}.flac")
    if os.path.exists(out): return out
    api = W.load("ace_music")
    enc = W.find(api, "TextEncodeAceStepAudio1.5")[0]
    api[enc]["inputs"].update(tags=tags, lyrics="[Instrumental]", bpm=bpm, duration=seconds, keyscale=key, timesignature="4",
                              language="en", seed=random.randint(0, 2**31))
    for k in W.find(api, "EmptyAceStep1.5LatentAudio"): api[k]["inputs"]["seconds"] = seconds
    for k in W.find(api, "KSampler"): api[k]["inputs"]["seed"] = random.randint(0, 2**31)
    _save_fmt(api)
    p = comfy.run(W.prune(api), d, "tmp")[0]
    os.replace(p, out)
    return out


def mix(timeline, total, out_wav):
    """timeline: list of {file, start, gain_db, kind: narration|sfx|ambience|music, dur?}. Music & ambience loop to `dur`;
    music is ducked under dialogue (sidechain). Output 48 kHz stereo, -14 LUFS, true peak -1.5 dB."""
    ins, filt, nar, fx, mus = [], [], [], [], []
    for i, t in enumerate(timeline):
        if t["kind"] in ("music", "ambience"):
            ins += ["-stream_loop", "-1"]
        ins += ["-i", t["file"]]
        lbl = f"a{i}"
        f = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={t.get('gain_db', 0)}dB"
        if t["kind"] in ("music", "ambience"):
            d = max(1.0, t["dur"]); fi = 1.5 if t["kind"] == "music" else 0.4
            f += f",atrim=0:{d:.3f},afade=t=in:d={fi},afade=t=out:st={max(0, d - fi - 0.5):.3f}:d={fi + 0.5}"
        f += f",adelay={int(t['start'] * 1000)}|{int(t['start'] * 1000)}[{lbl}]"
        filt.append(f)
        {"narration": nar, "music": mus}.get(t["kind"], fx).append(lbl)
    filt.append("".join(f"[{l}]" for l in nar) + f"amix=inputs={len(nar)}:normalize=0,apad=whole_dur={total}[nar]")
    filt.append("[nar]asplit=2[narout][narkey]" if mus else "[nar]anull[narout]")
    if mus:
        filt.append("".join(f"[{l}]" for l in mus) + f"amix=inputs={len(mus)}:normalize=0,apad=whole_dur={total}[mus]")
        filt.append("[mus][narkey]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350:makeup=1[duck]")
    final = ["[narout]"] + (["[duck]"] if mus else []) + [f"[{l}]" for l in fx]
    filt.append("".join(final) + f"amix=inputs={len(final)}:normalize=0,atrim=0:{total},"
                "alimiter=limit=0.89:level=false,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
    script = out_wav + ".filter.txt"; open(script, "w").write(";".join(filt))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex_script", script, "-map", "[out]", "-ar", "48000", out_wav]
    subprocess.run(cmd, check=True)
    return out_wav
