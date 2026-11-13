"""Instagram Reel from the finished YouTube video (new videos only — a project with a NO_REEL file is skipped).

  1. pick ~30 s of whole, consecutive scenes that make sense on their own (local LLM chooses between candidate windows,
     preferring the opening hook); the cut always lands after the last spoken word of a scene, never mid-sentence
  2. add a proper ending: a narrator closing line (same narrator voice) over an end card "FULL STORY ON YOUTUBE"
  3. 9:16 1080x1920: blurred fill + full-width video, hook headline on top, big word-by-word captions below
     (all inside Instagram's safe zones), loudness -14 LUFS
  4. INSTAGRAM_REEL.txt: caption + hashtags (max 5, Instagram's limit) + posting settings
  5. checks (review/REEL_QC.md): format, loudness, silence/black/frozen video, speech = expected words (start + ending),
     on-screen text readable, standalone story + caption facts (LLM judge), caption rules.
     A failed selection-related check retries with the next-best clip (max 3 tries).

Run alone:  python -m studio.reel <project> [--force]"""
import json, os, re, shutil, subprocess, sys, time
import numpy as np
import soundfile as sf
from . import config as C, llm

RW, RH = 1080, 1920
VID_Y, VID_H = 560, 608                     # full-width 16:9 video band
MIN_S, TARGET_S, MAX_S = 20.0, 30.0, 42.0   # clip length before the end card
SR = 48000
FONTS = os.path.join(C.ROOT, "studio", "fonts_reel")   # static Montserrat weights (libass cannot pick weights of variable fonts)
MAX_TAGS = 5
DANGLING = re.compile(r"^(and|but|so|also|then|that|this|these|those|he|she|they|it|his|her|their|which|meanwhile|still|plus|because)\b", re.I)


def log(proj, msg):
    print(f"[reel] {msg}")
    with open(os.path.join(proj, "production.log"), "a") as f: f.write(f"[{time.strftime('%H:%M:%S')}] reel: {msg}\n")


def _ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def _probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate"
                        ":format=duration,size", "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)


# ---------------------------------------------------------------- 1. choose the clip
class TL:
    """The master's timeline (same maths as the QC Project)."""
    def __init__(self, proj):
        from .qc.core import Project
        self.pr = pr = Project(proj)
        self.scenes = [s for s in pr.scenes if not s.get("_outro")]
        self.words = {s["id"]: pr.props[s["id"]]["words"] for s in pr.scenes}
        self.trans = {s["id"]: pr.props[s["id"]].get("_transition", "cut") for s in pr.scenes}
        from .pipeline import XFADE
        self.d_in = {s["id"]: (XFADE[self.trans[s["id"]]][1] if i else 0.0) for i, s in enumerate(pr.scenes)}

    def end_of(self, j):
        """Cut point after scene j: 0.45 s after its last word, never into the next transition."""
        s = self.scenes[j]; st = self.pr.start[s["id"]]
        w = self.words[s["id"]]
        e = st + (w[-1]["endMs"] / 1000 + 0.02 if w else self.pr.dur[s["id"]]) + 0.45
        ids = [x["id"] for x in self.pr.scenes]; k = ids.index(s["id"])
        if k + 1 < len(ids): e = min(e, self.pr.start[ids[k + 1]])
        return min(e, st + self.pr.dur[s["id"]])

    def lines(self, i, j):
        return [(s["id"], l["speaker"], l["text"]) for s in self.scenes[i:j + 1] for l in s.get("lines", [])]


def candidates(tl):
    out = []
    for i in range(len(tl.scenes)):
        if not tl.scenes[i].get("lines"): continue
        a = tl.pr.start[tl.scenes[i]["id"]]
        for j in range(i, len(tl.scenes)):
            L = tl.end_of(j) - a
            if L > MAX_S: break
            if L < MIN_S or not tl.scenes[j].get("lines"): continue
            ln = tl.lines(i, j)
            pen = abs(L - TARGET_S) / 4 + i * 0.6                                   # near 30 s, early (the hook) preferred
            if DANGLING.match(ln[0][2].strip()): pen += 4                          # starts with a reference to earlier context
            if ln[-1][2].rstrip().endswith("?"): pen += 3                          # ends on an open question
            if tl.scenes[j]["kind"] == "title_card" and j > i: pen += 2            # ends on a chapter card (= new topic starts)
            out.append({"i": i, "j": j, "start": round(a, 3), "end": round(tl.end_of(j), 3), "len": round(L, 1), "pen": round(pen, 2)})
    return sorted(out, key=lambda c: c["pen"])


