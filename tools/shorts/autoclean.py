"""Automatic removal of the image model's stray green / purple specks and smudges (2026-11-27), run on every new keyframe by build.py.
Only blobs that sit on SKIN (palms, faces) or on a FLAT plain surface are inpainted; blobs inside green areas (plants, banknotes,
Maya's olive shirt) or busy texture are left alone.  CLI check: python tools/shorts/autoclean.py <png|dir> [--dry]"""
import os, shutil, sys
import cv2, numpy as np

GREEN = ((35, 45, 60), (72, 215, 235))                 # minty green specks (OpenCV hue 0-180); not teal screens, not lit neon buttons
PURPLE = ((125, 70, 60), (165, 255, 255))
GREENISH = ((25, 40, 30), (95, 255, 255))              # anything green-ish, incl. olive (to recognise plants / shirts / notes)


def _skin(hsv):
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return (((h <= 25) | (h >= 170)) & (s >= 45) & (s <= 210) & (v >= 90))   # not pale paper / cream walls


def find(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); H, W = im.shape[:2]; skin = _skin(hsv)
    greenish = cv2.inRange(hsv, np.array(GREENISH[0]), np.array(GREENISH[1])) > 0
    hits = np.zeros((H, W), np.uint8); found = []
    for name, (lo, hi) in (("green", GREEN), ("purple", PURPLE)):
        m = cv2.morphologyEx(cv2.inRange(hsv, np.array(lo), np.array(hi)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        for k in range(1, n):
            x, y, w, h, a = st[k]
            if not (25 <= a <= 0.006 * H * W): continue
            blob = (lab == k).astype(np.uint8)
            ring = (cv2.dilate(blob, np.ones((13, 13), np.uint8)) - cv2.dilate(blob, np.ones((3, 3), np.uint8))) > 0
            if not ring.any(): continue
            on_skin = skin[ring].mean() > 0.45
            green_ring = greenish[ring].mean() if name == "green" else (cv2.inRange(hsv, np.array(lo), np.array(hi)) > 0)[ring].mean()
            flat = im[ring].reshape(-1, 3).std(0).max() < 16
            if green_ring > 0.25 and not on_skin: continue                # part of a plant, a banknote or the olive shirt
            box_fill = a / float(w * h)                                     # buttons / icons are solid rectangles; specks are blobby
            ok_skin = on_skin and skin[ring].mean() > 0.6 and a <= 2500
            ok_flat = flat and a <= 400
            bh = hsv[..., 0][blob > 0].mean(); bv = hsv[..., 2][blob > 0].mean(); bs = hsv[..., 1][blob > 0].mean()
            rv = np.median(hsv[..., 2][ring])
            cnt = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]; per = cv2.arcLength(max(cnt, key=cv2.contourArea), True)
            round_ = 4 * np.pi * a / max(per * per, 1) > 0.55
            sage = 36 <= bh <= 52 and 70 <= bs <= 175 and 95 <= bv <= 180          # the model's soft sage-green speck colour
            ok_dark = (name == "green" and sage and round_ and a <= 900 and rv < 110 and bv - rv > 35
                       and 3 < x and 3 < y and x + w < W - 3 and y + h < H - 3)  # dull round speck in dark hair / shadow
            if (ok_skin or ok_flat or ok_dark) and not (box_fill > 0.85 and a > 150):
                hits |= blob; found.append((name, int(cen[k][0]), int(cen[k][1]), int(a), "skin" if ok_skin else "flat" if ok_flat else "dark"))
    return hits, found


def clean(path, keep_dir=None, dry=False):
    im = cv2.imread(path)
    if im is None: return []
    hits, found = find(im)
    if found and not dry:
        if keep_dir:
            os.makedirs(keep_dir, exist_ok=True); shutil.copy(path, os.path.join(keep_dir, os.path.basename(path)[:-4] + "_raw.png"))
        mask = cv2.dilate(hits * 255, np.ones((7, 7), np.uint8))
        cv2.imwrite(path, cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA))
    return found


if __name__ == "__main__":
    tgt, dry = sys.argv[1], "--dry" in sys.argv
    files = [os.path.join(tgt, f) for f in sorted(os.listdir(tgt)) if f.endswith(".png")] if os.path.isdir(tgt) else [tgt]
    for f in files:
        r = clean(f, dry=dry)
        if r: print(os.path.basename(f), r)
