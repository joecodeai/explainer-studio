"""Show episodes on MiniMax H3 (ARCHITECTURE_V2.md).

Every stage scene becomes a few *beat shots* (1-3 consecutive lines, <= 12 s) in a fixed camera setup:
  two = medium-close two-shot, single_<char> = medium close-up on one character, solo = one-person scene.
Each shot is H3 Ref2VA at 864x480 (Flex 6-step) with OUR scene audio pinned at frame 0 (lip-sync to our voices) and either a
fresh keyframe or - when the camera setup is unchanged from the previous shot - the previous shot's last 5 frames (one
continuous take; a fresh keyframe there makes the pose snap back = the b1->b2 glitch). Shots are upscaled to 1080p, checked
(qc.animcheck + our-audio check), failures re-rendered with a new seed (a replaced shot also re-renders the rest of its take).
Writes talk/<scene>.json manifests and talk/ANIMATION_QC.json like the other talk stages.
"""
import hashlib, json, os, re, shutil, subprocess, time
import numpy as np, soundfile as sf
from PIL import Image
from . import assets, comfy, h3, llm
from . import config as C
from .pipeline import log, _j, _conv_still, _pose_img_any, _tag, TAIL

MAX_SHOT, MAX_LINES, SPLIT_LONG = 12.0, 3, 15.0
SIZE, HERO_SIZE = (864, 480), (1344, 768)
V_SIZE, V_HERO = (480, 864), (768, 1344)            # native 9:16 (reels): same pixel budget, portrait


def sizes():
    return (V_SIZE, V_HERO) if C.FORMAT == "vertical" else (SIZE, HERO_SIZE)


def _vertical(size):
    return size[1] > size[0]
BASE = (1280, 768)                                  # composite still; crops below are in this frame
CROP = {"two": (145, 40, 1135, 590), "left": (141, 30, 781, 390), "right": (499, 30, 1139, 390), "solo": (290, 20, 990, 414)}
CLOTHES = re.compile(r"hoodie|jacket|shirt|t-shirt|trousers|jeans|sweater|\btop\b|coat|dress|\bbag\b|strap|watch|sneakers|apron|badge|"
                     r"suit|blazer|skirt|boots|shoes|cargo", re.I)
VOICE = {"benny": "a lively, warm young male voice", "maya": "a calm, dry, warm female voice"}
SUBJ_RE = re.compile(r"\bthe (?:young |older |)(?:man|woman|person|guy|girl|clerk)(?: [a-z ]{0,40}?)? on the (left|right)\b", re.I)