def choose(tl, topic, title, cands, avoid=()):
    pool = [c for c in cands if (c["i"], c["j"]) not in avoid][:8]
    if not pool: return None
    desc = "\n\n".join(f"OPTION {k} ({c['len']} s, scenes {tl.scenes[c['i']]['id']}-{tl.scenes[c['j']]['id']}):\n" +
                       "\n".join(f"  {spk}: {t}" for _, spk, t in tl.lines(c["i"], c["j"])) for k, c in enumerate(pool))
    r = llm.chat([{"role": "user", "content":
        f"Our YouTube explainer \"{title}\" (topic: {topic}) gets a ~30-second Instagram Reel cut from it.\n\n{desc}\n\n"
        "Pick the option that works best as a STANDALONE reel for someone who never saw the video: it must make sense without "
        "earlier context (no dangling 'he/that/this'), hook the viewer in the first seconds, and end on a complete thought "
        "(not mid-argument). Then write:\n"
        "- hook: on-screen headline for the top of the reel, max 6 words, punchy, no hashtags, no emoji\n"
        "- closing: ONE narrator sentence (max 18 words) spoken at the very end that wraps up what the clip just said and tells "
        "viewers the full story is on our YouTube channel (must contain the word YouTube). No new facts. Not a question.\n"
        "- caption: Instagram caption, 2-4 short sentences: a hook line, what the reel is about, then a call to action to watch the "
        "full breakdown on YouTube (link in bio). Only facts that are in the option's lines. Talk about the story, never say \"this clip\" or \"this reel\". Max 2 emoji. No hashtags in it.\n"
        f"- hashtags: exactly {MAX_TAGS} relevant hashtags (mix of broad and specific), each starting with #"}],
        temperature=0.4, max_tokens=4000,
        schema={"type": "object", "required": ["option", "hook", "closing", "caption", "hashtags"], "properties": {
            "option": {"type": "integer"}, "hook": {"type": "string"}, "closing": {"type": "string"},
            "caption": {"type": "string"}, "hashtags": {"type": "array", "items": {"type": "string"}}}})
    k = r["option"] if isinstance(r.get("option"), int) and 0 <= r["option"] < len(pool) else 0
    c = dict(pool[k])
    c["hook"] = re.sub(r"[#*\"]", "", r["hook"]).strip()[:48]
    clo = r["closing"].replace("*", "").strip()
    if "youtube" not in clo.lower() or clo.endswith("?") or len(clo.split()) > 24:
        clo = "That's the short version. The full story is on our YouTube channel."
    c["closing"] = clo
    c["caption"] = with_cta(r["caption"].replace("#", "").strip())
    tags = []
    for t in r.get("hashtags") or []:
        t = "#" + re.sub(r"[^A-Za-z0-9_]", "", t.lstrip("#"))
        if len(t) > 2 and t.lower() not in [x.lower() for x in tags]: tags.append(t)
    c["hashtags"] = (tags + ["#news", "#explained", "#worldnews", "#currentaffairs", "#politics"])[:MAX_TAGS] if len(tags) < MAX_TAGS else tags[:MAX_TAGS]
    return c


def with_cta(cap):
    """Every caption must point to the YouTube video via the bio link (the user's bio shows the YouTube link)."""
    cap = cap.strip()
    if re.search(r"link in (my |our )?bio", cap, re.I): return cap
    return f"{cap.rstrip()} Full story on YouTube (link in bio)."


def fix_caption(tl, c, problems):
    lines = " ".join(t for _, _, t in tl.lines(c["i"], c["j"]))
    r = llm.chat([{"role": "user", "content":
        f"Rewrite this Instagram Reel caption. Problems found: {'; '.join(p['msg'] for p in problems)}\n\nCAPTION: {c['caption']}\n\n"
        f"The ONLY facts you may use: {lines}\n\n2-4 short sentences: a hook, what the reel shows, then a call to action to watch the full "
        "breakdown on YouTube (link in bio). Max 2 emoji, no hashtags, no facts beyond the lines above."}],
        temperature=0.2, max_tokens=2000, schema={"type": "object", "required": ["caption"], "properties": {"caption": {"type": "string"}}})
    return r["caption"].replace("#", "").strip() or c["caption"]


