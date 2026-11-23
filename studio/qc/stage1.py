"""Stage 1: fast automated inspection of the WHOLE video (OpenCV / FFmpeg / OCR / ASR / segmentation / geometry).
Every check returns a list of Findings. Per-scene checks are cached by the scene's render hash, per-asset checks by
the asset's file hash, so unchanged scenes and assets are never analysed twice."""
import difflib, json, os, re, subprocess
import numpy as np
from PIL import Image
from .core import (Finding, W, H, FPS, CHAR_H, FEET_Y, cam_for, camera_at, char_place, file_hash, log, pos_x,
                   proj_path, state_at, to_screen)
from . import models as M


# ================================================================ helpers
def frames(path, fps=None, size=(320, 180), gray=True, ss=None, t=None):
    """Stream frames from ffmpeg (chunked — never holds the whole video in RAM). Yields (time, ndarray)."""
    w, h = size
    vf = (f"fps={fps}," if fps else "") + f"scale={w}:{h}" + (",format=gray" if gray else ",format=rgb24")
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", path] + \
          (["-t", str(t)] if t else []) + ["-vf", vf, "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = w * h * (1 if gray else 3); i = 0; rate = fps or FPS
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n: break
            a = np.frombuffer(b, np.uint8).reshape((h, w) if gray else (h, w, 3))
            yield (ss or 0) + i / rate, a; i += 1
    finally:
        if p.poll() is None: p.kill()
        p.wait()


def frame_at(path, t, size=(W, H)):
    return next((a for _, a in frames(path, None, size, gray=False, ss=max(0, t), t=0.05)), None)


def norm_words(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = t.lower().replace("*", "").replace("'", "").replace("\u2019", "").replace("-", " ").replace("%", " percent")
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)                                   # 1,000 -> 1000
    t = re.sub(r"\d+(?:\.\d+)?", lambda m: " " + _num_words(m.group(0)) + " ", t)   # ASR digits vs spelled-out script
    ws = [_UKUS.get(w, w) for w in re.findall(r"[a-z0-9]+", t)]
    ws = [re.sub(r"(?<=[a-z]{3})is(e|ed|es|ing|ation|ations)$", r"iz\1", w) for w in ws]
    return [w for w in ws if w != "and"]                                      # "one hundred (and) twenty"


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
_NUMW = set(_ONES) | set(_TENS) | {"hundred", "thousand", "million", "billion", "trillion", "point", "oh"}
_UKUS = {"labour": "labor", "colour": "color", "favour": "favor", "honour": "honor", "neighbour": "neighbor", "behaviour": "behavior",
         "centre": "center", "programme": "program", "defence": "defense", "offence": "offense", "licence": "license",
         "travelled": "traveled", "cheque": "check", "analyse": "analyze", "metre": "meter", "litre": "liter", "theatre": "theater"}


