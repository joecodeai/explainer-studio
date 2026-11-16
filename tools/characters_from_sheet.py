"""Rebuild the show's recurring characters from the user's character sheet (library/show_refs/benny_maya_sheet.png).

The sheet (1536x1024) has Benny on the top half and Maya on the bottom half: a big portrait, a front/side/back turnaround,
an expression grid and "In Action" panels. We crop the front full-body view + the portrait of each character and ask the
image editor to redraw that exact character as a clean full-body base on a transparent background, then build every pose
from that base (assets.build_character). The old library folders are moved aside, not deleted.

  .venv/bin/python tools/characters_from_sheet.py [sheet.png]
"""
import json, os, shutil, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image
from studio import assets, comfy, imagegen, config as C

SHEET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(C.LIBRARY, "show_refs", "benny_maya_sheet.png")
# crop boxes as fractions of the sheet (x0, y0, x1, y1)
BOX = {"benny": {"front": (0.305, 0.01, 0.39, 0.48), "portrait": (0.08, 0.02, 0.31, 0.50), "face": (0.56, 0.02, 0.66, 0.17)},
       "maya": {"front": (0.30, 0.51, 0.385, 0.99), "portrait": (0.08, 0.51, 0.31, 0.99), "face": (0.555, 0.52, 0.66, 0.68)}}
POSES = ["neutral", "talk", "side_talk", "side_listen", "surprised", "happy", "worried", "thinking", "shrug", "point", "facepalm"]


def crops(cid, out_dir):
    im = Image.open(SHEET).convert("RGB"); W, H = im.size; paths = []
    for k, (x0, y0, x1, y1) in BOX[cid].items():
        p = os.path.join(out_dir, f"{cid}_{k}.png")
        im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))).save(p); paths.append(p)
    return paths


def main():
    show = json.load(open(os.path.join(C.LIBRARY, "show.json")))
    refdir = os.path.join(C.LIBRARY, "show_refs"); os.makedirs(refdir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M")
    for c in show["cast"]:
        cid = c["id"]; d = os.path.join(C.CHAR_LIB, cid)
        if os.path.exists(d): shutil.move(d, d + f"_old_{stamp}")          # keep the previous design
        os.makedirs(os.path.join(d, "_tmp"), exist_ok=True); os.makedirs(os.path.join(d, "poses"), exist_ok=True)
        refs = crops(cid, refdir)
        p = imagegen.edit(f"Redraw the exact same character shown in these reference images — identical face, hairstyle, hair colour, "
                          f"outfit, accessories, colours and art style ({show['style']}). {c['look']}. Full body, standing relaxed, facing "
                          f"the viewer, arms relaxed at the sides, small closed-mouth smile, MOUTH CLOSED. Isolated on a plain white background, "
                          f"no text, no other people.", refs, os.path.join(d, "_tmp"), "base", 896, 1344, seed=1234, fixed_size=True)
        p = assets._ensure_alpha(p, os.path.join(d, "_tmp"), "base")
        assets._crop(Image.open(p).convert("RGBA")).save(os.path.join(d, "base.png"))
        cc = dict(c, style=show["style"])
        assets.build_character(cc, POSES)
        print("built", cid, flush=True)
    comfy.free()


if __name__ == "__main__":
    main()
