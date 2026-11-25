"""Voices v2: one designed voice per speaker (narrator + every character), cloned for consistency; per-line TTS,
voice clean-up + loudness matching, tight scene assembly, word timings and per-line visemes."""
import glob, gc, hashlib, json, os, re, subprocess
import numpy as np, soundfile as sf
from . import config as C, pace

PRON_FILE = os.path.join(C.VOICE_LIB, "pronunciations.json")
REF_TEXT = ("Okay, here's the thing nobody tells you. It's not the big decisions that get you, it's the small ones, "
            "made fast, by people who really should have read the email first.")
GAP = 0.16          # seconds between lines of different speakers (snappy, but not overlapping)
GAP_SAME = 0.10


def _pron(text):
    d = json.load(open(PRON_FILE)) if os.path.exists(PRON_FILE) else {}
    for k, v in d.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text)
    return text


def _trim(wav, sr, pad=0.06):
    a = np.abs(wav); thr = max(a.max() * 0.025, 1e-4)
    idx = np.where(a > thr)[0]
    if not len(idx): return wav
    return wav[max(0, idx[0] - int(sr * 0.02)): min(len(wav), idx[-1] + int(sr * pad))]


def _clean(src, dst):
    """Voice chain: remove rumble, gentle de-click/compress, match loudness of every line (-19 LUFS), 48 kHz mono."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af",
                    "highpass=f=75,lowpass=f=14500,adeclick,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
                    "loudnorm=I=-19:TP=-2:LRA=7", "-ar", "48000", "-ac", "1", dst], check=True)


def voice_profiles(sc):
    """narrator + characters -> {speaker_id: {name, design}}"""
    prof = {"narrator": dict(C.NARRATOR)}
    for c in sc["characters"]:
        prof[c["id"]] = {"name": c["id"], "design": f"{c['voice']} Speaking naturally in English, expressive and conversational.",
                         "language": "English", **({"tts": c["tts"]} if c.get("tts") else {})}
    nv = sc.get("narrator_voice")         # a show can make one of its characters the narrator (same voice on and off screen)
    if nv in prof and nv != "narrator": prof["narrator"] = dict(prof[nv])
    return prof


MALE_MAX, FEMALE_MIN = 160.0, 165.0     # median speaking pitch (Hz): adult men ~85-155, women ~165-255


def gender(design):
    """'male' / 'female' / None from a voice description."""
    d = (design or "").lower()
    if re.search(r"\b(female|woman|girl|lady|she|her)\b", d): return "female"
    if re.search(r"\b(male|man|guy|boy|he|his|narrator)\b", d): return "male"
    return None


def pitch(wav_or_array, sr=None):
    """Median voiced F0 in Hz."""
    import librosa
    y, sr = (librosa.load(wav_or_array, sr=16000) if isinstance(wav_or_array, str) else (librosa.resample(np.asarray(wav_or_array, np.float32), orig_sr=sr, target_sr=16000), 16000))
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr)
    return float(np.nanmedian(f0)) if np.any(~np.isnan(f0)) else 0.0


def gender_ok(g, f0, tol=0.0):
    return not g or not f0 or (f0 <= MALE_MAX + tol if g == "male" else f0 >= FEMALE_MIN - tol)


_REINFORCE = {"male": " IMPORTANT: this is clearly an adult MAN's voice — low-to-mid male pitch, masculine chest resonance, never a female or child voice.",
              "female": " IMPORTANT: this is clearly an adult WOMAN's voice — female pitch and timbre, never a male voice."}


def _male_safe(design, g):
    # words like "bright/high pitch" push a male design into the female range
    return re.sub(r"\b(bright|high|higher|slightly higher)\s+pitch\b", "mid pitch", design, flags=re.I) if g == "male" else design


def ensure_voices(profiles, force=()):
    """Design each missing voice once (VoiceDesign) and keep it in the library forever.
    The designed voice must match the character's gender by pitch; otherwise it is redesigned (up to 5 tries, best kept)."""
    missing = [k for k, p in profiles.items() if k in force or not os.path.exists(os.path.join(C.VOICE_LIB, p["name"], "reference.wav"))]
    if not missing: return
    import torch
    from qwen_tts import Qwen3TTSModel
    m = Qwen3TTSModel.from_pretrained(C.TTS_DESIGN, device_map="cuda:0", dtype=torch.bfloat16)
    for k in missing:
        p = profiles[k]; vdir = os.path.join(C.VOICE_LIB, p["name"]); os.makedirs(vdir, exist_ok=True)
        g = gender(p["design"]); best = None
        for attempt in range(6):
            instr = _male_safe(p["design"], g) + (_REINFORCE.get(g, "") if attempt or k in force else "")
            if attempt >= 2 and g:          # model keeps missing: rewrite the design around the gender, keep accent/pace words
                core = re.sub(r"\b(\d+|[a-z]+(-|\s)?(pitch|timbre|tone)|bright|high|higher|young|youthful|light|soft|nasal|optimistic|"
                              r"male|female|man|woman|early|late|\d+s)\b,?", "", p["design"], flags=re.I)
                core = re.sub(r"\s*,\s*(,\s*)+", ", ", core).strip(" ,.")
                instr = ("A man in his late thirties with a deep, warm baritone voice and clearly masculine low pitch. " if g == "male" else
                         "A woman in her thirties with a clear, natural female voice and feminine pitch. ") + core + "."
            wavs, sr = m.generate_voice_design(text=REF_TEXT, language=p.get("language", "English"), instruct=instr)
            w = _trim(wavs[0], sr); f0 = pitch(w, sr)
            score = 0 if gender_ok(g, f0) else abs(f0 - (MALE_MAX if g == "male" else FEMALE_MIN))
            if best is None or score < best[0]: best = (score, w, sr, f0, instr)
            print(f"voice {k}: design try {attempt + 1} pitch {f0:.0f} Hz ({g or '?'}) {'ok' if score == 0 else 'WRONG GENDER'}")
            if score == 0: break
        score, w, sr, f0, instr = best
        if score and g and f0:              # last resort: small natural pitch shift (<= 3 semitones) into the right range
            import librosa
            target = MALE_MAX - 8 if g == "male" else FEMALE_MIN + 10
            st = float(np.clip(12 * np.log2(target / f0), -3, 3))
            w = librosa.effects.pitch_shift(np.asarray(w, np.float32), sr=sr, n_steps=st); f0 = pitch(w, sr)
            print(f"voice {k}: pitch-shifted {st:+.1f} st -> {f0:.0f} Hz")
        sf.write(os.path.join(vdir, "reference.wav"), w, sr)
        open(os.path.join(vdir, "reference.txt"), "w").write(REF_TEXT)
        prev = json.load(open(os.path.join(vdir, "profile.json"))) if os.path.exists(os.path.join(vdir, "profile.json")) else {}
        json.dump(dict(p, instruct=instr, f0=round(f0, 1), gender=g, redesigns=prev.get("redesigns", 0)),
                  open(os.path.join(vdir, "profile.json"), "w"), indent=1)
    del m; gc.collect(); torch.cuda.empty_cache()


