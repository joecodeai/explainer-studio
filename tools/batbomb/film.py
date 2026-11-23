"""Bat-bomb full YouTube film (16:9, ~12 min). Shot list: tools/batbomb/film_shots.py. Everything is cached per file.

  export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1; P=.venv/bin/python
  $P tools/batbomb/film.py voice            # every narration line (locked cloned voices) -> timeline.json
  $P tools/batbomb/film.py refs             # sheets for the new characters
  $P tools/batbomb/film.py kf [ids|prefix]  # one keyframe per shot (keyframes/<id>.png); delete one to redo it
  $P tools/batbomb/film.py anim [ids|prefix] [seed]   # LTX shots then H3 shots
  $P tools/batbomb/film.py sheets [prefix]  # 8-frame review strips per clip
  $P tools/batbomb/film.py mix              # natural-sound mix, subtitles, -> BATBOMB_FILM.mp4
Clip choice per shot: pick.json {id: filename} (defaults to the newest clip of the shot).
"""
import glob, hashlib, json, os, random, re, shutil, subprocess, sys, wave
import numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "tools")); sys.path.insert(0, os.path.dirname(__file__)); os.chdir(ROOT)
from studio import comfy, h3, imagegen, voice, script, workflows as W
from studio.hero import NEG
from film_shots import S, LOCK
import batbomb_voice_test as VT

OUT = "projects/batbomb-film"
TEST, SHORT = "projects/batbomb-animtest", "projects/batbomb-short"
VW, VH = 1920, 1080
GAP, HEAD, TAIL = 0.3, 0.5, 0.0
STYLE = ("2D hand-drawn animated feature film still, cel-shaded characters with clean confident ink outlines and soft painted shading, "
         "richly detailed painterly backgrounds with depth and atmospheric perspective, cinematic lighting, warm 1940s American period detail, "
         "slightly exaggerated expressive cartoon proportions, high production value animated movie look. "
         "Absolutely no text, letters, numbers or logos anywhere.")
LOOK = ("2D hand-drawn animated feature film, cel-shaded characters with clean ink outlines, painted backgrounds, "
        "smooth fluid professional character animation with weight, anticipation and follow-through, cinematic camera.")
REFS = {"fieser": f"{TEST}/refs/fieser.png", "bat": f"{TEST}/refs/bat.png", "adams": f"{TEST}/refs/adams.png", "rancher": f"{TEST}/refs/rancher.png",
        "fdr": f"{SHORT}/refs/fdr.png", "ryan": "library/show_refs/benny_front.png", "ryan_face": "library/show_refs/benny_face.png"}
for c in ("epler", "couffer", "commander", "dehaven", "king", "eleanor"): REFS[c] = f"{OUT}/refs/{c}.png"
NEW_CHARS = {
 "epler": "Lieutenant Colonel R. Bruce Epler, US Army Chemical Warfare Service officer in 1943: stern square-jawed man in his forties, short dark hair, khaki officer's uniform with tie and garrison cap, holding a clipboard.",
 "couffer": "Jack Couffer, a 17-year-old junior bat scientist in 1942: lanky, messy light-brown hair, freckles, eager bright eyes, white shirt with rolled-up sleeves, khaki trousers, canvas satchel over one shoulder.",
 "commander": "a 1943 US Army base commander, a full colonel: broad-shouldered red-faced man in his fifties, grey moustache, khaki uniform, peaked officer's cap.",
 "dehaven": "a 1943 US Marine Corps general: lean grey-haired man in his fifties with sharp features, green Marine service uniform with general's stars.",
 "king": "Fleet Admiral Ernest King in 1944, stylised and respectful: stern lean bald-headed man in his sixties, thin lips, dark blue US Navy uniform with many gold sleeve stripes.",
 "eleanor": "Eleanor Roosevelt in the 1930s, stylised and respectful: tall dignified woman in her forties, warm smile, wavy brown hair, cloche hat, long coat.",
}
REUSE_SFX = {"t2_fieser_h3": "hot desert wind, film camera whirring, a small glass syringe click", "t5_rancher_h3": "porch boards creaking, wind"}
M, R = "maya", "benny"