def _int_words(n):
    if n < 20: return _ONES[n]
    if n < 100: return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    for div, name in ((10**12, "trillion"), (10**9, "billion"), (10**6, "million"), (1000, "thousand"), (100, "hundred")):
        if n >= div:
            return _int_words(n // div) + " " + name + ("" if n % div == 0 else " " + _int_words(n % div))


def _num_words(s):
    i, _, d = s.partition(".")
    n = int(i) if len(i) < 13 else -1
    if not d and len(i) == 4 and (1910 <= n <= 1999 or 2010 <= n <= 2099):           # years: "twenty twenty six"
        return _int_words(n // 100) + " " + (_int_words(n % 100) if n % 100 >= 10 else "oh " + _ONES[n % 100])
    out = _int_words(n) if n >= 0 else " ".join(_ONES[int(c)] for c in i)
    if d: out += " point " + " ".join(_ONES[int(c)] for c in d)
    return out


def sim(a, b):
    """Best of word-level and character-level similarity (names are often heard right but spelled differently by ASR)."""
    a, b = norm_words(a), norm_words(b)
    if not a and not b: return 1.0
    w = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    c = difflib.SequenceMatcher(None, " ".join(a), " ".join(b), autojunk=False).ratio()
    # the same number can be said/written many ways ("twenty-four hundred thousand" = 2,400,000) -> also compare without number words
    an, bn = [x for x in a if x not in _NUMW], [x for x in b if x not in _NUMW]
    n = difflib.SequenceMatcher(None, an, bn, autojunk=False).ratio() if (an or bn) and len(an) < len(a) else 0
    return max(w, c, n)


_DICT = None


def is_word(w):
    global _DICT
    if _DICT is None:
        _DICT = set()
        for p in ("/usr/share/dict/american-english", "/usr/share/dict/british-english", "/usr/share/dict/words"):
            if os.path.exists(p): _DICT |= {x.strip().lower() for x in open(p, errors="ignore")}
    w = w.lower().strip(".,!?:;'\"()")
    return len(w) < 3 or w.isdigit() or w in _DICT or w.rstrip("s") in _DICT


# ================================================================ 1. frames (per scene)
def check_frames(pr, cache, cfg):
    out = []
    for s in pr.scenes:
        sid = s["id"]; key = pr.render_hash(sid) + ":frames4"
        hit = cache.get("frames", key)
        if hit is None:
            hit = _scan_scene(pr, s, cfg); cache.put("frames", key, hit)
        out += [Finding(**f) for f in hit]
    return out


def _scan_scene(pr, s, cfg):
    import cv2
    sid, kind = s["id"], s["kind"]; props = pr.props[sid]; t0 = pr.start[sid]
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                        "-of", "json", pr.render[sid]], capture_output=True, text=True)
    st = json.loads(r.stdout or "{}").get("streams", [{}])[0]
    res = []
    if (st.get("width"), st.get("height")) != (W, H):
        res.append(dict(category="visual", severity="CRITICAL", description=f"scene renders at {st.get('width')}x{st.get('height')}, expected {W}x{H}",
                        start=t0, scene=sid, fix="rerender", fix_args={"scene": sid}, recommendation="re-render the scene"))
    mean, std, lap, diff = [], [], [], []
    prev = None
    for t, a in frames(pr.render[sid], None, tuple(cfg["frame_scale"])):
        a32 = a.astype(np.float32)
        mean.append(float(a32.mean())); std.append(float(a32.std())); lap.append(float(cv2.Laplacian(a, cv2.CV_32F).var()))
        diff.append(0.0 if prev is None else float(np.abs(a32 - prev).mean())); prev = a32
    n = len(mean)
    if not n:
        return [dict(category="visual", severity="CRITICAL", description="scene render has no decodable frames", start=t0, scene=sid,
                     fix="rerender", fix_args={"scene": sid})]
    # expected visual events: line starts (camera moves/cuts) and the first 0.5 s (entrances/animations)
    events = [l["start"] for l in props.get("lines", [])]
    for m in props.get("cast", []):
        last = None
        for i in range(int(pr.dur[sid] * FPS)):
            st_ = state_at(m, props["cast"], props["lines"], i / FPS); k = (st_["pose"], st_["flip"])
            if k != last and last is not None: events.append(i / FPS)
            last = k
    events += [b["atMs"] / 1000 for b in props.get("beats", [])]
    near_event = lambda t: t < 0.5 or any(-0.15 < t - e < 0.7 for e in events)
    med_lap = float(np.median(lap)) or 1
    blur_run = 0
    for i in range(n):
        t = i / FPS
        if std[i] < 6 and kind != "title_card":
            res.append(dict(category="visual", severity="HIGH", description=f"blank / single-colour frame", start=t0 + t, end=t0 + t + 1 / FPS,
                            scene=sid, fix="rerender", fix_args={"scene": sid}, recommendation="re-render the scene; if it persists regenerate the source shot"))
        if 0 < i < n - 1 and diff[i] > 22 and diff[i + 1] > 22 and abs(mean[i + 1] - mean[i - 1]) < 4 and not near_event(t):
            res.append(dict(category="visual", severity="HIGH", description="single-frame flash / glitch", start=t0 + t, end=t0 + t + 1 / FPS,
                            scene=sid, fix="rerender", fix_args={"scene": sid}))
        if i and abs(mean[i] - mean[i - 1]) > 28 and not near_event(t):
            res.append(dict(category="visual", severity="MEDIUM", description=f"sudden brightness change ({mean[i - 1]:.0f}->{mean[i]:.0f})",
                            start=t0 + t, scene=sid, confidence=0.7, fix="rerender", fix_args={"scene": sid}))
        if kind in ("stage", "map", "chart") and i and diff[i] > 18 and not near_event(t):
            res.append(dict(category="animation", severity="MEDIUM", description="sudden jump inside a shot (no cut expected here)",
                            start=t0 + t, scene=sid, confidence=0.6, recommendation="check pose switch / camera move at this time"))
        blur_run = blur_run + 1 if (lap[i] < med_lap * 0.3 and kind not in ("title_card",) and not near_event(t)) else 0
        if blur_run == 4:
            res.append(dict(category="visual", severity="MEDIUM", description="blurred frames", start=t0 + t - 3 / FPS, scene=sid, confidence=0.6))
    # freezes (static picture where motion is expected)
    if kind in ("stage", "hero", "map"):
        run = 0
        for i in range(1, n):
            run = run + 1 if diff[i] < 0.12 else 0
            if run == int(2.5 * FPS):
                res.append(dict(category="animation", severity="MEDIUM", description="picture frozen for > 2.5 s", start=t0 + (i - run) / FPS,
                                end=t0 + i / FPS, scene=sid, fix="rerender" if kind != "hero" else "regen_hero", fix_args={"scene": sid}))
    if kind == "hero":
        dup = sum(1 for d in diff[1:] if d < 0.05) / max(1, n - 1)
        if dup > 0.3:
            res.append(dict(category="animation", severity="LOW", description=f"stuttering video ({dup:.0%} duplicated frames)", start=t0, scene=sid,
                            fix="regen_hero", fix_args={"scene": sid}, confidence=0.7))
    return _dedupe(res)


def _dedupe(rows, gap=0.6):
    out = []
    for r in rows:
        if out and out[-1]["description"].split("(")[0] == r["description"].split("(")[0] and r.get("start") is not None and \
           out[-1].get("start") is not None and r["start"] - (out[-1].get("end") or out[-1]["start"]) < gap:
            out[-1]["end"] = r.get("end") or r["start"]; continue
        out.append(r)
    return out


# ================================================================ 2. transitions (final video, full frame rate)
def check_transitions(pr, cache, cfg):
    key = file_hash(pr.video) + ":tr"
    hit = cache.get("transitions", key)
    if hit is not None: return [Finding(**f) for f in hit]
    res, win = [], cfg["transition_window"]
    for s in pr.scenes[1:]:
        tb = pr.start[s["id"]]
        fr = list(frames(pr.video, None, (320, 180), ss=max(0, tb - win), t=2 * win))
        for i, (t, a) in enumerate(fr):
            a32 = a.astype(np.float32)
            if a32.std() < 6 and s["kind"] != "title_card":
                res.append(dict(category="visual", severity="HIGH", description=f"blank frame during the transition into {s['id']} ({s.get('transition')})",
                                start=t, scene=s["id"], fix="transition", fix_args={"scene": s["id"]},
                                recommendation="use a fade for this transition")); break
            if 0 < i < len(fr) - 1:
                p, q = fr[i - 1][1].astype(np.float32), fr[i + 1][1].astype(np.float32)
                if np.abs(a32 - p).mean() > 30 and np.abs(q - a32).mean() > 30 and np.abs(q - p).mean() < 8:
                    res.append(dict(category="visual", severity="HIGH", description=f"one-frame glitch at the transition into {s['id']}",
                                    start=t, scene=s["id"], fix="transition", fix_args={"scene": s["id"]})); break
    cache.put("transitions", key, res)
    return [Finding(**f) for f in res]


