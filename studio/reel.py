"""Instagram Reel = a SUMMARY EDIT of the finished YouTube video (new videos only — a project with a NO_REEL file is skipped).
(The old "cut 30 s out of the video" version lives in reel_cut.py.)

  1. plan: the local LLM writes a tight narrator summary of the WHOLE story (hook -> what happened -> why it matters ->
     what's next) using only facts from the script, picks up to 2 real soundbites (character lines) and a visual scene per beat,
     plus on-screen number/keyword cards, headline, caption and hashtags. Numbers are checked against the script.
  2. audio: narrator voices the beats; soundbites come from the characters' real voice tracks; soft music bed; spoken CTA
     ("full breakdown on YouTube, link in bio") over an end card.
  3. video: each beat = the best matching shot from the video (clean, caption-free re-render): maps/charts/hero shots for the
     narrator, the speaker's own animated shot for soundbites; cuts on the beats, slow push-ins; 9:16 with headline, cards,
     name tags and big word-by-word captions.
  4. INSTAGRAM_REEL.txt (caption + 5 hashtags + settings) and review/REEL_QC.md.
  5. checks: format, loudness, silence/black/frozen, speech = planned words, start + CTA heard, on-screen text, caption rules,
     LLM judge (whole story / standalone / proper ending / facts / caption). Fails -> replan with the problems (max 3 tries).

Run alone:  python -m studio.reel <project> [--force]"""
import json, os, re, shutil, subprocess, sys, time
import numpy as np
import soundfile as sf
from . import config as C, llm

RW, RH = 1080, 1920
VID_Y, VID_H = 560, 608                     # full-width 16:9 video band
SR = 48000
FONTS = os.path.join(C.ROOT, "studio", "fonts_reel")   # static Montserrat weights (libass cannot pick weights of variable fonts)
MAX_TAGS = 5
VO_WORDS = (55, 105)                        # narrator words in the summary (~25-45 s with soundbites)
MAX_BITES, MAX_BITE_S = 2, 8.0
GAP = 0.14                                  # breath between beats
CTA_DEFAULT = "That's the short version. The full breakdown is on our YouTube channel, link in bio."


def log(proj, msg):
    print(f"[reel] {msg}")
    with open(os.path.join(proj, "production.log"), "a") as f: f.write(f"[{time.strftime('%H:%M:%S')}] reel: {msg}\n")


def _ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def _probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate"
                        ":format=duration,size", "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)


# ---------------------------------------------------------------- 1. plan the summary
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



def _nums(t):
    return {re.sub(r"[,\s]", "", m) for m in re.findall(r"\d[\d,.]*\d|\d", t)}


def _catalog(tl):
    """Scene list for the planner: what each scene SHOWS + its lines (character lines get a soundbite ref)."""
    chars = {c["id"]: c for c in tl.pr.script.get("characters", [])}
    rows, refs = [], {}
    for s in tl.scenes:
        p = tl.pr.props[s["id"]]; k = p["kind"]
        if k == "map": what = f'MAP "{(p.get("map") or {}).get("label", "")}"'
        elif k == "chart": what = f'CHART "{(p.get("chart") or {}).get("title", "")}"'
        elif k == "hero": what = "CINEMATIC SHOT"
        elif k == "title_card": what = f'CHAPTER CARD "{p.get("titleText", "")}"'
        else: what = "PEOPLE TALKING" if any(l["speaker"] != "narrator" for l in p["lines"]) else "PEOPLE LISTENING"
        rows.append(f"{s['id']} [{what}]")
        for i, l in enumerate(p["lines"]):
            if l["speaker"] == "narrator": rows.append(f"    narrator: {l['text']}")
            else:
                ref = f"{s['id']}#{i}"; c = chars.get(l["speaker"], {})
                refs[ref] = {"scene": s["id"], "i": i, "speaker": l["speaker"], "text": l["text"], "start": l["start"], "end": l["end"],
                             "name": c.get("tag_name") or c.get("name", l["speaker"]), "role": c.get("role", ""), "tag": c.get("tag", True) is not False}
                rows.append(f"    [{ref}] {refs[ref]['name']}: {l['text']}  ({l['end'] - l['start']:.1f} s)")
    return "\n".join(rows), refs


def _facts(tl):
    return " ".join(l["text"] for s in tl.scenes for l in tl.pr.props[s["id"]]["lines"])