def lines():
    sec = VT.sections()
    return {(int(k), i): ln for k, v in sec.items() for i, ln in enumerate(v)}


def lid(line): return f"L{line[0]}_{line[1]:02d}"


# ---------------------------------------------------------------- voice + timeline
def do_voice():
    L = lines()
    used = []
    for s in S:
        if s["line"] and s["line"] not in used: used.append(tuple(s["line"]))
    scenes = [{"id": lid(k), "lines": [L[k]]} for k in used]
    sh = script.load_show()
    chars = [{k: c[k] for k in ("id", "name", "look", "voice") if k in c} | ({"tts": c["tts"]} if c.get("tts") else {}) for c in sh["cast"]]
    os.makedirs(f"{OUT}/audio", exist_ok=True)
    json.dump(scenes, open(f"{OUT}/lines.json", "w"), indent=1)
    voice.narrate({"characters": chars, "narrator_voice": sh.get("narrator"), "scenes": scenes}, f"{OUT}/audio")
    timeline()


def timeline():
    """Shot start/duration: a line's shots share the line's time by weight; silent beats have fixed length."""
    t, tl, i = HEAD, [], 0
    while i < len(S):
        s = S[i]
        if s["line"]:
            grp = [x for x in S[i:] if x["line"] == s["line"]]
            grp = grp[: next((k for k, x in enumerate(S[i:]) if x["line"] != s["line"]), len(grp))]
            d = sf.info(f"{OUT}/audio/{lid(s['line'])}.wav").duration
            span = d + GAP; wsum = sum(x["w"] for x in grp); tt = t
            for x in grp:
                sd = span * x["w"] / wsum
                tl.append({"id": x["id"], "start": round(tt, 3), "dur": round(sd, 3), "line": lid(s["line"]), "line_start": round(t, 3)}); tt += sd
            t += span; i += len(grp)
        else:
            tl.append({"id": s["id"], "start": round(t, 3), "dur": s["beat"], "line": None}); t += s["beat"]; i += 1
    json.dump(tl, open(f"{OUT}/timeline.json", "w"), indent=1)
    print("shots %d, runtime %d:%02d" % (len(tl), *divmod(int(t + TAIL), 60)))


# ---------------------------------------------------------------- refs + keyframes
def do_refs():
    os.makedirs(f"{OUT}/refs", exist_ok=True); comfy.start()
    for c, desc in NEW_CHARS.items():
        p = f"{OUT}/refs/{c}.png"
        if os.path.exists(p): continue
        got = imagegen.t2i(f"{STYLE} Character model sheet on a plain flat light grey background: the SAME character shown full body three times "
                           f"(front, three-quarter, side) plus a large head close-up. Consistent design in every view. The character: {desc}",
                           f"{OUT}/refs", c, 1344, 768, seed=101)
        shutil.move(got, p); print("ref", p, flush=True)
    comfy.free()


def sel(arg):
    if not arg: return S
    keys = arg.split(",")
    return [s for s in S if any(s["id"] == k or (len(k) <= 2 and s["id"].startswith(k)) for k in keys)]


ENV_STYLE = ("2D hand-drawn animated feature film background painting, painterly, richly detailed, atmospheric perspective, cinematic lighting, "
             "1940s American period detail. Show only what the description names: add no extra vehicles, no extra animals, no extra objects. Absolutely no text, letters, numbers or logos anywhere.")
NO_PEOPLE = " There are absolutely no people in this image: no humans, no faces, no figures, no silhouettes of people anywhere."
ENV_SHOTS = {"e01", "a05", "a07", "a10", "c02", "c06", "c10", "c11", "c12", "e08", "e10", "f01", "f12", "g06", "g08", "g09", "g15", "g18", "g20", "g21",
             "h05", "h06", "h13", "h15", "h19", "i01", "i02", "i06", "d07", "d19", "c03", "c07", "a04", "g05"}
ONCE = (" The reference images are model sheets that show ONE person from several angles: draw each named person exactly ONCE, "
        "never repeat or clone a character, no extra copies.")


