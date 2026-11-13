"""QC core: findings, severity, scoring, config, cache, project timeline, and an exact port of the renderer's
character/camera geometry (so checks know where every face, mouth and foot is on screen at any time)."""
import hashlib, json, math, os, subprocess, time
from dataclasses import dataclass, field, asdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1920, 1080, 30

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
WEIGHT = {"CRITICAL": 40, "HIGH": 12, "MEDIUM": 4, "LOW": 1}
CATEGORIES = {   # report category -> score bucket
    "physical": "Physical positioning", "anatomy": "Character consistency", "identity": "Character consistency",
    "animation": "Animation quality", "lipsync": "Lip synchronization", "audio": "Audio quality", "voice": "Audio quality",
    "subtitle": "Subtitle accuracy", "text": "Subtitle accuracy", "continuity": "Scene continuity", "camera": "Visual quality",
    "visual": "Visual quality", "objects": "Physical positioning", "semantic": "Semantic accuracy", "ending": "Scene continuity",
}
SCORES = ["Visual quality", "Character consistency", "Physical positioning", "Animation quality", "Audio quality",
          "Lip synchronization", "Subtitle accuracy", "Scene continuity", "Semantic accuracy"]

DEFAULT_CONFIG = {
    "checks": {"frames": True, "transitions": True, "audio": True, "speech": True, "voices": True, "subtitles": True,
               "ocr": True, "grounding": True, "lipsync": True, "camera": True, "animation": True,
               "vlm_assets": True, "vlm_scenes": True},
    "pass_score": 85,            # every category score must reach this
    "max_fix_rounds": 3,
    "vlm_model": "qwen/qwen3-vl-30b",
    "frame_scale": [320, 180],   # stage-1 frame analysis resolution
    "lipsync_fps": 15,
    "transition_window": 0.8,    # seconds either side of each scene boundary, inspected at full frame rate
    "auto_fix": {"reposition": True, "regen_background": True, "regen_hero": True, "regen_talk": True, "fix_pose": True,
                 "retake_line": True, "retime_subtitles": True, "transition": True, "music_level": True},
}


def load_config(proj=None):
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    for p in [os.path.join(ROOT, "qc_config.json")] + ([os.path.join(proj, "qc_config.json")] if proj else []):
        if os.path.exists(p):
            user = json.load(open(p))
            for k, v in user.items():
                if isinstance(v, dict) and isinstance(cfg.get(k), dict): cfg[k].update(v)
                else: cfg[k] = v
    return cfg


@dataclass
class Finding:
    category: str                 # key of CATEGORIES
    severity: str                 # CRITICAL | HIGH | MEDIUM | LOW
    description: str
    start: float | None = None    # seconds in the final video
    end: float | None = None
    scene: str | None = None
    confidence: float = 0.9
    fix: str | None = None        # auto-fix action key (see qc.fix) or None = manual
    fix_args: dict = field(default_factory=dict)
    recommendation: str = ""
    source: str = "stage1"        # stage1 | stage2 (VLM)
    status: str = "open"          # open | fixed | manual

    @property
    def frame(self):
        return None if self.start is None else int(round(self.start * FPS))

    def key(self):
        return f"{self.category}|{self.scene}|{self.description[:80]}"

    def to_dict(self):
        d = asdict(self); d["frame"] = self.frame; d["auto_fixable"] = bool(self.fix); return d


def scores(findings):
    s = {k: 100.0 for k in SCORES}
    for f in findings:
        if f.status == "fixed": continue
        b = CATEGORIES.get(f.category, "Visual quality")
        s[b] = max(0.0, s[b] - WEIGHT[f.severity] * f.confidence)
    s = {k: round(v, 1) for k, v in s.items()}
    s["Overall"] = round(sum(s[k] for k in SCORES) / len(SCORES), 1)
    return s


def passed(findings, cfg):
    sc = scores(findings)
    crit = [f for f in findings if f.status != "fixed" and f.severity == "CRITICAL"]
    return not crit and all(sc[k] >= cfg["pass_score"] for k in SCORES), sc


# ---------------------------------------------------------------- cache (per scene render hash / per asset hash)
class Cache:
    def __init__(self, proj):
        self.path = os.path.join(proj, "work", "qc_cache.json")
        self.d = json.load(open(self.path)) if os.path.exists(self.path) else {}

    def get(self, ns, key):
        return self.d.get(ns, {}).get(key)

    def put(self, ns, key, val):
        self.d.setdefault(ns, {})[key] = val
        json.dump(self.d, open(self.path, "w"))


