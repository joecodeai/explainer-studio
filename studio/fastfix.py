"""Fast fixes from plain-language notes.

  ./fix <project>            apply the notes in <project>/FEEDBACK.txt (one note per line, e.g.
                              "s12 farmer is floating", "0:47 subtitles late", "ending too abrupt", "lawmaker sounds female",
                              "s05 change 'Labor' to 'Labour'", "s14 make the background less busy")
  ./fix <project> --qc       also apply every auto-fixable finding from the last QC report

The local LLM (no Claude tokens) turns each note into one or more concrete fix actions; the pipeline re-builds only
what changed (cached renders + segmented master), re-inspects only the touched scenes, and writes
review/fix_sheet.png (before | after of every touched scene). Handled notes are marked [done] in FEEDBACK.txt."""
import json, os, re, shutil, subprocess, sys, time
from . import config as C, llm, pipeline as PL
from .qc import fix as FX, recheck, scene_state
from .qc.core import Finding, Project, Cache, load_config, log

MENU = {
    "reposition": "move a character sideways: scene, char, x (0.1 left … 0.9 right) — floating feet, overlapping furniture/characters, off-screen",
    "auto_reposition": "let QC find a clear floor spot for every character in a scene: scene",
    "regen_background": "new background image for an environment: env, problem",
    "repaint_text": "remove garbled/wrong text painted in an environment's background (fast local repaint): env",
    "fix_pose": "redraw one character pose (bad hands, anatomy, wrong look): char, pose, problem",
    "regen_talk": "redo the talking mouth frames of a character pose: char, pose",
    "regen_hero": "regenerate an AI hero video shot: scene",
    "edit_line": "change the words of a spoken line (typo, wrong name, pronunciation): scene, line (0-based), text",
    "retake_line": "re-voice one line with the same words (glitch, odd tone): scene, line",
    "set_pose": "change the pose a speaker uses on a line: scene, line, pose",
    "set_shot": "change the camera shot of a line (wide, two_shot, closeup, detail): scene, line, shot",
    "beat_text": "change an on-screen beat/label text: scene, beat (0-based), text",
    "retime_subtitles": "subtitles out of sync in a scene: scene",
    "transition": "make the transition into a scene a soft fade: scene",
    "music_level": "music too loud / speech hard to hear: (no args)",
    "revoice": "a character's voice is wrong (gender, age, sounds like another character): speaker",
    "add_outro": "ending missing / abrupt / no sign-off: (no args)",
}


def _context(sc, props, pr):
    rows = []
    for s in sc["scenes"]:
        t = pr.start.get(s["id"])
        rows.append({"scene": s["id"], "kind": s["kind"], "time": f"{int(t // 60)}:{t % 60:04.1f}" if t is not None else "?",
                     "env": s.get("environment"), "cast": [c if isinstance(c, str) else c.get("id", c.get("char")) for c in s.get("cast", [])],
                     "lines": [f"{i}. {l['speaker']} ({l.get('pose')}): {l['text'][:70]}" for i, l in enumerate(s.get("lines", []))],
                     "beats": [b["text"] for b in s.get("beats", [])]})
    return {"characters": [{"id": c["id"], "voice": c.get("voice", "")[:60]} for c in sc["characters"]],
            "environments": [e["id"] for e in sc["environments"]], "poses": C.POSES, "scenes": rows}


