"""Remove the image model's stray colour specks (small isolated olive-green / purple dots) from keyframes by inpainting.
  python tools/shorts/despeckle.py <keyframes dir> <id,id,...> [--skip id:x,y;id:x,y]
Only the listed keyframes are touched (review tools/shorts/blobscan.py output first: real leaves, trees and drinks must not be listed).
Originals are kept in <dir>/_orig/. A before/after sheet goes to <dir>/_orig/despeckle_check.jpg."""
import cv2, numpy as np, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
D, ids = sys.argv[1], [i for i in sys.argv[2].split(",") if i]
skip = {}
if "--skip" in sys.argv:
    for t in sys.argv[sys.argv.index("--skip") + 1].split(";"):
        k, xy = t.split(":"); skip.setdefault(k, []).append(tuple(int(v) for v in xy.split(",")))
RANGES = [((128, 90, 70), (165, 255, 255)), ((30, 70, 60), (55, 255, 230))]
os.makedirs(f"{D}/_orig", exist_ok=True); sheet = []
for i in ids:
    p = f"{D}/{i}.png"; o = f"{D}/_orig/{i}.png"
    if not os.path.exists(o): shutil.copy(p, o)
    im = cv2.imread(o); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); H, W = im.shape[:2]; mask = np.zeros((H, W), np.uint8); boxes = []
    for lo, hi in RANGES:
        m = cv2.morphologyEx(cv2.inRange(hsv, np.array(lo), np.array(hi)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        for k in range(1, n):
            x, y, w, h, a = st[k]
            if not (40 <= a <= 0.0015 * H * W) or max(w, h) > 3 * min(w, h) or a < 0.55 * w * h: continue
            blob = (lab == k).astype(np.uint8); ring = cv2.dilate(blob, np.ones((15, 15), np.uint8)) - blob
            if (m[ring > 0] > 0).mean() > 0.15: continue
            if any(abs(x + w // 2 - sx) < 25 and abs(y + h // 2 - sy) < 25 for sx, sy in skip.get(i, [])): continue
            mask |= cv2.dilate(blob, np.ones((7, 7), np.uint8)); boxes.append((x, y, w, h))
    # the specks have soft halos: grow each mask a little more, then inpaint from the surrounding flat colour
    out = cv2.inpaint(im, cv2.dilate(mask, np.ones((5, 5), np.uint8)), 6, cv2.INPAINT_TELEA) if boxes else im
    cv2.imwrite(p, out); print(f"{i}: {len(boxes)} specks removed", flush=True)
    for x, y, w, h in boxes[:6]:
        c = lambda img: cv2.resize(img[max(0, y - 50):y + h + 50, max(0, x - 50):x + w + 50], (140, 140))
        sheet.append(cv2.putText(np.hstack([c(im), c(out)]), i, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2))
if sheet:
    rows = [np.hstack(sheet[k:k + 6] + [np.zeros_like(sheet[0])] * (6 - len(sheet[k:k + 6]))) for k in range(0, len(sheet), 6)]
    cv2.imwrite(f"{D}/_orig/despeckle_check.jpg", np.vstack(rows))
