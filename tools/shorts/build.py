"""Story Shorts builder (native 9:16, ~60 s, a complete story per Short). Topic files: tools/shorts/topics/<topic>.py

  export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1; P=.venv/bin/python
  $P tools/shorts/build.py <topic> all                  # voice -> refs -> kf -> anim -> mix
  $P tools/shorts/build.py <topic> voice|refs|kf|anim|mix [ids] [seed]
Everything is cached: delete keyframes/<id>.png or clips/<id>_* to redo one shot. Output: projects/short-<topic>/<TOPIC>_SHORT.mp4
Clip per shot = pick.json {id: file} if present, else the newest clip of the shot.
"""
import glob, hashlib, time, importlib, json, os, random, re, shutil, subprocess, sys, wave
import numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.dirname(__file__)); os.chdir(ROOT)
from studio import comfy, h3, imagegen, voice, script, workflows as W
from studio.hero import NEG

TOPIC = sys.argv[1]
T = importlib.import_module(f"topics.{TOPIC}")
OUT = f"projects/short-{TOPIC}"
W_, H_ = 1080, 1920
GAP, HEAD = getattr(T, "GAP", 0.3), 0.4
TAIL = getattr(T, "TAIL", 3.0)
STYLE = ("2D hand-drawn animated feature film still, cel-shaded characters with clean confident ink outlines and soft painted shading, "
         "richly detailed painterly backgrounds with depth and atmospheric perspective, cinematic lighting, " + T.ERA + ", "
         "slightly exaggerated expressive cartoon proportions, high production value animated movie look. "
         "Absolutely no text, letters, numbers or logos anywhere.")
ENV_STYLE = ("2D hand-drawn animated feature film background painting, painterly, richly detailed, atmospheric perspective, cinematic lighting, "
             + T.ERA + ". Show only what the description names: add no extra vehicles, animals or objects. Absolutely no text, letters, numbers or logos anywhere.")
NO_PEOPLE = " There are absolutely no people in this image: no humans, no faces, no figures anywhere."
ONCE = " The reference images show ONE character each: draw each referenced character exactly ONCE, never duplicate or clone a character."
LOOK = ("2D hand-drawn animated feature film, cel-shaded characters with clean ink outlines, painted backgrounds, "
        "smooth fluid professional character animation with weight, anticipation and follow-through, cinematic camera.")
STYLE = getattr(T, "STYLE", STYLE); ENV_STYLE = getattr(T, "ENV_STYLE", ENV_STYLE); LOOK = getattr(T, "LOOK", LOOK)
LTX_W, LTX_H = getattr(T, "LTX_WH", (704, 1280))        # flat 2D renders at half size and is upscaled in the mix
REFS = {"ryan": "library/show_refs/benny_front.png", "ryan_face": "library/show_refs/benny_face.png"}
REFS.update({c: f"{OUT}/refs/{c}.png" for c in getattr(T, "CHARS", {})})
M, R = "maya", "benny"
SHOTS = T.SHOTS


TEMPO = getattr(T, "TEMPO", 1.0)          # whole-line speed-up (never pauses inside a line)


def wav(s): return f"{OUT}/audio/{s['id']}" + (".t.wav" if TEMPO != 1.0 else ".wav")