def plan(note, ctx):
    r = llm.chat([{"role": "user", "content":
                   "You turn a video editor's note into concrete fix actions for an animated explainer.\n"
                   f"VIDEO: {json.dumps(ctx, ensure_ascii=False)}\n\nACTIONS (name: meaning: args):\n" +
                   "\n".join(f"- {k}: {v}" for k, v in MENU.items()) +
                   f"\n\nNOTE: {note}\n\nPick the smallest set of actions that fixes exactly what the note says (usually one). "
                   "Times like 1:23 refer to the 'time' column (a scene starts there). Use only ids that exist above."}],
                 temperature=0.1, max_tokens=4000,
                 schema={"type": "object", "required": ["actions"], "properties": {"actions": {"type": "array", "items": {
                     "type": "object", "required": ["action"], "properties": {
                         "action": {"type": "string", "enum": list(MENU)}, "scene": {"type": "string"}, "char": {"type": "string"},
                         "speaker": {"type": "string"}, "env": {"type": "string"}, "pose": {"type": "string"}, "shot": {"type": "string"},
                         "line": {"type": "integer"}, "beat": {"type": "integer"}, "x": {"type": "number"}, "text": {"type": "string"},
                         "problem": {"type": "string"}}}}}})
    return r.get("actions", [])


def apply_action(pr, cache, a, note):
    """Returns a short result string, or None if nothing could be done."""
    sc = pr.script; act = a["action"]; sid = a.get("scene")
    s = next((x for x in sc["scenes"] if x["id"] == sid), None)
    save = lambda: FX._save_script(pr)
    if act == "reposition" and s and a.get("char") is not None and a.get("x") is not None:
        s.setdefault("layout", {})[a["char"]] = float(min(0.9, max(0.1, a["x"]))); save(); return f"{sid}: {a['char']} -> x={a['x']:.2f}"
    if act == "edit_line" and s and a.get("text") and 0 <= a.get("line", -1) < len(s["lines"]):
        s["lines"][a["line"]]["text"] = a["text"]; save(); return f"{sid} line {a['line']}: \"{a['text'][:60]}\""
    if act == "set_pose" and s and a.get("pose") in C.POSES and 0 <= a.get("line", -1) < len(s["lines"]):
        s["lines"][a["line"]]["pose"] = a["pose"]; save(); return f"{sid} line {a['line']}: pose {a['pose']}"
    if act == "set_shot" and s and a.get("shot") and 0 <= a.get("line", -1) < len(s["lines"]):
        s["lines"][a["line"]]["shot"] = a["shot"]; save(); return f"{sid} line {a['line']}: shot {a['shot']}"
    if act == "beat_text" and s and a.get("text") and 0 <= a.get("beat", -1) < len(s.get("beats", [])):
        s["beats"][a["beat"]]["text"] = a["text"]; save(); return f"{sid} beat {a['beat']}: {a['text']}"
    if act == "repaint_text" and a.get("env"):
        from . import repaint, assets
        e = next((x for x in sc["environments"] if x["id"] == a["env"]), None)
        if not e: return None
        boxes = [bb for _, bb in repaint.garbled_text_boxes(assets.build_background(e), min_h=14)]
        from .qc import models as M; M.free()
        if not boxes: return f"{a['env']}: no text found to repaint"
        return FX.repaint_text(pr, cache, Finding("continuity", "MEDIUM", note, fix_args={"env": a["env"], "boxes": boxes}))
    args = {k: v for k, v in a.items() if k not in ("action",) and v not in (None, "")}
    if act == "auto_reposition": act = "reposition"
    if act == "retake_line" and s:
        ln = s["lines"][min(a.get("line", 0), len(s["lines"]) - 1)]
        from .voice import _line_key
        args = {"scene": sid, "key": _line_key(ln["speaker"], ln["text"])}
    if act == "regen_background": args.setdefault("problem", note)
    if act == "fix_pose": args.setdefault("problem", note)
    if act == "revoice" and "speaker" not in args and "char" in args: args["speaker"] = args["char"]
    fn = FX.ACTIONS.get(act)
    return fn(pr, cache, Finding("visual", "HIGH", note, scene=sid, fix=act, fix_args=args)) if fn else None