def check_library(profiles):
    """Speakers whose stored library voice does not match their gender (pitch measured once, cached in profile.json)."""
    bad = []
    for k, p in profiles.items():
        vdir = os.path.join(C.VOICE_LIB, p["name"]); ref = os.path.join(vdir, "reference.wav"); pj = os.path.join(vdir, "profile.json")
        if not os.path.exists(ref): continue
        meta = json.load(open(pj)) if os.path.exists(pj) else {}
        if "f0" not in meta:
            meta["f0"] = round(pitch(ref), 1); json.dump(meta, open(pj, "w"), indent=1)
        if meta.get("force_redesign") or not gender_ok(gender(p["design"]), meta["f0"], tol=10): bad.append(k)
    return bad


_SPK_TAG = {}          # speaker -> voice engine tag (set by narrate), so a voice change never reuses old cached lines


def _line_key(speaker, text):
    tag = _SPK_TAG.get(speaker) or ("cb" if ENGINE == "chatterbox" else "")
    return hashlib.md5((f"{speaker}|{text}" + (f"|{tag}" if tag else "")).encode()).hexdigest()[:10]


def line_pitch_wrong(sc, out_dir, profiles, n=5):
    """Speakers whose GENERATED lines sound like the wrong gender (median pitch of up to n lines, cached per line)."""
    cache_f = os.path.join(out_dir, "pitch_cache.json")
    cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    per = {}
    for s in sc["scenes"]:
        for ln in s["lines"]:
            key = _line_key(ln["speaker"], ln["text"]); f = os.path.join(out_dir, "lines", key + ".wav")
            if not os.path.exists(f) or len(per.get(ln["speaker"], [])) >= n: continue
            if key not in cache: cache[key] = pitch(f)
            if cache[key]: per.setdefault(ln["speaker"], []).append(cache[key])
    json.dump(cache, open(cache_f, "w"))
    return [k for k, v in per.items() if k in profiles and not gender_ok(gender(profiles[k]["design"]), float(np.median(v)), tol=10)]