# ---------------------------------------------------------------- voice
def do_voice():
    h3.free(); comfy.free()                     # TTS needs the GPU: unload any image/video model first
    sh = script.load_show()
    chars = [{k: c[k] for k in ("id", "name", "look", "voice") if k in c} | ({"tts": c["tts"]} if c.get("tts") else {}) for c in sh["cast"]]
    for c in chars:                                   # topic-level voice reference (same identity, different read), e.g. Maya's lively lock
        if c["id"] in getattr(T, "VOICE_REF", {}): c["tts"] = dict(c["tts"], **T.VOICE_REF[c["id"]])
    scenes = [{"id": s["id"], "lines": [{"speaker": s["spk"], "voice": s.get("tag", "narration"), "text": s["text"], "emotion": "neutral"}]} for s in SHOTS]
    os.makedirs(f"{OUT}/audio", exist_ok=True)
    json.dump(scenes, open(f"{OUT}/lines.json", "w"), indent=1)
    voice.narrate({"characters": chars, "narrator_voice": sh.get("narrator"), "scenes": scenes}, f"{OUT}/audio")
    if TEMPO != 1.0:
        for s in SHOTS:
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"{OUT}/audio/{s['id']}.wav", "-af", f"atempo={TEMPO}", wav(s)], check=True)
    t, tl = HEAD, []
    for s in SHOTS:
        d = sf.info(wav(s)).duration
        tl.append({"id": s["id"], "start": round(t, 3), "dur": round(d, 3)}); t += d + GAP
    json.dump(tl, open(f"{OUT}/timeline.json", "w"), indent=1)
    print("speech total %.1fs, video %.1fs" % (sum(x["dur"] for x in tl), t - GAP + TAIL), flush=True)


# ---------------------------------------------------------------- refs + keyframes
def do_refs():
    os.makedirs(f"{OUT}/refs", exist_ok=True); h3.free(); comfy.start()
    for c, desc in getattr(T, "CHARS", {}).items():
        p = f"{OUT}/refs/{c}.png"
        if os.path.exists(p): continue
        got = imagegen.t2i(f"{STYLE} Character model sheet on a plain flat light grey background: the SAME character shown full body three times "
                           f"(front, three-quarter, side) plus a large head close-up. Consistent design in every view. The character: {desc}",
                           f"{OUT}/refs", c, 1344, 768, seed=101)
        shutil.move(got, p); print("ref", p, flush=True)


def ref_view(path):
    """Landscape model sheet -> its front full-body view only, so the editor has exactly one figure to copy."""
    from PIL import Image
    out = os.path.join(OUT, "refs", "crop_" + os.path.basename(path))
    if os.path.exists(out): return out
    im = Image.open(path).convert("RGB"); w, h = im.size
    if w < h * 1.3: return path
    im.crop((0, 0, int(w * 0.25), h)).save(out); return out


def sel(arg): return [s for s in SHOTS if not arg or s["id"] in arg.split(",")]


def do_kf(arg=""):
    os.makedirs(f"{OUT}/keyframes", exist_ok=True); h3.free(); comfy.start()
    for s in sel(arg):
        if s["eng"] == "card": continue
        p = f"{OUT}/keyframes/{s['id']}.png"
        if os.path.exists(p): continue
        refs = s.get("refs", [])
        if s.get("env"): full = f"{ENV_STYLE} 9:16 vertical cinematic film frame. {s['kf']}{NO_PEOPLE}"
        else: full = f"{STYLE} 9:16 vertical cinematic film frame. {s['kf']}" + (ONCE if refs else "")
        rp = [ref_view(REFS[r]) for r in refs]
        seed = 501 + int(hashlib.md5(s["kf"].encode()).hexdigest()[:4], 16) % 1000
        got = (imagegen.edit(full, rp, f"{OUT}/keyframes", s["id"], 768, 1344, seed=seed, fixed_size=True) if rp
               else imagegen.t2i(full, f"{OUT}/keyframes", s["id"], 768, 1344, seed=seed))
        shutil.move(got, p); print("kf", p, flush=True)


# ---------------------------------------------------------------- animation
def silent(path, seconds):
    if not os.path.exists(path):
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\x00\x00" * int(24000 * seconds))
    return path


def ltx(image, prompt, out, seconds, seed):
    api = W.load("ltx_i2v"); n = lambda i: f"398:{i}"
    api[n(364)]["inputs"]["text"] = f"{prompt} {LOOK} Natural realistic ambient sound of the scene, no music, no speech."
    api[n(373)]["inputs"]["text"] = NEG + ", morphing, warping, melting, sliding feet, frozen still image, slideshow, music, speech, text"
    api[n(362)]["inputs"]["value"] = int(seconds); api[n(361)]["inputs"]["value"] = 24
    api[n(372)]["inputs"]["value"] = LTX_W; api[n(360)]["inputs"]["value"] = LTX_H
    api[n(366)]["inputs"]["batch_size"] = 1
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(339)]["inputs"]["noise_seed"] = seed; api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    got = comfy.run(W.prune(api), f"{OUT}/clips", os.path.basename(out)[:-4], timeout=1800)[0]
    shutil.move(got, out)