# ================================================================ 3. audio (final mix)
def check_audio(pr, cache, cfg):
    res = []
    r = subprocess.run(["ffmpeg", "-nostats", "-i", pr.video, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    lufs = float(I[-1]) if I else None; peak = float(TP[-1]) if TP else None
    if lufs is not None and abs(lufs + 14) > 1.5:
        res.append(Finding("audio", "MEDIUM", f"integrated loudness {lufs} LUFS (target -14)", fix="remaster", recommendation="re-run the master stage"))
    if peak is not None and peak > -0.5:
        res.append(Finding("audio", "HIGH", f"true peak {peak} dBFS — clipping", fix="remaster"))
    dur = os.path.getsize(pr.video) and __import__("studio.qc.core", fromlist=["probe_dur"]).probe_dur(pr.video)
    r = subprocess.run(["ffmpeg", "-nostats", "-i", pr.video, "-af", "silencedetect=n=-45dB:d=1.2", "-f", "null", "-"], capture_output=True, text=True).stderr
    for a, b in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r):
        a, b = float(a), float(b)
        if a > 0.5 and b < dur - 0.5:
            res.append(Finding("audio", "MEDIUM", f"unwanted silence {b - a:.1f} s", start=a, end=b, scene=pr.scene_at(a)))
    # dialogue structure: overlaps and long pauses inside a scene
    for s in pr.scenes:
        ls = pr.lines[s["id"]]
        for x, y in zip(ls, ls[1:]):
            t = pr.start[s["id"]] + y["start"]
            if y["start"] < x["end"] - 0.05:
                res.append(Finding("audio", "HIGH", f"overlapping dialogue ({x['speaker']} / {y['speaker']})", start=t, scene=s["id"]))
            elif y["start"] - x["end"] > 1.3:
                res.append(Finding("audio", "LOW", f"unnatural pause {y['start'] - x['end']:.1f} s between lines", start=pr.start[s["id"]] + x["end"], end=t, scene=s["id"]))
    # abrupt level jumps across scene boundaries
    import soundfile as sf
    wav = os.path.join(pr.dir, "work", "qc_master.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr.video, "-ac", "1", "-ar", "16000", wav], check=False)
    a, sr = sf.read(wav, dtype="float32")
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-6)
    for s in pr.scenes[1:]:
        i = int(pr.start[s["id"]] * sr); w = int(0.25 * sr)
        if w < i < len(a) - w:
            pre, post = db(a[i - w:i]), db(a[i:i + w])
            j = post - pre
            if abs(j) > 30 and min(pre, post) > -45:          # silence -> speech is a normal pause, not a glitch
                res.append(Finding("audio", "LOW", f"abrupt level change {j:+.0f} dB at the cut into {s['id']}", start=pr.start[s["id"]], scene=s["id"], confidence=0.6))
    return res


# ================================================================ 4. speech + subtitles (per line, ASR)
def check_speech(pr, cache, cfg):
    import soundfile as sf
    res = []
    master = os.path.join(pr.dir, "work", "qc_master.wav")
    if not os.path.exists(master):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr.video, "-ac", "1", "-ar", "16000", master], check=False)
    mix, msr = sf.read(master, dtype="float32")
    for s in pr.scenes:
        sid = s["id"]; props = pr.props[sid]; words = props.get("words", [])
        for ln in pr.lines[sid]:
            key = ln.get("key"); wav = os.path.join(pr.dir, "audio", "lines", f"{key}.wav")
            if not key or not os.path.exists(wav): continue
            t0 = pr.start[sid] + ln["start"]
            hit = cache.get("asr", f"{key}:{int(os.path.getmtime(wav))}")
            if hit is None:
                text, ws = M.asr(wav); hit = {"text": text, "words": ws}; cache.put("asr", f"{key}:{int(os.path.getmtime(wav))}", hit)
            script = ln["text"]; heard = hit["text"]; sm = sim(script, heard)
            a, b = norm_words(script), norm_words(heard)
            ops = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op[0] != "equal"]
            missing = [" ".join(a[i1:i2]) for tag, i1, i2, j1, j2 in ops if tag == "delete"]
            extra = [" ".join(b[j1:j2]) for tag, i1, i2, j1, j2 in ops if tag == "insert"]
            wrong = [f"'{' '.join(a[i1:i2])}'->'{' '.join(b[j1:j2])}'" for tag, i1, i2, j1, j2 in ops if tag == "replace"]
            if sm < 0.9:
                sev = "HIGH" if sm < 0.75 else "MEDIUM"
                det = "; ".join(x for x in [f"missing: {missing}" if missing else "", f"extra/repeated: {extra}" if extra else "",
                                            f"wrong: {wrong[:3]}" if wrong else ""] if x)
                res.append(Finding("audio", sev, f"spoken line does not match script (match {sm:.2f}) {det} — \"{script[:60]}\"",
                                   start=t0, end=pr.start[sid] + ln["end"], scene=sid, fix="retake_line",
                                   fix_args={"scene": sid, "key": key}, recommendation="regenerate this TTS line"))
            # intelligibility in the final mix (music / ambience masking speech)
            seg = mix[int(t0 * msr): int((pr.start[sid] + ln["end"]) * msr)]
            mk = f"{key}:{round(t0, 2)}:{os.path.getmtime(pr.video):.0f}"
            hm = cache.get("asr_mix", mk)
            if hm is None and len(seg) > msr * 0.3:
                hm = sim(script, M.asr(seg, msr)[0]); cache.put("asr_mix", mk, hm)
            if hm is not None and sm - hm > 0.25:
                res.append(Finding("audio", "MEDIUM", f"speech hard to hear in the final mix (clean {sm:.2f} vs mix {hm:.2f})", start=t0, scene=sid,
                                   fix="music_level", recommendation="lower music/ambience under dialogue", confidence=0.7))
            # subtitle timing vs heard word timing
            lw = [w for w in words if ln["start"] * 1000 - 50 <= w["startMs"] <= ln["end"] * 1000 + 50]
            aw = hit["words"]
            # whisper word times sometimes drift (esp. around numbers) and run past the end of the clip -> timing unreliable, don't judge
            if aw and aw[-1][2] > (ln["end"] - ln["start"]) + 0.2: aw = []
            if lw and aw:
                sa = [re.sub(r"[^a-z0-9]", "", w["text"].lower()) for w in lw]; sb = [re.sub(r"[^a-z0-9]", "", w[0].lower()) for w in aw]
                offs = []
                for blk in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_matching_blocks():
                    for k in range(blk.size):
                        offs.append(lw[blk.a + k]["startMs"] / 1000 - (ln["start"] + aw[blk.b + k][1]))
                if offs:
                    med, worst = float(np.median(np.abs(offs))), float(np.max(np.abs(offs)))
                    if med > 0.2 or worst > 0.6:
                        res.append(Finding("subtitle", "MEDIUM", f"subtitles out of sync with speech (median {med * 1000:.0f} ms, worst {worst * 1000:.0f} ms)",
                                           start=t0, scene=sid, fix="retime_subtitles", fix_args={"scene": sid}))
    return res


