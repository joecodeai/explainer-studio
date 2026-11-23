"""Bat-bomb YouTube Short (native 9:16, ~50 s): voice -> refs -> keyframes -> animate -> mix.

Every stage is cached (delete a file to redo just it). Run stages in order:
  P=".venv/bin/python"; export PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1
  $P tools/batbomb/short.py voice      # Maya + Ryan lines (locked cloned voices) -> timing
  $P tools/batbomb/short.py refs       # FDR sheet (others reused from the animation test)
  $P tools/batbomb/short.py kf         # 2 vertical keyframe options per shot -> pick -> keyframes/<id>.png
  $P tools/batbomb/short.py anim       # LTX shots then H3 shots
  $P tools/batbomb/short.py mix        # natural-sound mix + captions -> BATBOMB_SHORT.mp4
"""
import json, os, random, re, shutil, subprocess, sys, wave
import numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
from studio import comfy, h3, imagegen, voice, script, workflows as W
from studio.hero import NEG

OUT = "projects/batbomb-short"
TEST = "projects/batbomb-animtest"
W_, H_ = 1080, 1920
STYLE = ("2D hand-drawn animated feature film still, cel-shaded characters with clean confident ink outlines and soft painted shading, "
         "richly detailed painterly backgrounds with depth and atmospheric perspective, cinematic lighting, warm 1940s American period detail, "
         "slightly exaggerated expressive cartoon proportions, high production value animated movie look. "
         "Absolutely no text, letters, numbers or logos anywhere.")
LOOK = ("2D hand-drawn animated feature film, cel-shaded characters with clean ink outlines, painted backgrounds, "
        "smooth fluid professional character animation with weight, anticipation and follow-through, cinematic camera.")
REFS = {"fieser": f"{TEST}/refs/fieser.png", "bat": f"{TEST}/refs/bat.png", "adams": f"{TEST}/refs/adams.png",
        "fdr": f"{OUT}/refs/fdr.png", "ryan": "library/show_refs/benny_front.png", "ryan_face": "library/show_refs/benny_face.png"}

