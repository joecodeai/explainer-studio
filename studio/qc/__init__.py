"""Two-stage video quality control with automatic correction.

  Stage 1  fast technical inspection of the whole video (frames, transitions at full frame rate, audio, ASR vs script,
           subtitle sync, voices, OCR of every text element, ground-plane / furniture segmentation, measured lip-sync,
           camera framing, animation)
  Stage 2  vision-language review (Qwen3-VL) of every pose / background / hero shot used, one frame per scene for
           meaning and physical plausibility, and escalations from stage 1
  Fix      targeted corrections -> re-render only what changed -> re-inspect (cached), up to max_fix_rounds
  Report   review/QC_REPORT.md + qc_report.json: every finding with category, time range, frame, severity,
           confidence, recommendation, auto-fixable, status; per-category scores; PASS only with no open CRITICAL
           and every score >= pass_score.

  python -m studio.qc <project_dir> [--no-fix]
"""
import copy, json, os, time
from . import core, models as M
from .core import Finding, Cache, Project, load_config, log, scores, passed


GLOBAL_CHECKS = {"audio", "voices", "ending", "vlm_assets"}     # always run on the whole video (cheap / cross-scene)


def scoped(pr, only):
    """A view of the project limited to the scenes in `only` (plus the scene before each, so boundaries are checked).
    Timeline (pr.start / pr.dur), script and video stay complete."""
    if only is None: return pr
    ids = [s["id"] for s in pr.scenes]; keep = set()
    for i, sid in enumerate(ids):
        if sid in only: keep.add(sid); keep.add(ids[i - 1]) if i else None
    v = copy.copy(pr)
    v.scenes = [s for s in pr.scenes if s["id"] in keep]
    v.props = {k: p for k, p in pr.props.items() if k in keep}
    return v


def inspect(proj, cfg, round_no=0, only=None):
    """only = set of scene ids to re-inspect (fast re-check after a fix); None = whole video."""
    from . import stage1 as S1, stage2 as S2, animcheck as A
    pr = Project(proj); cache = Cache(proj); ch = cfg["checks"]; F = []
    sp = scoped(pr, only)
    t0 = time.time()
    if only is not None: log(proj, f"scoped re-inspection: {sorted({s['id'] for s in sp.scenes})} (+ whole-video audio/voice/ending checks)")
    steps = [("frames", S1.check_frames), ("transitions", S1.check_transitions), ("audio", S1.check_audio),
             ("speech", S1.check_speech), ("voices", S1.check_voices), ("ocr", S1.check_ocr), ("lipsync", S1.check_lipsync),
             ("camera", S1.check_camera), ("animation", S1.check_animation), ("talkshots", A.check_talkshots), ("ending", S1.check_ending)]
    for name, fn in steps:
        if not ch.get(name, True) and not (name == "speech" and ch.get("subtitles")): continue
        log(proj, f"stage 1: {name}")
        try:
            got = fn(pr if name in GLOBAL_CHECKS else sp, cache, cfg)
            for f in got: f.check = name
            F += got
        except Exception as e:
            log(proj, f"check {name} crashed: {e}"); F.append(Finding("visual", "LOW", f"QC check '{name}' could not run: {e}", confidence=1))
    unknown = []
    if ch.get("grounding", True):
        log(proj, "stage 1: grounding (floor + furniture segmentation)")
        try:
            g, unknown = S1.check_grounding(sp, cache, cfg)
            for f in g: f.check = "grounding"
            F += g
        except Exception as e: log(proj, f"grounding crashed: {e}"); F.append(Finding("physical", "LOW", f"grounding check could not run: {e}"))
    M.free()
    try:
        from .. import comfy; comfy.free()
    except Exception: pass
    if ch.get("vlm_assets", True) or ch.get("vlm_scenes", True):
        log(proj, "stage 2: vision-language review")
        try:
            if ch.get("vlm_assets", True):
                got = S2.check_assets(pr, cache, cfg)
                for f in got: f.check = "vlm_assets"
                F += got
            if ch.get("vlm_scenes", True):
                got = S2.check_scenes(sp, cache, cfg, unknown)
                for f in got: f.check = "vlm_scenes"
                F += got
        except Exception as e:
            log(proj, f"stage 2 crashed: {e}"); F.append(Finding("visual", "LOW", f"VLM review could not run: {e}"))
        M.free()
    log(proj, f"inspection round {round_no}: {len(F)} findings in {time.time() - t0:.0f}s")
    return pr, cache, F


def scene_state(proj):
    """Fingerprint per scene (render hash + its audio) — what changed after a fix decides what gets re-inspected."""
    out = {}
    try: ids = [p["id"] for p in json.load(open(os.path.join(proj, "work", "all_props.json")))]
    except Exception: return out
    for sid in ids:
        parts = []
        for f in (os.path.join(proj, "renders", f"{sid}.mp4.hash"), os.path.join(proj, "audio", f"{sid}.lines.json")):
            parts.append(open(f).read() if os.path.exists(f) else "")
        out[sid] = hash(tuple(parts))
    return out