def _sheet(proj, before_dir, touched, pr):
    """review/fix_sheet.png: before | after middle frame of every touched scene."""
    from PIL import Image, ImageDraw
    rows = []
    for sid in sorted(touched):
        t = pr.start[sid] + pr.dur[sid] / 2; pair = []
        for tag, vid in (("before", os.path.join(before_dir, "prev.mp4")), ("after", pr.video)):
            out = os.path.join(before_dir, f"{sid}_{tag}.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", vid, "-frames:v", "1", "-vf", "scale=640:-1", out])
            if os.path.exists(out):
                im = Image.open(out); ImageDraw.Draw(im).text((8, 6), f"{sid} {tag}", fill=(255, 40, 40)); pair.append(im)
        if len(pair) == 2:
            r = Image.new("RGB", (1290, pair[0].height), "white"); r.paste(pair[0], (0, 0)); r.paste(pair[1], (650, 0)); rows.append(r)
    if rows:
        sh = Image.new("RGB", (1290, sum(r.height + 6 for r in rows)), "white"); y = 0
        for r in rows: sh.paste(r, (0, y)); y += r.height + 6
        out = os.path.join(proj, "review", "fix_sheet.png"); sh.save(out); return out


def main(proj, use_qc=False):
    proj = os.path.abspath(proj); t0 = time.time()
    fb = os.path.join(proj, "FEEDBACK.txt")
    lines = open(fb).read().splitlines() if os.path.exists(fb) else []
    notes = [(i, l.strip()) for i, l in enumerate(lines) if l.strip() and not l.strip().startswith(("#", "[done]", "[skip]"))]
    pr = Project(proj); cache = Cache(proj); results = {}
    ctx = _context(pr.script, pr.props, pr)
    for i, note in notes:
        try:
            acts = plan(note, ctx)
        except Exception as e:
            acts = []; print("plan failed:", e)
        res = []
        for a in acts:
            try: r = apply_action(pr, cache, a, note)
            except Exception as e: r = None; print("action failed:", a, e)
            res.append(r or f"could not apply {a.get('action')}")
            print(f"• {note}\n    -> {a}\n    => {r}")
        results[i] = res
    if use_qc:
        rp = os.path.join(proj, "review", "qc_report.json")
        if os.path.exists(rp):
            F = [Finding(**{k: v for k, v in d.items() if k in Finding.__dataclass_fields__}) for d in json.load(open(rp))["findings"]]
            for f, r in FX.apply(pr, cache, [f for f in F if f.fix and f.status == "open"], load_config(proj)):
                if r: print(f"• QC: {f.description[:70]} => {r}")
    llm.unload()
    # snapshot, quick rebuild (cached everything + segmented master), scoped QC, before/after sheet
    bdir = os.path.join(proj, "work", "fix_before"); os.makedirs(bdir, exist_ok=True)
    if os.path.exists(pr.video): shutil.copy2(pr.video, os.path.join(bdir, "prev.mp4"))
    before = scene_state(proj)
    topic = open(os.path.join(proj, "TOPIC")).read().strip()
    PL.make_video(topic, approve=True, run_qc=False, review=False)
    touched = {k for k, v in scene_state(proj).items() if v != before.get(k)}
    log(proj, f"fastfix: rebuilt, touched scenes {sorted(touched)}")
    ok, scores, F = recheck(proj, touched) if touched else (None, None, None)
    sheet = _sheet(proj, bdir, touched, Project(proj)) if touched else None
    if touched and not os.path.exists(os.path.join(proj, "NO_REEL")):     # keep the Instagram Reel in sync with the fixed video
        from . import reel
        try: reel.make(proj)
        except Exception as e: print("reel rebuild failed:", e)
    for i, res in results.items():           # mark notes handled
        lines[i] = f"[done] {lines[i].strip()}   -> {'; '.join(res)[:200]}"
    if results: open(fb, "w").write("\n".join(lines) + "\n")
    print(f"\nfastfix done in {(time.time() - t0) / 60:.1f} min · touched {sorted(touched) or 'nothing'} · "
          f"QC {'PASS' if ok else 'FAIL' if ok is not None else 'not re-run'} {scores or ''}\nbefore/after: {sheet}")


if __name__ == "__main__":
    main(sys.argv[1], "--qc" in sys.argv)