M, R = "maya", "benny"
# id, speaker, voice tag, text, engine, refs, keyframe prompt, motion prompt, sfx (for H3 shots: natural foley prompt)
SHOTS = [
 ("s01", M, "narration", "In 1943, a Harvard chemist armed six sleeping bats with tiny firebombs, while Army cameramen filmed him doing it.",
  "h3", ["fieser", "bat"],
  "Vertical medium shot, 1943 desert airfield in bright midday sun: the chemist from the reference (lean, slicked dark hair, white lab coat "
  "over grey waistcoat and dark tie) stands at a folding wooden table holding a large glass-and-steel syringe, injecting a tiny grey capsule "
  "clipped to the chest of the sleepy hero bat from the reference cupped in his other hand. A metal tray of crushed ice with five more sleeping "
  "bats wearing tiny capsules sits on the table. Behind him, a brand-new wooden control tower and hangars under a hard blue sky. Exactly one person.",
  "The chemist slowly presses the syringe plunger into the tiny capsule on the sleepy bat's chest, then lifts the syringe away and glances up. "
  "The bat stirs and blinks. Slow push in. Exactly one person; he keeps the same face and lab coat. The capsule stays clipped to the bat's chest.",
  "hot desert wind, a fly buzzing, distant film camera whirring, a small glass syringe click"),
 ("s02", M, "dry", "The desert sun woke them up early.",
  "ltx", ["bat"],
  "Vertical close shot: on a metal tray of crushed ice on a folding table in bright desert sun, six small grey-brown bats like the hero bat "
  "from the reference, each with a tiny grey capsule clipped to its chest, are waking up, wings starting to open. Blurred new wooden airfield "
  "buildings behind. No people.",
  "The six small bats blink awake in the hot sun, stretch their dark wings and one by one lift off the ice tray, flapping up and away toward "
  "the wooden buildings in the background, each keeping its tiny capsule on its chest. The camera tilts up to follow them into the blue sky.", ""),
 ("s03", M, "narration", "Exactly fifteen minutes later, the barracks caught fire.",
  "ltx", [],
  "Vertical shot of a long brand-new 1943 wooden army barracks building on a sandy desert airfield in hard midday sun, orange flames "
  "bursting out of its windows and roof eaves, thick black smoke rising into a clear blue sky. The scene is completely deserted: no humans, no soldiers, no figures anywhere, only the burning building.",
  "Flames burst out through the windows and climb up the wooden walls, black smoke billows upward, sparks and embers fly, glass pops. "
  "The building is empty: nobody appears at any window or door, no people, no figures at any time. Slow push in.", ""),
 ("s04", M, "narration", "Then the control tower went up like a giant candle.",
  "ltx", [],
  "Vertical low-angle shot of a tall brand-new 1943 wooden airfield control tower on a lattice frame with a glass cab on top, bright flames "
  "bursting from the cab windows like a giant candle, black smoke pouring into a clear blue desert sky, distant mesas. No people.",
  "The fire roars up out of the glass cab and climbs the wooden tower like a giant candle flame, the windows burst, thick black smoke pours "
  "upward and drifts sideways, embers float down. The camera slowly tilts up the tower.", ""),
 ("s05", M, "deadpan", "The fire trucks raced to the gate, and the guards refused to open it, because the whole thing was top secret.",
  "ltx", [],
  "Vertical shot at a closed chain-link gate of a 1943 desert airfield: a young US Army military policeman in khaki uniform and white helmet "
  "stands stiffly behind the locked gate, arms folded. Outside the gate, two red 1940s fire engines wait with firemen. Behind the fence, "
  "black smoke rises from burning wooden buildings. Exactly three visible people: the guard and two firemen.",
  "The gate stays shut and locked with a padlock and chain the whole time and never opens. The guard stays standing in place behind it with "
  "his arms folded and slowly shakes his head once. Beyond, the firemen by the red fire engines throw up their hands in frustration. "
  "Black smoke rolls across the sky. Locked-off camera, nobody walks away.", ""),
 ("s06", M, "narration", "It all started with a dentist, who wrote to the President with a plan to firebomb Japan with bats.",
  "h3", ["adams"],
  "Vertical medium shot inside a cosy 1942 home study at night: the cheerful dentist from the reference (short, round, balding with grey "
  "fringe, round wire glasses, brown three-piece suit, red bow tie) sits at a wooden desk typing a letter on a black 1940s typewriter, "
  "a green-shaded desk lamp glowing, a framed photo of a cave on the wall, a stack of papers. Exactly one person.",
  "The dentist types eagerly on the typewriter, pauses, smiles to himself with a bright idea, pushes the carriage return and keeps typing. "
  "Gentle push in. Exactly one person; he keeps the same face, glasses and suit.",
  "vintage typewriter keys clacking and a carriage return bell, quiet room, a clock ticking"),
 ("s07", M, "narration", "Franklin Roosevelt passed it on with a note. This man is not a nut.",
  "h3", ["fdr"],
  "Vertical medium shot in a 1942 presidential office: the president from the reference (stylised, dignified: broad face, grey hair swept "
  "back, rimless pince-nez glasses, dark grey double-breasted suit) sits at a large wooden desk reading a typed letter, a fountain pen "
  "in his hand, flags and tall windows softly behind him. Exactly one person.",
  "The president reads the letter, raises one eyebrow, then writes a short note on a small card with his fountain pen and sets it on the "
  "letter. Locked-off camera, gentle light. Exactly one person; he keeps the same face and suit.",
  "fountain pen scratching on paper, paper rustle, quiet large office"),
 ("s08", R, "disbelief", "That's the reference? Not a nut?",
  "h3", ["ryan", "ryan_face"],
  "Vertical waist-up shot of the young man from the reference (thick curly dark brown hair, burnt-orange open hoodie over white t-shirt, "
  "black crossbody strap) standing in a small cosy modern apartment living room, looking at camera with a sceptical raised eyebrow. "
  "Exactly one person.",
  "The young man speaks to camera in disbelief, eyebrows raised, a small open-palm gesture, then a slow blink. Locked-off camera, waist-up. "
  "Exactly one person; he keeps the same face, hair and hoodie.", ""),
 ("s09", M, "narration", "Two years and two million dollars later, the bats finally worked, and the project was cancelled.",
  "ltx", ["bat"],
  "Vertical shot high above the desert: a five-foot olive-drab steel bomb casing hangs under a white parachute against a pale blue sky, "
  "its sides opening as a cloud of small bats like the reference spills out. Desert and mountains far below.",
  "The casing's sides fall away and hundreds of small bats pour out and scatter in all directions, wings flickering, the parachute swaying. "
  "The camera slowly drifts down with the casing.", ""),
 ("s10", M, "dry", "Subscribe for more.",
  "ltx", ["bat"],
  "Vertical shot at dusk: the hero bat from the reference hangs at the mouth of a huge desert cave, looking back at camera with big worried "
  "eyes, while behind it a river of millions of bats spirals up into an orange and violet sunset sky.",
  "The hero bat blinks, twitches its ears, then turns and drops off the rock and flies out to join the swirling river of bats rising into "
  "the sunset. The camera holds, then slowly cranes up.", ""),
]
GAP = 0.3            # between lines
TAIL = 3.6           # the final shot plays out fully (hero bat flies off into the swarm)