ENGINE = os.environ.get("TTS_ENGINE") or ("chatterbox" if os.path.exists(os.path.join(C.ROOT, ".venv-tts", "bin", "python")) else "qwen")


def _qwen_custom(todo, profiles):
    """Speakers with tts.engine == 'qwen_custom' (Ryan = preset 'Ryan'): fixed built-in identity + a written acting direction per
    line (library/voices/<id>/delivery.json). 3 takes per line; studio/tts_pick.py keeps the take closest to the character's anchor
    recording that says every word and moves the pitch the way the emotion needs."""
    import subprocess, tempfile, torch
    from qwen_tts import Qwen3TTSModel
    jobs = []
    by_model = {}
    for spk in todo: by_model.setdefault(profiles[spk]["tts"]["model"], []).append(spk)
    for model, spks in by_model.items():
      m = Qwen3TTSModel.from_pretrained(os.path.join(C.ROOT, model), device_map="cuda:0", dtype=torch.bfloat16)
      for spk in spks:
        items = todo[spk]
        t = profiles[spk]["tts"]; vdir = os.path.join(C.VOICE_LIB, profiles[spk]["name"]); os.makedirs(vdir, exist_ok=True)
        dl = json.load(open(os.path.join(vdir, "delivery.json"))) if os.path.exists(os.path.join(vdir, "delivery.json")) else {"profiles": {}, "emotion_to_profile": {}}
        design = t.get("engine") == "qwen_design"        # a voice made from a description: identity = design text + anchor pick
        clone = t.get("engine") == "qwen_clone"          # a voice cloned from ONE approved recording: identical timbre on every line
        if clone:
            cp = m.create_voice_clone_prompt(ref_audio=os.path.join(C.ROOT, t["ref_audio"]), ref_text=open(os.path.join(C.ROOT, t["ref_text"])).read().strip())
            gen = lambda text, instr: m.generate_voice_clone(text=text, language="English", voice_clone_prompt=cp)
        elif design:
            gen = lambda text, instr: m.generate_voice_design(text=text, language="English", instruct=(t["design"] + " " + instr).strip())
        else:
            gen = lambda text, instr: m.generate_custom_voice(text=text, language="English", speaker=t["speaker"], instruct=instr)
        anchor = os.path.join(C.ROOT, t["ref_audio"]) if clone else os.path.join(vdir, "anchor_design.wav" if design else f"anchor_{t['speaker']}.wav")
        if not os.path.exists(anchor):                     # the identity reference every take is compared against
            torch.manual_seed(1)
            w, sr = gen(REF_TEXT, dl["profiles"].get("normal", ""))
            sf.write(anchor, w[0], sr)
        for ln, f in items:
            prof = ln.get("delivery") or (ln.get("voice") if ln.get("voice") in dl["profiles"] else None) or dl["emotion_to_profile"].get(ln.get("emotion", "neutral"), "normal")
            direction = ln.get("direction") or dl["profiles"].get(prof, "")
            takes = []
            for k in range(6 if design else int(os.environ.get("VOICE_TAKES", 4))):            # clone: 4 takes differ only in delivery, never in voice            # a designed voice drifts more per take: more takes, closest to the anchor wins
                torch.manual_seed(int(hashlib.md5((ln["text"] + str(k)).encode()).hexdigest()[:8], 16))
                w, sr = gen(_pron(ln["text"].replace("*", "")), (t.get("base_direction", "") + " " + direction).strip())
                tf = f"{f}.take{k}.wav"; sf.write(tf, w[0], sr); takes.append(tf)
            jobs.append({"text": ln["text"].replace("*", ""), "emotion": ln.get("voice") or ln.get("emotion", "neutral"), "takes": takes, "anchor": anchor, "out": f + ".cb.wav",
                         "rate": dl.get("pace_words_per_sec", {}).get(prof, [0, 99])})
      del m; gc.collect(); torch.cuda.empty_cache()
    jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(jobs, jf); jf.close()
    subprocess.run([os.path.join(C.ROOT, ".venv-tts", "bin", "python"), os.path.join(C.ROOT, "studio", "tts_pick.py"), jf.name], check=True)
    for j in jobs:
        f = j["out"][:-len(".cb.wav")]
        if not os.path.exists(j["out"]): continue      # duplicate line text (same cache file) already handled by an earlier job
        w, sr = sf.read(j["out"], dtype="float32")
        raw = f + ".raw.wav"; sf.write(raw, _trim(w, sr), sr); _clean(raw, f); os.remove(raw); os.remove(j["out"])
        for tf in j["takes"]:
            if os.path.exists(tf): os.remove(tf)


