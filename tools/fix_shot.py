"""Re-render ONLY the named H3 shots of a finished video, then re-assemble (everything else stays exactly as it is).

  python tools/fix_shot.py projects/<slug> <scene> <shot> [<shot> ...]      e.g.  ... projects/ryan-pattinson-jobs-reel s03 3
  python tools/fix_shot.py projects/<slug> s01:2,3 s03:1,2,3              several scenes in one run

Shot numbers are the `line` values in talk/ANIMATION_QC.json. Shots that continue the fixed shot's take are re-rendered too (so the
take stays continuous). Works by un-locking them in talk/h3/accepted.json and re-running the (cached) pipeline.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from studio import h3stage as H
from studio.pipeline import _j, TAIL


def shot_list(proj, sc):
    envs = {e["id"]: e for e in sc["environments"]}
    out, prev = [], None
    for s in sc["scenes"]:
        if s["kind"] != "stage" or not s.get("cast") or not _j(f"{proj}/audio/{s['id']}.lines.json"): continue
        cast = s["cast"][:2]; take = (s["environment"], tuple((c["char"], c.get("outfit")) for c in cast))
        for sh in H.compile_shots(s, _j(f"{proj}/audio/{s['id']}.lines.json"), s["_dur"] + TAIL + 2.6, [c["char"] for c in cast]):
            sh.update(scene=s["id"], take=take); sh["cont"] = bool(prev and prev["take"] == take and prev["setup"] == sh["setup"])
            sh["acc"] = H.acc_key(sh); out.append(sh); prev = sh
    return out


def main(proj, targets):
    sc = _j(f"{proj}/script.json")
    for s in sc["scenes"]:                         # scene durations come from the voice timing
        ln = _j(f"{proj}/audio/{s['id']}.lines.json")
        s["_dur"] = max(ln[-1]["end"] if ln else 0.0, float(s.get("hold") or 0))
    shots = shot_list(proj, sc)
    reg_p = f"{proj}/talk/h3/accepted.json"; reg = _j(reg_p) or {}
    if not reg:                                    # video made before the registry existed: seed it from the manifests
        qc = {(r["scene"], r["line"]): r for r in _j(f"{proj}/talk/ANIMATION_QC.json") or []}
        for s_id in dict.fromkeys(x["scene"] for x in shots):
            man = _j(f"{proj}/talk/{s_id}.json") or []
            for x in [y for y in shots if y["scene"] == s_id]:
                if x["k"] < len(man):
                    f = man[x["k"]]["video"]; r = qc.get((s_id, x["k"]), {})
                    reg[x["acc"]] = {"raw": f.replace("_1080.mp4", ".mp4"), "final": f, "qc": {"findings": r.get("findings", []), "ok": r.get("ok", True), "score": 0}}
    drop = []
    for i, x in enumerate(shots):
        if (x["scene"], x["k"]) in targets:
            drop.append(i); j = i + 1
            while j < len(shots) and shots[j]["cont"]: drop.append(j); j += 1
    ch_p = f"{proj}/talk/h3/chosen_attempts.json"; ch = _j(ch_p) or {}
    for i in sorted(set(drop)):
        reg.pop(shots[i]["acc"], None); print("re-render:", shots[i]["scene"], "#", shots[i]["k"], shots[i]["setup"])
        for k in [k for k in ch if k.startswith(f"{shots[i]['scene']}|{shots[i]['k']}|")]:
            ch[k] = int(ch[k]) + 1                 # next attempt = new seed; otherwise the identical cached clip comes back
    _j(reg_p, reg); _j(ch_p, ch)
    topic = open(f"{proj}/TOPIC").read().strip()
    subprocess.run([sys.executable, "make_video.py", topic, "--approve"], cwd=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."), check=True)


if __name__ == "__main__":
    a = sys.argv[2:]
    if any(":" in x for x in a):
        t = {(sc_, int(k)) for x in a for sc_, ks in [x.split(":")] for k in ks.split(",")}
    else:
        t = {(a[0], int(k)) for k in a[1:]}
    main(os.path.abspath(sys.argv[1]), t)