# ---------------------------------------------------------------- voice
def k_line(i): return f"{OUT}/audio/{SHOTS[i][0]}.wav"


def do_voice():
    sh = script.load_show()
    chars = [{k: c[k] for k in ("id", "name", "look", "voice") if k in c} | ({"tts": c["tts"]} if c.get("tts") else {}) for c in sh["cast"]]
    scenes = [{"id": s[0], "lines": [{"speaker": s[1], "voice": s[2], "text": s[3], "emotion": "neutral"}]} for s in SHOTS]
    os.makedirs(f"{OUT}/audio", exist_ok=True)
    json.dump(scenes, open(f"{OUT}/lines.json", "w"), indent=1)
    voice.narrate({"characters": chars, "narrator_voice": sh.get("narrator"), "scenes": scenes}, f"{OUT}/audio")
    t, tl = 0.4, []
    for i, s in enumerate(SHOTS):
        d = sf.info(k_line(i)).duration
        tl.append({"id": s[0], "start": round(t, 3), "dur": round(d, 3)}); t += d + GAP
    json.dump(tl, open(f"{OUT}/timeline.json", "w"), indent=1)
    print("speech total %.1fs, video %.1fs" % (sum(x["dur"] for x in tl), t - GAP + TAIL))


# ---------------------------------------------------------------- refs
def do_refs():
    os.makedirs(f"{OUT}/refs", exist_ok=True)
    comfy.start()
    for s in (1, 2):
        p = f"{OUT}/refs/fdr_s{s}.png"
        if not os.path.exists(p):
            got = imagegen.t2i(f"{STYLE} Character model sheet on a plain flat light grey background: the SAME character shown three times "
                               "(front view seated, three-quarter view, side view) plus a large head close-up. Consistent design in every view. "
                               "The character: President Franklin D. Roosevelt in 1942, drawn as a dignified, respectful stylised cartoon: a man of 60 "
                               "with a broad face, strong jaw, friendly confident expression, receding grey hair swept back, rimless pince-nez glasses, "
                               "dark grey double-breasted suit, white shirt, dark tie.", f"{OUT}/refs", f"fdr_s{s}", 1344, 768, seed=300 + s)
            shutil.move(got, p); print("ref", p)
    comfy.free()


# ---------------------------------------------------------------- keyframes
def do_kf(only=""):
    os.makedirs(f"{OUT}/keyframes", exist_ok=True)
    comfy.start()
    for sid, spk, tag, text, eng, refs, kp, mp, sfxp in SHOTS:
        if only and sid not in only.split(","): continue
        for s in (1, 2):
            p = f"{OUT}/keyframes/{sid}_s{s}.png"
            if os.path.exists(p): continue
            full = f"{STYLE} 9:16 vertical cinematic film frame. {kp}"
            rp = [REFS[r] for r in refs]
            got = (imagegen.edit(full, rp, f"{OUT}/keyframes", f"{sid}_s{s}", 768, 1344, seed=400 + s, fixed_size=True) if rp
                   else imagegen.t2i(full, f"{OUT}/keyframes", f"{sid}_s{s}", 768, 1344, seed=400 + s))
            shutil.move(got, p); print("kf", p, flush=True)
    comfy.free()


# ---------------------------------------------------------------- animation
def silent(path, seconds):
    if not os.path.exists(path):
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\x00\x00" * int(24000 * seconds))
    return path