ABSTRACT = {"i01", "i02"}


def kprompt(s):
    if s["id"] in ABSTRACT:
        return ("Minimal abstract image, 16:9: a pure black background with glowing orange embers and sparks floating in the darkness. "
                "Nothing else at all: no objects, no vehicles, no buildings, no people, no landscape, no text.")
    if s["id"] in ENV_SHOTS:
        return f"{ENV_STYLE} 16:9 cinematic film frame. " + s["kf"].format(**LOCK) + NO_PEOPLE
    return f"{STYLE} 16:9 cinematic film frame. " + s["kf"].format(**LOCK) + (ONCE if s["refs"] else "")


def ref_view(path):
    """Model sheets (3 full-body views + head) -> crop to the front full-body view + the head close-up, so the editor has one person to copy."""
    from PIL import Image
    out = os.path.join(OUT, "refs", "crop_" + os.path.basename(path))
    if os.path.exists(out): return out
    im = Image.open(path).convert("RGB"); w, h = im.size
    if w < h * 1.3: return path                                   # not a landscape sheet (e.g. Ryan's single-view refs)
    front = im.crop((0, 0, int(w * 0.25), h))                   # ONE full-body front view only: nothing to duplicate
    os.makedirs(os.path.dirname(out), exist_ok=True); front.save(out); return out


def do_kf(arg=""):
    os.makedirs(f"{OUT}/keyframes", exist_ok=True); comfy.start()
    for s in sel(arg):
        if s["eng"] in ("reuse", "card"): continue
        p = f"{OUT}/keyframes/{s['id']}.png"
        if os.path.exists(p): continue
        rp = [ref_view(REFS[r]) for r in s["refs"]]
        seed = 501 + int(hashlib.md5(s["kf"].encode()).hexdigest()[:4], 16) % 1000
        got = (imagegen.edit(kprompt(s), rp, f"{OUT}/keyframes", s["id"], 1344, 768, seed=seed, fixed_size=True) if rp
               else imagegen.t2i(kprompt(s), f"{OUT}/keyframes", s["id"], 1344, 768, seed=seed))
        shutil.move(got, p); print("kf", p, flush=True)
    comfy.free()


# ---------------------------------------------------------------- animation
def silent(path, seconds):
    if not os.path.exists(path):
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\x00\x00" * int(24000 * seconds))
    return path


def ltx(image, prompt, out, seconds, seed):
    api = W.load("ltx_i2v"); n = lambda i: f"398:{i}"
    api[n(364)]["inputs"]["text"] = f"{prompt} {LOOK} Natural realistic ambient sound of the scene, no music, no speech."
    api[n(373)]["inputs"]["text"] = NEG + ", morphing, warping, melting, sliding feet, frozen still image, slideshow, music"
    api[n(362)]["inputs"]["value"] = int(seconds); api[n(361)]["inputs"]["value"] = 24
    api[n(372)]["inputs"]["value"] = 1280; api[n(360)]["inputs"]["value"] = 704
    api[n(366)]["inputs"]["batch_size"] = 1
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(339)]["inputs"]["noise_seed"] = seed; api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    got = comfy.run(W.prune(api), f"{OUT}/clips", os.path.basename(out)[:-4], timeout=1800)[0]
    shutil.move(got, out)


def people_rule(s):
    n = s.get("n") or 0
    return f" Exactly {n} {'person' if n == 1 else 'people'} in the shot, nobody else appears; everyone keeps the same face, hair and clothes." if n else ""