def plan(tl, topic, title, feedback=None):
    cat, refs = _catalog(tl); facts = _facts(tl); fnums = _nums(facts)
    ids = {s["id"] for s in tl.scenes}
    msgs = [{"role": "user", "content":
        f"Our YouTube news explainer \"{title}\" (topic: {topic}) gets an Instagram Reel. Instagram viewers will NOT watch the "
        "YouTube video, so the reel must give them THE WHOLE STORY in about 35 seconds, as a cleverly edited summary, then send "
        "them to YouTube for the full breakdown.\n\nTHE VIDEO, scene by scene (what is on screen + what is said):\n" + cat + "\n\n"
        "Write the reel as 4-7 beats in story order:\n"
        "- beat 1: a scroll-stopping hook: the most striking fact, then the video's running-gag question with a deadpan answer "
        "(e.g. \"The yen is nearly 160 to the dollar. So, is Japan worried? Hard to say, really.\"), narrator, max 20 words\n"
        "- KEEP IT FUN: reuse the video's running gag (the deadpan narrator lines in the scenes above) — call it back once in the "
        "middle after an escalating fact, and END the story on its payoff line. Jokes must sound like a spontaneous reaction, "
        "short and natural, never about deaths or victims. Still include what happens next.\n"
        "- then: what happened -> why it matters / the conflict -> what happens next. Plain, punchy sentences, max 18 words each.\n"
        f"- narrator beats total {VO_WORDS[0]}-{VO_WORDS[1]} words.\n"
        f"- up to {MAX_BITES} soundbites: real character lines that add a voice or emotion, referenced by their [ref] exactly "
        f"(max {MAX_BITE_S:.0f} s each; never a narrator line).\n"
        "- every narrator beat names the scene id whose visuals fit it best: prefer MAP, CHART, CINEMATIC SHOT or PEOPLE LISTENING "
        "scenes; avoid PEOPLE TALKING scenes for narrator beats (mouths would move under the narration).\n"
        "- card: optional 1-4 word on-screen text for the beat (a key number like \"750,000 homes\" or a keyword), or \"\".\n"
        "- ONLY facts and numbers that appear in the lines above. No new facts, no opinions, no 'this video/this reel'.\n"
        "Also write:\n- hook: on-screen headline at the top, max 6 words, no hashtags/emoji — ideally the running-gag question "
        "with its deadpan answer (e.g. \"Is Japan Worried? Hard to Say\")\n"
        "- cta: ONE closing narrator sentence, max 16 words, saying the full breakdown is on our YouTube channel, link in bio\n"
        "- caption: Instagram caption, 2-4 short sentences: a hook, the gist of the story with the running-gag line, then a call to action to watch the full "
        "breakdown on YouTube (link in bio). Only facts from the lines. Max 2 emoji. No hashtags in it.\n"
        f"- hashtags: exactly {MAX_TAGS} relevant hashtags, each starting with #"
        + (f"\n\nYOUR PREVIOUS ATTEMPT HAD THESE PROBLEMS — fix them:\n- " + "\n- ".join(feedback) if feedback else "")}]
    schema = {"type": "object", "required": ["hook", "beats", "cta", "caption", "hashtags"], "properties": {
        "hook": {"type": "string"}, "cta": {"type": "string"}, "caption": {"type": "string"},
        "hashtags": {"type": "array", "items": {"type": "string"}},
        "beats": {"type": "array", "items": {"type": "object", "required": ["type"], "properties": {
            "type": {"type": "string", "enum": ["vo", "bite"]}, "text": {"type": "string"}, "ref": {"type": "string"},
            "scene": {"type": "string"}, "card": {"type": "string"}}}}}}
    for attempt in range(3):
        r = llm.chat(msgs, temperature=0.5 if attempt else 0.4, max_tokens=5000, schema=schema)
        probs, beats = [], []
        for b in r.get("beats") or []:
            card = re.sub(r"[#*\"]", "", (b.get("card") or "")).strip()
            if len(card.split()) > 5: card = ""
            if card and not _nums(card) <= fnums: probs.append(f"card '{card}' has a number not in the script"); card = ""
            if b.get("type") == "bite":
                ref = (b.get("ref") or "").strip().strip("[]")
                x = refs.get(ref)
                if not x: probs.append(f"soundbite ref '{ref}' does not exist"); continue
                if x["end"] - x["start"] > MAX_BITE_S: probs.append(f"soundbite {ref} is longer than {MAX_BITE_S:.0f} s"); continue
                beats.append({"type": "bite", **x, "ref": ref, "card": card})
            else:
                t = (b.get("text") or "").replace("*", "").strip()
                if not t: continue
                sid = (b.get("scene") or "").strip()
                if sid not in ids: probs.append(f"beat '{t[:30]}...' uses unknown scene '{sid}'"); sid = tl.scenes[min(len(beats), len(tl.scenes) - 1)]["id"]
                bad = _nums(t) - fnums
                if bad: probs.append(f"narrator beat '{t[:50]}' has numbers not in the script: {sorted(bad)}")
                beats.append({"type": "vo", "text": t, "scene": sid, "card": card})
        nb = [b for b in beats if b["type"] == "bite"]
        if len(nb) > MAX_BITES: probs.append(f"{len(nb)} soundbites (max {MAX_BITES})")
        if not beats or beats[0]["type"] != "vo": probs.append("the first beat must be a narrator hook")
        nw = sum(len(b["text"].split()) for b in beats if b["type"] == "vo")
        if not VO_WORDS[0] <= nw <= VO_WORDS[1] + 15: probs.append(f"narrator beats have {nw} words (want {VO_WORDS[0]}-{VO_WORDS[1]})")
        if not 3 <= len(beats) <= 8: probs.append(f"{len(beats)} beats (want 4-7)")
        hard = [p for p in probs if "number" in p or "first beat" in p or "words" in p or "beats (want" in p]
        if not hard: break
        msgs = msgs[:1] + [{"role": "assistant", "content": json.dumps(r)},
                           {"role": "user", "content": "Problems:\n- " + "\n- ".join(probs) + "\nReturn the corrected JSON."}]
    if not beats: return None
    c = {"beats": beats, "hook": re.sub(r"[#*\"]", "", r.get("hook", "")).strip()[:48] or title[:48]}
    cta = (r.get("cta") or "").replace("*", "").strip()
    if "youtube" not in cta.lower() or len(cta.split()) > 22 or cta.endswith("?"): cta = CTA_DEFAULT
    c["cta"] = cta
    c["caption"] = with_cta(r.get("caption", "").replace("#", "").strip())
    tags = []
    for t in r.get("hashtags") or []:
        t = "#" + re.sub(r"[^A-Za-z0-9_]", "", t.lstrip("#"))
        if len(t) > 2 and t.lower() not in [x.lower() for x in tags]: tags.append(t)
    c["hashtags"] = (tags + ["#news", "#explained", "#worldnews", "#currentaffairs", "#politics"])[:MAX_TAGS]
    c["plan_notes"] = probs
    return c