# ================================================================ 5. voices (identity per speaker)
def check_voices(pr, cache, cfg):
    import librosa
    feats = {}
    for s in pr.scenes:
        for ln in pr.lines[s["id"]]:
            key = ln.get("key"); wav = os.path.join(pr.dir, "audio", "lines", f"{key}.wav")
            if not key or not os.path.exists(wav): continue
            v = cache.get("voice", f"{key}:{int(os.path.getmtime(wav))}")
            if v is None:
                y, sr = librosa.load(wav, sr=16000)
                if len(y) < 8000: continue
                mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[1:].mean(1)
                f0 = librosa.yin(y, fmin=60, fmax=400, sr=sr); f0 = float(np.median(f0[(f0 > 60) & (f0 < 400)])) if np.any((f0 > 60) & (f0 < 400)) else 0
                v = {"mfcc": mf.tolist(), "f0": f0}; cache.put("voice", f"{key}:{int(os.path.getmtime(wav))}", v)
            feats.setdefault(ln["speaker"], []).append((s["id"], pr.start[s["id"]] + ln["start"], v))
    res = []
    cent = {}
    for spk, rows in feats.items():
        mf = np.array([r[2]["mfcc"] for r in rows]); f0 = np.array([r[2]["f0"] for r in rows if r[2]["f0"] > 0])
        cent[spk] = (mf.mean(0), float(np.median(f0)) if len(f0) else 0)
        for sid, t, v in rows:   # voice drifting away from this speaker's own voice
            if v["f0"] > 0 and cent[spk][1] > 0 and abs(12 * np.log2(v["f0"] / cent[spk][1])) > 5:
                res.append(Finding("voice", "MEDIUM", f"{spk}'s voice pitch jumps {12 * np.log2(v['f0'] / cent[spk][1]):+.1f} semitones on this line",
                                   start=t, scene=sid, confidence=0.6, fix="retake_line",
                                   fix_args={"scene": sid, "key": next(l['key'] for l in pr.lines[sid] if abs(pr.start[sid] + l['start'] - t) < 0.01)}))
    from .. import voice as V
    prof = V.voice_profiles(pr.script)
    for spk_id, (_, f0) in cent.items():      # voice must match the character's gender
        g = V.gender(prof.get(spk_id, {}).get("design", ""))
        if prof.get(spk_id, {}).get("tts"): continue      # a voice the user chose (show cast): locked, never auto-redesigned
        if f0 and not V.gender_ok(g, f0, tol=10):
            first = feats[spk_id][0]
            res.append(Finding("voice", "CRITICAL", f"{spk_id} is a {g} character but the voice sounds {'female' if g == 'male' else 'male'} "
                               f"(median pitch {f0:.0f} Hz)", start=first[1], scene=first[0], confidence=0.85, fix="revoice",
                               fix_args={"speaker": spk_id}, recommendation=f"redesign {spk_id}'s voice as a clearly {g} voice and re-voice all lines"))
    spk = [k for k in cent if k != "narrator"]
    for i, a in enumerate(spk):
        for b in spk[i + 1:]:
            ma, fa = cent[a]; mb, fb = cent[b]
            cs = float(ma @ mb / (np.linalg.norm(ma) * np.linalg.norm(mb) + 1e-9))
            semis = abs(12 * np.log2((fa or 1) / (fb or 1)))
            if cs > 0.985 and semis < 1.5:
                res.append(Finding("voice", "HIGH", f"{a} and {b} sound almost identical (timbre {cs:.3f}, pitch Δ {semis:.1f} st)", confidence=0.6,
                                   recommendation="redesign one of the two voices"))
    return res


# ================================================================ 5b. ending: wrap-up + sign-off, not cut off
def check_ending(pr, cache, cfg):
    from .. import ending
    res = []
    last = pr.scenes[-1]; sid = last["id"]; props = pr.props[sid]
    t_end = pr.start[sid] + pr.dur[sid]
    for why in ([] if pr.script.get("no_outro") else ending.problems(pr.script)):   # show episodes end on their own joke
        res.append(Finding("ending", "CRITICAL", f"no proper ending: {why}", start=pr.start[sid], scene=sid, confidence=0.95, fix="add_outro",
                           recommendation="end with a narrator wrap-up (key takeaway) and a thanks-for-watching / subscribe sign-off"))
    lines = pr.lines.get(sid) or []
    if lines:
        tail = pr.dur[sid] - lines[-1]["end"]
        if tail < 0.8:
            res.append(Finding("ending", "HIGH", f"video ends abruptly {tail:.2f}s after the last word (needs >=0.8s to breathe)",
                               start=pr.start[sid] + lines[-1]["end"], scene=sid, confidence=0.8, fix="add_outro"))
    try:
        vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", pr.video],
                                  capture_output=True, text=True).stdout.strip())
        if vd < t_end - 0.3:
            res.append(Finding("ending", "CRITICAL", f"final video is cut short: {vd:.1f}s but the scenes run to {t_end:.1f}s",
                               start=vd, scene=sid, confidence=0.95, fix="remaster"))
    except ValueError:
        pass
    return res


# ================================================================ 6. OCR: on-screen text, charts, maps, beats, titles, captions, garbled text
def _ocr_cached(cache, key, img):
    hit = cache.get("ocr", key)
    if hit is None:
        hit = [(t, list(b)) for t, b in M.ocr(img)]; cache.put("ocr", key, hit)
    return hit


def _fmt_chart(v, unit):
    cur = unit in ("$", "€", "£", "¥", "₹")
    u = "%" if unit.strip().lower() in ("%", "percent", "pct") else (" " + unit.strip().lower()) if re.match(r"^[a-z]", unit.strip(), re.I) else unit
    num = f"{v:,.1f}" if v % 1 else f"{int(v):,}"
    return f"{unit}{num}" if cur else f"{num}{u}"


def _found(expected, texts, th=0.8):
    e = " ".join(norm_words(expected))
    if not e: return True
    for t in texts:
        n = " ".join(norm_words(t))
        if e in n or difflib.SequenceMatcher(None, e, n).ratio() >= th: return True
    joined = " ".join(" ".join(norm_words(t)) for t in texts)
    if e in joined: return True
    toks, n = joined.split(), len(e.split())
    for k in range(max(1, n - 1), n + 2):
        for i in range(len(toks) - k + 1):
            if difflib.SequenceMatcher(None, e, " ".join(toks[i:i + k])).ratio() >= th: return True
    return False


