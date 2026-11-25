"""Find small stray colour blobs (generation artifacts) in keyframes: python tools/shorts/blobscan.py <keyframes dir> [out.jpg]"""
import cv2, numpy as np, os, sys
D = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else None; crops = []
RANGES = {"purple": ((128, 90, 70), (165, 255, 255)), "green": ((30, 70, 60), (55, 255, 230))}
for f in sorted(os.listdir(D)):
    if not f.endswith(".png"): continue
    im = cv2.imread(os.path.join(D, f)); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); H, W = im.shape[:2]
    for name, (lo, hi) in RANGES.items():
        m = cv2.inRange(hsv, np.array(lo), np.array(hi)); m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        for k in range(1, n):
            x, y, w, h, a = st[k]
            if not (40 <= a <= 0.0015 * H * W) or max(w, h) > 3 * min(w, h) or a < 0.55 * w * h: continue   # small, compact, filled
            ring = cv2.dilate((lab == k).astype(np.uint8), np.ones((15, 15), np.uint8)) - (lab == k).astype(np.uint8)
            if (m[ring > 0] > 0).mean() > 0.15: continue                                           # part of a bigger same-colour area
            print(f"{f[:-4]:6s} {name:6s} at ({x + w // 2},{y + h // 2}) area {a}")
            if out:
                c = im[max(0, y - 60):y + h + 60, max(0, x - 60):x + w + 60].copy(); c = cv2.resize(c, (160, 160))
                crops.append(cv2.putText(c, f"{f[:-4]} {name[0]}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2))
if out and crops:
    rows = [np.hstack(crops[i:i + 10] + [np.zeros_like(crops[0])] * (10 - len(crops[i:i + 10]))) for i in range(0, len(crops), 10)]
    cv2.imwrite(out, np.vstack(rows))