def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


def log(proj, msg):
    line = f"[{time.strftime('%H:%M:%S')}] QC {msg}"
    print(line, flush=True)
    with open(os.path.join(proj, "production.log"), "a") as f: f.write(line + "\n")


def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


# ---------------------------------------------------------------- project timeline
XF = {"slide": 0.45, "zoom": 0.5, "wipe": 0.45, "whip": 0.3, "fade": 0.5, "cut": 0.04}


class Project:
    def __init__(self, proj):
        self.dir = proj
        self.name = os.path.basename(proj.rstrip("/"))
        self.video = os.path.join(proj, f"{self.name}.mp4")
        self.script = json.load(open(os.path.join(proj, "script.json")))
        ap = os.path.join(proj, "work", "all_props.json")
        if os.path.exists(ap): self.props = {p["id"]: p for p in json.load(open(ap))}
        else: self.props = {j["props"]["id"]: j["props"] for j in json.load(open(os.path.join(proj, "work", "render_jobs.json")))["jobs"]}
        self.scenes = [s for s in self.script["scenes"] if s["id"] in self.props]
        missing = [s["id"] for s in self.script["scenes"] if s["id"] not in self.props]
        if missing: raise RuntimeError(f"QC: props missing for scenes {missing} — run the render stage first")
        self.render = {s["id"]: os.path.join(proj, "renders", f"{s['id']}.mp4") for s in self.scenes}
        self.start, t, prev = {}, 0.0, None
        self.dur = {}
        for s in self.scenes:
            d = probe_dur(self.render[s["id"]]); self.dur[s["id"]] = d
            self.start[s["id"]] = 0.0 if prev is None else self.start[prev] + self.dur[prev] - XF.get(s.get("transition", "cut"), 0.04)
            prev = s["id"]
        self.lines = {}
        for s in self.scenes:
            p = os.path.join(proj, "audio", f"{s['id']}.lines.json")
            self.lines[s["id"]] = json.load(open(p)) if os.path.exists(p) else []

    def render_hash(self, sid):
        p = self.render[sid] + ".hash"
        return open(p).read().strip() if os.path.exists(p) else file_hash(self.render[sid])

    def scene_at(self, t):
        cur = None
        for s in self.scenes:
            if self.start[s["id"]] <= t: cur = s["id"]
        return cur


# ---------------------------------------------------------------- renderer geometry (port of Character.tsx / Scene.tsx)
SLOT = {"left": 0.27, "center": 0.5, "right": 0.73}
CHAR_H, FEET_Y, PUSH = 0.70, 0.95, 0.035


def pos_x(m):
    return m["x"] if m.get("x") is not None else SLOT[m["position"]]


def rnd(s, i):
    h = (2166136261 ^ i) & 0xFFFFFFFF
    for c in s:
        h = ((h ^ ord(c)) * 16777619) & 0xFFFFFFFF
    return (h % 10000) / 10000


def _pick(m, want):
    p = m["poses"]
    return want if want in p else "talk" if "talk" in p else "neutral" if "neutral" in p else next(iter(p))


def state_at(m, cast, lines, t):
    cur = next((l for l in lines if l["start"] <= t < l["end"] + 0.12), None)
    if cur is None:
        prev = [l for l in lines if l["end"] <= t]
        cur = prev[-1] if prev else (lines[0] if lines else None)
    speaking = bool(cur) and cur["speaker"] == m["char"] and cur["start"] <= t < cur["end"]
    is_speaker = bool(cur) and cur["speaker"] == m["char"]
    spm = next((c for c in cast if cur and c["char"] == cur["speaker"]), None)
    target = spm if spm and spm is not m else next((c for c in cast if c is not m), None)
    face_right = pos_x(target) > pos_x(m) if target else m["position"] != "right"
    if is_speaker:
        p = cur["pose"]
        conv = p in ("talk", "neutral", "side_talk") and cur.get("shot") == "two_shot" and len(cast) > 1
        pose = _pick(m, "side_talk" if conv else p)
    elif len(cast) > 1 and cur and cur["speaker"] != "narrator":
        react = {"surprised": "surprised", "angry": "worried", "excited": "happy", "sad": "worried", "confused": "thinking"}
        r = react.get(cur.get("emotion"))
        pose = _pick(m, r if r and r in m["poses"] and t - cur["start"] > 0.6 else "side_listen")
    else:
        pose = _pick(m, "neutral")
    side = pose.startswith("side_")
    return {"pose": pose, "flip": (not face_right) if side else False, "speaking": speaking, "line": cur, "is_speaker": is_speaker}