def with_cta(cap):
    """Every caption must point to the YouTube video via the bio link (the user's bio shows the YouTube link)."""
    cap = cap.strip()
    if re.search(r"link in (my |our )?bio", cap, re.I): return cap
    return f"{cap.rstrip()} Full story on YouTube (link in bio)."



def fix_caption(tl, c, problems):
    r = llm.chat([{"role": "user", "content":
        f"Rewrite this Instagram Reel caption. Problems found: {'; '.join(p['msg'] for p in problems)}\n\nCAPTION: {c['caption']}\n\n"
        f"The ONLY facts you may use: {_facts(tl)}\n\n2-4 short sentences: a hook, the gist of the story, then a call to action to watch "
        "the full breakdown on YouTube (link in bio). Max 2 emoji, no hashtags, no facts beyond the lines above."}],
        temperature=0.2, max_tokens=2000, schema={"type": "object", "required": ["caption"], "properties": {"caption": {"type": "string"}}})
    return r["caption"].replace("#", "").strip() or c["caption"]


# ---------------------------------------------------------------- 2. audio
def _read_mono(path):
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1: a = a.mean(1)
    if sr != SR:
        import torch, torchaudio
        a = torchaudio.functional.resample(torch.from_numpy(np.ascontiguousarray(a)), sr, SR).numpy()
    return a


def voice_beats(proj, c):
    """Narrator wavs for every vo beat + the CTA (cached per line by voice.narrate)."""
    from . import voice as V
    d = os.path.join(proj, "reel", "voice")
    scenes = [{"id": f"b{k}", "lines": [{"speaker": "narrator", "text": b["text"]}]} for k, b in enumerate(c["beats"]) if b["type"] == "vo"]
    scenes.append({"id": "cta", "lines": [{"speaker": "narrator", "text": c["cta"]}]})
    V.narrate({"characters": [], "scenes": scenes}, d)
    for k, b in enumerate(c["beats"]):
        if b["type"] == "vo": b["wav"] = os.path.join(d, f"b{k}.wav")
    return os.path.join(d, "cta.wav")


def _music_bed():
    import glob
    fs = sorted(glob.glob(os.path.join(C.SOUND_LIB, "music", "upbeat_*.flac")))
    return fs[0] if fs else None


