"""Automatic corrections. Each action changes only what the finding points at (one scene layout, one environment,
one pose, one TTS line, one transition...). The pipeline then re-renders just the affected scenes and QC re-inspects."""
import glob, json, os, shutil
import numpy as np
from PIL import Image
from .core import Finding, W, H, FEET_Y, log, pos_x, state_at, proj_path
from .stage1 import bg_analysis, silhouette
from .. import assets, config as C, imagegen

OPEN_FLOOR = [" Wide open empty floor across the whole lower half of the picture; all furniture pushed far back against the walls.",
              " Seen from standing eye level with a large clear empty floor area in the foreground and centre; no tables, chairs or desks in the front half.",
              " Furniture only along the back wall and the far left/right edges at normal room scale, eye-level camera, clear floor in front."]


def _save_script(pr):
    json.dump(pr.script, open(os.path.join(pr.dir, "script.json"), "w"), indent=1, ensure_ascii=False)


def _scene(pr, sid):
    return next(s for s in pr.script["scenes"] if s["id"] == sid)


# ---------------------------------------------------------------- grounding: move characters onto clear floor
def _char_ok(pr, cache, props, m, x):
    info, floor, masks = bg_analysis(pr, cache, props["background"])
    cast = [dict(c, x=(x if c["char"] == m["char"] else c.get("x"))) for c in props["cast"]]
    mm = next(c for c in cast if c["char"] == m["char"])
    poses = {(state_at(mm, cast, props["lines"], t)["pose"], state_at(mm, cast, props["lines"], t)["flip"])
             for t in [0.2] + [(l["start"] + l["end"]) / 2 for l in props["lines"]]}
    width = 0
    for pose, flip in poses:
        sil, feet = silhouette(pr, mm["poses"][pose], W * x, H * FEET_Y, flip)
        area = sil.sum() or 1
        cols = np.where(sil.any(0))[0]; width = max(width, (cols.max() - cols.min()) if len(cols) else 0)
        for o, om in zip(info["obstacles"], masks):
            if o["contact_y"] >= H * FEET_Y - 12 and (sil & om).sum() / area > 0.02: return False, width
        for fx, fy in feet:
            fx = min(W - 1, max(0, fx)); fy = min(H - 1, fy + 3)
            if any(om[fy, fx] for om in masks): return False, width
        if info["floor_found"] and feet:
            band = [floor[max(0, y - 6):min(H, y + 8), max(0, xx - 3):xx + 4].any() for xx, y in feet]
            if np.mean(band) < 0.4: return False, width
    return True, width


def reposition(pr, cache, f):
    sid = f.fix_args["scene"]; props = pr.props[sid]
    cast = sorted(props["cast"], key=pos_x)
    xs = np.round(np.arange(0.10, 0.905, 0.01), 3)
    ok = {m["char"]: {x: _char_ok(pr, cache, props, m, x) for x in xs} for m in cast}
    best, bestcost = None, 1e9

    def rec(i, chosen, cost):
        nonlocal best, bestcost
        if cost >= bestcost: return
        if i == len(cast): best, bestcost = dict(chosen), cost; return
        m = cast[i]
        for x in sorted(xs, key=lambda v: abs(v - pos_x(m))):
            good, wpx = ok[m["char"]][x]
            if not good: continue
            if i:
                pm = cast[i - 1]; px = chosen[pm["char"]]; pw = ok[pm["char"]][px][1]
                if (x - px) * W < (wpx + pw) / 2 + 40: continue                 # keep order and a gap between characters
            if len(cast) > 1 and i == len(cast) - 1 and (x - chosen[cast[0]["char"]]) * W > W * 0.75: continue   # still a conversation
            chosen[m["char"]] = x; rec(i + 1, chosen, cost + abs(x - pos_x(m))); del chosen[m["char"]]
    rec(0, {}, 0.0)
    if best is None:
        return regen_background(pr, cache, Finding("physical", "HIGH", "no clear floor for the cast", fix_args={"env": f.fix_args.get("env")}))
    s = _scene(pr, sid); s["layout"] = {k: float(v) for k, v in best.items()}; _save_script(pr)
    return f"{sid}: moved {', '.join(f'{k}->{v:.2f}' for k, v in best.items())}"


def repaint_text(pr, cache, f):
    """Garbled text in a background: repaint only those regions (seconds) instead of regenerating the whole background."""
    from .. import repaint, assets as A
    env = f.fix_args.get("env"); e = next((x for x in pr.script["environments"] if x["id"] == env), None)
    if not e or e.get("_repaints", 0) >= 2: return regen_background(pr, cache, f)
    src = A.build_background(e); base, ext = os.path.splitext(src)
    out = f"{base.split('_rp')[0]}_rp{e.get('_repaints', 0) + 1}{ext}"
    from .. import comfy; comfy.start()
    repaint.repaint(src, f.fix_args["boxes"], out)
    e["bg_file"] = out; e["_repaints"] = e.get("_repaints", 0) + 1; _save_script(pr)
    return f"background '{env}': {len(f.fix_args['boxes'])} text region(s) repainted"