def _chatterbox(todo, profiles):
    """Every line cloned from the speaker's ONE reference (fixed identity); emotion only changes delivery. Runs in .venv-tts.
    Speakers configured for another engine (tts.engine) are routed there."""
    import subprocess, tempfile
    qc = {k: v for k, v in todo.items() if profiles[k].get("tts", {}).get("engine") in ("qwen_custom", "qwen_design", "qwen_clone")}
    if qc: _qwen_custom(qc, profiles)
    todo = {k: v for k, v in todo.items() if k not in qc}
    if not todo: return
    jobs, outs = [], []
    for spk, items in todo.items():
        ref = os.path.join(C.VOICE_LIB, profiles[spk]["name"], "reference.wav")
        for ln, f in items:
            jobs.append({"text": _pron(ln["text"].replace("*", "")), "ref": ref, "emotion": ln.get("voice") or ln.get("emotion", "neutral"), "out": f + ".cb.wav"})
            outs.append(f)
    jf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(jobs, jf); jf.close()
    subprocess.run([os.path.join(C.ROOT, ".venv-tts", "bin", "python"), os.path.join(C.ROOT, "studio", "tts_cb.py"), jf.name], check=True)
    for j, f in zip(jobs, outs):
        w, sr = sf.read(j["out"], dtype="float32")
        raw = f + ".raw.wav"; sf.write(raw, _trim(w, sr), sr); _clean(raw, f); os.remove(raw); os.remove(j["out"])


def _pace_lines(files, texts):
    """Re-time every new line: breaths between sentences, beats on '...', no random pauses inside phrases (studio/pace.py)."""
    from faster_whisper import WhisperModel
    import torch, torchaudio
    try: m = WhisperModel("small.en", device="cuda", compute_type="float16")
    except Exception: m = WhisperModel("small.en", device="cpu", compute_type="int8")      # GPU busy (e.g. LTX running)
    for f in files:
        a, sr = sf.read(f, dtype="float32")
        a16 = torchaudio.functional.resample(torch.from_numpy(a), sr, 16000).numpy()
        segs, _ = m.transcribe(a16, word_timestamps=True, initial_prompt=texts[f], beam_size=5)
        asr = [(w.word, w.start, w.end) for seg in segs for w in seg.words]
        sw = texts[f].replace("*", "").split()
        if not asr or not sw: continue
        lw = align_words(sw, asr, len(a) / sr)
        sf.write(f, pace.pace(a, sr, lw), sr)
        for c in glob.glob(f.replace(".wav", ".words*.json")): os.remove(c)
    del m; gc.collect()


TEMPO_BASE = 2.95          # shared conversational tempo (words/second of actual speech) for EVERY character
TEMPO_EMO = {"excited": 1.15, "surprised": 1.0, "happy": 1.05, "confident": 1.02, "neutral": 1.0, "sarcastic": 0.95,
             "confused": 0.9, "worried": 1.03, "sad": 0.9, "angry": 1.05,
             "deadpan": 0.95, "dry": 0.97, "amused": 1.0, "curious": 0.98, "awkward": 0.93, "professional": 1.03, "concerned": 1.0,
             "tired": 0.9, "distracted": 0.95, "rationalising": 0.97, "fake_ill": 0.88, "formal": 1.0, "defeated": 0.88,
             "under_breath": 0.95, "earnest": 1.08, "research": 1.08, "deflated": 0.9}