# ---------------------------------------------------------------- shot list
def compile_shots(s, lines, end, cast_ids):
    """Group a scene's timed lines into beat shots and pick each shot's camera setup."""
    src = s.get("lines", [])
    items = []
    for i, ln in enumerate(lines):
        d = src[i] if i < len(src) else {}
        it = {"spk": ln["speaker"], "t0": ln["start"], "t1": ln["end"], "text": ln.get("text") or d.get("text", ""),
              "act": d.get("act", ""), "react": d.get("react", ""), "pause_after": d.get("pause_after"), "shot": d.get("shot", "two_shot")}
        if it["t1"] - it["t0"] > SPLIT_LONG:             # very long line: split by time, words shared out proportionally
            n = int(np.ceil((it["t1"] - it["t0"]) / MAX_SHOT)); words = it["text"].split(); dt = (it["t1"] - it["t0"]) / n
            for k in range(n):
                items.append({**it, "t0": it["t0"] + k * dt, "t1": it["t0"] + (k + 1) * dt,
                              "text": " ".join(words[len(words) * k // n: len(words) * (k + 1) // n])})
        else:
            items.append(it)
    if not items:                                        # silent visual beat (s["hold"]): one held/action shot
        setup = "solo" if len(cast_ids) < 2 else (f"single_{cast_ids[0]}" if C.FORMAT == "vertical" else "two")
        return [{"k": 0, "a": 0.0, "b": round(end, 3), "setup": setup, "main": None, "lines": [], "action": s.get("action", "")}]
    vert = C.FORMAT == "vertical"
    groups = []
    for it in items:
        close = it["shot"] == "closeup" and it["spk"] in cast_ids
        g = groups[-1] if groups else None
        spk_change = vert and g and it["spk"] in cast_ids and any(x["spk"] in cast_ids and x["spk"] != it["spk"] for x in g["lines"])
        if g and not close and not g["close"] and not spk_change and it["t1"] - g["lines"][0]["t0"] <= MAX_SHOT and len(g["lines"]) < MAX_LINES:
            g["lines"].append(it)
        else:
            groups.append({"lines": [it], "close": close})
    shots, run = [], 0
    for k, g in enumerate(groups):
        a = 0.0 if k == 0 else g["lines"][0]["t0"]
        b = groups[k + 1]["lines"][0]["t0"] if k + 1 < len(groups) else end
        on = [x["spk"] for x in g["lines"] if x["spk"] in cast_ids]
        main = max(set(on), key=lambda c: sum(x["t1"] - x["t0"] for x in g["lines"] if x["spk"] == c)) if on else None
        if len(cast_ids) < 2: setup = "solo"
        elif vert: setup = f"single_{main or (shots[-1]['main'] if shots and shots[-1]['main'] else cast_ids[0])}"   # 9:16 holds one face
        elif g["close"] and main: setup = f"single_{main}"
        elif run >= 3 and main and len(set(on)) == 1: setup = f"single_{main}"     # variety after ~30 s of two-shot
        else: setup = "two"
        run = run + 1 if setup == "two" else 0
        shots.append({"k": k, "a": round(a, 3), "b": round(b, 3), "setup": setup, "main": main, "lines": g["lines"]})
    return shots


# ---------------------------------------------------------------- pictures
def _ref_portrait(cid, outfit, work):
    """Identity reference: the character's own art for this outfit, head and upper body on light grey."""
    art = assets.art_id(cid, outfit)
    out = f"{work}/refs/{art}.png"
    if os.path.exists(out): return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = Image.open(_pose_img_any(art, "neutral")).convert("RGBA")
    x0, y0, x1, y1 = im.getbbox() or (0, 0, im.width, im.height)
    im = im.crop((x0, y0, x1, y0 + int((y1 - y0) * 0.55)))
    bg = Image.new("RGBA", im.size, (235, 235, 235, 255)); bg.alpha_composite(im)
    bg.convert("RGB").save(out); return out


def _keyframe_v(bg, cast, setup, size, work, sid):
    """9:16 keyframe: a portrait window of the 16:9 painted background + ONE character, medium shot (head in the upper third,
    framed to mid-thigh), turned toward where the other person stands off-screen."""
    from PIL import ImageOps
    out = f"{work}/{sid}_kfv_{setup}_{size[0]}.png"
    if os.path.exists(out): return out
    W, H = 1080, 1920
    who = cast[0] if setup == "solo" else next(c for c in cast if c["char"] == setup[7:])
    left = len(cast) < 2 or cast.index(who) == 0
    B = Image.open(bg).convert("RGB"); k = H / B.height; B = B.resize((int(B.width * k), H), Image.LANCZOS)
    cx = int(B.width * (0.38 if left else 0.62)) if len(cast) > 1 else B.width // 2
    x0 = max(0, min(B.width - W, cx - W // 2)); B = B.crop((x0, 0, x0 + W, H))
    pose = "side_listen" if len(cast) > 1 else "neutral"     # calm, mouth closed: H3 animates speech from our audio
    ch = Image.open(_pose_img_any(assets.art_id(who["char"], who.get("outfit")), pose)).convert("RGBA")
    if not left: ch = ImageOps.mirror(ch)
    bb = ch.getbbox() or (0, 0, ch.width, ch.height); ch = ch.crop(bb)
    hpx = int(H * 1.95); ch = ch.resize((max(1, int(ch.width * hpx / ch.height)), hpx), Image.LANCZOS)
    B = B.convert("RGBA"); B.alpha_composite(ch, (int(W / 2 - ch.width / 2), int(H * 0.09)))
    B.convert("RGB").resize(size, Image.LANCZOS).save(out)
    return out


def _keyframe(bg, cast, setup, size, work, sid):
    if _vertical(size): return _keyframe_v(bg, cast, setup, size, work, sid)
    base = f"{work}/{sid}_base.png"
    if not os.path.exists(base):
        _conv_still.variant = 0
        _conv_still(bg, cast, base, size=BASE)
    side = {c["char"]: ("left" if i == 0 else "right") for i, c in enumerate(cast)}
    box = CROP["solo"] if setup == "solo" else CROP["two"] if setup == "two" else CROP[side[setup[7:]]]
    out = f"{work}/{sid}_kf_{setup}_{size[0]}.png"
    Image.open(base).convert("RGB").crop(box).resize(size, Image.LANCZOS).save(out)
    return out


# ---------------------------------------------------------------- prompt (official H3 three-field format)
def _face_and_wear(c, outfit):
    parts = [p.strip() for p in c.get("look", "").split(",") if p.strip()]
    cut = next((i for i, p in enumerate(parts) if CLOTHES.search(p)), len(parts))
    face, wear = ", ".join(parts[:cut]), ", ".join(parts[cut:])
    if outfit:
        t = _tag(c, outfit)
        if " in the " in t: wear = t.split(" in the ", 1)[1]
        od = ((c.get("outfits") or {}).get(outfit) or {}).get("desc", "")
        hair = re.search(r"hair (?:in|up|tied|pulled|worn)[^,]*", od)
        if hair:                                     # e.g. home outfit = hair in a loose bun: say it, and drop the base 'long wavy hair'
            face = ", ".join([p for p in face.split(", ") if "hair" not in p] + [hair.group(0)])
            wear = ", ".join(p for p in wear.split(", ") if "hair" not in p)
    return face, wear


def _voice(c):
    if c["id"] in VOICE: return VOICE[c["id"]]
    return "a friendly female voice" if re.search(r"\b(woman|girl|she)\b", c.get("look", ""), re.I) else "a friendly male voice"


def build_prompt(sh, cast, chars, place):
    side = {c["char"]: ("left" if i == 0 else "right") for i, c in enumerate(cast)}
    offs = []
    if sh["setup"].startswith("single_"):                 # a close-up holds ONLY its character; the other is an off-screen voice
        offs = [c["char"] for c in cast if c["char"] != sh["setup"][7:]]
        cast = [c for c in cast if c["char"] == sh["setup"][7:]]
    subj = {c["char"]: f"<Subject {i + 1}>" for i, c in enumerate(cast)}
    by_side = {side[k]: subj[k] for k in subj}
    for o in offs: by_side[side[o]] = "the person off-screen"
    fix = lambda t: SUBJ_RE.sub(lambda m: by_side.get(m.group(1).lower(), m.group(0)), t or "").strip().rstrip(".")
    P = ["For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.", "", "subject_definitions:"]
    for i, c in enumerate(cast):
        ch = chars[c["char"]]; face, wear = _face_and_wear(ch, c.get("outfit"))
        where = f"the person on the {side[c['char']]}" if len(cast) > 1 else "the person"
        P.append(f"{subj[c['char']]} is {ch.get('name', c['char'])}, {where} in <Picture 1>, whose face and hair follow <Picture {i + 2}> "
                 f"exactly: {face}; wearing {wear}.")
    P += ["Do not carry over the plain grey backgrounds of the reference pictures, and add no bags, props or text that are not in <Picture 1>.",
          "", "integrated_multimodal_description:",
          f"2D hand-drawn anime cartoon exactly matching <Picture 1>: clean ink line art, flat cel shading, warm natural light, in {place}. "
          "Expressions are subtle and natural, never exaggerated; hands have five fingers."]
    st = sh["setup"]
    if st == "two":
        frame = f"[Shot 1] Medium two-shot, {by_side['left']} on the left facing right, {by_side['right']} on the right facing left, looking at each other."
    elif st == "solo":
        frame = f"[Shot 1] Medium shot of {subj[cast[0]['char']]}."
    else:
        who = st[7:]
        frame = (f"[Shot 1] Medium close-up on {subj[who]}" + (f", who is talking with someone off-screen to the {side[offs[0]]}" if offs else "") +
                 ". The camera stays on this tight close-up for the whole clip and never zooms or pulls out; nobody else ever enters the shot.")
    n = len(cast)
    P.append(frame + f" There {'is exactly one person' if n == 1 else f'are exactly {n} people'} in the scene and nobody else; "
             "each character appears only once and stays in place. The camera holds a static shot with no zoom and no movement for the whole clip.")
    for x in sh["lines"]:
        at = f"At 00:{max(0.0, x['t0'] - sh['a']):06.3f}, " if x["t0"] - sh["a"] > 0.2 else ""
        if x["spk"] in subj:
            others = [subj[c] for c in subj if c != x["spk"]]
            act = fix(x["act"]) or "talks naturally"
            act = re.sub(r"^" + re.escape(subj[x["spk"]]) + r"\s*", "", act)
            line = f"{at}{subj[x['spk']]} ({'S%d' % (list(subj).index(x['spk']) + 1)}), in {_voice(chars[x['spk']])}, {act}, and says: <d>[English] {x['text']}</d>"
            if others:
                line += f" While {subj[x['spk']]} speaks, {' and '.join(others)} keeps their lips completely closed" + (f": {fix(x['react'])}." if x["react"] else ".")
        elif x["spk"] in offs:                           # the other character, off-screen in this close-up
            line = (f"{at}{chars[x['spk']].get('name', x['spk'])} (S{len(subj) + 1}), off-screen to the {side[x['spk']]}, says in an off-screen voice: "
                    f"<d>[English] {x['text']}</d> while {' and '.join(subj.values())} listens with lips completely closed"
                    + (f": {fix(x['react'])}." if x["react"] else "."))
        elif x["spk"] in chars and x["spk"] != "narrator":   # a character heard but not seen (on the phone, on a call)
            line = (f"{at}{chars[x['spk']].get('name', x['spk'])} (S9) is heard off-screen, as a voice on a phone or call, saying: "
                    f"<d>[English] {x['text']}</d> while {' and '.join(subj.values())} listens with lips completely closed"
                    + (f": {fix(x['react'])}." if x["react"] else "."))
        else:                                            # narrator / off-screen voice
            line = (f"{at}An off-screen narrator (S9) says in an off-screen voiceover: <d>[English] {x['text']}</d> while everyone on screen "
                    f"keeps their lips completely closed" + (f"; {fix(x['act'] or x['react'])}." if (x["act"] or x["react"]) else "; they react naturally."))
        P.append(line)
        if x.get("pause_after") and float(x["pause_after"]) >= 0.5:
            P.append(f"Then a short silent beat, all mouths closed" + (f": {fix(x['react'])}." if x["react"] else "."))
    if not sh["lines"]:                                  # silent visual beat
        act = fix(sh.get("action")) or "holds still with a small natural expression, only blinking and breathing"
        P.append(f"{' and '.join(subj.values())} {act}. Nobody speaks; all mouths stay closed.")
    elif sh["b"] - sh["lines"][-1]["t1"] > 0.8:           # a silent tail (end of scene): hold, or H3 improvises action to fill it
        P.append("After the last line everyone holds still in place with a small natural expression, only blinking and breathing; "
                 "nobody walks, enters or leaves, and the framing does not change.")
    P += ["", "overall_soundscape:", f"Quiet room tone of {place}; no other voices.", "", "non_diegetic_music:", "N/A"]
    return "\n".join(P)


# ---------------------------------------------------------------- media helpers
def _ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def _slice(audio, sr, a, b, total, out):
    """Exact scene-audio slice [a, b), padded with silence to the clip length (32 kHz stereo for the H3 audio VAE)."""
    seg = audio[int(a * sr): int(b * sr)]
    pad = np.zeros((int(total * sr),) + audio.shape[1:], np.float32); pad[:len(seg)] = seg[:len(pad)]
    tmp = out + ".tmp.wav"; sf.write(tmp, pad, sr)
    _ff("-i", tmp, "-ar", "32000", "-ac", "2", out); os.remove(tmp)
    return out


def _tail(raw, n_used, clip, png):
    """The previous shot's last 5 used frames (the take's hand-off) + its last frame as <Picture 1>."""
    s = max(0, n_used - 5)
    _ff("-i", raw, "-vf", f"select='between(n\\,{s}\\,{n_used - 1})',setpts=N/24/TB", "-an", "-r", "24", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", clip)
    _ff("-i", raw, "-vf", f"select='eq(n\\,{n_used - 1})'", "-frames:v", "1", png)


REL_SINGLE = {"left": (0.008, 0.0, 0.628, 0.62), "right": (0.370, 0.0, 0.990, 0.62)}   # close-up window in a two-shot frame (relative)


def _from_state(shots, i, base):
    """Keyframe for a camera-angle change, taken from what the audience last saw in this scene (the last two-shot frame, or a
    crop of it around the close-up's character), so a cut never snaps the characters back to the default still."""
    sh = shots[i]
    if _vertical(sh["size"]):
        p = next((x for x in reversed(shots[:i]) if x["scene"] == sh["scene"] and x["setup"] == sh["setup"] and x.get("final")), None)
        if not p: return None
        import cv2
        cap = cv2.VideoCapture(p["final"]); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, min(n - 1, round((p["b"] - p["a"]) * 24) - 1))); ok, fr = cap.read(); cap.release()
        if not ok: return None
        out = base + f"_state_{sh['setup']}.png"
        Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).resize(tuple(sh["size"]), Image.LANCZOS).save(out)
        return out
    p = next((x for x in reversed(shots[:i]) if x["scene"] == sh["scene"] and x["setup"] == "two" and x.get("final")), None)
    if not p or sh["setup"] not in ("two",) and not sh["setup"].startswith("single_"): return None
    import cv2
    cap = cv2.VideoCapture(p["final"]); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, min(n - 1, round((p["b"] - p["a"]) * 24) - 1))); ok, fr = cap.read(); cap.release()
    if not ok: return None
    im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)); W, H = im.size
    if sh["setup"].startswith("single_"):
        ids = [c["char"] for c in sh["cast"]]
        x0, y0, x1, y1 = REL_SINGLE["left" if ids.index(sh["setup"][7:]) == 0 else "right"]
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    out = base + f"_state_{sh['setup']}.png"
    from PIL import ImageFilter                       # a close-up is a ~1.6x enlargement of the two-shot: re-sharpen the line art
    im = im.resize(tuple(sh["size"]), Image.LANCZOS)
    if sh["setup"].startswith("single_"): im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=110, threshold=2))
    im.save(out)
    return out