def build_audio(proj, c, cta_wav, out, voice_out):
    """Lay the beats end to end (narration + real soundbites), music bed underneath, CTA over the end card.
    Sets b['t0'], b['dur'] (reel time) on every beat. Returns (clip_len, total)."""
    parts, t = [], 0.0
    for b in c["beats"]:
        if b["type"] == "vo":
            a = _read_mono(b["wav"])
        else:
            src = _read_mono(os.path.join(proj, "audio", f"{b['scene']}.wav"))
            s0, s1 = max(0, int((b["start"] - 0.06) * SR)), int((b["end"] + 0.12) * SR)
            a = src[s0:s1].copy(); f = int(0.03 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
            b["win_start"] = b["start"] - 0.06
        b["t0"] = round(t, 3); b["dur"] = round(len(a) / SR + GAP, 3)
        parts.append(np.concatenate([a, np.zeros(int(GAP * SR), np.float32)])); t += b["dur"]
    clip_len = t + 0.25
    vo = _read_mono(cta_wav); lead, tail = 0.35, 1.2
    voice = np.zeros(int((clip_len + lead + len(vo) / SR + tail) * SR), np.float32)
    k = 0
    for p in parts: voice[k:k + len(p)] = p; k += len(p)
    e0 = int((clip_len + lead) * SR); voice[e0:e0 + len(vo)] = vo
    sf.write(voice_out, voice, SR)
    mix = np.stack([voice, voice], 1)
    mb = _music_bed()
    if mb:
        msr0 = sf.info(mb).samplerate
        m, msr = sf.read(mb, dtype="float32", start=int(2 * msr0), frames=int(len(mix) / SR * msr0) + msr0)
        if m.ndim == 1: m = np.stack([m, m], 1)
        if msr != SR:
            import torch, torchaudio
            m = torchaudio.functional.resample(torch.from_numpy(np.ascontiguousarray(m.T)), msr, SR).numpy().T
        m = m[:len(mix)] * 10 ** (-25 / 20)
        if len(m) < len(mix): m = np.pad(m, ((0, len(mix) - len(m)), (0, 0)))
        r = int(0.8 * SR); m[:r] *= np.linspace(0, 1, r)[:, None]; m[-r:] *= np.linspace(1, 0, r)[:, None]
        mix += m
    sf.write(out, np.clip(mix, -1, 1), SR)
    return clip_len, len(mix) / SR


# ---------------------------------------------------------------- 3. video
def clean_renders(proj, tl, ids):
    """The YouTube renders have small burned-in captions; the reel has its own big ones. Re-render just the reel's scenes with
    an empty word list (the renderer uses `words` only for captions) -> reel/clean/<id>.mp4, cached by props hash."""
    import hashlib
    from . import pipeline as PL
    d = os.path.join(proj, "reel", "clean"); os.makedirs(d, exist_ok=True)
    sig = PL._renderer_sig(); jobs = []
    for sid in ids:
        p = {k: v for k, v in tl.pr.props[sid].items() if not k.startswith("_")}; p["words"] = []
        p["beats"] = []; p["introduce"] = []          # the reel draws its own cards and name tags
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



def _window(tl, b, scene_len):
    """Where in the scene's clean render a narrator beat should come from: a stretch where nobody on screen is talking."""
    p = tl.pr.props[b["scene"]]; d = b["dur"]
    if p["kind"] != "stage": return min(0.15, max(0.0, scene_len - d)), False
    L = p["lines"]
    for i, l in enumerate(L):
        if l["speaker"] == "narrator":
            a = 0.0 if i == 0 else l["start"]; e = L[i + 1]["start"] if i + 1 < len(L) else scene_len
            if e - a >= min(d, 2.5): return a, False
    return 0.0, any(l["speaker"] != "narrator" for l in L)      # (start, lip-mismatch risk)


def build_video(proj, tl, c, clip_len):
    """16:9 caption-free edit: one segment per beat, hard cuts on the beats, slow push-in/out alternating."""
    files = clean_renders(proj, tl, sorted({b["scene"] for b in c["beats"]}))
    d = os.path.join(proj, "reel", "segs"); os.makedirs(d, exist_ok=True)
    F = C.FPS; segs = []
    for k, b in enumerate(c["beats"]):
        src = files[b["scene"]]
        L = float(_probe(src)["format"]["duration"])
        dur = b["dur"] + (clip_len - c["beats"][-1]["t0"] - c["beats"][-1]["dur"] if k == len(c["beats"]) - 1 else 0)
        b["dur_v"] = dur
        if b["type"] == "bite": st, risk = max(0.0, b["win_start"]), False
        else:
            b["dur"] = dur; st, risk = _window(tl, b, L)
        b["lip_risk"] = risk
        avail = max(0.3, L - st); rate = min(1.3, max(1.0, dur / avail))       # gentle slow-mo if the scene is a bit short
        n = int(round(dur * F)); z0, z1 = (1.0, 1.07) if k % 2 == 0 else (1.07, 1.0)
        zexpr = f"{z0}+({z1}-{z0})*on/{max(1, n - 1)}"
        out = os.path.join(d, f"{k:02d}.mp4")
        _ff("-ss", f"{st:.3f}", "-i", src, "-an", "-vf",
            f"setpts={rate:.4f}*(PTS-STARTPTS),fps={F},tpad=stop_mode=clone:stop_duration={dur + 1:.2f},trim=end_frame={n},"
            f"scale=1920:1080,zoompan=z='{zexpr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={F},setsar=1",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p", out)
        segs.append(out)
    lst = os.path.join(d, "list.txt"); open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    out = os.path.join(proj, "reel", "clip_v.mp4")
    _ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out)
    return out


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



def make_ass(path, words, c, clip_len, total):
    hdr = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {RW}\nPlayResY: {RH}\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
           "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           "Style: Head,Montserrat ExtraBold,76,&H002D1B0F,&H002D1B0F,&H00F0F4F5,&H00000000,0,0,0,0,100,100,0,0,3,22,0,2,70,70,0,1\n"
           "Style: Cap,Montserrat SemiBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H50000000,0,0,0,0,100,100,0,0,1,4,2,8,80,80,0,1\n"
           "Style: Card,Montserrat ExtraBold,58,&H002D1B0F,&H002D1B0F,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,3,16,0,9,40,40,0,1\n"
           "Style: CardN,Montserrat ExtraBold,64,&H003928D6,&H003928D6,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,3,16,0,9,40,40,0,1\n"
           "Style: TagN,Montserrat ExtraBold,40,&H002D1B0F,&H002D1B0F,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,3,12,0,1,40,40,0,1\n"
           "Style: TagR,Montserrat SemiBold,30,&H00FFFFFF,&H00FFFFFF,&H002D1B0F,&H00000000,0,0,0,0,100,100,0,0,3,10,0,1,40,40,0,1\n"
           "Style: End,Montserrat ExtraBold,120,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,3,5,60,60,0,1\n"
           "Style: Sub,Montserrat ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H003928D6,&H003928D6,0,0,0,0,100,100,2,0,3,22,0,5,60,60,0,1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = [f"Dialogue: 1,{_ass_t(0)},{_ass_t(clip_len)},Head,,0,0,0,,{{\\an2\\pos({RW // 2},{VID_Y - 40})\\fad(200,150)}}{_esc(c['hook'].upper())}"]
    for b in c["beats"]:
        a, e = b["t0"], b["t0"] + b.get("dur_v", b["dur"])
        if b.get("card"):
            st = "CardN" if re.search(r"\d", b["card"]) else "Card"
            ev.append(f"Dialogue: 4,{_ass_t(a + 0.25)},{_ass_t(e - 0.1)},{st},,0,0,0,,{{\\an9\\pos({RW - 46},{VID_Y + 40})\\fad(150,120)}}{_esc(b['card'].upper())}")
        if b["type"] == "bite" and b.get("tag", True):
            ev.append(f"Dialogue: 4,{_ass_t(a + 0.2)},{_ass_t(min(e, a + 3.5))},TagN,,0,0,0,,{{\\an1\\pos(46,{VID_Y + VID_H - 74})\\fad(150,150)}}{_esc(b['name'])}")
            if b.get("role"):
                ev.append(f"Dialogue: 4,{_ass_t(a + 0.2)},{_ass_t(min(e, a + 3.5))},TagR,,0,0,0,,{{\\an1\\pos(46,{VID_Y + VID_H - 26})\\fad(150,150)}}{_esc(b['role'])}")
    cap_y = VID_Y + VID_H + 70
    for ch in _chunks(words):
        for k, w in enumerate(ch):
            st = w["s"]; en = ch[k + 1]["s"] if k + 1 < len(ch) else max(w["e"], w["s"] + 0.25)
            txt = " ".join(("{\\c&H0066D1FF&}" + _esc(x["t"]) + "{\\c&H00FFFFFF&}") if x is w else _esc(x["t"]) for x in ch)
            ev.append(f"Dialogue: 2,{_ass_t(st)},{_ass_t(en)},Cap,,0,0,0,,{{\\an8\\pos({RW // 2},{cap_y})}}{txt}")
    mid = VID_Y + VID_H // 2
    ev.append(f"Dialogue: 3,{_ass_t(clip_len + 0.1)},{_ass_t(total)},End,,0,0,0,,{{\\an5\\pos({RW // 2},{mid - 40})\\fad(250,0)}}FULL STORY\\NON YOUTUBE")
    ev.append(f"Dialogue: 3,{_ass_t(clip_len + 0.3)},{_ass_t(total)},Sub,,0,0,0,,{{\\an5\\pos({RW // 2},{mid + 150})\\fad(250,0)}}LINK IN BIO")
    open(path, "w").write(hdr + "\n".join(ev) + "\n")


def reel_words(voice_wav, c):
    """Word timings straight from speech recognition of the reel's own voice track (narration + soundbites + CTA)."""
    from .qc import models as M
    _, hw = M.asr(voice_wav)
    out = []
    for w, a, e in hw:
        spk = next((b["type"] for b in c["beats"] if b["t0"] <= a < b["t0"] + b["dur"]), "end")
        out.append({"t": w, "s": a, "e": e, "spk": spk})
    return out


def render(proj, tl, c, out):
    rd = os.path.join(proj, "reel"); os.makedirs(rd, exist_ok=True)
    cta = voice_beats(proj, c)
    wav, vwav = os.path.join(rd, "reel_audio.wav"), os.path.join(rd, "reel_voice.wav")
    clip_len, total = build_audio(proj, c, cta, wav, vwav)
    words = reel_words(vwav, c)
    clip = build_video(proj, tl, c, clip_len)
    ass = os.path.join(rd, "reel.ass"); make_ass(ass, words, c, clip_len, total)
    card = total - clip_len
    v = (f"[0:v]setpts=PTS-STARTPTS,fps={C.FPS},tpad=stop_mode=clone:stop_duration={card + 0.5:.3f},trim=0:{total:.3f},split[a][b];"
         f"[a]scale=-2:{RH},crop={RW}:{RH},boxblur=28:2,eq=brightness=-0.25:saturation=0.75[bg];"
         f"[b]scale={RW}:{VID_H},boxblur=10:1:enable='gte(t,{clip_len:.3f})',"
         f"drawbox=x=0:y=0:w=iw:h=ih:color=0x0f1b2d@0.75:t=fill:enable='gte(t,{clip_len:.3f})'[fg];"
         f"[bg][fg]overlay=0:{VID_Y},ass='{ass}':fontsdir='{FONTS}',format=yuv420p[v]")
    tmp = out + ".tmp.mp4"
    _ff("-i", clip, "-i", wav, "-filter_complex", v + f";[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample={SR},alimiter=limit=0.79:level=false[aud]",
        "-map", "[v]", "-map", "[aud]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
        "-r", str(C.FPS), "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-movflags", "+faststart", tmp)
    os.replace(tmp, out)
    _ff("-ss", "1.2", "-i", out, "-frames:v", "1", "-q:v", "2", os.path.join(rd, "cover.jpg"))
    return {"clip_len": round(clip_len, 2), "total": round(total, 2), "words": words}


# ---------------------------------------------------------------- 4. checks
def _f(sev, check, msg):
    return {"severity": sev, "check": check, "msg": msg}



def check(proj, tl, c, out, meta, caption_txt):
    from .qc import models as M
    from .qc.stage1 import sim, norm_words, is_word
    F = []
    p = _probe(out); v = next((s for s in p["streams"] if s["codec_type"] == "video"), {}); a = next((s for s in p["streams"] if s["codec_type"] == "audio"), {})
    dur = float(p["format"]["duration"]); size = int(p["format"]["size"])
    if (v.get("width"), v.get("height")) != (RW, RH): F.append(_f("CRITICAL", "format", f"video is {v.get('width')}x{v.get('height')}, not {RW}x{RH} (9:16)"))
    if v.get("codec_name") != "h264" or v.get("pix_fmt") != "yuv420p": F.append(_f("CRITICAL", "format", f"video codec {v.get('codec_name')}/{v.get('pix_fmt')} (need h264/yuv420p)"))
    if v.get("r_frame_rate") not in (f"{C.FPS}/1",): F.append(_f("HIGH", "format", f"frame rate {v.get('r_frame_rate')}"))
    if a.get("codec_name") != "aac": F.append(_f("CRITICAL", "format", "no AAC audio track"))
    if not 20 <= dur <= 70: F.append(_f("CRITICAL", "length", f"reel is {dur:.1f} s (want 20-70, ideally 35-50)"))
    if size > 100e6: F.append(_f("HIGH", "format", f"file is {size / 1e6:.0f} MB"))
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
    for b in c["beats"]:
        if b.get("lip_risk"): F.append(_f("MEDIUM", "visual", f"narration at {b['t0']:.1f} s plays over a shot of someone talking ({b['scene']})"))
    # speech
    expected = " ".join(b["text"] for b in c["beats"]) + " " + c["cta"]
    wav = os.path.join(proj, "reel", "check.wav"); _ff("-i", out, "-vn", "-ac", "1", "-ar", "16000", wav)
    heard, hw = M.asr(wav)
    s = sim(expected, heard)
    if s < 0.8: F.append(_f("CRITICAL", "speech", f"audio doesn't match the planned summary (similarity {s:.2f})"))
    ew, hw_ = norm_words(expected), norm_words(heard)
    if ew[:3] and sim(" ".join(ew[:4]), " ".join(hw_[:4])) < 0.6: F.append(_f("HIGH", "speech", f"hook not heard at the start: \"{' '.join(hw_[:6])}\""))
    cw = norm_words(c["cta"])
    if sim(" ".join(cw[-4:]), " ".join(hw_[-5:])) < 0.6: F.append(_f("CRITICAL", "ending", f"closing line not heard at the end: \"{' '.join(hw_[-8:])}\""))
    if not [w for w in hw if w[1] > meta["clip_len"] - 0.05]: F.append(_f("CRITICAL", "ending", "nothing spoken over the end card"))
    # on-screen text
    fr = os.path.join(proj, "reel", "chk"); os.makedirs(fr, exist_ok=True)
    def grab(t, name):
        pth = os.path.join(fr, name); _ff("-ss", f"{t:.2f}", "-i", out, "-frames:v", "1", pth); return pth
    from PIL import Image
    head = grab(1.5, "head.png"); endf = grab(dur - 0.4, "end.png")
    ht = " ".join(t for t, _ in M.ocr(Image.open(head).crop((0, 120, RW, VID_Y))))
    if sim(c["hook"], ht) < 0.6: F.append(_f("HIGH", "text", f"headline not readable: OCR \"{ht}\" vs \"{c['hook']}\""))
    if any(not is_word(w) and len(w) >= 4 for w in norm_words(c["hook"])): F.append(_f("MEDIUM", "text", f"headline has odd words: {c['hook']}"))
    ws = [w for w in meta["words"] if w["s"] > 2 and w["e"] < meta["clip_len"] - 0.5 and w["spk"] == "vo"]
    if ws:
        w = ws[len(ws) // 2]; capf = grab((w["s"] + w["e"]) / 2, "cap.png")
        boxes = M.ocr(Image.open(capf).crop((0, VID_Y + VID_H, RW, 1560)))
        dup = M.ocr(Image.open(capf).crop((0, VID_Y + int(VID_H * 0.8), RW, VID_Y + VID_H)))
        if sim(" ".join(t for t, _ in dup), " ".join(x["t"] for x in ws if abs(x["s"] - w["s"]) < 2.5)) > 0.5:
            F.append(_f("HIGH", "text", "small YouTube captions are burned into the video too (double captions)"))
        if not boxes: F.append(_f("HIGH", "text", f"no captions visible at {w['s']:.1f} s"))
        elif any(bb[0] < 30 or bb[2] > RW - 30 for _, bb in boxes): F.append(_f("MEDIUM", "text", "captions touch the screen edge"))
    for b in c["beats"]:
        if b.get("card"):
            cf = grab(b["t0"] + min(1.2, b.get("dur_v", b["dur"]) / 2), "card.png")
            ct = " ".join(t for t, _ in M.ocr(Image.open(cf).crop((0, VID_Y, RW, VID_Y + 220))))
            if sim(b["card"], ct) < 0.6: F.append(_f("MEDIUM", "text", f"card '{b['card']}' not readable (OCR '{ct[:40]}')"))
            break
    et = " ".join(t for t, _ in M.ocr(endf)).upper()
    if "YOUTUBE" not in et.replace(" ", ""): F.append(_f("CRITICAL", "ending", f"end card text missing (OCR: {et[:60]})"))
    M.free()
    # caption rules
    if len(c["caption"]) + len(" ".join(c["hashtags"])) > 2200: F.append(_f("HIGH", "caption", "caption longer than 2200 characters"))
    if not 1 <= len(c["hashtags"]) <= MAX_TAGS: F.append(_f("HIGH", "caption", f"{len(c['hashtags'])} hashtags (Instagram allows {MAX_TAGS})"))
    if not re.search(r"link in (my |our )?bio", c["caption"], re.I): F.append(_f("HIGH", "caption", "caption does not say 'link in bio'"))
    if len(c["caption"]) < 60: F.append(_f("MEDIUM", "caption", "caption is very short"))
    # story judge
    try:
        j = llm.chat([{"role": "user", "content":
            "You review an Instagram Reel that summarises a longer news explainer for people who will not watch the full video.\n"
            f"WHAT THE REEL SAYS (speech recognition): {heard}\nON-SCREEN HEADLINE: {c['hook']}\n"
            f"ON-SCREEN CARDS: {[b['card'] for b in c['beats'] if b.get('card')]}\nINSTAGRAM CAPTION: {c['caption']}\n"
            f"FACTS AVAILABLE (the full video's script): {_facts(tl)}\n\n"
            "Answer strictly: whole_story = a first-time viewer gets the whole idea (what happened, why it matters, what comes next); "
            "standalone = no unexplained references or names; strong_hook = the first sentence makes you want to keep watching; "
            "proper_ending = ends with a wrap-up + pointer to YouTube, not mid-argument; facts_ok = every claim, number and name in the "
            "reel, headline and cards is supported by the script; caption_ok = the caption only states supported facts and fits the reel. "
            "Give a short reason for any false."}],
            temperature=0.0, max_tokens=2500,
            schema={"type": "object", "required": ["whole_story", "standalone", "strong_hook", "proper_ending", "facts_ok", "caption_ok", "reason"],
                    "properties": {k: {"type": "boolean"} for k in ("whole_story", "standalone", "strong_hook", "proper_ending", "facts_ok", "caption_ok")} | {"reason": {"type": "string"}}})
        for k, sev, nm in (("whole_story", "CRITICAL", "story"), ("standalone", "HIGH", "story"), ("strong_hook", "MEDIUM", "story"),
                           ("proper_ending", "CRITICAL", "ending"), ("facts_ok", "CRITICAL", "facts"), ("caption_ok", "HIGH", "caption")):
            if j.get(k) is False: F.append(_f(sev, nm, f"judge: {k} = false — {j.get('reason', '')[:180]}"))
    except Exception as e:
        F.append(_f("LOW", "story", f"story judge unavailable: {e}"))
    return F


# ---------------------------------------------------------------- 5. caption file + report
def caption_file(proj, sc, c, meta, ok, F, out):
    name = os.path.basename(out); nb = sum(b["type"] == "bite" for b in c["beats"])
    txt = (f"=== INSTAGRAM REEL ===\nVideo ................ reel/{name}  ({meta['total']:.0f} s, 1080x1920)\n"
           f"Cover ................ reel/cover.jpg (or pick a frame in the app)\nMade as .............. summary edit of the YouTube video "
           f"({len(c['beats'])} beats, {nb} soundbite{'s' if nb != 1 else ''}) + YouTube call to action\nChecks ............... "
           f"{'PASS' if ok else 'FAIL — see review/REEL_QC.md'}\n\n\n=== CAPTION (copy everything below) ===\n"
           f"{c['caption']}\n\n{' '.join(c['hashtags'])}\n\n\n=== SETTINGS ===\n"
           "Audio ................ keep original audio (music is already mixed in)\n"
           "AI label ............. turn ON \"AI info\" (AI-generated illustrations and animation)\n"
           "Link ................. caption says \"link in bio\" — your bio already has the YouTube link\n"
           "Share to Facebook .... optional\n")
    open(os.path.join(proj, "INSTAGRAM_REEL.txt"), "w").write(txt)
    return txt


def report(proj, c, F, ok, tries):
    rows = "\n".join(f"| {f['severity']} | {f['check']} | {f['msg']} |" for f in F) or "| — | — | no problems found |"
    beats = "\n".join(f"{k + 1}. `{b['t0']:.1f}s` " + (f"**{b['name']}** (soundbite, {b['ref']}): \"{b['text']}\"" if b["type"] == "bite"
                      else f"narrator over {b['scene']}: {b['text']}") + (f"  — card: **{b['card']}**" if b.get("card") else "")
                      for k, b in enumerate(c["beats"]))
    md = (f"# Instagram Reel QC — {'PASS' if ok else 'FAIL'}\n\nSummary edit, {len(c['beats'])} beats. Attempts: {tries}.\n\n"
          f"Headline: **{c['hook']}**\n\n{beats}\n\nEnd: _{c['cta']}_\n\n| Severity | Check | Finding |\n|---|---|---|\n{rows}\n")
    os.makedirs(os.path.join(proj, "review"), exist_ok=True)
    open(os.path.join(proj, "review", "REEL_QC.md"), "w").write(md)


# ---------------------------------------------------------------- driver
_W = {"CRITICAL": 10, "HIGH": 3, "MEDIUM": 1}


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
    if not force and state.get("master_mtime") == mm and state.get("ok") and state.get("v") == 2 and os.path.exists(out):
        log(proj, "up to date"); return out
    sc = json.load(open(os.path.join(proj, "script.json")))
    topic = open(os.path.join(proj, "TOPIC")).read().strip() if os.path.exists(os.path.join(proj, "TOPIC")) else sc["title"]
    tl = TL(proj)
    prev = state.get("plan") if state.get("v") == 2 else None
    feedback, best, tries = None, None, 0
    for attempt in range(3):
        if attempt == 0 and prev and not force and all(b["scene"] in tl.pr.props for b in prev["beats"]):
            c = json.loads(json.dumps(prev))
        else:
            c = plan(tl, topic, sc["title"], feedback)
            if not c: break
        llm.unload(); tries += 1
        log(proj, f"try {tries}: {len(c['beats'])} beats ({sum(b['type'] == 'bite' for b in c['beats'])} soundbites), hook \"{c['hook']}\"")
        meta = render(proj, tl, c, out)
        txt = caption_file(proj, sc, c, meta, False, [], out)
        F = check(proj, tl, c, out, meta, txt)
        serious = [f for f in F if f["severity"] in ("CRITICAL", "HIGH")]
        if serious and all(f["check"] == "caption" for f in serious):
            c["caption"] = with_cta(fix_caption(tl, c, serious)); log(proj, f"caption rewritten: {c['caption'][:90]}")
            txt = caption_file(proj, sc, c, meta, False, [], out)
            F = check(proj, tl, c, out, meta, txt)
        ok = not any(f["severity"] in ("CRITICAL", "HIGH") for f in F)
        score = sum(_W.get(f["severity"], 0) for f in F)
        if best is None or score < best[2]:
            best = (json.loads(json.dumps(c)), meta, score, F, ok); shutil.copy2(out, out + ".best.mp4")
        log(proj, f"checks {'PASS' if ok else 'FAIL'}: " + "; ".join(f"{f['severity']} {f['msg'][:80]}" for f in F if f["severity"] != "LOW")[:500])
        if ok: break
        feedback = [f["msg"] for f in F if f["severity"] in ("CRITICAL", "HIGH")]
        if not any(f["check"] in ("speech", "ending", "story", "facts", "length", "caption", "text") for f in F if f["severity"] in ("CRITICAL", "HIGH")):
            break                                           # not a planning problem: replanning wouldn't help
    if not best: log(proj, "no reel plan"); return None
    c, meta, _, F, ok = best
    os.replace(out + ".best.mp4", out)
    caption_file(proj, sc, c, meta, ok, F, out); report(proj, c, F, ok, tries)
    json.dump({"v": 2, "master_mtime": mm, "ok": ok, "plan": {k: c[k] for k in ("beats", "hook", "cta", "caption", "hashtags")}},
              open(state_p, "w"), indent=1)
    for f in ("reel_audio.wav", "reel_voice.wav", "check.wav", "clip_v.mp4"):
        if os.path.exists(os.path.join(rd, f)): os.remove(os.path.join(rd, f))
    shutil.rmtree(os.path.join(rd, "segs"), ignore_errors=True)
    log(proj, f"{'PASS' if ok else 'FAIL'} -> {out} ({meta['total']:.0f} s)")
    return out


if __name__ == "__main__":
    make(sys.argv[1], force="--force" in sys.argv)
