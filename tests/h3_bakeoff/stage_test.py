import json, sys, time
sys.path.insert(0, ".")
from studio.h3stage import stage_h3
proj = "projects/ryan-blackout-rumor-reel"
sc = json.load(open(f"{proj}/script.json"))
sc["scenes"] = [s for s in sc["scenes"] if s["id"] in sys.argv[1].split(",")]
print("envs with _file:", [e["id"] for e in sc["environments"] if e.get("_file")], flush=True)
t = time.time(); print("done:", stage_h3(proj, sc), f"{time.time() - t:.0f}s", flush=True)