def _match_tempo(items):
    """items: [(wav, text, emotion)]. Nudge each line toward one shared tempo (baseline x emotion), so all characters talk at a
    similar, natural pace: pitch-preserving WSOLA, at most -13%/+15%, pauses scale with the speech."""
    import subprocess
    for f, text, emo in items:
        a, sr = sf.read(f, dtype="float32")
        sil, _ = pace._silences(a, sr, 0.12)
        speech = max(0.3, len(a) / sr - sum(y - x for x, y in sil))
        words = len(re.findall(r"[A-Za-z0-9']+", text))
        if words < 3: continue                     # one- or two-word lines: leave the actor's timing alone
        rate = words / speech; target = TEMPO_BASE * TEMPO_EMO.get(emo, 1.0)
        k = max(0.87, min(1.15, target / rate))
        if abs(k - 1) < 0.04: continue
        tmp = f + ".tempo.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-af", f"atempo={k:.3f}", "-ar", str(sr), tmp], check=True)
        os.replace(tmp, f)
        for c in glob.glob(f.replace(".wav", ".words*.json")): os.remove(c)


def narrate(sc, out_dir, _round=0):
    """Generate every line (cached by speaker+text), clean it, assemble one wav + line timing per scene.
    Voices that come out as the wrong gender (library reference OR the actual lines) are redesigned and re-voiced (max 2 rounds)."""
    os.makedirs(os.path.join(out_dir, "lines"), exist_ok=True)
    profiles = voice_profiles(sc)
    for k, p in profiles.items():
        t = p.get("tts") or {}
        if t.get("engine") == "qwen_custom": _SPK_TAG[k] = f"qc_{t['speaker']}"
        if t.get("engine") == "qwen_design": _SPK_TAG[k] = "qd_" + hashlib.md5(t["design"].encode()).hexdigest()[:6]   # new voice = new cache
        if t.get("engine") == "qwen_clone": _SPK_TAG[k] = "ql_" + hashlib.md5(open(os.path.join(C.ROOT, t["ref_audio"]), "rb").read()).hexdigest()[:6]
    spoken = {ln["speaker"] for s in sc["scenes"] for ln in s["lines"]}
    locked = {k for k, p in profiles.items() if p.get("tts")}     # voices the user chose (show cast): never redesigned or re-voiced for 'gender'
    ref_bad = [k for k in check_library(profiles) if k in spoken and k not in locked] if _round < 2 else []
    line_bad = [k for k in line_pitch_wrong(sc, out_dir, profiles) if k in spoken and k not in locked] if _round < 2 else []
    redesign = set(ref_bad) | (set(line_bad) if _round > 0 else set())     # round 0: lines wrong but reference ok -> just re-voice
    wrong = sorted(redesign | set(line_bad))
    if wrong:
        print("voice: wrong gender ->", "redesign" if redesign else "", sorted(redesign), "re-voice", wrong)
        if redesign: ensure_voices({k: profiles[k] for k in redesign}, force=redesign)
        pc = os.path.join(out_dir, "pitch_cache.json")
        if os.path.exists(pc): os.remove(pc)
        for s in sc["scenes"]:
            for ln in s["lines"]:
                if ln["speaker"] in wrong:
                    for f in glob.glob(os.path.join(out_dir, "lines", _line_key(ln["speaker"], ln["text"]) + ".*")) + \
                             glob.glob(os.path.join(out_dir, s["id"] + ".words.json")): os.remove(f)
    todo = {}
    for s in sc["scenes"]:
        for ln in s["lines"]:
            f = os.path.join(out_dir, "lines", f"{_line_key(ln['speaker'], ln['text'])}.wav")
            if not os.path.exists(f): todo.setdefault(ln["speaker"], []).append((ln, f))
    if todo and ENGINE == "chatterbox":
        ensure_voices({k: profiles[k] for k in profiles})
        _chatterbox(todo, profiles)
    elif todo:
        ensure_voices({k: profiles[k] for k in profiles})
        import torch
        from qwen_tts import Qwen3TTSModel
        m = Qwen3TTSModel.from_pretrained(C.TTS_BASE, device_map="cuda:0", dtype=torch.bfloat16)
        groups = {}
        for spk, items in todo.items():
            vdir = os.path.join(C.VOICE_LIB, profiles[spk]["name"])
            for ln, f in items:            # emotion-specific reference (same voice, different delivery) when the library has one
                st = {"excited": "excited", "surprised": "excited", "sarcastic": "sarcastic"}.get(ln.get("emotion", ""), "")
                if st and not os.path.exists(os.path.join(vdir, f"ref_{st}.wav")): st = ""
                groups.setdefault((spk, st), []).append((ln, f))
        for (spk, st), items in groups.items():
            vdir = os.path.join(C.VOICE_LIB, profiles[spk]["name"])
            ra, rt = (os.path.join(vdir, f"ref_{st}.wav"), REF_TEXT) if st else (os.path.join(vdir, "reference.wav"), open(os.path.join(vdir, "reference.txt")).read())
            prompt = m.create_voice_clone_prompt(ref_audio=ra, ref_text=rt)
            for i in range(0, len(items), 8):
                batch = items[i:i + 8]
                wavs, sr = m.generate_voice_clone(text=[_pron(ln["text"].replace("*", "")) for ln, _ in batch], language=["English"] * len(batch),
                                                  voice_clone_prompt=prompt * len(batch))
                for (ln, f), w in zip(batch, wavs):
                    raw = f + ".raw.wav"; sf.write(raw, _trim(w, sr), sr); _clean(raw, f); os.remove(raw)
        del m; gc.collect(); torch.cuda.empty_cache()
    if todo:
        _pace_lines([f for items in todo.values() for _, f in items], {f: ln["text"] for items in todo.values() for ln, f in items})
        _match_tempo([(f, ln["text"].replace("*", ""), ln.get("voice") or ln.get("emotion", "neutral")) for items in todo.values() for ln, f in items])
        if _round < 1 and line_pitch_wrong(sc, out_dir, profiles):
            return narrate(sc, out_dir, _round + 1)
    # assemble scenes
    for s in sc["scenes"]:
        parts, timing, t, prev = [], [], 0.0, None
        for ln in s["lines"]:
            a, sr = sf.read(os.path.join(out_dir, "lines", f"{_line_key(ln['speaker'], ln['text'])}.wav"), dtype="float32")
            if prev is not None:
                g = pace.gap_between(prev, ln)          # conversational timing: questions, interruptions, joke beats
                parts.append(np.random.default_rng(len(parts)).normal(0, 2e-4, int(sr * g)).astype(np.float32)); t += g
            timing.append({"speaker": ln["speaker"], "start": round(t, 3), "end": round(t + len(a) / sr, 3), "text": ln["text"],
                           "key": _line_key(ln["speaker"], ln["text"])})
            parts.append(a); t += len(a) / sr; prev = ln
        hold = float(s.get("hold") or 0)          # silent visual beats (empty office, a held look): the scene lasts at least this long
        if hold > t:
            parts.append(np.zeros(int(48000 * (hold - t)), np.float32)); t = hold
        sf.write(os.path.join(out_dir, f"{s['id']}.wav"), np.concatenate(parts) if parts else np.zeros(4800, np.float32), 48000)
        json.dump(timing, open(os.path.join(out_dir, f"{s['id']}.lines.json"), "w"), indent=1)
        s["_dur"] = t


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align_words(script_words, asr, dur):
    """Give every SCRIPT word the time of the matching ASR word (difflib alignment on normalised tokens);
    unmatched script words are spread evenly between their matched neighbours."""
    import difflib
    from .qc.stage1 import norm_words   # spells out digits ("120" -> one hundred twenty), UK/US spelling, years
    # token level: one script word or one ASR word can be several tokens ("twenty-nine", "29.36")
    a, ai = [], []
    for i, w in enumerate(script_words):
        for tok in (norm_words(w) or [_norm(w)]): a.append(tok); ai.append(i)
    b, bt = [], []
    for w, s0, s1 in asr:
        toks = norm_words(w) or [_norm(w)]
        step = (s1 - s0) / len(toks)
        for k, tok in enumerate(toks): b.append(tok); bt.append((s0 + step * k, s0 + step * (k + 1)))
    t = [None] * len(script_words)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            i = ai[blk.a + k]; s0, s1 = bt[blk.b + k]
            t[i] = [s0, s1] if t[i] is None else [min(t[i][0], s0), max(t[i][1], s1)]
    i = 0
    while i < len(t):
        if t[i] is None:
            j = i
            while j < len(t) and t[j] is None: j += 1
            lo = t[i - 1][1] if i > 0 else (asr[0][1] if j == len(t) or t[j] is None else min(asr[0][1], t[j][0]))
            hi = t[j][0] if j < len(t) else max(lo + 0.2 * (j - i), asr[-1][2] if asr else dur)
            hi = max(hi, lo + 0.05 * (j - i))
            step = (hi - lo) / (j - i)
            for k in range(i, j): t[k] = [lo + step * (k - i), lo + step * (k - i + 1)]
            i = j
        else:
            i += 1
    return [[w, x[0], x[1]] for w, x in zip(script_words, t)]