# ---------------------------------------------------------------- 2. audio (clip + voiced ending)
def closing_voice(proj, sc, text):
    from . import voice as V
    d = os.path.join(proj, "reel", "voice")
    mini = {"characters": [], "scenes": [{"id": "reel_end", "lines": [{"speaker": "narrator", "text": text}]}]}
    V.narrate(mini, d)
    return os.path.join(d, "reel_end.wav")


def _music_bed():
    import glob
    fs = sorted(glob.glob(os.path.join(C.SOUND_LIB, "music", "upbeat_*.flac")))
    return fs[0] if fs else None


def build_audio(proj, master, c, vo_wav, out):
    """Clip audio from the master mix + narrator closing line over a soft music bed. Returns (clip_len, total_len)."""
    tmp = os.path.join(proj, "reel", "clip_a.wav")
    _ff("-ss", f"{c['start']:.3f}", "-to", f"{c['end']:.3f}", "-i", master, "-vn", "-ac", "2", "-ar", str(SR), tmp)
    a, _ = sf.read(tmp, dtype="float32")
    n = len(a); fi, fo = int(0.25 * SR), int(0.35 * SR)
    a[:fi] *= np.linspace(0, 1, fi)[:, None]; a[-fo:] *= np.linspace(1, 0, fo)[:, None]
    vo, vsr = sf.read(vo_wav, dtype="float32")
    if vo.ndim > 1: vo = vo.mean(1)
    if vsr != SR:
        import torch, torchaudio
        vo = torchaudio.functional.resample(torch.from_numpy(vo), vsr, SR).numpy()
    lead, tail = 0.35, 1.1
    card = np.zeros((int((lead + len(vo) / SR + tail) * SR), 2), np.float32)
    card[int(lead * SR):int(lead * SR) + len(vo)] += vo[:, None]
    mb = _music_bed()
    if mb:
        msr0 = sf.info(mb).samplerate
        m, msr = sf.read(mb, dtype="float32", start=int(2 * msr0), frames=int(len(card) / SR * msr0) + msr0)
        if m.ndim == 1: m = np.stack([m, m], 1)
        if msr != SR:
            import torch, torchaudio
            m = torchaudio.functional.resample(torch.from_numpy(np.ascontiguousarray(m.T)), msr, SR).numpy().T
        m = m[:len(card)] * 10 ** (-24 / 20)
        if len(m) < len(card): m = np.pad(m, ((0, len(card) - len(m)), (0, 0)))
        r = int(0.6 * SR); m[:r] *= np.linspace(0, 1, r)[:, None]; m[-r:] *= np.linspace(1, 0, r)[:, None]
        card += m
    full = np.concatenate([a, card])
    sf.write(out, np.clip(full, -1, 1), SR)
    return n / SR, len(full) / SR, lead, len(vo) / SR


# ---------------------------------------------------------------- 3. captions (ASS) + video
def _ass_t(t):
    t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _esc(t):
    return t.replace("\\", "").replace("{", "(").replace("}", ")")


def _chunks(words, max_w=3, max_c=18):
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_w or len(" ".join(x["t"] for x in cur + [w])) > max_c or w["spk"] != cur[0]["spk"]
                    or cur[-1]["t"].endswith((".", "!", "?"))):
            out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return out