def do_anim(arg="", seed=31):
    os.makedirs(f"{OUT}/clips", exist_ok=True)
    tl = {x["id"]: x for x in json.load(open(f"{OUT}/timeline.json"))}
    jobs = [s for s in sel(arg) if s["eng"] in ("ltx", "h3")]
    for s in sorted(jobs, key=lambda s: s["eng"] != "ltx"):
        out = f"{OUT}/clips/{s['id']}_{s['eng']}_s{seed}.mp4"
        if os.path.exists(out): continue
        kf = f"{OUT}/keyframes/{s['id']}.png"
        if not os.path.exists(kf): print("no keyframe", s["id"]); continue
        secs = max(5, int(np.ceil(tl[s["id"]]["dur"] + 0.8)))
        mv = s["mv"].format(**LOCK) + people_rule(s)
        try:
            if s["eng"] == "ltx":
                ltx(kf, mv, out, min(secs, 10), seed)
            else:
                comfy.free()
                talk = s["line"] and lines()[tuple(s["line"])]["speaker"] == R
                audio = f"{OUT}/audio/{lid(s['line'])}.wav" if talk else silent(f"{OUT}/silent_{secs}.wav", secs)
                r = h3.render(out, keyframe=kf, refs=[REFS[x] for x in s["refs"]], audio=audio, prompt=f"{mv} {LOOK}",
                              size=(1344, 768), seconds=secs, seed=seed, mode="flex", anchor_audio=bool(talk))
                print("h3", s["id"], r, flush=True)
            print("clip", out, flush=True)
        except Exception as e:
            print("FAILED", s["id"], repr(e)[:300], flush=True)
    comfy.free(); h3.free()


def do_sheets(arg=""):
    os.makedirs(f"{OUT}/qc", exist_ok=True)
    for s in sel(arg):
        for f in sorted(glob.glob(f"{OUT}/clips/{s['id']}_*.mp4")):
            o = f"{OUT}/qc/{os.path.basename(f)[:-4]}.jpg"
            if os.path.exists(o): continue
            n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                                    "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip() or 8)
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f, "-vf",
                            f"select='not(mod(n\\,{max(1, n // 6)}))',scale=320:-1,tile=6x1", "-frames:v", "1", o])


# ---------------------------------------------------------------- mix
def sfx(prompt, seconds):
    from studio import config as C
    d = os.path.join(C.SOUND_LIB, "sfx_natural"); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, hashlib.md5(f"{prompt}|{seconds}".encode()).hexdigest()[:12] + ".flac")
    if os.path.exists(out): return out
    api = W.load("sa3_sfx")
    pos = [k for k, v in api.items() if v["class_type"] == "CLIPTextEncode" and isinstance(v["inputs"].get("text"), list)][0]
    api[pos]["inputs"]["text"] = f"{prompt}, realistic field recording, natural ambience, no music, no speech"
    for k in W.find(api, "EmptyLatentAudio"): api[k]["inputs"]["seconds"] = float(seconds)
    for k in W.find(api, "KSampler"): api[k]["inputs"]["seed"] = random.randint(0, 2**31)
    for k in W.find(api, "SaveAudioAdvanced"): api[k]["inputs"]["format"] = "flac"
    p = comfy.run(W.prune(api), d, "tmp")[0]; os.replace(p, out); return out


def load(path, sr=48000):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def db(x): return 10 ** (x / 20)


def clip_for(s, pick):
    if s["eng"] == "reuse": return s["reuse"]
    if s["id"] in pick: return f"{OUT}/clips/{pick[s['id']]}"
    c = sorted(glob.glob(f"{OUT}/clips/{s['id']}_*.mp4"), key=os.path.getmtime)
    return c[-1] if c else None