def seg_len(i, tl):
    """Screen time of shot i: from half a gap before its line to half a gap before the next (last shot gets the tail)."""
    a = 0.0 if i == 0 else tl[i]["start"] - GAP / 2
    b = tl[i]["start"] + tl[i]["dur"] + TAIL if i == len(tl) - 1 else tl[i + 1]["start"] - GAP / 2
    return a, b - a


def do_anim(arg="", seed=21):
    os.makedirs(f"{OUT}/clips", exist_ok=True)
    tl = json.load(open(f"{OUT}/timeline.json")); idx = {x["id"]: i for i, x in enumerate(tl)}
    for s in sorted(sel(arg), key=lambda s: s["eng"] != "ltx"):
        out = f"{OUT}/clips/{s['id']}_{s['eng']}_s{seed}.mp4"
        if os.path.exists(out): continue
        secs = max(5, int(np.ceil(seg_len(idx[s["id"]], tl)[1] + 0.5)))
        kf = f"{OUT}/keyframes/{s['id']}.png"; t0 = time.time()
        try:
            if s["eng"] == "card":
                card(s["card"], out, seg_len(idx[s["id"]], tl)[1] + 0.3)
            elif s["eng"] == "ltx" and secs > 10:          # longer than one LTX clip: continue from its own last frame, no freeze
                a, b, last = out[:-4] + "_a.mp4", out[:-4] + "_b.mp4", out[:-4] + "_last.png"
                ltx(kf, s["mv"], a, 10, seed)
                subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-sseof", "-0.1", "-i", a, "-frames:v", "1", "-update", "1", last], check=True)
                ltx(last, s["mv"], b, max(5, secs - 10 + 1), seed + 7)
                subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", a, "-i", b, "-filter_complex",
                                "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "16",
                                "-pix_fmt", "yuv420p", "-c:a", "aac", out], check=True)
                for f in (a, b, last): os.remove(f)
            elif s["eng"] == "ltx":
                ltx(kf, s["mv"], out, min(secs, 10), seed)
            else:
                comfy.free()
                talk = s["spk"] == R
                audio = wav(s) if talk else silent(f"{OUT}/silent_{secs}.wav", secs)
                h3.render(out, keyframe=kf, refs=[kf] if getattr(T, "H3_REF_KF", False) else [REFS[x] for x in s.get("refs", [])], audio=audio, prompt=f"{s['mv']} {LOOK}",
                          size=(768, 1344), seconds=secs, seed=seed, mode="flex", anchor_audio=talk)
            print("clip", out, "%.0fs" % (time.time() - t0), flush=True)
        except Exception as e:
            print("FAILED", s["id"], repr(e)[:300], flush=True)
    comfy.free(); h3.free()


