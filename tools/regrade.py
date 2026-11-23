"""Re-grade a finished video's H3 shots (colour lock to each shot's source frame) from the existing raw clips — no H3 re-render —
then re-assemble. For videos finished before the colour lock existed, or after changing the grading.

  python tools/regrade.py projects/<slug>
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from studio import h3stage as H
from studio.pipeline import _j
from fix_shot import shot_list


def main(proj):
    sc = _j(f"{proj}/script.json")
    for s in sc["scenes"]:
        ln = _j(f"{proj}/audio/{s['id']}.lines.json")
        s["_dur"] = max(ln[-1]["end"] if ln else 0.0, float(s.get("hold") or 0))
    envs = {e["id"]: e for e in sc["environments"]}; scenes = {s["id"]: s for s in sc["scenes"]}
    shots = shot_list(proj, sc); reg_p = f"{proj}/talk/h3/accepted.json"; reg = _j(reg_p)
    work = f"{proj}/work/h3"
    for i, sh in enumerate(shots):
        e = reg[sh["acc"]]; s = scenes[sh["scene"]]
        sh.update(raw=e["raw"], cast=s["cast"][:2], size=H.HERO_SIZE if i == 0 else H.SIZE)
        base = f"{work}/{sh['scene']}_{sh['k']}_rg"; dur = sh["b"] - sh["a"]
        if sh["cont"]:
            p = shots[i - 1]; kf = base + "_from_prev.png"
            H._tail(p["final"], round((p["b"] - p["a"]) * 24), base + "_from_prev.mp4", kf)
        else:
            kf = H._from_state(shots, i, base) or H._keyframe(envs[s["environment"]]["_file"], sh["cast"], sh["setup"], sh["size"], work, sh["scene"])
        out = e["raw"].replace(".mp4", "_1080c.mp4")
        H._finish(e["raw"], dur, out, fresh=not sh["cont"], ref=kf)
        sh["final"] = out; e["final"] = out
        print("regraded", sh["scene"], sh["k"], sh["setup"])
    _j(reg_p, reg)
    for sid in dict.fromkeys(x["scene"] for x in shots):
        mine = [x for x in shots if x["scene"] == sid]
        _j(f"{proj}/talk/{sid}.json", [{"video": x["final"], "start": x["a"], "end": x["b"]} for x in mine])
        for f in (f"{proj}/renders/{sid}.mp4", f"{proj}/renders/{sid}.mp4.hash"):
            if os.path.exists(f): os.remove(f)
    rep = _j(f"{proj}/talk/ANIMATION_QC.json") or []
    fin = {(x["scene"], x["k"]): x["final"] for x in shots}
    for r in rep: r["video"] = fin.get((r["scene"], r["line"]), r["video"])
    _j(f"{proj}/talk/ANIMATION_QC.json", rep)
    topic = open(f"{proj}/TOPIC").read().strip()
    subprocess.run([sys.executable, "make_video.py", topic, "--approve"], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), check=True)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