def check_ocr(pr, cache, cfg):
    res = []
    for s in pr.scenes:
        sid, kind = s["id"], s["kind"]; props = pr.props[sid]; d = pr.dur[sid]; t0 = pr.start[sid]
        rh = pr.render_hash(sid)
        def grab(tt, tag):
            img = frame_at(pr.render[sid], min(d - 0.05, max(0, tt)))
            return [] if img is None else _ocr_cached(cache, f"{rh}:{tag}:{tt:.2f}", Image.fromarray(img))
        if kind == "title_card" and props.get("titleText"):
            r = grab(d * 0.75, "title"); txt = [t for t, b in r if b[3] < 880]
            if not _found(props["titleText"], txt, 0.75):
                res.append(Finding("text", "HIGH", f"title card text not rendered correctly: expected '{props['titleText']}', read {txt}", start=t0, scene=sid))
        if kind == "chart" and props.get("chart"):
            c = props["chart"]; r = grab(d - 0.1, "chart"); txt = [t for t, b in r if b[3] < 900]
            if c.get("mode") in ("stats", "timeline") and c.get("items"):
                exp = ([c["title"]] if c.get("title") else []) + [it["value"] for it in c["items"]] + [it["label"] for it in c["items"]]
            else:
                exp = ([c["title"]] if c.get("title") else []) + list(c["labels"]) + [_fmt_chart(v, c.get("unit", "")) for v in c["values"]]
            miss = [e for e in exp if not _found(e, txt, 0.75)]
            if miss:
                res.append(Finding("text", "MEDIUM" if len(miss) < len(exp) / 2 else "HIGH", f"chart text missing/misread: {miss} (read {txt})",
                                   start=t0 + d - 0.1, scene=sid, confidence=0.7, recommendation="check chart labels/values in script.json"))
        if kind == "map" and props.get("map"):
            mp = props["map"]; r = grab(d - 0.1, "map"); txt = [t for t, b in r if b[3] < 900]
            exp = ([mp["label"]] if mp.get("label") else []) + [p["name"] for p in mp.get("places", [])]
            miss = [e for e in exp if not _found(e, txt, 0.7)]
            if miss:
                res.append(Finding("text", "MEDIUM", f"map labels not readable: {miss}", start=t0 + d - 0.1, scene=sid, confidence=0.6,
                                   recommendation="labels may overlap; check map scene"))
        for b in (props.get("beats", []) if kind != "title_card" else []):    # renderer hides beats on chapter cards
            tb = b["atMs"] / 1000 + 0.9
            if tb > d - 0.1: continue
            r = grab(tb, f"beat{b['atMs']}"); txt = [t for t, bb in r if bb[3] < 880]
            if not _found(b["text"], txt, 0.7):
                res.append(Finding("text", "MEDIUM", f"on-screen keyword '{b['text']}' not readable (read {txt})", start=t0 + tb, scene=sid, confidence=0.6))
        if kind == "hero" and os.path.exists(os.path.join(pr.dir, "hero", f"{sid}.mp4")):
            src = os.path.join(pr.dir, "hero", f"{sid}.mp4"); sd = __import__("studio.qc.core", fromlist=["probe_dur"]).probe_dur(src)
            def grab(tt, tag, src=src, sd=sd):
                img = frame_at(src, min(sd - 0.05, max(0, tt * sd / max(d, 0.01))))
                return [] if img is None else _ocr_cached(cache, f"{file_hash(src)}:{tag}", Image.fromarray(img))
            allowed = set(norm_words(" ".join(l["text"] for l in props.get("lines", [])) + " " + " ".join(b["text"] for b in props.get("beats", []))))
            junk = set()
            for frac in (0.2, 0.6, 0.95):
                for t, bb in grab(d * frac, f"hero{frac}"):
                    for w in norm_words(t):
                        if len(w) > 18 or len(set(w)) / max(1, len(w)) < 0.35: continue        # OCR hallucination on textures
                        if w not in allowed and not is_word(w) and len(w) >= 3: junk.add(w)
            if junk:
                res.append(Finding("visual", "HIGH", f"garbled text inside the AI image: {sorted(junk)[:8]}", start=t0, end=t0 + d, scene=sid,
                                   fix="regen_hero", fix_args={"scene": sid}, recommendation="regenerate the hero shot without text"))
        # captions: rendered words must stay separate and inside the frame
        for k, page in enumerate(_pages(props.get("words", []))[:3]):
            tm = (page[0]["startMs"] + page[-1]["endMs"]) / 2000
            if tm > d - 0.1: continue
            r = grab(tm, f"cap{k}"); txt = [(t, bb) for t, bb in r if bb[1] > 850 and not t.strip().upper().startswith("SOURCE")]
            if not txt: continue
            joined = " ".join(norm_words(" ".join(t for t, _ in txt)))
            ws = [re.sub(r"[^a-z0-9']", "", w["text"].lower()) for w in page]
            merged = [f"{a}{b}" for a, b in zip(ws, ws[1:]) if a and b and len(a + b) > 6 and f"{a}{b}" in joined.split()]
            if merged:
                res.append(Finding("subtitle", "MEDIUM", f"caption words run together: {merged}", start=t0 + tm, scene=sid, confidence=0.7))
            if any(bb[0] < 15 or bb[2] > W - 15 for _, bb in txt):
                res.append(Finding("subtitle", "HIGH", "caption runs off the edge of the screen", start=t0 + tm, scene=sid))
    # backgrounds: big garbled text painted into a background
    for bg in sorted({p["background"] for p in pr.props.values() if p.get("kind") == "stage" and p.get("background")}):
        f = proj_path(pr.dir, bg)
        if not os.path.exists(f): continue
        r = _ocr_cached(cache, file_hash(f) + ":bg", f)
        big = [t for t, bb in r if bb[3] - bb[1] > 38 and any(not is_word(w) and len(w) >= 3 for w in norm_words(t))]
        if big:
            env = next((s.get("environment") for s in pr.scenes if pr.props[s["id"]].get("background") == bg), None)
            res.append(Finding("continuity", "MEDIUM", f"garbled large text in background {os.path.basename(bg)}: {big[:5]}", confidence=0.7,
                               scene=next((s["id"] for s in pr.scenes if pr.props[s["id"]].get("background") == bg), None),
                               fix="repaint_text", fix_args={"env": env, "boxes": [list(bb) for t, bb in r if t in big]}))
    return res