def regen_background(pr, cache, f):
    env = f.fix_args.get("env")
    e = next((x for x in pr.script["environments"] if x["id"] == env), None)
    if not e: return None
    n = int(e.get("_qc_bg_attempt", 0))
    if n >= len(OPEN_FLOOR): return None
    base = e.get("_qc_base_prompt", e["prompt"]); e["_qc_base_prompt"] = base
    e["prompt"] = base + OPEN_FLOOR[n]; e["_qc_bg_attempt"] = n + 1
    for s in pr.script["scenes"]:
        if s.get("environment") == env: s.pop("layout", None)
    _save_script(pr)
    return f"background '{env}' regenerated with open floor (attempt {n + 1})"


# ---------------------------------------------------------------- characters
def _rig(char):
    rp = os.path.join(C.CHAR_LIB, assets.slug(char), "rig.json"); return rp, json.load(open(rp))


def regen_talk(pr, cache, f):
    rp, rig = _rig(f.fix_args["char"]); pz = rig["poses"].get(f.fix_args["pose"])
    if not pz: return None
    n = int(pz.get("_qc_talk_attempt", 0))
    if n >= 2: return None
    for v in (pz.pop("talk", None) or {}).values():
        p = os.path.join(C.LIBRARY, v)
        if os.path.exists(p): os.remove(p)
    pz["_qc_talk_attempt"] = n + 1
    json.dump(rig, open(rp, "w"), indent=1)
    return f"mouth frames for {f.fix_args['char']}/{f.fix_args['pose']} will be regenerated"


def fix_pose(pr, cache, f):
    char, pose = f.fix_args["char"], f.fix_args["pose"]
    rp, rig = _rig(char); pz = rig["poses"].get(pose)
    if not pz or int(pz.get("_qc_fix_attempt", 0)) >= 2: return None
    d = os.path.join(C.CHAR_LIB, assets.slug(char)); src = os.path.join(C.LIBRARY, pz["img"])
    os.makedirs(os.path.join(d, "_orig"), exist_ok=True)
    keep = os.path.join(d, "_orig", os.path.basename(src))
    if not os.path.exists(keep): shutil.copy(src, keep)
    refs = [src]
    prompt = ("Keep this cartoon character EXACTLY the same — same pose, framing, face, hair, outfit, colours and flat art style, "
              f"mouth closed — and fix only this defect: {f.fix_args['problem']}. Transparent background, no text.")
    if f.fix_args.get("match_reference") and "neutral" in rig["poses"]:
        refs.append(os.path.join(C.LIBRARY, rig["poses"]["neutral"]["img"]))
        prompt = ("Redraw the character in the first image in exactly the same pose and framing, but make the face, hair, outfit, "
                  "colours and accessories match the character in the second image exactly. Mouth closed. Transparent background, no text.")
    tmp = os.path.join(d, "_tmp")
    p = imagegen.edit(prompt, refs, tmp, f"{pose}_qcfix", seed=101 + int(pz.get("_qc_fix_attempt", 0)))
    p = assets._ensure_alpha(p, tmp, f"{pose}_qcfix")
    img = assets._crop(Image.open(p).convert("RGBA")); img.save(src)
    det = assets._detector()
    m = assets._boxes(det, img, "mouth.", 0.22); eyes = [e for _, e in assets._boxes(det, img, "eye.", 0.22)][:2] or pz["eyes"]
    pz.update(w=img.width, h=img.height, eyes=eyes, mouth=m[0][1] if m else pz["mouth"], mouth_est=not m)
    pz["_qc_fix_attempt"] = int(pz.get("_qc_fix_attempt", 0)) + 1
    pz.pop("talk", None)
    json.dump(rig, open(rp, "w"), indent=1)
    assets.fix_anchors()
    for k in [k for k in cache.d.get("vlm_pose", {})]: pass
    return f"{char}/{pose} redrawn to fix: {f.fix_args['problem'][:80]}"


# ---------------------------------------------------------------- shots, audio, subtitles, transitions
def regen_hero(pr, cache, f):
    sid = f.fix_args["scene"]; s = _scene(pr, sid)
    n = int(s.get("_qc_hero_attempt", 0))
    if n >= 2: return None
    for p in [os.path.join(pr.dir, "hero", f"{sid}.mp4")] + glob.glob(os.path.join(pr.dir, "work", f"hero_{sid}_*")):
        if os.path.exists(p): os.remove(p)
    s["_qc_hero_attempt"] = n + 1; _save_script(pr)
    return f"{sid}: hero shot regenerated (new seed)"


def retake_line(pr, cache, f):
    sid, key = f.fix_args["scene"], f.fix_args["key"]; s = _scene(pr, sid)
    tries = s.setdefault("_qc_retakes", {})
    if tries.get(key, 0) >= 2: return None
    tries[key] = tries.get(key, 0) + 1; _save_script(pr)
    for p in glob.glob(os.path.join(pr.dir, "audio", "lines", key + ".*")) + \
             [os.path.join(pr.dir, "audio", f"{sid}{x}") for x in (".wav", ".lines.json", ".words.json")]:
        if os.path.exists(p): os.remove(p)
    return f"{sid}: line {key} re-voiced"


