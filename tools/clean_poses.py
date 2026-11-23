"""Run assets.clean_face_spots on every pose of the given library characters (default: Ryan and Maya in all outfits)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import assets, config as C
dirs = sys.argv[1:] or [d for d in os.listdir(C.CHAR_LIB) if d.split("_o_")[0] in ("benny", "maya") and "_old_" not in d]
det = assets._detector()
for d in sorted(dirs):
    for f in sorted(glob.glob(os.path.join(C.CHAR_LIB, d, "poses", "*.png"))):
        if any(t in f for t in ("_mid", "_open", "_nomouth")): continue
        n = assets.clean_face_spots(f, det)
        if n: print(f"cleaned {n:5d} px  {d}/{os.path.basename(f)}", flush=True)
print("DONE", flush=True)
