"""The image model's stray colour specks (small isolated olive-green / purple dots): detect and inpaint, per image or per video frame.
Shared by promo.py (per-frame Reel cleaning) and clipclean.py (cleaning finished animated clips in place)."""
import cv2, numpy as np

RANGES = [((128, 90, 70), (165, 255, 255)), ((30, 70, 60), (55, 255, 230))]


def despeck(fr):
    """Return the frame with small isolated green / purple blobs inpainted (thresholds scale with frame size)."""
    H, W = fr.shape[:2]; k = W * H / (1920 * 1080)
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV); mask = None
    for lo, hi in RANGES:
        m = cv2.morphologyEx(cv2.inRange(hsv, np.array(lo), np.array(hi)), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if not (max(12, 40 * k) <= a <= 0.0015 * W * H) or max(w, h) > 3 * min(w, h) or a < 0.55 * w * h: continue
            x0, y0 = max(0, x - 8), max(0, y - 8); sub = m[y0:y + h + 8, x0:x + w + 8]; blob = (lab[y0:y + h + 8, x0:x + w + 8] == i)
            if (sub[~blob] > 0).mean() > 0.15: continue                       # part of a bigger same-colour area: real, leave it
            if mask is None: mask = np.zeros(m.shape, np.uint8)
            cv2.rectangle(mask, (x - 4, y - 4), (x + w + 4, y + h + 4), 255, -1)
    return cv2.inpaint(fr, mask, 6, cv2.INPAINT_TELEA) if mask is not None else fr