def ltx(image, prompt, out, seconds, seed):
    api = W.load("ltx_i2v")
    n = lambda i: f"398:{i}"
    api[n(364)]["inputs"]["text"] = f"{prompt} {LOOK} Natural realistic ambient sound of the scene, no music, no speech."
    api[n(373)]["inputs"]["text"] = NEG + ", morphing, warping, melting, sliding feet, frozen still image, slideshow, music"
    api[n(362)]["inputs"]["value"] = int(seconds)
    api[n(361)]["inputs"]["value"] = 24
    api[n(372)]["inputs"]["value"] = 704
    api[n(360)]["inputs"]["value"] = 1280
    api[n(366)]["inputs"]["batch_size"] = 1
    api[n(351)]["inputs"].update({"resize_type": "scale longer dimension", "resize_type.longer_size": 1536, "scale_method": "lanczos"})
    api[n(339)]["inputs"]["noise_seed"] = seed
    api[n(338)]["inputs"]["noise_seed"] = seed + 1
    api["395"]["inputs"]["image"] = comfy.upload(image)
    api["75"]["inputs"].update({"format": "mp4", "format.codec": "h264"})
    got = comfy.run(W.prune(api), f"{OUT}/clips", os.path.basename(out)[:-4], timeout=1800)[0]
    shutil.move(got, out)


def do_anim(only="", seed=21, engine=""):
    os.makedirs(f"{OUT}/clips", exist_ok=True)
    tl = {x["id"]: x for x in json.load(open(f"{OUT}/timeline.json"))}
    jobs = [s for s in SHOTS if (not only or s[0] in only.split(",")) and (not engine or s[4] == engine)]
    for sid, spk, tag, text, eng, refs, kp, mp, sfxp in sorted(jobs, key=lambda s: s[4] != "ltx"):
        out = f"{OUT}/clips/{sid}_{eng}_s{seed}.mp4"
        if os.path.exists(out): continue
        secs = max(5, int(np.ceil(tl[sid]["dur"] + GAP + 0.6)))
        kf = f"{OUT}/keyframes/{sid}.png"
        if eng == "ltx":
            ltx(kf, mp, out, secs, seed)
        else:
            comfy.free()
            audio = k_line(SHOTS.index(next(s for s in SHOTS if s[0] == sid))) if spk == R else silent(f"{OUT}/silent_{secs}.wav", secs)
            r = h3.render(out, keyframe=kf, refs=[REFS[x] for x in refs], audio=audio, prompt=f"{mp} {LOOK}",
                          size=(768, 1344), seconds=secs, seed=seed, mode="flex", anchor_audio=(spk == R))
            print("h3", sid, r, flush=True)
        print("clip", out, flush=True)
    comfy.free(); h3.free()


# ---------------------------------------------------------------- mix
def sfx(prompt, seconds):
    """Stable Audio 3 natural foley (realistic, not cartoon), cached in the shared sound library."""
    import hashlib
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


def captions(tl, words_by_line, total):
    """Shorts-style burned captions: 2-3 word chunks, centred lower third, white with a black outline."""
    def ts(t): h, m = divmod(t, 3600); m, s = divmod(m, 60); return f"{int(h)}:{int(m):02d}:{s:05.2f}"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: C,Montserrat ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,80,80,560,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = []
    for x, words in zip(tl, words_by_line):
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(cur) == 3 or re.search(r"[.,?!]$", w["w"]): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for j, c in enumerate(chunks):
            a = x["start"] + c[0]["s"]; b = x["start"] + (chunks[j + 1][0]["s"] if j + 1 < len(chunks) else c[-1]["e"] + 0.25)
            txt = " ".join(w["w"] for w in c).upper()
            ev.append(f"Dialogue: 0,{ts(a)},{ts(min(b, total))},C,,0,0,0,,{txt}")
    return head + "\n".join(ev) + "\n"


def line_words(i):
    """Word timings of a voiced line (distil-large-v3), spelled as in the script."""
    from faster_whisper import WhisperModel
    global _asr
    try: _asr
    except NameError: _asr = WhisperModel("distil-large-v3", device="cuda", compute_type="float16")
    a = load(k_line(i), 16000)
    ws = [w for sg in _asr.transcribe(a, language="en", word_timestamps=True, beam_size=5)[0] for w in sg.words]
    script_words = SHOTS[i][3].split()
    if len(ws) == len(script_words):
        return [{"w": sw, "s": w.start, "e": w.end} for sw, w in zip(script_words, ws)]
    # counts differ (numbers etc.): spread the script words evenly over the spoken span
    s0, e0 = (ws[0].start, ws[-1].end) if ws else (0, sf.info(k_line(i)).duration)
    step = (e0 - s0) / len(script_words)
    return [{"w": w, "s": s0 + k * step, "e": s0 + (k + 1) * step} for k, w in enumerate(script_words)]


