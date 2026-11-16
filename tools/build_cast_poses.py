"""Build poses for the recurring cast's base designs, then every outfit (library/show.json)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import assets, comfy, config as C
POSES = ["neutral", "talk", "side_talk", "side_listen", "surprised", "happy", "worried", "thinking", "shrug", "point", "facepalm"]
show = json.load(open(os.path.join(C.LIBRARY, "show.json")))
only = set(sys.argv[1:])
for c in show["cast"]:
    cc = dict(c, style=show["style"])
    if not only or c["id"] in only: assets.build_character(cc, POSES); print("poses", c["id"], flush=True)
for c in show["cast"]:
    for o in c.get("outfits", {}):
        assets.build_outfit(dict(c, style=show["style"]), o, POSES[:-1]); print("outfit", c["id"], o, flush=True)
comfy.free(); print("DONE", flush=True)
