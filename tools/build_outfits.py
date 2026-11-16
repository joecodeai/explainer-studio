"""Build every outfit in library/show.json for the recurring cast (same face/hair, different clothes)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import assets, comfy, config as C
POSES = ["neutral", "talk", "side_talk", "side_listen", "surprised", "happy", "worried", "thinking", "shrug", "point"]
show = json.load(open(os.path.join(C.LIBRARY, "show.json")))
for c in show["cast"]:
    for o in c.get("outfits", {}):
        assets.build_outfit(dict(c, style=show["style"]), o, POSES); print("built", c["id"], o, flush=True)
comfy.free()