def _finish(raw, dur, out, fresh=True, ref=None):
    """1080p, trimmed to the shot, COLOUR-LOCKED to its own first frame. H3 slowly drifts in brightness/tint over a clip, so at a cut
    a drifted shot end met a fresh shot start (a visible lighting jump). Per frame we pull the LAB mean/spread (temporally smoothed)
    back to the opening frames', within tight limits (no flicker). A fresh-keyframe shot also holds frame 2 over frames 0-1 (the
    pasted keyframe pops when H3 redraws it); timing, so lip-sync, is unchanged. `ref` = the image the shot started from (the last
    frame the audience saw, or its close-up crop): lock to IT, because H3 has already re-lit the picture by frame 2."""
    import cv2
    need = max(1, int(round(dur * 24)))
    cap = cv2.VideoCapture(raw); fr = []
    while len(fr) < need:
        ok, f = cap.read()
        if not ok: break
        fr.append(f)
    cap.release()
    fr += [fr[-1]] * (need - len(fr))
    if fresh and len(fr) > 3: fr[0] = fr[1] = fr[2]
    lab = [cv2.cvtColor(f, cv2.COLOR_BGR2LAB).astype(np.float32) for f in fr]
    mu = np.array([x.reshape(-1, 3).mean(0) for x in lab]); sd = np.array([x.reshape(-1, 3).std(0) for x in lab]) + 1e-3
    k = 9
    sm = lambda a: np.array([np.concatenate([a[:1].repeat(k, 0), a, a[-1:].repeat(k, 0)])[i:i + 2 * k + 1].mean(0) for i in range(len(a))])
    mu, sd = sm(mu), sm(sd); mu0, sd0 = mu[:3].mean(0), sd[:3].mean(0)
    h, w = fr[0].shape[:2]
    if ref:
        r = cv2.cvtColor(cv2.resize(cv2.imread(ref), (w, h), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2LAB).astype(np.float32).reshape(-1, 3)
        mu0, sd0 = r.mean(0), r.std(0) + 1e-3
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", "24", "-i", "-", "-an",
                          "-vf", ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.5" if h > w else
                                  "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,unsharp=5:5:0.5"),
                          "-r", str(C.FPS), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for x, m, sdev in zip(lab, mu, sd):
        g = np.clip(sd0 / sdev, 0.82, 1.18)
        y = (x - m) * g + m + np.clip(mu0 - m, -24, 24)
        p.stdin.write(cv2.cvtColor(np.clip(y, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode: raise RuntimeError(f"finishing {raw} failed")


def _env(x, sr, hop=0.05):
    m = x.mean(axis=1) if x.ndim > 1 else x; n = int(sr * hop)
    return np.array([np.sqrt((m[i:i + n] ** 2).mean()) for i in range(0, len(m) - n, n)])


def _audio_ok(raw, slice_wav):
    """H3 must hand back OUR audio (it is pinned); a low correlation means the anchor did not take."""
    t = raw + ".a.wav"; _ff("-i", raw, "-ac", "1", "-ar", "16000", t)
    a, _ = sf.read(slice_wav); b, _ = sf.read(t); os.remove(t)
    ea, eb = _env(a, 32000), _env(b, 16000); n = min(len(ea), len(eb))
    if n < 10 or ea[:n].std() < 1e-4: return 1.0
    return float(np.corrcoef(ea[:n], eb[:n])[0, 1])


def acc_key(sh):
    """Identity of a shot for the accepted-shots registry: what is said and when, in which framing (not the prompt wording)."""
    lines = "|".join(f"{x['spk']}:{x['text']}" for x in sh["lines"])
    return hashlib.md5(f"{sh['scene']}|{sh['k']}|{sh['a']:.3f}|{sh['b']:.3f}|{sh['setup']}|{lines}".encode()).hexdigest()[:16]


# ---------------------------------------------------------------- the stage
def stage_h3(proj, sc):
    from .qc import animcheck as A, core as QC
    chars = {c["id"]: c for c in sc["characters"]}
    envs = {e["id"]: e for e in sc["environments"]}
    work = f"{proj}/work/h3"; cache = f"{proj}/talk/h3"
    for d in (work, cache, f"{proj}/talk"): os.makedirs(d, exist_ok=True)
    scenes = [s for s in sc["scenes"] if s["kind"] == "stage" and s.get("cast") and envs.get(s.get("environment"), {}).get("_file")
              and os.path.exists(f"{proj}/audio/{s['id']}.wav") and (_j(f"{proj}/audio/{s['id']}.lines.json") or s.get("hold"))]
    if not scenes: return set()
    tries = int(os.environ.get("H3_TRIES", "2")); hero = os.environ.get("H3_HERO", "1") == "1"
    vlm_every = int(os.environ.get("H3_VLM_EVERY", "2"))

    # 1) shot list for the whole video
    shots, prev = [], None
    chosen = _j(f"{cache}/chosen_attempts.json") or {}     # the attempt QC picked last time (a restart does not redo retries)
    for s in scenes:
        cast = s["cast"][:2]; ids = [c["char"] for c in cast]
        lines = _j(f"{proj}/audio/{s['id']}.lines.json") or []
        end = s["_dur"] + TAIL + 2.6
        place = envs[s["environment"]]["prompt"].split(":")[0].split(".")[0]
        take_key = (s["environment"], tuple((c["char"], c.get("outfit")) for c in cast))
        for sh in compile_shots(s, lines, end, ids):
            sh.update(scene=s["id"], cast=cast, place=place, take=take_key, env=envs[s["environment"]]["_file"])
            sh["cont"] = bool(prev and prev["take"] == take_key and prev["setup"] == sh["setup"])
            sz, hz = sizes()
            sh["size"] = hz if hero and not shots else sz
            sh["prompt"] = build_prompt(sh, cast, chars, place)
            sh["refs"] = [_ref_portrait(c["char"], c.get("outfit"), work) for c in cast
                          if not sh["setup"].startswith("single_") or c["char"] == sh["setup"][7:]]
            sh["seed0"] = int(hashlib.md5(f"{s['id']}|{sh['k']}|{sh['prompt']}".encode()).hexdigest()[:7], 16)
            sh["akey"] = f"{s['id']}|{sh['k']}|{sh['seed0']}"
            sh["attempt"] = int(chosen.get(sh["akey"], 0))
            shots.append(sh); prev = sh
    log(proj, f"h3: {len(shots)} shots for {len(scenes)} scenes ({sum(sh['cont'] for sh in shots)} continue a take)")
    acc = _j(f"{cache}/accepted.json") or {}            # finished shots are locked: later code/prompt changes never re-render them
    for sh in shots:
        sh["acc"] = acc_key(sh)
        e = acc.get(sh["acc"])
        if e and os.path.exists(e["raw"]) and os.path.exists(e["final"]):
            sh.update(raw=e["raw"], final=e["final"], qc=e.get("qc") or {"findings": [], "ok": True, "score": 0}, locked=True)
    for i, sh in enumerate(shots):                      # a re-rendered shot invalidates the rest of its continuous take
        if i and sh["cont"] and sh.get("locked") and not shots[i - 1].get("locked"): sh.pop("locked")
    nl = sum(bool(sh.get("locked")) for sh in shots)
    if nl: log(proj, f"h3: {nl} accepted shot(s) reused as they are, {len(shots) - nl} to render")
    audio = {}

    def render(i):
        sh = shots[i]
        if sh.get("locked"): return
        if sh["scene"] not in audio: audio[sh["scene"]] = sf.read(f"{proj}/audio/{sh['scene']}.wav", dtype="float32")
        wav, sr = audio[sh["scene"]]
        dur = sh["b"] - sh["a"]; total = h3.frames_for(dur) / 24
        base = f"{work}/{sh['scene']}_{sh['k']}"
        sh["slice"] = _slice(wav, sr, sh["a"], sh["b"], total, base + ".wav")
        guide = None
        if sh["cont"] and shots[i - 1].get("final"):
            p = shots[i - 1]
            kf = base + "_from_prev.png"; guide = base + "_from_prev.mp4"
            _tail(p["final"], round((p["b"] - p["a"]) * 24), guide, kf)       # colour-locked frames
        else:
            kf = _from_state(shots, i, base) or _keyframe(sh["env"], sh["cast"], sh["setup"], sh["size"], work, sh["scene"])
        seed = sh["seed0"] + 7919 * sh["attempt"]
        key = hashlib.md5(b"".join(open(f, "rb").read() for f in [kf, sh["slice"]] + sh["refs"] + ([guide] if guide else []))
                          + f"{sh['prompt']}|{sh['size']}|{seed}|flex".encode()).hexdigest()[:16]
        raw, fin = f"{cache}/{key}.mp4", f"{cache}/{key}_1080c.mp4"
        if not os.path.exists(raw):
            t0 = time.time()
            h3.render(raw + ".part.mp4", keyframe=kf, refs=sh["refs"], audio=sh["slice"], prompt=sh["prompt"], size=sh["size"],
                      seconds=dur, seed=seed, mode="flex", guide_clip=guide)
            os.replace(raw + ".part.mp4", raw)
            log(proj, f"h3 {sh['scene']}#{sh['k']} {sh['setup']}{' (continues take)' if guide else ''} {dur:.1f}s "
                      f"attempt {sh['attempt'] + 1}: {time.time() - t0:.0f}s")
        if not os.path.exists(fin): _finish(raw, dur, fin, fresh=not guide, ref=kf)
        sh["raw"], sh["final"] = raw, fin

    def qc_one(sh, cfg):
        ids = [c["char"] for c in sh["cast"]]
        main = sh["main"]
        silent = main is None
        aud = sh["slice"]
        if main and len({x["spk"] for x in sh["lines"] if x["spk"] in ids}) > 1:     # mute the other speaker: main mouth on its words only
            x, sr = sf.read(aud, dtype="float32")
            for ln in sh["lines"]:
                if ln["spk"] != main:
                    x[int(max(0, ln["t0"] - sh["a"]) * sr): int((ln["t1"] - sh["a"]) * sr)] = 0
            aud = aud.replace(".wav", "_main.wav"); sf.write(aud, x, sr)
        side = None
        if sh["setup"] == "two" and main: side = "left" if ids.index(main) == 0 else "right"
        n_people = len(ids) if sh["setup"] == "two" else 1
        desc = (f"{len(ids)} animated cartoon characters talking in {sh['place']}" if sh["setup"] == "two"
                else f"a medium close-up of one animated cartoon character in {sh['place']}")
        try:
            r = A.check_shot(sh["final"], aud, desc, n_people, refs=sh["refs"], silent=silent, work=work, cfg=cfg,
                             speaker_side=side, vlm_every=vlm_every, twos=True)     # H3 animates on twos
        except Exception as e:
            r = {"findings": [{"severity": "MEDIUM", "check": "qc", "msg": f"check crashed: {e!r}", "frame": None, "t": None}], "score": 1, "ok": True}
        r = json.loads(json.dumps(r))
        for f in r["findings"]:                          # fewer people seen = the detector missing someone (dark clothes on a dark
            if f["check"] == "people" and f["severity"] == "HIGH":   # background), or a close-up; MORE people = a real duplicate, stays HIGH
                seen = [int(v) for v in re.findall(r"\d+", f["msg"].split("saw", 1)[-1].split("in", 1)[0])]
                if seen and max(seen) < n_people: f["severity"] = "MEDIUM"   # close-ups hold ONE person: an extra one is a real fail
        for f in r["findings"]:                          # on twos a fast natural gesture steps 7-10 per drawing; a real pop/cut is 12+
            if f["check"] == "glitch" and f["severity"] == "HIGH" and "sudden jump" in f["msg"]:
                m = re.search(r"change ([0-9.]+)", f["msg"])
                if m and float(m.group(1)) < 12: f["severity"] = "MEDIUM"
        corr = _audio_ok(sh["raw"], sh["slice"])
        if corr < 0.8:
            r["findings"].append({"severity": "HIGH", "check": "audio", "msg": f"H3 did not keep our voice track (corr {corr:.2f})", "frame": None, "t": None})
        r["ok"] = not any(f["severity"] in ("CRITICAL", "HIGH") for f in r["findings"])
        r["score"] = sum(A.SEV_W[f["severity"]] for f in r["findings"])
        return r

    def gpu_to_h3():
        comfy.free(); llm.unload()
        from .qc import models as QM
        QM.free()

    def gpu_to_qc():
        h3.free()

    # 2) render everything in order (takes continue from the previous shot's real frames)
    gpu_to_h3()
    for i in range(len(shots)):
        try: render(i)
        except Exception as e: log(proj, f"h3 {shots[i]['scene']}#{shots[i]['k']} failed: {e!r}")
    # 3) QC; failures get a new seed, and every later shot of the same continuous take is re-rendered from the new frames
    gpu_to_qc(); cfg = QC.load_config(proj)
    for sh in shots:
        if sh.get("final") and not sh.get("locked"): sh["qc"] = qc_one(sh, cfg)
    for rnd in range(1, tries):
        bad = [i for i, sh in enumerate(shots) if sh.get("final") and not sh.get("locked") and not sh["qc"]["ok"]]
        if not bad: break
        log(proj, f"h3 QC round {rnd}: re-rendering {len(bad)} shot(s)")
        gpu_to_h3()
        old = {}
        for i in bad:
            sh = shots[i]; old[i] = {k: sh[k] for k in ("raw", "final", "qc", "attempt")}
            sh["attempt"] = old[i]["attempt"] + 1
            try: render(i)
            except Exception as e: log(proj, f"h3 retry {sh['scene']}#{sh['k']} failed: {e!r}"); sh.update(old.pop(i))
        gpu_to_qc()
        redo = []
        for i in list(old):
            sh = shots[i]; r = qc_one(sh, cfg)
            if r["score"] < old[i]["qc"]["score"]:
                sh["qc"] = r; j = i + 1
                while j < len(shots) and shots[j]["cont"]: redo.append(j); shots[j].pop("locked", None); j += 1
            else:
                sh.update(old[i])
        redo = sorted(set(redo) - set(old))
        if redo:
            gpu_to_h3()
            for j in redo:
                try: render(j)
                except Exception as e: log(proj, f"h3 take re-render {shots[j]['scene']}#{shots[j]['k']} failed: {e!r}")
            gpu_to_qc()
            for j in redo: shots[j]["qc"] = qc_one(shots[j], cfg)
    from .qc import models as QM
    QM.free(); llm.unload()
    _j(f"{cache}/chosen_attempts.json", {sh["akey"]: sh["attempt"] for sh in shots})
    _j(f"{cache}/accepted.json", {**acc, **{sh["acc"]: {"raw": sh["raw"], "final": sh["final"], "qc": sh.get("qc")} for sh in shots if sh.get("final")}})
    # 4) manifests + report
    report, done = [], set()
    for s in scenes:
        mine = [sh for sh in shots if sh["scene"] == s["id"]]
        if not all(sh.get("final") for sh in mine):
            log(proj, f"h3: scene {s['id']} incomplete, falls back"); continue
        json.dump([{"video": sh["final"], "start": sh["a"], "end": sh["b"]} for sh in mine], open(f"{proj}/talk/{s['id']}.json", "w"), indent=1)
        done.add(s["id"])
        for sh in mine:
            q = sh.get("qc") or {"findings": [], "ok": False}
            report.append({"scene": s["id"], "line": sh["k"], "start": sh["a"], "end": sh["b"], "video": sh["final"], "setup": sh["setup"],
                           "continues_take": sh["cont"], "ok": q.get("ok", False), "attempts": sh["attempt"] + 1,
                           "chosen_attempt": sh["attempt"] + 1, "findings": q.get("findings", [])})
    json.dump(report, open(f"{proj}/talk/ANIMATION_QC.json", "w"), indent=1)
    log(proj, f"h3: {len(done)}/{len(scenes)} scenes animated; QC {sum(r['ok'] for r in report)}/{len(report)} shots clean")
    return done