def run(proj, fix=True, rebuild=None):
    """rebuild(proj): re-run the production stages after fixes (pipeline.make_video(..., qc=False))."""
    cfg = load_config(proj); history = []
    rounds = cfg["max_fix_rounds"] if fix else 0
    prev_keys = {}; only = None; prev_F = []
    for r in range(rounds + 1):
        pr, cache, F = inspect(proj, cfg, r, only=only)
        if only is not None:          # carry over findings of scenes that were not touched by the fix
            fresh = {f.key() for f in F}
            F += [f for f in prev_F if getattr(f, "check", None) not in GLOBAL_CHECKS and f.scene not in only
                  and f.key() not in fresh and f.status == "open"]
        prev_F = F
        for k, f0 in prev_keys.items():          # findings that disappeared after a fix -> verified fixed
            if k not in {f.key() for f in F}: history.append({"round": r, "finding": f0.to_dict(), "result": "fixed (verified by re-inspection)"})
        ok, sc = passed(F, cfg)
        _report(pr, F, sc, ok, history, cfg)
        if ok or r == rounds: break
        fixable = [f for f in F if f.fix]
        if not fixable: break
        from .. import llm
        llm.unload()
        log(proj, f"auto-fix round {r + 1}: {len(fixable)} fixable findings")
        applied = __import__("studio.qc.fix", fromlist=["apply"]).apply(pr, cache, fixable, cfg)
        acted = [(f, res) for f, res in applied if res]
        for f, res in applied:
            history.append({"round": r + 1, "finding": f.to_dict(), "result": res or "could not auto-fix (needs manual review)"})
        if not acted: break
        prev_keys = {f.key(): f for f, res in acted}
        before = scene_state(proj)
        if rebuild: rebuild(proj)
        after = scene_state(proj)
        only = {k for k in after if after[k] != before.get(k)}
        log(proj, f"fix touched scenes: {sorted(only) or 'none'}")
    for f in F:
        if f.status == "open" and (not f.fix or any(h["finding"]["description"] == f.description and h["round"] > 0 for h in history)):
            f.status = "manual" if f.severity in ("CRITICAL", "HIGH") else f.status
    ok, sc = passed(F, cfg)
    _report(pr, F, sc, ok, history, cfg)
    return ok, sc, F


def _ts(t):
    return "" if t is None else f"{int(t // 60)}:{t % 60:05.2f}"


def _report(pr, F, sc, ok, history, cfg):
    out = os.path.join(pr.dir, "review"); os.makedirs(out, exist_ok=True)
    order = {s: i for i, s in enumerate(core.SEVERITIES)}
    F = sorted(F, key=lambda f: (order[f.severity], f.start if f.start is not None else -1))
    json.dump({"passed": ok, "scores": sc, "pass_score": cfg["pass_score"], "findings": [f.to_dict() for f in F], "fix_history": history},
              open(os.path.join(out, "qc_report.json"), "w"), indent=1)
    cnt = {s: sum(1 for f in F if f.severity == s and f.status != "fixed") for s in core.SEVERITIES}
    md = [f"# QC report — {pr.name}", "", f"**Result: {'PASS' if ok else 'FAIL'}** (every score ≥ {cfg['pass_score']} and no open CRITICAL)", "",
          "| Score | Value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sc.items()] + ["",
          f"Open findings: {cnt['CRITICAL']} critical · {cnt['HIGH']} high · {cnt['MEDIUM']} medium · {cnt['LOW']} low", "",
          "| Sev | Category | Time | Frame | Scene | Conf | Description | Recommended correction | Auto-fix | Status |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for f in F:
        rng = _ts(f.start) + (f"–{_ts(f.end)}" if f.end else "")
        md.append(f"| {f.severity} | {f.category} | {rng} | {f.frame if f.frame is not None else ''} | {f.scene or ''} | {f.confidence:.2f} | "
                  f"{f.description.replace('|', '/')} | {(f.recommendation or '').replace('|', '/')} | {f.fix or 'no'} | {f.status} |")
    if history:
        md += ["", "## Corrections applied", "", "| Round | Finding | Result |", "|---|---|---|"]
        md += [f"| {h['round']} | {h['finding']['description'][:110].replace('|', '/')} | {str(h['result']).replace('|', '/')} |" for h in history]
    open(os.path.join(out, "QC_REPORT.md"), "w").write("\n".join(md) + "\n")
    log(pr.dir, f"report: {'PASS' if ok else 'FAIL'} overall {sc['Overall']} — {cnt}")


def recheck(proj, only):
    """Fast re-inspection after a manual / feedback fix: inspect only the touched scenes (+ whole-video audio/voice/ending),
    keep the previous report's findings for every other scene, rewrite the report."""
    cfg = load_config(proj)
    prev = []
    rp = os.path.join(proj, "review", "qc_report.json")
    if os.path.exists(rp):
        old = json.load(open(rp))
        for d in old.get("findings", []):
            d = {k: v for k, v in d.items() if k in Finding.__dataclass_fields__}
            f = Finding(**d); f.check = None
            if f.scene not in only and f.category not in ("ending", "voice") and f.status != "fixed": prev.append(f)
        history = old.get("fix_history", [])
    else:
        history = []
    pr, cache, F = inspect(proj, cfg, 0, only=set(only))
    fresh = {f.key() for f in F}
    F += [f for f in prev if f.key() not in fresh and not (f.category == "audio" and f.scene is None)]
    ok, sc = passed(F, cfg)
    _report(pr, F, sc, ok, history, cfg)
    return ok, sc, F
