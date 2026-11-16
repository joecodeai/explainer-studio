"""Draw wardrobe outfits for Benny/Maya: turnaround views (front/side/back) + animation poses, from the character's base drawing.

  .venv/bin/python tools/build_wardrobe.py                         # base designs + every outfit used by an episode script given with --script
  .venv/bin/python tools/build_wardrobe.py benny:evening maya:denim  # specific outfits ("signature" = the base design)
  .venv/bin/python tools/build_wardrobe.py --script projects/<p>/script.json
Also syncs library/wardrobe.json into library/show.json (cast[].outfits) so episodes can use every outfit by name.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import assets, comfy, config as C

POSES = ["neutral", "talk", "side_talk", "side_listen", "surprised", "happy", "worried", "thinking", "shrug", "point",
         "side_view", "back_view", "walking", "sitting"]


def sync():
    wd = json.load(open(os.path.join(C.LIBRARY, "wardrobe.json")))
    f = os.path.join(C.LIBRARY, "show.json"); sh = json.load(open(f))
    for c in sh["cast"]:
        who = "the young man with curly hair" if c["id"] == "benny" else "the woman with long wavy hair"
        c["outfits"] = {o["outfit"]: {"desc": o["desc"], "tag": f"{who} in the {o['desc'].split(',')[0].split(' over ')[0].replace('a ', '', 1)}"}
                        for o in wd["outfits"] if o["char"] == c["id"] and o["outfit"] != "signature"}
    json.dump(sh, open(f, "w"), indent=1)
    return sh


def main(args):
    sh = sync(); cast = {c["id"]: dict(c, style=sh["style"]) for c in sh["cast"]}
    want = []
    if args and args[0] == "--script":
        sc = json.load(open(args[1]))
        want = sorted({(c["char"], c.get("outfit") or "signature") for s in sc["scenes"] for c in s.get("cast", []) if c["char"] in cast})
    else:
        want = [tuple(a.split(":")) for a in args] or [(cid, "signature") for cid in cast]
    for cid, o in want:
        if o == "signature": assets.build_character(cast[cid], POSES)
        else: assets.build_outfit(cast[cid], o, POSES)
        print("built", cid, o, flush=True)
    comfy.free(); print("DONE", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
