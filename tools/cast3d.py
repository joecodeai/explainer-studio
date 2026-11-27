"""Locked 3D cast + set plates (2026-11-27) -> library/show_refs3d/. One run; every 3D topic then uses these exact references.
Maya comes from the owner's pick (VIDEOS/_MAYA 3D OPTIONS, option 1, take 411, green palm smudge cleaned). Others are restyled from their
existing 2D references. Poses keep hands relaxed (open raised palms are where the image model paints green smudges).
  .venv/bin/python tools/cast3d.py [name,name]   (existing files are kept; delete one to redo it)"""
import os, shutil, sys
sys.argv = ["build.py", "atm"]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shorts"))
import build as B  # noqa: E402  (chdir's to the repo root)
import autoclean  # noqa: E402
from topics import show3d as S  # noqa: E402

D = "library/show_refs3d"; os.makedirs(D, exist_ok=True)
MAYA_PICK = "VIDEOS/_MAYA 3D OPTIONS/_frames/1_411_clean.png"
BG = " Plain flat light warm-grey studio background, nothing else in the image. Exactly one character."
FULL = "Full-body character reference, standing facing camera in a relaxed neutral pose, arms relaxed at the sides, hands relaxed. "
FACE = "Head-and-shoulders portrait reference facing camera, friendly expression, both hands out of frame. "
OLD = {"ryan": ["library/show_refs/benny_front.png", "library/show_refs/benny_face.png"],
       "brayden": ["projects/short-atm/refs/crop_brayden.png"], "gerald": ["projects/short-atm/refs/crop_gerald.png"]}
JOBS = {   # name: (prompt, refs, w, h, seed)
    "maya": (FULL + S.MAYA.replace("waist-up, ", "") + "dark jeans, white trainers." + BG, [MAYA_PICK], 768, 1344, 11),
    "maya_face": (FACE + S.MAYA.replace("waist-up, ", "") + BG, [MAYA_PICK], 1024, 1024, 12),
    "ryan": (FULL + S.RYAN.replace("waist-up, ", "") + "dark jeans, white trainers." + BG, OLD["ryan"], 768, 1344, 13),
    "ryan_face": (FACE + S.RYAN.replace("waist-up, ", "") + BG, OLD["ryan"], 1024, 1024, 14),
    "brayden": (FULL + S.BRAY.replace("waist-up, ", "") + "dark trousers, white trainers, muscular build." + BG, OLD["brayden"], 768, 1344, 15),
    "gerald": (FULL + S.GER.replace("waist-up, ", "") + "grey trousers, brown shoes, kind gentle face." + BG, OLD["gerald"], 768, 1344, 16),
}
T2I = {    # no-reference jobs: the fox and the set plates
    "fox": ("Full-body character reference: a small cute stylised orange fox with a cream chest, white-tipped bushy tail, dark paws and big "
            "expressive amber eyes, sitting facing camera, clever and mischievous." + BG.replace(" Exactly one character.", ""), 1024, 1024, 17),
    "set_studio": ("A bright cosy presenter's studio, wide shot: honey-wood desk, warm desk lamp, a tall bookshelf with books and small plants, a "
                   "potted plant, a big sunny window behind the desk with soft greenery outside, warm cream walls.", 1344, 768, 21),
    "set_office": ("A small softly lit office: an office chair facing camera, a side table with a box of tissues, a framed child's drawing of a "
                   "smiling sun on a cream wall, a notepad on the chair.", 1344, 768, 22),
    "set_kitchen": ("A small bright modern kitchen: cream cabinets, honey-wood worktop, a kettle, a small round table with two chairs, a window "
                    "with morning light.", 1344, 768, 23),
    "set_flat": ("A bare white empty flat: plain white walls, pale wooden floor, one bare light bulb hanging from the ceiling, a front door, "
                 "nothing else.", 1344, 768, 24),
    "set_street": ("A city street at night: a cash machine set into a red brick wall, a warm streetlight, wet pavement with soft reflections, "
                   "distant lit windows, soft blue ambient night light.", 1344, 768, 25),
}
only = sys.argv[1].split(",") if len(sys.argv) > 1 and not sys.argv[1].endswith(".py") else None
only = [a for a in (os.environ.get("ONLY", "").split(",")) if a] or None
B.h3.free(); B.comfy.start()
for name, (prompt, refs, w, h, seed) in JOBS.items():
    p = f"{D}/{name}.png"
    if os.path.exists(p) or (only and name not in only): continue
    got = B.imagegen.edit(f"{S.STYLE} {prompt}", refs, D, name, w, h, seed=seed, fixed_size=True)
    shutil.move(got, p); print("cast", p, autoclean.clean(p, keep_dir=f"{D}/_raw"), flush=True)
for name, (prompt, w, h, seed) in T2I.items():
    p = f"{D}/{name}.png"
    if os.path.exists(p) or (only and name not in only): continue
    style = S.ENV_STYLE if name.startswith("set_") else S.STYLE
    got = B.imagegen.t2i(f"{style} {prompt}" + (" An empty room with nobody in it." + B.NO_PEOPLE if name.startswith("set_") else ""),
                         D, name, w, h, seed=seed + 100)
    shutil.move(got, p); print("cast", p, autoclean.clean(p, keep_dir=f"{D}/_raw"), flush=True)
B.comfy.free()