def _ease(x):  # Easing.inOut(Easing.cubic)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def cam_for(props, l):
    if not l or not props["cast"]: return (1.0, W / 2, H / 2)
    sp = next((c for c in props["cast"] if c["char"] == l["speaker"]), None)
    feet, head, push = H * FEET_Y, H * (FEET_Y - CHAR_H), 1 + PUSH
    if l.get("shot") == "closeup" and sp:
        s = 1.6; return (s, W * pos_x(sp), head + (H / 2 - 70) / (s * push))
    if l.get("shot") == "detail": return (1.2, W / 2, H * 0.4)
    if l.get("shot") == "wide": return (1.0, W / 2, H / 2)
    xs = [W * pos_x(c) for c in props["cast"]]; s = 1.06
    return (s, (min(xs) + max(xs)) / 2, feet - (H / 2 - 25) / (s * push))


def camera_at(props, t):
    lines = props["lines"]; dur_f = props["durationInFrames"]
    if not lines: s, x, y = 1.0, W / 2, H / 2
    else:
        idx = next((i for i, l in enumerate(lines) if t < l["end"] + 0.1), len(lines) - 1)
        cur, prev = lines[idx], lines[max(0, idx - 1)]
        a, b = cam_for(props, prev), cam_for(props, cur)
        d = 0.12 if cur.get("shot") == "closeup" or prev.get("shot") == "closeup" else 0.55
        k = 1.0 if idx == 0 else _ease(min(1, max(0, (t - (cur["start"] - 0.05)) / d)))
        s, x, y = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k)
    s *= 1 + PUSH * min(1, (t * FPS) / max(1, dur_f))
    x = min(max(x, W / (2 * s)), W - W / (2 * s)); y = min(max(y, H / (2 * s)), H - H / (2 * s))
    return s, x, y


def to_screen(cam, pt):
    s, cx, cy = cam
    return (W / 2 + s * (pt[0] - cx), H / 2 + s * (pt[1] - cy))


def char_place(m, cast, lines, t, fps=FPS):
    """World-space placement of a character at scene time t: pose, box, and a function mapping
    pose-image fractions (u,v) to world pixels (applies flip / breathe / sway / talk-wobble / hop exactly as the renderer)."""
    st = state_at(m, cast, lines, t)
    since = 0
    for k in range(1, 13):
        if state_at(m, cast, lines, t - k / fps)["pose"] != st["pose"]: break
        since = k
    p0 = m["poses"][st["pose"]]
    th = H * CHAR_H; w = p0["w"] * th / p0["h"]; cx = W * pos_x(m)
    seed = rnd(m["char"], 1) * 10
    breathe = 1 + math.sin(t * 2.1 + seed) * 0.006
    sway = math.sin(t * 0.7 + seed) * 0.9
    talk = math.sin(t * 8.5) * 1.4 if st["speaking"] else 0
    ph = (t + seed) % 1.6
    nod = (math.sin((ph / 0.35) * math.pi) * 0.018 if (not st["is_speaker"] and st["line"] and st["line"]["speaker"] != "narrator" and ph < 0.35) else 0)
    hop = math.sin((since / 8) * math.pi) * 5 if since < 8 else 0
    ox, oy = cx, H * FEET_Y - hop               # transform origin = bottom centre of the character box
    ang = math.radians(sway + talk); sy = breathe - nod; sx = -1 if st["flip"] else 1

    def world(u, v):
        x, y = (u - 0.5) * w * sx, (v - 1) * th * sy
        return (ox + x * math.cos(ang) - y * math.sin(ang), oy + x * math.sin(ang) + y * math.cos(ang))
    return {"state": st, "pose": st["pose"], "img": p0, "w": w, "h": th, "cx": cx, "feet_y": oy, "world": world,
            "box": (cx - w / 2, oy - th, cx + w / 2, oy)}


def proj_path(proj, rel):
    return os.path.join(proj, "public", rel)