def card(c, out, seconds, fps=24):
    """Motion-graphic card (no AI): flat background, a big word/number pops in, a small line fades in under it, slow push-in."""
    from PIL import Image, ImageDraw, ImageFont
    fdir = "studio/fonts_reel"; big = ImageFont.truetype(f"{fdir}/Montserrat-ExtraBold.ttf", c.get("size", 300))
    small = ImageFont.truetype(f"{fdir}/Montserrat-ExtraBold.ttf", 64)
    bg, fg, acc = c.get("bg", "#2E4A62"), c.get("fg", "#F6EBD9"), c.get("accent", "#F2A65A")
    n = int(seconds * fps); cy = 760
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W_}x{H_}", "-r", str(fps), "-i", "-",
                          "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for k in range(n):
        t = k / fps; im = Image.new("RGB", (W_, H_), bg); d = ImageDraw.Draw(im)
        ring = tuple(min(255, int(int(bg[i:i + 2], 16) * 1.15)) for i in (1, 3, 5))
        for r in range(9):                                            # rings ripple outward continuously: the card never sits still
            rad = 300 + r * 110 + (t * 70) % 110
            d.ellipse([W_ / 2 - rad, cy - rad, W_ / 2 + rad, cy + rad], outline=ring, width=6)
        e = min(1, t / 0.45); e = 1 - (1 - e) ** 3                   # ease-out pop
        if e > 0:
            layer = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            ld.text((W_ / 2, cy), c["big"], font=big, fill=fg, anchor="mm")
            sc = 0.75 + 0.25 * e + 0.08 * t / seconds
            layer = layer.resize((int(W_ * sc), int(H_ * sc)), Image.LANCZOS)
            ox, oy = (layer.width - W_) // 2, int(cy * sc - cy + 12 * np.sin(t * 2.2))
            layer = layer.crop((ox, oy, ox + W_, oy + H_)); a = layer.split()[3].point(lambda v: int(v * e))
            im.paste(layer, (0, 0), a)
        if c.get("small") and t > 0.4:
            a = min(1, (t - 0.4) / 0.4); col = tuple(int(int(bg[i:i + 2], 16) * (1 - a) + int(acc[i:i + 2], 16) * a) for i in (1, 3, 5))
            d.text((W_ / 2, cy + 260 + int(20 * (1 - a))), c["small"], font=small, fill=col, anchor="mm")
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()


def do_sheets():
    os.makedirs(f"{OUT}/qc", exist_ok=True)
    for f in sorted(glob.glob(f"{OUT}/clips/*.mp4")):
        o = f"{OUT}/qc/{os.path.basename(f)[:-4]}.jpg"
        if os.path.exists(o): continue
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f, "-vf", "fps=1,scale=200:-1,tile=8x1", "-frames:v", "1", o])


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


_asr = None
def line_words(s):
    """Word timings (distil-large-v3), spelled as in the script; falls back to even spacing when counts differ."""
    global _asr
    from faster_whisper import WhisperModel
    if _asr is None:
        try: _asr = WhisperModel("distil-large-v3", device="cuda", compute_type="float16")
        except RuntimeError: _asr = WhisperModel("distil-large-v3", device="cpu", compute_type="int8")   # GPU busy with another render
    ws = [w for sg in _asr.transcribe(load(wav(s), 16000), language="en", word_timestamps=True, beam_size=5)[0] for w in sg.words]
    sw = s["text"].split()
    if len(ws) == len(sw): return [{"w": a, "s": w.start, "e": w.end} for a, w in zip(sw, ws)]
    s0, e0 = (ws[0].start, ws[-1].end) if ws else (0, sf.info(wav(s)).duration); st = (e0 - s0) / len(sw)
    return [{"w": w, "s": s0 + k * st, "e": s0 + (k + 1) * st} for k, w in enumerate(sw)]