def srt(tl):
    """One subtitle block per ~12 words, timed by word share within each spoken line."""
    L = lines(); out = []; seen = set()
    def ts(t): h, m = divmod(t, 3600); m, s = divmod(m, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    for x in tl:
        if not x["line"] or x["line"] in seen: continue
        seen.add(x["line"])
        sec, idx = int(x["line"][1:].split("_")[0]), int(x["line"].split("_")[1])
        text = L[(sec, idx)]["text"]; d = sf.info(f"{OUT}/audio/{x['line']}.wav").duration
        words = text.split(); chunks = [words[i:i + 12] for i in range(0, len(words), 12)]; t = x["line_start"]
        for c in chunks:
            cd = d * len(c) / len(words); out.append((t, t + cd, " ".join(c))); t += cd
    return "\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(out))


def do_mix():
    tl = json.load(open(f"{OUT}/timeline.json")); byid = {s["id"]: s for s in S}
    pick = json.load(open(f"{OUT}/pick.json")) if os.path.exists(f"{OUT}/pick.json") else {}
    total = tl[-1]["start"] + tl[-1]["dur"] + TAIL; sr = 48000; n = int(total * sr)
    speech, amb = np.zeros(n, np.float32), np.zeros(n, np.float32)
    for line in {x["line"] for x in tl if x["line"]}:
        st = next(x["line_start"] for x in tl if x["line"] == line)
        a = load(f"{OUT}/audio/{line}.wav"); i0 = int(st * sr); speech[i0:i0 + len(a)] += a[: n - i0]
    comfy.start(); os.makedirs(f"{OUT}/seg", exist_ok=True); lst = []
    for k, x in enumerate(tl):
        s = byid[x["id"]]; d = x["dur"]; a0 = int(x["start"] * sr); o = f"{OUT}/seg/{k:03d}.mp4"
        if s["eng"] == "card":
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s={VW}x{VH}:r=24:d={d}", "-vf",
                            f"drawtext=fontfile=studio/fonts_reel/Montserrat-ExtraBold.ttf:text='{s['kf']}':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2:"
                            f"alpha='if(lt(t,0.6),t/0.6,if(gt(t,{d - 0.6}),({d}-t)/0.6,1))'", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
            src = load(sfx(s["sfx"], 3)); lvl = -18
        else:
            clip = clip_for(s, pick)
            if not clip: raise SystemExit(f"no clip for {s['id']}")
            h3like = "_h3" in os.path.basename(clip); skip = 0.125 if h3like else 0.0
            cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout)
            pad = max(0.0, d - (cd - skip))
            if pad > 0.05: print(f"WARN {s['id']}: clip {cd:.1f}s < shot {d:.1f}s, holding last frame {pad:.1f}s")
            vf = f"scale={VW}:{VH}:force_original_aspect_ratio=increase:flags=lanczos,crop={VW}:{VH},fps=24" + (f",tpad=stop_mode=clone:stop_duration={pad:.3f}" if pad > 0 else "")
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(skip), "-i", clip, "-t", f"{d:.3f}", "-an", "-vf", vf,
                            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
            if h3like:
                key = next((k for k in REUSE_SFX if k in clip), None)
                talk = s["line"] and lines()[tuple(s["line"])]["speaker"] == R
                prompt = s["sfx"] or (REUSE_SFX[key] if key else "") or ("quiet small apartment room tone" if (talk or "ryan" in s["refs"]) else "soft outdoor wind")
                src = load(sfx(prompt, int(np.ceil(d)) + 1)); lvl = -32 if "ryan" in s["refs"] else -24
            else:
                src = load(clip); lvl = -20
        src = src[: int(d * sr)]
        if len(src):
            fade = min(len(src) // 2, int(0.25 * sr)); env = np.ones(len(src), np.float32)
            if fade: env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
            gain = min(db(lvl) / (np.abs(src).max() + 1e-6), 3.0)
            amb[a0:a0 + len(src)] += (src * env * gain)[: n - a0]
        lst.append(f"file '{os.path.abspath(o)}'")
    comfy.free()
    sf.write(f"{OUT}/mix.wav", np.clip(speech + amb, -1, 1), sr)
    open(f"{OUT}/seg/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/seg/list.txt", "-c", "copy", f"{OUT}/picture.mp4"], check=True)
    open(f"{OUT}/subtitles.srt", "w").write(srt(tl))
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"{OUT}/picture.mp4", "-i", f"{OUT}/mix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", f"{OUT}/BATBOMB_FILM.mp4"], check=True)
    print("done", f"{OUT}/BATBOMB_FILM.mp4", "%d:%02d" % divmod(int(total), 60))


if __name__ == "__main__":
    st = sys.argv[1]; arg = sys.argv[2] if len(sys.argv) > 2 else ""
    {"voice": do_voice, "timeline": timeline, "refs": do_refs, "kf": lambda: do_kf(arg), "sheets": lambda: do_sheets(arg), "mix": do_mix,
     "anim": lambda: do_anim(arg, int(sys.argv[3]) if len(sys.argv) > 3 else 31)}[st]()