def make_ass(path, words, hook, clip_len, total):
    """words: [{t, s, e, spk}] in reel time. Captions word-by-word (active word yellow); hook headline; end-card text."""
    hdr = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {RW}\nPlayResY: {RH}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           "Style: Head,Montserrat ExtraBold,76,&H002D1B0F,&H002D1B0F,&H00F0F4F5,&H00000000,0,0,0,0,100,100,0,0,3,22,0,2,70,70,0,1\n"
           "Style: Cap,Montserrat SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H50000000,0,0,0,0,100,100,0,0,1,4,2,8,80,80,0,1\n"
           "Style: End,Montserrat ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,3,5,60,60,0,1\n"
           "Style: Sub,Montserrat SemiBold,58,&H003928D6,&H003928D6,&H00000000,&H64000000,0,0,0,0,100,100,2,0,1,0,2,5,60,60,0,1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = [f"Dialogue: 1,{_ass_t(0)},{_ass_t(clip_len)},Head,,0,0,0,,{{\\an2\\pos({RW // 2},{VID_Y - 40})\\fad(200,150)}}{_esc(hook.upper())}"]
    cap_y = VID_Y + VID_H + 70
    for ch in _chunks(words):
        for k, w in enumerate(ch):
            st = w["s"]; en = ch[k + 1]["s"] if k + 1 < len(ch) else max(w["e"], w["s"] + 0.25)
            txt = " ".join(("{\\c&H0066D1FF&}" + _esc(x["t"]) + "{\\c&H00FFFFFF&}") if x is w else _esc(x["t"]) for x in ch)
            ev.append(f"Dialogue: 2,{_ass_t(st)},{_ass_t(en)},Cap,,0,0,0,,{{\\an8\\pos({RW // 2},{cap_y})}}{txt}")
    mid = VID_Y + VID_H // 2
    ev.append(f"Dialogue: 3,{_ass_t(clip_len + 0.1)},{_ass_t(total)},End,,0,0,0,,{{\\an5\\pos({RW // 2},{mid - 40})\\fad(250,0)}}FULL STORY\\NON YOUTUBE")
    ev.append(f"Dialogue: 3,{_ass_t(clip_len + 0.3)},{_ass_t(total)},Sub,,0,0,0,,{{\\an5\\pos({RW // 2},{mid + 150})\\fad(250,0)}}Link in bio")
    open(path, "w").write(hdr + "\n".join(ev) + "\n")


def reel_words(tl, c, vo_len, lead, clip_len, closing):
    """Word timings in reel time: the clip's words (from the props) + the closing line spread over its audio."""
    out = []
    for s in tl.scenes[c["i"]:c["j"] + 1]:
        st = tl.pr.start[s["id"]] + 0.02 - c["start"]
        for w in tl.words[s["id"]]:
            a, b = st + w["startMs"] / 1000, st + w["endMs"] / 1000
            if a < clip_len - 0.05: out.append({"t": w["text"], "s": a, "e": min(b, clip_len), "spk": w["speaker"]})
    ws = closing.split(); tot = sum(len(w) + 2 for w in ws); t = clip_len + lead
    for w in ws:
        d = vo_len * (len(w) + 2) / tot
        out.append({"t": w, "s": t, "e": t + d, "spk": "narrator_end"}); t += d
    return out


def clean_renders(proj, tl, ids):
    """The YouTube renders have small burned-in captions; the reel has its own big ones. Re-render just the reel's scenes with
    an empty word list (the renderer uses `words` only for captions) -> reel/clean/<id>.mp4, cached by props hash."""
    import hashlib
    from . import pipeline as PL
    d = os.path.join(proj, "reel", "clean"); os.makedirs(d, exist_ok=True)
    sig = PL._renderer_sig(); jobs = []
    for sid in ids:
        p = {k: v for k, v in tl.pr.props[sid].items() if not k.startswith("_")}; p["words"] = []
        h = hashlib.md5((json.dumps(p, sort_keys=True) + sig).encode()).hexdigest()
        out = os.path.join(d, f"{sid}.mp4")
        if not (os.path.exists(out) and os.path.exists(out + ".hash") and open(out + ".hash").read() == h):
            jobs.append({"props": p, "out": out, "_h": h})
    if jobs:
        cfg = {"publicDir": f"{proj}/public", "bundleDir": f"{proj}/work/bundle", "concurrency": max(4, (os.cpu_count() or 8) // 2),
               "jobs": [{"props": j["props"], "out": j["out"]} for j in jobs]}
        jf = os.path.join(d, "jobs.json"); json.dump(cfg, open(jf, "w"))
        env = dict(os.environ, PATH=C.NODE + ":" + os.environ["PATH"])
        r = subprocess.run(["node", "render_scenes.mjs", jf], cwd=C.REMOTION, env=env, capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError("reel clean render failed:\n" + r.stderr[-2000:])
        for j in jobs: open(j["out"] + ".hash", "w").write(j["_h"])
    return {sid: os.path.join(d, f"{sid}.mp4") for sid in ids}


def clean_clip(proj, tl, c, clip_len):
    """16:9 caption-free video of the clip: clean scene renders joined with the master's own transitions/timing."""
    ids = c["scenes"]; files = clean_renders(proj, tl, ids)
    from .pipeline import XFADE
    out = os.path.join(proj, "reel", "clip_v.mp4")
    args, fc, last = [], [], "0:v"
    for k, sid in enumerate(ids): args += ["-i", files[sid]]
    for k in range(1, len(ids)):
        kind, d = XFADE[tl.trans[ids[k]]]
        off = tl.pr.start[ids[k]] - c["start"]
        fc.append(f"[{last}]{'' if k > 1 else f'fps={C.FPS},'}settb=AVTB[a{k}];[{k}:v]fps={C.FPS},settb=AVTB[b{k}];"
                  f"[a{k}][b{k}]xfade=transition={kind}:duration={d}:offset={off:.4f}[x{k}]")
        last = f"x{k}"
    fc.append(f"[{last}]tpad=stop_mode=clone:stop_duration=1,trim=0:{clip_len:.4f},setpts=PTS-STARTPTS[v]")
    _ff(*args, "-filter_complex", ";".join(fc), "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", out)
    return out


def render(proj, tl, c, master, out):
    """Clean (caption-free) clip -> 9:16 with blurred fill, headline, big captions and the end card, in one ffmpeg pass."""
    rd = os.path.join(proj, "reel"); os.makedirs(rd, exist_ok=True)
    sc = tl.pr.script
    vo = closing_voice(proj, sc, c["closing"])
    wav = os.path.join(rd, "reel_audio.wav")
    clip_len, total, lead, vo_len = build_audio(proj, master, c, vo, wav)
    words = reel_words(tl, c, vo_len, lead, clip_len, c["closing"])
    ass = os.path.join(rd, "reel.ass"); make_ass(ass, words, c["hook"], clip_len, total)
    card = total - clip_len
    src = ["-i", clean_clip(proj, tl, c, clip_len)]; ai = 1
    v = f"[0:v]setpts=PTS-STARTPTS,fps={C.FPS}[clip];"
    v += (f"[clip]tpad=stop_mode=clone:stop_duration={card + 0.5:.3f},trim=0:{total:.3f},split[a][b];"
          f"[a]scale=-2:{RH},crop={RW}:{RH},boxblur=28:2,eq=brightness=-0.22:saturation=0.8[bg];"
          f"[b]scale={RW}:{VID_H},boxblur=10:1:enable='gte(t,{clip_len:.3f})',"
          f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.62:t=fill:enable='gte(t,{clip_len:.3f})'[fg];"
          f"[bg][fg]overlay=0:{VID_Y},ass='{ass}':fontsdir='{FONTS}',format=yuv420p[v]")
    tmp = out + ".tmp.mp4"
    _ff(*src, "-i", wav, "-filter_complex", v + f";[{ai}:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample={SR}[aud]",
        "-map", "[v]", "-map", "[aud]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
        "-r", str(C.FPS), "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", tmp)
    os.replace(tmp, out)
    _ff("-ss", "1.2", "-i", out, "-frames:v", "1", "-q:v", "2", os.path.join(rd, "cover.jpg"))
    return {"clip_len": round(clip_len, 2), "total": round(total, 2), "words": words, "vo": vo}


# ---------------------------------------------------------------- 5. checks
def _f(sev, check, msg):
    return {"severity": sev, "check": check, "msg": msg}


def check(proj, tl, c, out, meta, caption_txt):
    from .qc import models as M
    from .qc.stage1 import sim, norm_words, is_word
    F = []
    # format
    p = _probe(out); v = next((s for s in p["streams"] if s["codec_type"] == "video"), {}); a = next((s for s in p["streams"] if s["codec_type"] == "audio"), {})
    dur = float(p["format"]["duration"]); size = int(p["format"]["size"])
    if (v.get("width"), v.get("height")) != (RW, RH): F.append(_f("CRITICAL", "format", f"video is {v.get('width')}x{v.get('height')}, not {RW}x{RH} (9:16)"))
    if v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p": F.append(_f("CRITICAL", "format", f"video codec {v.get('codec_name')}/{v.get('pix_fmt')} (need h264/yuv420p)"))
    if v.get("r_frame_rate") not in (f"{C.FPS}/1",): F.append(_f("HIGH", "format", f"frame rate {v.get('r_frame_rate')}"))
    if a.get("codec_name") != "aac": F.append(_f("CRITICAL", "format", "no AAC audio track"))
    if not 15 <= dur <= 60: F.append(_f("CRITICAL", "length", f"reel is {dur:.1f} s (want 15-60, ideally ~30-40)"))
    if size > 100e6: F.append(_f("HIGH", "format", f"file is {size / 1e6:.0f} MB"))
    # loudness / silence / black / frozen
    r = subprocess.run(["ffmpeg", "-nostats", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)
    if I and not -17 <= float(I[-1]) <= -11: F.append(_f("HIGH", "audio", f"loudness {I[-1]} LUFS (target -14)"))
    if TP and float(TP[-1]) > -0.5: F.append(_f("HIGH", "audio", f"true peak {TP[-1]} dBFS (clipping risk)"))
    r = subprocess.run(["ffmpeg", "-nostats", "-i", out, "-af", "silencedetect=n=-45dB:d=1.3", "-vf", "blackdetect=d=0.3:pix_th=0.08,freezedetect=n=0.002:d=4",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    for s0, s1 in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r):
        if float(s0) < dur - 1.5: F.append(_f("HIGH", "audio", f"{float(s1) - float(s0):.1f} s of silence at {float(s0):.1f} s"))
    for b in re.findall(r"black_start:([\d.]+)", r): F.append(_f("HIGH", "visual", f"black frames at {float(b):.1f} s"))
    for z in re.findall(r"freeze_start: ([\d.]+)", r):
        if float(z) < meta["clip_len"] - 4.5: F.append(_f("MEDIUM", "visual", f"video frozen for 4+ s at {float(z):.1f} s"))
    # speech: everything expected is said, starts at the start of a sentence, ends with the closing line
    expected = " ".join(t for _, _, t in tl.lines(c["i"], c["j"])) + " " + c["closing"]
    wav = os.path.join(proj, "reel", "check.wav"); _ff("-i", out, "-vn", "-ac", "1", "-ar", "16000", wav)
    heard, hw = M.asr(wav)
    s = sim(expected, heard)
    if s < 0.8: F.append(_f("CRITICAL", "speech", f"audio doesn't match the clip's lines (similarity {s:.2f}) — words cut or missing"))
    ew, hw_ = norm_words(expected), norm_words(heard)
    if ew[:3] and sim(" ".join(ew[:4]), " ".join(hw_[:4])) < 0.6: F.append(_f("HIGH", "speech", f"starts mid-sentence: heard \"{' '.join(hw_[:6])}\""))
    cw = norm_words(c["closing"])
    if sim(" ".join(cw[-4:]), " ".join(hw_[-5:])) < 0.6: F.append(_f("CRITICAL", "ending", f"closing line not heard at the end: \"{' '.join(hw_[-8:])}\""))
    tail = [w for w in hw if w[1] > meta["clip_len"] - 0.05]
    if not tail: F.append(_f("CRITICAL", "ending", "nothing spoken over the end card"))
    # on-screen text
    fr = os.path.join(proj, "reel", "chk"); os.makedirs(fr, exist_ok=True)
    def grab(t, name):
        pth = os.path.join(fr, name); _ff("-ss", f"{t:.2f}", "-i", out, "-frames:v", "1", pth); return pth
    head = grab(1.5, "head.png"); endf = grab(dur - 0.4, "end.png")
    from PIL import Image
    top = Image.open(head).crop((0, 120, RW, VID_Y))
    ht = " ".join(t for t, _ in M.ocr(top))
    if sim(c["hook"], ht) < 0.6: F.append(_f("HIGH", "text", f"headline not readable: OCR \"{ht}\" vs \"{c['hook']}\""))
    if any(not is_word(w) and len(w) >= 4 for w in norm_words(c["hook"])): F.append(_f("MEDIUM", "text", f"headline has odd words: {c['hook']}"))
    ws = [w for w in meta["words"] if w["s"] > 2 and w["e"] < meta["clip_len"] - 0.5]
    if ws:
        w = ws[len(ws) // 2]; capf = grab((w["s"] + w["e"]) / 2, "cap.png")
        boxes = M.ocr(Image.open(capf).crop((0, VID_Y + VID_H, RW, 1560)))
        dup = M.ocr(Image.open(capf).crop((0, VID_Y + int(VID_H * 0.8), RW, VID_Y + VID_H)))
        if sim(" ".join(t for t, _ in dup), " ".join(x["t"] for x in ws if abs(x["s"] - w["s"]) < 2.5)) > 0.5:
            F.append(_f("HIGH", "text", "small YouTube captions are burned into the video too (double captions)"))
        if not boxes: F.append(_f("HIGH", "text", f"no captions visible at {w['s']:.1f} s"))
        elif any(bb[0] < 30 or bb[2] > RW - 30 for _, bb in boxes): F.append(_f("MEDIUM", "text", "captions touch the screen edge"))
    et = " ".join(t for t, _ in M.ocr(endf)).upper()
    if "YOUTUBE" not in et.replace(" ", ""): F.append(_f("CRITICAL", "ending", f"end card text missing (OCR: {et[:60]})"))
    M.free()
    # caption rules
    tags = re.findall(r"#\w+", caption_txt)
    if len(c["caption"]) + len(" ".join(c["hashtags"])) > 2200: F.append(_f("HIGH", "caption", "caption longer than 2200 characters"))
    if not 1 <= len(c["hashtags"]) <= MAX_TAGS: F.append(_f("HIGH", "caption", f"{len(c['hashtags'])} hashtags (Instagram allows {MAX_TAGS})"))
    if not re.search(r"link in (my |our )?bio", c["caption"], re.I): F.append(_f("HIGH", "caption", "caption does not say 'link in bio'"))
    if len(c["caption"]) < 60: F.append(_f("MEDIUM", "caption", "caption is very short"))
    # story judge (fresh LLM call on what is actually heard)
    try:
        j = llm.chat([{"role": "user", "content":
            "You review a 30-second Instagram Reel cut from a longer news explainer.\n"
            f"WHAT THE REEL SAYS (speech recognition): {heard}\nON-SCREEN HEADLINE: {c['hook']}\nINSTAGRAM CAPTION: {c['caption']}\n"
            f"FACTS AVAILABLE (the clip's script lines): {expected}\n\n"
            "Answer strictly: standalone = a first-time viewer understands it without the full video; clean_start = it doesn't open "
            "mid-thought or with an unexplained reference; proper_ending = it ends with a wrap-up / sign-off, not mid-argument; "
            "caption_ok = caption and headline only state facts found in the script lines and fit the reel. Give a short reason for any false."}],
            temperature=0.0, max_tokens=2000,
            schema={"type": "object", "required": ["standalone", "clean_start", "proper_ending", "caption_ok", "reason"], "properties": {
                "standalone": {"type": "boolean"}, "clean_start": {"type": "boolean"}, "proper_ending": {"type": "boolean"},
                "caption_ok": {"type": "boolean"}, "reason": {"type": "string"}}})
        for k, sev, nm in (("standalone", "CRITICAL", "story"), ("clean_start", "HIGH", "story"), ("proper_ending", "CRITICAL", "ending"),
                           ("caption_ok", "HIGH", "caption")):
            if j.get(k) is False: F.append(_f(sev, nm, f"judge: {k} = false — {j.get('reason', '')[:160]}"))
    except Exception as e:
        F.append(_f("LOW", "story", f"story judge unavailable: {e}"))
    return F


# ---------------------------------------------------------------- 4. caption file + report
def caption_file(proj, sc, c, meta, ok, F, out):
    name = os.path.basename(out)
    txt = (f"=== INSTAGRAM REEL ===\nVideo ................ reel/{name}  ({meta['total']:.0f} s, 1080x1920)\n"
           f"Cover ................ reel/cover.jpg (or pick a frame in the app)\nTaken from ........... {c['start'] // 60:.0f}:{c['start'] % 60:04.1f} - "
           f"{c['end'] // 60:.0f}:{c['end'] % 60:04.1f} of the YouTube video + closing line\nChecks ............... "
           f"{'PASS' if ok else 'FAIL — see review/REEL_QC.md'}\n\n\n=== CAPTION (copy everything below) ===\n"
           f"{c['caption']}\n\n{' '.join(c['hashtags'])}\n\n\n=== SETTINGS ===\n"
           "Audio ................ keep original audio (music is already mixed in)\n"
           "AI label ............. turn ON \"AI info\" if the reel has realistic-looking AI footage; optional for cartoon-only\n"
           "Link ................. caption says \"link in bio\" — your bio already has the YouTube link\n"
           "Share to Facebook .... optional\n")
    open(os.path.join(proj, "INSTAGRAM_REEL.txt"), "w").write(txt)
    return txt


def report(proj, c, F, ok, tries):
    rows = "\n".join(f"| {f['severity']} | {f['check']} | {f['msg']} |" for f in F) or "| — | — | no problems found |"
    md = (f"# Instagram Reel QC — {'PASS' if ok else 'FAIL'}\n\nClip: {c['start']:.1f}–{c['end']:.1f} s of the master "
          f"(scenes {c['scenes']}), {c['len']} s + closing line. Attempts: {tries}.\n\nHook: **{c['hook']}**  \nClosing: _{c['closing']}_\n\n"
          f"| Severity | Check | Finding |\n|---|---|---|\n{rows}\n")
    os.makedirs(os.path.join(proj, "review"), exist_ok=True)
    open(os.path.join(proj, "review", "REEL_QC.md"), "w").write(md)


# ---------------------------------------------------------------- driver
def make(proj, force=False):
    proj = os.path.abspath(proj)
    if os.path.exists(os.path.join(proj, "NO_REEL")): return None
    name = os.path.basename(proj.rstrip("/")); master = os.path.join(proj, f"{name}.mp4")
    if not os.path.exists(master): return None
    rd = os.path.join(proj, "reel"); os.makedirs(rd, exist_ok=True)
    out = os.path.join(rd, f"{name}_reel.mp4")
    state_p = os.path.join(rd, "reel.json")
    state = json.load(open(state_p)) if os.path.exists(state_p) else {}
    mm = int(os.path.getmtime(master))
    if not force and state.get("master_mtime") == mm and state.get("ok") and os.path.exists(out):
        log(proj, "up to date"); return out
    sc = json.load(open(os.path.join(proj, "script.json")))
    topic = open(os.path.join(proj, "TOPIC")).read().strip() if os.path.exists(os.path.join(proj, "TOPIC")) else sc["title"]
    tl = TL(proj); cands = candidates(tl)
    if not cands:
        log(proj, "no usable 20-42 s window of whole scenes"); return None
    prev = state.get("choice")
    tried, best = [], None
    for attempt in range(3):
        if attempt == 0 and prev and not force and prev.get("scenes") == [s["id"] for s in tl.scenes[prev["i"]:prev["j"] + 1]]:
            c = dict(prev); c.update(next((x for x in cands if (x["i"], x["j"]) == (prev["i"], prev["j"])), {}))   # same clip, new timings
        else:
            c = choose(tl, topic, sc["title"], cands, avoid=[(t["i"], t["j"]) for t in tried])
            if not c: break
        c["scenes"] = [s["id"] for s in tl.scenes[c["i"]:c["j"] + 1]]
        llm.unload()
        log(proj, f"try {attempt + 1}: scenes {c['scenes'][0]}-{c['scenes'][-1]} ({c['len']} s) hook \"{c['hook']}\"")
        meta = render(proj, tl, c, master, out)
        txt = caption_file(proj, sc, c, meta, False, [], out)
        F = check(proj, tl, c, out, meta, txt)
        ok = not any(f["severity"] in ("CRITICAL", "HIGH") for f in F)
        serious = [f for f in F if f["severity"] in ("CRITICAL", "HIGH")]
        if serious and all(f["check"] == "caption" for f in serious):     # only the caption is off: rewrite it, keep the clip
            c["caption"] = with_cta(fix_caption(tl, c, serious)); log(proj, f"caption rewritten: {c['caption'][:90]}")
            txt = caption_file(proj, sc, c, meta, False, [], out)
            F = check(proj, tl, c, out, meta, txt); ok = not any(f["severity"] in ("CRITICAL", "HIGH") for f in F)
        tried.append(c)
        if best is None or sum({"CRITICAL": 10, "HIGH": 3, "MEDIUM": 1}.get(f["severity"], 0) for f in F) < best[2]:
            best = (c, meta, sum({"CRITICAL": 10, "HIGH": 3, "MEDIUM": 1}.get(f["severity"], 0) for f in F), F, ok)
            shutil.copy2(out, out + ".best.mp4")
        log(proj, f"checks {'PASS' if ok else 'FAIL'}: " + "; ".join(f"{f['severity']} {f['msg'][:70]}" for f in F if f["severity"] != "LOW")[:400])
        if ok: break
        if not any(f["check"] in ("speech", "ending", "story", "length", "caption", "text") for f in F if f["severity"] in ("CRITICAL", "HIGH")):
            break                                     # not a clip-choice problem: another clip wouldn't help
    c, meta, _, F, ok = best
    os.replace(out + ".best.mp4", out)
    caption_file(proj, sc, c, meta, ok, F, out); report(proj, c, F, ok, len(tried))
    json.dump({"master_mtime": mm, "ok": ok, "choice": {k: c[k] for k in ("i", "j", "start", "end", "len", "hook", "closing", "caption", "hashtags", "scenes")}},
              open(state_p, "w"), indent=1)
    for f in ("clip_a.wav", "reel_audio.wav", "check.wav", "clip_v.mp4"):
        if os.path.exists(os.path.join(rd, f)): os.remove(os.path.join(rd, f))
    log(proj, f"{'PASS' if ok else 'FAIL'} -> {out} ({meta['total']:.0f} s)")
    return out


if __name__ == "__main__":
    make(sys.argv[1], force="--force" in sys.argv)