def captions(tl, total):
    def ts(t): h, m = divmod(t, 3600); m, s = divmod(m, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: C,Montserrat ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,80,80,560,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = []
    for x, s in zip(tl, SHOTS):
        chunks, cur = [], []
        for w in line_words(s):
            cur.append(w)
            if len(cur) == 3 or re.search(r"[.,?!]$", w["w"]): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for j, c in enumerate(chunks):
            a = x["start"] + c[0]["s"]; b = x["start"] + (chunks[j + 1][0]["s"] if j + 1 < len(chunks) else c[-1]["e"] + 0.25)
            ev.append(f"Dialogue: 0,{ts(a)},{ts(min(b, total))},C,,0,0,0,,{' '.join(w['w'] for w in c).upper()}")
    return head + "\n".join(ev) + "\n"


def clip_for(s, pick):
    if s["id"] in pick: return f"{OUT}/clips/{pick[s['id']]}"
    c = sorted(glob.glob(f"{OUT}/clips/{s['id']}_*.mp4"), key=os.path.getmtime)
    if not c: raise SystemExit(f"no clip for {s['id']}")
    return c[-1]


def do_mix():
    tl = json.load(open(f"{OUT}/timeline.json"))
    pick = json.load(open(f"{OUT}/pick.json")) if os.path.exists(f"{OUT}/pick.json") else {}
    total = tl[-1]["start"] + tl[-1]["dur"] + TAIL; sr = 48000; n = int(total * sr)
    speech, amb = np.zeros(n, np.float32), np.zeros(n, np.float32)
    os.makedirs(f"{OUT}/seg", exist_ok=True); lst = []; h3.free(); comfy.start()
    for i, (x, s) in enumerate(zip(tl, SHOTS)):
        a = load(wav(s)); st = int(x["start"] * sr); speech[st:st + len(a)] += a[: n - st]
        s0, L = seg_len(i, tl); clip = clip_for(s, pick); h3like = "_h3_" in clip; skip = 0.125 if h3like else 0.0
        cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout)
        pad = max(0.0, L - (cd - skip)); slow = ""
        if 0 < pad and L / (cd - skip) <= 1.2:            # up to 20% short: slow the clip down slightly instead of freezing a frame
            slow = f"setpts=PTS*{L / (cd - skip):.4f},"; pad = 0.0
        if pad > 0.05: print(f"WARN {s['id']}: clip {cd:.1f}s < shot {L:.1f}s, holding last frame {pad:.1f}s")
        o = f"{OUT}/seg/{i:02d}.mp4"
        vf = slow + f"scale={W_}:{H_}:force_original_aspect_ratio=increase:flags=lanczos,crop={W_}:{H_},fps=24" + (f",tpad=stop_mode=clone:stop_duration={pad:.3f}" if pad > 0 else "")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(skip), "-i", clip, "-t", f"{L:.3f}", "-an", "-vf", vf,
                        "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
        lst.append(f"file '{os.path.abspath(o)}'")
        if s["eng"] == "card": src = load(sfx(s.get("sfx") or "quiet room tone", int(np.ceil(L)) + 1)); lvl = -24
        elif h3like: src = load(sfx(s.get("sfx") or "quiet small apartment room tone", int(np.ceil(L)) + 1)); lvl = -32 if s["spk"] == R else -24
        else: src = load(clip); lvl = -20
        src = src[: int(L * sr)]; a0 = int(s0 * sr)
        if len(src):
            fade = min(len(src) // 2, int(0.25 * sr)); env = np.ones(len(src), np.float32)
            if fade: env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
            amb[a0:a0 + len(src)] += (src * env * min(db(lvl) / (np.abs(src).max() + 1e-6), 3.0))[: n - a0]
    comfy.free()
    sf.write(f"{OUT}/mix.wav", np.clip(speech + amb, -1, 1), sr)
    open(f"{OUT}/seg/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/seg/list.txt", "-c", "copy", f"{OUT}/picture.mp4"], check=True)
    open(f"{OUT}/captions.ass", "w").write(captions(tl, total))
    final = f"{OUT}/{TOPIC.upper()}_SHORT.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"{OUT}/picture.mp4", "-i", f"{OUT}/mix.wav",
                    "-vf", f"subtitles={OUT}/captions.ass:fontsdir={os.path.abspath('studio/fonts_reel')}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", final], check=True)
    print("done", final, "%.1fs" % total, flush=True)


if __name__ == "__main__":
    st = sys.argv[2]; arg = sys.argv[3] if len(sys.argv) > 3 else ""
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 21
    if st == "all":
        do_voice(); do_refs(); do_kf(); do_anim(); do_sheets(); do_mix()
    else:
        {"voice": do_voice, "refs": do_refs, "kf": lambda: do_kf(arg), "anim": lambda: do_anim(arg, seed),
         "sheets": do_sheets, "mix": do_mix}[st]()