def _pages(words):
    pages, cur, ln = [], [], 0
    for w in words:
        prev = cur[-1] if cur else None
        if cur and ((prev["speaker"] != w["speaker"]) or (w["startMs"] - prev["endMs"] > 350) or ln + len(w["text"]) > 38):
            pages.append(cur); cur, ln = [], 0
        cur.append(w); ln += len(w["text"]) + 1
        if re.search(r"[.!?]$", w["text"]) and ln > 18: pages.append(cur); cur, ln = [], 0
    if cur: pages.append(cur)
    return pages


# ================================================================ 7. physical positioning / grounding
FURNITURE = "table. desk. chair. sofa. armchair. bench. counter. bookshelf. cabinet. podium. bed. bar counter."
FLOORS = "floor. ground. pavement. street. carpet. rug. grass. stage floor."


def bg_analysis(pr, cache, bg):
    """Segment a background once: floor mask + furniture masks with their floor-contact line (depth cue)."""
    f = proj_path(pr.dir, bg); h = file_hash(f)
    npz = os.path.join(pr.dir, "work", f"qc_bg_{h}.npz")
    hit = cache.get("bg", h)
    if hit is not None and os.path.exists(npz):
        z = np.load(npz); return hit, z["floor"], [z[f"m{i}"] for i in range(len(hit["obstacles"]))]
    im = Image.open(f).convert("RGB").resize((W, H))
    det = M.detect(im, FURNITURE, 0.33)
    obs = [(s, l, b) for s, l, b in det if (b[2] - b[0]) * (b[3] - b[1]) < 0.6 * W * H]
    # non-max suppression across labels (table/desk/counter often overlap)
    keep = []
    for s, l, b in obs:
        if all(_iou(b, k[2]) < 0.6 for k in keep): keep.append((s, l, b))
    masks = M.segment(im, [b for _, _, b in keep]) if keep else []
    fl = [b for s, l, b in M.detect(im, FLOORS, 0.2) if b[3] > H * 0.6]
    floor = np.zeros((H, W), bool)
    for m in (M.segment(im, fl[:2]) if fl else []): floor |= m
    for m in masks: floor &= ~m
    info = {"floor_found": bool(floor.mean() > 0.02), "obstacles": []}
    for (s, l, b), m in zip(keep, masks):
        ys = np.where(m.any(1))[0]
        info["obstacles"].append({"label": l, "score": round(s, 2), "box": [round(v) for v in b], "contact_y": int(ys.max()) if len(ys) else int(b[3])})
    np.savez_compressed(npz, floor=floor, **{f"m{i}": m for i, m in enumerate(masks)})
    cache.put("bg", h, info)
    return info, floor, masks


def _iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - ix * iy
    return ix * iy / u if u else 0


_SIL = {}


