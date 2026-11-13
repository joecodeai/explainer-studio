"""Progress tracking for the current video and the whole batch (no model needed).
The pipeline calls stage() at every stage; durations are learned (moving average) so time-remaining gets better each run.
View with:  ./progress   (two live bars + time remaining)"""
import json, os, time
from . import config as C

STATE = os.path.join(C.ROOT, "logs", "progress.json")
TIMES = os.path.join(C.ROOT, "logs", "stage_times.json")
STAGES = ["script", "voice", "assets", "hero", "talk", "sound", "render", "master", "qc", "reel", "done"]
DEFAULT = {"script": 900, "voice": 90, "assets": 240, "hero": 200, "talk": 1500, "sound": 60, "render": 330, "master": 45, "qc": 420, "reel": 240}


def _load(p, d):
    try: return json.load(open(p))
    except Exception: return d


def _save(p, d):
    tmp = p + ".tmp"; json.dump(d, open(tmp, "w"), indent=1); os.replace(tmp, p)


def expected():
    t = dict(DEFAULT); t.update(_load(TIMES, {})); return t


def batch_start(projects, skip_script=True):
    _save(STATE, {"batch": {"items": [os.path.basename(p.rstrip("/")) for p in projects], "done": [], "started": time.time(),
                            "skip_script": skip_script}, "current": None})


def stage(proj, name):
    s = _load(STATE, {"batch": None, "current": None}); now = time.time()
    name_p = os.path.basename(proj.rstrip("/"))
    cur = s.get("current")
    if cur and cur.get("proj") == name_p and cur.get("stage") and cur["stage"] != name:
        dur = now - cur["stage_started"]
        if dur > 2 and not cur.get("cached"):
            t = _load(TIMES, {}); old = t.get(cur["stage"], DEFAULT.get(cur["stage"], dur))
            t[cur["stage"]] = round(0.6 * old + 0.4 * dur, 1); _save(TIMES, t)
        cur.setdefault("finished", []).append(cur["stage"])
    if not cur or cur.get("proj") != name_p:
        cur = {"proj": name_p, "video_started": now, "finished": []}
    cur.update(stage=name, stage_started=now)
    s["current"] = cur
    if name == "done" and s.get("batch") and name_p not in s["batch"]["done"]:
        s["batch"]["done"].append(name_p)
    _save(STATE, s)


def snapshot():
    s = _load(STATE, {}); exp = expected(); now = time.time()
    b, cur = s.get("batch"), s.get("current")
    stages = [x for x in STAGES[:-1] if not (b and b.get("skip_script") and x == "script")]
    per_video = sum(exp[x] for x in stages)
    v_frac, v_left = 0.0, per_video
    if cur and cur.get("stage") != "done":
        doneT = sum(exp[x] for x in stages if x in cur.get("finished", []))
        st = cur.get("stage"); el = now - cur.get("stage_started", now)
        inT = min(el, exp.get(st, 60) * 0.95) if st in exp else 0
        rest = sum(exp[x] for x in stages if x not in cur.get("finished", []) and x != st)
        v_frac = (doneT + inT) / max(1, doneT + exp.get(st, 0) + rest)
        v_left = max(exp.get(st, 0) - el, 0.1 * exp.get(st, 0)) + rest
    elif cur and cur.get("stage") == "done":
        v_frac, v_left = 1.0, 0
    n = len(b["items"]) if b else 1; d = len(b["done"]) if b else 0
    in_prog = 1 if (cur and cur.get("stage") != "done" and b and cur["proj"] in b["items"] and cur["proj"] not in b["done"]) else 0
    all_frac = (d + (v_frac if in_prog else 0)) / max(1, n)
    all_left = (v_left if in_prog else 0) + max(0, n - d - in_prog) * per_video
    return {"video": cur.get("proj") if cur else None, "stage": cur.get("stage") if cur else None, "video_frac": v_frac, "video_left": v_left,
            "all_frac": all_frac, "all_left": all_left, "done": d, "total": n}