def do_mix(pick):
    tl = json.load(open(f"{OUT}/timeline.json"))
    total = tl[-1]["start"] + tl[-1]["dur"] + TAIL
    sr = 48000; n = int(total * sr)
    speech, amb = np.zeros(n, np.float32), np.zeros(n, np.float32)
    segs = []
    comfy.start()
    for i, (x, s) in enumerate(zip(tl, SHOTS)):
        a = load(k_line(i)); st = int(x["start"] * sr); speech[st:st + len(a)] += a[: n - st]
        seg_start = 0.0 if i == 0 else x["start"] - GAP / 2
        seg_end = total if i == len(tl) - 1 else tl[i + 1]["start"] - GAP / 2
        clip = f"{OUT}/clips/{pick[s[0]]}"
        segs.append((clip, seg_start, seg_end - seg_start, s[4]))
        # ambience: LTX's own generated sound for LTX shots; natural foley for H3 shots (Ryan's shot: room tone only)
        L = seg_end - seg_start; a0 = int(seg_start * sr)
        if s[4] == "ltx":
            src = load(clip)
            off = 0
        else:
            src = load(sfx(s[8] or "quiet small apartment room tone", int(np.ceil(L)) + 1)); off = 0
        src = src[off: off + int(L * sr)]
        fade = min(len(src), int(0.25 * sr)); env = np.ones(len(src), np.float32)
        if fade: env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
        lvl = -20 if s[4] == "ltx" else -24
        if s[1] == R: lvl = -32
        gain = min(db(lvl) / (np.abs(src).max() + 1e-6), 3.0)        # never boost a near-silent track into hiss
        amb[a0:a0 + len(src)] += (src * env * gain)[: n - a0]
    comfy.free()
    mixwav = f"{OUT}/mix.wav"
    sf.write(mixwav, np.clip(speech + amb, -1, 1), sr)
    # picture
    os.makedirs(f"{OUT}/seg", exist_ok=True); lst = []
    for k, (clip, st, d, eng) in enumerate(segs):
        o = f"{OUT}/seg/{k:02d}.mp4"; skip = 0.125 if eng == "h3" else 0.0          # H3: skip the fresh-keyframe pop frames
        cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip], capture_output=True, text=True).stdout)
        pad = max(0.0, d - (cd - skip))
        vf = f"scale={W_}:{H_}:force_original_aspect_ratio=increase:flags=lanczos,crop={W_}:{H_},fps=24" + (f",tpad=stop_mode=clone:stop_duration={pad:.3f}" if pad > 0 else "")
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(skip), "-i", clip, "-t", f"{d:.3f}", "-an", "-vf", vf,
                        "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", o], check=True)
        lst.append(f"file '{os.path.abspath(o)}'")
    open(f"{OUT}/seg/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/seg/list.txt", "-c", "copy", f"{OUT}/picture.mp4"], check=True)
    ass = f"{OUT}/captions.ass"
    open(ass, "w").write(captions(tl, [line_words(i) for i in range(len(SHOTS))], total))
    fonts = os.path.abspath("studio/fonts_reel")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", f"{OUT}/picture.mp4", "-i", mixwav,
                    "-vf", f"subtitles={ass}:fontsdir={fonts}", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-shortest", f"{OUT}/BATBOMB_SHORT.mp4"], check=True)
    print("done", f"{OUT}/BATBOMB_SHORT.mp4", "%.1fs" % total)


if __name__ == "__main__":
    st = sys.argv[1]; arg = sys.argv[2] if len(sys.argv) > 2 else ""
    if st == "voice": do_voice()
    elif st == "refs": do_refs()
    elif st == "kf": do_kf(arg)
    elif st == "anim": do_anim(arg, int(sys.argv[3]) if len(sys.argv) > 3 else 21, sys.argv[4] if len(sys.argv) > 4 else "")
    elif st == "mix": do_mix(json.load(open(f"{OUT}/pick.json")))