def silhouette(pr, pz, x_center, feet_y, flip=False):
    """Character alpha mask placed in world coordinates (H x W bool) + feet points."""
    path = proj_path(pr.dir, pz["img"])
    if path not in _SIL:
        _SIL[path] = np.asarray(Image.open(path).convert("RGBA").split()[-1]) > 128
    a = _SIL[path]
    th = int(H * CHAR_H); w = max(1, int(pz["w"] * th / pz["h"]))
    m = np.asarray(Image.fromarray(a.astype(np.uint8) * 255).resize((w, th), Image.NEAREST)) > 0
    if flip: m = m[:, ::-1]
    out = np.zeros((H, W), bool)
    x0 = int(x_center - w / 2); y0 = int(feet_y - th)
    sx0, sy0 = max(0, -x0), max(0, -y0); dx0, dy0 = max(0, x0), max(0, y0)
    ww, hh = min(w - sx0, W - dx0), min(th - sy0, H - dy0)
    if ww > 0 and hh > 0: out[dy0:dy0 + hh, dx0:dx0 + ww] = m[sy0:sy0 + hh, sx0:sx0 + ww]
    rows = np.where(m.any(1))[0]
    bottom = rows.max() if len(rows) else th - 1
    feet_cols = np.where(m[max(0, bottom - int(th * 0.03)):bottom + 1].any(0))[0]
    feet = [(x0 + int(c), y0 + int(bottom)) for c in feet_cols[:: max(1, len(feet_cols) // 12)]] if len(feet_cols) else []
    return out, feet


def grounding_eval(pr, cache, s, layout=None):
    """Evaluate (or, with a candidate layout {char: x}, simulate) the physical placement of every cast member."""
    props = pr.props[s["id"]]
    if props.get("kind") != "stage" or not props.get("background"): return [], None
    info, floor, masks = bg_analysis(pr, cache, props["background"])
    cast = [dict(c, x=(layout or {}).get(c["char"], c.get("x"))) for c in props["cast"]]
    lines = props["lines"]
    times = sorted({round((l["start"] + l["end"]) / 2, 2) for l in lines} | {0.2})
    probs = []
    for m in cast:
        poses = {}
        for t in times:
            st = state_at(m, cast, lines, t); poses.setdefault((st["pose"], st["flip"]), t)
        for (pose, flip), t in poses.items():
            pz = m["poses"][pose]; cx = W * pos_x(m)
            sil, feet = silhouette(pr, pz, cx, H * FEET_Y, flip)
            area = sil.sum() or 1
            for o, om in zip(info["obstacles"], masks):
                if o["contact_y"] >= H * FEET_Y - 12:          # object stands closer to the camera than the character
                    ov = (sil & om).sum() / area
                    if ov > 0.03:
                        probs.append(("front", m["char"], pose, t, f"{m['char']} ({pose}) is drawn inside/through the {o['label']} that stands in front of them ({ov:.0%} overlap)"))
            if feet:
                fy = [min(H - 1, y + 3) for _, y in feet]; fx = [min(W - 1, max(0, x)) for x, _ in feet]
                on_obj = [o["label"] for o, om in zip(info["obstacles"], masks) if np.mean([om[y, x] for x, y in zip(fx, fy)]) > 0.5]
                if on_obj:
                    probs.append(("standing_on", m["char"], pose, t, f"{m['char']}'s feet are on the {on_obj[0]}, not on the floor"))
                elif info["floor_found"]:
                    band = [floor[max(0, y - 6):min(H, y + 8), max(0, x - 3):x + 4].any() for x, y in zip(fx, fy)]
                    if np.mean(band) < 0.4:
                        probs.append(("off_floor", m["char"], pose, t, f"{m['char']}'s feet are not on the floor surface (floating / against the wall)"))
                else:
                    probs.append(("floor_unknown", m["char"], pose, t, "floor not detected"))
    # character / character intersection (closest moment = all poses at the same time)
    for t in times:
        sils = []
        for m in cast:
            st = state_at(m, cast, lines, t); sils.append((m["char"], silhouette(pr, m["poses"][st["pose"]], W * pos_x(m), H * FEET_Y, st["flip"])[0]))
        for i in range(len(sils)):
            for j in range(i + 1, len(sils)):
                ov = (sils[i][1] & sils[j][1]).sum() / max(1, min(sils[i][1].sum(), sils[j][1].sum()))
                if ov > 0.03: probs.append(("chars", sils[i][0] + "+" + sils[j][0], "", t, f"{sils[i][0]} and {sils[j][0]} intersect ({ov:.0%})"))
    return probs, info


def check_grounding(pr, cache, cfg):
    res, unknown = [], []
    for s in pr.scenes:
        probs, info = grounding_eval(pr, cache, s)
        seen = set()
        for kind, who, pose, t, desc in probs:
            if (kind, who) in seen: continue
            seen.add((kind, who))
            tt = pr.start[s["id"]] + t
            if kind == "floor_unknown":
                unknown.append((s["id"], who)); continue
            sev = "HIGH" if kind in ("front", "standing_on", "off_floor") else "MEDIUM"
            res.append(Finding("physical", sev, desc, start=pr.start[s["id"]], end=pr.start[s["id"]] + pr.dur[s["id"]], scene=s["id"],
                               fix="reposition", fix_args={"scene": s["id"], "env": s.get("environment")},
                               recommendation="move the character to clear floor; if there is none, regenerate the background with open floor"))
    return res, unknown


# ================================================================ 8. lip-sync (measured on the rendered frames)
def _mouth_templates(pr, pz):
    """Gray crops of the closed / mid / open mouth drawings of one pose around the mouth, in pose-image pixels."""
    key = pz["img"]
    if key in _TPL: return _TPL[key]
    mb = pz["mouth"]; W0, H0 = pz["w"], pz["h"]
    x0, x1 = (mb["x"] - mb["w"] * 0.6) * W0, (mb["x"] + mb["w"] * 1.6) * W0
    y0, y1 = (mb["y"] - mb["h"] * 1.5) * H0, (mb["y"] + mb["h"] * 3.5) * H0
    box = tuple(int(round(v)) for v in (max(0, x0), max(0, y0), min(W0, x1), min(H0, y1)))
    full = {}
    for k, rel in [("closed", pz["img"])] + list((pz.get("talk") or {}).items()):
        im = Image.open(proj_path(pr.dir, rel)).convert("RGBA")
        bg = Image.new("RGBA", im.size, (200, 200, 200, 255)); bg.alpha_composite(im)
        full[k] = np.asarray(bg.convert("L"), np.float32)
    if "open" in full and full["open"].shape == full["closed"].shape:
        # the detected mouth box can be wrong (facepalm, side views) -> use where the closed and open drawings really differ
        import cv2
        d = (np.abs(full["open"] - full["closed"]) > 40).astype(np.uint8)
        d = cv2.morphologyEx(d, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(d)
        if n > 1:
            i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            bx, by, bw, bh, area = st[i]
            if area > 30:
                px, py = max(6, int(bw * 0.3)), max(6, int(bh * 0.3))
                box = (max(0, bx - px), max(0, by - py), min(W0, bx + bw + px), min(H0, by + bh + py))
    tpl = {k: v[box[1]:box[3], box[0]:box[2]] for k, v in full.items()}
    _TPL[key] = (box, tpl)
    return _TPL[key]


_TPL = {}


def check_lipsync(pr, cache, cfg):
    """Identify, frame by frame, WHICH mouth drawing (closed / mid / open) is on screen for every character by matching the
    rendered pixels against that character's own mouth frames; compare with who is speaking and the expected visemes."""
    import cv2
    res = []
    fps = cfg["lipsync_fps"]
    for s in pr.scenes:
        sid = s["id"]; props = pr.props[sid]
        if props.get("kind") != "stage" or not props.get("cast"): continue
        lines = props["lines"]
        for m in props["cast"]:   # renderer falls back to an overlay mouth when a pose has no talk frames
            for l in lines:
                if l["speaker"] != m["char"]: continue
                st = state_at(m, props["cast"], lines, (l["start"] + l["end"]) / 2)
                if not m["poses"][st["pose"]].get("talk"):
                    res.append(Finding("lipsync", "HIGH", f"{m['char']} pose '{st['pose']}' has no mouth frames (overlay mouth = risk of double mouth)",
                                       start=pr.start[sid] + l["start"], scene=sid, fix="regen_talk", fix_args={"char": m["char"], "pose": st["pose"]}))
                    break
        key = pr.render_hash(sid) + ":lip6"
        obs = cache.get("lip", key)
        if obs is None:
            obs = {m["char"]: [] for m in props["cast"]}
            for t, img in frames(pr.render[sid], fps, (W, H)):
                cam = camera_at(props, t)
                for m in props["cast"]:
                    pl = char_place(m, props["cast"], lines, t); pz = pl["img"]
                    if not pz.get("mouth") or not pz.get("talk"): obs[m["char"]].append(None); continue
                    box, tpl = _mouth_templates(pr, pz)
                    u0, v0, u1, v1 = box[0] / pz["w"], box[1] / pz["h"], box[2] / pz["w"], box[3] / pz["h"]
                    pts = [to_screen(cam, pl["world"](u, v)) for u, v in ((u0, v0), (u1, v0), (u0, v1))]
                    # affine map pose-crop pixels -> screen; sample the rendered frame back into pose-crop space
                    tw, th_ = tpl["closed"].shape[1], tpl["closed"].shape[0]
                    src = np.float32([[0, 0], [tw, 0], [0, th_]]); dst = np.float32(pts)
                    if min(p[0] for p in pts) < 0 or min(p[1] for p in pts) < 0 or max(p[0] for p in pts) >= W or max(p[1] for p in pts) >= H:
                        obs[m["char"]].append(None); continue
                    Aff = cv2.getAffineTransform(src, dst)
                    patch = cv2.warpAffine(img, Aff, (tw, th_), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_AREA).astype(np.float32)
                    best = {}
                    for k, T_ in tpl.items():
                        # allow a few pixels of slack (sway / rounding): best shifted match
                        r = cv2.matchTemplate(cv2.copyMakeBorder(patch, 3, 3, 3, 3, cv2.BORDER_REPLICATE), T_, cv2.TM_SQDIFF_NORMED)
                        best[k] = float(r.min())
                    lab = min(best, key=best.get)
                    obs[m["char"]].append([lab, round(best["closed"], 4), round(best[lab], 4)])
            cache.put("lip", key, obs)
        # expected openness from the audio visemes
        def expected_open(m, t):
            l = next((l for l in lines if l["start"] <= t < l["end"] and l["speaker"] == m["char"]), None)
            if not l: return False
            v = next((c["value"] for c in l.get("visemes", []) if c["start"] <= t < c["end"]), "X")
            return v not in ("X", "A")
        for m in props["cast"]:
            o = obs.get(m["char"], [])
            def is_open(x): return x is not None and x[0] != "closed" and x[2] < x[1] * 0.85
            def ratio(t0, t1):
                v = [x for i, x in enumerate(o) if x is not None and t0 <= i / fps < t1]
                return (sum(1 for x in v if is_open(x)) / len(v)) if len(v) >= 4 else None
            for l in lines:
                r = ratio(l["start"] + 0.1, l["end"] - 0.05)
                if r is None: continue
                t = pr.start[sid] + l["start"]
                if l["speaker"] == m["char"] and r < 0.12 and l["end"] - l["start"] > 0.8:
                    res.append(Finding("lipsync", "HIGH", f"{m['char']}'s mouth stays closed while speaking (open in {r:.0%} of frames)", start=t,
                                       end=pr.start[sid] + l["end"], scene=sid, fix="regen_talk",
                                       fix_args={"char": m["char"], "pose": state_at(m, props["cast"], lines, (l['start'] + l['end']) / 2)["pose"]}))
                if l["speaker"] != m["char"] and r > 0.08:
                    res.append(Finding("lipsync", "HIGH", f"{m['char']}'s mouth opens while {l['speaker']} is talking ({r:.0%} of frames)", start=t,
                                       end=pr.start[sid] + l["end"], scene=sid, recommendation="listener must keep the closed mouth"))
                if l["speaker"] == m["char"]:
                    pairs = [(is_open(x), expected_open(m, i / fps)) for i, x in enumerate(o) if x is not None and l["start"] <= i / fps < l["end"]]
                    if len(pairs) >= 8:
                        agree = sum(1 for a, b in pairs if a == b) / len(pairs)
                        if agree < 0.6:
                            res.append(Finding("lipsync", "MEDIUM", f"{m['char']}'s mouth shapes match the audio in only {agree:.0%} of frames", start=t,
                                               end=pr.start[sid] + l["end"], scene=sid, confidence=0.7))
            for x, y in zip(lines, lines[1:]):
                r = ratio(x["end"] + 0.15, y["start"] - 0.05)
                if r is not None and y["start"] - x["end"] > 0.5 and r > 0.15:
                    res.append(Finding("lipsync", "MEDIUM", f"{m['char']}'s mouth moves when nobody is speaking", start=pr.start[sid] + x["end"],
                                       end=pr.start[sid] + y["start"], scene=sid, confidence=0.7))
    return res


# ================================================================ 9. camera / composition (analytic, every line)
def check_camera(pr, cache, cfg):
    res = []
    for s in pr.scenes:
        sid = s["id"]; props = pr.props[sid]
        if props.get("kind") != "stage": continue
        for l in props["lines"]:
            t = (l["start"] + l["end"]) / 2; cam = camera_at(props, t)
            for m in props["cast"]:
                pl = char_place(m, props["cast"], props["lines"], t)
                hx, hy = to_screen(cam, pl["world"](0.5, 0.0)); fx, fy = to_screen(cam, pl["world"](0.5, 1.0))
                x0 = to_screen(cam, (pl["box"][0], 0))[0]; x1 = to_screen(cam, (pl["box"][2], 0))[0]
                tt = pr.start[sid] + t
                if hy < -4:
                    res.append(Finding("camera", "HIGH", f"{m['char']}'s head is cut off at the top", start=tt, scene=sid))
                if l.get("shot") != "closeup" and fy > H + 2:
                    res.append(Finding("camera", "MEDIUM", f"{m['char']}'s feet are cut off", start=tt, scene=sid))
                if l.get("shot") != "closeup" and (x0 < -0.25 * (x1 - x0) or x1 > W + 0.25 * (x1 - x0)):
                    res.append(Finding("camera", "MEDIUM", f"{m['char']} is cropped at the frame edge", start=tt, scene=sid, confidence=0.7))
                # beats in the top band must not cover a face
                for b in props.get("beats", []):
                    bt = b["atMs"] / 1000
                    if bt <= t < bt + 2.6 and l.get("shot") != "closeup" and hy < 175:
                        bw = min(700, 60 * len(b["text"])); bx0, bx1 = W / 2 - bw / 2, W / 2 + bw / 2
                        if bx0 < hx < bx1:
                            res.append(Finding("camera", "MEDIUM", f"keyword '{b['text']}' covers {m['char']}'s face", start=tt, scene=sid))
    return _uniq(res)


def check_animation(pr, cache, cfg):
    res = []
    for s in pr.scenes:
        props = pr.props[s["id"]]
        if props.get("kind") != "stage": continue
        for m in props["cast"]:
            seq, last = [], None
            for i in range(int(pr.dur[s["id"]] * 10)):
                p = state_at(m, props["cast"], props["lines"], i / 10)["pose"]
                if p != last: seq.append(i / 10); last = p
            for a, b in zip(seq, seq[2:]):
                if b - a < 1.2:
                    res.append(Finding("animation", "LOW", f"{m['char']} switches pose 3 times within {b - a:.1f} s (jerky)", start=pr.start[s["id"]] + a,
                                       scene=s["id"], confidence=0.6)); break
    return res


def _uniq(rows):
    seen, out = set(), []
    for f in rows:
        k = (f.scene, f.description)
        if k not in seen: seen.add(k); out.append(f)
    return out