def word_timings(sc, out_dir):
    """Word timestamps per line (ASR timing, script text), offset into scene time. Also flags emphasised words (*word*)."""
    from faster_whisper import WhisperModel
    import torch, torchaudio
    m = None
    for s in sc["scenes"]:
        out = os.path.join(out_dir, f"{s['id']}.words.json")
        lines = json.load(open(os.path.join(out_dir, f"{s['id']}.lines.json")))
        if os.path.exists(out) and json.load(open(out)).get("sig") == [l["key"] for l in lines] + ["w3"]:
            continue
        words = []
        for ln in lines:
            cache = os.path.join(out_dir, "lines", ln["key"] + ".words3.json")
            if os.path.exists(cache):
                lw = json.load(open(cache))
            else:
                if m is None: m = WhisperModel("small.en", device="cuda", compute_type="float16")
                a, sr = sf.read(os.path.join(out_dir, "lines", ln["key"] + ".wav"), dtype="float32")
                a16 = torchaudio.functional.resample(torch.from_numpy(a), sr, 16000).numpy()
                segs, _ = m.transcribe(a16, word_timestamps=True, initial_prompt=ln["text"], beam_size=5)
                asr = [w for seg in segs for w in seg.words]
                sw = ln["text"].split(); lw = []
                dur = len(a) / sr
                if asr:
                    lw = align_words(sw, [(w.word, w.start, w.end) for w in asr], dur)
                else:
                    lw = [[w, i * dur / len(sw), (i + 1) * dur / len(sw)] for i, w in enumerate(sw)]
                for x, y in zip(lw, lw[1:]):
                    y[1] = max(y[1], x[1] + 0.04); x[2] = max(x[1] + 0.04, min(x[2], y[1]))
                json.dump(lw, open(cache, "w"))
            for w, a0, a1 in lw:
                emph = "*" in w or bool(re.match(r"^[\$€£]?\d", w))
                words.append({"text": w.replace("*", ""), "startMs": int((ln["start"] + a0) * 1000), "endMs": int((ln["start"] + a1) * 1000),
                              "speaker": ln["speaker"], "emph": emph})
        json.dump({"sig": [l["key"] for l in lines] + ["w3"], "words": words}, open(out, "w"))
    del m; gc.collect()


def visemes(sc, out_dir):
    """Rhubarb per line (only that line's speaker will animate), offset into scene time."""
    for s in sc["scenes"]:
        lines = json.load(open(os.path.join(out_dir, f"{s['id']}.lines.json")))
        for ln in lines:
            cache = os.path.join(out_dir, "lines", ln["key"] + ".visemes.json")
            if not os.path.exists(cache):
                dlg = cache + ".txt"; open(dlg, "w").write(ln["text"].replace("*", ""))
                r = subprocess.run([C.RHUBARB, "-f", "json", "--extendedShapes", "GHX", "-d", dlg,
                                    os.path.join(out_dir, "lines", ln["key"] + ".wav")], capture_output=True, text=True)
                json.dump(json.loads(r.stdout)["mouthCues"] if r.returncode == 0 else [], open(cache, "w"))
            ln["visemes"] = [{"start": round(c["start"] + ln["start"], 3), "end": round(c["end"] + ln["start"], 3), "value": c["value"]}
                             for c in json.load(open(cache))]
        json.dump(lines, open(os.path.join(out_dir, f"{s['id']}.lines.json"), "w"), indent=1)