def retime_subtitles(pr, cache, f):
    sid = f.fix_args["scene"]
    for ln in pr.lines.get(sid, []):
        for p in glob.glob(os.path.join(pr.dir, "audio", "lines", ln.get("key", "x") + ".words*.json")): os.remove(p)
    p = os.path.join(pr.dir, "audio", f"{sid}.words.json")
    if os.path.exists(p): os.remove(p)
    return f"{sid}: subtitle timing rebuilt from speech"


def transition(pr, cache, f):
    s = _scene(pr, f.fix_args["scene"])
    if s.get("transition") == "fade": return None
    s["transition"] = "fade"; _save_script(pr)
    return f"{s['id']}: transition changed to fade"


def music_level(pr, cache, f):
    mix = pr.script.setdefault("mix", {}); cur = mix.get("music_db", -15)
    if cur <= -24: return None
    mix["music_db"] = cur - 3; _save_script(pr)
    return f"music lowered to {mix['music_db']} dB"


def rerender(pr, cache, f):
    p = pr.render[f.fix_args["scene"]] + ".hash"
    if os.path.exists(p): os.remove(p)
    return f"{f.fix_args['scene']}: re-rendered"


def add_outro(pr, cache, f):
    from .. import ending
    if pr.script.get("_qc_outro_tries", 0) >= 2: return None
    pr.script["_qc_outro_tries"] = pr.script.get("_qc_outro_tries", 0) + 1
    changed = ending.ensure_outro(pr.script, pr.script.get("title", ""))
    last = pr.script["scenes"][-1]
    if not changed and last.get(ending.OUTRO_TAG) and not last.get("_tail"):
        last["_tail"] = 1.2; changed = True              # outro exists but ends abruptly -> hold the last card longer
    if not changed: return None
    _save_script(pr)
    return f"ending: outro scene {last['id']} — \"{last['lines'][-1]['text'][:80]}\""


def revoice(pr, cache, f):
    from .. import voice as V
    spk = f.fix_args["speaker"]; prof = V.voice_profiles(pr.script).get(spk)
    if not prof: return None
    pj = os.path.join(C.VOICE_LIB, prof["name"], "profile.json")
    meta = json.load(open(pj)) if os.path.exists(pj) else {}
    if meta.get("redesigns", 0) >= 2: return None
    meta["force_redesign"] = True; meta["redesigns"] = meta.get("redesigns", 0) + 1
    os.makedirs(os.path.dirname(pj), exist_ok=True); json.dump(meta, open(pj, "w"), indent=1)
    return f"{spk}: voice will be redesigned as {V.gender(prof['design'])} and all lines re-voiced"


def remaster(pr, cache, f):
    return "master re-run"


ACTIONS = {"reposition": reposition, "regen_background": regen_background, "regen_talk": regen_talk, "fix_pose": fix_pose,
           "regen_hero": regen_hero, "retake_line": retake_line, "retime_subtitles": retime_subtitles, "transition": transition,
           "music_level": music_level, "rerender": rerender, "remaster": remaster,
           "add_outro": add_outro, "revoice": revoice, "repaint_text": repaint_text}
CFG_KEY = {"reposition": "reposition", "regen_background": "regen_background", "regen_talk": "regen_talk", "fix_pose": "fix_pose",
           "regen_hero": "regen_hero", "retake_line": "retake_line", "retime_subtitles": "retime_subtitles", "transition": "transition",
           "music_level": "music_level"}


def apply(pr, cache, findings, cfg):
    """Apply one fix per distinct target. Returns list of (finding, result-text or None)."""
    done, out = set(), []
    order = ["add_outro", "revoice", "repaint_text", "fix_pose", "regen_talk", "regen_background", "reposition", "regen_hero", "retake_line", "retime_subtitles",
             "transition", "music_level", "rerender", "remaster"]
    for f in sorted([f for f in findings if f.fix and f.status == "open"], key=lambda f: order.index(f.fix) if f.fix in order else 99):
        if not cfg["auto_fix"].get(CFG_KEY.get(f.fix, f.fix), True): continue
        tgt = (f.fix, json.dumps({k: v for k, v in f.fix_args.items() if k != "problem"}, sort_keys=True))
        if tgt in done: out.append((f, "same fix as above")); continue
        if f.fix == "reposition" and ("regen_background", json.dumps({"env": f.fix_args.get("env")}, sort_keys=True)) in done:
            out.append((f, "background regenerated instead")); continue
        done.add(tgt)
        try: r = ACTIONS[f.fix](pr, cache, f)
        except Exception as e: r = None; log(pr.dir, f"fix {f.fix} failed: {e}")
        out.append((f, r))
        if f.fix == "reposition" and r and r.startswith("background"): done.add(("regen_background", json.dumps({"env": f.fix_args.get("env")}, sort_keys=True)))
    return out
